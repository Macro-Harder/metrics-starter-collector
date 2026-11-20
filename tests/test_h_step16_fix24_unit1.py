"""Step 16 fix pass 24 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-24-02 (Medium, B24-C02
and B24-B02) of Step 16 round 24. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-24-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head read what
stands before the closing words through the standing test
of fix pass 23 Unit 1 as restated, which reads a main verb
in its base form and its irregular forms only where the
word stands in the widened closed constant
_MAIN_VERB_WORDS, beside the ed and ing ending test and
the s ending read in general, and reads a prose run join
only in the token shapes the earlier passes and fix pass
23 landed and a prose aside only in the shapes those
passes landed, and a clause break only in the comma,
semicolon and colon shapes, so prose standing before a
direct or fused closing in the shapes of this round takes
a tally statement head and stands present but not
derivable, against the restated boundary of fix pass 23
itself in its stated terms, which states the main verb
limb in terms as any inflection of a main verb and the
join and aside limbs in terms as a prose run join or a
prose aside standing before the closing words. Forty one
distinct alone forms stand driven in three subfamilies:
(a) prose sentences whose closing words stand in the
direct trace summary form, thirteen forms, each carrying
a bare noun subject and a main verb standing before the
closing words in a base form or an irregular form the
widened constant does not name, carrying no ed ending,
no ing ending and no s ending the test reads; (b) prose
sentences whose last word stands in a fused trace summary
form, fourteen forms in the same verb shapes, two of them
standing only at counts and forms the widening of fix
pass 23 Unit 2 admitted; and (c) prose standing before a
governed closing inside one statement, fourteen forms,
prose runs joined to the closing by a pound sign token, a
yen sign token, a cent sign token, a copyright sign token
or a double dagger token, a prose run carrying an aside
in curly single quotation marks, in a low single
quotation mark and a closing single quotation mark, in
double corner bracket marks or in fullwidth angle bracket
marks, and verb first prose clauses in the same verb
shapes. One form stands driven in both papers in the same
words and stands counted once in this pinning, as the
register disposition states: the prose run of subfamily
(c) carrying an aside opening on a low single quotation
mark and closing on a single quotation mark. The first
direct form of each paper, Panel walk trace summary and
Panel blew trace summary, each stand joined by a gate
ruling form and a beside form, and the curly single
quotation form stands joined by a gate ruling form, each
alone form standing present but not derivable on the
entering bytes, naming Step 2 and the feeder piece. The
defect stands bounded in the open by its held controls:
the inserted prose tails in the unread verb shapes stand
missing, the whole run standing condition holding at the
inserted limbs; the article carrying fused between prose
sentences stand missing; the asterisk token form stands
missing; the cured join and aside forms stand missing;
the read verb shapes stand missing; the s, ed and ing
forms of the fresh verbs stand missing; and the ten word
fused between prose sentence in the fresh verb shape
stands missing. Locus: derivation_core.py,
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
fix pass 23 widened to; every form of R16-24-01, written
for Unit 1 in its entering behaviour and amended in place
by fix pass 24 Unit 2 to its cured behaviour, governed
beside its counted sibling, in ten subfamilies, with its
beside form standing present over Step 3 with Step 2
named uncounted and its gate ruling form standing
governed, and the candidate forms of its correctness
paper standing governed; the bounding controls of this
item standing
missing, as stated above; every form of R16-23-02
standing missing in its cured form, and every form of
R16-23-01 standing governed in its cured form; every form
of R16-22-02, R16-21-02, R16-20-02, R16-19-02, R16-18-02
and R16-17-02 standing missing in its cured form; the
governed fused prefix forms and the variant forms behind
their governed prefixes standing governed; the mixed
inserted runs and the prose order runs past the widened
reach standing missing; the seven enumerated family
adverbs and tallyho standing missing, the fused family
forms standing missing, and the twelve prose adverbs of
R16-14-02 standing missing; the Board talli boundary
control standing missing; the folded round 10 prose
sentence record standing governed; the four folded marker
shape records standing present but not derivable; the
golden prose lines standing unflipped; and the read and
absent feeder controls byte for byte.
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


class TestStep16Fix24Unit1(FixtureTestCase):

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
    # R16-24-02 defect forms, subfamily (a): prose sentences
    # whose closing words stand in the direct trace summary
    # form, alone, each standing missing under the no feeder
    # record code after the cure. The seven forms of B24-C02
    # stand first, then the six forms of B24-B02.
    # ------------------------------------------------------

    def test_r16_24_02_direct_panel_walk_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel walk trace summary")))

    def test_r16_24_02_direct_clerk_talk_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk talk trace summary")))

    def test_r16_24_02_direct_panel_wait_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel wait trace summary")))

    def test_r16_24_02_direct_team_mend_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team mend summary trace")))

    def test_r16_24_02_direct_panel_sang_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel sang trace summary")))

    def test_r16_24_02_direct_clerk_swam_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk swam summary trace")))

    def test_r16_24_02_direct_panel_stole_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel stole trace summary")))

    def test_r16_24_02_direct_panel_blew_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel blew trace summary")))

    def test_r16_24_02_direct_clerk_flew_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk flew summary trace")))

    def test_r16_24_02_direct_team_grew_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team grew trace summary")))

    def test_r16_24_02_direct_panel_knew_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel knew summary trace")))

    def test_r16_24_02_direct_clerk_threw_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk threw trace summary")))

    def test_r16_24_02_direct_team_sang_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team sang summary trace")))

    def test_r16_24_02_direct_gate_ruling_walk_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel walk trace summary"), ruling=True))

    def test_r16_24_02_direct_gate_ruling_curly_aside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger ‘panel’ trace summary"), ruling=True))

    def test_r16_24_02_direct_gate_ruling_blew_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel blew trace summary"), ruling=True))

    def test_r16_24_02_direct_beside_walk_nowhere(self):
        self._beside_step2_nowhere(
            _prose("Panel walk trace summary"))

    def test_r16_24_02_direct_beside_blew_nowhere(self):
        self._beside_step2_nowhere(
            _prose("Panel blew trace summary"))
    # ------------------------------------------------------
    # R16-24-02 defect forms, subfamily (b): prose sentences
    # whose last word stands in a fused trace summary form,
    # alone. The eight forms of B24-C02 stand first, then
    # the six forms of B24-B02.
    # ------------------------------------------------------

    def test_r16_24_02_fused_walk_plain_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel walk tracesummary")))

    def test_r16_24_02_fused_walk_behind_prefix_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel walk boardtracesummary")))

    def test_r16_24_02_fused_walk_between_two_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel walk traceboardgatesummary")))

    def test_r16_24_02_fused_walk_between_five_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel walk traceboardgatereviewannexpanelsummary")))

    def test_r16_24_02_fused_walk_between_six_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel walk traceboardgatereviewannexpanelboardsummary")))

    def test_r16_24_02_fused_walk_between_seven_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel walk traceboardgatereviewannexpanelboardgatesummary")))

    def test_r16_24_02_fused_walk_between_eight_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel "
                    "walk traceboardgatereviewannexpanelboardgatereviewsummary")))

    def test_r16_24_02_fused_walk_between_nine_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel "
                    "walk traceboardgatereviewannexpanelboardgatereviewannexsummary")))

    def test_r16_24_02_fused_blew_plain_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel blew tracesummary")))

    def test_r16_24_02_fused_flew_reversed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk flew summarytrace")))

    def test_r16_24_02_fused_grew_behind_prefix_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team grew boardtracesummary")))

    def test_r16_24_02_fused_knew_between_two_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel knew traceboardgatesummary")))

    def test_r16_24_02_fused_threw_between_ten_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Clerk "
                    "threw traceboardgatereviewannexpanelboardgatereviewpanelsummary")))

    def test_r16_24_02_fused_sang_widened_summary_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Team sang tracesummarisedeseseseses")))
    # ------------------------------------------------------
    # R16-24-02 defect forms, subfamily (c): prose standing
    # before a governed closing inside one statement, alone.
    # The five forms of B24-C02 stand first, then the nine
    # further forms of B24-B02, the shared low single form
    # standing counted once.
    # ------------------------------------------------------

    def test_r16_24_02_run_curly_single_aside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger ‘panel’ trace summary")))

    def test_r16_24_02_run_low_single_aside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger ‚panel‘ trace summary")))

    def test_r16_24_02_clause_verb_first_walk_direct_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Walk panel trace summary")))

    def test_r16_24_02_clause_verb_first_walk_fused_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Walk panel tracesummary")))

    def test_r16_24_02_clause_verb_first_walk_reversed_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Walk ledger summarytrace")))

    def test_r16_24_02_run_pound_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger £ trace summary")))

    def test_r16_24_02_run_yen_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger ¥ trace summary")))

    def test_r16_24_02_run_cent_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger ¢ trace summary")))

    def test_r16_24_02_run_copyright_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger © trace summary")))

    def test_r16_24_02_run_double_dagger_join_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger ‡ trace summary")))

    def test_r16_24_02_run_double_corner_aside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger 『panel』 trace summary")))

    def test_r16_24_02_run_fullwidth_angle_aside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger 〈panel〉 trace summary")))

    def test_r16_24_02_clause_verb_first_blew_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Blew panel summary trace")))

    def test_r16_24_02_clause_verb_first_flew_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Flew ledger trace summary")))

    def test_r16_24_02_code_level_prose_no_head(self):
        for run in (                    "Panel walk trace summary",
                    "Clerk talk trace summary",
                    "Panel wait trace summary",
                    "Team mend summary trace",
                    "Panel sang trace summary",
                    "Clerk swam summary trace",
                    "Panel stole trace summary",
                    "Panel blew trace summary",
                    "Clerk flew summary trace",
                    "Team grew trace summary",
                    "Panel knew summary trace",
                    "Clerk threw trace summary",
                    "Team sang summary trace",
                    "Panel walk tracesummary",
                    "Panel walk boardtracesummary",
                    "Panel walk traceboardgatesummary",
                    "Panel walk traceboardgatereviewannexpanelsummary",
                    "Panel "
                    "walk traceboardgatereviewannexpanelboardsummary",
                    "Panel "
                    "walk traceboardgatereviewannexpanelboardgatesummary",
                    "Panel "
                    "walk traceboardgatereviewannexpanelboardgatereviewsummary",
                    "Panel "
                    "walk traceboardgatereviewannexpanelboardgatereviewannexsummary",
                    "Panel blew tracesummary",
                    "Clerk flew summarytrace",
                    "Team grew boardtracesummary",
                    "Panel knew traceboardgatesummary",
                    "Clerk "
                    "threw traceboardgatereviewannexpanelboardgatereviewpanelsummary",
                    "Team sang tracesummarisedeseseseses",
                    "Ledger ‘panel’ trace summary",
                    "Ledger ‚panel‘ trace summary",
                    "Walk panel trace summary",
                    "Walk panel tracesummary",
                    "Walk ledger summarytrace",
                    "Ledger £ trace summary",
                    "Ledger ¥ trace summary",
                    "Ledger ¢ trace summary",
                    "Ledger © trace summary",
                    "Ledger ‡ trace summary",
                    "Ledger 『panel』 trace summary",
                    "Ledger 〈panel〉 trace summary",
                    "Blew panel summary trace",
                    "Flew ledger trace summary",
                    ):
            self.assertFalse(_tally_statement_head(
                run + ": LANDED figures stand here, "
                "no counts stated"), run)

    # ------------------------------------------------------
    # Held controls: the bounding forms of this item, the
    # inserted prose tails in the unread verb shapes, the
    # article carrying fused between forms, the asterisk
    # token form, the cured join and aside forms in the
    # same openings, the read verb shapes, the s, ed and
    # ing forms of the fresh verbs, the ten word fused
    # between prose sentence in the fresh verb shape, the
    # verb first forms in read verb shapes, and the cured
    # verb form in the same constructions
    # ------------------------------------------------------

    def test_r16_24_02_bounding_inserted_tails_missing(self):
        for run in ("Panel blew trace board gate summary",
                    "Clerk threw summary board gate trace",
                    "Panel walk trace board gate summary",
                    "Panel fled trace board gate summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_24_02_bounding_article_and_asterisk_missing(self):
        for run in ("The panel blew "
                    "traceboardgatereviewannexpanelboardgatereviewpanelsummary",
                    "The panel walk "
                    "traceboardgatereviewannexpanelsummary",
                    "Ledger * trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_24_02_bounding_cured_join_aside_missing(self):
        for run in ("Ledger ~ trace summary",
                    "Ledger = trace summary",
                    "Ledger + trace summary",
                    "Ledger »panel« trace summary",
                    "Ledger ›panel‹ trace summary",
                    "Ledger – trace summary",
                    "Ledger — trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_24_02_bounding_read_verbs_and_inflections_missing(self):
        for run in ("Panel open trace summary",
                    "Panel close trace summary",
                    "Panel watch trace summary",
                    "Panel move trace summary",
                    "Panel call trace summary",
                    "Panel gave trace summary",
                    "Panel took trace summary",
                    "Panel chose trace summary",
                    "Panel wrote trace summary",
                    "Panel walks trace summary",
                    "Panel walked trace summary",
                    "Panel walking trace summary",
                    "Open ledger summary trace",
                    "Gave panel summary trace",
                    "Panel edit trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_24_02_bounding_ten_word_fused_between_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Panel walk "
            "traceboardgatereviewannexpanelboardgatereviewannexpanelboardsummary")))

    # ------------------------------------------------------
    # Held controls: the bounding forms of the item, the
    # inserted prose tails in the fresh verb shapes, the
    # article carrying fused between prose sentences, the
    # hyphen token, parenthetical and bracketed forms, the
    # section sign token, single quotation aside and
    # asterisk token join forms in their cured shapes, the
    # verb phrase forms, and the s, ed and ing forms of the
    # fresh verbs
    # ------------------------------------------------------

    def test_bounding_inserted_prose_tails_missing(self):
        for run in ("Panel grant trace board gate summary",
                    "Panel sought trace board gate summary",
                    "Clerk taught summary board gate trace",
                    "Panel edit trace board gate summary",
                    "Panel paid trace board gate summary",
                    "Clerk brought summary board gate trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_article_fused_between_missing(self):
        for run in ("The panel sought "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "The panel grant "
                    "traceboardgatereviewannexpanelsummary",
                    "The panel reviewed the "
                    "traceboardgatereviewannexsummary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_hyphen_parenthetical_bracketed_missing(self):
        for run in ("Ledger - trace summary",
                    "Ledger (panel) trace summary",
                    "Ledger [panel] trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_cured_join_aside_forms_missing(self):
        for run in ("Ledger § trace summary",
                    "Ledger 'panel' trace summary",
                    "Ledger * trace summary",
                    "Ledger @ trace summary",
                    "Ledger # trace summary",
                    "Ledger % trace summary",
                    "Ledger ^ trace summary",
                    "Ledger & trace summary",
                    "Ledger `panel` trace summary",
                    "Ledger «panel» trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_verb_phrase_forms_missing(self):
        for run in ("Reviews filing trace summary",
                    "Filing reviews trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_bounding_fresh_verb_inflections_missing(self):
        for run in ("Panel grants trace summary",
                    "Panel granted trace summary",
                    "Panel granting trace summary",
                    "Panel seeks trace summary",
                    "Clerk teaches summary trace",
                    "Panel sleeps trace summary",
                    "Team wepted summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the forty four forms of R16-23-02, the
    # forty two forms of R16-22-02, the thirty nine forms
    # of R16-21-02, the thirty six forms of R16-20-02,
    # the thirty forms of R16-19-02, the twenty one forms
    # of R16-18-02 and the eleven prose and comma clause
    # forms of R16-17-02 standing missing in their cured
    # forms
    # ------------------------------------------------------

    def test_control_fix23_converse_forms_missing(self):
        for run in ("Panel grant trace summary",
                    "Clerk shut summary trace",
                    "Board hide trace summary",
                    "Team cast summary trace",
                    "Panel bound trace summary",
                    "Clerk taught summary trace",
                    "Panel ran trace summary",
                    "Panel sought trace summary",
                    "Team thought trace summary",
                    "Panel bought summary trace",
                    "Clerk wept trace summary",
                    "Team slept summary trace",
                    "Panel grant tracesummary",
                    "Clerk shut summarytrace",
                    "Panel grant boardtracesummary",
                    "Team cast traceboardgatesummary",
                    "Panel grant "
                    "traceboardgatereviewannexpanelsummary",
                    "Panel grant "
                    "traceboardgatereviewannexpanelboardsummary",
                    "Panel grant "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "Panel grant "
                    "traceboardgatereviewannexpanelboardgatereviewsummary",
                    "Panel grant "
                    "traceboardgatereviewannexpanelboardgatereviewannexsummary",
                    "Grant panel tracesummary",
                    "Panel sought tracesummary",
                    "Clerk taught summarytrace",
                    "Team thought boardtracesummary",
                    "Panel bought traceboardgatesummary",
                    "Clerk wept "
                    "traceboardgatereviewannexpanelboardgatereviewpanelsummary",
                    "Team slept tracesummarisedeseseses",
                    "Ledger $ trace summary",
                    "Ledger ! trace summary",
                    "Ledger ? trace summary",
                    "Ledger • trace summary",
                    "Ledger ‹panel› trace summary",
                    "Ledger „panel“ trace summary",
                    "Ledger 「panel」 trace summary",
                    "Grant panel trace summary",
                    "Shut ledger summary trace",
                    "Hide panel summary trace",
                    "Ledger † trace summary",
                    "Ledger € trace summary",
                    "Ledger ° trace summary",
                    "Ledger “panel” trace summary",
                    "Sought panel summary trace",
                    "Taught ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_control_fix22_converse_forms_missing(self):
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
                    "Team drove summary trace",
                    "Panel edit tracesummary",
                    "Clerk print summarytrace",
                    "Panel edit boardtracesummary",
                    "Team stamp traceboardgatesummary",
                    "Panel edit "
                    "traceboardgatereviewannexpanelsummary",
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
                    "Team drove tracesummarisedeseses",
                    "Ledger § trace summary",
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
                    "Ledger «panel» trace summary",
                    "Paid panel summary trace",
                    "Brought ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_control_fix21_converse_forms_missing(self):
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
            self._assert_q4_missing(self._q4_alone(_prose(run)))

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
    # in the forms fix pass 22 widened to, and in the beside
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
    # Held controls: every form of R16-23-01, written for
    # Unit 1 in its entering behaviour and amended in place
    # by fix pass 23 Unit 2 to its cured behaviour,
    # governed beside its counted sibling, in ten
    # subfamilies, as the amendment note records, and the
    # held forms Logbooktally, Clipboardtally,
    # Worksheettally, Handbooktally, Drawertallies,
    # Boardtallyuo and Trace summarieseses standing
    # governed in their exact forms
    # ------------------------------------------------------

    def test_r16_23_01_held_subfamily_a_missing(self):
        for head in ("Chesttally", "Shelftally", "Cratetally",
                     "Trunktally", "Cabinetstallies",
                     "Vaultstallies", "Exhibitstallies",
                     "Attachmentstallies", "Supplementstallies",
                     "Portfoliotaly", "Almanactally",
                     "Compendiumtally", "Gazettetally",
                     "Docketstallies", "Catalogstallies",
                     "Manifeststallies", "Foliostallies",
                     "Scrollstallies", "Volumestallies"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_23_01_held_subfamily_b_missing(self):
        for head in ("Boardchesttally", "Gateshelftally",
                     "Reviewcratetally", "Boardtrunktally",
                     "Gatechesttallies", "Boardportfoliotaly",
                     "Gatealmanactally", "Reviewcompendiumtallies",
                     "Boarddocketstally", "Gatecatalogstally",
                     "Reviewfoliostallies", "Boardscrollstally"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_23_01_held_subfamily_c_missing(self):
        for head in ("Boardchesttallyed", "Gateshelftallyes",
                     "Boardportfoliotalye", "Gatedocketstalliez"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_23_01_held_subfamily_d_missing(self):
        for head in ("Tallyou", "Tallyuo", "Talleou",
                     "Boardtallyou", "Boardtallyue"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_23_01_held_subfamily_e_missing(self):
        for head in ("Trace summarisereseseseses",
                     "Trace summarisingeseseseses",
                     "Trace summarieseseseseses",
                     "Trace summarisedeseseseses",
                     "Trace summariseeseseseseses",
                     "Trace summaryeseseseseses",
                     "Trace summarisationeseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_23_01_held_subfamily_f_missing(self):
        for head in ("Boardtracesummarisereseseseses",
                     "Tracessummarieseseseseses",
                     "Boardtracesummarisedeseseseses",
                     "Tracessummaryeseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_23_01_held_subfamily_g_missing(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewannexpanelsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewannexpaneltrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewannexpanelsummary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_23_01_held_subfamily_h_missing(self):
        for head in ("Trace board gate review annex panel board "
                     "gate review annex panel board gate review summary",
                     "Trace board gate annex review panel board "
                     "gate annex review panel board gate review summary",
                     "Summary board gate review annex panel board "
                     "gate review annex panel board gate trace",
                     "Summary board gate annex review panel board "
                     "gate annex review panel board gate trace"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_23_01_held_subfamily_i_missing(self):
        self._candidate_governed(
            _bad("Trace board gate review annex panel board "
                 "gate review annex panel board gate review "
                 "for step 2"),
            _read("Trace board gate review annex panel board "
                  "gate review annex panel board gate review "
                  "for step 2"))

    def test_r16_23_01_held_subfamily_j_missing(self):
        for head in ("Trace ʜummarise",
                     "Board ʁally",
                     "Trace summarisɵ",
                     "Board ʪally",
                     "Trace summariseʮ",
                     "Board tʌlly",
                     "Board ʔally",
                     "Board talʎy",
                     "Trace ʁummarise",
                     "Trace sɰmmarise",
                     "Trace suɲmarise",
                     "Trace summaɻise",
                     "Trace summarisʜ"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_23_01_held_beside_and_gate_ruling_missing(self):
        self._beside_step2_uncounted(_bad("Chesttally"))
        self._beside_step2_uncounted(_bad("Portfoliotaly"))
        self._assert_q4_governed(
            self._q4_alone(_bad("Chesttally"), ruling=True),
            path=RULING_2)
        self._assert_q4_governed(
            self._q4_alone(_bad("Portfoliotaly"), ruling=True),
            path=RULING_2)

    def test_r16_23_01_held_standing_forms_governed(self):
        for head in ("Logbooktally", "Clipboardtally",
                     "Worksheettally", "Handbooktally",
                     "Drawertallies", "Boardtallyuo",
                     "Trace summarieseses"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Held controls: every form of R16-24-01, written for
    # Unit 1 in its entering behaviour and amended in
    # place by fix pass 24 Unit 2 to its cured behaviour,
    # governed beside its counted sibling, in ten
    # subfamilies, as the amendment note records, with
    # its beside form standing present over Step 3 with
    # Step 2 named uncounted and its gate ruling form
    # standing governed, and the candidate forms of the
    # correctness paper standing governed
    # ------------------------------------------------------

    def test_r16_24_01_held_subfamily_a_missing(self):
        for head in ("Atlastally",
                     "Diarytally",
                     "Beacontally",
                     "Codextally",
                     "Digesttally",
                     "Chronicletally",
                     "Cheststallies",
                     "Shelvestallies",
                     "Cratestallies",
                     "Trunkstallies",
                     "Diarytallies",
                     "Almanacstallies",
                     "Compendiumstallies",
                     "Gazettestallies"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_24_01_held_subfamily_b_missing(self):
        for head in ("Boardatlastally",
                     "Gatediarytallies",
                     "Reviewbeacontally",
                     "Gatecodextally",
                     "Reviewdigesttallies",
                     "Boardalmanacstally",
                     "Gatealmanacstally",
                     "Reviewcheststally",
                     "Boardtrunkstally"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_24_01_held_subfamily_c_missing(self):
        for head in ("Boardatlastallyed",
                     "Gatebeacontallyes",
                     "Boardatlastallye",
                     "Gatecodexstalliez"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_24_01_held_subfamily_d_missing(self):
        for head in ("Tallyeo2",
                     "Tallya",
                     "Tallyeou",
                     "Boardtallyeo2",
                     "Boardtallya",
                     "Boardtallyeou",
                     "Talleuo",
                     "Tallyoi",
                     "Boardtallyoi",
                     "Boardtalleuo"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_24_01_held_subfamily_e_missing(self):
        for head in ("Trace summarisereseseseseses",
                     "Trace summarisingeseseseseses",
                     "Trace summarieseseseseseses",
                     "Trace summarisedeseseseseses",
                     "Trace summariseeseseseseseses",
                     "Trace summaryeseseseseseses",
                     "Trace summarisationeseseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_24_01_held_subfamily_f_missing(self):
        for head in ("Boardtracesummarisereseseseseses",
                     "Tracessummarieseseseseseses",
                     "Boardtracesummarisedeseseseseses",
                     "Tracessummaryeseseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_24_01_held_subfamily_g_missing(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewannexpanelboardsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardtrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardsummary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_24_01_held_subfamily_h_missing(self):
        for head in ("Trace board gate review annex panel board gate review annex panel board gate review annex summary",
                     "Trace board gate annex review panel board gate annex review panel board gate annex review summary",
                     "Summary board gate review annex panel board gate review annex panel board gate review trace",
                     "Summary board gate annex review panel board gate annex review panel board gate annex trace",
                     "Trace board gate review annex panel board gate review annex panel board gate review board summary",
                     "Trace board gate annex review panel board gate annex review panel board gate review board summary",
                     "Summary board gate review annex panel board gate review annex panel board gate review trace",
                     "Summary board gate annex review panel board gate annex review panel board gate review trace"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_24_01_held_subfamily_i_missing(self):
        for head in ("Trace board gate review annex panel board gate review annex panel board gate review annex for step 2",
                     "Trace board gate review annex panel board gate review annex panel board gate review board for step 2"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_24_01_held_subfamily_j_missing(self):
        for head in ("Trace summarisʌ",
                     "Board ʡally",
                     "Trace summariseʔ",
                     "Trace sʂummarise",
                     "Board talʃy",
                     "Board ɓally",
                     "Board tɔlly",
                     "Board talɳy",
                     "Trace ʕummarise",
                     "Trace sɤmmarise",
                     "Trace suɶmarise",
                     "Trace summaɺise",
                     "Trace summarisʝ"):
            self._candidate_governed(_bad(head), _read(head))

    def test_r16_24_01_held_beside_and_gate_ruling(self):
        self._beside_step2_uncounted(_bad("Atlastally"))
        self._assert_q4_governed(
            self._q4_alone(_bad("Atlastally"), ruling=True),
            path=RULING_2)

    def test_r16_24_01_held_candidate_forms_governed(self):
        for head in ("Ledgertally", "Indextally", "Memotally",
                     "Slipstally", "Charttally", "Sheettallies",
                     "Foldertallies", "Annextallies",
                     "Scheduletallies", "Minutestallies",
                     "Archivestallies", "Slipstallies",
                     "Compasstally", "Censustallies",
                     "Committeetallies", "Counciltallies",
                     "Registrytallies", "Logtallies",
                     "Booktallies", "Boardledgertally",
                     "Gateindextally", "Reviewmemotally",
                     "Boardcharttallies", "Gatefoldertallies",
                     "Boardledgertallyed", "Gateindextallyes"):
            self._candidate_governed(_bad(head), _read(head))

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
