"""Module 2: inventory, part of the shell.

This module gives every file the walk finds its place in the record:
a recognised piece with a record class and, where the name carries
one, a step number; a near match name, listed and never read as the
piece it nearly names; or other material the report does not use.
It also owns the closed name patterns and the gate alias set, the
piece identity rule, the split form assembly of the metrics record,
the record change force reading, and the Step 22 content classing
stated at Margin M4 List 2. It derives no metric, and it holds no
StepUniverse construction: that construction stands in the
Derivation core alone.
"""
import re

from metrics_starter_collector.derivation_core import (
    CLS_ADJUDICATION, CLS_AUDIT_PAPER, CLS_BOARD_MEMBER, CLS_CITATION,
    CLS_COST_LEDGER, CLS_DECISION_QUEUE, CLS_DEFECT_REGISTER,
    CLS_FIX_REGISTER, CLS_GATE_ADJUDICATION, CLS_GATE_RECORD,
    CLS_GATE_RULING, CLS_INSTALL_REGISTER, CLS_METRICS_PAGE,
    CLS_METRICS_SINGLE, CLS_OPENING_RECORD, CLS_OTHER_REGISTER,
    CLS_PATH_LEDGER, CLS_REGATE_RECORD, CLS_ROSTER, CLS_SNAPSHOT,
    CLS_SNAPSHOT_MANIFEST, CLS_STEP_COMPANION, CLS_STEP_RECORD,
    CLS_TIER_RECORD, CLS_TRACE)

# The gate alias set, stated once here. The forms counted as gate
# evidence for a step are the gate record, the gate ruling with its
# round and re-audit variants, the regate record, and the gate
# adjudication. Outcomes are read only from this set.
GATE_ALIAS_CLASSES = (CLS_GATE_RECORD, CLS_GATE_RULING,
                      CLS_REGATE_RECORD, CLS_GATE_ADJUDICATION)

# Files whose whole name, at any depth, settles their class.
_EXACT_NAMES = {
    "PATH-LEDGER.md": CLS_PATH_LEDGER,
    "TIER-RECORD.md": CLS_TIER_RECORD,
    "DECISION-QUEUE.md": CLS_DECISION_QUEUE,
    "DESIGN-BRIEF.md": CLS_CITATION,
    "DESIGN-PLAN.md": CLS_CITATION,
    "NEXT-VERSION-PLAN.md": CLS_CITATION,
    "RECOVERY-RECORD.md": CLS_CITATION,
    "INSTALL-REGISTER.md": CLS_INSTALL_REGISTER,
}

# Suffix forms inside steps/, tried in order. Each entry pairs the
# tail of the file name, after the step-NN- prefix, with its class.
_STEP_SUFFIXES = (
    ("snapshot-manifest.md", CLS_SNAPSHOT_MANIFEST),
    ("gate-record.md", CLS_GATE_RECORD),
    ("regate-record.md", CLS_REGATE_RECORD),
    ("gate-adjudication.md", CLS_GATE_ADJUDICATION),
    ("opening-record.md", CLS_OPENING_RECORD),
    ("roster-artifact.md", CLS_ROSTER),
    ("snapshot.md", CLS_SNAPSHOT),
    ("trace.md", CLS_TRACE),
    ("record.md", CLS_STEP_RECORD),
)

_STEP_PREFIX = re.compile(r"^step-(\d{2})([a-z])?-(.+)$")
_AUDIT_NAME = re.compile(r"^step(\d+)-?(.*)$")
_METRICS_SINGLE_STEM = "build-metrics-record"
_METRICS_PAGE_PREFIX = "build-metrics-record-part-"
_METRICS_PAGE_PREFIXES = ("build-metrics-record-part-",
                          "build-metrics-record-page-")


def _audit_dir_class(base):
    """Class for a file under audit/, or None where it has none."""
    found = _AUDIT_NAME.match(base)
    step = int(found.group(1)) if found else None
    if "fix-register" in base:
        return CLS_FIX_REGISTER, step
    if "defect-register" in base:
        return CLS_DEFECT_REGISTER, step
    if "adjudication" in base:
        return CLS_ADJUDICATION, step
    return CLS_AUDIT_PAPER, step


def _step_file_class(base):
    """Class for a steps/ style name, or None where unrecognised."""
    found = _STEP_PREFIX.match(base)
    if not found:
        return None
    step = int(found.group(1))
    tail = found.group(3)
    if tail.startswith("gate-ruling"):
        return CLS_GATE_RULING, step
    for suffix, record_class in _STEP_SUFFIXES:
        if tail == suffix:
            return record_class, step
    if tail.endswith("-trace.md"):
        return CLS_TRACE, step
    if tail.startswith("board-member-"):
        return CLS_BOARD_MEMBER, step
    if tail.endswith(".md"):
        return CLS_STEP_COMPANION, step
    return None


def _audit_style_class(base):
    """Class for audit forms that stand outside the audit folder."""
    found = re.match(r"^step(\d+)-?(.*)$", base)
    if not found:
        return None
    step = int(found.group(1))
    if "fix-register" in base:
        return CLS_FIX_REGISTER, step
    if "defect-register" in base:
        return CLS_DEFECT_REGISTER, step
    if "adjudication" in base:
        return CLS_ADJUDICATION, step
    return CLS_AUDIT_PAPER, step


# The Step 22 content form, stated at Margin M4 List 2 and in the
# Slice 1 entry: Step 22 is classed by content as that step gate
# record, held by the Release-gate Keeper, not by name alone. The
# two wordings that carry that holding in the records are the held
# by form, "held by the Release-gate Keeper", and the role line
# form, "Release-gate Keeper, Step 22, holding this gate alone".
# Either wording, standing anywhere in the piece text, is the
# content test. A recognised Step 22 piece whose text carries one
# of those wordings classes as the Step 22 gate record, whatever
# record name its file name carries. A Step 22 piece whose file
# name carries the gate record name but whose text carries
# neither wording does not class as a gate record on its name
# alone: it classes as a step companion, the generic recognised
# form for a steps file. Content classing operates only inside
# the recognised set: a name the name rules do not recognise
# stays unrecognised, whatever its text carries, and a call with
# no text stands as the name alone classification.
_STEP22_KEEPER_FORMS = (
    "held by the Release-gate Keeper",
    "Release-gate Keeper, Step 22, holding this gate alone",
)


def _content_class(record_class, step, text):
    """Apply the Step 22 content classing to a name classification."""
    if text is None or step != 22:
        return record_class, step
    for form in _STEP22_KEEPER_FORMS:
        if form in text:
            return CLS_GATE_RECORD, step
    if record_class == CLS_GATE_RECORD:
        return CLS_STEP_COMPANION, step
    return record_class, step


def classify(rel_path, text=None):
    """Return (record_class, step) for a recognised path, else None.

    With no text, the classification is by name alone. With the
    piece text, the Step 22 content classing stated above applies
    to a recognised Step 22 piece, in place of its name result.
    """
    found = _classify_by_name(rel_path)
    if found is None:
        return None
    record_class, step = found
    return _content_class(record_class, step, text)


def _classify_by_name(rel_path):
    """Return the name alone classification for a path, else None.

    The plural collection names, step-NN-records.md and its gate
    form, are not pieces: they name a set, not one record, and this
    function returns None for them before any other rule can take
    them.
    """
    parts = rel_path.split("/")
    base = parts[-1]
    if re.match(r"^step-\d+[a-z]?-(gate-)?records\.md$", base):
        return None
    # The decision queue file stands at the root of the tree with
    # that exact name only, under Margin M4 List 1: a file with
    # that name at another level is not the queue feeder and
    # triggers no D-1 precedence.
    if base == "DECISION-QUEUE.md" and len(parts) != 1:
        return None
    if base in _EXACT_NAMES:
        return _EXACT_NAMES[base], None
    if "cost-ledger" in base or "cost_ledger" in base:
        return CLS_COST_LEDGER, None
    stem = base[:-3] if base.endswith(".md") else base
    if stem == _METRICS_SINGLE_STEM:
        return CLS_METRICS_SINGLE, None
    if base.startswith(_METRICS_PAGE_PREFIXES):
        return CLS_METRICS_PAGE, None
    if parts[0] == "audit":
        return _audit_dir_class(base)
    if parts[0] == "registers":
        if base == "defect-register.md":
            return CLS_DEFECT_REGISTER, None
        if base.endswith(".md"):
            return CLS_OTHER_REGISTER, None
        return None
    stepped = _step_file_class(base)
    if stepped is not None:
        return stepped
    if re.match(r"^step\d", base):
        return _audit_style_class(base)
    return None


# Near match names: a name that nearly names a closed pattern is
# listed as unrecognised beside the pattern it nearly names, is
# never read as that piece, and counts as not found for its class.
_NEAR_MATCHES = (
    (re.compile(r"step-\d+-record"), "steps/step-NN-record.md"),
    (re.compile(r"step-\d+-gate"), "steps/step-NN-gate-record.md"),
    (re.compile(r"path[-_ ]?ledger", re.I), "PATH-LEDGER.md"),
    (re.compile(r"metrics[-_ ]?record", re.I),
     "wiki/wiki/synthesis/build-metrics-record.md"),
    (re.compile(r"step-\d+-trace"), "steps/step-NN-trace.md"),
    (re.compile(r"step-\d+-roster"),
     "steps/step-NN-roster-artifact.md"),
    (re.compile(r"decision[-_ ]?queue", re.I), "DECISION-QUEUE.md"),
    (re.compile(r"decision[-_ ]?queu", re.I), "DECISION-QUEUE.md"),
    (re.compile(r"queue[-_ ]?decision", re.I), "DECISION-QUEUE.md"),
    (re.compile(r"decisions?[-_ ]?queue", re.I), "DECISION-QUEUE.md"),
)


def near_match_note(rel_path):
    """Return the nearest closed pattern note for a name, or None."""
    base = rel_path.split("/")[-1]
    for pattern, note in _NEAR_MATCHES:
        if pattern.search(base):
            if "NN" in note:
                numbered = re.search(r"step-(\d+)", base)
                if numbered:
                    note = note.replace(
                        "NN", numbered.group(1).zfill(2))
            return note
    return None


def identity_for(record_class, step, rel_path, text=None):
    """Piece identity, by record identity and not by path alone.

    The identity joins the record class, the step where the piece
    belongs to one, and the file name form, so two paths that yield
    the same record yield one identity and count once. Where the
    piece text stands, the Step 22 content classing applies to
    the class the identity carries, in the same form as classify.
    """
    record_class, step = _content_class(record_class, step, text)
    base = rel_path.split("/")[-1]
    if step is not None:
        return "%s:%d:%s" % (record_class, step, base)
    return "%s:%s" % (record_class, base)


_PAGE_ORDER = re.compile(r"Page order:\s*(\d+)")


def _page_sort_key(piece):
    """Sort key for one split page: stated order, then path order.

    A page that states its own page order sorts by that order. A
    page that states none sorts after every page that states one,
    in sorted relative path order among its own kind.
    """
    if piece.text:
        stated = _PAGE_ORDER.search(piece.text)
        if stated:
            return (0, int(stated.group(1)), piece.paths[0])
    return (1, 0, piece.paths[0])


def _stated_page_order(piece):
    """Return the page order a piece states for itself, or None."""
    if piece.text:
        stated = _PAGE_ORDER.search(piece.text)
        if stated:
            return int(stated.group(1))
    return None


def assemble_metrics_record(pieces):
    """Assemble the metrics record in its governing physical form.

    Decision D-08. Where a single page piece stands, the single
    page form governs and split pages beside it are not assembled.
    Where only split pages stand, the pages are read together in
    the page order the pages themselves state, or in sorted
    relative path order where no order is stated. A page that
    stands but was not read in full supplies no tables, in the
    same absent form as a missing page. Returns the assembled
    text and the path the assembled record is cited by, or
    (None, None) where no form stands.
    """
    singles = [p for p in pieces
               if p.record_class == CLS_METRICS_SINGLE
               and p.text is not None]
    pages = [p for p in pieces
             if p.record_class == CLS_METRICS_PAGE
             and p.text is not None]
    if singles and pages and any(
            _stated_page_order(piece) == 1 for piece in singles) \
            and any((_stated_page_order(piece) or 0) > 1
                    for piece in pages):
        # A piece at the single page path that states itself as
        # page one, with a later page standing beside it stating a
        # later page order, is page one of a split record, not a
        # standalone single page: it assembles with the other pages
        # in page order. A piece at that path stating no page order,
        # or stating a page order with no later page beside it, is
        # the single page form and governs over split pages beside
        # it.
        ordered = sorted(singles + pages, key=_page_sort_key)
        return "\n".join(p.text for p in ordered), ordered[0].paths[0]
    if singles:
        for piece in singles:
            if piece.text.strip():
                return piece.text, piece.paths[0]
        return singles[0].text, singles[0].paths[0]
    if not pages:
        return None, None
    ordered = sorted(pages, key=_page_sort_key)
    return "\n".join(p.text for p in ordered), ordered[0].paths[0]


_FORM_A_ITEM = re.compile(
    r"^\s*(\d+)\.\s+([^:\n]+):\s*(NOT IN FORCE|IN FORCE)\b")

# The five record change names the force statement may state, by
# change number. Change 1 also carries the longer form the metrics
# record itself uses for the same change.
_RECORD_CHANGE_NAMES = {
    1: ("timestamped state transitions",
        "timestamped state transitions in the path record"),
    2: ("decision queue timestamps and origin",),
    3: ("origin step on findings",),
    4: ("agent-turn and per-agent engagement telemetry",),
    5: ("explicit loop round markers",),
}


def record_change_force(assembled_text):
    """Read the Form A record change statement of a metrics record.

    A Form A statement is a numbered list in the assembled text.
    Each item records a force state only where the name it states
    is the settled name of the change its number names. An item
    naming no settled change, or naming the change of another
    number, records nothing. Prose restatements create no force
    state on their own. Where a number stands twice, the first
    statement governs. Returns a dict from change number to the
    force words stated.
    """
    states = {}
    if not assembled_text:
        return states
    for line in assembled_text.splitlines():
        item = _FORM_A_ITEM.match(line)
        if not item:
            continue
        if item.group(1) != str(int(item.group(1))):
            continue
        number = int(item.group(1))
        names = _RECORD_CHANGE_NAMES.get(number)
        if names is None:
            continue
        stated = " ".join(item.group(2).split()).lower()
        if stated not in names:
            continue
        if number not in states:
            states[number] = item.group(3)
    return states


# The settled mapping from record changes to record classes. Each
# of the five changes creates a field, a timestamping practice, a
# marker or an export inside a record kind the taxonomy classes
# independently of the change, and none creates a record class, so
# each change maps to no class and no header count moves on force
# grounds under this mapping.
RECORD_CHANGE_CLASSES = {1: (), 2: (), 3: (), 4: (), 5: ()}


# ---------------------------------------------------------- instance key
#
# The instance key, under the Spin 772 key rule. An instance is
# named by its step number and, where the file name carries one,
# the single letter instance marker that stands between the step
# number and the rest of the name, as in step-02r-record.md for
# the restart instance R of Step 2. The key is a name form only:
# it is taken from the file name, never from record text, so a
# recycle marker standing inside one record names no new key and
# that record instance counts once, and a step record, a gate
# file, the path ledger and the metrics record that give the same
# step number and the same marker, or no marker, name one and the
# same instance. Two different markers are never merged: figures
# recorded under a replaced or restart marker stay under their
# own key. The plain instance key is "step-N" and a marked
# instance key is "step-N-m", with N the step number with no zero
# padding and m the marker letter in lower case.

_INSTANCE_NAME = re.compile(r"^step-(\d{2})([a-z])?-.+$")


def instance_marker(rel_path):
    """Return the instance marker letter in a step file name, or ""."""
    base = rel_path.split("/")[-1]
    found = _INSTANCE_NAME.match(base)
    if found and found.group(2):
        return found.group(2)
    return ""


def instance_key_for(step, rel_path=None, marker=None):
    """Return the instance key for a step and marker, as a string."""
    if marker is None:
        marker = instance_marker(rel_path) if rel_path else ""
    if marker:
        return "step-%d-%s" % (step, marker.lower())
    return "step-%d" % step


def piece_instance_key(piece):
    """Return the instance key a captured piece belongs to.

    The key is read from the first of the piece paths, in sorted
    order, that carries a step file name form. A piece whose paths
    carry no such form, but which belongs to a step, keys on the
    plain instance of that step. A piece belonging to no step has
    no instance key and this function returns None.
    """
    if piece.step is None:
        return None
    for path in sorted(piece.paths):
        if _INSTANCE_NAME.match(path.split("/")[-1]):
            return instance_key_for(piece.step, path)
    return instance_key_for(piece.step)


def instance_keys(pieces, classes=None):
    """Return the distinct instance keys of pieces, in first seen order.

    Where classes stands, only pieces whose record class stands
    in it are counted. Each distinct key stands once, however many
    pieces or record kinds name it.
    """
    keys = []
    for piece in pieces:
        if classes is not None and piece.record_class not in classes:
            continue
        key = piece_instance_key(piece)
        if key is not None and key not in keys:
            keys.append(key)
    return keys


# --------------------------------------------------- gate outcome reading
#
# The gate outcome reading this slice delivers. It reads gate
# files under the gate alias set above only: the gate record, the
# gate ruling with its round and re-audit variants, and the regate
# record are the counted sources; the gate adjudication is read
# as evidence beside them and is never a counted source, never a
# separate gate, and an outcome standing only in an adjudication
# enters no count. The Step 22 content classing above applies to
# the class each source stands in, in the same form as classify.
# Step records and their gate histories are not gate files and
# are never read here, and a name outside the alias set, however
# near, is not read as a gate file: such a piece is reported in
# the near match sources of its step instance only.
#
# The reading supplies facts and derives no metric. Its result,
# from gate_outcome_facts, is a dict keyed by instance key in the
# form above. Each value is a dict with these fields:
#   step: the step number, as an int.
#   instance: the instance marker letter, or "" for the plain
#     instance.
#   instance_key: the instance key string.
#   sources: a tuple of source dicts, one per counted or evidence
#     gate piece for the instance, in sorted path order. Each
#     source dict carries record_class, path (the first path of
#     the piece), closure_state (the exact token after the
#     Closure state label, as recorded, or None where the piece
#     states none), and first_ruling_outcome (the word after the
#     First ruling outcome label, one of Go, Hold, Recycle or
#     Kill, or None where the piece states none).
#   counted_sources: the sources tuple with every adjudication
#     source removed.
#   adjudication_sources: the sources whose class is the gate
#     adjudication.
#   adjudication_only: True where an adjudication source stands
#     and no counted source stands.
#   closure_states: the distinct closure_state tokens of the
#     counted sources, in source order, as recorded, with no
#     token normalised or dropped: a token outside the settled
#     closure vocabulary stands here in its recorded form.
#   first_closure_state: the closure_state of the first counted
#     source in sorted path order, or None.
#   first_ruling_outcomes: the distinct first ruling outcome
#     words of the counted sources, in source order.
#   first_ruling_outcome: the first such word, or None.
#   both_names: True where a gate record source and a gate
#     ruling source both stand among the counted sources.
#   disagreement: True where the gate record and gate ruling
#     sources of the instance state different recorded forms,
#     in closure_state or in first_ruling_outcome. The forms are
#     stated and never silently resolved. A regate source states
#     a later ruling in a sequence and never by itself makes a
#     disagreement, and an adjudication source never does.
#   disagreement_forms: the distinct recorded forms behind a
#     disagreement, closure states first, in source order.
#   recycled: True where a regate source stands for the instance
#     or a counted source text carries a recycle marker. A
#     recycled instance still yields this one key and one entry.
#   near_match_sources: a tuple of source dicts for pieces of
#     this step that are classed as step companions and whose
#     names begin with the gate stem but stand outside the alias
#     set, in the same source dict form, listed beside the
#     counted sources and never counted themselves.
#   missing_gate: True where no counted source and no
#     adjudication source stands for the instance, which is the
#     form an entry takes where only near match sources stand.

GATE_COUNTED_CLASSES = (CLS_GATE_RECORD, CLS_GATE_RULING,
                        CLS_REGATE_RECORD)

_CLOSURE_STATE = re.compile(r"Closure state:\s*([A-Za-z0-9][A-Za-z0-9-]*)")
_FIRST_RULING_OUTCOME = re.compile(
    r"First ruling outcome:\s*(Go|Hold|Recycle|Kill)\b")
_RECYCLE_MARKER = re.compile(r"\brecycl", re.I)


def _gate_source(piece, record_class):
    """One gate source dict, read from a piece in its held form."""
    text = piece.text or ""
    closure = _CLOSURE_STATE.search(text)
    outcome = _FIRST_RULING_OUTCOME.search(text)
    return {
        "record_class": record_class,
        "path": piece.paths[0] if piece.paths else "",
        "closure_state": closure.group(1) if closure else None,
        "first_ruling_outcome": outcome.group(1) if outcome else None,
    }


def gate_outcome_facts(pieces):
    """Read the gate outcome facts of a capture, by instance key.

    Pieces stand as the capture holds them: a piece with no text
    supplies a source with no closure state and no outcome word.
    Pieces belonging to no step, and pieces in no class this
    reading names, supply no entry.
    """
    grouped = {}
    order = []
    for piece in pieces:
        if piece.step is None:
            continue
        record_class, _step = _content_class(
            piece.record_class, piece.step, piece.text)
        is_gate = record_class in GATE_ALIAS_CLASSES
        is_near = False
        if not is_gate and record_class == CLS_STEP_COMPANION:
            base = piece.paths[0].split("/")[-1] if piece.paths else ""
            tail = _STEP_PREFIX.match(base)
            if tail and tail.group(3).startswith("gate-"):
                is_near = True
        if not is_gate and not is_near:
            continue
        key = piece_instance_key(piece)
        if key not in grouped:
            grouped[key] = {"sources": [], "near": []}
            order.append(key)
        if is_gate:
            grouped[key]["sources"].append(
                (_gate_source(piece, record_class), piece))
        else:
            grouped[key]["near"].append(_gate_source(piece, record_class))
    facts = {}
    for key in order:
        held = grouped[key]
        held["sources"].sort(key=lambda item: item[0]["path"])
        sources = tuple(source for source, _piece in held["sources"])
        counted = tuple(s for s in sources
                        if s["record_class"] != CLS_GATE_ADJUDICATION)
        adjudication = tuple(s for s in sources
                             if s["record_class"] == CLS_GATE_ADJUDICATION)
        closure_states = []
        for source in counted:
            token = source["closure_state"]
            if token is not None and token not in closure_states:
                closure_states.append(token)
        outcomes = []
        for source in counted:
            word = source["first_ruling_outcome"]
            if word is not None and word not in outcomes:
                outcomes.append(word)
        named = [s for s in counted
                 if s["record_class"] in (CLS_GATE_RECORD, CLS_GATE_RULING)]
        named_closures = {s["closure_state"] for s in named
                          if s["closure_state"] is not None}
        named_outcomes = {s["first_ruling_outcome"] for s in named
                          if s["first_ruling_outcome"] is not None}
        disagreement = len(named_closures) > 1 or len(named_outcomes) > 1
        disagreement_forms = []
        if disagreement:
            for source in named:
                for value in (source["closure_state"],
                              source["first_ruling_outcome"]):
                    if value is not None and \
                            value not in disagreement_forms:
                        disagreement_forms.append(value)
        recycled = any(s["record_class"] == CLS_REGATE_RECORD
                       for s in counted) or any(
            piece.text and _RECYCLE_MARKER.search(piece.text)
            for _source, piece in held["sources"]
            if piece.record_class != CLS_GATE_ADJUDICATION)
        first_piece_step = None
        marker = ""
        if held["sources"]:
            first_piece_step = held["sources"][0][1].step
            marker = instance_marker(held["sources"][0][0]["path"])
        elif held["near"]:
            marker = instance_marker(held["near"][0]["path"])
        step = first_piece_step
        if step is None:
            digits = re.search(r"step-(\d+)", key)
            step = int(digits.group(1)) if digits else None
        facts[key] = {
            "step": step,
            "instance": marker,
            "instance_key": key,
            "sources": sources,
            "counted_sources": counted,
            "adjudication_sources": adjudication,
            "adjudication_only": bool(adjudication) and not counted,
            "closure_states": tuple(closure_states),
            "first_closure_state": counted[0]["closure_state"]
                if counted else None,
            "first_ruling_outcomes": tuple(outcomes),
            "first_ruling_outcome": outcomes[0] if outcomes else None,
            "both_names": any(
                s["record_class"] == CLS_GATE_RECORD for s in counted)
                and any(s["record_class"] == CLS_GATE_RULING
                        for s in counted),
            "disagreement": disagreement,
            "disagreement_forms": tuple(disagreement_forms),
            "recycled": recycled,
            "near_match_sources": tuple(
                sorted(held["near"], key=lambda s: s["path"])),
            "missing_gate": not sources,
        }
    return facts


# The same reading under its plain name, for callers that name
# the operation rather than the facts it returns.
read_gate_outcomes = gate_outcome_facts
