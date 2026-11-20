"""Step 16 fix pass 19 unit 2 tests: the Q-4 widening unit.

Pinning tests for register item R16-19-01 (Medium, B19-C01
and B19-B01) of Step 16 round 19. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-19-01: malformed tally statement heads the restated
boundary of fix pass 18 still does not reach, in sixty
one distinct alone forms in ten subfamilies, on the
counted pattern head agnosticism ground alone in every
subfamily: (a) genuine heads fused from record words the
governed fused prefix enumeration of thirty eight does
not name, and tally forms fused behind the plurals of
governed prefixes other than boards, fourteen forms;
(b) composite openings, a governed prefix in the opening
position with an unnamed record word immediately before
the tally form, six forms; (c) variant spellings in that
composite opening position, four forms; (d) variant
spellings past the widened variant sets of fourteen,
five forms; (e) the summary word in further plural forms
past the thirty four, eight forms; (f) fused trace
summary closings built on those forms, four forms;
(g) fused closings with six governed words fused between
the closing words, three forms; (h) inserted word
closings at nine words forward and eight words reversed,
four forms; (i) the for step closing at nine inserted
words, one form; and (j) the tally and summary words
carrying further stroke and hook letters the folding
does not replace, twelve defect forms, beside the held
barred u letter form standing governed already and
standing as no part of the widening. Each alone form
stands missing beside its counted sibling on the
entering bytes, the beside forms standing present over
Step 3 with Step 2 named uncounted and the gate ruling
forms standing missing in the same form. Locus:
derivation_core.py, _fold_word, _tally_word and the
constants _TALLY_WORD_FORMS, _TOTALLY_FAMILY,
_GOVERNED_FUSED_PREFIXES, _TALLY_WORD_VARIANT_FORMS and
_TALLY_WORD_VARIANT_FUSED_FORMS, _summary_word and the
constant _SUMMARY_WORD_FORMS, _fused_trace_summary with
_fused_between_closing, and _tally_statement_head, its
closing tests standing after its docstring. The cure
these tests pin widens those tests in general terms, so
each driven form stands counted, in the alone position
taking the governed not derivable form naming the step
and the feeder piece, and in the beside position naming
the step uncounted, in gate records and gate rulings
alike, while every held control stands exactly as
before.

Held controls stand pinned beside the defect forms, in
full: every form of R16-19-02 standing missing in its
prose form, alone, beside and in gate rulings, as Unit 1
of this pass left it, its thirty distinct alone forms
and its bounding held controls among them, and every
form of R16-18-02 and R16-17-02 standing missing in the
same way; the held letter form standing governed in its
exact form; the governed fused prefix forms and the
variant forms behind their governed prefixes standing
governed; the seven enumerated family adverbs and
tallyho standing missing, the fused family forms
standing missing, and the twelve prose adverbs of
R16-14-02 standing missing; the Board talli boundary
control standing missing; the folded round 10 prose
sentence record standing governed; the four folded
marker shape records standing present but not
derivable; the golden prose lines standing unflipped;
and the read and absent feeder controls byte for byte.
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


class TestStep16Fix19Unit2(FixtureTestCase):

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
    # R16-19-01 defect forms, subfamily (a): genuine heads
    # fused from record words past the thirty eight, and
    # tally forms fused behind the plurals of governed
    # prefixes other than boards, fourteen forms, each
    # standing governed beside its counted sibling after
    # the cure
    # ------------------------------------------------------

    def test_r16_19_01_subfamily_a_governed(self):
        for head in ("Memotally", "Slipstally", "Charttally",
                     "Sheettally", "Pagetalies", "Panelstally",
                     "Gatestallies", "Teamstally", "Packettally",
                     "Foldertallies", "Bindertally", "Sheettallied",
                     "Panelstallies", "Recordstallied"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_19_01_subfamily_b_governed(self):
        for head in ("Boardmemotally", "Gatecharttally",
                     "Reviewslipstally", "Boardpackettally",
                     "Gatefoldertally", "Reviewbindertally"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_19_01_subfamily_c_governed(self):
        for head in ("Gatememotalleys", "Boardcharttallyed",
                     "Boardpackettallye", "Gatefoldertalliez"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_19_01_subfamily_d_governed(self):
        for head in ("Tallyie", "Tallyin", "Talleies",
                     "Boardtallyie", "Boardtallyin"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_19_01_subfamily_e_governed(self):
        for head in ("Trace summariseeses",
                     "Trace summarizationeses",
                     "Trace summarieseses", "Trace summarisedses",
                     "Trace summarisedes", "Trace summarizeres",
                     "Trace summarisationeses",
                     "Trace summaryeses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_19_01_subfamily_f_governed(self):
        for head in ("Boardtracesummariseeses",
                     "Tracessummarieseses",
                     "Boardtracesummarisedes",
                     "Tracessummaryeses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_19_01_subfamily_g_governed(self):
        for head in ("Traceboardgatereviewannexpanelboardsummary",
                     "Summaryboardgatereviewannexpanelboardtrace",
                     "Tracesboardgatereviewannexpanelboardsummary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_19_01_subfamily_h_governed(self):
        for head in ("Trace board gate review annex panel board "
                     "gate review annex summary",
                     "Trace board gate annex review panel board "
                     "gate annex review summary",
                     "Summary board gate review annex panel board "
                     "gate review trace",
                     "Summary board gate annex review panel board "
                     "gate annex trace"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_19_01_subfamily_i_governed(self):
        self._candidate_governed(
            _bad("Trace board gate review annex panel board "
                 "gate review annex for step 2"),
            _read("Trace board gate review annex panel board "
                  "gate review annex for step 2"))

    def test_r16_19_01_subfamily_j_governed(self):
        for head in ("Trace summarise\u02a0",
                     "Trace summaris\uab53e",
                     "Board ta\u026dly",
                     "Trace summarise\u0221",
                     "Board tall\uab79",
                     "Trace \u029bummarise",
                     "Trace summarise\u0180",
                     "Board t\u00e6lly",
                     "Board ta\u014bly",
                     "Board tall\u00fe",
                     "Trace \u0292ummarise",
                     "Trace summarise\u026d"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_19_01_beside_forms_uncounted(self):
        for head in ("Memotally", "Trace summariseeses",
                     "Packettally", "Trace summarisedes"):
            self._beside_step2_uncounted(_bad(head))

    def test_r16_19_01_gate_ruling_forms_governed(self):
        for head in ("Memotally", "Packettally"):
            report = self._q4_alone(_bad(head), ruling=True)
            self._assert_q4_governed(report, path=RULING_2)

    def test_r16_19_01_code_level_forms(self):
        for word in ("memotally", "slipstally", "charttally",
                     "sheettally", "pagetalies", "panelstally",
                     "gatestallies", "teamstally", "packettally",
                     "foldertallies", "bindertally", "sheettallied",
                     "panelstallies", "recordstallied",
                     "boardmemotally", "gatecharttally",
                     "reviewslipstally", "boardpackettally",
                     "gatefoldertally", "reviewbindertally",
                     "gatememotalleys", "boardcharttallyed",
                     "boardpackettallye", "gatefoldertalliez",
                     "tallyie", "tallyin", "talleies",
                     "boardtallyie", "boardtallyin"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ("summariseeses", "summarizationeses",
                     "summarieseses", "summarisedses",
                     "summarisedes", "summarizeres",
                     "summarisationeses", "summaryeses"):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ("boardtracesummariseeses",
                     "tracessummarieseses",
                     "boardtracesummarisedes",
                     "tracessummaryeses",
                     "traceboardgatereviewannexpanelboardsummary",
                     "summaryboardgatereviewannexpanelboardtrace",
                     "tracesboardgatereviewannexpanelboardsummary"):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        for head in ("Memotally",
                     "Trace board gate review annex panel board "
                     "gate review annex summary",
                     "Summary board gate annex review panel board "
                     "gate annex trace",
                     "Trace board gate review annex panel board "
                     "gate review annex for step 2",
                     "Trace summariseeses"):
            line = head + ": items checked stand here"
            self.assertTrue(_tally_statement_head(line), head)
        self.assertEqual(_fold_word("summarise\u02a0"),
                         "summarised")
        self.assertEqual(_fold_word("summaris\uab53e"),
                         "summarise")
        self.assertEqual(_fold_word("ta\u026dly"), "tally")
        self.assertEqual(_fold_word("summarise\u0221"),
                         "summarised")
        self.assertEqual(_fold_word("tall\uab79"), "tally")
        self.assertEqual(_fold_word("\u029bummarise"),
                         "summarise")
        self.assertEqual(_fold_word("summarise\u0180"),
                         "summarised")
        self.assertEqual(_fold_word("t\u00e6lly"), "tally")
        self.assertEqual(_fold_word("ta\u014bly"), "tally")
        self.assertEqual(_fold_word("tall\u00fe"), "tally")
        self.assertEqual(_fold_word("\u0292ummarise"),
                         "summarise")
        self.assertEqual(_fold_word("summarise\u026d"),
                         "summarised")

    # ------------------------------------------------------
    # Held controls: every form of R16-19-02 standing
    # missing in its prose form as Unit 1 of this pass
    # left it, its thirty distinct alone forms in full,
    # with its gate ruling and beside forms
    # ------------------------------------------------------

    def test_r16_19_02_held_direct_forms_missing(self):
        for run in ("Panel reviews trace summary",
                    "Board records summary trace",
                    "Clerk opens trace summary",
                    "Minutes contain trace summary",
                    "Panel wants summary trace",
                    "Clerk brings summary trace",
                    "Board accepts summary trace",
                    "Gatekeepers receive trace summary",
                    "Panel logs trace summary",
                    "Clerk marks summary trace",
                    "Minutes log trace summary",
                    "Board opens summary trace",
                    "Panel posts trace summary",
                    "Team tracks summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_19_02_held_fused_forms_missing(self):
        for run in ("Panel reviews tracesummary",
                    "Board records summarytrace",
                    "Panel reviews boardtracesummary",
                    "Clerk opens traceboardgatesummary",
                    "Panel reviews "
                    "traceboardgatereviewannexpanelsummary",
                    "Panel logs tracesummary",
                    "Clerk marks summarytrace",
                    "Minutes log boardtracesummary",
                    "Panel posts traceboardgatesummary",
                    "Panel logs "
                    "traceboardgatereviewannexpanelsummary",
                    "Panel logs tracesummarisinges"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_19_02_held_run_and_clause_forms_missing(self):
        for run in ("Ledger [panel] trace summary",
                    "Ledger / trace summary",
                    "Ledger -- trace summary",
                    "Logs panel summary trace",
                    "Marks ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_19_02_held_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel reviews trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel logs trace summary"), ruling=True))
        self._beside_step2_nowhere(
            _prose("Panel reviews trace summary"))
        self._beside_step2_nowhere(
            _prose("Panel logs trace summary"))

    def test_r16_19_02_held_code_level_prose_no_head(self):
        for run in ("Panel reviews trace summary",
                    "Panel logs trace summary",
                    "Panel logs tracesummary",
                    "Panel logs "
                    "traceboardgatereviewannexpanelsummary",
                    "Ledger [panel] trace summary",
                    "Ledger / trace summary",
                    "Ledger -- trace summary"):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)

    def test_r16_19_02_bounding_controls_missing(self):
        for run in ("Panel reviews trace board gate review "
                    "annex panel board gate summary",
                    "Panel logs trace board gate summary",
                    "Panel reviewed trace board gate summary",
                    "Clerk filed summary board gate trace",
                    "Panel reviewed trace board gate review "
                    "annex panel summary",
                    "She filed the trace gate summary",
                    "Panel reviews; trace summary",
                    "Clerk opens; summary trace",
                    "Reviews filing trace summary",
                    "Filing reviews trace summary",
                    "Filing / trace summary",
                    "Filing -- trace summary",
                    "Filing: trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_19_02_bounding_article_forms_missing(self):
        for run in ("The panel reviewed the "
                    "traceboardgatereviewannexpanelsummary",
                    "The panel logs "
                    "traceboardgatereviewannexpanelsummary",
                    "The panel reviewed the "
                    "traceboardgatereviewannexsummary",
                    "The panel reviewed the "
                    "traceboardgateannexreviewsummary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the cured converse forms of fix
    # passes 18 and 17 standing missing, and the governed
    # closings of fix pass 18 standing governed
    # ------------------------------------------------------

    def test_control_fix18_converse_forms_missing(self):
        for run in ("Panel reviewed trace summary",
                    "Clerk filed summary trace",
                    "Minutes show trace summary",
                    "Board recorded summary trace",
                    "Board filed summary trace",
                    "Panel reviewed tracesummary",
                    "Clerk filed summarytrace",
                    "Minutes show boardtracesummary",
                    "Panel reviewed traceboardgatesummary",
                    "Clerk filed summaryboardgatetrace",
                    "Panel reviewed "
                    "traceboardgatereviewannexsummary",
                    "Panel reviewed tracesummarizings",
                    "Reviewers noted tracesummary",
                    "Panel filed summarytrace",
                    "Gatekeepers reviewed boardtracesummary",
                    "Noted filing summary trace",
                    "Filing noted trace summary",
                    "Filing - trace summary",
                    "Filing (noted) trace summary",
                    "Filing; trace summary",
                    "Noted filing; summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_control_fix17_converse_forms_missing(self):
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

    def test_control_fix18_underreach_forms_governed(self):
        for head in ("Filestally", "Notestally", "Logtally",
                     "Booktallies", "Cardtallying", "Boardstallies",
                     "Foliotally", "Scrolltallies", "Volumetally",
                     "Notebooktallied", "Boardfiletally",
                     "Gatenotestally", "Reviewbooktally",
                     "Boardfoliotally", "Gatescrolltally",
                     "Gatefiletallyed", "Boardnotestalleys",
                     "Reviewbooktallyes", "Gatefoliotalleys",
                     "Talliez", "Tallieing", "Boardtalliez",
                     "Boardtallieing", "Tallye", "Talleied",
                     "Tallyings", "Boardtallye", "Boardtallyings",
                     "Trace summarisinges", "Trace summarieses",
                     "Trace summarisees", "Trace summariseses",
                     "Trace summarizingses", "Trace summaryings",
                     "Trace summarisationes", "Trace summariseres",
                     "Boardtracesummarisinges", "Tracesummarieses",
                     "Boardtracessummarisees",
                     "Boardtracesummarisationes", "Tracessummaryings",
                     "Traceboardgatereviewannexpanelsummary",
                     "Summaryboardgatereviewannexpaneltrace",
                     "Tracesboardgatereviewannexpanelsummary",
                     "Trace board gate review annex panel board "
                     "gate review summary",
                     "Trace board gate annex review panel board "
                     "gate annex summary",
                     "Summary board gate review annex panel board "
                     "gate trace",
                     "Summary board gate annex review panel board "
                     "gate trace",
                     "Trace board gate review annex panel board "
                     "gate review for step 2",
                     "Trace board gate annex review panel board "
                     "gate annex for step 2",
                     "Board ta\u026cly", "Board \u0288ally",
                     "Board tall\u01b4", "Trace \u0255ummarise",
                     "Trace s\u026fmmarise",
                     "Trace summarise\u018c",
                     "Trace summarise\u0256", "Trace s\u028bmmarise",
                     "Trace summar\u026ase", "Board t\u0251lly"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Held controls: every governed direct, fused and
    # inserted closing standing governed beside its
    # counted sibling, the long head and the Round head
    # among them, and in the beside and gate ruling
    # positions, with the governed tally forms
    # ------------------------------------------------------

    def test_governed_direct_closings_governed(self):
        for head in ("Trace summary", "Summary trace",
                     "Trace summaries", "Trace summarisers",
                     "Trace summarizers", "Trace summarisings",
                     "Trace summarys",
                     "Alpha beta gamma delta epsilon trace summary",
                     "Round's trace summary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_governed_direct_beside_and_gate_ruling(self):
        self._beside_step2_uncounted(_bad("Trace summary"))
        report = self._q4_alone(_bad("Trace summary"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    def test_governed_fused_closings_governed(self):
        for head in ("Tracesummary", "Tracesummaries",
                     "Boardtracesummary", "Boardtracesummarising",
                     "Boardtracesummarization", "Summarytrace",
                     "Boardsummarytraces", "Traceboardgatesummary",
                     "Traceboardgatepanelsummary",
                     "Summaryboardgatetrace", "Tracesboardsummary",
                     "Summaryboardtraces",
                     "Boardtracesummarisers",
                     "Boardtracessummarisers",
                     "Traceboardgatereviewannexpanelsummary",
                     "Summaryboardgatereviewannexpaneltrace",
                     "Tracesboardgatereviewannexpanelsummary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_governed_fused_beside_and_gate_ruling(self):
        self._beside_step2_uncounted(_bad("Tracesummary"))
        report = self._q4_alone(_bad("Tracesummary"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    def test_governed_inserted_closings_governed(self):
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
            self._candidate_governed(_bad(head), _read(head))

    def test_governed_tally_and_variant_forms_governed(self):
        for head in ("Boardtally", "Gate2tally", "Reviewtally",
                     "Step2tally", "Passtally", "Chairtally",
                     "Greentally", "Alphatally", "Boardtallied",
                     "Boardtallies", "Boardtallying",
                     "Gate record tally",
                     "Boardtallys", "Boardtallyed", "Boardtallyes",
                     "Tallys", "Tallyed", "Tallyes", "Talley",
                     "Talleys", "Talleyed", "Tallyies", "Tallie",
                     "Talleying"):
            self._candidate_governed(_bad(head), _read(head))

    def test_held_letter_form_governed(self):
        self._candidate_governed(_bad("Trace s\u0289mmarise"),
                                 _read("Trace s\u0289mmarise"))

    def test_code_level_governed_closings_head(self):
        for line in ("Trace summary: items checked stand here. "
                     "LANDED figures stand here, no counts stated",
                     "Tracesummary: items checked stand here. "
                     "LANDED figures stand here, no counts stated",
                     "Alpha beta gamma delta epsilon trace summary: "
                     "items checked stand here. LANDED figures "
                     "stand here, no counts stated"):
            self.assertTrue(_tally_statement_head(line), line)

    # ------------------------------------------------------
    # Held controls: the mixed inserted runs, the prose
    # order runs past the widened reach, the family forms
    # and the prose adverbs
    # ------------------------------------------------------

    def test_control_mixed_inserted_runs_missing(self):
        for run in ("Trace board of summary",
                    "Summary of board trace",
                    "Trace of board gate summary",
                    "Summary board of the trace",
                    "Trace the board summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_control_prose_order_past_wide_reach_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Trace review annex panel gate board gate "
            "review summary")))
        self._assert_q4_missing(self._q4_alone(_prose(
            "Summary review annex panel gate board gate trace")))

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
