"""Step 16 fix pass 22 unit 2 tests: the Q-4 widening unit.

Pinning tests for register item R16-22-01 (Medium, B22-C01
and B22-B01) of Step 16 round 22. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-22-01: malformed tally statement heads the restated
boundary of fix pass 21 still does not reach, in seventy
distinct alone forms in ten subfamilies, on the counted
pattern head agnosticism ground alone in every
subfamily: (a) genuine heads fused from record words
the governed fused prefix enumeration of seventy five
does not name, and tally forms fused behind the plurals
of governed prefixes and of record words, sixteen
forms; (b) a governed prefix in the opening position
with an unnamed record word immediately before the
tally form, ten forms; (c) variant spellings in that
composite opening position, four forms; (d) variant
spellings past the widened variant sets of twenty five
and twenty six, eight forms; (e) the summary word in
further forms past the fifty six, seven forms; (f)
fused trace summary closings built on those forms,
four forms; (g) fused closings with nine governed
words fused between the closing words, three forms;
(h) inserted word closings at twelve words forward and
eleven words reversed, four forms; (i) the for step
closing at twelve inserted words, one form; and (j)
the tally and summary words carrying further stroke
and hook letters the folding does not replace, thirteen
forms, no letter standing in both papers, the thirteen
letters standing at distinct codepoints across the two
papers, as the register states in the open. Twelve
forms stand driven in both papers in the same words
and stand counted once in this pinning, as the
register disposition states. Each alone form stands
missing beside its counted sibling on the entering
bytes, the beside forms standing present over Step 3
with Step 2 standing nowhere on the row and the gate
ruling forms standing missing in the same form. Locus:
derivation_core.py, _fold_word, _tally_word and the
constants _TALLY_WORD_FORMS, _TOTALLY_FAMILY,
_GOVERNED_FUSED_PREFIXES, _TALLY_WORD_VARIANT_FORMS
and _TALLY_WORD_VARIANT_FUSED_FORMS, _summary_word
and the constant _SUMMARY_WORD_FORMS,
_fused_trace_summary with _fused_between_closing, and
_tally_statement_head, its closing tests standing
after its docstring, against the standing test as fix
pass 22 Unit 1 restated it. The cure these tests pin
widens those tests in general terms, so each driven
form stands counted, in the alone position taking the
governed not derivable form naming the step and the
feeder piece, and in the beside position naming the
step uncounted, in gate records and gate rulings
alike, while every held control stands exactly as
before, and while no form of R16-22-02 reopens in any
position under the standing test as Unit 1 of this
pass restated it.

Held controls stand pinned beside the defect forms, in
full: every form of R16-22-02 standing missing in its
prose form, alone, beside and in gate rulings, as Unit
1 of this pass left it, its forty two distinct alone
forms and its bounding held controls among them, and
every form of R16-21-02, R16-20-02, R16-19-02,
R16-18-02 and R16-17-02 standing missing in the same
way; the cured underreach forms of fix pass 21 Unit 2
standing governed; the held standing forms
Logbooktally, Clipboardtally, Worksheettally and
Handbooktally standing governed in their exact forms;
the governed fused prefix forms and the variant forms
behind their governed prefixes standing governed; the
seven enumerated family adverbs and tallyho standing
missing, the fused family forms standing missing, and
the twelve prose adverbs of R16-14-02 standing
missing; the Board talli boundary control standing
missing; the folded round 10 prose sentence record
standing governed; the four folded marker shape
records standing present but not derivable; the golden
prose lines standing unflipped; and the read and
absent feeder controls byte for byte.
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


class TestStep16Fix22Unit2(FixtureTestCase):

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
    # R16-22-01 defect forms, subfamily (a): genuine
    # tally statement heads fused from record words the
    # governed fused prefix enumeration of seventy five
    # does not name, and tally forms fused behind the
    # plurals of governed prefixes and of record words
    # ------------------------------------------------------

    def test_r16_22_01_subfamily_a_governed(self):
        for head in ("Cabinettally",
                     "Vaulttally",
                     "Drawertally",
                     "Registerstallies",
                     "Binderstallies",
                     "Cardstallies",
                     "Exhibittally",
                     "Attachmenttally",
                     "Supplementtally",
                     "Addendumtally",
                     "Agendastally",
                     "Briefstallies",
                     "Protocolstally",
                     "Reportstallies",
                     "Reviewstallies",
                     "Notebookstallies"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-22-01 defect forms, subfamily (b): a governed
    # prefix standing in the opening position with a
    # record word the widened enumeration does not name
    # standing immediately before the tally form
    # ------------------------------------------------------

    def test_r16_22_01_subfamily_b_governed(self):
        for head in ("Boardcabinettally",
                     "Gatevaulttally",
                     "Reviewdrawertally",
                     "Boardexhibittally",
                     "Gateattachmenttally",
                     "Reviewsupplementtallies",
                     "Boardagendastally",
                     "Gatereportstally",
                     "Reviewbriefstallies",
                     "Boardprotocolstally"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-22-01 defect forms, subfamily (c): the variant
    # spellings standing in that composite opening
    # position
    # ------------------------------------------------------

    def test_r16_22_01_subfamily_c_governed(self):
        for head in ("Boardcabinettallyed",
                     "Gatevaulttallyes",
                     "Boardagendastallye",
                     "Gatereportstalliez"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-22-01 defect forms, subfamily (d): variant
    # spellings past the widened variant sets of twenty
    # five and twenty six
    # ------------------------------------------------------

    def test_r16_22_01_subfamily_d_governed(self):
        for head in ("Tallyeu",
                     "Tallyau",
                     "Boardtallyeu",
                     "Boardtallyau",
                     "Tallyui",
                     "Talleui",
                     "Boardtallyui",
                     "Boardtallyuo"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-22-01 defect forms, subfamily (e): the summary
    # word in further forms past the fifty six
    # ------------------------------------------------------

    def test_r16_22_01_subfamily_e_governed(self):
        for head in ("Trace summarisereseseses",
                     "Trace summarisingeseseses",
                     "Trace summarieseseseses",
                     "Trace summarisedeseseses",
                     "Trace summariseeseseseses",
                     "Trace summaryeseseseses",
                     "Trace summarisationeseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-22-01 defect forms, subfamily (f): fused trace
    # summary closings built on those further forms
    # ------------------------------------------------------

    def test_r16_22_01_subfamily_f_governed(self):
        for head in ("Boardtracesummarisereseseses",
                     "Tracessummarieseseseses",
                     "Boardtracesummarisedeseseses",
                     "Tracessummaryeseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-22-01 defect forms, subfamily (g): fused
    # closings with nine governed words fused between
    # the closing words
    # ------------------------------------------------------

    def test_r16_22_01_subfamily_g_governed(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewannexsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewannextrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewannexsummary"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-22-01 defect forms, subfamily (h): inserted
    # word closings at twelve words forward and eleven
    # words reversed
    # ------------------------------------------------------

    def test_r16_22_01_subfamily_h_governed(self):
        for head in ("Trace board gate review annex panel board gate review "
                     "annex panel board gate summary",
                     "Trace board gate annex review panel board gate annex "
                     "review panel board gate summary",
                     "Summary board gate review annex panel board gate "
                     "review annex panel board trace",
                     "Summary board gate annex review panel board gate "
                     "annex review panel board trace"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-22-01 defect forms, subfamily (i): the for step
    # closing at twelve inserted words
    # ------------------------------------------------------

    def test_r16_22_01_subfamily_i_governed(self):
        self._candidate_governed(
            _bad("Trace board gate review annex panel board "
                 "gate review annex panel board gate for step 2"),
            _read("Trace board gate review annex panel board "
                  "gate review annex panel board gate for step 2"))

    # ------------------------------------------------------
    # R16-22-01 defect forms, subfamily (j): the tally
    # and summary words carrying further stroke and hook
    # letters the folding does not replace. No letter of
    # this subfamily stands in both papers, the thirteen
    # letters standing at distinct codepoints across the
    # two papers, as the register states in the open.
    # ------------------------------------------------------

    def test_r16_22_01_subfamily_j_governed(self):
        for head in ("Trace \u028dummarise",
                     "Board \u0298ally",
                     "Trace summaris\u025e",
                     "Board \u02adally",
                     "Trace summarise\u025f",
                     "Board \u0299ally",
                     "Board ta\u029ely",
                     "Board tall\u02a2",
                     "Trace \u0280ummarise",
                     "Trace su\u0274marise",
                     "Trace summa\u0278ise",
                     "Trace summaris\u029a",
                     "Trace summaris\u02a1"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-22-01 beside and gate ruling forms: the beside
    # forms standing present over Step 3 with Step 2
    # named uncounted after the cure, and the gate ruling
    # forms standing governed in the ruling form
    # ------------------------------------------------------

    def test_r16_22_01_beside_forms_uncounted(self):
        for head in ("Cabinettally", "Trace summarisereseseses",
                     "Exhibittally", "Trace summarisedeseseses"):
            self._beside_step2_uncounted(_bad(head))

    def test_r16_22_01_gate_ruling_forms_governed(self):
        for head in ("Cabinettally", "Exhibittally",
                     "Trace summarisereseseses"):
            report = self._q4_alone(_bad(head), ruling=True)
            self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # R16-22-01 code level forms: the driven words under
    # the word tests, the driven heads under the head
    # test, and the thirteen defect letters under the fold
    # ------------------------------------------------------

    def test_r16_22_01_code_level_forms(self):
        for word in ("cabinettally",
                     "vaulttally",
                     "drawertally",
                     "registerstallies",
                     "binderstallies",
                     "cardstallies",
                     "exhibittally",
                     "attachmenttally",
                     "supplementtally",
                     "addendumtally",
                     "agendastally",
                     "briefstallies",
                     "protocolstally",
                     "reportstallies",
                     "reviewstallies",
                     "notebookstallies",
                     "boardcabinettally",
                     "gatevaulttally",
                     "reviewdrawertally",
                     "boardexhibittally",
                     "gateattachmenttally",
                     "reviewsupplementtallies",
                     "boardagendastally",
                     "gatereportstally",
                     "reviewbriefstallies",
                     "boardprotocolstally",
                     "boardcabinettallyed",
                     "gatevaulttallyes",
                     "boardagendastallye",
                     "gatereportstalliez",
                     "tallyeu",
                     "tallyau",
                     "boardtallyeu",
                     "boardtallyau",
                     "tallyui",
                     "talleui",
                     "boardtallyui",
                     "boardtallyuo"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ("summarisereseseses",
                     "summarisingeseseses",
                     "summarieseseseses",
                     "summarisedeseseses",
                     "summariseeseseseses",
                     "summaryeseseseses",
                     "summarisationeseseseses"):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ("boardtracesummarisereseseses",
                     "tracessummarieseseseses",
                     "boardtracesummarisedeseseses",
                     "tracessummaryeseseseses",
                     "traceboardgatereviewannexpanelboardgatereviewannexsummary",
                     "summaryboardgatereviewannexpanelboardgatereviewannextrace",
                     "tracesboardgatereviewannexpanelboardgatereviewannexsummary"):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        for head in ("Cabinettally",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate summary",
                     "Summary board gate annex review panel board "
                     "gate annex review panel board trace",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate for step 2",
                     "Trace summarisereseseses"):
            line = head + ": items checked stand here"
            self.assertTrue(_tally_statement_head(line), head)
        self.assertEqual(_fold_word("\u028dummarise"), "summarise")
        self.assertEqual(_fold_word("\u0298ally"), "tally")
        self.assertEqual(_fold_word("summaris\u025e"), "summarise")
        self.assertEqual(_fold_word("\u02adally"), "tally")
        self.assertEqual(_fold_word("summarise\u025f"), "summarised")
        self.assertEqual(_fold_word("\u0299ally"), "tally")
        self.assertEqual(_fold_word("ta\u029ely"), "tally")
        self.assertEqual(_fold_word("tall\u02a2"), "tally")
        self.assertEqual(_fold_word("\u0280ummarise"), "summarise")
        self.assertEqual(_fold_word("su\u0274marise"), "summarise")
        self.assertEqual(_fold_word("summa\u0278ise"), "summarise")
        self.assertEqual(_fold_word("summaris\u029a"), "summarise")
        self.assertEqual(_fold_word("summaris\u02a1"), "summarised")

    # ------------------------------------------------------
    # Held controls: every form of R16-21-02 standing
    # missing in its prose form, as Unit 1 of this pass
    # left it, its thirty nine distinct alone forms in
    # three subfamilies, its gate ruling and beside forms
    # and its bounding held controls
    # ------------------------------------------------------

    def test_r16_21_02_held_direct_forms_missing(self):
        for run in ("Panel draft trace summary",
                    "Clerk lodge summary trace",
                    "Board publish trace summary",
                    "Team gather summary trace",
                    "Panel chose trace summary",
                    "Clerk spoke summary trace",
                    "Panel broke trace summary",
                    "Clerk kept summary trace",
                    "Team drew trace summary",
                    "Panel froze summary trace",
                    "Team found summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_21_02_held_fused_forms_missing(self):
        for run in ("Panel draft tracesummary",
                    "Clerk lodge summarytrace",
                    "Panel draft boardtracesummary",
                    "Team publish traceboardgatesummary",
                    "Panel draft traceboardgatereviewannexpanelsummary",
                    "Panel draft traceboardgatereviewannexpanelboardsummary",
                    "Panel draft traceboardgatereviewannexpanelboardgatesummary",
                    "Draft panel tracesummary",
                    "Panel chose tracesummary",
                    "Clerk kept summarytrace",
                    "Team drew boardtracesummary",
                    "Panel froze traceboardgatesummary",
                    "Clerk spoke traceboardgatereviewannexpanelboardgatesummary",
                    "Team found tracesummarisedeses"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_21_02_held_run_and_clause_forms_missing(self):
        for run in ("Ledger _ trace summary",
                    "Ledger ~ trace summary",
                    "Ledger = trace summary",
                    "Ledger + trace summary",
                    "Draft panel trace summary",
                    "Lodge ledger summary trace",
                    "Publish panel summary trace",
                    "Ledger // trace summary",
                    "Ledger \u2014 trace summary",
                    'Ledger "panel" trace summary',
                    "Ledger *panel* trace summary",
                    "Ledger _panel_ trace summary",
                    "Chose panel summary trace",
                    "Kept ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_21_02_held_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel draft trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel chose trace summary"), ruling=True))
        self._beside_step2_nowhere(_prose("Panel draft trace summary"))
        self._beside_step2_nowhere(_prose("Panel chose trace summary"))

    def test_r16_21_02_held_code_level_prose_no_head(self):
        for run in ("Panel draft trace summary",
                    "Clerk spoke trace summary",
                    "Panel draft tracesummary",
                    "Ledger _ trace summary",
                    "Chose panel summary trace"):
            line = run + ": items checked stand here"
            self.assertFalse(_tally_statement_head(line), run)

    def test_r16_21_02_bounding_controls_missing(self):
        for run in ("Panel draft trace board gate summary",
                    "Panel draft trace board gate review "
                    "annex panel board gate summary",
                    "Panel chose trace board gate summary",
                    "Clerk kept summary board gate trace",
                    "Panel reviewed trace board gate summary",
                    "Panel logs trace board gate summary",
                    "The panel drafted the "
                    "traceboardgatereviewannexpanelsummary",
                    "The panel chose "
                    "traceboardgatereviewannexpanelsummary",
                    "The panel reviewed the "
                    "traceboardgatereviewannexsummary",
                    "Ledger - trace summary",
                    "Ledger (panel) trace summary",
                    "Ledger [panel] trace summary",
                    "Ledger \\\\ trace summary",
                    "Ledger || trace summary",
                    "Reviews filing trace summary",
                    "Filing reviews trace summary",
                    "Panel drafts "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "Panel drafts trace summary",
                    "Clerk lodges summary trace",
                    "Panel drafted trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: every form of R16-22-02 standing
    # missing in its prose form, as Unit 1 of this pass
    # left it, its direct forms
    # ------------------------------------------------------

    def test_r16_22_02_held_direct_forms_missing(self):
        for run in ("Panel edit trace summary",
                    "Clerk bind summary trace",
                    "Board print trace summary",
                    "Team stamp summary trace",
                    "Panel wore trace summary",
                    "Clerk swore summary trace",
                    "Panel tore trace summary",
                    "Panel paid trace summary",
                    "Clerk brought summary trace",
                    "Team caught trace summary",
                    "Panel sold summary trace",
                    "Clerk woke trace summary",
                    "Team drove summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the fused forms of R16-22-02
    # standing missing in the same way
    # ------------------------------------------------------

    def test_r16_22_02_held_fused_forms_missing(self):
        for run in ("Panel edit tracesummary",
                    "Clerk print summarytrace",
                    "Panel edit boardtracesummary",
                    "Team stamp traceboardgatesummary",
                    "Panel edit traceboardgatereviewannexpanelsummary",
                    "Panel edit "
                    "traceboardgatereviewannexpanelboardsummary",
                    "Panel edit "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "Panel edit "
                    "traceboardgatereviewannexpanelboardgatereviewsummary",
                    "Edit panel tracesummary",
                    "Panel paid tracesummary",
                    "Clerk brought summarytrace",
                    "Team caught boardtracesummary",
                    "Panel sold traceboardgatesummary",
                    "Clerk woke "
                    "traceboardgatereviewannexpanelboardgatereviewsummary",
                    "Team drove tracesummarisedeseses"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the run join, aside and verb first
    # clause forms of R16-22-02 standing missing in the
    # same way
    # ------------------------------------------------------

    def test_r16_22_02_held_run_and_clause_forms_missing(self):
        for run in ("Ledger \u00a7 trace summary",
                    "Ledger @ trace summary",
                    "Ledger # trace summary",
                    "Ledger % trace summary",
                    "Ledger 'panel' trace summary",
                    "Ledger `panel` trace summary",
                    "Edit panel trace summary",
                    "Print ledger summary trace",
                    "Stamp panel summary trace",
                    "Ledger ^ trace summary",
                    "Ledger & trace summary",
                    "Ledger \u00abpanel\u00bb trace summary",
                    "Paid panel summary trace",
                    "Brought ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_22_02_held_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel edit trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel paid trace summary"), ruling=True))
        self._beside_step2_nowhere(_prose("Panel edit trace summary"))
        self._beside_step2_nowhere(_prose("Panel paid trace summary"))

    def test_r16_22_02_held_code_level_prose_no_head(self):
        for run in ("Panel edit trace summary",
                    "Panel paid trace summary",
                    "Panel edit tracesummary",
                    "Ledger @ trace summary",
                    "Paid panel summary trace"):
            line = run + ": items checked stand here"
            self.assertFalse(_tally_statement_head(line), run)

    def test_r16_22_02_bounding_controls_missing(self):
        for run in ("Panel edit trace board gate summary",
                    "Panel paid trace board gate summary",
                    "Clerk brought summary board gate trace",
                    "Panel draft trace board gate summary",
                    "Panel chose trace board gate summary",
                    "Clerk kept summary board gate trace",
                    "The panel paid "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "Ledger - trace summary",
                    "Ledger (panel) trace summary",
                    "Ledger [panel] trace summary",
                    "Ledger \\ trace summary",
                    "Ledger || trace summary",
                    "Reviews filing trace summary",
                    "Filing reviews trace summary",
                    "Panel drafts "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "Panel edits trace summary",
                    "Panel edited trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the cured underreach forms of fix
    # pass 21 Unit 2 standing governed in their exact
    # forms, the fused and tally heads among them
    # ------------------------------------------------------

    def test_control_fix21_underreach_forms_governed(self):
        for head in ("Reporttally",
                     "Agendatally",
                     "Reporttallies",
                     "Dossierstally",
                     "Voucherstally",
                     "Ticketstally",
                     "Brieftally",
                     "Protocoltally",
                     "Pagestally",
                     "Packetstallies",
                     "Folderstallies",
                     "Dossierstallies",
                     "Voucherstallies",
                     "Ticketstallies",
                     "Annexestally",
                     "Schedulestally",
                     "Boardreporttally",
                     "Gateagendatally",
                     "Reviewbrieftally",
                     "Boardpagestally",
                     "Gatepacketstally",
                     "Reviewfolderstallies",
                     "Boardannexestally",
                     "Boardreporttallyed",
                     "Gateagendatallyes",
                     "Boardpagestallye",
                     "Gatepacketstalliez",
                     "Tallyio",
                     "Tallyua",
                     "Boardtallyio",
                     "Boardtallyua",
                     "Tallyiu",
                     "Talleio",
                     "Boardtallyiu",
                     "Trace summarisereseses",
                     "Trace summarisingeseses",
                     "Trace summarieseseses",
                     "Trace summarisedeseses",
                     "Trace summariseeseseses",
                     "Trace summaryeseseses",
                     "Trace summarisationeseseses",
                     "Boardtracesummarisereseses",
                     "Tracessummarieseseses",
                     "Boardtracesummarisedeseses",
                     "Tracessummaryeseseses",
                     "Traceboardgatereviewannexpanelboardgatereviewsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewtrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewsummary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_held_standing_forms_of_this_item_governed(self):
        for head in ("Logbooktally", "Clipboardtally",
                     "Worksheettally", "Handbooktally"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Held controls: the cured converse forms of fix
    # passes 19, 18 and 17 standing missing, and the
    # governed underreach forms of fix pass 19 standing
    # governed
    # ------------------------------------------------------

    def test_r16_19_02_held_forms_missing(self):
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
                    "Team tracks summary trace",
                    "Panel reviews tracesummary",
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
                    "Panel logs tracesummarisinges",
                    "Ledger [panel] trace summary",
                    "Ledger / trace summary",
                    "Ledger -- trace summary",
                    "Logs panel summary trace",
                    "Marks ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

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

    def test_control_fix20_underreach_forms_governed(self):
        for head in (
                     "Dossiertally", "Annextally", "Scheduletally",
                     "Appendixtally", "Dossiertallies", "Memostally",
                     "Chartstallies", "Sheetstallies", "Vouchertally",
                     "Tickettally", "Ledgerstally", "Rosterstallies",
                     "Journalstally", "Chairstally", "Boarddossiertally",
                     "Gateannextally", "Reviewappendixtally", "Boardvouchertally",
                     "Gatedossiertally", "Reviewtickettally", "Boarddossiertallyed",
                     "Gateannextallyes", "Boardvouchertallye", "Gatedossiertalliez",
                     "Tallyia", "Tallyeo", "Boardtallyia",
                     "Boardtallyeo", "Tallyiz", "Talleiz",
                     "Boardtallyiz", "Trace summarisedeses", "Trace summarisereses",
                     "Trace summarisingeses", "Trace summariesese", "Trace summariseeseses",
                     "Trace summaryeseses", "Trace summarisationeseses", "Boardtracesummarisedeses",
                     "Tracessummarisereses", "Boardtracesummariseeseses", "Tracessummaryeseses",
                     "Traceboardgatereviewannexpanelboardgatesummary", "Summaryboardgatereviewannexpanelboardgatetrace", "Tracesboardgatereviewannexpanelboardgatesummary",
                     "Trace board gate review annex panel board gate review annex panel summary", "Trace board gate annex review panel board gate annex review panel summary", "Summary board gate review annex panel board gate review annex trace",
                     "Summary board gate annex review panel board gate annex review trace", "Trace board gate review annex panel board gate review annex panel for step 2", "Trace ƈummarise",
                     "Board taƥly", "Trace summariseʄ", "Trace ɋummarise",
                     "Board tallʗ", "Board ƫally", "Board tɐlly",
                     "Trace ƨummarise", "Trace summarisɘ", "Board ȶally"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix19_underreach_forms_governed(self):
        for head in ("Memotally", "Slipstally", "Charttally",
                     "Sheettally", "Pagetalies", "Panelstally",
                     "Gatestallies", "Teamstally", "Packettally",
                     "Foldertallies", "Bindertally", "Sheettallied",
                     "Panelstallies", "Recordstallied",
                     "Boardmemotally", "Gatecharttally",
                     "Reviewslipstally", "Boardpackettally",
                     "Gatefoldertally", "Reviewbindertally",
                     "Gatememotalleys", "Boardcharttallyed",
                     "Boardpackettallye", "Gatefoldertalliez",
                     "Tallyie", "Tallyin", "Talleies",
                     "Boardtallyie", "Boardtallyin",
                     "Trace summariseeses",
                     "Trace summarizationeses",
                     "Trace summarieseses", "Trace summarisedses",
                     "Trace summarisedes", "Trace summarizeres",
                     "Trace summarisationeses",
                     "Trace summaryeses",
                     "Boardtracesummariseeses", "Tracessummarieseses",
                     "Boardtracesummarisedes",
                     "Tracessummaryeses",
                     "Traceboardgatereviewannexpanelboardsummary",
                     "Summaryboardgatereviewannexpanelboardtrace",
                     "Tracesboardgatereviewannexpanelboardsummary",
                     "Trace board gate review annex panel board "
                     "gate review annex summary",
                     "Trace board gate annex review panel board "
                     "gate annex review summary",
                     "Summary board gate review annex panel board "
                     "gate review trace",
                     "Summary board gate annex review panel board "
                     "gate annex trace",
                     "Trace board gate review annex panel board "
                     "gate review annex for step 2",
                     "Trace summarise\u02a0",
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

    # ------------------------------------------------------
    # Held controls: every governed direct, fused and
    # inserted closing standing governed beside its
    # counted sibling, the long head and the Round head
    # among them, and in the beside and gate ruling
    # positions, with the governed tally forms, the held
    # letter form and the held candidate form
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

    def test_held_standing_forms_governed(self):
        self._candidate_governed(_bad("Trace s\u0289mmarise"),
                                 _read("Trace s\u0289mmarise"))

    def test_held_candidate_form_governed(self):
        self._candidate_governed(_bad("Pagetallies"),
                                 _read("Pagetallies"))

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
