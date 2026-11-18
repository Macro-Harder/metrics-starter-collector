"""Step 16 fix pass 11 unit 2 tests: the Q-4 long marker unit.

Pinning tests for register item R16-11-02 (Medium,
B11-02) of Step 16 round 11. The governing rule of the
pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-11-02: a numbered tally statement standing in the
numbered no colon residual position, behind a bracketed
or parenthesised marker whose token is longer than the
six character limbs of the marker match, takes Q-4
present but not derivable, naming the step and the
feeder piece, although the settled residual places a
numbered head whose run closes on punctuation other
than a colon outside the scan. The marker token matches
no limb at all, so the line is treated as carrying no
marker, the colon condition never engages, and the run
takes the head on the closing tests. The three driven
forms are (1234567) Board tally, [1234567] Board tally
and (appendix) Trace summary, each closing its opening
run on a full stop with no colon in the head. The held
contrasts in the same form, (123456) Board tally and
(1) Board tally, stand missing, so the position turns
on the length of the marker token alone. Locus:
derivation_core.py, _tally_statement_head, its marker
limbs and the colon condition engagement.

The cure these tests pin makes a bracketed or
parenthesised token at the head of the line a list
marker for the scan whatever its length, so the colon
condition engages for it exactly as it engages inside
the present limbs: a head behind such a marker counts
only where a colon closes the run, and a numbered no
colon line under such a marker stands in the settled
residual, missing, in gate records and gate rulings
alike. With a colon closing the run, such heads stand
governed exactly as their counted siblings count.

Held controls stand pinned beside the defect forms:
the held contrasts and every marker form cured by fix
passes 8 to 11; the counted siblings under every driven
head; the golden prose lines flipping nothing; the
settled R16-7-03 prose position; the run closure limb
as Unit 1 restated it; the folded round 10 prose
sentence record and the folded round 11 record, Trace
for step 2a standing missing; every cured head form of
fix passes 7 to 11, sampled here through the Unit 1
heads; the read control and the genuinely absent
missing form.

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
from tests.test_h_step16_fix7_unit2 import (
    GATE_2, GOLDEN_BOARD_LINE, GOLDEN_CLOSING_LINE, _bad, _read)
from tests.test_h_step16_unit1 import _write_tree

RULING_2 = "steps/step-02-gate-ruling.md"
GATE_3 = "steps/step-03-gate-record.md"

PROSE_FRAGMENT = (
    "A malformed fragment stands in prose position here. "
    "LANDED figures stand here, no counts stated")
PROSE_SENTENCE_CLOSING_ON_TALLY = (
    "Record the board tally. LANDED figures stand "
    "here, no counts stated")


def _dot_form(prefix, head):
    return (prefix + head + ". LANDED figures stand here, "
            "no counts stated")


def _assert_no_absence(test, block):
    test.assertNotIn("no first trace record stands", block)
    test.assertNotIn("no feeder record for the metric exists",
                     block)
    test.assertNotIn("no-feeder-record", block)


class TestStep16Fix11Unit2(FixtureTestCase):

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

    def _alone(self, line, ruling=False):
        return self._run(self._alone_files(line, ruling=ruling))

    def _assert_governed(self, report, path=GATE_2):
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(path, q4)
        _assert_no_absence(self, q4)

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
    # Defect forms, R16-11-02, long marker no colon lines
    # standing in the settled residual, alone
    # ------------------------------------------------------

    def test_r16_11_02_long_paren_marker_no_colon_tally(self):
        """B11-02 defect: (1234567) Board tally, no colon."""
        report = self._alone(_dot_form("(1234567) ", "Board tally"))
        self._assert_missing(report)

    def test_r16_11_02_long_bracket_marker_no_colon_tally(self):
        """B11-02 defect: [1234567] Board tally, no colon."""
        report = self._alone(_dot_form("[1234567] ", "Board tally"))
        self._assert_missing(report)

    def test_r16_11_02_long_paren_marker_no_colon_summary(self):
        """B11-02 defect: (appendix) Trace summary, no colon."""
        report = self._alone(_dot_form("(appendix) ", "Trace summary"))
        self._assert_missing(report)

    def test_r16_11_02_long_bracket_word_marker_no_colon(self):
        """B11-02 general form: [appendix] Trace summary."""
        report = self._alone(_dot_form("[appendix] ", "Trace summary"))
        self._assert_missing(report)

    def test_r16_11_02_very_long_digit_marker_no_colon(self):
        """B11-02 general form: a twelve digit bracket marker."""
        report = self._alone(
            _dot_form("[123456789012] ", "Board tally"))
        self._assert_missing(report)

    def test_r16_11_02_long_paren_marker_gate_ruling(self):
        """B11-02 gate ruling form: the long paren marker."""
        report = self._alone(
            _dot_form("(1234567) ", "Board tally"), ruling=True)
        self._assert_missing(report)

    def test_r16_11_02_long_paren_marker_beside(self):
        """B11-02 beside form: the residual step stays unnamed."""
        files = self._alone_files(
            _dot_form("(1234567) ", "Board tally"))
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)
        self.assertNotIn("uncounted", q4)

    # ------------------------------------------------------
    # Colon forms under the long markers, governed, and
    # their counted siblings
    # ------------------------------------------------------

    def test_r16_11_02_long_paren_marker_colon_tally(self):
        """Colon form: (1234567) Board tally with its colon."""
        report = self._alone("(1234567) " + _bad("Board tally"))
        self._assert_governed(report)

    def test_r16_11_02_long_bracket_marker_colon_tally(self):
        """Colon form: [1234567] Board tally with its colon."""
        report = self._alone("[1234567] " + _bad("Board tally"))
        self._assert_governed(report)

    def test_r16_11_02_long_paren_marker_colon_summary(self):
        """Colon form: (appendix) Trace summary, its colon."""
        report = self._alone("(appendix) " + _bad("Trace summary"))
        self._assert_governed(report)

    def test_r16_11_02_long_paren_marker_counted(self):
        """Counted sibling: (1234567) Board tally counted."""
        report = self._alone("(1234567) " + _read("Board tally"))
        self._assert_counted(report)

    def test_r16_11_02_long_bracket_marker_counted(self):
        """Counted sibling: [1234567] Board tally counted."""
        report = self._alone("[1234567] " + _read("Board tally"))
        self._assert_counted(report)

    def test_r16_11_02_long_paren_summary_counted(self):
        """Counted sibling: (appendix) Trace summary counted."""
        report = self._alone("(appendix) " + _read("Trace summary"))
        self._assert_counted(report)

    def test_r16_11_02_long_marker_trace_for_step_colon(self):
        """Colon form: a long marker trace for step line."""
        line = ("(1234567) Trace for step 2: items checked stand "
                "here. LANDED figures stand here, no counts stated")
        self._assert_governed(self._alone(line))

    def test_r16_11_02_long_marker_trace_for_step_no_colon(self):
        """Residual form: a long marker trace for step, no colon."""
        line = ("(1234567) Trace for step 2 items checked stand "
                "here. LANDED figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    # ------------------------------------------------------
    # Held contrasts inside the present limbs, standing
    # missing in the same form
    # ------------------------------------------------------

    def test_r16_11_held_contrast_six_digit_paren_no_colon(self):
        """Held contrast: (123456) Board tally in dot form."""
        report = self._alone(_dot_form("(123456) ", "Board tally"))
        self._assert_missing(report)

    def test_r16_11_held_contrast_one_digit_paren_no_colon(self):
        """Held contrast: (1) Board tally in dot form."""
        report = self._alone(_dot_form("(1) ", "Board tally"))
        self._assert_missing(report)

    def test_r16_11_held_contrast_six_digit_bracket_no_colon(self):
        """Held contrast: [123456] Board tally in dot form."""
        report = self._alone(_dot_form("[123456] ", "Board tally"))
        self._assert_missing(report)

    def test_r16_11_held_short_paren_marker_colon(self):
        """Held marker form: (1) Board tally with its colon."""
        report = self._alone("(1) " + _bad("Board tally"))
        self._assert_governed(report)

    def test_r16_11_held_bracket_roman_marker_colon(self):
        """Held marker form: [iv] Board tally with its colon."""
        report = self._alone("[iv] " + _bad("Board tally"))
        self._assert_governed(report)

    # ------------------------------------------------------
    # Closure, colon condition and prose controls
    # ------------------------------------------------------

    def test_r16_11_closure_prose_run_past_tally_colon_close(self):
        """Closure control: a run past tally closing on a colon."""
        line = ("Board tally, and its figures stand here: LANDED "
                "figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_11_closure_run_past_tally_dot_close(self):
        """Closure control: a run past tally closing on a dot."""
        line = ("Board tally and its figures stand here. LANDED "
                "figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_11_residual_numbered_tally_no_colon(self):
        """Residual control: a numbered tally head, no colon."""
        line = ("1. Board tally items checked stand here. LANDED "
                "figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_11_residual_numbered_trace_summary_no_colon(self):
        """Residual control: numbered trace summary, no colon."""
        line = ("1. Trace summary items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_11_colon_plain_trace_for_step_with_colon(self):
        """Colon control: plain trace for step, its colon."""
        line = ("Trace for step 2: items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_governed(self._alone(line))

    def test_r16_11_prose_sentence_closing_on_tally_governed(self):
        """Folded control: a prose run closing on tally stands."""
        report = self._alone(PROSE_SENTENCE_CLOSING_ON_TALLY)
        self._assert_governed(report)

    def test_r16_11_golden_board_tally_member_line(self):
        """Golden control: the board tally member line."""
        self._assert_missing(self._alone(GOLDEN_BOARD_LINE))

    def test_r16_11_golden_closing_prose_line(self):
        """Golden control: the closing board tally prose line."""
        self._assert_missing(self._alone(GOLDEN_CLOSING_LINE))

    def test_r16_11_prose_fragment_no_head(self):
        """Prose control: a fragment with no tally head."""
        self._assert_missing(self._alone(PROSE_FRAGMENT))

    def test_r16_11_trace_for_step_alphanumeric_missing(self):
        """Boundary control: Trace for step 2a stands missing."""
        line = ("Trace for step 2a: items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    # ------------------------------------------------------
    # Held cured heads of Unit 1 and the earlier passes
    # ------------------------------------------------------

    def test_r16_11_held_unit1_fused_head(self):
        """Held head of R16-11-01: Step2tally alone."""
        self._assert_governed(self._alone(_bad("Step2tally")))

    def test_r16_11_held_unit1_colon_inside_head(self):
        """Held head of R16-11-01: Board: tally alone."""
        self._assert_governed(self._alone(_bad("Board: tally")))

    def test_r16_11_held_unit1_abbreviation_dot_head(self):
        """Held head of R16-11-01: the abbreviation dot head."""
        self._assert_governed(
            self._alone(_bad("Board tally dept. tally")))

    def test_r16_11_held_unit1_dot_marker_head(self):
        """Held head of R16-11-01: A1. Board tally alone."""
        self._assert_governed(self._alone("A1. " + _bad("Board tally")))

    def test_r16_11_held_board_tally_head(self):
        """Held head of R16-7-03: Board tally alone."""
        self._assert_governed(self._alone(_bad("Board tally")))

    def test_r16_11_held_trace_summary_head(self):
        """Held head of R16-7-03: Trace summary alone."""
        self._assert_governed(self._alone(_bad("Trace summary")))

    # ------------------------------------------------------
    # Read and absent controls, byte for byte
    # ------------------------------------------------------

    def test_r16_11_held_read_control_byte_for_byte(self):
        """Held control: the gate records read, 8 LANDED of 8."""
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_11_held_absent_feeder_byte_for_byte(self):
        """Held control: no gate records, genuinely absent."""
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
