"""Step 16 fix pass 13 unit 1 tests: the Q-4 tally word unit.

Pinning tests for register item R16-13-02 (Medium, B13-02)
of Step 16 round 13. The governing rule of the pass, in
its extended form: a piece not read in full, for whatever
reason, is not read, and its converse: a piece that is no
feeder flips nothing.

R16-13-02: a prose line whose opening run closes on an
ordinary prose word the narrowed tally word test of fix
pass 12 still admits by its letter test takes a tally
statement head at _tally_statement_head, so Q-4 reports
present but not derivable over a line that is no feeder,
alone, beside, and in gate rulings. The closing words are
rectally and septally, ordinary adverbs of the totally
family in form: the tally letters stand as the tal ending
of the stem of each word before the ly suffix, and the
stem standing before the tally letters ends in c in
rectally (rec) and in p in septally (sep), letters the
narrowed letter test does not exclude, because the family
letter of each word stands inside its stem and not at the
end of the letters before tally. Locus: derivation_core.py,
_tally_word, its ends with tally limb and its prefix letter
test, read through _tally_statement_head. The cure these
tests pin: the tally word test widens its totally family
exclusion so those prose words no longer stand as the
tally word, the letters standing before tally ending in
c or in p standing as family stem endings beside the
vowel letters and n, r or s, while every governed form
stands: the exact words tally, tallies, tallied and
tallying, the fused prefix forms ending in tally whose
prefix ends in another consonant or in a digit
(Boardtally, Gate2tally, Reviewtally, Step2tally), the
trace summary closings in their governed forms, and the
for step forms.

Held controls stand pinned beside the defect forms:
the twenty driven forms of R16-13-01 in their entering
behaviour (Q-4 missing in each alone form beside a counted
sibling counting 2 of 2 LANDED under the same head, Step 2
standing nowhere in the beside form, and the gate ruling
form standing missing; Unit 2 item, neither cured nor
altered by this unit); the eight forms of R16-12-02 in
their cured missing forms; the twelve forms of R16-12-01
in their cured governed forms; the closing Board talli
standing missing as a boundary control, its accent standing
on a final letter the tally word does not carry, folding
to talli, a different word under every limb; the folded
round 10 prose sentence record, whose opening run closes
on the word tally itself, standing governed; the four
folded marker shape records (nested parenthesis, spaced
parenthesis, empty parenthesis, brace token) standing
present but not derivable; the golden prose lines standing
unflipped; the settled R16-7-03 prose position; the folded
round 11 record (Trace for step 2a standing missing); and
the run closure limb.
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

RECTALLY_LINE = ("The results were recorded rectally: LANDED "
                 "figures stand here, no counts stated")
SEPTALLY_LINE = ("The sample was taken septally: LANDED figures "
                 "stand here, no counts stated")


def _dot_form(prefix, head):
    return (prefix + head + ". LANDED figures stand here, "
            "no counts stated")


def _prose(word_run):
    return (word_run + " LANDED figures stand here, "
            "no counts stated")


class TestStep16Fix13Unit1(FixtureTestCase):

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
    # R16-13-02 defect forms: prose closing words escaping
    # the narrowed letter test stand missing after the cure
    # ------------------------------------------------------

    def test_r16_13_02_prose_rectally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(RECTALLY_LINE))

    def test_r16_13_02_prose_septally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(SEPTALLY_LINE))

    def test_r16_13_02_prose_rectally_gate_ruling_missing(self):
        self._assert_q4_missing(
            self._q4_alone(RECTALLY_LINE, ruling=True))

    def test_r16_13_02_prose_rectally_beside_step2_nowhere(self):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=RECTALLY_LINE)
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)

    # ------------------------------------------------------
    # Held controls: R16-13-01 driven forms in their
    # entering behaviour, Q-4 missing in each, Unit 2 item,
    # neither cured nor altered by this unit
    # ------------------------------------------------------

    def test_r16_13_held_01_fused_tallied_missing(self):
        self._candidate_missing(_bad("Boardtallied"),
                                _read("Boardtallied"))

    def test_r16_13_held_01_fused_tallies_missing(self):
        self._candidate_missing(_bad("Boardtallies"),
                                _read("Boardtallies"))

    def test_r16_13_held_01_fused_tallying_missing(self):
        self._candidate_missing(_bad("Boardtallying"),
                                _read("Boardtallying"))

    def test_r16_13_held_01_fused_prefix_pass_missing(self):
        self._candidate_missing(_bad("Passtally"),
                                _read("Passtally"))

    def test_r16_13_held_01_fused_prefix_chair_missing(self):
        self._candidate_missing(_bad("Chairtally"),
                                _read("Chairtally"))

    def test_r16_13_held_01_fused_prefix_green_missing(self):
        self._candidate_missing(_bad("Greentally"),
                                _read("Greentally"))

    def test_r16_13_held_01_fused_prefix_alpha_missing(self):
        self._candidate_missing(_bad("Alphatally"),
                                _read("Alphatally"))

    def test_r16_13_held_01_fused_prefix_pass_beside_nowhere(self):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=_bad("Passtally"))
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)

    def test_r16_13_held_01_summary_summarize_american_missing(self):
        self._candidate_missing(_bad("Trace summarize"),
                                _read("Trace summarize"))

    def test_r16_13_held_01_summary_summarized_american_missing(self):
        self._candidate_missing(_bad("Trace summarized"),
                                _read("Trace summarized"))

    def test_r16_13_held_01_summary_summarises_british_missing(self):
        self._candidate_missing(_bad("Trace summarises"),
                                _read("Trace summarises"))

    def test_r16_13_held_01_summary_summarize_gate_ruling_missing(self):
        report = self._q4_alone(_bad("Trace summarize"),
                                ruling=True)
        self._assert_q4_missing(report)

    def test_r16_13_held_01_fused_tracesummarise_british_missing(self):
        self._candidate_missing(_bad("Boardtracesummarise"),
                                _read("Boardtracesummarise"))

    def test_r16_13_held_01_fused_tracesummarised_missing(self):
        self._candidate_missing(_bad("Tracesummarised"),
                                _read("Tracesummarised"))

    def test_r16_13_held_01_fused_summarytraces_reversed_missing(self):
        self._candidate_missing(_bad("Boardsummarytraces"),
                                _read("Boardsummarytraces"))

    def test_r16_13_held_01_stroke_letter_t_tally_missing(self):
        self._candidate_missing(_bad("Board ŧally"),
                                _read("Board ŧally"))

    def test_r16_13_held_01_inserted_two_words_summary_missing(self):
        self._candidate_missing(_bad("Trace board gate summary"),
                                _read("Trace board gate summary"))

    def test_r16_13_held_01_inserted_reversed_summary_missing(self):
        self._candidate_missing(_bad("Summary board trace"),
                                _read("Summary board trace"))

    def test_r16_13_held_01_fused_tallied_for_step_missing(self):
        self._candidate_missing(_bad("Boardtallied for step 2"),
                                _read("Boardtallied for step 2"))

    def test_r16_13_held_01_inserted_trace_for_step_missing(self):
        self._candidate_missing(_bad("Trace board for step 2"),
                                _read("Trace board for step 2"))

    # ------------------------------------------------------
    # Held controls: R16-12-02 stands cured in its restated
    # boundary, its eight forms standing missing or standing
    # nowhere on the row
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

    def test_r16_12_02_held_prose_totally_beside_nowhere(self):
        line = _prose("The figures stand totally:")
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=line)
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)

    # ------------------------------------------------------
    # Held controls: R16-12-01 stands cured in its restated
    # boundary, its twelve forms standing governed
    # ------------------------------------------------------

    def test_r16_12_01_held_tallied_closing_governed(self):
        self._candidate_governed(_bad("Board tallied"),
                                 _read("Board tallied"))

    def test_r16_12_01_held_tallied_head_word_alone_governed(self):
        self._candidate_governed(_bad("Tallied"), _read("Tallied"))

    def test_r16_12_01_held_tallied_beside_step2_uncounted(self):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=_bad("Board tallied"))
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_r16_12_01_held_summarise_british_governed(self):
        self._candidate_governed(_bad("Trace summarise"),
                                 _read("Trace summarise"))

    def test_r16_12_01_held_summarised_british_governed(self):
        self._candidate_governed(_bad("Trace summarised"),
                                 _read("Trace summarised"))

    def test_r16_12_01_held_summarise_gate_ruling_governed(self):
        report = self._q4_alone(_bad("Trace summarise"),
                                ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    def test_r16_12_01_held_fused_prefix_summary_governed(self):
        self._candidate_governed(_bad("Boardtracesummary"),
                                 _read("Boardtracesummary"))

    def test_r16_12_01_held_fused_plural_summary_governed(self):
        self._candidate_governed(_bad("Tracesummaries"),
                                 _read("Tracesummaries"))

    def test_r16_12_01_held_tallies_for_step_governed(self):
        self._candidate_governed(_bad("Tallies for step 2"),
                                 _read("Tallies for step 2"))

    def test_r16_12_01_held_fused_tally_for_step_governed(self):
        self._candidate_governed(_bad("Boardtally for step 2"),
                                 _read("Boardtally for step 2"))

    def test_r16_12_01_held_stroke_letter_tally_governed(self):
        self._candidate_governed(_bad("Board tałly"),
                                 _read("Board tałly"))

    def test_r16_12_01_held_inserted_word_summary_governed(self):
        self._candidate_governed(_bad("Trace board summary"),
                                 _read("Trace board summary"))

    # ------------------------------------------------------
    # Held controls: the Board talli boundary control, the
    # governed fused prefix forms, the marker shapes, the
    # golden lines, and the settled positions
    # ------------------------------------------------------

    def test_r16_13_held_closing_talli_different_word_missing(self):
        self._candidate_missing(_bad("Board tallí"),
                                _read("Board tallí"))

    def test_r16_13_governed_fused_boardtally(self):
        self._candidate_governed(_bad("Boardtally"),
                                 _read("Boardtally"))

    def test_r16_13_governed_fused_gate2tally(self):
        self._candidate_governed(_bad("Gate2tally"),
                                 _read("Gate2tally"))

    def test_r16_13_governed_fused_reviewtally(self):
        self._candidate_governed(_bad("Reviewtally"),
                                 _read("Reviewtally"))

    def test_r16_13_governed_fused_step2tally(self):
        self._candidate_governed(_bad("Step2tally"),
                                 _read("Step2tally"))

    def test_r16_13_held_marker_nested_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("((1)) ", "Board tally")))

    def test_r16_13_held_marker_spaced_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("(a b) ", "Board tally")))

    def test_r16_13_held_marker_empty_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("() ", "Board tally")))

    def test_r16_13_held_marker_brace_token_governed(self):
        self._assert_q4_governed(self._q4_alone(
            "{1} " + _bad("Board tally")))

    def test_r16_13_held_golden_board_line_missing(self):
        self._assert_q4_missing(self._q4_alone(GOLDEN_BOARD_LINE))

    def test_r16_13_held_golden_closing_line_missing(self):
        self._assert_q4_missing(self._q4_alone(GOLDEN_CLOSING_LINE))

    def test_r16_13_held_prose_sentence_closing_on_tally(self):
        line = ("Record the board tally. LANDED figures stand "
                "here, no counts stated")
        self._assert_q4_governed(self._q4_alone(line))

    def test_r16_13_held_prose_fragment_no_head_missing(self):
        line = ("A malformed fragment stands in prose position "
                "here. LANDED figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_13_held_closure_run_past_tally_colon(self):
        line = ("Board tally, and its figures stand here: LANDED "
                "figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_13_held_closure_run_past_summary_dot(self):
        line = ("Trace summary of the board stands here. LANDED "
                "figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_13_held_trace_for_step_alphanumeric_missing(self):
        line = ("Trace for step 2a: items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_13_held_read_control_byte_for_byte(self):
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_13_held_absent_feeder_byte_for_byte(self):
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
