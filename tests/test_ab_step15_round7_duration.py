"""Step 15 fix round 7 tests: duration record, denial use, titles.

Each charged case pins one fix register item in the duration helper
machinery of derivation_core.py. F15-49: the spared anaphoric subject
set in the scope test omitted record, so a clause withdrawing the
record was scoped elsewhere and a figure printed from a withdrawn
record, in both positions, where the log and statement twins were
taken out. F15-50: the listed denial words absent, withdrawn,
retracted and wrong matched in non denial uses inside the scope,
as bare attributive modifiers of another noun, erasing genuinely
standing figures on every consumer. F15-51: the abbreviation set in
the sentence end machinery omitted common title forms, so a stop
after Prof. or Capt. hid a following retraction exactly as a stop
after e.g. did before its cure. F15-53: the scope figure comparison
read digits only, so a different figure stated in words was not
recognised as a different figure. F15-54: wrong stood only in the
was wrong and is wrong phrases, so the anaphoric form is the wrong
one and wrong referring to the duration itself printed a figure
against its own note, while wrong modifying another noun must not
take a mention out. Assertions pin the full printed figures and
grounds: the parser result as a whole, the Step 1 banked wait
figure as a whole, and the full T-2 and T-4 ground statements.
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


class TestStep15Round7Duration(FixtureTestCase):

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

    def _assert_interval_stands(self, note_text):
        root, report = self._report(note_text)
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("no-feeder-record", t2)
        self.assertIn("an interval duration stands in the "
                      "transition log", t2)
        self.assertNotIn("no BANKED, SUSPENDED or halt interval "
                         "duration stands", t2)
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

    # ------------------------------------------------------------ F15-49

    def test_f15_49_record_withdrawn_after_clause_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands, the "
            "record was withdrawn.")

    def test_f15_49_record_withdrawn_before_clause_taken_out(self):
        self._assert_taken_out(
            "The record was withdrawn, Step 1 BANKED interval "
            "duration 5 hours stands.")

    def test_f15_49_record_withdrawn_unvalued_interval_taken_out(self):
        for note in (
                "Note: an interval duration stands for Step 1, the "
                "record was withdrawn.",
                "The record was withdrawn, an interval duration "
                "stands for Step 1."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_49_control_log_and_statement_forms_still_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, the "
                "log was withdrawn.",
                "The log was withdrawn, Step 1 BANKED interval "
                "duration 5 hours stands.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "statement was withdrawn.",
                "The statement was withdrawn, Step 1 BANKED interval "
                "duration 5 hours stands."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_49_control_plain_other_subjects_still_scope_elsewhere(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, the "
                "appendix is missing.",
                "Step 1 BANKED interval duration 5 hours stands, none "
                "of it was charged to the budget.",
                "None of the reviewers objected, Step 1 BANKED "
                "interval duration 5 hours stands.",
                "No record stands for the earlier work, Step 1 BANKED "
                "interval duration 5 hours stands."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    # ------------------------------------------------------------ F15-50

    def test_f15_50_absent_minded_note_banked_stands(self):
        self._assert_banked_stands(
            "Note: an absent minded note records a BANKED interval "
            "duration 5 hours for Step 1.")

    def test_f15_50_absent_minded_note_interval_path_stands(self):
        self._assert_interval_stands(
            "Note: an absent minded note records an interval "
            "duration for Step 1.")

    def test_f15_50_retracted_note_still_records_stands(self):
        self._assert_banked_stands(
            "Note: the retracted note still records a BANKED "
            "interval duration 5 hours for Step 1.")

    def test_f15_50_withdrawn_draft_replaced_by_duration_stands(self):
        self._assert_banked_stands(
            "Note: a withdrawn draft is replaced by a BANKED "
            "interval duration 5 hours for Step 1.")

    def test_f15_50_wrong_date_beside_standing_duration_stands(self):
        self._assert_banked_stands(
            "Note: the date was wrong and a BANKED interval "
            "duration 5 hours stands for Step 1.")

    def test_f15_50_absent_minded_clerk_after_position_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, noted "
            "by an absent minded clerk.")

    def test_f15_50_control_denial_positions_still_taken_out(self):
        for note in (
                "Note: the interval duration is absent for this "
                "step.",
                "Note: the interval duration was withdrawn from "
                "this log.",
                "Note: the interval duration stands retracted in "
                "this log.",
                "Note: an absent BANKED interval duration 5 hours "
                "is noted for this step.",
                "Note: a withdrawn interval duration is noted for "
                "this step.",
                "Note: a retracted BANKED interval duration 5 hours "
                "is noted for this step.",
                "Note: the claim was wrong, an interval duration "
                "is noted for this step."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    # ------------------------------------------------------------ F15-51

    def test_f15_51_prof_and_capt_unvalued_retraction_taken_out(self):
        for title in ("Prof.", "Capt."):
            note = ('The draft states "an interval duration '
                    'stands". That claim, ' + title + " Lane noted, "
                    "was withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_51_prof_and_capt_banked_retraction_taken_out(self):
        for title in ("Prof.", "Capt."):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands. That claim, " + title + " Lane noted, "
                    "was withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_51_completed_title_set_retraction_taken_out(self):
        for title in ("Mrs.", "Ms.", "Lt.", "Col.", "Gen.", "Sen.",
                      "Rep.", "Gov.", "St."):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands. That claim, " + title + " Lane noted, "
                    "was withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)
        for suffix in ("Jr.", "Sr."):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands. That claim, Lane " + suffix + " noted, "
                    "was withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_51_control_dr_mr_and_true_end_after_abbreviation(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim, Dr. Lane noted, was withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim, Mr. Lane noted, was withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim was withdrawn by Dr."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_51_control_title_before_mention_stands(self):
        self._assert_banked_stands(
            "Prof. Lane noted, Step 1 BANKED interval duration "
            "5 hours stands.")

    # ------------------------------------------------------------ F15-53

    def test_f15_53_different_figure_in_words_scopes_elsewhere(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "no interval duration ten hours was recorded for "
            "Step 1.")

    def test_f15_53_same_figure_in_words_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "no interval duration five hours was recorded for "
            "Step 1.")

    def test_f15_53_tens_word_different_figures_scope_elsewhere(self):
        for words in ("twenty hours", "thirty hours",
                      "twenty five hours"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, and no interval duration " + words +
                    " was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_53_control_digit_different_figure_still_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "no interval duration 10 hours was recorded for Step 1.")

    # ------------------------------------------------------------ F15-54

    def test_f15_54_wrong_banked_attributive_taken_out(self):
        self._assert_taken_out(
            "Note: the wrong BANKED interval duration 5 hours is "
            "noted for this step.")

    def test_f15_54_is_the_wrong_one_taken_out(self):
        self._assert_taken_out(
            "Note: a BANKED interval duration 5 hours is the wrong "
            "one for this step.")

    def test_f15_54_wrong_interval_duration_taken_out(self):
        self._assert_taken_out(
            "Note: the wrong interval duration was recorded for "
            "this step.")

    def test_f15_54_control_wrong_other_noun_stands(self):
        for note in (
                "Note: the wrong date stands beside a BANKED "
                "interval duration 5 hours for Step 1.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "and the date is the wrong one."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)


if __name__ == "__main__":
    unittest.main()
