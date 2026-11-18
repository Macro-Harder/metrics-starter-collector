"""Step 16 fix pass 12 unit 2 tests: the Q-4 tally head unit.

Pinning tests for register item R16-12-01 (Medium, B12-01)
of Step 16 round 12. The governing rule of the pass, in
its extended form: a piece not read in full, for whatever
reason, is not read, and its converse: a piece that is no
feeder flips nothing.

R16-12-01: a malformed tally statement under a head the
fix pass 11 restated boundary, as narrowed by fix pass 12
Unit 1, still does not reach takes Q-4 missing under the
no feeder record code, alone, beside with the step
dropped unnamed, and in gate rulings, while its counted
sibling under the same head counts 2 of 2 LANDED, because
_trace_candidates counts the numeric tally pattern with
no head test at all. The twelve driven forms stand in six
subfamilies: (a) the past tense closing, Board tallied,
Tallied standing alone, and Board tallied beside; (b) the
British summary spellings, Trace summarise, Trace
summarised, and Trace summarise in a gate ruling; (c) the
fused trace summary closings past exact equality,
Boardtracesummary fused behind a prefix and
Tracesummaries fused with the plural; (d) the for step
closings under a tally word the cure itself admits,
Tallies for step 2 and Boardtally for step 2; (e) the
stroke letter closing, Board tałly, the letter ł, l with
a stroke, standing in place of a letter the tally word
itself carries; and (f) the inserted word closing, Trace
board summary, a word standing between the trace word and
the summary word. Locus: derivation_core.py, _fold_word,
_tally_word, and _tally_statement_head and its closing
tests. The cure these tests pin widens the stated
boundary: the tally word stands in its past tense form
tallied as well; the summary word stands in its British
spellings summarise and summarised as well; the fused
trace summary closing stands behind a fused prefix and
in the fused plural as well; the for step limb reads its
head word through the tally word test; the accent
folding folds the stroke letter to the letter it stands
in place of; and the trace summary closing stands with
one word standing between the trace word and the summary
word. Subfamily (d) stands against the cure own stated
word forms; the other five subfamilies stand on the
counted pattern head agnosticism ground alone, so the
widened boundary stands restated in the open in the unit
report and in the docstring of _tally_statement_head in
the same terms.

Held controls stand pinned beside the defect forms:
R16-12-02 stands cured as Unit 1 left it, prose lines
closing on totally, accidentally, digitally,
incidentally, mentally, or tallyho flipping nothing,
alone, beside, and in gate rulings, under the narrowed
tally word boundary of Unit 1 in its stated terms; the
closing Board tallí stands missing as a boundary control,
its accent standing on a final letter the tally word
does not carry, folding to talli, a different word under
every limb; the folded round 10 prose sentence record,
whose opening run closes on the word tally itself,
standing governed; the four folded marker shape records
(nested parenthesis, spaced parenthesis, empty
parenthesis, brace token) standing present but not
derivable; the golden prose lines standing unflipped;
the settled R16-7-03 prose position; the numbered no
colon residual as extended by fix pass 11 Unit 2, bracket
and parenthesis markers at any length engaging the colon
condition; the folded round 11 record (Trace for step 2a
standing missing); the run closure limb; and the colon
conditions per boundary in both directions.
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


def _dot_form(prefix, head):
    return (prefix + head + ". LANDED figures stand here, "
            "no counts stated")


def _prose(word_run):
    return (word_run + " LANDED figures stand here, "
            "no counts stated")


class TestStep16Fix12Unit2(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _q4_alone(self, line, ruling=False):
        files = _clean_files()
        if ruling:
            files[RULING_2] = gate_ruling(2, extra=line)
        else:
            files[GATE_2] = gate_record(2, extra=line)
        return self._run(files)

    def _assert_q4_governed(self, report, path=GATE_2):
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("Step 2", q4)
        self.assertIn(path, q4)
        self.assertNotIn("no-feeder-record", q4)

    def _assert_q4_counted(self, report):
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("Step 2, 2 of 2 LANDED", q4)

    def _assert_q4_missing(self, report):
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "missing", "Q-4")
        self.assertIn("no-feeder-record", q4)

    def _candidate_governed(self, line, counted_line):
        self._assert_q4_counted(self._q4_alone(counted_line))
        self._assert_q4_governed(self._q4_alone(line))

    def _candidate_missing(self, line, counted_line):
        self._assert_q4_counted(self._q4_alone(counted_line))
        self._assert_q4_missing(self._q4_alone(line))

    # ------------------------------------------------------
    # R16-12-01 defect forms: the six subfamilies stand
    # governed after the cure, each beside its counted
    # sibling counting 2 of 2 LANDED under the same head
    # ------------------------------------------------------

    def test_r16_12_01_tallied_closing_governed(self):
        self._candidate_governed(_bad("Board tallied"),
                                 _read("Board tallied"))

    def test_r16_12_01_tallied_head_word_alone_governed(self):
        self._candidate_governed(_bad("Tallied"), _read("Tallied"))

    def test_r16_12_01_tallied_beside_step2_uncounted(self):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=_bad("Board tallied"))
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_r16_12_01_summarise_british_governed(self):
        self._candidate_governed(_bad("Trace summarise"),
                                 _read("Trace summarise"))

    def test_r16_12_01_summarised_british_governed(self):
        self._candidate_governed(_bad("Trace summarised"),
                                 _read("Trace summarised"))

    def test_r16_12_01_summarise_gate_ruling_governed(self):
        report = self._q4_alone(_bad("Trace summarise"),
                                ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    def test_r16_12_01_fused_prefix_trace_summary_governed(self):
        self._candidate_governed(_bad("Boardtracesummary"),
                                 _read("Boardtracesummary"))

    def test_r16_12_01_fused_plural_trace_summary_governed(self):
        self._candidate_governed(_bad("Tracesummaries"),
                                 _read("Tracesummaries"))

    def test_r16_12_01_tallies_for_step_governed(self):
        self._candidate_governed(_bad("Tallies for step 2"),
                                 _read("Tallies for step 2"))

    def test_r16_12_01_fused_tally_for_step_governed(self):
        self._candidate_governed(_bad("Boardtally for step 2"),
                                 _read("Boardtally for step 2"))

    def test_r16_12_01_stroke_letter_tally_governed(self):
        self._candidate_governed(_bad("Board tałly"),
                                 _read("Board tałly"))

    def test_r16_12_01_inserted_word_trace_summary_governed(self):
        self._candidate_governed(_bad("Trace board summary"),
                                 _read("Trace board summary"))

    # ------------------------------------------------------
    # Held controls: R16-12-02 stands cured as Unit 1 left
    # it, its eight forms standing missing or standing
    # nowhere on the row, under the narrowed boundary
    # ------------------------------------------------------

    def test_r16_12_02_held_prose_totally_colon_missing(self):
        line = _prose("The figures stand totally:")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_held_prose_accidentally_colon_missing(self):
        line = _prose("The count was checked accidentally:")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_held_prose_digitally_colon_missing(self):
        line = _prose("The results were recorded digitally:")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_held_prose_incidentally_colon_missing(self):
        line = _prose("The figures changed incidentally:")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_held_prose_mentally_dot_missing(self):
        line = _prose("The board reasoned mentally.")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_held_prose_tallyho_colon_missing(self):
        line = _prose("The dawn cry was tallyho:")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_held_prose_totally_gate_ruling_missing(self):
        line = _prose("The figures stand totally:")
        self._assert_q4_missing(self._q4_alone(line, ruling=True))

    def test_r16_12_02_held_prose_totally_beside_step2_nowhere(self):
        line = _prose("The figures stand totally:")
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=line)
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)

    # ------------------------------------------------------
    # Held controls: the Board tallí boundary control, the
    # folded prose sentence record, the marker shapes, the
    # golden lines, and the governed forms standing
    # ------------------------------------------------------

    def test_r16_12_held_closing_talli_different_word_missing(self):
        self._candidate_missing(_bad("Board tallí"),
                                _read("Board tallí"))

    def test_r16_12_held_prose_sentence_closing_on_tally(self):
        line = ("Record the board tally. LANDED figures stand "
                "here, no counts stated")
        self._assert_q4_governed(self._q4_alone(line))

    def test_r16_12_held_marker_nested_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("((1)) ", "Board tally")))

    def test_r16_12_held_marker_spaced_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("(a b) ", "Board tally")))

    def test_r16_12_held_marker_empty_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("() ", "Board tally")))

    def test_r16_12_held_marker_brace_token_governed(self):
        self._assert_q4_governed(self._q4_alone(
            "{1} " + _bad("Board tally")))

    def test_r16_12_held_golden_board_line_missing(self):
        self._assert_q4_missing(self._q4_alone(GOLDEN_BOARD_LINE))

    def test_r16_12_held_golden_closing_line_missing(self):
        self._assert_q4_missing(self._q4_alone(GOLDEN_CLOSING_LINE))

    def test_r16_12_governed_exact_board_tally(self):
        self._candidate_governed(_bad("Board tally"),
                                 _read("Board tally"))

    def test_r16_12_governed_tallies_closing(self):
        self._candidate_governed(_bad("Board tallies"),
                                 _read("Board tallies"))

    def test_r16_12_governed_tallying_closing(self):
        self._candidate_governed(_bad("Board tallying"),
                                 _read("Board tallying"))

    def test_r16_12_governed_fused_boardtally(self):
        self._candidate_governed(_bad("Boardtally"),
                                 _read("Boardtally"))

    def test_r16_12_governed_fused_gate2tally(self):
        self._candidate_governed(_bad("Gate2tally"),
                                 _read("Gate2tally"))

    def test_r16_12_governed_fused_reviewtally(self):
        self._candidate_governed(_bad("Reviewtally"),
                                 _read("Reviewtally"))

    def test_r16_12_governed_fused_step2tally(self):
        self._candidate_governed(_bad("Step2tally"),
                                 _read("Step2tally"))

    def test_r16_12_governed_accented_closing(self):
        self._candidate_governed(_bad("Board tálly"),
                                 _read("Board tálly"))

    def test_r16_12_governed_trace_summary_closing(self):
        self._candidate_governed(_bad("Trace summary"),
                                 _read("Trace summary"))

    def test_r16_12_governed_summary_trace_reversed(self):
        self._candidate_governed(_bad("Summary trace"),
                                 _read("Summary trace"))

    def test_r16_12_governed_fused_tracesummary(self):
        self._candidate_governed(_bad("TraceSummary"),
                                 _read("TraceSummary"))

    def test_r16_12_governed_fused_summarytrace(self):
        self._candidate_governed(_bad("Summarytrace"),
                                 _read("Summarytrace"))

    def test_r16_12_governed_summaries_closing(self):
        self._candidate_governed(_bad("Trace summaries"),
                                 _read("Trace summaries"))

    def test_r16_12_governed_trace_for_step(self):
        self._candidate_governed(_bad("Trace for step 2"),
                                 _read("Trace for step 2"))

    def test_r16_12_governed_tally_for_step(self):
        self._candidate_governed(_bad("Tally for step 2"),
                                 _read("Tally for step 2"))

    def test_r16_12_governed_accented_tally_for_step(self):
        self._candidate_governed(_bad("Tálly for step 2"),
                                 _read("Tálly for step 2"))

    # ------------------------------------------------------
    # Held controls: prose positions, closure limb, colon
    # conditions, folded records, residuals, read control
    # ------------------------------------------------------

    def test_r16_12_held_prose_fragment_no_head_missing(self):
        line = ("A malformed fragment stands in prose position "
                "here. LANDED figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_held_closure_run_past_tally_colon(self):
        line = ("Board tally, and its figures stand here: LANDED "
                "figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_held_closure_run_past_summary_dot(self):
        line = ("Trace summary of the board stands here. LANDED "
                "figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_held_trace_for_step_alphanumeric_missing(self):
        line = ("Trace for step 2a: items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_held_numbered_tally_no_colon_missing(self):
        line = ("1. Board tally. LANDED figures stand here, "
                "no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_held_numbered_summary_no_colon_missing(self):
        line = ("1. Trace summary. LANDED figures stand here, "
                "no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_held_long_paren_marker_no_colon_missing(self):
        self._assert_q4_missing(
            self._q4_alone(_dot_form("(1234567) ", "Board tally")))

    def test_r16_12_held_long_bracket_marker_no_colon_missing(self):
        self._assert_q4_missing(
            self._q4_alone(_dot_form("[1234567] ", "Board tally")))

    def test_r16_12_held_long_paren_marker_colon_governed(self):
        prefix = "(1234567) "
        self._candidate_governed(prefix + _bad("Board tally"),
                                 prefix + _read("Board tally"))

    def test_r16_12_held_long_bracket_marker_colon_governed(self):
        prefix = "[1234567] "
        self._candidate_governed(prefix + _bad("Board tally"),
                                 prefix + _read("Board tally"))

    def test_r16_12_held_very_long_paren_marker_any_length(self):
        prefix = "(" + "9" * 500 + ") "
        self._candidate_governed(prefix + _bad("Board tally"),
                                 prefix + _read("Board tally"))
        self._assert_q4_missing(
            self._q4_alone(_dot_form(prefix, "Board tally")))

    def test_r16_12_held_numbered_exclamation_residual(self):
        line = ("1. Board tally! LANDED figures stand here, "
                "no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_held_numbered_early_colon_then_head(self):
        line = ("1. Note: Board tally: LANDED figures stand here, "
                "no counts stated")
        self._assert_q4_governed(self._q4_alone(line))

    def test_r16_12_held_numbered_dot_close_colon_other(self):
        line = ("1. Board tally. Note: LANDED figures stand here, "
                "no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_held_decimal_head_step_256(self):
        self._candidate_governed(_bad("Step 2.5.6 tally"),
                                 _read("Step 2.5.6 tally"))

    def test_r16_12_held_decimal_head_dot_closing_governed(self):
        line = ("Step 2.5 tally. LANDED figures stand here, "
                "no counts stated")
        self._assert_q4_governed(self._q4_alone(line))

    def test_r16_12_held_read_control_byte_for_byte(self):
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_12_held_absent_feeder_byte_for_byte(self):
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
