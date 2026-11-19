"""Step 16 fix pass 16 unit 2 tests: the Q-4 tally head unit.

Pinning tests for register item R16-16-01 (Medium, B16-01
with B16-C01, B16-C02, B16-C03, B16-C04, B16-C05 and
B16-C06 merged) of Step 16 round 16. The governing rule
of the pass, in its extended form: a piece not read in
full, for whatever reason, is not read, and its
converse: a piece that is no feeder flips nothing.

R16-16-01: malformed tally statement heads the restated
boundary of fix pass 15 still does not reach, in forty
four distinct alone forms in nine subfamilies, each
standing missing in the entering behaviour where the
counted pattern admits it, on the counted pattern head
agnosticism ground alone in every subfamily: (a) fused
heads on record words the widened enumeration does not
name, Ledgertally, Rostertally, Registertally,
Dockettallies, Journaltallied, Censustallying,
Committeetally, Counciltallies and Workgrouptally;
(b) variant spellings in the further position,
Gateboardtallyed, Reviewboardtallys and
Gateboardtallyes; (c) variant spellings past tallys and
tallyed, Tallyes, Talley, Talleys and Talleyed standing
alone, and Boardtalley, Boardtallyies and Chairtalleyed
behind governed prefixes, the Tallyes alone form
entering on the counted pattern ground alone against
the express standalone exclusion in the restated
boundary, on the register15 Tallys alone precedent;
(d) summary forms past the sixteen, Trace summarisers,
Trace summarizers, Trace summarisings and Trace
summarys; (e) fused closings on those forms,
Boardtracesummarisers, Boardtracesummarizers,
Tracesummarisers and Boardtracessummarisers; (f) fused
closings with further words fused between, and the
plural trace word in the fused between form,
Traceboardgatesummary, Traceboardgatepanelsummary,
Summaryboardgatetrace, Tracesboardsummary and
Summaryboardtraces; (g) inserted closings past five
words forward and four reversed, every inserted word
governed and standing in record order, six inserted
words forward in two forms and five inserted words
reversed; (h) the for step closing past four inserted
words, five and six inserted words; and (i) further
stroke and hook letters past the fold widened set, the
letters \u026b, \u01ad, \u0282, \u0271, \u0289 and
\u0257 in the driven positions, and the thorn letter
form Trace summarise\u00fe. The beside forms stand
driven in the Ledgertally head and in the Trace
summarisers head, and the gate ruling form in the
Ledgertally head. Locus: derivation_core.py, _fold_word,
_tally_word and its constants, _summary_word and its
constant, _fused_trace_summary, and _tally_statement_head
and its closing tests, against _trace_candidates and
the shared constant _TALLY_COUNTED_PATTERN, which
carries no head test. The cure these tests pin widens
the reach to take every form of the item, in its driven
positions, and restates the boundary it extends,
including the prefix question at its new width and the
tallyes alone position, under the inserted closing test
as fix pass 16 Unit 1 restated it, so the widening at
the inserted and for step counts widens no converse
admission of R16-16-02.

Held controls stand pinned beside the defect forms, in
full: the other item of the pass standing as Unit 1
left it, the prose order runs and the prose sentences
closing on a colon taking no tally statement head in
any position, alone, beside, and in gate rulings, its
bounding controls standing missing, and prose at the
counts this unit widens to standing missing where its
inserted words stand out of record order or its closing
stands as the tail of a prose sentence; every governed
closing standing governed alone, beside, and in gate
rulings at every admitted count; the governed forms
standing governed, the exact word sets as fix pass 15
and Unit 1 left them, the governed fused forms and the
governed trace summary forms; the seven enumerated
family adverbs and tallyho standing missing; the fused
family forms subtotally and semirectally standing
missing; the Board tall\u00ed boundary control standing
missing; the folded round 10 prose sentence record
standing governed; and the four folded marker shape
records standing present but not derivable.
"""
from metrics_starter_collector.derivation_core import (
    _fold_word, _fused_trace_summary, _inserted_words_governed,
    _summary_word, _tally_statement_head, _tally_word)
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


class TestStep16Fix16Unit2(FixtureTestCase):

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
    # R16-16-01 defect forms, subfamily (a): fused heads
    # on record words the widened enumeration does not
    # name, alone, each standing governed beside its
    # counted sibling
    # ------------------------------------------------------

    def test_r16_16_01_fused_ledgertally_governed(self):
        self._candidate_governed(_bad("Ledgertally"),
                                 _read("Ledgertally"))

    def test_r16_16_01_fused_rostertally_governed(self):
        self._candidate_governed(_bad("Rostertally"),
                                 _read("Rostertally"))

    def test_r16_16_01_fused_registertally_governed(self):
        self._candidate_governed(_bad("Registertally"),
                                 _read("Registertally"))

    def test_r16_16_01_fused_dockettallies_governed(self):
        self._candidate_governed(_bad("Dockettallies"),
                                 _read("Dockettallies"))

    def test_r16_16_01_fused_journaltallied_governed(self):
        self._candidate_governed(_bad("Journaltallied"),
                                 _read("Journaltallied"))

    def test_r16_16_01_fused_censustallying_governed(self):
        self._candidate_governed(_bad("Censustallying"),
                                 _read("Censustallying"))

    def test_r16_16_01_fused_committeetally_governed(self):
        self._candidate_governed(_bad("Committeetally"),
                                 _read("Committeetally"))

    def test_r16_16_01_fused_counciltallies_governed(self):
        self._candidate_governed(_bad("Counciltallies"),
                                 _read("Counciltallies"))

    def test_r16_16_01_fused_workgrouptally_governed(self):
        self._candidate_governed(_bad("Workgrouptally"),
                                 _read("Workgrouptally"))

    # ------------------------------------------------------
    # R16-16-01 defect forms, subfamily (b): the variant
    # spellings in the further position
    # ------------------------------------------------------

    def test_r16_16_01_variant_further_gateboardtallyed_governed(self):
        self._candidate_governed(_bad("Gateboardtallyed"),
                                 _read("Gateboardtallyed"))

    def test_r16_16_01_variant_further_reviewboardtallys_governed(self):
        self._candidate_governed(_bad("Reviewboardtallys"),
                                 _read("Reviewboardtallys"))

    def test_r16_16_01_variant_further_gateboardtallyes_governed(self):
        self._candidate_governed(_bad("Gateboardtallyes"),
                                 _read("Gateboardtallyes"))

    # ------------------------------------------------------
    # R16-16-01 defect forms, subfamily (c): the variant
    # spellings past tallys and tallyed, standing alone
    # and behind governed prefixes
    # ------------------------------------------------------

    def test_r16_16_01_variant_tallyes_alone_governed(self):
        self._candidate_governed(_bad("Tallyes"),
                                 _read("Tallyes"))

    def test_r16_16_01_variant_talley_alone_governed(self):
        self._candidate_governed(_bad("Talley"),
                                 _read("Talley"))

    def test_r16_16_01_variant_talleys_alone_governed(self):
        self._candidate_governed(_bad("Talleys"),
                                 _read("Talleys"))

    def test_r16_16_01_variant_talleyed_alone_governed(self):
        self._candidate_governed(_bad("Talleyed"),
                                 _read("Talleyed"))

    def test_r16_16_01_variant_boardtalley_governed(self):
        self._candidate_governed(_bad("Boardtalley"),
                                 _read("Boardtalley"))

    def test_r16_16_01_variant_boardtallyies_governed(self):
        self._candidate_governed(_bad("Boardtallyies"),
                                 _read("Boardtallyies"))

    def test_r16_16_01_variant_chairtalleyed_governed(self):
        self._candidate_governed(_bad("Chairtalleyed"),
                                 _read("Chairtalleyed"))

    # ------------------------------------------------------
    # R16-16-01 defect forms, subfamily (d): the summary
    # word in further forms past the sixteen
    # ------------------------------------------------------

    def test_r16_16_01_summary_summarisers_governed(self):
        self._candidate_governed(_bad("Trace summarisers"),
                                 _read("Trace summarisers"))

    def test_r16_16_01_summary_summarizers_governed(self):
        self._candidate_governed(_bad("Trace summarizers"),
                                 _read("Trace summarizers"))

    def test_r16_16_01_summary_summarisings_governed(self):
        self._candidate_governed(_bad("Trace summarisings"),
                                 _read("Trace summarisings"))

    def test_r16_16_01_summary_summarys_governed(self):
        self._candidate_governed(_bad("Trace summarys"),
                                 _read("Trace summarys"))

    # ------------------------------------------------------
    # R16-16-01 defect forms, subfamily (e): the fused
    # trace summary closings built on those forms
    # ------------------------------------------------------

    def test_r16_16_01_fused_boardtracesummarisers_governed(self):
        self._candidate_governed(_bad("Boardtracesummarisers"),
                                 _read("Boardtracesummarisers"))

    def test_r16_16_01_fused_boardtracesummarizers_governed(self):
        self._candidate_governed(_bad("Boardtracesummarizers"),
                                 _read("Boardtracesummarizers"))

    def test_r16_16_01_fused_tracesummarisers_governed(self):
        self._candidate_governed(_bad("Tracesummarisers"),
                                 _read("Tracesummarisers"))

    def test_r16_16_01_fused_boardtracessummarisers_governed(self):
        self._candidate_governed(_bad("Boardtracessummarisers"),
                                 _read("Boardtracessummarisers"))

    # ------------------------------------------------------
    # R16-16-01 defect forms, subfamily (f): the fused
    # closings with further words fused between, and the
    # plural trace word in the fused between form
    # ------------------------------------------------------

    def test_r16_16_01_between_traceboardgatesummary_governed(self):
        self._candidate_governed(_bad("Traceboardgatesummary"),
                                 _read("Traceboardgatesummary"))

    def test_r16_16_01_between_traceboardgatepanelsummary_governed(self):
        self._candidate_governed(_bad("Traceboardgatepanelsummary"),
                                 _read("Traceboardgatepanelsummary"))

    def test_r16_16_01_between_summaryboardgatetrace_governed(self):
        self._candidate_governed(_bad("Summaryboardgatetrace"),
                                 _read("Summaryboardgatetrace"))

    def test_r16_16_01_between_tracesboardsummary_governed(self):
        self._candidate_governed(_bad("Tracesboardsummary"),
                                 _read("Tracesboardsummary"))

    def test_r16_16_01_between_summaryboardtraces_governed(self):
        self._candidate_governed(_bad("Summaryboardtraces"),
                                 _read("Summaryboardtraces"))

    # ------------------------------------------------------
    # R16-16-01 defect forms, subfamily (g): the inserted
    # word closings past the widened reach, every
    # inserted word governed and standing in record order
    # ------------------------------------------------------

    def test_r16_16_01_inserted_six_forward_board_governed(self):
        self._candidate_governed(_bad("Trace board gate review annex panel board summary"),
                                 _read("Trace board gate review annex panel board summary"))

    def test_r16_16_01_inserted_six_forward_gate_governed(self):
        self._candidate_governed(_bad("Trace board gate review annex panel gate summary"),
                                 _read("Trace board gate review annex panel gate summary"))

    def test_r16_16_01_inserted_five_reversed_governed(self):
        self._candidate_governed(_bad("Summary board gate review annex panel trace"),
                                 _read("Summary board gate review annex panel trace"))

    # ------------------------------------------------------
    # R16-16-01 defect forms, subfamily (h): the for step
    # closing past four inserted words
    # ------------------------------------------------------

    def test_r16_16_01_for_step_five_inserted_governed(self):
        self._candidate_governed(_bad("Trace board gate review annex panel for step 2"),
                                 _read("Trace board gate review annex panel for step 2"))

    def test_r16_16_01_for_step_six_inserted_governed(self):
        self._candidate_governed(_bad("Trace board gate review annex panel board for step 2"),
                                 _read("Trace board gate review annex panel board for step 2"))

    # ------------------------------------------------------
    # R16-16-01 defect forms, subfamily (i): the further
    # stroke and hook letters past the widened fold set
    # ------------------------------------------------------

    def test_r16_16_01_stroke_l_tally_governed(self):
        self._candidate_governed(_bad("Board ta\u026bly"),
                                 _read("Board ta\u026bly"))

    def test_r16_16_01_stroke_t_tally_governed(self):
        self._candidate_governed(_bad("Board \u01adally"),
                                 _read("Board \u01adally"))

    def test_r16_16_01_stroke_s_summary_governed(self):
        self._candidate_governed(_bad("Trace \u0282ummarise"),
                                 _read("Trace \u0282ummarise"))

    def test_r16_16_01_stroke_m_summary_governed(self):
        self._candidate_governed(_bad("Trace su\u0271marise"),
                                 _read("Trace su\u0271marise"))

    def test_r16_16_01_stroke_u_summary_governed(self):
        self._candidate_governed(_bad("Trace s\u0289mmarise"),
                                 _read("Trace s\u0289mmarise"))

    def test_r16_16_01_stroke_d_summary_governed(self):
        self._candidate_governed(_bad("Trace summaris\u0257"),
                                 _read("Trace summaris\u0257"))

    def test_r16_16_01_thorn_summary_governed(self):
        self._candidate_governed(_bad("Trace summarise\u00fe"),
                                 _read("Trace summarise\u00fe"))

    # ------------------------------------------------------
    # R16-16-01 defect forms: the beside forms in the
    # Ledgertally head and in the Trace summarisers head,
    # and the gate ruling form in the Ledgertally head
    # ------------------------------------------------------

    def test_r16_16_01_beside_ledgertally_uncounted(self):
        self._beside_step2_uncounted(_bad("Ledgertally"))

    def test_r16_16_01_beside_summarisers_uncounted(self):
        self._beside_step2_uncounted(_bad("Trace summarisers"))

    def test_r16_16_01_gate_ruling_ledgertally_governed(self):
        report = self._q4_alone(_bad("Ledgertally"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # R16-16-01 defect forms at code level: the word
    # tests, the fused test, the inserted tests and the
    # fold standing in their cured reach
    # ------------------------------------------------------

    def test_code_level_new_fused_prefix_forms(self):
        for word in ("ledgertally", "rostertally",
                     "registertally", "dockettallies",
                     "journaltallied", "censustallying",
                     "committeetally", "counciltallies",
                     "workgrouptally"):
            self.assertTrue(_tally_word(_fold_word(word)), word)

    def test_code_level_variant_further_and_new_forms(self):
        for word in ("gateboardtallyed", "reviewboardtallys",
                     "gateboardtallyes", "boardtalley",
                     "boardtallyies", "chairtalleyed"):
            self.assertTrue(_tally_word(_fold_word(word)), word)

    def test_code_level_variant_alone_forms(self):
        for word in ("tallyes", "talley", "talleys", "talleyed"):
            self.assertTrue(_tally_word(_fold_word(word)), word)

    def test_code_level_summary_further_forms(self):
        for word in ("summarisers", "summarizers",
                     "summarisings", "summarys"):
            self.assertTrue(_summary_word(_fold_word(word)), word)

    def test_code_level_fused_further_forms(self):
        for word in ("boardtracesummarisers",
                     "boardtracesummarizers", "tracesummarisers",
                     "boardtracessummarisers",
                     "traceboardgatesummary",
                     "traceboardgatepanelsummary",
                     "summaryboardgatetrace", "tracesboardsummary",
                     "summaryboardtraces"):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)

    def test_code_level_inserted_widened_counts(self):
        self.assertTrue(_tally_statement_head(
            "Trace board gate review annex panel board summary: "
            "items checked stand here. LANDED figures stand "
            "here, no counts stated"))
        self.assertTrue(_tally_statement_head(
            "Summary board gate review annex panel trace: "
            "items checked stand here. LANDED figures stand "
            "here, no counts stated"))
        self.assertTrue(_tally_statement_head(
            "Trace board gate review annex panel for step 2: "
            "items checked stand here. LANDED figures stand "
            "here, no counts stated"))
        self.assertTrue(_tally_statement_head(
            "Trace board gate review annex panel board for "
            "step 2: items checked stand here. LANDED figures "
            "stand here, no counts stated"))

    def test_code_level_wide_order_prose_no_head(self):
        self.assertFalse(_tally_statement_head(
            "Trace review board gate annex panel board summary: "
            "items checked stand here. LANDED figures stand "
            "here, no counts stated"))
        self.assertFalse(_tally_statement_head(
            "Trace panel gate review annex panel board summary: "
            "items checked stand here. LANDED figures stand "
            "here, no counts stated"))
        self.assertFalse(_tally_statement_head(
            "Trace panel review board gate annex for step 2: "
            "items checked stand here. LANDED figures stand "
            "here, no counts stated"))

    def test_code_level_fold_further_letters(self):
        self.assertEqual(_fold_word("ta\u026bly"), "tally")
        self.assertEqual(_fold_word("\u01adally"), "tally")
        self.assertEqual(_fold_word("\u0282ummarise"), "summarise")
        self.assertEqual(_fold_word("su\u0271marise"), "summarise")
        self.assertEqual(_fold_word("s\u0289mmarise"), "summarise")
        self.assertEqual(_fold_word("summaris\u0257"), "summarised")
        self.assertEqual(_fold_word("summarise\u00fe"), "summarised")
    # ------------------------------------------------------
    # Held controls: the other item of the pass standing
    # as Unit 1 left it, its prose order runs taking no
    # tally statement head in any position
    # ------------------------------------------------------

    def test_r16_16_02_held_prose_order_forward_two_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace review board summary")))

    def test_r16_16_02_held_prose_order_forward_three_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace panel gate board summary")))

    def test_r16_16_02_held_prose_order_forward_four_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace annex panel gate board summary")))

    def test_r16_16_02_held_prose_order_forward_five_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace review annex panel gate board summary")))

    def test_r16_16_02_held_prose_order_reversed_two_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary review board trace")))

    def test_r16_16_02_held_prose_order_reversed_three_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary panel gate board trace")))

    def test_r16_16_02_held_prose_order_reversed_four_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary review annex panel gate trace")))

    def test_r16_16_02_held_prose_order_for_step_two_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace review board for step 2")))

    def test_r16_16_02_held_prose_order_for_step_three_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace panel gate board for step 2")))

    def test_r16_16_02_held_prose_order_for_step_four_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace annex panel gate board for step 2")))

    def test_r16_16_02_held_prose_order_gate_ruling_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace review board summary"), ruling=True))

    def test_r16_16_02_held_prose_order_beside_step2_nowhere(self):
        self._beside_step2_nowhere(
            _prose("Trace review board summary"))
    # ------------------------------------------------------
    # Held controls: the prose sentences of R16-16-02
    # closing on a colon taking no tally statement head
    # in any position, as Unit 1 left them
    # ------------------------------------------------------

    def test_r16_16_02_held_prose_sentence_reviewed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("We reviewed the trace board gate summary")))

    def test_r16_16_02_held_prose_sentence_filed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("She filed the summary board trace")))

    def test_r16_16_02_held_prose_sentence_for_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("For the trace board summary")))

    def test_r16_16_02_held_prose_sentence_of_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Of the summary board trace")))

    def test_r16_16_02_held_prose_sentence_panel_reviewed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The panel reviewed the trace gate summary")))

    def test_r16_16_02_held_prose_sentence_gate_ruling_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("We reviewed the trace board gate summary"),
            ruling=True))

    def test_r16_16_02_held_prose_sentence_beside_step2_nowhere(self):
        self._beside_step2_nowhere(
            _prose("We reviewed the trace board gate summary"))

    def test_r16_16_02_held_code_level_prose_order_not_governed(self):
        for words in (("review", "board"), ("panel", "gate", "board"),
                      ("annex", "panel", "gate", "board"),
                      ("review", "annex", "panel", "gate", "board")):
            self.assertFalse(_inserted_words_governed(
                [_fold_word(word) for word in words]), words)

    def test_r16_16_02_held_code_level_sentence_tail_no_head(self):
        self.assertFalse(_tally_statement_head(
            "We reviewed the trace board gate summary: LANDED "
            "figures stand here, no counts stated"))
        self.assertFalse(_tally_statement_head(
            "For the trace board summary: LANDED figures stand "
            "here, no counts stated"))
    # ------------------------------------------------------
    # Held controls: the bounding forms of R16-16-02, and
    # prose at the counts this unit widens to standing
    # missing where its inserted words stand out of
    # record order or its closing stands as the tail of
    # a prose sentence
    # ------------------------------------------------------

    def test_bounding_mixed_trace_board_of_summary_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace board of summary")))

    def test_bounding_mixed_summary_of_board_trace_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary of board trace")))

    def test_bounding_mixed_trace_of_board_gate_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace of board gate summary")))

    def test_bounding_mixed_summary_board_of_trace_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary board of the trace")))

    def test_bounding_mixed_trace_the_board_summary_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace the board summary")))

    def test_bounding_prose_order_past_reach_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Summary review annex panel gate board trace")))

    def test_bounding_prose_order_six_forward_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace review board gate annex panel board summary")))

    def test_bounding_prose_order_for_step_five_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Trace panel review board gate annex for step 2")))

    def test_bounding_prose_sentence_widened_count_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("We reviewed the trace board gate review annex panel board summary")))
    # ------------------------------------------------------
    # Held controls: every governed inserted closing
    # standing governed beside its counted sibling, in
    # record order, at every count the boundary admitted
    # entering this unit, and in the beside and gate
    # ruling positions
    # ------------------------------------------------------

    def test_governed_inserted_trace_board_summary(self):
        self._candidate_governed(_bad("Trace board summary"),
                                 _read("Trace board summary"))

    def test_governed_inserted_trace_board_gate_summary(self):
        self._candidate_governed(_bad("Trace board gate summary"),
                                 _read("Trace board gate summary"))

    def test_governed_inserted_trace_board_gate_review(self):
        self._candidate_governed(_bad("Trace board gate review summary"),
                                 _read("Trace board gate review summary"))

    def test_governed_inserted_trace_board_gate_annex(self):
        self._candidate_governed(_bad("Trace board gate annex summary"),
                                 _read("Trace board gate annex summary"))

    def test_governed_inserted_summary_board_trace(self):
        self._candidate_governed(_bad("Summary board trace"),
                                 _read("Summary board trace"))

    def test_governed_inserted_summary_board_gate_trace(self):
        self._candidate_governed(_bad("Summary board gate trace"),
                                 _read("Summary board gate trace"))

    def test_governed_inserted_summary_board_gate_review(self):
        self._candidate_governed(_bad("Summary board gate review trace"),
                                 _read("Summary board gate review trace"))

    def test_governed_inserted_summary_variant_form(self):
        self._candidate_governed(_bad("Trace board gate summarising"),
                                 _read("Trace board gate summarising"))

    def test_governed_inserted_inserted_four_forward(self):
        self._candidate_governed(_bad("Trace board gate review annex summary"),
                                 _read("Trace board gate review annex summary"))

    def test_governed_inserted_inserted_five_forward(self):
        self._candidate_governed(_bad("Trace board gate review annex panel summary"),
                                 _read("Trace board gate review annex panel summary"))

    def test_governed_inserted_inserted_four_reversed(self):
        self._candidate_governed(_bad("Summary board gate review annex trace"),
                                 _read("Summary board gate review annex trace"))

    def test_governed_inserted_inserted_annex_review(self):
        self._candidate_governed(_bad("Trace board gate annex review summary"),
                                 _read("Trace board gate annex review summary"))

    def test_governed_inserted_inserted_rev_annex_review(self):
        self._candidate_governed(_bad("Summary board gate annex review trace"),
                                 _read("Summary board gate annex review trace"))

    def test_governed_inserted_for_step_plain(self):
        self._candidate_governed(_bad("Trace for step 2"),
                                 _read("Trace for step 2"))

    def test_governed_inserted_for_step_one_inserted(self):
        self._candidate_governed(_bad("Trace board for step 2"),
                                 _read("Trace board for step 2"))

    def test_governed_inserted_for_step_two_inserted(self):
        self._candidate_governed(_bad("Trace board gate for step 2"),
                                 _read("Trace board gate for step 2"))

    def test_governed_inserted_for_step_three_inserted(self):
        self._candidate_governed(_bad("Trace board gate review for step 2"),
                                 _read("Trace board gate review for step 2"))

    def test_governed_inserted_for_step_four_inserted(self):
        self._candidate_governed(_bad("Trace board gate review annex for step 2"),
                                 _read("Trace board gate review annex for step 2"))

    def test_governed_inserted_for_step_annex_inserted(self):
        self._candidate_governed(_bad("Trace board gate annex for step 2"),
                                 _read("Trace board gate annex for step 2"))

    def test_governed_inserted_beside_step2_uncounted(self):
        self._beside_step2_uncounted(_bad("Trace board gate summary"))

    def test_governed_inserted_gate_ruling_governed(self):
        report = self._q4_alone(
            _bad("Trace board gate summary"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    def test_code_level_record_order_governed(self):
        for words in (("board",), ("board", "gate"),
                      ("board", "gate", "review"),
                      ("board", "gate", "annex"),
                      ("board", "gate", "review", "annex"),
                      ("board", "gate", "annex", "review"),
                      ("board", "gate", "review", "annex", "panel")):
            self.assertTrue(_inserted_words_governed(
                [_fold_word(word) for word in words]), words)

    def test_code_level_head_standing_governed(self):
        self.assertTrue(_tally_statement_head(
            "Trace board gate summary: items checked stand "
            "here. LANDED figures stand here, no counts stated"))
    # ------------------------------------------------------
    # Held controls: the governed fused forms, the
    # governed trace summary forms, and the exact word
    # sets as fix pass 15 and Unit 1 left them
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

    def test_governed_trace_summary_plain(self):
        self._candidate_governed(_bad("Trace summary"),
                                 _read("Trace summary"))

    def test_governed_summary_trace_reversed(self):
        self._candidate_governed(_bad("Summary trace"),
                                 _read("Summary trace"))

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
                     "summarization", "summarisations",
                     "summarizations", "summariser",
                     "summarizer"):
            self.assertTrue(_summary_word(_fold_word(word)), word)

    def test_code_level_tally_variant_positions(self):
        self.assertTrue(_tally_word(_fold_word("boardtallys")))
        self.assertTrue(_tally_word(_fold_word("boardtallyed")))
        self.assertTrue(_tally_word(_fold_word("boardtallyes")))
        self.assertTrue(_tally_word(_fold_word("tallys")))
        self.assertTrue(_tally_word(_fold_word("tallyed")))
    # ------------------------------------------------------
    # Held controls: the seven enumerated family adverbs
    # and tallyho standing missing, the fused family
    # forms standing missing, and the twelve prose
    # adverbs of R16-14-02 standing missing
    # ------------------------------------------------------

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

    def test_held_prose_rectally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The results were recorded rectally")))

    def test_held_prose_septally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The sample was taken septally")))

    def test_held_prose_tallyho_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The dawn cry was tallyho")))

    def test_held_prose_subtotally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The count was taken subtotally")))

    def test_held_prose_semirectally_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The count was taken semirectally")))

    def test_held_prose_mentally_missing(self):
        line = ("The board reasoned mentally. LANDED figures "
                "stand here, no counts stated")
        self._assert_q4_missing(self._q4_alone(line))

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
