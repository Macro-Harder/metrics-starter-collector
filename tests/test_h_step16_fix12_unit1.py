"""Step 16 fix pass 12 unit 1 tests: the Q-4 tally word unit.

Pinning tests for register item R16-12-02 (Medium, B12-02)
of Step 16 round 12. The governing rule of the pass, in
its extended form: a piece not read in full, for whatever
reason, is not read, and its converse: a piece that is no
feeder flips nothing.

R16-12-02: a prose line whose opening run closes on an
ordinary prose word the tally word test admits by its
letters alone takes a tally statement head at
_tally_statement_head, so Q-4 reports present but not
derivable over a line that is no feeder, alone, beside,
and in gate rulings. The closing words are adverbs ending
in the letters tally, formed on other stems (totally,
accidentally, digitally, incidentally, mentally), and a
word beginning with the letters tally (tallyho). Locus:
derivation_core.py, _tally_word, read through
_tally_statement_head. The cure these tests pin: the
tally word test is narrowed so those prose words no
longer stand as the tally word, while every governed
form stands: the exact words tally and tallies, the
tallying form, the fused prefix forms ending in tally
(Boardtally, Gate2tally, Reviewtally, Step2tally), the
trace summary closings in their governed forms, and the
for step forms.

Held controls stand pinned beside the defect forms:
the twelve driven forms of R16-12-01 in their entering
behaviour (Q-4 missing in each, Unit 2 item, neither
cured nor altered by this unit); the folded round 10
prose sentence record, whose opening run closes on the
word tally itself, standing governed; the four folded
marker shape records (nested parenthesis, spaced
parenthesis, empty parenthesis, brace token) standing
present but not derivable; the golden prose lines
standing unflipped; the settled R16-7-03 prose position;
the numbered no colon residual as extended by fix pass
11 Unit 2, bracket and parenthesis markers at any length
engaging the colon condition; the folded round 11 record
(Trace for step 2a standing missing); the run closure
limb; and the colon conditions per boundary in both
directions.
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


class TestStep16Fix12Unit1(FixtureTestCase):

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
    # R16-12-02 defect forms: prose closing words admitted
    # by their letters alone stand missing after the cure
    # ------------------------------------------------------

    def test_r16_12_02_prose_totally_colon_missing(self):
        line = _prose("The figures stand totally:")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_prose_accidentally_colon_missing(self):
        line = _prose("The count was checked accidentally:")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_prose_digitally_colon_missing(self):
        line = _prose("The results were recorded digitally:")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_prose_incidentally_colon_missing(self):
        line = _prose("The figures changed incidentally:")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_prose_mentally_dot_missing(self):
        line = _prose("The board reasoned mentally.")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_prose_tallyho_colon_missing(self):
        line = _prose("The dawn cry was tallyho:")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_12_02_prose_totally_gate_ruling_missing(self):
        line = _prose("The figures stand totally:")
        self._assert_q4_missing(self._q4_alone(line, ruling=True))

    def test_r16_12_02_prose_totally_beside_step2_nowhere(self):
        line = _prose("The figures stand totally:")
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=line)
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)

    # ------------------------------------------------------
    # Held controls: R16-12-01 driven forms stand exactly
    # in their entering behaviour, Q-4 missing in each
    # ------------------------------------------------------

    def test_r16_12_held_01_tallied_closing_missing(self):
        self._candidate_missing(_bad("Board tallied"),
                                _read("Board tallied"))

    def test_r16_12_held_01_tallied_head_word_alone_missing(self):
        self._candidate_missing(_bad("Tallied"), _read("Tallied"))

    def test_r16_12_held_01_summarise_british_missing(self):
        self._candidate_missing(_bad("Trace summarise"),
                                _read("Trace summarise"))

    def test_r16_12_held_01_summarised_british_missing(self):
        self._candidate_missing(_bad("Trace summarised"),
                                _read("Trace summarised"))

    def test_r16_12_held_01_fused_prefix_trace_summary_missing(self):
        self._candidate_missing(_bad("Boardtracesummary"),
                                _read("Boardtracesummary"))

    def test_r16_12_held_01_fused_plural_trace_summary_missing(self):
        self._candidate_missing(_bad("Tracesummaries"),
                                _read("Tracesummaries"))

    def test_r16_12_held_01_tallies_for_step_missing(self):
        self._candidate_missing(_bad("Tallies for step 2"),
                                _read("Tallies for step 2"))

    def test_r16_12_held_01_fused_tally_for_step_missing(self):
        self._candidate_missing(_bad("Boardtally for step 2"),
                                _read("Boardtally for step 2"))

    def test_r16_12_held_01_stroke_letter_tally_missing(self):
        self._candidate_missing(_bad("Board tałly"),
                                _read("Board tałly"))

    def test_r16_12_held_01_inserted_word_trace_summary_missing(self):
        self._candidate_missing(_bad("Trace board summary"),
                                _read("Trace board summary"))

    def test_r16_12_held_01_tallied_beside_step2_nowhere(self):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=_bad("Board tallied"))
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)

    def test_r16_12_held_01_summarise_gate_ruling_missing(self):
        report = self._q4_alone(_bad("Trace summarise"),
                                ruling=True)
        self._assert_q4_missing(report)

    # ------------------------------------------------------
    # Held controls: the four folded marker shape records
    # stand present but not derivable
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Governed forms the narrowed tally word test keeps:
    # exact words, the tallying form, the fused prefix
    # forms, trace summary closings, for step forms
    # ------------------------------------------------------

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
    # conditions, folded records, goldens, residuals
    # ------------------------------------------------------

    def test_r16_12_held_prose_sentence_closing_on_tally(self):
        line = ("Record the board tally. LANDED figures stand "
                "here, no counts stated")
        self._assert_q4_governed(self._q4_alone(line))

    def test_r16_12_held_golden_board_line_missing(self):
        self._assert_q4_missing(self._q4_alone(GOLDEN_BOARD_LINE))

    def test_r16_12_held_golden_closing_line_missing(self):
        self._assert_q4_missing(self._q4_alone(GOLDEN_CLOSING_LINE))

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

    def test_r16_12_held_closing_talli_different_word_missing(self):
        self._candidate_missing(_bad("Board tallí"),
                                _read("Board tallí"))

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
