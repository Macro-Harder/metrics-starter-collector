"""Module 1: shell reader, the thin shell.

Parses the command line arguments in __main__, validates the root,
walks the root once in sorted relative path order, reads each
discovered piece once, enforces the limits in minimal form, builds
one CapturedRead, and delivers the finished report to stdout or to
the one operator named file. This is the only module that touches
the filesystem besides the Inventory classification it calls.
"""
import os
import re
from pathlib import Path

from metrics_starter_collector import inventory
from metrics_starter_collector.derivation_core import (
    CLS_DECISION_QUEUE, CLS_GATE_ADJUDICATION, CLS_GATE_RECORD,
    CLS_GATE_RULING, CLS_METRICS_PAGE, CLS_METRICS_SINGLE, CLS_PATH_LEDGER,
    CLS_REGATE_RECORD, CLS_STEP_RECORD, CLS_TIER_RECORD, CapturedRead,
    Piece)

FILE_LIMIT = 1000000
TREE_BYTE_LIMIT = 25000000
TREE_FILE_LIMIT = 2000
LINE_LIMIT = 65536
WALK_BOUND = 10000


class UnreadableInputError(Exception):
    """The shell cannot produce a CapturedRead at all for this root."""


class UsageError(Exception):
    """A command line or delivery form the grammar refuses."""


_FULL_TS = re.compile(r"(\d{4}-\d{2}-\d{2})[ T](\d{2}):(\d{2})"
                      r"(?::(\d{2}))?(?:\s*(CST|UTC|EST|EDT|CDT))?")
_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _latest_timestamp(texts):
    best = None
    best_key = None
    for text in texts:
        for m in _FULL_TS.finditer(text):
            key = (m.group(1), m.group(2), m.group(3),
                   m.group(4) or "00")
            if best_key is None or key > best_key:
                best_key = key
                best = m.group(0)
        for m in _DATE.finditer(text):
            key = (m.group(1), "00", "00", "00")
            if best_key is None or key > best_key:
                best_key = key
                best = m.group(1)
    return best


def _read_piece_file(path):
    """Read one file once. Return (size, text, quality, reason)."""
    try:
        data = path.read_bytes()
    except OSError as exc:
        return 0, None, "unreadable", \
            "unreadable-piece: unreadable: %s" % exc
    size = len(data)
    if size > FILE_LIMIT:
        return size, None, "over limit", \
            "over limit: file limit %d bytes crossed" % FILE_LIMIT
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return size, None, "malformed", "malformed: not valid UTF-8"
    for line in text.splitlines():
        if len(line.encode("utf-8")) > LINE_LIMIT:
            return size, None, "over limit", \
                "over limit: line limit %d bytes crossed" % LINE_LIMIT
    return size, text, None, None


def _split_page_order(text, rel):
    if text:
        m = re.search(r"Page order:\s*(\d+)", text)
        if m:
            return (0, int(m.group(1)), rel)
    return (1, 0, rel)


def _assemble_metrics(pieces):
    """Assemble the metrics record in its governing physical form."""
    singles = [p for p in pieces if p.record_class == CLS_METRICS_SINGLE
               and p.text is not None]
    if singles:
        return singles[0].text, singles[0].paths[0]
    pages = [p for p in pieces if p.record_class == CLS_METRICS_PAGE
             and p.text is not None]
    if not pages:
        return None, None
    pages.sort(key=lambda p: _split_page_order(p.text, p.paths[0]))
    return "\n".join(p.text for p in pages), pages[0].paths[0]


def _definitions_version(assembled):
    if not assembled:
        return None
    m = re.search(r"Definitions version:\s*(.+)", assembled)
    if m:
        return m.group(1).strip()
    return None


def _build_identity(pieces, assembled):
    if assembled:
        m = re.search(r"^#\s*Build metrics record:\s*(.+)$", assembled, re.M)
        if m:
            return m.group(1).strip()
        m = re.search(r"^- Project:\s*(.+)$", assembled, re.M)
        if m:
            return m.group(1).strip()
    for p in pieces:
        if p.text and p.record_class == CLS_STEP_RECORD:
            m = re.search(r"Build:\s*(.+)\.", p.text)
            if m:
                return m.group(1).strip()
    return None


def capture_read(root):
    """Walk the root once and build the one CapturedRead for the run."""
    root_path = Path(root)
    if not root_path.exists() or not root_path.is_dir():
        raise UnreadableInputError(
            "capture the record tree: root %s: not a readable directory"
            % (root,))
    root_resolved = root_path.resolve()
    entries = []
    walk_note = None
    count = 0
    for dirpath, dirnames, filenames in os.walk(str(root_path)):
        dirnames.sort()
        for name in sorted(dirnames) + sorted(filenames):
            count += 1
            if count > WALK_BOUND:
                walk_note = ("the whole walk bound of %d entries was "
                             "reached and entries beyond it were not "
                             "visited" % WALK_BOUND)
                break
            full = Path(dirpath) / name
            rel = str(full.relative_to(root_path))
            if full.is_symlink():
                try:
                    target = full.resolve()
                except OSError:
                    continue
                if target != root_resolved and \
                        root_resolved not in target.parents:
                    continue
            if full.is_file():
                entries.append(rel)
            elif full.is_dir() and \
                    inventory.classify(rel) is not None:
                entries.append(rel)
        if walk_note:
            break
    entries.sort()
    alias_map = {}
    by_target = {}
    for rel in entries:
        try:
            key = str((root_path / rel).resolve())
        except OSError:
            key = rel
        by_target.setdefault(key, []).append(rel)
    canonical_entries = []
    for key in by_target:
        rels_sorted = sorted(by_target[key])
        canonical = rels_sorted[0]
        for candidate in rels_sorted:
            if not (root_path / candidate).is_symlink():
                canonical = candidate
                break
        alias_map[canonical] = tuple(rels_sorted)
        canonical_entries.append(canonical)
    entries = sorted(canonical_entries)
    classified = []
    for rel in entries:
        found = inventory.classify(rel)
        note = None
        if found is None:
            note = inventory.near_match_note(rel)
        classified.append((rel, found, note))

    def stat_size(rel):
        full = root_path / rel
        try:
            if full.is_dir() and not full.is_symlink():
                return 0
            return full.stat().st_size
        except OSError:
            return 0

    tree_bytes = 0
    tree_files = 0
    cut_rels = []
    cut_kind = None
    last_visited = None
    cutting = False
    for rel, found, note in classified:
        if found is None and note is None:
            continue
        size = stat_size(rel)
        tree_files += 1
        tree_bytes += size
        if not cutting and (tree_bytes > TREE_BYTE_LIMIT or
                            tree_files > TREE_FILE_LIMIT):
            cutting = True
            crossed = []
            if tree_bytes > TREE_BYTE_LIMIT:
                crossed.append("tree byte limit %d bytes"
                               % TREE_BYTE_LIMIT)
            if tree_files > TREE_FILE_LIMIT:
                crossed.append("tree file limit %d files"
                               % TREE_FILE_LIMIT)
            cut_kind = " and ".join(crossed)
        if cutting:
            cut_rels.append(rel)
        else:
            last_visited = rel
    cut_set = set(cut_rels)
    raw = {}
    near = []
    for rel, found, note in classified:
        if found is None:
            if note is not None:
                near.append((rel, note))
            continue
        cls, step = found
        if rel in cut_set:
            size = stat_size(rel)
            text = None
            quality = "over limit"
            reason = ("not read: the %s was crossed, with a record "
                      "part total of %d bytes in %d files, and this "
                      "piece stands past the limit in walk order"
                      % (cut_kind, tree_bytes, tree_files))
        else:
            size, text, quality, reason = _read_piece_file(
                root_path / rel)
        ident = inventory.identity_for(cls, step, rel)
        raw.setdefault(ident, []).append(
            (rel, cls, step, size, text, quality, reason,
             alias_map.get(rel, (rel,))))
    pieces = []
    for ident in sorted(raw, key=lambda i: min(x[0] for x in raw[i])):
        group = sorted(raw[ident], key=lambda x: x[0])
        rel0, cls, step, size0, text0, quality0, reason0 = group[0][:7]
        paths = tuple(sorted({p for x in group for p in x[7]}))
        form = None
        if cls == CLS_METRICS_SINGLE:
            form = "single page form"
        elif cls == CLS_METRICS_PAGE:
            form = "split page form"
        if len(group) > 1:
            texts = {x[4] for x in group}
            if len(texts) == 1 and text0 is not None:
                pieces.append(Piece(ident, paths, cls, step, size0, text0,
                                    None, quality0, form_state=form))
            else:
                pieces.append(Piece(
                    ident, paths, cls, step, size0, None,
                    "not read in full: duplicate content disagreement "
                    "between the paths that yield this piece", quality0,
                    form_state=form))
            continue
        pieces.append(Piece(ident, paths, cls, step, size0, text0,
                            reason0, quality0, form_state=form))
    pieces.sort(key=lambda p: p.paths[0])
    assembled, single_path = _assemble_metrics(pieces)
    if single_path is None:
        singles = [p for p in pieces if p.record_class == CLS_METRICS_SINGLE]
        if singles:
            single_path = singles[0].paths[0]
    texts = [p.text for p in pieces if p.text is not None]
    latest = _latest_timestamp(texts)
    version = _definitions_version(assembled)
    identity = _build_identity(pieces, assembled)
    evidenced = sorted({p.step for p in pieces if p.step is not None and
                        p.record_class in (CLS_STEP_RECORD, CLS_GATE_RECORD,
                                           CLS_GATE_RULING,
                                           CLS_REGATE_RECORD,
                                           CLS_GATE_ADJUDICATION)})
    totals = {}
    per_step = (CLS_STEP_RECORD, CLS_GATE_RECORD, CLS_GATE_RULING,
                CLS_REGATE_RECORD, CLS_GATE_ADJUDICATION)
    per_build = (CLS_PATH_LEDGER, CLS_TIER_RECORD, CLS_METRICS_SINGLE,
                 CLS_DECISION_QUEUE)
    for p in pieces:
        entry = totals.setdefault(p.record_class,
                                  {"expected": 0, "found": 0,
                                   "not_found": 0, "not_yet_recordable": 0})
        entry["found"] += 1
    for cls, entry in totals.items():
        if cls in per_step:
            entry["expected"] = len(evidenced)
        elif cls in per_build:
            entry["expected"] = 1
        else:
            entry["expected"] = entry["found"]
        entry["not_found"] = max(0, entry["expected"] - entry["found"])
    return CapturedRead(root=str(root), pieces=pieces,
                        inventory_totals=totals, latest_timestamp=latest,
                        definitions_version=version,
                        build_identity=identity, near_matches=near,
                        assembled_metrics=assembled,
                        metrics_single_path=single_path,
                        walk_note=walk_note,
                        tree_bytes=tree_bytes, tree_files=tree_files,
                        tree_cut_paths=tuple(cut_rels),
                        tree_cut_kind=cut_kind,
                        tree_last_visited=last_visited,
                        tree_byte_limit=TREE_BYTE_LIMIT,
                        tree_file_limit=TREE_FILE_LIMIT)


def deliver_report(text, root, report_path):
    """Deliver the finished report to stdout or to the one named file."""
    import sys
    if report_path is None:
        try:
            sys.stdout.write(text)
            sys.stdout.flush()
        except (BrokenPipeError, OSError) as exc:
            raise UsageError(
                "deliver the report: destination standard output: %s"
                % (exc,))
        return
    destination = Path(report_path)
    root_resolved = Path(root).resolve()
    try:
        dest_resolved = destination.resolve()
    except OSError as exc:
        raise UsageError("deliver the report: destination %s: %s"
                         % (report_path, exc))
    if dest_resolved == root_resolved or \
            root_resolved in dest_resolved.parents:
        raise UsageError(
            "deliver the report: destination %s: the destination lies "
            "inside the tree read, which is refused" % (report_path,))
    parent = destination.parent
    if not parent.exists():
        raise UsageError(
            "deliver the report: destination %s: the parent directory "
            "does not stand" % (report_path,))
    # A destination that stands as something other than a plain file,
    # or a link to something other than a plain file, is written
    # through its own name, never replaced. Replacing such a name
    # would destroy the name itself and could report success where
    # the target cannot be written at all, as a link to a full device
    # shows. Writing through the name lets the operating system
    # failure stand, and the destination is left as it stood.
    write_through = False
    if destination.is_symlink():
        write_through = not dest_resolved.is_file()
    elif destination.exists() and not destination.is_file():
        write_through = True
    if write_through:
        try:
            with open(destination, "w", encoding="utf-8",
                      newline="\n") as handle:
                handle.write(text)
        except OSError as exc:
            raise UsageError("deliver the report: destination %s: %s"
                             % (report_path, exc))
        return
    # A link to a plain file delivers to the resolved file, so the
    # link itself stands. Any other plain destination delivers to
    # itself. Both go by way of a temporary file in the same
    # directory and a replace, so a failure leaves no partial file
    # and a prior file at the destination is left as it stood.
    target = dest_resolved if destination.is_symlink() else destination
    tmp = target.parent / (target.name + ".tmp-msc")
    try:
        tmp.write_text(text, encoding="utf-8", newline="\n")
        os.replace(str(tmp), str(target))
    except OSError as exc:
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass
        raise UsageError("deliver the report: destination %s: %s"
                         % (report_path, exc))
