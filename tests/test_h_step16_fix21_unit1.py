"""Step 16 fix pass 21 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-21-02 (Medium, B21-C02
and B21-B02) of Step 16 round 21. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-21-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head read what
stands before the closing words through the standing test
of fix pass 20 Unit 1 as restated, which reads a main verb
in its base form and its irregular forms only where the
word stands in the widened closed constant
_MAIN_VERB_WORDS, beside the ed and ing ending test and
the s ending read in general, and reads a prose run join
only in the hyphen token, double hyphen token, slash
token, backslash and pipe shapes and a prose aside only
in the parenthetical, bracketed, brace and angle shapes,
and a clause break only in the comma, semicolon and colon
shapes, so prose standing before a direct or fused
closing in the shapes of this round takes a tally
statement head and stands present but not derivable,
against the restated boundary itself, which states the
main verb limb in terms as a main verb form in any
inflection of a main verb, its base form among them, and
the run join limb in terms as a prose run join standing
before the closing words. Thirty nine distinct alone
forms stand driven in three subfamilies: (a) prose
sentences whose closing words stand in the direct trace
summary form, eleven forms, each carrying a bare noun
subject and a main verb standing before the closing words
in a base form or an irregular form the widened constant
does not name, carrying no ed ending, no ing ending and
no s ending the test reads; (b) prose sentences whose
last word stands in a fused trace summary form, fourteen
forms in the same verb shapes, two of them standing only
at counts and forms the widening of fix pass 20 Unit 2
admitted; and (c) prose standing before a governed
closing inside one statement, fourteen forms, prose runs
joined to the closing by an underscore token, a tilde
token, an equals token, a plus token or a double slash
token, or joined by a long dash token in the stated form,
a prose run carrying an aside in double quotation marks,
in asterisks or in underscore marks, and verb first prose
clauses in the same verb shapes. Three forms stand driven
in both papers in the same words and stand counted once
in this pinning, as the register disposition states: the
two prose sentences of subfamily (a) carrying the verbs
chose and spoke, and the one prose run form of subfamily
(c) joined by a tilde. The first direct form of the
correctness paper and the first direct form of the
breaker paper each stand joined by a gate ruling form and
a beside form, each alone form standing present but not
derivable on the entering bytes, naming Step 2 and the
feeder piece. The defect stands bounded in the open by
its held controls: the inserted prose tails in the fresh
verb shapes stand missing, the whole run standing
condition holding at the inserted limbs; the article
carrying fused between prose sentences stand missing; the
hyphen token, parenthetical and bracketed forms stand
missing; the double backslash and double pipe join forms
stand missing; the verb phrase forms stand missing; and
the seven word fused between prose sentences in the read
verb shapes stand missing. Locus: derivation_core.py,
_tally_statement_head, its direct trace summary closing
limb and its fused closing limb read through
_fused_trace_summary and _before_closing_stands_as_head
with the constants _SENTENCE_FUNCTION_WORDS,
_MAIN_VERB_WORDS and _NAMING_WORDS_WITH_VERB_ENDINGS and
the helper _word_stands_as_main_verb. The cure these
tests pin restates what a direct or fused closing is in
standing: what stands before the closing words in the
statement must stand wholly as head words, naming words
carrying no sentence function word, no main verb form in
any inflection, its base form, its s form, its ed form,
its ing form or an irregular form of it, no clause break
and no prose run join or aside in any of its shapes
before the closing, so a prose sentence, prose clause or
prose run of the driven shapes takes no tally statement
head in any position, while every governed closing keeps
standing governed in every driven position.

Held controls stand pinned beside the defect forms, in
full: every governed direct, fused and inserted closing
standing governed beside its counted sibling, alone,
beside, and in gate rulings, the long trace summary head
and the Round trace summary head among them, in the forms
fix pass 20 widened to; every form of R16-21-01 standing
in its entering behaviour untouched by this unit, its
sixty five distinct alone forms in ten subfamilies
standing missing beside their counted siblings, with its
beside and gate ruling forms in the same entering form,
so the widening of Unit 2 finds them exactly as they
stand, and the held forms Logbooktally and Trace
summarieseses of that item standing governed in their
exact forms; the bounding controls of this item standing
missing, as stated above; every form of R16-20-02,
R16-19-02, R16-18-02 and R16-17-02 standing missing in
its cured form; the governed fused prefix forms and the
variant forms behind their governed prefixes standing
governed; the mixed inserted runs and the prose order
runs past the widened reach standing missing; the seven
enumerated family adverbs and tallyho standing missing,
the fused family forms standing missing, and the twelve
prose adverbs of R16-14-02 standing missing; the Board
talli boundary control standing missing; the folded round
10 prose sentence record standing governed; the four
folded marker shape records standing present but not
derivable; the golden prose lines standing unflipped; and
the read and absent feeder controls byte for byte.
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


class TestStep16Fix21Unit1(FixtureTestCase):

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
    # R16-21-02 defect forms, subfamily (a): prose sentences
    # whose closing words stand in the direct trace summary
    # form, alone, each standing missing under the no feeder
    # record code after the cure. The seven forms of B21-C02
    # stand first, then the four further forms of B21-B02.
    # ------------------------------------------------------

    def test_r16_21_02_direct_panel_draft_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel draft trace summary")))

    def test_r16_21_02_direct_clerk_lodge_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk lodge summary trace")))

    def test_r16_21_02_direct_board_publish_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Board publish trace summary")))

    def test_r16_21_02_direct_team_gather_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team gather summary trace")))

    def test_r16_21_02_direct_panel_chose_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel chose trace summary")))

    def test_r16_21_02_direct_clerk_spoke_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk spoke summary trace")))

    def test_r16_21_02_direct_panel_broke_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel broke trace summary")))

    def test_r16_21_02_direct_clerk_kept_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk kept summary trace")))

    def test_r16_21_02_direct_team_drew_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team drew trace summary")))

    def test_r16_21_02_direct_panel_froze_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel froze summary trace")))

    def test_r16_21_02_direct_team_found_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team found summary trace")))

    def test_r16_21_02_direct_gate_ruling_draft_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel draft trace summary"), ruling=True))

    def test_r16_21_02_direct_gate_ruling_chose_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel chose trace summary"), ruling=True))

    def test_r16_21_02_direct_beside_draft_nowhere(self):
        self._beside_step2_nowhere(
            _prose("Panel draft trace summary"))

    def test_r16_21_02_direct_beside_chose_nowhere(self):
        self._beside_step2_nowhere(
            _prose("Panel chose trace summary"))

    # ------------------------------------------------------
    # R16-21-02 defect forms, subfamily (b): prose sentences
    # whose last word stands in a fused trace summary form.
    # The eight forms of B21-C02 stand first, then the six
    # forms of B21-B02.
    # ------------------------------------------------------

    def test_r16_21_02_fused_draft_plain_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel draft tracesummary")))

    def test_r16_21_02_fused_lodge_reversed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk lodge summarytrace")))

    def test_r16_21_02_fused_draft_behind_prefix_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel draft boardtracesummary")))

    def test_r16_21_02_fused_publish_between_two_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team publish traceboardgatesummary")))

    def test_r16_21_02_fused_draft_between_five_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Panel draft traceboardgatereviewannexpanelsummary")))

    def test_r16_21_02_fused_draft_between_six_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Panel draft "
            "traceboardgatereviewannexpanelboardsummary")))

    def test_r16_21_02_fused_draft_between_seven_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Panel draft "
            "traceboardgatereviewannexpanelboardgatesummary")))

    def test_r16_21_02_fused_draft_verb_first_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Draft panel tracesummary")))

    def test_r16_21_02_fused_chose_plain_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel chose tracesummary")))

    def test_r16_21_02_fused_kept_reversed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk kept summarytrace")))

    def test_r16_21_02_fused_drew_behind_prefix_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team drew boardtracesummary")))

    def test_r16_21_02_fused_froze_between_two_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel froze traceboardgatesummary")))

    def test_r16_21_02_fused_spoke_between_seven_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Clerk spoke "
            "traceboardgatereviewannexpanelboardgatesummary")))

    def test_r16_21_02_fused_found_widened_summary_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team found tracesummarisedeses")))

    # ------------------------------------------------------
    # R16-21-02 defect forms, subfamily (c): prose standing
    # before a governed closing inside one statement, in
    # underscore, tilde, equals and plus join forms, in
    # double slash and long dash join forms, in quoted,
    # asterisk and underscore aside forms, and in verb
    # first clause forms. The seven forms of B21-C02 stand
    # first, then the seven further forms of B21-B02, the
    # tilde join form standing driven in both papers in
    # the same words and counted once here.
    # ------------------------------------------------------

    def test_r16_21_02_run_underscore_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger _ trace summary")))

    def test_r16_21_02_run_tilde_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger ~ trace summary")))

    def test_r16_21_02_run_equals_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger = trace summary")))

    def test_r16_21_02_run_plus_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger + trace summary")))

    def test_r16_21_02_clause_verb_first_draft_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Draft panel trace summary")))

    def test_r16_21_02_clause_verb_first_lodge_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Lodge ledger summary trace")))

    def test_r16_21_02_clause_verb_first_publish_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Publish panel summary trace")))

    def test_r16_21_02_run_double_slash_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger // trace summary")))

    def test_r16_21_02_run_long_dash_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger — trace summary")))

    def test_r16_21_02_run_quoted_aside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger "panel" trace summary')))

    def test_r16_21_02_run_asterisk_aside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger *panel* trace summary")))

    def test_r16_21_02_run_underscore_aside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger _panel_ trace summary")))

    def test_r16_21_02_clause_verb_first_chose_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Chose panel summary trace")))

    def test_r16_21_02_clause_verb_first_kept_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Kept ledger trace summary")))

    def test_r16_21_02_code_level_prose_no_head(self):
        for run in ("Panel draft trace summary",
                    "Clerk lodge summary trace",
                    "Board publish trace summary",
                    "Team gather summary trace",
                    "Panel chose trace summary",
                    "Clerk spoke summary trace",
                    "Clerk spoke trace summary",
                    "Panel broke trace summary",
                    "Clerk kept summary trace",
                    "Team drew trace summary",
                    "Panel froze summary trace",
                    "Team found summary trace",
                    "Panel draft tracesummary",
                    "Clerk lodge summarytrace",
                    "Panel draft boardtracesummary",
                    "Team publish traceboardgatesummary",
                    "Panel draft "
                    "traceboardgatereviewannexpanelsummary",
                    "Panel draft "
                    "traceboardgatereviewannexpanelboardsummary",
                    "Panel draft "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "Draft panel tracesummary",
                    "Panel chose tracesummary",
                    "Clerk kept summarytrace",
                    "Team drew boardtracesummary",
                    "Panel froze traceboardgatesummary",
                    "Clerk spoke "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "Team found tracesummarisedeses",
                    "Ledger _ trace summary",
                    "Ledger ~ trace summary",
                    "Ledger = trace summary",
                    "Ledger + trace summary",
                    "Draft panel trace summary",
                    "Lodge ledger summary trace",
                    "Publish panel summary trace",
                    "Ledger // trace summary",
                    "Ledger — trace summary",
                    'Ledger "panel" trace summary',
                    "Ledger *panel* trace summary",
                    "Ledger _panel_ trace summary",
                    "Chose panel summary trace",
                    "Kept ledger trace summary"):
            self.assertFalse(_tally_statement_head(
                run + ": LANDED figures stand here, "
                "no counts stated"), run)

    # ------------------------------------------------------
    # Held controls: the bounding forms of the item, the
    # inserted prose tails in the fresh verb shapes, the
    # article carrying fused between prose sentences, the
    # hyphen token, parenthetical and bracketed forms, the
    # double backslash and double pipe join forms, the verb
    # phrase forms, and the seven word fused between prose
    # sentences in the read verb shapes beside the s and ed
    # forms of the fresh verbs
    # ------------------------------------------------------

    def test_bounding_inserted_prose_tails_missing(self):
        for run in ("Panel draft trace board gate summary",
                    "Panel draft trace board gate review "
                    "annex panel board gate summary",
                    "Panel chose trace board gate summary",
                    "Clerk kept summary board gate trace",
                    "Panel reviewed trace board gate summary",
                    "Panel logs trace board gate summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_article_fused_between_missing(self):
        for run in ("The panel drafted the "
                    "traceboardgatereviewannexpanelsummary",
                    "The panel chose "
                    "traceboardgatereviewannexpanelsummary",
                    "The panel reviewed the "
                    "traceboardgatereviewannexsummary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_hyphen_parenthetical_bracketed_missing(self):
        for run in ("Ledger - trace summary",
                    "Ledger (panel) trace summary",
                    "Ledger [panel] trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_double_backslash_double_pipe_missing(self):
        for run in ("Ledger \\\\ trace summary",
                    "Ledger || trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_verb_phrase_forms_missing(self):
        for run in ("Reviews filing trace summary",
                    "Filing reviews trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_read_verb_forms_missing(self):
        for run in ("Panel drafts "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "Panel drafts trace summary",
                    "Clerk lodges summary trace",
                    "Panel drafted trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the thirty six forms of R16-20-02, the
    # thirty forms of R16-19-02, the twenty one forms of
    # R16-18-02 and the eleven prose and comma clause forms
    # of R16-17-02 standing missing in their cured forms
    # ------------------------------------------------------

    def test_control_fix20_converse_forms_missing(self):
        for run in ("Panel submit trace summary",
                    "Clerk attest summary trace",
                    "Board endorse trace summary",
                    "Team compile summary trace",
                    "Panel undertook trace summary",
                    "Clerk foresaw summary trace",
                    "Panel overcame trace summary",
                    "Panel vote trace summary",
                    "Clerk type summary trace",
                    "Team sort trace summary",
                    "Panel merge summary trace",
                    "Clerk fetch trace summary",
                    "Team parse summary trace",
                    "Panel submit tracesummary",
                    "Clerk attest summarytrace",
                    "Panel submit boardtracesummary",
                    "Team endorse traceboardgatesummary",
                    "Panel submit "
                    "traceboardgatereviewannexpanelsummary",
                    "Panel submit "
                    "traceboardgatereviewannexpanelboardsummary",
                    "Endorse team tracesummary",
                    "Panel vote tracesummary",
                    "Clerk type summarytrace",
                    "Team sort boardtracesummary",
                    "Panel merge traceboardgatesummary",
                    "Clerk fetch "
                    "traceboardgatereviewannexpanelboardsummary",
                    "Panel vote tracesummariseeses",
                    "Ledger \\ trace summary",
                    "Ledger | trace summary",
                    "Ledger: trace summary",
                    "Ledger {panel} trace summary",
                    "Ledger <panel> trace summary",
                    "Submit panel trace summary",
                    "Attest ledger summary trace",
                    "Submit panel summary trace",
                    "Vote panel summary trace",
                    "Type ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_control_fix19_converse_forms_missing(self):
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

    # ------------------------------------------------------
    # Held controls: every governed direct, fused and
    # inserted closing standing governed beside its counted
    # sibling, the long head and the Round head among them,
    # in the forms fix pass 20 widened to, and in the beside
    # and gate ruling positions
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
                     "Boardtracessummarisers",
                     "Traceboardgatereviewannexpanelsummary",
                     "Summaryboardgatereviewannexpaneltrace",
                     "Tracesboardgatereviewannexpanelsummary"):
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

    def test_governed_variant_forms_governed(self):
        for head in ("Boardtallys", "Boardtallyed", "Boardtallyes",
                     "Tallys", "Tallyed", "Tallyes", "Talley",
                     "Talleys", "Talleyed", "Tallyies", "Tallie",
                     "Talleying"):
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
    # Held controls: every form of R16-21-01 standing in
    # its entering behaviour untouched by this unit, its
    # sixty five distinct alone forms in ten subfamilies
    # standing missing beside their counted siblings, with
    # its beside and gate ruling forms in the same entering
    # form, and the held forms Logbooktally and Trace
    # summarieseses standing governed in their exact forms
    # ------------------------------------------------------

    def test_r16_21_01_held_subfamily_a_missing(self):
        for head in ("Reporttally", "Agendatally", "Reporttallies",
                     "Dossierstally", "Voucherstally", "Ticketstally",
                     "Brieftally", "Protocoltally", "Pagestally",
                     "Packetstallies", "Folderstallies",
                     "Dossierstallies", "Voucherstallies",
                     "Ticketstallies", "Annexestally", "Schedulestally"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_21_01_held_subfamily_b_missing(self):
        for head in ("Boardreporttally", "Gateagendatally",
                     "Reviewbrieftally", "Boardpagestally",
                     "Gatepacketstally", "Reviewfolderstallies",
                     "Boardannexestally"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_21_01_held_subfamily_c_missing(self):
        for head in ("Boardreporttallyed", "Gateagendatallyes",
                     "Boardpagestallye", "Gatepacketstalliez"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_21_01_held_subfamily_d_missing(self):
        for head in ("Tallyio", "Tallyua", "Boardtallyio",
                     "Boardtallyua", "Tallyiu", "Talleio",
                     "Boardtallyiu"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_21_01_held_subfamily_e_missing(self):
        for head in ("Trace summarisereseses",
                     "Trace summarisingeseses",
                     "Trace summarieseseses",
                     "Trace summarisedeseses",
                     "Trace summariseeseseses",
                     "Trace summaryeseseses",
                     "Trace summarisationeseseses"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_21_01_held_subfamily_f_missing(self):
        for head in ("Boardtracesummarisereseses",
                     "Tracessummarieseseses",
                     "Boardtracesummarisedeseses",
                     "Tracessummaryeseseses"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_21_01_held_subfamily_g_missing(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewtrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewsummary"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_21_01_held_subfamily_h_missing(self):
        for head in ("Trace board gate review annex panel board "
                     "gate review annex panel board summary",
                     "Trace board gate annex review panel board "
                     "gate annex review panel board summary",
                     "Summary board gate review annex panel board "
                     "gate review annex panel trace",
                     "Summary board gate annex review panel board "
                     "gate annex review panel trace"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_21_01_held_subfamily_i_missing(self):
        self._candidate_missing(
            _bad("Trace board gate review annex panel board "
                 "gate review annex panel board for step 2"),
            _read("Trace board gate review annex panel board "
                  "gate review annex panel board for step 2"))

    def test_r16_21_01_held_subfamily_j_missing(self):
        for head in ("Trace ʑummarise",
                     "Board tallʏ",
                     "Board ʇally",
                     "Trace summarɩse",
                     "Trace ʓummarise",
                     "Board ʦally",
                     "Board ʧally",
                     "Board tɒlly",
                     "Board taɮly",
                     "Trace ʅummarise",
                     "Trace summarisɛ",
                     "Trace summarisʤ"):
            self._candidate_missing(_bad(head), _read(head))

    def test_r16_21_01_held_beside_and_gate_ruling_missing(self):
        self._beside_step2_nowhere(_bad("Reporttally"))
        self._beside_step2_nowhere(_bad("Pagestally"))
        self._assert_q4_missing(
            self._q4_alone(_bad("Reporttally"), ruling=True))
        self._assert_q4_missing(
            self._q4_alone(_bad("Pagestally"), ruling=True))

    def test_r16_21_01_held_standing_forms_governed(self):
        self._candidate_governed(_bad("Logbooktally"),
                                 _read("Logbooktally"))
        self._candidate_governed(_bad("Trace summarieseses"),
                                 _read("Trace summarieseses"))

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
        self._candidate_missing(_bad("Board tallí"),
                                _read("Board tallí"))

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
