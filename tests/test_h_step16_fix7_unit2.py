"""Step 16 fix pass 7 unit 2 tests: the Q-4 tally head unit.

Pinning tests for register item R16-7-03 (Medium, B7-03)
of Step 16 round 7. The governing rule of the pass, in
its extended form: a piece not read in full, for whatever
reason, is not read, and its converse: a piece that is no
feeder flips nothing.

R16-7-03: a malformed tally statement under a head
outside the settled head test of fix pass 6 Unit 3 takes
Q-4 missing under the no feeder record code, alone and
beside, while its counted sibling under the same head
counts, because _trace_candidates counts the numeric
tally pattern with no head test at all while
_malformed_trace_statements reaches only lines opening
with Gate tally, Trace tally, or Trace for step. The
five heads B7-03 drives are Board tally, Step 2 tally,
Tally, Gate record tally, and Trace summary, in gate
records and in the gate ruling form. Locus:
derivation_core.py, _malformed_trace_statements, the
tally branch, against _trace_candidates. The cure these
tests pin: the malformed tally scan reaches every tally
statement head the row itself counts, in the alone
position taking the governed not derivable form naming
the step and the feeder piece, and in the beside
position naming the step uncounted in the present row
coverage.

Held controls stand pinned beside the defect forms:
the golden board tally lines, which are no trace
statements of this row and must still flip nothing;
every cured Q-4 form of fix passes 5 and 6, the Counts
form, the full trace form, the tally form in its
settled heads in plain, blockquote, list and heading
forms, the same step fallback on the line limit route,
the non feeder boundary of R16-5-12, the converse limb
of R16-6-07, and the step companion converse forms;
the same step seam; and the genuinely absent missing
form.

Trees are written through the Unit 1 module helpers of
fix pass 1, because the constructions turn on exact
byte counts. The product is invoked through run_tool,
which runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, gate_ruling,
    row_block, run_tool)
from tests.test_h_step16_fix3_unit1 import (
    ABSENT_Q4, READ_Q4, TRACE_2, TRACE_3, _clean_files)
from tests.test_h_step16_fix4_unit1 import (
    COMPANION_PATH, COMPANION_TEXT, PURPLE_PATH)
from tests.test_h_step16_fix5_unit3 import (
    FULL_TRACE_BAD, PURPLE_COUNTS_BAD_C5)
from tests.test_h_step16_fix6_unit3 import (
    BLUE_PATH, BLUE_BAD_FIRST_TRACE, BLUE_TEXT, GATE_2,
    PLAIN_PATH, PLAIN_COUNTS_TEXT, TALLY_B6_BAD,
    TALLY_C6_A_BAD, TALLY_C6_B_BAD)
from tests.test_h_step16_unit1 import _padded, _write_tree

RULING_2 = "steps/step-02-gate-ruling.md"
RULING_3 = "steps/step-03-gate-ruling.md"
GATE_3 = "steps/step-03-gate-record.md"
TRACE_2_SMALL = (
    "First trace for step 2: 2 LANDED of 2 items "
    "checked, 0 PARTIAL, 0 CONTRADICTED.")

HEADS = ("Board tally", "Step 2 tally", "Tally",
         "Gate record tally", "Trace summary")


def _bad(head):
    return (head + ": items checked stand here. LANDED "
            "figures stand here, no counts stated")


def _read(head):
    return (head + ": 2 of 2 LANDED, 0 PARTIAL, "
            "0 CONTRADICTED")


GOLDEN_BOARD_LINE = (
    "- Board tally: member 1, recycle for a narrow "
    "completion pass, with four required completions; "
    "member 2, approve with notes, with four notes "
    "carried forward.")
GOLDEN_CLOSING_LINE = (
    "3. Record the board tally and this verdict in the "
    "closing entry: member 1 RECYCLE for roster closure "
    "only, its three completions LANDED and its stated "
    "approval condition satisfied; member 2 approve "
    "with notes, six notes binding.")


def _assert_no_absence(test, block):
    test.assertNotIn("no first trace record stands", block)
    test.assertNotIn("no feeder record for the metric exists",
                     block)
    test.assertNotIn("no-feeder-record", block)


class TestStep16Fix7Unit2(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _alone_files(self, line, ruling=False):
        files = _clean_files()
        if ruling:
            files[RULING_2] = gate_ruling(2, extra=line)
        else:
            files[GATE_2] = gate_record(2, extra=line)
        return files

    def _assert_alone_cured(self, report, path=GATE_2):
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(path, q4)
        _assert_no_absence(self, q4)

    def _assert_beside_cured(self, report):
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def _beside_files(self, line):
        files = self._alone_files(line)
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        return files

    def _assert_counted(self, report):
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2, 2 of 2 LANDED", q4)
        self.assertIn("totals 2 LANDED", q4)

    # ------------------------------------------------------
    # Defect forms, R16-7-03, five heads alone
    # ------------------------------------------------------

    def test_r16_7_03_board_tally_alone(self):
        """B7-03 Board tally head: a malformed tally alone."""
        report = self._run(self._alone_files(_bad("Board tally")))
        self._assert_alone_cured(report)

    def test_r16_7_03_step_2_tally_alone(self):
        """B7-03 Step 2 tally head: a malformed tally alone."""
        report = self._run(self._alone_files(_bad("Step 2 tally")))
        self._assert_alone_cured(report)

    def test_r16_7_03_tally_alone(self):
        """B7-03 Tally head: a malformed tally alone."""
        report = self._run(self._alone_files(_bad("Tally")))
        self._assert_alone_cured(report)

    def test_r16_7_03_gate_record_tally_alone(self):
        """B7-03 Gate record tally head: a malformed tally alone."""
        report = self._run(
            self._alone_files(_bad("Gate record tally")))
        self._assert_alone_cured(report)

    def test_r16_7_03_trace_summary_alone(self):
        """B7-03 Trace summary head: a malformed tally alone."""
        report = self._run(self._alone_files(_bad("Trace summary")))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Defect forms, R16-7-03, five heads beside a counted trace
    # ------------------------------------------------------

    def test_r16_7_03_board_tally_beside_counted(self):
        """B7-03 Board tally beside form: the step dropped."""
        report = self._run(self._beside_files(_bad("Board tally")))
        self._assert_beside_cured(report)

    def test_r16_7_03_step_2_tally_beside_counted(self):
        """B7-03 Step 2 tally beside form: the step dropped."""
        report = self._run(self._beside_files(_bad("Step 2 tally")))
        self._assert_beside_cured(report)

    def test_r16_7_03_tally_beside_counted(self):
        """B7-03 Tally beside form: the step dropped."""
        report = self._run(self._beside_files(_bad("Tally")))
        self._assert_beside_cured(report)

    def test_r16_7_03_gate_record_tally_beside_counted(self):
        """B7-03 Gate record tally beside form: step dropped."""
        report = self._run(
            self._beside_files(_bad("Gate record tally")))
        self._assert_beside_cured(report)

    def test_r16_7_03_trace_summary_beside_counted(self):
        """B7-03 Trace summary beside form: the step dropped."""
        report = self._run(self._beside_files(_bad("Trace summary")))
        self._assert_beside_cured(report)

    # ------------------------------------------------------
    # Defect form, R16-7-03, the gate ruling form
    # ------------------------------------------------------

    def test_r16_7_03_board_tally_gate_ruling_alone(self):
        """B7-03 gate ruling form: a malformed Board tally."""
        report = self._run(
            self._alone_files(_bad("Board tally"), ruling=True))
        self._assert_alone_cured(report, path=RULING_2)

    # ------------------------------------------------------
    # Counted sibling controls of the defect constructions
    # ------------------------------------------------------

    def test_r16_7_03_board_tally_counted_control(self):
        """Counted control: the Board tally counted form."""
        report = self._run(self._alone_files(_read("Board tally")))
        self._assert_counted(report)

    def test_r16_7_03_step_2_tally_counted_control(self):
        """Counted control: the Step 2 tally counted form."""
        report = self._run(self._alone_files(_read("Step 2 tally")))
        self._assert_counted(report)

    def test_r16_7_03_tally_counted_control(self):
        """Counted control: the Tally counted form."""
        report = self._run(self._alone_files(_read("Tally")))
        self._assert_counted(report)

    def test_r16_7_03_gate_record_tally_counted_control(self):
        """Counted control: the Gate record tally counted form."""
        report = self._run(
            self._alone_files(_read("Gate record tally")))
        self._assert_counted(report)

    def test_r16_7_03_trace_summary_counted_control(self):
        """Counted control: the Trace summary counted form."""
        report = self._run(self._alone_files(_read("Trace summary")))
        self._assert_counted(report)

    def test_r16_7_03_board_tally_gate_ruling_counted_control(self):
        """Counted control: the Board tally in a gate ruling."""
        report = self._run(
            self._alone_files(_read("Board tally"), ruling=True))
        self._assert_counted(report)

    # ------------------------------------------------------
    # Held controls, the settled tally heads of fix pass 6
    # ------------------------------------------------------

    def test_r16_7_held_settled_gate_tally_alone(self):
        """Held control: the settled Gate tally form alone."""
        report = self._run(self._alone_files(TALLY_B6_BAD))
        self._assert_alone_cured(report)

    def test_r16_7_held_settled_trace_tally_alone(self):
        """Held control: the settled Trace tally form alone."""
        report = self._run(self._alone_files(TALLY_C6_B_BAD))
        self._assert_alone_cured(report)

    def test_r16_7_held_settled_trace_for_step_alone(self):
        """Held control: the settled Trace for step form alone."""
        report = self._run(self._alone_files(TALLY_C6_A_BAD))
        self._assert_alone_cured(report)

    def test_r16_7_held_settled_gate_tally_blockquote_form(self):
        """Held control: a malformed Gate tally as a blockquote."""
        report = self._run(self._alone_files("> " + TALLY_B6_BAD))
        self._assert_alone_cured(report)

    def test_r16_7_held_settled_gate_tally_list_form(self):
        """Held control: a malformed Gate tally as a list item."""
        report = self._run(self._alone_files("- " + TALLY_B6_BAD))
        self._assert_alone_cured(report)

    def test_r16_7_held_settled_gate_tally_heading_form(self):
        """Held control: a malformed Gate tally as a heading."""
        report = self._run(self._alone_files("## " + TALLY_B6_BAD))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Held controls, the cured Q-4 forms of fix pass 5
    # ------------------------------------------------------

    def test_r16_7_held_counts_form_alone(self):
        """Held control: the cured Counts form alone, fix pass 5."""
        files = _clean_files()
        files[PURPLE_PATH] = PURPLE_COUNTS_BAD_C5
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(PURPLE_PATH, q4)
        _assert_no_absence(self, q4)

    def test_r16_7_held_full_trace_form_alone(self):
        """Held control: the cured full trace form alone."""
        files = _clean_files()
        files[RULING_2] = gate_ruling(2, extra=FULL_TRACE_BAD)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(RULING_2, q4)
        _assert_no_absence(self, q4)

    def test_r16_7_held_same_step_fallback_line_limit_route(self):
        """Held control: the same step bound on the line limit."""
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=TRACE_2_SMALL)
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        files[COMPANION_PATH] = COMPANION_TEXT + ("x" * 70000) + "\n"
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2, 2 LANDED of 2 items checked", q4)
        self.assertIn("totals 6 LANDED", q4)
        self.assertIn("Bound:", q4)
        bound = q4[q4.find("Bound:"):]
        self.assertIn(COMPANION_PATH, bound)
        self.assertIn("line limit", bound)

    def test_r16_7_held_blue_paper_malformed_first_trace_read(self):
        """Held R16-6-07 converse: a blue paper flips nothing."""
        files = _clean_files()
        files[BLUE_PATH] = BLUE_BAD_FIRST_TRACE
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_7_held_blue_paper_unread_non_feeder_boundary(self):
        """Held R16-5-12: an unread blue paper flips nothing."""
        files = _clean_files()
        files[BLUE_PATH] = _padded(BLUE_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_7_held_plain_paper_unread_non_feeder_boundary(self):
        """Held R16-5-12: an unread plain paper flips nothing."""
        files = _clean_files()
        files[PLAIN_PATH] = _padded(PLAIN_COUNTS_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    # ------------------------------------------------------
    # Held controls, converse forms and the golden lines
    # ------------------------------------------------------

    def test_r16_7_held_companion_counted_tally_converse(self):
        """Held converse: a counted tally in a step companion."""
        files = _clean_files()
        files[COMPANION_PATH] = (
            "# Step 2 notes\n\n" + _read("Board tally") + "\n")
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_7_held_companion_malformed_tally_converse(self):
        """Held converse: a malformed tally in a step companion."""
        files = _clean_files()
        files[COMPANION_PATH] = (
            "# Step 2 notes\n\n" + _bad("Board tally") + "\n")
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_7_held_same_step_seam(self):
        """Held seam: a malformed tally for a counted step."""
        files = _clean_files()
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        files[RULING_3] = gate_ruling(3, extra=TALLY_B6_BAD)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("uncounted", q4)

    def test_r16_7_held_golden_board_tally_member_line(self):
        """Held golden form: the board tally member line."""
        report = self._run(self._alone_files(GOLDEN_BOARD_LINE))
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "missing", "Q-4")
        self.assertIn("no-feeder-record", q4)
        self.assertNotIn("uncounted", q4)

    def test_r16_7_held_golden_closing_prose_line(self):
        """Held golden form: the closing board tally prose line."""
        report = self._run(self._alone_files(GOLDEN_CLOSING_LINE))
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "missing", "Q-4")
        self.assertIn("no-feeder-record", q4)
        self.assertNotIn("uncounted", q4)

    def test_r16_7_held_read_control_byte_for_byte(self):
        """Held control: the gate records read, 8 LANDED of 8."""
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_7_held_absent_feeder_byte_for_byte(self):
        """Held control: no gate records, genuinely absent."""
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
