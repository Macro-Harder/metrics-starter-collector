"""Step 16 fix pass 35 unit 2 tests: the Q-4 closing unit.

Pinning tests for register item R16-35-01 (Medium,
B35-C01 and B35-B01) of Step 16 round 35. The
governing rule of the pass, in its extended form: a
piece not read in full, for whatever reason, is not
read, and its converse: a piece that is no feeder
flips nothing.

R16-35-01: malformed tally statement heads standing
unread past the widened boundary of fix pass 34, on
the counted pattern head agnosticism ground alone:
the pattern standing counted over a plain whole word
pattern, so a malformed head whose counted sibling
counts stands missing in the row although it stands
as a feeder statement in a form the row cannot parse.
Two hundred and thirty six distinct alone forms stand
driven in ten subfamilies: (a) tally forms fused
behind record words no widening has named and behind
the plurals of record words in the same position,
twenty two forms; (b) composite openings built on
those forms, nine forms; (c) a variant spelling in
that composite opening position built on those words,
three forms; (d) the variant spellings past the
widened variant sets of one hundred and twelve and one
hundred and fifteen, eighteen forms; (e) the summary
word in further forms at the seventeenth and
eighteenth es repetitions of its families, seven
forms; (f) the fused closings built on those forms,
four forms; (g) the fused closings with twenty two
governed words fused between the closing words, three
forms; (h) the inserted closings with twenty five
words of subject between in their wide, middle swap
and full swap shapes in both directions, six forms;
(i) the for step closing with twenty five words of
subject between, one form; and (j) further Latin and
kindred letters past the widened fold set, each
standing in a position the folding does not read, one
hundred and sixty three forms, the correctness forms
of that subfamily standing in the template and
codepoint form that paper states, at the positions
and codepoints the register names, drawn from the
forty letter pool U+0289 to U+02B0, and the breaker
forms standing in the words the breaker paper names.
The fifty seven underreach assertions of the round 35
breaker exhibit stand adopted in this module: the
fifty three alone form assertions of B35-B01 stand
among the defect tests of the subfamilies above in
their driven words, and the beside assertions, the
gate ruling assertion and the code level assertion of
that exhibit stand as defect tests here in the forms
the exhibit names them, in the exhibit test names
themselves. The defect stands bounded in the open by
its held controls: every form of R16-35-02 standing
missing, every held form of that item standing missing
in its recorded form, every governed closing of that
item standing governed, and on the underreach side the
governed neighbours of both papers standing governed,
the governed candidates of subfamily (a) of the
correctness paper standing governed through the
governed stems and blocks at the close of their fused
forms, the governed variant composite opening of that
paper standing governed, the eighty three governed
letter forms of subfamily (j) of the correctness paper
standing governed at their positions, the candidate
record words of the breaker paper standing governed in
their probed forms, Songbooktally and Songbookstallies
standing governed in their present standings,
Boarddictionarytally standing governed through the
further position limb, the widest form of every
summary family standing governed in the widened
enumeration at its family position, the candidate
letters of the breaker paper standing folded to their
words, the fused and inserted closings standing at
their governed counts, the twenty one word fused
between closing, the twenty four word forward and
reversed inserted closings and the twenty four word
for step closing standing governed, and the plain
Latin spellings standing at their standings. Locus:
derivation_core.py, _tally_statement_head and its
standing helpers and constants. The cure these tests
pin widens what a malformed tally statement head is in
standing: the governed fused prefix set widened by the
record words and plural stems of this round, the
variant sets widened by the spellings of this round,
the summary word set widened by the further forms of
this round, the fused between reach widened to twenty
two governed words, the inserted closings standing at
twenty five words forward, twenty five words reversed
and twenty five words in the for step form under the
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


class TestStep16Fix35Unit2(FixtureTestCase):

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
    # Defect forms of R16-35-01, subfamily (a):
    # fused record words and the plurals of record words.
    # ------------------------------------------------------

    def test_r16_35_01_a_00_governed(self):
        self._candidate(_bad('Anthembookstallies'), _read('Anthembookstallies'))

    def test_r16_35_01_a_01_governed(self):
        self._candidate(_bad('Choirbookstallies'), _read('Choirbookstallies'))

    def test_r16_35_01_a_02_governed(self):
        self._candidate(_bad('Psalmbookstallies'), _read('Psalmbookstallies'))

    def test_r16_35_01_a_03_governed(self):
        self._candidate(_bad('Chantbookstallies'), _read('Chantbookstallies'))

    def test_r16_35_01_a_04_governed(self):
        self._candidate(_bad('Versebookstallies'), _read('Versebookstallies'))

    def test_r16_35_01_a_05_governed(self):
        self._candidate(_bad('Ledgerbookstallies'), _read('Ledgerbookstallies'))

    def test_r16_35_01_a_06_governed(self):
        self._candidate(_bad('Recordbookstallies'), _read('Recordbookstallies'))

    def test_r16_35_01_a_07_governed(self):
        self._candidate(_bad('Matinstally'), _read('Matinstally'))

    def test_r16_35_01_a_08_governed(self):
        self._candidate(_bad('Matinstallies'), _read('Matinstallies'))

    def test_r16_35_01_a_09_governed(self):
        self._candidate(_bad('Complinetally'), _read('Complinetally'))

    def test_r16_35_01_a_10_governed(self):
        self._candidate(_bad('Complinestallies'), _read('Complinestallies'))

    def test_r16_35_01_a_11_governed(self):
        self._candidate(_bad('Antiphonarytally'), _read('Antiphonarytally'))

    def test_r16_35_01_a_12_governed(self):
        self._candidate(_bad('Lectiontally'), _read('Lectiontally'))

    def test_r16_35_01_a_13_governed(self):
        self._candidate(_bad('Pericopetally'), _read('Pericopetally'))

    def test_r16_35_01_a_14_governed(self):
        self._candidate(_bad('Canontally'), _read('Canontally'))

    def test_r16_35_01_a_15_governed(self):
        self._candidate(_bad('Tropariontally'), _read('Tropariontally'))

    def test_r16_35_01_a_16_governed(self):
        self._candidate(_bad('Antiphonariestallies'), _read('Antiphonariestallies'))

    def test_r16_35_01_a_17_governed(self):
        self._candidate(_bad('Lectionstallies'), _read('Lectionstallies'))

    def test_r16_35_01_a_18_governed(self):
        self._candidate(_bad('Canonstallies'), _read('Canonstallies'))

    def test_r16_35_01_a_19_governed(self):
        self._candidate(_bad('Pericopestallies'), _read('Pericopestallies'))

    def test_r16_35_01_a_20_governed(self):
        self._candidate(_bad('Missalettestallies'), _read('Missalettestallies'))

    def test_r16_35_01_a_21_governed(self):
        self._candidate(_bad('Hymnariestallies'), _read('Hymnariestallies'))

    # ------------------------------------------------------
    # Defect forms of R16-35-01, subfamily (b):
    # composite openings built on those forms.
    # ------------------------------------------------------

    def test_r16_35_01_b_00_governed(self):
        self._candidate(_bad('Boardanthembookstallies'), _read('Boardanthembookstallies'))

    def test_r16_35_01_b_01_governed(self):
        self._candidate(_bad('Boardmatinstally'), _read('Boardmatinstally'))

    def test_r16_35_01_b_02_governed(self):
        self._candidate(_bad('Boardledgerbookstallies'), _read('Boardledgerbookstallies'))

    def test_r16_35_01_b_03_governed(self):
        self._candidate(_bad('Boardlectiontally'), _read('Boardlectiontally'))

    def test_r16_35_01_b_04_governed(self):
        self._candidate(_bad('Gatecanontally'), _read('Gatecanontally'))

    def test_r16_35_01_b_05_governed(self):
        self._candidate(_bad('Reviewpericopetally'), _read('Reviewpericopetally'))

    def test_r16_35_01_b_06_governed(self):
        self._candidate(_bad('Boardantiphonarytally'), _read('Boardantiphonarytally'))

    def test_r16_35_01_b_07_governed(self):
        self._candidate(_bad('Boardlectionstallies'), _read('Boardlectionstallies'))

    def test_r16_35_01_b_08_governed(self):
        self._candidate(_bad('Gatecanonstallies'), _read('Gatecanonstallies'))

    # ------------------------------------------------------
    # Defect forms of R16-35-01, subfamily (c):
    # a variant spelling in that composite opening position.
    # ------------------------------------------------------

    def test_r16_35_01_c_00_governed(self):
        self._candidate(_bad('Boardmatinstallye'), _read('Boardmatinstallye'))

    def test_r16_35_01_c_01_governed(self):
        self._candidate(_bad('Boardlectiontallye'), _read('Boardlectiontallye'))

    def test_r16_35_01_c_02_governed(self):
        self._candidate(_bad('Gatecanontalliez'), _read('Gatecanontalliez'))

    # ------------------------------------------------------
    # Defect forms of R16-35-01, subfamily (d):
    # the variant spellings past the widened variant sets.
    # ------------------------------------------------------

    def test_r16_35_01_d_00_governed(self):
        self._candidate(_bad('Tallya12'), _read('Tallya12'))

    def test_r16_35_01_d_01_governed(self):
        self._candidate(_bad('Tallyo11'), _read('Tallyo11'))

    def test_r16_35_01_d_02_governed(self):
        self._candidate(_bad('Tallyu11'), _read('Tallyu11'))

    def test_r16_35_01_d_03_governed(self):
        self._candidate(_bad('Tallyai11'), _read('Tallyai11'))

    def test_r16_35_01_d_04_governed(self):
        self._candidate(_bad('Tallyez10'), _read('Tallyez10'))

    def test_r16_35_01_d_05_governed(self):
        self._candidate(_bad('Tallyaz10'), _read('Tallyaz10'))

    def test_r16_35_01_d_06_governed(self):
        self._candidate(_bad('Tallyeo13'), _read('Tallyeo13'))

    def test_r16_35_01_d_07_governed(self):
        self._candidate(_bad('Tallyia5'), _read('Tallyia5'))

    def test_r16_35_01_d_08_governed(self):
        self._candidate(_bad('Tallye11'), _read('Tallye11'))

    def test_r16_35_01_d_09_governed(self):
        self._candidate(_bad('Boardtallya12'), _read('Boardtallya12'))

    def test_r16_35_01_d_10_governed(self):
        self._candidate(_bad('Boardtallyo11'), _read('Boardtallyo11'))

    def test_r16_35_01_d_11_governed(self):
        self._candidate(_bad('Boardtallyu11'), _read('Boardtallyu11'))

    def test_r16_35_01_d_12_governed(self):
        self._candidate(_bad('Boardtallyai11'), _read('Boardtallyai11'))

    def test_r16_35_01_d_13_governed(self):
        self._candidate(_bad('Boardtallyez10'), _read('Boardtallyez10'))

    def test_r16_35_01_d_14_governed(self):
        self._candidate(_bad('Boardtallyaz10'), _read('Boardtallyaz10'))

    def test_r16_35_01_d_15_governed(self):
        self._candidate(_bad('Boardtallyeo13'), _read('Boardtallyeo13'))

    def test_r16_35_01_d_16_governed(self):
        self._candidate(_bad('Boardtallyia5'), _read('Boardtallyia5'))

    def test_r16_35_01_d_17_governed(self):
        self._candidate(_bad('Boardtallye11'), _read('Boardtallye11'))

    # ------------------------------------------------------
    # Defect forms of R16-35-01, subfamily (e):
    # the summary word in further forms.
    # ------------------------------------------------------

    def test_r16_35_01_e_00_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseseseseseseses'))

    def test_r16_35_01_e_01_governed(self):
        self._candidate(_bad('Trace summarisingeseseseseseseseseseseseseseseseses'), _read('Trace summarisingeseseseseseseseseseseseseseseseses'))

    def test_r16_35_01_e_02_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseseseseseses'))

    def test_r16_35_01_e_03_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseseseseseses'))

    def test_r16_35_01_e_04_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseseseseseses'))

    def test_r16_35_01_e_05_governed(self):
        self._candidate(_bad('Trace summaryeseseseseseseseseseseseseseseseseses'), _read('Trace summaryeseseseseseseseseseseseseseseseseses'))

    def test_r16_35_01_e_06_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseseseseseses'))

    # ------------------------------------------------------
    # Defect forms of R16-35-01, subfamily (f):
    # the fused closings built on those forms.
    # ------------------------------------------------------

    def test_r16_35_01_f_00_governed(self):
        self._candidate(_bad('Boardtracesummarisereseseseseseseseseseseseseseseseses'), _read('Boardtracesummarisereseseseseseseseseseseseseseseseses'))

    def test_r16_35_01_f_01_governed(self):
        self._candidate(_bad('Tracessummarieseseseseseseseseseseseseseseseseses'), _read('Tracessummarieseseseseseseseseseseseseseseseseses'))

    def test_r16_35_01_f_02_governed(self):
        self._candidate(_bad('Boardtracesummarisedeseseseseseseseseseseseseseseseses'), _read('Boardtracesummarisedeseseseseseseseseseseseseseseseses'))

    def test_r16_35_01_f_03_governed(self):
        self._candidate(_bad('Tracessummaryeseseseseseseseseseseseseseseseseses'), _read('Tracessummaryeseseseseseseseseseseseseseseseseses'))

    # ------------------------------------------------------
    # Defect forms of R16-35-01, subfamily (g):
    # the fused closings with twenty two governed words fused between.
    # ------------------------------------------------------

    def test_r16_35_01_g_00_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary'))

    def test_r16_35_01_g_01_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatetrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatetrace'))

    def test_r16_35_01_g_02_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary'))

    # ------------------------------------------------------
    # Defect forms of R16-35-01, subfamily (h):
    # the inserted closings with twenty five words of subject between.
    # ------------------------------------------------------

    def test_r16_35_01_h_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel summary'))

    def test_r16_35_01_h_01_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex panel summary'), _read('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex panel summary'))

    def test_r16_35_01_h_02_governed(self):
        self._candidate(_bad('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel summary'), _read('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel summary'))

    def test_r16_35_01_h_03_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel trace'))

    def test_r16_35_01_h_04_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex panel trace'), _read('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex panel trace'))

    def test_r16_35_01_h_05_governed(self):
        self._candidate(_bad('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel trace'), _read('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel trace'))

    # ------------------------------------------------------
    # Defect forms of R16-35-01, subfamily (i):
    # the for step closing with twenty five words of subject between.
    # ------------------------------------------------------

    def test_r16_35_01_i_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel for step 2'))

    # ------------------------------------------------------
    # Defect forms of R16-35-01, subfamily (j):
    # further letters past the widened fold set.
    # ------------------------------------------------------

    def test_r16_35_01_j_000_governed(self):
        self._candidate(_bad('Board ʎally'), _read('Board ʎally'))

    def test_r16_35_01_j_001_governed(self):
        self._candidate(_bad('Board ʏally'), _read('Board ʏally'))

    def test_r16_35_01_j_002_governed(self):
        self._candidate(_bad('Board ʑally'), _read('Board ʑally'))

    def test_r16_35_01_j_003_governed(self):
        self._candidate(_bad('Board ʓally'), _read('Board ʓally'))

    def test_r16_35_01_j_004_governed(self):
        self._candidate(_bad('Board ʗally'), _read('Board ʗally'))

    def test_r16_35_01_j_005_governed(self):
        self._candidate(_bad('Board ʜally'), _read('Board ʜally'))

    def test_r16_35_01_j_006_governed(self):
        self._candidate(_bad('Board ʝally'), _read('Board ʝally'))

    def test_r16_35_01_j_007_governed(self):
        self._candidate(_bad('Board ʟally'), _read('Board ʟally'))

    def test_r16_35_01_j_008_governed(self):
        self._candidate(_bad('Board ʤally'), _read('Board ʤally'))

    def test_r16_35_01_j_009_governed(self):
        self._candidate(_bad('Board ʥally'), _read('Board ʥally'))

    def test_r16_35_01_j_010_governed(self):
        self._candidate(_bad('Board ʩally'), _read('Board ʩally'))

    def test_r16_35_01_j_011_governed(self):
        self._candidate(_bad('Board ʫally'), _read('Board ʫally'))

    def test_r16_35_01_j_012_governed(self):
        self._candidate(_bad('Board ʬally'), _read('Board ʬally'))

    def test_r16_35_01_j_013_governed(self):
        self._candidate(_bad('Board ʮally'), _read('Board ʮally'))

    def test_r16_35_01_j_014_governed(self):
        self._candidate(_bad('Board ʯally'), _read('Board ʯally'))

    def test_r16_35_01_j_015_governed(self):
        self._candidate(_bad('Board ʰally'), _read('Board ʰally'))

    def test_r16_35_01_j_016_governed(self):
        self._candidate(_bad('Board taʍly'), _read('Board taʍly'))

    def test_r16_35_01_j_017_governed(self):
        self._candidate(_bad('Board taʏly'), _read('Board taʏly'))

    def test_r16_35_01_j_018_governed(self):
        self._candidate(_bad('Board taʐly'), _read('Board taʐly'))

    def test_r16_35_01_j_019_governed(self):
        self._candidate(_bad('Board taʑly'), _read('Board taʑly'))

    def test_r16_35_01_j_020_governed(self):
        self._candidate(_bad('Board taʓly'), _read('Board taʓly'))

    def test_r16_35_01_j_021_governed(self):
        self._candidate(_bad('Board taʔly'), _read('Board taʔly'))

    def test_r16_35_01_j_022_governed(self):
        self._candidate(_bad('Board taʖly'), _read('Board taʖly'))

    def test_r16_35_01_j_023_governed(self):
        self._candidate(_bad('Board taʗly'), _read('Board taʗly'))

    def test_r16_35_01_j_024_governed(self):
        self._candidate(_bad('Board taʙly'), _read('Board taʙly'))

    def test_r16_35_01_j_025_governed(self):
        self._candidate(_bad('Board taʚly'), _read('Board taʚly'))

    def test_r16_35_01_j_026_governed(self):
        self._candidate(_bad('Board taʛly'), _read('Board taʛly'))

    def test_r16_35_01_j_027_governed(self):
        self._candidate(_bad('Board taʜly'), _read('Board taʜly'))

    def test_r16_35_01_j_028_governed(self):
        self._candidate(_bad('Board taʝly'), _read('Board taʝly'))

    def test_r16_35_01_j_029_governed(self):
        self._candidate(_bad('Board taʠly'), _read('Board taʠly'))

    def test_r16_35_01_j_030_governed(self):
        self._candidate(_bad('Board taʡly'), _read('Board taʡly'))

    def test_r16_35_01_j_031_governed(self):
        self._candidate(_bad('Board taʢly'), _read('Board taʢly'))

    def test_r16_35_01_j_032_governed(self):
        self._candidate(_bad('Board taʣly'), _read('Board taʣly'))

    def test_r16_35_01_j_033_governed(self):
        self._candidate(_bad('Board taʤly'), _read('Board taʤly'))

    def test_r16_35_01_j_034_governed(self):
        self._candidate(_bad('Board taʥly'), _read('Board taʥly'))

    def test_r16_35_01_j_035_governed(self):
        self._candidate(_bad('Board taʦly'), _read('Board taʦly'))

    def test_r16_35_01_j_036_governed(self):
        self._candidate(_bad('Board taʨly'), _read('Board taʨly'))

    def test_r16_35_01_j_037_governed(self):
        self._candidate(_bad('Board taʩly'), _read('Board taʩly'))

    def test_r16_35_01_j_038_governed(self):
        self._candidate(_bad('Board taʪly'), _read('Board taʪly'))

    def test_r16_35_01_j_039_governed(self):
        self._candidate(_bad('Board taʫly'), _read('Board taʫly'))

    def test_r16_35_01_j_040_governed(self):
        self._candidate(_bad('Board taʬly'), _read('Board taʬly'))

    def test_r16_35_01_j_041_governed(self):
        self._candidate(_bad('Board taʭly'), _read('Board taʭly'))

    def test_r16_35_01_j_042_governed(self):
        self._candidate(_bad('Board taʮly'), _read('Board taʮly'))

    def test_r16_35_01_j_043_governed(self):
        self._candidate(_bad('Board taʯly'), _read('Board taʯly'))

    def test_r16_35_01_j_044_governed(self):
        self._candidate(_bad('Board taʰly'), _read('Board taʰly'))

    def test_r16_35_01_j_045_governed(self):
        self._candidate(_bad('Trace sʍmmarise'), _read('Trace sʍmmarise'))

    def test_r16_35_01_j_046_governed(self):
        self._candidate(_bad('Trace sʎmmarise'), _read('Trace sʎmmarise'))

    def test_r16_35_01_j_047_governed(self):
        self._candidate(_bad('Trace sʏmmarise'), _read('Trace sʏmmarise'))

    def test_r16_35_01_j_048_governed(self):
        self._candidate(_bad('Trace sʐmmarise'), _read('Trace sʐmmarise'))

    def test_r16_35_01_j_049_governed(self):
        self._candidate(_bad('Trace sʑmmarise'), _read('Trace sʑmmarise'))

    def test_r16_35_01_j_050_governed(self):
        self._candidate(_bad('Trace sʓmmarise'), _read('Trace sʓmmarise'))

    def test_r16_35_01_j_051_governed(self):
        self._candidate(_bad('Trace sʔmmarise'), _read('Trace sʔmmarise'))

    def test_r16_35_01_j_052_governed(self):
        self._candidate(_bad('Trace sʖmmarise'), _read('Trace sʖmmarise'))

    def test_r16_35_01_j_053_governed(self):
        self._candidate(_bad('Trace sʗmmarise'), _read('Trace sʗmmarise'))

    def test_r16_35_01_j_054_governed(self):
        self._candidate(_bad('Trace sʙmmarise'), _read('Trace sʙmmarise'))

    def test_r16_35_01_j_055_governed(self):
        self._candidate(_bad('Trace sʚmmarise'), _read('Trace sʚmmarise'))

    def test_r16_35_01_j_056_governed(self):
        self._candidate(_bad('Trace sʜmmarise'), _read('Trace sʜmmarise'))

    def test_r16_35_01_j_057_governed(self):
        self._candidate(_bad('Trace sʝmmarise'), _read('Trace sʝmmarise'))

    def test_r16_35_01_j_058_governed(self):
        self._candidate(_bad('Trace sʞmmarise'), _read('Trace sʞmmarise'))

    def test_r16_35_01_j_059_governed(self):
        self._candidate(_bad('Trace sʟmmarise'), _read('Trace sʟmmarise'))

    def test_r16_35_01_j_060_governed(self):
        self._candidate(_bad('Trace sʠmmarise'), _read('Trace sʠmmarise'))

    def test_r16_35_01_j_061_governed(self):
        self._candidate(_bad('Trace sʢmmarise'), _read('Trace sʢmmarise'))

    def test_r16_35_01_j_062_governed(self):
        self._candidate(_bad('Trace sʣmmarise'), _read('Trace sʣmmarise'))

    def test_r16_35_01_j_063_governed(self):
        self._candidate(_bad('Trace sʤmmarise'), _read('Trace sʤmmarise'))

    def test_r16_35_01_j_064_governed(self):
        self._candidate(_bad('Trace sʥmmarise'), _read('Trace sʥmmarise'))

    def test_r16_35_01_j_065_governed(self):
        self._candidate(_bad('Trace sʦmmarise'), _read('Trace sʦmmarise'))

    def test_r16_35_01_j_066_governed(self):
        self._candidate(_bad('Trace sʨmmarise'), _read('Trace sʨmmarise'))

    def test_r16_35_01_j_067_governed(self):
        self._candidate(_bad('Trace sʩmmarise'), _read('Trace sʩmmarise'))

    def test_r16_35_01_j_068_governed(self):
        self._candidate(_bad('Trace sʪmmarise'), _read('Trace sʪmmarise'))

    def test_r16_35_01_j_069_governed(self):
        self._candidate(_bad('Trace sʫmmarise'), _read('Trace sʫmmarise'))

    def test_r16_35_01_j_070_governed(self):
        self._candidate(_bad('Trace sʬmmarise'), _read('Trace sʬmmarise'))

    def test_r16_35_01_j_071_governed(self):
        self._candidate(_bad('Trace sʭmmarise'), _read('Trace sʭmmarise'))

    def test_r16_35_01_j_072_governed(self):
        self._candidate(_bad('Trace sʮmmarise'), _read('Trace sʮmmarise'))

    def test_r16_35_01_j_073_governed(self):
        self._candidate(_bad('Trace sʯmmarise'), _read('Trace sʯmmarise'))

    def test_r16_35_01_j_074_governed(self):
        self._candidate(_bad('Trace sʰmmarise'), _read('Trace sʰmmarise'))

    def test_r16_35_01_j_075_governed(self):
        self._candidate(_bad('Trace sumʍarise'), _read('Trace sumʍarise'))

    def test_r16_35_01_j_076_governed(self):
        self._candidate(_bad('Trace sumʎarise'), _read('Trace sumʎarise'))

    def test_r16_35_01_j_077_governed(self):
        self._candidate(_bad('Trace sumʏarise'), _read('Trace sumʏarise'))

    def test_r16_35_01_j_078_governed(self):
        self._candidate(_bad('Trace sumʐarise'), _read('Trace sumʐarise'))

    def test_r16_35_01_j_079_governed(self):
        self._candidate(_bad('Trace sumʑarise'), _read('Trace sumʑarise'))

    def test_r16_35_01_j_080_governed(self):
        self._candidate(_bad('Trace sumʓarise'), _read('Trace sumʓarise'))

    def test_r16_35_01_j_081_governed(self):
        self._candidate(_bad('Trace sumʔarise'), _read('Trace sumʔarise'))

    def test_r16_35_01_j_082_governed(self):
        self._candidate(_bad('Trace sumʖarise'), _read('Trace sumʖarise'))

    def test_r16_35_01_j_083_governed(self):
        self._candidate(_bad('Trace sumʗarise'), _read('Trace sumʗarise'))

    def test_r16_35_01_j_084_governed(self):
        self._candidate(_bad('Trace sumʙarise'), _read('Trace sumʙarise'))

    def test_r16_35_01_j_085_governed(self):
        self._candidate(_bad('Trace sumʚarise'), _read('Trace sumʚarise'))

    def test_r16_35_01_j_086_governed(self):
        self._candidate(_bad('Trace sumʛarise'), _read('Trace sumʛarise'))

    def test_r16_35_01_j_087_governed(self):
        self._candidate(_bad('Trace sumʜarise'), _read('Trace sumʜarise'))

    def test_r16_35_01_j_088_governed(self):
        self._candidate(_bad('Trace sumʝarise'), _read('Trace sumʝarise'))

    def test_r16_35_01_j_089_governed(self):
        self._candidate(_bad('Trace sumʞarise'), _read('Trace sumʞarise'))

    def test_r16_35_01_j_090_governed(self):
        self._candidate(_bad('Trace sumʟarise'), _read('Trace sumʟarise'))

    def test_r16_35_01_j_091_governed(self):
        self._candidate(_bad('Trace sumʠarise'), _read('Trace sumʠarise'))

    def test_r16_35_01_j_092_governed(self):
        self._candidate(_bad('Trace sumʡarise'), _read('Trace sumʡarise'))

    def test_r16_35_01_j_093_governed(self):
        self._candidate(_bad('Trace sumʢarise'), _read('Trace sumʢarise'))

    def test_r16_35_01_j_094_governed(self):
        self._candidate(_bad('Trace sumʣarise'), _read('Trace sumʣarise'))

    def test_r16_35_01_j_095_governed(self):
        self._candidate(_bad('Trace sumʤarise'), _read('Trace sumʤarise'))

    def test_r16_35_01_j_096_governed(self):
        self._candidate(_bad('Trace sumʥarise'), _read('Trace sumʥarise'))

    def test_r16_35_01_j_097_governed(self):
        self._candidate(_bad('Trace sumʦarise'), _read('Trace sumʦarise'))

    def test_r16_35_01_j_098_governed(self):
        self._candidate(_bad('Trace sumʨarise'), _read('Trace sumʨarise'))

    def test_r16_35_01_j_099_governed(self):
        self._candidate(_bad('Trace sumʩarise'), _read('Trace sumʩarise'))

    def test_r16_35_01_j_100_governed(self):
        self._candidate(_bad('Trace sumʪarise'), _read('Trace sumʪarise'))

    def test_r16_35_01_j_101_governed(self):
        self._candidate(_bad('Trace sumʫarise'), _read('Trace sumʫarise'))

    def test_r16_35_01_j_102_governed(self):
        self._candidate(_bad('Trace sumʬarise'), _read('Trace sumʬarise'))

    def test_r16_35_01_j_103_governed(self):
        self._candidate(_bad('Trace sumʭarise'), _read('Trace sumʭarise'))

    def test_r16_35_01_j_104_governed(self):
        self._candidate(_bad('Trace sumʮarise'), _read('Trace sumʮarise'))

    def test_r16_35_01_j_105_governed(self):
        self._candidate(_bad('Trace sumʯarise'), _read('Trace sumʯarise'))

    def test_r16_35_01_j_106_governed(self):
        self._candidate(_bad('Trace sumʰarise'), _read('Trace sumʰarise'))

    def test_r16_35_01_j_107_governed(self):
        self._candidate(_bad('Trace summariʎe'), _read('Trace summariʎe'))

    def test_r16_35_01_j_108_governed(self):
        self._candidate(_bad('Trace summariʏe'), _read('Trace summariʏe'))

    def test_r16_35_01_j_109_governed(self):
        self._candidate(_bad('Trace summariʔe'), _read('Trace summariʔe'))

    def test_r16_35_01_j_110_governed(self):
        self._candidate(_bad('Trace summariʖe'), _read('Trace summariʖe'))

    def test_r16_35_01_j_111_governed(self):
        self._candidate(_bad('Trace summariʗe'), _read('Trace summariʗe'))

    def test_r16_35_01_j_112_governed(self):
        self._candidate(_bad('Trace summariʙe'), _read('Trace summariʙe'))

    def test_r16_35_01_j_113_governed(self):
        self._candidate(_bad('Trace summariʚe'), _read('Trace summariʚe'))

    def test_r16_35_01_j_114_governed(self):
        self._candidate(_bad('Trace summariʝe'), _read('Trace summariʝe'))

    def test_r16_35_01_j_115_governed(self):
        self._candidate(_bad('Trace summariʞe'), _read('Trace summariʞe'))

    def test_r16_35_01_j_116_governed(self):
        self._candidate(_bad('Trace summariʟe'), _read('Trace summariʟe'))

    def test_r16_35_01_j_117_governed(self):
        self._candidate(_bad('Trace summariʠe'), _read('Trace summariʠe'))

    def test_r16_35_01_j_118_governed(self):
        self._candidate(_bad('Trace summariʡe'), _read('Trace summariʡe'))

    def test_r16_35_01_j_119_governed(self):
        self._candidate(_bad('Trace summariʢe'), _read('Trace summariʢe'))

    def test_r16_35_01_j_120_governed(self):
        self._candidate(_bad('Trace summariʣe'), _read('Trace summariʣe'))

    def test_r16_35_01_j_121_governed(self):
        self._candidate(_bad('Trace summariʤe'), _read('Trace summariʤe'))

    def test_r16_35_01_j_122_governed(self):
        self._candidate(_bad('Trace summariʥe'), _read('Trace summariʥe'))

    def test_r16_35_01_j_123_governed(self):
        self._candidate(_bad('Trace summariʦe'), _read('Trace summariʦe'))

    def test_r16_35_01_j_124_governed(self):
        self._candidate(_bad('Trace summariʨe'), _read('Trace summariʨe'))

    def test_r16_35_01_j_125_governed(self):
        self._candidate(_bad('Trace summariʩe'), _read('Trace summariʩe'))

    def test_r16_35_01_j_126_governed(self):
        self._candidate(_bad('Trace summariʪe'), _read('Trace summariʪe'))

    def test_r16_35_01_j_127_governed(self):
        self._candidate(_bad('Trace summariʫe'), _read('Trace summariʫe'))

    def test_r16_35_01_j_128_governed(self):
        self._candidate(_bad('Trace summariʬe'), _read('Trace summariʬe'))

    def test_r16_35_01_j_129_governed(self):
        self._candidate(_bad('Trace summariʭe'), _read('Trace summariʭe'))

    def test_r16_35_01_j_130_governed(self):
        self._candidate(_bad('Trace summariʮe'), _read('Trace summariʮe'))

    def test_r16_35_01_j_131_governed(self):
        self._candidate(_bad('Trace summariʯe'), _read('Trace summariʯe'))

    def test_r16_35_01_j_132_governed(self):
        self._candidate(_bad('Trace summariʰe'), _read('Trace summariʰe'))

    def test_r16_35_01_j_133_governed(self):
        self._candidate(_bad('Trace summarisʍ'), _read('Trace summarisʍ'))

    def test_r16_35_01_j_134_governed(self):
        self._candidate(_bad('Trace summarisʎ'), _read('Trace summarisʎ'))

    def test_r16_35_01_j_135_governed(self):
        self._candidate(_bad('Trace summarisʑ'), _read('Trace summarisʑ'))

    def test_r16_35_01_j_136_governed(self):
        self._candidate(_bad('Trace summarisʓ'), _read('Trace summarisʓ'))

    def test_r16_35_01_j_137_governed(self):
        self._candidate(_bad('Trace summarisʔ'), _read('Trace summarisʔ'))

    def test_r16_35_01_j_138_governed(self):
        self._candidate(_bad('Trace summarisʖ'), _read('Trace summarisʖ'))

    def test_r16_35_01_j_139_governed(self):
        self._candidate(_bad('Trace summarisʗ'), _read('Trace summarisʗ'))

    def test_r16_35_01_j_140_governed(self):
        self._candidate(_bad('Trace summarisʙ'), _read('Trace summarisʙ'))

    def test_r16_35_01_j_141_governed(self):
        self._candidate(_bad('Trace summarisʛ'), _read('Trace summarisʛ'))

    def test_r16_35_01_j_142_governed(self):
        self._candidate(_bad('Trace summarisʞ'), _read('Trace summarisʞ'))

    def test_r16_35_01_j_143_governed(self):
        self._candidate(_bad('Trace summarisʟ'), _read('Trace summarisʟ'))

    def test_r16_35_01_j_144_governed(self):
        self._candidate(_bad('Trace summarisʠ'), _read('Trace summarisʠ'))

    def test_r16_35_01_j_145_governed(self):
        self._candidate(_bad('Trace summarisʣ'), _read('Trace summarisʣ'))

    def test_r16_35_01_j_146_governed(self):
        self._candidate(_bad('Trace summarisʥ'), _read('Trace summarisʥ'))

    def test_r16_35_01_j_147_governed(self):
        self._candidate(_bad('Trace summarisʦ'), _read('Trace summarisʦ'))

    def test_r16_35_01_j_148_governed(self):
        self._candidate(_bad('Trace summarisʨ'), _read('Trace summarisʨ'))

    def test_r16_35_01_j_149_governed(self):
        self._candidate(_bad('Trace summarisʩ'), _read('Trace summarisʩ'))

    def test_r16_35_01_j_150_governed(self):
        self._candidate(_bad('Trace summarisʪ'), _read('Trace summarisʪ'))

    def test_r16_35_01_j_151_governed(self):
        self._candidate(_bad('Trace summarisʫ'), _read('Trace summarisʫ'))

    def test_r16_35_01_j_152_governed(self):
        self._candidate(_bad('Trace summarisʬ'), _read('Trace summarisʬ'))

    def test_r16_35_01_j_153_governed(self):
        self._candidate(_bad('Trace summarisʭ'), _read('Trace summarisʭ'))

    def test_r16_35_01_j_154_governed(self):
        self._candidate(_bad('Trace summarisʮ'), _read('Trace summarisʮ'))

    def test_r16_35_01_j_155_governed(self):
        self._candidate(_bad('Trace summarisʯ'), _read('Trace summarisʯ'))

    def test_r16_35_01_j_156_governed(self):
        self._candidate(_bad('Trace summarisʰ'), _read('Trace summarisʰ'))

    def test_r16_35_01_j_157_governed(self):
        self._candidate(_bad('Board Ȼally'), _read('Board Ȼally'))

    def test_r16_35_01_j_158_governed(self):
        self._candidate(_bad('Trace summaȻise'), _read('Trace summaȻise'))

    def test_r16_35_01_j_159_governed(self):
        self._candidate(_bad('Board taȻy'), _read('Board taȻy'))

    def test_r16_35_01_j_160_governed(self):
        self._candidate(_bad('Board ƚally'), _read('Board ƚally'))

    def test_r16_35_01_j_161_governed(self):
        self._candidate(_bad('Trace summaƚise'), _read('Trace summaƚise'))

    def test_r16_35_01_j_162_governed(self):
        self._candidate(_bad('Trace suǲmarise'), _read('Trace suǲmarise'))

    # ------------------------------------------------------
    # Adopted assertions of the round 35 breaker exhibit:
    # the beside, gate ruling and code level assertions
    # of B35-B01, in the forms the exhibit names them,
    # standing in the exhibit test names themselves.
    # ------------------------------------------------------

    def test_b35_lectiontally_beside(self):
        q4 = self._beside(_bad("Lectiontally"))
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_b35_summarised_beside(self):
        q4 = self._beside(_bad('Trace summarisedeseseseseseseseseseseseseseseseses'))
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_b35_lectiontally_gate_ruling(self):
        report = self._q4_alone(_bad("Lectiontally"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    def test_b35_code_level_underreach_forms(self):
        for word in ("lectiontally", "lectionstallies",
                     "boardlectiontally", "tallye11", "boardtallyaz10"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ('summarisedeseseseseseseseseseseseseseseseses', 'summaryeseseseseseseseseseseseseseseseseses'):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ('boardtracesummarisedeseseseseseseseseseseseseseseseses',
                     'traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary'):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        for head in ("Lectiontally",
                     'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel summary',
                     'Trace summarisedeseseseseseseseseseseseseseseseses'):
            line = head + ": items checked stand here"
            self.assertTrue(_tally_statement_head(line), head)

    # ------------------------------------------------------
    # Held controls of R16-35-02, standing missing in the
    # cure of this unit: every distinct converse form of
    # the register, one test per form.
    # ------------------------------------------------------

    def test_control_converse_000_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snort trace summary')))

    def test_control_converse_001_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grunt trace summary')))

    def test_control_converse_002_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wail trace summary')))

    def test_control_converse_003_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bawl trace summary')))

    def test_control_converse_004_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sniffle trace summary')))

    def test_control_converse_005_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cry trace summary')))

    def test_control_converse_006_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel howl trace summary')))

    def test_control_converse_007_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shriek trace summary')))

    def test_control_converse_008_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel squeal trace summary')))

    def test_control_converse_009_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel beam trace summary')))

    def test_control_converse_010_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sulk trace summary')))

    def test_control_converse_011_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel brood trace summary')))

    def test_control_converse_012_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wonder trace summary')))

    def test_control_converse_013_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whinny trace summary')))

    def test_control_converse_014_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel neigh trace summary')))

    def test_control_converse_015_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bellow trace summary')))

    def test_control_converse_016_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel roar trace summary')))

    def test_control_converse_017_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel growl trace summary')))

    def test_control_converse_018_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bark trace summary')))

    def test_control_converse_019_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel purr trace summary')))

    def test_control_converse_020_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cluck trace summary')))

    def test_control_converse_021_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel quack trace summary')))

    def test_control_converse_022_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel honk trace summary')))

    def test_control_converse_023_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chirp trace summary')))

    def test_control_converse_024_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel warble trace summary')))

    def test_control_converse_025_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel croak trace summary')))

    def test_control_converse_026_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel buzz trace summary')))

    def test_control_converse_027_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk scoff summary trace')))

    def test_control_converse_028_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team jeer trace summary')))

    def test_control_converse_029_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wail summary trace')))

    def test_control_converse_030_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk fumble trace summary')))

    def test_control_converse_031_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team hesitate summary trace')))

    def test_control_converse_032_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snort tracesummary')))

    def test_control_converse_033_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grunt tracesummary')))

    def test_control_converse_034_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wail tracesummary')))

    def test_control_converse_035_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bawl tracesummary')))

    def test_control_converse_036_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sniffle tracesummary')))

    def test_control_converse_037_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cry tracesummary')))

    def test_control_converse_038_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel howl tracesummary')))

    def test_control_converse_039_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shriek tracesummary')))

    def test_control_converse_040_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel squeal tracesummary')))

    def test_control_converse_041_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel beam tracesummary')))

    def test_control_converse_042_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sulk tracesummary')))

    def test_control_converse_043_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel brood tracesummary')))

    def test_control_converse_044_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wonder tracesummary')))

    def test_control_converse_045_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whinny tracesummary')))

    def test_control_converse_046_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel neigh tracesummary')))

    def test_control_converse_047_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bellow tracesummary')))

    def test_control_converse_048_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel roar tracesummary')))

    def test_control_converse_049_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel growl tracesummary')))

    def test_control_converse_050_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bark tracesummary')))

    def test_control_converse_051_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel purr tracesummary')))

    def test_control_converse_052_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cluck tracesummary')))

    def test_control_converse_053_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel quack tracesummary')))

    def test_control_converse_054_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel honk tracesummary')))

    def test_control_converse_055_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chirp tracesummary')))

    def test_control_converse_056_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel warble tracesummary')))

    def test_control_converse_057_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel croak tracesummary')))

    def test_control_converse_058_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel buzz tracesummary')))

    def test_control_converse_059_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk scoff summarytrace')))

    def test_control_converse_060_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team jeer boardtracesummary')))

    def test_control_converse_061_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wail traceboardgatesummary')))

    def test_control_converse_062_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk snort traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary')))

    def test_control_converse_063_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team scoff tracesummarisationeseseseseseseseseseseseseseseseses')))

    def test_control_converse_064_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩐ trace summary')))

    def test_control_converse_065_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩑ trace summary')))

    def test_control_converse_066_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩒ trace summary')))

    def test_control_converse_067_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩓ trace summary')))

    def test_control_converse_068_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩔ trace summary')))

    def test_control_converse_069_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩕ trace summary')))

    def test_control_converse_070_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩖ trace summary')))

    def test_control_converse_071_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩗ trace summary')))

    def test_control_converse_072_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩘ trace summary')))

    def test_control_converse_073_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩙ trace summary')))

    def test_control_converse_074_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩚ trace summary')))

    def test_control_converse_075_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩛ trace summary')))

    def test_control_converse_076_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩜ trace summary')))

    def test_control_converse_077_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩝ trace summary')))

    def test_control_converse_078_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩞ trace summary')))

    def test_control_converse_079_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩟ trace summary')))

    def test_control_converse_080_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩠ trace summary')))

    def test_control_converse_081_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩡ trace summary')))

    def test_control_converse_082_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩢ trace summary')))

    def test_control_converse_083_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩣ trace summary')))

    def test_control_converse_084_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩤ trace summary')))

    def test_control_converse_085_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩥ trace summary')))

    def test_control_converse_086_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩦ trace summary')))

    def test_control_converse_087_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩧ trace summary')))

    def test_control_converse_088_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩨ trace summary')))

    def test_control_converse_089_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩩ trace summary')))

    def test_control_converse_090_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩪ trace summary')))

    def test_control_converse_091_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩫ trace summary')))

    def test_control_converse_092_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩬ trace summary')))

    def test_control_converse_093_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩭ trace summary')))

    def test_control_converse_094_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩮ trace summary')))

    def test_control_converse_095_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩯ trace summary')))

    def test_control_converse_096_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧌ trace summary')))

    def test_control_converse_097_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧍ trace summary')))

    def test_control_converse_098_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧎ trace summary')))

    def test_control_converse_099_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧏ trace summary')))

    def test_control_converse_100_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧐ trace summary')))

    def test_control_converse_101_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧑ trace summary')))

    def test_control_converse_102_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌔ trace summary')))

    def test_control_converse_103_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⏡ trace summary')))

    def test_control_converse_104_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⬰ trace summary')))

    def test_control_converse_105_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⬱ trace summary')))

    def test_control_converse_106_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃪ trace summary')))

    def test_control_converse_107_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃫ trace summary')))

    def test_control_converse_108_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃬ trace summary')))

    def test_control_converse_109_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃭ trace summary')))

    def test_control_converse_110_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃮ trace summary')))

    def test_control_converse_111_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃯ trace summary')))

    def test_control_converse_112_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃰ trace summary')))

    def test_control_converse_113_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x⃪ trace summary')))

    def test_control_converse_114_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x⃫ trace summary')))

    def test_control_converse_115_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x⃬ trace summary')))

    def test_control_converse_116_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x⃭ trace summary')))

    def test_control_converse_117_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x⃮ trace summary')))

    def test_control_converse_118_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x⃯ trace summary')))

    def test_control_converse_119_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x⃰ trace summary')))

    def test_control_converse_120_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹇panel⹈ trace summary')))

    def test_control_converse_121_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹝panel\u2e5e trace summary')))

    def test_control_converse_122_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Snort panel trace summary')))

    def test_control_converse_123_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Grunt panel trace summary')))

    def test_control_converse_124_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Wail panel trace summary')))

    def test_control_converse_125_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Bawl panel trace summary')))

    def test_control_converse_126_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Sniffle panel trace summary')))

    def test_control_converse_127_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Cry panel trace summary')))

    def test_control_converse_128_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Howl panel trace summary')))

    def test_control_converse_129_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Shriek panel trace summary')))

    def test_control_converse_130_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Squeal panel trace summary')))

    def test_control_converse_131_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Beam panel trace summary')))

    def test_control_converse_132_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Sulk panel trace summary')))

    def test_control_converse_133_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Brood panel trace summary')))

    def test_control_converse_134_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Wonder panel trace summary')))

    def test_control_converse_135_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Whinny panel trace summary')))

    def test_control_converse_136_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Neigh panel trace summary')))

    def test_control_converse_137_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Bellow panel trace summary')))

    def test_control_converse_138_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Roar panel trace summary')))

    def test_control_converse_139_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Growl panel trace summary')))

    def test_control_converse_140_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Bark panel trace summary')))

    def test_control_converse_141_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Purr panel trace summary')))

    def test_control_converse_142_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Cluck panel trace summary')))

    def test_control_converse_143_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Quack panel trace summary')))

    def test_control_converse_144_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Honk panel trace summary')))

    def test_control_converse_145_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Chirp panel trace summary')))

    def test_control_converse_146_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Warble panel trace summary')))

    def test_control_converse_147_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Croak panel trace summary')))

    def test_control_converse_148_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Buzz panel trace summary')))

    def test_control_converse_149_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Snort ledger trace summary')))

    # ------------------------------------------------------
    # Held controls of R16-35-02 named in the register,
    # standing missing in their recorded forms.
    # ------------------------------------------------------

    def test_control_held35_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hum trace summary')))

    def test_control_held35_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋈ trace summary')))

    def test_control_held35_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋊ trace summary')))

    def test_control_held35_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋋ trace summary')))

    def test_control_held35_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋌ trace summary')))

    def test_control_held35_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧈ trace summary')))

    def test_control_held35_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧉ trace summary')))

    def test_control_held35_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦅panel⦆ trace summary')))

    def test_control_held35_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⟦panel⟧ trace summary')))

    def test_control_held35_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger （panel） trace summary')))

    def test_control_held35_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸕panel⸖ trace summary')))

    def test_control_held35_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⁅panel⁆ trace summary')))

    def test_control_held35_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃔ trace summary')))

    def test_control_held35_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃐ trace summary')))

    def test_control_held35_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃑ trace summary')))

    def test_control_held35_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃒ trace summary')))

    def test_control_held35_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃓ trace summary')))

    def test_control_held35_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃔ trace summary')))

    def test_control_held35_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃕ trace summary')))

    def test_control_held35_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃖ trace summary')))

    def test_control_held35_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃗ trace summary')))

    def test_control_held35_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃘ trace summary')))

    def test_control_held35_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃙ trace summary')))

    def test_control_held35_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃚ trace summary')))

    def test_control_held35_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃛ trace summary')))

    def test_control_held35_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃜ trace summary')))

    def test_control_held35_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃝ trace summary')))

    def test_control_held35_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃞ trace summary')))

    def test_control_held35_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃟ trace summary')))

    def test_control_held35_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃠ trace summary')))

    def test_control_held35_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃡ trace summary')))

    def test_control_held35_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃢ trace summary')))

    def test_control_held35_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃣ trace summary')))

    def test_control_held35_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃤ trace summary')))

    def test_control_held35_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃥ trace summary')))

    def test_control_held35_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹗panel⹘ trace summary')))

    def test_control_held35_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹙panel⹚ trace summary')))

    # ------------------------------------------------------
    # Governed closings of R16-35-02, standing governed
    # in the cure of this unit.
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
    # Held governed forms of R16-35-01, standing governed
    # in the cure of this unit: the governed neighbours
    # of both papers in their recorded forms.
    # ------------------------------------------------------

    def test_control_underheld_000_governed(self):
        self._candidate(_bad('Workbookstallies'), _read('Workbookstallies'))

    def test_control_underheld_001_governed(self):
        self._candidate(_bad('Yearbookstallies'), _read('Yearbookstallies'))

    def test_control_underheld_002_governed(self):
        self._candidate(_bad('Logbookstallies'), _read('Logbookstallies'))

    def test_control_underheld_003_governed(self):
        self._candidate(_bad('Textbookstallies'), _read('Textbookstallies'))

    def test_control_underheld_004_governed(self):
        self._candidate(_bad('Handbookstallies'), _read('Handbookstallies'))

    def test_control_underheld_005_governed(self):
        self._candidate(_bad('Cookbookstallies'), _read('Cookbookstallies'))

    def test_control_underheld_006_governed(self):
        self._candidate(_bad('Scrapbookstallies'), _read('Scrapbookstallies'))

    def test_control_underheld_007_governed(self):
        self._candidate(_bad('Daybookstallies'), _read('Daybookstallies'))

    def test_control_underheld_008_governed(self):
        self._candidate(_bad('Guestbookstallies'), _read('Guestbookstallies'))

    def test_control_underheld_009_governed(self):
        self._candidate(_bad('Manualstallies'), _read('Manualstallies'))

    def test_control_underheld_010_governed(self):
        self._candidate(_bad('Gradualstallies'), _read('Gradualstallies'))

    def test_control_underheld_011_governed(self):
        self._candidate(_bad('Workbooktally'), _read('Workbooktally'))

    def test_control_underheld_012_governed(self):
        self._candidate(_bad('Manualtally'), _read('Manualtally'))

    def test_control_underheld_013_governed(self):
        self._candidate(_bad('Boardanthembooktallye'), _read('Boardanthembooktallye'))

    def test_control_underheld_014_governed(self):
        self._candidate(_bad('Songbooktally'), _read('Songbooktally'))

    def test_control_underheld_015_governed(self):
        self._candidate(_bad('Songbookstallies'), _read('Songbookstallies'))

    def test_control_underheld_016_governed(self):
        self._candidate(_bad('Nocturntally'), _read('Nocturntally'))

    def test_control_underheld_017_governed(self):
        self._candidate(_bad('Antiphontally'), _read('Antiphontally'))

    def test_control_underheld_018_governed(self):
        self._candidate(_bad('Rubrictally'), _read('Rubrictally'))

    def test_control_underheld_019_governed(self):
        self._candidate(_bad('Boarddictionarytally'), _read('Boarddictionarytally'))

    def test_control_underheld_020_governed(self):
        self._candidate(_bad('Boardnocturntallye'), _read('Boardnocturntallye'))

    def test_control_underheld_021_governed(self):
        self._candidate(_bad('Tallye10'), _read('Tallye10'))

    def test_control_underheld_022_governed(self):
        self._candidate(_bad('Boardtallye10'), _read('Boardtallye10'))

    def test_control_underheld_023_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseseseseseses'))

    def test_control_underheld_024_governed(self):
        self._candidate(_bad('Trace summarisingeseseseseseseseseseseseseseseses'), _read('Trace summarisingeseseseseseseseseseseseseseseses'))

    def test_control_underheld_025_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseseseseses'))

    def test_control_underheld_026_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseseseseses'))

    def test_control_underheld_027_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseseseseses'))

    def test_control_underheld_028_governed(self):
        self._candidate(_bad('Trace summaryeseseseseseseseseseseseseseseseses'), _read('Trace summaryeseseseseseseseseseseseseseseseses'))

    def test_control_underheld_029_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseseseseses'))

    def test_control_underheld_030_governed(self):
        self._candidate(_bad('Board ǉally'), _read('Board ǉally'))

    def test_control_underheld_031_governed(self):
        self._candidate(_bad('Trace suǉmarise'), _read('Trace suǉmarise'))

    def test_control_underheld_032_governed(self):
        self._candidate(_bad('Board Ǳally'), _read('Board Ǳally'))

    def test_control_underheld_033_governed(self):
        self._candidate(_bad('Board taǱy'), _read('Board taǱy'))

    def test_control_underheld_034_governed(self):
        self._candidate(_bad('Board Ⱥally'), _read('Board Ⱥally'))

    def test_control_underheld_035_governed(self):
        self._candidate(_bad('Trace summaȺise'), _read('Trace summaȺise'))

    def test_control_underheld_036_governed(self):
        self._candidate(_bad('Board ʐally'), _read('Board ʐally'))

    def test_control_underheld_037_governed(self):
        self._candidate(_bad('Trace summarisʐ'), _read('Trace summarisʐ'))

    def test_control_underheld_038_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'))

    def test_control_underheld_039_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardtrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardtrace'))

    def test_control_underheld_040_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'))

    def test_control_underheld_041_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex summary'))

    def test_control_underheld_042_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex trace'))

    def test_control_underheld_043_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex for step 2'))

    def test_control_underheld_044_governed(self):
        self._candidate(_bad('Board ʉally'), _read('Board ʉally'))

    def test_control_underheld_045_governed(self):
        self._candidate(_bad('Board ʊally'), _read('Board ʊally'))

    def test_control_underheld_046_governed(self):
        self._candidate(_bad('Board ʋally'), _read('Board ʋally'))

    def test_control_underheld_047_governed(self):
        self._candidate(_bad('Board ʌally'), _read('Board ʌally'))

    def test_control_underheld_048_governed(self):
        self._candidate(_bad('Board ʍally'), _read('Board ʍally'))

    def test_control_underheld_049_governed(self):
        self._candidate(_bad('Board ʐally'), _read('Board ʐally'))

    def test_control_underheld_050_governed(self):
        self._candidate(_bad('Board ʒally'), _read('Board ʒally'))

    def test_control_underheld_051_governed(self):
        self._candidate(_bad('Board ʔally'), _read('Board ʔally'))

    def test_control_underheld_052_governed(self):
        self._candidate(_bad('Board ʕally'), _read('Board ʕally'))

    def test_control_underheld_053_governed(self):
        self._candidate(_bad('Board ʖally'), _read('Board ʖally'))

    def test_control_underheld_054_governed(self):
        self._candidate(_bad('Board ʘally'), _read('Board ʘally'))

    def test_control_underheld_055_governed(self):
        self._candidate(_bad('Board ʙally'), _read('Board ʙally'))

    def test_control_underheld_056_governed(self):
        self._candidate(_bad('Board ʚally'), _read('Board ʚally'))

    def test_control_underheld_057_governed(self):
        self._candidate(_bad('Board ʛally'), _read('Board ʛally'))

    def test_control_underheld_058_governed(self):
        self._candidate(_bad('Board ʞally'), _read('Board ʞally'))

    def test_control_underheld_059_governed(self):
        self._candidate(_bad('Board ʠally'), _read('Board ʠally'))

    def test_control_underheld_060_governed(self):
        self._candidate(_bad('Board ʡally'), _read('Board ʡally'))

    def test_control_underheld_061_governed(self):
        self._candidate(_bad('Board ʢally'), _read('Board ʢally'))

    def test_control_underheld_062_governed(self):
        self._candidate(_bad('Board ʣally'), _read('Board ʣally'))

    def test_control_underheld_063_governed(self):
        self._candidate(_bad('Board ʦally'), _read('Board ʦally'))

    def test_control_underheld_064_governed(self):
        self._candidate(_bad('Board ʧally'), _read('Board ʧally'))

    def test_control_underheld_065_governed(self):
        self._candidate(_bad('Board ʨally'), _read('Board ʨally'))

    def test_control_underheld_066_governed(self):
        self._candidate(_bad('Board ʪally'), _read('Board ʪally'))

    def test_control_underheld_067_governed(self):
        self._candidate(_bad('Board ʭally'), _read('Board ʭally'))

    def test_control_underheld_068_governed(self):
        self._candidate(_bad('Board taʉly'), _read('Board taʉly'))

    def test_control_underheld_069_governed(self):
        self._candidate(_bad('Board taʊly'), _read('Board taʊly'))

    def test_control_underheld_070_governed(self):
        self._candidate(_bad('Board taʋly'), _read('Board taʋly'))

    def test_control_underheld_071_governed(self):
        self._candidate(_bad('Board taʌly'), _read('Board taʌly'))

    def test_control_underheld_072_governed(self):
        self._candidate(_bad('Board taʎly'), _read('Board taʎly'))

    def test_control_underheld_073_governed(self):
        self._candidate(_bad('Board taʒly'), _read('Board taʒly'))

    def test_control_underheld_074_governed(self):
        self._candidate(_bad('Board taʕly'), _read('Board taʕly'))

    def test_control_underheld_075_governed(self):
        self._candidate(_bad('Board taʘly'), _read('Board taʘly'))

    def test_control_underheld_076_governed(self):
        self._candidate(_bad('Board taʞly'), _read('Board taʞly'))

    def test_control_underheld_077_governed(self):
        self._candidate(_bad('Board taʟly'), _read('Board taʟly'))

    def test_control_underheld_078_governed(self):
        self._candidate(_bad('Board taʧly'), _read('Board taʧly'))

    def test_control_underheld_079_governed(self):
        self._candidate(_bad('Trace sʉmmarise'), _read('Trace sʉmmarise'))

    def test_control_underheld_080_governed(self):
        self._candidate(_bad('Trace sʊmmarise'), _read('Trace sʊmmarise'))

    def test_control_underheld_081_governed(self):
        self._candidate(_bad('Trace sʋmmarise'), _read('Trace sʋmmarise'))

    def test_control_underheld_082_governed(self):
        self._candidate(_bad('Trace sʌmmarise'), _read('Trace sʌmmarise'))

    def test_control_underheld_083_governed(self):
        self._candidate(_bad('Trace sʒmmarise'), _read('Trace sʒmmarise'))

    def test_control_underheld_084_governed(self):
        self._candidate(_bad('Trace sʕmmarise'), _read('Trace sʕmmarise'))

    def test_control_underheld_085_governed(self):
        self._candidate(_bad('Trace sʘmmarise'), _read('Trace sʘmmarise'))

    def test_control_underheld_086_governed(self):
        self._candidate(_bad('Trace sʛmmarise'), _read('Trace sʛmmarise'))

    def test_control_underheld_087_governed(self):
        self._candidate(_bad('Trace sʡmmarise'), _read('Trace sʡmmarise'))

    def test_control_underheld_088_governed(self):
        self._candidate(_bad('Trace sʧmmarise'), _read('Trace sʧmmarise'))

    def test_control_underheld_089_governed(self):
        self._candidate(_bad('Trace sumʉarise'), _read('Trace sumʉarise'))

    def test_control_underheld_090_governed(self):
        self._candidate(_bad('Trace sumʊarise'), _read('Trace sumʊarise'))

    def test_control_underheld_091_governed(self):
        self._candidate(_bad('Trace sumʋarise'), _read('Trace sumʋarise'))

    def test_control_underheld_092_governed(self):
        self._candidate(_bad('Trace sumʌarise'), _read('Trace sumʌarise'))

    def test_control_underheld_093_governed(self):
        self._candidate(_bad('Trace sumʒarise'), _read('Trace sumʒarise'))

    def test_control_underheld_094_governed(self):
        self._candidate(_bad('Trace sumʕarise'), _read('Trace sumʕarise'))

    def test_control_underheld_095_governed(self):
        self._candidate(_bad('Trace sumʘarise'), _read('Trace sumʘarise'))

    def test_control_underheld_096_governed(self):
        self._candidate(_bad('Trace sumʧarise'), _read('Trace sumʧarise'))

    def test_control_underheld_097_governed(self):
        self._candidate(_bad('Trace summariʉe'), _read('Trace summariʉe'))

    def test_control_underheld_098_governed(self):
        self._candidate(_bad('Trace summariʊe'), _read('Trace summariʊe'))

    def test_control_underheld_099_governed(self):
        self._candidate(_bad('Trace summariʋe'), _read('Trace summariʋe'))

    def test_control_underheld_100_governed(self):
        self._candidate(_bad('Trace summariʌe'), _read('Trace summariʌe'))

    def test_control_underheld_101_governed(self):
        self._candidate(_bad('Trace summariʍe'), _read('Trace summariʍe'))

    def test_control_underheld_102_governed(self):
        self._candidate(_bad('Trace summariʐe'), _read('Trace summariʐe'))

    def test_control_underheld_103_governed(self):
        self._candidate(_bad('Trace summariʑe'), _read('Trace summariʑe'))

    def test_control_underheld_104_governed(self):
        self._candidate(_bad('Trace summariʒe'), _read('Trace summariʒe'))

    def test_control_underheld_105_governed(self):
        self._candidate(_bad('Trace summariʓe'), _read('Trace summariʓe'))

    def test_control_underheld_106_governed(self):
        self._candidate(_bad('Trace summariʕe'), _read('Trace summariʕe'))

    def test_control_underheld_107_governed(self):
        self._candidate(_bad('Trace summariʘe'), _read('Trace summariʘe'))

    def test_control_underheld_108_governed(self):
        self._candidate(_bad('Trace summariʛe'), _read('Trace summariʛe'))

    def test_control_underheld_109_governed(self):
        self._candidate(_bad('Trace summariʜe'), _read('Trace summariʜe'))

    def test_control_underheld_110_governed(self):
        self._candidate(_bad('Trace summariʧe'), _read('Trace summariʧe'))

    def test_control_underheld_111_governed(self):
        self._candidate(_bad('Trace summarisʉ'), _read('Trace summarisʉ'))

    def test_control_underheld_112_governed(self):
        self._candidate(_bad('Trace summarisʊ'), _read('Trace summarisʊ'))

    def test_control_underheld_113_governed(self):
        self._candidate(_bad('Trace summarisʋ'), _read('Trace summarisʋ'))

    def test_control_underheld_114_governed(self):
        self._candidate(_bad('Trace summarisʌ'), _read('Trace summarisʌ'))

    def test_control_underheld_115_governed(self):
        self._candidate(_bad('Trace summarisʏ'), _read('Trace summarisʏ'))

    def test_control_underheld_116_governed(self):
        self._candidate(_bad('Trace summarisʐ'), _read('Trace summarisʐ'))

    def test_control_underheld_117_governed(self):
        self._candidate(_bad('Trace summarisʒ'), _read('Trace summarisʒ'))

    def test_control_underheld_118_governed(self):
        self._candidate(_bad('Trace summarisʕ'), _read('Trace summarisʕ'))

    def test_control_underheld_119_governed(self):
        self._candidate(_bad('Trace summarisʘ'), _read('Trace summarisʘ'))

    def test_control_underheld_120_governed(self):
        self._candidate(_bad('Trace summarisʚ'), _read('Trace summarisʚ'))

    def test_control_underheld_121_governed(self):
        self._candidate(_bad('Trace summarisʜ'), _read('Trace summarisʜ'))

    def test_control_underheld_122_governed(self):
        self._candidate(_bad('Trace summarisʝ'), _read('Trace summarisʝ'))

    def test_control_underheld_123_governed(self):
        self._candidate(_bad('Trace summarisʡ'), _read('Trace summarisʡ'))

    def test_control_underheld_124_governed(self):
        self._candidate(_bad('Trace summarisʢ'), _read('Trace summarisʢ'))

    def test_control_underheld_125_governed(self):
        self._candidate(_bad('Trace summarisʤ'), _read('Trace summarisʤ'))

    def test_control_underheld_126_governed(self):
        self._candidate(_bad('Trace summarisʧ'), _read('Trace summarisʧ'))


if __name__ == "__main__":
    import unittest
    unittest.main()
