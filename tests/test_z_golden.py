"""Golden tests on the real subject tree, read in place, run last.

Both golden tests run the product through the pre install invocation
route, as a subprocess, python3 -m metrics_starter_collector from the
public repo root, with the root argument first, against the golden
subject tree at the fold in trace checker design tree, read in place.
The subject tree is never copied and never written to.

The limited test holds the Slice 1 tracer form: for the rows whose
verdict the expected file states as present, it compares verdict,
value and row coverage,
with the Q-4 bound part kept in that form because the Step 13
exception naming stands in the limited expected file, and it defers
the E-1 bound part and every reconciliation part to the certifying
slices. For the other fourteen rows it compares verdict, reason and
pointer only, the refusal form. The full test holds the full row
level form: every part the full expected file carries on a row, in
its stated order, including the bound part and the reconciliation
part on present rows, the reason part on rows that are not present,
and the Statement part on the D-1 row only.

Designed skip: where the golden subject tree is absent, both tests
skip with the reason golden subject tree not present on this machine,
and nothing else in this module skips. Where the tree stands but an
identity fact fails, the test fails with the failed fact named.
"""
import subprocess
import sys
import unittest
from pathlib import Path

from tests.fixture_builder import (FixtureTestCase, GOLDEN_ROOT,
                                     STARTER_ORDER, assert_verdict,
                                     row_block, row_order,
                                     statement_segment)

SKIP_REASON = "golden subject tree not present on this machine"
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
PART_ORDER = ("Verdict", "Value", "Row coverage", "Bound",
              "Reconciled against", "Statement", "Reason", "Pointer")
EXPECTED_IDENTITY = {"files": 309, "bytes": 6747042,
                     "metrics_record_bytes": 133092}
GATE_RECORD_STEPS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                     16, 17, 18, 22)
GATE_RULING_PLAIN_STEPS = (20, 21, 23)


def run_tool(root):
    """Run the product through the module entry route as a subprocess."""
    cmd = [sys.executable, "-m", "metrics_starter_collector", str(root)]
    return subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(REPO_ROOT), timeout=120)


def load_expected(name):
    """Load one golden expected file as an ordered list of rows.

    Each row is a pair, the metric code and its labelled parts in file
    order, each part a pair of its label and its value. The provenance
    line and the subject line carry no metric code and load as no row.
    """
    rows = []
    for line in (HERE / name).read_text(encoding="utf-8").splitlines():
        head, _, _ = line.partition(" | ")
        code = head.split(" ", 1)[0]
        if code not in STARTER_ORDER:
            continue
        parts = []
        for segment in line.split(" | ")[1:]:
            label, _, value = segment.partition(": ")
            parts.append((label, value))
        rows.append((code, parts))
    return rows


def check_identity(test):
    """Assert the golden tree identity facts, or skip if it is absent."""
    if not GOLDEN_ROOT.exists():
        test.skipTest(SKIP_REASON)
    files = [p for p in GOLDEN_ROOT.rglob("*") if p.is_file()]
    test.assertEqual(len(files), EXPECTED_IDENTITY["files"],
                     "golden identity failed: file count")
    total = sum(p.stat().st_size for p in files)
    test.assertEqual(total, EXPECTED_IDENTITY["bytes"],
                     "golden identity failed: tree size in bytes")
    record = (GOLDEN_ROOT / "wiki" / "wiki" / "synthesis"
              / "build-metrics-record.md")
    test.assertTrue(record.is_file(),
                    "golden identity failed: metrics record stands")
    test.assertEqual(record.stat().st_size,
                     EXPECTED_IDENTITY["metrics_record_bytes"],
                     "golden identity failed: metrics record size")
    steps = GOLDEN_ROOT / "steps"
    for step in GATE_RECORD_STEPS:
        name = "step-%02d-gate-record.md" % step
        test.assertTrue((steps / name).is_file(),
                        "golden identity failed: gate form split, "
                        + name + " stands")
    for step in GATE_RULING_PLAIN_STEPS:
        name = "step-%02d-gate-ruling.md" % step
        test.assertTrue((steps / name).is_file(),
                        "golden identity failed: gate form split, "
                        + name + " stands")
    for suffix in ("round2", "round3", "round4"):
        name = "step-20-gate-ruling-%s.md" % suffix
        test.assertTrue((steps / name).is_file(),
                        "golden identity failed: gate form split, "
                        + name + " stands")
    test.assertTrue((steps / "step-19-gate-ruling-reaudit-8.md").is_file(),
                    "golden identity failed: gate form split, Step 19 "
                    "stands in the reaudit 8 ruling form only")
    test.assertFalse((steps / "step-19-gate-ruling.md").exists(),
                     "golden identity failed: gate form split, no plain "
                     "Step 19 gate ruling stands")
    rulings = [p for p in steps.glob("step-*-gate-ruling*.md")
               if p.is_file()]
    test.assertEqual(len(rulings), 7,
                     "golden identity failed: gate ruling file count")


def _printed_part(block, label):
    """Return the printed row's own segment for one labelled part.

    The row line of the block is split into its labelled parts in
    the form the Slice 7 parts_of helper provides: chunks separated
    by space, vertical bar, space, each chunk a label and a value
    divided by colon and space. A part the printed row does not
    carry yields an empty segment, so an assertion against it fails.
    """
    if not block:
        return ""
    line = block.splitlines()[0]
    for chunk in line.split(" | ")[1:]:
        name, _, value = chunk.partition(": ")
        if name.strip() == label:
            return value.strip()
    return ""


def _assert_atoms(test, block, text, code, label):
    """Assert the content of one expected part in its own part segment.

    Every segment of the expected part, short or long, stands
    asserted whole against the printed row's own segment for that
    part, part scoped, never against the row block as a whole, so a
    segment carrying the right numbers and names but the wrong
    wording, or a figure standing in the wrong part, fails the
    comparison.
    """
    part = _printed_part(block, label)
    for segment in text.split(";"):
        segment = segment.strip()
        if not segment:
            continue
        test.assertIn(segment, part,
                      "%s %s part segment does not carry: %s; "
                      "printed part: %s"
                      % (code, label, segment, part[:400]))


def _part(parts, label):
    for name, value in parts:
        if name == label:
            return value
    return None


def _assert_part(test, block, parts, label, code):
    value = _part(parts, label)
    test.assertIsNotNone(value, "%s carries a %s part" % (code, label))
    _assert_atoms(test, block, value, code, label)


def _assert_reason(test, block, parts, code):
    """Assert a reason part through its three named subparts in order."""
    value = _part(parts, "Reason")
    test.assertIsNotNone(value, "%s carries a Reason part" % code)
    lowered = value.lower()
    broken = lowered.find("broken link,")
    required = lowered.find("form required,")
    held = lowered.find("form held,")
    if "broken link," in lowered:
        test.assertTrue(0 <= broken < required < held,
                        "%s reason subpart order" % code)
    _assert_atoms(test, block, value, code, "Reason")


def _assert_no_statement_part(test, block, code):
    test.assertNotIn("Statement:", block,
                     "%s carries no Statement part" % code)


def compare_limited(test, expected_name):
    """The Slice 1 limited comparison, in tracer and refusal form."""
    check_identity(test)
    rows = load_expected(expected_name)
    test.assertEqual([code for code, _ in rows], STARTER_ORDER)
    result = run_tool(GOLDEN_ROOT)
    test.assertEqual(result.returncode, 0, result.stderr)
    test.assertEqual(row_order(result.stdout), STARTER_ORDER)
    for code, parts in rows:
        block = row_block(result.stdout, code)
        test.assertTrue(block, code)
        verdict = _part(parts, "Verdict")
        assert_verdict(test, block, verdict, code)
        if code != "D-1":
            _assert_no_statement_part(test, block, code)
        test.assertIsNone(_part(parts, "Statement"),
                          "%s limited row carries no Statement part" % code)
        if verdict == "present":
            _assert_part(test, block, parts, "Value", code)
            _assert_part(test, block, parts, "Row coverage", code)
            test.assertIsNone(_part(parts, "Reconciled against"),
                              "%s limited row defers its reconciliation "
                              "part" % code)
            if code == "Q-4":
                _assert_part(test, block, parts, "Bound", code)
            else:
                test.assertIsNone(_part(parts, "Bound"),
                                  "%s limited row defers its bound part "
                                  "in tracer form" % code)
        else:
            _assert_reason(test, block, parts, code)
        _assert_part(test, block, parts, "Pointer", code)
    q4 = row_block(result.stdout, "Q-4")
    test.assertRegex(q4, r"(?<!\d)(?<!\d\.)105(?!\d)(?!\.\d)")
    test.assertRegex(q4, r"(?<!\d)(?<!\d\.)106(?!\d)(?!\.\d)")
    test.assertNotIn("record disagrees", statement_segment(q4).lower())


def compare_full(test, expected_name):
    """The full row level comparison, every part in its stated order."""
    check_identity(test)
    rows = load_expected(expected_name)
    test.assertEqual([code for code, _ in rows], STARTER_ORDER)
    result = run_tool(GOLDEN_ROOT)
    test.assertEqual(result.returncode, 0, result.stderr)
    test.assertEqual(row_order(result.stdout), STARTER_ORDER)
    for code, parts in rows:
        labels = [label for label, _ in parts]
        test.assertEqual(labels,
                         [label for label in PART_ORDER
                          if label in labels],
                         "%s part order" % code)
        test.assertEqual(labels[-1], "Pointer",
                         "%s pointer part stands last" % code)
        block = row_block(result.stdout, code)
        test.assertTrue(block, code)
        verdict = _part(parts, "Verdict")
        assert_verdict(test, block, verdict, code)
        if code == "D-1":
            statement = _part(parts, "Statement")
            test.assertIsNotNone(statement,
                                 "D-1 full row carries a Statement part")
            test.assertEqual(labels.index("Statement"),
                             labels.index("Verdict") + 1,
                             "D-1 Statement part stands after the "
                             "Verdict part")
            if "Reason" in labels:
                test.assertLess(labels.index("Statement"),
                                labels.index("Reason"),
                                "D-1 Statement part stands before the "
                                "Reason part")
            test.assertIn("Statement:", block,
                          "D-1 printed row carries a Statement part")
            _assert_atoms(test, block, statement, code, "Statement")
        else:
            test.assertIsNone(_part(parts, "Statement"),
                              "%s carries no Statement part" % code)
            _assert_no_statement_part(test, block, code)
        if verdict == "present":
            _assert_part(test, block, parts, "Value", code)
            if _part(parts, "Row coverage") is not None:
                _assert_part(test, block, parts, "Row coverage", code)
            if _part(parts, "Bound") is not None:
                _assert_part(test, block, parts, "Bound", code)
            _assert_part(test, block, parts, "Reconciled against", code)
        else:
            _assert_reason(test, block, parts, code)
        _assert_part(test, block, parts, "Pointer", code)
    q4 = row_block(result.stdout, "Q-4")
    test.assertRegex(q4, r"(?<!\d)(?<!\d\.)105(?!\d)(?!\.\d)")
    test.assertRegex(q4, r"(?<!\d)(?<!\d\.)106(?!\d)(?!\.\d)")
    test.assertNotIn("record disagrees", statement_segment(q4).lower())


class TestGolden(FixtureTestCase):

    def test_golden_comparison_limited(self):
        compare_limited(self, "golden_expected_limited.txt")

    def test_golden_comparison_full(self):
        compare_full(self, "golden_expected_full.txt")


if __name__ == "__main__":
    unittest.main()
