"""Step 16 fix pass 15 unit 2 tests: the Q-4 tally head unit.

Pinning tests for register item R16-15-01 (Medium, B15-01,
B15-C01, B15-C02 and B15-C03 merged) of Step 16 round 15.
The governing rule of the pass, in its extended form: a
piece not read in full, for whatever reason, is not read,
and its converse: a piece that is no feeder flips nothing.

R16-15-01: malformed tally statement heads stand missing
past the restated boundaries of fix pass 14, while their
counted siblings count under the same heads, because
_trace_candidates counts the numeric tally pattern with
no head test at all. Thirty seven distinct alone forms
stand in nine subfamilies, every one standing on the
counted pattern head agnosticism ground alone, so the
cure widens the stated boundary and restates it: (a)
fused heads on prefixes the governed enumeration does
not name, Paneltally, Recordtally, Teamtally,
Paneltallies, Recordtallied, Teamtallying and
Gaterecordtally; (b) governed prefixes in further
positions, Gateboardtally, Reviewboardtally and
Boardboardtally; (c) variant spellings past tallys,
Boardtallyed, Boardtallyes, Chairtallyed, Tallys alone
and Tallyed alone, the Tallys alone form entering on the
counted pattern ground alone against the express
standalone exclusion in the restated boundary; (d)
summary plurals and agent nouns, Trace summarisations,
Trace summarizations, Trace summariser and Trace
summarizer, the B15-C02 forms standing already driven
inside this subfamily in the same words; (e) fused on
those, Boardtracesummarisations and Boardtracesummariser;
(f) fused with a word fused between, Traceboardsummary,
Summaryboardtrace and Boardtracegatesummary; (g)
inserted closings past three words, Trace board gate
review annex summary, Trace board gate review annex
panel summary and Summary board gate review annex trace,
with the B15-C01 forms Trace board gate annex review
summary and Summary board gate annex review trace; (h)
the for step closing past two inserted words, Trace
board gate review for step 2 and Trace board gate review
annex for step 2, with the B15-C01 form Trace board gate
annex for step 2; (i) further stroke letters, Board
tall\u024f, Board t\u2c65lly, Trace summa\u024dise and
Trace summar\u0268se, with the B15-C03 form Trace
summarise\u00f0. The beside forms stand driven in the
Trace summarisations head and in the Paneltally head,
and the gate ruling form in the Paneltally head, and the
B15-C01 heads stand carried in their alone and beside
positions. Locus: derivation_core.py, _fold_word,
_tally_word and its constants, _summary_word and its
constant, _fused_trace_summary, _tally_statement_head
and its closing tests, and the governed inserted word
helpers those tests read through.

Held controls stand pinned beside the defect forms, in
full: the other item of the pass standing as Unit 1 left
it, the prose runs Summary of the board trace, Summary
of the trace and Trace of the board summary taking no
tally statement head in any position, alone, beside and
in gate rulings, and its bounding control Summary of the
panel board gate trace standing missing; prose runs at
the counts this unit widens to standing missing where
their inserted words carry a prose joining word; every
governed inserted closing at the counts the boundary
admitted entering this unit standing governed; the
governed forms standing governed, the exact word sets as
fix pass 14 and Unit 1 left them, the governed fused
forms and the governed trace summary forms; the seven
enumerated family adverbs and tallyho standing missing;
the fused family forms subtotally and semirectally
standing missing; the Board tall\u00ed boundary control
standing missing; the folded round 10 prose sentence
record standing governed; and the four folded marker
shape records standing present but not derivable.
"""
from metrics_starter_collector.derivation_core import (
    _fold_word, _fused_trace_summary, _summary_word,
    _tally_word)
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


class TestStep16Fix15Unit2(FixtureTestCase):

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

    def _beside_step2_uncounted(self, line):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=line)
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    # ------------------------------------------------------
    # R16-15-01 defect forms, subfamily (a): fused heads on
    # prefixes the governed enumeration does not name, each
    # standing governed beside its counted sibling
    # ------------------------------------------------------

    def test_r16_15_01_fused_paneltally_governed(self):
        self._candidate_governed(_bad("Paneltally"),
                                 _read("Paneltally"))

    def test_r16_15_01_fused_recordtally_governed(self):
        self._candidate_governed(_bad("Recordtally"),
                                 _read("Recordtally"))

    def test_r16_15_01_fused_teamtally_governed(self):
        self._candidate_governed(_bad("Teamtally"),
                                 _read("Teamtally"))

    def test_r16_15_01_fused_paneltallies_governed(self):
        self._candidate_governed(_bad("Paneltallies"),
                                 _read("Paneltallies"))

    def test_r16_15_01_fused_recordtallied_governed(self):
        self._candidate_governed(_bad("Recordtallied"),
                                 _read("Recordtallied"))

    def test_r16_15_01_fused_teamtallying_governed(self):
        self._candidate_governed(_bad("Teamtallying"),
                                 _read("Teamtallying"))

    def test_r16_15_01_fused_gaterecordtally_governed(self):
        self._candidate_governed(_bad("Gaterecordtally"),
                                 _read("Gaterecordtally"))

    # ------------------------------------------------------
    # R16-15-01 defect forms, subfamily (b): governed
    # prefixes in further positions
    # ------------------------------------------------------

    def test_r16_15_01_further_gateboardtally_governed(self):
        self._candidate_governed(_bad("Gateboardtally"),
                                 _read("Gateboardtally"))

    def test_r16_15_01_further_reviewboardtally_governed(self):
        self._candidate_governed(_bad("Reviewboardtally"),
                                 _read("Reviewboardtally"))

    def test_r16_15_01_further_boardboardtally_governed(self):
        self._candidate_governed(_bad("Boardboardtally"),
                                 _read("Boardboardtally"))

    # ------------------------------------------------------
    # R16-15-01 defect forms, subfamily (c): variant
    # spellings past tallys
    # ------------------------------------------------------

    def test_r16_15_01_variant_boardtallyed_governed(self):
        self._candidate_governed(_bad("Boardtallyed"),
                                 _read("Boardtallyed"))

    def test_r16_15_01_variant_boardtallyes_governed(self):
        self._candidate_governed(_bad("Boardtallyes"),
                                 _read("Boardtallyes"))

    def test_r16_15_01_variant_chairtallyed_governed(self):
        self._candidate_governed(_bad("Chairtallyed"),
                                 _read("Chairtallyed"))

    def test_r16_15_01_variant_tallys_alone_governed(self):
        self._candidate_governed(_bad("Tallys"), _read("Tallys"))

    def test_r16_15_01_variant_tallyed_alone_governed(self):
        self._candidate_governed(_bad("Tallyed"), _read("Tallyed"))

    # ------------------------------------------------------
    # R16-15-01 defect forms, subfamily (d): summary
    # plurals and agent nouns, the B15-C02 forms standing
    # inside this subfamily in the same words
    # ------------------------------------------------------

    def test_r16_15_01_summary_summarisations_governed(self):
        self._candidate_governed(_bad("Trace summarisations"),
                                 _read("Trace summarisations"))

    def test_r16_15_01_summary_summarizations_governed(self):
        self._candidate_governed(_bad("Trace summarizations"),
                                 _read("Trace summarizations"))

    def test_r16_15_01_summary_summariser_governed(self):
        self._candidate_governed(_bad("Trace summariser"),
                                 _read("Trace summariser"))

    def test_r16_15_01_summary_summarizer_governed(self):
        self._candidate_governed(_bad("Trace summarizer"),
                                 _read("Trace summarizer"))

    # ------------------------------------------------------
    # R16-15-01 defect forms, subfamily (e): fused on the
    # further summary forms
    # ------------------------------------------------------

    def test_r16_15_01_fused_summarisations_governed(self):
        self._candidate_governed(
            _bad("Boardtracesummarisations"),
            _read("Boardtracesummarisations"))

    def test_r16_15_01_fused_summariser_governed(self):
        self._candidate_governed(_bad("Boardtracesummariser"),
                                 _read("Boardtracesummariser"))

    # ------------------------------------------------------
    # R16-15-01 defect forms, subfamily (f): fused with a
    # word fused between the closing words
    # ------------------------------------------------------

    def test_r16_15_01_between_traceboardsummary_governed(self):
        self._candidate_governed(_bad("Traceboardsummary"),
                                 _read("Traceboardsummary"))

    def test_r16_15_01_between_summaryboardtrace_governed(self):
        self._candidate_governed(_bad("Summaryboardtrace"),
                                 _read("Summaryboardtrace"))

    def test_r16_15_01_between_boardtracegate_governed(self):
        self._candidate_governed(
            _bad("Boardtracegatesummary"),
            _read("Boardtracegatesummary"))

    # ------------------------------------------------------
    # R16-15-01 defect forms, subfamily (g): inserted
    # closings past three words, the B15-C01 forms standing
    # inside this subfamily
    # ------------------------------------------------------

    def test_r16_15_01_inserted_four_forward_governed(self):
        self._candidate_governed(
            _bad("Trace board gate review annex summary"),
            _read("Trace board gate review annex summary"))

    def test_r16_15_01_inserted_five_forward_governed(self):
        self._candidate_governed(
            _bad("Trace board gate review annex panel summary"),
            _read("Trace board gate review annex panel summary"))

    def test_r16_15_01_inserted_four_reversed_governed(self):
        self._candidate_governed(
            _bad("Summary board gate review annex trace"),
            _read("Summary board gate review annex trace"))

    def test_r16_15_01_inserted_c01_forward_governed(self):
        self._candidate_governed(
            _bad("Trace board gate annex review summary"),
            _read("Trace board gate annex review summary"))

    def test_r16_15_01_inserted_c01_reversed_governed(self):
        self._candidate_governed(
            _bad("Summary board gate annex review trace"),
            _read("Summary board gate annex review trace"))

    # ------------------------------------------------------
    # R16-15-01 defect forms, subfamily (h): the for step
    # closing past two inserted words, the B15-C01 form
    # standing inside this subfamily
    # ------------------------------------------------------

    def test_r16_15_01_for_step_three_governed(self):
        self._candidate_governed(
            _bad("Trace board gate review for step 2"),
            _read("Trace board gate review for step 2"))

    def test_r16_15_01_for_step_four_governed(self):
        self._candidate_governed(
            _bad("Trace board gate review annex for step 2"),
            _read("Trace board gate review annex for step 2"))

    def test_r16_15_01_for_step_c01_three_governed(self):
        self._candidate_governed(
            _bad("Trace board gate annex for step 2"),
            _read("Trace board gate annex for step 2"))

    # ------------------------------------------------------
    # R16-15-01 defect forms, subfamily (i): further
    # stroke letters, the B15-C03 form standing inside
    # this subfamily
    # ------------------------------------------------------

    def test_r16_15_01_stroke_y_tally_governed(self):
        self._candidate_governed(_bad("Board tall\u024f"),
                                 _read("Board tall\u024f"))

    def test_r16_15_01_stroke_a_tally_governed(self):
        self._candidate_governed(_bad("Board t\u2c65lly"),
                                 _read("Board t\u2c65lly"))

    def test_r16_15_01_stroke_r_summary_governed(self):
        self._candidate_governed(_bad("Trace summa\u024dise"),
                                 _read("Trace summa\u024dise"))

    def test_r16_15_01_stroke_i_summary_governed(self):
        self._candidate_governed(_bad("Trace summar\u0268se"),
                                 _read("Trace summar\u0268se"))

    def test_r16_15_01_stroke_eth_summary_governed(self):
        self._candidate_governed(_bad("Trace summarise\u00f0"),
                                 _read("Trace summarise\u00f0"))

    # ------------------------------------------------------
    # R16-15-01 defect forms in the beside and gate ruling
    # positions, the B15-C01 heads in their beside
    # positions as carried
    # ------------------------------------------------------

    def test_r16_15_01_beside_summarisations_uncounted(self):
        self._beside_step2_uncounted(_bad("Trace summarisations"))

    def test_r16_15_01_beside_paneltally_uncounted(self):
        self._beside_step2_uncounted(_bad("Paneltally"))

    def test_r16_15_01_beside_c01_forward_uncounted(self):
        self._beside_step2_uncounted(
            _bad("Trace board gate annex review summary"))

    def test_r16_15_01_beside_c01_reversed_uncounted(self):
        self._beside_step2_uncounted(
            _bad("Summary board gate annex review trace"))

    def test_r16_15_01_beside_c01_for_step_uncounted(self):
        self._beside_step2_uncounted(
            _bad("Trace board gate annex for step 2"))

    def test_r16_15_01_gate_ruling_paneltally_governed(self):
        report = self._q4_alone(_bad("Paneltally"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # R16-15-01 defect forms at code level: the word tests
    # and the fused test standing in their cured reach
    # ------------------------------------------------------

    def test_code_level_new_fused_prefix_forms(self):
        for word in ("paneltally", "recordtally", "teamtally",
                     "paneltallies", "recordtallied",
                     "teamtallying", "gaterecordtally",
                     "gateboardtally", "reviewboardtally",
                     "boardboardtally"):
            self.assertTrue(_tally_word(_fold_word(word)), word)

    def test_code_level_variant_spellings(self):
        for word in ("boardtallyed", "boardtallyes",
                     "chairtallyed", "tallys", "tallyed"):
            self.assertTrue(_tally_word(_fold_word(word)), word)

    def test_code_level_summary_further_forms(self):
        for word in ("summarisations", "summarizations",
                     "summariser", "summarizer"):
            self.assertTrue(_summary_word(_fold_word(word)), word)

    def test_code_level_fused_further_forms(self):
        for word in ("boardtracesummarisations",
                     "boardtracesummariser", "traceboardsummary",
                     "summaryboardtrace", "boardtracegatesummary"):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)

    # ------------------------------------------------------
    # Held controls: the other item of the pass standing
    # as Unit 1 left it, its prose runs taking no tally
    # statement head in any position, and prose at the
    # counts this unit widens to standing missing where a
    # prose joining word stands among its inserted words
    # ------------------------------------------------------

    def test_held_prose_summary_of_board_trace_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary of the board trace")))

    def test_held_prose_summary_of_the_trace_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary of the trace")))

    def test_held_prose_trace_of_board_summary_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace of the board summary")))

    def test_held_prose_gate_ruling_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary of the board trace"), ruling=True))

    def test_held_prose_beside_step2_nowhere(self):
        self._beside_step2_nowhere(
            _prose("Summary of the board trace"))

    def test_held_bounding_panel_board_gate_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary of the panel board gate trace")))

    def test_held_prose_four_forward_joining_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace of the board gate summary")))

    def test_held_prose_four_reversed_joining_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary of the board gate review trace")))

    def test_held_prose_for_step_joining_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace of the board gate for step 2")))

    # ------------------------------------------------------
    # Held controls: every governed inserted closing at
    # the counts the boundary admitted entering this unit
    # standing governed, and the governed trace summary
    # forms standing governed
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

    def test_governed_trace_summary_plain(self):
        self._candidate_governed(_bad("Trace summary"),
                                 _read("Trace summary"))

    def test_governed_summary_trace_reversed(self):
        self._candidate_governed(_bad("Summary trace"),
                                 _read("Summary trace"))

    # ------------------------------------------------------
    # Held controls: the governed fused forms, the exact
    # word sets as fix pass 14 and Unit 1 left them, the
    # enumerated family, tallyho and the fused family
    # forms
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

    def test_code_level_boardtallys_variant_governed(self):
        self.assertTrue(_tally_word(_fold_word("boardtallys")))

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
