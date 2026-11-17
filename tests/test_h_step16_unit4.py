"""Step 16 fix unit 4 tests: the Terms section definitions.

Pinning tests for register item R16-09 (Medium) of Step 16 round 1,
which also carries the T-7 part of U-R3. The Terms section at the
foot of the driven report, design/steps/step-16r-useit-report-foldin.txt,
carries six lines only, defining its reason codes, while the reason
lines rely on terms that section never explains, as listed by the
first reader (spin 1105) and checked by the correctness auditor
(spin 1106). Surface fact 3 under guard LG-11 fails: a term appears
in a reason line that the report itself does not explain in its
terms section. The locus is derivation_core.py _terms_lines, which
emits one terms line per reason code token and nothing else, so the
report_renderer.py fallback glossary, which does carry broken link,
form required and form held, never runs.

The register form is usage driven, under LG-11 surface fact 3: no
term appears in a reason line that the report does not explain. The
Terms section is not a fixed full glossary: a report defines the
terms its own rows use, and a control report whose rows use none of
the added terms must not gain definitions for them. The six reason
code definitions standing today must stay present and unchanged in
wording and in their standing order.

The fold in shape is constructed by this module from the F-16
miniature case, rather than driving the real fold in tree, because
a suite test must stand on files inside the suite alone: the real
tree stands outside the product repo and is not carried to the
bench the suite runs on. The constructed form keeps every fact the
register establishes for the driven report: the same six reason
codes stand used, and the rows between them use every term the
register lists, in the same row positions the driven report uses
them. The one construction change against the miniature is stated
in the files builder: the gate files carry no closure state line,
so the F-2 row states, step by step, that the recorded closure
state matches no named closure form in the hardened closure state
vocabulary, as the driven report states it. The product is invoked
through run_tool, which runs the module entry route as a
subprocess.
"""
import re

from tests.fixture_builder import (
    FixtureTestCase, build_case, f16_miniature_case, gate_record,
    metrics_record, run_tool, step_record, tracked_tempdir)

METRICS_PATH = "wiki/wiki/synthesis/build-metrics-record.md"

# The six reason code definition lines standing today, byte for
# byte, in the order the driven report prints them. These lines
# must stay present and unchanged in wording.
SIX_CODE_LINES = [
    "date-only-form: the record carries dates only, with no time "
    "of day, where a time of day is required",
    "missing-field: a field the derivation requires does not "
    "stand in the record",
    "no code fits: the code list holds no code naming the case "
    "the records stand in",
    "no-feeder-record: no feeder record for the metric stands "
    "in the tree",
    "no-post-triage-breakdown: no post triage severity breakdown "
    "stands in the form the row counts from",
    "no-measurement-basis: no measurement basis for the figure "
    "stands in the records",
]

# The added term lines the cure must carry, label and definition,
# in register order. The definitions of broken link, form required
# and form held stand in the report_renderer.py fallback glossary
# and are carried in its wording exactly. Every other term has no
# glossary entry anywhere in the product; its wording is taken
# from the brief passages that govern its row, as the register
# entry for R16-09 cites them.
ADDED_TERM_LINES = [
    "broken link: the link that broke, naming the missing "
    "record, the missing field, or the wrong form where the "
    "break stands in one of those forms",
    "feeder: a record inside the root that a row rests on and "
    "takes its figures or its position from",
    "feeder record: the record that stands as the feeder for a "
    "row; a row whose feeder record does not stand in the tree "
    "is missing",
    "derivation: the working out of a row figure from its "
    "feeder records under the settled definitions",
    "derivable: a row is derivable where its figure can be "
    "worked out from its feeder records in the forms its "
    "derivation requires; present but not derivable means feeder "
    "material stands but no figure can be worked out from it",
    "BANKED: the named state of an item that stands banked, "
    "waiting on a decision, and of an interval recorded under "
    "that state in the path ledger",
    "base: the starting staffing count stated for a step, "
    "against which the staffed count and the additions over "
    "base are read",
    "spin-ups: agents added for a step above its base, counted "
    "from roster addition entries for that step and never from "
    "a total alone",
    "total spins: the total spins figure stated for a step in "
    "its feeder records, standing apart from its base figure "
    "and from its roster additions",
    "roster additions: the entries in a roster or closing "
    "record that name the agents added over the base for a step",
    "form required: the form the derivation required",
    "form held: the form or the absence the record actually held",
    "flow scale: the settled severity scale a post triage "
    "breakdown is stated under, whose levels are Critical, "
    "High, Medium and Low",
    "triage: the judging of a finding or an entry that settles "
    "its severity and the step it is charged to before it is "
    "counted",
    "post triage: the position after triage; a post triage "
    "breakdown states the counts of a round as judged at "
    "triage, under the flow scale",
    "hardened closure state vocabulary: the settled set of "
    "named closure states a gate record or gate ruling can "
    "state; a recorded closure state matching no name in that "
    "set counts as no named closure form",
    "LANDED: the first trace outcome where the item checked "
    "stands landed at the first trace",
    "PARTIAL: the first trace outcome where the item checked "
    "stands only partly landed at the first trace",
    "CONTRADICTED: the first trace outcome where the item "
    "checked stands contradicted at the first trace",
    "first trace: the first fold in trace over a set of items, "
    "at which the outcome of each item checked is counted as "
    "LANDED, PARTIAL or CONTRADICTED",
    "sum test: the check that the parts of a trace contribution "
    "add to the total its record states; a contribution whose "
    "parts do not sum to its stated total stands excepted",
    "proxy: a labelled figure that stands in place of a "
    "position it does not measure; a proxy figure is reported "
    "as a proxy only and never as a token or money figure",
    "documented units: the units of the labelled proxy basis "
    "stated in the records, in which a proxy figure is counted",
    "foundation statement: the statement on the D-1 row naming "
    "the feeder that row rests on and the exception or rule "
    "that lets it rest there",
    "degraded form: the weaker form of a row that relaxes one "
    "named check only; the T-4 degraded form relaxes the queue "
    "cross check only and still requires the same durations as "
    "the full form",
    "queue cross check: the check of a row position against "
    "the decision queue file inside the root, where that file "
    "stands",
    "outcome record: a record that states the outcome of a "
    "round or of a step in a form the derivation names, by "
    "which records are mapped to rounds",
    "List 3: the code list the data quality section refers to; "
    "where List 3 holds no code naming a case, that case stands "
    "recorded as no code fits",
]

# One body pattern per added term label, in the same order as
# ADDED_TERM_LINES: the pattern the driven report body, above its
# Terms section, must match for the term to stand used there.
ADDED_TERM_BODY_PATTERNS = [
    r"broken link", r"feeder", r"feeder record", r"derivation",
    r"derivable", r"\bBANKED\b", r"\bbase\b", r"[Ss]pin-ups",
    r"total spins", r"roster additions?", r"form required",
    r"form held", r"flow scale", r"\btriage\b", r"post[ -]triage",
    r"hardened closure state vocabulary", r"\bLANDED\b",
    r"\bPARTIAL\b", r"\bCONTRADICTED\b", r"first trace",
    r"sum test", r"\bproxy\b", r"documented units",
    r"[Ff]oundation statement", r"degraded form",
    r"queue cross check", r"outcome record\b", r"\bList 3\b",
]

# Terms the control report body never uses, in label form. Its
# Terms section must carry no line for any of them.
CONTROL_ABSENT_LABELS = [
    "List 3", "flow scale", "triage", "post triage",
    "hardened closure state vocabulary", "degraded form",
    "queue cross check", "sum test", "proxy", "documented units",
    "CONTRADICTED", "derivation", "outcome record",
]

# Terms the control report body does use, in label form. Its
# Terms section must carry a line for each of them.
CONTROL_USED_LABELS = [
    "broken link", "form required", "form held", "feeder",
    "feeder record", "derivable", "BANKED", "base", "spin-ups",
    "total spins", "roster additions", "foundation statement",
    "first trace",
]


def _foldin_files():
    """The fold in shape files: the F-16 miniature, one change.

    The gate files of the miniature state a closure state; the
    driven report states none. Removing the closure state line
    from every gate file of the miniature gives the driven form,
    in which the F-2 row states the hardened closure state
    vocabulary position step by step. Every other file stands
    byte for byte as the miniature states it.
    """
    case = f16_miniature_case()
    files = dict(case["files"])
    for rel in list(files):
        if "gate-record" in rel or "gate-ruling" in rel:
            files[rel] = files[rel].replace(
                "Closure state: CLOSED-PASS.\n", "")
    return case["features"], files


def _control_files():
    """The control tree files: a small complete tree, steps 1 to 3.

    Its rows use only the standing terms of the small tree form:
    no loop rounds case, no severity breakdown, no proxy figure,
    no trace contribution and no banked wait form stands in it,
    so none of the added terms of the fold in shape stands used
    in its body beyond the standing small tree terms.
    """
    files = {}
    transitions = []
    for n in (1, 2, 3):
        files["steps/step-%02d-record.md" % n] = step_record(n)
        files["steps/step-%02d-gate-record.md" % n] = gate_record(n)
        transitions.append(
            "Step %d IN PROGRESS 2026-11-01 09:00, closed "
            "2026-11-01 17:00." % n)
    files["PATH-LEDGER.md"] = (
        "# Path ledger\n\nSteps stated: 1, 2, 3.\n\n"
        "## Transitions\n\n%s\n" % "\n".join(transitions))
    files["TIER-RECORD.md"] = "# Tier record\n\nTier: Low. Base: 2.\n"
    files[METRICS_PATH] = metrics_record(
        body="Step table stands complete for the fixture steps.")
    return files


def _run(files, features=()):
    root = tracked_tempdir("msc_step16_unit4_")
    built = build_case(
        {"name": "u4-tree", "features": tuple(features),
         "files": files}, root)
    result = run_tool(built)
    return result


def _terms_lines(report):
    """Return the lines of the Terms section of one report."""
    lines = report.splitlines()
    if "Terms" not in lines:
        return []
    return lines[lines.index("Terms") + 1:]


def _body(report):
    """Return the report above its Terms section."""
    lines = report.splitlines()
    if "Terms" not in lines:
        return report
    return "\n".join(lines[:lines.index("Terms")])


class TestStep16Unit4(FixtureTestCase):

    def test_r16_09_foldin_shape_terms_defines_every_required_term(self):
        """R16-09, defect form: every register term stands defined."""
        features, files = _foldin_files()
        result = _run(files, features)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        body = _body(result.stdout)
        terms = _terms_lines(result.stdout)
        labels = [line.split(":", 1)[0] for line in ADDED_TERM_LINES]
        for label, pattern in zip(labels, ADDED_TERM_BODY_PATTERNS):
            self.assertRegex(
                body, pattern,
                "the fold in shape body does not use the term: "
                + label)
        for line in ADDED_TERM_LINES:
            self.assertIn(line, terms)

    def test_r16_09_six_reason_code_definitions_unchanged(self):
        """R16-09, standing codes: the six lines stand unchanged."""
        features, files = _foldin_files()
        result = _run(files, features)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        terms = _terms_lines(result.stdout)
        self.assertEqual(terms[:len(SIX_CODE_LINES)], SIX_CODE_LINES)

    def test_r16_09_control_terms_not_used_gain_no_definitions(self):
        """R16-09, restraint: unused terms gain no definition line."""
        result = _run(_control_files())
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        terms = _terms_lines(result.stdout)
        for label in CONTROL_ABSENT_LABELS:
            self.assertFalse(
                any(line.startswith(label + ":") for line in terms),
                "the control Terms section defines a term its rows "
                "never use: " + label)

    def test_r16_09_control_terms_used_stand_defined(self):
        """R16-09, usage form: the terms the control uses stand defined."""
        result = _run(_control_files())
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        terms = _terms_lines(result.stdout)
        for label in CONTROL_USED_LABELS:
            self.assertTrue(
                any(line.startswith(label + ":") for line in terms),
                "the control Terms section does not define a term "
                "its rows use: " + label)


if __name__ == "__main__":
    import unittest
    unittest.main()
