"""Step 16 fix pass 23 unit 2 tests: the Q-4 widening unit.

Pinning tests for register item R16-23-01 (Medium, B23-C01
and B23-B01) of Step 16 round 23. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-23-01: malformed tally statement heads the restated
boundary of fix pass 22 still does not reach, in seventy
two distinct alone forms in ten subfamilies, on the
counted pattern head agnosticism ground alone in every
subfamily: (a) genuine heads fused from record words the
governed fused prefix enumeration of ninety one does not
name, Chesttally, Shelftally, Cratetally and Trunktally
among the plain forms, Portfoliotaly standing fused from
the portfolio word and the taly spelling, Almanactally,
Compendiumtally and Gazettetally among the plain forms,
and tally forms fused behind the plurals cabinets,
vaults, exhibits, attachments, supplements, dockets,
catalogs, manifests, folios, scrolls and volumes,
nineteen forms; (b) composite openings, a governed
prefix in the opening position with an unnamed record
word immediately before the tally form, Boardchesttally,
Gateshelftally and Reviewcratetally among them, twelve
forms; (c) variant spellings in that composite opening
position, Boardchesttallyed, Gateshelftallyes,
Boardportfoliotalye and Gatedocketstalliez, four forms;
(d) variant spellings past the widened variant sets of
twenty nine and thirty one, Tallyou, Tallyuo and
Talleou, and Boardtallyou and Boardtallyue, five forms;
(e) the summary word in further forms past the sixty
three, Trace summarisereseseseses, Trace
summarisingeseseseses, Trace summarieseseseseses and
Trace summarisedeseseseses, and Trace
summariseeseseseseses, Trace summaryeseseseseses and
Trace summarisationeseseseseses, seven forms; (f) fused
trace summary closings built on those forms,
Boardtracesummarisereseseseses,
Tracessummarieseseseseses,
Boardtracesummarisedeseseseses and
Tracessummaryeseseseseses, four forms; (g) fused
closings with ten governed words fused between the
closing words, three forms; (h) inserted word closings
at thirteen words forward and twelve words reversed,
four forms; (i) the for step closing at thirteen
inserted words, one form; and (j) the tally and summary
words carrying further stroke and hook letters the
folding does not replace, thirteen forms, the letter
ʁ standing in both papers in different words and
the letter ʜ standing twice in the summary word
in different positions, as the register states in the
open. Eighteen forms stand driven in both papers in the
same words and stand counted once in this pinning, as
the register disposition states. Each alone form stands
missing beside its counted sibling on the entering
bytes. The beside forms stand driven in the Portfoliotaly
head and in the Trace summarisedeseseseses head by the
breaker paper, and the gate ruling form in the
Portfoliotaly head: the register disposition states the
beside forms in the entering form, present over Step 3
with Step 2 standing nowhere on the row, while the
breaker exhibit beside assertions state the cured form,
Step 2 named uncounted in the beside row; this unit
settles the difference in its own terms in the open in
its report, pinning the beside forms in the cured form
in this module, as the form model of fix pass 22 Unit 2
pinned its beside forms, the entering form standing
verified by Unit 1 of this pass in its held tests.
Locus: derivation_core.py, _fold_word, _tally_word and
the constants _TALLY_WORD_FORMS, _TOTALLY_FAMILY,
_GOVERNED_FUSED_PREFIXES, _TALLY_WORD_VARIANT_FORMS
and _TALLY_WORD_VARIANT_FUSED_FORMS, _summary_word
and the constant _SUMMARY_WORD_FORMS,
_fused_trace_summary with _fused_between_closing, and
_tally_statement_head, its closing tests standing
after its docstring, against the standing test as fix
pass 23 Unit 1 restated it. The cure these tests pin
widens those tests in general terms, so each driven
form stands counted, in the alone position taking the
governed not derivable form naming the step and the
feeder piece, and in the beside position naming the
step uncounted, in gate records and gate rulings
alike, while every held control stands exactly as
before, and while no form of R16-23-02 reopens in any
position under the standing test as Unit 1 of this
pass restated it.

Held controls stand pinned beside the defect forms, in
full: every form of R16-23-02 standing missing in its
prose form, alone, beside and in gate rulings, as Unit
1 of this pass left it, its forty four distinct alone
forms and its bounding held controls among them, and
every form of R16-22-02, R16-21-02, R16-19-02,
R16-18-02 and R16-17-02 standing missing in the same
way; the cured underreach forms of fix passes 22, 21,
20 and 19 standing governed; the held standing forms
Logbooktally, Clipboardtally, Worksheettally,
Handbooktally, Drawertallies, Boardtallyuo and Trace
summarieseses standing governed in their exact forms;
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


class TestStep16Fix23Unit2(FixtureTestCase):

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
    # R16-23-01 defect forms, subfamily (a): genuine
    # tally statement heads fused from record words the
    # governed fused prefix enumeration of ninety one
    # does not name, and tally forms fused behind the
    # plurals of governed prefixes and of record words
    # ------------------------------------------------------

    def test_r16_23_01_subfamily_a_governed(self):
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

    # ------------------------------------------------------
    # R16-23-01 defect forms, subfamily (b): a governed
    # prefix standing in the opening position with a
    # record word the widened enumeration does not name
    # standing immediately before the tally form
    # ------------------------------------------------------

    def test_r16_23_01_subfamily_b_governed(self):
        for head in ("Boardchesttally", "Gateshelftally",
                     "Reviewcratetally", "Boardtrunktally",
                     "Gatechesttallies", "Boardportfoliotaly",
                     "Gatealmanactally", "Reviewcompendiumtallies",
                     "Boarddocketstally", "Gatecatalogstally",
                     "Reviewfoliostallies", "Boardscrollstally"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-23-01 defect forms, subfamily (c): the variant
    # spellings standing in that composite opening
    # position
    # ------------------------------------------------------

    def test_r16_23_01_subfamily_c_governed(self):
        for head in ("Boardchesttallyed", "Gateshelftallyes",
                     "Boardportfoliotalye", "Gatedocketstalliez"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-23-01 defect forms, subfamily (d): variant
    # spellings past the widened variant sets of twenty
    # nine and thirty one
    # ------------------------------------------------------

    def test_r16_23_01_subfamily_d_governed(self):
        for head in ("Tallyou", "Tallyuo", "Talleou",
                     "Boardtallyou", "Boardtallyue"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-23-01 defect forms, subfamily (e): the summary
    # word in further forms past the sixty three
    # ------------------------------------------------------

    def test_r16_23_01_subfamily_e_governed(self):
        for head in ("Trace summarisereseseseses",
                     "Trace summarisingeseseseses",
                     "Trace summarieseseseseses",
                     "Trace summarisedeseseseses",
                     "Trace summariseeseseseseses",
                     "Trace summaryeseseseseses",
                     "Trace summarisationeseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-23-01 defect forms, subfamily (f): fused trace
    # summary closings built on those further forms
    # ------------------------------------------------------

    def test_r16_23_01_subfamily_f_governed(self):
        for head in ("Boardtracesummarisereseseseses",
                     "Tracessummarieseseseseses",
                     "Boardtracesummarisedeseseseses",
                     "Tracessummaryeseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-23-01 defect forms, subfamily (g): fused
    # closings with ten governed words fused between
    # the closing words
    # ------------------------------------------------------

    def test_r16_23_01_subfamily_g_governed(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewannexpanelsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewannexpaneltrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewannexpanelsummary"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-23-01 defect forms, subfamily (h): inserted
    # word closings at thirteen words forward and
    # twelve words reversed
    # ------------------------------------------------------

    def test_r16_23_01_subfamily_h_governed(self):
        for head in ("Trace board gate review annex panel board "
                     "gate review annex panel board gate review summary",
                     "Trace board gate annex review panel board "
                     "gate annex review panel board gate review summary",
                     "Summary board gate review annex panel board "
                     "gate review annex panel board gate trace",
                     "Summary board gate annex review panel board "
                     "gate annex review panel board gate trace"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-23-01 defect forms, subfamily (i): the for step
    # closing at thirteen inserted words
    # ------------------------------------------------------

    def test_r16_23_01_subfamily_i_governed(self):
        self._candidate_governed(
            _bad("Trace board gate review annex panel board "
                 "gate review annex panel board gate review "
                 "for step 2"),
            _read("Trace board gate review annex panel board "
                  "gate review annex panel board gate review "
                  "for step 2"))

    # ------------------------------------------------------
    # R16-23-01 defect forms, subfamily (j): the tally
    # and summary words carrying further stroke and hook
    # letters the folding does not replace. The letter
    # ʁ stands in both papers in different words,
    # and the letter ʜ stands twice in the summary
    # word in different positions, as the register
    # states in the open.
    # ------------------------------------------------------

    def test_r16_23_01_subfamily_j_governed(self):
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

    # ------------------------------------------------------
    # R16-23-01 beside and gate ruling forms: the beside
    # forms standing present over Step 3 with Step 2
    # named uncounted after the cure, in the exhibit
    # form this unit settles in the open, and the gate
    # ruling forms standing governed in the ruling form
    # ------------------------------------------------------

    def test_r16_23_01_beside_forms_uncounted(self):
        for head in ("Portfoliotaly", "Chesttally",
                     "Trace summarisedeseseseses"):
            self._beside_step2_uncounted(_bad(head))

    def test_r16_23_01_gate_ruling_forms_governed(self):
        for head in ("Portfoliotaly", "Chesttally",
                     "Trace summarisedeseseseses"):
            report = self._q4_alone(_bad(head), ruling=True)
            self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # R16-23-01 code level forms: the driven words under
    # the word tests, the driven heads under the head
    # test, and the thirteen defect letters under the fold
    # ------------------------------------------------------

    def test_r16_23_01_code_level_forms(self):
        for word in ("chesttally",
                     "shelftally",
                     "cratetally",
                     "trunktally",
                     "cabinetstallies",
                     "vaultstallies",
                     "exhibitstallies",
                     "attachmentstallies",
                     "supplementstallies",
                     "portfoliotaly",
                     "almanactally",
                     "compendiumtally",
                     "gazettetally",
                     "docketstallies",
                     "catalogstallies",
                     "manifeststallies",
                     "foliostallies",
                     "scrollstallies",
                     "volumestallies",
                     "boardchesttally",
                     "gateshelftally",
                     "reviewcratetally",
                     "boardtrunktally",
                     "gatechesttallies",
                     "boardportfoliotaly",
                     "gatealmanactally",
                     "reviewcompendiumtallies",
                     "boarddocketstally",
                     "gatecatalogstally",
                     "reviewfoliostallies",
                     "boardscrollstally",
                     "boardchesttallyed",
                     "gateshelftallyes",
                     "boardportfoliotalye",
                     "gatedocketstalliez",
                     "tallyou",
                     "tallyuo",
                     "talleou",
                     "boardtallyou",
                     "boardtallyue"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ("summarisereseseseses",
                     "summarisingeseseseses",
                     "summarieseseseseses",
                     "summarisedeseseseses",
                     "summariseeseseseseses",
                     "summaryeseseseseses",
                     "summarisationeseseseseses"):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ("boardtracesummarisereseseseses",
                     "tracessummarieseseseseses",
                     "boardtracesummarisedeseseseses",
                     "tracessummaryeseseseseses",
                     "traceboardgatereviewannexpanelboardgatereviewannexpanelsummary",
                     "summaryboardgatereviewannexpanelboardgatereviewannexpaneltrace",
                     "tracesboardgatereviewannexpanelboardgatereviewannexpanelsummary"):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        for head in ("Chesttally",
                     "Portfoliotaly",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate review summary",
                     "Summary board gate annex review panel board "
                     "gate annex review panel board gate trace",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate review "
                     "for step 2",
                     "Trace summarisedeseseseses"):
            line = head + ": items checked stand here"
            self.assertTrue(_tally_statement_head(line), head)
        self.assertEqual(_fold_word("ʜummarise"), "summarise")
        self.assertEqual(_fold_word("ʁally"), "tally")
        self.assertEqual(_fold_word("summarisɵ"), "summarise")
        self.assertEqual(_fold_word("ʪally"), "tally")
        self.assertEqual(_fold_word("summariseʮ"), "summarised")
        self.assertEqual(_fold_word("tʌlly"), "tally")
        self.assertEqual(_fold_word("ʔally"), "tally")
        self.assertEqual(_fold_word("talʎy"), "tally")
        self.assertEqual(_fold_word("ʁummarise"), "summarise")
        self.assertEqual(_fold_word("sɰmmarise"), "summarise")
        self.assertEqual(_fold_word("suɲmarise"), "summarise")
        self.assertEqual(_fold_word("summaɻise"), "summarise")
        self.assertEqual(_fold_word("summarisʜ"), "summarise")

    # ------------------------------------------------------
    # Held controls: every form of R16-23-02 standing
    # missing in its prose form, as Unit 1 of this pass
    # left it, its direct forms
    # ------------------------------------------------------

    def test_r16_23_02_held_direct_forms_missing(self):
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
                    "Team slept summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the fused forms of R16-23-02
    # standing missing in the same way
    # ------------------------------------------------------

    def test_r16_23_02_held_fused_forms_missing(self):
        for run in ("Panel grant tracesummary",
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
                    "Team slept tracesummarisedeseseses"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the run join, aside and verb first
    # clause forms of R16-23-02 standing missing in the
    # same way
    # ------------------------------------------------------

    def test_r16_23_02_held_run_and_clause_forms_missing(self):
        for run in ("Ledger $ trace summary",
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

    def test_r16_23_02_held_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel grant trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel sought trace summary"), ruling=True))
        self._beside_step2_nowhere(_prose("Panel grant trace summary"))
        self._beside_step2_nowhere(_prose("Panel sought trace summary"))

    def test_r16_23_02_held_code_level_prose_no_head(self):
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
            self.assertFalse(_tally_statement_head(
                run + ": LANDED figures stand here, "
                "no counts stated"), run)

    # ------------------------------------------------------
    # Held controls: the bounding forms of R16-23-02, the
    # inserted prose tails in the fresh verb shapes, the
    # article carrying fused between prose sentences, the
    # hyphen token, parenthetical and bracketed forms, the
    # cured join and aside forms, the verb phrase forms,
    # and the s, ed and ing forms of the fresh verbs
    # ------------------------------------------------------

    def test_r16_23_02_bounding_inserted_prose_tails_missing(self):
        for run in ("Panel grant trace board gate summary",
                    "Panel sought trace board gate summary",
                    "Clerk taught summary board gate trace",
                    "Panel edit trace board gate summary",
                    "Panel paid trace board gate summary",
                    "Clerk brought summary board gate trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_23_02_bounding_article_fused_between_missing(self):
        for run in ("The panel sought "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "The panel grant "
                    "traceboardgatereviewannexpanelsummary",
                    "The panel reviewed the "
                    "traceboardgatereviewannexsummary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_23_02_bounding_hyphen_parenthetical_bracketed_missing(self):
        for run in ("Ledger - trace summary",
                    "Ledger (panel) trace summary",
                    "Ledger [panel] trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_23_02_bounding_cured_join_aside_forms_missing(self):
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

    def test_r16_23_02_bounding_verb_phrase_forms_missing(self):
        for run in ("Reviews filing trace summary",
                    "Filing reviews trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_23_02_bounding_fresh_verb_inflections_missing(self):
        for run in ("Panel grants trace summary",
                    "Panel granted trace summary",
                    "Panel granting trace summary",
                    "Panel seeks trace summary",
                    "Clerk teaches summary trace",
                    "Panel sleeps trace summary",
                    "Team wepted summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the cured underreach forms of fix
    # pass 22 Unit 2 standing governed in their exact
    # forms, subfamily by subfamily
    # ------------------------------------------------------

    def test_control_fix22_subfamily_a_governed(self):
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

    def test_control_fix22_subfamily_b_governed(self):
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

    def test_control_fix22_subfamily_c_governed(self):
        for head in ("Boardcabinettallyed",
                     "Gatevaulttallyes",
                     "Boardagendastallye",
                     "Gatereportstalliez"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix22_subfamily_d_governed(self):
        for head in ("Tallyeu",
                     "Tallyau",
                     "Boardtallyeu",
                     "Boardtallyau",
                     "Tallyui",
                     "Talleui",
                     "Boardtallyui",
                     "Boardtallyuo"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix22_subfamily_e_governed(self):
        for head in ("Trace summarisereseseses",
                     "Trace summarisingeseseses",
                     "Trace summarieseseseses",
                     "Trace summarisedeseseses",
                     "Trace summariseeseseseses",
                     "Trace summaryeseseseses",
                     "Trace summarisationeseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix22_subfamily_f_governed(self):
        for head in ("Boardtracesummarisereseseses",
                     "Tracessummarieseseseses",
                     "Boardtracesummarisedeseseses",
                     "Tracessummaryeseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix22_subfamily_g_governed(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewannexsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewannextrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewannexsummary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix22_subfamily_h_governed(self):
        for head in ("Trace board gate review annex panel board gate review "
                     "annex panel board gate summary",
                     "Trace board gate annex review panel board gate annex "
                     "review panel board gate summary",
                     "Summary board gate review annex panel board gate "
                     "review annex panel board trace",
                     "Summary board gate annex review panel board gate "
                     "annex review panel board trace"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix22_subfamily_i_governed(self):
        self._candidate_governed(
            _bad("Trace board gate review annex panel board "
                 "gate review annex panel board gate for step 2"),
            _read("Trace board gate review annex panel board "
                  "gate review annex panel board gate for step 2"))

    def test_control_fix22_subfamily_j_governed(self):
        for head in ("Trace ʍummarise",
                     "Board ʘally",
                     "Trace summarisɞ",
                     "Board ʭally",
                     "Trace summariseɟ",
                     "Board ʙally",
                     "Board taʞly",
                     "Board tallʢ",
                     "Trace ʀummarise",
                     "Trace suɴmarise",
                     "Trace summaɸise",
                     "Trace summarisʚ",
                     "Trace summarisʡ"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix22_beside_forms_uncounted(self):
        for head in ("Cabinettally", "Trace summarisereseseses",
                     "Exhibittally", "Trace summarisedeseseses"):
            self._beside_step2_uncounted(_bad(head))

    def test_control_fix22_gate_ruling_forms_governed(self):
        for head in ("Cabinettally", "Exhibittally",
                     "Trace summarisereseseses"):
            report = self._q4_alone(_bad(head), ruling=True)
            self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # Held controls: every form of R16-22-02 standing
    # missing in its prose form, as Unit 1 of fix pass 22
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
        for run in ("Ledger § trace summary",
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
    # Held controls: every form of R16-21-02 standing
    # missing in its prose form, as Unit 1 of fix pass 22
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
                    "Ledger — trace summary",
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
                     "Worksheettally", "Handbooktally",
                     "Drawertallies", "Boardtallyuo",
                     "Trace summarieseses"):
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
                     "Trace summariseʠ",
                     "Trace summarisꭓe",
                     "Board taɭly",
                     "Trace summariseȡ",
                     "Board tallꭹ",
                     "Trace ʛummarise",
                     "Trace summariseƀ",
                     "Board tælly",
                     "Board taŋly",
                     "Board tallþ",
                     "Trace ʒummarise",
                     "Trace summariseɭ"):
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
        self._candidate_governed(_bad("Trace sʉmmarise"),
                                 _read("Trace sʉmmarise"))

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
