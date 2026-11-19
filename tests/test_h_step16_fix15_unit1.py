"""Step 16 fix pass 15 unit 1 tests: the Q-4 inserted unit.

Pinning tests for register item R16-15-02 (Medium, B15-02)
of Step 16 round 15. The governing rule of the pass, in
its extended form: a piece not read in full, for whatever
reason, is not read, and its converse: a piece that is no
feeder flips nothing.

R16-15-02: the widened inserted limbs of
_tally_statement_head in derivation_core.py, as fix pass
14 Unit 2 widened them (inserted closings at up to three
words forward and two and three words reversed; the for
step closing at up to two inserted words), read closings
by word count alone with no test on the inserted words,
so ordinary prose runs whose words stand in the trace
summary order take a tally statement head and stand
present but not derivable: Summary of the board trace
(reversed order, three inserted words), Summary of the
trace (reversed, two inserted words), and Trace of the
board summary (forward, three inserted words), each
alone, beside, and in a gate ruling. The held control
bounding the defect at exactly the widened counts:
Summary of the panel board gate trace (four inserted
words, reversed) stands missing. Locus:
derivation_core.py, _tally_statement_head and its
inserted closing limbs, and any helper those limbs read
through. The cure these tests pin fixes what an inserted
closing is: an inserted closing stands only where every
word standing between the trace word and the summary
word, or between the trace word and the for step words,
stands as a governed head word, one of the governed
inserted words board, gate, review and annex, the words
the genuine inserted heads carry standing between their
closing words as whole head words naming the record, its
gate, its review or its annex, so a prose run carrying a
word that stands as no governed head word, of and the
among them, takes no tally statement head in any
position, while every governed inserted closing keeps
standing governed at every count the boundary admits
today, and no count widens.

Held controls stand pinned beside the defect forms, in
full: the thirty seven alone forms of R16-15-01 standing
missing exactly as they enter, this unit curing none of
them, the inserted counts past the widened reach and the
for step counts past two inserted words among them;
every governed inserted closing standing governed, the
closings whose inserted words are governed head words,
at every count the boundary admits today, forward,
reversed, and in the for step limbs, including the
R16-14-01 forms Trace board gate summary, Summary board
trace and Trace board gate annex summary; the governed
fused forms standing governed; the exact word sets
standing as fix pass 14 left them, including tallys
behind a governed fused prefix and tallys alone as no
tally word; the seven enumerated family adverbs and
tallyho standing missing; the fused family forms
subtotally and semirectally standing missing; the Board
tall\u00ed boundary control standing missing; the folded
round 10 prose sentence record standing governed; and
the four folded marker shape records standing present
but not derivable.
"""
from metrics_starter_collector.derivation_core import (
    _fold_word, _summary_word, _tally_word)
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


def _prose(run):
    return (run + ": LANDED figures stand here, "
            "no counts stated")


class TestStep16Fix15Unit1(FixtureTestCase):

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

    def _beside_step2_nowhere(self, line):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=line)
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)

    # ------------------------------------------------------
    # R16-15-02 defect forms: the three prose runs closing
    # on a colon, alone, in a gate ruling and beside, each
    # standing missing under the no feeder record code
    # ------------------------------------------------------

    def test_r16_15_02_prose_summary_of_board_trace_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary of the board trace")))

    def test_r16_15_02_prose_summary_of_the_trace_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary of the trace")))

    def test_r16_15_02_prose_trace_of_board_summary_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace of the board summary")))

    def test_r16_15_02_prose_gate_ruling_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary of the board trace"), ruling=True))

    def test_r16_15_02_prose_beside_step2_nowhere(self):
        self._beside_step2_nowhere(
            _prose("Summary of the board trace"))

    def test_r16_15_02_bounding_control_four_words_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary of the panel board gate trace")))

    # ------------------------------------------------------
    # Held controls: the thirty seven alone forms of
    # R16-15-01 standing missing exactly as they enter,
    # beside their counted siblings, this unit curing
    # none of them
    # ------------------------------------------------------

    def test_r16_15_01_held_paneltally_missing(self):
        self._candidate_missing(_bad("Paneltally"),
                                _read("Paneltally"))

    def test_r16_15_01_held_recordtally_missing(self):
        self._candidate_missing(_bad("Recordtally"),
                                _read("Recordtally"))

    def test_r16_15_01_held_teamtally_missing(self):
        self._candidate_missing(_bad("Teamtally"),
                                _read("Teamtally"))

    def test_r16_15_01_held_paneltallies_missing(self):
        self._candidate_missing(_bad("Paneltallies"),
                                _read("Paneltallies"))

    def test_r16_15_01_held_recordtallied_missing(self):
        self._candidate_missing(_bad("Recordtallied"),
                                _read("Recordtallied"))

    def test_r16_15_01_held_teamtallying_missing(self):
        self._candidate_missing(_bad("Teamtallying"),
                                _read("Teamtallying"))

    def test_r16_15_01_held_gaterecordtally_missing(self):
        self._candidate_missing(_bad("Gaterecordtally"),
                                _read("Gaterecordtally"))

    def test_r16_15_01_held_gateboardtally_missing(self):
        self._candidate_missing(_bad("Gateboardtally"),
                                _read("Gateboardtally"))

    def test_r16_15_01_held_reviewboardtally_missing(self):
        self._candidate_missing(_bad("Reviewboardtally"),
                                _read("Reviewboardtally"))

    def test_r16_15_01_held_boardboardtally_missing(self):
        self._candidate_missing(_bad("Boardboardtally"),
                                _read("Boardboardtally"))

    def test_r16_15_01_held_boardtallyed_missing(self):
        self._candidate_missing(_bad("Boardtallyed"),
                                _read("Boardtallyed"))

    def test_r16_15_01_held_boardtallyes_missing(self):
        self._candidate_missing(_bad("Boardtallyes"),
                                _read("Boardtallyes"))

    def test_r16_15_01_held_chairtallyed_missing(self):
        self._candidate_missing(_bad("Chairtallyed"),
                                _read("Chairtallyed"))

    def test_r16_15_01_held_tallys_alone_missing(self):
        self._candidate_missing(_bad("Tallys"), _read("Tallys"))

    def test_r16_15_01_held_tallyed_alone_missing(self):
        self._candidate_missing(_bad("Tallyed"), _read("Tallyed"))

    def test_r16_15_01_held_summarisations_missing(self):
        self._candidate_missing(_bad("Trace summarisations"),
                                _read("Trace summarisations"))

    def test_r16_15_01_held_summarizations_missing(self):
        self._candidate_missing(_bad("Trace summarizations"),
                                _read("Trace summarizations"))

    def test_r16_15_01_held_summariser_missing(self):
        self._candidate_missing(_bad("Trace summariser"),
                                _read("Trace summariser"))

    def test_r16_15_01_held_summarizer_missing(self):
        self._candidate_missing(_bad("Trace summarizer"),
                                _read("Trace summarizer"))

    def test_r16_15_01_held_fused_summarisations_missing(self):
        self._candidate_missing(_bad("Boardtracesummarisations"),
                                _read("Boardtracesummarisations"))

    def test_r16_15_01_held_fused_summariser_missing(self):
        self._candidate_missing(_bad("Boardtracesummariser"),
                                _read("Boardtracesummariser"))

    def test_r16_15_01_held_traceboardsummary_missing(self):
        self._candidate_missing(_bad("Traceboardsummary"),
                                _read("Traceboardsummary"))

    def test_r16_15_01_held_boardtracegatesummary_missing(self):
        self._candidate_missing(_bad("Boardtracegatesummary"),
                                _read("Boardtracegatesummary"))

    def test_r16_15_01_held_summaryboardtrace_missing(self):
        self._candidate_missing(_bad("Summaryboardtrace"),
                                _read("Summaryboardtrace"))

    def test_r16_15_01_held_inserted_four_forward_missing(self):
        self._candidate_missing(
            _bad("Trace board gate review annex summary"),
            _read("Trace board gate review annex summary"))

    def test_r16_15_01_held_inserted_five_forward_missing(self):
        self._candidate_missing(
            _bad("Trace board gate review annex panel summary"),
            _read("Trace board gate review annex panel summary"))

    def test_r16_15_01_held_inserted_four_reversed_missing(self):
        self._candidate_missing(
            _bad("Summary board gate review annex trace"),
            _read("Summary board gate review annex trace"))

    def test_r16_15_01_held_inserted_annex_review_missing(self):
        self._candidate_missing(
            _bad("Trace board gate annex review summary"),
            _read("Trace board gate annex review summary"))

    def test_r16_15_01_held_inserted_rev_annex_review_missing(self):
        self._candidate_missing(
            _bad("Summary board gate annex review trace"),
            _read("Summary board gate annex review trace"))

    def test_r16_15_01_held_for_step_three_missing(self):
        self._candidate_missing(
            _bad("Trace board gate review for step 2"),
            _read("Trace board gate review for step 2"))

    def test_r16_15_01_held_for_step_four_missing(self):
        self._candidate_missing(
            _bad("Trace board gate review annex for step 2"),
            _read("Trace board gate review annex for step 2"))

    def test_r16_15_01_held_for_step_annex_three_missing(self):
        self._candidate_missing(
            _bad("Trace board gate annex for step 2"),
            _read("Trace board gate annex for step 2"))

    def test_r16_15_01_held_stroke_y_tally_missing(self):
        self._candidate_missing(_bad("Board tall\u024f"),
                                _read("Board tall\u024f"))

    def test_r16_15_01_held_stroke_a_tally_missing(self):
        self._candidate_missing(_bad("Board t\u2c65lly"),
                                _read("Board t\u2c65lly"))

    def test_r16_15_01_held_stroke_r_summary_missing(self):
        self._candidate_missing(_bad("Trace summa\u024dise"),
                                _read("Trace summa\u024dise"))

    def test_r16_15_01_held_stroke_i_summary_missing(self):
        self._candidate_missing(_bad("Trace summar\u0268se"),
                                _read("Trace summar\u0268se"))

    def test_r16_15_01_held_stroke_eth_summary_missing(self):
        self._candidate_missing(_bad("Trace summarise\u00f0"),
                                _read("Trace summarise\u00f0"))

    def test_r16_15_01_held_beside_step2_nowhere(self):
        self._beside_step2_nowhere(_bad("Trace summarisations"))

    def test_r16_15_01_held_gate_ruling_missing(self):
        report = self._q4_alone(_bad("Paneltally"), ruling=True)
        self._assert_q4_missing(report)

    # ------------------------------------------------------
    # Held controls: every governed inserted closing
    # standing governed beside its counted sibling, at
    # every count the boundary admits today, forward,
    # reversed, and in the for step limbs
    # ------------------------------------------------------

    def test_governed_inserted_trace_board_summary(self):
        self._candidate_governed(_bad("Trace board summary"),
                                 _read("Trace board summary"))

    def test_governed_inserted_trace_board_gate_summary(self):
        self._candidate_governed(_bad("Trace board gate summary"),
                                 _read("Trace board gate summary"))

    def test_governed_inserted_trace_board_gate_review(self):
        self._candidate_governed(
            _bad("Trace board gate review summary"),
            _read("Trace board gate review summary"))

    def test_governed_inserted_trace_board_gate_annex(self):
        self._candidate_governed(
            _bad("Trace board gate annex summary"),
            _read("Trace board gate annex summary"))

    def test_governed_inserted_summary_board_trace(self):
        self._candidate_governed(_bad("Summary board trace"),
                                 _read("Summary board trace"))

    def test_governed_inserted_summary_board_gate_trace(self):
        self._candidate_governed(_bad("Summary board gate trace"),
                                 _read("Summary board gate trace"))

    def test_governed_inserted_summary_board_gate_review(self):
        self._candidate_governed(
            _bad("Summary board gate review trace"),
            _read("Summary board gate review trace"))

    def test_governed_inserted_summary_variant_form(self):
        self._candidate_governed(
            _bad("Trace board gate summarising"),
            _read("Trace board gate summarising"))

    def test_governed_for_step_plain(self):
        self._candidate_governed(_bad("Trace for step 2"),
                                 _read("Trace for step 2"))

    def test_governed_for_step_one_inserted(self):
        self._candidate_governed(_bad("Trace board for step 2"),
                                 _read("Trace board for step 2"))

    def test_governed_for_step_two_inserted(self):
        self._candidate_governed(
            _bad("Trace board gate for step 2"),
            _read("Trace board gate for step 2"))

    # ------------------------------------------------------
    # Held controls: the governed fused forms, the exact
    # word sets as fix pass 14 left them, the enumerated
    # family, tallyho and the fused family forms
    # ------------------------------------------------------

    def test_governed_fused_boardtally(self):
        self._candidate_governed(_bad("Boardtally"),
                                 _read("Boardtally"))

    def test_governed_fused_gate2tally(self):
        self._candidate_governed(_bad("Gate2tally"),
                                 _read("Gate2tally"))

    def test_governed_fused_reviewtally(self):
        self._candidate_governed(_bad("Reviewtally"),
                                 _read("Reviewtally"))

    def test_governed_fused_step2tally(self):
        self._candidate_governed(_bad("Step2tally"),
                                 _read("Step2tally"))

    def test_governed_fused_passtally(self):
        self._candidate_governed(_bad("Passtally"),
                                 _read("Passtally"))

    def test_governed_fused_chairtally(self):
        self._candidate_governed(_bad("Chairtally"),
                                 _read("Chairtally"))

    def test_governed_fused_greentally(self):
        self._candidate_governed(_bad("Greentally"),
                                 _read("Greentally"))

    def test_governed_fused_alphatally(self):
        self._candidate_governed(_bad("Alphatally"),
                                 _read("Alphatally"))

    def test_governed_fused_boardtallied(self):
        self._candidate_governed(_bad("Boardtallied"),
                                 _read("Boardtallied"))

    def test_governed_fused_boardtallies(self):
        self._candidate_governed(_bad("Boardtallies"),
                                 _read("Boardtallies"))

    def test_governed_fused_boardtallying(self):
        self._candidate_governed(_bad("Boardtallying"),
                                 _read("Boardtallying"))

    def test_code_level_governed_fused_forms(self):
        for word in ("boardtally", "gate2tally", "reviewtally",
                     "step2tally", "passtally", "chairtally",
                     "greentally", "alphatally", "boardtallied",
                     "boardtallies", "boardtallying"):
            self.assertTrue(_tally_word(_fold_word(word)), word)

    def test_code_level_exact_word_sets(self):
        for word in ("tally", "tallies", "tallied", "tallying"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ("summary", "summaries", "summarise",
                     "summarised", "summarises", "summarize",
                     "summarizes", "summarized", "summarising",
                     "summarizing", "summarisation",
                     "summarization"):
            self.assertTrue(_summary_word(_fold_word(word)), word)

    def test_code_level_tallys_variant_governed_prefix_only(self):
        self.assertTrue(_tally_word(_fold_word("boardtallys")))
        self.assertFalse(_tally_word(_fold_word("tallys")))

    def test_held_prose_totally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The figures stand totally")))

    def test_held_prose_accidentally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The count was checked accidentally")))

    def test_held_prose_digitally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The results were recorded digitally")))

    def test_held_prose_incidentally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The figures changed incidentally")))

    def test_held_prose_mentally_missing(self):
        line = ("The board reasoned mentally. LANDED figures "
                "stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_held_prose_rectally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The results were recorded rectally")))

    def test_held_prose_septally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was taken septally")))

    def test_held_prose_tallyho_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The dawn cry was tallyho")))

    def test_code_level_family_and_tallyho_no_tally_word(self):
        for word in ("totally", "accidentally", "digitally",
                     "incidentally", "mentally", "rectally",
                     "septally", "tallyho", "subtotally",
                     "semirectally", "brutally", "capitally",
                     "vitally", "fatally", "prenatally",
                     "neonatally", "mortally", "frontally",
                     "dentally", "distally", "horizontally",
                     "coastally"):
            self.assertFalse(_tally_word(_fold_word(word)), word)

    def test_held_fused_subtotally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The count was taken subtotally")))

    def test_held_fused_semirectally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The count was taken semirectally")))

    # ------------------------------------------------------
    # Held controls: the twelve prose adverbs of
    # R16-14-02 standing missing in their cured forms
    # ------------------------------------------------------

    def test_held_adverb_brutally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The blow landed brutally")))

    def test_held_adverb_capitally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The fund grew capitally")))

    def test_held_adverb_vitally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was checked vitally")))

    def test_held_adverb_fatally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The blow landed fatally")))

    def test_held_adverb_prenatally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was taken prenatally")))

    def test_held_adverb_neonatally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The unit cared for infants neonatally")))

    def test_held_adverb_mortally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The figure was wounded mortally")))

    def test_held_adverb_frontally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was taken frontally")))

    def test_held_adverb_dentally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The tooth was examined dentally")))

    def test_held_adverb_distally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The limb was measured distally")))

    def test_held_adverb_horizontally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The line extended horizontally")))

    def test_held_adverb_coastally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The route was charted coastally")))

    # ------------------------------------------------------
    # Held controls: the Board talli boundary control, the
    # folded records, the golden lines, and the settled
    # positions
    # ------------------------------------------------------

    def test_held_closing_talli_different_word_missing(self):
        self._candidate_missing(_bad("Board tall\u00ed"),
                                _read("Board tall\u00ed"))

    def test_held_prose_sentence_closing_on_tally(self):
        line = ("Record the board tally. LANDED figures stand "
                "here, no counts stated")
        self._assert_q4_governed(self._q4_alone(line))

    def test_held_marker_nested_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("((1)) ", "Board tally")))

    def test_held_marker_spaced_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("(a b) ", "Board tally")))

    def test_held_marker_empty_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("() ", "Board tally")))

    def test_held_marker_brace_token_governed(self):
        self._assert_q4_governed(self._q4_alone(
            "{1} " + _bad("Board tally")))

    def test_held_golden_board_line_missing(self):
        self._assert_q4_missing(self._q4_alone(GOLDEN_BOARD_LINE))

    def test_held_golden_closing_line_missing(self):
        self._assert_q4_missing(self._q4_alone(GOLDEN_CLOSING_LINE))

    def test_held_prose_fragment_no_head_missing(self):
        line = ("A malformed fragment stands in prose position "
                "here. LANDED figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_held_closure_run_past_tally_colon(self):
        line = ("Board tally, and its figures stand here: LANDED "
                "figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_held_closure_run_past_summary_dot(self):
        line = ("Trace summary of the board stands here. LANDED "
                "figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_held_trace_for_step_alphanumeric_missing(self):
        line = ("Trace for step 2a: items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_held_read_control_byte_for_byte(self):
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_held_absent_feeder_byte_for_byte(self):
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
