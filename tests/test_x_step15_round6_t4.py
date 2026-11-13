"""Step 15 fix round 6 tests: T-4 banked attribution and queue counts.

Each charged case pins one fix register item in the T-4 machinery
of derivation_core.py. F15-40: _t4_banked_durations took the first
Step token in a ledger line as the step of every BANKED figure in
that line, so a figure standing second in its line, in a clause
naming its own step, was attributed to the step the line named
first. Each BANKED figure is attributed to the step its own clause
names, and the tests assert the full printed step, never the bare
substring the round 5 module asserted. F15-45: _derive_t4 set its
banked flag from the presence of any decision queue piece, so T-4
stated that banked item counts stand for directory, malformed,
dangling, empty and disagreement queues, while D-1 on the same
report stated no complete decision table stands. The counts stand
only where a queue piece carries readable decision items, on the
same completeness ground the D-1 queue selection applies.
Control cases pin the behaviour that must not move: the reversed
word order, a single mention line, a sound queue, and a queue fed
from a readable duplicate.
"""
import os
import unittest

from metrics_starter_collector.derivation_core import _t4_banked_durations
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, path_ledger,
                                     queue_file, row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
QUEUE_ROW_8 = ("| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
               "2026-11-01 17:00 |")
QUEUE_ROW_4 = ("| Q-2 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
               "2026-11-01 13:00 |")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round6T4(FixtureTestCase):

    # ------------------------------------------------------------ F15-40

    def _date_only_report(self, note):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, result.stdout

    def _assert_step1_banked_wait(self, note):
        root, report = self._date_only_report(note)
        self.assertEqual(_t4_banked_durations(capture(root)),
                         [(1, 5.0, True)])
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 banked wait 5 hours", t4)
        self.assertNotIn("Step 2 banked wait", t4)
        return root, report

    def test_f15_40_denial_step2_first_banked_step1_second(self):
        self._assert_step1_banked_wait(
            "Note: No interval duration was recorded for Step 2, "
            "but Step 1 BANKED interval duration 5 hours stands.")

    def test_f15_40_denial_step2_colon_banked_step1_second(self):
        self._assert_step1_banked_wait(
            "Note: No interval duration for Step 2: Step 1 BANKED "
            "interval duration 5 hours stands.")

    def test_f15_40_control_reversed_word_order_step1(self):
        self._assert_step1_banked_wait(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "no interval duration was recorded for Step 2.")

    def test_f15_40_control_single_mention_line_step1(self):
        self._assert_step1_banked_wait(
            "Step 1 BANKED interval duration 5 hours stands.")

    def test_f15_40_two_mentions_each_attributed_to_own_clause(self):
        root, report = self._date_only_report(
            "Step 2 BANKED interval duration 3 hours stands, and "
            "Step 1 BANKED interval duration 5 hours stands.")
        self.assertEqual(_t4_banked_durations(capture(root)),
                         [(2, 3.0, True), (1, 5.0, True)])
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 2 banked wait 3 hours; "
                      "Step 1 banked wait 5 hours", t4)

    def test_f15_40_control_clause_naming_no_step_keeps_line_step(self):
        root, report = self._date_only_report(
            "For Step 2, BANKED interval duration 5 hours stands.")
        self.assertEqual(_t4_banked_durations(capture(root)),
                         [(2, 5.0, True)])
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 2 banked wait 5 hours", t4)

    # ------------------------------------------------------------ F15-45

    def _assert_damaged_queue_weaker_form(self, root):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t4 = row_block(result.stdout, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn("no figure stands", t4)
        self.assertIn("no queue piece carries readable decision "
                      "items", t4)
        self.assertNotIn("banked item counts stand", t4)
        self.assertNotIn("banked states and item counts stand", t4)
        d1 = row_block(result.stdout, "D-1")
        assert_verdict(self, d1, "present but not derivable", "D-1")
        self.assertIn("no complete decision table stands", d1)
        return result.stdout

    def test_f15_45_directory_queue_weaker_form(self):
        root = build_tree(base_case())
        (root / "DECISION-QUEUE.md").mkdir()
        self._assert_damaged_queue_weaker_form(root)

    def test_f15_45_malformed_queue_weaker_form(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = b"\xff\xfe\x00 not a queue"
        self._assert_damaged_queue_weaker_form(build_tree(table))

    def test_f15_45_dangling_queue_weaker_form(self):
        root = build_tree(base_case())
        os.symlink(str(root / "missing-target.md"),
                   str(root / "DECISION-QUEUE.md"))
        self._assert_damaged_queue_weaker_form(root)

    def test_f15_45_empty_queue_weaker_form(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = b""
        self._assert_damaged_queue_weaker_form(build_tree(table))

    def test_f15_45_disagreement_queue_weaker_form(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = b""
        table["sub/DECISION-QUEUE.md"] = queue_file([QUEUE_ROW_8])
        table["zzz/DECISION-QUEUE.md"] = queue_file([QUEUE_ROW_4])
        self._assert_damaged_queue_weaker_form(build_tree(table))

    def test_f15_45_control_sound_queue_counts_stand(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = queue_file([QUEUE_ROW_8])
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t4 = row_block(result.stdout, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn("banked item counts stand and no duration "
                      "figure stands", t4)
        self.assertIn("banked states and item counts stand in the "
                      "feeder records", t4)

    def test_f15_45_control_duplicate_queue_counts_stand(self):
        table = base_case()
        table["DECISION-QUEUE.md"] = b""
        table["sub/DECISION-QUEUE.md"] = queue_file([QUEUE_ROW_8])
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t4 = row_block(result.stdout, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn("banked item counts stand and no duration "
                      "figure stands", t4)

    def test_f15_45_banked_state_without_queue_counts_do_not_stand(self):
        table = base_case()
        ledger = table["PATH-LEDGER.md"]
        table["PATH-LEDGER.md"] = ledger + \
            "\nStep 1 BANKED state is recorded.\n"
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        t4 = row_block(result.stdout, "T-4")
        assert_verdict(self, t4, "present but not derivable", "T-4")
        self.assertIn("banked states stand and no duration figure "
                      "stands", t4)
        self.assertNotIn("banked item counts stand", t4)


if __name__ == "__main__":
    unittest.main()
