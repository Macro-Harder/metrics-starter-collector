"""Step 16 fix pass 18 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-18-02 (Medium, B18-B02,
B18-C08 and B18-C09) of Step 16 round 18. The governing
rule of the pass, in its extended form: a piece not read
in full, for whatever reason, is not read, and its
converse: a piece that is no feeder flips nothing.

R16-18-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head read what
stands before the closing words through the standing test
of fix pass 17 Unit 1, which reads only the sentence
function words and the comma, so prose standing before a
direct or fused closing in the shapes of this round takes
a tally statement head and stands present but not
derivable. Four subfamilies stand driven: (a) prose
sentences whose closing words stand in the direct trace
summary form, five forms, each carrying a bare noun
subject and a main verb before the closing words and no
sentence function word and no comma before them; (b) prose
sentences whose last word stands in a fused trace summary
form, ten forms in the same shape; (c) prose standing
before a governed closing inside one statement, four
forms, prose clauses in verb phrase form, a prose run
joined to the closing by a hyphen, and a prose run
carrying a parenthetical; and (d) prose clauses set off by
a semicolon standing before the direct and reversed
direct closings, two forms. Twenty one distinct alone
forms in all, the first direct form driven in a gate
ruling and beside a counted Step 3 trace as well. The
defect stands bounded in the open by its held controls:
the inserted prose tails stand missing in the same no
function word shape, the whole run condition holding at
the inserted limbs; the inserted sentence tail of the
earlier item stands missing; the eleven prose forms and
the two comma clause forms of R16-17-02 stand missing;
and the article carrying fused between prose sentences at
four fused words stand missing. Locus: derivation_core.py,
_tally_statement_head, its direct trace summary closing
limb and its fused closing limb read through
_fused_trace_summary and _before_closing_stands_as_head.
The cure these tests pin restates what a direct or fused
closing is in standing: what stands before the closing
words in the statement must stand wholly as head words,
naming words carrying no sentence function word, no main
verb form, no clause break and no prose run join before
the closing, so a prose sentence, prose clause or prose
run of the driven shapes takes no tally statement head in
any position, while every governed closing keeps standing
governed in every driven position.

Held controls stand pinned beside the defect forms, in
full: every governed direct, fused and inserted closing
standing governed beside its counted sibling, alone,
beside, and in gate rulings, the long trace summary head
and the Round trace summary head among them; every form
of R16-18-01 standing in its entering behaviour untouched
by this unit, its sixty distinct alone forms in ten
subfamilies standing missing beside their counted
siblings, the widening of Unit 2 to find them exactly as
they stand; the bounding controls of this item standing
missing, as stated above; the eleven prose forms of
R16-17-02 standing missing; the mixed inserted runs and
the prose order runs past the widened reach standing
missing; the seven enumerated family adverbs and tallyho
standing missing, the fused family forms standing
missing, and the twelve prose adverbs of R16-14-02
standing missing; the Board talli boundary control
standing missing; the folded round 10 prose sentence
record standing governed; the four folded marker shape
records standing present but not derivable; the golden
prose lines standing unflipped; and the read and absent
feeder controls byte for byte.
"""
from metrics_starter_collector.derivation_core import (
    _tally_statement_head)
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


class TestStep16Fix18Unit1(FixtureTestCase):

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
    # R16-18-02 defect forms, subfamily (a): prose sentences
    # whose closing words stand in the direct trace summary
    # form, alone, each standing missing under the no feeder
    # record code after the cure
    # ------------------------------------------------------

    def test_r16_18_02_direct_panel_reviewed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel reviewed trace summary")))

    def test_r16_18_02_direct_clerk_filed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk filed summary trace")))

    def test_r16_18_02_direct_minutes_show_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Minutes show trace summary")))

    def test_r16_18_02_direct_board_recorded_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Board recorded summary trace")))

    def test_r16_18_02_direct_board_filed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Board filed summary trace")))

    def test_r16_18_02_direct_gate_ruling_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel reviewed trace summary"), ruling=True))

    def test_r16_18_02_direct_beside_step2_nowhere(self):
        self._beside_step2_nowhere(
            _prose("Panel reviewed trace summary"))

    # ------------------------------------------------------
    # R16-18-02 defect forms, subfamily (b): prose sentences
    # whose last word stands in a fused trace summary form
    # ------------------------------------------------------

    def test_r16_18_02_fused_plain_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel reviewed tracesummary")))

    def test_r16_18_02_fused_reversed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk filed summarytrace")))

    def test_r16_18_02_fused_behind_prefix_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Minutes show boardtracesummary")))

    def test_r16_18_02_fused_between_record_order_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel reviewed traceboardgatesummary")))

    def test_r16_18_02_fused_between_reversed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk filed summaryboardgatetrace")))

    def test_r16_18_02_fused_between_four_widened_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Panel reviewed traceboardgatereviewannexsummary")))

    def test_r16_18_02_fused_widened_summary_form_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel reviewed tracesummarizings")))

    def test_r16_18_02_fused_reviewers_noted_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Reviewers noted tracesummary")))

    def test_r16_18_02_fused_panel_filed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel filed summarytrace")))

    def test_r16_18_02_fused_gatekeepers_reviewed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Gatekeepers reviewed boardtracesummary")))

    # ------------------------------------------------------
    # R16-18-02 defect forms, subfamily (c): prose standing
    # before a governed closing inside one statement, in
    # verb phrase form, joined by a hyphen, and carrying a
    # parenthetical
    # ------------------------------------------------------

    def test_r16_18_02_clause_noted_filing_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Noted filing summary trace")))

    def test_r16_18_02_clause_filing_noted_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Filing noted trace summary")))

    def test_r16_18_02_run_hyphen_joined_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Filing - trace summary")))

    def test_r16_18_02_run_parenthetical_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Filing (noted) trace summary")))

    # ------------------------------------------------------
    # R16-18-02 defect forms, subfamily (d): prose clauses
    # set off by a semicolon standing before the direct and
    # reversed direct closings
    # ------------------------------------------------------

    def test_r16_18_02_semicolon_filing_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Filing; trace summary")))

    def test_r16_18_02_semicolon_noted_filing_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Noted filing; summary trace")))

    def test_r16_18_02_code_level_prose_no_head(self):
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
            self.assertFalse(_tally_statement_head(
                run + ": LANDED figures stand here, "
                "no counts stated"), run)

    # ------------------------------------------------------
    # Held controls: the bounding forms of the item, the
    # inserted prose tails in the no function word shape,
    # the inserted sentence tail, and the article carrying
    # fused between prose sentences at four fused words
    # ------------------------------------------------------

    def test_bounding_inserted_prose_tails_missing(self):
        for run in ("Panel reviewed trace board gate summary",
                    "Clerk filed summary board gate trace",
                    "Panel reviewed trace board gate review "
                    "annex panel summary"):
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

    # ------------------------------------------------------
    # Held controls: the eleven prose forms of R16-17-02
    # standing missing in their cured forms
    # ------------------------------------------------------

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
    # Held controls: every governed direct, fused and
    # inserted closing standing governed beside its counted
    # sibling, the long head and the Round head among them,
    # and in the beside and gate ruling positions
    # ------------------------------------------------------

    def test_governed_direct_closings_governed(self):
        for head in ("Trace summary", "Summary trace",
                     "Trace summaries", "Trace summarisers",
                     "Trace summarizers", "Trace summarisings",
                     "Trace summarys",
                     "Alpha beta gamma delta epsilon trace summary",
                     "Round's trace summary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_governed_direct_beside_step2_uncounted(self):
        self._beside_step2_uncounted(_bad("Trace summary"))

    def test_governed_direct_gate_ruling_governed(self):
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
                     "Boardtracessummarisers"):
            self._candidate_governed(_bad(head), _read(head))

    def test_governed_fused_beside_step2_uncounted(self):
        self._beside_step2_uncounted(_bad("Tracesummary"))

    def test_governed_fused_gate_ruling_governed(self):
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

    def test_governed_tally_fused_forms_governed(self):
        for head in ("Boardtally", "Gate2tally", "Reviewtally",
                     "Step2tally", "Passtally", "Chairtally",
                     "Greentally", "Alphatally", "Boardtallied",
                     "Boardtallies", "Boardtallying",
                     "Gate record tally"):
            self._candidate_governed(_bad(head), _read(head))

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
    # Held controls: every form of R16-18-01 standing in its
    # entering behaviour, missing beside its counted
    # sibling, in ten subfamilies, so the widening of Unit 2
    # finds them exactly as they stand
    # ------------------------------------------------------

    def test_r16_18_01_held_subfamily_a_missing(self):
        for head in ("Filestally", "Notestally", "Logtally",
                     "Booktallies", "Cardtallying", "Boardstallies",
                     "Foliotally", "Scrolltallies", "Volumetally",
                     "Notebooktallied"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_18_01_held_subfamily_b_missing(self):
        for head in ("Boardfiletally", "Gatenotestally",
                     "Reviewbooktally", "Boardfoliotally",
                     "Gatescrolltally"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_18_01_held_subfamily_c_missing(self):
        for head in ("Gatefiletallyed", "Boardnotestalleys",
                     "Reviewbooktallyes", "Gatefoliotalleys"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_18_01_held_subfamily_d_missing(self):
        for head in ("Talliez", "Tallieing", "Boardtalliez",
                     "Boardtallieing", "Tallye", "Talleied",
                     "Tallyings", "Boardtallye", "Boardtallyings"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_18_01_held_subfamily_e_missing(self):
        for head in ("Trace summarisinges", "Trace summarieses",
                     "Trace summarisees", "Trace summariseses",
                     "Trace summarizingses", "Trace summaryings",
                     "Trace summarisationes", "Trace summariseres"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_18_01_held_subfamily_f_missing(self):
        for head in ("Boardtracesummarisinges", "Tracesummarieses",
                     "Boardtracessummarisees",
                     "Boardtracesummarisationes",
                     "Tracessummaryings"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_18_01_held_subfamily_g_missing(self):
        for head in ("Traceboardgatereviewannexpanelsummary",
                     "Summaryboardgatereviewannexpaneltrace",
                     "Tracesboardgatereviewannexpanelsummary"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_18_01_held_subfamily_h_missing(self):
        for head in ("Trace board gate review annex panel board "
                     "gate review summary",
                     "Trace board gate annex review panel board "
                     "gate annex summary",
                     "Summary board gate review annex panel board "
                     "gate trace",
                     "Summary board gate annex review panel board "
                     "gate trace"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_18_01_held_subfamily_i_missing(self):
        for head in ("Trace board gate review annex panel board "
                     "gate review for step 2",
                     "Trace board gate annex review panel board "
                     "gate annex for step 2"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_18_01_held_subfamily_j_missing(self):
        for head in ("Board ta\u026cly", "Board \u0288ally",
                     "Board tall\u01b4", "Trace \u0255ummarise",
                     "Trace s\u026fmmarise",
                     "Trace summarise\u018c",
                     "Trace summarise\u0256", "Trace s\u028bmmarise",
                     "Trace summar\u026ase", "Board t\u0251lly"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_18_01_held_beside_and_gate_ruling_missing(self):
        self._beside_step2_nowhere(_bad("Filestally"))
        report = self._q4_alone(_bad("Filestally"), ruling=True)
        self._assert_q4_missing(report)

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
