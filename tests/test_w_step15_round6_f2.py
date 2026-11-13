"""Step 15 fix round 6 tests: F-2 governing piece selection.

Each case pins one fix round 6 finding in derivation_core.py:
F15-39, the F15-30 selection in _f2_first_closure holding two
limbs, so a scan past a head piece carrying no content walked
past a substantive piece carrying no closure, and past a
disagreement merged piece, to a closure standing behind them,
counting a ruling the standing head rule denies. The governing
test is one test in ranked order: the first piece carrying
substantive text governs, closure or not derivable, a
disagreement merged piece also governs as contested, and only
pieces carrying neither are passed over.
Control cases pin the behaviour that must not move: the twin
trees with no gate record standing, where the substantive no
closure piece is itself the head; the CB4-1 form where a no
content gate record beside a sound ruling still counts the
ruling; and identical duplicate gate records merging as one
substantive piece, not as a disagreement.
"""
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, gate_record,
                                     gate_ruling, row_block, run_tool)

NO_CLOSURE_RULING = ("# Step 2 gate ruling\n\n"
                     "The ruling stands with no closure stated.\n")
NO_CLOSURE_ADJUDICATION = ("# Step 2 gate adjudication\n\n"
                           "The adjudication stands with no closure "
                           "stated.\n")


class TestStep15Round6F2(FixtureTestCase):

    def _assert_f2_not_derivable(self, root):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        self.assertNotIn("100 percent", block)
        self.assertIn("plain approvals 0", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 0", block)
        self.assertIn("carry no first ruling outcome", block)
        self.assertIn("Step 2", block)
        return block

    def _assert_f2_single_pass(self, root):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 100 percent", block)
        self.assertIn("plain approvals 1", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 1", block)
        self.assertNotIn("carry no first ruling outcome", block)
        return block

    def _directory_gate_record(self, root):
        gate = root / "steps" / "step-02-gate-record.md"
        gate.unlink()
        gate.mkdir()

    # ------------------------------------------------------------ form (a)

    def test_f15_39_directory_before_no_closure_ruling_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = NO_CLOSURE_RULING
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._directory_gate_record(root)
        self._assert_f2_not_derivable(root)

    def test_f15_39_twin_no_gate_record_no_closure_ruling_not_derivable(self):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-ruling.md"] = NO_CLOSURE_RULING
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._assert_f2_not_derivable(root)

    # ------------------------------------------------------------ form (b)

    def test_f15_39_regate_directory_before_no_closure_adjudication(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-adjudication.md"] = \
            NO_CLOSURE_ADJUDICATION
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        self._directory_gate_record(root)
        self._assert_f2_not_derivable(root)

    def test_f15_39_regate_twin_no_gate_record_no_closure_adjudication(self):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-adjudication.md"] = \
            NO_CLOSURE_ADJUDICATION
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        self._assert_f2_not_derivable(root)

    # ------------------------------------------------------------ form (c)

    def test_f15_39_disagreement_record_with_ruling_behind_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/sub/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-FAIL")
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._assert_f2_not_derivable(root)

    # ------------------------------------------------------------ controls

    def test_f15_39_control_directory_record_sound_ruling_counts(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._directory_gate_record(root)
        self._assert_f2_single_pass(root)

    def test_f15_39_control_identical_duplicate_record_counts(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/sub/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._assert_f2_single_pass(root)


if __name__ == "__main__":
    unittest.main()
