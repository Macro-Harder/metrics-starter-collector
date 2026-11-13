"""Step 15 fix round 12 tests: denial machinery, round 12.

Each charged case pins one fix register item in the duration
denial machinery of derivation_core.py. F15-101 (C11-3 with
CB11-5, Medium): the shared run's phrase token enumerated its
prepositions, a subset of its own stated shape, so article
phrases opening with across, within, between, behind, upon,
per or via left a denied figure standing, the interval path
carrying the false T-2 stands statement. F15-102 (CB11-6,
Low): a group set off by a mixed em and en dash pair was no
run token. F15-103 (C11-2 limb, Medium): the joined subject
test still enumerated, so a whenever join and the pronoun
one each read a new subject as the mention itself and erased
a standing figure. F15-104 (CB11-7 with C11-2 limb, Medium):
the joined subject adverb slot took one word only, so two
adverbs between the conjunction and the subject (and quite
rightly Lane, and very quickly Lane, and quite rightly the
draft, and very quietly Reyes) took the figure out. F15-105
(CB11-8, Medium): the joined span's anaphoric search read a
carrier word anywhere in the span, so Record-Keeper,
Log-Book, Claim-Handler, Lane Record and the log keeper each
took the figure out, although the withdrawn subject is a
person or a role. F15-106 (CB11-9, Low): surnames with two
lowercase particles (de la Cruz, van der Berg, de los Reyes)
defeated the name reading. F15-107 (CB11-15, Medium): the
doubled frame's split complement failed where its
parenthetical was set off by quotes or brackets, although
the dash pair twin inside one part was removed with the
frame. Assertions pin the parser result as a whole, the
Step 1 banked wait figure, and the T-2 and T-4 grounds, in
the form of the round 11 denial module.
"""
import unittest

from metrics_starter_collector.derivation_core import _t4_banked_durations
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, path_ledger,
                                     row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
T4_MISSING_SHOWS = ("no banked state and no decision item count "
                    "stands in the feeder records for this metric")
EM = "\u2014"
EN = "\u2013"


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round12Denial(FixtureTestCase):

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
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertIn(T4_MISSING_SHOWS, t4)
        self.assertNotIn("banked wait", report)
        return root, report

    # ------------------------------------------------------------ F15-101

    def test_f15_101_new_preposition_phrases_after_taken_out(self):
        for phrase in ("across the wide plain",
                       "within the stated limit",
                       "between the two lines",
                       "behind the closed door",
                       "upon the record",
                       "per the record",
                       "via the log"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, the duration was " + phrase +
                    " withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_101_new_preposition_phrases_before_and_interval_taken_out(self):
        for note in (
                "The duration was across the board withdrawn, "
                "Step 1 BANKED interval duration 5 hours stands.",
                "The duration was behind the scenes withdrawn, "
                "Step 1 BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration was across the board withdrawn.",
                "Note: an interval duration stands for Step 1, "
                "the duration was within the stated limit "
                "withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_101_control_draft_twins_new_prepositions_stand(self):
        for phrase in ("across the board", "within the stated limit",
                       "via the log", "behind the scenes"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, the draft was " + phrase +
                    " withdrawn.")
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_101_control_settled_phrases_still_taken_out(self):
        for phrase in ("in the end", "under the old rules",
                       "in the final analysis", "on the record"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, the duration was " + phrase +
                    " withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    # ------------------------------------------------------------ F15-102

    def test_f15_102_mixed_dash_pair_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was " + EM + " Lane noted " + EN +
                " withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was " + EN + " Lane noted " + EM +
                " withdrawn.",
                "The duration was " + EM + " Lane noted " + EN +
                " withdrawn, Step 1 BANKED interval duration 5 "
                "hours stands."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_102_control_same_dash_pairs_taken_out_and_draft_mixed_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was " + EM + " Lane noted " + EM +
                " withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was " + EN + " Lane noted " + EN +
                " withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, the "
            "draft was " + EM + " Lane noted " + EN +
            " withdrawn.")

    # ------------------------------------------------------------ F15-103

    def test_f15_103_whenever_join_new_subject_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "whenever Reyes became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "whenever Lane became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "whenever the draft became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_103_pronoun_one_new_subject_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "and one became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and someone became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_103_control_mention_itself_new_joins_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "whenever it became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "whenever the duration became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "whenever the record became withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    # ------------------------------------------------------------ F15-104

    def test_f15_104_stacked_adverbs_name_subjects_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "and quite rightly Lane became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and very quickly Lane became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and very quietly Reyes became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_104_stacked_adverbs_article_subject_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "and quite rightly the draft became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and very quietly the draft became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_104_control_one_adverb_still_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "and quickly Lane became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and also Lane became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_104_control_mention_itself_stacked_adverbs_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "and quite rightly it became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and very quietly the duration became withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    # ------------------------------------------------------------ F15-105

    def test_f15_105_hyphenated_carrier_names_stand(self):
        for name in ("Record-Keeper", "Log-Book", "Claim-Handler"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands and " + name + " became withdrawn.")
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_105_two_word_and_role_subjects_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "and Lane Record became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and the log keeper became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and the record keeper became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_105_control_genuine_carrier_subjects_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "and the record became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and the duration became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and the claim became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and the log became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and very quietly the record became withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_105_control_plain_name_and_pronoun_subjects_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "and Lane became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and she became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    # ------------------------------------------------------------ F15-106

    def test_f15_106_two_particle_surnames_stand(self):
        for name in ("de la Cruz", "van der Berg", "de los Reyes"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands and " + name + " became withdrawn.")
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_106_control_one_particle_and_plain_surnames_stand(self):
        for name in ("van Lane", "de Cruz", "Lane"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands and " + name + " became withdrawn.")
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_106_particle_surnames_interval_path_stand(self):
        for note in (
                "Note: an interval duration stands for Step 1 and "
                "de la Cruz became withdrawn.",
                "Note: an interval duration stands for Step 1 and "
                "van der Berg became withdrawn."):
            with self.subTest(note=note):
                self._assert_interval_stands(note)

    # ------------------------------------------------------------ F15-107

    def test_f15_107_quoted_parenthetical_split_complement_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, not "
            "only was it not, \"Lane noted\", withdrawn, it was "
            "also logged.")

    def test_f15_107_bracketed_parenthetical_split_complement_stands(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, not "
            "only was it not, [Lane noted], withdrawn, it was "
            "also logged.")

    def test_f15_107_control_comma_and_dash_twins_still_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "not only was it not, Lane noted, withdrawn, it "
                "was also logged.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "not only was it not " + EM + " Lane noted " +
                EM + " withdrawn, it was also logged."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_107_quoted_parenthetical_genuine_denial_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was, \"Lane noted\", withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was, [Lane noted], withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_107_control_other_subject_quoted_parenthetical_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was, \"Lane noted\", withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was, [Lane noted], withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_107_control_genuine_denial_beside_frame_taken_out(self):
        self._assert_taken_out(
            "Not only was no BANKED interval duration 5 hours "
            "recorded for Step 1.")


if __name__ == "__main__":
    unittest.main()
