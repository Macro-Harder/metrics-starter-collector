"""Step 15 fix round 12 tests: figure ladder multipliers.

Each charged case pins fix register item F15-108 (CB11-10)
in the figure reading machinery of derivation_core.py.
F15-90 built the scale ladder above thousand rung by rung:
each scale word multiplies the group before it, its tail
is the compound of the rungs below it, but its multiplier
took only a hundred form, a small form or digits. A
multiplier that is itself a scale compound therefore read
as no figure at all: "one thousand million" and "one
hundred thousand million" named no figure, and a denial
of one thousand million hours took a standing 5 hours out
by the no figure route, although the denial names a
different figure. The cure extends the ladder's own rule
to the multiplier side: a rung's multiplier is the
compound of the rungs below it, as its tail already is,
so a multiplier compound may itself climb the ladder rung
by rung (a thousand as the multiplier of million, a
million as the multiplier of billion), each scale word in
the multiplier standing below the rung it multiplies. A
multiplier naming the rung itself or a higher rung stands
outside the form, and the ladder's stop at trillion,
sustained as a design bound in confirmation round 11,
stands unchanged. Assertions pin the direct reading
through _clause_subject and the denial scoping in both
directions: a denial of the same figure takes the
standing figure out, and a denial of a different figure
leaves it standing, the parser result as a whole and the
printed T-4 row. The settled figure forms of rounds 6 to
11 hold as controls.
"""
import unittest

from metrics_starter_collector.derivation_core import (
    _clause_subject, _t4_banked_durations)
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, path_ledger,
                                     row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
T4_MISSING_SHOWS = ("no banked state and no decision item count "
                    "stands in the feeder records for this metric")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round12Figures(FixtureTestCase):

    # ------------------------------------------------------------ shared

    def _report(self, note_text):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note_text, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, result.stdout

    def _assert_stands(self, note_text, parsed, wait_text):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)), parsed)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        self.assertIn(wait_text, t4)
        return root, report

    def _assert_taken_out(self, note_text):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)), [])
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertIn(T4_MISSING_SHOWS, t4)
        self.assertNotIn("banked wait", report)
        return root, report

    def _denial_note(self, standing, words):
        return ("Step 1 BANKED interval duration " + standing +
                " hours stands, and no interval duration " + words +
                " hours was recorded for Step 1.")

    def _assert_reading(self, words, value):
        step, figure = _clause_subject(
            "no interval duration " + words + " hours was recorded")
        self.assertIsNone(step)
        self.assertEqual(figure, value)

    def _assert_no_reading(self, words):
        step, figure = _clause_subject(
            "no interval duration " + words + " hours was recorded")
        self.assertIsNone(step)
        self.assertIsNone(figure)

    # ---------------------------------------------------------- F15-108

    def test_f15_108_direct_thousand_multiplier_of_million(self):
        for words, value in (("one thousand million", 1000000000.0),
                             ("one hundred thousand million",
                              100000000000.0),
                             ("two thousand million", 2000000000.0),
                             ("five thousand million", 5000000000.0),
                             ("one thousand and five million",
                              1005000000.0),
                             ("one thousand five hundred million",
                              1500000000.0),
                             ("fifteen hundred thousand million",
                              1500000000000.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_108_direct_crossed_multipliers_higher_rungs(self):
        for words, value in (("one thousand billion",
                              1000000000000.0),
                             ("one million billion",
                              1000000000000000.0),
                             ("one hundred thousand billion",
                              100000000000000.0),
                             ("one thousand trillion",
                              1000000000000000.0),
                             ("one trillion and five thousand million",
                              1005000000000.0),
                             ("one billion and five thousand million",
                              6000000000.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_108_direct_hyphenated_crossed_forms(self):
        for words, value in (("one-thousand-million", 1000000000.0),
                             ("one-hundred-thousand-million",
                              100000000000.0),
                             ("one-thousand-and-five-million",
                              1005000000.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)

    def test_f15_108_point_form_with_crossed_multiplier(self):
        self._assert_reading("one thousand million point five",
                             1000000000.5)

    def test_f15_108_same_figure_denial_taken_out(self):
        for standing, words in (("1000000000", "one thousand million"),
                                ("100000000000",
                                 "one hundred thousand million"),
                                ("1005000000",
                                 "one thousand and five million")):
            with self.subTest(words=words):
                self._assert_taken_out(self._denial_note(standing, words))
        self._assert_taken_out(
            "No interval duration one thousand million hours was "
            "recorded for Step 1, Step 1 BANKED interval duration "
            "1000000000 hours stands.")

    def test_f15_108_different_figure_denial_stands(self):
        for standing, words in (("5", "one thousand million"),
                                ("5", "one hundred thousand million"),
                                ("1000000", "one thousand million"),
                                ("1000000000",
                                 "one hundred thousand million")):
            with self.subTest(words=words):
                self._assert_stands(
                    self._denial_note(standing, words),
                    [(1, float(standing), True)],
                    "Step 1 banked wait " + standing + " hours")

    def test_f15_108_bound_multipliers_stop_below_the_rung(self):
        for words in ("one million million",
                      "one billion billion",
                      "one billion million",
                      "one trillion billion",
                      "one quadrillion"):
            with self.subTest(words=words):
                self._assert_no_reading(words)

    def test_f15_108_control_settled_scale_forms_hold(self):
        for words, value in (("thirteen hundred", 1300.0),
                             ("fifteen hundred thousand", 1500000.0),
                             ("400 and nine", 409.0),
                             ("10,000", 10000.0),
                             ("one hundred thousand", 100000.0),
                             ("eleven hundred thousand", 1100000.0),
                             ("one million and five", 1000005.0),
                             ("one million and five thousand and five",
                              1005005.0),
                             ("two hundred and fifty million",
                              250000000.0),
                             ("fifteen hundred million", 1500000000.0),
                             ("one billion five hundred million",
                              1500000000.0),
                             ("one trillion and five billion and nine",
                              1005000000009.0),
                             ("two trillion and five billion and nine "
                              "million and seven", 2005009000007.0)):
            with self.subTest(words=words):
                self._assert_reading(words, value)
        self._assert_taken_out(
            self._denial_note("1300", "thirteen hundred"))
        self._assert_taken_out(
            self._denial_note("1000005", "one million and five"))
        self._assert_stands(
            self._denial_note("5", "one million and five"),
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")


if __name__ == "__main__":
    unittest.main()
