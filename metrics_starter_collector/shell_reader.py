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
                      r"(?:\s*(CST|UTC|EST|EDT|CDT))?")
_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _latest_timestamp(texts):
    best = None
    best_key = None
    for text in texts:
        for m in _FULL_TS.finditer(text):
            key = (m.group(1), m.group(2))
            if best_key is None or key > best_key:
                best_key = key
                best = m.group(0)
        for m in _DATE.finditer(text):
            key = (m.group(1), "00:00")
            if best_key is None or key > best_key:
                best_key = key
                best = m.group(1)
    return best


def _read_piece_file(path):
    """Read one file once. Return (size, text, quality, reason)."""
    try:
        data = path.read_bytes()
    except OSError as exc:
        return 0, None, "unreadable", "unreadable: %s" % exc
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
    visited_targets = set()
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
                if str(target) in visited_targets:
                    continue
                visited_targets.add(str(target))
            if full.is_file():
                entries.append(rel)
        if walk_note:
            break
    entries.sort()
    raw = {}
    near = []
    for rel in entries:
        found = inventory.classify(rel)
        if found is None:
            note = inventory.near_match_note(rel)
            if note is not None:
                near.append((rel, note))
            continue
        cls, step = found
        size, text, quality, reason = _read_piece_file(root_path / rel)
        ident = inventory.identity_for(cls, step, rel)
        raw.setdefault(ident, []).append(
            (rel, cls, step, size, text, quality, reason))
    pieces = []
    for ident in sorted(raw, key=lambda i: min(x[0] for x in raw[i])):
        group = sorted(raw[ident], key=lambda x: x[0])
        rel0, cls, step, size0, text0, quality0, reason0 = group[0]
        paths = tuple(x[0] for x in group)
        if len(group) > 1:
            texts = {x[4] for x in group}
            if len(texts) == 1 and text0 is not None:
                pieces.append(Piece(ident, paths, cls, step, size0, text0,
                                    None, quality0))
            else:
                pieces.append(Piece(
                    ident, paths, cls, step, size0, None,
                    "not read in full: duplicate content disagreement "
                    "between the paths that yield this piece", quality0))
            continue
        pieces.append(Piece(ident, paths, cls, step, size0, text0,
                            reason0, quality0))
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
                        walk_note=walk_note)


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
    tmp = parent / (destination.name + ".tmp-msc")
    try:
        tmp.write_text(text, encoding="utf-8", newline="\n")
        os.replace(str(tmp), str(destination))
    except OSError as exc:
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass
        raise UsageError("deliver the report: destination %s: %s"
                         % (report_path, exc))
