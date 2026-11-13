"""Module 3: derivation core.

Pure component. Receives one CapturedRead and returns one ReportModel.
Never touches the filesystem, never reads a clock, never uses randomness.
The five core types live here: CapturedRead, Piece, StepUniverse,
DerivationResult and ReportModel.
"""
import re
from dataclasses import dataclass, field
from datetime import datetime

STARTER_ORDER = ["T-1", "T-2", "T-4", "T-7", "E-1", "E-2", "E-3", "E-4",
                 "F-2", "Q-1", "Q-3", "Q-4", "D-1", "B-1", "B-2", "B-3", "B-4"]

REASON_CODES = ["missing-field", "no-feeder-record", "date-only-form",
                "no-post-triage-breakdown", "no-measurement-basis",
                "truncated-no-correcting-record", "record-disagrees",
                "unreconciled-figure", "unknown-definitions-version",
                "no-named-rule", "partial-span", "governing-scale-conflict",
                "over-limit-piece", "malformed-piece", "unreadable-piece"]

QUALITY_STATES = ("truncated", "malformed", "over limit", "unreadable")

# Record class names, one home. Inventory imports these.
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

    def reason_text(self):
        if self.shows is None:
            return None
        follows = self.follows
        if follows.lower().startswith(self.code_token.lower()):
            follows = follows[len(self.code_token):].lstrip()
        return ("What the record shows: " + self.shows +
                " What follows: " + self.code_token + " " + follows)


@dataclass
class ReportModel:
    header_lines: list
    coverage: str
    inventory_lines: list
    results: list
    data_quality: list
    no_usable: bool = False


# ---------------------------------------------------------------- helpers

FULL_TS_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})")
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")


def _parse_ts(text):
    m = FULL_TS_RE.search(text)
    if not m:
        return None
    try:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                        int(m.group(4)), int(m.group(5)))
    except ValueError:
        return None


def _fmt_num(value):
    if value == int(value):
        return str(int(value))
    return ("%.2f" % value).rstrip("0").rstrip(".")


def _step_list_text(steps):
    steps = sorted(steps)
    if not steps:
        return "none"
    parts = []
    run = [steps[0]]
    for s in steps[1:]:
        if s == run[-1] + 1:
            run.append(s)
        else:
            parts.append(_run_text(run))
            run = [s]
    parts.append(_run_text(run))
    return ", ".join(parts)


def _run_text(run):
    if len(run) == 1:
        return "Step %d" % run[0]
    if len(run) == 2:
        return "Step %d and Step %d" % (run[0], run[1])
    return "Steps %d to %d" % (run[0], run[-1])


def _named_steps(steps):
    steps = sorted(steps)
    if not steps:
        return "none"
    if len(steps) == 1:
        return "Step %d" % steps[0]
    return "Steps " + ", ".join(str(s) for s in steps)


def _each_step(steps):
    """Name every step in the Step N form, one name per step."""
    steps = sorted(steps)
    if not steps:
        return "none"
    return ", ".join("Step %d" % s for s in steps)


def _join_names(names):
    names = list(names)
    if not names:
        return "none"
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return names[0] + " and " + names[1]
    return ", ".join(names[:-1]) + " and " + names[-1]


def build_step_universe(captured):
    evidenced = set()
    for p in captured.pieces:
        if p.step is not None and p.record_class in (
                CLS_STEP_RECORD, CLS_GATE_RECORD, CLS_GATE_RULING,
                CLS_REGATE_RECORD, CLS_GATE_ADJUDICATION):
            evidenced.add(p.step)
    ledger_steps = set()
    for p, text in captured.texts_of(CLS_PATH_LEDGER):
        m = re.search(r"Steps stated:\s*([0-9, ]+)", text)
        if m:
            for tok in m.group(1).split(","):
                tok = tok.strip()
                if tok.isdigit():
                    ledger_steps.add(int(tok))
        for m in re.finditer(r"Step (\d+)\b", text):
            ledger_steps.add(int(m.group(1)))
    metrics_steps = set()
    if captured.assembled_metrics:
        for m in re.finditer(r"^\|\s*(\d+)\.\s", captured.assembled_metrics,
                             re.M):
            metrics_steps.add(int(m.group(1)))
        for m in re.finditer(r"Step (\d+) closing entry", captured.assembled_metrics):
            metrics_steps.add(int(m.group(1)))
    metrics_count_claim = None
    if captured.assembled_metrics:
        m = re.search(r"step universe as (\d+) steps?",
                      captured.assembled_metrics, re.I)
        if m:
            metrics_count_claim = int(m.group(1))
    disagreements = []
    if ledger_steps and ledger_steps != evidenced:
        disagreements.append(
            "the path ledger states steps %s while step records and gate "
            "files evidence steps %s" % (_named_steps(ledger_steps),
                                         _named_steps(evidenced)))
    if metrics_steps and not metrics_steps.issubset(evidenced | ledger_steps):
        disagreements.append(
            "the metrics record states steps %s beyond the evidenced "
            "universe" % _named_steps(metrics_steps - evidenced - ledger_steps))
    if metrics_count_claim is not None and \
            metrics_count_claim != len(evidenced):
        metrics_name = "build-metrics-record.md"
        if captured.metrics_single_path:
            metrics_name = captured.metrics_single_path.rsplit("/", 1)[-1]
        ledger_clause = ""
        if captured.pieces_of(CLS_PATH_LEDGER):
            ledger_clause = " and stated in PATH-LEDGER.md"
        disagreements.append(
            "the metrics record in %s states the step universe as %d "
            "steps, which disagrees with the step universe of %d steps "
            "evidenced by step records and gate files%s; neither count "
            "is picked as the count, and derivations and denominators "
            "are computed on the evidenced universe"
            % (metrics_name, metrics_count_claim, len(evidenced),
               ledger_clause))
    return StepUniverse(tuple(sorted(evidenced)), tuple(sorted(ledger_steps)),
                        tuple(sorted(metrics_steps)), tuple(disagreements),
                        metrics_count_claim)


def _known_version(version):
    if version is None:
        return True
    return ("SHA-256" in version and "bytes" in version and
            re.search(r"[0-9a-fA-F]{64}", version) is not None)


def _feeder_stands(captured, code):
    kinds = FEEDER_MAP[code]
    for kind in kinds:
        if kind == "path ledger transition log" or kind == "path ledger banked states":
            if captured.pieces_of(CLS_PATH_LEDGER):
                return True
        elif kind == "decision queue file":
            if captured.pieces_of(CLS_DECISION_QUEUE):
                return True
        elif kind == "gate verdict records" or kind == "gate records":
            if captured.pieces_of(*GATE_CLASSES):
                return True
        elif kind == "gate rulings":
            if captured.pieces_of(CLS_GATE_RULING):
                return True
        elif kind == "gate adjudications":
            if captured.pieces_of(CLS_GATE_ADJUDICATION, CLS_ADJUDICATION):
                return True
        elif kind == "step records":
            if captured.pieces_of(CLS_STEP_RECORD):
                return True
        elif kind == "roster artifacts":
            if captured.pieces_of(CLS_ROSTER):
                return True
        elif kind == "cost ledger token figures" or kind == "cost ledger money figures":
            if captured.pieces_of(CLS_COST_LEDGER):
                return True
        elif kind == "audit round records" or kind == "audit records":
            if captured.pieces_of(CLS_AUDIT_PAPER, CLS_FIX_REGISTER):
                return True
        elif kind == "defect registers":
            if captured.pieces_of(CLS_DEFECT_REGISTER, CLS_FIX_REGISTER):
                return True
        elif kind == "first trace records":
            if captured.pieces_of(CLS_TRACE):
                return True
        elif kind == "metrics record":
            if captured.assembled_metrics is not None:
                return True
    return False


# ------------------------------------------------------------- T-1 and T-2

def _ledger_piece(captured):
    """The single ledger piece the ledger feeders read.

    Selection only: where a ledger piece carrying substantive text
    stands in the identity group, that piece feeds the derivations,
    even where a piece with no content at the canonical path sorts
    ahead of its path, as the step record and metrics record
    selections already feed from the sound duplicate on the same
    shapes. Where no piece in the group carries substantive text,
    the first piece in path order stands, so the standing not read
    in full and empty forms hold unchanged.
    """
    found = captured.pieces_of(CLS_PATH_LEDGER)
    for piece in found:
        if piece.text is not None and piece.text.strip():
            return piece
    return found[0] if found else None


def _step_intervals(captured):
    """Per step intervals from transition lines carrying two full stamps."""
    intervals = {}
    ledger = _ledger_piece(captured)
    if ledger is None or ledger.text is None:
        return intervals
    for line in ledger.text.splitlines():
        if "Step" not in line:
            continue
        m = re.search(r"Step (\d+)\b", line)
        if not m:
            continue
        stamps = FULL_TS_RE.findall(line)
        if len(stamps) >= 2:
            times = [datetime(int(a), int(b), int(c), int(d), int(e))
                     for (a, b, c, d, e) in stamps]
            hours = (times[1] - times[0]).total_seconds() / 3600.0
            intervals.setdefault(int(m.group(1)), hours)
    return intervals


def _ledger_has_full_ts(captured):
    ledger = _ledger_piece(captured)
    if ledger is None or ledger.text is None:
        return False
    for line in ledger.text.splitlines():
        if "Step" in line and FULL_TS_RE.search(line):
            return True
    return False


def _ledger_has_dates(captured):
    ledger = _ledger_piece(captured)
    if ledger is None or ledger.text is None:
        return False
    return DATE_RE.search(ledger.text) is not None


def _derive_t1(captured, universe):
    ledger = _ledger_piece(captured)
    pointer = ledger.paths[0] if ledger else "PATH-LEDGER.md"
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    if ledger is None:
        return DerivationResult(
            "T-1", "missing", "no interval figure", denom, pointer,
            shows="no path ledger piece stands in the capture, so no "
                  "transition log holds any timestamp field",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing",
            rule_name="T-1 feeder standing rule")
    if ledger.text is None:
        code = {"malformed": "malformed-piece",
                "over limit": "over-limit-piece"}.get(
                    ledger.quality_state or "", "unreadable-piece")
        return DerivationResult(
            "T-1", "present but not derivable", "no interval figure",
            denom, pointer,
            shows="a path ledger piece is present but not read in "
                  "full in the capture, so no transition log can be "
                  "read to form an interval",
            code_token=code,
            follows=code + " the piece is marked not read in full in "
                    "the inventory and no figure is read from it, so "
                    "no interval figure stands",
            rule_name="T-1 not read in full rule")
    intervals = _step_intervals(captured)
    if not _ledger_has_full_ts(captured):
        if _ledger_has_dates(captured):
            recorded = re.findall(r"Recorded (\d{4}-\d{2}-\d{2})",
                                  ledger.text)
            entry_steps = [int(m.group(1)) for m in re.finditer(
                r"^- Step (\d+)\b", ledger.text, re.M)]
            if recorded and len(set(recorded)) == 1 and \
                    "IN PROGRESS" not in ledger.text:
                if entry_steps:
                    denom += ("; transitions cover Steps %d to %d only"
                              % (min(entry_steps), max(entry_steps)))
                return DerivationResult(
                    "T-1", "missing", "no interval figure", denom, pointer,
                    shows="the transition log holds %d entries marked "
                          "Recorded %s, every one date only %s, no time "
                          "of day, no IN PROGRESS entry"
                          % (len(recorded), recorded[0][:4], recorded[0]),
                    code_token="date-only-form",
                    follows="date-only-form no timestamp with a time of "
                            "day can form an interval, so the metric is "
                            "missing on the date only ground",
                    rule_name="T-1 date only boundary rule")
            return DerivationResult(
                "T-1", "missing", "no interval figure", denom, pointer,
                shows="the transition log in PATH-LEDGER.md holds timestamp "
                      "fields in date only form, and no entry carries a "
                      "time of day from which an interval can form",
                code_token="date-only-form",
                follows="date-only-form the metric specific boundary makes "
                        "the row missing where no timestamp with a time of "
                        "day stands",
                rule_name="T-1 date only boundary rule")
        return DerivationResult(
            "T-1", "missing", "no interval figure", denom, pointer,
            shows="the transition log in PATH-LEDGER.md holds no timestamp "
                  "field for any step",
            code_token="no-feeder-record",
            follows="no interval can form from the log as it stands, so "
                    "the row is missing",
            rule_name="T-1 feeder standing rule")
    covered = sorted(intervals)
    uncovered = [s for s in universe.evidenced if s not in intervals]
    if uncovered:
        return DerivationResult(
            "T-1", "present but not derivable",
            "intervals stand for " + _each_step(covered), denom, pointer,
            shows="the transition log yields a full timestamp interval "
                  "for %s and no interval for %s"
                  % (_each_step(covered), _each_step(uncovered)),
            code_token="partial-span",
            follows="partial-span the series covers only part of the step "
                    "universe, so no build level figure stands",
            rule_name="T-1 mixed series rule")
    figures = "; ".join("Step %d elapsed %s hours" % (s, _fmt_num(intervals[s]))
                        for s in covered)
    return DerivationResult("T-1", "present", figures, denom, pointer,
                            rule_name="T-1 interval rule")


# Negation, denial and retraction markers for the duration tests.
# A marker in the clause fragment before a mention, or in the
# fragment after it up to the end of its sentence, takes that
# mention out where the marker stands inside the mention's own
# clause scope: the mention is denied in any auxiliary form (was not,
# has not been, was never, does not), after a comma, after
# intervening words, or as a contraction, or it is denied by another
# verb or word (cannot, absent, without, fails to record, refuses to
# record, unrecorded, missing, omitted, denied, removed, nowhere,
# none recorded), quoted and retracted, or only discussed or named
# as a heading. A comma or a colon opens a new clause part: a marker
# in another part takes the mention out only where that part is not
# scoped to another subject, carrying no duration mention of its
# own and naming neither a different step nor a different figure.
# A mention retracted by name in the following sentence on the same
# line does not stand. A neighbouring line that denies any duration
# stands takes out a mention that carries no value of its own. The
# marker sets cover these proven shapes; an unlisted synonym
# remains outside the handling, a known boundary of the cure.
_BEFORE_NEGATION_RE = re.compile(
    r"\b(?:no|not|never|without|cannot|unrecorded|missing|omitted|"
    r"denied|removed|nowhere|none)\b|\b\w+n't\b|"
    r"\bfails?\s+to\b|\bfailed\s+to\b|\brefus(?:e|es|ed)\s+to\b",
    re.I)
_AFTER_NEGATION_RE = re.compile(
    r"\b(?:not|never|no|cannot|absent|withdrawn|retracted|"
    r"unrecorded|missing|omitted|denied|removed|nowhere|none)\b|"
    r"\b\w+n't\b|\bwas\s+wrong\b|\bis\s+wrong\b", re.I)
_RETRACTION_RE = re.compile(
    r"\b(?:withdrawn|retracted)\b|\bwas\s+wrong\b|\bis\s+wrong\b",
    re.I)
_RETRACTION_REF_RE = re.compile(
    r"\bthat\s+(?:claim|note|statement)\b", re.I)
_SENTENCE_END_RE = re.compile(r"[.;]\"?(?:\s|$)")
_NON_ASSERTIVE_RE = re.compile(
    r"\bis\s+discussed\b|\bheading\s+only\b|\bsee\s+the\s+note\b|"
    r"\bsee\s+above\b", re.I)
_NEIGHBOUR_DENIAL_RE = re.compile(
    r"\bno\s+(?:such\s+)?(?:interval\s+)?duration\b|"
    r"\bduration\s+(?:is|was)\s+not\s+recorded\b", re.I)


def _clause_fragments(line, start, end):
    """The clause fragments around a mention in one line.

    The before fragment runs from the last sentence or clause break
    before the mention; the after fragment runs to the end of the
    mention's own sentence.
    """
    before_all = line[:start]
    cut = max(before_all.rfind("."), before_all.rfind(";"))
    before = before_all[cut + 1:]
    after_all = line[end:]
    stops = [i for i in (after_all.find("."), after_all.find(";"))
             if i >= 0]
    after = after_all[:min(stops)] if stops else after_all
    return before, after


def _after_is_negated(after):
    cleaned = re.sub(r"\bnot\s+only\b", "", after, flags=re.I)
    return _AFTER_NEGATION_RE.search(cleaned) is not None


def _clause_subject(text):
    """The step and the hours figure a clause part names."""
    step = re.search(r"Step (\d+)\b", text)
    figure = re.search(r"(\d+(?:\.\d+)?)\s*hours", text, re.I)
    return (int(step.group(1)) if step else None,
            float(figure.group(1)) if figure else None)


def _subclause_scoped_elsewhere(part, mention_step, mention_figure):
    """Whether a clause part is scoped to another subject.

    A part carrying its own duration mention, or naming a
    different step or a different hours figure than the mention
    under test, belongs to that other subject, so a denial marker
    inside it does not reach the mention under test.
    """
    if re.search(r"interval duration", part, re.I) or \
            re.search(r"\bBANKED\b", part, re.I):
        return True
    step, figure = _clause_subject(part)
    if mention_step is not None and step is not None and \
            step != mention_step:
        return True
    if mention_figure is not None and figure is not None and \
            figure != mention_figure:
        return True
    return False


def _mention_subject(before, after, mention):
    """The step and figure of the clause the mention stands in.

    The clause is the part after the last comma or colon before
    the mention, the mention itself, and the part before the
    first comma or colon after it.
    """
    before_parts = re.split(r"[,:]", before)
    after_parts = re.split(r"[,:]", after)
    own = (before_parts[-1] if before_parts else "") + " " + \
        mention + " " + (after_parts[0] if after_parts else "")
    return _clause_subject(own)


def _before_negated_in_scope(before, after, mention):
    """Whether a marker before a mention takes the mention out.

    A marker in the mention's own clause part counts. A marker in
    an earlier comma or colon part counts only where that part is
    not scoped to another subject.
    """
    parts = re.split(r"[,:]", before)
    step, figure = _mention_subject(before, after, mention)
    for idx, part in enumerate(parts):
        if _BEFORE_NEGATION_RE.search(part) is None:
            continue
        if idx == len(parts) - 1:
            return True
        if not _subclause_scoped_elsewhere(part, step, figure):
            return True
    return False


def _after_negated_in_scope(after, before, mention):
    """The after side of _before_negated_in_scope, on the same scope.

    A marker in the mention's own clause part counts. A marker in
    a later comma or colon part counts only where that part is
    not scoped to another subject.
    """
    parts = re.split(r"[,:]", after)
    step, figure = _mention_subject(before, after, mention)
    for idx, part in enumerate(parts):
        if not _after_is_negated(part):
            continue
        if idx == 0:
            return True
        if not _subclause_scoped_elsewhere(part, step, figure):
            return True
    return False


def _retracted_in_following_sentence(line, end):
    """Whether the next sentence on the line retracts the mention.

    The following sentence must name the claim it takes back
    (that claim, that note or that statement) and carry a
    retraction marker, so an unrelated following sentence never
    takes a standing mention out.
    """
    rest = line[end:]
    match = _SENTENCE_END_RE.search(rest)
    if match is None:
        return False
    following = rest[match.end():]
    match = _SENTENCE_END_RE.search(following)
    if match is not None:
        following = following[:match.start()]
    return _RETRACTION_REF_RE.search(following) is not None and \
        _RETRACTION_RE.search(following) is not None


def _neighbouring_denial(lines, idx):
    for other in (idx - 1, idx + 1):
        if 0 <= other < len(lines) and \
                _NEIGHBOUR_DENIAL_RE.search(lines[other]):
            return True
    return False


def _interval_duration_mentions_stand(text):
    """Whether an interval duration stands in a text.

    A mention inside a negated, denied or retracted statement does
    not stand, in any of the shapes the markers above cover. Any
    other mention stands.
    """
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        for m in re.finditer(r"interval duration", line, re.I):
            before, after = _clause_fragments(line, m.start(),
                                              m.end())
            if _before_negated_in_scope(before, after, m.group(0)):
                continue
            if _after_negated_in_scope(after, before, m.group(0)):
                continue
            if _NON_ASSERTIVE_RE.search(after):
                continue
            if _retracted_in_following_sentence(line, m.end()):
                continue
            valued = re.search(r"\d", before + after) is not None \
                or "banked" in before.lower()
            if not valued and _neighbouring_denial(lines, idx):
                continue
            return True
    return False


def _banked_duration_stands(text):
    """Whether a BANKED line carrying a number stands as a duration.

    The BANKED alternative takes the same negation handling as the
    interval duration path: a BANKED mention denied in its own
    clause scope, before it or after it, stands as no duration.
    """
    for line in text.splitlines():
        for m in re.finditer(r"BANKED", line):
            before, after = _clause_fragments(line, m.start(),
                                              m.end())
            if re.search(r"\d", after) is None:
                continue
            if _before_negated_in_scope(before, after, m.group(0)):
                continue
            if _after_negated_in_scope(after, before, m.group(0)):
                continue
            if _retracted_in_following_sentence(line, m.end()):
                continue
            return True
    return False


def _t2_duration_stands(text):
    """The T-2 duration test over a transition log text."""
    return _interval_duration_mentions_stand(text) or \
        _banked_duration_stands(text)


def _derive_t2(captured, universe, t1):
    ledger = _ledger_piece(captured)
    pointer = ledger.paths[0] if ledger else "PATH-LEDGER.md"
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    if ledger is not None and ledger.text is None:
        code = t1.code_token or "unreadable-piece"
        return DerivationResult(
            "T-2", "present but not derivable", "no interval figure",
            denom, pointer,
            shows="a path ledger piece is present but not read in "
                  "full in the capture, so no transition log can be "
                  "read to carry an active figure",
            code_token=code,
            follows=code + " the piece is marked not read in full in "
                    "the inventory and no figure is read from it, so "
                    "no active figure stands",
            rule_name="T-2 not read in full rule")
    if t1.verdict == "missing" and t1.code_token == "date-only-form":
        has_duration = False
        if ledger is not None and ledger.text is not None:
            has_duration = _t2_duration_stands(ledger.text)
        if not has_duration:
            return DerivationResult(
                "T-2", "missing", "no interval figure", denom, pointer,
                shows="no BANKED, SUSPENDED or halt interval duration "
                      "stands in the transition log and T-1 is missing "
                      "on the date only ground",
                code_token="date-only-form",
                follows="date-only-form T-2 is missing where T-1 is "
                        "missing on that ground and no interval duration "
                        "stands",
                rule_name="T-2 date only boundary rule")
    if t1.verdict == "present but not derivable":
        intervals = _step_intervals(captured)
        covered = sorted(intervals)
        uncovered = [s for s in universe.evidenced if s not in intervals]
        return DerivationResult(
            "T-2", "present but not derivable", "no figure stands", denom,
            pointer,
            shows="the elapsed series stands incomplete, with an "
                  "interval for %s and no interval for %s, so the "
                  "active series that rests on it stands incomplete in "
                  "the same places"
                  % (_each_step(covered), _each_step(uncovered)),
            code_token=t1.code_token or "missing-field",
            follows=(t1.code_token or "missing-field") +
                    " the active figure rests on the elapsed series, so "
                    "no active figure stands",
            rule_name="T-2 mixed series rule")
    if t1.verdict == "missing":
        has_duration = False
        if ledger is not None and ledger.text is not None:
            has_duration = _t2_duration_stands(ledger.text)
        if has_duration:
            shows = ("the elapsed row is missing, and an interval "
                     "duration stands in the transition log, but no "
                     "active figure can carry from a missing elapsed "
                     "row")
        else:
            shows = ("the elapsed row is missing, and no interval "
                     "duration stands in the transition log to carry "
                     "an active figure")
        return DerivationResult(
            "T-2", "missing", "no interval figure", denom, pointer,
            shows=shows,
            code_token="no-feeder-record",
            follows="no feeder record yields an active figure, so the "
                    "row is missing",
            rule_name="T-2 feeder standing rule")
    intervals = _step_intervals(captured)
    figures = "; ".join("Step %d active %s hours" % (s, _fmt_num(intervals[s]))
                        for s in sorted(intervals))
    return DerivationResult("T-2", "present", figures, denom, pointer,
                            rule_name="T-2 interval rule")


def _t4_banked_durations(captured):
    """Banked durations in the ledger, as (step, hours, interval form).

    A BANKED mention denied in its own clause feeds no duration,
    under the same negation handling the T-2 BANKED alternative
    takes in _banked_duration_stands. Each figure is attributed
    to the step its own clause names, under the clause scope the
    duration helpers already use: the step named inside the
    mention's own clause part governs, never a step named in
    another clause of the same line. A figure whose own clause
    names no step keeps the line's first Step token, the standing
    attribution, because that token is the only step the line
    names for it.
    """
    found = []
    ledger = _ledger_piece(captured)
    if ledger is None or ledger.text is None:
        return found

    def _banked_mention_denied(line, start):
        # The T-2 BANKED alternative's negation handling, shared:
        # a BANKED mention denied in its own clause scope, by a
        # marker in the clause fragment before it or in the
        # fragment after it, or retracted in the following
        # sentence on the line, stands as no duration.
        before, after = _clause_fragments(
            line, start, start + len("BANKED"))
        return _before_negated_in_scope(before, after, "BANKED") or \
            _after_negated_in_scope(after, before, "BANKED") or \
            _retracted_in_following_sentence(
                line, start + len("BANKED"))

    def _mention_step(line, match, line_step):
        before, after = _clause_fragments(
            line, match.start(), match.end())
        step, _figure = _mention_subject(
            before, after, match.group(0))
        if step is not None:
            return step
        return line_step

    for line in ledger.text.splitlines():
        step_match = re.search(r"Step (\d+)\b", line)
        line_step = int(step_match.group(1)) if step_match else None
        for m in re.finditer(
                r"BANKED interval duration\s+(\d+(?:\.\d+)?)\s*hours",
                line):
            if _banked_mention_denied(line, m.start()):
                continue
            found.append((_mention_step(line, m, line_step),
                          float(m.group(1)), True))
        if "interval duration" in line:
            continue
        for m in re.finditer(r"BANKED[^\n]*?(\d+(?:\.\d+)?)\s*hours",
                             line):
            if _banked_mention_denied(line, m.start()):
                continue
            found.append((_mention_step(line, m, line_step),
                          float(m.group(1)), False))
    return found


def _derive_t4(captured, universe):
    from metrics_starter_collector.cross_check import \
        t4_cross_check_statement
    ledger = _ledger_piece(captured)
    pointer = ledger.paths[0] if ledger else "PATH-LEDGER.md"
    denom = "denominator decision items and banked states in the tree"
    if ledger is not None and ledger.text is None:
        code = {"malformed": "malformed-piece",
                "over limit": "over-limit-piece"}.get(
                    ledger.quality_state or "", "unreadable-piece")
        return DerivationResult(
            "T-4", "present but not derivable", "no figure stands",
            denom, pointer,
            shows="a path ledger piece is present but not read in "
                  "full in the capture, so no banked state can be "
                  "read to form a wait figure",
            code_token=code,
            follows=code + " the piece is marked not read in full in "
                    "the inventory and no figure is read from it, so "
                    "no wait figure stands",
            rule_name="T-4 not read in full rule")
    banked = False
    durations = False
    if ledger is not None and ledger.text is not None:
        # A banked mention denied in its own clause stands as no
        # banked state and no duration, under the same shared
        # negation handling the T-2 BANKED alternative takes.
        for line in ledger.text.splitlines():
            for m in re.finditer(r"banked", line, re.I):
                before, after = _clause_fragments(
                    line, m.start(), m.end())
                if _before_negated_in_scope(before, after,
                                            m.group(0)):
                    continue
                if _after_negated_in_scope(after, before,
                                           m.group(0)):
                    continue
                if _retracted_in_following_sentence(line, m.end()):
                    continue
                banked = True
                if re.search(r"\d+(?:\.\d+)?\s*hours", after):
                    durations = True
    queue = captured.pieces_of(CLS_DECISION_QUEUE)
    # Banked item counts stand only where a queue piece carries
    # readable decision items, on the same completeness ground
    # the D-1 queue selection applies: a piece whose text parses
    # to a decision item table, from the canonical piece or from
    # a readable duplicate. A queue piece standing in any other
    # state (a directory, malformed, dangling, empty, or a
    # disagreement piece carrying no text) carries no readable
    # items, so its mere presence states no item count.
    queue_counts_stand = False
    for piece in queue:
        if piece.text is not None and \
                _decision_items(piece.text) is not None:
            queue_counts_stand = True
            break
    if queue_counts_stand:
        banked = True
    if not banked and not queue:
        return DerivationResult(
            "T-4", "missing", "no figure stands", denom, pointer,
            shows="no banked state and no decision item count stands in "
                  "the feeder records for this metric",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing",
            rule_name="T-4 feeder standing rule")
    parsed = _t4_banked_durations(captured)
    if not banked and not queue_counts_stand and not parsed and \
            _decision_items(captured.assembled_metrics) is None:
        return DerivationResult(
            "T-4", "present but not derivable", "no figure stands",
            denom, pointer,
            shows="a decision queue piece stands in the capture, "
                  "but no queue piece carries readable decision "
                  "items, so no banked item count stands in the "
                  "feeder records, and the path ledger holds no "
                  "banked state",
            code_token="missing-field",
            follows="missing-field no complete decision queue "
                    "stands, so no banked item count can form and "
                    "no wait figure stands",
            rule_name="T-4 queue completeness rule")
    interval_durations = [(s, v) for s, v, is_interval in parsed
                          if is_interval]
    table_items = _decision_items(captured.assembled_metrics)
    metrics_name = captured.metrics_single_path.rsplit("/", 1)[-1] \
        if captured.metrics_single_path else "build-metrics-record.md"
    cross = t4_cross_check_statement(
        [(s, v) for s, v, _ in parsed], captured.assembled_metrics,
        metrics_name)
    if interval_durations and table_items is None and not queue \
            and cross is None:
        figures = "; ".join(
            "Step %d banked wait %s hours" % (s, _fmt_num(v))
            if s is not None else "banked wait %s hours" % _fmt_num(v)
            for s, v in interval_durations)
        return DerivationResult(
            "T-4", "present", figures, denom, pointer,
            statement="the row is shown without its queue cross check, "
                      "from the BANKED interval durations standing in "
                      "the feeder records, with only the decision table "
                      "cross check absent.",
            rule_name="T-4 degraded form rule")
    if not durations:
        if queue_counts_stand or table_items:
            figures = ("banked item counts stand and no duration "
                       "figure stands")
            shows = ("banked states and item counts stand in the feeder "
                     "records and every duration is absent")
            if table_items:
                open_items = [i for i in table_items if not i["ruled"]]
                if open_items:
                    first_origin = open_items[0]["origin"]
                    same_origin = [i for i in open_items
                                   if i["origin"] == first_origin]
                    figures = ("banked item counts stand, for example "
                               "Step %s: %d banked questions open; no "
                               "duration figure"
                               % (first_origin, len(same_origin)))
                    shows += (", and the decision table rows %s stand open"
                              % _join_names([i["item"] for i in open_items]))
        else:
            figures = ("banked states stand and no duration figure "
                       "stands")
            shows = ("banked states stand in the feeder records and "
                     "every duration is absent")
            if queue:
                shows += (", and no banked item count stands because "
                          "no queue piece carries readable decision "
                          "items")
        return DerivationResult(
            "T-4", "present but not derivable", figures, denom, pointer,
            shows=shows,
            code_token="missing-field",
            follows="missing-field a count of items is not a time, and "
                    "the degraded form does not apply because the "
                    "durations themselves are absent, not only the "
                    "cross check, so no wait figure stands",
            rule_name="T-4 duration absence rule")
    return DerivationResult(
        "T-4", "present but not derivable",
        "durations stand in part and no build level figure stands",
        denom, pointer,
        shows="banked interval durations stand for part of the universe "
              "only",
        code_token="partial-span",
        follows="partial-span the durations cover only part of the step "
                "universe, so no build level figure stands",
        statement=cross,
        rule_name="T-4 mixed series rule")


_NUM_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
              6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def _loop_steps(captured, universe):
    """Loop steps in the universe, under the T-7 population rule.

    A step is a loop step where its step record names it as one: the
    record title carries the word loop, as the target tree records
    name their loop steps, or the record states the loop step form in
    its body.
    """
    loop = []
    for s in sorted(universe.evidenced):
        for p in captured.step_pieces(s, CLS_STEP_RECORD):
            if p.text is None:
                continue
            title = p.text.splitlines()[0] if p.text.splitlines() else ""
            if "loop" in title.lower() or \
                    "loop step" in p.text.lower():
                loop.append(s)
                break
    return loop


def _metrics_table_empty(captured, heading):
    """Whether a metrics record table section holds no rows.

    Returns (empty, stale_text) where stale_text is the sentence in
    the section stating that nothing has run yet, or None.
    """
    text = captured.assembled_metrics
    if not text:
        return False, None
    m = re.search(r"## %s\n(.*?)(?=\n## |\Z)" % re.escape(heading),
                  text, re.S)
    if not m:
        if heading.lower() in text.lower() and \
                "no rows" in text.lower():
            return True, "no rows"
        return False, None
    section = m.group(1)
    if "(no rows yet)" not in section and "no rows" not in section.lower():
        return False, None
    stale = None
    for line in section.splitlines():
        if "has run yet" in line or "has run" in line:
            stale = line.strip()
            break
    return True, stale


def _t7_pass_count(captured, step):
    """Pass count evidenced in a step own record, or None.

    Forms: an explicit pass count statement, an explicit rounds
    statement (including one held in a board ruling inside the
    record), or the round headings of a re-audit loop record, where
    the rounds stand as one initial round plus one round per
    re-audit heading.
    """
    texts = _step_texts(captured, step, (CLS_STEP_RECORD,))
    joined = "\n".join(texts)
    if not joined:
        return None
    m = re.search(r"Pass count in this record:\s*(\d+)\s*passes", joined)
    if m:
        return int(m.group(1))
    m = re.search(r"states\s+(\d+)\s+rounds for this step", joined)
    if m:
        return int(m.group(1))
    head_rounds = [int(x) for x in re.findall(
        r"^## Re-audit[^\n]*\(round (\d+)", joined, re.M)]
    reaudit_heads = re.findall(r"^## Re-audit", joined, re.M)
    if head_rounds and min(head_rounds) == 1:
        # The re-audit headings enumerate the rounds themselves, a
        # re-audit of round 1 standing among them.
        return max(head_rounds)
    if reaudit_heads:
        # The headings name the inputs of each following round, so
        # the rounds stand as one initial round plus one round per
        # re-audit heading.
        return 1 + len(reaudit_heads)
    return None


def _t7_verdict_count(captured, step):
    """Verdict record count for one loop step, under G-05.

    The count is the number of verdict records for the step in the
    closed verdict record set, the gate alias set plus
    adjudications. Board rulings held inside step records are never
    verdict records. An explicit verdict record count statement in a
    verdict record stands as the count it states. The count states
    records, not pieces: partitioned copies of one record, standing
    as their own pieces under the duplicate partition, are copies at
    one identity and count once, so the number of distinct
    identities among the step gate pieces is the record count.
    """
    pieces = captured.step_pieces(step, *GATE_CLASSES)
    for p in pieces:
        if p.text:
            m = re.search(r"Verdict record count for this step:\s*(\d+)",
                          p.text)
            if m:
                return int(m.group(1))
    return len({p.identity for p in pieces})


def _derive_t7(captured, universe):
    metrics_path = captured.metrics_single_path or \
        "wiki/wiki/synthesis/build-metrics-record.md"
    gates = captured.pieces_of(*GATE_CLASSES)
    pointer = metrics_path
    loop = _loop_steps(captured, universe)
    table_empty, stale = _metrics_table_empty(captured, "Loop round table")
    if not loop:
        if table_empty and gates:
            return DerivationResult(
                "T-7", "present but not derivable", "no round count figure",
                "denominator loop steps in the step universe", pointer,
                shows="the loop round table in the metrics record holds "
                      "no rows and still carries stale text, while gate "
                      "files in the tree carry round counts for the "
                      "loop steps, and the two counts cannot be "
                      "reconciled to one count",
                code_token="record-disagrees",
                follows="the verdict record count and the step record "
                        "pass count cannot be reconciled to one count, "
                        "with both counts named in the record",
                rule_name="T-7 irreconcilable counts rule")
        return DerivationResult(
            "T-7", "missing", "no round count figure",
            "denominator population loop steps none in the step universe",
            pointer,
            shows="no loop step and no verdict record for a loop step "
                  "stands in the tree, so the population the metric "
                  "counts over is empty",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing, with its empty "
                    "population stated",
            rule_name="T-7 empty population rule")
    verdict_counts = {s: _t7_verdict_count(captured, s) for s in loop}
    pass_counts = {s: _t7_pass_count(captured, s) for s in loop}
    board_steps = []
    for s in loop:
        for p in captured.step_pieces(s, CLS_STEP_RECORD):
            if p.text and "board ruling" in p.text.lower() and \
                    pass_counts[s] is not None:
                board_steps.append(s)
                break
    irreconcilable = [s for s in loop if pass_counts[s] is not None
                      and pass_counts[s] != verdict_counts[s]]
    compact = ", ".join(str(s) for s in loop[:-1])
    if compact:
        compact += " and " + str(loop[-1])
    else:
        compact = str(loop[-1])
    excluded_entries = ""
    for s in board_steps:
        recs = captured.step_pieces(s, CLS_STEP_RECORD)
        name = recs[0].paths[0].rsplit("/", 1)[-1] if recs else ""
        excluded_entries += ("; Step %d board ruling held inside %s "
                             "excluded from the verdict record set"
                             % (s, name))
    denom = ("denominator population loop steps %s; loop steps in the "
             "population: %s; excluded: board rulings held inside step "
             "records and every record form outside the closed verdict "
             "record set%s"
             % (compact, _each_step(loop), excluded_entries))
    if irreconcilable:
        clauses = []
        if table_empty:
            clauses.append("the loop round table holds no rows and "
                           "still carries stale text")
        groups = {}
        for s in loop:
            groups.setdefault(verdict_counts[s], []).append(s)
        count_bits = []
        for count in sorted(groups):
            steps = groups[count]
            if count == 1 and len(steps) >= 3:
                count_bits.append("counts of 1 for Steps %d to %d"
                                  % (min(steps), max(steps)))
            else:
                for s in steps:
                    count_bits.append("%d for Step %d" % (count, s))
        if count_bits:
            if len(count_bits) == 1:
                joined_bits = count_bits[0]
            else:
                joined_bits = ", ".join(count_bits[:-1]) + \
                    " and " + count_bits[-1]
            clauses.append("gate files give " + joined_bits)
        for s in irreconcilable:
            rulings = captured.step_pieces(s, CLS_GATE_RULING)
            heads = 0
            for p in captured.step_pieces(s, CLS_STEP_RECORD):
                if p.text:
                    heads += len(re.findall(r"^## Re-audit", p.text, re.M))
            if heads and len(rulings) == 1:
                clauses.append(
                    "Step %d records %s rounds in its own record while "
                    "only the last round has a ruling file"
                    % (s, _NUM_WORDS.get(pass_counts[s], str(pass_counts[s]))))
            elif s in board_steps:
                clauses.append(
                    "Step %d records %d rounds in a board ruling held "
                    "inside its step record, while the closed verdict "
                    "record set gives a verdict record count of %d for "
                    "that step" % (s, pass_counts[s], verdict_counts[s]))
            else:
                clauses.append(
                    "Step %d pass count is %d passes and the verdict "
                    "record count is %d verdict record for that step"
                    % (s, pass_counts[s], verdict_counts[s]))
        return DerivationResult(
            "T-7", "present but not derivable", "no round count figure",
            denom, pointer,
            shows=", ".join(clauses),
            code_token="record-disagrees",
            follows="the verdict record count and the step record pass "
                    "count cannot be reconciled to one count, with both "
                    "counts named",
            rule_name="T-7 irreconcilable counts rule")
    if all(verdict_counts[s] >= 1 for s in loop):
        figures = "; ".join("Step %d: %d rounds counted"
                            % (s, verdict_counts[s]) for s in loop)
        return DerivationResult(
            "T-7", "present", figures, denom, pointer,
            statement="the rounds are counted from verdict records in "
                      "the closed verdict record set and are marked "
                      "as counted.",
            rule_name="T-7 counted rounds rule")
    return DerivationResult(
        "T-7", "present but not derivable", "no round count figure",
        denom, pointer,
        shows="verdict records stand for steps in the tree and no "
              "round mapping in the settled form stands for them",
        code_token="missing-field",
        follows="the round count field the derivation needs is absent "
                "from the verdict records as they stand",
        rule_name="T-7 round mapping rule")


# ------------------------------------------------------------- E-1 and E-2

def _step_texts(captured, step, classes):
    out = []
    for p in captured.step_pieces(step, *classes):
        if p.text is not None:
            out.append(p.text)
    return out


def _parse_staffed_base(captured, step):
    """Return (staffed, base) for one step from its feeder records."""
    texts = _step_texts(captured, step,
                        (CLS_STEP_RECORD, CLS_SNAPSHOT, CLS_ROSTER,
                         CLS_OPENING_RECORD, CLS_STEP_COMPANION))
    joined = "\n".join(texts)
    if not joined:
        return None
    m = re.search(r"Base:\s*(\d+)\.\s*Team staffed:\s*(\d+)", joined)
    if m:
        return int(m.group(2)), int(m.group(1))
    m = re.search(r"Staffed and base \(E-1\):\s*(\d+)\s*/\s*(\d+)", joined)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"[Ss]taffed\s+(\d+)\s+against\s+(?:the step chosen base of|a base of|its base of|the base of)\s+(\d+)", joined)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"Step team at Low:[^\n]*count\s+(\d+)", joined)
    if m:
        base = int(m.group(1))
        holders = len(set(re.findall(r"holder\s+(\d+)", joined)))
        staffed = holders if holders > base else base
        return staffed, base
    m = re.search(r"Step total: Low\s+(\d+)", joined)
    if m:
        return int(m.group(1)), int(m.group(1))
    m = re.search(r"counted as [^.]*", joined)
    if m and "plus" in m.group(0):
        nums = [int(x) for x in re.findall(r"(\d+)\s*(?:plus|,)", m.group(0))]
        tail = re.findall(r"plus\s+\w+\s+(\d+)", m.group(0))
        total = sum(nums) + sum(int(x) for x in tail)
        if total:
            return total, total
    m = re.search(r"size chosen\s+(\d+)", joined)
    if m:
        total = int(m.group(1))
        m2 = re.search(r"imagination team \(Low\s+(\d+)\)", joined)
        if m2:
            total += int(m2.group(1))
        return total, total
    m = re.search(r"being team\s+(\d+)\s*\(", joined)
    if m:
        return int(m.group(1)), int(m.group(1))
    m = re.search(r"counted as pre-plan research\s+(\d+), Research Clerk\s+"
                  r"\d+, probe runner\s+(\d+), design team\s+(\d+)", joined)
    if m:
        total = int(m.group(1)) + int(m.group(2)) + int(m.group(3))
        return total, total
    m = re.search(r"Units in loop order:\s*([^.\n]*)", joined)
    if m:
        nums = [int(x) for x in re.findall(r"(\d+)", m.group(1))]
        if nums:
            return sum(nums), sum(nums)
    m = re.search(r"being\s+([^.\n]*?)\s+as team", joined)
    if m:
        nums = [int(x) for x in re.findall(r"Low\s+(\d+)", m.group(1))]
        nums += [int(x) for x in re.findall(r"Tracer\s+(\d+)", m.group(1))]
        if nums:
            return sum(nums), sum(nums)
    m = re.search(r"Team:\s*[A-Za-z]+,\s*count\s+(\d+)", joined)
    if m:
        return int(m.group(1)), int(m.group(1))
    m = re.search(r"^-\s*Teams:\s*([^\n]*)", joined, re.M)
    if m:
        total = 0
        for chunk in m.group(1).split(","):
            nums = re.findall(r"\d+", chunk)
            if nums:
                total += int(nums[0])
        if total:
            return total, total
    m = re.search(r"Design team:\s*(\d+)\s+distinct members", joined)
    if m:
        return int(m.group(1)), int(m.group(1))
    m = re.search(r"team at its Low base of\s+(\d+)", joined)
    if m:
        return int(m.group(1)), int(m.group(1))
    m = re.search(r"base of\s+(\d+)[^\n]*counting its (\w+) distinct", joined)
    if m:
        words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        return words.get(m.group(2), int(m.group(1))), int(m.group(1))
    return None


def _parse_base(captured, step):
    pair = _parse_staffed_base(captured, step)
    if pair:
        return pair[1]
    texts = _step_texts(captured, step, (CLS_STEP_RECORD, CLS_SNAPSHOT))
    joined = "\n".join(texts)
    m = re.search(r"Base:\s*(\d+)", joined)
    if m:
        return int(m.group(1))
    m = re.search(r"base of\s+(\d+)", joined)
    if m:
        return int(m.group(1))
    return None


def _parse_total_spins(captured, step):
    texts = _step_texts(captured, step,
                        (CLS_STEP_RECORD, CLS_SNAPSHOT, CLS_ROSTER))
    joined = "\n".join(texts)
    if not joined:
        return None
    m = re.search(r"Total spins:\s*(\d+)", joined)
    if m:
        return int(m.group(1))
    m = re.search(r"Final count, actual:[^\n]*?and\s+(\d+)\s+with the Auditor", joined)
    if m:
        return int(m.group(1))
    m = re.search(r"share for Step %d is amended to\s+(\d+)" % step, joined)
    if m:
        return int(m.group(1))
    m = re.search(r"Total planned:\s*(\d+)\s*spins", joined)
    if m:
        return int(m.group(1))
    m = re.search(r"[Pp]lanned spawns for this step[^\n]*?(\d+)\s+in total", joined)
    if m:
        return int(m.group(1))
    m = re.search(r"actual\s+(\d+)\s+spawns", joined)
    if m:
        return int(m.group(1))
    m = re.search(r"Spins \(E-2\):\s*(\d+)\s+in total", joined)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s*\(total spins for the step", joined)
    if m:
        return int(m.group(1))
    return None


def _parse_additions(captured, step):
    texts = _step_texts(captured, step,
                        (CLS_STEP_RECORD, CLS_SNAPSHOT, CLS_ROSTER))
    joined = "\n".join(texts)
    m = re.search(r"Roster additions over base:\s*(\d+)", joined)
    if m:
        return int(m.group(1))
    m = re.search(r"[Aa]dditions over base:\s*(\d+)", joined)
    if m:
        return int(m.group(1))
    if captured.step_pieces(step, CLS_ROSTER):
        total = _parse_total_spins(captured, step)
        base = _parse_base(captured, step)
        if total is not None and base is not None:
            return total - base
        if total is not None:
            return total
    return None


def _derive_e1(captured, universe):
    rosters = captured.pieces_of(CLS_ROSTER)
    pointer = rosters[0].paths[0] if rosters else \
        (captured.first_path(CLS_STEP_RECORD) or "steps/step-01-record.md")
    denom_base = "denominator step universe %d steps" % len(universe.evidenced)
    covered = {}
    for s in universe.evidenced:
        pair = _parse_staffed_base(captured, s)
        if pair:
            covered[s] = pair
    if not captured.pieces_of(CLS_STEP_RECORD, CLS_ROSTER):
        return DerivationResult(
            "E-1", "missing", "no figure stands", denom_base, pointer,
            shows="no step record and no roster artifact stands in the "
                  "tree for this metric",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing",
            rule_name="E-1 feeder standing rule")
    if not covered:
        return DerivationResult(
            "E-1", "present but not derivable", "no figure stands",
            denom_base, pointer,
            shows="step records stand in the tree and no staffed count "
                  "beside a stated base stands in the form the derivation "
                  "accepts for any step",
            code_token="missing-field",
            follows="missing-field the staffed and base fields the "
                    "derivation needs are absent from the feeder records, "
                    "so no figure stands",
            rule_name="E-1 defined form rule")
    figure_parts = ["Step %d staffed %d of base %d"
                    % (s, covered[s][0], covered[s][1])
                    for s in sorted(covered)]
    for s in sorted({p.step for p in rosters if p.step is not None}):
        for p in captured.step_pieces(s, CLS_ROSTER):
            if p.text is None:
                continue
            counts = re.findall(r"equals (\d+)", p.text)
            if counts:
                named = "named spawns" if "named spawns" in p.text \
                    else "spawns"
                figure_parts.append("roster artifact Step %d lists %s %s"
                                    % (s, counts[-1], named))
            break
    figures = "; ".join(figure_parts)
    remainder = [s for s in universe.evidenced if s not in covered]
    if remainder:
        # A remainder step whose feeder record stands in the tree but
        # was not read in full is named on that ground, never as a
        # step stating no base: the base was not found absent, the
        # record was not read.
        unreadable_remainder = [
            s for s in remainder
            if any(p.text is None for p in captured.step_pieces(
                s, CLS_STEP_RECORD, CLS_ROSTER, CLS_SNAPSHOT,
                CLS_OPENING_RECORD, CLS_STEP_COMPANION))]
        plain_remainder = [s for s in remainder
                           if s not in unreadable_remainder]
        clauses = []
        if plain_remainder:
            clauses.append("remainder " +
                           _step_list_text(plain_remainder) +
                           " named, no base stated")
        if unreadable_remainder:
            clauses.append("remainder " +
                           _step_list_text(unreadable_remainder) +
                           " named, feeder record present but not "
                           "read in full")
        denom = (denom_base + "; covered " +
                 _step_list_text(sorted(covered)) +
                 "; " + "; ".join(clauses))
        statement = ("Present under the present with coverage form: the "
                     "covered part yields E-1 in its defined form and "
                     "the uncovered remainder is named.")
    else:
        denom = denom_base + "; covered " + _step_list_text(sorted(covered))
        statement = ("Present under the present with coverage form: the "
                     "covered part yields E-1 in its defined form and "
                     "no uncovered remainder stands.")
    return DerivationResult("E-1", "present", figures, denom, pointer,
                            statement=statement,
                            rule_name="E-1 present with coverage rule")


def _derive_e2(captured, universe):
    roster_steps = sorted({p.step for p in captured.pieces_of(CLS_ROSTER)
                           if p.step is not None})
    pointer = None
    for s in roster_steps:
        recs = captured.step_pieces(s, CLS_STEP_RECORD)
        if recs:
            pointer = recs[0].paths[0]
            break
    if pointer is None:
        pointer = captured.first_path(CLS_STEP_RECORD) or "steps/step-01-record.md"
    denom_base = "denominator step universe %d steps" % len(universe.evidenced)
    totals = {}
    additions = {}
    for s in universe.evidenced:
        total = _parse_total_spins(captured, s)
        if total is not None:
            totals[s] = total
        add = _parse_additions(captured, s)
        if add is not None:
            additions[s] = add
    if not captured.pieces_of(CLS_STEP_RECORD, CLS_ROSTER):
        return DerivationResult(
            "E-2", "missing", "no figure stands", denom_base, pointer,
            shows="no step record and no roster artifact stands in the "
                  "tree for this metric",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing",
            rule_name="E-2 feeder standing rule")
    if not totals and not additions:
        return DerivationResult(
            "E-2", "present but not derivable", "no figure stands",
            denom_base, pointer,
            shows="step records stand in the tree and no total spins "
                  "figure and no additions figure stands in the form the "
                  "derivation accepts",
            code_token="missing-field",
            follows="missing-field the spin fields the derivation needs "
                    "are absent from the feeder records, so no figure "
                    "stands",
            rule_name="E-2 defined form rule")
    parts = []
    if totals:
        seg = "; ".join("Step %d: %d" % (s, totals[s]) for s in sorted(totals))
        parts.append("total spins " + seg)
    if additions:
        keys = sorted(additions)
        if len(keys) == 1:
            parts.append("additions over base stated for Step %d" % keys[0])
        elif len(keys) == 2:
            parts.append("additions over base stated for Steps %d and %d"
                         % (keys[0], keys[1]))
        else:
            parts.append("additions over base stated for Steps " +
                         ", ".join(str(k) for k in keys))
    computed = {}
    for s in sorted(totals):
        if s in additions:
            continue
        base = _parse_base(captured, s)
        if base is not None:
            computed[s] = totals[s] - base
    for s in sorted(computed):
        parts.append("additions over base Step %d: %d" % (s, computed[s]))
    detail_total = None
    stated_total = None
    for s in universe.evidenced:
        joined = "\n".join(_step_texts(
            captured, s, (CLS_STEP_RECORD, CLS_SNAPSHOT, CLS_ROSTER)))
        if detail_total is None:
            m = re.search(r"Detail total spins:\s*(\d+)", joined)
            if m:
                detail_total = int(m.group(1))
        if stated_total is None:
            m = re.search(r"Stated total spins:\s*(\d+)", joined)
            if m:
                stated_total = int(m.group(1))
    if detail_total is not None and stated_total is not None:
        parts.append("detail total spins %d" % detail_total)
        parts.append("stated total spins %d" % stated_total)
        parts.append("variance %d" % abs(detail_total - stated_total))
    cumulative = []
    for s in universe.evidenced:
        joined = "\n".join(_step_texts(
            captured, s, (CLS_STEP_RECORD, CLS_SNAPSHOT)))
        m = re.search(r"Budget at closure:\s*(\d+) of (\d+) documented "
                      r"units", joined)
        if m:
            cumulative.append("Step %d closing %s of %s"
                              % (s, m.group(1), m.group(2)))
            continue
        m = re.search(r"Final budget:\s*(\d+) of (\d+) documented units",
                      joined)
        if m:
            cumulative.append("Step %d final %s of %s"
                              % (s, m.group(1), m.group(2)))
    if cumulative:
        parts.append("cumulative documented units at " +
                     " and at ".join(cumulative))
    if totals and (additions or computed):
        parts.append("additions over base and total spins both reported "
                     "labelled")
    no_base = [s for s in universe.evidenced if _parse_base(captured, s) is None]
    if no_base:
        # A step whose feeder record stands in the tree but was not
        # read in full is named on that ground, never under the
        # missing field code for an absent stated base: the base was
        # not found absent, the record was not read.
        unreadable_no_base = [
            s for s in no_base
            if any(p.text is None for p in captured.step_pieces(
                s, CLS_STEP_RECORD, CLS_ROSTER, CLS_SNAPSHOT))]
        plain_no_base = [s for s in no_base
                         if s not in unreadable_no_base]
        clauses = []
        if plain_no_base:
            clauses.append(_step_list_text(plain_no_base) +
                           " named against additions over base only "
                           "with code missing-field for the absent "
                           "stated base, total spins still reported")
        if unreadable_no_base:
            clauses.append(_step_list_text(unreadable_no_base) +
                           " named against additions over base only, "
                           "feeder record present but not read in full")
        denom = denom_base + "; " + "; ".join(clauses)
        statement = ("Present under the G-03 coverage form in its own "
                     "terms: the covered steps yield both labelled "
                     "quantities in their defined form and the steps "
                     "that state no base are named against additions "
                     "over base only.")
    else:
        denom = denom_base
        statement = ("Present under the G-03 coverage form in its own "
                     "terms: the covered steps yield both labelled "
                     "quantities in their defined form.")
    return DerivationResult("E-2", "present", "; ".join(parts), denom,
                            pointer, statement=statement,
                            rule_name="E-2 labelled quantities rule")


# ------------------------------------------------------- E-3, E-4, F-2

def _cost_ledger(captured):
    """Parse the cost ledger pieces in the capture, under D-09.

    Only the ledger entry forms count as figures: a per step entry
    naming the step, with a money figure, a token figure, or both; a
    Budget line; and a Build total stated line. A figure standing in
    any other record, in prose in the ledger, or in the metrics
    record is never read here. Returns the per step figures, the
    budget figures, the stated build totals and the ledger pieces.
    """
    money = {}
    tokens = {}
    budget_money = None
    budget_token = None
    stated_money = None
    stated_token = None
    pieces = captured.pieces_of(CLS_COST_LEDGER)
    for p in pieces:
        if p.text is None:
            continue
        for m in re.finditer(r"Step (\d+):\s*money (\d+(?:\.\d+)?)"
                             r"(?:,\s*tokens (\d+(?:\.\d+)?))?", p.text):
            money[int(m.group(1))] = float(m.group(2))
            if m.group(3) is not None:
                tokens[int(m.group(1))] = float(m.group(3))
        for m in re.finditer(r"Step (\d+):\s*tokens (\d+(?:\.\d+)?)",
                             p.text):
            tokens.setdefault(int(m.group(1)), float(m.group(2)))
        for m in re.finditer(r"Budget:\s*money (\d+(?:\.\d+)?)"
                             r"(?:,\s*tokens (\d+(?:\.\d+)?))?", p.text):
            budget_money = float(m.group(1))
            if m.group(2) is not None:
                budget_token = float(m.group(2))
        for m in re.finditer(r"Budget:\s*tokens (\d+(?:\.\d+)?)", p.text):
            if budget_token is None:
                budget_token = float(m.group(1))
        for m in re.finditer(r"Build total stated:\s*money "
                             r"(\d+(?:\.\d+)?)"
                             r"(?:,\s*tokens (\d+(?:\.\d+)?))?", p.text):
            stated_money = float(m.group(1))
            if m.group(2) is not None:
                stated_token = float(m.group(2))
        for m in re.finditer(r"Build total stated:\s*tokens "
                             r"(\d+(?:\.\d+)?)", p.text):
            if stated_token is None:
                stated_token = float(m.group(1))
    return {"money": money, "tokens": tokens,
            "budget_money": budget_money, "budget_token": budget_token,
            "stated_money": stated_money, "stated_token": stated_token,
            "pieces": pieces}


def _step_money_nil(captured):
    """Per step nil money statements standing in step records.

    A nil phrase counts as a statement for a step only where it
    stands as a statement segment of its own in that step record:
    a segment between sentence or clause boundaries. A nil phrase
    inside a segment that states the whole build figure restates
    the whole build figure; under the entry limb of the field
    acceptance test it belongs to the whole build statement, not
    to the step, and is not a per step statement. Returns a map
    from a step to the nil phrases its record states, in record
    order, each phrase in the form money nil, money nil external
    or money zero external.
    """
    phrases = {}
    for p in captured.pieces_of(CLS_STEP_RECORD):
        if p.step is None or p.text is None:
            continue
        for segment in re.split(r"[.;\n]", p.text):
            m = re.search(r"money\s+(nil|zero)(\s+external)?", segment,
                          re.I)
            if m and "whole build" not in segment.lower():
                phrase = "money " + m.group(1).lower()
                if m.group(2):
                    phrase += " external"
                phrases.setdefault(p.step, []).append(phrase)
    return phrases


def _whole_build_money(captured):
    """The whole build money statement in a step record, or none.

    Returns (piece, value) for the first step record, in capture
    order, whose budget act states a money figure for the whole
    build in the form Money: N external spend for the whole build,
    and (None, None) where no step record states one.
    """
    for p in captured.pieces_of(CLS_STEP_RECORD):
        if p.text is None:
            continue
        m = re.search(r"Money:\s*(\d+(?:\.\d+)?)\s+external spend "
                      r"for the whole build", p.text)
        if m:
            return p, float(m.group(1))
    return None, None


def _derive_e3(captured, universe):
    pointer = captured.first_path(CLS_INSTALL_REGISTER) or \
        "registers/INSTALL-REGISTER.md"
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    led = _cost_ledger(captured)
    ledgers = led["pieces"]
    if not ledgers:
        return DerivationResult(
            "E-3", "missing", "no token figure", denom, pointer,
            shows="no cost ledger stands inside the tree, the only "
                  "file under registers is the install register with "
                  "no token figures, and step records state tokens "
                  "NOT RECORDED because no feeder metering exists",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists, and the "
                    "documented units proxy is not the metric, so the "
                    "row is missing",
            rule_name="E-3 feeder standing rule")
    if all(p.text is None for p in ledgers):
        code = {"malformed": "malformed-piece",
                "over limit": "over-limit-piece"}.get(
                    ledgers[0].quality_state or "", "unreadable-piece")
        return DerivationResult(
            "E-3", "present but not derivable", "no token figure", denom,
            ledgers[0].paths[0],
            shows="a cost ledger stands in the tree at %s and it was "
                  "not read in full, so it supplies no token figure "
                  "for any step" % ledgers[0].paths[0],
            code_token=code,
            follows=code + " the piece is marked not read in full in "
                    "the inventory and no figure is read from it, so "
                    "no token figure stands",
            rule_name="E-3 not read in full rule")
    tokens = led["tokens"]
    if not tokens:
        # The feeder for E-3 is the cost ledger token figures. A
        # ledger that meters no tokens holds no feeder record for
        # this metric, however much money it meters.
        return DerivationResult(
            "E-3", "missing", "no token figure", denom, pointer,
            shows="a cost ledger stands inside the tree and it meters "
                  "no token figure for any step, and step records "
                  "state tokens NOT RECORDED because no feeder "
                  "metering exists for tokens",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists, and the "
                    "documented units proxy is not the metric, so the "
                    "row is missing",
            rule_name="E-3 feeder standing rule")
    if led["stated_token"] is not None and \
            sum(tokens.values()) != led["stated_token"]:
        total = sum(tokens.values())
        return DerivationResult(
            "E-3", "present but not derivable",
            "per step token figures sum to %s against a stated build "
            "total of %s" % (_fmt_num(total),
                             _fmt_num(led["stated_token"])),
            denom, ledgers[0].paths[0],
            shows="the cost ledger states per step token figures "
                  "which sum to %s, and states a build total of %s "
                  "for tokens" % (_fmt_num(total),
                                  _fmt_num(led["stated_token"])),
            code_token="unreconciled-figure",
            follows="unreconciled-figure the per step token figures "
                    "and the stated build total do not reconcile, so "
                    "the metric in its defined form does not yield",
            rule_name="E-3 unreconciled figure rule")
    covered = [s for s in universe.evidenced if s in tokens]
    if universe.evidenced and len(covered) == len(universe.evidenced):
        figures = "; ".join("Step %d tokens %s" % (s, _fmt_num(tokens[s]))
                            for s in covered)
        return DerivationResult("E-3", "present", figures, denom,
                                ledgers[0].paths[0],
                                rule_name="E-3 token series rule")
    remainder = [s for s in universe.evidenced if s not in tokens]
    figures = ("token figures stand for " + _step_list_text(covered)
               if covered else "no token figure")
    denom += ("; covered span " + _step_list_text(covered) +
              "; remainder " + _step_list_text(remainder) +
              " named, steps outside the covered span are not "
              "reported as zero")
    return DerivationResult(
        "E-3", "present but not derivable", figures, denom,
        ledgers[0].paths[0],
        shows="the cost ledger meters tokens for %s only, part of "
              "the step universe" % _step_list_text(covered),
        code_token="partial-span",
        follows="partial-span the covered span is named in the "
                "coverage and steps outside it are not reported as "
                "zero, so no build level figure stands",
        rule_name="E-3 partial metering rule")


def _e4_pointer(captured, led, nil_phrases, covered):
    """Pointer for the E-4 row, in the single pointer form.

    A step record that states a closing budget figure beside its
    per step nil statement is the record the row rests on where one
    stands. Otherwise the cost ledger where it supplies the series,
    and otherwise the record of the first covered step, or the
    first step record standing.
    """
    for s in sorted(covered):
        if s not in nil_phrases:
            continue
        for p in captured.step_pieces(s, CLS_STEP_RECORD):
            if p.text and "Budget at closure" in p.text:
                return p.paths[0]
    if led["money"]:
        return led["pieces"][0].paths[0]
    for s in sorted(covered):
        found = captured.step_pieces(s, CLS_STEP_RECORD)
        if found:
            return found[0].paths[0]
    if led["pieces"]:
        return led["pieces"][0].paths[0]
    return captured.first_path(CLS_STEP_RECORD) or \
        "steps/step-01-record.md"


def _derive_e4(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    led = _cost_ledger(captured)
    nil_phrases = _step_money_nil(captured)
    covered = {}
    for s in universe.evidenced:
        if s in led["money"]:
            covered[s] = led["money"][s]
        elif s in nil_phrases:
            covered[s] = 0.0
    ledgers = led["pieces"]
    step_records = captured.pieces_of(CLS_STEP_RECORD)
    if not step_records and not ledgers:
        return DerivationResult(
            "E-4", "missing", "no figure stands", denom,
            "steps/step-01-record.md",
            shows="no per step money figure and no cost ledger money "
                  "figure stands in the feeder records, and no step "
                  "record stands in the tree",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing",
            rule_name="E-4 feeder standing rule")
    pointer = _e4_pointer(captured, led, nil_phrases, covered)
    if led["stated_money"] is not None and led["money"]:
        total = sum(led["money"].values())
        if total != led["stated_money"]:
            series = "; ".join(
                "Step %d: %s" % (s, _fmt_num(led["money"][s]))
                for s in sorted(led["money"]))
            return DerivationResult(
                "E-4", "present but not derivable",
                "per step money figures sum to %s against a stated "
                "build total of %s"
                % (_fmt_num(total), _fmt_num(led["stated_money"])),
                denom, ledgers[0].paths[0],
                shows="the cost ledger states per step money figures, "
                      "%s, which sum to %s, and states a build total "
                      "of %s" % (series, _fmt_num(total),
                                 _fmt_num(led["stated_money"])),
                code_token="unreconciled-figure",
                follows="unreconciled-figure the per step money "
                        "figures and the stated build total do not "
                        "reconcile, so the metric in its defined form "
                        "does not yield",
                rule_name="E-4 unreconciled figure rule")
    if not covered:
        return DerivationResult(
            "E-4", "present but not derivable", "no figure stands",
            denom, pointer,
            shows="step records stand in the tree and no per step "
                  "money figure stands in the form the derivation "
                  "accepts for any step",
            code_token="missing-field",
            follows="missing-field the per step money field the "
                    "derivation needs is absent from the feeder "
                    "records, so the metric in its defined form does "
                    "not yield",
            rule_name="E-4 defined form rule")
    covered_steps = sorted(covered)
    if universe.evidenced and \
            len(covered_steps) == len(universe.evidenced):
        figures = "; ".join(
            "Step %d money %s" % (s, _fmt_num(covered[s]))
            if s in led["money"] else
            "Step %d %s" % (s, nil_phrases[s][0])
            for s in covered_steps)
        return DerivationResult("E-4", "present", figures, denom,
                                pointer, rule_name="E-4 series rule")
    remainder = [s for s in universe.evidenced if s not in covered]
    nil_covered = [s for s in covered_steps if s not in led["money"]]
    covered_form = "with per step nil statements" \
        if len(nil_covered) == len(covered_steps) else \
        "with per step money figures"
    denom += ("; covered " + _step_list_text(covered_steps) + " " +
              covered_form + "; remainder " +
              _step_list_text(remainder) +
              " named, no per step money figure stands")
    whole_piece, whole_value = _whole_build_money(captured)
    if whole_value == 0 and len(nil_covered) == len(covered_steps):
        examples = []
        pointer_step = None
        for s in covered_steps:
            for p in captured.step_pieces(s, CLS_STEP_RECORD):
                if p.text and "Budget at closure" in p.text:
                    pointer_step = s
                    break
            if pointer_step is not None:
                break
        chosen = []
        if pointer_step is not None:
            chosen.append((pointer_step, nil_phrases[pointer_step][0]))
        for s in covered_steps:
            phrase = next((ph for ph in nil_phrases[s]
                           if ph.startswith("money zero")), None)
            if phrase is not None:
                chosen.append((s, phrase))
                break
        last = covered_steps[-1]
        last_phrase = next(
            (ph for ph in nil_phrases[last] if "external" in ph),
            nil_phrases[last][0])
        chosen.append((last, last_phrase))
        seen = set()
        for step, phrase in sorted(chosen):
            if step not in seen:
                seen.add(step)
                examples.append("Step %d %s" % (step, phrase))
        figures = ("whole build money figure nil external spend; "
                   "per step nil statements for %s, for example %s"
                   % (_step_list_text(covered_steps),
                      ", ".join(examples)))
        shows = ("a split series stands, a whole build nil figure "
                 "and per step nil statements for the later steps, "
                 "and nothing per step for %s"
                 % _step_list_text(remainder))
        if captured.assembled_metrics and \
                "no feeder record carries money for this step" in \
                captured.assembled_metrics:
            shows += (", with the cross check table marking Money "
                      "NOT RECORDED for %s" % _step_list_text(remainder))
        return DerivationResult(
            "E-4", "present but not derivable", figures, denom, pointer,
            shows=shows,
            code_token="missing-field",
            follows="missing-field no complete per step money series "
                    "stands in the feeders, so the metric in its "
                    "defined form does not yield",
            rule_name="E-4 partial series rule")
    series = "; ".join(
        "Step %d money %s" % (s, _fmt_num(covered[s]))
        if s in led["money"] else
        "Step %d %s" % (s, nil_phrases[s][0])
        for s in covered_steps)
    figures = series + "; no complete per step money series stands"
    return DerivationResult(
        "E-4", "present but not derivable", figures, denom, pointer,
        shows="a partial money series stands in the feeder records, "
              "with per step statements for part of the universe and "
              "nothing per step for the remainder steps named in the "
              "coverage",
        code_token="missing-field",
        follows="missing-field no complete per step money series "
                "stands in the feeders, so the metric in its defined "
                "form does not yield",
        rule_name="E-4 partial series rule")


_CLOSURE_TOKENS = ("CLOSED-PASS", "CLOSED-QUALIFIED", "CLOSED-FAIL",
                   "RECYCLED")


def _recorded_closure(text):
    """Return the recorded closure state in a settled form, or None.

    Matching is on the recorded closure state field and on the verdict
    forms the gate records use, exact forms only, never on a closure
    token mentioned in prose.
    """
    exact = r"(?![-A-Za-z0-9])"
    m = re.search(r"(?:Step closure state|Closure state):\s*"
                  r"(CLOSED-PASS|CLOSED-QUALIFIED|CLOSED-FAIL|RECYCLED)"
                  + exact, text)
    if m:
        return m.group(1)
    for line in text.splitlines():
        m = re.match(r"\s*(CLOSED-PASS|CLOSED-QUALIFIED|CLOSED-FAIL|"
                     r"RECYCLED)\s*[.,]", line)
        if m:
            return m.group(1)
    m = re.search(r"recorded as\s+(CLOSED-PASS|CLOSED-QUALIFIED|"
                  r"CLOSED-FAIL|RECYCLED)" + exact, text)
    if m:
        return m.group(1)
    m = re.search(r"recorded\s+(RECYCLED)\b", text)
    if m:
        return m.group(1)
    m = re.search(r"closes\s+(CLOSED-PASS|CLOSED-QUALIFIED|CLOSED-FAIL)"
                  + exact, text)
    if m:
        return m.group(1)
    m = re.search(r"Verdict grade:\s*(FAIL)\b", text)
    if m:
        return m.group(1)
    return None


def _f2_ranked_pieces(captured, step):
    ranked = []
    for cls, rank in ((CLS_GATE_RECORD, 0), (CLS_GATE_RULING, 1),
                      (CLS_GATE_ADJUDICATION, 2), (CLS_REGATE_RECORD, 3)):
        for p in captured.step_pieces(step, cls):
            name = p.paths[0]
            r = rank
            num = 0
            if "round" in name or "reaudit" in name:
                r = 3
                m = re.search(r"(?:round|reaudit)-?(\d+)", name)
                num = int(m.group(1)) if m else 0
            if cls == CLS_REGATE_RECORD:
                # G-02 order: base form first, regate variants last.
                # A regate record ranks behind every piece that is
                # not itself a regate, numbered round or re-audit
                # named rulings included, so a regate is the counted
                # first ruling only where no earlier ruling piece
                # stands.
                r = 4
            ranked.append((r, num, name, p))
    ranked.sort(key=lambda item: (item[0], item[1], item[2]))
    # Selection within each identity group, and nothing else: where
    # a piece at an identity carries substantive text and a duplicate
    # at the same identity carries none (its text was not read in
    # full, or it carries no content at all), the ranked list rests
    # on the substantive piece for that identity, so the gate record
    # selection feeds from the readable duplicate as the step record
    # and metrics record selections do on the same shapes. Where no
    # piece at an identity carries substantive text, every piece at
    # that identity stands in the ranked list as it stands today, so
    # the standing not derivable forms hold unchanged. The ranked
    # order itself, and every counting passage that rests on this
    # list, are unchanged.
    selected = {}
    for item in ranked:
        piece = item[3]
        if piece.text is not None and piece.text.strip() and \
                piece.identity not in selected:
            selected[piece.identity] = piece
    if selected:
        ranked = [item for item in ranked
                  if item[3].identity not in selected
                  or item[3] is selected[item[3].identity]]
    return ranked


def _f2_base_closures(ranked):
    """The closures standing in a step base gate record and ruling.

    Only the base forms count, the pieces whose file name carries
    no round or re-audit naming, as the F15-14 conflict guard has
    always read them.
    """
    closures = set()
    for item in ranked:
        piece = item[3]
        base_name = piece.paths[0].rsplit("/", 1)[-1]
        if piece.record_class in (CLS_GATE_RECORD, CLS_GATE_RULING) \
                and "round" not in base_name \
                and "reaudit" not in base_name and piece.text:
            found = _recorded_closure(piece.text)
            if found:
                closures.add(found)
    return closures


def _f2_first_closure(ranked):
    """The piece carrying a step first ruling, and its closure.

    One governing test in ranked order. The first piece carrying
    substantive text governs, closure or not: a governing piece
    carrying no closure in the settled forms leaves the step not
    derivable, whatever stands behind it, as the pinned head rule
    has always stated for a substantive head. A disagreement
    merged piece also governs, as contested: it carries no text
    of its own, because its copies disagree, and its copies
    closures are the contest the base closure conflict guard
    weighs, so it returns with a closure of None and the step is
    not derivable on that ground. Only pieces carrying neither
    substantive text nor a disagreement are passed over: a piece
    with no content at all, its text not read in full or empty,
    carries no closure either, and it does not erase a sound
    ruling at another alias form of the same step, so the scan
    continues past it to the governing piece. Where no governing
    piece stands in the group, the head piece stands with a
    closure of None, so the standing not derivable forms hold
    unchanged.
    """
    if not ranked:
        return None, None
    for item in ranked:
        piece = item[3]
        if piece.text is not None and piece.text.strip():
            return piece, _recorded_closure(piece.text)
        if piece.text is None and piece.not_read_reason and \
                "duplicate content disagreement" in \
                piece.not_read_reason:
            return piece, None
    return ranked[0][3], None


def _derive_f2(captured, universe):
    gates = captured.pieces_of(*GATE_CLASSES)
    pointer = None
    for p in captured.pieces_of(CLS_SNAPSHOT):
        if p.text and "steps ruled on" in p.text:
            pointer = p.paths[0]
            break
    if pointer is None:
        pointer = gates[0].paths[0] if gates else \
            (captured.first_path(CLS_STEP_RECORD) or "steps/step-01-record.md")
    history_steps = []
    for s in sorted(universe.evidenced):
        if captured.step_pieces(s, *GATE_CLASSES):
            continue
        for p in captured.step_pieces(s, CLS_STEP_RECORD):
            if p.text and "gate history" in p.text.lower():
                history_steps.append(s)
                break
    if not gates and not history_steps:
        return DerivationResult(
            "F-2", "missing", "no rate figure",
            "denominator steps ruled on, with plain approvals and "
            "qualified approvals as two subcounts under that one "
            "denominator", pointer,
            shows="no gate record, gate ruling or gate adjudication "
                  "stands in the tree for any step",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing",
            rule_name="F-2 feeder standing rule")
    plain = 0
    qualified = 0
    ruled = 0
    not_derivable = []
    unruled = []
    not_approved = []
    recycled_notes = []
    adjudication_only = []
    keeper_note = None
    for s in sorted(universe.evidenced):
        ranked = _f2_ranked_pieces(captured, s)
        if not ranked:
            if s in history_steps:
                not_derivable.append(s)
            else:
                unruled.append(s)
            continue
        regates = [item for item in ranked
                   if item[3].record_class == CLS_REGATE_RECORD]
        closure = None
        if regates:
            if len(_f2_base_closures(ranked)) > 1:
                not_derivable.append(s)
                continue
            first, closure = _f2_first_closure(ranked)
            if first is not None and \
                    first.record_class == CLS_GATE_ADJUDICATION:
                adjudication_only.append(s)
            # The recycled note scan rests on the same base gate
            # record and gate ruling pieces as the conflict guard
            # above, so the note can never name a closure the
            # counting does not rest on. A first ruling standing
            # outside that pair counts in the non regate form.
            for item in ranked:
                piece = item[3]
                base_name = piece.paths[0].rsplit("/", 1)[-1]
                if piece.record_class not in (CLS_GATE_RECORD,
                                              CLS_GATE_RULING) \
                        or "round" in base_name \
                        or "reaudit" in base_name:
                    continue
                if piece.text:
                    earlier = _recorded_closure(piece.text)
                    if earlier in ("CLOSED-FAIL", "RECYCLED", "FAIL"):
                        recycled_notes.append(
                            "Step %d ran as two instances with the first "
                            "instance closed %s" % (s, earlier))
                        not_approved.append(s)
                        break
        else:
            if len(_f2_base_closures(ranked)) > 1:
                not_derivable.append(s)
                continue
            first, closure = _f2_first_closure(ranked)
            if first is not None and \
                    first.record_class == CLS_GATE_ADJUDICATION:
                adjudication_only.append(s)
        if closure is None:
            not_derivable.append(s)
        elif closure == "CLOSED-PASS":
            plain += 1
            ruled += 1
        elif closure == "CLOSED-QUALIFIED":
            qualified += 1
            ruled += 1
        elif closure in ("CLOSED-FAIL", "RECYCLED", "FAIL"):
            ruled += 1
            if s not in not_approved:
                not_approved.append(s)
        else:
            not_derivable.append(s)
        if s == 22 and closure:
            for item in ranked:
                piece = item[3]
                if piece.text and "Keeper" in piece.text:
                    keeper_note = (
                        "Step 22 is classed by content as that step gate "
                        "record with closure %s" % closure)
                    break
    denom = ("denominator %d steps ruled on, with plain approvals and "
             "qualified approvals as two subcounts under that one "
             "denominator" % ruled)
    if unruled:
        denom += ("; " + _step_list_text(unruled) +
                  " named, no gate record or gate ruling stands for "
                  "that step")
    subcounts = ("plain approvals %d; qualified approvals %d; steps "
                 "ruled on %d" % (plain, qualified, ruled))
    note_parts = list(recycled_notes)
    for s in sorted(set(not_approved) - set(
            n for n in not_approved
            if any(note.startswith("Step %d " % n)
                   for note in recycled_notes))):
        note_parts.append("Step %d ruled and not approved" % s)
    if not_derivable:
        facts = []
        classes = {p.record_class for p in gates}
        if CLS_GATE_RECORD in classes and CLS_GATE_RULING in classes:
            facts.append("first ruling outcomes stand in gate files "
                         "under both gate names")
        for s in adjudication_only:
            if s in not_derivable:
                facts.append("Step %d first ruling stands only in its "
                             "gate adjudication" % s)
        facts.extend(recycled_notes)
        if keeper_note:
            facts.append(keeper_note)
        facts.append("the steps named here carry no first ruling "
                     "outcome in the settled forms: " +
                     _named_steps(not_derivable))
        figures = "no rate figure; " + subcounts
        for p in captured.pieces_of(CLS_SNAPSHOT):
            if p.text and p.step is not None:
                m = re.search(r"(\d+) of (\d+) steps ruled on", p.text)
                if m:
                    figures += ("; the only stated figure is the "
                                "provisional snapshot figure %s of %s "
                                "steps ruled on at Step %d"
                                % (m.group(1), m.group(2), p.step))
                    break
        if note_parts and not recycled_notes:
            figures += "; " + "; ".join(note_parts)
        return DerivationResult(
            "F-2", "present but not derivable", figures, denom, pointer,
            shows=", ".join(facts),
            code_token="missing-field",
            follows="missing-field one or more step contributions are "
                    "not derivable in the settled forms, so no rate is "
                    "printed",
            rule_name="F-2 first ruling rule")
    if ruled == 0:
        return DerivationResult(
            "F-2", "present but not derivable",
            "no rate figure; " + subcounts, denom, pointer,
            shows="gate pieces stand in the tree and no step has been "
                  "ruled on, so the denominator of steps ruled on is zero",
            code_token="missing-field",
            follows="missing-field the ruling outcome field is absent "
                    "for every step, so no rate is printed",
            rule_name="F-2 empty denominator rule")
    rate = (plain + qualified) * 100.0 / ruled
    figures = ("first-time approval rate %s percent; %s"
               % (_fmt_num(rate), subcounts))
    extra_notes = list(recycled_notes)
    if recycled_notes:
        extra_notes = [note + ", and that first instance was not "
                              "approved; the recycled step counts once"
                       for note in recycled_notes]
    plain_not_approved = [s for s in sorted(set(not_approved))
                          if not any(note.startswith("Step %d " % s)
                                     for note in recycled_notes)]
    for s in plain_not_approved:
        extra_notes.append("Step %d ruled and not approved" % s)
    if extra_notes:
        figures += "; " + "; ".join(extra_notes)
    return DerivationResult("F-2", "present", figures, denom, pointer,
                            rule_name="F-2 first ruling rule")


# ------------------------------------------------------- Q-1, Q-3, Q-4

_SEV_RE = re.compile(r"(Critical|High|Medium|Low)\s+(\d+)")


def _sev_counts_in(line):
    counts = {}
    for name, value in _SEV_RE.findall(line):
        if name not in counts:
            counts[name] = int(value)
    return counts


def _fmt_sev(counts):
    return ", ".join("%s %d" % (name, counts[name]) for name in counts)


def _repair_cited(piece):
    """Whether a piece repairs its own truncation in place.

    The recognition marker is a Completion section inside the same
    piece, standing after the truncated part, headed Completion
    section, stating that the piece was found truncated and
    identifying its piece as this file, which supplies the missing
    content in place.
    """
    if piece.text is None:
        return False
    base = piece.paths[0].rsplit("/", 1)[-1]
    return ("Completion section" in piece.text and
            "found truncated" in piece.text and base in piece.text and
            "supplies the missing content in place" in piece.text)


def _is_truncated_piece(piece):
    if piece.text is None or _repair_cited(piece):
        return False
    lines = [line for line in piece.text.splitlines() if line.strip()]
    if not lines:
        return False
    last = lines[-1].strip()
    if "[truncated" in last:
        return True
    if piece.record_class != CLS_AUDIT_PAPER:
        return False
    if last.startswith(("#", "|", "-", "*")):
        return False
    return not last.endswith((".", "!", "?", ":", "`", '"'))


def _accepted_breakdown(piece):
    """Post triage severity breakdown in a round record, or None.

    Accepted forms under G-06: a line that states it is post triage
    carrying severity counts, in any round record; a Totals line in
    a gate adjudication table or in a register; and a verdict
    summary line, a verdict grade or a no finding outstanding
    statement carrying the four severity counts. Pre triage lines,
    attack totals and fresh break lines never qualify.
    """
    if piece.text is None:
        return None
    for line in piece.text.splitlines():
        counts = _sev_counts_in(line)
        if not counts:
            continue
        low = line.lower()
        if "pre triage" in low or "pre-triage" in low:
            continue
        if "attack" in low or "fresh breaks" in low:
            continue
        if "post triage" in low or "post-triage" in low:
            return counts, line
        if piece.record_class in (CLS_GATE_ADJUDICATION, CLS_ADJUDICATION,
                                  CLS_FIX_REGISTER, CLS_DEFECT_REGISTER) \
                and "totals" in low:
            return counts, line
        if "verdict grade" in low or "no finding is outstanding" in low:
            return counts, line
    return None


def _round_number_for_piece(piece):
    name = piece.paths[0].rsplit("/", 1)[-1]
    m = re.search(r"round(\d+)", name)
    if m:
        return int(m.group(1))
    m = re.search(r"reaudit-(\d+)", name)
    if m:
        return int(m.group(1)) + 1
    if "reaudit" in name:
        return 2
    m = re.search(r"fix-register-(\d+)", name)
    if m:
        return int(m.group(1))
    if piece.text:
        for line in piece.text.splitlines()[:3]:
            if line.startswith("#"):
                m = re.search(r"Round (\d+)", line)
                if m:
                    return int(m.group(1))
    return 1


def _governing_rounds(captured):
    """Governing severity scale statements for Q-1, under G-07 and WV-6.

    Returns (governing, conflict_round_numbers). A later governing
    statement that states it resolves the conflict supersedes the
    conflict for the rounds it names.
    """
    governing = {}
    conflict = set()
    order = (CLS_GATE_ADJUDICATION, CLS_ADJUDICATION)
    for p in captured.pieces_of(*order):
        if p.text is None:
            continue
        resolves = "resolves the conflict" in p.text.lower()
        statements = []
        for m in re.finditer(r"Scale (\w+) governs Rounds? ([0-9, and]+)",
                             p.text):
            rounds = {int(x) for x in re.findall(r"\d+", m.group(2))}
            statements.append((m.group(1), rounds))
        for m in re.finditer(
                r"commissioned severity scale governs Rounds? "
                r"([0-9, and]+)", p.text, re.I):
            rounds = {int(x) for x in re.findall(r"\d+", m.group(1))}
            statements.append(("commissioned scale", rounds))
        for scale, rounds in statements:
            if resolves:
                for r in rounds:
                    governing[r] = scale
                    conflict.discard(r)
                continue
            for r in rounds:
                if r in governing and governing[r] != scale:
                    conflict.add(r)
                else:
                    governing.setdefault(r, scale)
    return governing, conflict


def _q1_rounds(captured):
    """Audit rounds evidenced in the tree, keyed by (step, round)."""
    rounds = {}

    def entry(key):
        return rounds.setdefault(key, {"pieces": [], "breakdown": None,
                                       "source": None, "line": None,
                                       "truncated": False,
                                       "attack_numbers": None})

    sources = captured.pieces_of(CLS_AUDIT_PAPER, CLS_FIX_REGISTER,
                                 CLS_DEFECT_REGISTER, CLS_GATE_RULING)
    for p in sources:
        if p.step is None:
            continue
        key = (p.step, _round_number_for_piece(p))
        e = entry(key)
        e["pieces"].append(p)
        found = _accepted_breakdown(p)
        if found and e["breakdown"] is None:
            e["breakdown"], e["line"] = found
            e["source"] = p
        if _is_truncated_piece(p):
            e["truncated"] = True
        if p.text:
            m = re.search(r"(\d+) numbered attacks", p.text)
            if m:
                e["attack_numbers"] = int(m.group(1))
            elif any("attack" in line.lower() and "total" in line.lower()
                     and _sev_counts_in(line)
                     for line in p.text.splitlines()):
                e["attack_numbers"] = e["attack_numbers"] or 0
    for p in captured.pieces_of(CLS_GATE_ADJUDICATION, CLS_ADJUDICATION):
        if p.step is None:
            continue
        found = _accepted_breakdown(p)
        if not found:
            continue
        key = (p.step, _round_number_for_piece(p))
        e = entry(key)
        e["pieces"].append(p)
        if e["breakdown"] is None:
            e["breakdown"], e["line"] = found
            e["source"] = p
    return rounds


def _derive_q1(captured, universe):
    registers = captured.pieces_of(CLS_FIX_REGISTER)
    papers = captured.pieces_of(CLS_AUDIT_PAPER, CLS_ADJUDICATION,
                                 CLS_GATE_ADJUDICATION)
    if registers:
        pointer = max(registers, key=lambda p: p.size).paths[0]
    elif papers:
        pointer = papers[0].paths[0]
    else:
        pointer = captured.metrics_single_path or \
            "wiki/wiki/synthesis/build-metrics-record.md"
    rounds = _q1_rounds(captured)
    governing, conflict_numbers = _governing_rounds(captured)
    if not rounds and not conflict_numbers:
        return DerivationResult(
            "Q-1", "missing", "no count figure",
            "denominator population audit rounds evidenced in the "
            "tree: none; excluded: none", pointer,
            shows="no audit round is evidenced in the tree, so the "
                  "population the metric counts over is empty",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing, with its empty "
                    "population stated",
            rule_name="Q-1 empty population rule")
    # Mixed severity scales stated on breakdown lines, with no
    # governing statement, block the rounds that state them (D-10).
    scale_by_round = {}
    for key, e in rounds.items():
        if e["line"]:
            m = re.search(r"on Scale (\w+)", e["line"])
            if m:
                scale_by_round[key] = m.group(1)
    mixed_blocked = set()
    if len(set(scale_by_round.values())) > 1 and not governing:
        mixed_blocked = set(scale_by_round)
    qualifying = {}
    excluded = []
    for key in sorted(rounds):
        step, rnd = key
        e = rounds[key]
        name = "Step %d Round %d" % (step, rnd)
        if rnd in conflict_numbers or key in mixed_blocked:
            excluded.append((key, "governing scale conflict"))
        elif e["breakdown"] is not None:
            qualifying[key] = e
        elif e["attack_numbers"] is not None:
            excluded.append((key, "the round totals grade attacks, "
                                  "not triaged findings"))
        elif e["truncated"]:
            excluded.append((key, "truncated with no correcting "
                                  "record, and the round is marked "
                                  "incomplete"))
        else:
            excluded.append((key, "no post triage breakdown"))
    for r in sorted(conflict_numbers):
        if all(key[1] != r for key in rounds):
            excluded.append(((None, r), "governing scale conflict"))
            excluded.sort(key=lambda item: (item[0][0] is None,
                                            item[0][0] or 0, item[0][1]))
    excl_text = "; ".join(
        "%s excluded: %s" % (
            "Round %d" % key[1] if key[0] is None else
            "Step %d Round %d" % key, reason)
        for key, reason in excluded)
    count_bits = []
    for key in sorted(qualifying):
        e = qualifying[key]
        adjective = "adjudicated breakdown" if e["source"].record_class \
            in (CLS_GATE_ADJUDICATION, CLS_ADJUDICATION) else "breakdown"
        count_bits.append("Step %d Round %d %s %s"
                          % (key[0], key[1], adjective,
                             _fmt_sev(e["breakdown"])))
    counts_label = "bounded counts" if excluded else "counts"
    denom = ("denominator population audit rounds evidenced in the "
             "tree, stated before the counts; excluded: %s; %s: %s"
             % (excl_text or "none", counts_label,
                "; ".join(count_bits) if count_bits else "none"))
    # Shows, built from the records that stand in this tree.
    clauses = []
    table_empty, stale = _metrics_table_empty(captured, "Audit round table")
    if table_empty:
        clauses.append("the audit round table is empty with stale text")
    if registers:
        biggest = max(registers, key=lambda p: p.size)
        entries = None
        if biggest.text:
            m = re.search(r"[Ff]indings and checks registered:\s*(\d+)",
                          biggest.text)
            if m:
                entries = int(m.group(1))
        if entries is not None:
            clauses.append("the Step %d fix register holds %d entries "
                           "with no severity breakdown"
                           % (biggest.step, entries))
            for p in captured.step_pieces(biggest.step, CLS_AUDIT_PAPER):
                if p.text and "red" in p.paths[0]:
                    for line in p.text.splitlines():
                        counts = _sev_counts_in(line)
                        if counts and "totals" in line.lower():
                            clauses.append(
                                "the Step %d Red paper totals %s are "
                                "pre triage paper counts"
                                % (biggest.step, _fmt_sev(counts)))
                            break
                    break
    for key in sorted(rounds):
        e = rounds[key]
        if e["attack_numbers"]:
            clauses.append("the Step %d totals grade %d numbered "
                           "attacks, not triaged findings"
                           % (key[0], e["attack_numbers"]))
            break
    statement = None
    for key in sorted(qualifying):
        e = qualifying[key]
        src = e["source"]
        if src is not None and src.text and \
                "corrected total" in src.text.lower():
            truncated_names = [p.paths[0] for p in e["pieces"]
                               if _is_truncated_piece(p)]
            if truncated_names:
                statement = ("source citation: %s, the correcting "
                             "record that names the corrected total "
                             "for the truncated paper %s."
                             % (src.paths[0], truncated_names[0]))
    if conflict_numbers or mixed_blocked:
        blocked = sorted(conflict_numbers) or \
            sorted({key[1] for key in mixed_blocked})
        if mixed_blocked and not conflict_numbers:
            clauses.append("the rounds state mixed severity scales, "
                           "Scale %s among them, with no governing "
                           "statement for the tree"
                           % " and Scale ".join(
                               sorted(set(scale_by_round.values()))))
        else:
            clauses.append("governing adjudications conflict over %s, "
                           "and the conflict is not resolved by a later "
                           "governing statement"
                           % _join_names(["Round %d" % r for r in blocked]))
        return DerivationResult(
            "Q-1", "present but not derivable", "bounded counts only",
            denom, pointer,
            shows=", ".join(clauses) if clauses else
                  "two governing adjudications claim the severity "
                  "scale for the same rounds in conflict",
            code_token="governing-scale-conflict",
            follows="governing adjudications in conflict govern the "
                    "covered rounds, so no count stands for those "
                    "rounds, and rounds outside the covered rounds "
                    "are judged on their own records",
            statement=statement,
            rule_name="Q-1 conflicting governing adjudications rule")
    truncated_only = [key for key, reason in excluded
                      if reason.startswith("truncated")]
    if truncated_only and not qualifying and \
            len(truncated_only) == len(excluded):
        key = truncated_only[0]
        return DerivationResult(
            "Q-1", "present but not derivable", "no count figure",
            denom, pointer,
            shows="the audit paper for Step %d Round %d is truncated "
                  "and no correcting record in the tree names a "
                  "corrected total for it, and the round is marked "
                  "incomplete" % key,
            code_token="truncated-no-correcting-record",
            follows="a truncated paper visible part is counted only "
                    "where a correcting record names the corrected "
                    "total, so no count stands for the round",
            statement=statement,
            rule_name="Q-1 truncation rule")
    if not excluded and qualifying:
        return DerivationResult(
            "Q-1", "present", "severity counts for every round in "
            "the population", denom, pointer,
            statement=statement,
            rule_name="Q-1 post triage rule")
    if not clauses:
        clauses.append("some rounds state a post triage breakdown "
                       "and the rest state none, so the row stands "
                       "in bounded form")
    return DerivationResult(
        "Q-1", "present but not derivable", "bounded counts only",
        denom, pointer,
        shows=", ".join(clauses),
        code_token="no-post-triage-breakdown",
        follows="only rounds whose own records state post triage "
                "breakdowns contribute bounded counts, round by "
                "round for those rounds only",
        statement=statement,
        rule_name="Q-1 bounded form rule")


def _derive_q3(captured, universe):
    from metrics_starter_collector.cross_check import \
        q3_contested_statement
    pointer = captured.metrics_single_path or \
        "wiki/wiki/synthesis/build-metrics-record.md"
    denom = ("denominator population register entries that carry a "
             "defect triage disposition")
    registers = captured.pieces_of(CLS_DEFECT_REGISTER, CLS_FIX_REGISTER)
    zero_printed = False
    if captured.assembled_metrics and re.search(
            r"Escapes attributed[^\n]*\b0\b", captured.assembled_metrics):
        zero_printed = True
    register_zero = False
    own_basis = False
    for p in registers:
        if p.text is None:
            continue
        if re.search(r"[Ee]scaped defects[^.\n]*\b0\b", p.text) or \
                re.search(r"[Ee]scapes[^.\n]*printed as 0", p.text):
            register_zero = True
        if re.search(r"[Mm]easurement basis:", p.text):
            own_basis = True
    correcting = None
    for p in captured.pieces:
        if p.text is None or p in registers:
            continue
        if p.record_class == CLS_METRICS_SINGLE:
            continue
        low = p.text.lower()
        if "zero for escaped defects" in low and \
                "measurement basis" in low:
            correcting = p
            break
    origin_steps = []
    for p in registers:
        if p.text is None:
            continue
        for line in p.text.splitlines():
            if "disposition" not in line.lower():
                continue
            m = re.search(r"origin step Step (\d+)", line)
            if m:
                origin_steps.append(int(m.group(1)))
    figures_zero = ("no escaped defect figure; the printed zero is "
                    "never stated as a measured zero")
    if correcting is not None and (register_zero or zero_printed):
        return DerivationResult(
            "Q-3", "present",
            "escaped defects 0, a measured zero whose measurement "
            "basis is supplied by a correcting record", denom,
            registers[0].paths[0] if registers else pointer,
            statement="source citation: %s, the correcting record "
                      "that names the zero for escaped defects and "
                      "states its measurement basis."
                      % correcting.paths[0],
            rule_name="Q-3 correcting record basis rule")
    if own_basis and register_zero:
        return DerivationResult(
            "Q-3", "present",
            "escaped defects 0, a measured zero with its measurement "
            "basis stated in the register", denom,
            registers[0].paths[0],
            statement="the register states the measurement basis for "
                      "the zero it prints, so the zero counts as a "
                      "measured zero.",
            rule_name="Q-3 measured zero rule")
    if zero_printed or register_zero:
        shows = ("no origin step field stands on any finding, fix "
                 "entry or defect item in the tree")
        table_steps = sorted(set(int(m.group(1)) for m in re.finditer(
            r"^\|\s*(\d+)\.\s", captured.assembled_metrics or "", re.M)))
        if zero_printed and table_steps:
            shows += (", and the cross check table prints Escapes "
                      "attributed as 0 on every row for Steps %d to "
                      "%d with no measurement basis"
                      % (min(table_steps), max(table_steps)))
        else:
            shows += (", and a zero for escapes is printed with no "
                      "measurement basis stated for it")
        return DerivationResult(
            "Q-3", "present but not derivable", figures_zero, denom,
            pointer if zero_printed else registers[0].paths[0],
            shows=shows,
            code_token="no-measurement-basis",
            follows="a printed zero with no measurement basis is a "
                    "placeholder, so the metric is present but not "
                    "derivable",
            rule_name="Q-3 placeholder zero rule")
    if not registers:
        return DerivationResult(
            "Q-3", "missing", "no figure stands", denom, pointer,
            shows="no defect register and no audit record carrying a "
                  "defect triage disposition stands in the tree",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="Q-3 feeder standing rule")
    contested = q3_contested_statement(captured, universe, origin_steps)
    if contested is not None:
        return DerivationResult(
            "Q-3", "present but not derivable", "no figure stands",
            denom, registers[0].paths[0],
            shows="a register entry carries an origin step field for "
                  "a step whose place in the step universe is "
                  "contested by another record",
            code_token="record-disagrees",
            follows="the contested origin step is carried on the "
                    "evidenced universe under the bridge rule, with "
                    "the disagreement named in the statement line, "
                    "so no escaped defect figure stands",
            statement=contested,
            rule_name="Q-3 contested origin step rule")
    return DerivationResult(
        "Q-3", "present but not derivable", "no figure stands", denom,
        registers[0].paths[0],
        shows="register entries stand in the tree and no origin step "
              "field that passes the acceptance test stands on them",
        code_token="missing-field",
        follows="the origin step field the derivation needs is "
                "absent from the register entries, so no figure stands",
        rule_name="Q-3 origin step rule")


_TRACE_RES = (
    re.compile(r"(\d+)\s+of\s+(\d+)\s+(?:checklist items\s+)?LANDED"),
    re.compile(r"LANDED:\s*(\d+)\s+of\s+(\d+)"),
    re.compile(r"[Ff]ull trace:?\s*(\d+)\s+of\s+(\d+)\s+LANDED"),
    re.compile(r"(\d+)\s+LANDED\s+and\s+\d+\s+PARTIAL\s+of\s+(\d+)"),
    re.compile(r"(\d+)\s+elements,\s+(\d+)\s+LANDED"),
)
_COUNTS_RE = re.compile(r"(\d+)\s+items checked\.\s+LANDED\s+(\d+)")
_NONLANDED_RE = re.compile(r"non-LANDED,?\s+(\d+)\s+in all")
_NONLANDED_BEFORE_RE = re.compile(r"(\d+)\s+non-LANDED in all")


def _nonlanded_count(text):
    """The largest non-LANDED in all count a piece states, or None.

    A piece that recounts a trace states both the header count it
    corrects and its own recount; the recount is the larger figure,
    and a piece that only restates the header count states the
    smaller one alone.
    """
    counts = [int(m.group(1)) for m in _NONLANDED_RE.finditer(text)]
    counts += [int(m.group(1))
               for m in _NONLANDED_BEFORE_RE.finditer(text)]
    return max(counts) if counts else None


_SUMMARY_FORMS = (
    (re.compile(r"Counts:\s*(\d+)\s+items checked\.\s*LANDED\s+(\d+)",
                re.I), True),
    (re.compile(r"Full trace:?\s*\**(\d+) of (\d+) LANDED", re.I), False),
    (re.compile(r"Elements:\s*(\d+)[.,]?\s*LANDED\s*(\d+)", re.I), True),
    (re.compile(r"(\d+) of (\d+) checklist items LANDED", re.I), False),
    (re.compile(r"(\d+) elements,\s*(\d+) LANDED", re.I), True),
)


def _summary_trace(piece):
    """Summary trace reading for one piece, under G-08 and G-09.

    Only summary tally forms count as a first trace of a step: a
    Counts line over items checked, a Full trace line, an Elements
    line, a checklist items tally, an elements tally, or the trace
    header pin rows form. Which forms a piece may offer depends on
    its class and its place in the record order, and a prose recount
    of another record trace is never the step first trace. Returns
    (landed, total) or None.
    """
    cls = piece.record_class
    text = piece.text
    name = piece.paths[0].rsplit("/", 1)[-1].lower()
    if cls == CLS_AUDIT_PAPER and "purple" not in name:
        return None
    if cls not in (CLS_TRACE, CLS_AUDIT_PAPER, CLS_GATE_RECORD,
                   CLS_GATE_RULING, CLS_BOARD_MEMBER):
        return None
    if cls in (CLS_GATE_RECORD, CLS_GATE_RULING, CLS_BOARD_MEMBER):
        allowed = _SUMMARY_FORMS[3:]
    elif cls == CLS_AUDIT_PAPER:
        allowed = _SUMMARY_FORMS[:2]
    else:
        allowed = _SUMMARY_FORMS
    # A summary tally line also states its PARTIAL count; a prose
    # mention of another record trace does not. Tally lines are
    # searched before the piece as a whole.
    tally_text = "\n".join(line for line in text.splitlines()
                           if "PARTIAL" in line)
    for haystack in (tally_text, text):
        for pattern, total_first in allowed:
            m = pattern.search(haystack)
            if m:
                first, second = int(m.group(1)), int(m.group(2))
                if total_first:
                    return second, first
                return first, second
    if cls == CLS_TRACE:
        m = re.search(r"Pin rows traced:\s*(\d+)", text)
        m2 = re.search(r"LANDED:\s*(\d+)\b", text)
        if m and m2:
            return int(m2.group(1)), int(m.group(1))
    return None


def _trace_candidates(captured, step):
    """First trace reading for one step, by record order with form
    precedence under G-08, plus the unreconciled totals evidence.

    Returns (found, totals, recount) where found is a list holding
    at most one (landed, total, piece) entry, totals the set of
    distinct totals the records state for the step, and recount a
    (recount piece, confirming piece, nonlanded count) triple or
    None.
    """
    found = []
    order = (CLS_TRACE, CLS_AUDIT_PAPER, CLS_GATE_RECORD, CLS_GATE_RULING,
             CLS_BOARD_MEMBER)
    for cls in order:
        pieces = list(captured.step_pieces(step, cls))
        if cls == CLS_AUDIT_PAPER:
            # Record order inside the audit papers: a round own paper
            # stands before its re-audit variants, and variants stand
            # in round order, so the first trace of a step is never
            # a later round re-trace.
            def paper_key(p):
                name = p.paths[0].rsplit("/", 1)[-1]
                variant = ("reaudit" in name or "round" in name)
                num = 0
                m = re.search(r"(?:reaudit|round)-?(\d+)", name)
                if m:
                    num = int(m.group(1))
                return (1 if variant else 0, num, name)
            pieces.sort(key=paper_key)
        for p in pieces:
            if p.text is None:
                continue
            reading = _summary_trace(p)
            if reading is None:
                continue
            found.append((reading[0], reading[1], p))
            break
        if found:
            break
    totals = set()
    recount = None
    if found:
        landed0, total0 = found[0][0], found[0][1]
        totals.add(total0)
        for cls in (CLS_BOARD_MEMBER, CLS_GATE_RECORD, CLS_GATE_RULING):
            for p in captured.step_pieces(step, cls):
                if p.text is None:
                    continue
                nonlanded = _nonlanded_count(p.text)
                if nonlanded is not None:
                    if landed0 + nonlanded != total0:
                        totals.add(landed0 + nonlanded)
                        if recount is None:
                            recount = [p, None, nonlanded]
        if recount is not None:
            for cls in (CLS_GATE_RECORD, CLS_GATE_RULING):
                for p in captured.step_pieces(step, cls):
                    if p.text is None or p is recount[0]:
                        continue
                    if _nonlanded_count(p.text) == recount[2]:
                        recount[1] = p
                        break
                if recount[1] is not None:
                    break
    return found, totals, recount


_Q4_CORRECTED_FIGURE_RES = (
    re.compile(r"corrected figure(?:\s+is)?\s*:?\s*(\d+)\s+of\s+(\d+)",
               re.I),
    re.compile(r"corrected total\s*:\s*(\d+)\s+of\s+(\d+)", re.I),
)
_Q4_CORRECTED_TOTAL_RES = (
    re.compile(r"corrected total[^.\n]{0,60}?\bis\s+(\d+)\b", re.I),
    re.compile(r"corrected total\s*:\s*(\d+)\b", re.I),
)


def _q4_correction(captured, trace_piece):
    """Correcting record for one first trace, under D-19 and WV-10.

    A correcting record is recognised where a piece other than the
    trace itself and other than the metrics record names the trace
    it corrects, by its path or by its file name, and states the
    corrected figure or the corrected total for that trace on the
    same line as the naming, in the forms the Q-1 and Q-3 limbs
    recognise: a corrected figure stated directly after the words
    corrected figure, a corrected total in colon form, or a
    corrected total stated with the word is close after the words
    corrected total. The scan follows the Q-3 correcting record
    scan: any piece in the tree can carry the correction, in the
    register form or in the audit paper form. Returns a triple
    (piece, landed, total) where landed is None where the record
    states a corrected total only, or None where no correcting
    record stands for the trace.
    """
    names = (trace_piece.paths[0],
             trace_piece.paths[0].rsplit("/", 1)[-1])
    for p in captured.pieces:
        if p is trace_piece or p.text is None:
            continue
        if p.record_class in (CLS_METRICS_SINGLE, CLS_METRICS_PAGE):
            continue
        for line in p.text.splitlines():
            if not any(name in line for name in names):
                continue
            for pattern in _Q4_CORRECTED_FIGURE_RES:
                m = pattern.search(line)
                if m:
                    return p, int(m.group(1)), int(m.group(2))
            for pattern in _Q4_CORRECTED_TOTAL_RES:
                m = pattern.search(line)
                if m:
                    return p, None, int(m.group(1))
    return None


def _derive_q4(captured, universe):
    from metrics_starter_collector.cross_check import \
        q4_cross_check_statement
    denom_base = "denominator steps with a first trace in the step universe"
    covered = {}
    corrections = {}
    unreconciled = {}
    zero_total = []
    analogue = []
    not_applicable = []
    trace_pieces = {}
    any_trace_piece = False
    for s in sorted(universe.evidenced):
        record_texts = _step_texts(captured, s, (CLS_STEP_RECORD,))
        joined = "\n".join(record_texts).lower()
        if "no trace applies" in joined:
            not_applicable.append(s)
            continue
        if "no fold in trace as such" in joined or \
                "no fold-in trace as such" in joined:
            analogue.append(s)
        found, totals, recount = _trace_candidates(captured, s)
        if captured.step_pieces(s, CLS_TRACE):
            any_trace_piece = True
        if not found:
            continue
        trace_pieces[s] = found[0][2]
        correction = _q4_correction(captured, found[0][2])
        if correction is not None:
            corr_piece, corr_landed, corr_total = correction
            landed = corr_landed if corr_landed is not None \
                else found[0][0]
            corrections[s] = (corr_piece, landed, corr_total,
                              corr_landed is not None)
            if corr_total == 0:
                zero_total.append(s)
                continue
            covered[s] = (landed, corr_total)
            continue
        if len(totals) > 1:
            unreconciled[s] = (found[0][0], sorted(totals), recount,
                               found[0][2])
            continue
        if found[0][1] == 0:
            zero_total.append(s)
            continue
        covered[s] = (found[0][0], found[0][1])
    if not covered and not unreconciled:
        if any_trace_piece:
            standing = captured.pieces_of(CLS_TRACE)
            return DerivationResult(
                "Q-4", "present but not derivable", "no figure stands",
                denom_base, standing[0].paths[0],
                shows="trace records stand in the tree and no "
                      "first trace in the defined form stands for any "
                      "step, so the present with coverage form does "
                      "not stand",
                code_token="missing-field",
                follows="the first trace field the derivation needs "
                        "is absent from the records as they stand, "
                        "and partial coverage without the defined "
                        "form is not present",
                rule_name="Q-4 first trace rule")
        return DerivationResult(
            "Q-4", "missing", "no figure stands", denom_base,
            captured.metrics_single_path or
            "wiki/wiki/synthesis/build-metrics-record.md",
            shows="no first trace record stands in the tree for this "
                  "metric",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the "
                    "tree, so the row is missing",
            rule_name="Q-4 feeder standing rule")
    figures_bits = []
    for s in sorted(set(list(covered) + list(unreconciled))):
        if s in covered:
            figures_bits.append("Step %d first trace %d of %d LANDED"
                                % (s, covered[s][0], covered[s][1]))
        else:
            landed, totals, recount, piece = unreconciled[s]
            if piece.record_class == CLS_TRACE and "Pin rows traced" in \
                    (piece.text or ""):
                figures_bits.append(
                    "Step %d trace header %d pin rows with LANDED %d"
                    % (s, totals[0], landed))
            else:
                figures_bits.append(
                    "Step %d first trace totals %s against %s with "
                    "LANDED %d" % (s, totals[0], totals[-1], landed))
    denom = denom_base
    remainder_bits = []
    statement_bits = []
    for s in sorted(unreconciled):
        landed, totals, recount, piece = unreconciled[s]
        remainder_bits.append(
            "remainder Step %d named as part of the remainder with "
            "both totals named, %d against %d, the LANDED count %d "
            "the same in every record form" % (s, totals[0],
                                               totals[-1], landed))
        if recount is not None:
            recount_name = recount[0].paths[0].rsplit("/", 1)[-1]
            confirm = ""
            if recount[1] is not None:
                confirm = " confirmed by %s" % \
                    recount[1].paths[0].rsplit("/", 1)[-1]
            statement_bits.append(
                "Present under the present with coverage form "
                "together with the unreconciled step total rule: "
                "Step %d forms no landed share because its trace "
                "states two totals that do not reconcile, the trace "
                "header at %d and the board recount at %d in %s%s, "
                "and the remainder naming with both totals stands as "
                "the complete marking for that step."
                % (s, totals[0], totals[-1], recount_name, confirm))
    for s in analogue:
        remainder_bits.append("remainder Step %d named as an analogue "
                              "only step" % s)
    for s in zero_total:
        remainder_bits.append("remainder Step %d named with its zero "
                              "total" % s)
    if remainder_bits:
        denom += "; " + "; ".join(remainder_bits)
    for s in not_applicable:
        denom += ("; Step %d not applicable, excluded from the "
                  "population" % s)
    pointer = None
    for s in sorted(trace_pieces):
        if trace_pieces[s].record_class == CLS_TRACE:
            pointer = trace_pieces[s].paths[0]
            break
    if pointer is None and trace_pieces:
        pointer = trace_pieces[sorted(trace_pieces)[0]].paths[0]
    if pointer is None:
        pointer = captured.metrics_single_path or \
            "wiki/wiki/synthesis/build-metrics-record.md"
    cross = q4_cross_check_statement(captured, covered)
    if statement_bits:
        statement = " ".join(statement_bits)
    else:
        statement = ("present under the present with coverage form: "
                     "the covered steps stand in the figures and the "
                     "remainder steps are named in the denominator.")
    if cross is not None:
        statement = (statement + " " + cross) if statement_bits \
            else cross
    citations = []
    for s in sorted(corrections):
        corr_piece, landed, total, stated_figure = corrections[s]
        if stated_figure:
            citations.append(
                "source citation: %s, the correcting record that "
                "names the trace %s and states the corrected figure "
                "%d of %d LANDED."
                % (corr_piece.paths[0], trace_pieces[s].paths[0],
                   landed, total))
        else:
            citations.append(
                "source citation: %s, the correcting record that "
                "names the trace %s and states the corrected total %d."
                % (corr_piece.paths[0], trace_pieces[s].paths[0],
                   total))
    if citations:
        statement = (statement + " " + " ".join(citations)) \
            if statement else " ".join(citations)
    return DerivationResult("Q-4", "present", "; ".join(figures_bits),
                            denom, pointer,
                            statement=statement,
                            rule_name="Q-4 present with coverage rule")


# ------------------------------------------------------------- D-1

def _decision_items(text):
    """Parse decision item rows from a text holding an item table."""
    if not text:
        return None
    lines = text.splitlines()
    header_at = None
    for idx, line in enumerate(lines):
        if line.strip().startswith("|") and "Item" in line and \
                "Ruled" in line and "Raised" in line:
            header_at = idx
            break
    if header_at is None:
        return None
    items = []
    idx = header_at + 1
    while idx < len(lines):
        line = lines[idx]
        idx += 1
        stripped = line.strip()
        if not stripped.startswith("|"):
            if not items:
                continue
            # A split form page boundary can stand between the rows
            # of one table in the assembled record: a page heading
            # and its page order line, with no new table header on
            # the next page. Any other text ends the table, so a
            # later table in the same record is never read as more
            # rows of this one.
            run = [stripped]
            while idx < len(lines) and \
                    not lines[idx].strip().startswith("|"):
                run.append(lines[idx].strip())
                idx += 1
            is_page_break = any(
                text.startswith("Page order:") or
                (text.startswith("#") and "page" in text.lower())
                for text in run)
            if is_page_break and idx < len(lines):
                continue
            break
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 5:
            if items:
                break
            continue
        if cells[0] in ("Item", "---") or set(cells[0]) <= set("-: "):
            if items:
                break
            continue
        items.append({"item": cells[0], "origin": cells[1],
                      "raised": cells[2], "presented": cells[3],
                      "ruled": cells[4]})
    return items


def _item_latency_hours(item):
    raised = _parse_ts(item["raised"])
    ruled = _parse_ts(item["ruled"])
    if raised is None or ruled is None:
        return None
    return (ruled - raised).total_seconds() / 3600.0


def _median(values):
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def _d1_from_items(items, pointer, statement):
    denom = "denominator decision items in the governing feeder"
    ruled = []
    open_items = []
    date_only_items = []
    detail = []
    for item in items:
        latency = _item_latency_hours(item)
        raised_full = _parse_ts(item["raised"]) is not None
        ruled_full = _parse_ts(item["ruled"]) is not None
        if latency is not None:
            ruled.append(latency)
            detail.append("Item %s: raised %s, ruled %s, latency %s hours"
                          % (item["item"], item["raised"], item["ruled"],
                             _fmt_num(latency)))
        elif not item["ruled"]:
            open_items.append(item["item"])
        elif not raised_full or not ruled_full:
            date_only_items.append(item["item"])
        else:
            open_items.append(item["item"])
    if not ruled:
        shows = ("the governing feeder holds %d decision items and no "
                 "item is ruled: every item stands open or in date only "
                 "form, so no latency can form" % len(items))
        details = []
        for item in items:
            details.append(
                "Item %s: raised %s, presented %s, ruled %s"
                % (item["item"], item["raised"] or "blank",
                   item["presented"] or "blank",
                   item["ruled"] or "blank"))
        if details:
            shows += "; " + "; ".join(details)
        if open_items:
            shows += "; open items named: " + ", ".join(open_items)
        figures = "no median and no longest figure stands"
        if open_items:
            figures = ("no median and no longest figure; items %s "
                       "named as open" % _join_names(open_items))
        return DerivationResult(
            "D-1", "present but not derivable", figures, denom, pointer,
            shows=shows,
            code_token="missing-field",
            follows="missing-field no item is ruled, so no latency, "
                    "median or longest can form, and an open item is "
                    "never counted as a latency of zero",
            statement=statement,
            rule_name="D-1 latency rule")
    figures = ("median %s hours; longest %s hours; %s"
               % (_fmt_num(_median(ruled)), _fmt_num(max(ruled)),
                  "; ".join(detail)))
    coverage = denom
    if open_items:
        coverage += "; open items named: " + ", ".join(open_items)
    if date_only_items:
        coverage += ("; date only items excluded and named: " +
                     ", ".join(date_only_items))
    return DerivationResult("D-1", "present", figures, coverage, pointer,
                            statement=statement,
                            rule_name="D-1 latency rule")


def _derive_d1(captured, universe):
    from metrics_starter_collector.cross_check import d1_cross_check_statement
    metrics_path = captured.metrics_single_path or \
        "wiki/wiki/synthesis/build-metrics-record.md"
    all_queue_pieces = captured.pieces_of(CLS_DECISION_QUEUE)
    queue_pieces = [p for p in all_queue_pieces
                    if p.paths[0] == "DECISION-QUEUE.md"]
    queue_items = None
    queue_unusable = False
    queue_pointer = "DECISION-QUEUE.md"
    if queue_pieces:
        piece = queue_pieces[0]
        if piece.text is not None:
            queue_items = _decision_items(piece.text)
        if queue_items is None:
            queue_unusable = True
    if queue_items is None:
        # A readable duplicate queue feeds the row where the
        # canonical queue piece carries no readable decision table,
        # as the ledger and metrics selections feed from a readable
        # piece where one stands.
        for piece in all_queue_pieces:
            if piece.paths[0] == "DECISION-QUEUE.md":
                continue
            if piece.text is None:
                continue
            items = _decision_items(piece.text)
            if items is not None:
                queue_items = items
                queue_pointer = piece.paths[0]
                queue_unusable = False
                break
    table_items = _decision_items(captured.assembled_metrics)
    if queue_items is not None:
        statement = ("the in tree %s in "
                     "the named form supplied the row, as the foundation "
                     "statement for this row." % queue_pointer)
        result = _d1_from_items(queue_items, queue_pointer, statement)
        extra = d1_cross_check_statement(
            result, table_items, feeder_items=queue_items,
            metrics_name=metrics_path.rsplit("/", 1)[-1])
        if extra:
            result.statement = (result.statement or "") + " " + extra
        return result
    if table_items:
        statement = ("the metrics record decision table "
                     "under the D-09 exception supplied the row, as the "
                     "foundation statement for this row.")
        result = _d1_from_items(table_items, metrics_path, statement)
        result.denominator += (
            ", the metrics record decision table under the D-09 "
            "exception, no DECISION-QUEUE.md in the named form "
            "standing in this tree")
        return result
    if queue_unusable:
        statement = ("a feeder record stood but was "
                     "unusable in form: the DECISION-QUEUE.md file at the "
                     "root supplied no row, as the foundation statement "
                     "for this row.")
        return DerivationResult(
            "D-1", "present but not derivable", "no figure stands",
            "denominator decision items in the governing feeder",
            "DECISION-QUEUE.md",
            shows="a file at the root carries the exact name for the "
                  "queue form and it holds no decision item table whose "
                  "rows carry the five stated fields, and no complete "
                  "decision table stands either",
            code_token="missing-field",
            follows="missing-field no complete feeder stands, so no "
                    "latency figure can form",
            statement=statement,
            rule_name="D-1 feeder selection rule")
    statement = ("no feeder stood: no DECISION-QUEUE.md "
                 "file in the named form stands and the metrics record "
                 "holds no decision table, as the foundation statement "
                 "for this row.")
    return DerivationResult(
        "D-1", "missing", "no figure stands",
        "denominator decision items in the governing feeder", metrics_path,
        shows="no queue file in the named form stands in the tree and "
              "the metrics record holds no decision table",
        code_token="no-feeder-record",
        follows="no feeder record for the metric exists in the tree, so "
                "the row is missing",
        statement=statement,
        rule_name="D-1 feeder selection rule")


# ------------------------------------------------------------- B family

def _derive_b1(captured, universe, t1, t2):
    metrics_path = captured.metrics_single_path or \
        "wiki/wiki/synthesis/build-metrics-record.md"
    denom = "denominator the whole build"
    derived = "T-1 and T-2"
    ledger = _ledger_piece(captured)
    gate_ruling = None
    gate_basis = None
    for p in captured.pieces_of(*GATE_CLASSES):
        if p.text and "Closing ruling" in p.text:
            for line in p.text.splitlines():
                if "Closing ruling" in line and FULL_TS_RE.search(line):
                    gate_ruling = p
                    gate_basis = ("UTC" if "UTC" in line else
                                  "CST" if "CST" in line else None)
                    break
        if gate_ruling:
            break
    ledger_basis = None
    ledger_first = False
    if ledger is not None and ledger.text is not None:
        for line in ledger.text.splitlines():
            if "Step" in line and FULL_TS_RE.search(line):
                ledger_first = True
                if "UTC" in line:
                    ledger_basis = "UTC"
                elif "CST" in line:
                    ledger_basis = "CST"
                m = re.search(r"basis stated as\s+(\w+)", line)
                if m:
                    ledger_basis = m.group(1)
                break
    if ledger_first and ledger_basis and gate_ruling is not None and \
            gate_basis != ledger_basis:
        return DerivationResult(
            "B-1", "present but not derivable", "no total figure stands",
            denom, ledger.paths[0],
            shows="the first timestamp in PATH-LEDGER.md states its "
                  "basis as %s and the closing ruling in %s states %s"
                  % (ledger_basis, gate_ruling.paths[0],
                     "no time basis" if gate_basis is None else
                     "its basis as " + gate_basis),
            code_token="no code fits",
            follows="no code fits the shared time basis for the cross "
                    "piece interval cannot be stated, so the elapsed "
                    "limb does not form and no total is printed",
            derived_from=derived,
            rule_name="B-1 shared time basis rule")
    if t1.verdict == "missing" and t2.verdict == "missing":
        closing_clause = ""
        for p in captured.pieces_of(*GATE_CLASSES):
            if p.text and re.search(
                    r"closing the build|build is complete|"
                    r"build stands complete", p.text, re.I):
                if p.step is not None:
                    closing_clause = (
                        " beside the Step %d %s closing the build"
                        % (p.step, p.record_class))
                break
        return DerivationResult(
            "B-1", "missing", "no elapsed or active figure", denom,
            metrics_path,
            shows="both inputs T-1 and T-2 are missing, no feeder "
                  "record holds a B-1 figure, and the build summary "
                  "states the whole build figures are not computed "
                  "yet" + closing_clause,
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists and a "
                    "never computed figure whose inputs are missing "
                    "is missing",
            derived_from=derived,
            rule_name="B-1 composition rule")
    if t1.verdict != "present" or t2.verdict != "present":
        blocker = "T-1" if t1.verdict != "present" else "T-2"
        code = t1.code_token if blocker == "T-1" else t2.code_token
        code = code or "missing-field"
        if code == "no code fits":
            code = "missing-field"
        return DerivationResult(
            "B-1", "present but not derivable", "no total figure stands",
            denom, metrics_path,
            shows="the input row %s does not stand present, so the "
                  "composed total cannot form" % blocker,
            code_token=code,
            follows=code + " the input that blocks the row is named in "
                    "the record shows part, and no total is printed "
                    "until both limbs form",
            derived_from=derived,
            rule_name="B-1 composition rule")
    intervals = _step_intervals(captured)
    total_active = sum(intervals.values())
    figures = ("total active %s hours; elapsed limb stands from the "
               "transition log" % _fmt_num(total_active))
    return DerivationResult("B-1", "present", figures, denom,
                            ledger.paths[0] if ledger else metrics_path,
                            derived_from=derived,
                            rule_name="B-1 composition rule")


def _b2_proxy_position(captured):
    """The documented units position at build close, or None.

    The position is the figure the latest step record states as
    its final or closing budget in documented units. It stands on
    a labelled proxy basis only: it is never a money or token
    figure, and this helper returns it only so the B-2 row can
    name it as a proxy, in that labelled form.
    """
    best = None
    for s in sorted({p.step for p in captured.pieces_of(CLS_STEP_RECORD)
                     if p.step is not None}):
        for p in captured.step_pieces(s, CLS_STEP_RECORD):
            if p.text is None:
                continue
            m = re.search(r"Final budget:\s*(\d+) of (\d+) documented "
                          r"units", p.text)
            if m is None:
                m = re.search(r"Budget at closure:\s*(\d+) of (\d+) "
                              r"documented units", p.text)
            if m:
                best = (int(m.group(1)), int(m.group(2)))
    return best


def _b2_tokens_not_recorded_clause(captured, universe):
    """The tokens NOT RECORDED clause for the B-2 reason, from the
    closing step records that state it in that form."""
    stated = [s for s in universe.evidenced
              if any(p.text and "tokens NOT RECORDED" in p.text
                     for p in captured.step_pieces(s, CLS_STEP_RECORD))]
    if not stated:
        return "with tokens stated as not recorded"
    if len(stated) >= 2 and stated[-1] == universe.evidenced[-1]:
        return ("with tokens NOT RECORDED in Steps %d and %d"
                % (stated[-2], stated[-1]))
    return "with tokens NOT RECORDED in " + _step_list_text(stated)


def _derive_b2(captured, universe):
    denom = "denominator the whole build budget in two limbs, money and tokens"
    led = _cost_ledger(captured)
    whole_piece, whole_value = _whole_build_money(captured)
    money_stand = bool(led["money"]) or led["budget_money"] is not None
    token_stand = bool(led["tokens"]) or led["budget_token"] is not None
    if led["pieces"] and (money_stand or token_stand):
        pointer = led["pieces"][0].paths[0]
        spent_money = sum(led["money"].values()) if led["money"] else None
        spent_token = sum(led["tokens"].values()) if led["tokens"] \
            else None
        if led["stated_money"] is not None and spent_money is not None \
                and spent_money != led["stated_money"]:
            return DerivationResult(
                "B-2", "present but not derivable",
                "money figures sum to %s against a stated build "
                "total of %s; no percentage stands"
                % (_fmt_num(spent_money),
                   _fmt_num(led["stated_money"])), denom, pointer,
                shows="the cost ledger states per step money figures "
                      "which sum to %s, and states a build total of "
                      "%s, and the two figures do not reconcile"
                      % (_fmt_num(spent_money),
                         _fmt_num(led["stated_money"])),
                code_token="unreconciled-figure",
                follows="unreconciled-figure the per step money "
                        "figures and the stated build total do not "
                        "reconcile, so no limb yields its percentage",
                rule_name="B-2 unreconciled figure rule")
        limbs = {}
        for limb, spent, budget, figures_map in (
                ("money", spent_money, led["budget_money"], led["money"]),
                ("token", spent_token, led["budget_token"], led["tokens"])):
            covered_steps = [s for s in universe.evidenced
                             if s in figures_map]
            partial = bool(figures_map) and universe.evidenced and \
                len(covered_steps) != len(universe.evidenced)
            if budget is not None and budget == 0 and \
                    (spent is not None or figures_map or
                     limb == "money"):
                limbs[limb] = ("undefined-zero", spent, budget,
                               covered_steps)
            elif budget is None and spent is not None:
                limbs[limb] = ("undefined-absent", spent, budget,
                               covered_steps)
            elif budget is not None and spent is not None and \
                    not partial:
                limbs[limb] = ("yields", spent, budget, covered_steps)
            elif not figures_map and budget is None:
                limbs[limb] = ("absent", spent, budget, covered_steps)
            else:
                limbs[limb] = ("blocked", spent, budget, covered_steps)
        if all(state == "yields" for state, _, _, _ in limbs.values()):
            figures = "; ".join(
                "%s spent %s against a %s budget of %s, %s percent"
                % (limb, _fmt_num(spent), limb, _fmt_num(budget),
                   _fmt_num(spent * 100.0 / budget))
                for limb, (state, spent, budget, _) in
                (("money", limbs["money"]), ("token", limbs["token"])))
            return DerivationResult("B-2", "present", figures, denom,
                                    pointer,
                                    rule_name="B-2 limb composition rule")
        segments = []
        shows_parts = []
        coverage_extra = []
        zero_limb = False
        partial_limb = False
        for limb, (state, spent, budget, covered_steps) in (
                ("money", limbs["money"]), ("token", limbs["token"])):
            label = "money" if limb == "money" else "token"
            if state == "yields":
                segments.append(
                    "%s spent %s against a %s budget of %s, %s percent"
                    % (label, _fmt_num(spent), label, _fmt_num(budget),
                       _fmt_num(spent * 100.0 / budget)))
                coverage_extra.append(
                    "%s limb yields its percentage: %s spent %s "
                    "against a %s budget of %s, %s percent"
                    % (label, label, _fmt_num(spent), label,
                       _fmt_num(budget),
                       _fmt_num(spent * 100.0 / budget)))
            elif state == "undefined-zero":
                zero_limb = True
                segments.append(
                    "%s spent %s against a %s budget of 0"
                    % (label,
                       _fmt_num(spent) if spent is not None else "nil",
                       label))
                shows_parts.append(
                    "a percentage against a budget of zero is "
                    "undefined for the %s limb" % label)
                if covered_steps and len(covered_steps) != \
                        len(universe.evidenced):
                    coverage_extra.append(
                        "%s covered span %s"
                        % (label, _step_list_text(covered_steps)))
            elif state == "undefined-absent":
                segments.append(
                    "%s spent %s stands and no %s budget figure stands"
                    % (label, _fmt_num(spent), label))
                shows_parts.append(
                    "a percentage against an absent budget is "
                    "undefined for the %s limb" % label)
            elif state == "absent":
                segments.append(
                    "%s spent and %s budget figures absent"
                    % (label, label))
                shows_parts.append(
                    "both the spent figure and the budget figure are "
                    "absent for the %s limb" % label)
            else:
                if covered_steps and len(covered_steps) != \
                        len(universe.evidenced):
                    partial_limb = True
                if covered_steps:
                    segments.append(
                        "%s figures stand for %s, no %s percentage "
                        "stands" % (label,
                                    _step_list_text(covered_steps),
                                    label))
                    shows_parts.append(
                        "the %s limb rests on a partial span, with "
                        "the covered span named in the coverage"
                        % label)
                    coverage_extra.append(
                        "%s covered span %s"
                        % (label, _step_list_text(covered_steps)))
                else:
                    segments.append("no %s percentage stands" % label)
                    shows_parts.append(
                        "the %s limb does not yield its percentage"
                        % label)
        if coverage_extra:
            denom += "; " + "; ".join(coverage_extra)
        if zero_limb:
            return DerivationResult(
                "B-2", "present but not derivable", "; ".join(segments),
                denom, pointer,
                shows="; ".join(shows_parts),
                code_token="no code fits",
                follows="no code fits a percentage against a budget of "
                        "zero is undefined, and no limb yields its "
                        "percentage in full, the undefined state is "
                        "reported as undefined and never as 0 and "
                        "never as 100, and no fitting code on the "
                        "closed list covers the zero budget limb ground",
                rule_name="B-2 zero budget rule")
        if partial_limb:
            return DerivationResult(
                "B-2", "present but not derivable", "; ".join(segments),
                denom, pointer,
                shows="; ".join(shows_parts),
                code_token="partial-span",
                follows="partial-span the row verdict follows the "
                        "weaker limb, with the covered span named in "
                        "the coverage and steps outside it not "
                        "reported as zero",
                rule_name="B-2 limb composition rule")
        return DerivationResult(
            "B-2", "present but not derivable", "; ".join(segments),
            denom, pointer,
            shows="; ".join(shows_parts),
            code_token="missing-field",
            follows="missing-field the row verdict follows the weaker "
                    "limb, and the blocking limb is named in the "
                    "record shows part",
            rule_name="B-2 limb composition rule")
    if whole_value == 0:
        figures = ("money spent nil against a money budget of 0; "
                   "token spent and token budget figures absent")
        proxy = _b2_proxy_position(captured)
        if proxy is not None:
            figures += ("; agent count position %d of %d documented "
                        "units stands on a labelled proxy basis and "
                        "is not entered as a money or token figure"
                        % proxy)
        return DerivationResult(
            "B-2", "present but not derivable", figures, denom,
            whole_piece.paths[0],
            shows="a percentage against a budget of zero is undefined "
                  "for the money limb, and both the spent figure and "
                  "the budget figure are absent for the token limb, "
                  + _b2_tokens_not_recorded_clause(captured, universe),
            code_token="no code fits",
            follows="no code fits a percentage against a budget of "
                    "zero is undefined, and no limb yields its "
                    "percentage in full, the undefined state is "
                    "reported as undefined and never as 0 and never "
                    "as 100, and no fitting code on the closed list "
                    "covers the zero budget limb ground",
            rule_name="B-2 zero budget rule")
    step_records = captured.pieces_of(CLS_STEP_RECORD)
    if step_records:
        return DerivationResult(
            "B-2", "present but not derivable", "no percentage stands",
            denom, step_records[0].paths[0],
            shows="no cost ledger stands in the tree, and neither "
                  "limb, money or tokens, yields its percentage from "
                  "the records that stand: no spent figure and no "
                  "budget figure stands for either limb",
            code_token="missing-field",
            follows="missing-field the row verdict follows the "
                    "weaker limb, and no limb yields its percentage "
                    "in full",
            rule_name="B-2 limb composition rule")
    return DerivationResult(
        "B-2", "missing", "no figure stands", denom,
        captured.first_path(CLS_STEP_RECORD) or "steps/step-01-record.md",
        shows="no cost ledger stands in the tree and neither limb, "
              "money or tokens, has any feeder record",
        code_token="no-feeder-record",
        follows="no feeder record for either limb exists in the "
                "tree, so the row is missing",
        rule_name="B-2 limb composition rule")


def _derive_b3_b4(captured, universe, t1, t2, code):
    metrics_path = captured.metrics_single_path or \
        "wiki/wiki/synthesis/build-metrics-record.md"
    denom = "denominator steps eligible for ranking"
    derived = "T-1 and T-2"
    label = "Slowest three steps" if code == "B-3" else "Fastest three steps"
    if t1.verdict == "missing" or t2.verdict == "missing":
        if code == "B-4" and t2.verdict == "missing":
            missing_text = "the input T-2 is missing"
        elif t1.verdict == "missing" and t2.verdict == "missing":
            missing_text = "both inputs T-1 and T-2 are missing"
        elif t1.verdict == "missing":
            missing_text = "the input T-1 is missing"
        else:
            missing_text = "the input T-2 is missing"
        return DerivationResult(
            code, "missing", "no ranking figure", denom, metrics_path,
            shows="no ranked list stands in the feeders and " +
                  missing_text,
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists and the "
                    "composed metric is missing where an input metric "
                    "is missing",
            derived_from=derived,
            rule_name=code + " composition rule")
    if t1.verdict != "present" or t2.verdict != "present":
        blocker = "T-1" if t1.verdict != "present" else "T-2"
        return DerivationResult(
            code, "present but not derivable", "no ranking figure", denom,
            metrics_path,
            shows="the input row %s does not stand present, so the "
                  "ranking cannot form" % blocker,
            code_token="missing-field",
            follows="missing-field the input that blocks the row is "
                    "named in the record shows part, so no ranking stands",
            derived_from=derived,
            rule_name=code + " composition rule")
    intervals = _step_intervals(captured)
    if code == "B-3":
        ordered = sorted(intervals.items(), key=lambda kv: (-kv[1], kv[0]))
    else:
        ordered = sorted(intervals.items(), key=lambda kv: (kv[1], kv[0]))
    top = ordered[:3]
    tied_steps = []
    if len(ordered) > 3:
        threshold = ordered[2][1]
        if any(value == threshold for _, value in ordered[3:]):
            top = ordered[:3] + [item for item in ordered[3:]
                                 if item[1] == threshold]
            tied_steps = [s for s, v in top if v == threshold]
    figures = label + ": " + "; ".join(
        "Step %d at %s hours" % (s, _fmt_num(v)) for s, v in top)
    if tied_steps:
        figures += ("; tied at %s hours: %s"
                    % (_fmt_num(ordered[2][1]), _each_step(tied_steps)))
    return DerivationResult(code, "present", figures,
                            denom + "; eligible steps %d" % len(intervals),
                            metrics_path, derived_from=derived,
                            rule_name=code + " ranking rule")


# ------------------------------------------------------------- assembly

_COMPOSED = ("B-1", "B-3", "B-4")


def _build_state(captured):
    """Return (state, piece) for the tree as a whole, under WV-5.

    A tree is halted only where a recognised piece states the halt in
    its own words in a single statement naming the build or the work:
    a statement carrying the word halted beside the word build or the
    word work. A tree is closed only where a recognised piece states
    a closing of the whole build. Every other tree stands in
    progress, and absence alone is never halt evidence.
    """
    for p in captured.pieces:
        if p.text is None:
            continue
        for segment in re.split(r"[.\n]", p.text):
            low = segment.lower()
            if "halted" in low and (re.search(r"\bbuild\b", low) or
                                    re.search(r"\bwork\b", low)):
                return "halted", p
    for p in captured.pieces:
        if p.text and re.search(r"closing the build|build is complete|"
                                r"build stands complete", p.text, re.I):
            return "closed", p
    return "in progress", None


def _t2_interval_duration_stands(captured):
    """Whether an interval duration stands in the transition log."""
    ledger = _ledger_piece(captured)
    if ledger is None or ledger.text is None:
        return False
    return _interval_duration_mentions_stand(ledger.text)


def _apply_version_refusal(captured, results):
    version = captured.definitions_version
    if version is None or _known_version(version):
        return
    by_code = {r.code: r for r in results}
    t2 = by_code["T-2"]
    if t2.verdict != "missing" and \
            not _t2_interval_duration_stands(captured):
        # On the Slice 4 variant no feeder record stands for T-2: the
        # transition log holds no interval duration from which an
        # active figure for T-2 could form, so the row stays missing
        # under the refusal, ahead of the generic limb below.
        t2.verdict = "missing"
        t2.figures = "no interval figure"
        t2.shows = ("no interval duration stands in the transition "
                    "log from which an active figure for this row "
                    "could form, and the tree states a definitions "
                    "version the tool does not know, named here as %s"
                    % version)
        t2.code_token = "no-feeder-record"
        t2.follows = ("no feeder record for the metric stands on "
                      "this tree, so the row is missing")
        t2.rule_name = t2.rule_name + "; WV-2 unknown version refusal"
    t7 = by_code["T-7"]
    if t7.verdict == "missing" and \
            captured.pieces_of(*GATE_CLASSES):
        # Gate verdict records stand for T-7 even where no loop step
        # is identified in the tree, so the row falls under the
        # refusal like every other metric whose feeder records stand.
        t7.verdict = "present but not derivable"
        t7.figures = "no figure stands"
        t7.shows = ("the tree states a definitions version the tool "
                    "does not know, named here as %s, in the build "
                    "header of the metrics record" % version)
        t7.code_token = "unknown-definitions-version"
        t7.follows = ("unknown-definitions-version every metric "
                      "whose feeder records stand falls to present "
                      "but not derivable, with the unknown version "
                      "named, and no value is guessed")
        t7.rule_name = t7.rule_name + "; WV-2 unknown version refusal"
    q4 = by_code["Q-4"]
    if q4.verdict == "missing" and \
            captured.pieces_of(*GATE_CLASSES):
        # Gate records are a named feeder kind for Q-4, so where
        # they stand the row falls under the refusal like every
        # other metric whose feeder records stand, even where no
        # first trace record stands for the row itself, in the
        # same form as the T-7 limb above.
        q4.verdict = "present but not derivable"
        q4.figures = "no figure stands"
        q4.shows = ("the tree states a definitions version the tool "
                    "does not know, named here as %s, in the build "
                    "header of the metrics record" % version)
        q4.code_token = "unknown-definitions-version"
        q4.follows = ("unknown-definitions-version every metric "
                      "whose feeder records stand falls to present "
                      "but not derivable, with the unknown version "
                      "named, and no value is guessed")
        q4.rule_name = q4.rule_name + "; WV-2 unknown version refusal"
    for result in results:
        if result.code in _COMPOSED:
            continue
        if result.verdict == "missing":
            continue
        if not _feeder_stands(captured, result.code):
            continue
        result.verdict = "present but not derivable"
        result.figures = "no figure stands"
        result.shows = ("the tree states a definitions version the tool "
                        "does not know, named here as %s, in the build "
                        "header of the metrics record" % version)
        result.code_token = "unknown-definitions-version"
        result.follows = ("unknown-definitions-version every metric "
                          "whose feeder records stand falls to present "
                          "but not derivable, with the unknown version "
                          "named, and no value is guessed")
        result.rule_name = result.rule_name + "; WV-2 unknown version refusal"
    for code in _COMPOSED:
        result = by_code[code]
        inputs = [by_code["T-1"], by_code["T-2"]]
        missing_inputs = [r.code for r in inputs
                          if r.verdict == "missing"]
        if missing_inputs and result.verdict != "missing":
            result.verdict = "missing"
            result.figures = "no elapsed or active figure" \
                if code == "B-1" else "no ranking figure"
            result.shows = ("the input row %s is missing, so the "
                            "composed row is missing"
                            % " and ".join(missing_inputs))
            result.code_token = "no-feeder-record"
            result.follows = ("the composed metric is missing where "
                              "an input metric is missing")
            result.rule_name = result.rule_name + \
                "; composition rule under WV-2"
        elif any(r.verdict == "present but not derivable" for r in inputs) \
                and result.verdict == "present":
            result.verdict = "present but not derivable"
            result.figures = "no figure stands"


def derive_report(captured):
    """Derive one ReportModel from one CapturedRead and nothing else."""
    if not captured.pieces:
        header = [
            "# Metrics starter set report",
            "Root: " + str(captured.root),
            "Build identity: no build identity was found in the tree",
            "Step universe: 0 steps",
            "0 pieces recognised",
            "Live line: latest record timestamp: " +
            (captured.latest_timestamp or "no timestamp was found"),
            "Coverage statement: no usable records stand in the tree, "
            "so the report carries no metric rows",
        ]
        return ReportModel(header, header[-1], ["## Piece inventory",
                                                "No piece stands."],
                           [], ["Datum line: the tree stated none for "
                                "the definitions version; form basis: "
                                "the settled forms of this version of "
                                "the tool."], no_usable=True)
    universe = build_step_universe(captured)
    results = {}
    results["T-1"] = _derive_t1(captured, universe)
    results["T-2"] = _derive_t2(captured, universe, results["T-1"])
    results["T-4"] = _derive_t4(captured, universe)
    results["T-7"] = _derive_t7(captured, universe)
    results["E-1"] = _derive_e1(captured, universe)
    results["E-2"] = _derive_e2(captured, universe)
    results["E-3"] = _derive_e3(captured, universe)
    results["E-4"] = _derive_e4(captured, universe)
    results["F-2"] = _derive_f2(captured, universe)
    results["Q-1"] = _derive_q1(captured, universe)
    results["Q-3"] = _derive_q3(captured, universe)
    results["Q-4"] = _derive_q4(captured, universe)
    results["D-1"] = _derive_d1(captured, universe)
    results["B-1"] = _derive_b1(captured, universe, results["T-1"],
                                results["T-2"])
    results["B-2"] = _derive_b2(captured, universe)
    results["B-3"] = _derive_b3_b4(captured, universe, results["T-1"],
                                  results["T-2"], "B-3")
    results["B-4"] = _derive_b3_b4(captured, universe, results["T-1"],
                                  results["T-2"], "B-4")
    ordered = [results[code] for code in STARTER_ORDER]
    from metrics_starter_collector.cross_check import \
        staffing_cross_check_statements
    covered_map = {}
    totals_map = {}
    for s in universe.evidenced:
        pair = _parse_staffed_base(captured, s)
        if pair:
            covered_map[s] = pair
        total = _parse_total_spins(captured, s)
        if total is not None:
            totals_map[s] = total
    f2_counted = set()
    for s in universe.evidenced:
        ranked = _f2_ranked_pieces(captured, s)
        if not ranked:
            continue
        # The counted test is the F-2 counting test itself, the
        # F15-14 base closure conflict guard included, so the cross
        # check statement claims only steps the counting counted.
        if len(_f2_base_closures(ranked)) > 1:
            continue
        _, counted_closure = _f2_first_closure(ranked)
        if counted_closure:
            f2_counted.add(s)
    for code, texts in staffing_cross_check_statements(
            captured, universe, covered_map, totals_map,
            f2_counted).items():
        result = results[code]
        joined = " ".join(texts)
        result.statement = (result.statement + " " + joined) \
            if result.statement else joined
    from metrics_starter_collector.cross_check import \
        cost_cross_check_statements
    cost_led = _cost_ledger(captured)
    cost_e4_money = dict(cost_led["money"])
    for step in _step_money_nil(captured):
        cost_e4_money.setdefault(step, 0.0)
    cost_b2_money = sum(cost_led["money"].values()) \
        if cost_led["money"] else None
    if cost_b2_money is None:
        _, cost_whole_value = _whole_build_money(captured)
        cost_b2_money = cost_whole_value
    cost_b2_token = sum(cost_led["tokens"].values()) \
        if cost_led["tokens"] else None
    for code, texts in cost_cross_check_statements(
            captured, dict(cost_led["tokens"]), cost_e4_money,
            cost_b2_money, cost_b2_token).items():
        result = results[code]
        joined = " ".join(texts)
        result.statement = (result.statement + " " + joined) \
            if result.statement else joined
    _apply_version_refusal(captured, ordered)

    build_state, halt_piece = _build_state(captured)
    if build_state != "closed":
        if build_state == "halted":
            state_note = ("the build stands halted, as the halt "
                          "naming for this row, stated in its own "
                          "words in %s."
                          % (halt_piece.paths[0] if halt_piece
                             else "a recognised piece"))
        else:
            state_note = ("the build stands in progress, as the open "
                          "state naming for this row.")
        for code in ("B-1", "B-2", "B-3", "B-4"):
            result = results[code]
            result.statement = (result.statement + " " + state_note) \
                if result.statement else state_note

    identity = captured.build_identity or \
        "no build identity was found in the tree"
    if universe.metrics_count_claim is not None and \
            universe.metrics_count_claim != len(universe.evidenced):
        metrics_name = "build-metrics-record.md"
        if captured.metrics_single_path:
            metrics_name = captured.metrics_single_path.rsplit("/", 1)[-1]
        universe_line = (
            "Step universe: disputed, %d steps stated in %s and %d "
            "steps evidenced by step records and gate files, neither "
            "count picked (%s)"
            % (universe.metrics_count_claim, metrics_name,
               len(universe.evidenced),
               _step_list_text(universe.evidenced)))
    else:
        universe_line = "Step universe: %d steps (%s)" % (
            len(universe.evidenced), _step_list_text(universe.evidenced))
    header = [
        "# Metrics starter set report",
        "Root: " + str(captured.root),
        "Build identity: " + identity,
        universe_line,
        "%d pieces recognised" % len(captured.pieces),
        "Live line: latest record timestamp: " +
        (captured.latest_timestamp or "no timestamp was found"),
    ]
    not_read = [p for p in captured.pieces if p.text is None]
    coverage_bits = []
    if build_state == "halted":
        coverage_bits.append(
            "the build stands halted: a recognised piece, %s, states "
            "the halt in its own words, and missing closing pieces "
            "count as missing pieces"
            % (halt_piece.paths[0] if halt_piece
               else "a recognised piece"))
    elif build_state == "in progress":
        missing_gate_steps = [
            s for s in universe.evidenced
            if not captured.step_pieces(s, *GATE_CLASSES)]
        state_bit = ("the build stands in progress: the closing "
                     "ruling for the build is absent, a missing piece")
        for s in missing_gate_steps:
            state_bit += ("; the closing ruling piece for Step %d "
                          "(step-%02d gate record) is a missing piece"
                          % (s, s))
        coverage_bits.append(state_bit)
    if universe.disagreements:
        coverage_bits.append("step universe disagreement stands: " +
                             "; ".join(universe.disagreements))
    if not_read:
        coverage_bits.append(
            "partial coverage: pieces not read in full: " + "; ".join(
                "%s (%d bytes, %s)" % (p.paths[0], p.size,
                                       p.not_read_reason or "not read in full")
                for p in not_read))
    if captured.walk_note:
        coverage_bits.append(captured.walk_note)
    if captured.tree_cut_paths:
        coverage_bits.append(
            "tree limit cut: the record part total of %d bytes in "
            "%d files crossed the %s, and the pieces past the limit "
            "were not read: %s"
            % (captured.tree_bytes, captured.tree_files,
               captured.tree_cut_kind or "tree limit",
               "; ".join(captured.tree_cut_paths)))
    if not coverage_bits:
        coverage_bits.append("the capture stands complete for the "
                             "pieces recognised")
    coverage = "Coverage statement: " + "; ".join(coverage_bits) + "."
    if build_state != "closed":
        header.append("Captured read statement: the verdicts in this "
                      "report are verdicts on the captured read.")
    for cls in sorted(captured.inventory_totals):
        totals = captured.inventory_totals[cls]
        header.append(
            "Class %s: expected %d, found %d"
            % (cls, totals["expected"], totals["found"]))
        header.append(
            "Class %s: not found %d" % (cls, totals["not_found"]))
        header.append(
            "Class %s: not yet recordable %d"
            % (cls, totals["not_yet_recordable"]))
    header.append(coverage)

    inventory_lines = ["## Piece inventory"]
    if captured.tree_cut_paths:
        inventory_lines.append(
            "- Record part total: %d bytes in %d files | tree limits: "
            "%d bytes and %d files | over limit"
            % (captured.tree_bytes, captured.tree_files,
               captured.tree_byte_limit, captured.tree_file_limit))
    for p in captured.pieces:
        state = p.quality_state or "read in full"
        if p.text is None and p.quality_state is None:
            state = "not read in full"
        if p.form_state:
            state = state + " | form: " + p.form_state
        if _repair_cited(p):
            state = state + (" | repair cited: the Completion section "
                             "in this piece supplies the missing "
                             "content in place")
        for path in p.paths:
            inventory_lines.append("- %s | %s | %d bytes | %s"
                                   % (path, p.record_class, p.size, state))
    for path, note in captured.near_matches:
        line = "- %s | unrecognised near match | not read" % path
        if note:
            line += " | nearest closed pattern: " + note
        inventory_lines.append(line)

    data_quality = []
    code_for_quality = {"malformed": "malformed-piece",
                        "over limit": "over-limit-piece",
                        "unreadable": "unreadable-piece",
                        "truncated": "truncated-no-correcting-record"}
    for p in captured.pieces:
        if p.text is None:
            code = code_for_quality.get(p.quality_state or "",
                                        "unreadable-piece")
            if p.not_read_reason and "duplicate" in p.not_read_reason:
                code = "record-disagrees"
            name = p.paths[0].split("/")[-1]
            data_quality.append(
                "Piece %s (%s): What the record shows: the piece at %s "
                "stands %s and was not read in full. What follows: %s "
                "the piece is marked not read in full in the inventory "
                "and derivations that need it follow the not read in "
                "full rule." % (name, p.paths[0], p.paths[0],
                                p.quality_state or "unreadable", code))
    for path in captured.size_unknown_paths:
        name = path.split("/")[-1]
        data_quality.append(
            "Piece %s (%s): What the record shows: the piece at %s "
            "could not be measured when the tree was read, so its "
            "size stands unknown in the capture. What follows: "
            "unreadable-piece the piece is carried in the inventory "
            "with its size unknown, and no tree total rests on a "
            "measured size for it." % (name, path, path))
    for p in captured.pieces:
        if _repair_cited(p):
            name = p.paths[0].split("/")[-1]
            data_quality.append(
                "Piece %s (%s): What the record shows: the piece was "
                "found truncated and its Completion section supplies "
                "the missing content in place, a repair cited in the "
                "piece itself. What follows: the repair stands, so "
                "the piece is read in full and is not listed as a "
                "truncation without repair."
                % (name, p.paths[0]))
    sample_paths = sorted(
        [path for p in captured.pieces for path in p.paths] +
        [path for path, note in captured.near_matches])
    sample_text = ", ".join(sample_paths[:12])
    if len(sample_paths) > 12:
        sample_text += ", and further entries in that same order"
    bias_text = (
        "pieces are missing by walk order position, in sorted "
        "relative path order, not spread evenly across the tree, so "
        "pieces whose paths sort after the cut point are cut whole "
        "and pieces whose paths sort before it are kept whole; the "
        "bias direction is that later walk order positions are the "
        "ones cut")
    over_pieces = [p for p in captured.pieces
                   if p.text is None and p.quality_state == "over limit"
                   and not (p.not_read_reason and
                            "tree limit" in p.not_read_reason)]
    if over_pieces:
        first_over = over_pieces[0]
        limit_text = first_over.not_read_reason or "over limit"
        if limit_text.startswith("over limit: "):
            limit_text = limit_text[len("over limit: "):]
        data_quality.append(
            "Walk order sample for %s: What the record shows: the "
            "%s cut the capture at %s; sampled entries in sorted "
            "relative path order: %s. What follows: "
            "over-limit-piece %s."
            % (first_over.paths[0], limit_text, first_over.paths[0],
               sample_text, bias_text))
    if captured.tree_cut_paths:
        cut_at = captured.tree_cut_paths[0]
        last_seen = captured.tree_last_visited or cut_at
        data_quality.append(
            "Walk order sample for %s: What the record shows: the "
            "%s cut the capture, with the last visited path before "
            "the cut at %s and the first piece past the limit at "
            "%s; sampled entries in sorted relative path order: %s. "
            "What follows: over-limit-piece %s."
            % (cut_at, captured.tree_cut_kind or "tree limit",
               last_seen, cut_at, sample_text, bias_text))
    if captured.walk_note:
        last_seen = sample_paths[-1] if sample_paths else "none"
        data_quality.append(
            "Walk order sample for the whole walk bound: What the "
            "record shows: the whole walk bound of 10000 entries "
            "cut the capture, with the last visited path at %s; "
            "sampled entries in sorted relative path order: %s. "
            "What follows: over-limit-piece %s."
            % (last_seen, sample_text, bias_text))
    if captured.definitions_version is None:
        datum = ("Datum line: the tree stated none for the definitions "
                 "version; form basis: the settled forms of this version "
                 "of the tool.")
    else:
        datum = ("Datum line: definitions version %s; form basis: the "
                 "settled forms of this version of the tool."
                 % captured.definitions_version)
    data_quality.append(datum)
    for result in ordered:
        if result.verdict != "present" and result.shows is not None:
            data_quality.append("Row %s outcome: %s"
                                % (result.code, result.reason_text()))
    return ReportModel(header, coverage, inventory_lines, ordered,
                       data_quality)
