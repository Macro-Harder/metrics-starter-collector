"""Step 15 fix round 8 tests: T-4 attribution reach and precedence.

Each charged case pins fix register item F15-57 (findings CB7-3
and CB7-4) in the T-4 attribution inside _t4_banked_durations in
derivation_core.py. CB7-3: the attribution widening of F15-48
searched the before and after fragments _clause_fragments
computes, and the after fragment runs only to the first semicolon
after the mention, so a step named in a semicolon part after a
BANKED figure was unreachable and the line first Step token
printed for the wrong step, where the comma twin attributed
correctly. The attribution search must read the mention whole
sentence scope, the parts beyond the first semicolon included;
the denial scoping keeps its semicolon breaks unchanged, only
the attribution search widens. CB7-4: the widened search took the
nearest after part naming any step, even a denial clause or an
appendix clause about another subject, ahead of a farther part
stating what the figure was recorded for. A part stating what
the figure was recorded for governs ahead of parts that merely
name a step inside a denial clause or an appendix clause, and a
denial scoped part does not attribute at all. Control cases pin
the behaviour that must not move: the F15-40 own part precedence,
the F15-48 before and after precedence with the nearest part
first on each side, the nearest governing part among plain
recorded for parts, the before side semicolon form, and the
sentence boundary of the widening, where a step in a previous
sentence stays outside and the line first Step token governs.
Every case asserts the parser result as a whole and the full
printed figures field of the T-4 row.
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


class TestStep15Round8Attribution(FixtureTestCase):

    def _assert_banked(self, note, parsed, figures):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note, steps="1, 2, 3")
        root = build_tree(table)
        self.assertEqual(_t4_banked_durations(capture(root)), parsed)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "T-4")
        assert_verdict(self, block, "present", "T-4")
        lines = block.splitlines()
        self.assertEqual(
            lines[0],
            "T-4 | present | Pointer: PATH-LEDGER.md | " + figures +
            " | denominator decision items and banked states in the tree")
        self.assertEqual(lines[1], T4_STATEMENT)
        return result.stdout

    # ---------------------------------------------------- CB7-3 reach

    def test_f15_57_semicolon_after_part_recorded_for_attributes(self):
        self._assert_banked(
            "Step 1 heading: BANKED interval duration 5 hours "
            "stands; recorded for Step 2.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")

    def test_f15_57_part_beyond_second_semicolon_attributes(self):
        self._assert_banked(
            "Step 1 heading: BANKED interval duration 5 hours "
            "stands; the review noted; recorded for Step 2.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")

    def test_f15_57_control_comma_twin_attributes(self):
        self._assert_banked(
            "Step 1 heading: BANKED interval duration 5 hours "
            "stands, recorded for Step 2.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")

    def test_f15_57_control_before_semicolon_subordinate_attributes(self):
        self._assert_banked(
            "Step 1 opened the run; for Step 2, BANKED interval "
            "duration 5 hours stands.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")

    def test_f15_57_control_previous_sentence_step_outside_scope(self):
        self._assert_banked(
            "Step 1 opened the run. BANKED interval duration "
            "5 hours stands; the review noted.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    # ----------------------------------------------- CB7-4 precedence

    def test_f15_57_denial_part_nearest_recorded_for_governs(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, no interval "
            "duration was recorded for Step 2, recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_57_appendix_part_nearest_recorded_for_governs(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, the Step 2 "
            "appendix was filed, recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_57_appendix_shows_part_recorded_for_governs(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, as the "
            "Step 2 appendix shows, recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_57_denial_part_alone_does_not_attribute(self):
        self._assert_banked(
            "Step 1 heading: BANKED interval duration 5 hours "
            "stands, no interval duration was recorded for Step 2.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_57_semicolon_denial_then_recorded_for_attributes(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands; no interval "
            "duration was recorded for Step 2; recorded for Step 1.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_57_control_before_denial_farther_recorded_nearest(self):
        self._assert_banked(
            "No interval duration was recorded for Step 2, the "
            "figure recorded for Step 1: BANKED interval duration "
            "5 hours stands.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    # ------------------------------------------------------ controls

    def test_f15_57_control_own_part_governs_over_recorded_for(self):
        self._assert_banked(
            "For Step 2, Step 1 BANKED interval duration 5 hours "
            "stands, recorded for Step 3.",
            [(1, 5.0, True)], "Step 1 banked wait 5 hours")

    def test_f15_57_control_after_plain_governs_over_before_plain(self):
        self._assert_banked(
            "Note for Step 3: BANKED interval duration 5 hours, "
            "Step 2 wait stands.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")

    def test_f15_57_control_two_after_parts_nearest_first(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, Step 2 wait "
            "noted, Step 1 wait noted.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")

    def test_f15_57_control_recorded_for_parts_nearest_first(self):
        self._assert_banked(
            "BANKED interval duration 5 hours stands, recorded for "
            "Step 2, recorded for Step 1.",
            [(2, 5.0, True)], "Step 2 banked wait 5 hours")


if __name__ == "__main__":
    unittest.main()
