"""Step 15 fix round 10 tests: falsity predicates, segment bounds.

Each charged case pins one fix register item in the attribution
machinery of derivation_core.py. F15-80 (CB9-11 with C9-1): the
falsity predicate set stopped at the named forms, so "wrong",
named in the F15-69 register itself, stood in no falsity
pattern, and its kin (untrue, fabricated, spurious, invalid)
stood in none either; each attributed its denied step at
tier 0. The word wrong also failed in the other direction:
with a carrier subject (the claim) the listed word test read
it as a denial of the mention itself and erased the standing
figure whole, genuine recorded for part included. A falsity
predicate stated of a recording scopes that recording's
attribution, whatever subject carries it, and does not deny
the figure itself. F15-81 (CB9-12): the attribution segment
reading kept its own closed boundary list, narrower than the
sentence boundary rule and the closure join set: "or" and
"while" were no segment bounds, so a denial standing before a
genuine recorded for joined by one of them scoped the genuine
wording too; a falsity predicate in the comma part immediately
before a bare recorded for part scoped nothing, so the bare
part attributed; and the segment split at every full stop
insulated a falsity predicate standing after a title (Dr.,
Prof.) from the wording it governs, where the shared boundary
rule holds that stop is no sentence end. Assertions pin the
parser result as a whole and the full printed figures, as the
round 9 attribution module does.
"""
import unittest

from metrics_starter_collector.derivation_core import _t4_banked_durations
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, path_ledger,
                                     row_block, run_tool)

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
T4_STATEMENT = (
    "Statement line: the row is shown without its queue cross check, "
    "from the BANKED interval durations standing in the feeder "
    "records, with only the decision table cross check absent.")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


class TestStep15Round10Attribution(FixtureTestCase):

    # ------------------------------------------------------------ shared

    def _report(self, note_text):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note_text, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, result.stdout

    def _assert_banked(self, note, parsed, figures):
        root, report = self._report(note)
        self.assertEqual(_t4_banked_durations(capture(root)), parsed)
        block = row_block(report, "T-4")
        assert_verdict(self, block, "present", "T-4")
        lines = block.splitlines()
        self.assertEqual(
            lines[0],
            "T-4 | present | Pointer: PATH-LEDGER.md | " + figures +
            " | denominator decision items and banked states in the tree")
        self.assertEqual(lines[1], T4_STATEMENT)
        return root, report

    def _assert_stepless(self, note):
        return self._assert_banked(
            note, [(None, 5.0, True)], "banked wait 5 hours")

    # ---------------------------------------------------------- F15-80

    def test_f15_80_wrong_with_genuine_recorded_for_governs_step1(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the figure "
            "recorded for Step 2 is wrong, recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_80_wrong_alone_attributes_nothing(self):
        root, report = self._assert_stepless(
            "BANKED interval duration 5 hours stands, the figure "
            "recorded for Step 2 is wrong.")
        self.assertNotIn("Step 2 banked wait", report)

    def test_f15_80_kin_predicates_never_attribute(self):
        for predicate in ("is untrue", "was fabricated",
                          "is spurious", "is invalid"):
            note = ("BANKED interval duration 5 hours stands, the "
                    "figure recorded for Step 2 " + predicate + ".")
            with self.subTest(note=note):
                root, report = self._assert_stepless(note)
                self.assertNotIn("Step 2 banked wait", report)

    def test_f15_80_kin_predicates_with_genuine_govern_step1(self):
        for predicate in ("is wrong", "is untrue", "was fabricated",
                          "is spurious", "is invalid"):
            note = ("BANKED interval duration 5 hours stands, the "
                    "figure recorded for Step 2 " + predicate +
                    ", recorded for Step 1.")
            with self.subTest(note=note):
                self._assert_banked(
                    note, [(1, 5.0, True)],
                    "Step 1 banked wait 5 hours")

    def test_f15_80_wrong_non_carrier_subjects_scope(self):
        for note in (
                "BANKED interval duration 5 hours stands, the entry "
                "recorded for Step 2 was wrong.",
                "BANKED interval duration 5 hours stands, the entry "
                "recorded for Step 2 is wrong.",
                "BANKED interval duration 5 hours stands, recorded "
                "for Step 2 wrong."):
            with self.subTest(note=note):
                root, report = self._assert_stepless(note)
                self.assertNotIn("Step 2 banked wait", report)

    def test_f15_80_wrong_carrier_subject_does_not_erase_mention(self):
        root, report = self._assert_stepless(
            "BANKED interval duration 5 hours stands, the claim "
            "recorded for Step 2 was wrong.")
        self.assertIn("banked wait 5 hours", report)

    def test_f15_80_wrong_carrier_with_genuine_governs_step1(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the claim "
            "recorded for Step 2 was wrong, recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_80_wrong_carrier_on_before_side_genuine_governs(self):
        self._assert_banked(
            "Recorded for Step 1, the claim recorded for Step 2 "
            "was wrong: BANKED interval duration 5 hours stands.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_80_controls_erroneous_and_subject_discipline(self):
        self._assert_stepless(
            "BANKED interval duration 5 hours stands, the figure "
            "recorded for Step 2 is erroneous.")
        self._assert_banked(
            "Step 1 BANKED interval duration 5 hours stands, the "
            "entry was withdrawn.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    # ---------------------------------------------------------- F15-81

    def test_f15_81_or_bound_genuine_governs(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, no interval "
            "duration was recorded for Step 2 or the figure "
            "recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_81_while_bound_genuine_governs(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, no interval "
            "duration was recorded for Step 2 while the figure "
            "recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_81_false_or_bound_genuine_governs(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the claim "
            "recorded for Step 2 is false or the figure recorded "
            "for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_81_or_bound_fallback_skips_scoped_step(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the figure "
            "recorded for Step 2 is invalid or Step 3 was noted.",
            [(3, 5.0, True)], "Step 3 banked wait 5 hours")

    def test_f15_81_adjacent_falsity_part_scopes_bare_recorded_for(self):
        for note in (
                "BANKED interval duration 5 hours stands, the "
                "recording is in error, recorded for Step 2.",
                "BANKED interval duration 5 hours stands, the claim "
                "is false, recorded for Step 2."):
            with self.subTest(note=note):
                root, report = self._assert_stepless(note)
                self.assertNotIn("Step 2 banked wait", report)

    def test_f15_81_adjacent_falsity_then_genuine_governs(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the recording "
            "is in error, recorded for Step 2, recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_81_control_falsity_with_own_wording_scopes_no_next(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the claim "
            "recorded for Step 2 is false, recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_81_title_stop_does_not_insulate_falsity(self):
        for title in ("Dr.", "Prof."):
            note = ("BANKED interval duration 5 hours stands, "
                    "recorded for Step 2 by " + title +
                    " Lane in error.")
            with self.subTest(note=note):
                root, report = self._assert_stepless(note)
                self.assertNotIn("Step 2 banked wait", report)

    def test_f15_81_controls_title_genuine_and_no_title_twin(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, recorded for "
            "Step 2 by Dr. Lane.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")
        self._assert_stepless(
            "BANKED interval duration 5 hours stands, recorded for "
            "Step 2 by Lane in error.")


if __name__ == "__main__":
    unittest.main()
