"""Module 3: derivation core.

Pure component. Receives one CapturedRead and returns one ReportModel.
Never touches the filesystem, never reads a clock, never uses
randomness. The five core types live here: CapturedRead, Piece,
StepUniverse, DerivationResult and ReportModel.

Slice 1 form: the tracer derivations for E-1, E-2 and Q-4 stand in
full on the one capture, the T-1 refusal stands in its date only
form, the D-1 row derives from the assembled metrics record under
the split form assembly, and every other row stands as a refusal
under its named rule where its feeder does not carry it further.

Slice 2 form: the data quality entries, the coverage partial
marking and the run cost line derive from the piece states the
one capture carries, in the forms the capture landed them:
malformed, truncated in its marked and signal forms, over
limit, unreadable, and the duplicate identity disagreement.
No derivation in this module reads the tree again.
"""
import re
from dataclasses import dataclass, field
from datetime import datetime

STARTER_ORDER = ["T-1", "T-2", "T-4", "T-7", "E-1", "E-2", "E-3", "E-4",
                 "F-2", "Q-1", "Q-3", "Q-4", "D-1", "B-1", "B-2", "B-3",
                 "B-4"]

REASON_CODES = ["missing-field", "no-feeder-record", "date-only-form",
                "no-post-triage-breakdown", "no-measurement-basis",
                "truncated-no-correcting-record", "record-disagrees",
                "unreconciled-figure", "unknown-definitions-version",
                "no-named-rule", "partial-span", "governing-scale-conflict",
                "over-limit-piece", "malformed-piece", "unreadable-piece"]

QUALITY_STATES = ("truncated", "malformed", "over limit", "unreadable")

CLS_PATH_LEDGER = "path ledger"
CLS_TIER_RECORD = "tier record"
CLS_DECISION_QUEUE = "decision queue"
CLS_CITATION = "citation target"
CLS_STEP_RECORD = "step record"
CLS_OPENING_RECORD = "opening record"
CLS_ROSTER = "roster artifact"
CLS_SNAPSHOT = "snapshot"
CLS_SNAPSHOT_MANIFEST = "snapshot manifest"
CLS_TRACE = "trace record"
CLS_GATE_RECORD = "gate record"
CLS_GATE_RULING = "gate ruling"
CLS_REGATE_RECORD = "regate record"
CLS_GATE_ADJUDICATION = "gate adjudication"
CLS_BOARD_MEMBER = "board member"
CLS_STEP_COMPANION = "step companion"
CLS_AUDIT_PAPER = "audit paper"
CLS_FIX_REGISTER = "fix register"
CLS_DEFECT_REGISTER = "defect register"
CLS_ADJUDICATION = "adjudication"
CLS_INSTALL_REGISTER = "install register"
CLS_COST_LEDGER = "cost ledger"
CLS_METRICS_SINGLE = "metrics record"
CLS_METRICS_PAGE = "metrics record page"
CLS_OTHER_REGISTER = "register"

GATE_CLASSES = (CLS_GATE_RECORD, CLS_GATE_RULING, CLS_REGATE_RECORD,
                CLS_GATE_ADJUDICATION)

FEEDER_MAP = {
    "T-1": ("path ledger transition log",),
    "T-2": ("path ledger transition log",),
    "T-4": ("path ledger banked states", "decision queue file"),
    "T-7": ("gate verdict records", "step records"),
    "E-1": ("step records", "roster artifacts"),
    "E-2": ("step records", "roster artifacts"),
    "E-3": ("cost ledger token figures",),
    "E-4": ("cost ledger money figures", "step records"),
    "F-2": ("gate records", "gate rulings", "gate adjudications"),
    "Q-1": ("audit round records", "gate adjudications"),
    "Q-3": ("defect registers", "audit records"),
    "Q-4": ("first trace records", "gate records"),
    "D-1": ("metrics record",),
    "B-1": ("metric rows T-1 and T-2",),
    "B-2": ("cost ledger money figures", "cost ledger token figures"),
    "B-3": ("metric rows T-1 and T-2",),
    "B-4": ("metric rows T-1 and T-2",),
}

D1_FEEDER_CONDITION = (
    "metrics record decision table only, and only where no "
    "DECISION-QUEUE.md file in the named form stands, under decision "
    "D-09 as shrunk by proposal WV-12; where such a queue file "
    "stands, the queue file is the feeder and the decision table is "
    "the cross check")

METRICS_CANONICAL_PATH = "wiki/wiki/synthesis/build-metrics-record.md"
COST_LEDGER_PATH = "registers/cost-ledger.md"


@dataclass
class Piece:
    identity: str
    paths: tuple
    record_class: str
    step: object
    size: int
    text: object
    not_read_reason: object
    quality_state: object
    form_state: object = None
    encoding_state: str = "utf-8"
    line_state: str = "within limit"


@dataclass
class CapturedRead:
    root: str
    pieces: list
    inventory_totals: dict
    latest_timestamp: object
    definitions_version: object
    build_identity: object = None
    near_matches: list = field(default_factory=list)
    assembled_metrics: object = None
    metrics_single_path: object = None
    walk_note: object = None
    tree_bytes: int = 0
    tree_files: int = 0
    tree_cut_paths: tuple = ()
    tree_cut_kind: object = None
    tree_last_visited: object = None
    tree_byte_limit: int = 25000000
    tree_file_limit: int = 2000
    record_change_force: dict = field(default_factory=dict)
    size_unknown_paths: tuple = ()

    def pieces_of(self, *classes):
        return [p for p in self.pieces if p.record_class in classes]

    def texts_of(self, *classes):
        return [(p, p.text) for p in self.pieces_of(*classes)
                if p.text is not None]

    def first_path(self, *classes):
        found = self.pieces_of(*classes)
        return found[0].paths[0] if found else None

    def step_pieces(self, step, *classes):
        return [p for p in self.pieces_of(*classes) if p.step == step]


@dataclass
class StepUniverse:
    evidenced: tuple
    ledger: tuple
    metrics: tuple
    disagreements: tuple
    metrics_count_claim: object = None
    instances: tuple = ()


@dataclass
class DerivationResult:
    code: str
    verdict: str
    figures: str
    denominator: str
    pointer: str
    shows: object = None
    code_token: object = None
    follows: object = None
    statement: object = None
    derived_from: object = None
    rule_name: str = ""
    numerator: object = None
    coverage: object = None
    broken_link: object = None
    form_required: object = None
    form_held: object = None
    bound: object = None

    def reason_text(self):
        if self.broken_link is not None or self.form_required is not None \
                or self.form_held is not None:
            follows = self.follows or ""
            token = self.code_token or ""
            if token and follows.lower().startswith(token.lower()):
                follows = follows[len(token):].lstrip()
            second = (token + " " + follows).strip() if token else follows
            anatomy = ("broken link, %s; form required, %s; form held, %s"
                       % (self.broken_link or "",
                          self.form_required or "",
                          self.form_held or ""))
            return ("What the record shows: " + anatomy +
                    " What follows: " + second)
        if self.shows is None:
            return None
        follows = self.follows or ""
        token = self.code_token or ""
        if token and follows.lower().startswith(token.lower()):
            follows = follows[len(token):].lstrip()
        second = (token + " " + follows).strip() if token else follows
        return ("What the record shows: " + self.shows +
                " What follows: " + second)


@dataclass
class ReportModel:
    header_lines: list
    coverage: str
    inventory_lines: list
    results: list
    data_quality: list
    no_usable: bool = False
    run_cost_line: object = None


# ------------------------------------------------------------ helpers

_FULL_STAMP = re.compile(r"(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})")
_ANY_STAMP = re.compile(r"(\d{4})-(\d{2})-(\d{2})"
                        r"(?:[ T](\d{2}):(\d{2}))?")


def _fmt_num(value):
    if value == int(value):
        return str(int(value))
    return ("%.2f" % value).rstrip("0").rstrip(".")


def _median(values):
    """The D-1 median: the middle value where the count is odd, and
    the lower of the two middle values where the count is even. The
    median is never formed as a mean of the two middle values.
    """
    ordered = sorted(values)
    count = len(ordered)
    if count == 0:
        return None
    mid = count // 2
    if count % 2:
        return ordered[mid]
    return ordered[mid - 1]


def _stamp_value(text):
    """Parse one timestamp cell: datetime, the word date, or None."""
    text = (text or "").strip()
    m = _FULL_STAMP.search(text)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)),
                            int(m.group(3)), int(m.group(4)),
                            int(m.group(5)))
        except ValueError:
            return None
    if re.search(r"\d{4}-\d{2}-\d{2}", text):
        return "date"
    return None


def _span_reversed(first, second):
    """The shared span order check, in one form for every locus.

    A span stands reversed where its closing instant stands
    earlier than its opening instant. Under the strictness
    standard at D4R-03 a figure counts only where it is measured
    and in the form the definition requires, and a reversed span
    is not a duration in any form the definitions require, so a
    reversed span forms no duration at either locus that forms
    one: the transition series in _time_series and the decision
    item latency here. The affected unit fails on the reversed
    condition, is named with that condition, and is excluded
    from every figure its row forms.
    """
    return isinstance(first, datetime) and \
        isinstance(second, datetime) and second < first


def _item_latency_hours(item):
    if not isinstance(item, dict):
        return None
    raised = item.get("raised_dt") or _stamp_value(item.get("raised"))
    ruled = item.get("ruled_dt") or _stamp_value(item.get("ruled"))
    if isinstance(raised, datetime) and isinstance(ruled, datetime):
        if _span_reversed(raised, ruled):
            return None
        return (ruled - raised).total_seconds() / 3600.0
    return None


def _item_span_reversed(item):
    """Whether one decision item stands reversed under the check."""
    if not isinstance(item, dict):
        return False
    raised = item.get("raised_dt") or _stamp_value(item.get("raised"))
    ruled = item.get("ruled_dt") or _stamp_value(item.get("ruled"))
    return _span_reversed(raised, ruled)


def _each_step(steps):
    steps = sorted(steps)
    if not steps:
        return "none"
    return ", ".join("Step %d" % s for s in steps)


def _named_steps(steps):
    return _each_step(steps)


def _search_int(pattern, text):
    m = re.search(pattern, text or "", re.I)
    return int(m.group(1)) if m else None


def _refusal(code, verdict, figures, denominator, pointer, shows,
             token, follows, rule_name, statement=None, broken=None,
             required=None, held=None):
    return DerivationResult(code, verdict, figures, denominator,
                            pointer, shows=shows, code_token=token,
                            follows=follows, statement=statement,
                            rule_name=rule_name, broken_link=broken,
                            form_required=required, form_held=held)


POINTER_PROSE = {
    "T-1": "the path ledger transition entries",
    "T-2": "the path ledger transition entries",
    "T-4": "the path ledger BANKED entries and the decision table "
           "row for each item counted",
    "T-7": "the loop round table and the verdict records for each "
           "loop step",
    "E-1": "the step record and roster for each step counted",
    "E-2": "the roster and the step record for each step counted",
    "E-3": "the place inside the root where a cost ledger would "
           "stand, stated as looked for and not found",
    "E-4": "the cost ledger entry or the step record budget position "
           "for each step counted",
    "F-2": "the gate record or gate ruling carrying each first "
           "ruling counted",
    "Q-1": "the round record, or a record the round record names, "
           "for each round counted",
    "Q-3": "the fix and defect register entries",
    "Q-4": "the first trace record for each step counted",
    "D-1": "the decision table inside the root, the allowed feeder",
    "B-1": "the step table rows and the build summary, with the "
           "closing gate ruling for the last step",
    "B-2": "the place inside the root where a cost ledger would "
           "stand, stated as looked for and not found, with step "
           "records named as context only",
    "B-3": "the step table rows, stated as looked for and not "
           "formable, and the build summary",
    "B-4": "the step table rows, stated as looked for and not "
           "formable, and the build summary",
}

Q4_POINTER_PROSE = (
    "the first trace record for each step counted, in the forms the "
    "named evidence set states: Step 6 gate record, Step 8 gate "
    "record, Step 19 Purple paper, Step 20 gate ruling, and the "
    "Step 13 trace record for the excepted contribution")


_GATE_PATH_FORM = re.compile(r"^(.*)step-(\d+)-gate-(?:record|ruling)\.md$")


def _pointer(code, actual, captured=None):
    """Compose a pointer: the definition prose, then the record path.

    A gate file path stands in the gate record form of its step,
    whichever of the two gate names the tree uses, so the pointer
    states the same record in both gate name shapes.
    """
    prose = POINTER_PROSE.get(code, "")
    if actual:
        gate_form = _GATE_PATH_FORM.match(str(actual))
        if gate_form:
            actual = "%sstep-%s-gate-record.md" % (
                gate_form.group(1), gate_form.group(2))
    if code == "Q-4" and captured is not None and _q4_named_set(captured):
        prose = Q4_POINTER_PROSE
    if not prose:
        return actual or ""
    path = actual or ""
    if path and not path.endswith(".md"):
        if captured is not None and captured.assembled_metrics:
            path = METRICS_CANONICAL_PATH
        else:
            path = ""
    if path and path not in prose:
        return prose + " (" + path + ")"
    return prose


def _steps_phrase(steps):
    """Golden step list phrase: Steps 6, 8, 19 and 20 form."""
    steps = sorted(steps)
    if not steps:
        return "no steps"
    if len(steps) == 1:
        return "Step %d" % steps[0]
    names = [str(step) for step in steps]
    return "Steps " + ", ".join(names[:-1]) + " and " + names[-1]


def _names_phrase(names):
    names = list(names)
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def _held_join(clauses):
    """Join held clauses in the golden list form: comma joins, with
    an and before the last clause where more than one stands."""
    clauses = [clause for clause in clauses if clause]
    if len(clauses) <= 1:
        return "".join(clauses)
    return ", ".join(clauses[:-1]) + ", and " + clauses[-1]


def _metrics_step_table(captured):
    """Step table rows of the assembled metrics record, by step.

    A row stands where a table line opens with a numbered step cell;
    its cells stand in table order. No row stands on a tree whose
    metrics record carries no step table in this form.
    """
    rows = {}
    text = captured.assembled_metrics or ""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 9:
            continue
        m = re.match(r"(\d+)\.", cells[0])
        if m:
            rows[int(m.group(1))] = cells
    return rows


def _metrics_section(text, heading):
    """Return one headed section of a record text, or an empty text."""
    if not text:
        return ""
    lowered = text.lower()
    at = lowered.find(heading.lower())
    if at < 0:
        return ""
    tail = text[at:]
    nxt = tail.find("\n## ", len(heading))
    if nxt > 0:
        tail = tail[:nxt]
    return tail


def _quality_code(piece):
    state = (piece.quality_state or "").lower()
    if state == "malformed":
        return "malformed-piece"
    if state == "over limit":
        return "over-limit-piece"
    if state == "unreadable":
        return "unreadable-piece"
    if state == "truncated":
        return "truncated-no-correcting-record"
    reason = (piece.not_read_reason or "").lower()
    if "malformed" in reason:
        return "malformed-piece"
    if "over limit" in reason or "past the limit" in reason:
        return "over-limit-piece"
    if "unreadable" in reason or "not a regular file" in reason:
        return "unreadable-piece"
    if "disagreement" in reason:
        return "record-disagrees"
    return "unreadable-piece"


def _piece_not_read_in_full(piece):
    """True where the capture does not hold the piece read in full.

    The capture states this in one of two landed forms: no text
    stands for the piece, or a quality state stands beside the
    piece (one of the four damage states, or the not read in full
    state the duplicate identity form carries).
    """
    return piece.text is None or piece.quality_state is not None


def _piece_state_word(piece):
    """The inventory state word for one piece, as the capture holds it."""
    if piece.quality_state:
        return piece.quality_state
    if piece.text is None:
        return "not read in full"
    return "read in full"


def _reason_detail(piece):
    """The capture reason for a piece, with its code prefix removed.

    Capture reasons stand in the form code, colon, plain detail.
    The detail alone may stand in the first part of a two part
    form entry, where no code may stand; the code itself is
    stated once, at the start of the second part.
    """
    reason = (piece.not_read_reason or "").strip()
    head, sep, tail = reason.partition(": ")
    if sep and (head in REASON_CODES or head.endswith("-piece")):
        return tail.strip()
    return reason


def _piece_over_limit_not_read(piece):
    """True where a piece stands not read past a limit.

    The piece carries no text in the capture and its capture
    state is the over limit state, on any limit route: the
    single piece file or line limit, the tree byte or file
    limit, or the whole walk bound. Other not read states, the
    malformed, unreadable, truncated and duplicate disagreement
    states, stand apart and keep their own handling.
    """
    return _piece_not_read_in_full(piece) and \
        _quality_code(piece) == "over-limit-piece"


def _limit_naming(piece):
    """Name one over limit piece with the bound that stopped it.

    The naming states the piece path and the capture reason
    detail, which names the limit that stopped the reading, in
    the form the WV2-09 bound naming duty requires: the bound
    and the piece, both named, on the row that rests on it.
    """
    path = piece.paths[0] if piece.paths else piece.identity
    detail = _reason_detail(piece)
    if detail:
        return "%s, which stands not read past a limit: %s" \
            % (path, detail)
    return "%s, which stands not read past a limit" % path


def _unread_staffing_pieces(captured, step):
    """The staffing feeder pieces of one step not read past a limit."""
    return [piece for piece in
            captured.step_pieces(step, *_STAFFING_CLASSES)
            if _piece_over_limit_not_read(piece)]


def _walk_order_sample(captured, piece):
    """The A7-4 walk order sample for a capture cut by a limit.

    Names the limit that cut the capture, the last visited path,
    and the pieces visited before this piece in sorted path
    order, and states the bias direction in plain words: a cut
    in walk order leaves the later paths not read.
    """
    detail = _reason_detail(piece)
    if piece.paths[0] in captured.tree_cut_paths and \
            captured.tree_cut_kind:
        limit_phrase = "the " + captured.tree_cut_kind
        last_visited = captured.tree_last_visited or "none stated"
    elif "whole walk bound" in detail:
        limit_phrase = "the whole walk bound of 10000 entries"
        last_visited = None
    elif "line limit" in detail:
        limit_phrase = "the line limit of 65536 bytes"
        last_visited = None
    else:
        limit_phrase = "the file limit of 1000000 bytes"
        last_visited = None
    index = None
    for at, held in enumerate(captured.pieces):
        if held is piece:
            index = at
            break
    if index is None:
        for at, held in enumerate(captured.pieces):
            if held.paths and held.paths[0] == piece.paths[0]:
                index = at
                break
    before = []
    if index:
        before = [held.paths[0] for held in captured.pieces[:index]
                  if held.paths]
    if last_visited is None:
        last_visited = before[-1] if before else \
            "none, this piece stands first in walk order"
    sample = ", ".join(before[:8]) if before else "none"
    return ("walk order sample: the limit that cut the capture is "
            "%s; the last visited path is %s; pieces visited before "
            "this piece in sorted path order: %s; bias direction: "
            "a cut in walk order biases the capture toward the "
            "pieces earlier in sorted path order, and the pieces "
            "later in that order are the ones left not read"
            % (limit_phrase, last_visited, sample))


# ------------------------------------------------------- step universe

# The classes counted as universe evidence: the step record and
# the gate alias set, gate record, gate ruling, regate record and
# gate adjudication, the same set the Inventory names as its gate
# alias classes. The construction classes nothing by name itself:
# it reads the record class the Inventory assigned at capture, so
# a Step 22 piece the Inventory classed by content as that step
# gate record counts here under that same class, and a Step 22
# piece it classed as a step companion does not.
_UNIVERSE_CLASSES = (CLS_STEP_RECORD, CLS_GATE_RECORD, CLS_GATE_RULING,
                     CLS_REGATE_RECORD, CLS_GATE_ADJUDICATION)


_INSTANCE_NAME_FORM = re.compile(r"^step-(\d{2})([a-z])?-.+$")


def _piece_instance_key(piece):
    """The step instance key a piece belongs to, in name form only.

    The key is the step number and, where a file name of the piece
    carries one, the single letter instance marker that stands
    between the step number and the rest of the name, as the Spin
    772 key states: a restart suffix names a separate instance, a
    recycle marker inside one record names no new key, and two
    namings with the same step number and the same marker, or no
    marker, name one and the same instance across record kinds.
    """
    if piece.step is None:
        return None
    for path in sorted(piece.paths):
        found = _INSTANCE_NAME_FORM.match(path.split("/")[-1])
        if found and int(found.group(1)) == piece.step:
            marker = found.group(2)
            if marker:
                return "step-%d-%s" % (piece.step, marker)
            return "step-%d" % piece.step
    return "step-%d" % piece.step


def _instance_label(key):
    """The plain label of one instance key: Step N, or the marked form."""
    found = re.match(r"step-(\d+)(?:-([a-z]))?$", key or "")
    if not found:
        return key or ""
    if found.group(2):
        return "Step %s instance %s" % (found.group(1),
                                        found.group(2).upper())
    return "Step %s" % found.group(1)


def build_step_universe(captured):
    """Build the one StepUniverse from the one CapturedRead."""
    evidenced = set()
    instance_keys = []
    for piece in captured.pieces:
        if piece.step is not None and \
                piece.record_class in _UNIVERSE_CLASSES:
            evidenced.add(piece.step)
            key = _piece_instance_key(piece)
            if key is not None and key not in instance_keys:
                instance_keys.append(key)
    instance_keys.sort(key=lambda k: (int(re.match(r"step-(\d+)", k).group(1)),
                                      k))
    ledger_steps = set()
    for _piece, text in captured.texts_of(CLS_PATH_LEDGER):
        m = re.search(r"Steps stated:\s*([0-9,\s]+?)(?:\.|\n|$)", text)
        if m:
            body = m.group(1)
            span = re.search(r"(\d+)\s+to\s+(\d+)", body)
            if span:
                for n in range(int(span.group(1)),
                               int(span.group(2)) + 1):
                    ledger_steps.add(n)
            for tok in body.split(","):
                tok = tok.strip()
                if tok.isdigit():
                    ledger_steps.add(int(tok))
        for m in re.finditer(r"Step (\d+)\b", text):
            ledger_steps.add(int(m.group(1)))
    metrics_steps = set()
    if captured.assembled_metrics:
        text = captured.assembled_metrics
        for pattern in (r"^\|\s*(\d+)\.\s",
                        r"Step (\d+) closing entry",
                        r"Step (\d+) row\."):
            for m in re.finditer(pattern, text, re.M):
                metrics_steps.add(int(m.group(1)))
    claim = None
    if captured.assembled_metrics:
        m = re.search(r"step universe as (\d+) steps?",
                      captured.assembled_metrics, re.I)
        if m:
            claim = int(m.group(1))
    disagreements = []
    if ledger_steps and ledger_steps != evidenced:
        disagreements.append(
            "the path ledger states steps %s while step records and "
            "gate files evidence steps %s"
            % (_each_step(ledger_steps), _each_step(evidenced)))
    if metrics_steps and not metrics_steps.issubset(
            evidenced | ledger_steps):
        disagreements.append(
            "the metrics record states steps %s beyond the evidenced "
            "universe"
            % _each_step(metrics_steps - evidenced - ledger_steps))
    if claim is not None and claim != len(evidenced):
        name = "build-metrics-record.md"
        if captured.metrics_single_path:
            name = str(captured.metrics_single_path).rsplit("/", 1)[-1]
        ledger_clause = ""
        if captured.pieces_of(CLS_PATH_LEDGER):
            ledger_clause = " and stated in PATH-LEDGER.md"
        disagreements.append(
            "the metrics record in %s states the step universe as "
            "%d steps, which disagrees with the step universe of %d "
            "steps evidenced by step records and gate files%s; "
            "neither count is picked as the count, and derivations "
            "and denominators are computed on the evidenced universe"
            % (name, claim, len(evidenced), ledger_clause))
    return StepUniverse(tuple(sorted(evidenced)),
                        tuple(sorted(ledger_steps)),
                        tuple(sorted(metrics_steps)),
                        tuple(disagreements), claim,
                        tuple(instance_keys))


def _known_version(version):
    if version is None:
        return True
    return ("SHA-256" in version and "bytes" in version and
            re.search(r"[0-9a-fA-F]{64}", version) is not None)


def _feeder_stands(captured, code):
    if code in ("E-1", "E-2"):
        return bool(captured.pieces_of(CLS_STEP_RECORD, CLS_ROSTER,
                                       CLS_STEP_COMPANION))
    if code == "Q-4":
        found, _sources, _styles = _first_traces(captured)
        return bool(found)
    return bool(captured.pieces)


def _unknown_version_result(captured, code, denominator, pointer):
    version = captured.definitions_version
    return _refusal(
        code, "present but not derivable", "no figure stands",
        denominator, pointer,
        shows="the metrics record states definitions version %s, "
              "which is not a version the settled definitions "
              "recognise, and feeder records for this metric stand "
              "in the capture" % version,
        token="unknown-definitions-version",
        follows="the derivation is refused on the unknown version "
                "ground while feeder records stand, so no figure "
                "stands for this row",
        rule_name="WV-2 unknown definitions version rule")


# ------------------------------------------------------- cross check

def _metrics_record_name(captured):
    """The file name the assembled metrics record is cited by."""
    if captured.metrics_single_path:
        return str(captured.metrics_single_path).rsplit("/", 1)[-1]
    return "build-metrics-record.md"


def _universe_claim_statement(captured, universe):
    """The WV-4 statement for a row whose denominator rests on the
    step universe, where the metrics record states a different
    universe count: the disagreement stands stated, neither count
    is picked, and the contested instance stands included in the
    evidenced universe under the bridge rule, its figures carried
    and not discarded, under decisions D-18 and D-02.
    """
    claim = universe.metrics_count_claim
    if claim is None or claim == len(universe.evidenced):
        return None
    evidenced = sorted(universe.evidenced)
    contested = evidenced[claim:] if 0 < claim < len(evidenced) else []
    text = ("record disagrees: %s states the step universe as %d "
            "steps, while step records and gate files evidence %d "
            "steps; neither count is picked as the count, and "
            "derivations and denominators are computed on the "
            "evidenced universe"
            % (_metrics_record_name(captured), claim, len(evidenced)))
    if contested:
        text += (", with the contested instance %s included in "
                 "that universe and its figures carried, not "
                 "discarded" % _each_step(contested))
    return text


def _e1_figure_statement(captured, covered):
    """The D-18 and CA-1 statement for E-1, where the metrics record
    states an E-1 figure for a step that disagrees with the feeder
    figure for that step: both figures and the disagreeing record
    are named, and the feeder figure stands.
    """
    text = captured.assembled_metrics or ""
    for found in re.finditer(r"E-1 for Step (\d+) as (\d+) of (\d+)",
                             text):
        step = int(found.group(1))
        stated = (int(found.group(2)), int(found.group(3)))
        if step in covered and covered[step] != stated:
            return ("record disagrees: %s states E-1 for Step %d "
                    "as %d of %d, while the step record and roster "
                    "for Step %d state %d of %d; the feeder figure "
                    "stands and the record figure is not followed"
                    % (_metrics_record_name(captured), step,
                       stated[0], stated[1], step,
                       covered[step][0], covered[step][1]))
    return None


def _e2_figure_statement(captured, totals):
    """The D-18 and CA-1 statement for E-2, in the same form as E-1:
    a total spins figure the metrics record states for a step, in
    the explicit statement form, that disagrees with the feeder
    total for that step.
    """
    text = captured.assembled_metrics or ""
    for found in re.finditer(r"E-2 for Step (\d+) as (\d+)", text):
        step = int(found.group(1))
        stated = int(found.group(2))
        if step in totals and totals[step] != stated:
            return ("record disagrees: %s states E-2 for Step %d "
                    "as %d, while the step records for Step %d "
                    "state total spins %d; the feeder figure stands "
                    "and the record figure is not followed"
                    % (_metrics_record_name(captured), step, stated,
                       step, totals[step]))
    return None


def _join_statements(*statements):
    """Join the statements that stand for one row, or return None."""
    held = [statement for statement in statements if statement]
    if not held:
        return None
    return "; ".join(held)


def _error_form(operation, piece, exc):
    """The plan Section 4 error form for a failed seam call.

    Every error carries the operation attempted, the piece or
    path involved, and the underlying cause. A seam failure
    surfaced in this form stands in the statement line of each
    row the seam serves, so no error is swallowed and no
    fallback that follows it stands in silence.
    """
    return ("error: operation %s on %s failed with %s: %s; "
            "the error stands stated in this report and the "
            "marking for the affected row does not stand from "
            "that operation" % (operation, piece,
                                type(exc).__name__, exc))


# ------------------------------------------------------------- ledger

def _ledger_piece(captured):
    found = captured.pieces_of(CLS_PATH_LEDGER)
    for piece in found:
        if piece.text is not None and piece.text.strip():
            return piece
    return found[0] if found else None


def _transition_tokens(captured):
    """Per step timestamp tokens from ledger transition lines only.

    A token is a datetime where the entry carries a time of day and
    the word date where it carries a date only. A time of day that
    stands outside a transition entry counts for nothing here. The
    D-05 date only boundary rests only on the Slice 1 refusal reason
    at plan Section 1, line 33, and the F-02 fixture label at
    Section 2: a timestamp with a time of day counts, and a date
    only form does not. No lexical grammar beyond that boundary is
    stated in the plan (DS-OQ-03 stands restated as not answered by
    the dated correction at plan line 457), so the reading below
    takes the clock readings as written, with a weekday word before
    a date read as a prefix only and never checked against the
    calendar, seconds and a zone offset read as part of the written
    form and never converted, and a clock reading with no date part
    forming no token at all.
    """
    ledger = _ledger_piece(captured)
    per_step = {}
    if ledger is None or ledger.text is None:
        return per_step, ledger
    for line in ledger.text.splitlines():
        if "Step" not in line:
            continue
        lowered = line.lower()
        if "in progress" not in lowered and "closed" not in lowered:
            continue
        m = re.search(r"Step (\d+)\b", line)
        if not m:
            continue
        step = int(m.group(1))
        tokens = []
        for hit in _ANY_STAMP.finditer(line):
            if hit.group(4) is not None:
                try:
                    tokens.append(datetime(
                        int(hit.group(1)), int(hit.group(2)),
                        int(hit.group(3)), int(hit.group(4)),
                        int(hit.group(5))))
                except ValueError:
                    tokens.append("date")
            else:
                tokens.append("date")
        if tokens:
            per_step.setdefault(step, []).extend(tokens)
    return per_step, ledger


def _time_series(captured):
    """Per step time figures from the one capture, in ledger form.

    Returns (series, ledger). Each series entry carries the step
    elapsed figure formed from the two transition timestamps of
    that step alone, the step active figure, which is the stated
    Active duration where the ledger states one, else a stated
    duration for the step, else the interval duration the pair
    forms, whether a transition entry stands for the step, and
    whether a date only form stands among its tokens. Timestamps
    of two different steps never pair. A pair that stands
    reversed under the shared order check at _span_reversed
    forms no elapsed figure and no active figure: the entry
    carries the reversed mark instead, so the step fails on the
    reversed condition and is excluded from every figure its
    consumers form, including the build totals.
    """
    per_step, ledger = _transition_tokens(captured)
    series = {}

    def entry(step):
        if step not in series:
            series[step] = {"elapsed": None, "active": None,
                            "entry": False, "date_only": False,
                            "has_full": False, "reversed": False,
                            "stated": None, "active_stated": None}
        return series[step]

    if ledger is None or ledger.text is None:
        return series, ledger
    for step, toks in per_step.items():
        held = entry(step)
        held["entry"] = True
        if any(tok == "date" for tok in toks):
            held["date_only"] = True
        if any(isinstance(tok, datetime) for tok in toks):
            held["has_full"] = True
        if len(toks) >= 2 and isinstance(toks[0], datetime) and \
                isinstance(toks[1], datetime):
            if _span_reversed(toks[0], toks[1]):
                held["reversed"] = True
            else:
                held["elapsed"] = (toks[1] - toks[0]).total_seconds() \
                    / 3600.0
    for line in ledger.text.splitlines():
        m = re.search(r"Step (\d+)\b", line)
        if not m:
            continue
        step = int(m.group(1))
        active = re.search(r"Active\s+(\d+(?:\.\d+)?)\s*hours", line)
        stated = re.search(
            r"(?:stated\s+duration\s+of|duration\s+of)\s+"
            r"(\d+(?:\.\d+)?)\s*hours", line)
        if active:
            entry(step)["active_stated"] = float(active.group(1))
        elif stated:
            entry(step)["stated"] = float(stated.group(1))
    for held in series.values():
        if held["reversed"]:
            held["active"] = None
        elif held["active_stated"] is not None:
            held["active"] = held["active_stated"]
        elif held["stated"] is not None:
            held["active"] = held["stated"]
        elif held["elapsed"] is not None:
            held["active"] = held["elapsed"]
    return series, ledger


def _span_failure_condition(held):
    """The condition one entered step failed, in the row form.

    The reversed condition stands first, on the shared order
    check: a step whose pair stands reversed failed on that
    condition whatever else its entries carry. A date only entry
    failed on the date only condition, and any other entered step
    with no figure failed for want of a full timestamp pair.
    """
    if held is None:
        return ("no transition entry stands for the step, so no "
                "duration forms")
    if held.get("reversed"):
        return ("its closing transition timestamp stands earlier "
                "than its opening transition timestamp, so the "
                "span stands reversed and forms no duration")
    if held.get("date_only"):
        if held.get("has_full"):
            return ("one of its transition entries carries a "
                    "date only and no time of day, so no duration "
                    "forms")
        return ("its transition entries carry dates only and no "
                "time of day, so no duration forms")
    return ("no full timestamp pair stands for the step, so no "
            "duration forms")


def _failing_step_clauses(series, steps):
    """One naming clause per failing step, in step order."""
    return ["Step %d: %s" % (step, _span_failure_condition(
        series.get(step))) for step in sorted(steps)]


def _t1_state(captured, universe):
    """Shared T-1 reading: (kind, complete, incomplete, ledger).

    Kind is one of no-ledger, not-read, no-entries, date-only,
    no-interval, partial, reversed, or complete. A step fails
    where a transition entry stands for it and no full pair
    forms. Where at least one pair forms and at least one
    entered step fails, the series is partial, and the
    incomplete list names every universe step with no pair; the
    derivations form their present rows from the passing steps
    alone under the aggregation rule at D4R-03. Where no pair
    forms, the row is missing: on the date only ground where a
    date only form stands among the entered steps, and on the
    no interval ground otherwise, save where an entered step
    stands reversed under the shared order check, which is the
    reversed kind: no unit passes and a feeder record stands,
    so the row is present but not derivable with the reversed
    condition named, under the same aggregation rule.
    """
    series, ledger = _time_series(captured)
    if ledger is None:
        return "no-ledger", {}, [], ledger
    if ledger.text is None:
        return "not-read", {}, [], ledger
    complete = {step: held["elapsed"] for step, held in series.items()
                if held["elapsed"] is not None}
    failed = [step for step, held in series.items()
              if held["entry"] and held["elapsed"] is None]
    if not complete and not failed:
        return "no-entries", {}, [], ledger
    if complete and failed:
        wanted = list(universe.evidenced) or sorted(series)
        incomplete = [s for s in wanted if s not in complete]
        return "partial", complete, incomplete, ledger
    if complete:
        return "complete", complete, [], ledger
    if any(series[step].get("reversed") for step in failed):
        return "reversed", {}, failed, ledger
    if any(series[step]["date_only"] for step in failed):
        return "date-only", {}, [], ledger
    return "no-interval", {}, [], ledger


def _split_span_present(code, figures, covered, failing, series,
                        denom, pointer, rule_name):
    """The present row for a split span series, under D4R-03.

    Where the units of a metric split, some passing and some
    failing, the row is present where at least one unit passes:
    the figure stands formed from the passing units alone, the
    row states the coverage those units give as its bound in
    the fixed three part form, and each failing unit is named
    with the condition it failed. The reconciliation clause
    restates the coverage bound in the same line as the value,
    in the covered and remainder form.
    """
    result = DerivationResult(code, "present", figures, denom,
                              pointer, rule_name=rule_name)
    result.coverage = denom + "; steps counted: " + \
        _each_step(sorted(covered))
    clauses = _failing_step_clauses(series, failing)
    result.bound = (
        _steps_phrase(sorted(failing)),
        "the interval link for " + "; ".join(clauses),
        "a path ledger transition entry pair for each excepted "
        "step, carrying a timestamp with a time of day on the "
        "entry that opens the step and on the entry that closes "
        "it, with the closing entry standing at or after the "
        "opening entry")
    result.reconciled_against = (
        "the transition entries in the path ledger for each "
        "covered step, with the coverage bound restated here: "
        "covered %s; remainder %s"
        % (_steps_phrase(sorted(covered)),
           _steps_phrase(sorted(failing))))
    return result


def _derive_t1(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    kind, complete, incomplete, ledger = _t1_state(captured, universe)
    pointer = ledger.paths[0] if ledger is not None else "PATH-LEDGER.md"
    pointer = _pointer("T-1", pointer, captured)
    if kind == "no-ledger":
        return _refusal(
            "T-1", "missing", "no interval figure", denom, pointer,
            shows="no path ledger piece stands in the capture, so no "
                  "transition log holds any timestamp field",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="T-1 feeder standing rule")
    if kind == "not-read":
        token = _quality_code(ledger)
        return _refusal(
            "T-1", "present but not derivable", "no interval figure",
            denom, pointer,
            shows="a path ledger piece is present but not read in "
                  "full in the capture, so no transition log can be "
                  "read to form an interval",
            token=token,
            follows="the piece is marked not read in full in the "
                    "inventory and no figure is read from it, so no "
                    "interval figure stands",
            rule_name="T-1 not read in full rule")
    if kind == "no-entries":
        return _refusal(
            "T-1", "missing", "no interval figure", denom, pointer,
            shows="the transition log in PATH-LEDGER.md holds no "
                  "timestamp field for any step",
            token="no-feeder-record",
            follows="no interval can form from the log as it "
                    "stands, so the row is missing",
            rule_name="T-1 feeder standing rule")
    if kind == "date-only":
        raw_dates = sorted(set(re.findall(
            r"\d{4}-\d{2}-\d{2}", ledger.text or "")))
        if len(raw_dates) == 1:
            held = ("dates only, every transition in the ledger "
                    "recorded %s with no time of day" % raw_dates[0])
        elif raw_dates:
            held = ("dates only, the transitions in the ledger "
                    "recorded on %s with no time of day"
                    % ", ".join(raw_dates))
        else:
            held = "dates only, with no time of day on any entry"
        return _refusal(
            "T-1", "missing", "no interval figure", denom, pointer,
            shows="the transition log in PATH-LEDGER.md holds "
                  "timestamp fields in date only form, and no entry "
                  "carries a time of day from which an interval can "
                  "form",
            token="date-only-form",
            follows="the metric specific boundary makes the row "
                    "missing where no timestamp with a time of day "
                    "stands",
            rule_name="T-1 date only boundary rule",
            broken="the timestamp field on the path ledger "
                   "transition entries, which carries dates only "
                   "and no time of day",
            required="a timestamp with a time of day on the "
                     "transition entry that opens the step and on "
                     "the entry that closes it",
            held=held)
    if kind == "no-interval":
        return _refusal(
            "T-1", "missing", "no interval figure", denom, pointer,
            shows="the transition log in PATH-LEDGER.md holds "
                  "timestamp fields that pair for no step, and "
                  "timestamps of two different steps form no "
                  "interval",
            token="no-feeder-record",
            follows="no interval can form from the log as it "
                    "stands, so the row is missing",
            rule_name="T-1 feeder standing rule")
    if kind == "reversed":
        series, _ledger = _time_series(captured)
        clauses = _failing_step_clauses(series, incomplete)
        return _refusal(
            "T-1", "present but not derivable", "no interval figure",
            denom, pointer,
            shows="the transition log stands as the feeder record "
                  "and no entered step forms a duration: "
                  + "; ".join(clauses),
            token="missing-field",
            follows="no unit passes and a feeder record stands, "
                    "so the row is present but not derivable with "
                    "the failed condition named, under the "
                    "aggregation rule",
            rule_name="T-1 mixed series rule")
    if kind == "partial":
        covered = sorted(complete)
        series, _ledger = _time_series(captured)
        failing = [step for step, held in series.items()
                   if held["entry"] and held["elapsed"] is None]
        figures = "; ".join(
            "Step %d elapsed %s hours" % (s, _fmt_num(complete[s]))
            for s in covered)
        return _split_span_present(
            "T-1", figures, covered, failing, series, denom,
            pointer, "T-1 interval rule")
    figures = "; ".join(
        "Step %d elapsed %s hours" % (s, _fmt_num(complete[s]))
        for s in sorted(complete))
    return DerivationResult("T-1", "present", figures, denom, pointer,
                            rule_name="T-1 interval rule")


def _derive_t2(captured, universe):
    """T-2 interval durations, formed from the same T-1 timestamps."""
    base = _derive_t1(captured, universe)
    denom = base.denominator
    kind, complete, incomplete, ledger = _t1_state(captured, universe)
    pointer = base.pointer
    series, _ledger = _time_series(captured)
    durations = {step: held["active"] for step, held in series.items()
                 if held["active"] is not None}
    if kind == "no-ledger" or (kind == "no-entries" and
                               not durations):
        return _refusal(
            "T-2", "missing", "no duration figure", denom, pointer,
            shows="no transition interval stands in the path ledger "
                  "from which a duration can form",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="T-2 feeder standing rule")
    if kind == "not-read":
        return _refusal(
            "T-2", "present but not derivable", "no duration figure",
            denom, pointer,
            shows="the path ledger piece is present but not read in "
                  "full in the capture",
            token=_quality_code(ledger),
            follows="no duration is read from a piece that is not "
                    "read in full, so no figure stands",
            rule_name="T-2 not read in full rule")
    if kind == "date-only":
        return _refusal(
            "T-2", "missing", "no duration figure", denom,
            _pointer("T-2", pointer, captured),
            shows="the transition log in PATH-LEDGER.md holds "
                  "timestamp fields in date only form, and no "
                  "interval can be formed from a date only field",
            token="date-only-form",
            follows="the row is missing on the same date only "
                    "ground as T-1, with elapsed from T-1 missing on "
                    "the same ground",
            rule_name="T-2 date only boundary rule",
            broken="the interval duration field in the path ledger, "
                   "and the T-1 elapsed input",
            required="BANKED, SUSPENDED and halt intervals with a "
                     "start and an end at time of day precision or "
                     "a stated duration, beside a formed elapsed "
                     "figure",
            held="no interval duration stands in the ledger and "
                 "the T-1 input is missing on the date only ground")
    if kind == "no-interval" and not durations:
        return _refusal(
            "T-2", "missing", "no duration figure", denom, pointer,
            shows="no interval duration stands in the path ledger, "
                  "and the timestamps of two different steps form "
                  "no interval",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="T-2 feeder standing rule")
    if kind == "reversed":
        clauses = _failing_step_clauses(series, incomplete)
        return _refusal(
            "T-2", "present but not derivable", "no duration figure",
            denom, pointer,
            shows="the transition log stands as the feeder record "
                  "and no entered step forms a duration: "
                  + "; ".join(clauses),
            token="missing-field",
            follows="no unit passes and a feeder record stands, "
                    "so the row is present but not derivable with "
                    "the failed condition named, under the "
                    "aggregation rule",
            rule_name="T-2 mixed series rule")
    failed = [step for step, held in series.items()
              if held["entry"] and held["active"] is None]
    if kind == "partial" or (durations and failed):
        figures = "; ".join(
            "Step %d duration %s hours" % (s, _fmt_num(durations[s]))
            for s in sorted(durations))
        return _split_span_present(
            "T-2", figures, sorted(durations), failed, series,
            denom, pointer, "T-2 interval duration rule")
    if not durations:
        return _refusal(
            "T-2", "missing", "no duration figure", denom, pointer,
            shows="no transition interval stands in the path ledger "
                  "from which a duration can form",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="T-2 feeder standing rule")
    figures = "; ".join(
        "Step %d duration %s hours" % (s, _fmt_num(durations[s]))
        for s in sorted(durations))
    return DerivationResult("T-2", "present", figures, denom, pointer,
                            rule_name="T-2 interval duration rule")


# ------------------------------------------------------------- T-4, T-7

def _decision_feeders(captured):
    """The D-1 and T-4 decision feeders, read from the one capture.

    The queue reading stands in the form Builder A delivered: at
    most one decision queue piece, at the root level exact name,
    its text the whole file where it stands in the named form and
    no text with a damage quality state where it stands unusable.
    The decision table stands in the assembled metrics record. The
    queue file, where it stands in the named form, takes
    precedence over the decision table under WV-12.
    """
    queue_pieces = captured.pieces_of(CLS_DECISION_QUEUE)
    queue_piece = queue_pieces[0] if queue_pieces else None
    queue_usable = queue_piece is not None and \
        queue_piece.text is not None and \
        queue_piece.quality_state is None
    queue_items = _table_items(queue_piece.text) if queue_usable \
        else []
    assembled = captured.assembled_metrics or ""
    section = _metrics_section(assembled, "## Decision table")
    table_items = _table_items(section if section else assembled)
    table_stands = bool(table_items) or \
        "## decision table" in assembled.lower()
    return {
        "queue_piece": queue_piece,
        "queue_usable": queue_usable,
        "queue_items": queue_items,
        "table_items": table_items,
        "table_stands": table_stands,
        "metrics_name": _metrics_record_name(captured),
    }


def _t4_marking(captured, durations):
    """The T-4 cross check marking, consumed through Module 4.

    The marking stands where the metrics record states a T-4 wait
    figure that disagrees with the feeder wait figure, under D-18
    and CA-1, in the statement line of the T-4 row, and it never
    overrides the feeder result.
    """
    pairs = [(step, value) for step, value, _item in durations]
    error = None
    try:
        from metrics_starter_collector.cross_check import \
            t4_cross_check_statement
        marking = t4_cross_check_statement(
            pairs, captured.assembled_metrics or "",
            _metrics_record_name(captured))
        if marking:
            return marking
    except Exception as exc:
        error = _error_form("t4_cross_check_statement",
                            _metrics_record_name(captured), exc)
    if len(pairs) != 1:
        return error
    found = re.search(r"T-4\s+wait\s+as\s+(\d+(?:\.\d+)?)\s*hours",
                      captured.assembled_metrics or "")
    if not found:
        return error
    stated = float(found.group(1))
    feeder = pairs[0][1]
    if stated == feeder:
        return error
    return _join_statements(
        error,
        "record disagrees: %s states T-4 wait as %s hours, "
        "while the path ledger BANKED entries state %s hours; "
        "the feeder figure stands and the record figure is "
        "not followed"
        % (_metrics_record_name(captured), _fmt_num(stated),
           _fmt_num(feeder)))


def _derive_t4(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    ledger = _ledger_piece(captured)
    pointer = ledger.paths[0] if ledger is not None else "PATH-LEDGER.md"
    if ledger is None or ledger.text is None:
        return _refusal(
            "T-4", "missing", "no banked duration figure", denom,
            pointer,
            shows="no path ledger piece in the capture holds a "
                  "banked state from which a wait can form",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="T-4 feeder standing rule")
    durations = []
    banked_seen = "banked" in ledger.text.lower()
    for line in ledger.text.splitlines():
        if "BANKED" not in line:
            continue
        m = re.search(r"(\d+(?:\.\d+)?)\s*hours", line)
        step = _search_int(r"Step (\d+)\b", line)
        item_match = re.search(r"\b(Q-\d+)\b", line)
        if m:
            durations.append((step, float(m.group(1)),
                              item_match.group(1) if item_match
                              else None))
    if durations:
        feeders = _decision_feeders(captured)
        figures = "; ".join(
            ("Step %d wait %s hours" % (s, _fmt_num(v)))
            if s is not None else ("wait %s hours" % _fmt_num(v))
            for s, v, _item in durations)
        named = [entry for entry in durations if entry[2]]
        if named:
            named_items = [entry[2] for entry in named]
            if feeders["queue_usable"]:
                governing = [item["item"]
                             for item in feeders["queue_items"]]
                if all(name in governing for name in named_items):
                    result = DerivationResult(
                        "T-4", "present", figures, denom,
                        _pointer("T-4", pointer, captured),
                        rule_name="T-4 banked rule")
                    result.statement = _t4_marking(
                        captured, durations)
                    return result
                return _refusal(
                    "T-4", "present but not derivable",
                    "no banked duration figure", denom,
                    _pointer("T-4", pointer, captured),
                    shows="banked entries stand in the path ledger "
                          "with durations naming %s, and the queue "
                          "file inside the root governs over the "
                          "decision table and holds no item of that "
                          "name" % _names_phrase(named_items),
                    token="missing-field",
                    follows="the governing queue file supplies no "
                            "item for the banked duration, and the "
                            "decision table does not rescue a queue "
                            "miss, so no wait figure stands",
                    rule_name="T-4 queue governing rule")
            if feeders["table_stands"]:
                table_names = [item["item"]
                               for item in feeders["table_items"]]
                if all(name in table_names for name in named_items):
                    result = DerivationResult(
                        "T-4", "present", figures, denom,
                        _pointer("T-4", pointer, captured),
                        rule_name="T-4 degraded banked rule")
                    parts = ["degraded form: the row is shown "
                             "without its queue cross check, the "
                             "decision table in the metrics record "
                             "standing as the cross check in place "
                             "of the queue file"]
                    marking = _t4_marking(captured, durations)
                    if marking:
                        parts.append(marking)
                    result.statement = "; ".join(parts)
                    return result
                return _refusal(
                    "T-4", "present but not derivable",
                    "no banked duration figure", denom,
                    _pointer("T-4", pointer, captured),
                    shows="banked entries stand in the path ledger "
                          "with durations naming %s, and no queue "
                          "file and no decision table inside the "
                          "root names that item"
                          % _names_phrase(named_items),
                    token="missing-field",
                    follows="no cross check record names the item "
                            "the banked duration matches, so no "
                            "wait figure stands",
                    rule_name="T-4 cross check standing rule")
            return _refusal(
                "T-4", "present but not derivable",
                "no banked duration figure", denom,
                _pointer("T-4", pointer, captured),
                shows="banked entries stand in the path ledger "
                      "with durations naming %s, and neither a "
                      "queue file nor a decision table stands "
                      "inside the root to name that item"
                      % _names_phrase(named_items),
                token="missing-field",
                follows="an item counts only where a queue file "
                        "or a decision table inside the root names "
                        "it, so no wait figure stands",
                rule_name="T-4 cross check standing rule")
        result = DerivationResult(
            "T-4", "present", figures, denom,
            _pointer("T-4", pointer, captured),
            rule_name="T-4 degraded banked rule")
        parts = []
        if not feeders["queue_usable"]:
            parts.append(
                "degraded form: the row is shown without its "
                "queue cross check, from the BANKED interval "
                "durations standing in the feeder records")
        marking = _t4_marking(captured, durations)
        if marking:
            parts.append(marking)
        result.statement = "; ".join(parts) if parts else None
        return result
    if banked_seen:
        section = _metrics_section(
            captured.assembled_metrics or "", "## Decision table")
        items = _table_items(section if section
                             else captured.assembled_metrics)
        example = ""
        if items:
            origins = []
            for item in items:
                origin = _search_int(r"(\d+)", item.get("origin") or "")
                if origin is not None:
                    origins.append(origin)
            if origins:
                mode = max(sorted(set(origins)), key=origins.count)
                count = origins.count(mode)
                example = (", for example %d banked questions open "
                           "at Step %d" % (count, mode))
        queue_stands = bool(captured.pieces_of(CLS_DECISION_QUEUE))
        if queue_stands:
            held_tail = ("and a queue file stands in the tree for "
                         "the cross check")
        else:
            held_tail = ("and no queue file stands in the tree for "
                         "the cross check")
        return _refusal(
            "T-4", "present but not derivable",
            "no banked duration figure", denom,
            _pointer("T-4", pointer, captured),
            shows="banked entries stand in the path ledger and no "
                  "banked entry carries an interval duration field",
            token="missing-field",
            follows="a banked entry with no duration supplies no "
                    "wait figure, so the row is not derivable",
            rule_name="T-4 banked duration field rule",
            broken="the BANKED interval duration field in the path "
                   "ledger",
            required="a BANKED interval duration for each wait, "
                     "with its blocker matching a decision item, "
                     "for the full form, and the same durations for "
                     "the degraded form, which relaxes the queue "
                     "cross check only",
            held=("banked states and item counts stand" + example +
                  ", and no BANKED interval duration stands "
                  "anywhere in the ledger, " + held_tail))
    return _refusal(
        "T-4", "present but not derivable", "no banked duration figure",
        denom, _pointer("T-4", pointer, captured),
        shows="a path ledger stands in form and holds no BANKED "
              "entry at all, and no banked item stands in any "
              "other named feeder",
        token="missing-field",
        follows="no BANKED entry stands in the path ledger from "
                "which a duration can be formed, so no wait "
                "figure stands, and a count of zero banked items "
                "is never printed as a duration",
        rule_name="T-4 zero banked entry rule",
        broken="a BANKED entry in the path ledger",
        required="a BANKED entry in the path ledger, carrying "
                 "an interval duration, from which a wait can "
                 "be formed",
        held="the path ledger stands in form, stating its steps "
             "and their transitions, and holds no BANKED entry")


def _t7_round_example(captured):
    """Example of scattered round evidence, from the records.

    A step whose rounds stand as an initial round plus a run of
    re-audit rounds in its own papers, while only one ruling file
    stands for the step, names the unlike forms the round
    evidence stands in. The round count is counted from the
    re-audit papers and ruling files the capture holds.
    """
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
             6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
             11: "eleven", 12: "twelve"}
    reaudit = {}
    initial = set()
    for piece in captured.pieces:
        for path in piece.paths:
            m = re.search(r"step-?(\d+)[^/]*reaudit-(\d+)", path)
            if m:
                reaudit.setdefault(int(m.group(1)), set()).add(
                    int(m.group(2)))
                continue
            m = re.search(r"step-?(\d+)[^/]*reaudit", path)
            if m:
                reaudit.setdefault(int(m.group(1)), set())
            elif piece.record_class == CLS_AUDIT_PAPER:
                m = re.search(r"step-?(\d+)", path)
                if m:
                    initial.add(int(m.group(1)))
    for step in sorted(reaudit):
        rounds = reaudit[step]
        count = max(rounds) if rounds else 0
        if count < 2 or step not in initial:
            continue
        rulings = [q for q in captured.pieces_of(CLS_GATE_RULING)
                   if q.step == step]
        if len(rulings) == 1:
            return ("for example Step %d running an initial round "
                    "and %s re-audit rounds in its step record "
                    "with only the last round carrying a ruling "
                    "file of its own"
                    % (step, words.get(count, str(count))))
    return None


# ------------------------------------------------------- Slice 5 helpers

def _header_count_excepted(header_line):
    """Whether one header count statement line carries the signal
    two exception, under the agreed negation rule.

    The exception fires only where the header count stands
    stated as a planned count or as a target count and no
    negation governs that statement. Governance is judged by
    grammatical position, not by membership in a closed list
    of subjects, auxiliaries or participle words. The closed
    classes of English grammar are completed, not sampled:
    a negation form is one of the negation words not, no,
    never, neither, nor, none, nothing, nobody or nowhere,
    the modal form cannot, or a contraction ending in n't,
    spaced or unspaced. A function word is a determiner, a
    pronoun, an auxiliary, copula or modal verb, a connective
    or preposition, or an adverb, adverbs standing in their
    ly form beside the listed forms. A verb form is a word
    in a participle or past form, ending in ed, en or wn, or
    one of the irregular verb forms, beside the phrase form
    set aside; a verb of statement, as stated, said or
    recorded, is no rejection predicate.

    A negation form standing in the same clause before the
    planned or target statement governs it, as not a planned
    count, neither a planned count, none of it a planned
    count, or isn't a planned count. A negation form standing
    in an earlier clause governs it where that clause is the
    negation standing alone: every word after the negation
    in that clause is a function word, so the negation has
    no complement of its own and can only attach to the
    statement that follows it, across any parenthetical
    clause between them, whatever subject or auxiliary
    stands before the negation, as the figure is not,
    strictly speaking, a planned count, does not, strictly
    speaking, state a planned count, not really, a planned
    count, or not a, strictly speaking, planned count. Where
    the nearest earlier clause carrying a negation form has
    a complement after the negation, as not audited, not
    counted or never audited, that negation governs its own
    complement, the search stops there, and the exception
    stands. A verb form standing as the predicate of the
    count statement in the same clause after the statement
    governs it, with or without a negation, as the planned
    count was rejected, the planned count was retracted, or
    the planned count was not accepted, whatever participle
    word stands in that position. A verb form standing in a
    later clause governs it where the clause carries no
    subject of its own before the verb form beyond function
    words, as a planned count, rejected, a planned count,
    not accepted, stated as a planned count, which will be
    rejected, or stated as a planned count, finally
    rejected, where the clause opens with a relative
    pronoun, as stated as a planned count, which the board
    rejected, the relative pronoun linking the clause to the
    count whatever subject stands inside it, or where the
    clause stands after a semicolon, as stated as a planned
    count; the board rejected it. A rejection in a later
    clause after a comma that carries a subject of its own
    and no relative opening, as stated as a planned count,
    the board rejected it, does not govern, and the search
    stops at the nearest later clause carrying a verb form.
    A later clause that restates the planned or target
    wording is the exception wording itself and is passed
    over. The weaker forms hardly and without are no
    negation form under this rule and keep excepting, as
    the findings left them. The brief form lines, the count
    stated as a planned count and the count stated as a
    target count with no negation standing, except.
    """
    negation_words = ("not", "no", "never", "neither", "nor",
                      "none", "nothing", "nobody", "nowhere",
                      "cannot")
    function_words = {
        "a", "an", "the", "it", "this", "that", "these",
        "those", "itself", "there", "which", "who", "whom",
        "whose", "he", "she", "they", "we", "you", "i", "him",
        "her", "us", "them", "his", "hers", "its", "their",
        "theirs", "our", "ours", "your", "yours", "my", "mine",
        "any", "some", "each", "every", "all", "own",
        "is", "was", "were", "are", "be", "been", "being",
        "am", "has", "have", "had", "does", "do", "did",
        "can", "could", "will", "would", "shall", "should",
        "may", "might", "must", "cannot", "get", "gets",
        "got", "and", "but", "or", "nor", "since", "as",
        "in", "on", "by", "for", "of", "to", "at", "from",
        "with", "after", "before", "then", "now", "later",
        "also", "still", "just", "even", "only", "again",
        "yet", "ever", "already", "longer", "aside"}
    irregular_verbs = {"struck", "withdrew", "kept", "held",
                       "sent", "left", "dealt", "meant",
                       "built"}
    statement_verbs = {"stated", "said", "described",
                       "called", "named", "listed", "noted",
                       "recorded", "presented", "written",
                       "marked", "shown"}

    def tokens(text):
        spaced = re.sub(r"\sn't\b", " n't", text)
        return re.findall(r"n't|[a-z]+(?:'[a-z]+)?", spaced)

    def is_negation(word):
        return word in negation_words or word.endswith("n't")

    def is_function(word):
        return word in function_words or word in negation_words \
            or word.endswith("n't") or word.endswith("ly")

    def is_verb_form(word):
        return word.endswith("ed") or word.endswith("en") \
            or word.endswith("wn") or word in irregular_verbs

    def predicate_index(words):
        for index, word in enumerate(words):
            if word == "set":
                if index + 1 < len(words) and \
                        words[index + 1] == "aside":
                    return index
                continue
            if is_verb_form(word) and \
                    word not in statement_verbs:
                return index
        return None

    found = re.search(
        r"\bplanned count\b|\btarget count\b"
        r"|\bstated as (?:a |an )?(?:planned|target)"
        r"(?: count)?\b",
        header_line)
    if not found:
        return False
    clauses_before = re.split(
        r"[,;]", header_line[:found.start()])
    if any(is_negation(word)
           for word in tokens(clauses_before[-1])):
        return False
    for clause in reversed(clauses_before[:-1]):
        words = tokens(clause)
        negated = [index for index, word in enumerate(words)
                   if is_negation(word)]
        if not negated:
            continue
        if all(is_function(word)
               for word in words[negated[0] + 1:]):
            return False
        break
    parts = re.split(r"([,;])", header_line[found.end():])
    segments = [(None, parts[0])]
    for index in range(1, len(parts), 2):
        segments.append((parts[index], parts[index + 1]))
    for position, (delimiter, segment) in enumerate(segments):
        if re.search(r"planned count|target count"
                     r"|stated as (?:a |an )?(?:planned|target)",
                     segment):
            continue
        words = tokens(segment)
        predicate = predicate_index(words)
        if predicate is None:
            continue
        head = words[:predicate]
        if position == 0:
            if all(is_function(word) for word in head):
                return False
            continue
        if delimiter == ";":
            return False
        if head and head[0] in ("which", "that"):
            return False
        if all(is_function(word) for word in head):
            return False
        break
    return True



def _last_corrected_count(lowered):
    """The corrected count a record states, or None.

    The corrected count is the figure stated by the last
    correction statement in the record, across the union of
    the three vocabularies: the corrected count form, the
    count in rows form, and the restates the count form. A
    record corrected once is judged on that one statement,
    exactly as it stood before; a record corrected in two
    statements is judged on the last one, in either
    implementation alike.
    """
    found = []
    for pattern in (r"corrected count:?\s*(\d+)",
                    r"correct\w*[^\n]*?(\d+)\s+rows",
                    r"restates? the count[^\n\d]*(\d+)"):
        for match in re.finditer(pattern, lowered):
            found.append((match.start(), int(match.group(1))))
    if not found:
        return None
    found.sort(key=lambda entry: entry[0])
    return found[-1][1]


def _following_table_data_rows(lines, start):
    """The data row count of the table that follows a header line.

    The table counted is the first markdown table at or after
    the line after the header count statement, in the shell
    reading form: its first pipe row is its header row and
    stands uncounted, a separator row stands uncounted, every
    later pipe row of that same table counts, and the count
    stops where that table ends, so a second table later in
    the same piece contributes no row to this count. Returns
    None where no table follows.
    """
    index = start
    while index < len(lines) and \
            not lines[index].strip().startswith("|"):
        index += 1
    if index >= len(lines):
        return None
    rows = 0
    index += 1
    while index < len(lines) and \
            lines[index].strip().startswith("|"):
        cells = lines[index].strip().strip("|")
        if not all(set(cell.strip()) <= set("-: ") and cell.strip()
                   for cell in cells.split("|")):
            rows += 1
        index += 1
    return rows


def _signal_failure(text):
    """The first completeness signal a text fails, or None.

    Signal one: a numbered Finding sequence with a gap, unless the
    record states in its own text that the sequence is partial or
    planned, or that numbers in the sequence are reserved or
    skipped by design. Signal two: a table whose row count
    disagrees with a count stated in its own header, unless the
    header count is stated as a planned or target count, or a
    governing correction in the record restates the count, in
    which case the corrected count is the count tested. The
    planned or target exception attaches to the header count
    statement itself: the count must stand stated in that
    statement as a planned count or as a target count, and a
    mention of planned or of a target count anywhere else
    in the piece carries no exception, and neither does a
    negated or derived form in the statement itself, as
    unplanned or targeted, which states no planned or target
    count, and neither does a statement a negation governs,
    as not a planned count, no planned count, never a target
    count, not planned count, or a planned count stated as
    rejected, each of which states the opposite of the
    exception condition. The governing correction stands honoured in every
    vocabulary the shell reading honours, the corrected count
    followed by its number, the corrected count stated as a
    count in rows, and the restates the count form, so a
    record corrected in any of those forms is judged on the
    same corrected count here, and where two correction
    statements stand in one record the corrected count is
    the figure the last such statement states, across the
    union of the three vocabularies alike. The rows tested
    are the rows of the one table that follows the header
    count statement, the same table the shell reading tests,
    so a second table later in the piece contributes no row
    to the count in either implementation. Signal
    three: a section a record contents list names that does not
    appear in the record, unless the contents list itself marks
    the section as deferred or not yet written, or a later
    governing entry in the record removes the section from the
    list. A piece failing a signal with no exception standing is
    treated as truncated and its visible part counts toward
    nothing.
    """
    if text is None:
        return None
    lowered = text.lower()
    findings = [int(x) for x in re.findall(r"Finding (\d+)\b", text)]
    if findings and findings[0] == 1 and not any(
            phrase in lowered for phrase in (
                "sequence is partial", "sequence is planned",
                "partial or planned", "reserved or skipped")):
        ordered = sorted(set(findings))
        if ordered != list(range(1, ordered[-1] + 1)):
            return "signal-one"
    stated = re.search(r"Rows stated in header:\s*(\d+)", text)
    if stated:
        header_start = text.rfind("\n", 0, stated.start()) + 1
        header_end = text.find("\n", stated.start())
        if header_end < 0:
            header_end = len(text)
        header_line = text[header_start:header_end].lower()
        if not _header_count_excepted(header_line):
            corrected = _last_corrected_count(lowered)
            count = corrected if corrected is not None \
                else int(stated.group(1))
            lines = text.splitlines()
            header_index = text[:stated.start()].count("\n")
            rows = _following_table_data_rows(
                lines, header_index + 1)
            if rows is not None and rows != count:
                return "signal-two"
    headings = {found.strip().lower() for found in
                re.findall(r"^#{1,6}\s+(.+)$", text, re.M)}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.lower().startswith("contents"):
            continue
        if "deferred" in stripped.lower() \
                or "not yet written" in stripped.lower():
            continue
        if ":" not in stripped:
            continue
        names = stripped.split(":", 1)[1].rstrip(".")
        for name in names.split(","):
            name = name.strip()
            if name and name.lower() not in headings:
                if "removed from the contents list" in lowered:
                    continue
                return "signal-three"
    return None


def _piece_step(piece):
    """The step a piece belongs to, from its record or its path.

    Audit paper pieces carry no step in the capture record, and
    their step stands in the step number their path names.
    """
    if piece.step is not None:
        return piece.step
    found = re.search(r"step-(\d+)", piece.paths[0])
    return int(found.group(1)) if found else None


def _loop_steps(captured):
    """Steps the step records themselves state as loop steps."""
    steps = set()
    for piece in captured.pieces_of(CLS_STEP_RECORD):
        if piece.text and "Loop step" in piece.text \
                and piece.step is not None:
            steps.add(piece.step)
    return sorted(steps)


def _t7_round_evidence(captured, step):
    """Outcome rounds, duplicate rounds and work rounds for a step.

    An outcome round stands where a closing outcome record states
    it, where a board ruling held inside the step record closes
    it under gap DG-02, or where a work record for the round
    stands as its verdict record in the degraded form. A round
    counts only where pairing evidence also stands: a record for
    the round stating the work it disposed of, or work inside it.
    """
    outcomes = {}
    duplicates = []
    work = set()
    for piece in captured.pieces:
        if piece.text is None or _piece_step(piece) != step:
            continue
        text = piece.text
        for found in re.finditer(r"board closes Round (\d+)", text):
            outcomes.setdefault(int(found.group(1)), "board")
        for found in re.finditer(
                r"Round (\d+) closing outcome record", text):
            rnd = int(found.group(1))
            if outcomes.get(rnd) == "closing":
                duplicates.append(rnd)
            outcomes.setdefault(rnd, "closing")
        lines = text.splitlines()
        first_line = lines[0] if lines else ""
        found = re.search(r"Round (\d+) work record", first_line)
        if found:
            rnd = int(found.group(1))
            outcomes.setdefault(rnd, "verdict")
            work.add(rnd)
        if "closing outcome record" in text:
            continue
        for found in re.finditer(r"Round (\d+) work\b", text):
            work.add(int(found.group(1)))
        for found in re.finditer(
                r"[Ww]ork (?:inside|Round) ?(?:inside )?Round (\d+)",
                text):
            work.add(int(found.group(1)))
        for found in re.finditer(
                r"[Ww]ork inside Round (\d+)", text):
            work.add(int(found.group(1)))
        for found in re.finditer(
                r"work Round (\d+) disposed of", text):
            work.add(int(found.group(1)))
    return outcomes, duplicates, work


def _derive_t7(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    gates = captured.pieces_of(*GATE_CLASSES)
    pointer = gates[0].paths[0] if gates else "steps/step-01-gate-record.md"
    pointer = _pointer("T-7", pointer, captured)
    if not _known_version(captured.definitions_version) and \
            (gates or captured.pieces_of(CLS_STEP_RECORD)):
        return _unknown_version_result(captured, "T-7", denom, pointer)
    if universe.evidenced and all(step == 22
                                   for step in universe.evidenced):
        # The Step 22 Keeper gate has no T-7 effect under G-04:
        # T-7 counts verdict records only for loop steps, and
        # Step 22 is not a loop step, so where the Step 22 gate
        # stands alone no T-7 feeder record stands.
        return _refusal(
            "T-7", "missing", "no rounds figure", denom, pointer,
            shows="no gate verdict record and no step record stands in "
                  "the capture for this metric",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="T-7 feeder standing rule")
    for piece in captured.pieces:
        if piece.text is None or piece.step is None:
            continue
        pass_count = _search_int(
            r"Pass count in this record:\s*(\d+)\s*passes", piece.text)
        if pass_count is None:
            continue
        verdict_count = None
        for other in captured.step_pieces(piece.step, *GATE_CLASSES):
            if other.text:
                verdict_count = _search_int(
                    r"Verdict record count for this step:\s*(\d+)",
                    other.text)
                if verdict_count is not None:
                    break
        if verdict_count is not None and verdict_count != pass_count:
            return _refusal(
                "T-7", "present but not derivable", "no rounds figure",
                denom, pointer,
                shows="the records for Step %d state irreconcilable "
                      "round counts: the step record states a pass "
                      "count of %d passes and the gate record states "
                      "a verdict record count of %d"
                      % (piece.step, pass_count, verdict_count),
                token="record-disagrees",
                follows="both counts stand named and neither count "
                        "is picked, so no round figure stands for "
                        "the step",
                rule_name="G-05 irreconcilable counts rule")
    loop_steps = _loop_steps(captured)
    if loop_steps:
        counted = {}
        failures = []
        for step in loop_steps:
            outcomes, duplicates, work = _t7_round_evidence(
                captured, step)
            if duplicates:
                failures.append(
                    "the mapping test part one failed for Step %d: "
                    "two closing outcome records stand for Round %d, "
                    "and a part one failure fails the step mapping "
                    "as a whole" % (step, duplicates[0]))
                continue
            unpaired = [rnd for rnd in sorted(outcomes)
                        if rnd not in work]
            if unpaired:
                failures.append(
                    "Step %d rounds unpaired: %s stand as outcome "
                    "records with no pairing record stating the "
                    "work disposed of, a mapping test part two "
                    "failure failing the single round"
                    % (step, ", ".join("Round %d" % rnd
                                       for rnd in unpaired)))
                continue
            if outcomes:
                counted[step] = sorted(outcomes)
        if failures:
            return _refusal(
                "T-7", "present but not derivable", "no rounds figure",
                denom, pointer,
                shows="loop steps stand in the step universe, %s, "
                      "and the records of a loop step do not map "
                      "to rounds by an outcome record"
                      % _each_step(loop_steps),
                token="no code fits",
                follows="the round mapping the row requires does "
                        "not stand for the step named, so no round "
                        "figure stands",
                rule_name="T-7 round mapping rule",
                broken="the round mapping link between the records "
                       "of a loop step and its rounds",
                required="rounds mapped by an outcome record for "
                         "the step, with both parts of the mapping "
                         "test standing, the mapping conditions and "
                         "the pairing evidence",
                held="; ".join(failures))
        if counted:
            figures = "; ".join(
                "Step %d: %d rounds counted" % (step, len(rounds))
                for step, rounds in sorted(counted.items()))
            figures += ("; counted from verdict records, the "
                        "rounds standing marked as counted, counted "
                        "not marked from any table entry, a table "
                        "entry alone counting nothing and outcome "
                        "records alone counting once as counted")
            coverage = denom + "; steps counted: " + _each_step(
                sorted(counted))
            result = DerivationResult(
                "T-7", "present", figures, coverage, pointer,
                rule_name="T-7 outcome record rule")
            result.coverage = coverage
            return result
        stated_rounds = []
        for piece in captured.pieces:
            if piece.text is None or piece.step is None:
                continue
            found = re.search(
                r"board ruling held inside this record states "
                r"(\d+) rounds for this step", piece.text, re.I)
            if found:
                stated_rounds.append((piece.step,
                                      int(found.group(1))))
        excluded = [
            "the board ruling held inside the Step %d step record, "
            "a board ruling stating a round count, excluded as a "
            "record form that is not an outcome record" % step
            for step, _count in stated_rounds]
        excluded.append(
            "check papers, register items and other non outcome "
            "records, excluded as record forms that record no "
            "outcome")
        held_parts = [
            "population: the loop steps in the step universe, "
            + _each_step(loop_steps)
            + "; excluded: " + "; ".join(excluded)]
        for step, count in stated_rounds:
            held_parts.append(
                "the board ruling held inside the Step %d record "
                "states %d rounds for this step, and a stated round "
                "count alone counts nothing, a table entry and an "
                "outcome record being matched by step and by "
                "outcome before either is counted" % (step, count))
        return _refusal(
            "T-7", "present but not derivable", "no rounds figure",
            denom, pointer,
            shows="gate and step records stand and no record states "
                  "a round count in a form the row can count",
            token="no code fits",
            follows="no round figure stands on the feeder records, "
                    "so the row is not derivable in this form",
            rule_name="T-7 round evidence rule",
            broken="the round mapping link between the records of "
                   "a loop step and its rounds",
            required="rounds mapped by an outcome record for the "
                     "step, in the verdict record forms the "
                     "derivation names",
            held=", and ".join(held_parts))
    assembled = captured.assembled_metrics or ""
    if "loop round table" in assembled.lower():
        held_parts = []
        loop_section = _metrics_section(assembled, "## Loop round table")
        if loop_section and ("no rows" in loop_section.lower() or
                             "(no rows yet)" in loop_section.lower()):
            clause = "the loop round table holds no rows"
            if "no loop step has run yet" in loop_section.lower():
                clause += " and still carries its stale opening text"
            held_parts.append(clause)
        held_parts.append(
            "round evidence stands scattered in unlike forms")
        example = _t7_round_example(captured)
        held_text = ", and ".join(held_parts)
        if example:
            held_text += ", " + example
        return _refusal(
            "T-7", "present but not derivable", "no rounds figure",
            denom, pointer,
            shows="gate and step records stand and no record states "
                  "a round count in a form the row can count",
            token="no code fits",
            follows="no round figure stands on the feeder records, "
                    "so the row is not derivable in this form",
            rule_name="T-7 round evidence rule",
            broken="the round mapping link between the records of "
                   "a loop step and its rounds",
            required="rounds mapped by an outcome record for the "
                     "step, in the verdict record forms the "
                     "derivation names",
            held=held_text)
    return _refusal(
        "T-7", "missing", "no rounds figure", denom, pointer,
        shows="the step universe holds no loop step for the metric "
              "to count, and no loop round table stands in the "
              "metrics record",
        token="no-feeder-record",
        follows="no feeder record for the metric exists in the "
                "tree, so the row is missing",
        rule_name="T-7 feeder standing rule")


# ------------------------------------------------------- staffing family

def _step_field(captured, step, patterns, classes):
    for piece in captured.step_pieces(step, *classes):
        if piece.text is None:
            continue
        for pattern in patterns:
            value = _search_int(pattern, piece.text)
            if value is not None:
                return value
    return None


_STAFFING_CLASSES = (CLS_STEP_RECORD, CLS_ROSTER, CLS_OPENING_RECORD,
                     CLS_STEP_COMPANION)


def _instance_field(pieces, patterns):
    """The first integer a pattern finds in one instance piece set."""
    for piece in pieces:
        if piece.text is None:
            continue
        for pattern in patterns:
            value = _search_int(pattern, piece.text)
            if value is not None:
                return value
    return None


def _steps_range_phrase(steps):
    """Steps A to B for a contiguous run, else the named list form."""
    steps = sorted(steps)
    if len(steps) > 1 and steps == list(range(steps[0], steps[-1] + 1)):
        return "Steps %d to %d" % (steps[0], steps[-1])
    return _each_step(steps)


def _e1_bound(covered_steps, uncovered_steps):
    """The E-1 bound and reconciliation for a present row whose
    coverage has a remainder: the bound names the excepted steps,
    the link excepted and the record that would clear it, and the
    reconciliation clause restates the coverage bound in the same
    line as the value, in the covered and remainder form.
    """
    if not uncovered_steps:
        return None, None
    remainder = _steps_range_phrase(uncovered_steps)
    covered = _steps_range_phrase(covered_steps)
    bound = (remainder,
             "the staffed against base link for %s, whose step "
             "records list staffing with no base count beside it"
             % remainder,
             "a step record for each of %s stating a base count "
             "beside its staffing list" % remainder)
    phrase = ""
    if len(covered_steps) > 1 and covered_steps == list(
            range(covered_steps[0], covered_steps[-1] + 1)):
        phrase = "present for %s as kept; " % covered
    phrase += "covered %s; remainder %s" % (covered, remainder)
    reconciled = ("the staffed and base counts in the step record "
                  "and roster for each covered step, with the "
                  "coverage bound restated here: " + phrase)
    return bound, reconciled


def _derive_e1_marked(captured, universe, pointer):
    """E-1 where the universe carries a marked instance.

    Coverage and figures stand per instance, under the Spin 772
    key: a restart suffixed instance is a separate instance and
    counts as itself, and a plain instance beside it counts as
    itself, so the row denominator is the instance count.
    """
    denom = "denominator step universe %d steps" % len(universe.instances)
    grouped = {}
    for piece in captured.pieces:
        if piece.record_class in _STAFFING_CLASSES and \
                piece.step is not None:
            grouped.setdefault(_piece_instance_key(piece),
                               []).append(piece)
    covered = {}
    for key in universe.instances:
        pieces = grouped.get(key, [])
        staffed = _instance_field(
            pieces, (r"Team staffed:\s*(\d+)", r"Named agents:\s*(\d+)"))
        base = _instance_field(pieces, (r"\bBase:\s*(\d+)",))
        step = int(re.match(r"step-(\d+)", key).group(1))
        if staffed is None or base is None:
            cells = _metrics_step_table(captured).get(step)
            if key == "step-%d" % step and cells is not None and \
                    len(cells) >= 6:
                found = re.match(r"(\d+)\s*/\s*(\d+)", cells[5])
                if found:
                    staffed, base = int(found.group(1)), \
                        int(found.group(2))
        if staffed is not None and base is not None:
            covered[key] = (staffed, base)
    if not _known_version(captured.definitions_version) and \
            _feeder_stands(captured, "E-1"):
        return _unknown_version_result(
            captured, "E-1", denom, _pointer("E-1", pointer, captured))
    if not covered:
        if captured.pieces_of(*_STAFFING_CLASSES):
            return _refusal(
                "E-1", "present but not derivable",
                "no staffed and base pair stands", denom,
                _pointer("E-1", pointer, captured),
                shows="step records and roster artifacts stand and "
                      "no step instance carries both a staffed "
                      "count and a base count for the same instance",
                token="missing-field",
                follows="both fields must stand for the same "
                        "instance, so no pair figure stands for "
                        "any instance",
                rule_name="E-1 same step pair rule")
        return _refusal(
            "E-1", "missing", "no staffed and base pair stands",
            denom, _pointer("E-1", pointer, captured),
            shows="no step record and no roster artifact stands in "
                  "the capture for this metric",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="E-1 feeder standing rule")
    keys = [key for key in universe.instances if key in covered]
    figures = "; ".join(
        "%s: %d of %d" % (_instance_label(key), covered[key][0],
                          covered[key][1])
        for key in keys)
    coverage = denom + "; steps counted: " + ", ".join(
        _instance_label(key) for key in keys)
    uncovered = [key for key in universe.instances if key not in covered]
    if uncovered:
        coverage += "; covered " + ", ".join(
            _instance_label(key) for key in keys) + "; remainder " + \
            ", ".join(_instance_label(key) for key in uncovered)
    marked_reconciled = None
    if uncovered:
        marked_reconciled = (
            "the staffed and base counts in the step record and "
            "roster for each covered step, with the coverage bound "
            "restated here: covered " + ", ".join(
                _instance_label(key) for key in keys)
            + "; remainder " + ", ".join(
                _instance_label(key) for key in uncovered))
    result = DerivationResult(
        "E-1", "present", figures, coverage,
        _pointer("E-1", pointer, captured),
        rule_name="E-1 staffing pair rule")
    result.coverage = coverage
    plain_covered = {}
    for key, pair in covered.items():
        plain_covered[int(re.match(r"step-(\d+)", key).group(1))] = pair
    if marked_reconciled is not None:
        result.reconciled_against = marked_reconciled
    result.statement = _join_statements(
        _e1_figure_statement(captured, plain_covered),
        _universe_claim_statement(captured, universe))
    return result


def _derive_e1(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    pointer = captured.first_path(
        CLS_STEP_RECORD, CLS_ROSTER, CLS_STEP_COMPANION) or \
        "steps/step-01-record.md"
    if any("-" in key[5:] and not key[5:].isdigit()
           for key in universe.instances):
        return _derive_e1_marked(captured, universe, pointer)
    covered = {}
    for step in universe.evidenced:
        staffed = _step_field(
            captured, step,
            (r"Team staffed:\s*(\d+)", r"Named agents:\s*(\d+)"),
            _STAFFING_CLASSES)
        base = _step_field(captured, step, (r"\bBase:\s*(\d+)",),
                           _STAFFING_CLASSES)
        if staffed is not None and base is not None:
            covered[step] = (staffed, base)
    for step, cells in _metrics_step_table(captured).items():
        if step in covered or len(cells) < 6:
            continue
        m = re.match(r"(\d+)\s*/\s*(\d+)", cells[5])
        if m:
            covered[step] = (int(m.group(1)), int(m.group(2)))
    if not _known_version(captured.definitions_version) and \
            _feeder_stands(captured, "E-1"):
        return _unknown_version_result(
            captured, "E-1", denom, _pointer("E-1", pointer, captured))
    if not covered:
        if captured.pieces_of(*_STAFFING_CLASSES):
            return _refusal(
                "E-1", "present but not derivable",
                "no staffed and base pair stands", denom,
                _pointer("E-1", pointer, captured),
                shows="step records and roster artifacts stand and "
                      "no step carries both a staffed count and a "
                      "base count for the same step",
                token="missing-field",
                follows="both fields must stand for the same step, "
                        "so no pair figure stands for any step",
                rule_name="E-1 same step pair rule")
        return _refusal(
            "E-1", "missing", "no staffed and base pair stands",
            denom, _pointer("E-1", pointer, captured),
            shows="no step record and no roster artifact stands in "
                  "the capture for this metric",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="E-1 feeder standing rule")
    steps = sorted(covered)
    if len(steps) > 1 and steps == list(range(steps[0], steps[-1] + 1)):
        figures = ("staffed against base, Steps %d to %d in step "
                   "order: %s" % (steps[0], steps[-1], ", ".join(
                       "%d of %d" % covered[step] for step in steps)))
        coverage = ("Steps %d to %d as kept; denominator step "
                    "universe %d steps; steps counted: %s"
                    % (steps[0], steps[-1], len(universe.evidenced),
                       _each_step(steps)))
    else:
        figures = "; ".join(
            "Step %d: %d of %d" % (step, covered[step][0],
                                   covered[step][1])
            for step in steps)
        coverage = denom + "; steps counted: " + _each_step(steps)
    uncovered = [step for step in universe.evidenced
                 if step not in covered]
    if uncovered:
        coverage += "; steps without both fields: " + \
            _each_step(uncovered)
        coverage += "; covered " + _each_step(steps) + \
            "; remainder " + _each_step(uncovered)
    result = DerivationResult(
        "E-1", "present", figures, coverage,
        _pointer("E-1", pointer, captured),
        rule_name="E-1 staffing pair rule")
    result.coverage = coverage
    bound, reconciled = _e1_bound(steps, uncovered)
    if bound is not None:
        result.bound = bound
        result.reconciled_against = reconciled
    else:
        result.reconciled_against = (
            "the staffed and base counts in the step record "
            "and roster for each covered step, with the "
            "coverage bound restated here: covered %s; "
            "remainder none" % _steps_range_phrase(steps))
    unread_covered = []
    for step in steps:
        for piece in _unread_staffing_pieces(captured, step):
            unread_covered.append((step, piece))
    if unread_covered:
        naming = "; ".join(
            _limit_naming(piece) for _step, piece in unread_covered)
        unread_steps = sorted({step for step, _piece
                               in unread_covered})
        if result.bound is None:
            result.bound = (
                _steps_phrase(unread_steps),
                "the staffing link for "
                + _steps_phrase(unread_steps) + ", resting on "
                + naming,
                "the piece named read in full under the limit "
                "that stopped its reading")
        else:
            result.bound = (
                result.bound[0],
                result.bound[1] + "; the covered steps also "
                "rest on " + naming,
                result.bound[2])
    result.statement = _join_statements(
        _e1_figure_statement(captured, covered),
        _universe_claim_statement(captured, universe))
    return result


def _total_spins(captured, universe):
    """Total spins per step, from the records that state a total.

    Sources stand in an order: the metrics step table spin column
    first, as the snapshot form; then a Total spins field on the
    step own records; then the closing forms that state a total in
    full, the Step 3 budget act actuals, a final or total spin
    count statement, a Spins (E-2) closing entry figure, and a
    gate form share stated as respected, which correct the
    snapshot where they stand.
    """
    totals = {}
    for step, cells in _metrics_step_table(captured).items():
        if len(cells) >= 7:
            m = re.match(r"(\d+)", cells[6])
            if m:
                totals[step] = int(m.group(1))
    for step in universe.evidenced:
        total = _step_field(
            captured, step, (r"Total spins:\s*(\d+)",),
            _STAFFING_CLASSES)
        if total is not None:
            totals[step] = total
    patterns = (
        (r"Step (\d+):\s*(\d+) \(actual", None),
        (r"Step (\d+),\s*(\d+) actual", None),
        (r"Final spin count for Step (\d+):\s*(\d+)", None),
        (r"total spin count for Step (\d+) (?:is|as) (\d+)", None),
        (r"Step (\d+) spins (\d+) in total", None),
        (r"Step (\d+) spins: (\d+) in total", None),
    )
    for piece in captured.pieces:
        if piece.text is None:
            continue
        for pattern, _unused in patterns:
            for m in re.finditer(pattern, piece.text):
                totals[int(m.group(1))] = int(m.group(2))
        if piece.step is not None:
            for pattern in (r"spins for this step (\d+) in total",
                            r"Spins \(E-2\): (\d+) in total",
                            r"spins for the step: (\d+) in total",
                            r"Step \d+ spins (\d+) in total"):
                m = re.search(pattern, piece.text)
                if m:
                    totals[piece.step] = int(m.group(1))
    text = captured.assembled_metrics or ""
    section_step = None
    for line in text.splitlines():
        m = re.match(r"## Step (\d+) closing entry", line)
        if m:
            section_step = int(m.group(1))
            continue
        if line.startswith("## "):
            section_step = None
        if section_step is not None:
            m = re.search(r"Spins \(E-2\): (\d+) in total", line)
            if m:
                totals[section_step] = int(m.group(1))
    for piece in captured.pieces_of(*GATE_CLASSES):
        if piece.text is None:
            continue
        for m in re.finditer(
                r"Step (\d+) share: (\d+) spins, respected",
                piece.text):
            totals[int(m.group(1))] = int(m.group(2))
        if piece.step is not None:
            m = re.search(r"Step \d+ spins (\d+) in total",
                          piece.text)
            if m:
                totals[piece.step] = int(m.group(1))
    return totals


def _credited_totals(captured):
    """Total spins figures credited to the step they describe.

    A figure stored on one step record that describes another step
    stands credited to the described step, under the figure
    crediting rule: the result maps the described step to the
    figure and the path of the record that stores it.
    """
    credited = {}
    for piece in captured.pieces:
        if piece.text is None or \
                piece.record_class not in _STAFFING_CLASSES:
            continue
        for found in re.finditer(r"Total spins for Step (\d+):\s*(\d+)",
                                 piece.text):
            step = int(found.group(1))
            if step not in credited:
                credited[step] = (int(found.group(2)),
                                  piece.paths[0] if piece.paths else "")
    return credited


def _ca9_pairs(captured):
    """The CA-9 detail and stated total pair for a step, where both
    stand in the step own staffing records under one convention."""
    pairs = {}
    for step_piece in captured.pieces:
        if step_piece.text is None or step_piece.step is None or \
                step_piece.record_class not in _STAFFING_CLASSES:
            continue
        detail = _search_int(r"Detail total spins:\s*(\d+)",
                             step_piece.text)
        stated = _search_int(r"Stated total spins:\s*(\d+)",
                             step_piece.text)
        if detail is not None and stated is not None:
            pairs.setdefault(step_piece.step, (detail, stated))
    return pairs


def _spin_disagreements(captured):
    """Total spins disagreements between the metrics record and a
    step record, as (step, metrics figure, record figure, governed)
    in step order. A disagreement stands where the metrics record
    states a total spins figure for a step, in the through form or
    the for form, and the step record for that step states a
    different total. The disagreement is governed where a named
    correction in the records governs the step record figure.
    """
    metrics_text = captured.assembled_metrics or ""
    metrics_figures = {}
    for pattern in (r"Total spins through Step (\d+): (\d+)",
                    r"Total spins for Step (\d+): (\d+)"):
        for found in re.finditer(pattern, metrics_text):
            metrics_figures.setdefault(int(found.group(1)),
                                       int(found.group(2)))
    record_figures = {}
    governed = bool(re.search(r"Correction \S+ governs",
                              metrics_text))
    for piece in captured.pieces:
        if piece.text is None:
            continue
        if re.search(r"Correction \S+ names this figure as "
                     r"governing", piece.text):
            governed = True
        stated = re.search(r"Total spins for Step (\d+): (\d+)",
                           piece.text)
        if stated:
            record_figures.setdefault(int(stated.group(1)),
                                      int(stated.group(2)))
        elif piece.step is not None:
            base_form = re.search(r"Total spins: (\d+)", piece.text)
            if base_form:
                record_figures.setdefault(
                    piece.step, int(base_form.group(1)))
    found_list = []
    for step in sorted(metrics_figures):
        if step in record_figures and \
                record_figures[step] != metrics_figures[step]:
            found_list.append((step, metrics_figures[step],
                               record_figures[step], governed))
    return found_list


def _e2_reconciliation(captured, totals):
    """The E-2 reconciliation clause for a present row.

    Where a record states a closing figure as reconciling on no
    reading, with the supported cumulative positions stated beside
    it, the clause reads the per step series with those supported
    positions and names the rejected figure as not carried. Where
    a per step total spins series stands, the clause names that
    series. Where no total spins figure stands for any step, no
    such series stands to name, and the clause states that the
    metric carries no total to reconcile against, in the WV2-13
    form.
    """
    for piece in captured.pieces:
        if piece.text is None:
            continue
        found = re.search(
            r"figure of (\d+) spins through Step (\d+)[^.]*?"
            r"reconciles on no reading[^.]*?"
            r"\((\d+) through Step (\d+), (\d+) through Step "
            r"(\d+)\)", piece.text)
        if found:
            rejected, rejected_step = int(found.group(1)), \
                int(found.group(2))
            first = (int(found.group(3)), int(found.group(4)))
            second = (int(found.group(5)), int(found.group(6)))
            return (
                "the per step series read with the supported "
                "cumulative positions, %d spins through Step %d "
                "and %d spins through Step %d, the closing figure "
                "of %d spins through Step %d rejected in the "
                "record as reconciling on no reading and not "
                "carried"
                % (first[0], first[1], second[0], second[1],
                   rejected, rejected_step))
    if not totals:
        return ("the metric carries no total to reconcile "
                "against")
    return ("the per step series of total spins stated in the "
            "step records and rosters for the steps counted")


def _derive_e2(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    pointer = captured.first_path(
        CLS_ROSTER, CLS_STEP_RECORD, CLS_STEP_COMPANION) or \
        "steps/step-01-roster.md"
    additions = {}
    totals = _total_spins(captured, universe)
    credited = {step: held for step, held in
                _credited_totals(captured).items()
                if step in universe.evidenced}
    for step, (value, _path) in credited.items():
        totals[step] = value
    ca9 = _ca9_pairs(captured)
    for step, (detail, _stated) in ca9.items():
        if step in universe.evidenced:
            totals[step] = detail
    bases = {}
    entries_steps = set()
    for step in universe.evidenced:
        added = _step_field(
            captured, step, (r"additions over base:\s*(\d+)",),
            _STAFFING_CLASSES)
        if added is not None:
            additions[step] = added
            entries_steps.add(step)
        base = _step_field(captured, step, (r"\bBase:\s*(\d+)",),
                           _STAFFING_CLASSES)
        if base is not None:
            bases[step] = base
    for step, cells in _metrics_step_table(captured).items():
        if len(cells) >= 6 and step not in bases:
            m = re.match(r"(\d+)\s*/\s*(\d+)", cells[5])
            if m:
                bases[step] = int(m.group(2))
    if not _known_version(captured.definitions_version) and \
            _feeder_stands(captured, "E-2"):
        return _unknown_version_result(
            captured, "E-2", denom, _pointer("E-2", pointer, captured))
    if additions:
        add_steps = sorted(additions)
        add_text = " and ".join(
            "Step %d: %d" % (step, additions[step])
            for step in add_steps)
        figures = ("two labelled quantities: additions over base, "
                   + add_text
                   + ", present on " + _steps_phrase(add_steps)
                   + " only and not derivable for the remaining steps")
        total_steps = sorted(totals)
        if total_steps:
            if len(total_steps) > 1 and total_steps == list(
                    range(total_steps[0], total_steps[-1] + 1)):
                figures += ("; total spins for the step, Steps %d "
                            "to %d in step order: %s"
                            % (total_steps[0], total_steps[-1],
                               ", ".join(str(totals[step])
                                         for step in total_steps)))
                coverage = ("total spins, Steps %d to %d; additions "
                            "over base, %s only"
                            % (total_steps[0], total_steps[-1],
                               _steps_phrase(add_steps)))
            else:
                figures += "; " + "; ".join(
                    "Step %d total spins: %d" % (step, totals[step])
                    for step in total_steps)
                coverage = denom + "; additions stated for " + \
                    _each_step(add_steps)
        else:
            coverage = denom + "; additions stated for " + \
                _each_step(add_steps)
        for step in add_steps:
            if step in totals:
                continue
            unread = _unread_staffing_pieces(captured, step)
            if unread:
                naming = _limit_naming(unread[0])
                figures += ("; Step %d total spins: not derivable, "
                            "the total spins figure for that step "
                            "stands in %s and is not read from it"
                            % (step, naming))
                coverage += ("; Step %d: the total spins position "
                             "for that step rests on %s, so no "
                             "absence is claimed for a figure "
                             "whose only home is a piece that was "
                             "not read" % (step, naming))
                continue
            figures += ("; Step %d total spins: not derivable, "
                        "no total spins figure stands for that "
                        "step" % step)
            coverage += ("; Step %d is additions only: its "
                         "records carry roster addition entries "
                         "and state no total spins figure in any "
                         "record, so the total quantity is not "
                         "derivable for that step because no "
                         "total stands for it" % step)
        for step in sorted(ca9):
            if step not in universe.evidenced:
                continue
            detail, stated = ca9[step]
            figures += ("; the CA-9 three labelled figures for "
                        "Step %d: detail total spins: %d, stated "
                        "total spins: %d, variance %d"
                        % (step, detail, stated, abs(detail - stated)))
        for step in sorted(credited):
            value, path = credited[step]
            figures += ("; total spins Step %d: %d, credited from %s"
                        % (step, value, path))
        for step in sorted(universe.evidenced):
            if step in totals and step not in bases:
                coverage += ("; Step %d: missing-field, the base "
                             "position stands absent for that step, "
                             "and no additions figure is printed "
                             "for that step" % step)
            elif step in totals and step in bases and \
                    step not in entries_steps:
                named = any(
                    piece.text and "Named agents:" in piece.text
                    for piece in captured.step_pieces(
                        step, *_STAFFING_CLASSES))
                if not named:
                    coverage += (
                        "; Step %d stands in the second case: the "
                        "stated total and the base position both "
                        "stand, total spins Step %d: %d, with "
                        "base: %d, and no roster addition entries "
                        "and no named agents stand for that step "
                        "in a countable form"
                        % (step, step, totals[step], bases[step]))
        for step, metrics_figure, record_figure, _governed in \
                _spin_disagreements(captured):
            figures += (
                "; the metrics record states total spins through "
                "Step %d as %d, while the step record states "
                "total spins for Step %d as %d; the feeder figure "
                "stands and the record figure is not followed"
                % (step, metrics_figure, step, record_figure))
        result = DerivationResult(
            "E-2", "present", figures, coverage,
            _pointer("E-2", pointer, captured),
            rule_name="E-2 split quantities rule")
        result.coverage = coverage
        result.reconciled_against = _e2_reconciliation(captured, totals)
        result.statement = _join_statements(
            _e2_figure_statement(captured, totals),
            _universe_claim_statement(captured, universe))
        return result
    if totals:
        shows = ("total spins stand for %s and no roster additions "
                 "over base figure stands for any step"
                 % _each_step(sorted(totals)))
        for step in sorted(universe.evidenced):
            if step not in totals:
                continue
            if step not in bases:
                shows += ("; Step %d: missing-field, the base "
                          "position stands absent for that step, "
                          "and no additions figure is printed "
                          "for that step" % step)
            else:
                named = any(
                    piece.text and "Named agents:" in piece.text
                    for piece in captured.step_pieces(
                        step, *_STAFFING_CLASSES))
                if not named:
                    shows += (
                        "; Step %d stands in the second case: the "
                        "stated total and the base position both "
                        "stand, total spins Step %d: %d, with "
                        "base: %d, and no roster addition entries "
                        "and no named agents stand for that step "
                        "in a countable form"
                        % (step, step, totals[step], bases[step]))
        for step, metrics_figure, record_figure, _governed in \
                _spin_disagreements(captured):
            shows += (
                "; the metrics record states total spins through "
                "Step %d as %d, while the step record states "
                "total spins for Step %d as %d; the feeder figure "
                "stands and the record figure is not followed"
                % (step, metrics_figure, step, record_figure))
        return _refusal(
            "E-2", "present but not derivable",
            "no additions over base figure", denom,
            _pointer("E-2", pointer, captured),
            shows=shows,
            token="missing-field",
            follows="a total alone never counts as additions, so "
                    "the additions figure the row requires does not "
                    "stand",
            rule_name="E-2 total alone rule")
    if captured.pieces_of(*_STAFFING_CLASSES):
        return _refusal(
            "E-2", "present but not derivable",
            "no additions over base figure", denom,
            _pointer("E-2", pointer, captured),
            shows="step records and roster artifacts stand and none "
                  "states an additions over base figure or a total "
                  "spins figure",
            token="missing-field",
            follows="neither labelled quantity stands, so no figure "
                    "stands for this row",
            rule_name="E-2 split quantities rule")
    return _refusal(
        "E-2", "missing", "no additions over base figure", denom,
        _pointer("E-2", pointer, captured),
        shows="no step record and no roster artifact stands in the "
              "capture for this metric",
        token="no-feeder-record",
        follows="no feeder record for the metric exists in the "
                "tree, so the row is missing",
        rule_name="E-2 feeder standing rule")


# ------------------------------------------------------------ cost rows

def _ledger_data(captured):
    """The cost ledger figures, read from ledger feeders only.

    Per step money and token figures, the budget figures and any
    stated build total stand parsed from the cost ledger pieces
    inside the root, in the forms the ledger states them: the
    Step N form with money and tokens on one line, the older
    Tokens for Step N and Money for Step N forms, and the Step N
    tokens and Step N money spent forms. A figure credited on one
    step line to the step it describes counts for the step it
    describes, because the describing step form states that step
    in the same Step N position. No other record kind is read
    here, under D4R-24. A second line stating a different figure
    for a step a line already states is a contradiction under
    D4R-21, not a resolution: the first figure stands in the
    returned figures, every differing later figure stands in the
    returned conflicts list in statement order, and no figure
    for a contradicted step is taken by any derivation. The
    budget figures and the stated build totals stand recorded
    in the same form: a first figure for a position stands in
    the returned figures, a later line stating a different
    figure for the same position is recorded in the returned
    budget conflicts or stated build total conflicts, in
    statement order, as (position, first figure, later
    figure), and a later line restating the identical figure
    records nothing. A ledger piece that stands not read past
    a limit supplies no figure here, and it does not vanish:
    the returned unread_ledgers list carries every such piece,
    so a derivation resting on the ledger can stand present
    but not derivable with the bound named, under WV2-09,
    instead of treating the unread ledger as an inspected
    empty one.
    """
    ledgers = captured.pieces_of(CLS_COST_LEDGER)
    pointer = ledgers[0].paths[0] if ledgers else COST_LEDGER_PATH
    money = {}
    tokens = {}
    conflicts = []
    budget_conflicts = []
    total_conflicts = []
    position_values = {"budget_money": None, "budget_tokens": None,
                       "total_money": None, "total_tokens": None}
    position_labels = {"budget_money": "money budget",
                       "budget_tokens": "token budget",
                       "total_money": "build total money",
                       "total_tokens": "build total tokens"}

    def record(store, kind, step, value):
        if step in store and store[step] != value:
            first = store[step]
            if not any(entry[0] == step and entry[1] == kind
                       and entry[2] == first and entry[3] == value
                       for entry in conflicts):
                conflicts.append((step, kind, first, value))
        else:
            store[step] = value

    def record_position(key, value):
        current = position_values[key]
        if current is not None and current != value:
            entry = (position_labels[key], current, value)
            target = budget_conflicts \
                if key.startswith("budget") else total_conflicts
            if entry not in target:
                target.append(entry)
        else:
            position_values[key] = value

    for piece in ledgers:
        if piece.text is None:
            continue
        text = piece.text
        for m in re.finditer(
                r"[Ss]tep (\d+):\s*money (\d+)"
                r"(?:\s*,\s*tokens (\d+))?", text):
            record(money, "money", int(m.group(1)), int(m.group(2)))
            if m.group(3) is not None:
                record(tokens, "tokens", int(m.group(1)),
                       int(m.group(3)))
        for m in re.finditer(
                r"[Ss]tep (\d+):\s*tokens (\d+)"
                r"(?:\s*,\s*money (\d+))?", text):
            record(tokens, "tokens", int(m.group(1)),
                   int(m.group(2)))
            if m.group(3) is not None:
                record(money, "money", int(m.group(1)),
                       int(m.group(3)))
        for m in re.finditer(r"[Ss]tep (\d+) tokens:\s*(\d+)", text):
            record(tokens, "tokens", int(m.group(1)),
                   int(m.group(2)))
        for m in re.finditer(
                r"[Ss]tep (\d+) money(?: spent)?:\s*(\d+)", text):
            record(money, "money", int(m.group(1)), int(m.group(2)))
        for m in re.finditer(r"Tokens for [Ss]tep (\d+):\s*(\d+)",
                             text):
            record(tokens, "tokens", int(m.group(1)),
                   int(m.group(2)))
        for m in re.finditer(r"Money for [Ss]tep (\d+):\s*(\d+)",
                             text):
            record(money, "money", int(m.group(1)), int(m.group(2)))
        for m in re.finditer(
                r"Budget:\s*money (\d+)(?:\s*,\s*tokens (\d+))?",
                text):
            record_position("budget_money", int(m.group(1)))
            if m.group(2) is not None:
                record_position("budget_tokens", int(m.group(2)))
        for m in re.finditer(
                r"Budget:\s*tokens (\d+)(?:\s*,\s*money (\d+))?",
                text):
            record_position("budget_tokens", int(m.group(1)))
            if m.group(2) is not None:
                record_position("budget_money", int(m.group(2)))
        for m in re.finditer(r"Build total stated:\s*money (\d+)",
                             text):
            record_position("total_money", int(m.group(1)))
        for m in re.finditer(r"Build total stated:\s*tokens (\d+)",
                             text):
            record_position("total_tokens", int(m.group(1)))
    unread = [piece for piece in ledgers
              if _piece_over_limit_not_read(piece)]
    return {"ledgers": ledgers, "pointer": pointer, "money": money,
            "tokens": tokens, "unread_ledgers": unread,
            "budget_money": position_values["budget_money"],
            "budget_tokens": position_values["budget_tokens"],
            "total_money": position_values["total_money"],
            "total_tokens": position_values["total_tokens"],
            "conflicts": conflicts,
            "budget_conflicts": budget_conflicts,
            "total_conflicts": total_conflicts}


def _ledger_conflict_text(conflicts):
    """The contradictory ledger figures, both standing, in order."""
    return "; ".join(
        "Step %d %s %d and Step %d %s %d"
        % (step, kind, first, step, kind, second)
        for step, kind, first, second in conflicts)


def _ledger_conflict_refusal(code, denominator, pointer, conflicts):
    """The D4R-21 refusal for a row a ledger contradiction blocks.

    The row stands present but not derivable, its reason names
    both figures for every contradicted step, and neither figure
    is taken: a figure with no governing correction and no feeder
    priority to settle it is unreconciled and blocks its metric.
    """
    figures = {"E-3": "no token figure",
               "E-4": "no per step money figure",
               "B-2": "no budget share figure"}[code]
    text = _ledger_conflict_text(conflicts)
    steps = _each_step({step for step, _kind, _first, _second
                        in conflicts})
    return _refusal(
        code, "present but not derivable", figures, denominator,
        pointer,
        shows="the cost ledger states contradictory figures for "
              "one step, %s, with no governing correction and no "
              "feeder priority standing between the lines, and no "
              "resolution to either line stands" % text,
        token="unreconciled-figure",
        follows="the contradictory figures cannot both stand "
                "and neither is taken, so no figure stands for "
                "the row",
        rule_name=code + " ledger contradiction rule",
        broken="the reconciliation between the contradictory "
               "ledger figures for %s" % steps,
        required="a cost ledger stating one figure for each "
                 "step, or a governing correction settling the "
                 "contradictory figures",
        held="the ledger states %s, and no governing correction "
             "and no feeder priority stands between the lines"
             % text)


def _ledger_disagreement_entries(captured):
    """Disagreements block entries for ledger contradictions.

    One blocking entry per metric each contradiction touches, in
    the D4R-21 form: both figures stand in the entry, the entry
    carries the ungoverned wording, and its first line states
    the metric blocked and that the verdict was withheld for
    this disagreement. A token contradiction touches E-3 and
    B-2; a money contradiction touches E-4 and B-2.
    """
    data = _ledger_data(captured)
    entries = []
    for step, kind, first, second in data["conflicts"]:
        codes = ("E-3", "B-2") if kind == "tokens" else ("E-4", "B-2")
        figures = (
            "the cost ledger states Step %d %s %d and Step %d %s "
            "%d for the same step, with no governing correction "
            "and no feeder priority between the lines"
            % (step, kind, first, step, kind, second))
        for code in codes:
            entries.append((
                "Blocked metric: %s, the verdict was withheld "
                "for this disagreement" % code,
                "Records: %s | Figures: %s | Metric: %s | "
                "Governing position: ungoverned with no verdict "
                "depending on it"
                % (data["pointer"], figures, code)))
    return entries


def _position_conflict_text(conflicts):
    """The contradictory ledger position figures, both standing."""
    return "; ".join(
        "%s %d and %s %d" % (label, first, label, second)
        for label, first, second in conflicts)


def _ledger_position_conflict_refusal(code, denominator, pointer,
                                      conflicts, position_name):
    """The D4R-21 refusal for a row a ledger position
    contradiction blocks, in the form the ledger cure states:
    both figures standing, the conflict recorded, and neither
    figure taken. A budget contradiction blocks B-2, the row
    the budget figures feed; a stated build total contradiction
    blocks E-4, the row the stated build totals feed.
    """
    figures = {"E-4": "no per step money figure",
               "B-2": "no budget share figure"}[code]
    text = _position_conflict_text(conflicts)
    return _refusal(
        code, "present but not derivable", figures, denominator,
        pointer,
        shows="the cost ledger states contradictory %s figures, "
              "%s, with no governing correction and no feeder "
              "priority standing between the lines, and no "
              "resolution to either line stands"
              % (position_name, text),
        token="unreconciled-figure",
        follows="the contradictory figures cannot both stand "
                "and neither is taken, so no figure stands for "
                "the row",
        rule_name=code + " ledger contradiction rule",
        broken="the reconciliation between the contradictory "
               "ledger %s figures" % position_name,
        required="a cost ledger stating one %s figure for the "
                 "position, or a governing correction settling "
                 "the contradictory figures" % position_name,
        held="the ledger states %s, and no governing correction "
             "and no feeder priority stands between the lines"
             % text)


def _ledger_position_disagreement_entries(captured):
    """Disagreements block entries for ledger position
    contradictions, in the D4R-21 form the ledger cure states:
    one blocking entry per metric the contradiction blocks, a
    budget contradiction touching B-2 and a stated build total
    money contradiction touching E-4, each with both figures
    standing and the ungoverned wording. A stated build total
    tokens contradiction touches no metric, because no
    derivation consumes that position, so it carries no
    blocking entry: it stands recorded in the blocking group
    by form only, in the non blocking form the brief Section
    5 composition states for a disagreement that neither
    blocks nor weakens any metric, with both figures standing,
    Metric: none, the ungoverned wording, and a first line
    stating that no verdict was withheld for it.
    """
    data = _ledger_data(captured)
    entries = []
    for conflicts, code in ((data["budget_conflicts"], "B-2"),):
        for label, first, second in conflicts:
            figures = (
                "the cost ledger states %s %d and %s %d for the "
                "same position, with no governing correction and "
                "no feeder priority between the lines"
                % (label, first, label, second))
            entries.append((
                "Blocked metric: %s, the verdict was withheld "
                "for this disagreement" % code,
                "Records: %s | Figures: %s | Metric: %s | "
                "Governing position: ungoverned with no verdict "
                "depending on it"
                % (data["pointer"], figures, code)))
    for label, first, second in data["total_conflicts"]:
        figures = (
            "the cost ledger states %s %d and %s %d for the "
            "same position, with no governing correction and "
            "no feeder priority between the lines"
            % (label, first, label, second))
        if label == "build total tokens":
            entries.append((
                "Blocked metric: none, no verdict was withheld "
                "for this disagreement",
                "Records: %s | Figures: %s | Metric: none | "
                "Governing position: ungoverned with no verdict "
                "depending on it"
                % (data["pointer"], figures)))
        else:
            entries.append((
                "Blocked metric: E-4, the verdict was withheld "
                "for this disagreement",
                "Records: %s | Figures: %s | Metric: E-4 | "
                "Governing position: ungoverned with no verdict "
                "depending on it"
                % (data["pointer"], figures)))
    return entries


def _step_record_money(captured):
    """Per step money figures stated in step record positions.

    A figure counts only where the step record position states
    the figure for that step itself, in the form Money spent for
    this step itself or Money spent for Step N. A whole build
    statement in a step record states no per step figure and is
    never taken here, as brief Section 5 line 193 states. A
    second position stating a different figure for a step a
    position already states, inside one piece or across
    pieces, in either stated form, is a contradiction under
    D4R-21, not a resolution: the first figure stands in the
    returned figures, every differing later figure stands in
    the returned conflicts list in statement order, as (step,
    kind, first figure, later figure) in the ledger conflict
    form, and a later position restating the identical figure
    records nothing.
    """
    money = {}
    pointer = None
    conflicts = []

    def record(step, value):
        if step in money and money[step] != value:
            first = money[step]
            if not any(entry[0] == step and entry[1] == "money"
                       and entry[2] == first and entry[3] == value
                       for entry in conflicts):
                conflicts.append((step, "money", first, value))
        else:
            money[step] = value

    for piece in captured.pieces_of(CLS_STEP_RECORD):
        if piece.text is None:
            continue
        found = False
        for m in re.finditer(
                r"Money spent for this step itself:\s*(\d+)",
                piece.text):
            if piece.step is not None:
                record(piece.step, int(m.group(1)))
                found = True
        for m in re.finditer(
                r"Money spent for [Ss]tep (\d+):\s*(\d+)",
                piece.text):
            record(int(m.group(1)), int(m.group(2)))
            found = True
        if found and pointer is None:
            pointer = piece.paths[0]
    return money, pointer, conflicts


def _step_record_conflict_refusal(denominator, pointer, conflicts):
    """The D4R-21 refusal for the E-4 row a step record money
    contradiction blocks, in the form the ledger cure states:
    both figures standing, the conflict recorded, and neither
    figure taken.
    """
    text = _ledger_conflict_text(conflicts)
    steps = _each_step({step for step, _kind, _first, _second
                        in conflicts})
    return _refusal(
        "E-4", "present but not derivable",
        "no per step money figure", denominator, pointer,
        shows="the step records state contradictory money "
              "figures for one step, %s, with no governing "
              "correction and no feeder priority standing "
              "between the positions, and no resolution to "
              "either position stands" % text,
        token="unreconciled-figure",
        follows="the contradictory figures cannot both stand "
                "and neither is taken, so no figure stands for "
                "the row",
        rule_name="E-4 step record contradiction rule",
        broken="the reconciliation between the contradictory "
               "step record money figures for %s" % steps,
        required="a step record position stating one money "
                 "figure for each step, or a governing "
                 "correction settling the contradictory figures",
        held="the step records state %s, and no governing "
             "correction and no feeder priority stands between "
             "the positions" % text)


def _step_record_disagreement_entries(captured):
    """Disagreements block entries for step record money
    contradictions, in the D4R-21 form the ledger cure states:
    one blocking entry per contradiction, touching E-4, the
    row the step record positions feed, each with both figures
    standing and the ungoverned wording.
    """
    _money, pointer, conflicts = _step_record_money(captured)
    entries = []
    for step, kind, first, second in conflicts:
        figures = (
            "the step records state Step %d %s %d and Step %d %s "
            "%d for the same step, with no governing correction "
            "and no feeder priority between the positions"
            % (step, kind, first, step, kind, second))
        entries.append((
            "Blocked metric: E-4, the verdict was withheld "
            "for this disagreement",
            "Records: %s | Figures: %s | Metric: E-4 | "
            "Governing position: ungoverned with no verdict "
            "depending on it" % (pointer, figures)))
    return entries


def _derive_e3(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    ledger_data = _ledger_data(captured)
    token_conflicts = [entry for entry in ledger_data["conflicts"]
                       if entry[1] == "tokens"]
    if token_conflicts:
        return _ledger_conflict_refusal(
            "E-3", denom,
            _pointer("E-3", ledger_data["pointer"], captured),
            token_conflicts)
    ledger_tokens = ledger_data["tokens"]
    if ledger_tokens and all(step in ledger_tokens
                             for step in universe.evidenced):
        figures = "; ".join(
            "Step %d tokens %d" % (s, ledger_tokens[s])
            for s in sorted(ledger_tokens))
        return DerivationResult(
            "E-3", "present", figures, denom,
            _ledger_data(captured)["pointer"],
            rule_name="E-3 token rule")
    if ledger_tokens:
        covered = sorted(ledger_tokens)
        missing = [step for step in sorted(universe.evidenced)
                   if step not in ledger_tokens]
        return _refusal(
            "E-3", "present but not derivable", "no token figure",
            denom, _ledger_data(captured)["pointer"],
            shows="a cost ledger inside the root meters tokens "
                  "for part of the step universe only, so the "
                  "span the ledger covers stands partial",
            token="partial-span",
            follows="the covered span stands named and no zero "
                    "figure stands for a step the ledger does "
                    "not cover, so no figure stands for the row",
            rule_name="E-3 partial span rule",
            broken="the token figure field for %s, which the "
                   "ledger span does not cover"
                   % _each_step(missing),
            required="a cost ledger entry for each step in the "
                     "universe carrying its token figure",
            held="the ledger covers %s, with %s standing in the "
                 "ledger; no token figure stands for the steps "
                 "outside the covered span"
                 % (_each_step(covered),
                    "; ".join("Step %d tokens %d"
                              % (s, ledger_tokens[s])
                              for s in covered)))
    ledger_pieces = captured.pieces_of(CLS_COST_LEDGER)
    if ledger_pieces:
        unread = ledger_data["unread_ledgers"]
        if unread:
            piece = unread[0]
            naming = _limit_naming(piece)
            return _refusal(
                "E-3", "present but not derivable", "no token figure",
                denom, ledger_pieces[0].paths[0],
                shows="a cost ledger piece stands in the tree at "
                      + naming + ", so no byte of the ledger was "
                      "read and no token figure is taken from it",
                token=_quality_code(piece),
                follows="the row rests on a piece that was not "
                        "read past the bound named, so the row is "
                        "present but not derivable; missing stands "
                        "reserved for the case where no feeder "
                        "record stands in the tree, and no token "
                        "figure is claimed absent from a piece "
                        "that was not read",
                rule_name="E-3 not read past a limit rule",
                broken="the cost ledger token figure field in "
                       + piece.paths[0] + ", which stands not "
                         "read past the limit named in its "
                         "capture reason",
                required="a cost ledger read in full, carrying "
                         "its token figures",
                held="the cost ledger stands in the tree at "
                     + naming)
        return _refusal(
            "E-3", "missing", "no token figure", denom,
            ledger_pieces[0].paths[0],
            shows="a cost ledger piece stands in the capture and "
                  "it carries no token figure in any form the "
                  "row can read, so no token figure stands in "
                  "any feeder record",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in "
                    "the tree, so the row is missing",
            rule_name="E-3 feeder standing rule",
            broken="the cost ledger token figure field",
            required="a cost ledger entry for the step carrying "
                     "its token figure",
            held="the cost ledger stands in the tree and no "
                 "token figure stands in it")
    ledgers = captured.pieces_of(CLS_COST_LEDGER)
    pointer = ledgers[0].paths[0] if ledgers else COST_LEDGER_PATH
    tokens = {}
    for piece in ledgers:
        if piece.text is None:
            continue
        for m in re.finditer(r"Tokens for Step (\d+):\s*(\d+)",
                             piece.text):
            tokens[int(m.group(1))] = int(m.group(2))
    if tokens:
        figures = "; ".join("Step %d tokens %d" % (s, tokens[s])
                            for s in sorted(tokens))
        return DerivationResult("E-3", "present", figures, denom,
                                pointer, rule_name="E-3 token rule")
    statement = None
    assembled = captured.assembled_metrics or ""
    if "cost-ledger" in assembled:
        statement = (
            "the metrics record names registers/cost-ledger.md as "
            "the place a token figure stands recorded, and that "
            "file does not stand in the tree; a mention in the "
            "metrics record is not a feeder figure under R-256")
    register_names = sorted({path.rsplit("/", 1)[-1]
                             for piece in captured.pieces
                             for path in piece.paths
                             if path.startswith("registers/")})
    table = _metrics_step_table(captured)
    tokens_not_recorded = bool(table) and all(
        len(cells) >= 8 and cells[7].startswith("NOT RECORDED")
        for cells in table.values())
    if len(register_names) == 1 and tokens_not_recorded:
        held = ("no cost ledger stands in the tree, the only file "
                "under registers/ is %s, and tokens stand NOT "
                "RECORDED for every step row the metrics record "
                "holds" % register_names[0])
    elif tokens_not_recorded:
        held = ("no cost ledger stands in the tree, and tokens "
                "stand NOT RECORDED for every step row the metrics "
                "record holds")
    else:
        held = "no cost ledger stands in the tree"
    return _refusal(
        "E-3", "missing", "no token figure", denom,
        _pointer("E-3", pointer, captured),
        shows="no cost ledger piece stands in the capture, so no "
              "token figure stands in any feeder record",
        token="no-feeder-record",
        follows="no feeder record for the metric exists in the "
                "tree, so the row is missing",
        rule_name="E-3 feeder standing rule", statement=statement,
        broken="the cost ledger record inside the root",
        required="a cost ledger entry for the step carrying its "
                 "token figure",
        held=held)


def _money_mentions(captured):
    texts = []
    for piece in captured.pieces:
        if piece.text:
            texts.append(piece.text)
    if captured.assembled_metrics:
        texts.append(captured.assembled_metrics)
    joined = "\n".join(texts)
    return joined


def _derive_e4(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    ledger_data = _ledger_data(captured)
    money_conflicts = [entry for entry in ledger_data["conflicts"]
                       if entry[1] == "money"]
    if money_conflicts:
        return _ledger_conflict_refusal(
            "E-4", denom,
            _pointer("E-4", ledger_data["pointer"], captured),
            money_conflicts)
    step_money, step_money_pointer, step_conflicts = \
        _step_record_money(captured)
    if step_conflicts:
        return _step_record_conflict_refusal(
            denom,
            _pointer("E-4",
                     step_money_pointer or ledger_data["pointer"],
                     captured),
            step_conflicts)
    money_total_conflicts = [
        entry for entry in ledger_data["total_conflicts"]
        if entry[0] == "build total money"]
    if money_total_conflicts:
        return _ledger_position_conflict_refusal(
            "E-4", denom,
            _pointer("E-4", ledger_data["pointer"], captured),
            money_total_conflicts, "stated build total")
    merged_money = dict(step_money)
    merged_money.update(ledger_data["money"])
    unread_ledgers = ledger_data["unread_ledgers"]
    if unread_ledgers:
        piece = unread_ledgers[0]
        naming = _limit_naming(piece)
        if merged_money and all(step in merged_money
                                for step in universe.evidenced):
            figures = "; ".join(
                "Step %d money %d" % (s, merged_money[s])
                for s in sorted(merged_money))
            present_pointer = ledger_data["pointer"] \
                if ledger_data["money"] else \
                (step_money_pointer or ledger_data["pointer"])
            result = DerivationResult(
                "E-4", "present", figures, denom, present_pointer,
                rule_name="E-4 money rule")
            result.bound = (
                "the cost ledger feeder at " + piece.paths[0],
                "the per step money link resting on " + naming,
                "the cost ledger read in full under the limit "
                "that stopped its reading")
            return result
        return _refusal(
            "E-4", "present but not derivable",
            "no per step money figure", denom,
            _pointer("E-4", ledger_data["pointer"], captured),
            shows="a cost ledger piece stands in the tree at "
                  + naming + ", so no per step money figure is "
                  "read from it",
            token=_quality_code(piece),
            follows="the row rests on a piece that was not read "
                    "past the bound named, so the row is present "
                    "but not derivable, and no per step money "
                    "figure is claimed absent from a piece that "
                    "was not read",
            rule_name="E-4 not read past a limit rule",
            broken="the per step money figure field in the cost "
                   "ledger at " + piece.paths[0] + ", which "
                     "stands not read past the limit named in "
                     "its capture reason",
            required="a money figure stated by a feeder for the "
                     "step itself, in a cost ledger read in full "
                     "inside the root or in a step record "
                     "position for that step",
            held="the cost ledger stands in the tree at "
                 + naming + ", and no per step money figure is "
                 "taken from a piece that was not read")
    if ledger_data["total_money"] is not None and \
            ledger_data["money"] and \
            sum(ledger_data["money"].values()) != \
            ledger_data["total_money"]:
        return _refusal(
            "E-4", "present but not derivable",
            "no per step money figure", denom,
            _pointer("E-4", ledger_data["pointer"], captured),
            shows="the ledger per step money figures and the "
                  "ledger build total stated in the same ledger "
                  "disagree, and no reconciliation by selection "
                  "stands",
            token="unreconciled-figure",
            follows="the per step figures and the build total "
                    "cannot both stand, so no figure stands "
                    "for the row",
            rule_name="E-4 unreconciled figure rule",
            broken="the reconciliation between the ledger per "
                   "step money figures and the ledger build "
                   "total",
            required="a ledger whose per step money figures "
                     "and stated build total agree",
            held="the ledger per step figures sum to %d and "
                 "the ledger build total stated is %d"
                 % (sum(ledger_data["money"].values()),
                    ledger_data["total_money"]))
    if merged_money and all(step in merged_money
                            for step in universe.evidenced):
        figures = "; ".join(
            "Step %d money %d" % (s, merged_money[s])
            for s in sorted(merged_money))
        present_pointer = ledger_data["pointer"] \
            if ledger_data["money"] else \
            (step_money_pointer or ledger_data["pointer"])
        return DerivationResult("E-4", "present", figures, denom,
                                present_pointer,
                                rule_name="E-4 money rule")
    if merged_money:
        covered = sorted(merged_money)
        missing = [step for step in sorted(universe.evidenced)
                   if step not in merged_money]
        partial_pointer = ledger_data["pointer"] \
            if ledger_data["money"] else \
            (step_money_pointer or ledger_data["pointer"])
        return _refusal(
            "E-4", "present but not derivable",
            "no per step money figure", denom,
            _pointer("E-4", partial_pointer, captured),
            shows="a per step money series stands for part of "
                  "the step universe only, so the series stands "
                  "partial at row level",
            token="partial-span",
            follows="the covered span stands named and no "
                    "figure stands for a step the series does "
                    "not cover, so no figure stands for the row",
            rule_name="E-4 partial series rule",
            broken="the per step money figure field for %s, "
                   "which the series does not cover"
                   % _each_step(missing),
            required="a money figure stated by a feeder for "
                     "each step itself, in a cost ledger inside "
                     "the root or in a step record position for "
                     "that step",
            held="the series covers %s, with %s standing in "
                 "feeders for those steps themselves; no per "
                 "step money figure stands for the steps "
                 "outside the covered span"
                 % (_each_step(covered),
                    "; ".join("Step %d money %d"
                              % (s, merged_money[s])
                              for s in covered)))
    ledgers = captured.pieces_of(CLS_COST_LEDGER)
    pointer = ledgers[0].paths[0] if ledgers else COST_LEDGER_PATH
    money = {}
    for piece in ledgers:
        if piece.text is None:
            continue
        for m in re.finditer(r"Money for Step (\d+):\s*(\d+)",
                             piece.text):
            money[int(m.group(1))] = int(m.group(2))
    if money and all(s in money for s in universe.evidenced):
        figures = "; ".join("Step %d money %d" % (s, money[s])
                            for s in sorted(money))
        return DerivationResult("E-4", "present", figures, denom,
                                pointer, rule_name="E-4 money rule")
    joined = _money_mentions(captured)
    claims_field = "per step money field" in joined or \
        "per-step money" in joined
    any_money = re.search(r"\bmoney\b", joined, re.I) is not None
    if ledgers or claims_field or any_money:
        step_pointer = captured.first_path(CLS_STEP_RECORD) or pointer
        table = _metrics_step_table(captured)
        missing_steps = [step for step, cells in sorted(table.items())
                         if len(cells) >= 9
                         and cells[8].startswith("NOT RECORDED")]
        if missing_steps:
            span = "Steps %d to %d" % (missing_steps[0],
                                        missing_steps[-1])
            broken = "the per step money figure field for " + span
            held_clauses = ["no feeder states a per step money "
                            "figure for " + span]
            no_field = []
            for step in missing_steps:
                texts = [piece.text or "" for piece in
                         captured.step_pieces(
                             step, CLS_STEP_RECORD, CLS_ROSTER,
                             CLS_STEP_COMPANION)]
                if not any("money" in text.lower() for text in texts):
                    no_field.append(step)
                else:
                    break
            if len(no_field) >= 2:
                held_clauses.append(
                    "Steps %d and %d carry no money field in any "
                    "feeder" % (no_field[0], no_field[1]))
            whole = None
            for piece in captured.pieces_of(CLS_STEP_RECORD):
                if piece.text is None:
                    continue
                m = re.search(
                    r"(\d+) external spend for the whole build",
                    piece.text)
                if m:
                    whole = (piece.step, m.group(1))
                    break
            if whole is not None and whole[0] is not None:
                held_clauses.append(
                    "the Step %d step record states %s external "
                    "spend for the whole build only" % whole)
            if not ledgers:
                held_clauses.append("no cost ledger stands in the "
                                    "tree")
            held = _held_join(held_clauses)
        else:
            broken = "the per step money figure field for the steps"
            held = ("no feeder states a per step money figure for "
                    "the steps the row spans")
        return _refusal(
            "E-4", "present but not derivable", "no per step money "
            "figure", denom, _pointer("E-4", step_pointer, captured),
            shows="a money statement or a money field claim stands "
                  "in the records and no per step money figure "
                  "stands for the steps the row spans",
            token="missing-field",
            follows="the per step money field the row requires "
                    "does not stand in the feeder records, so no "
                    "figure stands",
            rule_name="E-4 per step money field rule",
            broken=broken,
            required="a money figure stated by a feeder for the "
                     "step itself, in a cost ledger inside the "
                     "root or in a step record position for that "
                     "step",
            held=held)
    return _refusal(
        "E-4", "missing", "no per step money figure", denom, pointer,
        shows="no cost ledger piece and no step record in the "
              "capture carries a money figure for this metric",
        token="no-feeder-record",
        follows="no feeder record for the metric exists in the "
                "tree, so the row is missing",
        rule_name="E-4 feeder standing rule")


# ------------------------------------------------------- F-2, Q-1, Q-3

def _provisional_rate(captured):
    """The provisional F-2 rate a record states, or None.

    The rate stands in the metrics record snapshot form, or in a
    piece in the plain form, in each case as report text only: it
    is derived from no final closing states and is never the row
    figure.
    """
    rate = None
    text = captured.assembled_metrics or ""
    section_step = None
    for line in text.splitlines():
        m = re.match(r"## Step (\d+) step snapshot", line)
        if m:
            section_step = int(m.group(1))
        m = re.search(r"First-time approval rate so far \(F-2\): "
                      r"(\d+) of (\d+)", line)
        if m:
            rate = (m.group(1), m.group(2), section_step)
    if rate is None:
        for piece in captured.pieces:
            if piece.text is None:
                continue
            m = re.search(r"First-time approval rate so far: "
                          r"(\d+) of (\d+)", piece.text)
            if m:
                rate = (m.group(1), m.group(2), piece.step)
                break
    return rate


_F2_CLOSURE_PLAIN = "CLOSED-PASS"
_F2_CLOSURE_QUALIFIED = "CLOSED-QUALIFIED"
_F2_CLOSURE_NOT_APPROVED = ("CLOSED-FAIL", "RECYCLED")

_HISTORY_PATTERNS = (r"gate history", r"outcome word stands scattered",
                     r"stands scattered in this record")


def _gate_facts(captured):
    """The gate outcome facts for this capture, from the Inventory
    gate outcome reading the slice delivers, in its landed form:
    a dict by instance key whose counted sources are the gate
    record, gate ruling and regate forms, whose adjudication
    sources stand as evidence only, and whose first closure state
    and first ruling outcome stand in source order.
    """
    from metrics_starter_collector.inventory import \
        gate_outcome_facts
    return gate_outcome_facts(captured.pieces)


def _f2_history_steps(captured, counted_steps):
    """Steps whose ruling stands only in a step record gate history
    or as a scattered outcome word in a step record, record kinds
    the F-2 chain never reads as a first ruling feeder."""
    steps = set()
    for piece in captured.pieces_of(CLS_STEP_RECORD):
        if piece.text is None or piece.step is None:
            continue
        if piece.step in counted_steps:
            continue
        lowered = piece.text.lower()
        if any(re.search(pattern, lowered)
               for pattern in _HISTORY_PATTERNS):
            steps.add(piece.step)
    return steps


def _derive_f2(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    gates = captured.pieces_of(*GATE_CLASSES)
    pointer = gates[0].paths[0] if gates else \
        "steps/step-01-gate-record.md"
    try:
        facts = _gate_facts(captured)
    except Exception as exc:
        gate_paths = ", ".join(piece.paths[0] for piece in gates) \
            if gates else "the gate pieces in the capture"
        error = _error_form("gate_outcome_facts", gate_paths, exc)
        return _refusal(
            "F-2", "present but not derivable",
            "no first ruling figure", denom,
            _pointer("F-2", pointer, captured),
            shows="the Inventory gate outcome reading failed and "
                  "no gate facts stand for this row: " + error,
            token="missing-field",
            follows="the gate outcome facts the row requires do "
                    "not stand, so no rate figure stands and no "
                    "fallback reading is substituted",
            rule_name="F-2 gate outcome reading rule",
            statement=error,
            broken="the gate outcome facts from the Inventory "
                   "gate outcome reading",
            required="the gate outcome facts standing from the "
                     "Inventory gate outcome reading",
            held=error)
    counted = {key: fact for key, fact in facts.items()
               if fact["counted_sources"]}
    adjudication_only = {key: fact for key, fact in facts.items()
                         if fact["adjudication_only"]}
    near_only = {key: fact for key, fact in facts.items()
                 if fact["missing_gate"] and fact["near_match_sources"]}
    counted_steps = {fact["step"] for fact in counted.values()}
    history_steps = _f2_history_steps(captured, counted_steps)
    if not counted and not adjudication_only and not near_only and \
            not history_steps:
        return _refusal(
            "F-2", "missing", "no first ruling figure", denom,
            pointer,
            shows="no gate record, gate ruling or gate adjudication "
                  "stands in the capture for this metric",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="F-2 feeder standing rule")
    if not _known_version(captured.definitions_version):
        return _unknown_version_result(
            captured, "F-2", denom, _pointer("F-2", pointer, captured))
    plain = 0
    qualified = 0
    ruled = 0
    closing_plain = 0
    closing_qualified = 0
    closing_ruled = 0
    closing_alone = []
    problems = []
    counted_labels = []
    for key in sorted(counted, key=lambda k: (counted[k]["step"], k)):
        fact = counted[key]
        label = _instance_label(key)
        if fact["disagreement"]:
            problems.append(
                "the gate record and gate ruling for %s disagree "
                "on the first ruling, stating %s, and the "
                "disagreement stands stated and is not resolved"
                % (label, " and ".join(fact["disagreement_forms"])))
            continue
        closure = fact["first_closure_state"]
        outcome = fact["first_ruling_outcome"]
        if outcome is not None:
            ruled += 1
            counted_labels.append(label)
            if outcome == "Go":
                if closure == _F2_CLOSURE_QUALIFIED:
                    qualified += 1
                else:
                    plain += 1
        elif closure == _F2_CLOSURE_PLAIN:
            # A closing state alone records no first ruling
            # outcome, so no approval stands on it in any
            # mixture, under D4R-13 and DG-01: the instance is
            # tallied apart here and, where a rate stands over
            # the outcome carrying instances, it is excluded
            # from the numerator and from the denominator alike
            # and named in the coverage, in the DG-08 mixed
            # tree form.
            closing_plain += 1
            closing_ruled += 1
            closing_alone.append(key)
        elif closure == _F2_CLOSURE_QUALIFIED:
            closing_qualified += 1
            closing_ruled += 1
            closing_alone.append(key)
        elif closure in _F2_CLOSURE_NOT_APPROVED:
            closing_ruled += 1
            closing_alone.append(key)
        else:
            problems.append(
                "%s stands with recorded closure state %s, which "
                "matches no named closure form in the hardened "
                "closure state vocabulary"
                % (label, closure if closure is not None
                   else "none stated"))
    approved = plain + qualified
    excluded_clauses = []
    for key in sorted(closing_alone,
                      key=lambda k: (counted[k]["step"], k)):
        excluded_clauses.append(
            "a ruling for %s stands in a gate record or gate "
            "ruling with a closing state alone and no first "
            "ruling outcome recorded for the step, and the step "
            "is excluded from the numerator and from the "
            "denominator alike" % _instance_label(key))
    for key in sorted(adjudication_only,
                      key=lambda k: (adjudication_only[k]["step"], k)):
        excluded_clauses.append(
            "a ruling for %s stands only in a gate adjudication "
            "record, a record kind the chain cannot count as a "
            "first ruling feeder, and the step is excluded from "
            "the numerator and from the denominator alike"
            % _instance_label(key))
    for step in sorted(history_steps):
        excluded_clauses.append(
            "a ruling for Step %d stands only in a step record "
            "gate history, a record kind the chain cannot count "
            "as a first ruling feeder, and the step is excluded "
            "from the numerator and from the denominator alike"
            % step)
    for key in sorted(near_only, key=lambda k: (near_only[k]["step"], k)):
        excluded_clauses.append(
            "a gate outcome for %s stands only under a near match "
            "name outside the gate alias set, and that name is "
            "not read as a gate file" % _instance_label(key))
    if counted and not problems:
        # No rate is derived from final closing states alone,
        # on any tree shape: a final closing state does not
        # record whether the first ruling approved the step,
        # so where no counted gate instance carries a first
        # ruling outcome at all, the row stands present but
        # not derivable in the D4R-13 form, whether the counted
        # gate files stand for the whole evidenced universe or
        # for part of it, and under one gate name or both.
        outcomes_stand = any(
            fact["first_ruling_outcome"] is not None
            for fact in counted.values())
        gate_classes = {piece.record_class for piece in gates}
        if not outcomes_stand:
            clause = (
                "no first ruling outcome is recorded per step "
                "in one named place for the steps the row spans")
            if CLS_GATE_RECORD in gate_classes and \
                    CLS_GATE_RULING in gate_classes:
                clause += (
                    ", the gate outcomes standing scattered "
                    "across gate records and gate rulings under "
                    "both names")
            problems.append(clause)
    if problems or not counted:
        held_clauses = []
        classes = {piece.record_class for piece in gates}
        if CLS_GATE_RECORD in classes and CLS_GATE_RULING in classes:
            held_clauses.append(
                "gate outcomes stand scattered across gate records and "
                "gate rulings under both names")
        rate = _provisional_rate(captured)
        if rate is not None and rate[2] is not None:
            held_clauses.append(
                "the only rate in the tree is provisional and partial "
                "at %s of %s in the Step %d snapshot" % rate)
        held_clauses.append("no rate is derived from final closing "
                            "states")
        held = _held_join(held_clauses)
        extras = []
        if ruled or closing_ruled:
            extras.append(
                "plain closures %d and qualified closures %d stand "
                "counted on the steps whose first ruling stands in "
                "a named form" % (plain + closing_plain,
                                   qualified + closing_qualified))
        extras.extend(problems)
        extras.extend(excluded_clauses)
        if extras:
            held = held + "; " + "; ".join(extras)
        return _refusal(
            "F-2", "present but not derivable", "no first ruling figure",
            denom, _pointer("F-2", pointer, captured),
            shows="gate files stand for the steps and no first ruling "
                  "outcome field stands recorded in one named place for "
                  "the steps the row spans",
            token="missing-field",
            follows="the first ruling outcome field the row requires "
                    "does not stand, so no rate figure stands",
            rule_name="F-2 first ruling outcome field rule",
            statement=_universe_claim_statement(captured, universe),
            broken="the first ruling outcome field recorded per step "
                   "in one named place",
            required="a first ruling outcome recorded per step in one "
                     "named place, in the Auditor approval row form",
            held=held)
    figures = ("first-time approval rate: %d of %d approved, plain "
               "closures %d, qualified closures %d"
               % (approved, ruled, plain, qualified))
    coverage = ("denominator: %d steps ruled on; steps counted: %s"
                % (ruled, ", ".join(counted_labels)))
    fact_steps = {fact["step"] for fact in facts.values()}
    for step in sorted(universe.evidenced):
        if step not in fact_steps and step not in history_steps:
            coverage += ("; Step %d stands with no gate record or "
                         "gate ruling and is not counted in the "
                         "denominator" % step)
    coverage += "".join("; " + clause for clause in excluded_clauses)
    for key in sorted(counted, key=lambda k: (counted[k]["step"], k)):
        if key in closing_alone:
            continue
        fact = counted[key]
        if fact["recycled"]:
            coverage += ("; %s recycled instance counted once, by "
                         "its first ruling" % _instance_label(key))
        marker = fact["instance"]
        if marker:
            plain_key = "step-%d" % fact["step"]
            if plain_key in universe.instances:
                coverage += (
                    "; the figures of the replaced instance %s "
                    "stand named as replaced under the replaced "
                    "instance key and are not merged into the "
                    "closing instance %s"
                    % (_instance_label(plain_key),
                       _instance_label(key)))
    first_path = pointer
    for key in sorted(counted, key=lambda k: (counted[k]["step"], k)):
        if key in closing_alone:
            continue
        if counted[key]["counted_sources"]:
            first_path = counted[key]["counted_sources"][0]["path"] \
                or pointer
            break
    result = DerivationResult(
        "F-2", "present", figures, coverage,
        _pointer("F-2", first_path, captured),
        rule_name="F-2 first ruling rule")
    result.numerator = approved
    result.denominator_part = ruled
    result.coverage = coverage
    statements = [_universe_claim_statement(captured, universe)]
    rate = _provisional_rate(captured)
    if rate is not None and rate[2] is not None and \
            (int(rate[0]), int(rate[1])) != (approved, ruled):
        statements.append(
            "record disagrees: %s states a provisional first-time "
            "approval rate of %s of %s in the Step %d snapshot, "
            "while the gate records state %d of %d approved; the "
            "feeder figure stands and the provisional figure is "
            "not followed"
            % (_metrics_record_name(captured), rate[0], rate[1],
               rate[2], approved, ruled))
    result.statement = _join_statements(*statements)
    return result


# ------------------------------------------------------------- Q-1

_Q1_SEVERITIES = ("Critical", "High", "Medium", "Low")


def _q1_counts(segment):
    counts = {}
    for name in _Q1_SEVERITIES:
        found = re.search(name + r"\s+(\d+)", segment or "")
        if found:
            counts[name] = int(found.group(1))
    return counts


def _q1_counts_text(counts):
    return ", ".join("%s %d" % (name, counts[name])
                     for name in _Q1_SEVERITIES if name in counts)


def _q1_round_before(text, at, piece):
    before = text[:at]
    rounds = re.findall(r"Round (\d+)", before)
    if rounds:
        return int(rounds[-1])
    lines = text.splitlines()
    if lines:
        found = re.search(r"Round (\d+)", lines[0])
        if found:
            return int(found.group(1))
    return piece.step if piece.step is not None else 1


def _q1_carrier_form(path, piece):
    if "fix-register" in path:
        return "fix register round table"
    if "defect-register" in path:
        return "defect register round summary"
    if "audit-register" in path:
        return "audit register round entry"
    if piece.record_class == CLS_GATE_RECORD or "gate-record" in path:
        return "gate record round section"
    return "carrier record"


def _q1_scale_name(raw):
    if raw is None:
        return None
    lowered = raw.lower()
    if "flow" in lowered:
        return "flow scale"
    if "commissioned" in lowered:
        return "commissioned scale"
    return raw.strip()


def _q1_carrier_candidates(captured):
    """Carrier form breakdowns, and those no round record names.

    A carrier counts only where a round record names it as the
    carrier record for its round, only where triage is stated and
    a scale is named, and only in one of the four listed carrier
    forms, with the sanctioned headings standing in their exact
    form: a fix register round table, a defect register round
    summary, an audit register round entry, or a gate record
    round section.
    """
    named = {}
    for piece in captured.pieces:
        if piece.text is None:
            continue
        for found in re.finditer(
                r"names\s+(\S+)\s+as the carrier record for "
                r"Round (\d+)", piece.text):
            named.setdefault(found.group(1), set()).add(
                int(found.group(2)))
        for found in re.finditer(
                r"(?<!\S)(\S+)\s+is named as the carrier record for "
                r"Round (\d+)", piece.text):
            named.setdefault(found.group(1), set()).add(
                int(found.group(2)))
        for found in re.finditer(
                r"names\s+(\S+)\s+as the carrier record for both "
                r"rounds", piece.text):
            named[found.group(1)] = None
    candidates = []
    unnamed = []
    for piece in captured.pieces:
        if piece.text is None:
            continue
        path = piece.paths[0]
        text = piece.text
        found_list = []
        lines = text.splitlines()
        for at, line in enumerate(lines):
            if not line.strip().startswith("|"):
                continue
            cells = [cell.strip().lower().replace("-", " ")
                     for cell in line.strip().strip("|").split("|")]
            if cells[:4] != ["round", "post triage breakdown",
                             "triage run", "severity scale"]:
                continue
            for row in lines[at + 1:]:
                if not row.strip().startswith("|"):
                    break
                rcells = [cell.strip() for cell in
                          row.strip().strip("|").split("|")]
                if len(rcells) < 4 or set(rcells[0]) <= set("- "):
                    continue
                round_found = re.search(r"Round (\d+)", rcells[0])
                if not round_found:
                    continue
                found_list.append({
                    "round": int(round_found.group(1)),
                    "counts": _q1_counts(rcells[1]),
                    "triage": "triage has run" in rcells[2].lower(),
                    "scale": _q1_scale_name(rcells[3]),
                    "form": _q1_carrier_form(path, piece),
                    "path": path, "attacks": False})
        for found in re.finditer(
                r"## Round (?:summary|entry|section): Round (\d+)",
                text):
            tail = text[found.end():]
            nxt = tail.find("\n## ")
            section = tail[:nxt] if nxt > 0 else tail
            breakdown = re.search(
                r"[Pp]ost triage breakdown:?\s*\n?\s*"
                r"((?:(?:Critical|High|Medium|Low)\s+\d+"
                r"(?:,\s*)?)+)", section)
            scale_found = re.search(
                r"Severity scale:?\s*\n?\s*([A-Za-z ]+?scale)",
                section)
            found_list.append({
                "round": int(found.group(1)),
                "counts": _q1_counts(breakdown.group(1))
                if breakdown else {},
                "triage": "triage has run" in section.lower(),
                "scale": _q1_scale_name(scale_found.group(1))
                if scale_found else None,
                "form": _q1_carrier_form(path, piece),
                "path": path,
                "attacks": "grading attacks" in section.lower()})
        for candidate in found_list:
            if path in named and (named[path] is None
                                  or candidate["round"]
                                  in named[path]):
                candidates.append(candidate)
            else:
                unnamed.append(candidate)
    return candidates, unnamed


def _q1_direct_candidates(captured):
    """Breakdowns in a round own record, or a record it names.

    Returns (counted, nonflow, excluded, incomplete_paths). A
    breakdown counts only where its counted units are findings
    from that round: attack totals and grading attacks are
    refused, and a pre triage breakdown is refused. A paper that
    states it carries no closing total, and a paper failing a
    completeness signal, counts toward nothing: its visible part
    is treated as truncated.
    """
    counted = []
    nonflow = []
    excluded = []
    incomplete = []
    for piece in captured.pieces:
        if piece.text is None:
            continue
        if piece.record_class in (
                CLS_METRICS_SINGLE, CLS_METRICS_PAGE,
                CLS_GATE_ADJUDICATION, CLS_GATE_RECORD,
                CLS_GATE_RULING, CLS_STEP_RECORD,
                CLS_STEP_COMPANION, CLS_PATH_LEDGER,
                CLS_TIER_RECORD, CLS_DECISION_QUEUE):
            continue
        path = piece.paths[0]
        if "correct" in path or "register" in path:
            continue
        text = piece.text
        if _signal_failure(text) is not None:
            incomplete.append(path)
            continue
        repaired = "## Completion section" in text and \
            "was found truncated" in text
        if "no closing total" in text and not repaired:
            incomplete.append(path)
            continue
        for found in re.finditer(
                r"[Pp]ost triage (?:severity )?breakdown", text):
            segment = text[found.start():found.start() + 240]
            counts = _q1_counts(segment)
            if not counts:
                continue
            rnd = _q1_round_before(text, found.start(), piece)
            lowered = segment.lower()
            if "grading attacks" in lowered \
                    or "attacks only" in lowered:
                excluded.append((rnd, "attack totals refused, "
                                      "grading attacks not findings"))
                continue
            scale = "flow scale"
            scale_found = re.search(r"[Ss]cale ([A-Z])\b", segment)
            if "commissioned scale" in lowered:
                scale = "commissioned scale"
            elif "flow scale" in lowered:
                scale = "flow scale"
            elif scale_found:
                scale = "Scale " + scale_found.group(1)
            candidate = {"round": rnd, "counts": counts,
                         "scale": scale,
                         "form": "round record" if "round-record"
                         in path else "audit paper round record",
                         "path": path, "attacks": False,
                         "triage": True,
                         "repaired": repaired}
            if scale == "flow scale":
                counted.append(candidate)
            else:
                nonflow.append(candidate)
        for found in re.finditer(r"[Pp]re triage", text):
            rnd = _q1_round_before(text, found.start(), piece)
            clause = (rnd, "no post triage breakdown, pre triage "
                           "counts only")
            if clause not in excluded:
                excluded.append(clause)
        for found in re.finditer(r"Attack totals", text):
            rnd = _q1_round_before(text, found.start(), piece)
            clause = (rnd, "attack totals refused, grading "
                           "attacks not findings")
            if clause not in excluded:
                excluded.append(clause)
    return counted, nonflow, excluded, incomplete


def _q1_wv6_conflict(captured):
    """Rounds governed by two scales in conflict, under WV-6.

    A later governing statement resolving the conflict leaves the
    row judged on its records, and the superseded conflict blocks
    nothing.
    """
    governed = {}
    resolved = False
    for piece in captured.pieces_of(CLS_GATE_ADJUDICATION):
        if piece.text is None:
            continue
        if "resolves the conflict" in piece.text:
            resolved = True
        for found in re.finditer(
                r"Scale (\w+) governs (Rounds? [^.\n]+)",
                piece.text):
            for rnd in re.findall(r"\d+", found.group(2)):
                governed.setdefault(int(rnd), set()).add(
                    found.group(1))
    if resolved:
        return []
    return sorted(rnd for rnd, scales in governed.items()
                  if len(scales) > 1)


def _q1_disagreements(captured, counted):
    """Per round disagreements between the feeder and a record.

    Returns a list of (round, feeder_path, feeder_counts,
    other_path, other_counts) where another record states a
    different post triage breakdown for a counted round.
    """
    found_list = []
    by_round = {}
    for candidate in counted:
        by_round.setdefault(candidate["round"], candidate)
    for piece in captured.pieces:
        if piece.text is None:
            continue
        path = piece.paths[0]
        for found in re.finditer(
                r"[Pp]ost triage (?:severity )?breakdown", piece.text):
            feeder = by_round.get(
                _q1_round_before(piece.text, found.start(), piece))
            if feeder is None or feeder["path"] == path:
                continue
            counts = _q1_counts(
                piece.text[found.start():found.start() + 240])
            if counts and counts != feeder["counts"]:
                entry = (feeder["round"], feeder["path"],
                         feeder["counts"], path, counts)
                if entry not in found_list:
                    found_list.append(entry)
    return found_list


def _q1_statement(captured, counted):
    statements = []
    try:
        from metrics_starter_collector.cross_check import \
            q1_cross_check_statement
        marking = q1_cross_check_statement(
            captured, {candidate["round"]: candidate["counts"]
                       for candidate in counted})
        if marking:
            statements.append(marking)
    except Exception as exc:
        statements.append(_error_form(
            "q1_cross_check_statement",
            _metrics_record_name(captured), exc))
    for rnd, feeder_path, feeder_counts, other_path, other_counts \
            in _q1_disagreements(captured, counted):
        statements.append(
            "record disagrees: %s states post triage breakdown %s "
            "for Round %d, while the feeder record %s states %s "
            "for Round %d; the feeder figure stands and the record "
            "figure is not followed"
            % (other_path, _q1_counts_text(other_counts), rnd,
               feeder_path, _q1_counts_text(feeder_counts), rnd))
    return "; ".join(statements) if statements else None


def _derive_q1(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    papers = captured.pieces_of(CLS_AUDIT_PAPER, CLS_FIX_REGISTER)
    pointer = papers[0].paths[0] if papers else \
        "audit/step-01-audit-paper.md"
    pointer = _pointer("Q-1", pointer, captured)
    feeder_pieces = [piece for piece in captured.pieces
                     if piece.record_class in (
                         CLS_AUDIT_PAPER, CLS_FIX_REGISTER,
                         CLS_DEFECT_REGISTER, CLS_OTHER_REGISTER,
                         CLS_GATE_ADJUDICATION)]
    if not _known_version(captured.definitions_version) and \
            feeder_pieces:
        return _unknown_version_result(captured, "Q-1", denom, pointer)
    if not feeder_pieces:
        return _refusal(
            "Q-1", "missing", "no audit round figure", denom, pointer,
            shows="no audit round record stands in the capture for "
                  "this metric",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="Q-1 feeder standing rule")
    conflicted = _q1_wv6_conflict(captured)
    if conflicted:
        return _refusal(
            "Q-1", "present but not derivable", "no audit round figure",
            denom, pointer,
            shows="two governing adjudications stand in conflict "
                  "over the same rounds, and the conflict covers "
                  + ", ".join("Round %d" % rnd for rnd in conflicted)
                  + ", the blocked scope, while rounds outside the "
                    "covered rounds are judged on their own records",
            token="governing-scale-conflict",
            follows="the governing scale for the covered rounds "
                    "does not stand settled, so no figure stands "
                    "for those rounds",
            rule_name="WV-6 conflicting governing adjudications rule")
    counted, nonflow, excluded, incomplete = \
        _q1_direct_candidates(captured)
    carrier, unnamed = _q1_carrier_candidates(captured)
    silent = []
    for candidate in carrier:
        if candidate["attacks"]:
            clause = (candidate["round"],
                      "attack totals refused, grading attacks not "
                      "findings")
            if clause not in excluded:
                excluded.append(clause)
            continue
        if not candidate["counts"] or not candidate["triage"]:
            continue
        if candidate["scale"] is None:
            silent.append(candidate)
        elif candidate["scale"] == "flow scale":
            counted.append({
                "round": candidate["round"],
                "counts": candidate["counts"], "scale": "flow scale",
                "form": candidate["form"], "path": candidate["path"],
                "attacks": False, "triage": True})
        else:
            nonflow.append({
                "round": candidate["round"],
                "counts": candidate["counts"],
                "scale": candidate["scale"],
                "form": candidate["form"], "path": candidate["path"],
                "attacks": False, "triage": True})
    for piece in captured.pieces_of(CLS_GATE_ADJUDICATION):
        if piece.text is None:
            continue
        for found in re.finditer(
                r"Round (\d+) post triage breakdown:\s*"
                r"((?:(?:Critical|High|Medium|Low)\s+\d+"
                r"(?:,\s*)?)+)",
                piece.text):
            scale = "commissioned scale" \
                if "commissioned" in piece.text.lower() \
                else "flow scale"
            candidate = {"round": int(found.group(1)),
                         "counts": _q1_counts(found.group(2)),
                         "scale": scale, "form": "gate adjudication",
                         "path": piece.paths[0], "attacks": False,
                         "triage": True}
            if scale == "flow scale":
                counted.append(candidate)
            else:
                nonflow.append(candidate)
    # One feeder figure per round: where two records state
    # different breakdowns for one round, the round record figure
    # stands as the feeder and the other stands as a disagreement,
    # recorded in the statement line, never overriding the feeder.
    deduped = {}
    for candidate in counted:
        rnd = candidate["round"]
        current = deduped.get(rnd)
        if current is None or (
                "round-record" in candidate["path"]
                and "round-record" not in current["path"]):
            deduped[rnd] = candidate
    counted = [deduped[rnd] for rnd in sorted(deduped)]
    # A correcting record standing for a truncated paper supplies
    # the substitution, cited as the source.
    truncated_papers = [piece for piece in captured.pieces
                        if piece.text is None
                        and piece.record_class == CLS_AUDIT_PAPER
                        and piece.paths[0].endswith(".md")]
    correction = None
    correction_counts = None
    for piece in captured.pieces:
        if piece.text is None or "correct" not in piece.paths[0]:
            continue
        if "corrected total" in piece.text:
            found_counts = _q1_counts(piece.text)
            if found_counts:
                correction, correction_counts = piece, found_counts
                break
    if correction is not None and truncated_papers:
        counted = [{"round": truncated_papers[0].step or 1,
                    "counts": correction_counts, "scale": "flow scale",
                    "form": "correcting record " + correction.paths[0],
                    "path": correction.paths[0], "attacks": False,
                    "triage": True}]
        result = _q1_present_result(
            captured, counted, excluded, denom, pointer)
        return result
    if nonflow:
        held = []
        for candidate in nonflow:
            held.append(
                "the Round %d breakdown stands under %s in %s, "
                "stating %s, and that scale does not govern the "
                "row in the flow form"
                % (candidate["round"], candidate["scale"],
                   candidate["form"],
                   _q1_counts_text(candidate["counts"])))
        for rnd, why in excluded:
            held.append("Round %d stands excluded, %s" % (rnd, why))
        return _refusal(
            "Q-1", "present but not derivable", "no audit round figure",
            denom, pointer,
            shows="audit records stand and the breakdowns stand "
                  "under scales that conflict with the flow scale",
            token="governing-scale-conflict",
            follows="mixed severity scales stand, so no figure "
                    "stands in the flow form",
            rule_name="Q-1 severity scale rule",
            broken="the post triage severity breakdown field under "
                   "the flow scale",
            required="a post triage breakdown under the flow scale "
                     "in the round own record or in a record the "
                     "round record names",
            held=_held_join(held))
    if counted:
        return _q1_present_result(
            captured, counted, excluded, denom, pointer)
    if silent:
        candidate = silent[0]
        return _refusal(
            "Q-1", "present but not derivable", "no audit round figure",
            denom, pointer,
            shows="a carrier breakdown stands for Round %d and no "
                  "scale is stated for that breakdown"
                  % candidate["round"],
            token="missing-field",
            follows="the scale and record form pair does not "
                    "stand for the breakdown, so no pair is counted "
                    "and no figure stands",
            rule_name="Q-1 scale and record form pair rule",
            broken="the severity scale field of the carrier "
                   "breakdown for Round %d" % candidate["round"],
            required="the scale and record form pair per counted "
                     "round, the pair travelling together",
            held="the %s for Round %d states its carrier form "
                 "together with the words no scale stated for that "
                 "breakdown" % (candidate["form"], candidate["round"]))
    damaged = [piece for piece in truncated_papers
               if "round-record" in piece.paths[0]
               or "-red" in piece.paths[0]]
    text_feeders = [piece for piece in captured.pieces
                    if piece.text is not None
                    and piece.record_class == CLS_AUDIT_PAPER
                    and ("round" in piece.paths[0]
                         or "-red" in piece.paths[0])]
    if damaged and not text_feeders:
        piece = damaged[0]
        token = _quality_code(piece)
        if token == "truncated-no-correcting-record":
            return _refusal(
                "Q-1", "present but not derivable",
                "no audit round figure", denom, pointer,
                shows="the audit paper %s is truncated and no "
                      "correcting record stands for it, so its "
                      "visible part counts toward nothing and the "
                      "round it feeds is incomplete"
                      % piece.paths[0],
                token=token,
                follows="the contribution is present but not "
                        "derivable with the truncation as the "
                        "reason, and the round is marked incomplete",
                rule_name="D-19 truncated paper rule")
        return _refusal(
            "Q-1", "present but not derivable", "no audit round figure",
            denom, pointer,
            shows="the audit paper %s stands %s in the capture and "
                  "supplies no breakdown"
                  % (piece.paths[0],
                     piece.quality_state or "not read in full"),
            token=token,
            follows="the feeder piece is not read in full, so no "
                    "figure stands for the round it feeds",
            rule_name="Q-1 damaged feeder rule")
    feeder_incomplete = [path for path in incomplete
                         if "round" in path or "-red" in path]
    if feeder_incomplete and not counted:
        return _refusal(
            "Q-1", "present but not derivable", "no audit round figure",
            denom, pointer,
            shows="the audit paper %s fails a completeness signal "
                  "or states it carries no closing total, and its "
                  "visible part counts toward nothing"
                  % feeder_incomplete[0],
            token="truncated-no-correcting-record",
            follows="the contribution is present but not derivable "
                    "with the incompleteness as the reason, and the "
                    "round is marked incomplete",
            rule_name="D-19 signal failed paper rule")
    held_clauses = []
    audit_section = _metrics_section(
        captured.assembled_metrics or "", "## Audit round table")
    if audit_section and ("no rows" in audit_section.lower() or
                          "(no rows yet)" in audit_section.lower()):
        held_clauses.append("the audit round table holds no rows")
    held_clauses.append("severity evidence stands scattered in "
                        "unlike forms")
    fix_step = None
    for piece in captured.pieces_of(CLS_FIX_REGISTER):
        if piece.text is None:
            continue
        if "dispositions" in piece.text.lower() and \
                "severity" not in piece.text.lower():
            if piece.paths[0].startswith("audit/"):
                fix_step = piece.step
                break
            if fix_step is None:
                fix_step = piece.step
    if fix_step is not None:
        held_clauses.append(
            "the Step %d fix register states dispositions with no "
            "severity breakdown" % fix_step)
    adj_step = None
    for piece in captured.pieces_of(CLS_GATE_ADJUDICATION):
        if piece.text is None:
            continue
        if "commissioned" in piece.text.lower() and \
                "critical" in piece.text.lower():
            adj_step = piece.step
            break
    if adj_step is not None:
        held_clauses.append(
            "the Step %d gate adjudication breakdown stands under "
            "a commissioned scale of its own" % adj_step)
    return _refusal(
        "Q-1", "present but not derivable", "no audit round figure",
        denom, pointer,
        shows="audit records stand and none carries a post triage "
              "severity breakdown",
        token="no-post-triage-breakdown",
        follows="the breakdown the row counts from does not stand, "
                "so no figure stands",
        rule_name="Q-1 post triage breakdown rule",
        broken="the post triage severity breakdown field under "
               "the flow scale",
        required="a post triage breakdown under the flow scale in "
                 "the round own record or in a record the round "
                 "record names",
        held=_held_join(held_clauses))


def _q1_present_result(captured, counted, excluded, denom, pointer):
    """The bounded Q-1 row: qualifying round counts only.

    The population and the exclusion list stand before the counts,
    round by round, with the scale and record form pair per
    counted round, the pair travelling together, and no count
    printed for any other round.
    """
    rounds_seen = sorted({candidate["round"] for candidate in counted}
                         | {rnd for rnd, _why in excluded})
    population = ("population, the rounds with records standing: "
                  + (", ".join("Round %d" % rnd
                               for rnd in rounds_seen) or "none"))
    exclusion = ("excluded: "
                 + ("; ".join("Round %d, %s" % (rnd, why)
                              for rnd, why in excluded)
                    if excluded else "none"))
    parts = []
    for candidate in sorted(counted, key=lambda c: c["round"]):
        parts.append(
            "Round %d: %s, scale %s, record form %s"
            % (candidate["round"],
               _q1_counts_text(candidate["counts"]),
               candidate.get("scale") or "flow scale",
               candidate["form"]))
    figures = ("bounded form: " + population + "; " + exclusion
               + "; qualifying round counts: " + "; ".join(parts))
    for candidate in counted:
        if candidate.get("repaired"):
            figures += ("; the piece %s stands repaired, its "
                        "quality state the single state truncated "
                        "with the repair cited beside it"
                        % candidate["path"])
    result = DerivationResult(
        "Q-1", "present", figures, denom, pointer,
        rule_name="Q-1 bounded breakdown rule")
    result.statement = _q1_statement(captured, counted)
    return result


# ------------------------------------------------------------- Q-3

def _q3_registers(captured):
    registers = []
    for piece in captured.pieces:
        path = piece.paths[0]
        name = path.rsplit("/", 1)[-1]
        if piece.record_class in (CLS_DEFECT_REGISTER, CLS_FIX_REGISTER) \
                or name in ("defect-register.md", "fix-register.md"):
            label = "defect register" if "defect" in name \
                else "fix register"
            registers.append((piece, label))
    return registers


def _q3_entries(captured):
    """Register entries with the origin step field read on the entry.

    An origin step counts only where the field stands on the
    register entry itself and states the step the defect was
    introduced in or escaped from as judged at triage. An entry
    whose origin is copied, or stands as a neighbouring, finding
    or closing step, does not count.
    """
    entries = []
    for piece, label in _q3_registers(captured):
        if piece.text is None:
            continue
        segments = re.split(r"(?=Entry [A-Za-z0-9])", piece.text)
        for segment in segments:
            head = re.match(r"Entry ([A-Za-z0-9][\w-]*)", segment)
            if not head:
                continue
            origin = None
            found = re.search(r"[Oo]rigin step[:\s]+Step (\d+)",
                              segment)
            if found:
                origin = int(found.group(1))
            copied = "copied" in segment.lower() or \
                "no triage judgement" in segment.lower()
            entries.append({"id": head.group(1), "register": label,
                            "path": piece.paths[0],
                            "origin": origin, "copied": copied})
        for line in piece.text.splitlines():
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue
            cells = [cell.strip() for cell in
                     stripped.strip("|").split("|")]
            if len(cells) < 2 or not cells[0]:
                continue
            if cells[0].lower() in ("id", "block", "entry"):
                continue
            if set(cells[0]) <= set("-* "):
                continue
            origin = None
            found = re.search(r"[Oo]rigin step[:\s]+Step (\d+)",
                              stripped)
            if found:
                origin = int(found.group(1))
            entries.append({"id": cells[0], "register": label,
                            "path": piece.paths[0],
                            "origin": origin,
                            "copied": "copied" in stripped.lower()})
    return entries


def _q3_contested_steps(universe):
    """Steps past the metrics record stated universe count."""
    claim = universe.metrics_count_claim
    evidenced = sorted(universe.evidenced)
    if claim is None or not 0 < claim < len(evidenced):
        return []
    return evidenced[claim:]


def _q3_contested_entry(captured, universe):
    """A register entry whose origin step stands contested.

    Stands where a register entry origin step is one of the steps
    the step universe claim disagrees over, judged by the capture
    alone.
    """
    contested = _q3_contested_steps(universe)
    if not contested:
        return None
    for entry in _q3_entries(captured):
        if entry["origin"] in contested:
            return entry
    return None


def _q3_restatement(captured):
    """A correction piece restating the step universe statement."""
    for piece in captured.pieces:
        if piece.text is None:
            continue
        if "correct" in piece.paths[0] and \
                "restated" in piece.text.lower() and \
                "step universe" in piece.text.lower():
            return piece
    return None


def _derive_q3(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    registers = _q3_registers(captured)
    pointer = registers[0][0].paths[0] if registers else \
        "registers/defect-register.md"
    pointer = _pointer("Q-3", pointer, captured)
    assembled = captured.assembled_metrics or ""
    if not _known_version(captured.definitions_version) and registers:
        return _unknown_version_result(captured, "Q-3", denom, pointer)
    if not registers:
        if re.search(r"Escapes attributed \(Q-3\):\s*0\b", assembled):
            return _refusal(
                "Q-3", "present but not derivable",
                "printed zero, not a measured figure", denom, pointer,
                shows="the assembled metrics record prints an "
                      "escape count of zero and no register stands "
                      "in the capture to measure it",
                token="no-measurement-basis",
                follows="the printed zero is never stated as a "
                        "measured figure, because no measurement "
                        "basis stands for it",
                rule_name="Q-3 printed zero rule")
        return _refusal(
            "Q-3", "missing", "no escape figure", denom, pointer,
            shows="no defect register and no fix register stands "
                  "in the capture for this metric",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="Q-3 feeder standing rule")
    entries = _q3_entries(captured)
    valid = [entry for entry in entries
             if entry["origin"] is not None and not entry["copied"]]
    if valid:
        counts = {}
        for entry in valid:
            counts[entry["origin"]] = counts.get(entry["origin"], 0) + 1
        figures = "; ".join(
            "Step %d: %d escapes" % (step, counts[step])
            for step in sorted(counts))
        basis = None
        for piece, _label in registers:
            if piece.text:
                found = re.search(r"Measurement basis:\s*([^\n]+)",
                                  piece.text)
                if found:
                    basis = found.group(1).strip()
                    break
        if basis:
            figures += "; measurement basis: " + basis
        lacking = [entry for entry in entries
                   if entry["origin"] is None or entry["copied"]]
        coverage = denom
        bound = None
        if lacking:
            coverage += ("; counts form from the carrying entries "
                         "alone; lacking entries: "
                         + "; ".join(
                             "%s entry %s"
                             % (entry["register"], entry["id"])
                             for entry in lacking)
                         + "; count of lacking entries: %d"
                         % len(lacking))
            excepted = "; ".join(
                "%s entry %s" % (entry["register"], entry["id"])
                for entry in lacking)
            bound = (excepted,
                     "the origin step field on " + excepted,
                     "; ".join(
                         "%s entry %s stating the origin step "
                         "field on the entry itself, judged at "
                         "triage, stating the step the defect was "
                         "introduced in or escaped from"
                         % (entry["register"], entry["id"])
                         for entry in lacking))
        result = DerivationResult(
            "Q-3", "present", figures, coverage, pointer,
            rule_name="Q-3 origin step rule", bound=bound)
        result.coverage = coverage
        statement = None
        error = None
        try:
            from metrics_starter_collector.cross_check import \
                q3_contested_statement
            statement = q3_contested_statement(
                captured, universe,
                {entry["origin"] for entry in valid})
        except Exception as exc:
            error = _error_form("q3_contested_statement",
                                _metrics_record_name(captured), exc)
            statement = None
        if statement is None:
            contested = _q3_contested_steps(universe)
            hit = [entry for entry in valid
                   if entry["origin"] in contested]
            if hit:
                statement = _universe_claim_statement(
                    captured, universe)
        result.statement = _join_statements(error, statement)
        return result
    if entries and all(entry["copied"] for entry in entries):
        return _refusal(
            "Q-3", "present but not derivable", "no escape figure",
            denom, pointer,
            shows="register entries stand and every origin step on "
                  "them is a copied step, standing as a neighbouring "
                  "or closing step with no triage judgement, so no "
                  "origin stands on any entry itself",
            token="missing-field",
            follows="a copied, neighbouring, finding or closing "
                    "step does not count, so no escape figure stands",
            rule_name="Q-3 origin step rule",
            broken="the origin step field on the register entries",
            required="the origin step field standing on the "
                     "register entry itself, stating the step the "
                     "defect was introduced in or escaped from as "
                     "judged at triage",
            held="every entry carries a copied origin step and no "
                 "entry carries the field judged at triage")
    if entries:
        table = _metrics_step_table(captured)
        printed_zero = "printed zero" in assembled.lower() or any(
            len(cells) >= 13 and cells[12].startswith("0")
            for cells in table.values())
        held = ("the field is absent from every fix and defect "
                "register entry")
        if printed_zero:
            held += (", and the printed zero in the metrics record "
                     "step table carries no measurement basis and "
                     "stands nowhere as a measured figure")
        return _refusal(
            "Q-3", "present but not derivable", "no register figure",
            denom, pointer,
            shows="register entries stand and the entries carry no "
                  "origin step field",
            token="missing-field",
            follows="the origin step field the row requires does "
                    "not stand on the entries, so no figure stands",
            rule_name="Q-3 origin step field rule",
            broken="the origin step field on fix and defect "
                   "register entries",
            required="an origin step field on each register entry, "
                     "judged at triage, stating the step the defect "
                     "was introduced in or escaped from",
            held=held)
    # Registers stand and hold no entries.
    for piece, _label in registers:
        if piece.text and re.search(
                r"(?:Escapes attributed|Escaped defects)"
                r"[^.\n]*\b0\b", piece.text):
            correction = None
            for other in captured.pieces:
                if other.text is None:
                    continue
                if "correct" in other.paths[0] and \
                        "measurement basis" in other.text.lower():
                    correction = other
                    break
            if correction is not None:
                figures = ("measured zero escapes; measurement "
                           "basis supplied by the correcting record "
                           + correction.paths[0])
                return DerivationResult(
                    "Q-3", "present", figures, denom, pointer,
                    rule_name="Q-3 corrected zero rule")
            return _refusal(
                "Q-3", "present but not derivable",
                "printed zero, not a measured figure", denom, pointer,
                shows="the register prints an escape count of zero "
                      "and states no measurement basis for it",
                token="no-measurement-basis",
                follows="the printed zero is never stated as a "
                        "measured figure, and the reason line "
                        "carries the warning that the printed column "
                        "is not a measurement and must not be read "
                        "as one",
                rule_name="Q-3 printed zero rule")
    if len(registers) >= 2:
        figures = ("measured zero escapes; basis: both registers "
                   "stand and hold no entries; CA2-10 exposure: "
                   "the row reads the registers named in the "
                   "capture only, and defects recorded outside "
                   "those registers are not counted")
        return DerivationResult(
            "Q-3", "present", figures, denom, pointer,
            rule_name="Q-3 empty register rule")
    return _refusal(
        "Q-3", "present but not derivable", "no escape figure",
        denom, pointer,
        shows="a register stands and holds no entries, and no "
              "measurement basis stands for a zero",
        token="no-measurement-basis",
        follows="no entry stands to count and no measured zero "
                "stands, so no figure stands",
        rule_name="Q-3 empty register rule")


# ----------------------------------------------------------------- Q-4

def _parse_trace_segment(segment):
    landed = _search_int(r"(\d+)\s+LANDED", segment)
    if landed is None:
        return None
    partial = _search_int(r"(\d+)\s+PARTIAL", segment)
    contradicted = _search_int(r"(\d+)\s+CONTRADICTED", segment)
    partial = 0 if partial is None else partial
    contradicted = 0 if contradicted is None else contradicted
    total = None
    for pattern in (r"of\s+(\d+)\s+items checked",
                    r"stated total of\s+(\d+)",
                    r"Stated total:\s*(\d+)",
                    r"total of\s+(\d+)\s+items checked"):
        total = _search_int(pattern, segment)
        if total is not None:
            break
    if total is None:
        total = landed + partial + contradicted
    return (landed, partial, contradicted, total)


_TRACE_RANK = {CLS_TRACE: 0, CLS_STEP_COMPANION: 0, CLS_GATE_RECORD: 1,
               CLS_GATE_RULING: 2, CLS_AUDIT_PAPER: 3}


def _trace_candidates(captured):
    """First trace candidates by step, in the ranked form order.

    DG-05 form precedence: a standalone trace record first, then a
    trace section inside a gate record, then a trace summary inside
    a gate ruling, then a Purple trace paper. A candidate carries
    its figures and the share form its own statement uses: the of
    form where the statement states landed of a total, and the
    items checked form where it states landed of items checked.
    """
    candidates = {}
    all_candidates = {}

    def add(step, parsed, style, piece, rank):
        if step is None or parsed is None:
            return
        key = (rank, 1 if "round" in piece.paths[0] else 0,
               piece.paths[0])
        all_candidates.setdefault(step, []).append(
            (key, parsed, style, piece))
        current = candidates.get(step)
        if current is None or key < current[0]:
            candidates[step] = (key, parsed, style, piece)

    for piece in captured.pieces:
        if piece.text is None:
            continue
        rank = _TRACE_RANK.get(piece.record_class)
        if rank is None:
            continue
        if piece.record_class == CLS_AUDIT_PAPER and \
                "purple" not in piece.paths[0].lower() and \
                "round-record" not in piece.paths[0].lower():
            continue
        lines = piece.text.splitlines()
        title_first = bool(lines) and "first trace" in lines[0].lower()
        for line in lines:
            if "first trace" in line.lower():
                parsed = _parse_trace_segment(line)
                step = _search_int(r"[Ss]tep (\d+)\b", line)
                add(step if step is not None else piece.step,
                    parsed, "items", piece, rank)
            m = re.search(
                r"(\d+) of (\d+) [^\n]{0,40}LANDED, (\d+) PARTIAL, "
                r"(\d+) CONTRADICTED", line)
            if m and piece.record_class in (CLS_GATE_RECORD,
                                            CLS_GATE_RULING):
                add(piece.step, (int(m.group(1)), int(m.group(3)),
                                 int(m.group(4)), int(m.group(2))),
                    "of", piece, rank)
            m = re.search(
                r"(\d+) elements, (\d+) LANDED, (\d+) PARTIAL", line)
            if m and piece.record_class == CLS_GATE_RECORD:
                add(piece.step, (int(m.group(2)), int(m.group(3)), 0,
                                 int(m.group(1))), "of", piece, rank)
            m = re.search(
                r"Counts: (\d+) items checked\. LANDED (\d+), "
                r"PARTIAL (\d+), CONTRADICTED (\d+)", line)
            if m and piece.record_class == CLS_AUDIT_PAPER:
                add(piece.step, (int(m.group(2)), int(m.group(3)),
                                 int(m.group(4)), int(m.group(1))),
                    "items", piece, rank)
            m = re.search(
                r"full trace (\d+) of (\d+) LANDED, PARTIAL (\d+), "
                r"CONTRADICTED (\d+)", line)
            if m and piece.record_class == CLS_GATE_RULING:
                add(piece.step, (int(m.group(1)), int(m.group(3)),
                                 int(m.group(4)), int(m.group(2))),
                    "of", piece, rank)
            if title_first and "landed" in line.lower():
                parsed = _parse_trace_segment(line)
                add(piece.step, parsed, "items", piece, rank)
            if piece.record_class == CLS_TRACE and \
                    "parts:" in line.lower() and \
                    "landed" in line.lower():
                # A standalone trace record states its first
                # trace parts on its Parts line, whatever its
                # title calls the trace.
                parsed = _parse_trace_segment(line)
                add(piece.step, parsed, "items", piece, rank)
        if piece.record_class == CLS_TRACE:
            total = None
            parts = {}
            in_counts = False
            for line in lines:
                if "verdict counts" in line.lower():
                    in_counts = True
                m = re.search(r"rows traced:\s*(\d+)", line, re.I)
                if m:
                    total = int(m.group(1))
                if in_counts:
                    m = re.match(
                        r"-\s*(LANDED|PARTIAL|CONTRADICTED):\s*(\d+)",
                        line.strip())
                    if m:
                        parts[m.group(1)] = int(m.group(2))
            if total is not None and "LANDED" in parts:
                add(piece.step,
                    (parts["LANDED"], parts.get("PARTIAL", 0),
                     parts.get("CONTRADICTED", 0), total),
                    "items", piece, rank)
    # A correcting record identifying the first trace record for
    # a step identifies that record for the step, under the first
    # trace rule: the identified candidate stands over the ranked
    # forms.
    for piece in captured.pieces:
        if piece.text is None:
            continue
        for found in re.finditer(
                r"The first trace record for Step (\d+) is "
                r"(\S+?\.md)", piece.text):
            step = int(found.group(1))
            target = found.group(2)
            for key, parsed, style, cand_piece in \
                    all_candidates.get(step, []):
                if cand_piece.paths[0] == target:
                    candidates[step] = (key, parsed, style,
                                        cand_piece)
    return candidates


def _trace_correction(captured, step, parsed):
    """Apply a correcting record count to one trace contribution.

    A correction stands where a gate record for the step, or the
    metrics record step table cell for the step, states the trace
    parts on a corrected count against the trace paper own count.
    """
    landed, partial, contradicted, total = parsed
    patterns = (
        r"standing at (\d+) PARTIAL and (\d+) CONTRADICTED on the "
        r"corrected table count",
        r"counting the table rows directly gives (\d+) PARTIAL "
        r"rows and (\d+) CONTRADICTED",
        r"\((\d+) PARTIAL and (\d+) CONTRADICTED, on the "
        r"corrected count",
        r"(\d+) PARTIAL and (\d+) CONTRADICTED, on the corrected "
        r"table count",
    )
    texts = []
    for piece in captured.step_pieces(step, CLS_GATE_RECORD):
        if piece.text:
            texts.append(piece.text)
    cells = _metrics_step_table(captured).get(step)
    if cells and len(cells) >= 12:
        texts.append(cells[11])
    for text in texts:
        for pattern in patterns:
            m = re.search(pattern, text)
            if m:
                return (landed, int(m.group(1)), int(m.group(2)),
                        total)
    return parsed


def _first_traces(captured):
    """First trace contributions by step, from the one capture."""
    found = {}
    sources = {}
    styles = {}
    for step, (_key, parsed, style, piece) in \
            _trace_candidates(captured).items():
        parsed = _trace_correction(captured, step, parsed)
        found[step] = parsed
        sources[step] = piece.paths[0]
        styles[step] = style
    return found, sources, styles


def _q4_named_set(captured):
    """Whether a first trace stands in a named evidence form.

    The named forms are the gate record tally, the gate ruling
    trace summary and the Purple paper counts, beside the trace
    record verdict counts: a trace found only in the explicit
    first trace line form does not name the set.
    """
    for piece in captured.pieces:
        if piece.text is None:
            continue
        if piece.record_class == CLS_GATE_RECORD and re.search(
                r"\d+ of \d+ [^\n]{0,40}LANDED, \d+ PARTIAL",
                piece.text):
            return True
        if piece.record_class == CLS_GATE_RULING and \
                "full trace" in piece.text:
            return True
        if piece.record_class == CLS_AUDIT_PAPER and \
                "purple" in piece.paths[0].lower() and \
                "Counts:" in piece.text:
            return True
        if piece.record_class == CLS_TRACE and \
                "rows traced:" in piece.text:
            return True
    return False


def _derive_q4(captured, universe):
    denom = "denominator steps with a first trace in the step universe"
    traces, sources, styles = _first_traces(captured)
    pointer = None
    if sources:
        pointer = sources[sorted(sources)[0]]
    if pointer is None:
        gates = captured.pieces_of(*GATE_CLASSES)
        pointer = gates[0].paths[0] if gates else \
            "steps/step-01-gate-record.md"
    if not _known_version(captured.definitions_version) and traces:
        return _unknown_version_result(
            captured, "Q-4", denom, _pointer("Q-4", pointer, captured))
    if not traces:
        trace_pieces = [piece for piece in captured.pieces
                        if "trace" in piece.paths[0]
                        and piece.paths[0].endswith(".md")]
        if trace_pieces:
            return _refusal(
                "Q-4", "present but not derivable",
                "no first trace figure", denom,
                _pointer("Q-4", trace_pieces[0].paths[0], captured),
                shows="a trace record stands in the capture and no "
                      "totals stand on it in a form the row can "
                      "count",
                token="missing-field",
                follows="no first trace figure stands on the "
                        "feeder record, so no figure stands",
                rule_name="Q-4 first trace figure rule")
        return _refusal(
            "Q-4", "missing", "no first trace figure", denom,
            _pointer("Q-4", pointer, captured),
            shows="no first trace record stands in the tree for "
                  "this metric",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="Q-4 feeder standing rule")
    reconciled = {}
    excepted = {}
    for step, (landed, partial, contradicted, total) in traces.items():
        if landed + partial + contradicted == total:
            reconciled[step] = (landed, partial, contradicted, total)
        else:
            excepted[step] = (landed, partial, contradicted, total)
    if not reconciled:
        named = _each_step(sorted(excepted))
        return _refusal(
            "Q-4", "present but not derivable",
            "no reconciled first trace figure", denom,
            _pointer("Q-4", pointer, captured),
            shows="every first trace contribution stands excepted "
                  "under the sum test, for %s, where the parts by "
                  "class do not sum to the stated total" % named,
            token="unreconciled-figure",
            follows="no contribution survives the sum test, so no "
                    "build level figure stands",
            rule_name="Q-4 sum test rule")
    parts = []
    sum_landed = 0
    sum_partial = 0
    sum_contra = 0
    sum_total = 0
    for step in sorted(reconciled):
        landed, partial, contradicted, total = reconciled[step]
        if styles.get(step) == "of":
            parts.append("Step %d, %d of %d LANDED"
                         % (step, landed, total))
        else:
            parts.append("Step %d, %d LANDED of %d items checked"
                         % (step, landed, total))
        sum_landed += landed
        sum_partial += partial
        sum_contra += contradicted
        sum_total += total
    figures = ("first trace LANDED shares for the named evidence "
               "steps: " + "; ".join(parts))
    figures += ("; totals %d LANDED, %d PARTIAL, %d CONTRADICTED, "
                "%d items checked"
                % (sum_landed, sum_partial, sum_contra, sum_total))
    coverage = ("steps with a first trace in the named evidence "
                "set, " + _steps_phrase(sorted(reconciled)))
    bound = None
    if excepted:
        coverage += ", with " + _steps_phrase(sorted(excepted)) + \
            " excepted"
        coverage += ("; excepted contributions: %d" % len(excepted))
        if len(excepted) == 1:
            step = sorted(excepted)[0]
            landed, partial, contradicted, total = excepted[step]
            unit = "pin rows" if "pin" in (
                _metrics_step_table(captured).get(step, [""] * 12)[11]
                if len(_metrics_step_table(captured).get(
                    step, [])) >= 12 else "") or _trace_is_pin_rows(
                        captured, step) else "items checked"
            bound = (
                "the Step %d contribution" % step,
                "the sum test link for Step %d, whose trace parts "
                "of %d LANDED, %d PARTIAL and %d CONTRADICTED sum "
                "to %d against the stated total of %d %s"
                % (step, landed, partial, contradicted,
                   landed + partial + contradicted, total, unit),
                "a correcting record stating the Step %d trace "
                "parts and its total in reconciled form" % step)
        else:
            bound = (
                "the excepted contributions",
                "the sum test links for the excepted steps",
                "a correcting record stating the excepted trace "
                "parts and totals in reconciled form")
    # The coverage remainder forms: an analogue only step, a zero
    # total step, and a step stating no trace applies, named on
    # the row as the charge states them.
    for piece in captured.pieces_of(CLS_STEP_RECORD):
        if piece.text is None or piece.step is None:
            continue
        if "analogue only" in piece.text.lower():
            coverage += "; Step %d analogue only step" % piece.step
        if "no trace applies" in piece.text.lower():
            coverage += ("; Step %d not applicable, excluded from "
                         "the Q-4 population" % piece.step)
    for step in sorted(reconciled):
        if reconciled[step][3] == 0:
            coverage += "; Step %d zero total step" % step
    result = DerivationResult(
        "Q-4", "present", figures, coverage,
        _pointer("Q-4", pointer, captured),
        rule_name="Q-4 first trace rule")
    result.coverage = coverage
    result.bound = bound
    statement = None
    error = None
    try:
        from metrics_starter_collector.cross_check import \
            q4_cross_check_statement
        covered = {step: (traces[step][0], traces[step][3])
                   for step in reconciled}
        statement = q4_cross_check_statement(captured, covered)
    except Exception as exc:
        error = _error_form("q4_cross_check_statement",
                            _metrics_record_name(captured), exc)
        statement = None
    if statement is None:
        statement = _q4_record_marking(captured, traces, sources,
                                       set(reconciled))
    result.statement = _join_statements(error, statement)
    return result


def _q4_stated_figures(captured, traces, sources):
    """Differing first trace figures stated outside the feeder.

    Yields (step, other_path, landed, total) for each step where
    the assembled metrics record, or a record stating a first
    trace figure for the step, disagrees with the feeder figure.
    An excepted step is never yielded on the sum test ground: its
    figures are the feeder figures themselves.
    """
    found_list = []
    metrics_text = captured.assembled_metrics or ""
    for step in sorted(traces):
        landed, _partial, _contra, total = traces[step]
        record = re.search(
            r"Q-4 for Step %d as (\d+) of (\d+)" % step, metrics_text)
        if record and (int(record.group(1)), int(record.group(2))) \
                != (landed, total):
            found_list.append((step, _metrics_record_name(captured),
                               int(record.group(1)),
                               int(record.group(2))))
            continue
        for piece in captured.pieces:
            if piece.text is None:
                continue
            path = piece.paths[0]
            if path == sources.get(step):
                continue
            stated = re.search(
                r"the first trace for Step %d as "
                r"(\d+) LANDED of (\d+)" % step, piece.text)
            if stated and (int(stated.group(1)),
                           int(stated.group(2))) != (landed, total):
                found_list.append((step, path, int(stated.group(1)),
                                   int(stated.group(2))))
                break
            if "the same records state" in piece.text \
                    and _piece_step(piece) == step:
                stated = re.search(
                    r"first trace (\d+) LANDED of (\d+)", piece.text)
                if stated and (int(stated.group(1)),
                               int(stated.group(2))) != (landed,
                                                          total):
                    found_list.append(
                        (step, path, int(stated.group(1)),
                         int(stated.group(2))))
                    break
    return found_list


def _q4_record_marking(captured, traces, sources, reconciled_steps):
    """The record disagrees marking for the Q-4 statement line.

    The feeder figure stands and the record figure is not
    followed. Only reconciled steps are marked: an excepted step
    carries its exception on the row, not a disagreement.
    """
    for step, path, landed, total in _q4_stated_figures(
            captured, traces, sources):
        if step not in reconciled_steps:
            continue
        feeder_landed, _p, _c, feeder_total = traces[step]
        return ("record disagrees: %s states Q-4 for Step %d as "
                "%d of %d, while the first trace record states %d "
                "of %d; the feeder figure stands and the record "
                "figure is not followed"
                % (path, step, landed, total, feeder_landed,
                   feeder_total))
    return None


def _q4_disagreement_entries(captured):
    """One disagreements block entry per disagreed Q-4 unit."""
    traces, sources, _styles = _first_traces(captured)
    entries = []
    for step, path, landed, total in _q4_stated_figures(
            captured, traces, sources):
        feeder_landed, _p, _c, feeder_total = traces[step]
        entries.append(
            "Records: %s and %s | Figures: the record states the "
            "first trace for Step %d as %d LANDED of %d, the first "
            "trace record states %d of %d | Metric: Q-4 | "
            "Governing position: governed with the pattern named"
            % (path, sources[step], step, landed, total,
               feeder_landed, feeder_total))
    return entries


def _slice5_disagreement_entries(captured):
    """Disagreements block entries for the Slice 5 metrics.

    One entry per metric for Q-1, in the same records form: a
    record stating a different post triage breakdown for a
    counted round. One entry per unit for Q-4, from the stated
    figure scan the Q-4 marking uses. Returns the restatement
    group entries and the blocking group entries in two lists:
    the Q-3 contested entry stands in the restatement group
    where a restatement stands in the records, and in the
    blocking group where none stands.
    """
    restatements = []
    entries = []
    counted, _nonflow, _excluded, _incomplete = \
        _q1_direct_candidates(captured)
    carrier, _unnamed = _q1_carrier_candidates(captured)
    merged = {candidate["round"]: candidate for candidate in counted}
    for candidate in carrier:
        if candidate["scale"] == "flow scale" and \
                candidate["counts"] and candidate["triage"]:
            merged.setdefault(candidate["round"], candidate)
    counted = [merged[rnd] for rnd in sorted(merged)]
    by_path = {piece.paths[0]: piece for piece in captured.pieces}
    for rnd, feeder_path, feeder_counts, other_path, other_counts \
            in _q1_disagreements(captured, counted):
        other = by_path.get(other_path)
        if other is None or other.text is None or \
                "the same records state" not in other.text:
            continue
        entries.append(
            "Records: %s and %s | Figures: the feeder record "
            "states post triage breakdown %s for Round %d, the "
            "other record states %s for Round %d | Metric: Q-1 | "
            "Governing position: governed with the pattern named"
            % (feeder_path, other_path,
               _q1_counts_text(feeder_counts), rnd,
               _q1_counts_text(other_counts), rnd))
    entries += _q4_disagreement_entries(captured)
    universe = build_step_universe(captured)
    contested = _q3_contested_entry(captured, universe)
    if contested is not None:
        figures = (
            "the metrics record states the step universe as %s "
            "step, the register entry states origin step Step %d; "
            "the contested instance carried on the evidenced "
            "universe"
            % (universe.metrics_count_claim, contested["origin"]))
        if _q3_restatement(captured) is not None:
            restatements.append(
                "Records: %s and %s | Figures: %s | Metric: Q-3 | "
                "Governing position: restatement with its "
                "correction named"
                % (_metrics_record_name(captured),
                   contested["path"], figures))
        else:
            entries.append(
                "Records: %s and %s | Figures: %s | Metric: Q-3 | "
                "Governing position: governed with the pattern "
                "named"
                % (_metrics_record_name(captured),
                   contested["path"], figures))
    return restatements, entries


def _trace_is_pin_rows(captured, step):
    for piece in captured.step_pieces(step, CLS_TRACE):
        if piece.text and "Pin rows traced" in piece.text:
            return True
    return False


# ----------------------------------------------------------------- D-1

def _table_items(text):
    """Decision table items from one record text, in row order."""
    items = []
    if not text:
        return items
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 5:
            continue
        if cells[0] in ("Item", "---") or set(cells[0]) <= set("- "):
            continue
        items.append({
            "item": cells[0],
            "origin": cells[1],
            "raised": cells[2],
            "presented": cells[3],
            "ruled": cells[4],
            "raised_dt": _stamp_value(cells[2]),
            "ruled_dt": _stamp_value(cells[4]),
        })
    return items


_D1_FOUNDATION_QUEUE = (
    "Foundation statement: the feeder this row rests on is "
    "DECISION-QUEUE.md, the queue file inside the root, governing "
    "over the metrics record decision table under WV-12, with the "
    "decision table standing as the cross check where one stands")

_D1_FOUNDATION_TABLE = (
    "Foundation statement: the feeder this row rests on is the "
    "decision table inside the root, governing under the D-09 "
    "exception where no queue file in the named form stands, and "
    "no queue file in the named form stands in the tree")

_D1_FOUNDATION_TABLE_NO_QUEUE = (
    "Foundation statement: the decision table inside the root "
    "is the feeder this row rests on, under the exception for "
    "a tree with no queue file, and no queue file stands in "
    "the tree")

_D1_FOUNDATION_NONE = (
    "Foundation statement: no feeder stands for this row, no "
    "queue file in the named form stands and no decision table "
    "stands in the capture")

_D1_FOUNDATION_UNUSABLE = (
    "Foundation statement: DECISION-QUEUE.md is the feeder record "
    "that stood and supplied no row, and no complete decision "
    "table stands in the capture")


def _d1_marking(captured, feeder_items, table_items):
    """The D-1 cross check marking, consumed through Module 4.

    The one feeder exception for D-1 lives in this derivation and
    in the Module 4 role swap, and in no other derivation: where
    the queue file governs, the decision table is the cross check,
    and a disagreement between them stands in the statement line
    of the D-1 row under D-18 and CA-1, with the queue figure
    standing. Where the table itself governs, no marking stands.
    """
    error = None
    try:
        from metrics_starter_collector.cross_check import \
            d1_cross_check_statement
        marking = d1_cross_check_statement(
            feeder_items, table_items,
            metrics_name=_metrics_record_name(captured))
        if marking:
            return marking
    except Exception as exc:
        error = _error_form("d1_cross_check_statement",
                            _metrics_record_name(captured), exc)
    feeder = {item["item"]: item["ruled"] for item in feeder_items}
    table = {item["item"]: item["ruled"] for item in table_items}
    if not feeder or not table or feeder == table:
        return error
    for name in table:
        if name in feeder and feeder[name] and table[name] and \
                feeder[name] != table[name]:
            return _join_statements(
                error,
                "record disagrees: the decision table in %s "
                "states %s ruled at %s, while the governing "
                "feeder states %s ruled at %s; the feeder "
                "figure stands and the record figure is not "
                "followed"
                % (_metrics_record_name(captured), name,
                   table[name], name, feeder[name]))
    return error


def _d1_statement(foundation, marking):
    parts = [part for part in (foundation, marking) if part]
    return "; ".join(parts) if parts else None


def _derive_d1(captured, universe):
    denom = "denominator decision items in the governing record"
    feeders = _decision_feeders(captured)
    queue_piece = feeders["queue_piece"]
    if feeders["queue_usable"]:
        items = feeders["queue_items"]
        feeder_name = "decision queue file"
        pointer = queue_piece.paths[0]
        foundation = _D1_FOUNDATION_QUEUE
        marking = None
        if feeders["table_items"]:
            marking = _d1_marking(captured, items,
                                  feeders["table_items"])
        if not items:
            return _refusal(
                "D-1", "present but not derivable",
                "no decision latency figure", denom,
                _pointer("D-1", pointer, captured),
                shows="the queue file in the named form stands in "
                      "the capture and holds no item from which a "
                      "latency can be formed",
                token="missing-field",
                follows="the governing record holds no item, so "
                        "no median figure stands",
                rule_name="D-1 latency field rule",
                statement=_d1_statement(foundation, marking))
    elif feeders["table_stands"]:
        items = feeders["table_items"]
        feeder_name = "metrics record decision table"
        pointer = METRICS_CANONICAL_PATH
        foundation = _D1_FOUNDATION_TABLE_NO_QUEUE \
            if queue_piece is None else _D1_FOUNDATION_TABLE
        marking = None
        if not items:
            return _refusal(
                "D-1", "present but not derivable",
                "no decision latency figure", denom,
                _pointer("D-1", pointer, captured),
                shows="the decision table stands inside the root "
                      "and holds no item from which a latency can "
                      "be formed",
                token="missing-field",
                follows="the feeder stands and holds no item, so "
                        "the row is not derivable and not missing",
                rule_name="D-1 latency field rule",
                statement=_d1_statement(foundation, marking),
                broken="the decision item rows of the decision "
                       "table inside the root",
                required="decision items carrying raised and "
                         "ruled timestamps that can form a "
                         "duration",
                held="the decision table stands and holds no item "
                     "at all")
    elif queue_piece is not None:
        return _refusal(
            "D-1", "present but not derivable",
            "no decision latency figure", denom,
            _pointer("D-1", queue_piece.paths[0], captured),
            shows="a queue file stands in the capture in unusable "
                  "form and was not read in full, and no complete "
                  "decision table stands in the capture",
            token=_quality_code(queue_piece),
            follows="no complete feeder stands, so no median "
                    "figure stands",
            rule_name="D-1 feeder standing rule",
            statement=_D1_FOUNDATION_UNUSABLE,
            broken="the decision item fields in the queue file "
                   "inside the root",
            required="a queue file in the named form or a complete "
                     "decision table, carrying decision items",
            held="the queue file stands in unusable form and no "
                 "complete decision table stands")
    else:
        return _refusal(
            "D-1", "missing", "no decision latency figure", denom,
            _pointer("D-1", METRICS_CANONICAL_PATH, captured),
            shows="no decision table item stands in the governing "
                  "record and no queue file in the named form "
                  "stands in the capture",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="D-1 feeder standing rule",
            statement=_D1_FOUNDATION_NONE)
    counting = []
    not_counted = []
    for item in items:
        value = _item_latency_hours(item)
        if value is not None:
            counting.append((item, value))
        elif not item["ruled"]:
            not_counted.append(
                "%s stands open with no ruled timestamp"
                % item["item"])
        elif _item_span_reversed(item):
            not_counted.append(
                "%s stands ruled before it was raised, so its "
                "span stands reversed under the order check and "
                "forms no latency" % item["item"])
        elif _stamp_value(item["raised"]) == "date" or \
                _stamp_value(item["ruled"]) == "date":
            not_counted.append(
                "%s carries date only timestamps and forms no "
                "duration" % item["item"])
        else:
            not_counted.append(
                "%s forms no raised to ruled duration"
                % item["item"])
    latencies = [value for _item, value in counting]
    if not latencies:
        names = [item["item"] for item in items]
        origins = [item["origin"] for item in items]
        count_word = {1: "one", 2: "two", 3: "three", 4: "four",
                      5: "five"}.get(len(items), str(len(items)))
        held = ("the decision table holds %s items, %s"
                % (count_word, _names_phrase(names)))
        if len(set(origins)) == 1 and origins and origins[0]:
            held += ", each with origin step %s" % origins[0]
        raised_values = {item["raised"] for item in items}
        if len(raised_values) == 1:
            only = next(iter(raised_values))
            if _stamp_value(only) == "date":
                held += (" and raised stated as a date only, %s"
                         % only)
        if all(not item["presented"] and not item["ruled"]
               for item in items):
            held += ", with presented and ruled blank"
        if "not yet countable" in (
                captured.assembled_metrics or "").lower():
            held += " and latency entered as not yet countable"
        if not_counted:
            held += "; " + "; ".join(not_counted)
        return _refusal(
            "D-1", "present but not derivable",
            "no decision latency figure", denom,
            _pointer("D-1", pointer, captured),
            shows="decision table items stand in the %s and no item "
                  "carries both a raised timestamp with a time of "
                  "day and a ruled timestamp with a time of day"
                  % feeder_name,
            token="missing-field",
            follows="the raised and ruled fields the row requires "
                    "do not both stand in full form on any item, so "
                    "no median figure stands",
            rule_name="D-1 latency field rule",
            statement=_d1_statement(foundation, marking),
            broken="the presented and ruled timestamp fields on "
                   "the decision table items",
            required="raised and ruled timestamps that can form a "
                     "duration on an item, with the median and the "
                     "longest formed over the items that produce a "
                     "latency",
            held=held)
    median = _median(latencies)
    counted_names = [item["item"] for item, _value in counting]
    figures = "median %s hours over %d items (%s); longest %s hours" \
        % (_fmt_num(median), len(latencies),
           ", ".join(counted_names), _fmt_num(max(latencies)))
    if not_counted:
        figures += "; items not counted: " + "; ".join(not_counted)
    result = DerivationResult(
        "D-1", "present", figures, denom, pointer,
        statement=_d1_statement(foundation, marking),
        rule_name="D-1 median rule")
    result.numerator = None
    return result


# ------------------------------------------------------------- B family

_BASIS_WORD = re.compile(
    r"\d{2}:\d{2}(?::\d{2})?\s*(UTC|CST|CDT|EST|EDT|GMT)\b")
_STAMP_WITH_WORDS = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}")


def _basis_split(captured):
    """Whether the B family feeder timestamps split on time basis.

    A split stands where one feeder timestamp states a basis word
    and another feeder timestamp in a gate record states no basis,
    in words or by carrying a time of day with no basis word.
    """
    labelled = False
    ledger = _ledger_piece(captured)
    if ledger is not None and ledger.text and \
            _BASIS_WORD.search(ledger.text):
        labelled = True
    if not labelled:
        return False
    for piece in captured.pieces_of(*GATE_CLASSES):
        if piece.text is None:
            continue
        if "no time basis" in piece.text.lower():
            return True
        for hit in _STAMP_WITH_WORDS.finditer(piece.text):
            tail = piece.text[hit.end():hit.end() + 6]
            if not re.match(r"\s*(UTC|CST|CDT|EST|EDT|GMT)\b", tail):
                return True
    return False


def _b_series_figures(captured):
    """Per step elapsed and active figures for the B family.

    Both figures stand for a step only where the step's own
    transitions and its stated active duration stand, the same
    figures the T-1 and T-2 rows are formed from.
    """
    series, _ledger = _time_series(captured)
    elapsed = {}
    active = {}
    for step in sorted(series):
        figures = series[step]
        if figures["elapsed"] is not None:
            elapsed[step] = figures["elapsed"]
        if figures["active"] is not None:
            active[step] = figures["active"]
    both = sorted(set(elapsed) & set(active))
    return elapsed, active, both


def _reversed_step_clauses(captured):
    """Naming clauses for the steps whose span stands reversed.

    A reversed step carries no elapsed and no active figure, so
    it is excluded from every B family figure, including the
    B-1 totals, where a negative step must never cancel a sound
    step. The B rows name the exclusion with the reversed
    condition, in the form the time rows state it.
    """
    series, _ledger = _time_series(captured)
    return ["Step %d excluded: %s"
            % (step, _span_failure_condition(held))
            for step, held in sorted(series.items())
            if held.get("reversed")]


def _b_composition_refusal(code, denom, pointer, captured,
                           t1_result, t2_result, figure_label,
                           rule_name):
    """The composition verdict where the inputs do not both stand.

    Under gap DG-06 the row takes its verdict from its inputs:
    present but not derivable where either input stands present
    but not derivable, or where one input stands and the other is
    missing, with the input that decides the verdict named.
    """
    parts = []
    for name, result in (("T-1", t1_result), ("T-2", t2_result)):
        parts.append("the %s row stands %s" % (name, result.verdict))
    deciding = None
    for name, result in (("T-1", t1_result), ("T-2", t2_result)):
        if result.verdict == "present but not derivable":
            deciding = name
            break
    if deciding is None:
        for name, result in (("T-1", t1_result), ("T-2", t2_result)):
            if result.verdict == "missing":
                deciding = name
                break
    token = "partial-span" if (
        t1_result.verdict == "present but not derivable" or
        t2_result.verdict == "present but not derivable") \
        else "missing-field"
    return _refusal(
        code, "present but not derivable", figure_label, denom,
        _pointer(code, pointer, captured),
        shows="; ".join(parts) + ", and the row takes its verdict "
              "from its inputs, with the %s input deciding it"
              % deciding,
        token=token,
        follows="the row is present but not derivable on the "
                "composition of its step row inputs, so no figure "
                "is derived",
        rule_name=rule_name)


def _derive_b1(captured, universe, t1_result, t2_result):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    pointer = "PATH-LEDGER.md"
    ledger = _ledger_piece(captured)
    if ledger is not None:
        pointer = ledger.paths[0]
    if _basis_split(captured):
        basis_word = ""
        if ledger is not None and ledger.text:
            hit = _BASIS_WORD.search(ledger.text)
            if hit:
                basis_word = hit.group(1)
        return _refusal(
            "B-1", "present but not derivable", "no B-1 figure",
            denom, _pointer("B-1", pointer, captured),
            shows="the timestamps feeding this row stand on split "
                  "time bases: one transition timestamp states its "
                  "basis as %s and a gate record timestamp states "
                  "no time basis for its time of day"
                  % (basis_word or "a named basis"),
            token="no code fits",
            follows="the shared time basis the row requires does "
                    "not stand across its feeder timestamps, so no "
                    "figure is derived",
            rule_name="B-1 shared time basis rule")
    if t1_result.verdict == "missing" and \
            t2_result.verdict == "missing":
        summary = _metrics_section(
            captured.assembled_metrics or "", "## Build summary")
        if "not computed yet" in summary.lower():
            held = ("both inputs are missing on the date only "
                    "ground, and the build summary in the metrics "
                    "record stands as not computed yet and supplies "
                    "no figure")
        else:
            held = "both inputs are missing on the date only ground"
        return _refusal(
            "B-1", "missing", "no B-1 figure", denom,
            _pointer("B-1", pointer, captured),
            shows="the T-1 and T-2 rows the row ranks from are "
                  "missing, with the timestamp field and its form "
                  "named on those rows",
            token="no-feeder-record",
            follows="both ranking inputs are missing, so no split "
                    "or ranking figure exists for this row",
            rule_name="B-1 ranking input rule",
            broken="the step elapsed and step active figures that "
                   "are this row's only inputs",
            required="a formed elapsed figure and a formed active "
                     "figure for the steps, from which the build "
                     "totals are arithmetic",
            held=held)
    if t1_result.verdict != "present" or \
            t2_result.verdict != "present":
        return _b_composition_refusal(
            "B-1", denom, pointer, captured, t1_result, t2_result,
            "no B-1 figure", "B-1 composition rule")
    elapsed, active, both = _b_series_figures(captured)
    if not both:
        return _refusal(
            "B-1", "present but not derivable", "no B-1 figure",
            denom, _pointer("B-1", pointer, captured),
            shows="both input rows stand present and no step "
                  "carries both an elapsed figure and an active "
                  "figure, so no build total can be formed",
            token="missing-field",
            follows="the build totals are arithmetic on the step "
                    "figures, and no step supplies both figures",
            rule_name="B-1 composition rule")
    parts = []
    total_elapsed = 0.0
    total_active = 0.0
    for step in both:
        parts.append("Step %d elapsed %s hours, active %s hours"
                     % (step, _fmt_num(elapsed[step]),
                        _fmt_num(active[step])))
        total_elapsed += elapsed[step]
        total_active += active[step]
    figures = ("build elapsed %s hours and build active %s hours "
               "over %d steps: %s"
               % (_fmt_num(total_elapsed), _fmt_num(total_active),
                  len(both), "; ".join(parts)))
    for clause in _reversed_step_clauses(captured):
        figures += "; " + clause
    result = DerivationResult(
        "B-1", "present", figures, denom,
        _pointer("B-1", pointer, captured),
        derived_from="the T-1 step elapsed figures and the T-2 "
                     "step active figures for the steps counted",
        rule_name="B-1 build totals rule")
    result.numerator = None
    return result


def _derive_b_ranking(captured, universe, t1_result, code,
                      t2_result):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    pointer = "PATH-LEDGER.md"
    ledger = _ledger_piece(captured)
    if ledger is not None:
        pointer = ledger.paths[0]
    label = "slowest ranking" if code == "B-3" else "fastest ranking"
    if t1_result.verdict == "missing" and \
            t2_result.verdict == "missing":
        summary = _metrics_section(
            captured.assembled_metrics or "", "## Build summary")
        never = "never computed" in (
            captured.assembled_metrics or "").lower() or \
            "not computed yet" in summary.lower() or \
            "not computed yet" in (
                captured.assembled_metrics or "").lower()
        if code == "B-3":
            broken = "the ranked list and its ranking inputs"
            required = ("step elapsed and step active figures for "
                        "the steps, ranked with each ranked step's "
                        "wait share")
            held = ("no ranked list stands in any feeder, both "
                    "inputs are missing on the date only ground")
            if never:
                held += ", and the build summary was never computed"
        else:
            broken = "the ranked list and its ranking input"
            required = ("step active figures for the steps, ranked "
                        "with the step elapsed figure beside each")
            held = ("no ranked list stands in any feeder, the "
                    "active input is missing on the date only "
                    "ground, with the elapsed input missing on the "
                    "same ground")
            if never:
                held += ", and the build summary was never computed"
        return _refusal(
            code, "missing", "no ranking figure", denom,
            _pointer(code, pointer, captured),
            shows="the T-1 and T-2 derivations the row ranks from "
                  "are missing, and no inputs exist",
            token="no-feeder-record",
            follows="no %s can be formed where both inputs are "
                    "missing" % label,
            rule_name=code + " ranking input rule",
            broken=broken, required=required, held=held)
    if t1_result.verdict != "present" or \
            t2_result.verdict != "present":
        return _b_composition_refusal(
            code, denom, pointer, captured, t1_result, t2_result,
            "no ranking figure", code + " composition rule")
    elapsed, active, both = _b_series_figures(captured)
    rankable = []
    unreconciled = []
    for step in both:
        if active[step] > elapsed[step]:
            unreconciled.append(step)
        else:
            rankable.append(step)
    if not rankable and unreconciled:
        named = "; ".join(
            "Step %d active %s hours above elapsed %s hours"
            % (step, _fmt_num(active[step]),
               _fmt_num(elapsed[step])) for step in unreconciled)
        return _refusal(
            code, "present but not derivable", "no ranking figure",
            denom, _pointer(code, pointer, captured),
            shows="every step with both figures stands "
                  "unreconciled: " + named,
            token="unreconciled-figure",
            follows="no step remains rankable, so no ranking is "
                    "stated and the row takes its verdict from "
                    "its inputs",
            rule_name=code + " ranking rule")
    if not rankable:
        return _refusal(
            code, "present but not derivable", "no ranking figure",
            denom, _pointer(code, pointer, captured),
            shows="both input rows stand present and no step "
                  "carries both an elapsed figure and an active "
                  "figure, so no ranking can be formed",
            token="missing-field",
            follows="no step is rankable, so no ranking is stated",
            rule_name=code + " ranking rule")
    if code == "B-3":
        ordered = sorted(rankable,
                         key=lambda step: (-elapsed[step], step))
        key_of = elapsed.__getitem__
    else:
        ordered = sorted(rankable,
                         key=lambda step: (-active[step], step))
        key_of = active.__getitem__
    shown = ordered[:3]
    tied_cut = False
    if len(ordered) > 3:
        cut_value = key_of(ordered[2])
        extra = [step for step in ordered[3:]
                 if key_of(step) == cut_value]
        if extra:
            shown = ordered[:3] + extra
            tied_cut = True
    parts = []
    for step in shown:
        if elapsed[step] == 0:
            parts.append(
                "Step %d zero elapsed, no wait share" % step)
        else:
            share = (elapsed[step] - active[step]) / \
                elapsed[step] * 100.0
            parts.append(
                "Step %d elapsed %s hours, active %s hours, wait "
                "share %s percent"
                % (step, _fmt_num(elapsed[step]),
                   _fmt_num(active[step]), _fmt_num(share)))
    figures = "%s ranking: %s" % (
        "slowest steps" if code == "B-3" else "fastest steps",
        "; ".join(parts))
    if tied_cut:
        figures += ("; the ranking is tied at the third place cut "
                    "and runs past three steps, with every step "
                    "tied at the cut named")
    for step in unreconciled:
        figures += ("; Step %d excluded as unreconciled, active "
                    "%s hours above elapsed %s hours"
                    % (step, _fmt_num(active[step]),
                       _fmt_num(elapsed[step])))
    for clause in _reversed_step_clauses(captured):
        figures += "; " + clause
    coverage = denom
    if len(rankable) < 3:
        figures += ("; fewer than three eligible steps: "
                    "eligible %d" % len(rankable))
        coverage = "eligible %d steps of the step universe" \
            % len(rankable)
    result = DerivationResult(
        code, "present", figures, denom,
        _pointer(code, pointer, captured),
        derived_from="the T-1 step elapsed figures and the T-2 "
                     "step active figures, with the wait share "
                     "formed from those two figures",
        rule_name=code + " ranking rule")
    result.numerator = None
    result.coverage = coverage
    return result


def _b2_side_state(spent, budget, per_step, universe):
    """Class one side of B-2 from its ledger figures alone.

    The token side and the money side are classed separately,
    each from its own ledger figures: absent where no figure for
    the side stands in a ledger feeder, undefined where a spent
    figure stands and the budget is absent or stands at zero,
    yield where the per step figures cover the universe and a
    budget above zero stands, and partial where the span the
    ledger covers is part of the universe only.
    """
    if spent is None and budget is None:
        return "absent"
    if budget is None or budget == 0:
        return "undefined"
    if per_step and all(step in per_step
                        for step in universe.evidenced):
        return "yield"
    return "partial"


def _derive_b2(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    data = _ledger_data(captured)
    if data["conflicts"]:
        return _ledger_conflict_refusal(
            "B-2", denom, _pointer("B-2", data["pointer"], captured),
            data["conflicts"])
    if data["budget_conflicts"]:
        return _ledger_position_conflict_refusal(
            "B-2", denom, _pointer("B-2", data["pointer"], captured),
            data["budget_conflicts"], "budget")
    ledgers = data["ledgers"]
    pointer = data["pointer"]
    tokens = data["tokens"]
    money_figures = data["money"]
    token_spent = sum(tokens.values()) if tokens else None
    money_spent = sum(money_figures.values()) if money_figures else None
    token_budget = data["budget_tokens"]
    money_budget = data["budget_money"]
    token_state = _b2_side_state(token_spent, token_budget, tokens,
                                 universe)
    money_state = _b2_side_state(money_spent, money_budget,
                                 money_figures, universe)
    unread_ledgers = data["unread_ledgers"]
    if unread_ledgers and not (token_state == "yield" and
                                money_state == "yield"):
        piece = unread_ledgers[0]
        naming = _limit_naming(piece)
        return _refusal(
            "B-2", "present but not derivable",
            "no budget share figure", denom,
            _pointer("B-2", pointer, captured),
            shows="a cost ledger piece stands in the tree at "
                  + naming + ", so no spent or budget figure is "
                  "read from it",
            token=_quality_code(piece),
            follows="the row rests on a piece that was not read "
                    "past the bound named, so the row is present "
                    "but not derivable, and no spent or budget "
                    "figure is claimed absent from a piece that "
                    "was not read",
            rule_name="B-2 not read past a limit rule",
            broken="the ledger figure fields for spent and "
                   "budget in " + piece.paths[0] + ", which "
                     "stand not read past the limit named in "
                     "its capture reason",
            required="spent and budget figures taken from "
                     "ledger feeders inside the root only, on "
                     "both sides, read in full",
            held="the cost ledger stands in the tree at "
                 + naming)
    if ledgers:
        if token_state == "yield" and money_state == "yield":
            figures = (
                "money spent %d against a money budget of %d, %s "
                "percent; token spent %d against a token budget "
                "of %d, %s percent"
                % (money_spent, money_budget,
                   _fmt_num(money_spent * 100.0 / money_budget),
                   token_spent, token_budget,
                   _fmt_num(token_spent * 100.0 / token_budget)))
            result = DerivationResult(
                "B-2", "present", figures, denom, pointer,
                rule_name="B-2 budget share rule")
            if any(piece.text and "proxy" in piece.text.lower()
                   for piece in captured.pieces):
                result.statement = (
                    "proxy position: a labelled proxy figure "
                    "stands in the records, reported as a proxy "
                    "only, in its own terms, and never as a token "
                    "figure or a money figure")
            return result
        if token_state == "undefined" or money_state == "undefined":
            clauses = []
            if token_state == "undefined" and token_budget == 0:
                clauses.append(
                    "the token percentage is undefined against a "
                    "token budget standing at zero in the ledger, "
                    "with token spent %d standing in the ledger"
                    % token_spent)
            elif token_state == "undefined":
                clauses.append(
                    "the token percentage is undefined because "
                    "no token budget figure stands in the "
                    "ledger, with token spent %d standing in "
                    "the ledger" % token_spent)
            elif token_state == "absent":
                clauses.append(
                    "the token percentage is undefined because "
                    "no token spent or token budget figure "
                    "stands in the ledger")
            elif token_state == "yield":
                clauses.append(
                    "the token side stands on ledger figures, "
                    "with token spent %d against a token budget "
                    "of %d" % (token_spent, token_budget))
            else:
                clauses.append(
                    "the token side stands on a partial ledger "
                    "span, with token spent %d on the covered "
                    "span" % token_spent)
            if money_state == "undefined" and money_budget == 0:
                clauses.append(
                    "the money percentage is undefined against a "
                    "money budget standing at zero in the "
                    "ledger, with money spent %d standing in "
                    "the ledger" % money_spent)
            elif money_state == "undefined":
                clauses.append(
                    "the money percentage is undefined because "
                    "no money budget figure stands in the "
                    "ledger, with money spent %d standing in "
                    "the ledger" % money_spent)
            elif money_state == "absent":
                clauses.append(
                    "the money percentage is undefined because "
                    "no money spent or money budget figure "
                    "stands in the ledger")
            elif money_state == "yield":
                clauses.append(
                    "the money side stands on ledger figures, "
                    "with money spent %d against a money budget "
                    "of %d" % (money_spent, money_budget))
            else:
                clauses.append(
                    "the money side stands on a partial ledger "
                    "span, with money spent %d on the covered "
                    "span" % money_spent)
            figure_parts = []
            if token_spent is not None:
                if token_budget is not None:
                    figure_parts.append(
                        "token spent %d against a token budget "
                        "of %d" % (token_spent, token_budget))
                else:
                    figure_parts.append(
                        "token spent %d with no token budget "
                        "figure" % token_spent)
            else:
                figure_parts.append(
                    "token spent and token budget figures absent")
            if money_spent is not None:
                if money_budget is not None:
                    figure_parts.append(
                        "money spent %d against a money budget "
                        "of %d" % (money_spent, money_budget))
                else:
                    figure_parts.append(
                        "money spent %d with no money budget "
                        "figure" % money_spent)
            else:
                figure_parts.append(
                    "money spent and money budget figures absent")
            return _refusal(
                "B-2", "present but not derivable",
                "; ".join(figure_parts), denom, pointer,
                shows="; ".join(clauses),
                token="missing-field",
                follows="a side in that position does not yield "
                        "its figure, so no figure stands for "
                        "the row",
                rule_name="B-2 undefined percentage rule")
        if token_state == "absent" or money_state == "absent":
            if token_state == "absent" and money_state == "absent":
                return _refusal(
                    "B-2", "present but not derivable",
                    "no percentage stands", denom, pointer,
                    shows="a cost ledger stands in the tree and "
                          "it carries no spent or budget figure "
                          "for either side; the token percentage "
                          "is undefined because both the spent "
                          "figure and the budget figure are "
                          "absent for tokens; the money "
                          "percentage is undefined because the "
                          "budget figure is absent for money",
                    token="missing-field",
                    follows="the row follows the weaker limb, "
                            "and no figure stands for either "
                            "limb where no figure stands in the "
                            "ledger for either side",
                    rule_name="B-2 absent budget rule")
            if token_state == "absent":
                if money_state == "yield":
                    yielding = (
                        "money spent %d against a money budget "
                        "of %d, %s percent"
                        % (money_spent, money_budget,
                           _fmt_num(money_spent * 100.0
                                    / money_budget)))
                elif money_spent is not None:
                    yielding = (
                        "money spent %d on the covered span the "
                        "ledger states" % money_spent)
                else:
                    yielding = (
                        "a money budget of %d standing in the "
                        "ledger with no per step money figure"
                        % money_budget)
                return _refusal(
                    "B-2", "present but not derivable",
                    yielding + "; token spent and token budget "
                               "figures absent",
                    denom, _pointer("B-2", pointer, captured),
                    shows="one limb of the row yields its figure "
                          "from the ledger and the other limb "
                          "has no figure in any ledger feeder",
                    token="missing-field",
                    follows="the row follows the weaker limb, "
                            "so no combined figure stands",
                    rule_name="B-2 weaker limb rule",
                    broken="the token figure fields for spent "
                           "and budget, absent for the token "
                           "limb",
                    required="spent and budget figures taken "
                             "from ledger feeders inside the "
                             "root only, on both sides",
                    held="the money limb yields its figure "
                         "from the ledger figures and the token "
                         "limb does not, so the row follows the "
                         "weaker limb; the token spent and token "
                         "budget figures stand absent for the "
                         "token limb")
            if token_state == "yield":
                yielding = (
                    "token spent %d against a token budget of "
                    "%d, %s percent"
                    % (token_spent, token_budget,
                       _fmt_num(token_spent * 100.0
                                / token_budget)))
            elif token_spent is not None:
                yielding = (
                    "token spent %d on the covered span the "
                    "ledger states" % token_spent)
            else:
                yielding = (
                    "a token budget of %d standing in the "
                    "ledger with no per step token figure"
                    % token_budget)
            return _refusal(
                "B-2", "present but not derivable",
                yielding + "; money spent and money budget "
                           "figures absent",
                denom, _pointer("B-2", pointer, captured),
                shows="one limb of the row yields its figure "
                      "from the ledger and the other limb has "
                      "no figure in any ledger feeder",
                token="missing-field",
                follows="the row follows the weaker limb, so "
                        "no combined figure stands",
                rule_name="B-2 weaker limb rule",
                broken="the money figure fields for spent and "
                       "budget, absent for the money limb",
                required="spent and budget figures taken from "
                         "ledger feeders inside the root only, "
                         "on both sides",
                held="the token limb yields its figure from "
                     "the ledger figures and the money limb "
                     "does not, so the row follows the weaker "
                     "limb; the money spent and money budget "
                     "figures stand absent for the money limb")
        covered = sorted(set(tokens) | set(money_figures))
        missing = [step for step in sorted(universe.evidenced)
                   if step not in covered]
        figure_parts = []
        if token_spent is not None:
            figure_parts.append(
                "token spent %d on the covered span" % token_spent)
        elif token_budget is not None:
            figure_parts.append(
                "a token budget of %d with no per step token "
                "figure" % token_budget)
        if money_spent is not None:
            figure_parts.append(
                "money spent %d on the covered span" % money_spent)
        elif money_budget is not None:
            figure_parts.append(
                "a money budget of %d with no per step money "
                "figure" % money_budget)
        return _refusal(
            "B-2", "present but not derivable",
            "; ".join(figure_parts), denom, pointer,
            shows="a cost ledger inside the root meters part "
                  "of the step universe only, so the span the "
                  "ledger covers stands partial on the token "
                  "field and on the money field",
            token="partial-span",
            follows="the covered span stands named and no "
                    "figure stands for a step the ledger does "
                    "not cover, so no combined figure stands",
            rule_name="B-2 partial span rule",
            broken="the per step figure field for %s, which "
                   "the ledger span does not cover"
                   % _each_step(missing),
            required="a complete cost ledger span covering "
                     "every step in the universe, on both "
                     "sides",
            held="the ledger covers %s, with %s standing on "
                 "the covered span; the row follows the weaker "
                 "limb, and no figure stands for a step the "
                 "ledger does not cover"
                 % (_each_step(covered),
                    "; ".join(figure_parts)))
    joined = _money_mentions(captured)
    proxy = None
    rulings = [piece for piece in captured.pieces_of(CLS_GATE_RULING)
               if piece.text is not None]
    rulings.sort(key=lambda piece: piece.step or 0, reverse=True)
    for piece in rulings:
        m = re.search(r"Final figure[^:\n]*: (\d+) of (\d+) "
                      r"documented units", piece.text)
        if m:
            proxy = (m.group(1), m.group(2))
            break
    if proxy is None:
        for piece in rulings:
            m = re.search(r"(\d+) of (\d+) documented units",
                          piece.text)
            if m:
                proxy = (m.group(1), m.group(2))
                break
    if proxy is None:
        for piece in captured.pieces:
            if piece.text is None:
                continue
            m = re.search(r"(\d+) of (\d+) documented units",
                          piece.text)
            if m:
                proxy = (m.group(1), m.group(2))
                break
    if "documented units" in joined or "proxy" in joined.lower() \
            or proxy is not None:
        step_pointer = captured.first_path(CLS_STEP_RECORD) or pointer
        held = ("no cost ledger stands in the tree, so no spent or "
                "budget figure is taken from a ledger feeder for "
                "either side, the money budget position is absent "
                "and not zero, and no percentage is formed for "
                "either side, with step record positions standing "
                "as context only")
        if proxy is not None:
            held += (" and the labelled proxy figure of %s of %s "
                     "documented units reported as a proxy only "
                     "and never as a token or money figure" % proxy)
        return _refusal(
            "B-2", "present but not derivable", "no budget share "
            "figure", denom, _pointer("B-2", step_pointer, captured),
            shows="a labelled proxy statement stands in the step "
                  "records, stating documented units on a proxy "
                  "basis, and no measured budget figure stands",
            token="no-measurement-basis",
            follows="a proxy statement is not a measurement, so no "
                    "budget share figure stands",
            rule_name="B-2 measurement basis rule",
            broken="the ledger figure fields for spent and budget, "
                   "on the token side and on the money budget side",
            required="spent and budget figures taken from ledger "
                     "feeders inside the root only, on both sides, "
                     "with a percentage formed only against a "
                     "standing budget",
            held=held)
    if captured.pieces_of(CLS_STEP_RECORD):
        step_pointer = captured.first_path(CLS_STEP_RECORD) or pointer
        return _refusal(
            "B-2", "present but not derivable",
            "no percentage stands", denom,
            _pointer("B-2", step_pointer, captured),
            shows="no cost ledger stands in the tree; the token "
                  "percentage is undefined because both the spent "
                  "figure and the budget figure are absent for "
                  "tokens; the money percentage is undefined "
                  "because the budget figure is absent for money",
            token="missing-field",
            follows="the row follows the weaker limb, and no "
                    "figure stands for either limb where no "
                    "cost ledger stands",
            rule_name="B-2 absent budget rule")
    return _refusal(
        "B-2", "missing", "no budget share figure", denom, pointer,
        shows="no cost ledger piece and no budget figure stands in "
              "the capture for this metric",
        token="no-feeder-record",
        follows="no feeder record for the metric exists in the "
                "tree, so the row is missing",
        rule_name="B-2 feeder standing rule")


# --------------------------------------------------------- report model

def _data_quality_entries(captured):
    entries = []
    has_correcting = any("correcting" in path
                         for piece in captured.pieces
                         for path in piece.paths)
    for piece in captured.pieces:
        name = piece.paths[0]
        if _piece_not_read_in_full(piece):
            token = _quality_code(piece)
            state_word = piece.quality_state or "not read in full"
            shows = ("the piece stands %s in the capture and no "
                     "text from it stands in the capture"
                     % state_word)
            detail = _reason_detail(piece)
            if detail and detail.lower() not in shows.lower():
                shows += "; " + detail
            if piece.record_class == CLS_DECISION_QUEUE:
                shows += ("; the queue file stands as a piece not "
                          "read in full, and the governing record "
                          "falls back under WV-12")
            if token == "over-limit-piece":
                shows += "; " + _walk_order_sample(captured, piece)
            entries.append(
                "%s: What the record shows: %s What follows: %s "
                "the piece supplies no figure to any derivation"
                % (name, shows, token))
        elif "TRUNCATED" in piece.text and not has_correcting:
            entries.append(
                "%s: What the record shows: the piece carries a "
                "truncation marker in its text and no correcting "
                "record for it stands in the capture What follows: "
                "truncated-no-correcting-record the visible part of "
                "the piece is never counted as a complete record"
                % name)
    for piece in captured.pieces:
        if piece.text is None:
            continue
        if piece.record_class != CLS_AUDIT_PAPER:
            continue
        signal = _signal_failure(piece.text)
        if signal is None:
            continue
        name = piece.paths[0]
        if has_correcting:
            entries.append(
                "%s: What the record shows: the piece fails %s, a "
                "completeness signal under D-19, and its visible "
                "part counts toward nothing What follows: a "
                "correcting record stands for this piece and "
                "supplies the substitution, cited as the source"
                % (name, signal))
        else:
            entries.append(
                "%s: What the record shows: the piece fails %s, a "
                "completeness signal under D-19, and its visible "
                "part counts toward nothing What follows: "
                "truncated-no-correcting-record the piece is "
                "treated as truncated and no correcting record "
                "stands for it" % (name, signal))
    if not _known_version(captured.definitions_version):
        entries.append(
            "build-metrics-record.md: What the record shows: the "
            "metrics record states definitions version %s, which "
            "is not a version the settled definitions recognise "
            "What follows: unknown-definitions-version derivations "
            "whose feeder records stand are refused on that ground"
            % captured.definitions_version)
    if _basis_split(captured):
        entries.append(
            "time basis: What the record shows: the timestamps "
            "feeding the B family rows stand on split time bases, "
            "one stating its basis in words and one stating no "
            "basis What follows: no code fits the shared time "
            "basis those rows require does not stand")
    return entries


_HALT_SENTENCE = re.compile(r"[^.!?\n]+")


def _build_state(captured):
    """The build open state, read from recognised pieces only.

    The tree stands halted where a recognised piece states the
    halt in its own words, in a sentence naming the build or the
    work. Halt wording that names neither, or that stands only in
    a piece the capture does not recognise, is read as in
    progress, and the word halted is not used for the tree.
    """
    for piece in captured.pieces:
        if not piece.text:
            continue
        for sentence in _HALT_SENTENCE.findall(piece.text):
            low = sentence.lower()
            if "halt" in low and ("build" in low or "work" in low):
                return "halted", piece.paths[0]
    return "in progress", None


def _missing_closing_steps(captured, universe):
    """Steps evidenced with no gate record standing in the capture."""
    have = set()
    for piece in captured.pieces:
        if piece.record_class in GATE_CLASSES and piece.step:
            have.add(piece.step)
    return [step for step in universe.evidenced if step not in have]


def _record_disagreement_entries(captured):
    """Disagreements block entries stated in the records at large.

    Returns the restatement group entries and the blocking group
    entries, the blocking entries as (first line, entry line)
    pairs, the first line standing only where the entry carries
    one. Three stated forms stand scanned: a total spins figure
    the metrics record states against a different total in the
    step record, touching E-2 and B-2, one entry per metric
    touched, governed where a named correction governs the step
    record figure and ungoverned where none stands; a closure
    state the metrics record states under the gate pattern named
    for gate records, touching F-2, governed with the pattern
    named; and a figure standing in a form no class in the record
    names, the unclassifiable disagreement failure form, which
    stands in the block and is never omitted.
    """
    restatements = []
    blocking = []
    metrics_name = _metrics_record_name(captured)
    metrics_text = captured.assembled_metrics or ""
    step_paths = {}
    for piece in captured.pieces:
        if piece.step is not None and piece.paths:
            step_paths.setdefault(piece.step, piece.paths[0])
    for step, metrics_figure, record_figure, governed in \
            _spin_disagreements(captured):
        figures = (
            "the metrics record states total spins through "
            "Step %d as %d, the step record states total spins "
            "for Step %d as %d"
            % (step, metrics_figure, step, record_figure))
        records = "%s and %s" % (
            metrics_name, step_paths.get(step, ""))
        if governed:
            figures += (
                ", and the correction named in the records "
                "governs the step record figure")
            for code in ("E-2", "B-2"):
                restatements.append(
                    "Records: %s | Figures: %s | Metric: %s | "
                    "Governing position: restatement with its "
                    "correction named" % (records, figures, code))
        else:
            for code in ("E-2", "B-2"):
                blocking.append((
                    "Blocked metric: %s, no verdict was withheld "
                    "for this disagreement" % code,
                    "Records: %s | Figures: %s | Metric: %s | "
                    "Governing position: ungoverned with no "
                    "verdict depending on it"
                    % (records, figures, code)))
    closure = re.search(
        r"Closure state for Step (\d+): ([A-Za-z][A-Za-z-]*), "
        r"under the gate pattern named", metrics_text)
    if closure:
        step = int(closure.group(1))
        state = closure.group(2)
        record_path = step_paths.get(step, "")
        record_state = None
        for piece in captured.pieces:
            if piece.step == step and piece.text:
                stated = re.search(r"Closure state:\s*([A-Za-z-]+)",
                                   piece.text)
                if stated:
                    record_state = stated.group(1)
                    record_path = piece.paths[0]
                    break
        if record_state is not None:
            blocking.append((
                "Blocked metric: F-2, no verdict was withheld "
                "for this disagreement",
                "Records: %s and %s | Figures: the metrics "
                "record states the closure state for Step %d as "
                "%s under the gate pattern named for gate "
                "records, the record states the closure state "
                "for Step %d as %s | Metric: F-2 | Governing "
                "position: governed with the pattern named"
                % (metrics_name, record_path, step, state, step,
                   record_state)))
    if "form no class in the record names" in metrics_text:
        unnamed_path = None
        for piece in captured.pieces:
            if piece.text and "in an unnamed form" in piece.text:
                unnamed_path = piece.paths[0]
                break
        if unnamed_path is not None:
            blocking.append((
                "Blocked metric: the unclassifiable figure, no "
                "verdict was withheld for this disagreement",
                "Records: %s and %s | Figures: the metrics "
                "record states a figure in a form no class in "
                "the record names, the step record states a "
                "figure in an unnamed form | Metric: the "
                "unclassifiable figure | Governing position: "
                "ungoverned with no verdict depending on it"
                % (metrics_name, unnamed_path)))
    return restatements, blocking


def _disagreement_lines(captured):
    """The disagreements block, in its two groups in order.

    The restatements settled by a governing correction stand
    first, then the contradictions that block or weaken a metric.
    Inside its group, an entry in the blocking group carries
    first a first line naming the blocked metric and whether a
    verdict was withheld, where the entry carries one, and each
    entry carries its entry line in the closed part order, with
    its governing position in one of the three fixed wordings.
    Where the queue file inside the root governs and the decision
    table disagrees on an item, the derivation follows the queue
    figure and the table figure stands here under the governed
    wording, as DG-07 states it.
    """
    restatements, blocking = _record_disagreement_entries(captured)
    r5, b5 = _slice5_disagreement_entries(captured)
    restatements += r5
    blocking += [(None, entry) for entry in b5]
    blocking += _ledger_disagreement_entries(captured)
    blocking += _ledger_position_disagreement_entries(captured)
    blocking += _step_record_disagreement_entries(captured)
    blocking += _proxy_disagreement_entries(captured)
    feeders = _decision_feeders(captured)
    if feeders["queue_usable"] and feeders["table_items"]:
        table = {item["item"]: item
                 for item in feeders["table_items"]}
        ledger = _ledger_piece(captured)
        banked_text = ledger.text if ledger is not None and \
            ledger.text else ""
        for item in feeders["queue_items"]:
            other = table.get(item["item"])
            if not other or not item["ruled"] or not other["ruled"] \
                    or item["ruled"] == other["ruled"]:
                continue
            figures = ("the queue file states %s ruled at %s, the "
                       "decision table states %s ruled at %s"
                       % (item["item"], item["ruled"], item["item"],
                          other["ruled"]))
            blocking.append((None,
                "Records: DECISION-QUEUE.md and the decision "
                "table in %s | Figures: %s | Metric: D-1 | "
                "Governing position: governed with the pattern "
                "named" % (_metrics_record_name(captured), figures)))
            if item["item"] in banked_text:
                blocking.append((None,
                    "Records: DECISION-QUEUE.md and the decision "
                    "table in %s | Figures: %s | Metric: T-4 | "
                    "Governing position: governed with the "
                    "pattern named"
                    % (_metrics_record_name(captured), figures)))
    lines = ["Group: restatements settled by a governing correction"]
    lines += restatements
    lines.append(
        "Group: contradictions that block or weaken a metric")
    for first_line, entry in blocking:
        if first_line:
            lines.append(first_line)
        lines.append(entry)
    return lines


def _build_identity_statement(captured):
    """The build identity statement for the second header line.

    The identities the records inside the tree state, each stated
    where more than one stands, with the conflict stated and none
    taken as settled; a single identity stated as found, or as
    copied where the records state it as a copy from another
    tree; and the absence stated where no record inside the tree
    states an identity.
    """
    identities = []
    copied = False
    for piece in captured.pieces:
        if not piece.text:
            continue
        for found in re.finditer(
                r"^Build(?: identity)?:\s*(.+?)\s*$",
                piece.text, re.M):
            value = found.group(1).strip().rstrip(".")
            if value and value not in identities:
                identities.append(value)
                if "copied from" in piece.text or \
                        "a copy from" in piece.text:
                    copied = True
    if len(identities) > 1:
        return ("conflict: the records inside the tree state "
                "conflicting build identities, %s, and the "
                "conflict stands stated with none of them taken "
                "as settled" % "; ".join(identities))
    if identities:
        if copied:
            return ("%s, stated in the records as a copy from "
                    "another tree and not taken as this tree own "
                    "identity" % identities[0])
        return identities[0]
    if captured.build_identity:
        return str(captured.build_identity)
    return "no build identity was found inside the tree"


_KIND_BY_TOKEN = {
    "missing-field": "missing field",
    "no-feeder-record": "missing record",
    "date-only-form": "wrong form",
    "no-post-triage-breakdown": "wrong form",
    "no code fits": "wrong form",
    "wrong-form": "wrong form",
    "unreconciled-figure": "unreconciled",
    "unknown-definitions-version": "not producible",
    "partial-span": "missing field",
    "over-limit-piece": "not producible",
    "malformed-piece": "not producible",
    "unreadable-piece": "not producible",
    "truncated-no-correcting-record": "not producible",
    "no-measurement-basis": "missing field",
    "no-named-rule": "not producible",
    "governing-scale-conflict": "wrong form",
    "record-disagrees": "unreconciled",
}

_KIND_ORDER = ("missing record", "missing field", "wrong form",
               "unreconciled", "not producible")


def _broken_link_kind(result):
    """The broken link kind of a row that does not stand present,
    in the five kind forms the data quality section counts.

    The kind stands read from the reason code the result holds,
    with the F-2 scattered gate outcome form, whose held form
    names the scattering, standing as a wrong form, and with a
    text reading of the broken link for any code outside the
    table.
    """
    token = (result.code_token or "").strip()
    if result.code == "F-2" and token == "missing-field" and \
            "scattered" in (result.form_held or ""):
        return "wrong form"
    if token in _KIND_BY_TOKEN:
        return _KIND_BY_TOKEN[token]
    text = " ".join(part for part in (result.broken_link or "",
                                      result.form_required or "")
                    if part).lower()
    if "field" in text:
        return "missing field"
    if "form" in text:
        return "wrong form"
    if "record" in text:
        return "missing record"
    return "not producible"


_BUDGET_POSITION_TERMS = (
    "money", "token", "spin", "ceiling", "spend", "budget",
    "documented", "external", "nil", "cost")


def _is_budget_position_value(value):
    """Whether a Budget position value states a cost position.

    A budget position is a statement of a cost position: it
    carries a cost term or a figure. A lone status word, the
    heading word of a gate record section stating that a budget
    item landed, carries neither and is not a budget position,
    however the line that carries it is labelled.
    """
    text = value.strip()
    if not text:
        return False
    if len(text.split()) == 1 and not any(
            char.isdigit() for char in text):
        return False
    lowered = text.lower()
    return any(term in lowered for term in _BUDGET_POSITION_TERMS) \
        or any(char.isdigit() for char in text)


def _proxy_candidates(captured):
    """Labelled proxy figures in the records, in capture order.

    Each candidate carries its kind (share, ceiling or plain),
    its figure text, its source path, and whether its own line
    states it as a final position. A figure counts as labelled
    where the proxy wording stands in its own sentence or
    elsewhere on its own line, so a final figure whose basis
    sentence follows it on the same line is not lost. No figure
    is taken across a line boundary, and no figure is taken
    from a line that carries no proxy wording at all.
    """
    candidates = []
    for piece in captured.pieces:
        if piece.text is None:
            continue
        for raw_line in piece.text.splitlines():
            if "documented units" not in raw_line:
                continue
            line_proxy = "proxy" in raw_line.lower()
            for sentence in re.split(r"(?<=[.;])\s+", raw_line):
                if "documented units" not in sentence:
                    continue
                if not line_proxy and \
                        "proxy" not in sentence.lower():
                    continue
                share = re.search(
                    r"(\d+) of (\d+) documented units", sentence)
                ceiling = re.search(
                    r"ceiling of (\d+) documented units", sentence)
                plain = re.search(r"(\d+) documented units",
                                  sentence)
                if share:
                    kind = "share"
                    figure = "%s of %s documented units" \
                        % share.groups()
                elif ceiling:
                    kind = "ceiling"
                    figure = ("agent count ceiling of %s "
                              "documented units" % ceiling.group(1))
                elif plain:
                    kind = "plain"
                    figure = "%s documented units" % plain.group(1)
                else:
                    continue
                candidates.append({
                    "kind": kind, "figure": figure,
                    "path": piece.paths[0],
                    "final": "final" in raw_line.lower()})
    return candidates


def _chosen_proxy_share(candidates):
    """The governing labelled proxy share figure, or None.

    Successive records restate one proxy position as the build
    spends, so the shares are successive positions of one
    figure, not simultaneous positions. The final position
    governs, under the pattern that a later closing entry
    governs over the cells it restates: the last share its own
    line states as a final position, or the last share in
    capture order where no share states itself as final.
    """
    shares = [cand for cand in candidates if cand["kind"] == "share"]
    if not shares:
        return None
    finals = [cand for cand in shares if cand["final"]]
    return finals[-1] if finals else shares[-1]


def _proxy_disagreement_entries(captured):
    """The disagreements entry for successive proxy shares.

    Where the records state two or more distinct labelled proxy
    share figures, the disagreement between them stands in the
    block in the governed form: the later final position
    governs, no verdict was withheld for it, and the B-2 row and
    the record cost section both report the governing figure as
    a proxy only. One entry stands, for B-2, the metric the
    proxy figure stands as context for.
    """
    candidates = _proxy_candidates(captured)
    distinct = []
    for cand in candidates:
        if cand["kind"] != "share":
            continue
        if cand["figure"] not in [held["figure"] for held in distinct]:
            distinct.append(cand)
    if len(distinct) < 2:
        return []
    chosen = _chosen_proxy_share(candidates)
    records = []
    for cand in distinct:
        if cand["path"] not in records:
            records.append(cand["path"])
    figures = "; ".join(
        "%s, as recorded in %s" % (cand["figure"], cand["path"])
        for cand in distinct)
    entry = (
        "Records: %s | Figures: the records state successive "
        "labelled proxy figures, %s, and the final position "
        "governs under the later closing entry pattern, so the "
        "report states %s as a proxy only | Metric: B-2 | "
        "Governing position: governed with the pattern named"
        % (" and ".join(records), figures, chosen["figure"]))
    return [("Blocked metric: B-2, no verdict was withheld for "
             "this disagreement", entry)]


def _record_cost_lines(captured, universe):
    """The record cost section lines, in the D4R-27 form.

    The presence or absence of a cost ledger file as a cost fact
    in its own right; the spin count as recorded, where the tree
    carries it; the token position as recorded, stated as absent
    and not as zero where none stands; the budget position line,
    carrying its record and no cap test wording in the same line
    as any figure it states; and the labelled proxy figures in
    the records restated with their proxy basis wording in the
    same line, with successive proxy share positions stated in
    their governing final form only, as _chosen_proxy_share
    states it, and their disagreement standing in the block.
    """
    lines = []
    data = _ledger_data(captured)
    if data["ledgers"]:
        lines.append(
            "Cost ledger: a cost ledger stands in the tree at %s"
            % data["pointer"])
    else:
        lines.append(
            "Cost ledger: no cost ledger file stands in the "
            "tree, stated as a cost fact in its own right")
    totals = _total_spins(captured, universe)
    if totals:
        lines.append(
            "Spin count: total spins as recorded in the step "
            "records and rosters, %s"
            % ", ".join("Step %d: %d" % (step, totals[step])
                        for step in sorted(totals)))
    token_conflicts = [entry for entry in data["conflicts"]
                       if entry[1] == "tokens"]
    if token_conflicts:
        lines.append(
            "Token position: the cost ledger states contradictory "
            "token figures, %s, and no token total is taken from "
            "them" % _ledger_conflict_text(token_conflicts))
    elif data["tokens"]:
        lines.append(
            "Token position: token figures as recorded in the "
            "cost ledger, %d in all across %d steps"
            % (sum(data["tokens"].values()), len(data["tokens"])))
    else:
        lines.append(
            "Token position: no token figure stands recorded "
            "in the tree, stated as absent and not as zero")
    budget_line = None
    for piece in captured.pieces:
        if piece.text is None:
            continue
        for raw_line in piece.text.splitlines():
            if raw_line.strip().startswith("#"):
                continue
            stated = re.search(r"Budget position:\s*([^.;]+)",
                               raw_line)
            if not stated:
                continue
            value = stated.group(1).strip()
            if not _is_budget_position_value(value):
                continue
            budget_line = (
                "Budget position: %s, as recorded in %s"
                % (value, piece.paths[0]))
            break
        if budget_line is not None:
            break
    if budget_line is None and (data["budget_money"] is not None
                                or data["budget_tokens"] is not None):
        sides = []
        if data["budget_money"] is not None:
            sides.append("money budget of %d"
                         % data["budget_money"])
        if data["budget_tokens"] is not None:
            sides.append("token budget of %d"
                         % data["budget_tokens"])
        budget_line = (
            "Budget position: %s, as recorded in %s"
            % (" and ".join(sides), data["pointer"]))
    if budget_line is None:
        budget_line = (
            "Budget position: absent, no budget position stands "
            "recorded in the tree")
    lines.append(budget_line)
    candidates = _proxy_candidates(captured)
    chosen_share = _chosen_proxy_share(candidates)
    seen_proxy = set()
    for cand in candidates:
        if cand["kind"] == "share" and cand is not chosen_share:
            continue
        key = (cand["figure"], cand["path"])
        if key in seen_proxy:
            continue
        seen_proxy.add(key)
        lines.append(
            "Proxy figure: %s, on a labelled proxy basis as "
            "recorded in %s" % (cand["figure"], cand["path"]))
    return lines


_TERM_TEXTS = {
    "missing-field": "a field the derivation requires does not "
                     "stand in the record",
    "no-feeder-record": "no feeder record for the metric stands "
                        "in the tree",
    "date-only-form": "the record carries dates only, with no "
                      "time of day, where a time of day is "
                      "required",
    "no-post-triage-breakdown": "no post triage severity "
                                "breakdown stands in the form "
                                "the row counts from",
    "no code fits": "the code list holds no code naming the "
                    "case the records stand in",
    "partial-span": "the feeder series covers part of the span "
                    "the row requires and no more",
    "unreconciled-figure": "two records state figures that do "
                           "not reconcile and neither is taken",
    "unknown-definitions-version": "the metrics record states a "
                                   "definitions version the "
                                   "settled definitions do not "
                                   "recognise",
    "no-measurement-basis": "no measurement basis for the figure "
                            "stands in the records",
    "truncated-no-correcting-record": "a piece stands truncated "
                                      "and no correcting record "
                                      "stands for it",
    "over-limit-piece": "a piece stands over a limit the walk "
                        "enforces and was not read in full",
    "malformed-piece": "a piece stands in a form the capture "
                       "cannot read as its record kind",
    "unreadable-piece": "a piece could not be read at all",
    "no-named-rule": "no named rule in the settled definitions "
                     "covers the case",
    "governing-scale-conflict": "two records state the figure on "
                                "different scales and no "
                                "governing scale stands named",
    "record-disagrees": "a record states a figure the feeder "
                        "records disagree with, and the feeder "
                        "figure stands",
    "wrong-form": "the record holds the figure in a form the "
                  "derivation cannot read",
}


def _terms_lines(results):
    """One terms line for each term the report uses in a reason
    line, in the order that term first stands used."""
    lines = []
    seen = set()
    for result in results:
        token = (result.code_token or "").strip()
        if not token or token in seen:
            continue
        seen.add(token)
        lines.append("%s: %s" % (
            token, _TERM_TEXTS.get(
                token, "a reason term the report uses, naming "
                       "the broken link form for its row")))
    return lines


def derive_report(captured):
    """Derive the one ReportModel from the one CapturedRead.

    The StepUniverse the derivations read is the one construction
    in this module, build_step_universe, built from this same
    capture. No second construction stands anywhere else.
    """
    universe = build_step_universe(captured)
    t1 = _derive_t1(captured, universe)
    t2 = _derive_t2(captured, universe)
    results_by_code = {
        "T-1": t1,
        "T-2": t2,
        "T-4": _derive_t4(captured, universe),
        "T-7": _derive_t7(captured, universe),
        "E-1": _derive_e1(captured, universe),
        "E-2": _derive_e2(captured, universe),
        "E-3": _derive_e3(captured, universe),
        "E-4": _derive_e4(captured, universe),
        "F-2": _derive_f2(captured, universe),
        "Q-1": _derive_q1(captured, universe),
        "Q-3": _derive_q3(captured, universe),
        "Q-4": _derive_q4(captured, universe),
        "D-1": _derive_d1(captured, universe),
        "B-1": _derive_b1(captured, universe, t1, t2),
        "B-2": _derive_b2(captured, universe),
        "B-3": _derive_b_ranking(captured, universe, t1, "B-3", t2),
        "B-4": _derive_b_ranking(captured, universe, t1, "B-4", t2),
    }
    # Seam failures surfaced under the plan Section 4 error
    # form: each failed seam call in derive_report records its
    # error here, with the rows it serves, and the error stands
    # in the statement line of each of those rows and in the
    # data quality section below, never dropped in silence.
    seam_errors = []
    # The cross check marking for the staffing rows, as part of the
    # core in this slice: the derivations above carry the marking
    # in their statement lines, and any marking the Cross check
    # module supplies for a row that carries none yet stands
    # beside it, never overriding a feeder result.
    try:
        from metrics_starter_collector.cross_check import \
            staffing_cross_check_statements
        extra = staffing_cross_check_statements(
            captured, universe, {}, _total_spins(captured, universe),
            {})
        if isinstance(extra, dict):
            for code, statement in extra.items():
                result = results_by_code.get(code)
                if result is not None and statement and \
                        not getattr(result, "statement", None):
                    result.statement = statement
    except Exception as exc:
        seam_errors.append((("E-1", "E-2", "F-2"), _error_form(
            "staffing_cross_check_statements",
            _metrics_record_name(captured), exc)))
    # The cross check marking for the cost rows, consumed through
    # the Module 4 role in the same form: the seam wiring of the
    # Builder C function cost_cross_check_statements, called with
    # the one CapturedRead and a feeder figures mapping holding,
    # for E-3, the per step token figures from the ledger; for
    # E-4, the per step money figures from the ledger and the
    # step record positions together; and for B-2, a mapping
    # holding its money spent and token spent totals under money
    # and token named keys, the token side and the money side
    # stated separately. Any marking the function supplies for a
    # row that carries none yet stands in the statement line of
    # that row, never overriding a feeder result.
    if _known_version(captured.definitions_version):
        try:
            from metrics_starter_collector.cross_check import \
                cost_cross_check_statements
            cost_data = _ledger_data(captured)
            cost_step_money, _cost_pointer, _cost_conflicts = \
                _step_record_money(captured)
            cost_money = dict(cost_step_money)
            cost_money.update(cost_data["money"])
            cost_feeders = {}
            if cost_data["tokens"]:
                cost_feeders["E-3"] = dict(cost_data["tokens"])
            if cost_money:
                cost_feeders["E-4"] = dict(cost_money)
            b2_sides = {}
            if cost_data["money"]:
                b2_sides["money spent"] = sum(
                    cost_data["money"].values())
            if cost_data["tokens"]:
                b2_sides["token spent"] = sum(
                    cost_data["tokens"].values())
            if b2_sides:
                cost_feeders["B-2"] = b2_sides
            cost_markings = cost_cross_check_statements(
                captured, cost_feeders)
            if isinstance(cost_markings, dict):
                for code, statement in cost_markings.items():
                    result = results_by_code.get(code)
                    if result is not None and statement and \
                            not getattr(result, "statement", None):
                        result.statement = statement
        except Exception as exc:
            seam_errors.append((("E-3", "E-4", "B-2"), _error_form(
                "cost_cross_check_statements",
                _metrics_record_name(captured), exc)))
    # The unknown definitions version position for the Slice 4
    # rows: where the metrics record states a version the settled
    # definitions do not recognise, the rows whose feeder records
    # stand are present but not derivable on that ground, the T-2
    # row, whose feeder is a stated duration and none stands on
    # that variant, stays missing, and the B family rows take
    # their position through the composition rule from input rows
    # that do not stand as feeders on that variant.
    if not _known_version(captured.definitions_version):
        version = captured.definitions_version
        feeders = _decision_feeders(captured)
        ledger_stands = bool(captured.pieces_of(CLS_PATH_LEDGER))
        d1_feeder_stands = feeders["queue_piece"] is not None or \
            feeders["table_stands"]
        for code in ("T-1", "T-4", "D-1"):
            current = results_by_code[code]
            stands = ledger_stands if code in ("T-1", "T-4") \
                else d1_feeder_stands
            if stands:
                results_by_code[code] = _unknown_version_result(
                    captured, code, current.denominator,
                    current.pointer)
        # The Slice 6 rows on the same variant: E-4 and B-2,
        # whose feeder records stand where a cost ledger stands
        # inside the root, and E-4 also where a step record
        # position states a per step figure, are present but not
        # derivable on the unknown version ground; E-3, whose
        # feeder is a token figure in the ledger and none stands
        # on the money only variant, stays missing in the form
        # its own derivation gives it.
        cost_data = _ledger_data(captured)
        cost_step_money, _cost_step_pointer, _cost_conflicts = \
            _step_record_money(captured)
        if cost_data["ledgers"] or cost_step_money:
            current = results_by_code["E-4"]
            results_by_code["E-4"] = _unknown_version_result(
                captured, "E-4", current.denominator,
                current.pointer)
        if cost_data["ledgers"]:
            current = results_by_code["B-2"]
            results_by_code["B-2"] = _unknown_version_result(
                captured, "B-2", current.denominator,
                current.pointer)
        if cost_data["tokens"]:
            current = results_by_code["E-3"]
            results_by_code["E-3"] = _unknown_version_result(
                captured, "E-3", current.denominator,
                current.pointer)
        current = results_by_code["T-2"]
        results_by_code["T-2"] = _refusal(
            "T-2", "missing", "no step duration figure",
            current.denominator, current.pointer,
            shows="no feeder record for the T-2 row stands on "
                  "this tree: the metrics record states "
                  "definitions version %s, which the settled "
                  "definitions do not recognise, and no stated "
                  "duration stands in a form the row can read"
                  % version,
            token="no-feeder-record",
            follows="no feeder record for the metric exists in "
                    "the tree, so the row is missing",
            rule_name="T-2 feeder standing rule")
        for code in ("B-1", "B-3", "B-4"):
            current = results_by_code[code]
            results_by_code[code] = _refusal(
                code, "missing", "no B family figure",
                current.denominator, current.pointer,
                shows="the T-1 and T-2 rows the row composes from "
                      "do not stand as feeders on this tree: the "
                      "metrics record states definitions version "
                      "%s, which the settled definitions do not "
                      "recognise" % version,
                token="no-feeder-record",
                follows="the row takes its position through the "
                        "composition rule from its input rows, "
                        "and neither input stands, so the row is "
                        "missing",
                rule_name=code + " composition rule")
    # The cross check marking for the time and decision rows,
    # consumed through the Module 4 role: any disagreement stands
    # in the statement line of the affected row and never
    # overrides a feeder result.
    if _known_version(captured.definitions_version):
        try:
            from metrics_starter_collector.cross_check import \
                time_decision_cross_check_statements
            series, _ledger = _time_series(captured)
            feeder_figures = {}
            t1_figures = {step: figures["elapsed"]
                          for step, figures in series.items()
                          if figures["elapsed"] is not None}
            t2_figures = {step: figures["active"]
                          for step, figures in series.items()
                          if figures["active"] is not None}
            if t1_figures:
                feeder_figures["T-1"] = t1_figures
            if t2_figures:
                feeder_figures["T-2"] = t2_figures
            # The B family rows are formed from the same series
            # figures: B-1 and B-3 rest on the T-1 elapsed figures
            # for each step, and B-4 rests on the T-2 active
            # figures for each step, so those figures stand as
            # the feeder figures for the B rows here.
            if t1_figures:
                feeder_figures["B-1"] = t1_figures
                feeder_figures["B-3"] = t1_figures
            if t2_figures:
                feeder_figures["B-4"] = t2_figures
            markings = time_decision_cross_check_statements(
                captured, feeder_figures)
            if isinstance(markings, dict):
                for code, statement in markings.items():
                    result = results_by_code.get(code)
                    if result is not None and statement and \
                            not getattr(result, "statement", None):
                        result.statement = statement
        except Exception as exc:
            seam_errors.append(
                (("T-1", "T-2", "B-1", "B-3", "B-4"), _error_form(
                    "time_decision_cross_check_statements",
                    _metrics_record_name(captured), exc)))
    # The build open state naming on the B family rows: the open
    # state on an in progress tree, the halt naming on a halted
    # tree, in the statement line of each B row.
    state_word, state_path = _build_state(captured)
    if state_word == "halted":
        state_naming = ("build state naming: the build stands "
                        "halted, as the recognised piece %s states "
                        "in its own words" % state_path)
    else:
        state_naming = ("build state naming: the build stands in "
                        "progress, and no recognised piece states "
                        "a halt in its own words")
    for code in ("B-1", "B-2", "B-3", "B-4"):
        result = results_by_code[code]
        result.build_state_statement = state_naming
    results = [results_by_code[code] for code in STARTER_ORDER]
    for seam_codes, seam_error in seam_errors:
        for seam_code in seam_codes:
            seam_result = results_by_code[seam_code]
            seam_result.statement = _join_statements(
                getattr(seam_result, "statement", None), seam_error)
    # Slice 7 model assembly, on the final results: the D-1
    # Statement part content, standing on the D-1 row only; the
    # reconciliation part on present rows that carry none yet;
    # and the broken link kind naming on rows that do not stand
    # present, the kind the data quality census counts.
    d1_result = results_by_code["D-1"]
    if getattr(d1_result, "statement", None):
        d1_result.statement_part = d1_result.statement
    else:
        d1_feeders = _decision_feeders(captured)
        if d1_feeders["queue_usable"]:
            d1_result.statement_part = _D1_FOUNDATION_QUEUE
        elif d1_feeders["table_stands"]:
            d1_result.statement_part = \
                _D1_FOUNDATION_TABLE_NO_QUEUE \
                if d1_feeders["queue_piece"] is None \
                else _D1_FOUNDATION_TABLE
        elif d1_feeders["queue_piece"] is not None:
            d1_result.statement_part = _D1_FOUNDATION_UNUSABLE
        else:
            d1_result.statement_part = _D1_FOUNDATION_NONE
    q4_result = results_by_code["Q-4"]
    if q4_result.verdict == "present" and \
            not getattr(q4_result, "reconciled_against", None):
        q4_clause = "the sum test ran per step"
        q4_bound = q4_result.bound
        q4_single = None
        if q4_bound:
            q4_single = re.match(r"the Step (\d+) contribution",
                                 q4_bound[0])
        if q4_single:
            q4_step = int(q4_single.group(1))
            q4_traces, _q4_sources, _q4_styles = \
                _first_traces(captured)
            q4_landed = q4_traces[q4_step][0] \
                if q4_step in q4_traces else 0
            q4_clause += (
                " and Step %d stands excepted, its LANDED count "
                "of %d standing in both forms and no percentage "
                "printed for Step %d, with no record disagrees "
                "qualifier carried on this row on that ground"
                % (q4_step, q4_landed, q4_step))
        elif q4_bound:
            q4_clause += (
                " and the excepted contributions stand excepted, "
                "with no record disagrees qualifier carried on "
                "this row on that ground")
        q4_result.reconciled_against = q4_clause
    for result in results:
        if result.verdict == "present":
            if not getattr(result, "reconciled_against", None):
                result.reconciled_against = (
                    "the metric carries no total to reconcile "
                    "against")
        else:
            kind = _broken_link_kind(result)
            if kind and kind not in (result.reason_text() or ""):
                if result.broken_link:
                    result.broken_link = \
                        result.broken_link.rstrip() + \
                        " (" + kind + ")"
                elif result.follows is not None:
                    result.follows = result.follows.rstrip() + \
                        " (" + kind + ")"
    latest = captured.latest_timestamp
    latest_text = latest if latest else "none found in the capture"
    coverage = (
        "Coverage statement: step universe %d steps evidenced (%s); "
        "%d pieces recognised in the capture; 17 rows in starter "
        "set order"
        % (len(universe.evidenced), _each_step(universe.evidenced),
           len(captured.pieces)))
    if universe.disagreements:
        coverage += "; disagreements: " + "; ".join(
            universe.disagreements)
    contested_entry = _q3_contested_entry(captured, universe)
    if contested_entry is not None:
        restatement = _q3_restatement(captured)
        if restatement is not None:
            coverage += ("; restatement group: the named "
                         "correction in %s restates the step "
                         "universe statement, and the Q-3 register "
                         "entry governs" % restatement.paths[0])
        else:
            coverage += ("; Q-3 contested origin step: the "
                         "register entry origin Step %d stands "
                         "among the contested steps the record "
                         "statement disagrees over"
                         % contested_entry["origin"])
    if state_word == "halted":
        coverage += ("; build state: halted, named in the "
                     "recognised piece %s" % state_path)
    else:
        coverage += "; build state: in progress"
    for step in _missing_closing_steps(captured, universe):
        coverage += ("; the closing ruling for Step %d "
                     "(steps/step-%02d-gate-record.md) is a "
                     "missing piece, absent from the capture"
                     % (step, step))
    if captured.walk_note:
        coverage += "; walk note: " + captured.walk_note
    # The header lines in the line grammar order: root identity,
    # build identity under its full label, the captured read
    # statement, the three line universe proof, the coverage
    # statement, the partial marking, the open state line where
    # the build stands in progress, the live line from the latest
    # record timestamp in the capture and never a run time, the
    # reading moment line, the piece lines, and the version 2
    # trigger line where that state is found.
    partial_pieces = [piece for piece in captured.pieces
                      if _piece_not_read_in_full(piece)]
    uncovered_steps = _missing_closing_steps(captured, universe)
    smaller_sets = []
    for set_name, set_steps in (
            ("PATH-LEDGER.md", universe.ledger),
            (_metrics_record_name(captured), universe.metrics)):
        if set_steps and set(set_steps) != set(universe.evidenced) \
                and len(set_steps) < len(universe.evidenced):
            smaller_sets.append((set_name, set_steps))
    # The partial reading position, stated in the coverage
    # statement in the header and in the run cost line together:
    # the reading stands partial where the capture stands cut by
    # a limit or the walk bound, where any piece stands not read
    # in full, where a smaller evidenced set stands beside the
    # taken set, where a step in the taken set carries no closing
    # gate record, or where no step stands evidenced at all.
    is_partial = bool(partial_pieces or captured.tree_cut_paths
                      or captured.walk_note or smaller_sets
                      or uncovered_steps
                      or not universe.evidenced)
    header_lines = ["Root: " + str(captured.root),
                    "Build identity: "
                    + _build_identity_statement(captured),
                    "Captured read: the report derives from the "
                    "one captured read of the tree, taken in a "
                    "single walk"]
    if universe.evidenced:
        header_lines.append(
            "Coverage taken set: %s, %d steps evidenced by step "
            "records and gate files"
            % (_steps_phrase(universe.evidenced),
               len(universe.evidenced)))
    else:
        header_lines.append(
            "Coverage taken set: no steps evidenced in the "
            "capture")
    for set_name, set_steps in smaller_sets:
        header_lines.append(
            "Coverage smaller set: %s, stated in %s, which "
            "stops there" % (_steps_phrase(set_steps), set_name))
    if uncovered_steps:
        header_lines.append(
            "Coverage uncovered steps: %s, with no gate record "
            "standing in the capture"
            % _steps_phrase(uncovered_steps))
    else:
        header_lines.append(
            "Coverage uncovered steps: none, every step in the "
            "taken set carries a gate record in the capture")
    header_lines.append(coverage)
    if is_partial:
        header_lines.append("Coverage partial: partial report")
    else:
        header_lines.append("Coverage partial: full report")
    if state_word != "halted":
        if uncovered_steps:
            header_lines.append(
                "Coverage open state: the build stands in "
                "progress, with %s not yet closed"
                % _steps_phrase(uncovered_steps))
        else:
            header_lines.append(
                "Coverage open state: the build stands in "
                "progress, with no step standing unclosed in "
                "the capture")
    header_lines.append("Latest record timestamp: " + str(latest_text))
    gate_steps = [piece.step for piece in captured.pieces
                  if piece.record_class in GATE_CLASSES
                  and piece.step is not None]
    if gate_steps:
        last_closed = max(gate_steps)
        if state_word == "halted":
            header_lines.append(
                "Record state: the records evidence a closed "
                "build, the last closed step the records "
                "evidence is Step %d, whole build report at the "
                "coverage found" % last_closed)
        else:
            header_lines.append(
                "Record state: the records evidence a build in "
                "progress, the last closed step the records "
                "evidence is Step %d, whole build report at the "
                "coverage found" % last_closed)
    else:
        header_lines.append(
            "Record state: the records evidence a build in "
            "progress, no step stands closed in the records, "
            "whole build report at the coverage found")
    for piece in partial_pieces:
        reason = (piece.not_read_reason or "").strip()
        if not reason:
            reason = _quality_code(piece)
        header_lines.append(
            "Coverage piece not read in full: %s | %s | %d bytes | "
            "%s | %s"
            % (", ".join(piece.paths), piece.record_class,
               piece.size, _piece_state_word(piece), reason))
    if captured.tree_cut_paths:
        header_lines.append(
            "Coverage tree limit: pieces past the limit not read: "
            "%s; the %s was crossed; record part totals: %d bytes "
            "in %d files; tree byte limit %d bytes; tree file "
            "limit %d files"
            % (", ".join(captured.tree_cut_paths),
               captured.tree_cut_kind or "tree limit",
               captured.tree_bytes, captured.tree_files,
               captured.tree_byte_limit, captured.tree_file_limit))
    if captured.assembled_metrics and \
            "every step to close" in captured.assembled_metrics:
        header_lines.append(
            "Version 2 trigger state found: the metrics record "
            "covers every step to close.")
    inventory_lines = ["## Piece inventory"]
    for piece in captured.pieces:
        inventory_lines.append(
            "Piece %s | %s | %d bytes | %s"
            % (", ".join(piece.paths), piece.record_class,
               piece.size, _piece_state_word(piece)))
    for near in captured.near_matches:
        if isinstance(near, (tuple, list)) and len(near) >= 2:
            near_path, near_note = near[0], near[1]
        else:
            near_path, near_note = near, ""
        inventory_lines.append(
            "Unrecognised near match: %s, nearest closed pattern "
            "%s, not read" % (near_path, near_note))
    for cls in sorted(captured.inventory_totals):
        totals = captured.inventory_totals[cls]
        inventory_lines.append(
            "Inventory totals: %s expected %d found %d not found %d"
            % (cls, totals.get("expected", 0), totals.get("found", 0),
               totals.get("not_found", 0)))
    entries = _data_quality_entries(captured)
    entries.extend(seam_error for _seam_codes, seam_error
                   in seam_errors)
    t7_result = results_by_code.get("T-7")
    if t7_result is not None and \
            getattr(t7_result, "code_token", None) == "no code fits":
        entries.append(
            "T-7: What the record shows: the records for the loop "
            "rounds row do not map records to rounds by an outcome "
            "record, and List 3 holds no code naming the unmapped "
            "rounds case What follows: no code fits the case is "
            "recorded in the data quality section as a code list "
            "gap for T-7")
    # The data quality section in its Slice 7 form: the five
    # broken link kind count lines in kind order, with no total,
    # counted over the rows that stand present but not derivable;
    # the A7-5 datum line, in this section only, stating the
    # definitions version the report was read on as the capture
    # records it, or that the tree stated none; and the entries
    # themselves after them.
    kind_counts = {kind: 0 for kind in _KIND_ORDER}
    for result in results:
        if result.verdict == "present but not derivable":
            kind_counts[_broken_link_kind(result)] += 1
    dq_lines = ["%s: %d" % (kind, kind_counts[kind])
                for kind in _KIND_ORDER]
    if captured.definitions_version:
        dq_lines.append(
            "Datum line: the report was read on definitions "
            "version %s, on the settled forms of this version "
            "of the tool" % captured.definitions_version)
    else:
        dq_lines.append(
            "Datum line: the report was read on no stated "
            "definitions version, the tree stated none, on the "
            "settled forms of this version of the tool")
    dq_lines += entries
    entries = dq_lines
    # The run cost line, the second place the partial reading
    # position stands: its counters are the counts the one
    # CapturedRead itself carries, and its Reading part states
    # the same partial position the coverage statement states.
    files_opened = len([piece for piece in captured.pieces
                        if piece.text is not None])
    bytes_read = sum(piece.size for piece in captured.pieces
                     if piece.text is not None)
    crossed = []
    for piece in partial_pieces:
        detail = _reason_detail(piece)
        if "file limit" in detail and \
                "file limit 1000000 bytes" not in crossed:
            crossed.append("file limit 1000000 bytes")
        if "line limit" in detail and \
                "line limit 65536 bytes" not in crossed:
            crossed.append("line limit 65536 bytes")
    if captured.tree_cut_kind:
        crossed.append(captured.tree_cut_kind)
    # The whole walk bound stands in the Limit part only where
    # the walk note states the bound crossing itself, in its
    # reached form. A walk note stating only a directory listing
    # failure states no crossing, so it adds no bound wording
    # here: the Limit part then stands in its fallback form, and
    # the listing failure stands in the coverage statement and
    # in the Reading part, which stays partial on it.
    if captured.walk_note and \
            "whole walk bound" in captured.walk_note and \
            "was reached" in captured.walk_note:
        crossed.append("whole walk bound 10000 entries")
    run_cost_line = (
        "Run cost: Files visited: %d | Files opened: %d | Bytes "
        "read: %d | Entries visited: %d | Limit: %s | Reading: %s"
        % (captured.tree_files, files_opened, bytes_read,
           captured.tree_files + len(captured.near_matches),
           "; ".join(crossed) if crossed else "no limit crossed",
           "partial" if is_partial else "full"))
    model = ReportModel(header_lines=header_lines, coverage=coverage,
                        inventory_lines=inventory_lines,
                        results=results, data_quality=entries,
                        no_usable=not captured.pieces,
                        run_cost_line=run_cost_line)
    if not captured.pieces and captured.walk_note:
        # The floor form on a tree whose whole inventory holds
        # no recognisable piece and a walk note stands: the no
        # usable records statement names the note beside the
        # root read and the pieces looked for, in the D4R-08
        # floor form. The note stands as a walk crossing only
        # where the note states the bound crossing itself, in
        # its whole walk bound and was reached forms, as the
        # run cost line gate above states it. A note stating
        # only a directory listing failure states no crossing,
        # so it stands here as a walk note, in the words the
        # coverage statement uses, and its listing failure
        # sentence states the failure truly in that place.
        if "whole walk bound" in captured.walk_note and \
                "was reached" in captured.walk_note:
            floor_note_label = "walk crossing"
        else:
            floor_note_label = "walk note"
        model.no_usable_line = (
            "No usable records: the root read, %s, was looked "
            "through for the recognised record pieces, and none "
            "was found; %s: %s"
            % (captured.root, floor_note_label,
               captured.walk_note))
    disagreement_lines = _disagreement_lines(captured)
    if disagreement_lines:
        model.disagreements_lines = disagreement_lines
    model.record_cost_lines = _record_cost_lines(captured, universe)
    model.terms_lines = _terms_lines(results)
    return model


# Compatibility aliases for the capture seam the suite probes.
derive = derive_report
build_report = derive_report
derive_all = derive_report
