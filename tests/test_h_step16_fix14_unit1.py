"""Step 16 fix pass 14 unit 1 tests: the Q-4 tally word unit.

Pinning tests for register item R16-14-02 (Medium, B14-02
and B14-C01 merged) of Step 16 round 14. The governing
rule of the pass, in its extended form: a piece not read
in full, for whatever reason, is not read, and its
converse: a piece that is no feeder flips nothing.

R16-14-02: ordinary prose adverbs of the totally family
shape standing unnamed in the enumerated _TOTALLY_FAMILY
take a tally statement head through the fused limb of
the restated _tally_word test, so a prose line closing
on such a word stands present but not derivable, a
feeder statement standing falsely claimed over a line
that is no feeder. Twelve distinct alone forms stand in
the union of the two round 14 papers: brutally,
capitally, vitally, fatally, prenatally, neonatally,
mortally, frontally, dentally, distally, horizontally
and coastally, the fatally form also driven in a Step 2
gate ruling and beside a counted Step 3 gate trace, and
the correctness paper driving its six forms (brutally,
capitally, vitally, fatally, prenatally and neonatally)
at code level against the pushed _tally_word itself.
Locus: derivation_core.py, _tally_word, read through
_tally_statement_head. The cure these tests pin narrows
what the tally word is, in its exact and governed fused
forms: a word stands as the tally word only where it is
one of the exact word forms, tally, tallies, tallied or
tallying, or where it ends with one of those same forms
behind one of the governed fused prefixes the earlier
cures govern, alpha, board, chair, gate2, green, pass,
review and step2, so no ordinary prose adverb of the
tal family shape stands as the tally word in any limb,
in any position, while every governed fused form keeps
standing governed and the exact word set stands
untouched.

Held controls stand pinned beside the defect forms, in
full: the sixteen alone forms of R16-14-01 standing
missing exactly as they enter, with their beside and
gate ruling forms, this unit curing none of them; the
governed fused forms standing governed, Boardtally,
Gate2tally, Reviewtally, Step2tally, Passtally,
Chairtally, Greentally, Alphatally, Boardtallied,
Boardtallies and Boardtallying among them; the exact
word set standing as the tally word; the seven
enumerated family adverbs and tallyho standing missing;
the fused family forms subtotally and semirectally
standing missing; the Board talli boundary control
standing missing; the folded round 10 prose sentence
record standing governed; the four folded marker shape
records standing present but not derivable; the golden
prose lines standing unflipped; the settled prose
position; and the run closure limb.
"""
from metrics_starter_collector.derivation_core import (
    _fold_word, _tally_word)
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


class TestStep16Fix14Unit1(FixtureTestCase):

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
    # R16-14-02 defect forms: the twelve prose adverbs of
    # the two round 14 papers, each closing a prose line
    # on a colon, standing missing after the cure
    # ------------------------------------------------------

    def test_r16_14_02_prose_brutally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The blow landed brutally")))

    def test_r16_14_02_prose_fatally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The blow landed fatally")))

    def test_r16_14_02_prose_vitally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was checked vitally")))

    def test_r16_14_02_prose_mortally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The figure was wounded mortally")))

    def test_r16_14_02_prose_frontally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was taken frontally")))

    def test_r16_14_02_prose_dentally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The tooth was examined dentally")))

    def test_r16_14_02_prose_distally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The limb was measured distally")))

    def test_r16_14_02_prose_horizontally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The line extended horizontally")))

    def test_r16_14_02_prose_coastally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The route was charted coastally")))

    def test_r16_14_02_prose_capitally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The fund grew capitally")))

    def test_r16_14_02_prose_prenatally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was taken prenatally")))

    def test_r16_14_02_prose_neonatally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The unit cared for infants neonatally")))

    def test_r16_14_02_prose_brutally_correctness_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The board spoke brutally")))

    def test_r16_14_02_prose_vitally_correctness_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The notes were kept vitally")))

    def test_r16_14_02_prose_fatally_correctness_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The driver was injured fatally")))

    def test_r16_14_02_prose_fatally_gate_ruling_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The blow landed fatally"), ruling=True))

    def test_r16_14_02_prose_fatally_beside_nowhere(self):
        files = _clean_files()
        files[GATE_2] = gate_record(
            2, extra=_prose("The blow landed fatally"))
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)

    def test_r16_14_02_code_level_correctness_six_no_tally_word(self):
        for word in ("brutally", "capitally", "vitally", "fatally",
                     "prenatally", "neonatally"):
            self.assertFalse(_tally_word(_fold_word(word)), word)

    def test_r16_14_02_code_level_breaker_six_no_tally_word(self):
        for word in ("mortally", "frontally", "dentally", "distally",
                     "horizontally", "coastally"):
            self.assertFalse(_tally_word(_fold_word(word)), word)

    # ------------------------------------------------------
    # Held controls: R16-14-01 stands in its entering
    # behaviour in full, its sixteen alone forms standing
    # missing beside their counted siblings, its beside
    # form dropping the step unnamed, and its gate ruling
    # form standing missing, none of them cured here
    # ------------------------------------------------------

    def test_r16_14_01_held_summary_summarising_missing(self):
        self._candidate_missing(_bad("Trace summarising"),
                                _read("Trace summarising"))

    def test_r16_14_01_held_summary_summarizing_missing(self):
        self._candidate_missing(_bad("Trace summarizing"),
                                _read("Trace summarizing"))

    def test_r16_14_01_held_summary_summarisation_missing(self):
        self._candidate_missing(_bad("Trace summarisation"),
                                _read("Trace summarisation"))

    def test_r16_14_01_held_summary_summarization_missing(self):
        self._candidate_missing(_bad("Trace summarization"),
                                _read("Trace summarization"))

    def test_r16_14_01_held_fused_tracesummarising_missing(self):
        self._candidate_missing(_bad("Boardtracesummarising"),
                                _read("Boardtracesummarising"))

    def test_r16_14_01_held_fused_tracesummarization_missing(self):
        self._candidate_missing(_bad("Boardtracesummarization"),
                                _read("Boardtracesummarization"))

    def test_r16_14_01_held_fused_tracessummary_missing(self):
        self._candidate_missing(_bad("Tracessummary"),
                                _read("Tracessummary"))

    def test_r16_14_01_held_fused_boardtracessummaries_missing(self):
        self._candidate_missing(_bad("Boardtracessummaries"),
                                _read("Boardtracessummaries"))

    def test_r16_14_01_held_inserted_three_words_missing(self):
        self._candidate_missing(
            _bad("Trace board gate review summary"),
            _read("Trace board gate review summary"))

    def test_r16_14_01_held_inserted_two_words_reversed_missing(self):
        self._candidate_missing(_bad("Summary board gate trace"),
                                _read("Summary board gate trace"))

    def test_r16_14_01_held_inserted_three_words_reversed_missing(self):
        self._candidate_missing(
            _bad("Summary board gate review trace"),
            _read("Summary board gate review trace"))

    def test_r16_14_01_held_for_step_two_inserted_missing(self):
        self._candidate_missing(_bad("Trace board gate for step 2"),
                                _read("Trace board gate for step 2"))

    def test_r16_14_01_held_tallys_variant_spelling_missing(self):
        self._candidate_missing(_bad("Boardtallys"),
                                _read("Boardtallys"))

    def test_r16_14_01_held_stroke_letter_l_bar_missing(self):
        self._candidate_missing(_bad("Board ta\u019aly"),
                                _read("Board ta\u019aly"))

    def test_r16_14_01_held_stroke_letter_d_summary_missing(self):
        self._candidate_missing(_bad("Trace summarise\u0111"),
                                _read("Trace summarise\u0111"))

    def test_r16_14_01_held_inserted_annex_summary_missing(self):
        self._candidate_missing(
            _bad("Trace board gate annex summary"),
            _read("Trace board gate annex summary"))

    def test_r16_14_01_held_summary_summarising_beside_nowhere(self):
        files = _clean_files()
        files[GATE_2] = gate_record(
            2, extra=_bad("Trace summarising"))
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)

    def test_r16_14_01_held_summary_summarizing_gate_ruling_missing(self):
        report = self._q4_alone(_bad("Trace summarizing"),
                                ruling=True)
        self._assert_q4_missing(report)

    # ------------------------------------------------------
    # Held controls: the governed fused forms stand
    # governed beside their counted siblings, and the
    # exact word set stands as the tally word
    # ------------------------------------------------------

    def test_r16_14_governed_fused_boardtally(self):
        self._candidate_governed(_bad("Boardtally"),
                                 _read("Boardtally"))

    def test_r16_14_governed_fused_gate2tally(self):
        self._candidate_governed(_bad("Gate2tally"),
                                 _read("Gate2tally"))

    def test_r16_14_governed_fused_reviewtally(self):
        self._candidate_governed(_bad("Reviewtally"),
                                 _read("Reviewtally"))

    def test_r16_14_governed_fused_step2tally(self):
        self._candidate_governed(_bad("Step2tally"),
                                 _read("Step2tally"))

    def test_r16_14_governed_fused_passtally(self):
        self._candidate_governed(_bad("Passtally"),
                                 _read("Passtally"))

    def test_r16_14_governed_fused_chairtally(self):
        self._candidate_governed(_bad("Chairtally"),
                                 _read("Chairtally"))

    def test_r16_14_governed_fused_greentally(self):
        self._candidate_governed(_bad("Greentally"),
                                 _read("Greentally"))

    def test_r16_14_governed_fused_alphatally(self):
        self._candidate_governed(_bad("Alphatally"),
                                 _read("Alphatally"))

    def test_r16_14_governed_fused_boardtallied(self):
        self._candidate_governed(_bad("Boardtallied"),
                                 _read("Boardtallied"))

    def test_r16_14_governed_fused_boardtallies(self):
        self._candidate_governed(_bad("Boardtallies"),
                                 _read("Boardtallies"))

    def test_r16_14_governed_fused_boardtallying(self):
        self._candidate_governed(_bad("Boardtallying"),
                                 _read("Boardtallying"))

    def test_r16_14_code_level_governed_fused_forms(self):
        for word in ("boardtally", "gate2tally", "reviewtally",
                     "step2tally", "passtally", "chairtally",
                     "greentally", "alphatally", "boardtallied",
                     "boardtallies", "boardtallying"):
            self.assertTrue(_tally_word(_fold_word(word)), word)

    def test_r16_14_code_level_exact_word_set(self):
        for word in ("tally", "tallies", "tallied", "tallying"):
            self.assertTrue(_tally_word(_fold_word(word)), word)

    # ------------------------------------------------------
    # Held controls: the enumerated family, tallyho and
    # the fused family forms stand missing, at row level
    # and at code level
    # ------------------------------------------------------

    def test_r16_14_held_prose_totally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The figures stand totally")))

    def test_r16_14_held_prose_accidentally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The count was checked accidentally")))

    def test_r16_14_held_prose_digitally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The results were recorded digitally")))

    def test_r16_14_held_prose_incidentally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The figures changed incidentally")))

    def test_r16_14_held_prose_mentally_dot_missing(self):
        line = ("The board reasoned mentally. LANDED figures "
                "stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_14_held_prose_rectally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The results were recorded rectally")))

    def test_r16_14_held_prose_septally_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was taken septally")))

    def test_r16_14_held_prose_tallyho_colon_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The dawn cry was tallyho")))

    def test_r16_14_code_level_family_and_tallyho_no_tally_word(self):
        for word in ("totally", "accidentally", "digitally",
                     "incidentally", "mentally", "rectally",
                     "septally", "tallyho", "subtotally",
                     "semirectally", "boardtallys"):
            self.assertFalse(_tally_word(_fold_word(word)), word)

    def test_r16_14_held_fused_subtotally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The count was taken subtotally")))

    def test_r16_14_held_fused_semirectally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The count was taken semirectally")))

    # ------------------------------------------------------
    # Held controls: the Board talli boundary control, the
    # folded records, the golden lines, and the settled
    # positions
    # ------------------------------------------------------

    def test_r16_14_held_closing_talli_different_word_missing(self):
        self._candidate_missing(_bad("Board tall\u00ed"),
                                _read("Board tall\u00ed"))

    def test_r16_14_held_prose_sentence_closing_on_tally(self):
        line = ("Record the board tally. LANDED figures stand "
                "here, no counts stated")
        self._assert_q4_governed(self._q4_alone(line))

    def test_r16_14_held_marker_nested_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("((1)) ", "Board tally")))

    def test_r16_14_held_marker_spaced_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("(a b) ", "Board tally")))

    def test_r16_14_held_marker_empty_paren_governed(self):
        self._assert_q4_governed(self._q4_alone(
            _dot_form("() ", "Board tally")))

    def test_r16_14_held_marker_brace_token_governed(self):
        self._assert_q4_governed(self._q4_alone(
            "{1} " + _bad("Board tally")))

    def test_r16_14_held_golden_board_line_missing(self):
        self._assert_q4_missing(self._q4_alone(GOLDEN_BOARD_LINE))

    def test_r16_14_held_golden_closing_line_missing(self):
        self._assert_q4_missing(self._q4_alone(GOLDEN_CLOSING_LINE))

    def test_r16_14_held_prose_fragment_no_head_missing(self):
        line = ("A malformed fragment stands in prose position "
                "here. LANDED figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_14_held_closure_run_past_tally_colon(self):
        line = ("Board tally, and its figures stand here: LANDED "
                "figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_14_held_closure_run_past_summary_dot(self):
        line = ("Trace summary of the board stands here. LANDED "
                "figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_14_held_trace_for_step_alphanumeric_missing(self):
        line = ("Trace for step 2a: items checked stand here. "
                "LANDED figures stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

    def test_r16_14_held_read_control_byte_for_byte(self):
        files = _clean_files()
        for step, trace in ((2, TRACE_2), (3, TRACE_3)):
            files["steps/step-%02d-gate-record.md" % step] = \
                gate_record(step, extra=trace)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_14_held_absent_feeder_byte_for_byte(self):
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
