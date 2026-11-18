"""Step 16 fix pass 10 unit 1 tests: the Q-4 tally head unit.

Pinning tests for register item R16-10-01 (Medium,
B10-01) of Step 16 round 10. The governing rule of the
pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-10-01: a malformed tally statement under a head
carrying a closing join, a head word mark, or a marker
shape the fix pass 9 word pattern, trace summary join
pattern and marker test do not reach takes Q-4 missing
under the no feeder record code in the alone position
and drops the step unnamed in the beside position,
while its counted sibling under the same head counts,
because _trace_candidates counts the numeric tally
pattern with no head test at all. The seventeen driven
heads stand in three families: closing joins past the
cured joins (Trace,summary; Trace/summary;
Trace_summary; Trace--summary; Trace - summary), head
words carrying marks past the cured word pattern
(Step+2, Step=2, Step#2, Step%2, Board& tally heads, a
non ASCII head, Board- tally, Board tally ,), and
marker shapes past the cured marker test (1:, (i), A.,
1- numbered forms, each numbered form carrying its
closing colon). Locus: derivation_core.py,
_tally_statement_head, against _trace_candidates.

The cure these tests pin is the general form of the
counted reach: a head is whatever opening run of the
line, behind whatever list marker the line carries,
closes with the tally words, the word tally, the words
trace summary in whatever join the run carries them,
or the trace for step form under its colon condition,
with no test on the marks the words of the run carry,
because the counted pattern itself carries no such
test. The run closure limb and the numbered colon
condition stand exactly as fix pass 9 left them: a run
that passes through the tally words and closes on
other words is no head, and a head behind a numbered
marker counts only where a colon closes the run.

Held controls stand pinned beside the defect forms:
the counted sibling of every new head, every head form
cured by fix passes 7, 8 and 9 as the round 10 register
enumerates them, the fresh governed heads of the round
10 drives, the golden prose lines flipping nothing, a
malformed tally fragment in prose position opening
with no tally statement head flipping nothing, the
prose sentence whose opening run closes on the word
tally standing governed in its folded form, the
numbered no colon residuals standing outside the scan,
the trace for step colon condition in both directions
with the spaced colon form standing governed, the read
control and the genuinely absent missing form.

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
PROSE_FRAGMENT = (
    "A malformed fragment stands in prose position here. "
    "LANDED figures stand here, no counts stated")
PROSE_SENTENCE_CLOSING_ON_TALLY = (
    "Record the board tally. LANDED figures stand "
    "here, no counts stated")
SPACED_HYPHEN_HEAD = "Trace - summary"
SPACED_COMMA_HEAD = "Board tally ,"

DEFECT_HEADS = (
    "Trace,summary",
    "Trace/summary",
    "Trace_summary",
    "Trace--summary",
    SPACED_HYPHEN_HEAD,
    "Step+2 tally",
    "Step=2 tally",
    "Step#2 tally",
    "Step%2 tally",
    "Board& tally",
    "Böard tally",
    "Board- tally",
    SPACED_COMMA_HEAD,
)

MARKER_DEFECTS = (
    ("colon", "1: "),
    ("roman_parenthesis", "(i) "),
    ("letter", "A. "),
    ("hyphen", "1- "),
)


def _assert_no_absence(test, block):
    test.assertNotIn("no first trace record stands", block)
    test.assertNotIn("no feeder record for the metric exists",
                     block)
    test.assertNotIn("no-feeder-record", block)


class TestStep16Fix10Unit1(FixtureTestCase):

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

    def _alone(self, line, ruling=False):
        return self._run(self._alone_files(line, ruling=ruling))

    # ------------------------------------------------------
    # Defect forms, R16-10-01, closing joins alone
    # ------------------------------------------------------

    def test_r16_10_01_trace_summary_comma_no_space_alone(self):
        """B10-01 closing join: Trace,summary alone."""
        report = self._alone(_bad("Trace,summary"))
        self._assert_alone_cured(report)

    def test_r16_10_01_trace_summary_slash_join_alone(self):
        """B10-01 closing join: Trace/summary alone."""
        report = self._alone(_bad("Trace/summary"))
        self._assert_alone_cured(report)

    def test_r16_10_01_trace_summary_underscore_join_alone(self):
        """B10-01 closing join: Trace_summary alone."""
        report = self._alone(_bad("Trace_summary"))
        self._assert_alone_cured(report)

    def test_r16_10_01_trace_summary_double_hyphen_join_alone(self):
        """B10-01 closing join: Trace--summary alone."""
        report = self._alone(_bad("Trace--summary"))
        self._assert_alone_cured(report)

    def test_r16_10_01_trace_summary_spaced_hyphen_join_alone(self):
        """B10-01 closing join: Trace - summary alone."""
        report = self._alone(_bad(SPACED_HYPHEN_HEAD))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Defect forms, R16-10-01, head word marks alone
    # ------------------------------------------------------

    def test_r16_10_01_plus_head_alone(self):
        """B10-01 word mark: Step+2 tally alone."""
        report = self._alone(_bad("Step+2 tally"))
        self._assert_alone_cured(report)

    def test_r16_10_01_equals_head_alone(self):
        """B10-01 word mark: Step=2 tally alone."""
        report = self._alone(_bad("Step=2 tally"))
        self._assert_alone_cured(report)

    def test_r16_10_01_hash_head_alone(self):
        """B10-01 word mark: Step#2 tally alone."""
        report = self._alone(_bad("Step#2 tally"))
        self._assert_alone_cured(report)

    def test_r16_10_01_percent_head_alone(self):
        """B10-01 word mark: Step%2 tally alone."""
        report = self._alone(_bad("Step%2 tally"))
        self._assert_alone_cured(report)

    def test_r16_10_01_ampersand_head_alone(self):
        """B10-01 word mark: Board& tally alone."""
        report = self._alone(_bad("Board& tally"))
        self._assert_alone_cured(report)

    def test_r16_10_01_non_ascii_head_alone(self):
        """B10-01 word mark: a non ASCII head alone."""
        report = self._alone(_bad("Böard tally"))
        self._assert_alone_cured(report)

    def test_r16_10_01_trailing_hyphen_head_alone(self):
        """B10-01 word mark: Board- tally alone."""
        report = self._alone(_bad("Board- tally"))
        self._assert_alone_cured(report)

    def test_r16_10_01_spaced_comma_head_alone(self):
        """B10-01 word mark: Board tally , alone."""
        report = self._alone(_bad(SPACED_COMMA_HEAD))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Defect forms, R16-10-01, marker shapes alone
    # ------------------------------------------------------

    def test_r16_10_01_colon_marker_alone(self):
        """B10-01 marker shape: 1: Board tally alone."""
        report = self._alone("1: " + _bad("Board tally"))
        self._assert_alone_cured(report)

    def test_r16_10_01_roman_parenthesis_marker_alone(self):
        """B10-01 marker shape: (i) Board tally alone."""
        report = self._alone("(i) " + _bad("Board tally"))
        self._assert_alone_cured(report)

    def test_r16_10_01_letter_marker_alone(self):
        """B10-01 marker shape: A. Board tally alone."""
        report = self._alone("A. " + _bad("Board tally"))
        self._assert_alone_cured(report)

    def test_r16_10_01_hyphen_marker_alone(self):
        """B10-01 marker shape: 1- Board tally alone."""
        report = self._alone("1- " + _bad("Board tally"))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Defect forms, R16-10-01, beside and gate ruling forms
    # ------------------------------------------------------

    def test_r16_10_01_trace_summary_slash_beside_counted(self):
        """B10-01 beside form: the slash join step dropped."""
        report = self._run(self._beside_files(_bad("Trace/summary")))
        self._assert_beside_cured(report)

    def test_r16_10_01_plus_head_gate_ruling_alone(self):
        """B10-01 gate ruling form: a plus head malformed tally."""
        report = self._alone(_bad("Step+2 tally"), ruling=True)
        self._assert_alone_cured(report, path=RULING_2)

    # ------------------------------------------------------
    # Counted sibling controls of the seventeen heads
    # ------------------------------------------------------

    def test_r16_10_01_trace_summary_comma_no_space_counted(self):
        """Counted control: Trace,summary counted form."""
        report = self._alone(_read("Trace,summary"))
        self._assert_counted(report)

    def test_r16_10_01_trace_summary_slash_join_counted(self):
        """Counted control: Trace/summary counted form."""
        report = self._alone(_read("Trace/summary"))
        self._assert_counted(report)

    def test_r16_10_01_trace_summary_underscore_join_counted(self):
        """Counted control: Trace_summary counted form."""
        report = self._alone(_read("Trace_summary"))
        self._assert_counted(report)

    def test_r16_10_01_trace_summary_double_hyphen_join_counted(self):
        """Counted control: Trace--summary counted form."""
        report = self._alone(_read("Trace--summary"))
        self._assert_counted(report)

    def test_r16_10_01_trace_summary_spaced_hyphen_join_counted(self):
        """Counted control: Trace - summary counted form."""
        report = self._alone(_read(SPACED_HYPHEN_HEAD))
        self._assert_counted(report)

    def test_r16_10_01_plus_head_counted(self):
        """Counted control: Step+2 tally counted form."""
        report = self._alone(_read("Step+2 tally"))
        self._assert_counted(report)

    def test_r16_10_01_equals_head_counted(self):
        """Counted control: Step=2 tally counted form."""
        report = self._alone(_read("Step=2 tally"))
        self._assert_counted(report)

    def test_r16_10_01_hash_head_counted(self):
        """Counted control: Step#2 tally counted form."""
        report = self._alone(_read("Step#2 tally"))
        self._assert_counted(report)

    def test_r16_10_01_percent_head_counted(self):
        """Counted control: Step%2 tally counted form."""
        report = self._alone(_read("Step%2 tally"))
        self._assert_counted(report)

    def test_r16_10_01_ampersand_head_counted(self):
        """Counted control: Board& tally counted form."""
        report = self._alone(_read("Board& tally"))
        self._assert_counted(report)

    def test_r16_10_01_non_ascii_head_counted(self):
        """Counted control: the non ASCII counted form."""
        report = self._alone(_read("Böard tally"))
        self._assert_counted(report)

    def test_r16_10_01_trailing_hyphen_head_counted(self):
        """Counted control: Board- tally counted form."""
        report = self._alone(_read("Board- tally"))
        self._assert_counted(report)

    def test_r16_10_01_spaced_comma_head_counted(self):
        """Counted control: Board tally , counted form."""
        report = self._alone(_read(SPACED_COMMA_HEAD))
        self._assert_counted(report)

    def test_r16_10_01_colon_marker_counted(self):
        """Counted control: the colon marker counted form."""
        report = self._alone("1: " + _read("Board tally"))
        self._assert_counted(report)

    def test_r16_10_01_roman_parenthesis_marker_counted(self):
        """Counted control: the roman marker counted form."""
        report = self._alone("(i) " + _read("Board tally"))
        self._assert_counted(report)

    def test_r16_10_01_letter_marker_counted(self):
        """Counted control: the letter marker counted form."""
        report = self._alone("A. " + _read("Board tally"))
        self._assert_counted(report)

    def test_r16_10_01_hyphen_marker_counted(self):
        """Counted control: the hyphen marker counted form."""
        report = self._alone("1- " + _read("Board tally"))
        self._assert_counted(report)

    # ------------------------------------------------------
    # Cured controls of the round 10 drives
    # ------------------------------------------------------

    def test_r16_10_cured_mixed_marks_head(self):
        """Cured control: Step_2/3 tally, counted and bad."""
        self._assert_counted(self._alone(_read("Step_2/3 tally")))
        self._assert_alone_cured(self._alone(_bad("Step_2/3 tally")))

    def test_r16_10_cured_apostrophe_hyphen_head(self):
        """Cured control: Board's-own tally, counted and bad."""
        self._assert_counted(self._alone(_read("Board's-own tally")))
        self._assert_alone_cured(
            self._alone(_bad("Board's-own tally")))

    def test_r16_10_cured_upper_case_head(self):
        """Cured control: BOARD TALLY, counted and bad."""
        self._assert_counted(self._alone(_read("BOARD TALLY")))
        self._assert_alone_cured(self._alone(_bad("BOARD TALLY")))

    def test_r16_10_cured_spaceless_paren_marker(self):
        """Cured control: 1)Board tally, counted and bad."""
        self._assert_counted(self._alone("1)" + _read("Board tally")))
        self._assert_alone_cured(
            self._alone("1)" + _bad("Board tally")))

    def test_r16_10_cured_spaceless_bracket_marker(self):
        """Cured control: [1]Board tally, counted and bad."""
        self._assert_counted(
            self._alone("[1]" + _read("Board tally")))
        self._assert_alone_cured(
            self._alone("[1]" + _bad("Board tally")))

    def test_r16_10_cured_semicolon_closing_board(self):
        """Cured control: Board tally closing at a semicolon."""
        line = ("Board tally; items checked stand here. LANDED "
                "figures stand here, no counts stated")
        self._assert_alone_cured(self._alone(line))

    def test_r16_10_cured_semicolon_closing_trace_summary(self):
        """Cured control: Trace summary closing at a semicolon."""
        line = ("Trace summary; items checked stand here. LANDED "
                "figures stand here, no counts stated")
        self._assert_alone_cured(self._alone(line))

    # ------------------------------------------------------
    # Closure, colon condition and prose controls
    # ------------------------------------------------------

    def test_r16_10_closure_prose_run_past_tally_colon_close(self):
        """Closure control: a run past tally closing on a colon."""
        line = ("Board tally, and its figures stand here: LANDED "
                "figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_10_closure_plain_trace_for_step_colon_after_items(self):
        """Closure control: trace for step colon after items."""
        line = ("Trace for step 2 items checked stand here: "
                "LANDED figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_10_colon_numbered_trace_for_step_no_colon(self):
        """Colon control: numbered trace for step, no colon."""
        line = ("1. Trace for step 2 items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_10_colon_numbered_trace_for_step_with_colon(self):
        """Colon control: numbered trace for step, its colon."""
        line = ("1. Trace for step 2: items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_alone_cured(self._alone(line))

    def test_r16_10_colon_plain_trace_for_step_with_colon(self):
        """Colon control: plain trace for step, its colon."""
        line = ("Trace for step 2: items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_alone_cured(self._alone(line))

    def test_r16_10_colon_plain_trace_for_step_spaced_colon(self):
        """Colon control: trace for step, a spaced colon."""
        line = ("Trace for step 2 : items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_alone_cured(self._alone(line))

    def test_r16_10_prose_sentence_closing_on_tally_governed(self):
        """Folded control: a prose run closing on tally stands."""
        report = self._alone(PROSE_SENTENCE_CLOSING_ON_TALLY)
        self._assert_alone_cured(report)

    def test_r16_10_residual_numbered_tally_no_colon(self):
        """Residual control: a numbered tally head, no colon."""
        line = ("1. Board tally items checked stand here. LANDED "
                "figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_10_residual_numbered_trace_summary_no_colon(self):
        """Residual control: numbered trace summary, no colon."""
        line = ("1. Trace summary items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_10_golden_board_tally_member_line(self):
        """Golden control: the board tally member line."""
        self._assert_missing(self._alone(GOLDEN_BOARD_LINE))

    def test_r16_10_golden_closing_prose_line(self):
        """Golden control: the closing board tally prose line."""
        self._assert_missing(self._alone(GOLDEN_CLOSING_LINE))

    def test_r16_10_prose_fragment_no_head(self):
        """Prose control: a fragment with no tally head."""
        self._assert_missing(self._alone(PROSE_FRAGMENT))

    # ------------------------------------------------------
    # Held cured heads of fix passes 7, 8 and 9
    # ------------------------------------------------------

    def test_r16_10_held_board_tally_head(self):
        """Held head of R16-7-03: Board tally alone."""
        self._assert_alone_cured(self._alone(_bad("Board tally")))

    def test_r16_10_held_step_2_tally_head(self):
        """Held head of R16-7-03: Step 2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step 2 tally")))

    def test_r16_10_held_tally_head(self):
        """Held head of R16-7-03: Tally alone."""
        self._assert_alone_cured(self._alone(_bad("Tally")))

    def test_r16_10_held_gate_record_tally_head(self):
        """Held head of R16-7-03: Gate record tally alone."""
        self._assert_alone_cured(
            self._alone(_bad("Gate record tally")))

    def test_r16_10_held_trace_summary_head(self):
        """Held head of R16-7-03: Trace summary alone."""
        self._assert_alone_cured(self._alone(_bad("Trace summary")))

    def test_r16_10_held_settled_gate_tally(self):
        """Held settled head: Gate tally alone."""
        self._assert_alone_cured(self._alone(TALLY_B6_BAD))

    def test_r16_10_held_settled_trace_for_step(self):
        """Held settled head: Trace for step 2 alone."""
        self._assert_alone_cured(self._alone(TALLY_C6_A_BAD))

    def test_r16_10_held_settled_trace_tally_for_step(self):
        """Held settled head: Trace tally for step 2 alone."""
        self._assert_alone_cured(self._alone(TALLY_C6_B_BAD))

    def test_r16_10_held_six_word_head(self):
        """Held head of R16-8-01: the six word head alone."""
        self._assert_alone_cured(self._alone(_bad(SIX_WORD)))

    def test_r16_10_held_review_head(self):
        """Held head of R16-8-01: the review head alone."""
        self._assert_alone_cured(self._alone(_bad(REVIEW_HEAD)))

    def test_r16_10_held_long_trace_summary_head(self):
        """Held head of R16-8-01: the long trace summary head."""
        self._assert_alone_cured(self._alone(_bad(LONG_SUMMARY)))

    def test_r16_10_held_numbered_list_board_tally(self):
        """Held head of R16-8-01: 1. Board tally alone."""
        self._assert_alone_cured(
            self._alone("1. " + _bad("Board tally")))

    def test_r16_10_held_hyphenated_step_head(self):
        """Held head of R16-8-01: Step-2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step-2 tally")))

    def test_r16_10_held_comma_board_head(self):
        """Held head of R16-8-01: Board, tally alone."""
        self._assert_alone_cured(self._alone(_bad("Board, tally")))

    def test_r16_10_held_fix9_underscore_head(self):
        """Held head of R16-9-01: Step_2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step_2 tally")))

    def test_r16_10_held_fix9_slash_head(self):
        """Held head of R16-9-01: Step/2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step/2 tally")))

    def test_r16_10_held_fix9_hyphenated_trace_summary(self):
        """Held head of R16-9-01: Trace-summary alone."""
        self._assert_alone_cured(self._alone(_bad("Trace-summary")))

    def test_r16_10_held_fix9_comma_trace_summary(self):
        """Held head of R16-9-01: Trace, summary alone."""
        self._assert_alone_cured(
            self._alone(_bad("Trace, summary")))

    def test_r16_10_held_fix9_apostrophe_head(self):
        """Held head of R16-9-01: Board's tally alone."""
        self._assert_alone_cured(self._alone(_bad("Board's tally")))

    def test_r16_10_held_fix9_double_hyphen_head(self):
        """Held head of R16-9-01: Step--2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step--2 tally")))

    def test_r16_10_held_fix9_parenthesised_numbered(self):
        """Held head of R16-9-01: (1) Board tally alone."""
        self._assert_alone_cured(
            self._alone("(1) " + _bad("Board tally")))

    def test_r16_10_held_fix9_bracket_numbered(self):
        """Held head of R16-9-01: [1] Board tally alone."""
        self._assert_alone_cured(
            self._alone("[1] " + _bad("Board tally")))

    def test_r16_10_held_fix9_numbered_no_space(self):
        """Held head of R16-9-01: 1.Board tally alone."""
        self._assert_alone_cured(
            self._alone("1." + _bad("Board tally")))

    def test_r16_10_held_fresh_gate_underscore_head(self):
        """Held fresh head: Gate_2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Gate_2 tally")))

    def test_r16_10_held_fresh_step_slash_head(self):
        """Held fresh head: Step/3 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step/3 tally")))

    def test_r16_10_held_fresh_bracket_trace_summary(self):
        """Held fresh head: [2] Trace summary alone."""
        self._assert_alone_cured(
            self._alone("[2] " + _bad("Trace summary")))

    def test_r16_10_held_fresh_paren_step_underscore(self):
        """Held fresh head: (3) Step_2 tally alone."""
        self._assert_alone_cured(
            self._alone("(3) " + _bad("Step_2 tally")))

    def test_r16_10_held_fresh_rounds_trace_summary(self):
        """Held fresh head: Round's trace summary alone."""
        self._assert_alone_cured(
            self._alone(_bad("Round's trace summary")))

    # ------------------------------------------------------
    # Read and absent controls, byte for byte
    # ------------------------------------------------------

    def test_r16_10_held_read_control_byte_for_byte(self):
        """Held control: the gate records read, 8 LANDED of 8."""
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_10_held_absent_feeder_byte_for_byte(self):
        """Held control: no gate records, genuinely absent."""
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
