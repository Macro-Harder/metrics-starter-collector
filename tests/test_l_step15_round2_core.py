"""Step 15 fix round 2 tests: derivation core cluster.

Each case pins one fix round 2 finding in derivation_core.py:
F15-14, the regate branch of the F-2 derivation lacking the base
closure conflict guard the non regate branch carries; F15-15, the
unreadable feeder wording split not extended to the path ledger
rows T-1 and T-2; and F15-16, the T-2 fallthrough statement denying
an interval duration that stands. Control cases pin the behaviour
that must not move: the M-1 recycled step counting, the genuinely
absent feeder wording, and the fallthrough statement where no
interval duration stands.
"""
import os
import unittest

from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, gate_record,
                                     gate_ruling, path_ledger, row_block,
                                     run_tool)


class TestStep15Round2Core(FixtureTestCase):

    # ------------------------------------------------------------ F15-14

    def test_f15_14_regate_conflicting_base_closures_not_derivable(self):
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
        self.assertNotIn("first-time approval rate", block)
        self.assertIn("plain approvals 0", block)
        self.assertIn("qualified approvals 0", block)
        self.assertIn("steps ruled on 0", block)

    def test_f15_14_control_without_regate_conflict_not_derivable(self):
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
        self.assertNotIn("100 percent", block)

    def test_f15_14_recycled_step_still_counted_once_by_first_ruling(self):
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

    # ------------------------------------------------------------ F15-15

    def test_f15_15_dangling_path_ledger_t1_and_t2_named_not_read(self):
        root = build_tree(base_case())
        ledger = root / "PATH-LEDGER.md"
        ledger.unlink()
        os.symlink("gone-ledger.md", str(ledger))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        for code in ("T-1", "T-2"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable",
                           code)
            self.assertIn("present but not read in full", block, code)
            self.assertIn("unreadable-piece", block, code)
            self.assertNotIn("no-feeder-record", block, code)
            self.assertNotIn("no path ledger piece stands", block,
                             code)

    def test_f15_15_fifo_path_ledger_t1_and_t2_named_not_read(self):
        root = build_tree(base_case())
        ledger = root / "PATH-LEDGER.md"
        ledger.unlink()
        os.mkfifo(str(ledger))
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        for code in ("T-1", "T-2"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable",
                           code)
            self.assertIn("present but not read in full", block, code)
            self.assertIn("unreadable-piece", block, code)
            self.assertNotIn("no-feeder-record", block, code)
            self.assertNotIn("no path ledger piece stands", block,
                             code)

    def test_f15_15_absent_path_ledger_wording_unchanged(self):
        table = base_case()
        del table["PATH-LEDGER.md"]
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-1")
        assert_verdict(self, block, "missing", "T-1")
        self.assertIn("no path ledger piece stands in the capture, "
                      "so no transition log holds any timestamp field",
                      block)
        self.assertIn("no-feeder-record", block)
        self.assertIn("no feeder record for the metric exists in "
                      "the tree", block)

    # ------------------------------------------------------------ F15-16

    def test_f15_16_date_only_banked_duration_t2_statement_true(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
            "Step 1 BANKED interval duration 5 hours.",
            steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t1 = row_block(result.stdout, "T-1")
        assert_verdict(self, t1, "missing", "T-1")
        self.assertIn("date-only-form", t1)
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("no-feeder-record", block)
        self.assertIn("no interval figure", block)
        self.assertNotIn("no interval duration stands in the "
                         "transition log to carry an active figure",
                         block)
        self.assertIn("an interval duration stands in the "
                      "transition log", block)

    def test_f15_16_control_no_duration_fallthrough_statement_stands(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            "Step 1 stands with no transitions recorded.",
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


if __name__ == "__main__":
    unittest.main()
