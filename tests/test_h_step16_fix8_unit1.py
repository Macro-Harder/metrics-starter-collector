"""Step 16 fix pass 8 unit 1 tests: the Q-4 tally head reach.

Pinning tests for register item R16-8-01 (Medium, B8-01)
of Step 16 round 8. The governing rule of the pass, in
its extended form: a piece not read in full, for whatever
reason, is not read, and its converse: a piece that is no
feeder flips nothing.

R16-8-01: a malformed tally statement under a head the
counted pattern itself takes, but the fix pass 7 head
test does not reach, takes Q-4 missing under the no
feeder record code in the alone position and drops the
step unnamed in the beside position, while its counted
sibling under the same head counts, because
_trace_candidates counts the numeric tally pattern with
no head test at all. The five driven forms are a six
word tally head, a long trace summary head, a numbered
list form, a hyphenated head and a comma head, beside
the six word gate record review head of the round 8
correctness construction. Locus: derivation_core.py,
_malformed_trace_statements and _tally_statement_head,
against _trace_candidates. The cure these tests pin:
the malformed tally scan reaches every tally statement
head the row itself counts, in the alone position taking
the governed not derivable form naming the step and the
feeder piece, and in the beside position naming the
step uncounted in the present row coverage, in gate
records and gate rulings alike.

Held controls stand pinned beside the defect forms:
the five word head standing cured, the five charged
heads and the settled heads of fix pass 7, the golden
prose lines flipping nothing, a malformed tally
fragment in prose position opening with no tally
statement head flipping nothing, the step companion
converse forms, the same step seam, the read control
and the genuinely absent missing form.

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
from tests.test_h_step16_fix4_unit1 import COMPANION_PATH
from tests.test_h_step16_fix6_unit3 import TALLY_B6_BAD
from tests.test_h_step16_fix7_unit2 import (
    GATE_2, GOLDEN_BOARD_LINE, GOLDEN_CLOSING_LINE, _bad, _read)
from tests.test_h_step16_unit1 import _write_tree

RULING_2 = "steps/step-02-gate-ruling.md"
GATE_3 = "steps/step-03-gate-record.md"

SIX_WORD = "Alpha beta gamma delta epsilon tally"
REVIEW_HEAD = "Step 2 gate record review tally"
LONG_SUMMARY = "Alpha beta gamma delta epsilon trace summary"
FIVE_WORD = "Alpha beta gamma delta tally"
PROSE_FRAGMENT = (
    "A malformed fragment stands in prose position here. "
    "LANDED figures stand here, no counts stated")


def _assert_no_absence(test, block):
    test.assertNotIn("no first trace record stands", block)
    test.assertNotIn("no feeder record for the metric exists",
                     block)
    test.assertNotIn("no-feeder-record", block)


class TestStep16Fix8Unit1(FixtureTestCase):

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

    def _assert_missing(self, report):
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "missing", "Q-4")
        self.assertIn("no-feeder-record", q4)
        self.assertNotIn("uncounted", q4)

    # ------------------------------------------------------
    # Defect forms, R16-8-01, five heads alone
    # ------------------------------------------------------

    def test_r16_8_01_six_word_tally_head_alone(self):
        """B8-01 six word head: a malformed tally alone."""
        report = self._run(self._alone_files(_bad(SIX_WORD)))
        self._assert_alone_cured(report)

    def test_r16_8_01_review_tally_head_alone(self):
        """Round 8 correctness head: gate record review tally."""
        report = self._run(self._alone_files(_bad(REVIEW_HEAD)))
        self._assert_alone_cured(report)

    def test_r16_8_01_long_trace_summary_head_alone(self):
        """B8-01 long trace summary head: a malformed tally."""
        report = self._run(self._alone_files(_bad(LONG_SUMMARY)))
        self._assert_alone_cured(report)

    def test_r16_8_01_numbered_list_tally_head_alone(self):
        """B8-01 numbered list form: 1. Board tally alone."""
        report = self._run(
            self._alone_files("1. " + _bad("Board tally")))
        self._assert_alone_cured(report)

    def test_r16_8_01_hyphenated_tally_head_alone(self):
        """B8-01 hyphenated head: Step-2 tally alone."""
        report = self._run(self._alone_files(_bad("Step-2 tally")))
        self._assert_alone_cured(report)

    def test_r16_8_01_comma_tally_head_alone(self):
        """B8-01 comma head: Board, tally alone."""
        report = self._run(self._alone_files(_bad("Board, tally")))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Defect forms, R16-8-01, beside a counted trace
    # ------------------------------------------------------

    def test_r16_8_01_six_word_tally_head_beside_counted(self):
        """B8-01 six word head beside form: the step dropped."""
        report = self._run(self._beside_files(_bad(SIX_WORD)))
        self._assert_beside_cured(report)

    def test_r16_8_01_long_trace_summary_head_beside_counted(self):
        """B8-01 long trace summary beside form: step dropped."""
        report = self._run(self._beside_files(_bad(LONG_SUMMARY)))
        self._assert_beside_cured(report)

    def test_r16_8_01_numbered_list_tally_head_beside_counted(self):
        """B8-01 numbered list beside form: the step dropped."""
        report = self._run(
            self._beside_files("1. " + _bad("Board tally")))
        self._assert_beside_cured(report)

    def test_r16_8_01_hyphenated_tally_head_beside_counted(self):
        """B8-01 hyphenated head beside form: step dropped."""
        report = self._run(self._beside_files(_bad("Step-2 tally")))
        self._assert_beside_cured(report)

    def test_r16_8_01_comma_tally_head_beside_counted(self):
        """B8-01 comma head beside form: the step dropped."""
        report = self._run(self._beside_files(_bad("Board, tally")))
        self._assert_beside_cured(report)

    # ------------------------------------------------------
    # Defect forms, R16-8-01, the gate ruling forms
    # ------------------------------------------------------

    def test_r16_8_01_six_word_tally_head_gate_ruling_alone(self):
        """B8-01 gate ruling form: a six word malformed tally."""
        report = self._run(
            self._alone_files(_bad(SIX_WORD), ruling=True))
        self._assert_alone_cured(report, path=RULING_2)

    def test_r16_8_01_review_tally_head_gate_ruling_alone(self):
        """Gate ruling form: the gate record review tally head."""
        report = self._run(
            self._alone_files(_bad(REVIEW_HEAD), ruling=True))
        self._assert_alone_cured(report, path=RULING_2)

    # ------------------------------------------------------
    # Counted sibling controls of the defect constructions
    # ------------------------------------------------------

    def test_r16_8_01_six_word_tally_head_counted_control(self):
        """Counted control: the six word head counted form."""
        report = self._run(self._alone_files(_read(SIX_WORD)))
        self._assert_counted(report)

    def test_r16_8_01_review_tally_head_counted_control(self):
        """Counted control: the review head counted form."""
        report = self._run(self._alone_files(_read(REVIEW_HEAD)))
        self._assert_counted(report)

    def test_r16_8_01_long_trace_summary_head_counted_control(self):
        """Counted control: the long trace summary counted."""
        report = self._run(self._alone_files(_read(LONG_SUMMARY)))
        self._assert_counted(report)

    def test_r16_8_01_numbered_list_tally_head_counted_control(self):
        """Counted control: the numbered list counted form."""
        report = self._run(
            self._alone_files("1. " + _read("Board tally")))
        self._assert_counted(report)

    def test_r16_8_01_hyphenated_tally_head_counted_control(self):
        """Counted control: the hyphenated head counted form."""
        report = self._run(self._alone_files(_read("Step-2 tally")))
        self._assert_counted(report)

    def test_r16_8_01_comma_tally_head_counted_control(self):
        """Counted control: the comma head counted form."""
        report = self._run(self._alone_files(_read("Board, tally")))
        self._assert_counted(report)

    # ------------------------------------------------------
    # Held controls, cured heads of fix pass 7
    # ------------------------------------------------------

    def test_r16_8_held_five_word_tally_head_alone(self):
        """Held control: the five word head stands cured."""
        report = self._run(self._alone_files(_bad(FIVE_WORD)))
        self._assert_alone_cured(report)

    def test_r16_8_held_board_tally_head_alone(self):
        """Held control: the charged Board tally head alone."""
        report = self._run(self._alone_files(_bad("Board tally")))
        self._assert_alone_cured(report)

    def test_r16_8_held_trace_summary_head_alone(self):
        """Held control: the charged Trace summary head alone."""
        report = self._run(self._alone_files(_bad("Trace summary")))
        self._assert_alone_cured(report)

    def test_r16_8_held_settled_gate_tally_alone(self):
        """Held control: the settled Gate tally form alone."""
        report = self._run(self._alone_files(TALLY_B6_BAD))
        self._assert_alone_cured(report)

    def test_r16_8_held_settled_gate_tally_blockquote_form(self):
        """Held control: a malformed Gate tally as a blockquote."""
        report = self._run(self._alone_files("> " + TALLY_B6_BAD))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Held controls, prose positions flipping nothing
    # ------------------------------------------------------

    def test_r16_8_held_golden_board_tally_member_line(self):
        """Held golden form: the board tally member line."""
        report = self._run(self._alone_files(GOLDEN_BOARD_LINE))
        self._assert_missing(report)

    def test_r16_8_held_golden_closing_prose_line(self):
        """Held golden form: the closing board tally prose line."""
        report = self._run(self._alone_files(GOLDEN_CLOSING_LINE))
        self._assert_missing(report)

    def test_r16_8_held_prose_fragment_no_head(self):
        """Held prose position: a fragment with no tally head."""
        report = self._run(self._alone_files(PROSE_FRAGMENT))
        self._assert_missing(report)

    def test_r16_8_held_companion_malformed_tally_converse(self):
        """Held converse: a malformed tally in a step companion."""
        files = _clean_files()
        files[COMPANION_PATH] = (
            "# Step 2 notes\n\n" + _bad(SIX_WORD) + "\n")
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_8_held_same_step_seam(self):
        """Held seam: a malformed tally for a counted step."""
        files = _clean_files()
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        files["steps/step-03-gate-ruling.md"] = gate_ruling(
            3, extra=TALLY_B6_BAD)
        report = self._run(files)
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("uncounted", q4)

    def test_r16_8_held_read_control_byte_for_byte(self):
        """Held control: the gate records read, 8 LANDED of 8."""
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_8_held_absent_feeder_byte_for_byte(self):
        """Held control: no gate records, genuinely absent."""
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
