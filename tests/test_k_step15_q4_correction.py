"""Step 15 fix round tests: the Q-4 correcting record limb (M-3).

Each case pins one limb of the Audit A M-3 finding. A correcting
record that names the trace it corrects and states the corrected
figure corrects the Q-4 row figure and is cited as the source on
that row, in the record forms the Q-1 and Q-3 limbs recognise: a
register correction (the Q-3 form) and an audit paper correction
(the Q-1 form). A correcting record that states a corrected total
reconciles a step whose trace states two totals, so the brief
section 6 unreconciled rule, applied net of correction, does not
fire for that step. The two control cases pin that the same trees
without a correcting record behave as they do today.
"""
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, row_block,
                                     run_tool, statement_segment)

TRACE_8_OF_10 = "# First trace\n\nElements: 10. LANDED 8, PARTIAL 2.\n"

CORRECTION_FIGURE_REGISTER = (
    "# Correction\n\nThe first trace in steps/step-01-trace.md is "
    "corrected and the corrected figure is 9 of 10 LANDED.\n")

CORRECTION_FIGURE_AUDIT_PAPER = (
    "# Correction\n\nThe first trace in steps/step-01-trace.md is "
    "corrected: the corrected figure is 9 of 10 LANDED.\n")

TRACE_HEADER_105 = "# First trace\n\nPin rows traced: 105\nLANDED: 52\n"

BOARD_RECOUNT_106 = (
    "# Board member statement\n\nBoard recount: 54 non-LANDED in all.\n")

CORRECTION_TOTAL_REGISTER = (
    "# Correction\n\nThe trace in steps/step-01-trace.md is corrected "
    "and the corrected total for that trace is 106.\n")


class TestStep15Q4Correction(FixtureTestCase):

    def test_m3_corrected_figure_register_form_used_and_cited(self):
        table = base_case()
        table["steps/step-01-trace.md"] = TRACE_8_OF_10
        table["registers/correction.md"] = CORRECTION_FIGURE_REGISTER
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("Step 1 first trace 9 of 10 LANDED", block)
        self.assertNotIn("8 of 10", block)
        self.assertIn("Pointer: steps/step-01-trace.md", block)
        segment = statement_segment(block)
        self.assertIn("source citation:", segment)
        self.assertIn("registers/correction.md", segment)
        self.assertNotIn("Pointer: registers/correction.md", block)

    def test_m3_corrected_figure_audit_paper_form_used_and_cited(self):
        table = base_case()
        table["steps/step-01-trace.md"] = TRACE_8_OF_10
        table["audit/step-01-correction.md"] = \
            CORRECTION_FIGURE_AUDIT_PAPER
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("Step 1 first trace 9 of 10 LANDED", block)
        self.assertNotIn("8 of 10", block)
        self.assertIn("Pointer: steps/step-01-trace.md", block)
        segment = statement_segment(block)
        self.assertIn("source citation:", segment)
        self.assertIn("audit/step-01-correction.md", segment)
        self.assertNotIn("Pointer: audit/step-01-correction.md", block)

    def test_m3_corrected_total_reconciles_step_out_of_remainder(self):
        table = base_case()
        table["steps/step-01-trace.md"] = TRACE_HEADER_105
        table["steps/step-01-board-member-1.md"] = BOARD_RECOUNT_106
        table["registers/correction.md"] = CORRECTION_TOTAL_REGISTER
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("Step 1 first trace 52 of 106 LANDED", block)
        self.assertNotIn("105", block)
        self.assertNotIn("remainder Step 1", block)
        self.assertIn("Pointer: steps/step-01-trace.md", block)
        segment = statement_segment(block)
        self.assertIn("source citation:", segment)
        self.assertIn("registers/correction.md", segment)

    def test_m3_control_uncorrected_figure_stands_without_citation(self):
        table = base_case()
        table["steps/step-01-trace.md"] = TRACE_8_OF_10
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("Step 1 first trace 8 of 10 LANDED", block)
        self.assertNotIn("source citation", block.lower())

    def test_m3_control_unreconciled_step_stands_in_remainder(self):
        table = base_case()
        table["steps/step-01-trace.md"] = TRACE_HEADER_105
        table["steps/step-01-board-member-1.md"] = BOARD_RECOUNT_106
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "Q-4")
        assert_verdict(self, block, "present", "Q-4")
        self.assertIn("remainder Step 1", block)
        self.assertIn("105", block)
        self.assertIn("106", block)
        self.assertNotIn("source citation", block.lower())


if __name__ == "__main__":
    unittest.main()
