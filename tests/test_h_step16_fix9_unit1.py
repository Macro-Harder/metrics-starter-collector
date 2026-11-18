"""Step 16 fix pass 9 unit 1 tests: the Q-4 tally head unit.

Pinning tests for register items R16-9-01 and R16-9-02
(Medium, B9-01 and B9-02) of Step 16 round 9. The
governing rule of the pass, in its extended form: a
piece not read in full, for whatever reason, is not
read, and its converse: a piece that is no feeder flips
nothing.

R16-9-01: a malformed tally statement under a head
carrying a mark or a marker form the fix pass 8 word
pattern and marker test do not reach takes Q-4 missing
under the no feeder record code in the alone position
and drops the step unnamed in the beside position,
while its counted sibling under the same head counts,
because _trace_candidates counts the numeric tally
pattern with no head test at all. The nine driven heads
are an underscore head, a slash head, a hyphenated
trace summary head, a comma trace summary head, an
apostrophe head, a double hyphen head, a parenthesised
numbered form, a bracket numbered form and a numbered
form with no space after its marker. Locus:
derivation_core.py, _tally_statement_head, against
_trace_candidates.

R16-9-02: a prose line whose opening run of plain words
passes through the tally words and closes later takes
Q-4 present but not derivable, standing in no tally
statement form, because the head test matches its head
patterns as a prefix only and its trace for step limb
carries no colon condition. The five driven forms are
the golden closing prose line with its numbered marker
removed, a run past the word tally, a run past the
words trace summary, a run closing past a first word
tally, and a numbered trace for step instruction line.
The cure these tests pin: the head test stands on the
counted pattern reach in both directions, a head being
a run that closes with the tally words, the trace
summary words or the trace for step form, the trace
for step limb and every numbered marker limb standing
under the colon condition of fix pass 8 Unit 1, so a
malformed tally line under any counted head stands as
a feeder statement in a form the row cannot parse, in
the alone position taking the governed not derivable
form naming the step and the feeder piece, and in the
beside position naming the step uncounted in the
present row coverage, in gate records and gate rulings
alike, while a line whose opening run does not close
with the tally words flips nothing.

Held controls stand pinned beside the defect forms:
the counted sibling of every new head, every head form
cured by fix pass 7 Unit 2 and fix pass 8 Unit 1, the
settled Gate tally, Trace tally and Trace for step
heads, the golden prose lines flipping nothing, a
malformed tally fragment in prose position opening
with no tally statement head flipping nothing, the
numbered no colon residuals standing outside the scan,
the step companion converse forms, the same step seam,
the read control and the genuinely absent missing form.

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
from tests.test_h_step16_fix6_unit3 import (
    TALLY_B6_BAD, TALLY_C6_A_BAD, TALLY_C6_B_BAD)
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
UNNUMBERED_CLOSING = (
    "Record the board tally and this verdict in the "
    "closing entry: member 1 RECYCLE for roster closure "
    "only, its three completions LANDED and its stated "
    "approval condition satisfied; member 2 approve "
    "with notes, six notes binding.")
TWENTY_WORD = " ".join(["Alpha"] * 19 + ["tally"])

NEW_HEADS = (
    "Step_2 tally",
    "Step/2 tally",
    "Trace-summary",
    "Trace, summary",
    "Board's tally",
    "Step--2 tally",
)


def _assert_no_absence(test, block):
    test.assertNotIn("no first trace record stands", block)
    test.assertNotIn("no feeder record for the metric exists",
                     block)
    test.assertNotIn("no-feeder-record", block)


class TestStep16Fix9Unit1(FixtureTestCase):

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
    # Defect forms, R16-9-01, marked heads alone
    # ------------------------------------------------------

    def test_r16_9_01_underscore_head_alone(self):
        """B9-01 underscore head: Step_2 tally alone."""
        report = self._run(self._alone_files(_bad("Step_2 tally")))
        self._assert_alone_cured(report)

    def test_r16_9_01_slash_head_alone(self):
        """B9-01 slash head: Step/2 tally alone."""
        report = self._run(self._alone_files(_bad("Step/2 tally")))
        self._assert_alone_cured(report)

    def test_r16_9_01_hyphenated_trace_summary_alone(self):
        """B9-01 hyphenated trace summary head alone."""
        report = self._run(self._alone_files(_bad("Trace-summary")))
        self._assert_alone_cured(report)

    def test_r16_9_01_comma_trace_summary_alone(self):
        """B9-01 comma trace summary head alone."""
        report = self._run(self._alone_files(_bad("Trace, summary")))
        self._assert_alone_cured(report)

    def test_r16_9_01_apostrophe_head_alone(self):
        """B9-01 apostrophe head: Board's tally alone."""
        report = self._run(self._alone_files(_bad("Board's tally")))
        self._assert_alone_cured(report)

    def test_r16_9_01_double_hyphen_head_alone(self):
        """B9-01 double hyphen head: Step--2 tally alone."""
        report = self._run(self._alone_files(_bad("Step--2 tally")))
        self._assert_alone_cured(report)

    def test_r16_9_01_parenthesised_numbered_head_alone(self):
        """B9-01 parenthesised form: (1) Board tally alone."""
        report = self._run(
            self._alone_files("(1) " + _bad("Board tally")))
        self._assert_alone_cured(report)

    def test_r16_9_01_bracket_numbered_head_alone(self):
        """B9-01 bracket form: [1] Board tally alone."""
        report = self._run(
            self._alone_files("[1] " + _bad("Board tally")))
        self._assert_alone_cured(report)

    def test_r16_9_01_numbered_no_space_head_alone(self):
        """B9-01 spaceless numbered form: 1.Board tally alone."""
        report = self._run(
            self._alone_files("1." + _bad("Board tally")))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Defect forms, R16-9-01, beside and gate ruling forms
    # ------------------------------------------------------

    def test_r16_9_01_underscore_head_beside_counted(self):
        """B9-01 underscore head beside form: step dropped."""
        report = self._run(self._beside_files(_bad("Step_2 tally")))
        self._assert_beside_cured(report)

    def test_r16_9_01_underscore_head_gate_ruling_alone(self):
        """B9-01 gate ruling form: an underscore malformed tally."""
        report = self._run(
            self._alone_files(_bad("Step_2 tally"), ruling=True))
        self._assert_alone_cured(report, path=RULING_2)

    # ------------------------------------------------------
    # Defect forms, R16-9-02, prose runs flipping nothing
    # ------------------------------------------------------

    def test_r16_9_02_unnumbered_closing_line_flips_nothing(self):
        """B9-02 golden closing line, its marker removed."""
        report = self._run(self._alone_files(UNNUMBERED_CLOSING))
        self._assert_missing(report)

    def test_r16_9_02_run_past_tally_flips_nothing(self):
        """B9-02 a run passing through tally, closing later."""
        line = ("Board tally and its figures stand here. LANDED "
                "figures stand here, no counts stated")
        report = self._run(self._alone_files(line))
        self._assert_missing(report)

    def test_r16_9_02_run_past_trace_summary_flips_nothing(self):
        """B9-02 a run passing through trace summary words."""
        line = ("Trace summary and discussion stand here. LANDED "
                "figures stand here, no counts stated")
        report = self._run(self._alone_files(line))
        self._assert_missing(report)

    def test_r16_9_02_tally_first_word_run_flips_nothing(self):
        """B9-02 a run opening on tally and closing later."""
        line = ("Tally of the round stands here. LANDED figures "
                "stand here, no counts stated")
        report = self._run(self._alone_files(line))
        self._assert_missing(report)

    def test_r16_9_02_numbered_trace_for_step_flips_nothing(self):
        """B9-02 a numbered trace for step instruction line."""
        line = ("1. Trace for step 2 items checked stand here in "
                "the entry: LANDED figures stand here, no counts "
                "stated")
        report = self._run(self._alone_files(line))
        self._assert_missing(report)

    def test_r16_9_02_numbered_trace_for_step_no_colon(self):
        """B9-02 numbered trace for step, no colon at its head."""
        line = ("1. Trace for step 2 items checked stand here. "
                "LANDED figures stand here, no counts stated")
        report = self._run(self._alone_files(line))
        self._assert_missing(report)

    # ------------------------------------------------------
    # Counted sibling controls of the new heads
    # ------------------------------------------------------

    def test_r16_9_01_underscore_head_counted_control(self):
        """Counted control: the underscore head counted form."""
        report = self._run(self._alone_files(_read("Step_2 tally")))
        self._assert_counted(report)

    def test_r16_9_01_slash_head_counted_control(self):
        """Counted control: the slash head counted form."""
        report = self._run(self._alone_files(_read("Step/2 tally")))
        self._assert_counted(report)

    def test_r16_9_01_hyphenated_trace_summary_counted_control(self):
        """Counted control: hyphenated trace summary counted."""
        report = self._run(self._alone_files(_read("Trace-summary")))
        self._assert_counted(report)

    def test_r16_9_01_comma_trace_summary_counted_control(self):
        """Counted control: comma trace summary counted form."""
        report = self._run(self._alone_files(_read("Trace, summary")))
        self._assert_counted(report)

    def test_r16_9_01_apostrophe_head_counted_control(self):
        """Counted control: the apostrophe head counted form."""
        report = self._run(self._alone_files(_read("Board's tally")))
        self._assert_counted(report)

    def test_r16_9_01_double_hyphen_head_counted_control(self):
        """Counted control: the double hyphen head counted."""
        report = self._run(self._alone_files(_read("Step--2 tally")))
        self._assert_counted(report)

    def test_r16_9_01_parenthesised_numbered_counted_control(self):
        """Counted control: the parenthesised counted form."""
        report = self._run(
            self._alone_files("(1) " + _read("Board tally")))
        self._assert_counted(report)

    def test_r16_9_01_bracket_numbered_counted_control(self):
        """Counted control: the bracket numbered counted form."""
        report = self._run(
            self._alone_files("[1] " + _read("Board tally")))
        self._assert_counted(report)

    def test_r16_9_01_numbered_no_space_counted_control(self):
        """Counted control: the spaceless numbered counted."""
        report = self._run(
            self._alone_files("1." + _read("Board tally")))
        self._assert_counted(report)

    # ------------------------------------------------------
    # Held controls, heads cured by fix passes 7 and 8
    # ------------------------------------------------------

    def test_r16_9_held_five_word_tally_head_alone(self):
        """Held control: the five word head stands cured."""
        report = self._run(self._alone_files(_bad(FIVE_WORD)))
        self._assert_alone_cured(report)

    def test_r16_9_held_six_word_tally_head_alone(self):
        """Held control: the six word head stands cured."""
        report = self._run(self._alone_files(_bad(SIX_WORD)))
        self._assert_alone_cured(report)

    def test_r16_9_held_review_tally_head_alone(self):
        """Held control: the gate record review head cured."""
        report = self._run(self._alone_files(_bad(REVIEW_HEAD)))
        self._assert_alone_cured(report)

    def test_r16_9_held_long_trace_summary_head_alone(self):
        """Held control: the long trace summary head cured."""
        report = self._run(self._alone_files(_bad(LONG_SUMMARY)))
        self._assert_alone_cured(report)

    def test_r16_9_held_hyphenated_tally_head_alone(self):
        """Held control: the hyphenated Step-2 head cured."""
        report = self._run(self._alone_files(_bad("Step-2 tally")))
        self._assert_alone_cured(report)

    def test_r16_9_held_comma_tally_head_alone(self):
        """Held control: the comma head Board, tally cured."""
        report = self._run(self._alone_files(_bad("Board, tally")))
        self._assert_alone_cured(report)

    def test_r16_9_held_numbered_list_tally_head_alone(self):
        """Held control: the numbered list form stands cured."""
        report = self._run(
            self._alone_files("1. " + _bad("Board tally")))
        self._assert_alone_cured(report)

    def test_r16_9_held_board_tally_head_alone(self):
        """Held control: the charged Board tally head alone."""
        report = self._run(self._alone_files(_bad("Board tally")))
        self._assert_alone_cured(report)

    def test_r16_9_held_trace_summary_head_alone(self):
        """Held control: the charged Trace summary head alone."""
        report = self._run(self._alone_files(_bad("Trace summary")))
        self._assert_alone_cured(report)

    def test_r16_9_held_settled_gate_tally_alone(self):
        """Held control: the settled Gate tally form alone."""
        report = self._run(self._alone_files(TALLY_B6_BAD))
        self._assert_alone_cured(report)

    def test_r16_9_held_settled_trace_tally_for_step_alone(self):
        """Held control: the settled Trace tally for step form."""
        report = self._run(self._alone_files(TALLY_C6_B_BAD))
        self._assert_alone_cured(report)

    def test_r16_9_held_settled_trace_for_step_alone(self):
        """Held control: the settled Trace for step form alone."""
        report = self._run(self._alone_files(TALLY_C6_A_BAD))
        self._assert_alone_cured(report)

    def test_r16_9_held_six_word_head_gate_ruling_alone(self):
        """Held control: a six word malformed tally, ruling."""
        report = self._run(
            self._alone_files(_bad(SIX_WORD), ruling=True))
        self._assert_alone_cured(report, path=RULING_2)

    def test_r16_9_held_twenty_word_head_alone(self):
        """Held control: a twenty word plain head governed."""
        report = self._run(self._alone_files(_bad(TWENTY_WORD)))
        self._assert_alone_cured(report)

    def test_r16_9_held_tab_separated_head_alone(self):
        """Held control: a tab separated head stands governed."""
        line = ("Board\ttally: items checked stand here. LANDED "
                "figures stand here, no counts stated")
        report = self._run(self._alone_files(line))
        self._assert_alone_cured(report)

    def test_r16_9_held_numbered_paren_marker_colon(self):
        """Held control: the 1) marker form with its colon."""
        report = self._run(
            self._alone_files("1) " + _bad("Board tally")))
        self._assert_alone_cured(report)

    def test_r16_9_held_numbered_hyphen_head_colon(self):
        """Held control: a numbered hyphenated head, colon."""
        report = self._run(
            self._alone_files("1. " + _bad("Step-2 tally")))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Held controls, prose positions flipping nothing
    # ------------------------------------------------------

    def test_r16_9_held_golden_board_tally_member_line(self):
        """Held golden form: the board tally member line."""
        report = self._run(self._alone_files(GOLDEN_BOARD_LINE))
        self._assert_missing(report)

    def test_r16_9_held_golden_closing_prose_line(self):
        """Held golden form: the closing board tally prose line."""
        report = self._run(self._alone_files(GOLDEN_CLOSING_LINE))
        self._assert_missing(report)

    def test_r16_9_held_prose_fragment_no_head(self):
        """Held prose position: a fragment with no tally head."""
        report = self._run(self._alone_files(PROSE_FRAGMENT))
        self._assert_missing(report)

    def test_r16_9_held_numbered_no_colon_residual(self):
        """Held residual: a numbered tally head, no colon."""
        line = ("1. Board tally items checked stand here. LANDED "
                "figures stand here, no counts stated")
        report = self._run(self._alone_files(line))
        self._assert_missing(report)

    def test_r16_9_held_numbered_trace_summary_no_colon(self):
        """Held residual: numbered trace summary, no colon."""
        line = ("1. Trace summary items checked stand here. "
                "LANDED figures stand here, no counts stated")
        report = self._run(self._alone_files(line))
        self._assert_missing(report)

    def test_r16_9_held_companion_malformed_tally_converse(self):
        """Held converse: a malformed tally in a step companion."""
        files = _clean_files()
        files[COMPANION_PATH] = (
            "# Step 2 notes\n\n" + _bad(SIX_WORD) + "\n")
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)

    def test_r16_9_held_same_step_seam(self):
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

    def test_r16_9_held_read_control_byte_for_byte(self):
        """Held control: the gate records read, 8 LANDED of 8."""
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_9_held_absent_feeder_byte_for_byte(self):
        """Held control: no gate records, genuinely absent."""
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
