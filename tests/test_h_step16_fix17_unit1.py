"""Step 16 fix pass 17 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-17-02 (Medium, B17-B02)
of Step 16 round 17. The governing rule of the pass, in
its extended form: a piece not read in full, for whatever
reason, is not read, and its converse: a piece that is no
feeder flips nothing.

R16-17-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head carry no whole
run standing condition and no test on what stands before
the closing words, the standing condition of fix pass 16
Unit 1 standing on the inserted limbs alone, so prose
lines whose closing words take a direct or fused trace
summary form take a tally statement head and stand present
but not derivable. Three subfamilies stand driven:
(a) prose sentences whose closing words stand in the
direct trace summary form, four forms; (b) prose sentences
whose last word stands in a fused trace summary form, five
forms; and (c) prose standing before a governed closing
inside one statement, two forms. Eleven distinct alone
forms in all, with the first direct form driven in a gate
ruling and beside a counted Step 3 trace as well. The
defect stands bounded in the open by its held controls:
the inserted sentence tail She filed the trace gate
summary stands missing, the whole run condition holding
at the inserted limbs, and the fused between prose
sentences at four fused words stand missing in both
middle orders. Locus: derivation_core.py,
_tally_statement_head, its direct trace summary closing
limb and its fused closing limb read through
_fused_trace_summary. The cure these tests pin fixes what
a direct or fused closing is in standing: the words
standing before the closing words must stand as head
words, naming words carrying no sentence function word
and no clause break before the closing, so a prose
sentence or a prose clause of the driven shapes takes no
tally statement head in any position, while every governed
closing keeps standing governed in every driven position.

Held controls stand pinned beside the defect forms, in
full: every governed direct, fused and inserted closing
standing governed beside its counted sibling, alone,
beside, and in gate rulings, the long trace summary head
and the Round trace summary head among them; every form
of R16-17-01 standing in its defect form untouched by
this unit, its thirty seven breaker alone forms and its
correctness further forms standing missing beside their
counted siblings, with its held letter form standing
governed; the forty four charged forms of R16-16-01
standing governed and the fifteen prose forms of
R16-16-02 standing missing, as the round 17 breaker
exhibit holds them; the mixed inserted runs and the prose
order runs past the widened reach standing missing; the
seven enumerated family adverbs and tallyho standing
missing, the fused family forms standing missing, and the
twelve prose adverbs of R16-14-02 standing missing; the
Board talli boundary control standing missing; the folded
round 10 prose sentence record standing governed; the
four folded marker shape records standing present but not
derivable; the golden prose lines standing unflipped; and
the read and absent feeder controls byte for byte.
"""
from metrics_starter_collector.derivation_core import (
    _fold_word, _tally_statement_head)
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


class TestStep16Fix17Unit1(FixtureTestCase):

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
    # R16-17-02 defect forms, subfamily (a): prose sentences
    # whose closing words stand in the direct trace summary
    # form, alone, each standing missing under the no feeder
    # record code after the cure
    # ------------------------------------------------------

    def test_r16_17_02_direct_reviewed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("We reviewed the trace summary")))

    def test_r16_17_02_direct_filed_reversed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("She filed the summary trace")))

    def test_r16_17_02_direct_panel_noted_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The panel noted the trace summary")))

    def test_r16_17_02_direct_for_opening_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("For the trace summary")))

    def test_r16_17_02_direct_gate_ruling_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("We reviewed the trace summary"), ruling=True))

    def test_r16_17_02_direct_beside_step2_nowhere(self):
        self._beside_step2_nowhere(
            _prose("We reviewed the trace summary"))

    # ------------------------------------------------------
    # R16-17-02 defect forms, subfamily (b): prose sentences
    # whose last word stands in a fused trace summary form
    # ------------------------------------------------------

    def test_r16_17_02_fused_plain_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("We reviewed the tracesummary")))

    def test_r16_17_02_fused_reversed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("She filed the summarytrace")))

    def test_r16_17_02_fused_behind_prefix_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("We reviewed the boardtracesummary")))

    def test_r16_17_02_fused_between_record_order_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("We reviewed the traceboardgatesummary")))

    def test_r16_17_02_fused_between_reversed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("She filed the summaryboardgatetrace")))

    def test_r16_17_02_fused_gate_ruling_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("We reviewed the tracesummary"), ruling=True))

    def test_r16_17_02_fused_beside_step2_nowhere(self):
        self._beside_step2_nowhere(
            _prose("We reviewed the tracesummary"))

    # ------------------------------------------------------
    # R16-17-02 defect forms, subfamily (c): prose standing
    # before a governed closing inside one statement
    # ------------------------------------------------------

    def test_r16_17_02_clause_filing_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("The filing, trace summary")))

    def test_r16_17_02_clause_noted_filing_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Noted in the filing, the summary trace")))

    def test_r16_17_02_code_level_prose_no_head(self):
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
            self.assertFalse(_tally_statement_head(
                run + ": LANDED figures stand here, "
                "no counts stated"), run)

    # ------------------------------------------------------
    # Held controls: the bounding forms of the item, the
    # inserted sentence tail and the fused between prose
    # sentences at four fused words in both middle orders
    # ------------------------------------------------------

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
    # Held controls: every governed direct closing standing
    # governed beside its counted sibling, the long head
    # and the Round head among them, and in the beside and
    # gate ruling positions
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
    # Held controls: every form of R16-17-01 standing in
    # its defect form untouched by this unit, beside its
    # counted sibling, in the beside and gate ruling forms,
    # and its held letter form standing governed
    # ------------------------------------------------------

    def test_r16_17_01_held_breaker_forms_missing(self):
        for head in ("Archivestally", "Minutestally", "Indextally",
                     "Archivestallies", "Minutestallied",
                     "Indextallying", "Boardarchivetally",
                     "Gateindextally", "Reviewminutestally",
                     "Gatearchivetallyed", "Boardindextalleys",
                     "Reviewminutestallyes", "Tallyies", "Tallie",
                     "Boardtallie", "Talleying", "Boardtalleying",
                     "Trace summarizings", "Trace summaryes",
                     "Trace summarizationes",
                     "Boardtracesummarizings", "Tracesummaryes",
                     "Boardtracessummaryes",
                     "Traceboardgatereviewannexsummary",
                     "Summaryboardgatereviewannextrace",
                     "Tracesboardgatereviewannexsummary",
                     "Trace board gate review annex panel board "
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
                     "gate for step 2",
                     "Board ta\u029fly", "Trace \u0283ummarise",
                     "Trace s\u028ammarise", "Trace summari\u0290e",
                     "Trace summarise\ua77a"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_17_01_held_correctness_forms_missing(self):
        for head in ("Archivetally", "Catalogtallies",
                     "Manifesttally", "Registrytally",
                     "Trace summaryses", "Trace summariseds",
                     "Trace summariserses", "Tracesummaryses",
                     "Boardtracesummariseds",
                     "Trace summaris\u0247d"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_17_01_held_beside_step2_nowhere(self):
        self._beside_step2_nowhere(_bad("Archivestally"))

    def test_r16_17_01_held_gate_ruling_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _bad("Archivestally"), ruling=True))

    def test_r16_17_01_held_letter_t_hook_governed(self):
        self._candidate_governed(_bad("Board \u01acally"),
                                 _read("Board \u01acally"))

    # ------------------------------------------------------
    # Held controls: the fix pass 16 items in their restated
    # boundaries, as the round 17 breaker exhibit holds them
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
            self._candidate_governed(_bad(head), _read(head))

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
