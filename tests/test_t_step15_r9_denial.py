"""Step 15 fix round 9 tests: predicative runs, subjects, frames.

Each charged case pins one fix register item in the duration
denial machinery of derivation_core.py. F15-65 (CB8-4 and
C8-4): the predicative intervening run of F15-58 stopped at
single adverbs and the listed as phrases, so stacked adverbs
joined by and (was flatly and completely withdrawn), degree
adverbs (was very flatly withdrawn), parenthetical phrases
between copula and listed word (was in fact withdrawn, was
in effect withdrawn, was for all purposes withdrawn),
parenthetical clauses set off by commas (was, Lane noted,
withdrawn) and the progressive stance (is becoming
withdrawn) each left a denied figure standing; all still
deny, in both positions, on both the BANKED and interval
paths, and the F15-50 separation holds exactly, so bare
attributive uses and listed words predicative of other
subjects still spare standing figures. F15-66 (CB8-5): the
predicative subject test after a conjunction took only the
article forms as another subject, so a bare name or a pronoun
subject (stands and Lane became withdrawn, stands and she
became withdrawn, stands and May became withdrawn) took the
figure out; those spare the figure, exactly as the article
forms do, and a conjunction clause whose subject is the
figure itself still denies. F15-67 (CB8-6): the not only
guard stripped one contiguous phrase only, so the comma
split (not, only,), the not just frame, and the doubled
frame (not only was it not withdrawn) were each read as
denials; each takes the verdict the Breaker paper records
for it, and a genuine denial standing beside the frame,
outside its scope, still denies. Assertions pin the full
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


class TestStep15Round9Denial(FixtureTestCase):

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

    # ------------------------------------------------------------ F15-65

    def test_f15_65_stacked_adverbs_and_after_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands, the "
            "duration was flatly and completely withdrawn.")

    def test_f15_65_stacked_adverbs_and_before_and_interval_taken_out(self):
        for note in (
                "The duration was flatly and completely withdrawn, "
                "Step 1 BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, the "
                "duration was flatly and completely withdrawn.",
                "The duration was flatly and completely withdrawn, "
                "an interval duration stands for Step 1."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_65_degree_adverb_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration was very flatly withdrawn.",
                "The duration was very flatly withdrawn, Step 1 "
                "BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, the "
                "duration was very flatly withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_65_parenthetical_phrases_after_taken_out(self):
        for phrase in ("in fact", "in effect", "for all purposes"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, the duration was " + phrase +
                    " withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_65_parenthetical_phrases_before_and_interval_taken_out(self):
        for note in (
                "The duration was in fact withdrawn, Step 1 BANKED "
                "interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, the "
                "duration was in effect withdrawn.",
                "The duration was for all purposes withdrawn, an "
                "interval duration stands for Step 1."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_65_parenthetical_clause_after_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration was, Lane noted, withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration was, as Lane noted, withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_65_parenthetical_clause_before_and_interval_taken_out(self):
        for note in (
                "The duration was, Lane noted, withdrawn, Step 1 "
                "BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, the "
                "duration was, Lane noted, withdrawn.",
                "The duration was, as Lane noted, withdrawn, an "
                "interval duration stands for Step 1."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_65_progressive_stance_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, the "
                "duration is becoming withdrawn.",
                "The duration is becoming withdrawn, Step 1 BANKED "
                "interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, the "
                "duration is becoming withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_65_control_other_subject_and_attributive_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, the "
                "draft was flatly and completely withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "draft was very flatly withdrawn.",
                "The draft was in fact withdrawn, Step 1 BANKED "
                "interval duration 5 hours stands.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "draft was, Lane noted, withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, the "
                "appendix is becoming withdrawn.",
                "Note: the flatly withdrawn figure is replaced by a "
                "BANKED interval duration 5 hours for Step 1."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    # ------------------------------------------------------------ F15-66

    def test_f15_66_bare_name_subject_after_conjunction_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands and "
                "Lane became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands and "
                "May became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_66_pronoun_subject_after_conjunction_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands and "
            "she became withdrawn.")

    def test_f15_66_name_and_pronoun_interval_path_stand(self):
        for note in (
                "Note: an interval duration stands for Step 1 and "
                "Lane became withdrawn.",
                "Note: an interval duration stands for Step 1 and "
                "she became withdrawn."):
            with self.subTest(note=note):
                self._assert_interval_stands(note)

    def test_f15_66_control_figure_itself_after_conjunction_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands and "
                "the duration became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands and "
                "it became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands and "
                "the record became withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_66_control_comma_part_name_subject_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, and "
            "Lane became withdrawn.")

    # ------------------------------------------------------------ F15-67

    def test_f15_67_doubled_frame_after_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, not "
            "only was it not withdrawn, it was also logged.")

    def test_f15_67_doubled_frame_before_stands(self):
        self._assert_banked_stands(
            "Not only was the duration not withdrawn, a BANKED "
            "interval duration 5 hours stands for Step 1.")

    def test_f15_67_doubled_frame_interval_path_stands(self):
        self._assert_interval_stands(
            "Not only was the duration not withdrawn, an interval "
            "duration stands for Step 1.")

    def test_f15_67_comma_split_frame_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "not, only, it is also logged.",
                "It was not, only, a BANKED interval duration 5 "
                "hours stands for Step 1."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)
        self._assert_interval_stands(
            "It was not, only, an interval duration stands for "
            "Step 1.")

    def test_f15_67_not_just_frame_stands(self):
        for note in (
                "Not just a BANKED interval duration 5 hours stands "
                "for Step 1, it is also logged.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "not just that, it is also logged."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)
        self._assert_interval_stands(
            "Not just an interval duration stands for Step 1, it "
            "is also logged.")

    def test_f15_67_control_genuine_denial_beside_frame_taken_out(self):
        for note in (
                "Not only a BANKED interval duration 5 hours stands "
                "for Step 1, the Step 1 duration was also not "
                "recorded.",
                "Not only was no BANKED interval duration 5 hours "
                "recorded for Step 1."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_67_control_plain_not_only_frames_still_stand(self):
        for note in (
                "Not only a BANKED interval duration 5 hours stands "
                "for Step 1, it is also logged.",
                "Step 1 BANKED interval duration 5 hours stands, not "
                "only that, it is also logged."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)


if __name__ == "__main__":
    unittest.main()
