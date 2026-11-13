"""Step 15 fix round 5 tests: F-2 selection pair.

Each case pins one fix round 5 finding in derivation_core.py:
F15-30, the F-2 counting taking ranked[0] for a step across every
gate alias form, so a gate record carrying no content and no
closure erases a sound ruling or adjudication at another alias
form of the same step; and F15-38, derive_report building
f2_counted for the staffing cross check without the F15-14 base
closure conflict guard, so the cross check statement claims a
conflicted step was counted while the figures exclude it.
Control cases pin the behaviour that must not move: the F15-14
conflict guard in both its forms, the standing not derivable form
where no piece at a step carries a settled closure, and the cross
check claim where a contested step is counted in truth.
"""
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, gate_record,
                                     gate_ruling, metrics_record,
                                     row_block, run_tool)

COUNTED_CLAIM = ("support a first ruling for Step 3 counted in "
                 "the denominator on the evidenced universe")


class TestStep15Round5F2(FixtureTestCase):

    # ------------------------------------------------------------ F15-30

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

    def test_f15_30_directory_gate_record_sound_ruling_counts(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        root = build_tree(table)
        gate = root / "steps" / "step-02-gate-record.md"
        gate.unlink()
        gate.mkdir()
        self._assert_f2_single_pass(root)

    def test_f15_30_zero_byte_gate_record_sound_ruling_counts(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = b""
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._assert_f2_single_pass(root)

    def test_f15_30_malformed_gate_record_sound_ruling_counts(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = \
            b"\xff\xfe not a gate record \x80"
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._assert_f2_single_pass(root)

    def test_f15_30_malformed_ruling_sound_adjudication_counts(self):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-ruling.md"] = \
            b"\xff\xfe not a gate ruling \x80"
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-PASS")
        root = build_tree(table)
        self._assert_f2_single_pass(root)

    def test_f15_30_directory_gate_record_sound_ruling_fail_counts(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-FAIL")
        root = build_tree(table)
        gate = root / "steps" / "step-02-gate-record.md"
        gate.unlink()
        gate.mkdir()
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 0 percent", block)
        self.assertIn("plain approvals 0", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 1", block)
        self.assertIn("Step 2 ruled and not approved", block)
        self.assertNotIn("carry no first ruling outcome", block)

    def test_f15_30_control_conflicting_base_pair_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-FAIL")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        self.assertIn("plain approvals 0", block)
        self.assertIn("steps ruled on 0", block)

    def test_f15_30_control_conflict_with_regate_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        self.assertNotIn("100 percent", block)
        self.assertIn("plain approvals 0", block)
        self.assertIn("steps ruled on 0", block)

    def test_f15_30_control_no_closure_anywhere_not_derivable(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-ruling.md"] = (
            "# Step 2 gate ruling\n\n"
            "The ruling stands with no closure stated.\n")
        root = build_tree(table)
        gate = root / "steps" / "step-02-gate-record.md"
        gate.unlink()
        gate.mkdir()
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        self.assertIn("plain approvals 0", block)
        self.assertIn("steps ruled on 0", block)
        self.assertIn("carry no first ruling outcome", block)
        self.assertIn("Step 2", block)

    def test_f15_30_control_substantive_head_no_closure_not_derivable(self):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-adjudication.md"] = (
            "# Step 2 gate adjudication\n\n"
            "The adjudication stands with no closure stated.\n")
        table["steps/step-02-gate-ruling-reaudit-8.md"] = \
            gate_ruling(2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        self.assertIn("plain approvals 0", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 0", block)
        self.assertIn("carry no first ruling outcome", block)
        self.assertIn("Step 2", block)

    # ------------------------------------------------------------ F15-38

    def _contested_conflict_tree(self, with_regate):
        table = base_case(steps=(1, 2, 3))
        table["steps/step-03-gate-ruling.md"] = gate_ruling(
            3, "CLOSED-FAIL")
        if with_regate:
            table["steps/step-03-regate-record.md"] = gate_record(
                3, "CLOSED-QUALIFIED")
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(
                body="Step universe as 2 steps is stated here.")
        return build_tree(table)

    def _assert_conflicted_step_not_claimed_counted(self, root):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present but not derivable", "F-2")
        self.assertIn("plain approvals 2", block)
        self.assertIn("steps ruled on 2", block)
        self.assertNotIn(COUNTED_CLAIM, block)
        self.assertNotIn("for Step 3 counted in the denominator",
                         block)
        return block

    def test_f15_38_conflicted_contested_with_regate_not_claimed(self):
        self._assert_conflicted_step_not_claimed_counted(
            self._contested_conflict_tree(True))

    def test_f15_38_conflicted_contested_without_regate_not_claimed(self):
        self._assert_conflicted_step_not_claimed_counted(
            self._contested_conflict_tree(False))

    def test_f15_38_control_contested_counted_step_claimed(self):
        table = base_case(steps=(1, 2, 3))
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(
                body="Step universe as 2 steps is stated here.")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("plain approvals 3", block)
        self.assertIn("steps ruled on 3", block)
        self.assertIn(COUNTED_CLAIM, block)


if __name__ == "__main__":
    unittest.main()
