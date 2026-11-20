"""Step 16 fix pass 18 unit 2 tests: the Q-4 tally head unit.

Pinning tests for register item R16-18-01 (Medium, B18-B01
merged with B18-C01 to B18-C07) of Step 16 round 18. The
governing rule of the pass, in its extended form: a piece
not read in full, for whatever reason, is not read, and
its converse: a piece that is no feeder flips nothing.

R16-18-01: sixty distinct alone forms in ten subfamilies
stand missing beside their counted siblings on the
counted pattern ground alone, past the restated boundary
of fix pass 17. The counted pattern counts the numeric
tally form with no head test at all, so every head under
which a counted sibling counts stands as a tally
statement head in the reach the row itself uses. The
subfamilies stand as follows: (a) genuine heads fused
from record words the widened governed fused prefix
enumeration of twenty seven still does not name, ten
forms; (b) composite openings, a governed prefix
standing in the opening position with an unnamed record
word standing immediately before the tally form, five
forms; (c) variant spellings in that composite opening
position, four forms; (d) variant spellings past the
widened variant sets, standing alone and behind governed
prefixes, nine forms; (e) summary word further forms
past the twenty six, eight forms; (f) fused trace
summary closings built on those forms, five forms;
(g) fused closings with five governed words fused
between the closing words, three forms; (h) inserted
closings at eight words forward and seven words
reversed, four forms; (i) for step closings at eight
inserted words, two forms; and (j) further stroke and
hook fold letters past the widened fold set, ten forms.
The beside forms stand driven in the Filestally head and
in the Trace summarisinges head, and the gate ruling
form in the Filestally head. Locus: derivation_core.py,
_fold_word, _tally_word and its constants, _summary_word
and its constant, _fused_trace_summary with
_fused_between_closing, and _tally_statement_head and
its closing tests, against _trace_candidates and the
shared constant _TALLY_COUNTED_PATTERN, which carries
no head test. The cure these tests pin widens the stated
boundary in general terms and restates it: the governed
fused prefix enumeration at its new width, the variant
spellings in their positions, the summary word in its
further forms, the fused between reach at five words,
the inserted counts at eight forward, seven reversed
and eight in the for step form under the wide record
order, and the folding at its further letters, so each
defect form stands governed, alone, beside, and in gate
rulings, while every form standing missing for governed
reasons stays missing and every form standing governed
stays governed.

Held controls stand pinned beside the defect forms, in
full: every form of R16-18-02 standing missing in its
cured standing as fix pass 18 Unit 1 left it, its prose
sentences, prose clauses and prose runs standing missing
alone, beside and in gate rulings, the fused between
prose sentence at the widened count of five fused words
standing missing among them, and its bounding inserted
prose tails and fused between prose sentences standing
missing; the eleven prose forms of R16-17-02 standing
missing; the governed direct, fused and inserted
closings standing governed in every driven position, the
long trace summary head and the Round trace summary head
among them; the held letter form of the earlier passes
standing governed; the mixed inserted runs and the prose
order runs at the admitted counts and at the widened
counts standing missing; the seven enumerated family
adverbs and tallyho standing missing, the fused family
forms standing missing, and the twelve prose adverbs of
R16-14-02 standing missing; the Board talli boundary
control standing missing; the folded round 10 prose
sentence record standing governed; the four folded
marker shape records standing present but not derivable;
the golden prose lines standing unflipped; and the read
and absent feeder controls byte for byte.
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


class TestStep16Fix18Unit2(FixtureTestCase):

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
    # R16-18-01 defect forms, subfamily (a): genuine heads
    # fused from record words the widened enumeration of
    # twenty seven still does not name, each standing
    # governed beside its counted sibling after the cure
    # ------------------------------------------------------

    def test_r16_18_01_subfamily_a_governed(self):
        for head in ("Filestally", "Notestally", "Logtally",
                     "Booktallies", "Cardtallying", "Boardstallies",
                     "Foliotally", "Scrolltallies", "Volumetally",
                     "Notebooktallied"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_18_01_subfamily_b_governed(self):
        for head in ("Boardfiletally", "Gatenotestally",
                     "Reviewbooktally", "Boardfoliotally",
                     "Gatescrolltally"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_18_01_subfamily_c_governed(self):
        for head in ("Gatefiletallyed", "Boardnotestalleys",
                     "Reviewbooktallyes", "Gatefoliotalleys"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_18_01_subfamily_d_governed(self):
        for head in ("Talliez", "Tallieing", "Boardtalliez",
                     "Boardtallieing", "Tallye", "Talleied",
                     "Tallyings", "Boardtallye", "Boardtallyings"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_18_01_subfamily_e_governed(self):
        for head in ("Trace summarisinges", "Trace summarieses",
                     "Trace summarisees", "Trace summariseses",
                     "Trace summarizingses", "Trace summaryings",
                     "Trace summarisationes", "Trace summariseres"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_18_01_subfamily_f_governed(self):
        for head in ("Boardtracesummarisinges", "Tracesummarieses",
                     "Boardtracessummarisees",
                     "Boardtracesummarisationes",
                     "Tracessummaryings"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_18_01_subfamily_g_governed(self):
        for head in ("Traceboardgatereviewannexpanelsummary",
                     "Summaryboardgatereviewannexpaneltrace",
                     "Tracesboardgatereviewannexpanelsummary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_18_01_subfamily_h_governed(self):
        for head in ("Trace board gate review annex panel board "
                     "gate review summary",
                     "Trace board gate annex review panel board "
                     "gate annex summary",
                     "Summary board gate review annex panel board "
                     "gate trace",
                     "Summary board gate annex review panel board "
                     "gate trace"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_18_01_subfamily_i_governed(self):
        for head in ("Trace board gate review annex panel board "
                     "gate review for step 2",
                     "Trace board gate annex review panel board "
                     "gate annex for step 2"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_18_01_subfamily_j_governed(self):
        for head in ("Board ta\u026cly", "Board \u0288ally",
                     "Board tall\u01b4", "Trace \u0255ummarise",
                     "Trace s\u026fmmarise",
                     "Trace summarise\u018c",
                     "Trace summarise\u0256", "Trace s\u028bmmarise",
                     "Trace summar\u026ase", "Board t\u0251lly"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_18_01_beside_filestally_uncounted(self):
        self._beside_step2_uncounted(_bad("Filestally"))

    def test_r16_18_01_beside_summarisinges_uncounted(self):
        self._beside_step2_uncounted(_bad("Trace summarisinges"))

    def test_r16_18_01_gate_ruling_filestally_governed(self):
        report = self._q4_alone(_bad("Filestally"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # Code level defect tests: the widened reach in general
    # combination forms of the same families
    # ------------------------------------------------------

    def test_code_level_new_prefixes_and_composites(self):
        for word in ("filestally", "notestally", "logtally",
                     "booktallies", "cardtallying", "boardstallies",
                     "foliotally", "scrolltallies", "volumetally",
                     "notebooktallied", "boardfiletally",
                     "gatenotestally", "reviewbooktally",
                     "boardfoliotally", "gatescrolltally",
                     "gatebooktally", "reviewcardtallied",
                     "panelfoliotallying", "chairlogtallies"):
            self.assertTrue(_tally_word(word), word)

    def test_code_level_variant_spellings_positions(self):
        for word in ("tallye", "talleied", "tallyings", "talliez",
                     "tallieing", "boardtallye", "boardtallyings",
                     "boardtalliez", "boardtallieing",
                     "gatefiletallyed", "boardnotestalleys",
                     "reviewbooktallyes", "gatefoliotalleys",
                     "chairtallyings", "paneltalliez"):
            self.assertTrue(_tally_word(word), word)

    def test_code_level_summary_word_further_forms(self):
        for word in ("summarisinges", "summarieses", "summarisees",
                     "summariseses", "summarizingses", "summaryings",
                     "summarisationes", "summariseres"):
            self.assertTrue(_summary_word(word), word)

    def test_code_level_fused_closings_further_forms(self):
        for word in ("boardtracesummarisinges", "tracesummarieses",
                     "boardtracessummarisees",
                     "boardtracesummarisationes",
                     "tracessummaryings",
                     "traceboardgatereviewannexpanelsummary",
                     "summaryboardgatereviewannexpaneltrace",
                     "tracesboardgatereviewannexpanelsummary"):
            self.assertTrue(_fused_trace_summary(word), word)

    def test_code_level_inserted_and_for_step_widened(self):
        for run in ("Trace board gate review annex panel board "
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
                    "gate annex for step 2"):
            self.assertTrue(_tally_statement_head(
                run + ": items checked stand here. LANDED "
                "figures stand here, no counts stated"), run)

    def test_code_level_fold_further_letters(self):
        self.assertEqual(_fold_word("ta\u026cly"), "tally")
        self.assertEqual(_fold_word("\u0288ally"), "tally")
        self.assertEqual(_fold_word("tall\u01b4"), "tally")
        self.assertEqual(_fold_word("\u0255ummarise"), "summarise")
        self.assertEqual(_fold_word("s\u026fmmarise"), "summarise")
        self.assertEqual(_fold_word("summarise\u018c"), "summarised")
        self.assertEqual(_fold_word("summarise\u0256"), "summarised")
        self.assertEqual(_fold_word("s\u028bmmarise"), "summarise")
        self.assertEqual(_fold_word("summar\u026ase"), "summarise")
        self.assertEqual(_fold_word("t\u0251lly"), "tally")
        for head in ("Board ta\u026cly", "Trace summarise\u018c"):
            self.assertTrue(_tally_statement_head(
                head + ": items checked stand here. LANDED "
                "figures stand here, no counts stated"), head)

    # ------------------------------------------------------
    # Held controls: every form of R16-18-02 standing
    # missing in its cured standing, alone, beside and in
    # gate rulings, the fused between prose sentence at the
    # widened count standing missing among them
    # ------------------------------------------------------

    def test_control_r16_18_02_prose_forms_missing(self):
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

    def test_control_r16_18_02_gate_ruling_and_beside(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel reviewed trace summary"), ruling=True))
        self._beside_step2_nowhere(
            _prose("Panel reviewed trace summary"))

    def test_control_r16_18_02_fused_between_widened_count(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Panel reviewed "
            "traceboardgatereviewannexpanelsummary")))
        self._assert_q4_missing(self._q4_alone(_prose(
            "Clerk filed "
            "summaryboardgatereviewannexpaneltrace")))

    def test_control_r16_18_02_code_level_no_head(self):
        for run in ("Panel reviewed trace summary",
                    "Panel reviewed tracesummary",
                    "Panel reviewed "
                    "traceboardgatereviewannexpanelsummary",
                    "Filing; trace summary"):
            self.assertFalse(_tally_statement_head(
                run + ": LANDED figures stand here, "
                "no counts stated"), run)

    def test_bounding_inserted_prose_tails_missing(self):
        for run in ("Panel reviewed trace board gate summary",
                    "Clerk filed summary board gate trace",
                    "Panel reviewed trace board gate review "
                    "annex panel summary",
                    "Panel reviewed trace board gate review "
                    "annex panel board gate summary",
                    "Clerk filed summary board gate review "
                    "annex panel board gate trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_inserted_sentence_tail_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("She filed the trace gate summary")))

    def test_bounding_fused_between_four_words_missing(self):
        for run in ("The panel reviewed the "
                    "traceboardgatereviewannexsummary",
                    "The panel reviewed the "
                    "traceboardgateannexreviewsummary"):
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

    # ------------------------------------------------------
    # Held controls: governed closings standing governed,
    # the held letter form, and the widened count standings
    # ------------------------------------------------------

    def test_governed_direct_closings_governed(self):
        for head in ("Trace summary", "Summary trace",
                     "Trace summaries", "Trace summarisers",
                     "Trace summarizers", "Trace summarisings",
                     "Trace summarys",
                     "Alpha beta gamma delta epsilon trace summary",
                     "Round's trace summary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_governed_fused_closings_governed(self):
        for head in ("Tracesummary", "Tracesummaries",
                     "Boardtracesummary", "Boardtracesummarising",
                     "Boardtracesummarization", "Summarytrace",
                     "Boardsummarytraces", "Traceboardgatesummary",
                     "Traceboardgatepanelsummary",
                     "Summaryboardgatetrace", "Tracesboardsummary",
                     "Summaryboardtraces",
                     "Boardtracesummarisers",
                     "Boardtracessummarisers"):
            self._candidate_governed(_bad(head), _read(head))

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
                     "Trace board gate review annex panel board "
                     "gate summary",
                     "Summary board gate review annex panel board "
                     "trace",
                     "Trace for step 2", "Trace board for step 2",
                     "Trace board gate for step 2",
                     "Trace board gate review annex for step 2",
                     "Trace board gate review annex panel board "
                     "gate for step 2"):
            self._candidate_governed(_bad(head), _read(head))

    def test_governed_tally_fused_forms_governed(self):
        for head in ("Boardtally", "Gate2tally", "Reviewtally",
                     "Step2tally", "Passtally", "Chairtally",
                     "Greentally", "Alphatally", "Boardtallied",
                     "Boardtallies", "Boardtallying",
                     "Gate record tally"):
            self._candidate_governed(_bad(head), _read(head))

    def test_held_letter_t_hook_governed(self):
        self._candidate_governed(_bad("Board \u01acally"),
                                 _read("Board \u01acally"))

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
    # Held controls: prose and ungoverned forms standing
    # missing at the widened counts and past them
    # ------------------------------------------------------

    def test_control_mixed_inserted_runs_missing(self):
        for run in ("Trace board of summary",
                    "Summary of board trace",
                    "Trace of board gate summary",
                    "Summary board of the trace",
                    "Trace the board summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_control_prose_order_at_widened_counts_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Trace review annex panel gate board gate "
            "review summary")))
        self._assert_q4_missing(self._q4_alone(_prose(
            "Summary review annex panel gate board gate trace")))
        self._candidate_missing(_bad(
            "Traceboardpanelgatereviewannexsummary"),
            _read("Traceboardpanelgatereviewannexsummary"))

    def test_control_prose_order_past_wide_reach_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Trace review annex panel gate board gate "
            "review summary")))
        self._assert_q4_missing(self._q4_alone(_prose(
            "Summary review annex panel gate board gate trace")))

    def test_control_converse_hunting_forms_missing(self):
        for run in ("Traceofsummary", "Tracethesummary",
                    "Trace 2 summary", "Trace board board summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

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
