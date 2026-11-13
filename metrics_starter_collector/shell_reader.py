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
    CLS_ADJUDICATION, CLS_AUDIT_PAPER, CLS_BOARD_MEMBER,
    CLS_DECISION_QUEUE, CLS_DEFECT_REGISTER, CLS_FIX_REGISTER,
    CLS_GATE_ADJUDICATION, CLS_GATE_RECORD, CLS_GATE_RULING,
    CLS_METRICS_PAGE, CLS_METRICS_SINGLE, CLS_OTHER_REGISTER,
    CLS_PATH_LEDGER, CLS_REGATE_RECORD, CLS_STEP_RECORD, CLS_TIER_RECORD,
    CLS_TRACE, GATE_CLASSES, CapturedRead, Piece)

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


def _evidenced_rounds(pieces, step):
    """Rounds or passes evidenced for one step, in the CA-5 forms.

    The forms mirror the round evidence the core reads for T-7: a
    pass count or rounds statement in the step own record, the
    re-audit round headings of a loop record, an explicit verdict
    record count in a verdict record, or the count of gate pieces
    standing for the step. The largest evidenced count governs.
    Returns 0 where no round is evidenced for the step.
    """
    candidates = []
    texts = [p.text for p in pieces
             if p.step == step and p.record_class == CLS_STEP_RECORD
             and p.text]
    joined = "\n".join(texts)
    if joined:
        m = re.search(r"Pass count in this record:\s*(\d+)\s*passes",
                      joined)
        if m:
            candidates.append(int(m.group(1)))
        m = re.search(r"states\s+(\d+)\s+rounds for this step", joined)
        if m:
            candidates.append(int(m.group(1)))
        head_rounds = [int(x) for x in re.findall(
            r"^## Re-audit[^\n]*\(round (\d+)", joined, re.M)]
        reaudit_heads = re.findall(r"^## Re-audit", joined, re.M)
        if head_rounds and min(head_rounds) == 1:
            candidates.append(max(head_rounds))
        elif reaudit_heads:
            candidates.append(1 + len(reaudit_heads))
    gate_pieces = [p for p in pieces
                   if p.step == step and p.record_class in GATE_CLASSES]
    verdict = None
    for p in gate_pieces:
        if p.text:
            m = re.search(r"Verdict record count for this step:\s*(\d+)",
                          p.text)
            if m:
                verdict = int(m.group(1))
                break
    if verdict is None and gate_pieces:
        verdict = len(gate_pieces)
    if verdict is not None:
        candidates.append(verdict)
    return max(candidates) if candidates else 0


def capture_read(root):
    """Walk the root once and build the one CapturedRead for the run."""
    root_path = Path(root)
    if not root_path.exists() or not root_path.is_dir():
        raise UnreadableInputError(
            "capture the record tree: root %s: not a readable directory"
            % (root,))
    root_resolved = root_path.resolve()
    entries = []
    damaged = {}
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
                except (OSError, RuntimeError) as exc:
                    # A link loop or an unresolvable link target. The
                    # entry is damage inside a readable tree, never a
                    # run failure: where the name is a recognised
                    # record name the entry stands as a damaged piece.
                    if inventory.classify(rel) is not None:
                        entries.append(rel)
                        damaged[rel] = (
                            "unreadable-piece: unreadable: symlink "
                            "loop or unresolvable link target: %s" % exc)
                    continue
                if target != root_resolved and \
                        root_resolved not in target.parents:
                    # A link whose target sits outside the root is not
                    # followed. Where the name is a recognised record
                    # name the entry still stands as a damaged piece,
                    # so the refusal is never silent.
                    if inventory.classify(rel) is not None:
                        entries.append(rel)
                        if target.exists():
                            damaged[rel] = (
                                "unreadable-piece: unreadable: link "
                                "target outside the tree, not followed")
                        else:
                            damaged[rel] = (
                                "unreadable-piece: unreadable: dangling "
                                "link, the link target does not stand")
                    elif not target.exists() and \
                            inventory.near_match_note(rel) is not None:
                        # A dangling link at a near match name is not
                        # a piece, but the name stands in the near
                        # match listing, in the same form as a regular
                        # file at that name.
                        entries.append(rel)
                    continue
                if full.is_file():
                    entries.append(rel)
                elif full.is_dir() and \
                        inventory.classify(rel) is not None:
                    entries.append(rel)
                elif inventory.classify(rel) is not None:
                    entries.append(rel)
                    if target.exists():
                        # The target stands but is not a regular
                        # file: a FIFO, a socket or a device at the
                        # end of the link. The reason states that
                        # true damage, in the same form the direct
                        # case at a recognised name uses.
                        damaged[rel] = (
                            "unreadable-piece: unreadable: not a "
                            "regular file")
                    else:
                        damaged[rel] = (
                            "unreadable-piece: unreadable: dangling "
                            "link, the link target does not stand")
                elif not target.exists() and \
                        inventory.near_match_note(rel) is not None:
                    # As in the outside target passage above: a
                    # dangling link at a near match name stands in
                    # the near match listing, in the same form as a
                    # regular file at that name.
                    entries.append(rel)
                continue
            if full.is_file():
                entries.append(rel)
            elif full.is_dir() and \
                    inventory.classify(rel) is not None:
                entries.append(rel)
            elif inventory.classify(rel) is not None:
                # A non regular file (a FIFO, a socket, a device) at a
                # recognised record name. It is never opened, because
                # opening such a file can block, and it stands as a
                # damaged piece instead of vanishing.
                entries.append(rel)
                damaged[rel] = (
                    "unreadable-piece: unreadable: not a regular file")
        if walk_note:
            break
    entries.sort()
    alias_map = {}
    by_target = {}
    for rel in entries:
        if rel in damaged:
            # A damaged entry is never merged with another path by
            # link target: its own path is the piece that stands.
            key = "damaged:" + rel
        else:
            try:
                key = str((root_path / rel).resolve())
            except (OSError, RuntimeError):
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

    size_unknown = []

    def stat_size(rel):
        full = root_path / rel
        try:
            if full.is_dir() and not full.is_symlink():
                return 0
            return full.stat().st_size
        except OSError:
            # A failed stat never stands silent: the path is carried
            # on the CapturedRead and marked size unknown in the data
            # quality section of the report.
            if rel not in size_unknown:
                size_unknown.append(rel)
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
        if rel in damaged:
            size = stat_size(rel)
            text = None
            quality = "unreadable"
            reason = damaged[rel]
        elif rel in cut_set:
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
        cls = group[0][1]
        step = group[0][2]
        form = None
        if cls == CLS_METRICS_SINGLE:
            form = "single page form"
        elif cls == CLS_METRICS_PAGE:
            form = "split page form"
        # An entry that yields no readable content never merges with
        # another entry at the same identity and never displaces a
        # sound one: there is no second content for it to disagree
        # with, because the entry has no readable content at all.
        # The partition rests on the read outcome, not on the walk
        # damaged map alone, so it covers every no content form in
        # the same way: the walk damaged forms (dangling links, FIFOs
        # and loop links) and the read forms (a directory, a link to
        # a directory, a malformed file, an over limit file and a
        # piece past the tree limit). Each such entry stands as its
        # own piece, marked with its true state, and the sound
        # entries at the identity merge and read exactly as they do
        # where no such entry stands.
        broken = [x for x in group if x[4] is None]
        rest = [x for x in group if x[4] is not None]
        for x in broken:
            pieces.append(Piece(ident, x[7], x[1], x[2], x[3], None,
                                x[6], x[5], form_state=form))
        # An entry whose text carries no substantive content (an
        # empty file: in the proven forms a zero byte file, or a
        # file holding a single newline) stands in the same no
        # content family. Where a substantive entry stands at the
        # same identity, each such empty entry stands as its own
        # piece, carrying its true read state (its empty text, its
        # measured size, no quality fault and no not read reason),
        # and never merges with or displaces the substantive piece:
        # a disagreement requires two substantive differing texts,
        # and an entry with no content has no content to disagree
        # with. Where no substantive entry stands at the identity,
        # the empty entries are not partitioned at all and keep the
        # standing treatment exactly: identical empty entries still
        # merge into one piece, and a lone empty entry stands as it
        # stands today.
        if any(x[4].strip() for x in rest):
            empties = [x for x in rest if not x[4].strip()]
            standing = [x for x in rest if x[4].strip()]
            for x in empties:
                pieces.append(Piece(ident, x[7], x[1], x[2], x[3],
                                    x[4], x[6], x[5],
                                    form_state=form))
        else:
            standing = rest
        if not standing:
            continue
        group = standing
        rel0, cls, step, size0, text0, quality0, reason0 = group[0][:7]
        paths = tuple(sorted({p for x in group for p in x[7]}))
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
    # M-2: the Form A record change statement is parsed from the
    # assembled metrics record text, through the Inventory, during
    # this single walk, and the per change force state is recorded
    # on the CapturedRead below.
    force = inventory.record_change_force(assembled)
    totals = {}
    per_build = (CLS_PATH_LEDGER, CLS_TIER_RECORD, CLS_METRICS_SINGLE,
                 CLS_DECISION_QUEUE)
    per_round = (CLS_AUDIT_PAPER, CLS_BOARD_MEMBER, CLS_FIX_REGISTER,
                 CLS_DEFECT_REGISTER, CLS_ADJUDICATION, CLS_TRACE,
                 CLS_OTHER_REGISTER)
    for p in pieces:
        entry = totals.setdefault(p.record_class,
                                  {"expected": 0, "found": 0,
                                   "not_found": 0, "not_yet_recordable": 0})
        entry["found"] += 1

    def ensure(cls):
        return totals.setdefault(cls, {"expected": 0, "found": 0,
                                       "not_found": 0,
                                       "not_yet_recordable": 0})

    assigned = set()
    if evidenced:
        # Per step class: one step record per step instance.
        entry = ensure(CLS_STEP_RECORD)
        entry["expected"] = len(evidenced)
        assigned.add(CLS_STEP_RECORD)
        # Gate alias classes share the one CA-5 expectation of one
        # first gate piece per step instance in any alias form. Each
        # alias class states its own found count, and the count of
        # steps holding no gate piece in any alias form stands once,
        # on the gate record class line, never once per alias.
        steps_with_gate = {p.step for p in pieces
                           if p.record_class in GATE_CLASSES
                           and p.step is not None}
        gate_missing = len([s for s in evidenced
                            if s not in steps_with_gate])
        for cls in GATE_CLASSES:
            entry = ensure(cls)
            entry["expected"] = entry["found"]
            assigned.add(cls)
        carrier = ensure(CLS_GATE_RECORD)
        carrier["expected"] = carrier["found"] + gate_missing
    # Per build classes: one per build. The metrics record counts as
    # one in either physical form, so where split pages stand and no
    # single page stands, the single page class carries no separate
    # expectation and the pages are listed as found.
    metrics_forms_stand = bool(
        [p for p in pieces if p.record_class == CLS_METRICS_PAGE]) and \
        not [p for p in pieces if p.record_class == CLS_METRICS_SINGLE]
    for cls in per_build:
        if cls == CLS_METRICS_SINGLE and metrics_forms_stand:
            continue
        entry = ensure(cls)
        entry["expected"] = 1
        assigned.add(cls)
    # Per round classes: the expectation is the number of rounds or
    # passes evidenced for the steps, in the step own records or in
    # verdict records. Where no round is evidenced at all, found
    # pieces alone are listed for these classes, by the fallback
    # below, and not found is 0 by that rule.
    total_rounds = sum(_evidenced_rounds(pieces, s) for s in evidenced)
    if total_rounds:
        for cls in per_round:
            entry = ensure(cls)
            entry["expected"] = total_rounds
            assigned.add(cls)
    for cls, entry in totals.items():
        if cls not in assigned:
            entry["expected"] = entry["found"]
        entry["not_found"] = max(0, entry["expected"] - entry["found"])
    # M-2 force application: a class whose creating record change
    # stands NOT IN FORCE carries its expected count under not yet
    # recordable and under no other state. Under the settled mapping
    # in the Inventory every one of the five changes maps to no
    # record class, so this passage moves no count; the force state
    # above is parsed and recorded, not defaulted.
    for number, state in sorted(force.items()):
        if state != "NOT IN FORCE":
            continue
        for cls in inventory.RECORD_CHANGE_CLASSES.get(number, ()):
            entry = totals.get(cls)
            if entry is None:
                continue
            entry["not_yet_recordable"] += entry["expected"]
            entry["not_found"] = 0
            entry["expected"] = 0
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
                        tree_file_limit=TREE_FILE_LIMIT,
                        record_change_force=force,
                        size_unknown_paths=tuple(sorted(size_unknown)))


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
    except (OSError, RuntimeError) as exc:
        raise UsageError("deliver the report: destination %s: %s"
                         % (report_path, exc))
    # The resolved path governs, and the named path is checked with
    # it: a destination is refused where either its resolved path or
    # its named path lies inside the tree read. A link standing
    # inside the tree and pointing outside it is therefore refused
    # in this same form, because the destination as named lies
    # inside the tree and the write would land outside it through
    # the link, which the read only rule bars.
    dest_named = Path(os.path.abspath(str(destination)))
    root_named = Path(os.path.abspath(str(root)))
    inside = False
    for base in (root_resolved, root_named):
        for candidate in (dest_resolved, dest_named):
            if candidate == base or base in candidate.parents:
                inside = True
    if not inside:
        # Every prefix of the named destination is checked in
        # resolved form as well. A destination named through an
        # alias of the root itself resolves into the tree at that
        # prefix, even where neither the full named path nor the
        # fully resolved path lies inside the tree, as with a report
        # named through the root alias and then out through a link
        # standing inside the tree. Such a destination is refused in
        # the same form: the write would pass through the tree read.
        prefix = Path(dest_named.anchor)
        for part in dest_named.parts[1:]:
            prefix = prefix / part
            try:
                resolved_prefix = prefix.resolve()
            except (OSError, RuntimeError) as exc:
                raise UsageError(
                    "deliver the report: destination %s: %s"
                    % (report_path, exc))
            if resolved_prefix == root_resolved or \
                    root_resolved in resolved_prefix.parents:
                inside = True
                break
    if inside:
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
