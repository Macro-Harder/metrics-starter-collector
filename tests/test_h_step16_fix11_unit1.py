"""Step 16 fix pass 11 unit 1 tests: the Q-4 tally head unit.

Pinning tests for register item R16-11-01 (Medium,
B11-01) of Step 16 round 11. The governing rule of the
pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-11-01: a malformed tally statement under a head
the fix pass 10 general form reduces past, cuts at
early sentence punctuation, or stands behind a marker
shape its marker match does not strip takes Q-4
missing under the no feeder record code in the alone
position and drops the step unnamed in the beside
position, while its counted sibling under the same
head counts, because _trace_candidates counts the
numeric tally pattern with no head test at all. The
sixteen driven heads stand in three subfamilies:
words the reduction treats unexpectedly (Step2tally,
Boardtally and TraceSummary fused; Board tallying,
Board tallies and Trace summaries suffixed or plural;
Summary trace reversed; Board tálly accented, with an
acute accent on the a), heads cut by early sentence
punctuation inside the head (Step 2.5 tally, Board
tally dept. tally, Board: tally), and marker shapes
past the general marker form (A1., II., No., 1.2. and
1.. dot markers, each carrying its closing colon).
Locus: derivation_core.py, _tally_statement_head and
_malformed_trace_statements, against _trace_candidates.

The cure these tests pin reaches every head form
above: the reduction sees a closing that stands fused
or accented as the closing words it is, and the parity
forms stand reached in the forms the register states,
so a malformed tally line under any of them stands as
a feeder statement in the governed forms, alone and
beside, in gate records and gate rulings alike. The
extended boundary the cure lands stands stated in the
unit report and in the docstring of
_tally_statement_head in the same terms.

Held controls stand pinned beside the defect forms:
the counted sibling of every one of the sixteen heads;
the golden prose lines flipping nothing and both
golden comparisons standing green in their own module;
the settled R16-7-03 prose position; the numbered
colon condition in both directions inside the general
marker form, with the held contrasts of R16-11-02
inside the code limb standing missing and the marker
limbs length behaviour standing exactly as it stands
for this unit; the run closure limb in its prose
forms; the folded round 10 prose sentence record
governed in its exact form; the folded round 11
record Trace for step 2a standing missing; every cured
head form of fix passes 7 to 10 as the round 11
register enumerates them, beside the fresh governed
heads of the round 10 and round 11 drives; the read
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
UNNUMBERED_CLOSING = (
    "Record the board tally and this verdict in the "
    "closing entry: member 1 RECYCLE for roster closure "
    "only, its three completions LANDED and its stated "
    "approval condition satisfied; member 2 approve "
    "with notes, six notes binding.")
ACCENTED_HEAD = "Board tálly"

DEFECT_HEADS = (
    "Step2tally",
    "Boardtally",
    "TraceSummary",
    "Board tallying",
    "Board tallies",
    "Trace summaries",
    "Summary trace",
    ACCENTED_HEAD,
    "Step 2.5 tally",
    "Board tally dept. tally",
    "Board: tally",
)

MARKER_DEFECTS = (
    ("alphanumeric", "A1. "),
    ("multi_letter", "II. "),
    ("word_abbreviation", "No. "),
    ("dotted_sequence", "1.2. "),
    ("double_dot", "1.. "),
)


def _assert_no_absence(test, block):
    test.assertNotIn("no first trace record stands", block)
    test.assertNotIn("no feeder record for the metric exists",
                     block)
    test.assertNotIn("no-feeder-record", block)


class TestStep16Fix11Unit1(FixtureTestCase):

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

    def _candidate(self, head, prefix=""):
        self._assert_counted(
            self._alone(prefix + _read(head)))
        self._assert_alone_cured(
            self._alone(prefix + _bad(head)))

    # ------------------------------------------------------
    # Defect forms, R16-11-01, words the reduction treats
    # unexpectedly, alone
    # ------------------------------------------------------

    def test_r16_11_01_fused_step_digit_tally_alone(self):
        """B11-01 fused closing: Step2tally alone."""
        report = self._alone(_bad("Step2tally"))
        self._assert_alone_cured(report)

    def test_r16_11_01_fused_board_tally_alone(self):
        """B11-01 fused closing: Boardtally alone."""
        report = self._alone(_bad("Boardtally"))
        self._assert_alone_cured(report)

    def test_r16_11_01_fused_trace_summary_alone(self):
        """B11-01 fused closing: TraceSummary alone."""
        report = self._alone(_bad("TraceSummary"))
        self._assert_alone_cured(report)

    def test_r16_11_01_tallying_closing_alone(self):
        """B11-01 suffixed closing: Board tallying alone."""
        report = self._alone(_bad("Board tallying"))
        self._assert_alone_cured(report)

    def test_r16_11_01_tallies_closing_alone(self):
        """B11-01 plural closing: Board tallies alone."""
        report = self._alone(_bad("Board tallies"))
        self._assert_alone_cured(report)

    def test_r16_11_01_summaries_closing_alone(self):
        """B11-01 plural closing: Trace summaries alone."""
        report = self._alone(_bad("Trace summaries"))
        self._assert_alone_cured(report)

    def test_r16_11_01_reversed_closing_alone(self):
        """B11-01 reversed closing: Summary trace alone."""
        report = self._alone(_bad("Summary trace"))
        self._assert_alone_cured(report)

    def test_r16_11_01_accented_closing_alone(self):
        """B11-01 accented closing: the accented tally head."""
        report = self._alone(_bad(ACCENTED_HEAD))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Defect forms, R16-11-01, heads cut by early sentence
    # punctuation inside the head, alone
    # ------------------------------------------------------

    def test_r16_11_01_decimal_head_alone(self):
        """B11-01 run cut: Step 2.5 tally alone."""
        report = self._alone(_bad("Step 2.5 tally"))
        self._assert_alone_cured(report)

    def test_r16_11_01_abbreviation_dot_head_alone(self):
        """B11-01 run cut: Board tally dept. tally alone."""
        report = self._alone(_bad("Board tally dept. tally"))
        self._assert_alone_cured(report)

    def test_r16_11_01_colon_inside_head_alone(self):
        """B11-01 run cut: Board: tally alone."""
        report = self._alone(_bad("Board: tally"))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Defect forms, R16-11-01, marker shapes past the
    # general marker form, alone
    # ------------------------------------------------------

    def test_r16_11_01_marker_alphanumeric_dot_alone(self):
        """B11-01 marker shape: A1. Board tally alone."""
        report = self._alone("A1. " + _bad("Board tally"))
        self._assert_alone_cured(report)

    def test_r16_11_01_marker_multi_letter_dot_alone(self):
        """B11-01 marker shape: II. Board tally alone."""
        report = self._alone("II. " + _bad("Board tally"))
        self._assert_alone_cured(report)

    def test_r16_11_01_marker_word_abbreviation_dot_alone(self):
        """B11-01 marker shape: No. Board tally alone."""
        report = self._alone("No. " + _bad("Board tally"))
        self._assert_alone_cured(report)

    def test_r16_11_01_marker_dotted_sequence_alone(self):
        """B11-01 marker shape: 1.2. Board tally alone."""
        report = self._alone("1.2. " + _bad("Board tally"))
        self._assert_alone_cured(report)

    def test_r16_11_01_marker_double_dot_alone(self):
        """B11-01 marker shape: 1.. Board tally alone."""
        report = self._alone("1.. " + _bad("Board tally"))
        self._assert_alone_cured(report)

    # ------------------------------------------------------
    # Defect forms, R16-11-01, beside and gate ruling forms
    # ------------------------------------------------------

    def test_r16_11_01_fused_step_digit_tally_beside(self):
        """B11-01 beside form: the fused head step dropped."""
        report = self._run(self._beside_files(_bad("Step2tally")))
        self._assert_beside_cured(report)

    def test_r16_11_01_fused_board_tally_gate_ruling(self):
        """B11-01 gate ruling form: a fused malformed tally."""
        report = self._alone(_bad("Boardtally"), ruling=True)
        self._assert_alone_cured(report, path=RULING_2)

    # ------------------------------------------------------
    # Counted sibling controls of the sixteen heads
    # ------------------------------------------------------

    def test_r16_11_01_fused_step_digit_tally_counted(self):
        """Counted control: Step2tally counted form."""
        self._assert_counted(self._alone(_read("Step2tally")))

    def test_r16_11_01_fused_board_tally_counted(self):
        """Counted control: Boardtally counted form."""
        self._assert_counted(self._alone(_read("Boardtally")))

    def test_r16_11_01_fused_trace_summary_counted(self):
        """Counted control: TraceSummary counted form."""
        self._assert_counted(self._alone(_read("TraceSummary")))

    def test_r16_11_01_tallying_closing_counted(self):
        """Counted control: Board tallying counted form."""
        self._assert_counted(self._alone(_read("Board tallying")))

    def test_r16_11_01_tallies_closing_counted(self):
        """Counted control: Board tallies counted form."""
        self._assert_counted(self._alone(_read("Board tallies")))

    def test_r16_11_01_summaries_closing_counted(self):
        """Counted control: Trace summaries counted form."""
        self._assert_counted(self._alone(_read("Trace summaries")))

    def test_r16_11_01_reversed_closing_counted(self):
        """Counted control: Summary trace counted form."""
        self._assert_counted(self._alone(_read("Summary trace")))

    def test_r16_11_01_accented_closing_counted(self):
        """Counted control: the accented counted form."""
        self._assert_counted(self._alone(_read(ACCENTED_HEAD)))

    def test_r16_11_01_decimal_head_counted(self):
        """Counted control: Step 2.5 tally counted form."""
        self._assert_counted(self._alone(_read("Step 2.5 tally")))

    def test_r16_11_01_abbreviation_dot_head_counted(self):
        """Counted control: the abbreviation dot counted form."""
        self._assert_counted(
            self._alone(_read("Board tally dept. tally")))

    def test_r16_11_01_colon_inside_head_counted(self):
        """Counted control: Board: tally counted form."""
        self._assert_counted(self._alone(_read("Board: tally")))

    def test_r16_11_01_marker_alphanumeric_dot_counted(self):
        """Counted control: the A1. marker counted form."""
        self._assert_counted(
            self._alone("A1. " + _read("Board tally")))

    def test_r16_11_01_marker_multi_letter_dot_counted(self):
        """Counted control: the II. marker counted form."""
        self._assert_counted(
            self._alone("II. " + _read("Board tally")))

    def test_r16_11_01_marker_word_abbreviation_dot_counted(self):
        """Counted control: the No. marker counted form."""
        self._assert_counted(
            self._alone("No. " + _read("Board tally")))

    def test_r16_11_01_marker_dotted_sequence_counted(self):
        """Counted control: the 1.2. marker counted form."""
        self._assert_counted(
            self._alone("1.2. " + _read("Board tally")))

    def test_r16_11_01_marker_double_dot_counted(self):
        """Counted control: the 1.. marker counted form."""
        self._assert_counted(
            self._alone("1.. " + _read("Board tally")))

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

    def test_r16_11_closure_run_past_trace_summary(self):
        """Closure control: a run past the trace summary words."""
        line = ("Trace summary and discussion stand here. LANDED "
                "figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_11_closure_unnumbered_closing_line(self):
        """Closure control: the golden closing line, unnumbered."""
        self._assert_missing(self._alone(UNNUMBERED_CLOSING))

    def test_r16_11_closure_plain_trace_for_step_colon_after(self):
        """Closure control: trace for step colon after items."""
        line = ("Trace for step 2 items checked stand here: "
                "LANDED figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_11_colon_numbered_trace_for_step_no_colon(self):
        """Colon control: numbered trace for step, no colon."""
        line = ("1. Trace for step 2 items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_11_colon_numbered_trace_for_step_with_colon(self):
        """Colon control: numbered trace for step, its colon."""
        line = ("1. Trace for step 2: items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_alone_cured(self._alone(line))

    def test_r16_11_colon_plain_trace_for_step_with_colon(self):
        """Colon control: plain trace for step, its colon."""
        line = ("Trace for step 2: items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_alone_cured(self._alone(line))

    def test_r16_11_colon_plain_trace_for_step_spaced_colon(self):
        """Colon control: trace for step, a spaced colon."""
        line = ("Trace for step 2 : items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_alone_cured(self._alone(line))

    def test_r16_11_prose_sentence_closing_on_tally_governed(self):
        """Folded control: a prose run closing on tally stands."""
        report = self._alone(PROSE_SENTENCE_CLOSING_ON_TALLY)
        self._assert_alone_cured(report)

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

    def test_r16_11_held_contrast_six_digit_paren_no_colon(self):
        """Held contrast of R16-11-02: (123456) in dot form."""
        line = ("(123456) Board tally. LANDED figures stand "
                "here, no counts stated")
        self._assert_missing(self._alone(line))

    def test_r16_11_held_contrast_one_digit_paren_no_colon(self):
        """Held contrast of R16-11-02: (1) in dot form."""
        line = ("(1) Board tally. LANDED figures stand here, "
                "no counts stated")
        self._assert_missing(self._alone(line))

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
    # Held cured heads of fix passes 7, 8 and 9
    # ------------------------------------------------------

    def test_r16_11_held_board_tally_head(self):
        """Held head of R16-7-03: Board tally alone."""
        self._assert_alone_cured(self._alone(_bad("Board tally")))

    def test_r16_11_held_step_2_tally_head(self):
        """Held head of R16-7-03: Step 2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step 2 tally")))

    def test_r16_11_held_tally_head(self):
        """Held head of R16-7-03: Tally alone."""
        self._assert_alone_cured(self._alone(_bad("Tally")))

    def test_r16_11_held_gate_record_tally_head(self):
        """Held head of R16-7-03: Gate record tally alone."""
        self._assert_alone_cured(
            self._alone(_bad("Gate record tally")))

    def test_r16_11_held_trace_summary_head(self):
        """Held head of R16-7-03: Trace summary alone."""
        self._assert_alone_cured(self._alone(_bad("Trace summary")))

    def test_r16_11_held_settled_gate_tally(self):
        """Held settled head: Gate tally alone."""
        self._assert_alone_cured(self._alone(TALLY_B6_BAD))

    def test_r16_11_held_settled_trace_for_step(self):
        """Held settled head: Trace for step 2 alone."""
        self._assert_alone_cured(self._alone(TALLY_C6_A_BAD))

    def test_r16_11_held_settled_trace_tally_for_step(self):
        """Held settled head: Trace tally for step 2 alone."""
        self._assert_alone_cured(self._alone(TALLY_C6_B_BAD))

    def test_r16_11_held_six_word_head(self):
        """Held head of R16-8-01: the six word head alone."""
        self._assert_alone_cured(self._alone(_bad(SIX_WORD)))

    def test_r16_11_held_review_head(self):
        """Held head of R16-8-01: the review head alone."""
        self._assert_alone_cured(self._alone(_bad(REVIEW_HEAD)))

    def test_r16_11_held_long_trace_summary_head(self):
        """Held head of R16-8-01: the long trace summary head."""
        self._assert_alone_cured(self._alone(_bad(LONG_SUMMARY)))

    def test_r16_11_held_numbered_list_board_tally(self):
        """Held head of R16-8-01: 1. Board tally alone."""
        self._assert_alone_cured(
            self._alone("1. " + _bad("Board tally")))

    def test_r16_11_held_hyphenated_step_head(self):
        """Held head of R16-8-01: Step-2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step-2 tally")))

    def test_r16_11_held_comma_board_head(self):
        """Held head of R16-8-01: Board, tally alone."""
        self._assert_alone_cured(self._alone(_bad("Board, tally")))

    def test_r16_11_held_fix9_underscore_head(self):
        """Held head of R16-9-01: Step_2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step_2 tally")))

    def test_r16_11_held_fix9_slash_head(self):
        """Held head of R16-9-01: Step/2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step/2 tally")))

    def test_r16_11_held_fix9_hyphenated_trace_summary(self):
        """Held head of R16-9-01: Trace-summary alone."""
        self._assert_alone_cured(self._alone(_bad("Trace-summary")))

    def test_r16_11_held_fix9_comma_trace_summary(self):
        """Held head of R16-9-01: Trace, summary alone."""
        self._assert_alone_cured(
            self._alone(_bad("Trace, summary")))

    def test_r16_11_held_fix9_apostrophe_head(self):
        """Held head of R16-9-01: Board's tally alone."""
        self._assert_alone_cured(self._alone(_bad("Board's tally")))

    def test_r16_11_held_fix9_double_hyphen_head(self):
        """Held head of R16-9-01: Step--2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step--2 tally")))

    def test_r16_11_held_fix9_parenthesised_numbered(self):
        """Held head of R16-9-01: (1) Board tally alone."""
        self._assert_alone_cured(
            self._alone("(1) " + _bad("Board tally")))

    def test_r16_11_held_fix9_bracket_numbered(self):
        """Held head of R16-9-01: [1] Board tally alone."""
        self._assert_alone_cured(
            self._alone("[1] " + _bad("Board tally")))

    def test_r16_11_held_fix9_numbered_no_space(self):
        """Held head of R16-9-01: 1.Board tally alone."""
        self._assert_alone_cured(
            self._alone("1." + _bad("Board tally")))

    # ------------------------------------------------------
    # Held cured heads of fix pass 10
    # ------------------------------------------------------

    def test_r16_11_held_fix10_comma_no_space_summary(self):
        """Held head of R16-10-01: Trace,summary alone."""
        self._assert_alone_cured(self._alone(_bad("Trace,summary")))

    def test_r16_11_held_fix10_slash_summary(self):
        """Held head of R16-10-01: Trace/summary alone."""
        self._assert_alone_cured(self._alone(_bad("Trace/summary")))

    def test_r16_11_held_fix10_underscore_summary(self):
        """Held head of R16-10-01: Trace_summary alone."""
        self._assert_alone_cured(self._alone(_bad("Trace_summary")))

    def test_r16_11_held_fix10_double_hyphen_summary(self):
        """Held head of R16-10-01: Trace--summary alone."""
        self._assert_alone_cured(
            self._alone(_bad("Trace--summary")))

    def test_r16_11_held_fix10_spaced_hyphen_summary(self):
        """Held head of R16-10-01: Trace - summary alone."""
        self._assert_alone_cured(
            self._alone(_bad("Trace - summary")))

    def test_r16_11_held_fix10_plus_head(self):
        """Held head of R16-10-01: Step+2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step+2 tally")))

    def test_r16_11_held_fix10_equals_head(self):
        """Held head of R16-10-01: Step=2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step=2 tally")))

    def test_r16_11_held_fix10_hash_head(self):
        """Held head of R16-10-01: Step#2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step#2 tally")))

    def test_r16_11_held_fix10_percent_head(self):
        """Held head of R16-10-01: Step%2 tally alone."""
        self._assert_alone_cured(self._alone(_bad("Step%2 tally")))

    def test_r16_11_held_fix10_ampersand_head(self):
        """Held head of R16-10-01: Board& tally alone."""
        self._assert_alone_cured(self._alone(_bad("Board& tally")))

    def test_r16_11_held_fix10_non_ascii_head(self):
        """Held head of R16-10-01: Böard tally alone."""
        self._assert_alone_cured(self._alone(_bad("Böard tally")))

    def test_r16_11_held_fix10_trailing_hyphen_head(self):
        """Held head of R16-10-01: Board- tally alone."""
        self._assert_alone_cured(self._alone(_bad("Board- tally")))

    def test_r16_11_held_fix10_spaced_comma_head(self):
        """Held head of R16-10-01: Board tally , alone."""
        self._assert_alone_cured(
            self._alone(_bad("Board tally ,")))

    def test_r16_11_held_fix10_colon_marker(self):
        """Held head of R16-10-01: 1: Board tally alone."""
        self._assert_alone_cured(
            self._alone("1: " + _bad("Board tally")))

    def test_r16_11_held_fix10_roman_parenthesis_marker(self):
        """Held head of R16-10-01: (i) Board tally alone."""
        self._assert_alone_cured(
            self._alone("(i) " + _bad("Board tally")))

    def test_r16_11_held_fix10_letter_marker(self):
        """Held head of R16-10-01: A. Board tally alone."""
        self._assert_alone_cured(
            self._alone("A. " + _bad("Board tally")))

    def test_r16_11_held_fix10_hyphen_marker(self):
        """Held head of R16-10-01: 1- Board tally alone."""
        self._assert_alone_cured(
            self._alone("1- " + _bad("Board tally")))

    # ------------------------------------------------------
    # Fresh governed heads of the round 10 and round 11
    # drives
    # ------------------------------------------------------

    def test_r16_11_fresh_gate_underscore_head(self):
        """Fresh governed head: Gate_2 tally, counted and bad."""
        self._candidate("Gate_2 tally")

    def test_r16_11_fresh_step_slash_head(self):
        """Fresh governed head: Step/3 tally, counted and bad."""
        self._candidate("Step/3 tally")

    def test_r16_11_fresh_bracket_trace_summary(self):
        """Fresh governed head: [2] Trace summary forms."""
        self._candidate("Trace summary", prefix="[2] ")

    def test_r16_11_fresh_paren_step_underscore(self):
        """Fresh governed head: (3) Step_2 tally forms."""
        self._candidate("Step_2 tally", prefix="(3) ")

    def test_r16_11_fresh_rounds_trace_summary(self):
        """Fresh governed head: Round's trace summary forms."""
        self._candidate("Round's trace summary")

    def test_r16_11_fresh_mixed_marks_head(self):
        """Fresh governed head: Step_2/3 tally forms."""
        self._candidate("Step_2/3 tally")

    def test_r16_11_fresh_apostrophe_hyphen_head(self):
        """Fresh governed head: Board's-own tally forms."""
        self._candidate("Board's-own tally")

    def test_r16_11_fresh_upper_case_head(self):
        """Fresh governed head: BOARD TALLY forms."""
        self._candidate("BOARD TALLY")

    def test_r16_11_fresh_spaceless_paren_marker(self):
        """Fresh governed head: 1)Board tally forms."""
        self._candidate("Board tally", prefix="1)")

    def test_r16_11_fresh_spaceless_bracket_marker(self):
        """Fresh governed head: [1]Board tally forms."""
        self._candidate("Board tally", prefix="[1]")

    def test_r16_11_fresh_semicolon_closing_board(self):
        """Fresh governed head: Board tally at a semicolon."""
        line = ("Board tally; items checked stand here. LANDED "
                "figures stand here, no counts stated")
        self._assert_alone_cured(self._alone(line))

    def test_r16_11_fresh_semicolon_closing_summary(self):
        """Fresh governed head: Trace summary at a semicolon."""
        line = ("Trace summary; items checked stand here. LANDED "
                "figures stand here, no counts stated")
        self._assert_alone_cured(self._alone(line))

    def test_r16_11_fresh_at_sign_summary(self):
        """Fresh governed head: Trace@summary forms."""
        self._candidate("Trace@summary")

    def test_r16_11_fresh_dollar_step_head(self):
        """Fresh governed head: Step$2 tally forms."""
        self._candidate("Step$2 tally")

    def test_r16_11_fresh_tilde_board_head(self):
        """Fresh governed head: Board~ tally forms."""
        self._candidate("Board~ tally")

    def test_r16_11_fresh_caret_step_head(self):
        """Fresh governed head: Step^2 tally forms."""
        self._candidate("Step^2 tally")

    def test_r16_11_fresh_star_board_head(self):
        """Fresh governed head: Board* tally forms."""
        self._candidate("Board* tally")

    def test_r16_11_fresh_three_space_summary(self):
        """Fresh governed head: trace summary apart by spaces."""
        self._candidate("Trace   summary")

    def test_r16_11_fresh_paren_letter_marker(self):
        """Fresh governed head: (x) Board tally forms."""
        self._candidate("Board tally", prefix="(x) ")

    def test_r16_11_fresh_digit_colon_marker(self):
        """Fresh governed head: 2: Board tally forms."""
        self._candidate("Board tally", prefix="2: ")

    def test_r16_11_fresh_letter_paren_marker(self):
        """Fresh governed head: B) Board tally forms."""
        self._candidate("Board tally", prefix="B) ")

    def test_r16_11_fresh_bracket_roman_marker(self):
        """Fresh governed head: [iv] Board tally forms."""
        self._candidate("Board tally", prefix="[iv] ")

    def test_r16_11_fresh_letter_dot_marker(self):
        """Fresh governed head: Q. Board tally forms."""
        self._candidate("Board tally", prefix="Q. ")

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
