"""Step 16 fix unit 3 tests: the partial cause statement.

Pinning tests for register item R16-05 (Medium) of Step 16 round 1.
Where the partial position rests on the no steps evidenced limb,
the report marks itself partial in both governed places and, under
brief D4R-08, its coverage statement must state that cause and name
the pieces missing and the steps not covered. The defect form is
the run (c) form of the correctness paper: every recognised piece
read in full, no limit crossed, the step universe at 0 steps
evidenced because the tree keeps its step record in a near match
form, and no line stating why the report is partial or naming the
pieces missing.

The trees are constructed in the run (c) shape by this module,
rather than driving the real Touchstone tree, because a suite test
must stand on files inside the suite alone: the real tree stands
outside the product repo and is not carried to the bench the suite
runs on. The constructed form keeps every fact the correctness
paper establishes for run (c): the path ledger states Step 1, the
step record stands in the near match form steps/step-1-record.md,
the recognised pieces stand read in full, and no limit is crossed.

The bounded controls stand in the run (a) and run (b) shapes. In
run (a) the partial position rests on a smaller evidenced set
beside the taken set, and in run (b) on a step in the taken set
with no closing gate record; in both shapes the naming duty stands
discharged through other coverage lines, and their partial
statements must stay byte for byte as they stand. A complete tree
stands as the non partial control: it carries no partial statement
at all. The product is invoked through run_tool, which runs the
module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, coverage_statement, gate_record, metrics_record,
    run_tool, step_record, tracked_tempdir)

METRICS_PATH = "wiki/wiki/synthesis/build-metrics-record.md"


def _base_files():
    """The small complete tree files, steps 1 to 3, as plain data."""
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


def _run_c_files():
    """The run (c) shape: Step 1 stated, its record a near match."""
    files = {}
    files["PATH-LEDGER.md"] = (
        "# Path ledger\n\nSteps stated: 1.\n\n"
        "## Transitions\n\n"
        "Step 1 IN PROGRESS 2026-11-01 09:00, closed "
        "2026-11-01 17:00.\n")
    files["TIER-RECORD.md"] = "# Tier record\n\nTier: Low. Base: 2.\n"
    files[METRICS_PATH] = metrics_record(
        body="Step table stands complete for the fixture steps.")
    files["steps/step-1-record.md"] = step_record(1)
    return files


def _write_tree(files):
    """Write one tree under a tracked temporary directory."""
    root = tracked_tempdir("msc_step16_unit3_") / "tree"
    for rel in sorted(files):
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(files[rel], encoding="utf-8")
    return root


def _line(report, prefix):
    """Return the one report line opening with the given prefix."""
    found = [ln for ln in report.splitlines()
             if ln.startswith(prefix)]
    return found[0] if len(found) == 1 else None


class TestStep16Unit3(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def test_r16_05_no_steps_evidenced_names_missing_pieces(self):
        """R16-05, run (c) form: the cause and the pieces stand named."""
        report = self._run(_run_c_files())
        self.assertIn("Coverage taken set: no steps evidenced in "
                      "the capture", report)
        self.assertIn("Coverage partial: partial report", report)
        self.assertIn("Limit: no limit crossed", report)
        self.assertIn("Reading: partial", report)
        coverage = coverage_statement(report)
        self.assertIn("partial cause: no step stands evidenced in "
                      "the capture", coverage)
        self.assertIn("steps not covered: Step 1", coverage)
        self.assertIn("pieces missing: the step record for Step 1 "
                      "(steps/step-01-record.md)", coverage)
        self.assertIn("the gate record for Step 1 "
                      "(steps/step-01-gate-record.md)", coverage)
        self.assertIn("each a missing piece, absent from the "
                      "capture", coverage)

    def test_r16_05_no_steps_evidenced_two_stated_steps(self):
        """R16-05, wider form: every stated step and piece is named."""
        files = _run_c_files()
        del files["steps/step-1-record.md"]
        files["PATH-LEDGER.md"] = (
            "# Path ledger\n\nSteps stated: 1, 2.\n\n"
            "## Transitions\n\n"
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed "
            "2026-11-01 17:00.\n"
            "Step 2 IN PROGRESS 2026-11-01 09:00, closed "
            "2026-11-01 17:00.\n")
        report = self._run(files)
        self.assertIn("Coverage partial: partial report", report)
        coverage = coverage_statement(report)
        self.assertIn("partial cause: no step stands evidenced in "
                      "the capture", coverage)
        self.assertIn("steps not covered: Steps 1 and 2", coverage)
        for step in (1, 2):
            self.assertIn("the step record for Step %d "
                          "(steps/step-%02d-record.md)" % (step, step),
                          coverage)
            self.assertIn("the gate record for Step %d "
                          "(steps/step-%02d-gate-record.md)"
                          % (step, step), coverage)

    def test_r16_05_control_run_a_smaller_set_unchanged(self):
        """Bounded control, run (a) shape: statements byte for byte."""
        files = _base_files()
        transitions = []
        for n in (1, 2):
            transitions.append(
                "Step %d IN PROGRESS 2026-11-01 09:00, closed "
                "2026-11-01 17:00." % n)
        files["PATH-LEDGER.md"] = (
            "# Path ledger\n\nSteps stated: 1, 2.\n\n"
            "## Transitions\n\n%s\n" % "\n".join(transitions))
        report = self._run(files)
        self.assertEqual(
            _line(report, "Coverage smaller set: "),
            "Coverage smaller set: Steps 1 and 2, stated in "
            "PATH-LEDGER.md, which stops there")
        self.assertEqual(
            _line(report, "Coverage statement: "),
            "Coverage statement: step universe 3 steps evidenced "
            "(Step 1, Step 2, Step 3); 9 pieces recognised in the "
            "capture; 17 rows in starter set order; disagreements: "
            "the path ledger states steps Step 1, Step 2 while step "
            "records and gate files evidence steps Step 1, Step 2, "
            "Step 3; build state: in progress")
        self.assertEqual(_line(report, "Coverage partial: "),
                         "Coverage partial: partial report")
        self.assertNotIn("partial cause: no step stands evidenced",
                         report)

    def test_r16_05_control_run_b_uncovered_step_unchanged(self):
        """Bounded control, run (b) shape: statements byte for byte."""
        files = _base_files()
        del files["steps/step-03-gate-record.md"]
        report = self._run(files)
        self.assertEqual(
            _line(report, "Coverage uncovered steps: "),
            "Coverage uncovered steps: Step 3, with no gate record "
            "standing in the capture")
        self.assertEqual(
            _line(report, "Coverage statement: "),
            "Coverage statement: step universe 3 steps evidenced "
            "(Step 1, Step 2, Step 3); 8 pieces recognised in the "
            "capture; 17 rows in starter set order; build state: in "
            "progress; the closing ruling for Step 3 "
            "(steps/step-03-gate-record.md) is a missing piece, "
            "absent from the capture")
        self.assertEqual(_line(report, "Coverage partial: "),
                         "Coverage partial: partial report")
        self.assertEqual(
            _line(report, "Coverage open state: "),
            "Coverage open state: the build stands in progress, "
            "with Step 3 not yet closed")
        self.assertNotIn("partial cause: no step stands evidenced",
                         report)

    def test_r16_05_control_complete_report_not_partial(self):
        """Non partial control: a complete report, no partial line."""
        report = self._run(_base_files())
        self.assertEqual(_line(report, "Coverage partial: "),
                         "Coverage partial: full report")
        self.assertEqual(
            _line(report, "Coverage statement: "),
            "Coverage statement: step universe 3 steps evidenced "
            "(Step 1, Step 2, Step 3); 9 pieces recognised in the "
            "capture; 17 rows in starter set order; build state: in "
            "progress")
        run_cost = _line(report, "Run cost: ")
        self.assertIsNotNone(run_cost)
        self.assertIn("Reading: full", run_cost)
        self.assertNotIn("partial cause", report)
        self.assertNotIn("pieces missing", report)


if __name__ == "__main__":
    import unittest
    unittest.main()
