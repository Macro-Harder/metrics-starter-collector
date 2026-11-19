"""Step 16 fix pass 17 unit 2 tests: the Q-4 tally head unit.

Pinning tests for register item R16-17-01 (Medium, B17-B01
merged with B17-C01 to B17-C06) of Step 16 round 17. The
governing rule of the pass, in its extended form: a piece
not read in full, for whatever reason, is not read, and
its converse: a piece that is no feeder flips nothing.

R16-17-01: forty seven distinct alone forms in ten
subfamilies stand missing beside their counted siblings
on the counted pattern ground alone, past the restated
boundary of fix pass 16. The counted pattern counts the
numeric tally form with no head test at all, so every
head under which a counted sibling counts stands as a
tally statement head in the reach the row itself uses.
The subfamilies stand as follows: (a) genuine heads fused
from record words and whole words the widened governed
fused prefix enumeration of twenty still does not name,
ten forms; (b) composite openings, a governed prefix
standing in the opening position with an unnamed record
word standing immediately before the tally form, three
forms; (c) variant spellings in that composite opening
position, three forms; (d) variant spellings past the
talley family, standing alone and behind governed
prefixes, five forms, the Tallyies alone form standing
flagged in exactly the standing form against its express
standalone exclusion, folded in this register against the
Tallys and Tallyes precedent; (e) summary plurals past
the twenty, six forms; (f) fused closings built on those
forms, five forms; (g) fused closings with four governed
words fused between the closing words, three forms;
(h) inserted closings past six forward and five reversed,
wide and middle swap forms, four forms; (i) for step
closings past six inserted words, two forms; and
(j) further stroke and hook fold letters, six forms. One
driven form stands as a held control and is no defect
form: Board Tally with a hook on its first letter stands
governed, and it stays governed. Locus:
derivation_core.py, _fold_word, _tally_word and its
constants, _summary_word and its constant,
_fused_trace_summary, and _tally_statement_head and its
closing tests, against _trace_candidates and the shared
constant _TALLY_COUNTED_PATTERN, which carries no head
test. The cure these tests pin widens the stated boundary
in general terms and restates it: the governed fused
prefix enumeration at its new width, the variant
spellings in their positions, the summary word in its
further plural forms, the fused between reach at four
words, the inserted counts at seven forward, six reversed
and seven in the for step form under the wide record
order, and the folding at its further letters, so each
defect form stands governed, present and derivable in
the row form the exhibits state, alone, beside, and in
gate rulings, while every form standing missing for
governed reasons stays missing and every form standing
governed stays governed.

Held controls stand pinned beside the defect forms, in
full: the held letter control of subfamily (j) standing
governed; the forms of R16-17-02 standing in their cured
standings under fix pass 17 Unit 1, its prose sentences
and prose clauses standing missing in every position, its
bounding inserted sentence tail and its fused between
prose sentences at four fused words standing missing, and
its governed direct, fused and inserted closings standing
governed; the correctness converse hunting of round 17
standing held whole, the prose order runs at the admitted
counts and at the widened counts, the prose sentences at
those counts, the mixed runs carrying a joining word, the
fused between prose forms, the inserted digit form and
the repeated word run, each standing missing; prose at
the counts this unit widens to standing missing where its
inserted words step back before the record order has
stood complete; the forty four charged forms of
R16-16-01 standing governed and the prose forms of
R16-16-02 standing missing, in their restated boundaries;
the mixed inserted runs standing missing; the seven
enumerated family adverbs and tallyho standing missing,
the fused family forms standing missing, and the twelve
prose adverbs of R16-14-02 standing missing; the Board
talli boundary control standing missing; the folded
round 10 prose sentence record standing governed; the
four folded marker shape records standing present but
not derivable; the golden prose lines standing
unflipped; and the read and absent feeder controls byte
for byte.
"""
from metrics_starter_collector.derivation_core import (
    _fold_word, _fused_trace_summary, _summary_word,
    _tally_statement_head, _tally_word)
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


class TestStep16Fix17Unit2(FixtureTestCase):

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

    def _candidate(self, line, counted_line):
        self._assert_q4_counted(self._q4_alone(counted_line))
        self._assert_q4_governed(self._q4_alone(line))

    def _candidate_missing(self, line, counted_line):
        self._assert_q4_counted(self._q4_alone(counted_line))
        self._assert_q4_missing(self._q4_alone(line))

    def _beside(self, line):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=line)
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        return row_block(self._run(files), "Q-4")

    def _beside_step2_uncounted(self, line):
        q4 = self._beside(line)
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def _beside_step2_nowhere(self, line):
        q4 = self._beside(line)
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertNotIn("Step 2", q4)

    # ------------------------------------------------------
    # R16-17-01 defect forms, subfamily (a): genuine heads
    # fused from record words and whole words the widened
    # enumeration of twenty still does not name
    # ------------------------------------------------------

    def test_a_fused_archivestally(self):
        self._candidate(_bad("Archivestally"), _read("Archivestally"))

    def test_a_fused_minutestally(self):
        self._candidate(_bad("Minutestally"), _read("Minutestally"))

    def test_a_fused_indextally(self):
        self._candidate(_bad("Indextally"), _read("Indextally"))

    def test_a_fused_archivestallies(self):
        self._candidate(_bad("Archivestallies"),
                        _read("Archivestallies"))

    def test_a_fused_minutestallied(self):
        self._candidate(_bad("Minutestallied"),
                        _read("Minutestallied"))

    def test_a_fused_indextallying(self):
        self._candidate(_bad("Indextallying"),
                        _read("Indextallying"))

    def test_a_fused_archivetally(self):
        self._candidate(_bad("Archivetally"), _read("Archivetally"))

    def test_a_fused_catalogtallies(self):
        self._candidate(_bad("Catalogtallies"),
                        _read("Catalogtallies"))

    def test_a_fused_manifesttally(self):
        self._candidate(_bad("Manifesttally"), _read("Manifesttally"))

    def test_a_fused_registrytally(self):
        self._candidate(_bad("Registrytally"), _read("Registrytally"))

    # ------------------------------------------------------
    # R16-17-01 defect forms, subfamily (b): composite
    # openings, a governed prefix in the opening position
    # with an unnamed record word immediately before the
    # tally form
    # ------------------------------------------------------

    def test_b_composite_boardarchivetally(self):
        self._candidate(_bad("Boardarchivetally"),
                        _read("Boardarchivetally"))

    def test_b_composite_gateindextally(self):
        self._candidate(_bad("Gateindextally"),
                        _read("Gateindextally"))

    def test_b_composite_reviewminutestally(self):
        self._candidate(_bad("Reviewminutestally"),
                        _read("Reviewminutestally"))

    # ------------------------------------------------------
    # R16-17-01 defect forms, subfamily (c): variant
    # spellings in the composite opening position
    # ------------------------------------------------------

    def test_c_variant_gatearchivetallyed(self):
        self._candidate(_bad("Gatearchivetallyed"),
                        _read("Gatearchivetallyed"))

    def test_c_variant_boardindextalleys(self):
        self._candidate(_bad("Boardindextalleys"),
                        _read("Boardindextalleys"))

    def test_c_variant_reviewminutestallyes(self):
        self._candidate(_bad("Reviewminutestallyes"),
                        _read("Reviewminutestallyes"))

    # ------------------------------------------------------
    # R16-17-01 defect forms, subfamily (d): variant
    # spellings past the talley family, alone and fused.
    # The Tallyies alone form stands flagged in exactly
    # the standing form against its express standalone
    # exclusion, on the Tallys and Tallyes precedent.
    # ------------------------------------------------------

    def test_d_variant_tallyies_alone_flagged(self):
        self._candidate(_bad("Tallyies"), _read("Tallyies"))

    def test_d_variant_tallie_alone(self):
        self._candidate(_bad("Tallie"), _read("Tallie"))

    def test_d_variant_talleying_alone(self):
        self._candidate(_bad("Talleying"), _read("Talleying"))

    def test_d_variant_boardtallie(self):
        self._candidate(_bad("Boardtallie"), _read("Boardtallie"))

    def test_d_variant_boardtalleying(self):
        self._candidate(_bad("Boardtalleying"),
                        _read("Boardtalleying"))

    # ------------------------------------------------------
    # R16-17-01 defect forms, subfamily (e): the summary
    # word in further plural forms past the twenty
    # ------------------------------------------------------

    def test_e_summary_summarizings(self):
        self._candidate(_bad("Trace summarizings"),
                        _read("Trace summarizings"))

    def test_e_summary_summaryes(self):
        self._candidate(_bad("Trace summaryes"),
                        _read("Trace summaryes"))

    def test_e_summary_summarizationes(self):
        self._candidate(_bad("Trace summarizationes"),
                        _read("Trace summarizationes"))

    def test_e_summary_summaryses(self):
        self._candidate(_bad("Trace summaryses"),
                        _read("Trace summaryses"))

    def test_e_summary_summariseds(self):
        self._candidate(_bad("Trace summariseds"),
                        _read("Trace summariseds"))

    def test_e_summary_summariserses(self):
        self._candidate(_bad("Trace summariserses"),
                        _read("Trace summariserses"))

    # ------------------------------------------------------
    # R16-17-01 defect forms, subfamily (f): fused trace
    # summary closings built on the further forms
    # ------------------------------------------------------

    def test_f_fused_boardtracesummarizings(self):
        self._candidate(_bad("Boardtracesummarizings"),
                        _read("Boardtracesummarizings"))

    def test_f_fused_tracesummaryes(self):
        self._candidate(_bad("Tracesummaryes"),
                        _read("Tracesummaryes"))

    def test_f_fused_boardtracessummaryes(self):
        self._candidate(_bad("Boardtracessummaryes"),
                        _read("Boardtracessummaryes"))

    def test_f_fused_tracesummaryses(self):
        self._candidate(_bad("Tracesummaryses"),
                        _read("Tracesummaryses"))

    def test_f_fused_boardtracesummariseds(self):
        self._candidate(_bad("Boardtracesummariseds"),
                        _read("Boardtracesummariseds"))

    # ------------------------------------------------------
    # R16-17-01 defect forms, subfamily (g): fused closings
    # with four governed words fused between the closing
    # words, in either order and with the plural trace word
    # ------------------------------------------------------

    def test_g_fused_between_four_forward(self):
        head = "Traceboardgatereviewannexsummary"
        self._candidate(_bad(head), _read(head))

    def test_g_fused_between_four_reversed(self):
        head = "Summaryboardgatereviewannextrace"
        self._candidate(_bad(head), _read(head))

    def test_g_fused_between_four_plural_trace(self):
        head = "Tracesboardgatereviewannexsummary"
        self._candidate(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-17-01 defect forms, subfamily (h): inserted
    # closings past six forward and five reversed, wide
    # and middle swap forms
    # ------------------------------------------------------

    def test_h_inserted_seven_forward_wide(self):
        head = ("Trace board gate review annex panel board "
                "gate summary")
        self._candidate(_bad(head), _read(head))

    def test_h_inserted_seven_forward_middle_swap(self):
        head = ("Trace board gate annex review panel board "
                "gate summary")
        self._candidate(_bad(head), _read(head))

    def test_h_inserted_six_reversed_wide(self):
        head = ("Summary board gate review annex panel board "
                "trace")
        self._candidate(_bad(head), _read(head))

    def test_h_inserted_six_reversed_middle_swap(self):
        head = ("Summary board gate annex review panel board "
                "trace")
        self._candidate(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-17-01 defect forms, subfamily (i): the for step
    # closing past six inserted words
    # ------------------------------------------------------

    def test_i_for_step_seven_inserted(self):
        head = ("Trace board gate review annex panel board "
                "gate for step 2")
        self._candidate(_bad(head), _read(head))

    def test_i_for_step_seven_inserted_middle_swap(self):
        head = ("Trace board gate annex review panel board "
                "gate for step 2")
        self._candidate(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-17-01 defect forms, subfamily (j): further stroke
    # and hook letters past the widened fold set
    # ------------------------------------------------------

    def test_j_letter_small_capital_l_tally(self):
        self._candidate(_bad("Board ta\u029fly"),
                        _read("Board ta\u029fly"))

    def test_j_letter_esh_summary(self):
        self._candidate(_bad("Trace \u0283ummarise"),
                        _read("Trace \u0283ummarise"))

    def test_j_letter_upsilon_summary(self):
        self._candidate(_bad("Trace s\u028ammarise"),
                        _read("Trace s\u028ammarise"))

    def test_j_letter_z_hook_summary(self):
        self._candidate(_bad("Trace summari\u0290e"),
                        _read("Trace summari\u0290e"))

    def test_j_letter_insular_d_summary(self):
        self._candidate(_bad("Trace summarise\ua77a"),
                        _read("Trace summarise\ua77a"))

    def test_j_letter_barred_e_summary(self):
        self._candidate(_bad("Trace summaris\u0247d"),
                        _read("Trace summaris\u0247d"))

    # ------------------------------------------------------
    # R16-17-01 defect forms in the beside and gate ruling
    # positions, as the exhibits drive them
    # ------------------------------------------------------

    def test_beside_archivestally_step2_uncounted(self):
        self._beside_step2_uncounted(_bad("Archivestally"))

    def test_beside_summarizings_step2_uncounted(self):
        self._beside_step2_uncounted(_bad("Trace summarizings"))

    def test_gate_ruling_archivestally_governed(self):
        report = self._q4_alone(_bad("Archivestally"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # R16-17-01 code level defect tests: the widened reach
    # at the word tests, the fused test, the head test and
    # the fold, in general combination forms of the same
    # families beside the driven forms
    # ------------------------------------------------------

    def test_code_level_new_prefix_combinations(self):
        for word in ("archivestally", "archivestallied",
                     "archivetally", "archivetallies",
                     "catalogtally", "catalogtallying",
                     "manifesttallies", "manifesttallying",
                     "registrytallied", "registrytallyies",
                     "minutestallyed", "indextallys",
                     "boardarchivestally", "gatecatalogtallyed",
                     "reviewregistrytallyes"):
            self.assertTrue(_tally_word(_fold_word(word)), word)

    def test_code_level_variant_spellings_positions(self):
        for word in ("tallyies", "tallie", "talleying",
                     "boardtallie", "boardtalleying",
                     "chairtallie", "chairtalleying"):
            self.assertTrue(_tally_word(_fold_word(word)), word)

    def test_code_level_further_summary_forms(self):
        for word in ("summarizings", "summaryes",
                     "summarizationes", "summaryses",
                     "summariseds", "summariserses"):
            self.assertTrue(_summary_word(_fold_word(word)), word)

    def test_code_level_further_fused_closings(self):
        for word in ("boardtracesummarizings", "tracesummaryes",
                     "boardtracessummaryes", "tracesummaryses",
                     "boardtracesummariseds",
                     "summarysesboardtrace",
                     "traceboardgatereviewannexsummary",
                     "summaryboardgatereviewannextrace",
                     "tracesboardgatereviewannexsummary",
                     "boardtraceboardgatereviewannexsummary"):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)

    def test_code_level_inserted_widened_counts_head(self):
        for head in ("Trace board gate review annex panel board "
                     "gate summary",
                     "Trace board gate annex review panel board "
                     "gate summary",
                     "Summary board gate review annex panel board "
                     "trace",
                     "Summary board gate annex review panel board "
                     "trace",
                     "Trace board gate review annex panel board "
                     "gate for step 2",
                     "Trace board gate annex review panel board "
                     "gate for step 2"):
            line = (head + ": items checked stand here. LANDED "
                    "figures stand here, no counts stated")
            self.assertTrue(_tally_statement_head(line), head)

    def test_code_level_further_fold_letters(self):
        self.assertEqual(_fold_word("ta\u029fly"), "tally")
        self.assertEqual(_fold_word("\u0283ummarise"), "summarise")
        self.assertEqual(_fold_word("s\u028ammarise"), "summarise")
        self.assertEqual(_fold_word("summari\u0290e"), "summarise")
        self.assertEqual(_fold_word("summarise\ua77a"),
                         "summarised")
        self.assertEqual(_fold_word("summaris\u0247d"),
                         "summarised")
        self.assertEqual(_fold_word("\u01acally"), "tally")

    # ------------------------------------------------------
    # Held control: the one driven form of subfamily (j)
    # that stands governed and is no defect form
    # ------------------------------------------------------

    def test_control_letter_t_hook_tally_governed(self):
        self._candidate(_bad("Board \u01acally"),
                        _read("Board \u01acally"))

    # ------------------------------------------------------
    # Held controls: Unit 1 cured forms staying in their
    # cured standings, the prose sentences and prose
    # clauses of R16-17-02 standing missing in every
    # position, its bounding forms standing missing, and
    # its governed closings standing governed
    # ------------------------------------------------------

    def test_unit1_prose_forms_missing(self):
        for run in ("We reviewed the trace summary",
                    "She filed the summary trace",
                    "The panel noted the trace summary",
                    "For the trace summary",
                    "We reviewed the tracesummary",
                    "She filed the summarytrace",
                    "We reviewed the boardtracesummary",
                    "We reviewed the traceboardgatesummary",
                    "She filed the summaryboardgatetrace",
                    "The filing, trace summary",
                    "Noted in the filing, the summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_unit1_prose_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("We reviewed the trace summary"), ruling=True))
        self._beside_step2_nowhere(
            _prose("We reviewed the trace summary"))
        self._beside_step2_nowhere(
            _prose("We reviewed the tracesummary"))

    def test_unit1_bounding_forms_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("She filed the trace gate summary")))
        for run in ("The panel reviewed the "
                    "traceboardgatereviewannexsummary",
                    "The panel reviewed the "
                    "traceboardgateannexreviewsummary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_unit1_governed_closings_governed(self):
        for head in ("Trace summary", "Summary trace",
                     "Trace summaries", "Trace summarisers",
                     "Trace summarizers", "Trace summarisings",
                     "Trace summarys",
                     "Alpha beta gamma delta epsilon trace summary",
                     "Round's trace summary",
                     "Tracesummary", "Tracesummaries",
                     "Boardtracesummary", "Boardtracesummarising",
                     "Boardtracesummarization", "Summarytrace",
                     "Boardsummarytraces", "Traceboardgatesummary",
                     "Traceboardgatepanelsummary",
                     "Summaryboardgatetrace", "Tracesboardsummary",
                     "Summaryboardtraces",
                     "Boardtracesummarisers",
                     "Boardtracessummarisers"):
            self._candidate(_bad(head), _read(head))

    def test_unit1_governed_beside_and_gate_ruling(self):
        self._beside_step2_uncounted(_bad("Trace summary"))
        self._beside_step2_uncounted(_bad("Tracesummary"))
        report = self._q4_alone(_bad("Trace summary"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)
        report = self._q4_alone(_bad("Tracesummary"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # Held controls: the correctness converse hunting of
    # round 17 standing held whole, and prose at the counts
    # this unit widens to standing missing where its words
    # step back before the record order has stood complete
    # or its closing stands as the tail of a sentence
    # ------------------------------------------------------

    def test_converse_correctness_forms_missing(self):
        for run in ("Traceofsummary", "Tracethesummary",
                    "Trace 2 summary", "Trace board board summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_converse_prose_at_widened_counts_missing(self):
        for run in ("Trace review annex panel gate board gate "
                    "summary",
                    "Summary review annex panel gate board trace",
                    "Trace review annex panel gate board gate "
                    "for step 2",
                    "Trace gate board review summary",
                    "We reviewed the trace board gate review annex "
                    "panel board gate summary",
                    "She filed the summary board gate review annex "
                    "panel board trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_converse_fused_between_out_of_order_missing(self):
        for head in ("Tracegateboardreviewsummary",
                     "Traceboardreviewgatesummary"):
            self._candidate_missing(_bad(head), _read(head))

    # ------------------------------------------------------
    # Held controls: the fix pass 16 items in their restated
    # boundaries, the governed inserted closings, the mixed
    # runs and the prose order runs
    # ------------------------------------------------------

    def test_control_fix16_underreach_forms_governed(self):
        for head in ("Ledgertally", "Rostertally", "Registertally",
                     "Dockettallies", "Journaltallied",
                     "Censustallying", "Committeetally",
                     "Counciltallies", "Workgrouptally",
                     "Gateboardtallyed", "Reviewboardtallys",
                     "Gateboardtallyes", "Tallyes", "Talley",
                     "Talleys", "Talleyed", "Boardtalley",
                     "Boardtallyies", "Chairtalleyed",
                     "Trace summarisers", "Trace summarizers",
                     "Trace summarisings", "Trace summarys",
                     "Boardtracesummarisers",
                     "Boardtracesummarizers", "Tracesummarisers",
                     "Boardtracessummarisers",
                     "Traceboardgatesummary",
                     "Traceboardgatepanelsummary",
                     "Summaryboardgatetrace", "Tracesboardsummary",
                     "Summaryboardtraces",
                     "Trace board gate review annex panel board "
                     "summary",
                     "Trace board gate review annex panel gate "
                     "summary",
                     "Summary board gate review annex panel trace",
                     "Trace board gate review annex panel for "
                     "step 2",
                     "Trace board gate review annex panel board "
                     "for step 2",
                     "Board ta\u026bly", "Board \u01adally",
                     "Trace \u0282ummarise",
                     "Trace su\u0271marise",
                     "Trace s\u0289mmarise",
                     "Trace summaris\u0257", "Trace summarise\u00fe"):
            self._candidate(_bad(head), _read(head))

    def test_control_fix16_converse_forms_missing(self):
        for run in ("Trace review board summary",
                    "Trace panel gate board summary",
                    "Trace annex panel gate board summary",
                    "Trace review annex panel gate board summary",
                    "Summary review board trace",
                    "Summary panel gate board trace",
                    "Summary review annex panel gate trace",
                    "Trace review board for step 2",
                    "Trace panel gate board for step 2",
                    "Trace annex panel gate board for step 2",
                    "We reviewed the trace board gate summary",
                    "She filed the summary board trace",
                    "For the trace board summary",
                    "Of the summary board trace",
                    "The panel reviewed the trace gate summary",
                    "We reviewed the trace board gate annex "
                    "review summary",
                    "We reviewed the trace board gate review "
                    "annex summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_control_governed_inserted_closings_governed(self):
        for head in ("Trace board summary",
                     "Trace board gate summary",
                     "Trace board gate review summary",
                     "Trace board gate annex summary",
                     "Trace board gate annex review summary",
                     "Summary board trace", "Summary board gate trace",
                     "Summary board gate review trace",
                     "Summary board gate annex review trace",
                     "Trace board gate review annex summary",
                     "Trace board gate review annex panel summary",
                     "Summary board gate review annex trace",
                     "Trace for step 2", "Trace board for step 2",
                     "Trace board gate for step 2",
                     "Trace board gate review annex for step 2"):
            self._candidate(_bad(head), _read(head))

    def test_control_mixed_inserted_runs_missing(self):
        for run in ("Trace board of summary",
                    "Summary of board trace",
                    "Trace of board gate summary",
                    "Summary board of the trace",
                    "Trace the board summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_control_prose_order_past_wide_reach_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Trace review annex panel gate board summary")))
        self._assert_q4_missing(self._q4_alone(_prose(
            "Summary review annex panel gate board trace")))

    # ------------------------------------------------------
    # Held controls: the family adverbs, tallyho, the fused
    # family forms, and the twelve prose adverbs
    # ------------------------------------------------------

    def test_control_family_and_adverb_forms_missing(self):
        for line in (
                "The figures stand totally: LANDED figures stand "
                "here, no counts stated",
                "The results were recorded rectally: LANDED "
                "figures stand here, no counts stated",
                "The sample was taken septally: LANDED figures "
                "stand here, no counts stated",
                "The count was taken subtotally: LANDED figures "
                "stand here, no counts stated",
                "The count was taken semirectally: LANDED figures "
                "stand here, no counts stated",
                "The dawn cry was tallyho: LANDED figures stand "
                "here, no counts stated"):
            self._assert_q4_missing(self._q4_alone(line))
        for word in ("brutally", "capitally", "vitally", "fatally",
                     "prenatally", "neonatally", "mortally",
                     "frontally", "dentally", "distally",
                     "horizontally", "coastally"):
            line = ("The blow landed " + word + ": LANDED figures "
                    "stand here, no counts stated")
            self._assert_q4_missing(self._q4_alone(line))

    def test_code_level_family_and_adverbs_no_tally_word(self):
        for word in ("totally", "accidentally", "digitally",
                     "incidentally", "mentally", "rectally",
                     "septally", "subtotally", "semirectally",
                     "tallyho", "brutally", "capitally", "vitally",
                     "fatally", "prenatally", "neonatally",
                     "mortally", "frontally", "dentally",
                     "distally", "horizontally", "coastally"):
            self.assertFalse(_tally_word(_fold_word(word)), word)

    # ------------------------------------------------------
    # Held controls: the folded records, the golden lines,
    # and the settled positions
    # ------------------------------------------------------

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

    def test_held_prose_sentence_closing_on_tally(self):
        line = ("Record the board tally. LANDED figures stand "
                "here, no counts stated")
        self._assert_q4_governed(self._q4_alone(line))

    def test_held_closing_talli_different_word_missing(self):
        self._candidate_missing(_bad("Board tall\u00ed"),
                                _read("Board tall\u00ed"))

    def test_held_marker_shapes_governed(self):
        for prefix in ("((1)) ", "(a b) ", "() "):
            self._assert_q4_governed(
                self._q4_alone(_dot_form(prefix, "Board tally")))
        self._assert_q4_governed(
            self._q4_alone("{1} " + _bad("Board tally")))

    def test_held_numbered_no_colon_residual(self):
        self._assert_q4_missing(
            self._q4_alone(_dot_form("(1234567) ", "Board tally")))
        self._assert_q4_missing(
            self._q4_alone(_dot_form("(appendix) ", "Trace summary")))
        line = ("1. Board tally! LANDED figures stand here, "
                "no counts stated")
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
