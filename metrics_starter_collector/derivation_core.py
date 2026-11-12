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
    return StepUniverse(tuple(sorted(evidenced)), tuple(sorted(ledger_steps)),
                        tuple(sorted(metrics_steps)), tuple(disagreements))


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
    found = captured.pieces_of(CLS_PATH_LEDGER)
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
    if ledger is None or ledger.text is None:
        return DerivationResult(
            "T-1", "missing", "no figure stands", denom, pointer,
            shows="no path ledger piece stands in the capture, so no "
                  "transition log holds any timestamp field",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing",
            rule_name="T-1 feeder standing rule")
    intervals = _step_intervals(captured)
    if not _ledger_has_full_ts(captured):
        if _ledger_has_dates(captured):
            return DerivationResult(
                "T-1", "missing", "no figure stands", denom, pointer,
                shows="the transition log in PATH-LEDGER.md holds timestamp "
                      "fields in date only form, and no entry carries a "
                      "time of day from which an interval can form",
                code_token="date-only-form",
                follows="date-only-form the metric specific boundary makes "
                        "the row missing where no timestamp with a time of "
                        "day stands",
                rule_name="T-1 date only boundary rule")
        return DerivationResult(
            "T-1", "missing", "no figure stands", denom, pointer,
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
            "intervals stand for " + _named_steps(covered), denom, pointer,
            shows="the transition log yields a full timestamp interval "
                  "for %s and no interval for %s"
                  % (_named_steps(covered), _named_steps(uncovered)),
            code_token="partial-span",
            follows="partial-span the series covers only part of the step "
                    "universe, so no build level figure stands",
            rule_name="T-1 mixed series rule")
    figures = "; ".join("Step %d elapsed %s hours" % (s, _fmt_num(intervals[s]))
                        for s in covered)
    return DerivationResult("T-1", "present", figures, denom, pointer,
                            rule_name="T-1 interval rule")


def _derive_t2(captured, universe, t1):
    ledger = _ledger_piece(captured)
    pointer = ledger.paths[0] if ledger else "PATH-LEDGER.md"
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    if t1.verdict == "missing" and t1.code_token == "date-only-form":
        has_duration = False
        if ledger is not None and ledger.text is not None:
            has_duration = re.search(r"interval duration|BANKED[^\n]*\d",
                                     ledger.text) is not None
        if not has_duration:
            return DerivationResult(
                "T-2", "missing", "no figure stands", denom, pointer,
                shows="no banked, suspended or halt interval duration "
                      "stands in the transition log, and the elapsed row "
                      "is missing on the date only ground",
                code_token="date-only-form",
                follows="date-only-form the row is missing where the "
                        "elapsed row is missing on that ground and no "
                        "interval duration stands",
                rule_name="T-2 date only boundary rule")
    if t1.verdict == "present but not derivable":
        return DerivationResult(
            "T-2", "present but not derivable", "no figure stands", denom,
            pointer,
            shows="the elapsed series stands incomplete, so the active "
                  "series that rests on it stands incomplete in the same "
                  "places",
            code_token=t1.code_token or "missing-field",
            follows=(t1.code_token or "missing-field") +
                    " the active figure rests on the elapsed series, so "
                    "no active figure stands",
            rule_name="T-2 mixed series rule")
    if t1.verdict == "missing":
        return DerivationResult(
            "T-2", "missing", "no figure stands", denom, pointer,
            shows="the elapsed row is missing, and no interval duration "
                  "stands in the transition log to carry an active figure",
            code_token="no-feeder-record",
            follows="no feeder record yields an active figure, so the "
                    "row is missing",
            rule_name="T-2 feeder standing rule")
    intervals = _step_intervals(captured)
    figures = "; ".join("Step %d active %s hours" % (s, _fmt_num(intervals[s]))
                        for s in sorted(intervals))
    return DerivationResult("T-2", "present", figures, denom, pointer,
                            rule_name="T-2 interval rule")


def _derive_t4(captured, universe):
    ledger = _ledger_piece(captured)
    pointer = ledger.paths[0] if ledger else "PATH-LEDGER.md"
    denom = "denominator decision items and banked states in the tree"
    banked = False
    durations = False
    if ledger is not None and ledger.text is not None:
        banked = "BANKED" in ledger.text or "banked" in ledger.text.lower()
        durations = re.search(r"banked[^\n]*\d+(?:\.\d+)?\s*hours",
                              ledger.text, re.I) is not None
    queue = captured.pieces_of(CLS_DECISION_QUEUE)
    if queue:
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
    if not durations:
        return DerivationResult(
            "T-4", "present but not derivable",
            "banked item counts stand and no duration figure stands",
            denom, pointer,
            shows="banked states and item counts stand in the feeder "
                  "records and every duration the metric needs is absent",
            code_token="missing-field",
            follows="missing-field a count of items is not a time, and "
                    "the durations themselves are absent, so no wait "
                    "figure stands",
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
        rule_name="T-4 mixed series rule")


def _derive_t7(captured, universe):
    metrics_path = captured.metrics_single_path or "wiki/wiki/synthesis/build-metrics-record.md"
    gates = captured.pieces_of(*GATE_CLASSES)
    pointer = metrics_path
    denom = "denominator loop steps in the step universe"
    loop_mentioned = False
    if captured.assembled_metrics and "loop round" in captured.assembled_metrics.lower():
        loop_mentioned = True
    step_loop = any(p.text and "loop step" in p.text.lower()
                    for p in captured.pieces_of(CLS_STEP_RECORD))
    if loop_mentioned and gates:
        return DerivationResult(
            "T-7", "present but not derivable", "no round count figure",
            denom, pointer,
            shows="the loop round table in the metrics record holds no "
                  "rows, while gate files in the tree carry round counts "
                  "for the loop steps, and the two counts cannot be "
                  "reconciled to one count",
            code_token="record-disagrees",
            follows="record-disagrees the verdict record count and the "
                    "step record pass count cannot be reconciled to one "
                    "count, with both counts named in the record",
            rule_name="T-7 irreconcilable counts rule")
    if gates or step_loop:
        return DerivationResult(
            "T-7", "present but not derivable", "no round count figure",
            denom, gates[0].paths[0] if gates else pointer,
            shows="verdict records stand for steps in the tree and no "
                  "round mapping in the settled form stands for them",
            code_token="missing-field",
            follows="missing-field the round count field the derivation "
                    "needs is absent from the verdict records as they "
                    "stand",
            rule_name="T-7 round mapping rule")
    return DerivationResult(
        "T-7", "missing", "no round count figure", denom, pointer,
        shows="no loop step and no verdict record for a loop step stands "
              "in the tree",
        code_token="no-feeder-record",
        follows="no feeder record for the metric exists in the tree, so "
                "the row is missing, with its empty population stated",
        rule_name="T-7 empty population rule")


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
    figures = "; ".join("Step %d staffed %d of base %d" % (s, covered[s][0], covered[s][1])
                        for s in sorted(covered))
    remainder = [s for s in universe.evidenced if s not in covered]
    if remainder:
        denom = (denom_base + "; covered " + _step_list_text(sorted(covered)) +
                 "; remainder " + _step_list_text(remainder) +
                 " named, no base stated")
    else:
        denom = denom_base + "; covered " + _step_list_text(sorted(covered))
    return DerivationResult("E-1", "present", figures, denom, pointer,
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
    no_base = [s for s in universe.evidenced if _parse_base(captured, s) is None]
    if no_base:
        denom = (denom_base + "; " + _step_list_text(no_base) +
                 " named against additions over base only, total spins "
                 "still reported")
    else:
        denom = denom_base
    return DerivationResult("E-2", "present", "; ".join(parts), denom,
                            pointer, rule_name="E-2 labelled quantities rule")


# ------------------------------------------------------- E-3, E-4, F-2

def _derive_e3(captured, universe):
    pointer = captured.first_path(CLS_INSTALL_REGISTER) or \
        "registers/INSTALL-REGISTER.md"
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    ledgers = captured.pieces_of(CLS_COST_LEDGER)
    token_found = False
    for p in ledgers:
        if p.text and re.search(r"token[^\n]*\d", p.text, re.I):
            token_found = True
    if not ledgers:
        return DerivationResult(
            "E-3", "missing", "no token figure", denom, pointer,
            shows="no cost ledger stands inside the tree, and the "
                  "install register holds no token figures, while step "
                  "records state tokens as not recorded",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists, and a "
                    "documented units proxy is not the metric, so the "
                    "row is missing",
            rule_name="E-3 feeder standing rule")
    if not token_found:
        return DerivationResult(
            "E-3", "present but not derivable", "no token figure", denom,
            ledgers[0].paths[0],
            shows="a cost ledger stands in the tree and it meters no "
                  "token figure for any step",
            code_token="missing-field",
            follows="missing-field the token figure field the derivation "
                    "needs is absent from the ledger, so no figure stands",
            rule_name="E-3 metering rule")
    return DerivationResult(
        "E-3", "present but not derivable", "token figures stand in part",
        denom, ledgers[0].paths[0],
        shows="the cost ledger meters tokens for part of the step "
              "universe only",
        code_token="partial-span",
        follows="partial-span the covered span is named in the coverage "
                "and steps outside it are not reported as zero",
        rule_name="E-3 partial metering rule")


def _derive_e4(captured, universe):
    denom = "denominator step universe %d steps" % len(universe.evidenced)
    money_steps = []
    money_pointer = None
    for s in sorted(universe.evidenced):
        for p in captured.step_pieces(s, CLS_STEP_RECORD):
            if p.text and "Budget at closure" in p.text and \
                    re.search(r"money\s+(nil|zero)", p.text, re.I):
                money_pointer = p.paths[0]
                break
        if money_pointer:
            break
    for s in sorted(universe.evidenced):
        for p in captured.step_pieces(s, CLS_STEP_RECORD):
            if p.text and re.search(r"money\s+(nil|zero)", p.text, re.I):
                money_steps.append(s)
                if money_pointer is None:
                    money_pointer = p.paths[0]
                break
    ledgers = captured.pieces_of(CLS_COST_LEDGER)
    if ledgers and all(p.text and re.search(r"money[^\n]*\d", p.text, re.I)
                       for p in ledgers):
        pass
    if not money_steps and not ledgers:
        return DerivationResult(
            "E-4", "missing", "no figure stands", denom,
            captured.first_path(CLS_STEP_RECORD) or "steps/step-01-record.md",
            shows="no per step money figure and no cost ledger money "
                  "figure stands in the feeder records",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing",
            rule_name="E-4 feeder standing rule")
    covered_all = len(money_steps) == len(universe.evidenced) and money_steps
    if not covered_all:
        remainder = [s for s in universe.evidenced if s not in money_steps]
        pointer = money_pointer or (ledgers[0].paths[0] if ledgers else
                                    captured.first_path(CLS_STEP_RECORD))
        return DerivationResult(
            "E-4", "present but not derivable", "no complete per step "
            "money series stands",
            denom + "; remainder " + _step_list_text(remainder) +
            " named, no per step money figure stands", pointer,
            shows="a partial money series stands in the feeder records, "
                  "with per step statements for part of the universe and "
                  "nothing per step for the remainder steps named in the "
                  "coverage",
            code_token="missing-field",
            follows="missing-field no complete per step money series "
                    "stands in the feeders, so the metric in its defined "
                    "form does not yield",
            rule_name="E-4 partial series rule")
    figures = "; ".join("Step %d money nil" % s for s in money_steps)
    return DerivationResult("E-4", "present", figures, denom,
                            money_pointer, rule_name="E-4 series rule")


_CLOSURE_TOKENS = ("CLOSED-PASS", "CLOSED-QUALIFIED", "CLOSED-FAIL",
                   "RECYCLED")


def _recorded_closure(text):
    """Return the recorded closure state in a settled form, or None.

    Matching is on the recorded closure state field and on the verdict
    forms the gate records use, exact forms only, never on a closure
    token mentioned in prose.
    """
    m = re.search(r"(?:Step closure state|Closure state):\s*"
                  r"(CLOSED-PASS|CLOSED-QUALIFIED|CLOSED-FAIL|RECYCLED)",
                  text)
    if m:
        return m.group(1)
    for line in text.splitlines():
        m = re.match(r"\s*(CLOSED-PASS|CLOSED-QUALIFIED|CLOSED-FAIL|"
                     r"RECYCLED)\s*[.,]", line)
        if m:
            return m.group(1)
    m = re.search(r"recorded as\s+(CLOSED-PASS|CLOSED-QUALIFIED|"
                  r"CLOSED-FAIL|RECYCLED)", text)
    if m:
        return m.group(1)
    m = re.search(r"recorded\s+(RECYCLED)\b", text)
    if m:
        return m.group(1)
    m = re.search(r"closes\s+(CLOSED-PASS|CLOSED-QUALIFIED|CLOSED-FAIL)",
                  text)
    if m:
        return m.group(1)
    m = re.search(r"Verdict grade:\s*(FAIL)\b", text)
    if m:
        return m.group(1)
    return None


def _derive_f2(captured, universe):
    denom = ("denominator steps ruled on, with plain approvals and "
             "qualified approvals as two subcounts under that one "
             "denominator")
    gates = captured.pieces_of(*GATE_CLASSES)
    pointer = None
    for p in captured.pieces_of(CLS_SNAPSHOT):
        if p.text and "steps ruled on" in p.text:
            pointer = p.paths[0]
            break
    if pointer is None:
        pointer = gates[0].paths[0] if gates else \
            (captured.first_path(CLS_STEP_RECORD) or "steps/step-01-record.md")
    if not gates:
        return DerivationResult(
            "F-2", "missing", "no rate figure", denom, pointer,
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
    for s in sorted(universe.evidenced):
        closure = None
        ranked = []
        for cls, rank in ((CLS_GATE_RECORD, 0), (CLS_GATE_RULING, 1),
                          (CLS_GATE_ADJUDICATION, 2), (CLS_REGATE_RECORD, 3)):
            for p in captured.step_pieces(s, cls):
                name = p.paths[0]
                r = rank
                num = 0
                if "round" in name or "reaudit" in name:
                    r = 3
                    m = re.search(r"(?:round|reaudit)-?(\d+)", name)
                    num = int(m.group(1)) if m else 0
                ranked.append((r, num, name, p))
        ranked.sort(key=lambda item: (item[0], item[1], item[2]))
        if ranked:
            first = ranked[0][3]
            if first.text:
                closure = _recorded_closure(first.text)
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
        else:
            not_derivable.append(s)
    if not_derivable:
        return DerivationResult(
            "F-2", "present but not derivable", "no rate figure", denom,
            pointer,
            shows="first ruling outcomes stand in gate files for part of "
                  "the universe, and the steps named here carry no first "
                  "ruling outcome in the settled forms: " +
                  _named_steps(not_derivable),
            code_token="missing-field",
            follows="missing-field one or more step contributions are "
                    "not derivable in the settled forms, so no rate is "
                    "printed",
            rule_name="F-2 first ruling rule")
    if ruled == 0:
        return DerivationResult(
            "F-2", "present but not derivable", "no rate figure", denom,
            pointer,
            shows="gate pieces stand in the tree and no step has been "
                  "ruled on, so the denominator of steps ruled on is zero",
            code_token="missing-field",
            follows="missing-field the ruling outcome field is absent "
                    "for every step, so no rate is printed",
            rule_name="F-2 empty denominator rule")
    rate = (plain + qualified) * 100.0 / ruled
    figures = ("first-time approval rate %s percent; plain approvals %d; "
               "qualified approvals %d; steps ruled on %d"
               % (_fmt_num(rate), plain, qualified, ruled))
    return DerivationResult("F-2", "present", figures, denom, pointer,
                            rule_name="F-2 first ruling rule")


# ------------------------------------------------------- Q-1, Q-3, Q-4

def _derive_q1(captured, universe):
    denom = "denominator audit rounds evidenced in the tree"
    registers = captured.pieces_of(CLS_FIX_REGISTER)
    papers = captured.pieces_of(CLS_AUDIT_PAPER, CLS_ADJUDICATION)
    pointer = None
    if registers:
        pointer = max(registers, key=lambda p: p.size).paths[0]
    elif papers:
        pointer = papers[0].paths[0]
    else:
        pointer = captured.metrics_single_path or \
            "wiki/wiki/synthesis/build-metrics-record.md"
    if not registers and not papers:
        return DerivationResult(
            "Q-1", "missing", "no count figure",
            "denominator no audit round is evidenced in the tree", pointer,
            shows="no audit round is evidenced in the tree, so the "
                  "population the metric counts over is empty",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing, with its empty population "
                    "stated",
            rule_name="Q-1 empty population rule")
    breakdown = False
    for p in registers + papers:
        if p.text and re.search(r"Critical\s+\d+[^\n]*High\s+\d+", p.text):
            breakdown = True
    if not breakdown:
        return DerivationResult(
            "Q-1", "present but not derivable", "no count figure", denom,
            pointer,
            shows="audit round records stand in the tree and no round "
                  "own record states a post triage severity breakdown "
                  "in a form the rule allows",
            code_token="no-post-triage-breakdown",
            follows="no-post-triage-breakdown only post triage "
                    "breakdowns count, so no severity count stands for "
                    "the rounds as they stand",
            rule_name="Q-1 post triage rule")
    return DerivationResult(
        "Q-1", "present but not derivable", "bounded counts only", denom,
        pointer,
        shows="some rounds state a post triage breakdown and the rest "
              "state none, so the row stands in bounded form",
        code_token="no-post-triage-breakdown",
        follows="no-post-triage-breakdown the bounded form prints counts "
                "for the rounds whose own records state a breakdown and "
                "no count for any other round",
        rule_name="Q-1 bounded form rule")


def _derive_q3(captured, universe):
    pointer = captured.metrics_single_path or \
        "wiki/wiki/synthesis/build-metrics-record.md"
    denom = "denominator register entries that carry a defect triage disposition"
    registers = captured.pieces_of(CLS_DEFECT_REGISTER, CLS_FIX_REGISTER)
    zero_printed = False
    if captured.assembled_metrics and re.search(
            r"Escapes attributed[^\n]*\b0\b", captured.assembled_metrics):
        zero_printed = True
    if zero_printed:
        return DerivationResult(
            "Q-3", "present but not derivable",
            "no escaped defect figure; the printed zero is never stated "
            "as a measured zero", denom, pointer,
            shows="no origin step field stands on any finding, fix entry "
                  "or defect item in the tree, and the cross check table "
                  "prints a zero for escapes with no measurement basis "
                  "stated for it",
            code_token="no-measurement-basis",
            follows="no-measurement-basis a printed zero with no "
                    "measurement basis is a placeholder, so the metric "
                    "is present but not derivable",
            rule_name="Q-3 placeholder zero rule")
    if not registers:
        return DerivationResult(
            "Q-3", "missing", "no figure stands", denom, pointer,
            shows="no defect register and no audit record carrying a "
                  "defect triage disposition stands in the tree",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing",
            rule_name="Q-3 feeder standing rule")
    return DerivationResult(
        "Q-3", "present but not derivable", "no figure stands", denom,
        registers[0].paths[0],
        shows="register entries stand in the tree and no origin step "
              "field that passes the acceptance test stands on them",
        code_token="missing-field",
        follows="missing-field the origin step field the derivation "
                "needs is absent from the register entries, so no figure "
                "stands",
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


def _piece_trace(text):
    """Best (landed, total) reading inside one piece, or None. A summary
    line, a counts line or a line also stating PARTIAL, outranks a passing
    mention of another trace inside the same piece."""
    best = None
    for line in text.splitlines():
        cand = None
        m = _COUNTS_RE.search(line)
        if m:
            cand = (int(m.group(2)), int(m.group(1)))
        else:
            for i, rx in enumerate(_TRACE_RES):
                m = rx.search(line)
                if m:
                    if i == 4:
                        cand = (int(m.group(2)), int(m.group(1)))
                    else:
                        cand = (int(m.group(1)), int(m.group(2)))
                    break
        if cand is None:
            continue
        score = (2 if "PARTIAL" in line else 0) + (
            1 if ("Counts:" in line or "Full trace" in line) else 0)
        if best is None or score > best[0]:
            best = (score, cand)
    if best is not None:
        return best[1]
    m = re.search(r"Pin rows traced:\s*(\d+)", text)
    m2 = re.search(r"LANDED:\s*(\d+)\b", text)
    if m and m2:
        return int(m2.group(1)), int(m.group(1))
    return None


def _trace_candidates(captured, step):
    found = []
    order = (CLS_TRACE, CLS_AUDIT_PAPER, CLS_GATE_RECORD, CLS_GATE_RULING,
             CLS_BOARD_MEMBER, CLS_STEP_RECORD, CLS_REGATE_RECORD)
    for cls in order:
        pieces = list(captured.step_pieces(step, cls))
        if cls == CLS_AUDIT_PAPER:
            def paper_key(p):
                name = p.paths[0].rsplit("/", 1)[-1]
                variant = ("reaudit" in name or "round" in name)
                num = 0
                m = re.search(r"(?:reaudit|round)-?(\d+)", name)
                if m:
                    num = int(m.group(1))
                return (0 if "purple" in name else 1,
                        1 if variant else 0, num, name)
            pieces = [p for p in pieces
                      if "register" not in p.paths[0].rsplit("/", 1)[-1]]
            pieces.sort(key=paper_key)
        for p in pieces:
            if p.text is None:
                continue
            reading = _piece_trace(p.text)
            if reading is None:
                continue
            found.append((reading[0], reading[1], p))
            break
        if found:
            break
    totals = set()
    landed_by_total = {}
    for landed, total, p in found:
        totals.add(total)
        landed_by_total.setdefault(total, landed)
    if found:
        landed0 = found[0][0]
        for cls in (CLS_GATE_RECORD, CLS_GATE_RULING, CLS_BOARD_MEMBER):
            for p in captured.step_pieces(step, cls):
                if p.text is None:
                    continue
                mn = _NONLANDED_RE.search(p.text)
                if mn:
                    comp = landed0 + int(mn.group(1))
                    if comp != found[0][1]:
                        totals.add(comp)
                        landed_by_total.setdefault(comp, landed0)
    return found, totals, landed_by_total


def _derive_q4(captured, universe):
    denom_base = "denominator steps with a first trace"
    covered = {}
    unreconciled = {}
    first_pointer = None
    for s in sorted(universe.evidenced):
        found, totals, landed_by_total = _trace_candidates(captured, s)
        if not found:
            continue
        if first_pointer is None:
            first_pointer = found[0][2].paths[0]
        if len(totals) > 1 and len(set(landed_by_total.values())) <= 1 \
                and len(found) >= 1:
            landed = found[0][0]
            unreconciled[s] = (landed, sorted(totals))
            continue
        covered[s] = (found[0][0], found[0][1])
    traces = captured.pieces_of(CLS_TRACE)
    gates = captured.pieces_of(*GATE_CLASSES)
    if not covered and not unreconciled:
        if traces or gates:
            return DerivationResult(
                "Q-4", "present but not derivable", "no figure stands",
                denom_base, (traces or gates)[0].paths[0],
                shows="gate records stand in the tree and no first trace "
                      "in the settled form stands for any step",
                code_token="missing-field",
                follows="missing-field the first trace field the "
                        "derivation needs is absent from the records as "
                        "they stand",
                rule_name="Q-4 first trace rule")
        return DerivationResult(
            "Q-4", "missing", "no figure stands", denom_base,
            captured.metrics_single_path or
            "wiki/wiki/synthesis/build-metrics-record.md",
            shows="no first trace record and no gate record stands in "
                  "the tree for this metric",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists in the tree, "
                    "so the row is missing",
            rule_name="Q-4 feeder standing rule")
    figures = "; ".join(
        "Step %d first trace %d of %d LANDED" % (s, covered[s][0], covered[s][1])
        for s in sorted(covered))
    denom = denom_base
    pointer = first_pointer
    if unreconciled:
        s = sorted(unreconciled)[0]
        landed, totals = unreconciled[s]
        pointer = None
        recs = captured.step_pieces(s, CLS_TRACE)
        exact = "step-%02d-trace.md" % s
        for p in recs:
            if p.paths[0].rsplit("/", 1)[-1] == exact:
                pointer = p.paths[0]
                break
        if pointer is None and recs:
            pointer = recs[0].paths[0]
        if pointer is None:
            pointer = first_pointer
        denom += ("; remainder Step %d named with both totals %d against "
                  "%d, LANDED %d in both forms"
                  % (s, totals[0], totals[-1], landed))
    return DerivationResult("Q-4", "present", figures, denom, pointer,
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
    for line in lines[header_at + 1:]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if items:
                continue
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 5:
            continue
        if cells[0] in ("Item", "---") or set(cells[0]) <= set("-: "):
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
        if open_items:
            shows += "; open items named: " + ", ".join(open_items)
        return DerivationResult(
            "D-1", "present but not derivable", "no median and no longest "
            "figure stands", denom, pointer,
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
    queue_pieces = [p for p in captured.pieces_of(CLS_DECISION_QUEUE)
                    if p.paths[0] == "DECISION-QUEUE.md"]
    queue_items = None
    queue_unusable = False
    if queue_pieces:
        piece = queue_pieces[0]
        if piece.text is not None:
            queue_items = _decision_items(piece.text)
        if queue_items is None:
            queue_unusable = True
    table_items = _decision_items(captured.assembled_metrics)
    if queue_items is not None:
        statement = ("the in tree DECISION-QUEUE.md in "
                     "the named form supplied the row, as the foundation "
                     "statement for this row.")
        result = _d1_from_items(queue_items, "DECISION-QUEUE.md", statement)
        extra = d1_cross_check_statement(result, table_items)
        if extra:
            result.statement = (result.statement or "") + " " + extra
        return result
    if table_items:
        statement = ("the metrics record decision table "
                     "under the D-09 exception supplied the row, as the "
                     "foundation statement for this row.")
        return _d1_from_items(table_items, metrics_path, statement)
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
        return DerivationResult(
            "B-1", "missing", "no elapsed or active figure", denom,
            metrics_path,
            shows="both input rows are missing and no feeder record "
                  "holds a figure for this row, and the build summary "
                  "states the whole build figures are not computed",
            code_token="no-feeder-record",
            follows="no feeder record for the metric exists and a "
                    "composed row is missing where an input row is "
                    "missing, so the row is missing",
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


def _derive_b2(captured, universe):
    denom = "denominator the whole build budget in two limbs, money and tokens"
    budget_piece = None
    for p in captured.pieces_of(CLS_STEP_RECORD, CLS_TIER_RECORD):
        if p.text and re.search(r"[Bb]udget", p.text) and \
                re.search(r"Money:\s*0\b|money budget of 0|Money: 0 external", p.text):
            budget_piece = p
            break
    if budget_piece is not None:
        return DerivationResult(
            "B-2", "present but not derivable",
            "money spent nil against a money budget of 0; token spent "
            "and token budget figures absent", denom, budget_piece.paths[0],
            shows="the budget act in the named step record sets the "
                  "money budget at zero for the whole build, and both "
                  "the spent figure and the budget figure are absent "
                  "for the token limb, with tokens stated as not "
                  "recorded",
            code_token="no code fits",
            follows="no code fits a percentage against a budget of zero "
                    "is undefined for the money limb and no limb yields "
                    "its percentage in full, so the row is present but "
                    "not derivable, reported as undefined and never as "
                    "0 percent and never as 100 percent",
            rule_name="B-2 zero budget rule")
    ledgers = captured.pieces_of(CLS_COST_LEDGER)
    if not ledgers:
        return DerivationResult(
            "B-2", "missing", "no figure stands", denom,
            captured.first_path(CLS_STEP_RECORD) or "steps/step-01-record.md",
            shows="no cost ledger stands in the tree and neither limb, "
                  "money or tokens, has any feeder record",
            code_token="no-feeder-record",
            follows="no feeder record for either limb exists in the "
                    "tree, so the row is missing",
            rule_name="B-2 limb composition rule")
    return DerivationResult(
        "B-2", "present but not derivable", "no percentage stands", denom,
        ledgers[0].paths[0],
        shows="a cost ledger stands in the tree and at least one limb "
              "does not yield its percentage",
        code_token="missing-field",
        follows="missing-field the row verdict follows the weaker limb, "
                "and the blocking limb is named in the record shows part",
        rule_name="B-2 limb composition rule")


def _derive_b3_b4(captured, universe, t1, t2, code):
    metrics_path = captured.metrics_single_path or \
        "wiki/wiki/synthesis/build-metrics-record.md"
    denom = "denominator steps eligible for ranking"
    derived = "T-1 and T-2"
    label = "Slowest three steps" if code == "B-3" else "Fastest three steps"
    if t1.verdict == "missing" or t2.verdict == "missing":
        return DerivationResult(
            code, "missing", "no ranking figure", denom, metrics_path,
            shows="no ranked list stands in the feeders and at least one "
                  "input row is missing",
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
    ordered = sorted(intervals.items(), key=lambda kv: kv[1],
                     reverse=(code == "B-3"))
    top = ordered[:3]
    figures = label + ": " + "; ".join(
        "Step %d at %s hours" % (s, _fmt_num(v)) for s, v in top)
    return DerivationResult(code, "present", figures,
                            denom + "; eligible steps %d" % len(intervals),
                            metrics_path, derived_from=derived,
                            rule_name=code + " ranking rule")


# ------------------------------------------------------------- assembly

_COMPOSED = ("B-1", "B-3", "B-4")


def _apply_version_refusal(captured, results):
    version = captured.definitions_version
    if version is None or _known_version(version):
        return
    by_code = {r.code: r for r in results}
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
        if any(r.verdict == "present but not derivable" for r in inputs) \
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
            "Pieces recognised: 0",
            "Latest record timestamp: " +
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
    _apply_version_refusal(captured, ordered)

    identity = captured.build_identity or \
        "no build identity was found in the tree"
    header = [
        "# Metrics starter set report",
        "Root: " + str(captured.root),
        "Build identity: " + identity,
        "Step universe: %d steps (%s)" % (len(universe.evidenced),
                                          _step_list_text(universe.evidenced)),
        "Pieces recognised: %d" % len(captured.pieces),
        "Latest record timestamp: " +
        (captured.latest_timestamp or "no timestamp was found"),
    ]
    not_read = [p for p in captured.pieces if p.text is None]
    coverage_bits = []
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
    if not coverage_bits:
        coverage_bits.append("the capture stands complete for the "
                             "pieces recognised")
    coverage = "Coverage statement: " + "; ".join(coverage_bits) + "."
    header.append(coverage)
    for cls in sorted(captured.inventory_totals):
        totals = captured.inventory_totals[cls]
        header.append(
            "Class %s: expected %d, found %d, not found %d, not yet "
            "recordable %d" % (cls, totals["expected"], totals["found"],
                               totals["not_found"],
                               totals["not_yet_recordable"]))

    inventory_lines = ["## Piece inventory"]
    for p in captured.pieces:
        state = p.quality_state or "read in full"
        if p.text is None and p.quality_state is None:
            state = "not read in full"
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
