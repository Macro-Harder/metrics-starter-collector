"""Step 15 fix round 5 tests: duration clause scope and denial words.

Each charged case pins one fix register item in the duration helper
machinery of derivation_core.py. F15-36: the clause fragment test
split a line only at a full stop or a semicolon and let the after
fragment run to the end of the sentence, so a denial scoped to
another step or another figure took out a genuinely standing BANKED
duration in the same sentence; a denial must take out only mentions
inside its own clause scope, with a comma or a colon acting as a
clause break where the denial is scoped to another subject. F15-37:
plain denial words and shapes outside the standing marker sets still
left a negated duration standing, on the interval duration path and
through the BANKED alternative; the marker handling takes up the
proven words and shapes. Control cases pin the behaviour that must
not move: the F15-29 registered shapes that share a comma or a colon
with the mention, the semicolon control, the two line standing plus
negated control, the not only guard, and the genuine standing forms.
"""
import unittest

from metrics_starter_collector.derivation_core import _t4_banked_durations
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, metrics_record,
                                     path_ledger, row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
FULL_INTERVALS = (
    "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 2 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
    "Step 3 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round5Duration(FixtureTestCase):

    # ------------------------------------------------------------ shared

    def _report(self, note_text, prefix=DATE_ONLY_LINE):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            prefix + note_text, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, result.stdout

    def _assert_duration_stands(self, note_text):
        root, report = self._report(note_text)
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("no-feeder-record", t2)
        self.assertIn("an interval duration stands in the "
                      "transition log", t2)
        self.assertNotIn("no BANKED, SUSPENDED or halt interval "
                         "duration stands", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("banked wait 5 hours", t4)
        return root, report

    def _assert_date_only_true_ground(self, note_text):
        root, report = self._report(note_text)
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("date-only-form", t2)
        self.assertIn("no BANKED, SUSPENDED or halt interval "
                      "duration stands", t2)
        self.assertNotIn("an interval duration stands in the "
                         "transition log, but no active figure", t2)
        return root, report

    # ------------------------------------------------------------ F15-36

    def test_f15_36_form_a_standing_then_denial_other_step_stands(self):
        self._assert_duration_stands(
            "Step 1 BANKED interval duration 5 hours stands, and no "
            "interval duration was recorded for Step 2.")

    def test_f15_36_form_b_denial_then_standing_comma_but_stands(self):
        self._assert_duration_stands(
            "No interval duration was recorded for Step 2, but "
            "Step 1 BANKED interval duration 5 hours stands.")

    def test_f15_36_form_c_denial_colon_standing_stands(self):
        self._assert_duration_stands(
            "No interval duration for Step 2: Step 1 BANKED "
            "interval duration 5 hours stands.")

    def test_f15_36_form_d_standing_colon_denial_stands(self):
        self._assert_duration_stands(
            "Step 1 BANKED interval duration 5 hours stands: no "
            "duration was recorded for Step 2.")

    def test_f15_36_form_e_denial_of_other_figure_stands(self):
        self._assert_duration_stands(
            "Step 1 BANKED interval duration 5 hours, not 10 "
            "hours, was recorded.")

    def test_f15_36_control_semicolon_form_still_stands(self):
        self._assert_duration_stands(
            "No interval duration was recorded for Step 2; Step 1 "
            "BANKED interval duration 5 hours stands.")

    def test_f15_36_control_two_line_standing_beside_negated_stands(self):
        self._assert_duration_stands(
            "Step 1 BANKED interval duration 5 hours.\n"
            "Note: no interval duration is recorded for Step 2.")

    def test_f15_36_control_comma_denial_same_clause_still_taken_out(self):
        self._assert_date_only_true_ground(
            "Note: interval duration, not recorded for this step.")

    def test_f15_36_control_quoted_retracted_same_sentence_taken_out(self):
        self._assert_date_only_true_ground(
            'The draft states "an interval duration stands", but '
            "that claim was withdrawn and no duration was "
            "recorded.")

    def test_f15_36_control_not_only_guard_still_stands(self):
        root, report = self._report(
            "Note: the interval duration was not only recorded "
            "for this step.")
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("no-feeder-record", t2)
        self.assertIn("an interval duration stands in the "
                      "transition log", t2)

    # ------------------------------------------------------------ F15-37

    def test_f15_37_new_denial_words_date_only_true_ground(self):
        for note in (
                "Note: the interval duration is unrecorded for "
                "this step.",
                "Note: the interval duration is missing from "
                "this log.",
                "Note: an interval duration is missing from "
                "this log.",
                "Note: the interval duration was omitted for "
                "this step.",
                "Note: the claim of an interval duration is "
                "denied.",
                "Note: the interval duration is denied in this "
                "log.",
                "Note: the interval duration was removed from "
                "this log.",
                "Note: an interval duration is nowhere recorded "
                "in this log.",
                "Note: interval duration: none recorded for "
                "this step."):
            with self.subTest(note=note):
                self._assert_date_only_true_ground(note)

    def test_f15_37_missing_before_mention_date_only_true_ground(self):
        self._assert_date_only_true_ground(
            "Note: a missing interval duration is noted for this "
            "step.")

    def test_f15_37_refuses_to_record_date_only_true_ground(self):
        self._assert_date_only_true_ground(
            "Note: the log refuses to record an interval "
            "duration.")

    def test_f15_37_banked_alternative_missing_t2_and_t4(self):
        root, report = self._report(
            "Step 1 BANKED interval duration 5 hours is missing "
            "from this log.")
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("date-only-form", t2)
        self.assertIn("no BANKED, SUSPENDED or halt interval "
                      "duration stands", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertIn("no banked state and no decision item count "
                      "stands", t4)
        self.assertNotIn("banked wait 5 hours", report)
        self.assertEqual(_t4_banked_durations(capture(root)), [])

    def test_f15_37_retracted_in_following_sentence_taken_out(self):
        self._assert_date_only_true_ground(
            'The draft states "an interval duration stands". '
            "That claim was withdrawn.")

    def test_f15_37_refusal_missing_word_t2_missing_no_feeder(self):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            FULL_INTERVALS + "\nNote: the interval duration is "
            "missing from this log.", steps="1, 2, 3")
        table["wiki/wiki/synthesis/build-metrics-record.md"] = \
            metrics_record(body="Step table stands.",
                           header_version="unknown-version-999")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "missing", "T-2")
        self.assertIn("no-feeder-record", block)
        self.assertIn("no interval duration stands in the "
                      "transition log from which an active figure "
                      "for this row could form", block)
        self.assertNotIn("unknown-definitions-version", block)

    def test_f15_37_control_following_sentence_affirmation_stands(self):
        root, report = self._report(
            "Step 1 BANKED interval duration 5 hours stands. "
            "That claim stands in the log.")
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("no-feeder-record", t2)
        self.assertIn("an interval duration stands in the "
                      "transition log", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("banked wait 5 hours", t4)

    def test_f15_37_control_two_sentence_other_step_denial_stands(self):
        root, report = self._report(
            "Step 1 BANKED interval duration 5 hours stands. "
            "No interval duration was recorded for Step 2.")
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("no-feeder-record", t2)
        self.assertIn("an interval duration stands in the "
                      "transition log", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn("banked wait 5 hours", t4)


if __name__ == "__main__":
    unittest.main()
