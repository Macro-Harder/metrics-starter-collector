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
    ordered = sorted(values)
    count = len(ordered)
    if count == 0:
        return None
    mid = count // 2
    if count % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


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


def _item_latency_hours(item):
    if not isinstance(item, dict):
        return None
    raised = item.get("raised_dt") or _stamp_value(item.get("raised"))
    ruled = item.get("ruled_dt") or _stamp_value(item.get("ruled"))
    if isinstance(raised, datetime) and isinstance(ruled, datetime):
        return (ruled - raised).total_seconds() / 3600.0
    return None


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


def _pointer(code, actual, captured=None):
    """Compose a pointer: the definition prose, then the record path."""
    prose = POINTER_PROSE.get(code, "")
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


def build_step_universe(captured):
    """Build the one StepUniverse from the one CapturedRead."""
    evidenced = set()
    for piece in captured.pieces:
        if piece.step is not None and \
                piece.record_class in _UNIVERSE_CLASSES:
            evidenced.add(piece.step)
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
                        tuple(disagreements), claim)


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
    stands outside a transition entry counts for nothing here.
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


def _t1_state(captured, universe):
    """Shared T-1 reading: (kind, complete, incomplete, ledger).

    Kind is one of no-ledger, not-read, no-entries, date-only,
    partial, or complete.
    """
    per_step, ledger = _transition_tokens(captured)
    if ledger is None:
        return "no-ledger", {}, [], ledger
    if ledger.text is None:
        return "not-read", {}, [], ledger
    if not per_step:
        return "no-entries", {}, [], ledger
    flat = [tok for toks in per_step.values() for tok in toks]
    if not any(isinstance(tok, datetime) for tok in flat):
        return "date-only", {}, [], ledger
    complete = {}
    for step, toks in per_step.items():
        if len(toks) >= 2 and isinstance(toks[0], datetime) and \
                isinstance(toks[1], datetime):
            hours = (toks[1] - toks[0]).total_seconds() / 3600.0
            complete[step] = hours
    wanted = list(universe.evidenced) or sorted(per_step)
    incomplete = [s for s in wanted if s not in complete]
    if incomplete:
        return "partial", complete, incomplete, ledger
    return "complete", complete, [], ledger


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
    if kind == "partial":
        covered = sorted(complete)
        return _refusal(
            "T-1", "present but not derivable",
            "intervals stand for " + _each_step(covered), denom,
            pointer,
            shows="the transition log yields a full timestamp "
                  "interval for %s and no full interval for %s"
                  % (_each_step(covered), _each_step(incomplete)),
            token="partial-span",
            follows="the series covers only part of the step "
                    "universe, so no build level figure stands",
            rule_name="T-1 mixed series rule")
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
    if kind in ("no-ledger", "no-entries"):
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
    if kind == "partial":
        return _refusal(
            "T-2", "present but not derivable",
            "durations stand for " + _each_step(sorted(complete)),
            denom, pointer,
            shows="a duration forms for %s and no duration forms "
                  "for %s" % (_each_step(sorted(complete)),
                              _each_step(incomplete)),
            token="partial-span",
            follows="the series covers only part of the step "
                    "universe, so no build level figure stands",
            rule_name="T-2 mixed series rule")
    figures = "; ".join(
        "Step %d duration %s hours" % (s, _fmt_num(complete[s]))
        for s in sorted(complete))
    return DerivationResult("T-2", "present", figures, denom, pointer,
                            rule_name="T-2 interval duration rule")


# ------------------------------------------------------------- T-4, T-7

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
        if m:
            durations.append((step, float(m.group(1))))
    if durations:
        figures = "; ".join(
            ("Step %d wait %s hours" % (s, _fmt_num(v)))
            if s is not None else ("wait %s hours" % _fmt_num(v))
            for s, v in durations)
        return DerivationResult("T-4", "present", figures, denom,
                                pointer, rule_name="T-4 banked rule")
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
        "T-4", "missing", "no banked duration figure", denom, pointer,
        shows="the path ledger holds no banked entry for any step",
        token="no-feeder-record",
        follows="no feeder record for the metric exists in the "
                "tree, so the row is missing",
        rule_name="T-4 feeder standing rule")


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


def _derive_t7(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    gates = captured.pieces_of(*GATE_CLASSES)
    pointer = gates[0].paths[0] if gates else "steps/step-01-gate-record.md"
    rounds = []
    for piece in captured.pieces:
        if piece.text is None:
            continue
        m = re.search(r"states\s+(\d+)\s+rounds for this step",
                      piece.text)
        if m and piece.step is not None:
            rounds.append((piece.step, int(m.group(1))))
    if rounds:
        figures = "; ".join("Step %d rounds %d" % (s, v)
                            for s, v in sorted(rounds))
        return DerivationResult("T-7", "present", figures, denom,
                                pointer, rule_name="T-7 rounds rule")
    if gates or captured.pieces_of(CLS_STEP_RECORD):
        held_parts = []
        loop_section = _metrics_section(
            captured.assembled_metrics or "", "## Loop round table")
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
            denom, _pointer("T-7", pointer, captured),
            shows="gate and step records stand and no record states "
                  "a round count in a form the row can count",
            token="missing-field",
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
        shows="no gate verdict record and no step record stands in "
              "the capture for this metric",
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


def _derive_e1(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    pointer = captured.first_path(
        CLS_STEP_RECORD, CLS_ROSTER, CLS_STEP_COMPANION) or \
        "steps/step-01-record.md"
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
    result = DerivationResult(
        "E-1", "present", figures, coverage,
        _pointer("E-1", pointer, captured),
        rule_name="E-1 staffing pair rule")
    result.coverage = coverage
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


def _derive_e2(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    pointer = captured.first_path(
        CLS_ROSTER, CLS_STEP_RECORD, CLS_STEP_COMPANION) or \
        "steps/step-01-roster.md"
    additions = {}
    totals = _total_spins(captured, universe)
    bases = {}
    for step in universe.evidenced:
        added = _step_field(
            captured, step, (r"additions over base:\s*(\d+)",),
            _STAFFING_CLASSES)
        if added is not None:
            additions[step] = added
        base = _step_field(captured, step, (r"\bBase:\s*(\d+)",),
                           _STAFFING_CLASSES)
        if base is not None:
            bases[step] = base
    for step, cells in _metrics_step_table(captured).items():
        if len(cells) >= 6 and step not in bases:
            m = re.match(r"(\d+)\s*/\s*(\d+)", cells[5])
            if m:
                bases[step] = int(m.group(2))
    for piece in captured.pieces_of(CLS_ROSTER):
        if piece.step is None or piece.step in additions:
            continue
        if not any("roster-artifact" in path for path in piece.paths):
            continue
        step = piece.step
        if step in totals and step in bases:
            additions[step] = totals[step] - bases[step]
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
        result = DerivationResult(
            "E-2", "present", figures, coverage,
            _pointer("E-2", pointer, captured),
            rule_name="E-2 split quantities rule")
        result.coverage = coverage
        return result
    if totals:
        return _refusal(
            "E-2", "present but not derivable",
            "no additions over base figure", denom,
            _pointer("E-2", pointer, captured),
            shows="total spins stand for %s and no roster additions "
                  "over base figure stands for any step"
                  % _each_step(sorted(totals)),
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

def _derive_e3(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
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
    if ledgers:
        return _refusal(
            "E-3", "present but not derivable", "no token figure",
            denom, pointer,
            shows="a cost ledger piece stands and it carries no "
                  "per step token figure",
            token="missing-field",
            follows="the token field the row requires does not "
                    "stand in the feeder record, so no figure stands",
            rule_name="E-3 token field rule")
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
    for piece in captured.pieces_of(CLS_STEP_RECORD, CLS_COST_LEDGER):
        if piece.text:
            texts.append(piece.text)
    if captured.assembled_metrics:
        texts.append(captured.assembled_metrics)
    joined = "\n".join(texts)
    return joined


def _derive_e4(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
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

def _derive_f2(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    gates = captured.pieces_of(*GATE_CLASSES)
    pointer = gates[0].paths[0] if gates else \
        "steps/step-01-gate-record.md"
    if not gates:
        return _refusal(
            "F-2", "missing", "no first ruling figure", denom,
            pointer,
            shows="no gate record, gate ruling or gate adjudication "
                  "stands in the capture for this metric",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="F-2 feeder standing rule")
    outcomes = 0
    for piece in gates:
        if piece.text and "First ruling outcome" in piece.text:
            outcomes += 1
    if outcomes == len([g for g in gates if g.text is not None]) and \
            outcomes:
        return DerivationResult(
            "F-2", "present",
            "first ruling outcomes recorded for %d steps" % outcomes,
            denom, pointer, rule_name="F-2 first ruling rule")
    held_clauses = []
    classes = {piece.record_class for piece in gates}
    if CLS_GATE_RECORD in classes and CLS_GATE_RULING in classes:
        held_clauses.append(
            "gate outcomes stand scattered across gate records and "
            "gate rulings under both names")
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
    if rate is not None and rate[2] is not None:
        held_clauses.append(
            "the only rate in the tree is provisional and partial "
            "at %s of %s in the Step %d snapshot" % rate)
    held_clauses.append("no rate is derived from final closing "
                        "states")
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
        broken="the first ruling outcome field recorded per step "
               "in one named place",
        required="a first ruling outcome recorded per step in one "
                 "named place, in the Auditor approval row form",
        held=_held_join(held_clauses))


def _derive_q1(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    papers = captured.pieces_of(CLS_AUDIT_PAPER, CLS_FIX_REGISTER)
    pointer = papers[0].paths[0] if papers else \
        "audit/step-01-audit-paper.md"
    if not papers:
        return _refusal(
            "Q-1", "missing", "no audit round figure", denom, pointer,
            shows="no audit round record stands in the capture for "
                  "this metric",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="Q-1 feeder standing rule")
    for piece in papers:
        if piece.text and "Post triage" in piece.text:
            return DerivationResult(
                "Q-1", "present",
                "post triage breakdown stands in the round record",
                denom, pointer, rule_name="Q-1 breakdown rule")
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
        denom, _pointer("Q-1", pointer, captured),
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


def _derive_q3(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    registers = captured.pieces_of(CLS_DEFECT_REGISTER, CLS_FIX_REGISTER)
    pointer = registers[0].paths[0] if registers else \
        "registers/defect-register.md"
    if not registers:
        return _refusal(
            "Q-3", "missing", "no register figure", denom, pointer,
            shows="no defect register and no fix register stands in "
                  "the capture for this metric",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="Q-3 feeder standing rule")
    entries = 0
    with_origin = 0
    for piece in registers:
        if piece.text is None:
            continue
        found = re.findall(r"Entry[^:\n]*:", piece.text)
        entries += len(found) or 1
        with_origin += len(re.findall(r"Origin step", piece.text))
    if entries and with_origin >= entries:
        return DerivationResult(
            "Q-3", "present",
            "register entries with an origin step: %d" % with_origin,
            denom, pointer, rule_name="Q-3 origin step rule")
    table = _metrics_step_table(captured)
    printed_zero = "printed zero" in (
        captured.assembled_metrics or "").lower() or any(
        len(cells) >= 13 and cells[12].startswith("0")
        for cells in table.values())
    held = "the field is absent from every fix and defect register entry"
    if printed_zero:
        held += (", and the printed zero in the metrics record "
                 "step table carries no measurement basis and "
                 "stands nowhere as a measured figure")
    return _refusal(
        "Q-3", "present but not derivable", "no register figure",
        denom, _pointer("Q-3", pointer, captured),
        shows="register entries stand and the entries carry no "
              "origin step field",
        token="missing-field",
        follows="the origin step field the row requires does not "
                "stand on the entries, so no figure stands",
        rule_name="Q-3 origin step field rule",
        broken="the origin step field on fix and defect register "
               "entries",
        required="an origin step field on each register entry, "
                 "judged at triage, stating the step the defect "
                 "was introduced in or escaped from",
        held=held)


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

    def add(step, parsed, style, piece, rank):
        if step is None or parsed is None:
            return
        key = (rank, 1 if "round" in piece.paths[0] else 0,
               piece.paths[0])
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
                "purple" not in piece.paths[0].lower():
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
    result = DerivationResult(
        "Q-4", "present", figures, coverage,
        _pointer("Q-4", pointer, captured),
        rule_name="Q-4 first trace rule")
    result.coverage = coverage
    result.bound = bound
    return result


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


def _derive_d1(captured, universe):
    denom = "denominator decision items in the governing record"
    pointer = METRICS_CANONICAL_PATH
    queue_pieces = captured.pieces_of(CLS_DECISION_QUEUE)
    items = []
    feeder_name = "metrics record decision table"
    if queue_pieces and queue_pieces[0].text is not None:
        queue_items = _table_items(queue_pieces[0].text)
        if queue_items:
            items = queue_items
            feeder_name = "decision queue file"
            pointer = queue_pieces[0].paths[0]
    if not items:
        section = _metrics_section(
            captured.assembled_metrics or "", "## Decision table")
        items = _table_items(section if section
                             else captured.assembled_metrics)
    if not items:
        return _refusal(
            "D-1", "missing", "no decision latency figure", denom,
            pointer,
            shows="no decision table item stands in the governing "
                  "record and no queue file in the named form "
                  "stands in the capture",
            token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="D-1 feeder standing rule")
    latencies = []
    for item in items:
        value = _item_latency_hours(item)
        if value is not None:
            latencies.append(value)
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
            broken="the presented and ruled timestamp fields on "
                   "the decision table items",
            required="raised and ruled timestamps that can form a "
                     "duration on an item, with the median and the "
                     "longest formed over the items that produce a "
                     "latency",
            held=held)
    median = _median(latencies)
    figures = "median %s hours over %d items" % (
        _fmt_num(median), len(latencies))
    result = DerivationResult("D-1", "present", figures, denom,
                              pointer, rule_name="D-1 median rule")
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


def _derive_b1(captured, universe, t1_result):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    pointer = "PATH-LEDGER.md"
    ledger = _ledger_piece(captured)
    if ledger is not None:
        pointer = ledger.paths[0]
    if _basis_split(captured):
        return _refusal(
            "B-1", "present but not derivable", "no B-1 figure",
            denom, _pointer("B-1", pointer, captured),
            shows="the timestamps feeding this row stand on split "
                  "time bases: one transition timestamp states its "
                  "basis in words and a gate record timestamp "
                  "states no basis for its time of day",
            token="no code fits",
            follows="the shared time basis the row requires does "
                    "not stand across its feeder timestamps, so no "
                    "figure is derived",
            rule_name="B-1 shared time basis rule")
    if t1_result.verdict == "missing":
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
    return _refusal(
        "B-1", "present but not derivable", "no B-1 figure", denom,
        pointer,
        shows="the T-1 series stands in the tracer form and the "
              "ranking the row states is not formed in this form",
        token="partial-span",
        follows="the row stands refused in the tracer form, with "
                "its ranking inputs named on the T-1 and T-2 rows",
        rule_name="B-1 tracer refusal rule")


def _derive_b_ranking(captured, universe, t1_result, code):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    pointer = "PATH-LEDGER.md"
    ledger = _ledger_piece(captured)
    if ledger is not None:
        pointer = ledger.paths[0]
    label = "slowest ranking" if code == "B-3" else "fastest ranking"
    if t1_result.verdict == "missing":
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
    return _refusal(
        code, "present but not derivable", "no ranking figure",
        denom, pointer,
        shows="the T-1 series stands in the tracer form and the "
              "%s the row states is not formed in this form" % label,
        token="partial-span",
        follows="the row stands refused in the tracer form, with "
                "its ranking inputs named on the T-1 and T-2 rows",
        rule_name=code + " tracer refusal rule")


def _derive_b2(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    ledgers = captured.pieces_of(CLS_COST_LEDGER)
    pointer = ledgers[0].paths[0] if ledgers else COST_LEDGER_PATH
    joined = _money_mentions(captured)
    if ledgers:
        return _refusal(
            "B-2", "present but not derivable", "no budget share "
            "figure", denom, pointer,
            shows="a cost ledger piece stands and the budget "
                  "figures the row forms its shares from do not "
                  "stand in a measured form",
            token="no-measurement-basis",
            follows="a share formed from figures with no "
                    "measurement basis does not stand, so no figure "
                    "stands",
            rule_name="B-2 measurement basis rule")
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


def derive_report(captured):
    """Derive the one ReportModel from the one CapturedRead.

    The StepUniverse the derivations read is the one construction
    in this module, build_step_universe, built from this same
    capture. No second construction stands anywhere else.
    """
    universe = build_step_universe(captured)
    t1 = _derive_t1(captured, universe)
    results_by_code = {
        "T-1": t1,
        "T-2": _derive_t2(captured, universe),
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
        "B-1": _derive_b1(captured, universe, t1),
        "B-2": _derive_b2(captured, universe),
        "B-3": _derive_b_ranking(captured, universe, t1, "B-3"),
        "B-4": _derive_b_ranking(captured, universe, t1, "B-4"),
    }
    results = [results_by_code[code] for code in STARTER_ORDER]
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
    if captured.walk_note:
        coverage += "; walk note: " + captured.walk_note
    header_lines = ["# Metrics starter set report",
                    "Root: " + str(captured.root)]
    if captured.build_identity:
        header_lines.append("Build: " + str(captured.build_identity))
    header_lines.append("Latest record timestamp: " + str(latest_text))
    header_lines.append(coverage)
    # The partial reading position, stated in the coverage
    # statement in the header: the reading stands partial where
    # the capture stands cut by a limit or the walk bound, or
    # where any piece stands not read in full, and every such
    # piece is named here with its state and its capture reason.
    partial_pieces = [piece for piece in captured.pieces
                      if _piece_not_read_in_full(piece)]
    is_partial = bool(partial_pieces or captured.tree_cut_paths
                      or captured.walk_note)
    if is_partial:
        header_lines.append("Coverage partial: partial report")
    else:
        header_lines.append("Coverage partial: full report")
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
    if not entries:
        entries = ["No data quality entries: every piece in the "
                   "capture was read in full."]
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
    if captured.walk_note:
        crossed.append("whole walk bound 10000 entries")
    run_cost_line = (
        "Run cost: Files visited: %d | Files opened: %d | Bytes "
        "read: %d | Entries visited: %d | Limit: %s | Reading: %s"
        % (captured.tree_files, files_opened, bytes_read,
           captured.tree_files + len(captured.near_matches),
           "; ".join(crossed) if crossed else "no limit crossed",
           "partial" if is_partial else "full"))
    return ReportModel(header_lines=header_lines, coverage=coverage,
                       inventory_lines=inventory_lines, results=results,
                       data_quality=entries,
                       no_usable=not captured.pieces,
                       run_cost_line=run_cost_line)


# Compatibility aliases for the capture seam the suite probes.
derive = derive_report
build_report = derive_report
derive_all = derive_report
