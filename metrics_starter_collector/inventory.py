"""Module 2: inventory, part of the shell.

Classifies each file found under the root as a recognised piece, an
unrecognised near match, or other material, by the closed name patterns
in Margin M4 of the design plan. Records piece identity by record
identity, not by path alone. Derives no metric.
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

_STEP = r"step-(\d{2})-"
_AUDIT_STEP = r"step(\d+)-"

_PATTERNS = [
    (re.compile(r"^build-metrics-record$"), CLS_METRICS_SINGLE, None),
    (re.compile(r"^build-metrics-record-part-"), CLS_METRICS_PAGE, None),
    (re.compile(r"^" + _STEP + r"snapshot-manifest\.md$"), CLS_SNAPSHOT_MANIFEST, 1),
    (re.compile(r"^" + _STEP + r"gate-record\.md$"), CLS_GATE_RECORD, 1),
    (re.compile(r"^" + _STEP + r"gate-ruling.*\.md$"), CLS_GATE_RULING, 1),
    (re.compile(r"^" + _STEP + r"regate-record\.md$"), CLS_REGATE_RECORD, 1),
    (re.compile(r"^" + _STEP + r"gate-adjudication\.md$"), CLS_GATE_ADJUDICATION, 1),
    (re.compile(r"^" + _STEP + r"opening-record\.md$"), CLS_OPENING_RECORD, 1),
    (re.compile(r"^" + _STEP + r"roster-artifact\.md$"), CLS_ROSTER, 1),
    (re.compile(r"^" + _STEP + r"snapshot\.md$"), CLS_SNAPSHOT, 1),
    (re.compile(r"^" + _STEP + r"trace\.md$"), CLS_TRACE, 1),
    (re.compile(r"^" + _STEP + r".+-trace\.md$"), CLS_TRACE, 1),
    (re.compile(r"^" + _STEP + r"board-member-.*\.md$"), CLS_BOARD_MEMBER, 1),
    (re.compile(r"^" + _STEP + r"record\.md$"), CLS_STEP_RECORD, 1),
    (re.compile(r"^" + _STEP + r".*\.md$"), CLS_STEP_COMPANION, 1),
    (re.compile(r"^" + _AUDIT_STEP + r".*fix-register.*\.md$"), CLS_FIX_REGISTER, 1),
    (re.compile(r"^" + _AUDIT_STEP + r"defect-register\.md$"), CLS_DEFECT_REGISTER, 1),
    (re.compile(r"^" + _AUDIT_STEP + r".*adjudication\.md$"), CLS_ADJUDICATION, 1),
    (re.compile(r"^step(\d+).*\.md$"), CLS_AUDIT_PAPER, 1),
]

_EXACT = {
    "PATH-LEDGER.md": CLS_PATH_LEDGER,
    "TIER-RECORD.md": CLS_TIER_RECORD,
    "DECISION-QUEUE.md": CLS_DECISION_QUEUE,
    "DESIGN-BRIEF.md": CLS_CITATION,
    "DESIGN-PLAN.md": CLS_CITATION,
    "NEXT-VERSION-PLAN.md": CLS_CITATION,
    "RECOVERY-RECORD.md": CLS_CITATION,
    "INSTALL-REGISTER.md": CLS_INSTALL_REGISTER,
}


def classify(rel_path):
    """Return (record_class, step) for a recognised path, else None."""
    parts = rel_path.split("/")
    base = parts[-1]
    if re.match(r"^step-\d+-records\.md$", base) or \
            re.match(r"^step-\d+-gate-records\.md$", base):
        return None
    if base in _EXACT:
        return _EXACT[base], None
    if "cost-ledger" in base or "cost_ledger" in base:
        return CLS_COST_LEDGER, None
    if parts[0] == "audit":
        # Audit papers live under the audit directory. Their names use
        # the step-01-red form in synthetic trees and the step12-red
        # form in the target tree, and the step companion catch all
        # for step records must not swallow them.
        m = re.search(r"step-?(\d+)", base)
        step = int(m.group(1)) if m else None
        if "fix-register" in base:
            return CLS_FIX_REGISTER, step
        if "defect-register" in base:
            return CLS_DEFECT_REGISTER, step
        if "adjudication" in base:
            return CLS_ADJUDICATION, step
        return CLS_AUDIT_PAPER, step
    if parts[0] == "registers" and base == "defect-register.md":
        return CLS_DEFECT_REGISTER, None
    stem = base[:-3] if base.endswith(".md") else base
    if stem == "build-metrics-record":
        return CLS_METRICS_SINGLE, None
    for pattern, cls, group in _PATTERNS:
        m = pattern.match(base)
        if m:
            step = int(m.group(group)) if group else None
            return cls, step
    if parts[0] == "registers" and base.endswith(".md"):
        return CLS_OTHER_REGISTER, None
    return None


_NEAR_RES = [
    (re.compile(r"step-\d+-record"), "steps/step-NN-record.md"),
    (re.compile(r"step-\d+-gate"), "steps/step-NN-gate-record.md"),
    (re.compile(r"path[-_ ]?ledger", re.I), "PATH-LEDGER.md"),
    (re.compile(r"metrics[-_ ]?record", re.I),
     "wiki/wiki/synthesis/build-metrics-record.md"),
    (re.compile(r"step-\d+-trace"), "steps/step-NN-trace.md"),
    (re.compile(r"step-\d+-roster"), "steps/step-NN-roster-artifact.md"),
    (re.compile(r"decision[-_ ]?queue", re.I), "DECISION-QUEUE.md"),
    (re.compile(r"decision[-_ ]?queu", re.I), "DECISION-QUEUE.md"),
    (re.compile(r"queue[-_ ]?decision", re.I), "DECISION-QUEUE.md"),
    (re.compile(r"decisions?[-_ ]?queue", re.I), "DECISION-QUEUE.md"),
]


def near_match_note(rel_path):
    """Return the nearest closed pattern note for a name, or None."""
    base = rel_path.split("/")[-1]
    for pattern, note in _NEAR_RES:
        if pattern.search(base):
            if "NN" in note:
                m = re.search(r"step-(\d+)", base)
                if m:
                    note = note.replace(
                        "NN", m.group(1).zfill(2))
            return note
    return None


def identity_for(record_class, step, rel_path):
    """Piece identity by record identity: class, step and name form."""
    base = rel_path.split("/")[-1]
    if step is not None:
        return "%s:%d:%s" % (record_class, step, base)
    return "%s:%s" % (record_class, base)


_FORM_A_ITEM = re.compile(
    r"^\s*(\d+)\.\s+([^:\n]+):\s*(NOT IN FORCE|IN FORCE)\b")

# The five E-03 record change names, by change number. The short
# forms are the names as the M-2 settlement states them; change 1
# also carries the longer form the metrics record itself uses.
_RECORD_CHANGE_NAMES = {
    1: ("timestamped state transitions",
        "timestamped state transitions in the path record"),
    2: ("decision queue timestamps and origin",),
    3: ("origin step on findings",),
    4: ("agent-turn and per-agent engagement telemetry",),
    5: ("explicit loop round markers",),
}


def record_change_force(assembled_text):
    """Parse the Form A record change statement from a metrics record.

    A force statement in Form A is a numbered list in the assembled
    metrics record text, each item naming one record change and
    stating IN FORCE or NOT IN FORCE immediately after the name.
    An item records a force state only where its stated name is the
    E-03 name of the change its number names: an item naming no
    E-03 change, or naming a change other than its number, records
    no force state. Returns a dict from change number to its force
    words. Prose restatements (Form B) are not parsed here: a
    restatement by number creates no force state on its own. Where
    a number stands twice, the first statement in the list governs,
    because the brief states no precedence for conflicting
    statements.
    """
    states = {}
    if not assembled_text:
        return states
    for line in assembled_text.splitlines():
        m = _FORM_A_ITEM.match(line)
        if m:
            if m.group(1) != str(int(m.group(1))):
                continue
            number = int(m.group(1))
            names = _RECORD_CHANGE_NAMES.get(number)
            if names is None:
                continue
            stated = " ".join(m.group(2).split()).lower()
            if stated not in names:
                continue
            if number not in states:
                states[number] = m.group(3)
    return states


# The settled mapping from record changes to record classes, Step 15.
# Each of the five E-03 changes creates a field, a timestamping
# practice, a marker or an export inside a record kind the taxonomy
# classes independently of the change, and none creates a record
# class, so each change maps to no class and no header count moves
# on force grounds under this mapping.
RECORD_CHANGE_CLASSES = {1: (), 2: (), 3: (), 4: (), 5: ()}
