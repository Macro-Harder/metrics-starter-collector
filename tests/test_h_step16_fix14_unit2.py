"""Step 16 fix pass 14 unit 2 tests: the Q-4 tally head unit.

Pinning tests for register item R16-14-01 (Medium, B14-01
and B14-C02 merged) of Step 16 round 14. The governing
rule of the pass, in its extended form: a piece not read
in full, for whatever reason, is not read, and its
converse: a piece that is no feeder flips nothing.

R16-14-01: malformed tally statement heads stand missing
past the restated enumeration reach of fix pass 13 as
fix pass 14 Unit 1 left it, while their counted siblings
count under the same heads, because _trace_candidates
counts the numeric tally pattern with no head test at
all. Sixteen alone forms stand in eight subfamilies:
(a) the summary word in its ing forms, Trace summarising
and Trace summarizing; (b) the summary word in its ation
forms, Trace summarisation and Trace summarization;
(c) the fused trace summary closings in the ing and
ation forms, Boardtracesummarising and
Boardtracesummarization; (d) the fused trace summary
closings with the plural trace word in the forward
order, Tracessummary and Boardtracessummaries; (e) the
inserted word closings past the widened reach, Trace
board gate review summary, Summary board gate trace,
Summary board gate review trace, and Trace board gate
annex summary, the B14-C02 form folded into this
subfamily; (f) the for step closing past the widened
inserted reach, Trace board gate for step 2; (g) the
tally word in its variant plural spelling, Boardtallys;
(h) the further stroke letters, Board ta\u019aly and
Trace summarise\u0111. The beside forms stand driven in
the Trace summarising head and in the Trace board gate
annex summary head, and the gate ruling form in the
Trace summarizing head. Locus: derivation_core.py,
_fold_word, _tally_word and its constants, _summary_word
and its constant, _fused_trace_summary, and the closing
tests of _tally_statement_head. The cure these tests pin
widens the reach to take every form of the item, in its
driven positions, and restates the boundary: the summary
word stands in its ing and ation forms in both spelling
families beside its enumerated forms, the fused trace
summary closing stands built on those forms and on the
plural trace word in the forward order, the inserted
word closing stands with three words between the trace
word and the summary word in the forward order and with
two or three words between them in the reversed order,
the for step closing stands with two words between the
trace word and the for step words, the tally word stands
in its variant plural spelling tallys behind a governed
fused prefix alone, and the folding folds the further
stroke letters \u019a to l and \u0111 to d beside the
two it already folds. The widening stands on the tally
and summary word forms and on the closing limbs, and
widens no fused limb admission that R16-14-02 stands
against: the tally word fused limb stands closed on the
governed fused prefixes of fix pass 14 Unit 1, so no
prose adverb of the tal family takes a tally statement
head through any limb this unit widens.

Held controls stand pinned beside the defect forms, in
full: the twelve alone forms of R16-14-02 standing
missing exactly as Unit 1 cured them; the governed fused
forms standing governed; the exact word sets standing as
restated by Unit 1; the seven enumerated family adverbs
and tallyho standing missing; the fused family forms
subtotally and semirectally standing missing; the Board
tall\u00ed boundary control standing missing; the folded
round 10 prose sentence record standing governed; the
four folded marker shape records standing present but
not derivable; the golden prose lines standing
unflipped; the settled prose position; and the run
closure limb.
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


class TestStep16Fix14Unit2(FixtureTestCase):

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

    def _beside_governed(self, head):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=_bad(head))
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        q4 = row_block(self._run(files), "Q-4")
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    # ------------------------------------------------------
    # R16-14-01 defect forms: the sixteen alone forms in
    # eight subfamilies, each standing governed beside a
    # counted sibling counting 2 of 2 LANDED under the
    # same head, with the beside and gate ruling forms
    # ------------------------------------------------------

    def test_r16_14_01_summary_summarising_governed(self):
        self._candidate_governed(_bad("Trace summarising"),
                                 _read("Trace summarising"))

    def test_r16_14_01_summary_summarizing_governed(self):
        self._candidate_governed(_bad("Trace summarizing"),
                                 _read("Trace summarizing"))

    def test_r16_14_01_summary_summarisation_governed(self):
        self._candidate_governed(_bad("Trace summarisation"),
                                 _read("Trace summarisation"))

    def test_r16_14_01_summary_summarization_governed(self):
        self._candidate_governed(_bad("Trace summarization"),
                                 _read("Trace summarization"))

    def test_r16_14_01_fused_tracesummarising_governed(self):
        self._candidate_governed(_bad("Boardtracesummarising"),
                                 _read("Boardtracesummarising"))

    def test_r16_14_01_fused_tracesummarization_governed(self):
        self._candidate_governed(_bad("Boardtracesummarization"),
                                 _read("Boardtracesummarization"))

    def test_r16_14_01_fused_tracessummary_governed(self):
        self._candidate_governed(_bad("Tracessummary"),
                                 _read("Tracessummary"))

    def test_r16_14_01_fused_boardtracessummaries_governed(self):
        self._candidate_governed(_bad("Boardtracessummaries"),
                                 _read("Boardtracessummaries"))

    def test_r16_14_01_inserted_three_words_governed(self):
        self._candidate_governed(
            _bad("Trace board gate review summary"),
            _read("Trace board gate review summary"))

    def test_r16_14_01_inserted_two_words_reversed_governed(self):
        self._candidate_governed(_bad("Summary board gate trace"),
                                 _read("Summary board gate trace"))

    def test_r16_14_01_inserted_three_words_reversed_governed(self):
        self._candidate_governed(
            _bad("Summary board gate review trace"),
            _read("Summary board gate review trace"))

    def test_r16_14_01_inserted_annex_summary_governed(self):
        self._candidate_governed(
            _bad("Trace board gate annex summary"),
            _read("Trace board gate annex summary"))

    def test_r16_14_01_for_step_two_inserted_governed(self):
        self._candidate_governed(_bad("Trace board gate for step 2"),
                                 _read("Trace board gate for step 2"))

    def test_r16_14_01_tallys_variant_spelling_governed(self):
        self._candidate_governed(_bad("Boardtallys"),
                                 _read("Boardtallys"))

    def test_r16_14_01_stroke_letter_l_bar_governed(self):
        self._candidate_governed(_bad("Board ta\u019aly"),
                                 _read("Board ta\u019aly"))

    def test_r16_14_01_stroke_letter_d_summary_governed(self):
        self._candidate_governed(_bad("Trace summarise\u0111"),
                                 _read("Trace summarise\u0111"))

    def test_r16_14_01_summary_summarising_beside_uncounted(self):
        self._beside_governed("Trace summarising")

    def test_r16_14_01_inserted_annex_summary_beside_uncounted(self):
        self._beside_governed("Trace board gate annex summary")

    def test_r16_14_01_summary_summarizing_gate_ruling_governed(self):
        report = self._q4_alone(_bad("Trace summarizing"),
                                ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # Held controls: R16-14-02 stands in its Unit 1 cured
    # form in full, its twelve alone forms standing
    # missing, none of them cured or widened against here
    # ------------------------------------------------------

    def test_r16_14_02_held_prose_brutally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The blow landed brutally")))

    def test_r16_14_02_held_prose_capitally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The fund grew capitally")))

    def test_r16_14_02_held_prose_vitally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was checked vitally")))

    def test_r16_14_02_held_prose_fatally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The blow landed fatally")))

    def test_r16_14_02_held_prose_prenatally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was taken prenatally")))

    def test_r16_14_02_held_prose_neonatally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The unit cared for infants neonatally")))

    def test_r16_14_02_held_prose_mortally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The figure was wounded mortally")))

    def test_r16_14_02_held_prose_frontally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was taken frontally")))

    def test_r16_14_02_held_prose_dentally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The tooth was examined dentally")))

    def test_r16_14_02_held_prose_distally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The limb was measured distally")))

    def test_r16_14_02_held_prose_horizontally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The line extended horizontally")))

    def test_r16_14_02_held_prose_coastally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The route was charted coastally")))

    # ------------------------------------------------------
    # Held controls: the governed fused forms stand
    # governed beside their counted siblings, and the
    # exact word sets stand as restated by Unit 1, with
    # the variant plural spelling standing as the tally
    # word behind a governed fused prefix alone
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

    def test_r16_14_code_level_exact_word_sets(self):
        for word in ("tally", "tallies", "tallied", "tallying"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ("summary", "summaries", "summarise",
                     "summarised", "summarises", "summarize",
                     "summarizes", "summarized"):
            self.assertTrue(_summary_word(_fold_word(word)), word)

    def test_r16_14_code_level_tallys_variant_governed_prefix_only(self):
        self.assertTrue(_tally_word(_fold_word("boardtallys")))
        self.assertFalse(_tally_word(_fold_word("tallys")))

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
                     "semirectally", "brutally", "capitally",
                     "vitally", "fatally", "prenatally",
                     "neonatally", "mortally", "frontally",
                     "dentally", "distally", "horizontally",
                     "coastally"):
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
