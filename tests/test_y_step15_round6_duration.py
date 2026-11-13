"""Step 15 fix round 6 tests: duration scope, positions, retraction.

Each charged case pins one fix register item in the duration helper
machinery of derivation_core.py. F15-41: the clause scope test in
_subclause_scoped_elsewhere recognised only a duration mention of
its own, a step name or an hours figure as a subject, so a clause
part denying something else in plain words (the appendix, the
budget, the reviewers, the earlier work, none the worse) and a part
carrying a bare duration mention with a different figure were
treated as unscoped and their markers took out a standing Step 1
BANKED interval duration of 5 hours. F15-42: the after marker set
carried absent, withdrawn, retracted and was wrong or is wrong
with no before set counterparts, so those words before a mention
never took it out. F15-43: _retracted_in_following_sentence cut the
following sentence at the first sentence end match, and the full
stop inside an abbreviation followed by a space matches, so a
retraction marker after an abbreviation was never seen. F15-44:
_subclause_scoped_elsewhere returned scoped elsewhere for any part
carrying its own duration mention, before the step and figure
comparison its docstring states, so a denial naming the same step
and the same figure in a second clause never reached the first
mention. Assertions pin the full printed figures and grounds: the
parser result as a whole, the Step 1 banked wait figure as a whole,
and the full T-2 and T-4 ground statements, never the bare banked
wait substring alone.
"""
import unittest

from metrics_starter_collector.derivation_core import _t4_banked_durations
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, path_ledger,
                                     row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
T4_MISSING_SHOWS = ("no banked state and no decision item count "
                    "stands in the feeder records for this metric")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round6Duration(FixtureTestCase):

    # ------------------------------------------------------------ shared

    def _report(self, note_text):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note_text, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, result.stdout

    def _assert_banked_stands(self, note_text):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)),
                         [(1, 5.0, True)])
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("no-feeder-record", t2)
        self.assertIn("an interval duration stands in the "
                      "transition log", t2)
        self.assertNotIn("no BANKED, SUSPENDED or halt interval "
                         "duration stands", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("Step 1 banked wait 5 hours", t4)
        self.assertNotIn("Step 2 banked wait", t4)
        return root, report

    def _assert_taken_out(self, note_text):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)), [])
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("date-only-form", t2)
        self.assertIn("no BANKED, SUSPENDED or halt interval "
                      "duration stands", t2)
        self.assertNotIn("an interval duration stands in the "
                         "transition log, but no active figure", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertIn(T4_MISSING_SHOWS, t4)
        self.assertNotIn("banked wait", report)
        return root, report

    # ------------------------------------------------------------ F15-41

    def test_f15_41_appendix_missing_other_clause_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, the "
            "appendix is missing.")

    def test_f15_41_none_charged_to_budget_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, none "
            "of it was charged to the budget.")

    def test_f15_41_none_of_reviewers_before_clause_stands(self):
        self._assert_banked_stands(
            "None of the reviewers objected, Step 1 BANKED interval "
            "duration 5 hours stands.")

    def test_f15_41_none_the_worse_interval_path_stands(self):
        root, report = self._report(
            "Note: an interval duration stands for Step 1, none "
            "the worse for the wait.")
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("no-feeder-record", t2)
        self.assertIn("an interval duration stands in the "
                      "transition log", t2)
        self.assertNotIn("no BANKED, SUSPENDED or halt interval "
                         "duration stands", t2)

    def test_f15_41_no_record_earlier_work_before_clause_stands(self):
        self._assert_banked_stands(
            "No record stands for the earlier work, Step 1 BANKED "
            "interval duration 5 hours stands.")

    def test_f15_41_bare_duration_other_figure_scoped_elsewhere(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "the 10 hour duration was not recorded.")

    def test_f15_41_control_other_step_record_missing_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, the "
            "Step 2 record is missing.")

    def test_f15_41_cured_denials_about_duration_still_taken_out(self):
        for note in (
                "Note: no interval duration is recorded for this "
                "step.",
                "Note: the interval duration was not recorded for "
                "this step.",
                "Note: interval duration, not recorded for this "
                "step.",
                "Note: the interval duration is missing from this "
                "log.",
                "Note: an interval duration is nowhere recorded in "
                "this log."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_41_cured_banked_denials_still_taken_out(self):
        for note in (
                "Note: no BANKED interval duration 5 hours was "
                "recorded.",
                "Note: a BANKED interval duration 5 hours was not "
                "recorded for this step.",
                "Step 1 BANKED interval duration 5 hours is missing "
                "from this log."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    # ------------------------------------------------------------ F15-42

    def test_f15_42_before_words_unvalued_taken_out(self):
        for note in (
                "Note: an absent interval duration is noted for "
                "this step.",
                "Note: a withdrawn interval duration is noted for "
                "this step.",
                "Note: a retracted interval duration is noted for "
                "this step.",
                "Note: the claim was wrong, an interval duration "
                "is noted for this step.",
                "Note: the claim is wrong, an interval duration "
                "is noted for this step."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_42_before_words_banked_valued_taken_out(self):
        for note in (
                "Note: an absent BANKED interval duration 5 hours "
                "is noted for this step.",
                "Note: a withdrawn BANKED interval duration 5 "
                "hours is noted for this step.",
                "Note: a retracted BANKED interval duration 5 "
                "hours is noted for this step."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_42_control_after_words_still_taken_out(self):
        for note in (
                "Note: the interval duration is absent for this "
                "step.",
                "Note: the interval duration was withdrawn from "
                "this log.",
                "Note: the interval duration was wrong for this "
                "step."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    # ------------------------------------------------------------ F15-43

    def test_f15_43_abbreviation_unvalued_retraction_taken_out(self):
        for note in (
                'The draft states "an interval duration stands". '
                "That claim, e.g. the draft note, was withdrawn.",
                'The draft states "an interval duration stands". '
                "That claim, i.e. the draft note, was withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_43_abbreviation_banked_retraction_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim, e.g. the draft note, was withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim, i.e. the draft note, was withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_43_control_decimal_and_quoted_end_taken_out(self):
        for note in (
                'The draft states "an interval duration stands". '
                "That claim of 5.5 hours was withdrawn.",
                'The draft states "an interval duration stands." '
                "That claim was withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_43_control_marker_before_abbreviation_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands. That "
            "claim was withdrawn, e.g. removed from the log.")

    def test_f15_43_control_abbreviation_before_mention_stands(self):
        self._assert_banked_stands(
            "See e.g. the note, Step 1 BANKED interval duration "
            "5 hours stands.")

    # ------------------------------------------------------------ F15-44

    def test_f15_44_same_step_same_figure_denial_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "no interval duration 5 hours was recorded for Step 1.")

    def test_f15_44_same_step_no_figure_denial_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "no interval duration was recorded for Step 1.")

    def test_f15_44_nested_other_step_then_same_step_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "no interval duration was recorded for Step 2, and no "
            "interval duration was recorded for Step 1.")

    def test_f15_44_control_different_step_or_figure_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "and no interval duration was recorded for Step 2.",
                "Step 1 BANKED interval duration 5 hours, not 10 "
                "hours, was recorded."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)


if __name__ == "__main__":
    unittest.main()
