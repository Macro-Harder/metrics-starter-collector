"""Step 15 fix round 10 tests: denial runs, parentheticals, subjects, frames.

Each charged case pins one fix register item in the duration
denial machinery of derivation_core.py. F15-74 (CB9-5): the
predicative intervening run stopped at ly adverbs, five named
adverbs and five degree words, so plain adverbs (was soon
withdrawn), comma stacked adverbs (was flatly, completely
withdrawn), further degree adverbs (was pretty flatly
withdrawn) and the getting progressive (is getting withdrawn)
each left a denied figure standing. F15-75 (CB9-6): the
parenthetical rejoin stopped at three phrases and a short
reporting clause with ten verbs, so further phrases (was, in
short, withdrawn), a longer reporting clause (was, as the
reviewer Lane quite rightly noted, withdrawn), further
reporting verbs (Lane explained, Lane stated, Lane confirmed)
and a parenthetical set off by parentheses (was (Lane noted)
withdrawn) each left the figure standing. F15-76 (CB9-7): the
joined subject test stopped at five pronouns, one word bare
names and five conjunctions, so a you subject, an initialled
name and the conjunctions or and and yet each took the figure
out although the withdrawn subject was not the duration.
F15-77 (CB9-8): the doubled affirming frame complement rule
took a narrower run than the predicative run, so a negated
complement carrying a widened form (not only was it not in
fact withdrawn, not only was it not recorded as withdrawn)
was read as a plain denial. Assertions pin the parser result
as a whole, the Step 1 banked wait figure, and the T-2 and
T-4 grounds, in the form of the round 9 denial module.
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


class TestStep15Round10Denial(FixtureTestCase):

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
        return root, report

    def _assert_taken_out(self, note_text):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)), [])
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("date-only-form", t2)
        self.assertIn("no BANKED, SUSPENDED or halt interval "
                      "duration stands", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertIn(T4_MISSING_SHOWS, t4)
        self.assertNotIn("banked wait", report)
        return root, report

    # ------------------------------------------------------------ F15-74

    def test_f15_74_plain_adverbs_after_taken_out(self):
        for adverb in ("soon", "later", "already", "indeed",
                       "just", "once"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, the duration was " + adverb +
                    " withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_74_plain_adverbs_before_and_interval_taken_out(self):
        for note in (
                "The duration was soon withdrawn, Step 1 BANKED "
                "interval duration 5 hours stands.",
                "The duration was already withdrawn, Step 1 "
                "BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration was later withdrawn.",
                "The duration was once withdrawn, an interval "
                "duration stands for Step 1."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_74_comma_stacked_adverbs_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was flatly, completely withdrawn.",
                "The duration was flatly, completely withdrawn, "
                "Step 1 BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration was flatly, completely withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was flatly, completely, utterly "
                "withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_74_further_degree_adverbs_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was pretty flatly withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was somewhat flatly withdrawn.",
                "The duration was pretty flatly withdrawn, Step "
                "1 BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration was somewhat flatly withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_74_getting_progressive_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration is getting withdrawn.",
                "The duration is getting withdrawn, Step 1 BANKED "
                "interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration is getting withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_74_control_other_subject_new_forms_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was soon withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was flatly, completely withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was pretty flatly withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the appendix is getting withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    # ------------------------------------------------------------ F15-75

    def test_f15_75_further_phrases_in_run_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was for all intents and purposes "
                "withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was in practice withdrawn.",
                "The duration was in practice withdrawn, Step 1 "
                "BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration was for all intents and purposes "
                "withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_75_comma_phrase_parenthetical_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was, in short, withdrawn.",
                "The duration was, in short, withdrawn, Step 1 "
                "BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration was, in short, withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_75_longer_reporting_clause_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was, as the reviewer Lane quite "
                "rightly noted, withdrawn.",
                "The duration was, as the reviewer Lane quite "
                "rightly noted, withdrawn, Step 1 BANKED "
                "interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration was, as the reviewer Lane quite "
                "rightly noted, withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_75_further_reporting_verbs_taken_out(self):
        for verb in ("explained", "stated", "confirmed"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, the duration was, Lane " + verb +
                    ", withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)
        for note in (
                "The duration was, Lane explained, withdrawn, "
                "Step 1 BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration was, Lane confirmed, withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_75_parentheses_parenthetical_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was (Lane noted) withdrawn.",
                "The duration was (Lane noted) withdrawn, Step 1 "
                "BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration was (Lane noted) withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_75_control_other_subject_parenthetical_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was, Lane explained, withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was (Lane noted) withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was, in short, withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was, as the reviewer Lane quite "
                "rightly noted, withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    # ------------------------------------------------------------ F15-76

    def test_f15_76_pronoun_you_after_conjunction_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands and "
            "you became withdrawn.")
        self._assert_interval_stands(
            "Note: an interval duration stands for Step 1 and "
            "you became withdrawn.")

    def test_f15_76_initialled_name_after_conjunction_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands and "
            "J. Lane became withdrawn.")
        self._assert_interval_stands(
            "Note: an interval duration stands for Step 1 and "
            "J. Lane became withdrawn.")

    def test_f15_76_new_conjunctions_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "or Lane became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and yet Lane became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)
        self._assert_interval_stands(
            "Note: an interval duration stands for Step 1 or "
            "Lane became withdrawn.")

    def test_f15_76_control_figure_itself_new_conjunctions_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "or it became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and yet it became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "or the duration became withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    # ------------------------------------------------------------ F15-77

    def test_f15_77_doubled_frame_in_fact_complement_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, not "
            "only was it not in fact withdrawn, it was also "
            "logged.")

    def test_f15_77_doubled_frame_recorded_as_complement_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, not "
            "only was it not recorded as withdrawn, it was also "
            "logged.")

    def test_f15_77_doubled_frame_before_position_stands(self):
        self._assert_banked_stands(
            "Not only was the duration not in fact withdrawn, a "
            "BANKED interval duration 5 hours stands for Step 1.")
        self._assert_interval_stands(
            "Not only was the duration not recorded as "
            "withdrawn, an interval duration stands for Step 1.")

    def test_f15_77_doubled_frame_widened_neighbours_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "not only was it not soon withdrawn, it was also "
                "logged.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "not only was it not getting withdrawn, it was "
                "also logged.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "not only was it not in practice withdrawn, it "
                "was also logged."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_77_control_genuine_denial_beside_frame_taken_out(self):
        for note in (
                "Not only was no BANKED interval duration 5 hours "
                "recorded for Step 1.",
                "Not only a BANKED interval duration 5 hours "
                "stands for Step 1, the Step 1 duration was also "
                "not recorded."):
            with self.subTest(note=note):
                self._assert_taken_out(note)


if __name__ == "__main__":
    unittest.main()
