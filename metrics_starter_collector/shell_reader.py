"""Module 1: shell reader, the thin shell.

This is the only module that touches the filesystem. It validates
the root the operator names, walks that tree once, level by level
from the root down, reads each discovered piece once, applies
the capture limits in the minimal form this slice needs, and
builds the one CapturedRead every later part of the run reads.
It also delivers the finished report, to standard output or to
the one operator named file. It holds no derivation rule.
"""
import os
import re
import stat
import sys
from datetime import datetime
from pathlib import Path

from metrics_starter_collector import inventory
from metrics_starter_collector.derivation_core import (
    CLS_ADJUDICATION, CLS_AUDIT_PAPER, CLS_BOARD_MEMBER,
    CLS_DECISION_QUEUE, CLS_DEFECT_REGISTER, CLS_FIX_REGISTER,
    CLS_GATE_RECORD, CLS_METRICS_PAGE, CLS_METRICS_SINGLE,
    CLS_OTHER_REGISTER, CLS_PATH_LEDGER, CLS_STEP_RECORD,
    CLS_TIER_RECORD, CLS_TRACE, GATE_CLASSES, CapturedRead, Piece)

# The capture limits, as named constants in this module, where
# limit enforcement stands. No operator option exists for any of
# them.
FILE_LIMIT = 1000000
TREE_BYTE_LIMIT = 25000000
TREE_FILE_LIMIT = 2000
LINE_LIMIT = 65536
WALK_BOUND = 10000


class UnreadableInputError(Exception):
    """The shell cannot produce a CapturedRead at all for the root."""


class UsageError(Exception):
    """A delivery form the command grammar refuses."""


_FULL_STAMP = re.compile(
    r"(\d{4}-\d{2}-\d{2})[ T](\d{2}):(\d{2})(?::(\d{2}))?"
    r"(?:\s*(CST|UTC|EST|EDT|CDT))?")
_DATE_ONLY = re.compile(r"(\d{4}-\d{2}-\d{2})")
_VERSION_LINE = re.compile(r"Definitions version:\s*(.+)")


def _latest_timestamp(texts):
    """The latest record timestamp found inside the captured texts.

    A timestamp with a time of day keys by its full value. A date
    standing alone keys at the start of its day. The winning stamp
    is returned in the form the record states it. A stamp stands
    as a record timestamp only where it is a real calendar stamp:
    each candidate is validated by forming its datetime, in the
    same form the Derivation core validates the same stamps, and
    a candidate that forms no datetime, an impossible date or an
    impossible time of day, is no timestamp and never wins. A
    date that stands in a text only as the date part of a full
    stamp candidate is no date standing alone: where that full
    stamp is refused, its date part does not key either, and a
    date keys at the start of its day only where it stands in
    the text apart from any full stamp.
    """
    winner = None
    winner_key = None
    for text in texts:
        full_starts = {found.start()
                       for found in _FULL_STAMP.finditer(text)}
        for found in _FULL_STAMP.finditer(text):
            year, month, day = (int(part) for part
                                in found.group(1).split("-"))
            try:
                moment = datetime(year, month, day,
                                  int(found.group(2)),
                                  int(found.group(3)),
                                  int(found.group(4) or "0"))
            except ValueError:
                continue
            key = (moment.year, moment.month, moment.day,
                   moment.hour, moment.minute, moment.second)
            if winner_key is None or key > winner_key:
                winner_key = key
                winner = found.group(0)
        for found in _DATE_ONLY.finditer(text):
            if found.start() in full_starts:
                continue
            year, month, day = (int(part) for part
                                in found.group(1).split("-"))
            try:
                moment = datetime(year, month, day)
            except ValueError:
                continue
            key = (moment.year, moment.month, moment.day, 0, 0, 0)
            if winner_key is None or key > winner_key:
                winner_key = key
                winner = found.group(1)
    return winner


TRUNCATION_MARKER = "TRUNCATED"

_CONTENTS_LINE = re.compile(r"^Contents(?: list)?:\s*(.+?)\s*$")
_HEADING_LINE = re.compile(r"^#{1,6}\s+(.+?)\s*$")

_SEQUENCE_ENTRY = re.compile(
    r"^(Finding|Item|Entry|Part|Round|Step)\s+(\d+)\s+"
    r"(stands|is|was|are|were|reads|states|holds|remains|applies)\b")
_SEQUENCE_TOTAL = (
    re.compile(r"(\d+)\s+(findings|items|entries|parts|rounds|steps)"
               r"\s+in total"),
    re.compile(r"total of\s+(\d+)\s+"
               r"(findings|items|entries|parts|rounds|steps)"),
    re.compile(r"(findings|items|entries|parts|rounds|steps) total:"
               r"\s*(\d+)"))
_SIGNAL_ONE_EXCEPTION = (
    re.compile(r"sequence is (partial|planned)"),
    re.compile(r"(partial|planned) sequence"),
    re.compile(r"numbers( in the sequence)? (are|were) "
               r"(reserved|skipped)"),
    re.compile(r"skipped by design"),
    re.compile(r"reserved by design"))

_HEADER_COUNT = (
    re.compile(r"rows stated in header:\s*(\d+)"),
    re.compile(r"(\d+)\s+rows stated in (the )?header"),
    re.compile(r"header[^\n:]*:\s*(\d+)\s+rows"))
# The correction vocabularies stand in the order the Derivation
# core collects them, so where two matches share one starting
# place in the record the last correction figure taken here is
# the figure the core takes.
_CORRECTED_COUNT = (
    re.compile(r"corrected count:?\s*(\d+)"),
    re.compile(r"correct\w*[^\n]*?(\d+)\s+rows"),
    re.compile(r"restates? the count[^\n\d]*(\d+)"))


def _signal_one_failure(text):
    """The signal one completeness failure in a text, or None.

    Signal one: a numbered sequence with a gap, or a final
    number below a total the same record states. A sequence
    entry is a statement line opening with its label and number,
    in the form Finding 1 stands. Entries stand grouped by
    label, in record order. The signal does not fire where the
    record states in its own text that the sequence is partial
    or planned, or that numbers in the sequence are reserved or
    skipped by design.
    """
    lowered = text.lower()
    for pattern in _SIGNAL_ONE_EXCEPTION:
        if pattern.search(lowered):
            return None
    sequences = {}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("|"):
            continue
        found = _SEQUENCE_ENTRY.match(stripped)
        if found:
            label = found.group(1).lower()
            number = int(found.group(2))
            entries = sequences.setdefault(label, [])
            if not entries or entries[-1] != number:
                entries.append(number)
    for label, entries in sequences.items():
        if len(entries) >= 2 and entries[0] == 1 and \
                all(b > a for a, b in zip(entries, entries[1:])):
            missing = [n for n in range(1, entries[-1] + 1)
                       if n not in entries]
            if missing:
                return ("the numbered %s sequence has a gap: "
                        "number %d does not appear, and the sequence "
                        "runs to %d" % (label, missing[0],
                                        entries[-1]))
    totals = {}
    for pattern in _SEQUENCE_TOTAL:
        for found in pattern.finditer(lowered):
            if found.lastindex == 2 and \
                    found.group(1).isdigit():
                totals[found.group(2)] = int(found.group(1))
            elif found.lastindex == 2:
                totals[found.group(1)] = int(found.group(2))
    for label, entries in sequences.items():
        total = totals.get(label + "s")
        if total is not None and entries and entries[-1] < total:
            return ("the numbered %s sequence ends at %d, below "
                    "the total of %d the same record states"
                    % (label, entries[-1], total))
    return None


def _table_data_rows(lines, start):
    """The data row count of the markdown table at or after start."""
    index = start
    while index < len(lines) and not lines[index].strip().startswith("|"):
        index += 1
    if index >= len(lines):
        return None
    rows = 0
    index += 1
    while index < len(lines) and lines[index].strip().startswith("|"):
        cells = lines[index].strip().strip("|")
        if not all(set(cell.strip()) <= set("-: ") and cell.strip()
                   for cell in cells.split("|")):
            rows += 1
        index += 1
    return rows


def _header_count_excepted(header_line):
    """Whether one header count statement line carries the signal
    two exception, under the agreed negation rule.

    The exception fires only where the header count stands
    stated as a planned count or as a target count and no
    negation governs that statement. A negation form is one of
    the words not, no or never, the modal form cannot, or a
    contraction ending in n't, as isn't. A rejection form is
    one of the words rejected, refused, denied, negated,
    withdrawn, superseded, cancelled, canceled or dropped.

    A negation form standing in the same clause before the
    planned or target statement governs it, as not a planned
    count, no planned count, never a target count, or isn't a
    planned count, and so does a negation form standing alone
    in its own clause before the statement, with no complement
    of its own in that clause, as not, strictly speaking, a
    planned count, because such a negation can only attach to
    the statement that follows it, across any parenthetical
    clause between them. A negation form standing in an
    earlier clause with a complement of its own in that
    clause, as not audited, stated as a planned count, governs
    that complement and does not govern the statement. A
    rejection form standing in the same clause after the
    statement governs it, as the planned count was rejected
    or the planned count was withdrawn, and so does a
    rejection form standing in a later clause that carries no
    subject of its own beyond a relative or auxiliary word,
    as a planned count, rejected, or stated as a planned
    count, which was rejected, because such a clause is the
    trailing part of the one statement. The brief form lines,
    the count stated as a planned count and the count stated
    as a target count with no negation standing, except.
    """
    negation = r"(?:\b(?:not|no|never|cannot)\b|\b\w+n't\b)"
    rejection = (
        r"\b(?:rejected|refused|denied|negated|withdrawn"
        r"|superseded|cancelled|canceled|dropped)\b")
    found = re.search(
        r"\bplanned count\b|\btarget count\b"
        r"|\bstated as (?:a |an )?(?:planned|target)"
        r"(?: count)?\b",
        header_line)
    if not found:
        return False
    clauses_before = re.split(
        r"[,;]", header_line[:found.start()])
    if re.search(negation, clauses_before[-1]):
        return False
    for clause in reversed(clauses_before[:-1]):
        if not re.search(negation, clause):
            continue
        if re.fullmatch(
                r"(?:(?:the|a|an|it|this|that|there) )?"
                r"(?:(?:count|record|statement|header) )?"
                r"(?:(?:is|was|were|are|be|been) )?"
                r"(?:not|no|never|cannot|\w+n't)"
                r"(?: (?:at all|any longer|longer))?",
                clause.strip().rstrip(".")):
            return False
        break
    clauses_after = re.split(
        r"[,;]", header_line[found.end():])
    if re.search(rejection, clauses_after[0]):
        return False
    for clause in clauses_after[1:]:
        rejected = re.search(rejection, clause)
        if not rejected:
            continue
        head_words = clause[:rejected.start()].split()
        if all(word in (
                "which", "that", "it", "this", "was", "were",
                "is", "are", "has", "have", "had", "been",
                "being", "since", "and", "but", "now", "then",
                "later", "subsequently")
               for word in head_words):
            return False
        break
    return True


def _signal_two_failure(text):
    """The signal two completeness failure in a text, or None.

    Signal two: a table whose row count disagrees with a count
    stated in its own header. The signal does not fire where
    the header count is stated in the record as a planned or
    target count. The exception attaches to the header count
    statement itself: the planned or target wording must stand
    in that statement, and a mention of a planned count or a
    target count anywhere else in the piece carries no
    exception. The exception fires only where the header count
    stands stated in that statement as a planned count or as a
    target count, on the word bounded forms planned count and
    target count and on the stated as a planned or stated as a
    target form, so a negated form, as unplanned, and a derived
    form, as targeted, state no exception, and neither does a
    statement a negation governs, as not a planned count, no
    planned count, never a target count, not planned count, or
    a planned count stated as rejected, each of which states
    the opposite of the exception condition. Where a governing
    correction in the record restates the count, the corrected
    count is the count tested, and the correction stands
    honoured in every vocabulary the Derivation core honours:
    a count in rows, the restates the count form, and the
    corrected count followed by its number, so a record
    corrected in any of them is judged on the same corrected
    count here as in the core, and where two correction
    statements stand in one record the corrected count is
    the figure the last such statement states, across the
    union of the three vocabularies alike. The rows tested
    are the rows of the one table that follows the header
    count statement, so a second table later in the piece
    contributes no row to this count.
    """
    lines = text.splitlines()
    lowered = text.lower()
    found_corrections = []
    for pattern in _CORRECTED_COUNT:
        for found in pattern.finditer(lowered):
            found_corrections.append(
                (found.start(), int(found.group(1))))
    corrected = None
    if found_corrections:
        found_corrections.sort(key=lambda entry: entry[0])
        corrected = found_corrections[-1][1]
    for index, line in enumerate(lines):
        stripped = line.strip()
        stated = None
        for pattern in _HEADER_COUNT:
            found = pattern.search(stripped.lower())
            if found:
                stated = int(found.group(1))
                break
        if stated is None:
            continue
        lowered_line = stripped.lower()
        if _header_count_excepted(lowered_line):
            continue
        tested = corrected if corrected is not None else stated
        rows = _table_data_rows(lines, index + 1)
        if rows is not None and rows != tested:
            return ("a table holds %d data rows, which disagrees "
                    "with the count of %d stated in its own header"
                    % (rows, tested))
    return None


def _signal_three_failure(text):
    """The signal three completeness failure in a text, or None.

    Signal three: a section a record contents list names that
    does not appear in the record. A contents line states its
    sections as a comma separated list after the Contents or
    Contents list label. A named section appears where a heading
    line in the record states that section name. A section the
    contents list itself marks as deferred or not yet written
    carries the exception form and the signal does not fire on
    that section, and a section a later governing entry in the
    record removes from the list does not fire either.
    """
    headings = set()
    for line in text.splitlines():
        found = _HEADING_LINE.match(line.strip())
        if found:
            headings.add(found.group(1).strip().lower())
    lines = text.splitlines()
    for index, line in enumerate(lines):
        found = _CONTENTS_LINE.match(line.strip())
        if not found:
            continue
        stated = found.group(1).rstrip(".")
        for name in stated.split(","):
            name = name.strip()
            if not name:
                continue
            segment = name.lower()
            if "deferred" in segment or \
                    "not yet written" in segment:
                continue
            plain = re.sub(r"\s*\((deferred|not yet written)\)\s*",
                           "", segment).strip()
            if plain in headings:
                continue
            removed = False
            for later in lines[index + 1:]:
                lowered_later = later.lower()
                if plain in lowered_later and (
                        "removed from the list" in lowered_later
                        or "removes the section" in lowered_later
                        or "removed from the contents" in lowered_later
                        or "no longer in the list" in lowered_later):
                    removed = True
                    break
            if not removed:
                return name
    return None


_COMPLETION_HEADING = re.compile(r"^#{1,6}\s+Completion section\s*$")


def _repair_citation(text):
    """The repair citation a Completion section carries, or None.

    A repair is recognised by a section inside the same piece,
    standing after the truncated part, headed Completion
    section, stating that the piece was found truncated,
    identifying its piece as this file, and supplying the
    missing content in place. A completion supplying only a
    corrected total is a correcting record, not a repair, and
    carries no citation here.
    """
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not _COMPLETION_HEADING.match(line.strip()):
            continue
        section = "\n".join(lines[index + 1:])
        lowered = section.lower()
        if "found truncated" not in lowered:
            continue
        if "this file" not in lowered:
            continue
        if "supplies the missing content in place" not in lowered \
                and "supplying the missing content in place" \
                not in lowered:
            continue
        return ("the piece was found truncated and a Completion "
                "section in this file supplies the missing content "
                "in place")
    return None


def _completeness_failure(text):
    """The first completeness signal a text fails, or None.

    Returns (signal name, detail). The three signals stand
    tested in their numbered order, each with its exception
    form, on a valid text file with no truncation marker.
    """
    detail = _signal_one_failure(text)
    if detail is not None:
        return "signal-one", detail
    detail = _signal_two_failure(text)
    if detail is not None:
        return "signal-two", detail
    missing_section = _signal_three_failure(text)
    if missing_section is not None:
        return "signal-three", (
            "the contents list names the section %s, which does "
            "not appear in the piece" % missing_section)
    return None


def _read_once(path):
    """Read one discovered file exactly once.

    Returns (size, text, quality_state, not_read_reason). A file
    that cannot be read, that crosses the file limit, that is not
    valid UTF-8, or that holds a line over the line limit yields
    no text and carries its state and reason instead. A piece
    carrying the truncation marker line, and a piece failing any
    of the three completeness signals, likewise yields no text
    and carries the truncated state, with the failed signal
    named in the reason: the visible part of a truncated piece
    counts toward nothing. A piece carrying a recognised
    Completion section repair keeps its completed text and
    carries the single state truncated, with the repair cited
    in its reason beside that state.
    """
    try:
        data = path.read_bytes()
    except OSError as exc:
        return 0, None, "unreadable", \
            "unreadable-piece: the piece could not be read: %s" % exc
    size = len(data)
    if size > FILE_LIMIT:
        return size, None, "over limit", \
            "over-limit-piece: the file limit of %d bytes was " \
            "crossed" % FILE_LIMIT
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return size, None, "malformed", \
            "malformed-piece: the piece is not valid UTF-8 text"
    for line in text.splitlines():
        if len(line.encode("utf-8")) > LINE_LIMIT:
            return size, None, "over limit", \
                "over-limit-piece: the line limit of %d bytes was " \
                "crossed" % LINE_LIMIT
    for line in text.splitlines():
        if line.strip() == TRUNCATION_MARKER:
            return size, None, "truncated", \
                "truncated-piece: the piece carries a truncation " \
                "marker and its visible part is not read in full"
    repair = _repair_citation(text)
    if repair is not None:
        return size, text, "truncated", \
            "repaired-truncation: %s; the piece stands in its " \
            "completed text with the repair cited beside its " \
            "truncated state" % repair
    failure = _completeness_failure(text)
    if failure is not None:
        signal, detail = failure
        return size, None, "truncated", \
            "truncated-piece: %s failed: %s, and its visible " \
            "part is not read in full" % (signal, detail)
    return size, text, None, None


def _definitions_version(assembled):
    """The definitions version the assembled record states, if any."""
    if not assembled:
        return None
    found = _VERSION_LINE.search(assembled)
    if found:
        return found.group(1).strip()
    return None


def _build_identity(pieces, assembled):
    """The build identity the tree states, from its own records."""
    if assembled:
        found = re.search(r"^#\s*Build metrics record:\s*(.+)$",
                          assembled, re.M)
        if found:
            return found.group(1).strip()
        found = re.search(r"^- Project:\s*(.+)$", assembled, re.M)
        if found:
            return found.group(1).strip()
    for piece in pieces:
        if piece.text and piece.record_class == CLS_STEP_RECORD:
            found = re.search(r"Build:\s*(.+)\.", piece.text)
            if found:
                return found.group(1).strip()
    return None


def _rounds_evidenced(pieces, step):
    """The round count one step evidences, for inventory totals.

    The forms are a pass count or rounds statement in the step own
    record, re-audit round headings in that record, an explicit
    verdict record count in a gate piece, or the count of gate
    pieces standing for the step. The largest evidenced count
    governs, and 0 stands where no round is evidenced.
    """
    candidates = []
    record_text = "\n".join(
        p.text for p in pieces
        if p.step == step and p.record_class == CLS_STEP_RECORD
        and p.text)
    if record_text:
        found = re.search(r"Pass count in this record:\s*(\d+)\s*passes",
                          record_text)
        if found:
            candidates.append(int(found.group(1)))
        found = re.search(r"states\s+(\d+)\s+rounds for this step",
                          record_text)
        if found:
            candidates.append(int(found.group(1)))
        numbered = [int(x) for x in re.findall(
            r"^## Re-audit[^\n]*\(round (\d+)", record_text, re.M)]
        headings = re.findall(r"^## Re-audit", record_text, re.M)
        if numbered and min(numbered) == 1:
            candidates.append(max(numbered))
        elif headings:
            candidates.append(1 + len(headings))
    gate_pieces = [p for p in pieces
                   if p.step == step
                   and p.record_class in GATE_CLASSES]
    verdict = None
    for piece in gate_pieces:
        if piece.text:
            found = re.search(
                r"Verdict record count for this step:\s*(\d+)",
                piece.text)
            if found:
                verdict = int(found.group(1))
                break
    if verdict is None and gate_pieces:
        verdict = len({p.identity for p in gate_pieces})
    if verdict is not None:
        candidates.append(verdict)
    return max(candidates) if candidates else 0


def _walk_entries(root_path, root_resolved):
    """Walk the root once, level by level from the root down.

    Entries are visited in the order of their names at each level
    of the tree, level by level, in the brief Section 5 order, so
    the same tree is always walked in the same order and the set
    of pieces the bound leaves unvisited is the same on every
    run. The walk first enumerates every entry name in that
    order, reading no piece, so the inventory the floor at
    D4R-08 is judged on is the inventory of the whole tree and
    not the part of it the bound reaches. The whole walk bound
    then cuts that order: entries past the bound are not visited
    and not read, the crossing is named in the walk note, and a
    recognisable piece past the bound still stands in the
    capture as a not visited piece, so its rows take the partial
    form and never the missing form and never the floor form.

    A directory that cannot be listed does not vanish in
    silence: the failure surfaces in the walk note in the error
    form, naming the operation, the directory, and the cause,
    and stating that its subtree was not visited, so the
    capture and its coverage statement carry the failure in
    the open and the reading stands partial on it.

    Returns (entries, damaged, walk_note, unvisited). Entries are
    the relative paths of files the capture may use, with link
    targets inside the root followed at most once. Damaged maps
    a relative path to its not read reason where the entry
    itself stands damaged: a link out of the tree, a dangling
    link, a link loop, or a non regular file standing at a
    recognised record name. Unvisited maps a relative path past
    the bound to its not visited reason. A directory is never
    classified or counted as a record piece in its own right:
    a container directory the walk descends into, such as the
    audit directory, stands as no piece anywhere. The one
    standing exception the capture keeps is a directory at a
    file name path, where it blocks the file piece that name
    carries: it stands as that damaged piece, unreadable, and
    not as a piece of its own.
    """
    ordered = []
    listing_failures = []
    level = [root_path]
    while level:
        next_level = []
        for directory in level:
            try:
                names = sorted(os.listdir(str(directory)))
            except OSError as exc:
                if directory == root_path:
                    shown = str(directory)
                else:
                    shown = str(directory.relative_to(root_path))
                listing_failures.append(
                    "the directory %s could not be listed: "
                    "list the directory %s: %s; its subtree "
                    "was not visited" % (shown, shown, exc))
                continue
            for name in names:
                full = directory / name
                rel = str(full.relative_to(root_path))
                ordered.append((rel, full))
                if not full.is_symlink() and full.is_dir():
                    next_level.append(full)
        level = next_level
    walk_notes = []
    if len(ordered) > WALK_BOUND:
        walk_notes.append(
            "the whole walk bound of %d entries was reached "
            "and entries beyond it were not visited"
            % WALK_BOUND)
    walk_notes.extend(listing_failures)
    walk_note = "; ".join(walk_notes) if walk_notes else None
    entries = []
    damaged = {}
    unvisited = {}
    seen_targets = set()
    for index, (rel, full) in enumerate(ordered):
        recognised = inventory.classify(rel) is not None
        if index >= WALK_BOUND:
            if recognised:
                entries.append(rel)
                unvisited[rel] = (
                    "over-limit-piece: not visited: the whole "
                    "walk bound of %d entries was crossed before "
                    "this piece was visited, and the piece was "
                    "not read" % WALK_BOUND)
            continue
        if full.is_symlink():
            try:
                target = full.resolve()
            except (OSError, RuntimeError) as exc:
                if recognised:
                    entries.append(rel)
                    damaged[rel] = (
                        "unreadable-piece: the link target could "
                        "not be resolved: %s" % exc)
                continue
            if target != root_resolved and \
                    root_resolved not in target.parents:
                if recognised:
                    entries.append(rel)
                    if target.exists():
                        damaged[rel] = (
                            "unreadable-piece: link target "
                            "outside the tree, not followed")
                    else:
                        damaged[rel] = (
                            "unreadable-piece: dangling link, "
                            "the link target does not stand")
                elif not target.exists() and \
                        inventory.near_match_note(rel) is not None:
                    entries.append(rel)
                continue
            target_key = str(target)
            if target_key in seen_targets:
                continue
            seen_targets.add(target_key)
            if full.is_file():
                entries.append(rel)
            elif recognised:
                entries.append(rel)
                if target.exists():
                    damaged[rel] = (
                        "unreadable-piece: the link target is "
                        "not a regular file")
                else:
                    damaged[rel] = (
                        "unreadable-piece: dangling link, the "
                        "link target does not stand")
            elif not target.exists() and \
                    inventory.near_match_note(rel) is not None:
                entries.append(rel)
            continue
        if full.is_file():
            entries.append(rel)
        elif full.is_dir():
            if recognised and rel.rsplit("/", 1)[-1].endswith(".md"):
                entries.append(rel)
                damaged[rel] = (
                    "unreadable-piece: not a regular file")
        elif recognised:
            entries.append(rel)
            damaged[rel] = (
                "unreadable-piece: not a regular file")
    entries.sort()
    return entries, damaged, walk_note, unvisited


def _canonical_paths(root_path, entries, damaged):
    """Group entry paths by the file they reach.

    Returns (canonical, aliases), where canonical lists one entry
    per reached file, in sorted order, and aliases maps each
    canonical entry to every path that reaches the same file. A
    damaged entry is never merged with another path: its own path
    is the piece that stands.
    """
    groups = {}
    for rel in entries:
        if rel in damaged:
            key = "damaged:" + rel
        else:
            try:
                key = str((root_path / rel).resolve())
            except (OSError, RuntimeError):
                key = rel
        groups.setdefault(key, []).append(rel)
    aliases = {}
    canonical = []
    for key in groups:
        paths = sorted(groups[key])
        chosen = paths[0]
        for candidate in paths:
            if not (root_path / candidate).is_symlink():
                chosen = candidate
                break
        aliases[chosen] = tuple(paths)
        canonical.append(chosen)
    canonical.sort()
    return canonical, aliases


def capture_read(root):
    """Walk the root once and build the one CapturedRead of the run.

    Raises UnreadableInputError where the shell cannot produce a
    CapturedRead at all: the root does not stand, or does not stand
    as a directory. Every failure after capture has begun is a
    piece level failure, marked on its piece, and the run still
    completes on the captured pieces.
    """
    root_path = Path(root)
    if not root_path.exists() or not root_path.is_dir():
        raise UnreadableInputError(
            "capture the record tree: root %s: not a readable "
            "directory" % (root,))
    root_resolved = root_path.resolve()
    entries, damaged, walk_note, unvisited = _walk_entries(
        root_path, root_resolved)
    unvisited_set = set(unvisited)
    entries, aliases = _canonical_paths(root_path, entries, damaged)
    classified = []
    for rel in entries:
        found = inventory.classify(rel)
        note = None
        if found is None:
            note = inventory.near_match_note(rel)
        classified.append((rel, found, note))

    size_unknown = []

    def measured_size(rel):
        full = root_path / rel
        try:
            if full.is_dir() and not full.is_symlink():
                return 0
            return full.stat().st_size
        except OSError:
            if rel not in size_unknown:
                size_unknown.append(rel)
            return 0

    # The record part totals, measured in walk order. The piece
    # where a tree limit is crossed, and every piece after it in
    # walk order, stands past the limit and is not read.
    tree_bytes = 0
    tree_files = 0
    cut_paths = []
    cut_kind = None
    last_visited = None
    cutting = False
    for rel, found, note in classified:
        if found is None and note is None:
            continue
        tree_files += 1
        tree_bytes += measured_size(rel)
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
            cut_paths.append(rel)
        else:
            last_visited = rel
    cut_set = set(cut_paths)

    raw = {}
    near_matches = []
    for rel, found, note in classified:
        if found is None:
            if note is not None:
                near_matches.append((rel, note))
            continue
        record_class, step = found
        if rel in damaged:
            size = measured_size(rel)
            text = None
            quality = "unreadable"
            reason = damaged[rel]
        elif rel in unvisited_set:
            size = measured_size(rel)
            text = None
            quality = "over limit"
            reason = unvisited[rel]
        elif rel in cut_set:
            size = measured_size(rel)
            text = None
            quality = "over limit"
            reason = ("over-limit-piece: not read: the %s was "
                      "crossed, with a record part total of %d bytes "
                      "in %d files, and this piece stands past the "
                      "limit in walk order"
                      % (cut_kind, tree_bytes, tree_files))
        else:
            size, text, quality, reason = _read_once(root_path / rel)
        # Content classing, Step 22 only: a piece read in full is
        # reclassed by its text under the Inventory content rule,
        # so a Step 22 gate piece standing under no gate name
        # counts in its content class, and a Step 22 piece named
        # as a gate record with no Keeper content in its text
        # does not. A piece with no text stands in its name class.
        if text is not None:
            content_found = inventory.classify(rel, text)
            if content_found is not None:
                record_class, step = content_found
        identity = inventory.identity_for(record_class, step, rel,
                                          text)
        raw.setdefault(identity, []).append(
            (rel, record_class, step, size, text, quality, reason,
             aliases.get(rel, (rel,))))

    pieces = _merge_identity_groups(raw)
    assembled, single_path = inventory.assemble_metrics_record(pieces)
    if single_path is None:
        singles = [p for p in pieces
                   if p.record_class == CLS_METRICS_SINGLE]
        if singles:
            single_path = singles[0].paths[0]
    texts = [p.text for p in pieces if p.text is not None]
    force = inventory.record_change_force(assembled)
    totals = _inventory_totals(pieces, force)
    return CapturedRead(
        root=str(root), pieces=pieces, inventory_totals=totals,
        latest_timestamp=_latest_timestamp(texts),
        definitions_version=_definitions_version(assembled),
        build_identity=_build_identity(pieces, assembled),
        near_matches=near_matches, assembled_metrics=assembled,
        metrics_single_path=single_path, walk_note=walk_note,
        tree_bytes=tree_bytes, tree_files=tree_files,
        tree_cut_paths=tuple(cut_paths), tree_cut_kind=cut_kind,
        tree_last_visited=last_visited,
        tree_byte_limit=TREE_BYTE_LIMIT,
        tree_file_limit=TREE_FILE_LIMIT,
        record_change_force=force,
        size_unknown_paths=tuple(sorted(size_unknown)))


def _merge_identity_groups(raw):
    """Turn grouped walk entries into Piece values, one per identity.

    An entry with no readable content never merges with another
    entry at its identity and never displaces a sound one: it
    stands as its own piece, marked with its true state. Entries
    whose text carries no substantive content stand apart in the
    same way where a substantive entry stands at the identity,
    and merge by their identical empty form where none does.
    Substantive entries at one identity merge into one piece
    where their texts agree, and yield one piece with no content
    and a disagreement reason where their texts differ.
    """
    pieces = []
    for identity in sorted(raw, key=lambda i: min(x[0] for x in raw[i])):
        group = sorted(raw[identity], key=lambda x: x[0])
        record_class = group[0][1]
        step = group[0][2]
        form = None
        if record_class == CLS_METRICS_SINGLE:
            form = "single page form"
        elif record_class == CLS_METRICS_PAGE:
            form = "split page form"
        for entry in [x for x in group if x[4] is None]:
            pieces.append(Piece(identity, entry[7], entry[1], entry[2],
                                entry[3], None, entry[6], entry[5],
                                form_state=form))
        rest = [x for x in group if x[4] is not None]
        if any(x[4].strip() for x in rest):
            for entry in [x for x in rest if not x[4].strip()]:
                pieces.append(Piece(identity, entry[7], entry[1],
                                    entry[2], entry[3], entry[4],
                                    entry[6], entry[5],
                                    form_state=form))
            standing = [x for x in rest if x[4].strip()]
        elif rest:
            seen_forms = []
            for entry in rest:
                if entry[4] not in seen_forms:
                    seen_forms.append(entry[4])
            for empty_text in seen_forms:
                same = [x for x in rest if x[4] == empty_text]
                paths = tuple(sorted({p for x in same for p in x[7]}))
                first = same[0]
                pieces.append(Piece(identity, paths, first[1],
                                    first[2], first[3], first[4],
                                    None, first[5], form_state=form))
            standing = []
        else:
            standing = rest
        if not standing:
            continue
        paths = tuple(sorted({p for x in standing for p in x[7]}))
        head = standing[0]
        if len(standing) > 1:
            texts = {x[4] for x in standing}
            if len(texts) == 1:
                pieces.append(Piece(identity, paths, record_class,
                                    step, head[3], head[4], None,
                                    head[5], form_state=form))
            else:
                pieces.append(Piece(
                    identity, paths, record_class, step, head[3], None,
                    "not read in full: duplicate content disagreement "
                    "between the paths that yield this piece: "
                    "duplicate identity with differing content, and "
                    "no content from either path is used",
                    "not read in full", form_state=form))
            continue
        pieces.append(Piece(identity, paths, record_class, step,
                            head[3], head[4], head[6], head[5],
                            form_state=form))
    pieces.sort(key=lambda p: p.paths[0])
    return pieces


def _inventory_totals(pieces, force):
    """The inventory totals, recorded during the single walk.

    Expected, found, not found and not yet recordable counts stand
    per record class. Step records are expected once per evidenced
    step. The gate alias classes share one expectation of one gate
    piece per evidenced step, with the steps holding no gate piece
    counted once, on the gate record class. Per build classes are
    expected once. Per round classes are expected at the round
    count the steps evidence, where any round is evidenced.
    """
    totals = {}

    def ensure(record_class):
        return totals.setdefault(
            record_class, {"expected": 0, "found": 0, "not_found": 0,
                           "not_yet_recordable": 0})

    for piece in pieces:
        ensure(piece.record_class)["found"] += 1
    evidenced = sorted({p.step for p in pieces if p.step is not None
                        and p.record_class in (
                            CLS_STEP_RECORD,) + GATE_CLASSES})
    assigned = set()
    if evidenced:
        entry = ensure(CLS_STEP_RECORD)
        entry["expected"] = len(evidenced)
        assigned.add(CLS_STEP_RECORD)
        steps_with_gate = {p.step for p in pieces
                           if p.record_class in GATE_CLASSES
                           and p.step is not None}
        gate_missing = len([s for s in evidenced
                            if s not in steps_with_gate])
        for record_class in GATE_CLASSES:
            entry = ensure(record_class)
            entry["expected"] = entry["found"]
            assigned.add(record_class)
        carrier = ensure(CLS_GATE_RECORD)
        carrier["expected"] = carrier["found"] + gate_missing
    split_only = bool([p for p in pieces
                       if p.record_class == CLS_METRICS_PAGE]) and \
        not [p for p in pieces if p.record_class == CLS_METRICS_SINGLE]
    for record_class in (CLS_PATH_LEDGER, CLS_TIER_RECORD,
                         CLS_METRICS_SINGLE, CLS_DECISION_QUEUE):
        if record_class == CLS_METRICS_SINGLE and split_only:
            continue
        ensure(record_class)["expected"] = 1
        assigned.add(record_class)
    per_round = (CLS_AUDIT_PAPER, CLS_BOARD_MEMBER, CLS_FIX_REGISTER,
                 CLS_DEFECT_REGISTER, CLS_ADJUDICATION, CLS_TRACE,
                 CLS_OTHER_REGISTER)
    total_rounds = sum(_rounds_evidenced(pieces, s) for s in evidenced)
    if total_rounds:
        for record_class in per_round:
            ensure(record_class)["expected"] = total_rounds
            assigned.add(record_class)
    for record_class, entry in totals.items():
        if record_class not in assigned:
            entry["expected"] = entry["found"]
        entry["not_found"] = max(0, entry["expected"] - entry["found"])
    # A class whose creating record change stands NOT IN FORCE
    # carries its expected count under not yet recordable and
    # under no other state. Under the settled mapping in the
    # Inventory every change maps to no record class, so this
    # passage moves no count; the force state is recorded above,
    # not defaulted.
    for number, state in sorted(force.items()):
        if state != "NOT IN FORCE":
            continue
        for record_class in inventory.RECORD_CHANGE_CLASSES.get(
                number, ()):
            entry = totals.get(record_class)
            if entry is None:
                continue
            entry["not_yet_recordable"] += entry["expected"]
            entry["not_found"] = 0
            entry["expected"] = 0
    return totals


def _inside_tree(root, report_path):
    """True where a report destination lies inside the tree read.

    The test is decided on resolved forms, and on the named form,
    and on every prefix of the named form resolved in turn, so a
    relative spelling, a spelling with parent segments, a link
    whose target stands inside the tree, an alias of the root, and
    the root itself given as the destination all count as inside.
    """
    root_resolved = Path(root).resolve()
    destination = Path(report_path)
    try:
        dest_resolved = destination.resolve()
    except (OSError, RuntimeError) as exc:
        raise UsageError("deliver the report: destination %s: %s"
                         % (report_path, exc))
    dest_named = Path(os.path.abspath(str(destination)))
    root_named = Path(os.path.abspath(str(root)))
    for base in (root_resolved, root_named):
        for candidate in (dest_resolved, dest_named):
            if candidate == base or base in candidate.parents:
                return True
    prefix = Path(dest_named.anchor)
    for part in dest_named.parts[1:]:
        prefix = prefix / part
        try:
            resolved_prefix = prefix.resolve()
        except (OSError, RuntimeError) as exc:
            raise UsageError("deliver the report: destination %s: %s"
                             % (report_path, exc))
        if resolved_prefix == root_resolved or \
                root_resolved in resolved_prefix.parents:
            return True
    return False


def deliver_report(text, root, report_path):
    """Deliver the finished report to its one destination.

    With no named file the destination is standard output. With a
    named file the write is a single write of finished text,
    encoded as UTF-8 with the LF line ending. A destination inside
    the tree read is refused. A delivery failure raises UsageError
    in the settled error form, falls back to no other destination,
    leaves no partial file, and leaves a prior file at the
    destination as it stood.
    """
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
    if _inside_tree(root, report_path):
        raise UsageError(
            "deliver the report: destination %s: the destination "
            "lies inside the tree read, which is refused"
            % (report_path,))
    if not destination.parent.exists():
        raise UsageError(
            "deliver the report: destination %s: the parent "
            "directory does not stand" % (report_path,))
    # A destination that already stands in a form other than a
    # regular file cannot take a single write of finished bytes.
    # It is refused here, before any opening that could block
    # without bound, as the delivery failure form states: a usage
    # error, no fallback destination, and the destination left
    # as it stood. A link is judged by the form it points at.
    try:
        standing_mode = os.stat(str(destination)).st_mode
    except FileNotFoundError:
        standing_mode = None
    except OSError as exc:
        raise UsageError("deliver the report: destination %s: %s"
                         % (report_path, exc))
    if standing_mode is not None and \
            not stat.S_ISREG(standing_mode):
        raise UsageError(
            "deliver the report: destination %s: the destination "
            "does not stand as a regular file and cannot be "
            "delivered to as named" % (report_path,))
    data = text.encode("utf-8")
    try:
        handle = os.open(
            str(destination),
            os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NONBLOCK,
            0o666)
    except OSError as exc:
        raise UsageError("deliver the report: destination %s: %s"
                         % (report_path, exc))
    try:
        if not stat.S_ISREG(os.fstat(handle).st_mode):
            raise UsageError(
                "deliver the report: destination %s: the "
                "destination does not stand as a regular file "
                "and cannot be delivered to as named"
                % (report_path,))
        written = os.write(handle, data)
        if written != len(data):
            raise OSError("short write: %d of %d bytes written"
                          % (written, len(data)))
    except UsageError:
        raise
    except OSError as exc:
        raise UsageError("deliver the report: destination %s: %s"
                         % (report_path, exc))
    finally:
        os.close(handle)
