"""Step 15 fix round 11 tests: denial runs, rejoins, subjects, frames.

Each charged case pins one fix register item in the duration
denial machinery of derivation_core.py. F15-86 (CB10-4): the
positional run on the shared _RUN_TOKEN vocabulary barred the
articles outright, so the plainest article carrying phrases of
the F15-75 family (was in the end withdrawn, was in a sense
withdrawn, was on the record withdrawn, was at the time
withdrawn, was in the long run withdrawn, was by the book
withdrawn) left a denied figure standing on the after, before
and interval paths, while the same phrases set off by commas
or parentheses were taken out, and a quoted adverb in the run
(was "flatly" withdrawn) stood with them. F15-87 (CB10-5): the
parenthetical rejoin still enumerated its setting off marks
(an em dash parenthetical, was [em dash] Lane noted [em dash]
withdrawn), its reporting verb tenses (the present tense
forms notes, says and observes beside the past tense family)
and its clause length (a reporting clause one word past the
nine word cap). F15-88 (CB10-6): the joined subject test still
enumerated its conjunctions (as, since and because joins), its
intervening adverbs (and also, and then, where yet alone was
admitted) and its name forms (the hyphenated Lane-Smith and
the internal capital McLane surnames). F15-89 (CB10-7): the
doubled affirming frame failed where its complement was split
by a comma parenthetical (not only was it not, Lane noted,
withdrawn and its in fact twin) and where the complement
carried an article phrase on the before side (not only was
the duration not in the end withdrawn). Assertions pin the
parser result as a whole, the Step 1 banked wait figure, and
the T-2 and T-4 grounds, in the form of the round 10 denial
module.
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


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round11Denial(FixtureTestCase):

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

    # ------------------------------------------------------------ F15-86

    def test_f15_86_article_phrases_after_taken_out(self):
        for phrase in ("in the end", "in a sense", "on the record",
                       "at the time", "in the long run", "by the book"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, the duration was " + phrase +
                    " withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_86_article_phrases_before_and_interval_taken_out(self):
        for note in (
                "The duration was in the end withdrawn, Step 1 "
                "BANKED interval duration 5 hours stands.",
                "The duration was on the record withdrawn, Step 1 "
                "BANKED interval duration 5 hours stands.",
                "Note: an interval duration stands for Step 1, "
                "the duration was in the end withdrawn.",
                "Note: an interval duration stands for Step 1, "
                "the duration was at the time withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_86_quoted_adverb_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was \"flatly\" withdrawn.",
                "The duration was \"flatly\" withdrawn, Step 1 "
                "BANKED interval duration 5 hours stands."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_86_control_set_off_twins_still_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was, in the end, withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was (in the end) withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was soon withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_86_control_other_subject_article_phrases_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was in the end withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was in a sense withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was \"flatly\" withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    # ------------------------------------------------------------ F15-87

    def test_f15_87_em_dash_parenthetical_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands, the "
            "duration was " + EM + " Lane noted " + EM +
            " withdrawn.")

    def test_f15_87_present_tense_reporting_verbs_taken_out(self):
        for verb in ("notes", "says", "observes"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands, the duration was, Lane " + verb +
                    ", withdrawn.")
            with self.subTest(note=note):
                self._assert_taken_out(note)
        self._assert_taken_out(
            "The duration was, Lane says, withdrawn, Step 1 "
            "BANKED interval duration 5 hours stands.")

    def test_f15_87_long_reporting_clause_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the duration was, as the senior reviewing "
                "officer Lane quite rightly and very carefully "
                "noted, withdrawn.",
                "The duration was, as the senior reviewing "
                "officer Lane quite rightly and very carefully "
                "noted, withdrawn, Step 1 BANKED interval "
                "duration 5 hours stands."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_87_control_other_subject_new_rejoin_shapes_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was " + EM + " Lane noted " + EM +
                " withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was, Lane notes, withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "the draft was, as the senior reviewing officer "
                "Lane quite rightly and very carefully noted, "
                "withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    # ------------------------------------------------------------ F15-88

    def test_f15_88_reason_clause_joins_stand(self):
        for join in ("as", "since", "because"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands " + join + " Lane became withdrawn.")
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_88_intervening_adverbs_stand(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "and also Lane became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and then Lane became withdrawn."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_88_compound_surnames_stand(self):
        for name in ("Lane-Smith", "McLane"):
            note = ("Step 1 BANKED interval duration 5 hours "
                    "stands and " + name + " became withdrawn.")
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_88_control_mention_itself_new_joins_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands "
                "as it became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "because it became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "and also it became withdrawn.",
                "Step 1 BANKED interval duration 5 hours stands "
                "since the duration became withdrawn."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    # ------------------------------------------------------------ F15-89

    def test_f15_89_split_complement_parenthetical_stands(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands, "
                "not only was it not, Lane noted, withdrawn, it "
                "was also logged.",
                "Step 1 BANKED interval duration 5 hours stands, "
                "not only was it not, in fact, withdrawn, it was "
                "also logged."):
            with self.subTest(note=note):
                self._assert_banked_stands(note)

    def test_f15_89_before_side_article_phrase_complement_stands(self):
        self._assert_banked_stands(
            "Not only was the duration not in the end "
            "withdrawn, a BANKED interval duration 5 hours "
            "stands for Step 1.")

    def test_f15_89_control_plain_doubled_stands_and_genuine_denial_taken_out(self):
        self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands, not "
            "only was it not withdrawn, it was also logged.")
        self._assert_taken_out(
            "Not only was no BANKED interval duration 5 hours "
            "recorded for Step 1.")


if __name__ == "__main__":
    unittest.main()
