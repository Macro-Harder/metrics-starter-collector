"""Step 15 fix round 3 tests: derivation core cluster.

Each case pins one fix round 3 finding in derivation_core.py:
F15-23, the regate recycled note scan reading pieces the F-2
counting does not rest on, so the note contradicts the counted
figures; F15-24, T-4 lacking the unreadable feeder split the
ledger rows T-1 and T-2 carry; and F15-25, the T-2 duration test
taking a negated mention of an interval duration as a standing
duration. Control cases pin the behaviour that must not move: the
M-1 recycled step counting by its first ruling, the F15-14 base
closure conflict guard, the genuinely absent ledger wording for
T-4, and the F15-16 statement where a duration genuinely stands.
"""
import os
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, gate_record,
                                     gate_ruling, path_ledger, row_block,
                                     run_tool)


class TestStep15Round3Core(FixtureTestCase):

    # ------------------------------------------------------------ F15-23

    def _assert_pass_with_no_recycled_note(self, block):
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 100 percent", block)
        self.assertIn("plain approvals 1", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 1", block)
        self.assertNotIn("ran as two instances", block)
        self.assertNotIn("was not approved", block)

    def test_f15_23_regate_adjudication_fail_beside_ruling_pass(self):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-ruling.md"] = gate_ruling(
            2, "CLOSED-PASS")
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self._assert_pass_with_no_recycled_note(
            row_block(result.stdout, "F-2"))

    def test_f15_23_regate_adjudication_fail_beside_record_pass(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self._assert_pass_with_no_recycled_note(
            row_block(result.stdout, "F-2"))

    def test_f15_23_regate_round_ruling_fail_beside_record_pass(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-PASS")
        table["steps/step-02-gate-ruling-round-1.md"] = gate_ruling(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self._assert_pass_with_no_recycled_note(
            row_block(result.stdout, "F-2"))

    def test_f15_23_adjudication_first_fail_with_regate_counts_not_approved(self):
        table = base_case(steps=(2,))
        del table["steps/step-02-gate-record.md"]
        table["steps/step-02-gate-adjudication.md"] = gate_record(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 0 percent", block)
        self.assertIn("plain approvals 0", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 1", block)
        self.assertIn("Step 2 ruled and not approved", block)
        self.assertNotIn("ran as two instances", block)

    def test_f15_23_control_recycled_step_still_counted_once_by_first_ruling(self):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = gate_record(
            2, "CLOSED-FAIL")
        table["steps/step-02-regate-record.md"] = gate_record(
            2, "CLOSED-QUALIFIED", extra="Recycled instance ruling.")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, "present", "F-2")
        self.assertIn("first-time approval rate 0 percent", block)
        self.assertIn("plain approvals 0", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 1", block)
        self.assertIn("first instance closed CLOSED-FAIL", block)
        self.assertIn("that first instance was not approved", block)

    def test_f15_23_control_regate_conflicting_base_closures_not_derivable(self):
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

    # ------------------------------------------------------------ F15-24

    def _assert_t4_not_read_in_full(self, root, code_token):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-4")
        assert_verdict(self, block, "present but not derivable", "T-4")
        self.assertIn("present but not read in full", block)
        self.assertIn(code_token, block)
        self.assertNotIn("no-feeder-record", block)
        self.assertNotIn("no feeder record for the metric exists",
                         block)

    def test_f15_24_dangling_path_ledger_t4_named_not_read(self):
        root = build_tree(base_case())
        ledger = root / "PATH-LEDGER.md"
        ledger.unlink()
        os.symlink("gone-ledger.md", str(ledger))
        self._assert_t4_not_read_in_full(root, "unreadable-piece")

    def test_f15_24_fifo_path_ledger_t4_named_not_read(self):
        root = build_tree(base_case())
        ledger = root / "PATH-LEDGER.md"
        ledger.unlink()
        os.mkfifo(str(ledger))
        self._assert_t4_not_read_in_full(root, "unreadable-piece")

    def test_f15_24_malformed_path_ledger_t4_named_not_read(self):
        table = base_case()
        table["PATH-LEDGER.md"] = b"\xff\xfe not a ledger \x80"
        root = build_tree(table)
        self._assert_t4_not_read_in_full(root, "malformed-piece")

    def test_f15_24_absent_path_ledger_t4_wording_unchanged(self):
        table = base_case()
        del table["PATH-LEDGER.md"]
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-4")
        assert_verdict(self, block, "missing", "T-4")
        self.assertIn("no banked state and no decision item count "
                      "stands in the feeder records for this metric",
                      block)
        self.assertIn("no-feeder-record", block)
        self.assertIn("no feeder record for the metric exists in "
                      "the tree, so the row is missing", block)

    # ------------------------------------------------------------ F15-25

    def test_f15_25_negated_duration_date_only_t2_true_ground(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
            "Note: no interval duration is recorded for this step.",
            steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t1 = row_block(result.stdout, "T-1")
        assert_verdict(self, t1, "missing", "T-1")
        self.assertIn("date-only-form", t1)
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("date-only-form", block)
        self.assertIn("no BANKED, SUSPENDED or halt interval "
                      "duration stands", block)
        self.assertNotIn("an interval duration stands in the "
                         "transition log, but no active figure",
                         block)

    def test_f15_25_negated_duration_no_timestamp_t2_true_ground(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 stands with no transitions recorded.\n"
            "Note: no interval duration is recorded for this step.",
            steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("no-feeder-record", block)
        self.assertIn("no interval duration stands in the "
                      "transition log to carry an active figure",
                      block)
        self.assertNotIn("an interval duration stands in the "
                         "transition log, but no active figure",
                         block)

    def test_f15_25_control_genuine_duration_t2_statement_stands(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
            "Step 1 BANKED interval duration 5 hours.",
            steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("no-feeder-record", block)
        self.assertIn("an interval duration stands in the "
                      "transition log", block)


if __name__ == "__main__":
    unittest.main()
