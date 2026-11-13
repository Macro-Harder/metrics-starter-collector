"""Step 15 fix round 8 tests: denial constructions and figure words.

Each charged case pins one fix register item in the duration
denial and figure machinery of derivation_core.py. F15-58
(CB7-5 and CB7-6): the predicative construction test of F15-50
required the copula to stand immediately before the listed
word, so a listed word predicative of the duration with an
adverb or a short phrase between the copula and the word
(was flatly withdrawn, was completely retracted, is hereby
withdrawn, was noted as withdrawn) printed the figure, and
stance verbs beyond the pinned set (became, appears, looks)
left a listed word predicative of the duration standing; both
widenings keep the F15-50 separation exactly, so bare
attributive uses and listed words predicative of other
subjects still leave standing figures standing. F15-59
(CB7-7): the not only guard stood on the after side only, so
a not only construction in the mention's before fragment
erased an affirmed figure on every consumer; the guard
applies on the before side as on the after side. F15-60
(CB7-8): the hyphenated attributive wrong-one form printed
its figure while its spaced and predicative twins were taken
out; the hyphenated form counts as the anaphoric denial,
while a wrong-one compound modifying another noun does not.
F15-61 (CB7-12): figure words stopped at the tens table, so
hundred forms read as no figure and point forms read as
their integer word; one hundred and two hundred read as
their figures and five point five reads as 5.5, so a denial
of a different figure scopes elsewhere and a standing figure
of another value survives it. Assertions pin the full
printed figures and grounds: the parser result as a whole,
the Step 1 banked wait figure as a whole, and the full T-2
and T-4 ground statements.
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


class TestStep15Round8DenialFigures(FixtureTestCase):

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

    # ------------------------------------------------------------ F15-58

    def test_f15_58_adverb_between_copula_and_word_after_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration was flatly withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration was completely retracted.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration is hereby withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_58_noted_as_phrase_after_taken_out(self):
        self._assert_taken_out(
            "The BANKED interval duration 5 hours for Step 1 was "
            "noted as withdrawn.")

    def test_f15_58_adverb_and_phrase_before_position_taken_out(self):
        for note in (
                "The duration was flatly withdrawn, Step 1 BANKED "
                "interval duration 5 hours stands.",
                "The duration was noted as withdrawn, Step 1 BANKED "
                "interval duration 5 hours stands."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_58_adverb_interval_path_taken_out(self):
        for note in (
                "Note: an interval duration stands for Step 1, the "
                "duration was flatly withdrawn.",
                "The duration was flatly withdrawn, an interval "
                "duration stands for Step 1."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_58_stance_verbs_after_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration appears retracted.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration looks absent.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration becomes retracted.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration appeared withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration looked absent.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration stays withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_58_stance_verbs_before_and_interval_taken_out(self):
        for note in (
                "The duration became withdrawn, Step 1 BANKED "
                "interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, the "
                "duration looks absent."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_58_control_plain_and_pinned_copulas_still_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration was withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration remains withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration seems withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration is said to be withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_58_control_other_subject_predicative_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, the "
                "draft was flatly withdrawn.",
                "The draft was completely retracted, Step 1 BANKED "
                "interval duration 5 hours stands.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "draft became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_58_control_bare_attributive_uses_stand(self):
        for note in (
                "Note: the withdrawn figure is replaced by a BANKED "
                "interval duration 5 hours for Step 1.",
                "Note: a retracted reading is replaced by a BANKED "
                "interval duration 5 hours for Step 1.",
                "Note: an absent minded note records a BANKED "
                "interval duration 5 hours for Step 1."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    # ------------------------------------------------------------ F15-59

    def test_f15_59_not_only_before_banked_stands(self):
        self._assert_banked_stands(
            "Not only a BANKED interval duration 5 hours stands for "
            "Step 1, it is also logged.")

    def test_f15_59_not_only_before_interval_stands(self):
        self._assert_interval_stands(
            "Note: not only an interval duration stands for Step 1, "
            "it is also logged.")

    def test_f15_59_control_after_side_not_only_still_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, not "
            "only that, it is also logged.")

    def test_f15_59_control_genuine_before_negation_still_taken_out(self):
        for note in (
                "The duration was withdrawn, Step 1 BANKED interval "
                "duration 5 hours stands.",
                "No BANKED interval duration 5 hours stands for "
                "Step 1."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    # ------------------------------------------------------------ F15-60

    def test_f15_60_hyphenated_attributive_wrong_one_taken_out(self):
        self._assert_taken_out(
            "Note: the wrong-one BANKED interval duration 5 hours "
            "is noted for this step.")

    def test_f15_60_control_spaced_and_predicative_twins_taken_out(self):
        for note in (
                "Note: the wrong BANKED interval duration 5 hours "
                "is noted for this step.",
                "Note: a BANKED interval duration 5 hours is the "
                "wrong-one for this step."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_60_control_wrong_one_other_subject_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "and the date is the wrong-one.",
                "Note: the wrong-one date stands beside a BANKED "
                "interval duration 5 hours for Step 1."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    # ------------------------------------------------------------ F15-61

    def test_f15_61_hundred_different_figure_scopes_elsewhere(self):
        for words in ("one hundred hours", "two hundred hours"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, and no interval duration " + words +
                    " was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_61_hundred_same_figure_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 100 hours stands, and "
            "no interval duration one hundred hours was recorded "
            "for Step 1.")

    def test_f15_61_point_different_figure_scopes_elsewhere(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "no interval duration five point five hours was "
            "recorded for Step 1.")

    def test_f15_61_point_same_figure_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5.5 hours stands, and "
            "no interval duration five point five hours was "
            "recorded for Step 1.")

    def test_f15_61_control_digit_and_tens_forms_hold(self):
        for words in ("100 hours", "forty two hours",
                      "twenty five hours", "ninety nine hours"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, and no interval duration " + words +
                    " was recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_banked_stands(note)


if __name__ == "__main__":
    unittest.main()
