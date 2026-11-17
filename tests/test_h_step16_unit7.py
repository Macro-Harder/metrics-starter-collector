"""Step 16 fix unit 7 tests: the wording group.

Pinning tests for register items R16-10, R16-22, R16-19 and
R16-18 of Step 16 round 1, all Low, all wording or state form
only. No verdict, figure, count or reason outside the four
named wordings may change.

R16-10, the B-1 part of U-R3 (spins 1103, 1105, 1106). The B-1
row on a tree whose T-1 and T-2 inputs both stand missing ends
by stating that both ranking inputs are missing, so no split
or ranking figure exists for this row, under a rule named the
B-1 ranking input rule. B-1 is a totals row: brief Section 1,
B-1, its feeders are the step elapsed and step active figures
only, and gap DG-06 clause 3 gives its missing form on those
inputs. It has no ranking inputs, no split and no ranking
figure. The cure these tests pin: the closing clause names
both inputs missing and no build total figure, in the totals
words of the row itself.

R16-22, U-08 (spins 1103, 1106, 1108), code wording only. Where
a cost ledger stands in the tree and carries no token figure,
the E-3 row reason token is no-feeder-record and its follows
text states that no feeder record for the metric exists in the
tree, while its own form held text states that the cost ledger
stands in the tree, and the Terms line at the foot of the same
report defines no-feeder-record in the words the held text
denies. The verdict, missing, stands. The cure these tests pin:
the branch carries the missing-field code, the code for a field
the derivation requires that does not stand in the record, and
a follows sentence that states the ledger stands and no token
figure stands in it. The Unit 1 behaviour at the same branch,
present but not derivable where the ledger stands unread past
a limit, and missing with the no-feeder-record code only where
no ledger stands at all, stays exactly as Unit 1 left it.

R16-19, U16D-03 (spins 1104, 1106, 1107). A link out of the
tree at a recognised record name is flagged in the piece
inventory with the state word unreadable, the same word used
for a permission failure, and with the size of the target file
outside the tree. Governing passages: brief Section 5, the
discovery and census component, a record inside the tree that
names a path outside the root is not followed, and the pointed
piece is flagged in the piece inventory as outside the root
and not read; and the piece inventory data shape in the same
section, whose reading states are read in full, malformed, not
read past a limit, or outside the root and not read. The cure
these tests pin: the outside link carries the brief state,
outside the root and not read, in the inventory and in the
coverage piece line, and prints no outside size; the size
printed for the piece is 0 bytes, the size of nothing inside
the tree. A genuinely unreadable piece inside the root keeps
the state word unreadable, and the outside link keeps its
piece treatment as Unit 6 pinned it: counted once in files
visited, not followed, and no figure taken from it.

R16-18, U16D-02 (spins 1104, 1106, 1107). One walk bound
piece data quality entry names two bounds as the limit that
cut the capture: its piece reason names the whole walk bound,
and its walk order sample then names a tree limit. The cure
these tests pin: the sample names the one bound that actually
cut that piece, the bound its own capture reason names. A
capture cut by a single tree limit names that limit in the
sample exactly as it does today.
"""
import os

from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, capture_derive_render,
    data_quality_entry_for, gate_record, metrics_record,
    row_block, run_tool, step_record, tracked_tempdir)

LEDGER_PATH = "registers/cost-ledger.md"
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


def _write_tree(files):
    """Write one tree under a tracked temporary directory."""
    holder = tracked_tempdir("msc_step16_unit7_")
    root = holder / "tree"
    for rel in sorted(files):
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(files[rel], encoding="utf-8")
    return holder, root


def _line(report, prefix):
    """Return the one report line opening with the given prefix."""
    found = [ln for ln in report.splitlines()
             if ln.startswith(prefix)]
    return found[0] if len(found) == 1 else None


def _sample_segment(entry_line):
    """Return the walk order sample segment of one entry line."""
    at = entry_line.find("walk order sample:")
    return entry_line[at:] if at >= 0 else ""


class TestStep16Unit7(FixtureTestCase):

    def _run(self, files):
        holder, root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return holder, root, result.stdout

    # R16-10

    def test_r16_10_b1_both_inputs_missing_totals_wording(self):
        """R16-10 defect: the B-1 closing clause names its own inputs."""
        files = _base_files()
        files["PATH-LEDGER.md"] = (
            "# Path ledger\n\nSteps stated: 1, 2, 3.\n\n"
            "## Transitions\n\n"
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-01.\n"
            "Step 2 IN PROGRESS 2026-11-02, closed 2026-11-02.\n"
            "Step 3 IN PROGRESS 2026-11-03, closed 2026-11-03.\n")
        holder, root, report = self._run(files)
        block = row_block(report, "B-1")
        assert_verdict(self, block, "missing", "B-1")
        self.assertIn(
            "both inputs are missing, so no build total figure "
            "exists for this row", block)
        self.assertNotIn("ranking", block)
        self.assertNotIn("split", block)
        self.assertIn(
            "the step elapsed and step active figures that are "
            "this row's only inputs", block)
        self.assertIn(
            "both inputs are missing on the date only ground",
            block)

    def test_r16_10_control_b1_present_row_unchanged(self):
        """Control: a B-1 row with inputs present stands byte for byte."""
        holder, root, report = self._run(_base_files())
        block = row_block(report, "B-1")
        first = block.splitlines()[0]
        self.assertEqual(
            first,
            "B-1 Total build elapsed and active time | Verdict: "
            "present | Value: build elapsed 24 hours and build "
            "active 24 hours over 3 steps: Step 1 elapsed 8 "
            "hours, active 8 hours; Step 2 elapsed 8 hours, "
            "active 8 hours; Step 3 elapsed 8 hours, active 8 "
            "hours | Row coverage: denominator step universe 3 "
            "steps | Reconciled against: the metric carries no "
            "total to reconcile against | Pointer: the step "
            "table rows and the build summary, with the closing "
            "gate ruling for the last step (PATH-LEDGER.md)")

    # R16-22

    def test_r16_22_e3_ledger_standing_no_token_code_wording(self):
        """R16-22 defect: the standing ledger branch code and follows."""
        files = _base_files()
        files[LEDGER_PATH] = (
            "# Cost ledger\n\nNo figures recorded here.\n")
        holder, root, report = self._run(files)
        block = row_block(report, "E-3")
        assert_verdict(self, block, "missing", "E-3")
        self.assertIn("missing-field", block)
        self.assertIn(
            "the cost ledger stands in the tree and no token "
            "figure stands in it, so the row is missing", block)
        self.assertNotIn("no-feeder-record", block)
        self.assertNotIn(
            "no feeder record for the metric exists", block)
        self.assertIn(
            "form held, the cost ledger stands in the tree and "
            "no token figure stands in it", block)

    def test_r16_22_control_e3_unread_and_absent_ledger_unchanged(self):
        """Control: the Unit 1 unread form and the absent form stand."""
        files = _base_files()
        files[LEDGER_PATH] = (
            "# Cost ledger\n\nStep 1: money 10, tokens 1000.\n"
            + "x" * 1100000)
        holder, root, report = self._run(files)
        block = row_block(report, "E-3")
        assert_verdict(self, block, "present but not derivable",
                       "E-3")
        self.assertIn(
            "registers/cost-ledger.md, which stands not read "
            "past a limit: the file limit of 1000000 bytes was "
            "crossed", block)
        self.assertIn(
            "no token figure is claimed absent from a piece "
            "that was not read", block)
        self.assertIn("over-limit-piece", block)
        holder, root, report = self._run(_base_files())
        block = row_block(report, "E-3")
        assert_verdict(self, block, "missing", "E-3")
        self.assertIn(
            "no-feeder-record no feeder record for the metric "
            "exists in the tree, so the row is missing", block)
        self.assertIn("no cost ledger stands in the tree", block)

    # R16-19

    def test_r16_19_outside_link_state_and_no_outside_size(self):
        """R16-19 defect: the outside link state and its printed size."""
        holder, root, report = self._run(_base_files())
        outside = holder / "outside-step.md"
        text = step_record(9)
        text += "x" * (157 - len(text.encode("utf-8")))
        outside.write_text(text, encoding="utf-8")
        self.assertEqual(outside.stat().st_size, 157)
        os.symlink(str(outside),
                   str(root / "steps" / "step-09-record.md"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        report = result.stdout
        self.assertIn(
            "Piece steps/step-09-record.md | step record | "
            "0 bytes | outside the root and not read", report)
        coverage = [ln for ln in report.splitlines()
                    if ln.startswith("Coverage piece not read in "
                                     "full: steps/step-09-record.md")]
        self.assertEqual(len(coverage), 1)
        self.assertIn("0 bytes | outside the root and not read",
                      coverage[0])
        self.assertNotIn("157 bytes", report)

    def test_r16_19_control_unreadable_inside_root_keeps_state_word(self):
        """Control: a piece unreadable inside the root keeps its word."""
        holder, root = _write_tree(_base_files())
        (root / "steps" / "step-09-record.md").mkdir(parents=True)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        report = result.stdout
        self.assertIn(
            "Piece steps/step-09-record.md | step record | "
            "0 bytes | unreadable", report)
        coverage = [ln for ln in report.splitlines()
                    if ln.startswith("Coverage piece not read in "
                                     "full: steps/step-09-record.md")]
        self.assertEqual(len(coverage), 1)
        self.assertIn("0 bytes | unreadable |", coverage[0])

    def test_r16_19_control_outside_link_piece_treatment_unchanged(self):
        """Control: the outside link piece treatment Unit 6 pinned."""
        holder, root = _write_tree(_base_files())
        outside = holder / "outside-marker.md"
        outside.write_text(
            step_record(9) + "\noutside the root marker\n",
            encoding="utf-8")
        os.symlink(str(outside),
                   str(root / "steps" / "step-09-record.md"))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        report = result.stdout
        self.assertNotIn("outside the root marker", report)
        run_cost = _line(report, "Run cost: ")
        self.assertIsNotNone(run_cost)
        self.assertIn("Files visited: 10", run_cost)
        self.assertIn("Entries visited: 10", run_cost)
        self.assertNotIn("Files not counted", run_cost)
        block = row_block(report, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertIn("Steps 1 to 3 in step order", block)

    # R16-18

    def test_r16_18_walk_bound_piece_sample_names_walk_bound(self):
        """R16-18 defect: the sample names the bound that cut the piece."""
        holder, root = _write_tree(_base_files())
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        import metrics_starter_collector.shell_reader as shell
        standing_walk = shell.WALK_BOUND
        standing_tree = shell.TREE_BYTE_LIMIT
        shell.WALK_BOUND = 5
        shell.TREE_BYTE_LIMIT = 10
        try:
            captured = capture_fn(root)
            report = render_fn(derive_fn(captured))
        finally:
            shell.WALK_BOUND = standing_walk
            shell.TREE_BYTE_LIMIT = standing_tree
        entry = data_quality_entry_for(
            report, "steps/step-01-record.md")
        self.assertTrue(entry, "no data quality entry stands")
        line = entry.splitlines()[0]
        self.assertIn(
            "not visited: the whole walk bound of 5 entries was "
            "crossed before this piece was visited", line)
        sample = _sample_segment(line)
        self.assertIn(
            "walk order sample: the limit that cut the capture "
            "is the whole walk bound", sample)
        self.assertNotIn("tree byte limit", sample)
        self.assertNotIn("tree file limit", sample)

    def test_r16_18_control_single_tree_limit_sample_unchanged(self):
        """Control: a single tree limit cut names that limit as today."""
        holder, root = _write_tree(_base_files())
        capture_fn, derive_fn, render_fn = capture_derive_render(
            self, root)
        import metrics_starter_collector.shell_reader as shell
        standing_tree = shell.TREE_BYTE_LIMIT
        shell.TREE_BYTE_LIMIT = 100
        try:
            captured = capture_fn(root)
            report = render_fn(derive_fn(captured))
        finally:
            shell.TREE_BYTE_LIMIT = standing_tree
        entry = data_quality_entry_for(
            report, "steps/step-01-record.md")
        self.assertTrue(entry, "no data quality entry stands")
        line = entry.splitlines()[0]
        sample = _sample_segment(line)
        self.assertIn(
            "walk order sample: the limit that cut the capture "
            "is the tree byte limit 100 bytes", sample)
        self.assertNotIn("whole walk bound", sample)


if __name__ == "__main__":
    import unittest
    unittest.main()
