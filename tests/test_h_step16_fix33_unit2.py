"""Step 16 fix pass 33 unit 2 tests: the Q-4 closing unit.

Pinning tests for register item R16-33-01 (Medium,
B33-C01 and B33-B01) of Step 16 round 33. The
governing rule of the pass, in its extended form: a
piece not read in full, for whatever reason, is not
read, and its converse: a piece that is no feeder
flips nothing.

R16-33-01: malformed tally statement heads standing
unread past the widened boundary of fix pass 32, on
the counted pattern head agnosticism ground alone:
the pattern standing counted over a plain whole word
pattern, so a malformed head whose counted sibling
counts stands missing in the row although it stands
as a feeder statement in a form the row cannot parse.
Two hundred and thirty four distinct alone forms
stand driven in ten subfamilies: (a) tally forms
fused behind record words no widening has named and
behind the plurals of record words in the same
position, twenty forms; (b) composite openings built
on those forms, six forms; (c) a variant spelling in
that composite opening position built on those words,
two forms; (d) the variant spellings past the widened
variant sets of ninety four and ninety five, twenty
forms; (e) the summary word in further forms at the
fifteenth and sixteenth es repetitions of its
families, seven forms; (f) the fused closings built
on those forms, four forms; (g) the fused closings
with twenty governed words fused between the closing
words, three forms; (h) the inserted closings with
twenty three words of subject between in their wide,
middle swap and full swap shapes in both directions,
six forms; (i) the for step closing with twenty three
words of subject between, one form, standing in its
driven form at twenty three words between, as both
papers of the round drive it, where the register
quotes the twenty two word governed control form in
its place, as the unit report records in the open;
and (j) further Latin and kindred letters past the
widened fold set, each standing in a position the
folding does not read, one hundred and sixty five
forms, the correctness forms of that subfamily
standing in their exact driven strings as the probe
records of the correctness staging record them and
the breaker forms standing in the words the breaker
paper names. The fifty nine underreach assertions of
the round 33 breaker exhibit stand adopted in this
module: the fifty five alone form assertions of
B33-B01 stand among the defect tests of the
subfamilies above in their driven words, and the
beside assertions, the gate ruling assertion and the
code level assertion of that exhibit stand as defect
tests here in the forms the exhibit names them. The
defect stands bounded in the open by its held
controls: every form of R16-33-02 standing missing,
every held form of that item standing missing in its
recorded form, every governed closing of that item
standing governed, and on the underreach side the
governed neighbours of both papers standing governed,
the governed candidates of subfamily (a) of the
correctness paper standing governed through the
governed stems and blocks at the close of their fused
forms, the governed composite openings and the
governed variant composite openings of that paper
standing governed, the widest form of every summary
family standing governed in the widened enumeration
at its family position, the summary fused form
standing governed through the fifteenth es
repetition, the eighty three governed letter forms
of subfamily (j) of the correctness paper standing
governed at their positions, Songbooktally,
Hymnbooktally, Prayerbooktally, Missaltally,
Sermontally and Memoirtally of the breaker paper
standing governed, Songbookstallies standing governed
in its present standings, Boarddictionarytally
standing governed through the further position limb,
the candidate letters of the breaker paper standing
folded to their words, the fused and inserted
closings standing at their governed counts, the
nineteen word fused between closing, the twenty two
word forward and reversed inserted closings and the
twenty two word for step closing standing governed,
and the plain Latin spellings standing at their
standings. Locus: derivation_core.py,
_tally_statement_head and its standing helpers and
constants. The cure these tests pin widens what a
malformed tally statement head is in standing: the
governed fused prefix set widened by the record words
and plural stems of this round, the variant sets
widened by the spellings of this round, the summary
word set widened by the further forms of this round,
the fused between reach widened to twenty governed
words, the inserted closings standing at twenty three
words forward, twenty three words reversed and
twenty three words in the for step form under the
wide test, and the folding widened by the whole word
readings of this round, so every driven form stands
governed beside its counted sibling while every
control stands as it stood.
"""

from metrics_starter_collector.derivation_core import (
    _fold_word, _fused_trace_summary, _summary_word,
    _tally_statement_head, _tally_word)
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, gate_ruling,
    row_block, run_tool)
from tests.test_h_step16_fix3_unit1 import (
    TRACE_3, _clean_files)
from tests.test_h_step16_fix7_unit2 import (
    GATE_2, _bad, _read)
from tests.test_h_step16_unit1 import _write_tree

RULING_2 = "steps/step-02-gate-ruling.md"
GATE_3 = "steps/step-03-gate-record.md"


def _prose(run):
    return (run + ": LANDED figures stand here, "
            "no counts stated")


class TestStep16Fix33Unit2(FixtureTestCase):

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

    # ------------------------------------------------------
    # Defect forms of R16-33-01, subfamily (a):
    # fused record words and the plurals of record words.
    # ------------------------------------------------------

    def test_r16_33_01_a_00_governed(self):
        self._candidate(_bad('Hymnalstallies'), _read('Hymnalstallies'))

    def test_r16_33_01_a_01_governed(self):
        self._candidate(_bad('Missalstallies'), _read('Missalstallies'))

    def test_r16_33_01_a_02_governed(self):
        self._candidate(_bad('Psalterstallies'), _read('Psalterstallies'))

    def test_r16_33_01_a_03_governed(self):
        self._candidate(_bad('Breviarystallies'), _read('Breviarystallies'))

    def test_r16_33_01_a_04_governed(self):
        self._candidate(_bad('Lectionarytally'), _read('Lectionarytally'))

    def test_r16_33_01_a_05_governed(self):
        self._candidate(_bad('Lectionarystallies'), _read('Lectionarystallies'))

    def test_r16_33_01_a_06_governed(self):
        self._candidate(_bad('Sketchbookstallies'), _read('Sketchbookstallies'))

    def test_r16_33_01_a_07_governed(self):
        self._candidate(_bad('Phrasebookstallies'), _read('Phrasebookstallies'))

    def test_r16_33_01_a_08_governed(self):
        self._candidate(_bad('Runebookstallies'), _read('Runebookstallies'))

    def test_r16_33_01_a_09_governed(self):
        self._candidate(_bad('Spellbookstallies'), _read('Spellbookstallies'))

    def test_r16_33_01_a_10_governed(self):
        self._candidate(_bad('Casebookstallies'), _read('Casebookstallies'))

    def test_r16_33_01_a_11_governed(self):
        self._candidate(_bad('Guidebookstallies'), _read('Guidebookstallies'))

    def test_r16_33_01_a_12_governed(self):
        self._candidate(_bad('Quarterlytally'), _read('Quarterlytally'))

    def test_r16_33_01_a_13_governed(self):
        self._candidate(_bad('Annualtally'), _read('Annualtally'))

    def test_r16_33_01_a_14_governed(self):
        self._candidate(_bad('Catechismtally'), _read('Catechismtally'))

    def test_r16_33_01_a_15_governed(self):
        self._candidate(_bad('Fasciclettally'), _read('Fasciclettally'))

    def test_r16_33_01_a_16_governed(self):
        self._candidate(_bad('Vespertally'), _read('Vespertally'))

    def test_r16_33_01_a_17_governed(self):
        self._candidate(_bad('Sermonstallies'), _read('Sermonstallies'))

    def test_r16_33_01_a_18_governed(self):
        self._candidate(_bad('Lecturestallies'), _read('Lecturestallies'))

    def test_r16_33_01_a_19_governed(self):
        self._candidate(_bad('Bookmarkstallies'), _read('Bookmarkstallies'))

    # ------------------------------------------------------
    # Defect forms of R16-33-01, subfamily (b):
    # composite openings built on those forms.
    # ------------------------------------------------------

    def test_r16_33_01_b_00_governed(self):
        self._candidate(_bad('Boardmissalstallies'), _read('Boardmissalstallies'))

    def test_r16_33_01_b_01_governed(self):
        self._candidate(_bad('Boardquarterlytally'), _read('Boardquarterlytally'))

    def test_r16_33_01_b_02_governed(self):
        self._candidate(_bad('Gateannualtally'), _read('Gateannualtally'))

    def test_r16_33_01_b_03_governed(self):
        self._candidate(_bad('Reviewcatechismtally'), _read('Reviewcatechismtally'))

    def test_r16_33_01_b_04_governed(self):
        self._candidate(_bad('Boardfasciclettally'), _read('Boardfasciclettally'))

    def test_r16_33_01_b_05_governed(self):
        self._candidate(_bad('Gatesermonstallies'), _read('Gatesermonstallies'))

    # ------------------------------------------------------
    # Defect forms of R16-33-01, subfamily (c):
    # a variant spelling in that composite opening position.
    # ------------------------------------------------------

    def test_r16_33_01_c_00_governed(self):
        self._candidate(_bad('Boardquarterlytallye'), _read('Boardquarterlytallye'))

    def test_r16_33_01_c_01_governed(self):
        self._candidate(_bad('Gateannualtalliez'), _read('Gateannualtalliez'))

    # ------------------------------------------------------
    # Defect forms of R16-33-01, subfamily (d):
    # the variant spellings past the widened variant sets.
    # ------------------------------------------------------

    def test_r16_33_01_d_00_governed(self):
        self._candidate(_bad('Tallya10'), _read('Tallya10'))

    def test_r16_33_01_d_01_governed(self):
        self._candidate(_bad('Tallyo9'), _read('Tallyo9'))

    def test_r16_33_01_d_02_governed(self):
        self._candidate(_bad('Tallyu9'), _read('Tallyu9'))

    def test_r16_33_01_d_03_governed(self):
        self._candidate(_bad('Tallyai9'), _read('Tallyai9'))

    def test_r16_33_01_d_04_governed(self):
        self._candidate(_bad('Tallyez8'), _read('Tallyez8'))

    def test_r16_33_01_d_05_governed(self):
        self._candidate(_bad('Tallyaz8'), _read('Tallyaz8'))

    def test_r16_33_01_d_06_governed(self):
        self._candidate(_bad('Tallyeo11'), _read('Tallyeo11'))

    def test_r16_33_01_d_07_governed(self):
        self._candidate(_bad('Tallyia3'), _read('Tallyia3'))

    def test_r16_33_01_d_08_governed(self):
        self._candidate(_bad('Tallye9'), _read('Tallye9'))

    def test_r16_33_01_d_09_governed(self):
        self._candidate(_bad('Boardtallya10'), _read('Boardtallya10'))

    def test_r16_33_01_d_10_governed(self):
        self._candidate(_bad('Boardtallyo9'), _read('Boardtallyo9'))

    def test_r16_33_01_d_11_governed(self):
        self._candidate(_bad('Boardtallyu9'), _read('Boardtallyu9'))

    def test_r16_33_01_d_12_governed(self):
        self._candidate(_bad('Boardtallyai9'), _read('Boardtallyai9'))

    def test_r16_33_01_d_13_governed(self):
        self._candidate(_bad('Boardtallyez8'), _read('Boardtallyez8'))

    def test_r16_33_01_d_14_governed(self):
        self._candidate(_bad('Boardtallyaz8'), _read('Boardtallyaz8'))

    def test_r16_33_01_d_15_governed(self):
        self._candidate(_bad('Boardtallyeo11'), _read('Boardtallyeo11'))

    def test_r16_33_01_d_16_governed(self):
        self._candidate(_bad('Boardtallyia3'), _read('Boardtallyia3'))

    def test_r16_33_01_d_17_governed(self):
        self._candidate(_bad('Boardtallye9'), _read('Boardtallye9'))

    def test_r16_33_01_d_18_governed(self):
        self._candidate(_bad('Boardtallyaz'), _read('Boardtallyaz'))

    def test_r16_33_01_d_19_governed(self):
        self._candidate(_bad('Boardtallyaz2'), _read('Boardtallyaz2'))

    # ------------------------------------------------------
    # Defect forms of R16-33-01, subfamily (e):
    # the summary word in further forms past the one
    # hundred and thirty three.
    # ------------------------------------------------------

    def test_r16_33_01_e_00_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseseseseses'))

    def test_r16_33_01_e_01_governed(self):
        self._candidate(_bad('Trace summarisingeseseseseseseseseseseseseseses'), _read('Trace summarisingeseseseseseseseseseseseseseses'))

    def test_r16_33_01_e_02_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseseseses'))

    def test_r16_33_01_e_03_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseseseses'))

    def test_r16_33_01_e_04_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseseseses'))

    def test_r16_33_01_e_05_governed(self):
        self._candidate(_bad('Trace summaryeseseseseseseseseseseseseseseses'), _read('Trace summaryeseseseseseseseseseseseseseseses'))

    def test_r16_33_01_e_06_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseseseses'))

    # ------------------------------------------------------
    # Defect forms of R16-33-01, subfamily (f):
    # the fused closings built on those forms.
    # ------------------------------------------------------

    def test_r16_33_01_f_00_governed(self):
        self._candidate(_bad('Boardtracesummarisereseseseseseseseseseseseseseses'), _read('Boardtracesummarisereseseseseseseseseseseseseseses'))

    def test_r16_33_01_f_01_governed(self):
        self._candidate(_bad('Tracessummarieseseseseseseseseseseseseseseses'), _read('Tracessummarieseseseseseseseseseseseseseseses'))

    def test_r16_33_01_f_02_governed(self):
        self._candidate(_bad('Boardtracesummarisedeseseseseseseseseseseseseseses'), _read('Boardtracesummarisedeseseseseseseseseseseseseseses'))

    def test_r16_33_01_f_03_governed(self):
        self._candidate(_bad('Tracessummaryeseseseseseseseseseseseseseseses'), _read('Tracessummaryeseseseseseseseseseseseseseseses'))

    # ------------------------------------------------------
    # Defect forms of R16-33-01, subfamily (g):
    # the fused closings with twenty governed words
    # fused between the closing words.
    # ------------------------------------------------------

    def test_r16_33_01_g_00_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'))

    def test_r16_33_01_g_01_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpaneltrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpaneltrace'))

    def test_r16_33_01_g_02_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'))

    # ------------------------------------------------------
    # Defect forms of R16-33-01, subfamily (h):
    # the inserted closings with twenty three words
    # of subject between.
    # ------------------------------------------------------

    def test_r16_33_01_h_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review summary'))

    def test_r16_33_01_h_01_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review summary'), _read('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review summary'))

    def test_r16_33_01_h_02_governed(self):
        self._candidate(_bad('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex summary'), _read('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex summary'))

    def test_r16_33_01_h_03_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review trace'))

    def test_r16_33_01_h_04_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review trace'), _read('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review trace'))

    def test_r16_33_01_h_05_governed(self):
        self._candidate(_bad('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex trace'), _read('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex trace'))

    # ------------------------------------------------------
    # Defect forms of R16-33-01, subfamily (i):
    # the for step closing with twenty three words
    # of subject between, in its driven form.
    # ------------------------------------------------------

    def test_r16_33_01_i_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review for step 2'))

    # ------------------------------------------------------
    # Defect forms of R16-33-01, subfamily (j):
    # further letters past the widened fold set, in
    # positions the folding does not read.
    # ------------------------------------------------------

    def test_r16_33_01_j_00_governed(self):
        self._candidate(_bad('Board Ɂally'), _read('Board Ɂally'))

    def test_r16_33_01_j_01_governed(self):
        self._candidate(_bad('Board ɂally'), _read('Board ɂally'))

    def test_r16_33_01_j_02_governed(self):
        self._candidate(_bad('Board Ƀally'), _read('Board Ƀally'))

    def test_r16_33_01_j_03_governed(self):
        self._candidate(_bad('Board Ʉally'), _read('Board Ʉally'))

    def test_r16_33_01_j_04_governed(self):
        self._candidate(_bad('Board Ɉally'), _read('Board Ɉally'))

    def test_r16_33_01_j_05_governed(self):
        self._candidate(_bad('Board ɉally'), _read('Board ɉally'))

    def test_r16_33_01_j_06_governed(self):
        self._candidate(_bad('Board Ɋally'), _read('Board Ɋally'))

    def test_r16_33_01_j_07_governed(self):
        self._candidate(_bad('Board ɋally'), _read('Board ɋally'))

    def test_r16_33_01_j_08_governed(self):
        self._candidate(_bad('Board Ɍally'), _read('Board Ɍally'))

    def test_r16_33_01_j_09_governed(self):
        self._candidate(_bad('Board ɍally'), _read('Board ɍally'))

    def test_r16_33_01_j_10_governed(self):
        self._candidate(_bad('Board Ɏally'), _read('Board Ɏally'))

    def test_r16_33_01_j_11_governed(self):
        self._candidate(_bad('Board ɏally'), _read('Board ɏally'))

    def test_r16_33_01_j_12_governed(self):
        self._candidate(_bad('Board ɐally'), _read('Board ɐally'))

    def test_r16_33_01_j_13_governed(self):
        self._candidate(_bad('Board ɑally'), _read('Board ɑally'))

    def test_r16_33_01_j_14_governed(self):
        self._candidate(_bad('Board ɒally'), _read('Board ɒally'))

    def test_r16_33_01_j_15_governed(self):
        self._candidate(_bad('Board ɘally'), _read('Board ɘally'))

    def test_r16_33_01_j_16_governed(self):
        self._candidate(_bad('Board ɚally'), _read('Board ɚally'))

    def test_r16_33_01_j_17_governed(self):
        self._candidate(_bad('Board ɜally'), _read('Board ɜally'))

    def test_r16_33_01_j_18_governed(self):
        self._candidate(_bad('Board ɝally'), _read('Board ɝally'))

    def test_r16_33_01_j_19_governed(self):
        self._candidate(_bad('Board ɞally'), _read('Board ɞally'))

    def test_r16_33_01_j_20_governed(self):
        self._candidate(_bad('Board ɟally'), _read('Board ɟally'))

    def test_r16_33_01_j_21_governed(self):
        self._candidate(_bad('Board ɡally'), _read('Board ɡally'))

    def test_r16_33_01_j_22_governed(self):
        self._candidate(_bad('Board ɤally'), _read('Board ɤally'))

    def test_r16_33_01_j_23_governed(self):
        self._candidate(_bad('Board ɥally'), _read('Board ɥally'))

    def test_r16_33_01_j_24_governed(self):
        self._candidate(_bad('Board ɦally'), _read('Board ɦally'))

    def test_r16_33_01_j_25_governed(self):
        self._candidate(_bad('Board taɁly'), _read('Board taɁly'))

    def test_r16_33_01_j_26_governed(self):
        self._candidate(_bad('Board taɂly'), _read('Board taɂly'))

    def test_r16_33_01_j_27_governed(self):
        self._candidate(_bad('Board taɃly'), _read('Board taɃly'))

    def test_r16_33_01_j_28_governed(self):
        self._candidate(_bad('Board taɄly'), _read('Board taɄly'))

    def test_r16_33_01_j_29_governed(self):
        self._candidate(_bad('Board taɅly'), _read('Board taɅly'))

    def test_r16_33_01_j_30_governed(self):
        self._candidate(_bad('Board taɈly'), _read('Board taɈly'))

    def test_r16_33_01_j_31_governed(self):
        self._candidate(_bad('Board taɉly'), _read('Board taɉly'))

    def test_r16_33_01_j_32_governed(self):
        self._candidate(_bad('Board taɊly'), _read('Board taɊly'))

    def test_r16_33_01_j_33_governed(self):
        self._candidate(_bad('Board taɋly'), _read('Board taɋly'))

    def test_r16_33_01_j_34_governed(self):
        self._candidate(_bad('Board taɌly'), _read('Board taɌly'))

    def test_r16_33_01_j_35_governed(self):
        self._candidate(_bad('Board taɍly'), _read('Board taɍly'))

    def test_r16_33_01_j_36_governed(self):
        self._candidate(_bad('Board taɎly'), _read('Board taɎly'))

    def test_r16_33_01_j_37_governed(self):
        self._candidate(_bad('Board taɏly'), _read('Board taɏly'))

    def test_r16_33_01_j_38_governed(self):
        self._candidate(_bad('Board taɐly'), _read('Board taɐly'))

    def test_r16_33_01_j_39_governed(self):
        self._candidate(_bad('Board taɑly'), _read('Board taɑly'))

    def test_r16_33_01_j_40_governed(self):
        self._candidate(_bad('Board taɒly'), _read('Board taɒly'))

    def test_r16_33_01_j_41_governed(self):
        self._candidate(_bad('Board taɓly'), _read('Board taɓly'))

    def test_r16_33_01_j_42_governed(self):
        self._candidate(_bad('Board taɘly'), _read('Board taɘly'))

    def test_r16_33_01_j_43_governed(self):
        self._candidate(_bad('Board taɚly'), _read('Board taɚly'))

    def test_r16_33_01_j_44_governed(self):
        self._candidate(_bad('Board taɜly'), _read('Board taɜly'))

    def test_r16_33_01_j_45_governed(self):
        self._candidate(_bad('Board taɝly'), _read('Board taɝly'))

    def test_r16_33_01_j_46_governed(self):
        self._candidate(_bad('Board taɞly'), _read('Board taɞly'))

    def test_r16_33_01_j_47_governed(self):
        self._candidate(_bad('Board taɟly'), _read('Board taɟly'))

    def test_r16_33_01_j_48_governed(self):
        self._candidate(_bad('Board taɡly'), _read('Board taɡly'))

    def test_r16_33_01_j_49_governed(self):
        self._candidate(_bad('Board taɤly'), _read('Board taɤly'))

    def test_r16_33_01_j_50_governed(self):
        self._candidate(_bad('Board taɥly'), _read('Board taɥly'))

    def test_r16_33_01_j_51_governed(self):
        self._candidate(_bad('Board taɦly'), _read('Board taɦly'))

    def test_r16_33_01_j_52_governed(self):
        self._candidate(_bad('Board taɧly'), _read('Board taɧly'))

    def test_r16_33_01_j_53_governed(self):
        self._candidate(_bad('Trace sɁmmarise'), _read('Trace sɁmmarise'))

    def test_r16_33_01_j_54_governed(self):
        self._candidate(_bad('Trace sɂmmarise'), _read('Trace sɂmmarise'))

    def test_r16_33_01_j_55_governed(self):
        self._candidate(_bad('Trace sɃmmarise'), _read('Trace sɃmmarise'))

    def test_r16_33_01_j_56_governed(self):
        self._candidate(_bad('Trace sɅmmarise'), _read('Trace sɅmmarise'))

    def test_r16_33_01_j_57_governed(self):
        self._candidate(_bad('Trace sɈmmarise'), _read('Trace sɈmmarise'))

    def test_r16_33_01_j_58_governed(self):
        self._candidate(_bad('Trace sɉmmarise'), _read('Trace sɉmmarise'))

    def test_r16_33_01_j_59_governed(self):
        self._candidate(_bad('Trace sɊmmarise'), _read('Trace sɊmmarise'))

    def test_r16_33_01_j_60_governed(self):
        self._candidate(_bad('Trace sɋmmarise'), _read('Trace sɋmmarise'))

    def test_r16_33_01_j_61_governed(self):
        self._candidate(_bad('Trace sɌmmarise'), _read('Trace sɌmmarise'))

    def test_r16_33_01_j_62_governed(self):
        self._candidate(_bad('Trace sɍmmarise'), _read('Trace sɍmmarise'))

    def test_r16_33_01_j_63_governed(self):
        self._candidate(_bad('Trace sɎmmarise'), _read('Trace sɎmmarise'))

    def test_r16_33_01_j_64_governed(self):
        self._candidate(_bad('Trace sɏmmarise'), _read('Trace sɏmmarise'))

    def test_r16_33_01_j_65_governed(self):
        self._candidate(_bad('Trace sɐmmarise'), _read('Trace sɐmmarise'))

    def test_r16_33_01_j_66_governed(self):
        self._candidate(_bad('Trace sɑmmarise'), _read('Trace sɑmmarise'))

    def test_r16_33_01_j_67_governed(self):
        self._candidate(_bad('Trace sɒmmarise'), _read('Trace sɒmmarise'))

    def test_r16_33_01_j_68_governed(self):
        self._candidate(_bad('Trace sɓmmarise'), _read('Trace sɓmmarise'))

    def test_r16_33_01_j_69_governed(self):
        self._candidate(_bad('Trace sɘmmarise'), _read('Trace sɘmmarise'))

    def test_r16_33_01_j_70_governed(self):
        self._candidate(_bad('Trace sɚmmarise'), _read('Trace sɚmmarise'))

    def test_r16_33_01_j_71_governed(self):
        self._candidate(_bad('Trace sɜmmarise'), _read('Trace sɜmmarise'))

    def test_r16_33_01_j_72_governed(self):
        self._candidate(_bad('Trace sɝmmarise'), _read('Trace sɝmmarise'))

    def test_r16_33_01_j_73_governed(self):
        self._candidate(_bad('Trace sɞmmarise'), _read('Trace sɞmmarise'))

    def test_r16_33_01_j_74_governed(self):
        self._candidate(_bad('Trace sɟmmarise'), _read('Trace sɟmmarise'))

    def test_r16_33_01_j_75_governed(self):
        self._candidate(_bad('Trace sɡmmarise'), _read('Trace sɡmmarise'))

    def test_r16_33_01_j_76_governed(self):
        self._candidate(_bad('Trace sɥmmarise'), _read('Trace sɥmmarise'))

    def test_r16_33_01_j_77_governed(self):
        self._candidate(_bad('Trace sɦmmarise'), _read('Trace sɦmmarise'))

    def test_r16_33_01_j_78_governed(self):
        self._candidate(_bad('Trace sɧmmarise'), _read('Trace sɧmmarise'))

    def test_r16_33_01_j_79_governed(self):
        self._candidate(_bad('Trace sumɁarise'), _read('Trace sumɁarise'))

    def test_r16_33_01_j_80_governed(self):
        self._candidate(_bad('Trace sumɂarise'), _read('Trace sumɂarise'))

    def test_r16_33_01_j_81_governed(self):
        self._candidate(_bad('Trace sumɃarise'), _read('Trace sumɃarise'))

    def test_r16_33_01_j_82_governed(self):
        self._candidate(_bad('Trace sumɄarise'), _read('Trace sumɄarise'))

    def test_r16_33_01_j_83_governed(self):
        self._candidate(_bad('Trace sumɅarise'), _read('Trace sumɅarise'))

    def test_r16_33_01_j_84_governed(self):
        self._candidate(_bad('Trace sumɈarise'), _read('Trace sumɈarise'))

    def test_r16_33_01_j_85_governed(self):
        self._candidate(_bad('Trace sumɉarise'), _read('Trace sumɉarise'))

    def test_r16_33_01_j_86_governed(self):
        self._candidate(_bad('Trace sumɊarise'), _read('Trace sumɊarise'))

    def test_r16_33_01_j_87_governed(self):
        self._candidate(_bad('Trace sumɋarise'), _read('Trace sumɋarise'))

    def test_r16_33_01_j_88_governed(self):
        self._candidate(_bad('Trace sumɌarise'), _read('Trace sumɌarise'))

    def test_r16_33_01_j_89_governed(self):
        self._candidate(_bad('Trace sumɍarise'), _read('Trace sumɍarise'))

    def test_r16_33_01_j_90_governed(self):
        self._candidate(_bad('Trace sumɎarise'), _read('Trace sumɎarise'))

    def test_r16_33_01_j_91_governed(self):
        self._candidate(_bad('Trace sumɏarise'), _read('Trace sumɏarise'))

    def test_r16_33_01_j_92_governed(self):
        self._candidate(_bad('Trace sumɐarise'), _read('Trace sumɐarise'))

    def test_r16_33_01_j_93_governed(self):
        self._candidate(_bad('Trace sumɑarise'), _read('Trace sumɑarise'))

    def test_r16_33_01_j_94_governed(self):
        self._candidate(_bad('Trace sumɒarise'), _read('Trace sumɒarise'))

    def test_r16_33_01_j_95_governed(self):
        self._candidate(_bad('Trace sumɓarise'), _read('Trace sumɓarise'))

    def test_r16_33_01_j_96_governed(self):
        self._candidate(_bad('Trace sumɘarise'), _read('Trace sumɘarise'))

    def test_r16_33_01_j_97_governed(self):
        self._candidate(_bad('Trace sumɚarise'), _read('Trace sumɚarise'))

    def test_r16_33_01_j_98_governed(self):
        self._candidate(_bad('Trace sumɜarise'), _read('Trace sumɜarise'))

    def test_r16_33_01_j_99_governed(self):
        self._candidate(_bad('Trace sumɝarise'), _read('Trace sumɝarise'))

    def test_r16_33_01_j_100_governed(self):
        self._candidate(_bad('Trace sumɞarise'), _read('Trace sumɞarise'))

    def test_r16_33_01_j_101_governed(self):
        self._candidate(_bad('Trace sumɟarise'), _read('Trace sumɟarise'))

    def test_r16_33_01_j_102_governed(self):
        self._candidate(_bad('Trace sumɡarise'), _read('Trace sumɡarise'))

    def test_r16_33_01_j_103_governed(self):
        self._candidate(_bad('Trace sumɤarise'), _read('Trace sumɤarise'))

    def test_r16_33_01_j_104_governed(self):
        self._candidate(_bad('Trace sumɥarise'), _read('Trace sumɥarise'))

    def test_r16_33_01_j_105_governed(self):
        self._candidate(_bad('Trace sumɦarise'), _read('Trace sumɦarise'))

    def test_r16_33_01_j_106_governed(self):
        self._candidate(_bad('Trace sumɧarise'), _read('Trace sumɧarise'))

    def test_r16_33_01_j_107_governed(self):
        self._candidate(_bad('Trace summariɁe'), _read('Trace summariɁe'))

    def test_r16_33_01_j_108_governed(self):
        self._candidate(_bad('Trace summariɂe'), _read('Trace summariɂe'))

    def test_r16_33_01_j_109_governed(self):
        self._candidate(_bad('Trace summariɃe'), _read('Trace summariɃe'))

    def test_r16_33_01_j_110_governed(self):
        self._candidate(_bad('Trace summariɄe'), _read('Trace summariɄe'))

    def test_r16_33_01_j_111_governed(self):
        self._candidate(_bad('Trace summariɅe'), _read('Trace summariɅe'))

    def test_r16_33_01_j_112_governed(self):
        self._candidate(_bad('Trace summariɈe'), _read('Trace summariɈe'))

    def test_r16_33_01_j_113_governed(self):
        self._candidate(_bad('Trace summariɉe'), _read('Trace summariɉe'))

    def test_r16_33_01_j_114_governed(self):
        self._candidate(_bad('Trace summariɌe'), _read('Trace summariɌe'))

    def test_r16_33_01_j_115_governed(self):
        self._candidate(_bad('Trace summariɍe'), _read('Trace summariɍe'))

    def test_r16_33_01_j_116_governed(self):
        self._candidate(_bad('Trace summariɎe'), _read('Trace summariɎe'))

    def test_r16_33_01_j_117_governed(self):
        self._candidate(_bad('Trace summariɏe'), _read('Trace summariɏe'))

    def test_r16_33_01_j_118_governed(self):
        self._candidate(_bad('Trace summariɐe'), _read('Trace summariɐe'))

    def test_r16_33_01_j_119_governed(self):
        self._candidate(_bad('Trace summariɑe'), _read('Trace summariɑe'))

    def test_r16_33_01_j_120_governed(self):
        self._candidate(_bad('Trace summariɒe'), _read('Trace summariɒe'))

    def test_r16_33_01_j_121_governed(self):
        self._candidate(_bad('Trace summariɓe'), _read('Trace summariɓe'))

    def test_r16_33_01_j_122_governed(self):
        self._candidate(_bad('Trace summariɘe'), _read('Trace summariɘe'))

    def test_r16_33_01_j_123_governed(self):
        self._candidate(_bad('Trace summariɚe'), _read('Trace summariɚe'))

    def test_r16_33_01_j_124_governed(self):
        self._candidate(_bad('Trace summariɜe'), _read('Trace summariɜe'))

    def test_r16_33_01_j_125_governed(self):
        self._candidate(_bad('Trace summariɝe'), _read('Trace summariɝe'))

    def test_r16_33_01_j_126_governed(self):
        self._candidate(_bad('Trace summariɞe'), _read('Trace summariɞe'))

    def test_r16_33_01_j_127_governed(self):
        self._candidate(_bad('Trace summariɟe'), _read('Trace summariɟe'))

    def test_r16_33_01_j_128_governed(self):
        self._candidate(_bad('Trace summariɡe'), _read('Trace summariɡe'))

    def test_r16_33_01_j_129_governed(self):
        self._candidate(_bad('Trace summariɤe'), _read('Trace summariɤe'))

    def test_r16_33_01_j_130_governed(self):
        self._candidate(_bad('Trace summariɥe'), _read('Trace summariɥe'))

    def test_r16_33_01_j_131_governed(self):
        self._candidate(_bad('Trace summariɦe'), _read('Trace summariɦe'))

    def test_r16_33_01_j_132_governed(self):
        self._candidate(_bad('Trace summariɧe'), _read('Trace summariɧe'))

    def test_r16_33_01_j_133_governed(self):
        self._candidate(_bad('Trace summarisɁ'), _read('Trace summarisɁ'))

    def test_r16_33_01_j_134_governed(self):
        self._candidate(_bad('Trace summarisɂ'), _read('Trace summarisɂ'))

    def test_r16_33_01_j_135_governed(self):
        self._candidate(_bad('Trace summarisɃ'), _read('Trace summarisɃ'))

    def test_r16_33_01_j_136_governed(self):
        self._candidate(_bad('Trace summarisɄ'), _read('Trace summarisɄ'))

    def test_r16_33_01_j_137_governed(self):
        self._candidate(_bad('Trace summarisɈ'), _read('Trace summarisɈ'))

    def test_r16_33_01_j_138_governed(self):
        self._candidate(_bad('Trace summarisɉ'), _read('Trace summarisɉ'))

    def test_r16_33_01_j_139_governed(self):
        self._candidate(_bad('Trace summarisɊ'), _read('Trace summarisɊ'))

    def test_r16_33_01_j_140_governed(self):
        self._candidate(_bad('Trace summarisɋ'), _read('Trace summarisɋ'))

    def test_r16_33_01_j_141_governed(self):
        self._candidate(_bad('Trace summarisɌ'), _read('Trace summarisɌ'))

    def test_r16_33_01_j_142_governed(self):
        self._candidate(_bad('Trace summarisɍ'), _read('Trace summarisɍ'))

    def test_r16_33_01_j_143_governed(self):
        self._candidate(_bad('Trace summarisɎ'), _read('Trace summarisɎ'))

    def test_r16_33_01_j_144_governed(self):
        self._candidate(_bad('Trace summarisɏ'), _read('Trace summarisɏ'))

    def test_r16_33_01_j_145_governed(self):
        self._candidate(_bad('Trace summarisɐ'), _read('Trace summarisɐ'))

    def test_r16_33_01_j_146_governed(self):
        self._candidate(_bad('Trace summarisɑ'), _read('Trace summarisɑ'))

    def test_r16_33_01_j_147_governed(self):
        self._candidate(_bad('Trace summarisɒ'), _read('Trace summarisɒ'))

    def test_r16_33_01_j_148_governed(self):
        self._candidate(_bad('Trace summarisɓ'), _read('Trace summarisɓ'))

    def test_r16_33_01_j_149_governed(self):
        self._candidate(_bad('Trace summarisɚ'), _read('Trace summarisɚ'))

    def test_r16_33_01_j_150_governed(self):
        self._candidate(_bad('Trace summarisɝ'), _read('Trace summarisɝ'))

    def test_r16_33_01_j_151_governed(self):
        self._candidate(_bad('Trace summarisɟ'), _read('Trace summarisɟ'))

    def test_r16_33_01_j_152_governed(self):
        self._candidate(_bad('Trace summarisɡ'), _read('Trace summarisɡ'))

    def test_r16_33_01_j_153_governed(self):
        self._candidate(_bad('Trace summarisɤ'), _read('Trace summarisɤ'))

    def test_r16_33_01_j_154_governed(self):
        self._candidate(_bad('Trace summarisɥ'), _read('Trace summarisɥ'))

    def test_r16_33_01_j_155_governed(self):
        self._candidate(_bad('Trace summarisɦ'), _read('Trace summarisɦ'))

    def test_r16_33_01_j_156_governed(self):
        self._candidate(_bad('Trace summarisɧ'), _read('Trace summarisɧ'))

    def test_r16_33_01_j_157_governed(self):
        self._candidate(_bad('Board ǆally'), _read('Board ǆally'))

    def test_r16_33_01_j_158_governed(self):
        self._candidate(_bad('Trace suǆmarise'), _read('Trace suǆmarise'))

    def test_r16_33_01_j_159_governed(self):
        self._candidate(_bad('Board ǌally'), _read('Board ǌally'))

    def test_r16_33_01_j_160_governed(self):
        self._candidate(_bad('Board taǌy'), _read('Board taǌy'))

    def test_r16_33_01_j_161_governed(self):
        self._candidate(_bad('Board ǎally'), _read('Board ǎally'))

    def test_r16_33_01_j_162_governed(self):
        self._candidate(_bad('Trace summaǎise'), _read('Trace summaǎise'))

    def test_r16_33_01_j_163_governed(self):
        self._candidate(_bad('Board Ǟally'), _read('Board Ǟally'))

    def test_r16_33_01_j_164_governed(self):
        self._candidate(_bad('Trace summarisǞ'), _read('Trace summarisǞ'))

    # ------------------------------------------------------
    # Adopted assertions of the round 33 breaker exhibit:
    # the beside, gate ruling and code level assertions
    # of B33-B01, in the forms the exhibit names them.
    # ------------------------------------------------------

    def test_b33_quarterlytally_beside(self):
        q4 = self._beside(_bad("Quarterlytally"))
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_b33_summarised_beside(self):
        q4 = self._beside(_bad('Trace summarisedeseseseseseseseseseseseseseses'))
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_b33_quarterlytally_gate_ruling(self):
        report = self._q4_alone(_bad("Quarterlytally"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    def test_b33_code_level_underreach_forms(self):
        for word in ("quarterlytally", "missalstallies",
                     "boardquarterlytally", "tallye9", "boardtallyaz"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ('summarisedeseseseseseseseseseseseseseses', 'summaryeseseseseseseseseseseseseseseses'):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ('boardtracesummarisedeseseseseseseseseseseseseseses',
                     'traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        for head in ("Quarterlytally",
                     'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review summary',
                     'Trace summarisedeseseseseseseseseseseseseseses'):
            line = head + ": items checked stand here"
            self.assertTrue(_tally_statement_head(line), head)
        self.assertEqual(_fold_word("\u01c6ally"), "tally")
        self.assertEqual(_fold_word("su\u01c6marise"), "summarise")

    # ------------------------------------------------------
    # Held controls of R16-33-02, standing missing in the
    # cure of this unit: every distinct converse form of
    # the register, one test per form.
    # ------------------------------------------------------

    def test_control_converse_000_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel smirk trace summary')))

    def test_control_converse_001_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk laugh summary trace')))

    def test_control_converse_002_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stretch trace summary')))

    def test_control_converse_003_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel pout trace summary')))

    def test_control_converse_004_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk mumble summary trace')))

    def test_control_converse_005_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stammer trace summary')))

    def test_control_converse_006_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel quiver summary trace')))

    def test_control_converse_007_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk hobble trace summary')))

    def test_control_converse_008_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team limp summary trace')))

    def test_control_converse_009_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel smirk tracesummary')))

    def test_control_converse_010_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk laugh summarytrace')))

    def test_control_converse_011_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stretch tracesummary')))

    def test_control_converse_012_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel pout tracesummary')))

    def test_control_converse_013_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk mumble summarytrace')))

    def test_control_converse_014_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stammer boardtracesummary')))

    def test_control_converse_015_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel quiver traceboardgatesummary')))

    def test_control_converse_016_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk pout traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_converse_017_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team mumble tracesummarisationeseseseseseseseseseseseseseses')))

    def test_control_converse_018_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋉ trace summary')))

    def test_control_converse_019_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨝ trace summary')))

    def test_control_converse_020_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨞ trace summary')))

    def test_control_converse_021_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨟ trace summary')))

    def test_control_converse_022_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨠ trace summary')))

    def test_control_converse_023_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨡ trace summary')))

    def test_control_converse_024_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨢ trace summary')))

    def test_control_converse_025_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨣ trace summary')))

    def test_control_converse_026_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨤ trace summary')))

    def test_control_converse_027_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨥ trace summary')))

    def test_control_converse_028_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨦ trace summary')))

    def test_control_converse_029_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨧ trace summary')))

    def test_control_converse_030_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨨ trace summary')))

    def test_control_converse_031_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨩ trace summary')))

    def test_control_converse_032_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨪ trace summary')))

    def test_control_converse_033_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨫ trace summary')))

    def test_control_converse_034_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨬ trace summary')))

    def test_control_converse_035_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨭ trace summary')))

    def test_control_converse_036_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨮ trace summary')))

    def test_control_converse_037_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨯ trace summary')))

    def test_control_converse_038_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨰ trace summary')))

    def test_control_converse_039_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨱ trace summary')))

    def test_control_converse_040_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨲ trace summary')))

    def test_control_converse_041_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨳ trace summary')))

    def test_control_converse_042_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨴ trace summary')))

    def test_control_converse_043_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨵ trace summary')))

    def test_control_converse_044_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌒ trace summary')))

    def test_control_converse_045_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌀ trace summary')))

    def test_control_converse_046_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌁ trace summary')))

    def test_control_converse_047_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⍟ trace summary')))

    def test_control_converse_048_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⎕ trace summary')))

    def test_control_converse_049_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⏚ trace summary')))

    def test_control_converse_050_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧀ trace summary')))

    def test_control_converse_051_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧁ trace summary')))

    def test_control_converse_052_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧂ trace summary')))

    def test_control_converse_053_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧃ trace summary')))

    def test_control_converse_054_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃔ trace summary')))

    def test_control_converse_055_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃕ trace summary')))

    def test_control_converse_056_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃜ trace summary')))

    def test_control_converse_057_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃝ trace summary')))

    def test_control_converse_058_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃞ trace summary')))

    def test_control_converse_059_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃟ trace summary')))

    def test_control_converse_060_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹕panel⹖ trace summary')))

    def test_control_converse_061_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Smirk panel trace summary')))

    def test_control_converse_062_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Laugh panel summary trace')))

    def test_control_converse_063_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Stretch panel trace summary')))

    def test_control_converse_064_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Pout ledger trace summary')))

    # ------------------------------------------------------
    # Held controls of R16-33-02 named in the register,
    # standing missing in their recorded forms.
    # ------------------------------------------------------

    def test_control_held33_000_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sigh trace summary')))

    def test_control_held33_001_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel blink trace summary')))

    def test_control_held33_002_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wink trace summary')))

    def test_control_held33_003_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace summary')))

    def test_control_held33_004_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cough trace summary')))

    def test_control_held33_005_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sneeze trace summary')))

    def test_control_held33_006_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stare trace summary')))

    def test_control_held33_007_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gaze trace summary')))

    def test_control_held33_008_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel frown trace summary')))

    def test_control_held33_009_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace summary')))

    def test_control_held33_010_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hum trace summary')))

    def test_control_held33_011_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sob trace summary')))

    def test_control_held33_012_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel weep trace summary')))

    def test_control_held33_013_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chuckle trace summary')))

    def test_control_held33_014_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel giggle trace summary')))

    def test_control_held33_015_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snore trace summary')))

    def test_control_held33_016_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yawn trace summary')))

    def test_control_held33_017_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel kneel trace summary')))

    def test_control_held33_018_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bow trace summary')))

    def test_control_held33_019_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wave trace summary')))

    def test_control_held33_020_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap trace summary')))

    def test_control_held33_021_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew trace summary')))

    def test_control_held33_022_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sip trace summary')))

    def test_control_held33_023_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp trace summary')))

    def test_control_held33_024_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel doze trace summary')))

    def test_control_held33_025_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sang trace summary')))

    def test_control_held33_026_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel swam trace summary')))

    def test_control_held33_027_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel froze trace summary')))

    def test_control_held33_028_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chose trace summary')))

    def test_control_held33_029_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel spoke trace summary')))

    def test_control_held33_030_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel woke trace summary')))

    def test_control_held33_031_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wore trace summary')))

    def test_control_held33_032_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tore trace summary')))

    def test_control_held33_033_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hid trace summary')))

    def test_control_held33_034_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bit trace summary')))

    def test_control_held33_035_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fled trace summary')))

    def test_control_held33_036_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bled trace summary')))

    def test_control_held33_037_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fed trace summary')))

    def test_control_held33_038_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel led trace summary')))

    def test_control_held33_039_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sped trace summary')))

    def test_control_held33_040_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shone trace summary')))

    def test_control_held33_041_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shook trace summary')))

    def test_control_held33_042_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stole trace summary')))

    def test_control_held33_043_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel broke trace summary')))

    def test_control_held33_044_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel drove trace summary')))

    def test_control_held33_045_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel rode trace summary')))

    def test_control_held33_046_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wrote trace summary')))

    def test_control_held33_047_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel rose trace summary')))

    def test_control_held33_048_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fell trace summary')))

    def test_control_held33_049_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sigh trace summary')))

    def test_control_held33_050_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk sob summary trace')))

    def test_control_held33_051_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team blink trace summary')))

    def test_control_held33_052_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wink trace summary')))

    def test_control_held33_053_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cough trace summary')))

    def test_control_held33_054_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stare trace summary')))

    def test_control_held33_055_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glare trace summary')))

    def test_control_held33_056_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grin trace summary')))

    def test_control_held33_057_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel frown trace summary')))

    def test_control_held33_058_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace summary')))

    def test_control_held33_059_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sneeze trace summary')))

    def test_control_held33_060_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whisper trace summary')))

    def test_control_held33_061_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel murmur trace summary')))

    def test_control_held33_062_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tremble trace summary')))

    def test_control_held33_063_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shiver trace summary')))

    def test_control_held33_064_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wobble trace summary')))

    def test_control_held33_065_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel froze trace summary')))

    def test_control_held33_066_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel broke trace summary')))

    def test_control_held33_067_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel spoke trace summary')))

    def test_control_held33_068_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel woke trace summary')))

    def test_control_held33_069_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stole trace summary')))

    def test_control_held33_070_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shook trace summary')))

    def test_control_held33_071_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sang trace summary')))

    def test_control_held33_072_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sank trace summary')))

    def test_control_held33_073_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel swam trace summary')))

    def test_control_held33_074_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel rang trace summary')))

    def test_control_held33_075_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wove trace summary')))

    def test_control_held33_076_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tore trace summary')))

    def test_control_held33_077_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wore trace summary')))

    def test_control_held33_078_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋈ trace summary')))

    def test_control_held33_079_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋊ trace summary')))

    def test_control_held33_080_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋋ trace summary')))

    def test_control_held33_081_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋌ trace summary')))

    def test_control_held33_082_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⟦panel⟧ trace summary')))

    def test_control_held33_083_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ❴panel❵ trace summary')))

    def test_control_held33_084_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ‹panel› trace summary')))

    def test_control_held33_085_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦋panel⦌ trace summary')))

    def test_control_held33_086_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⟨panel⟩ trace summary')))

    def test_control_held33_087_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger 《panel》 trace summary')))

    def test_control_held33_088_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃑ trace summary')))

    def test_control_held33_089_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃖ trace summary')))

    def test_control_held33_090_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃗ trace summary')))

    def test_control_held33_091_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃛ trace summary')))

    def test_control_held33_092_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃡ trace summary')))

    def test_control_held33_093_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃥ trace summary')))

    def test_control_held33_094_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃐ trace summary')))

    def test_control_held33_095_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃒ trace summary')))

    def test_control_held33_096_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃢ trace summary')))

    def test_control_held33_097_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ❨panel❩ trace summary')))

    def test_control_held33_098_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ❪panel❫ trace summary')))

    def test_control_held33_099_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ❬panel❭ trace summary')))

    def test_control_held33_100_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ❮panel❯ trace summary')))

    def test_control_held33_101_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ❰panel❱ trace summary')))

    def test_control_held33_102_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ❴panel❵ trace summary')))

    def test_control_held33_103_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦇panel⦈ trace summary')))

    def test_control_held33_104_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦉panel⦊ trace summary')))

    def test_control_held33_105_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦋panel⦌ trace summary')))

    def test_control_held33_106_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦍panel⦎ trace summary')))

    def test_control_held33_107_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦏panel⦐ trace summary')))

    def test_control_held33_108_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦑panel⦒ trace summary')))

    def test_control_held33_109_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦓panel⦔ trace summary')))

    def test_control_held33_110_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦕panel⦖ trace summary')))

    def test_control_held33_111_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦗panel⦘ trace summary')))

    def test_control_held33_112_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧼panel⧽ trace summary')))

    def test_control_held33_113_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ｟panel｠ trace summary')))

    def test_control_held33_114_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger 〚panel〛 trace summary')))

    def test_control_held33_115_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger 〔panel〕 trace summary')))

    def test_control_held33_116_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger 〖panel〗 trace summary')))

    def test_control_held33_117_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger 〘panel〙 trace summary')))

    def test_control_held33_118_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger «panel» trace summary')))

    def test_control_held33_119_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ‹panel› trace summary')))

    def test_control_held33_120_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger 〈panel〉 trace summary')))

    def test_control_held33_121_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger 《panel》 trace summary')))

    def test_control_held33_122_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger “panel” trace summary')))

    def test_control_held33_123_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ‘panel’ trace summary')))

    def test_control_held33_124_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸠panel⸡ trace summary')))

    def test_control_held33_125_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌈panel⌉ trace summary')))

    def test_control_held33_126_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌊panel⌋ trace summary')))

    def test_control_held33_127_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⟅panel⟆ trace summary')))

    def test_control_held33_128_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \\ trace summary')))

    def test_control_held33_129_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger || trace summary')))

    def test_control_held33_130_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger * trace summary')))

    def test_control_held33_131_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace board gate summary')))

    def test_control_held33_132_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace board gate summary')))

    def test_control_held33_133_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yank trace board gate summary')))

    def test_control_held33_134_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bore trace board gate summary')))

    def test_control_held33_135_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk rode summary board gate trace')))

    def test_control_held33_136_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fled trace board gate summary')))

    def test_control_held33_137_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sought trace board gate summary')))

    def test_control_held33_138_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel paid trace board gate summary')))

    def test_control_held33_139_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chose trace board gate summary')))

    def test_control_held33_140_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel reviewed trace board gate summary')))

    def test_control_held33_141_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel logs trace board gate summary')))

    def test_control_held33_142_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel bore traceboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held33_143_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel chose traceboardgatereviewannexpanelsummary')))

    def test_control_held33_144_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel reviewed the traceboardgatereviewannexsummary')))

    # ------------------------------------------------------
    # Governed closings of R16-33-02, standing governed
    # beside their counted siblings.
    # ------------------------------------------------------

    def test_control_governed_00_governed(self):
        self._candidate(_bad('Trace summary'), _read('Trace summary'))

    def test_control_governed_01_governed(self):
        self._candidate(_bad('Summary trace'), _read('Summary trace'))

    def test_control_governed_02_governed(self):
        self._candidate(_bad('Tracesummary'), _read('Tracesummary'))

    def test_control_governed_03_governed(self):
        self._candidate(_bad('Boardtracesummary'), _read('Boardtracesummary'))

    def test_control_governed_04_governed(self):
        self._candidate(_bad('Trace board summary'), _read('Trace board summary'))

    def test_control_governed_05_governed(self):
        self._candidate(_bad('Trace board gate summary'), _read('Trace board gate summary'))

    def test_control_governed_06_governed(self):
        self._candidate(_bad('Alpha beta gamma delta epsilon trace summary'), _read('Alpha beta gamma delta epsilon trace summary'))

    def test_control_governed_07_governed(self):
        self._candidate(_bad("Round's trace summary"), _read("Round's trace summary"))

    # ------------------------------------------------------
    # Held governed controls of R16-33-01 named in the
    # register, standing governed in the cure.
    # ------------------------------------------------------

    def test_control_underheld_000_governed(self):
        self._candidate(_bad('Hymnaltally'), _read('Hymnaltally'))

    def test_control_underheld_001_governed(self):
        self._candidate(_bad('Missaltally'), _read('Missaltally'))

    def test_control_underheld_002_governed(self):
        self._candidate(_bad('Psaltertally'), _read('Psaltertally'))

    def test_control_underheld_003_governed(self):
        self._candidate(_bad('Almanactally'), _read('Almanactally'))

    def test_control_underheld_004_governed(self):
        self._candidate(_bad('Almanacstallies'), _read('Almanacstallies'))

    def test_control_underheld_005_governed(self):
        self._candidate(_bad('Gazettetally'), _read('Gazettetally'))

    def test_control_underheld_006_governed(self):
        self._candidate(_bad('Gazettestallies'), _read('Gazettestallies'))

    def test_control_underheld_007_governed(self):
        self._candidate(_bad('Breviarytally'), _read('Breviarytally'))

    def test_control_underheld_008_governed(self):
        self._candidate(_bad('Notebookstallies'), _read('Notebookstallies'))

    def test_control_underheld_009_governed(self):
        self._candidate(_bad('Boardhymnaltally'), _read('Boardhymnaltally'))

    def test_control_underheld_010_governed(self):
        self._candidate(_bad('Gatepsaltertally'), _read('Gatepsaltertally'))

    def test_control_underheld_011_governed(self):
        self._candidate(_bad('Boardalmanactally'), _read('Boardalmanactally'))

    def test_control_underheld_012_governed(self):
        self._candidate(_bad('Reviewgazettetally'), _read('Reviewgazettetally'))

    def test_control_underheld_013_governed(self):
        self._candidate(_bad('Boardbreviarytally'), _read('Boardbreviarytally'))

    def test_control_underheld_014_governed(self):
        self._candidate(_bad('Boardhymnaltallye'), _read('Boardhymnaltallye'))

    def test_control_underheld_015_governed(self):
        self._candidate(_bad('Boardmissaltalliez'), _read('Boardmissaltalliez'))

    def test_control_underheld_016_governed(self):
        self._candidate(_bad('Gatepsaltertallye'), _read('Gatepsaltertallye'))

    def test_control_underheld_017_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseseseses'))

    def test_control_underheld_018_governed(self):
        self._candidate(_bad('Trace summarisingeseseseseseseseseseseseseses'), _read('Trace summarisingeseseseseseseseseseseseseses'))

    def test_control_underheld_019_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseseses'))

    def test_control_underheld_020_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseseses'))

    def test_control_underheld_021_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseseses'))

    def test_control_underheld_022_governed(self):
        self._candidate(_bad('Trace summaryeseseseseseseseseseseseseseses'), _read('Trace summaryeseseseseseseseseseseseseseses'))

    def test_control_underheld_023_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseseses'))

    def test_control_underheld_024_governed(self):
        self._candidate(_bad('Tracessummaryeseseseseseseseseseseseseseses'), _read('Tracessummaryeseseseseseseseseseseseseseses'))

    def test_control_underheld_025_governed(self):
        self._candidate(_bad('Board Ʌally'), _read('Board Ʌally'))

    def test_control_underheld_026_governed(self):
        self._candidate(_bad('Board Ɇally'), _read('Board Ɇally'))

    def test_control_underheld_027_governed(self):
        self._candidate(_bad('Board ɇally'), _read('Board ɇally'))

    def test_control_underheld_028_governed(self):
        self._candidate(_bad('Board ɓally'), _read('Board ɓally'))

    def test_control_underheld_029_governed(self):
        self._candidate(_bad('Board ɔally'), _read('Board ɔally'))

    def test_control_underheld_030_governed(self):
        self._candidate(_bad('Board ɕally'), _read('Board ɕally'))

    def test_control_underheld_031_governed(self):
        self._candidate(_bad('Board ɖally'), _read('Board ɖally'))

    def test_control_underheld_032_governed(self):
        self._candidate(_bad('Board ɗally'), _read('Board ɗally'))

    def test_control_underheld_033_governed(self):
        self._candidate(_bad('Board əally'), _read('Board əally'))

    def test_control_underheld_034_governed(self):
        self._candidate(_bad('Board ɛally'), _read('Board ɛally'))

    def test_control_underheld_035_governed(self):
        self._candidate(_bad('Board ɠally'), _read('Board ɠally'))

    def test_control_underheld_036_governed(self):
        self._candidate(_bad('Board ɢally'), _read('Board ɢally'))

    def test_control_underheld_037_governed(self):
        self._candidate(_bad('Board ɣally'), _read('Board ɣally'))

    def test_control_underheld_038_governed(self):
        self._candidate(_bad('Board ɧally'), _read('Board ɧally'))

    def test_control_underheld_039_governed(self):
        self._candidate(_bad('Board ɨally'), _read('Board ɨally'))

    def test_control_underheld_040_governed(self):
        self._candidate(_bad('Board taɆly'), _read('Board taɆly'))

    def test_control_underheld_041_governed(self):
        self._candidate(_bad('Board taɇly'), _read('Board taɇly'))

    def test_control_underheld_042_governed(self):
        self._candidate(_bad('Board taɔly'), _read('Board taɔly'))

    def test_control_underheld_043_governed(self):
        self._candidate(_bad('Board taɕly'), _read('Board taɕly'))

    def test_control_underheld_044_governed(self):
        self._candidate(_bad('Board taɖly'), _read('Board taɖly'))

    def test_control_underheld_045_governed(self):
        self._candidate(_bad('Board taɗly'), _read('Board taɗly'))

    def test_control_underheld_046_governed(self):
        self._candidate(_bad('Board taəly'), _read('Board taəly'))

    def test_control_underheld_047_governed(self):
        self._candidate(_bad('Board taɛly'), _read('Board taɛly'))

    def test_control_underheld_048_governed(self):
        self._candidate(_bad('Board taɠly'), _read('Board taɠly'))

    def test_control_underheld_049_governed(self):
        self._candidate(_bad('Board taɢly'), _read('Board taɢly'))

    def test_control_underheld_050_governed(self):
        self._candidate(_bad('Board taɣly'), _read('Board taɣly'))

    def test_control_underheld_051_governed(self):
        self._candidate(_bad('Board taɨly'), _read('Board taɨly'))

    def test_control_underheld_052_governed(self):
        self._candidate(_bad('Trace sɄmmarise'), _read('Trace sɄmmarise'))

    def test_control_underheld_053_governed(self):
        self._candidate(_bad('Trace sɆmmarise'), _read('Trace sɆmmarise'))

    def test_control_underheld_054_governed(self):
        self._candidate(_bad('Trace sɇmmarise'), _read('Trace sɇmmarise'))

    def test_control_underheld_055_governed(self):
        self._candidate(_bad('Trace sɔmmarise'), _read('Trace sɔmmarise'))

    def test_control_underheld_056_governed(self):
        self._candidate(_bad('Trace sɕmmarise'), _read('Trace sɕmmarise'))

    def test_control_underheld_057_governed(self):
        self._candidate(_bad('Trace sɖmmarise'), _read('Trace sɖmmarise'))

    def test_control_underheld_058_governed(self):
        self._candidate(_bad('Trace sɗmmarise'), _read('Trace sɗmmarise'))

    def test_control_underheld_059_governed(self):
        self._candidate(_bad('Trace səmmarise'), _read('Trace səmmarise'))

    def test_control_underheld_060_governed(self):
        self._candidate(_bad('Trace sɛmmarise'), _read('Trace sɛmmarise'))

    def test_control_underheld_061_governed(self):
        self._candidate(_bad('Trace sɠmmarise'), _read('Trace sɠmmarise'))

    def test_control_underheld_062_governed(self):
        self._candidate(_bad('Trace sɢmmarise'), _read('Trace sɢmmarise'))

    def test_control_underheld_063_governed(self):
        self._candidate(_bad('Trace sɣmmarise'), _read('Trace sɣmmarise'))

    def test_control_underheld_064_governed(self):
        self._candidate(_bad('Trace sɤmmarise'), _read('Trace sɤmmarise'))

    def test_control_underheld_065_governed(self):
        self._candidate(_bad('Trace sɨmmarise'), _read('Trace sɨmmarise'))

    def test_control_underheld_066_governed(self):
        self._candidate(_bad('Trace sumɆarise'), _read('Trace sumɆarise'))

    def test_control_underheld_067_governed(self):
        self._candidate(_bad('Trace sumɇarise'), _read('Trace sumɇarise'))

    def test_control_underheld_068_governed(self):
        self._candidate(_bad('Trace sumɔarise'), _read('Trace sumɔarise'))

    def test_control_underheld_069_governed(self):
        self._candidate(_bad('Trace sumɕarise'), _read('Trace sumɕarise'))

    def test_control_underheld_070_governed(self):
        self._candidate(_bad('Trace sumɖarise'), _read('Trace sumɖarise'))

    def test_control_underheld_071_governed(self):
        self._candidate(_bad('Trace sumɗarise'), _read('Trace sumɗarise'))

    def test_control_underheld_072_governed(self):
        self._candidate(_bad('Trace suməarise'), _read('Trace suməarise'))

    def test_control_underheld_073_governed(self):
        self._candidate(_bad('Trace sumɛarise'), _read('Trace sumɛarise'))

    def test_control_underheld_074_governed(self):
        self._candidate(_bad('Trace sumɠarise'), _read('Trace sumɠarise'))

    def test_control_underheld_075_governed(self):
        self._candidate(_bad('Trace sumɢarise'), _read('Trace sumɢarise'))

    def test_control_underheld_076_governed(self):
        self._candidate(_bad('Trace sumɣarise'), _read('Trace sumɣarise'))

    def test_control_underheld_077_governed(self):
        self._candidate(_bad('Trace sumɨarise'), _read('Trace sumɨarise'))

    def test_control_underheld_078_governed(self):
        self._candidate(_bad('Trace summariɆe'), _read('Trace summariɆe'))

    def test_control_underheld_079_governed(self):
        self._candidate(_bad('Trace summariɇe'), _read('Trace summariɇe'))

    def test_control_underheld_080_governed(self):
        self._candidate(_bad('Trace summariɊe'), _read('Trace summariɊe'))

    def test_control_underheld_081_governed(self):
        self._candidate(_bad('Trace summariɋe'), _read('Trace summariɋe'))

    def test_control_underheld_082_governed(self):
        self._candidate(_bad('Trace summariɔe'), _read('Trace summariɔe'))

    def test_control_underheld_083_governed(self):
        self._candidate(_bad('Trace summariɕe'), _read('Trace summariɕe'))

    def test_control_underheld_084_governed(self):
        self._candidate(_bad('Trace summariɖe'), _read('Trace summariɖe'))

    def test_control_underheld_085_governed(self):
        self._candidate(_bad('Trace summariɗe'), _read('Trace summariɗe'))

    def test_control_underheld_086_governed(self):
        self._candidate(_bad('Trace summariəe'), _read('Trace summariəe'))

    def test_control_underheld_087_governed(self):
        self._candidate(_bad('Trace summariɛe'), _read('Trace summariɛe'))

    def test_control_underheld_088_governed(self):
        self._candidate(_bad('Trace summariɠe'), _read('Trace summariɠe'))

    def test_control_underheld_089_governed(self):
        self._candidate(_bad('Trace summariɢe'), _read('Trace summariɢe'))

    def test_control_underheld_090_governed(self):
        self._candidate(_bad('Trace summariɣe'), _read('Trace summariɣe'))

    def test_control_underheld_091_governed(self):
        self._candidate(_bad('Trace summariɨe'), _read('Trace summariɨe'))

    def test_control_underheld_092_governed(self):
        self._candidate(_bad('Trace summarisɅ'), _read('Trace summarisɅ'))

    def test_control_underheld_093_governed(self):
        self._candidate(_bad('Trace summarisɆ'), _read('Trace summarisɆ'))

    def test_control_underheld_094_governed(self):
        self._candidate(_bad('Trace summarisɇ'), _read('Trace summarisɇ'))

    def test_control_underheld_095_governed(self):
        self._candidate(_bad('Trace summarisɔ'), _read('Trace summarisɔ'))

    def test_control_underheld_096_governed(self):
        self._candidate(_bad('Trace summarisɕ'), _read('Trace summarisɕ'))

    def test_control_underheld_097_governed(self):
        self._candidate(_bad('Trace summarisɖ'), _read('Trace summarisɖ'))

    def test_control_underheld_098_governed(self):
        self._candidate(_bad('Trace summarisɗ'), _read('Trace summarisɗ'))

    def test_control_underheld_099_governed(self):
        self._candidate(_bad('Trace summarisɘ'), _read('Trace summarisɘ'))

    def test_control_underheld_100_governed(self):
        self._candidate(_bad('Trace summarisə'), _read('Trace summarisə'))

    def test_control_underheld_101_governed(self):
        self._candidate(_bad('Trace summarisɛ'), _read('Trace summarisɛ'))

    def test_control_underheld_102_governed(self):
        self._candidate(_bad('Trace summarisɜ'), _read('Trace summarisɜ'))

    def test_control_underheld_103_governed(self):
        self._candidate(_bad('Trace summarisɞ'), _read('Trace summarisɞ'))

    def test_control_underheld_104_governed(self):
        self._candidate(_bad('Trace summarisɠ'), _read('Trace summarisɠ'))

    def test_control_underheld_105_governed(self):
        self._candidate(_bad('Trace summarisɢ'), _read('Trace summarisɢ'))

    def test_control_underheld_106_governed(self):
        self._candidate(_bad('Trace summarisɣ'), _read('Trace summarisɣ'))

    def test_control_underheld_107_governed(self):
        self._candidate(_bad('Trace summarisɨ'), _read('Trace summarisɨ'))

    def test_control_underheld_108_governed(self):
        self._candidate(_bad('Songbooktally'), _read('Songbooktally'))

    def test_control_underheld_109_governed(self):
        self._candidate(_bad('Hymnbooktally'), _read('Hymnbooktally'))

    def test_control_underheld_110_governed(self):
        self._candidate(_bad('Prayerbooktally'), _read('Prayerbooktally'))

    def test_control_underheld_111_governed(self):
        self._candidate(_bad('Sermontally'), _read('Sermontally'))

    def test_control_underheld_112_governed(self):
        self._candidate(_bad('Memoirtally'), _read('Memoirtally'))

    def test_control_underheld_113_governed(self):
        self._candidate(_bad('Songbookstallies'), _read('Songbookstallies'))

    def test_control_underheld_114_governed(self):
        self._candidate(_bad('Boarddictionarytally'), _read('Boarddictionarytally'))

    def test_control_underheld_115_governed(self):
        self._candidate(_bad('Board ǒally'), _read('Board ǒally'))

    def test_control_underheld_116_governed(self):
        self._candidate(_bad('Board ǔally'), _read('Board ǔally'))

    def test_control_underheld_117_governed(self):
        self._candidate(_bad('Board ǖally'), _read('Board ǖally'))

    def test_control_underheld_118_governed(self):
        self._candidate(_bad('Board ǘally'), _read('Board ǘally'))

    def test_control_underheld_119_governed(self):
        self._candidate(_bad('Board ǚally'), _read('Board ǚally'))

    def test_control_underheld_120_governed(self):
        self._candidate(_bad('Board ǜally'), _read('Board ǜally'))

    def test_control_underheld_121_governed(self):
        self._candidate(_bad('Board Ǫally'), _read('Board Ǫally'))

    def test_control_underheld_122_governed(self):
        self._candidate(_bad('Board Ǭally'), _read('Board Ǭally'))

    def test_control_underheld_123_governed(self):
        self._candidate(_bad('Board Ȍally'), _read('Board Ȍally'))

    def test_control_underheld_124_governed(self):
        self._candidate(_bad('Board Ȏally'), _read('Board Ȏally'))

    def test_control_underheld_125_governed(self):
        self._candidate(_bad('Board Ȕally'), _read('Board Ȕally'))

    def test_control_underheld_126_governed(self):
        self._candidate(_bad('Board Ȗally'), _read('Board Ȗally'))

    def test_control_underheld_127_governed(self):
        self._candidate(_bad('Board Ƞally'), _read('Board Ƞally'))

    def test_control_underheld_128_governed(self):
        self._candidate(_bad('Board Ȫally'), _read('Board Ȫally'))

    def test_control_underheld_129_governed(self):
        self._candidate(_bad('Board Ȱally'), _read('Board Ȱally'))

    def test_control_underheld_130_governed(self):
        self._candidate(_bad('Board ɀally'), _read('Board ɀally'))

    def test_control_underheld_131_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary'))

    def test_control_underheld_132_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannextrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannextrace'))

    def test_control_underheld_133_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary'))

    def test_control_underheld_134_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate summary'))

    def test_control_underheld_135_governed(self):
        self._candidate(_bad('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate summary'), _read('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate summary'))

    def test_control_underheld_136_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate trace'))

    def test_control_underheld_137_governed(self):
        self._candidate(_bad('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate trace'), _read('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate trace'))

    def test_control_underheld_138_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate for step 2'))

