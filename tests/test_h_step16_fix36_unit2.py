"""Step 16 fix pass 36 unit 2 tests: the Q-4 closing unit.

Pinning tests for register item R16-36-01 (Medium,
B36-C01 and B36-B01) of Step 16 round 36. The
governing rule of the pass, in its extended form: a
piece not read in full, for whatever reason, is not
read, and its converse: a piece that is no feeder
flips nothing.

R16-36-01: malformed tally statement heads standing
unread past the widened boundary of fix pass 35, on
the counted pattern head agnosticism ground alone.
Three hundred and sixty five distinct alone forms
stand driven in ten subfamilies: (a) tally forms
fused behind record words no widening has named and
behind the plurals of record words in the same
position, twenty two forms; (b) composite openings
built on those forms, eight forms; (c) a variant
spelling in that composite opening position built on
those words, two forms; (d) the variant spellings
past the widened variant sets of one hundred and
twenty one and one hundred and twenty four, eighteen
forms; (e) the summary word in further forms at the
eighteenth and nineteenth es repetitions of its
families, seven forms; (f) the fused closings built
on those forms, four forms; (g) the fused closings
with twenty three governed words fused between the
closing words, three forms; (h) the inserted
closings with twenty six words of subject between in
their wide, middle swap and full swap shapes in both
directions, six forms; (i) the for step closing with
twenty six words of subject between, one form; and
(j) further Latin and kindred letters past the
widened fold set, each standing in a position the
folding does not read, two hundred and ninety four
forms, drawn from the forty eight letter pool
U+02B1 to U+02E0 at six positions, beside the six
fold letters of the breaker paper. The fifty seven
underreach assertions of the round 36 breaker
exhibit stand adopted in this module: the fifty
three alone form assertions of B36-B01 stand among
the defect tests of the subfamilies above in their
driven words, and the beside assertions, the gate
ruling assertion and the code level assertion of
that exhibit stand as defect tests here in the forms
the exhibit names them, in the exhibit test names
themselves. The defect stands bounded in the open by
its held controls: every form of R16-36-02 standing
missing, every held form of that item standing
missing in its recorded form, every governed closing
of that item standing governed, and on the
underreach side the governed neighbours of both
papers standing governed. Locus:
derivation_core.py, _tally_statement_head and its
standing helpers and constants. The cure these tests
pin widens what a malformed tally statement head is
in standing: the governed fused prefix set widened
by the record words and plural stems of this round,
the variant sets widened by the spellings of this
round, the summary word set widened by the further
forms of this round, the fused between reach widened
to twenty three governed words, the inserted
closings standing at twenty six words forward,
twenty six words reversed and twenty six words in
the for step form under the wide test, and the
folding widened by the whole word readings of this
round, so every driven form stands governed beside
its counted sibling while every control stands as it
stood.
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


class TestStep16Fix36Unit2(FixtureTestCase):

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

    def _candidate_governed(self, line, counted_line):
        self._assert_q4_counted(self._q4_alone(counted_line))
        self._assert_q4_governed(self._q4_alone(line))

    def _beside(self, line):
        files = _clean_files()
        files[GATE_2] = gate_record(2, extra=line)
        files[GATE_3] = gate_record(3, extra=TRACE_3)
        return row_block(self._run(files), "Q-4")

    # Defect forms of R16-36-01, subfamily (a): fused record words.

    def test_r16_36_01_a_00_governed(self):
        self._candidate(_bad('Sacramentarytally'), _read('Sacramentarytally'))

    def test_r16_36_01_a_01_governed(self):
        self._candidate(_bad('Sacramentariestallies'), _read('Sacramentariestallies'))

    def test_r16_36_01_a_02_governed(self):
        self._candidate(_bad('Evangelarytally'), _read('Evangelarytally'))

    def test_r16_36_01_a_03_governed(self):
        self._candidate(_bad('Epistolarytally'), _read('Epistolarytally'))

    def test_r16_36_01_a_04_governed(self):
        self._candidate(_bad('Homiliarytally'), _read('Homiliarytally'))

    def test_r16_36_01_a_05_governed(self):
        self._candidate(_bad('Martyrologytally'), _read('Martyrologytally'))

    def test_r16_36_01_a_06_governed(self):
        self._candidate(_bad('Necrologytally'), _read('Necrologytally'))

    def test_r16_36_01_a_07_governed(self):
        self._candidate(_bad('Bestiarytally'), _read('Bestiarytally'))

    def test_r16_36_01_a_08_governed(self):
        self._candidate(_bad('Processionaltally'), _read('Processionaltally'))

    def test_r16_36_01_a_09_governed(self):
        self._candidate(_bad('Responsorialtally'), _read('Responsorialtally'))

    def test_r16_36_01_a_10_governed(self):
        self._candidate(_bad('Antiphonertally'), _read('Antiphonertally'))

    def test_r16_36_01_a_11_governed(self):
        self._candidate(_bad('Collectartally'), _read('Collectartally'))

    def test_r16_36_01_a_12_governed(self):
        self._candidate(_bad('Servicebookstallies'), _read('Servicebookstallies'))

    def test_r16_36_01_a_13_governed(self):
        self._candidate(_bad('Altarbookstallies'), _read('Altarbookstallies'))

    def test_r16_36_01_a_14_governed(self):
        self._candidate(_bad('Choralbookstallies'), _read('Choralbookstallies'))

    def test_r16_36_01_a_15_governed(self):
        self._candidate(_bad('Officebookstallies'), _read('Officebookstallies'))

    def test_r16_36_01_a_16_governed(self):
        self._candidate(_bad('Evangeliarytally'), _read('Evangeliarytally'))

    def test_r16_36_01_a_17_governed(self):
        self._candidate(_bad('Lapidarytally'), _read('Lapidarytally'))

    def test_r16_36_01_a_18_governed(self):
        self._candidate(_bad('Breviariestallies'), _read('Breviariestallies'))

    def test_r16_36_01_a_19_governed(self):
        self._candidate(_bad('Martyrologiestallies'), _read('Martyrologiestallies'))

    def test_r16_36_01_a_20_governed(self):
        self._candidate(_bad('Lectionariestallies'), _read('Lectionariestallies'))

    def test_r16_36_01_a_21_governed(self):
        self._candidate(_bad('Evangeliariestallies'), _read('Evangeliariestallies'))

    # Defect forms of R16-36-01, subfamily (b): composite openings.

    def test_r16_36_01_b_00_governed(self):
        self._candidate(_bad('Boardsacramentarytally'), _read('Boardsacramentarytally'))

    def test_r16_36_01_b_01_governed(self):
        self._candidate(_bad('Gateevangelarytally'), _read('Gateevangelarytally'))

    def test_r16_36_01_b_02_governed(self):
        self._candidate(_bad('Boardmartyrologystallies'), _read('Boardmartyrologystallies'))

    def test_r16_36_01_b_03_governed(self):
        self._candidate(_bad('Gatemartyrologytally'), _read('Gatemartyrologytally'))

    def test_r16_36_01_b_04_governed(self):
        self._candidate(_bad('Reviewcollectartally'), _read('Reviewcollectartally'))

    def test_r16_36_01_b_05_governed(self):
        self._candidate(_bad('Boardevangeliarytally'), _read('Boardevangeliarytally'))

    def test_r16_36_01_b_06_governed(self):
        self._candidate(_bad('Boardsacramentariestallies'), _read('Boardsacramentariestallies'))

    def test_r16_36_01_b_07_governed(self):
        self._candidate(_bad('Gatemartyrologiestallies'), _read('Gatemartyrologiestallies'))

    # Defect forms of R16-36-01, subfamily (c): variant composite openings.

    def test_r16_36_01_c_00_governed(self):
        self._candidate(_bad('Boardsacramentarytallye'), _read('Boardsacramentarytallye'))

    def test_r16_36_01_c_01_governed(self):
        self._candidate(_bad('Gatecollectartalliez'), _read('Gatecollectartalliez'))

    # Defect forms of R16-36-01, subfamily (d): variant spellings.

    def test_r16_36_01_d_00_governed(self):
        self._candidate(_bad('Tallya13'), _read('Tallya13'))

    def test_r16_36_01_d_01_governed(self):
        self._candidate(_bad('Tallyo12'), _read('Tallyo12'))

    def test_r16_36_01_d_02_governed(self):
        self._candidate(_bad('Tallyu12'), _read('Tallyu12'))

    def test_r16_36_01_d_03_governed(self):
        self._candidate(_bad('Tallyai12'), _read('Tallyai12'))

    def test_r16_36_01_d_04_governed(self):
        self._candidate(_bad('Tallyez11'), _read('Tallyez11'))

    def test_r16_36_01_d_05_governed(self):
        self._candidate(_bad('Tallyaz11'), _read('Tallyaz11'))

    def test_r16_36_01_d_06_governed(self):
        self._candidate(_bad('Tallyeo14'), _read('Tallyeo14'))

    def test_r16_36_01_d_07_governed(self):
        self._candidate(_bad('Tallyia6'), _read('Tallyia6'))

    def test_r16_36_01_d_08_governed(self):
        self._candidate(_bad('Tallye12'), _read('Tallye12'))

    def test_r16_36_01_d_09_governed(self):
        self._candidate(_bad('Boardtallya13'), _read('Boardtallya13'))

    def test_r16_36_01_d_10_governed(self):
        self._candidate(_bad('Boardtallyo12'), _read('Boardtallyo12'))

    def test_r16_36_01_d_11_governed(self):
        self._candidate(_bad('Boardtallyu12'), _read('Boardtallyu12'))

    def test_r16_36_01_d_12_governed(self):
        self._candidate(_bad('Boardtallyai12'), _read('Boardtallyai12'))

    def test_r16_36_01_d_13_governed(self):
        self._candidate(_bad('Boardtallyez11'), _read('Boardtallyez11'))

    def test_r16_36_01_d_14_governed(self):
        self._candidate(_bad('Boardtallyaz11'), _read('Boardtallyaz11'))

    def test_r16_36_01_d_15_governed(self):
        self._candidate(_bad('Boardtallyeo14'), _read('Boardtallyeo14'))

    def test_r16_36_01_d_16_governed(self):
        self._candidate(_bad('Boardtallyia6'), _read('Boardtallyia6'))

    def test_r16_36_01_d_17_governed(self):
        self._candidate(_bad('Boardtallye12'), _read('Boardtallye12'))

    # Defect forms of R16-36-01, subfamily (e): summary word further forms.

    def test_r16_36_01_e_00_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseseseseseseseses'))

    def test_r16_36_01_e_01_governed(self):
        self._candidate(_bad('Trace summarisingeseseseseseseseseseseseseseseseseses'), _read('Trace summarisingeseseseseseseseseseseseseseseseseses'))

    def test_r16_36_01_e_02_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseseseseseseses'))

    def test_r16_36_01_e_03_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseseseseseseses'))

    def test_r16_36_01_e_04_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseseseseseseses'))

    def test_r16_36_01_e_05_governed(self):
        self._candidate(_bad('Trace summaryeseseseseseseseseseseseseseseseseseses'), _read('Trace summaryeseseseseseseseseseseseseseseseseseses'))

    def test_r16_36_01_e_06_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseseseseseseses'))

    # Defect forms of R16-36-01, subfamily (f): fused closings on those forms.

    def test_r16_36_01_f_00_governed(self):
        self._candidate(_bad('Boardtracesummarisereseseseseseseseseseseseseseseseseses'), _read('Boardtracesummarisereseseseseseseseseseseseseseseseseses'))

    def test_r16_36_01_f_01_governed(self):
        self._candidate(_bad('Tracessummarieseseseseseseseseseseseseseseseseseses'), _read('Tracessummarieseseseseseseseseseseseseseseseseseses'))

    def test_r16_36_01_f_02_governed(self):
        self._candidate(_bad('Boardtracesummarisedeseseseseseseseseseseseseseseseseses'), _read('Boardtracesummarisedeseseseseseseseseseseseseseseseseses'))

    def test_r16_36_01_f_03_governed(self):
        self._candidate(_bad('Tracessummaryeseseseseseseseseseseseseseseseseseses'), _read('Tracessummaryeseseseseseseseseseseseseseseseseseses'))

    # Defect forms of R16-36-01, subfamily (g): fused between at twenty three words.

    def test_r16_36_01_g_00_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'))

    def test_r16_36_01_g_01_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewtrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewtrace'))

    def test_r16_36_01_g_02_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'))

    # Defect forms of R16-36-01, subfamily (h): inserted closings at twenty six words.

    def test_r16_36_01_h_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board summary'))

    def test_r16_36_01_h_01_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex panel board summary'), _read('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex panel board summary'))

    def test_r16_36_01_h_02_governed(self):
        self._candidate(_bad('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board summary'), _read('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board summary'))

    def test_r16_36_01_h_03_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board trace'))

    def test_r16_36_01_h_04_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex panel board trace'), _read('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex panel board trace'))

    def test_r16_36_01_h_05_governed(self):
        self._candidate(_bad('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board trace'), _read('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board trace'))

    # Defect forms of R16-36-01, subfamily (i): for step closing at twenty six words.

    def test_r16_36_01_i_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board for step 2'))

    # Defect forms of R16-36-01, subfamily (j): further letters past the fold set.

    def test_r16_36_01_j_000_governed(self):
        self._candidate(_bad('Board ʱally'), _read('Board ʱally'))

    def test_r16_36_01_j_001_governed(self):
        self._candidate(_bad('Board ʲally'), _read('Board ʲally'))

    def test_r16_36_01_j_002_governed(self):
        self._candidate(_bad('Board ʳally'), _read('Board ʳally'))

    def test_r16_36_01_j_003_governed(self):
        self._candidate(_bad('Board ʴally'), _read('Board ʴally'))

    def test_r16_36_01_j_004_governed(self):
        self._candidate(_bad('Board ʵally'), _read('Board ʵally'))

    def test_r16_36_01_j_005_governed(self):
        self._candidate(_bad('Board ʶally'), _read('Board ʶally'))

    def test_r16_36_01_j_006_governed(self):
        self._candidate(_bad('Board ʷally'), _read('Board ʷally'))

    def test_r16_36_01_j_007_governed(self):
        self._candidate(_bad('Board ʸally'), _read('Board ʸally'))

    def test_r16_36_01_j_008_governed(self):
        self._candidate(_bad('Board ʹally'), _read('Board ʹally'))

    def test_r16_36_01_j_009_governed(self):
        self._candidate(_bad('Board ʺally'), _read('Board ʺally'))

    def test_r16_36_01_j_010_governed(self):
        self._candidate(_bad('Board ʻally'), _read('Board ʻally'))

    def test_r16_36_01_j_011_governed(self):
        self._candidate(_bad('Board ʼally'), _read('Board ʼally'))

    def test_r16_36_01_j_012_governed(self):
        self._candidate(_bad('Board ʽally'), _read('Board ʽally'))

    def test_r16_36_01_j_013_governed(self):
        self._candidate(_bad('Board ʾally'), _read('Board ʾally'))

    def test_r16_36_01_j_014_governed(self):
        self._candidate(_bad('Board ʿally'), _read('Board ʿally'))

    def test_r16_36_01_j_015_governed(self):
        self._candidate(_bad('Board ˀally'), _read('Board ˀally'))

    def test_r16_36_01_j_016_governed(self):
        self._candidate(_bad('Board ˁally'), _read('Board ˁally'))

    def test_r16_36_01_j_017_governed(self):
        self._candidate(_bad('Board ˂ally'), _read('Board ˂ally'))

    def test_r16_36_01_j_018_governed(self):
        self._candidate(_bad('Board ˃ally'), _read('Board ˃ally'))

    def test_r16_36_01_j_019_governed(self):
        self._candidate(_bad('Board ˄ally'), _read('Board ˄ally'))

    def test_r16_36_01_j_020_governed(self):
        self._candidate(_bad('Board ˅ally'), _read('Board ˅ally'))

    def test_r16_36_01_j_021_governed(self):
        self._candidate(_bad('Board ˆally'), _read('Board ˆally'))

    def test_r16_36_01_j_022_governed(self):
        self._candidate(_bad('Board ˇally'), _read('Board ˇally'))

    def test_r16_36_01_j_023_governed(self):
        self._candidate(_bad('Board ˈally'), _read('Board ˈally'))

    def test_r16_36_01_j_024_governed(self):
        self._candidate(_bad('Board ˉally'), _read('Board ˉally'))

    def test_r16_36_01_j_025_governed(self):
        self._candidate(_bad('Board ˊally'), _read('Board ˊally'))

    def test_r16_36_01_j_026_governed(self):
        self._candidate(_bad('Board ˋally'), _read('Board ˋally'))

    def test_r16_36_01_j_027_governed(self):
        self._candidate(_bad('Board ˌally'), _read('Board ˌally'))

    def test_r16_36_01_j_028_governed(self):
        self._candidate(_bad('Board ˍally'), _read('Board ˍally'))

    def test_r16_36_01_j_029_governed(self):
        self._candidate(_bad('Board ˎally'), _read('Board ˎally'))

    def test_r16_36_01_j_030_governed(self):
        self._candidate(_bad('Board ˏally'), _read('Board ˏally'))

    def test_r16_36_01_j_031_governed(self):
        self._candidate(_bad('Board ːally'), _read('Board ːally'))

    def test_r16_36_01_j_032_governed(self):
        self._candidate(_bad('Board ˑally'), _read('Board ˑally'))

    def test_r16_36_01_j_033_governed(self):
        self._candidate(_bad('Board ˒ally'), _read('Board ˒ally'))

    def test_r16_36_01_j_034_governed(self):
        self._candidate(_bad('Board ˓ally'), _read('Board ˓ally'))

    def test_r16_36_01_j_035_governed(self):
        self._candidate(_bad('Board ˔ally'), _read('Board ˔ally'))

    def test_r16_36_01_j_036_governed(self):
        self._candidate(_bad('Board ˕ally'), _read('Board ˕ally'))

    def test_r16_36_01_j_037_governed(self):
        self._candidate(_bad('Board ˖ally'), _read('Board ˖ally'))

    def test_r16_36_01_j_038_governed(self):
        self._candidate(_bad('Board ˗ally'), _read('Board ˗ally'))

    def test_r16_36_01_j_039_governed(self):
        self._candidate(_bad('Board ˘ally'), _read('Board ˘ally'))

    def test_r16_36_01_j_040_governed(self):
        self._candidate(_bad('Board ˙ally'), _read('Board ˙ally'))

    def test_r16_36_01_j_041_governed(self):
        self._candidate(_bad('Board ˚ally'), _read('Board ˚ally'))

    def test_r16_36_01_j_042_governed(self):
        self._candidate(_bad('Board ˛ally'), _read('Board ˛ally'))

    def test_r16_36_01_j_043_governed(self):
        self._candidate(_bad('Board ˜ally'), _read('Board ˜ally'))

    def test_r16_36_01_j_044_governed(self):
        self._candidate(_bad('Board ˝ally'), _read('Board ˝ally'))

    def test_r16_36_01_j_045_governed(self):
        self._candidate(_bad('Board ˞ally'), _read('Board ˞ally'))

    def test_r16_36_01_j_046_governed(self):
        self._candidate(_bad('Board ˟ally'), _read('Board ˟ally'))

    def test_r16_36_01_j_047_governed(self):
        self._candidate(_bad('Board ˠally'), _read('Board ˠally'))

    def test_r16_36_01_j_048_governed(self):
        self._candidate(_bad('Board taʱly'), _read('Board taʱly'))

    def test_r16_36_01_j_049_governed(self):
        self._candidate(_bad('Board taʲly'), _read('Board taʲly'))

    def test_r16_36_01_j_050_governed(self):
        self._candidate(_bad('Board taʳly'), _read('Board taʳly'))

    def test_r16_36_01_j_051_governed(self):
        self._candidate(_bad('Board taʴly'), _read('Board taʴly'))

    def test_r16_36_01_j_052_governed(self):
        self._candidate(_bad('Board taʵly'), _read('Board taʵly'))

    def test_r16_36_01_j_053_governed(self):
        self._candidate(_bad('Board taʶly'), _read('Board taʶly'))

    def test_r16_36_01_j_054_governed(self):
        self._candidate(_bad('Board taʷly'), _read('Board taʷly'))

    def test_r16_36_01_j_055_governed(self):
        self._candidate(_bad('Board taʸly'), _read('Board taʸly'))

    def test_r16_36_01_j_056_governed(self):
        self._candidate(_bad('Board taʹly'), _read('Board taʹly'))

    def test_r16_36_01_j_057_governed(self):
        self._candidate(_bad('Board taʺly'), _read('Board taʺly'))

    def test_r16_36_01_j_058_governed(self):
        self._candidate(_bad('Board taʻly'), _read('Board taʻly'))

    def test_r16_36_01_j_059_governed(self):
        self._candidate(_bad('Board taʼly'), _read('Board taʼly'))

    def test_r16_36_01_j_060_governed(self):
        self._candidate(_bad('Board taʽly'), _read('Board taʽly'))

    def test_r16_36_01_j_061_governed(self):
        self._candidate(_bad('Board taʾly'), _read('Board taʾly'))

    def test_r16_36_01_j_062_governed(self):
        self._candidate(_bad('Board taʿly'), _read('Board taʿly'))

    def test_r16_36_01_j_063_governed(self):
        self._candidate(_bad('Board taˀly'), _read('Board taˀly'))

    def test_r16_36_01_j_064_governed(self):
        self._candidate(_bad('Board taˁly'), _read('Board taˁly'))

    def test_r16_36_01_j_065_governed(self):
        self._candidate(_bad('Board ta˂ly'), _read('Board ta˂ly'))

    def test_r16_36_01_j_066_governed(self):
        self._candidate(_bad('Board ta˃ly'), _read('Board ta˃ly'))

    def test_r16_36_01_j_067_governed(self):
        self._candidate(_bad('Board ta˄ly'), _read('Board ta˄ly'))

    def test_r16_36_01_j_068_governed(self):
        self._candidate(_bad('Board ta˅ly'), _read('Board ta˅ly'))

    def test_r16_36_01_j_069_governed(self):
        self._candidate(_bad('Board taˆly'), _read('Board taˆly'))

    def test_r16_36_01_j_070_governed(self):
        self._candidate(_bad('Board taˇly'), _read('Board taˇly'))

    def test_r16_36_01_j_071_governed(self):
        self._candidate(_bad('Board taˈly'), _read('Board taˈly'))

    def test_r16_36_01_j_072_governed(self):
        self._candidate(_bad('Board taˉly'), _read('Board taˉly'))

    def test_r16_36_01_j_073_governed(self):
        self._candidate(_bad('Board taˊly'), _read('Board taˊly'))

    def test_r16_36_01_j_074_governed(self):
        self._candidate(_bad('Board taˋly'), _read('Board taˋly'))

    def test_r16_36_01_j_075_governed(self):
        self._candidate(_bad('Board taˌly'), _read('Board taˌly'))

    def test_r16_36_01_j_076_governed(self):
        self._candidate(_bad('Board taˍly'), _read('Board taˍly'))

    def test_r16_36_01_j_077_governed(self):
        self._candidate(_bad('Board taˎly'), _read('Board taˎly'))

    def test_r16_36_01_j_078_governed(self):
        self._candidate(_bad('Board taˏly'), _read('Board taˏly'))

    def test_r16_36_01_j_079_governed(self):
        self._candidate(_bad('Board taːly'), _read('Board taːly'))

    def test_r16_36_01_j_080_governed(self):
        self._candidate(_bad('Board taˑly'), _read('Board taˑly'))

    def test_r16_36_01_j_081_governed(self):
        self._candidate(_bad('Board ta˒ly'), _read('Board ta˒ly'))

    def test_r16_36_01_j_082_governed(self):
        self._candidate(_bad('Board ta˓ly'), _read('Board ta˓ly'))

    def test_r16_36_01_j_083_governed(self):
        self._candidate(_bad('Board ta˔ly'), _read('Board ta˔ly'))

    def test_r16_36_01_j_084_governed(self):
        self._candidate(_bad('Board ta˕ly'), _read('Board ta˕ly'))

    def test_r16_36_01_j_085_governed(self):
        self._candidate(_bad('Board ta˖ly'), _read('Board ta˖ly'))

    def test_r16_36_01_j_086_governed(self):
        self._candidate(_bad('Board ta˗ly'), _read('Board ta˗ly'))

    def test_r16_36_01_j_087_governed(self):
        self._candidate(_bad('Board ta˘ly'), _read('Board ta˘ly'))

    def test_r16_36_01_j_088_governed(self):
        self._candidate(_bad('Board ta˙ly'), _read('Board ta˙ly'))

    def test_r16_36_01_j_089_governed(self):
        self._candidate(_bad('Board ta˚ly'), _read('Board ta˚ly'))

    def test_r16_36_01_j_090_governed(self):
        self._candidate(_bad('Board ta˛ly'), _read('Board ta˛ly'))

    def test_r16_36_01_j_091_governed(self):
        self._candidate(_bad('Board ta˜ly'), _read('Board ta˜ly'))

    def test_r16_36_01_j_092_governed(self):
        self._candidate(_bad('Board ta˝ly'), _read('Board ta˝ly'))

    def test_r16_36_01_j_093_governed(self):
        self._candidate(_bad('Board ta˞ly'), _read('Board ta˞ly'))

    def test_r16_36_01_j_094_governed(self):
        self._candidate(_bad('Board ta˟ly'), _read('Board ta˟ly'))

    def test_r16_36_01_j_095_governed(self):
        self._candidate(_bad('Board taˠly'), _read('Board taˠly'))

    def test_r16_36_01_j_096_governed(self):
        self._candidate(_bad('Trace sʱmmarise'), _read('Trace sʱmmarise'))

    def test_r16_36_01_j_097_governed(self):
        self._candidate(_bad('Trace sʲmmarise'), _read('Trace sʲmmarise'))

    def test_r16_36_01_j_098_governed(self):
        self._candidate(_bad('Trace sʳmmarise'), _read('Trace sʳmmarise'))

    def test_r16_36_01_j_099_governed(self):
        self._candidate(_bad('Trace sʴmmarise'), _read('Trace sʴmmarise'))

    def test_r16_36_01_j_100_governed(self):
        self._candidate(_bad('Trace sʵmmarise'), _read('Trace sʵmmarise'))

    def test_r16_36_01_j_101_governed(self):
        self._candidate(_bad('Trace sʶmmarise'), _read('Trace sʶmmarise'))

    def test_r16_36_01_j_102_governed(self):
        self._candidate(_bad('Trace sʷmmarise'), _read('Trace sʷmmarise'))

    def test_r16_36_01_j_103_governed(self):
        self._candidate(_bad('Trace sʸmmarise'), _read('Trace sʸmmarise'))

    def test_r16_36_01_j_104_governed(self):
        self._candidate(_bad('Trace sʹmmarise'), _read('Trace sʹmmarise'))

    def test_r16_36_01_j_105_governed(self):
        self._candidate(_bad('Trace sʺmmarise'), _read('Trace sʺmmarise'))

    def test_r16_36_01_j_106_governed(self):
        self._candidate(_bad('Trace sʻmmarise'), _read('Trace sʻmmarise'))

    def test_r16_36_01_j_107_governed(self):
        self._candidate(_bad('Trace sʼmmarise'), _read('Trace sʼmmarise'))

    def test_r16_36_01_j_108_governed(self):
        self._candidate(_bad('Trace sʽmmarise'), _read('Trace sʽmmarise'))

    def test_r16_36_01_j_109_governed(self):
        self._candidate(_bad('Trace sʾmmarise'), _read('Trace sʾmmarise'))

    def test_r16_36_01_j_110_governed(self):
        self._candidate(_bad('Trace sʿmmarise'), _read('Trace sʿmmarise'))

    def test_r16_36_01_j_111_governed(self):
        self._candidate(_bad('Trace sˀmmarise'), _read('Trace sˀmmarise'))

    def test_r16_36_01_j_112_governed(self):
        self._candidate(_bad('Trace sˁmmarise'), _read('Trace sˁmmarise'))

    def test_r16_36_01_j_113_governed(self):
        self._candidate(_bad('Trace s˂mmarise'), _read('Trace s˂mmarise'))

    def test_r16_36_01_j_114_governed(self):
        self._candidate(_bad('Trace s˃mmarise'), _read('Trace s˃mmarise'))

    def test_r16_36_01_j_115_governed(self):
        self._candidate(_bad('Trace s˄mmarise'), _read('Trace s˄mmarise'))

    def test_r16_36_01_j_116_governed(self):
        self._candidate(_bad('Trace s˅mmarise'), _read('Trace s˅mmarise'))

    def test_r16_36_01_j_117_governed(self):
        self._candidate(_bad('Trace sˆmmarise'), _read('Trace sˆmmarise'))

    def test_r16_36_01_j_118_governed(self):
        self._candidate(_bad('Trace sˇmmarise'), _read('Trace sˇmmarise'))

    def test_r16_36_01_j_119_governed(self):
        self._candidate(_bad('Trace sˈmmarise'), _read('Trace sˈmmarise'))

    def test_r16_36_01_j_120_governed(self):
        self._candidate(_bad('Trace sˉmmarise'), _read('Trace sˉmmarise'))

    def test_r16_36_01_j_121_governed(self):
        self._candidate(_bad('Trace sˊmmarise'), _read('Trace sˊmmarise'))

    def test_r16_36_01_j_122_governed(self):
        self._candidate(_bad('Trace sˋmmarise'), _read('Trace sˋmmarise'))

    def test_r16_36_01_j_123_governed(self):
        self._candidate(_bad('Trace sˌmmarise'), _read('Trace sˌmmarise'))

    def test_r16_36_01_j_124_governed(self):
        self._candidate(_bad('Trace sˍmmarise'), _read('Trace sˍmmarise'))

    def test_r16_36_01_j_125_governed(self):
        self._candidate(_bad('Trace sˎmmarise'), _read('Trace sˎmmarise'))

    def test_r16_36_01_j_126_governed(self):
        self._candidate(_bad('Trace sˏmmarise'), _read('Trace sˏmmarise'))

    def test_r16_36_01_j_127_governed(self):
        self._candidate(_bad('Trace sːmmarise'), _read('Trace sːmmarise'))

    def test_r16_36_01_j_128_governed(self):
        self._candidate(_bad('Trace sˑmmarise'), _read('Trace sˑmmarise'))

    def test_r16_36_01_j_129_governed(self):
        self._candidate(_bad('Trace s˒mmarise'), _read('Trace s˒mmarise'))

    def test_r16_36_01_j_130_governed(self):
        self._candidate(_bad('Trace s˓mmarise'), _read('Trace s˓mmarise'))

    def test_r16_36_01_j_131_governed(self):
        self._candidate(_bad('Trace s˔mmarise'), _read('Trace s˔mmarise'))

    def test_r16_36_01_j_132_governed(self):
        self._candidate(_bad('Trace s˕mmarise'), _read('Trace s˕mmarise'))

    def test_r16_36_01_j_133_governed(self):
        self._candidate(_bad('Trace s˖mmarise'), _read('Trace s˖mmarise'))

    def test_r16_36_01_j_134_governed(self):
        self._candidate(_bad('Trace s˗mmarise'), _read('Trace s˗mmarise'))

    def test_r16_36_01_j_135_governed(self):
        self._candidate(_bad('Trace s˘mmarise'), _read('Trace s˘mmarise'))

    def test_r16_36_01_j_136_governed(self):
        self._candidate(_bad('Trace s˙mmarise'), _read('Trace s˙mmarise'))

    def test_r16_36_01_j_137_governed(self):
        self._candidate(_bad('Trace s˚mmarise'), _read('Trace s˚mmarise'))

    def test_r16_36_01_j_138_governed(self):
        self._candidate(_bad('Trace s˛mmarise'), _read('Trace s˛mmarise'))

    def test_r16_36_01_j_139_governed(self):
        self._candidate(_bad('Trace s˜mmarise'), _read('Trace s˜mmarise'))

    def test_r16_36_01_j_140_governed(self):
        self._candidate(_bad('Trace s˝mmarise'), _read('Trace s˝mmarise'))

    def test_r16_36_01_j_141_governed(self):
        self._candidate(_bad('Trace s˞mmarise'), _read('Trace s˞mmarise'))

    def test_r16_36_01_j_142_governed(self):
        self._candidate(_bad('Trace s˟mmarise'), _read('Trace s˟mmarise'))

    def test_r16_36_01_j_143_governed(self):
        self._candidate(_bad('Trace sˠmmarise'), _read('Trace sˠmmarise'))

    def test_r16_36_01_j_144_governed(self):
        self._candidate(_bad('Trace sumʱarise'), _read('Trace sumʱarise'))

    def test_r16_36_01_j_145_governed(self):
        self._candidate(_bad('Trace sumʲarise'), _read('Trace sumʲarise'))

    def test_r16_36_01_j_146_governed(self):
        self._candidate(_bad('Trace sumʳarise'), _read('Trace sumʳarise'))

    def test_r16_36_01_j_147_governed(self):
        self._candidate(_bad('Trace sumʴarise'), _read('Trace sumʴarise'))

    def test_r16_36_01_j_148_governed(self):
        self._candidate(_bad('Trace sumʵarise'), _read('Trace sumʵarise'))

    def test_r16_36_01_j_149_governed(self):
        self._candidate(_bad('Trace sumʶarise'), _read('Trace sumʶarise'))

    def test_r16_36_01_j_150_governed(self):
        self._candidate(_bad('Trace sumʷarise'), _read('Trace sumʷarise'))

    def test_r16_36_01_j_151_governed(self):
        self._candidate(_bad('Trace sumʸarise'), _read('Trace sumʸarise'))

    def test_r16_36_01_j_152_governed(self):
        self._candidate(_bad('Trace sumʹarise'), _read('Trace sumʹarise'))

    def test_r16_36_01_j_153_governed(self):
        self._candidate(_bad('Trace sumʺarise'), _read('Trace sumʺarise'))

    def test_r16_36_01_j_154_governed(self):
        self._candidate(_bad('Trace sumʻarise'), _read('Trace sumʻarise'))

    def test_r16_36_01_j_155_governed(self):
        self._candidate(_bad('Trace sumʼarise'), _read('Trace sumʼarise'))

    def test_r16_36_01_j_156_governed(self):
        self._candidate(_bad('Trace sumʽarise'), _read('Trace sumʽarise'))

    def test_r16_36_01_j_157_governed(self):
        self._candidate(_bad('Trace sumʾarise'), _read('Trace sumʾarise'))

    def test_r16_36_01_j_158_governed(self):
        self._candidate(_bad('Trace sumʿarise'), _read('Trace sumʿarise'))

    def test_r16_36_01_j_159_governed(self):
        self._candidate(_bad('Trace sumˀarise'), _read('Trace sumˀarise'))

    def test_r16_36_01_j_160_governed(self):
        self._candidate(_bad('Trace sumˁarise'), _read('Trace sumˁarise'))

    def test_r16_36_01_j_161_governed(self):
        self._candidate(_bad('Trace sum˂arise'), _read('Trace sum˂arise'))

    def test_r16_36_01_j_162_governed(self):
        self._candidate(_bad('Trace sum˃arise'), _read('Trace sum˃arise'))

    def test_r16_36_01_j_163_governed(self):
        self._candidate(_bad('Trace sum˄arise'), _read('Trace sum˄arise'))

    def test_r16_36_01_j_164_governed(self):
        self._candidate(_bad('Trace sum˅arise'), _read('Trace sum˅arise'))

    def test_r16_36_01_j_165_governed(self):
        self._candidate(_bad('Trace sumˆarise'), _read('Trace sumˆarise'))

    def test_r16_36_01_j_166_governed(self):
        self._candidate(_bad('Trace sumˇarise'), _read('Trace sumˇarise'))

    def test_r16_36_01_j_167_governed(self):
        self._candidate(_bad('Trace sumˈarise'), _read('Trace sumˈarise'))

    def test_r16_36_01_j_168_governed(self):
        self._candidate(_bad('Trace sumˉarise'), _read('Trace sumˉarise'))

    def test_r16_36_01_j_169_governed(self):
        self._candidate(_bad('Trace sumˊarise'), _read('Trace sumˊarise'))

    def test_r16_36_01_j_170_governed(self):
        self._candidate(_bad('Trace sumˋarise'), _read('Trace sumˋarise'))

    def test_r16_36_01_j_171_governed(self):
        self._candidate(_bad('Trace sumˌarise'), _read('Trace sumˌarise'))

    def test_r16_36_01_j_172_governed(self):
        self._candidate(_bad('Trace sumˍarise'), _read('Trace sumˍarise'))

    def test_r16_36_01_j_173_governed(self):
        self._candidate(_bad('Trace sumˎarise'), _read('Trace sumˎarise'))

    def test_r16_36_01_j_174_governed(self):
        self._candidate(_bad('Trace sumˏarise'), _read('Trace sumˏarise'))

    def test_r16_36_01_j_175_governed(self):
        self._candidate(_bad('Trace sumːarise'), _read('Trace sumːarise'))

    def test_r16_36_01_j_176_governed(self):
        self._candidate(_bad('Trace sumˑarise'), _read('Trace sumˑarise'))

    def test_r16_36_01_j_177_governed(self):
        self._candidate(_bad('Trace sum˒arise'), _read('Trace sum˒arise'))

    def test_r16_36_01_j_178_governed(self):
        self._candidate(_bad('Trace sum˓arise'), _read('Trace sum˓arise'))

    def test_r16_36_01_j_179_governed(self):
        self._candidate(_bad('Trace sum˔arise'), _read('Trace sum˔arise'))

    def test_r16_36_01_j_180_governed(self):
        self._candidate(_bad('Trace sum˕arise'), _read('Trace sum˕arise'))

    def test_r16_36_01_j_181_governed(self):
        self._candidate(_bad('Trace sum˖arise'), _read('Trace sum˖arise'))

    def test_r16_36_01_j_182_governed(self):
        self._candidate(_bad('Trace sum˗arise'), _read('Trace sum˗arise'))

    def test_r16_36_01_j_183_governed(self):
        self._candidate(_bad('Trace sum˘arise'), _read('Trace sum˘arise'))

    def test_r16_36_01_j_184_governed(self):
        self._candidate(_bad('Trace sum˙arise'), _read('Trace sum˙arise'))

    def test_r16_36_01_j_185_governed(self):
        self._candidate(_bad('Trace sum˚arise'), _read('Trace sum˚arise'))

    def test_r16_36_01_j_186_governed(self):
        self._candidate(_bad('Trace sum˛arise'), _read('Trace sum˛arise'))

    def test_r16_36_01_j_187_governed(self):
        self._candidate(_bad('Trace sum˜arise'), _read('Trace sum˜arise'))

    def test_r16_36_01_j_188_governed(self):
        self._candidate(_bad('Trace sum˝arise'), _read('Trace sum˝arise'))

    def test_r16_36_01_j_189_governed(self):
        self._candidate(_bad('Trace sum˞arise'), _read('Trace sum˞arise'))

    def test_r16_36_01_j_190_governed(self):
        self._candidate(_bad('Trace sum˟arise'), _read('Trace sum˟arise'))

    def test_r16_36_01_j_191_governed(self):
        self._candidate(_bad('Trace sumˠarise'), _read('Trace sumˠarise'))

    def test_r16_36_01_j_192_governed(self):
        self._candidate(_bad('Trace summariʱe'), _read('Trace summariʱe'))

    def test_r16_36_01_j_193_governed(self):
        self._candidate(_bad('Trace summariʲe'), _read('Trace summariʲe'))

    def test_r16_36_01_j_194_governed(self):
        self._candidate(_bad('Trace summariʳe'), _read('Trace summariʳe'))

    def test_r16_36_01_j_195_governed(self):
        self._candidate(_bad('Trace summariʴe'), _read('Trace summariʴe'))

    def test_r16_36_01_j_196_governed(self):
        self._candidate(_bad('Trace summariʵe'), _read('Trace summariʵe'))

    def test_r16_36_01_j_197_governed(self):
        self._candidate(_bad('Trace summariʶe'), _read('Trace summariʶe'))

    def test_r16_36_01_j_198_governed(self):
        self._candidate(_bad('Trace summariʷe'), _read('Trace summariʷe'))

    def test_r16_36_01_j_199_governed(self):
        self._candidate(_bad('Trace summariʸe'), _read('Trace summariʸe'))

    def test_r16_36_01_j_200_governed(self):
        self._candidate(_bad('Trace summariʹe'), _read('Trace summariʹe'))

    def test_r16_36_01_j_201_governed(self):
        self._candidate(_bad('Trace summariʺe'), _read('Trace summariʺe'))

    def test_r16_36_01_j_202_governed(self):
        self._candidate(_bad('Trace summariʻe'), _read('Trace summariʻe'))

    def test_r16_36_01_j_203_governed(self):
        self._candidate(_bad('Trace summariʼe'), _read('Trace summariʼe'))

    def test_r16_36_01_j_204_governed(self):
        self._candidate(_bad('Trace summariʽe'), _read('Trace summariʽe'))

    def test_r16_36_01_j_205_governed(self):
        self._candidate(_bad('Trace summariʾe'), _read('Trace summariʾe'))

    def test_r16_36_01_j_206_governed(self):
        self._candidate(_bad('Trace summariʿe'), _read('Trace summariʿe'))

    def test_r16_36_01_j_207_governed(self):
        self._candidate(_bad('Trace summariˀe'), _read('Trace summariˀe'))

    def test_r16_36_01_j_208_governed(self):
        self._candidate(_bad('Trace summariˁe'), _read('Trace summariˁe'))

    def test_r16_36_01_j_209_governed(self):
        self._candidate(_bad('Trace summari˂e'), _read('Trace summari˂e'))

    def test_r16_36_01_j_210_governed(self):
        self._candidate(_bad('Trace summari˃e'), _read('Trace summari˃e'))

    def test_r16_36_01_j_211_governed(self):
        self._candidate(_bad('Trace summari˄e'), _read('Trace summari˄e'))

    def test_r16_36_01_j_212_governed(self):
        self._candidate(_bad('Trace summari˅e'), _read('Trace summari˅e'))

    def test_r16_36_01_j_213_governed(self):
        self._candidate(_bad('Trace summariˆe'), _read('Trace summariˆe'))

    def test_r16_36_01_j_214_governed(self):
        self._candidate(_bad('Trace summariˇe'), _read('Trace summariˇe'))

    def test_r16_36_01_j_215_governed(self):
        self._candidate(_bad('Trace summariˈe'), _read('Trace summariˈe'))

    def test_r16_36_01_j_216_governed(self):
        self._candidate(_bad('Trace summariˉe'), _read('Trace summariˉe'))

    def test_r16_36_01_j_217_governed(self):
        self._candidate(_bad('Trace summariˊe'), _read('Trace summariˊe'))

    def test_r16_36_01_j_218_governed(self):
        self._candidate(_bad('Trace summariˋe'), _read('Trace summariˋe'))

    def test_r16_36_01_j_219_governed(self):
        self._candidate(_bad('Trace summariˌe'), _read('Trace summariˌe'))

    def test_r16_36_01_j_220_governed(self):
        self._candidate(_bad('Trace summariˍe'), _read('Trace summariˍe'))

    def test_r16_36_01_j_221_governed(self):
        self._candidate(_bad('Trace summariˎe'), _read('Trace summariˎe'))

    def test_r16_36_01_j_222_governed(self):
        self._candidate(_bad('Trace summariˏe'), _read('Trace summariˏe'))

    def test_r16_36_01_j_223_governed(self):
        self._candidate(_bad('Trace summariːe'), _read('Trace summariːe'))

    def test_r16_36_01_j_224_governed(self):
        self._candidate(_bad('Trace summariˑe'), _read('Trace summariˑe'))

    def test_r16_36_01_j_225_governed(self):
        self._candidate(_bad('Trace summari˒e'), _read('Trace summari˒e'))

    def test_r16_36_01_j_226_governed(self):
        self._candidate(_bad('Trace summari˓e'), _read('Trace summari˓e'))

    def test_r16_36_01_j_227_governed(self):
        self._candidate(_bad('Trace summari˔e'), _read('Trace summari˔e'))

    def test_r16_36_01_j_228_governed(self):
        self._candidate(_bad('Trace summari˕e'), _read('Trace summari˕e'))

    def test_r16_36_01_j_229_governed(self):
        self._candidate(_bad('Trace summari˖e'), _read('Trace summari˖e'))

    def test_r16_36_01_j_230_governed(self):
        self._candidate(_bad('Trace summari˗e'), _read('Trace summari˗e'))

    def test_r16_36_01_j_231_governed(self):
        self._candidate(_bad('Trace summari˘e'), _read('Trace summari˘e'))

    def test_r16_36_01_j_232_governed(self):
        self._candidate(_bad('Trace summari˙e'), _read('Trace summari˙e'))

    def test_r16_36_01_j_233_governed(self):
        self._candidate(_bad('Trace summari˚e'), _read('Trace summari˚e'))

    def test_r16_36_01_j_234_governed(self):
        self._candidate(_bad('Trace summari˛e'), _read('Trace summari˛e'))

    def test_r16_36_01_j_235_governed(self):
        self._candidate(_bad('Trace summari˜e'), _read('Trace summari˜e'))

    def test_r16_36_01_j_236_governed(self):
        self._candidate(_bad('Trace summari˝e'), _read('Trace summari˝e'))

    def test_r16_36_01_j_237_governed(self):
        self._candidate(_bad('Trace summari˞e'), _read('Trace summari˞e'))

    def test_r16_36_01_j_238_governed(self):
        self._candidate(_bad('Trace summari˟e'), _read('Trace summari˟e'))

    def test_r16_36_01_j_239_governed(self):
        self._candidate(_bad('Trace summariˠe'), _read('Trace summariˠe'))

    def test_r16_36_01_j_240_governed(self):
        self._candidate(_bad('Trace summarisʱ'), _read('Trace summarisʱ'))

    def test_r16_36_01_j_241_governed(self):
        self._candidate(_bad('Trace summarisʲ'), _read('Trace summarisʲ'))

    def test_r16_36_01_j_242_governed(self):
        self._candidate(_bad('Trace summarisʳ'), _read('Trace summarisʳ'))

    def test_r16_36_01_j_243_governed(self):
        self._candidate(_bad('Trace summarisʴ'), _read('Trace summarisʴ'))

    def test_r16_36_01_j_244_governed(self):
        self._candidate(_bad('Trace summarisʵ'), _read('Trace summarisʵ'))

    def test_r16_36_01_j_245_governed(self):
        self._candidate(_bad('Trace summarisʶ'), _read('Trace summarisʶ'))

    def test_r16_36_01_j_246_governed(self):
        self._candidate(_bad('Trace summarisʷ'), _read('Trace summarisʷ'))

    def test_r16_36_01_j_247_governed(self):
        self._candidate(_bad('Trace summarisʸ'), _read('Trace summarisʸ'))

    def test_r16_36_01_j_248_governed(self):
        self._candidate(_bad('Trace summarisʹ'), _read('Trace summarisʹ'))

    def test_r16_36_01_j_249_governed(self):
        self._candidate(_bad('Trace summarisʺ'), _read('Trace summarisʺ'))

    def test_r16_36_01_j_250_governed(self):
        self._candidate(_bad('Trace summarisʻ'), _read('Trace summarisʻ'))

    def test_r16_36_01_j_251_governed(self):
        self._candidate(_bad('Trace summarisʼ'), _read('Trace summarisʼ'))

    def test_r16_36_01_j_252_governed(self):
        self._candidate(_bad('Trace summarisʽ'), _read('Trace summarisʽ'))

    def test_r16_36_01_j_253_governed(self):
        self._candidate(_bad('Trace summarisʾ'), _read('Trace summarisʾ'))

    def test_r16_36_01_j_254_governed(self):
        self._candidate(_bad('Trace summarisʿ'), _read('Trace summarisʿ'))

    def test_r16_36_01_j_255_governed(self):
        self._candidate(_bad('Trace summarisˀ'), _read('Trace summarisˀ'))

    def test_r16_36_01_j_256_governed(self):
        self._candidate(_bad('Trace summarisˁ'), _read('Trace summarisˁ'))

    def test_r16_36_01_j_257_governed(self):
        self._candidate(_bad('Trace summaris˂'), _read('Trace summaris˂'))

    def test_r16_36_01_j_258_governed(self):
        self._candidate(_bad('Trace summaris˃'), _read('Trace summaris˃'))

    def test_r16_36_01_j_259_governed(self):
        self._candidate(_bad('Trace summaris˄'), _read('Trace summaris˄'))

    def test_r16_36_01_j_260_governed(self):
        self._candidate(_bad('Trace summaris˅'), _read('Trace summaris˅'))

    def test_r16_36_01_j_261_governed(self):
        self._candidate(_bad('Trace summarisˆ'), _read('Trace summarisˆ'))

    def test_r16_36_01_j_262_governed(self):
        self._candidate(_bad('Trace summarisˇ'), _read('Trace summarisˇ'))

    def test_r16_36_01_j_263_governed(self):
        self._candidate(_bad('Trace summarisˈ'), _read('Trace summarisˈ'))

    def test_r16_36_01_j_264_governed(self):
        self._candidate(_bad('Trace summarisˉ'), _read('Trace summarisˉ'))

    def test_r16_36_01_j_265_governed(self):
        self._candidate(_bad('Trace summarisˊ'), _read('Trace summarisˊ'))

    def test_r16_36_01_j_266_governed(self):
        self._candidate(_bad('Trace summarisˋ'), _read('Trace summarisˋ'))

    def test_r16_36_01_j_267_governed(self):
        self._candidate(_bad('Trace summarisˌ'), _read('Trace summarisˌ'))

    def test_r16_36_01_j_268_governed(self):
        self._candidate(_bad('Trace summarisˍ'), _read('Trace summarisˍ'))

    def test_r16_36_01_j_269_governed(self):
        self._candidate(_bad('Trace summarisˎ'), _read('Trace summarisˎ'))

    def test_r16_36_01_j_270_governed(self):
        self._candidate(_bad('Trace summarisˏ'), _read('Trace summarisˏ'))

    def test_r16_36_01_j_271_governed(self):
        self._candidate(_bad('Trace summarisː'), _read('Trace summarisː'))

    def test_r16_36_01_j_272_governed(self):
        self._candidate(_bad('Trace summarisˑ'), _read('Trace summarisˑ'))

    def test_r16_36_01_j_273_governed(self):
        self._candidate(_bad('Trace summaris˒'), _read('Trace summaris˒'))

    def test_r16_36_01_j_274_governed(self):
        self._candidate(_bad('Trace summaris˓'), _read('Trace summaris˓'))

    def test_r16_36_01_j_275_governed(self):
        self._candidate(_bad('Trace summaris˔'), _read('Trace summaris˔'))

    def test_r16_36_01_j_276_governed(self):
        self._candidate(_bad('Trace summaris˕'), _read('Trace summaris˕'))

    def test_r16_36_01_j_277_governed(self):
        self._candidate(_bad('Trace summaris˖'), _read('Trace summaris˖'))

    def test_r16_36_01_j_278_governed(self):
        self._candidate(_bad('Trace summaris˗'), _read('Trace summaris˗'))

    def test_r16_36_01_j_279_governed(self):
        self._candidate(_bad('Trace summaris˘'), _read('Trace summaris˘'))

    def test_r16_36_01_j_280_governed(self):
        self._candidate(_bad('Trace summaris˙'), _read('Trace summaris˙'))

    def test_r16_36_01_j_281_governed(self):
        self._candidate(_bad('Trace summaris˚'), _read('Trace summaris˚'))

    def test_r16_36_01_j_282_governed(self):
        self._candidate(_bad('Trace summaris˛'), _read('Trace summaris˛'))

    def test_r16_36_01_j_283_governed(self):
        self._candidate(_bad('Trace summaris˜'), _read('Trace summaris˜'))

    def test_r16_36_01_j_284_governed(self):
        self._candidate(_bad('Trace summaris˝'), _read('Trace summaris˝'))

    def test_r16_36_01_j_285_governed(self):
        self._candidate(_bad('Trace summaris˞'), _read('Trace summaris˞'))

    def test_r16_36_01_j_286_governed(self):
        self._candidate(_bad('Trace summaris˟'), _read('Trace summaris˟'))

    def test_r16_36_01_j_287_governed(self):
        self._candidate(_bad('Trace summarisˠ'), _read('Trace summarisˠ'))

    def test_r16_36_01_j_288_governed(self):
        self._candidate(_bad('Board taȺy'), _read('Board taȺy'))

    def test_r16_36_01_j_289_governed(self):
        self._candidate(_bad('Board ƛally'), _read('Board ƛally'))

    def test_r16_36_01_j_290_governed(self):
        self._candidate(_bad('Trace summaƛise'), _read('Trace summaƛise'))

    def test_r16_36_01_j_291_governed(self):
        self._candidate(_bad('Trace summaǲise'), _read('Trace summaǲise'))

    def test_r16_36_01_j_292_governed(self):
        self._candidate(_bad('Trace summaǂise'), _read('Trace summaǂise'))

    def test_r16_36_01_j_293_governed(self):
        self._candidate(_bad('Trace suȺmarise'), _read('Trace suȺmarise'))

    # Adopted assertions of the round 36 breaker exhibit, in the exhibit test names.

    def test_b36_sacramentarytally_beside(self):
            q4 = self._beside(_bad("Sacramentarytally"))
            assert_verdict(self, q4, "present", "Q-4")
            self.assertIn("totals 4 LANDED", q4)
            self.assertIn("Step 2", q4)
            self.assertIn("uncounted", q4)

    def test_b36_summarised_beside(self):
            q4 = self._beside(_bad('Trace summarisedeseseseseseseseseseseseseseseseseses'))
            assert_verdict(self, q4, "present", "Q-4")
            self.assertIn("totals 4 LANDED", q4)
            self.assertIn("Step 2", q4)
            self.assertIn("uncounted", q4)

    def test_b36_sacramentarytally_gate_ruling(self):
            report = self._q4_alone(_bad("Sacramentarytally"), ruling=True)
            self._assert_q4_governed(report, path=RULING_2)

    def test_b36_code_level_underreach_forms(self):
            for word in ("sacramentarytally", "sacramentariestallies",
                         "boardsacramentarytally", "tallye12", "boardtallyaz11"):
                self.assertTrue(_tally_word(_fold_word(word)), word)
            for word in ('summarisedeseseseseseseseseseseseseseseseseses', 'summaryeseseseseseseseseseseseseseseseseseses'):
                self.assertTrue(_summary_word(_fold_word(word)), word)
            for word in ('boardtracesummarisedeseseseseseseseseseseseseseseseseses', 'traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'):
                self.assertTrue(_fused_trace_summary(
                    _fold_word(word)), word)
            for head in ("Sacramentarytally",
                         'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board summary',
                         'Trace summarisedeseseseseseseseseseseseseseseseseses'):
                line = head + ": items checked stand here"
                self.assertTrue(_tally_statement_head(line), head)

    # Held controls of R16-36-02: every distinct converse form, standing missing.

    def test_control_converse_000_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel march trace summary')))

    def test_control_converse_001_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel stumble trace summary')))

    def test_control_converse_002_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel tumble trace summary')))

    def test_control_converse_003_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel teeter trace summary')))

    def test_control_converse_004_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel sway trace summary')))

    def test_control_converse_005_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel twirl trace summary')))

    def test_control_converse_006_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel crouch trace summary')))

    def test_control_converse_007_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel hop trace summary')))

    def test_control_converse_008_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel skip trace summary')))

    def test_control_converse_009_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel crawl trace summary')))

    def test_control_converse_010_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel roll trace summary')))

    def test_control_converse_011_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel bounce trace summary')))

    def test_control_converse_012_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel wheeze trace summary')))

    def test_control_converse_013_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel pant trace summary')))

    def test_control_converse_014_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel blush trace summary')))

    def test_control_converse_015_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel yell trace summary')))

    def test_control_converse_016_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel cheer trace summary')))

    def test_control_converse_017_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel point trace summary')))

    def test_control_converse_018_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel beckon trace summary')))

    def test_control_converse_019_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel salute trace summary')))

    def test_control_converse_020_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel curtsy trace summary')))

    def test_control_converse_021_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel sidestep trace summary')))

    def test_control_converse_022_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel backtrack trace summary')))

    def test_control_converse_023_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel wander trace summary')))

    def test_control_converse_024_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel stroll trace summary')))

    def test_control_converse_025_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel saunter trace summary')))

    def test_control_converse_026_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel trudge trace summary')))

    def test_control_converse_027_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel plod trace summary')))

    def test_control_converse_028_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel dash trace summary')))

    def test_control_converse_029_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel sprint trace summary')))

    def test_control_converse_030_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel race trace summary')))

    def test_control_converse_031_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel chase trace summary')))

    def test_control_converse_032_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel listen trace summary')))

    def test_control_converse_033_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel taste trace summary')))

    def test_control_converse_034_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel touch trace summary')))

    def test_control_converse_035_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel grip trace summary')))

    def test_control_converse_036_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel hit trace summary')))

    def test_control_converse_037_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Clerk keel summary trace')))

    def test_control_converse_038_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Team reel trace summary')))

    def test_control_converse_039_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel stagger summary trace')))

    def test_control_converse_040_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Clerk totter trace summary')))

    def test_control_converse_041_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Team teeter summary trace')))

    def test_control_converse_042_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel march tracesummary')))

    def test_control_converse_043_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel stumble tracesummary')))

    def test_control_converse_044_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel tumble tracesummary')))

    def test_control_converse_045_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel teeter tracesummary')))

    def test_control_converse_046_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel sway tracesummary')))

    def test_control_converse_047_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel twirl tracesummary')))

    def test_control_converse_048_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel crouch tracesummary')))

    def test_control_converse_049_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel hop tracesummary')))

    def test_control_converse_050_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel skip tracesummary')))

    def test_control_converse_051_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel crawl tracesummary')))

    def test_control_converse_052_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel roll tracesummary')))

    def test_control_converse_053_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel bounce tracesummary')))

    def test_control_converse_054_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel wheeze tracesummary')))

    def test_control_converse_055_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel pant tracesummary')))

    def test_control_converse_056_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel blush tracesummary')))

    def test_control_converse_057_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel yell tracesummary')))

    def test_control_converse_058_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel cheer tracesummary')))

    def test_control_converse_059_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel point tracesummary')))

    def test_control_converse_060_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel beckon tracesummary')))

    def test_control_converse_061_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel salute tracesummary')))

    def test_control_converse_062_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel curtsy tracesummary')))

    def test_control_converse_063_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel sidestep tracesummary')))

    def test_control_converse_064_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel backtrack tracesummary')))

    def test_control_converse_065_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel wander tracesummary')))

    def test_control_converse_066_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel stroll tracesummary')))

    def test_control_converse_067_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel saunter tracesummary')))

    def test_control_converse_068_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel trudge tracesummary')))

    def test_control_converse_069_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel plod tracesummary')))

    def test_control_converse_070_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel dash tracesummary')))

    def test_control_converse_071_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel sprint tracesummary')))

    def test_control_converse_072_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel race tracesummary')))

    def test_control_converse_073_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel chase tracesummary')))

    def test_control_converse_074_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel listen tracesummary')))

    def test_control_converse_075_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel taste tracesummary')))

    def test_control_converse_076_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel touch tracesummary')))

    def test_control_converse_077_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel grip tracesummary')))

    def test_control_converse_078_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel hit tracesummary')))

    def test_control_converse_079_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Clerk keel summarytrace')))

    def test_control_converse_080_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Team reel boardtracesummary')))

    def test_control_converse_081_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel stagger traceboardgatesummary')))

    def test_control_converse_082_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Clerk wheeze traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_converse_083_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Team keel tracesummarisationeseseseseseseseseseseseseseseseseses')))

    def test_control_converse_084_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a70 trace summary')))

    def test_control_converse_085_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a71 trace summary')))

    def test_control_converse_086_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a72 trace summary')))

    def test_control_converse_087_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a73 trace summary')))

    def test_control_converse_088_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a74 trace summary')))

    def test_control_converse_089_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a75 trace summary')))

    def test_control_converse_090_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a76 trace summary')))

    def test_control_converse_091_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a77 trace summary')))

    def test_control_converse_092_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a78 trace summary')))

    def test_control_converse_093_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a79 trace summary')))

    def test_control_converse_094_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a7a trace summary')))

    def test_control_converse_095_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a7b trace summary')))

    def test_control_converse_096_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a7c trace summary')))

    def test_control_converse_097_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a7d trace summary')))

    def test_control_converse_098_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a7e trace summary')))

    def test_control_converse_099_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a7f trace summary')))

    def test_control_converse_100_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a80 trace summary')))

    def test_control_converse_101_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a81 trace summary')))

    def test_control_converse_102_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a82 trace summary')))

    def test_control_converse_103_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a83 trace summary')))

    def test_control_converse_104_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a84 trace summary')))

    def test_control_converse_105_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a85 trace summary')))

    def test_control_converse_106_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a86 trace summary')))

    def test_control_converse_107_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a87 trace summary')))

    def test_control_converse_108_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a88 trace summary')))

    def test_control_converse_109_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a89 trace summary')))

    def test_control_converse_110_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a8a trace summary')))

    def test_control_converse_111_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a8b trace summary')))

    def test_control_converse_112_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a8c trace summary')))

    def test_control_converse_113_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a8d trace summary')))

    def test_control_converse_114_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a8e trace summary')))

    def test_control_converse_115_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a8f trace summary')))

    def test_control_converse_116_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a90 trace summary')))

    def test_control_converse_117_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a91 trace summary')))

    def test_control_converse_118_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a92 trace summary')))

    def test_control_converse_119_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a93 trace summary')))

    def test_control_converse_120_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a94 trace summary')))

    def test_control_converse_121_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a95 trace summary')))

    def test_control_converse_122_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a96 trace summary')))

    def test_control_converse_123_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a97 trace summary')))

    def test_control_converse_124_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a98 trace summary')))

    def test_control_converse_125_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a99 trace summary')))

    def test_control_converse_126_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a9a trace summary')))

    def test_control_converse_127_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a9b trace summary')))

    def test_control_converse_128_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a9c trace summary')))

    def test_control_converse_129_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a9d trace summary')))

    def test_control_converse_130_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a9e trace summary')))

    def test_control_converse_131_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a9f trace summary')))

    def test_control_converse_132_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aa0 trace summary')))

    def test_control_converse_133_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aa1 trace summary')))

    def test_control_converse_134_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aa2 trace summary')))

    def test_control_converse_135_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aa3 trace summary')))

    def test_control_converse_136_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aa4 trace summary')))

    def test_control_converse_137_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aa5 trace summary')))

    def test_control_converse_138_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aa6 trace summary')))

    def test_control_converse_139_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aa7 trace summary')))

    def test_control_converse_140_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aa8 trace summary')))

    def test_control_converse_141_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aa9 trace summary')))

    def test_control_converse_142_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aaa trace summary')))

    def test_control_converse_143_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aab trace summary')))

    def test_control_converse_144_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aac trace summary')))

    def test_control_converse_145_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aad trace summary')))

    def test_control_converse_146_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aae trace summary')))

    def test_control_converse_147_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aaf trace summary')))

    def test_control_converse_148_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ab0 trace summary')))

    def test_control_converse_149_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ab1 trace summary')))

    def test_control_converse_150_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ab2 trace summary')))

    def test_control_converse_151_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ab3 trace summary')))

    def test_control_converse_152_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ab4 trace summary')))

    def test_control_converse_153_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ab5 trace summary')))

    def test_control_converse_154_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ab6 trace summary')))

    def test_control_converse_155_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ab7 trace summary')))

    def test_control_converse_156_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ab8 trace summary')))

    def test_control_converse_157_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ab9 trace summary')))

    def test_control_converse_158_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aba trace summary')))

    def test_control_converse_159_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2abb trace summary')))

    def test_control_converse_160_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2abc trace summary')))

    def test_control_converse_161_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2abd trace summary')))

    def test_control_converse_162_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2abe trace summary')))

    def test_control_converse_163_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2abf trace summary')))

    def test_control_converse_164_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ac0 trace summary')))

    def test_control_converse_165_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ac1 trace summary')))

    def test_control_converse_166_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ac2 trace summary')))

    def test_control_converse_167_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ac3 trace summary')))

    def test_control_converse_168_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ac4 trace summary')))

    def test_control_converse_169_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ac5 trace summary')))

    def test_control_converse_170_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ac6 trace summary')))

    def test_control_converse_171_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ac7 trace summary')))

    def test_control_converse_172_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ac8 trace summary')))

    def test_control_converse_173_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ac9 trace summary')))

    def test_control_converse_174_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aca trace summary')))

    def test_control_converse_175_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2acb trace summary')))

    def test_control_converse_176_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2acc trace summary')))

    def test_control_converse_177_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2acd trace summary')))

    def test_control_converse_178_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ace trace summary')))

    def test_control_converse_179_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2acf trace summary')))

    def test_control_converse_180_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ad0 trace summary')))

    def test_control_converse_181_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ad1 trace summary')))

    def test_control_converse_182_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ad2 trace summary')))

    def test_control_converse_183_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ad3 trace summary')))

    def test_control_converse_184_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ad4 trace summary')))

    def test_control_converse_185_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ad5 trace summary')))

    def test_control_converse_186_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ad6 trace summary')))

    def test_control_converse_187_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ad7 trace summary')))

    def test_control_converse_188_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ad8 trace summary')))

    def test_control_converse_189_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ad9 trace summary')))

    def test_control_converse_190_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ada trace summary')))

    def test_control_converse_191_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2adb trace summary')))

    def test_control_converse_192_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2adc trace summary')))

    def test_control_converse_193_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2add trace summary')))

    def test_control_converse_194_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ade trace summary')))

    def test_control_converse_195_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2adf trace summary')))

    def test_control_converse_196_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ae0 trace summary')))

    def test_control_converse_197_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ae1 trace summary')))

    def test_control_converse_198_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ae2 trace summary')))

    def test_control_converse_199_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ae3 trace summary')))

    def test_control_converse_200_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ae4 trace summary')))

    def test_control_converse_201_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ae5 trace summary')))

    def test_control_converse_202_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ae6 trace summary')))

    def test_control_converse_203_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ae7 trace summary')))

    def test_control_converse_204_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ae8 trace summary')))

    def test_control_converse_205_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2ae9 trace summary')))

    def test_control_converse_206_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aea trace summary')))

    def test_control_converse_207_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aeb trace summary')))

    def test_control_converse_208_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aec trace summary')))

    def test_control_converse_209_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aed trace summary')))

    def test_control_converse_210_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aee trace summary')))

    def test_control_converse_211_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aef trace summary')))

    def test_control_converse_212_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2af0 trace summary')))

    def test_control_converse_213_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2af1 trace summary')))

    def test_control_converse_214_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2af2 trace summary')))

    def test_control_converse_215_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2af3 trace summary')))

    def test_control_converse_216_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2af4 trace summary')))

    def test_control_converse_217_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2af5 trace summary')))

    def test_control_converse_218_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2af6 trace summary')))

    def test_control_converse_219_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2af7 trace summary')))

    def test_control_converse_220_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2af8 trace summary')))

    def test_control_converse_221_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2af9 trace summary')))

    def test_control_converse_222_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2afa trace summary')))

    def test_control_converse_223_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2afb trace summary')))

    def test_control_converse_224_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2afc trace summary')))

    def test_control_converse_225_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2afd trace summary')))

    def test_control_converse_226_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2afe trace summary')))

    def test_control_converse_227_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2aff trace summary')))

    def test_control_converse_228_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe20 trace summary')))

    def test_control_converse_229_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe21 trace summary')))

    def test_control_converse_230_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe22 trace summary')))

    def test_control_converse_231_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe23 trace summary')))

    def test_control_converse_232_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe24 trace summary')))

    def test_control_converse_233_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe25 trace summary')))

    def test_control_converse_234_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe26 trace summary')))

    def test_control_converse_235_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe27 trace summary')))

    def test_control_converse_236_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe28 trace summary')))

    def test_control_converse_237_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe29 trace summary')))

    def test_control_converse_238_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe2a trace summary')))

    def test_control_converse_239_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe2b trace summary')))

    def test_control_converse_240_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe2c trace summary')))

    def test_control_converse_241_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe2d trace summary')))

    def test_control_converse_242_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe2e trace summary')))

    def test_control_converse_243_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \ufe2f trace summary')))

    def test_control_converse_244_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe20 trace summary')))

    def test_control_converse_245_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe21 trace summary')))

    def test_control_converse_246_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe22 trace summary')))

    def test_control_converse_247_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe23 trace summary')))

    def test_control_converse_248_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe24 trace summary')))

    def test_control_converse_249_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe25 trace summary')))

    def test_control_converse_250_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe26 trace summary')))

    def test_control_converse_251_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe27 trace summary')))

    def test_control_converse_252_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe28 trace summary')))

    def test_control_converse_253_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe29 trace summary')))

    def test_control_converse_254_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe2a trace summary')))

    def test_control_converse_255_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe2b trace summary')))

    def test_control_converse_256_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe2c trace summary')))

    def test_control_converse_257_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe2d trace summary')))

    def test_control_converse_258_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe2e trace summary')))

    def test_control_converse_259_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\ufe2f trace summary')))

    def test_control_converse_260_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u29d2 trace summary')))

    def test_control_converse_261_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2b32 trace summary')))

    def test_control_converse_262_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u20f1 trace summary')))

    def test_control_converse_263_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\u20f2 trace summary')))

    def test_control_converse_264_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e30panel\u2e31 trace summary')))

    def test_control_converse_265_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e32panel\u2e33 trace summary')))

    def test_control_converse_266_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e34panel\u2e35 trace summary')))

    def test_control_converse_267_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e36panel\u2e37 trace summary')))

    def test_control_converse_268_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e38panel\u2e39 trace summary')))

    def test_control_converse_269_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e3apanel\u2e3b trace summary')))

    def test_control_converse_270_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e3cpanel\u2e3d trace summary')))

    def test_control_converse_271_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e40panel\u2e41 trace summary')))

    def test_control_converse_272_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e42panel\u2e43 trace summary')))

    def test_control_converse_273_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e49panel\u2e4a trace summary')))

    def test_control_converse_274_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e4bpanel\u2e4c trace summary')))

    def test_control_converse_275_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e4dpanel\u2e4e trace summary')))

    def test_control_converse_276_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('March panel trace summary')))

    def test_control_converse_277_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Stumble panel trace summary')))

    def test_control_converse_278_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Tumble panel trace summary')))

    def test_control_converse_279_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Teeter panel trace summary')))

    def test_control_converse_280_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Sway panel trace summary')))

    def test_control_converse_281_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Twirl panel trace summary')))

    def test_control_converse_282_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Crouch panel trace summary')))

    def test_control_converse_283_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Hop panel trace summary')))

    def test_control_converse_284_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Skip panel trace summary')))

    def test_control_converse_285_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Crawl panel trace summary')))

    def test_control_converse_286_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Roll panel trace summary')))

    def test_control_converse_287_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Bounce panel trace summary')))

    def test_control_converse_288_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Wheeze panel trace summary')))

    def test_control_converse_289_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Pant panel trace summary')))

    def test_control_converse_290_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Blush panel trace summary')))

    def test_control_converse_291_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Yell panel trace summary')))

    def test_control_converse_292_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Cheer panel trace summary')))

    def test_control_converse_293_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Point panel trace summary')))

    def test_control_converse_294_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Beckon panel trace summary')))

    def test_control_converse_295_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Salute panel trace summary')))

    def test_control_converse_296_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Curtsy panel trace summary')))

    def test_control_converse_297_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Sidestep panel trace summary')))

    def test_control_converse_298_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Backtrack panel trace summary')))

    def test_control_converse_299_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Wander panel trace summary')))

    def test_control_converse_300_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Stroll panel trace summary')))

    def test_control_converse_301_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Saunter panel trace summary')))

    def test_control_converse_302_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Trudge panel trace summary')))

    def test_control_converse_303_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Plod panel trace summary')))

    def test_control_converse_304_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Dash panel trace summary')))

    def test_control_converse_305_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Sprint panel trace summary')))

    def test_control_converse_306_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Race panel trace summary')))

    def test_control_converse_307_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Chase panel trace summary')))

    def test_control_converse_308_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Listen panel trace summary')))

    def test_control_converse_309_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Taste panel trace summary')))

    def test_control_converse_310_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Touch panel trace summary')))

    def test_control_converse_311_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Grip panel trace summary')))

    def test_control_converse_312_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Hit panel trace summary')))

    def test_control_converse_313_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Wheeze ledger trace summary')))

    # Held controls of R16-36-02 named in the register, standing as they stood.

    def test_control_held_00_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel snore trace summary')))

    def test_control_held_01_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel chuckle trace summary')))

    def test_control_held_02_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel giggle trace summary')))

    def test_control_held_03_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel stare trace summary')))

    def test_control_held_04_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel glare trace summary')))

    def test_control_held_05_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel blink trace summary')))

    def test_control_held_06_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel wink trace summary')))

    def test_control_held_07_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel nod trace summary')))

    def test_control_held_08_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel shrug trace summary')))

    def test_control_held_09_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel whistle trace summary')))

    def test_control_held_10_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel sing trace summary')))

    def test_control_held_11_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel dance trace summary')))

    def test_control_held_12_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel stride trace summary')))

    def test_control_held_13_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel creep trace summary')))

    def test_control_held_14_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel limp trace summary')))

    def test_control_held_15_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel wobble trace summary')))

    def test_control_held_16_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel spin trace summary')))

    def test_control_held_17_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel bow trace summary')))

    def test_control_held_18_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel kneel trace summary')))

    def test_control_held_19_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel leap trace summary')))

    def test_control_held_20_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel jump trace summary')))

    def test_control_held_21_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel climb trace summary')))

    def test_control_held_22_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel slide trace summary')))

    def test_control_held_23_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel shake trace summary')))

    def test_control_held_24_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel shiver trace summary')))

    def test_control_held_25_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel quiver trace summary')))

    def test_control_held_26_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel cough trace summary')))

    def test_control_held_27_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel sneeze trace summary')))

    def test_control_held_28_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel yawn trace summary')))

    def test_control_held_29_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel hiccup trace summary')))

    def test_control_held_30_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel burp trace summary')))

    def test_control_held_31_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel smile trace summary')))

    def test_control_held_32_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel frown trace summary')))

    def test_control_held_33_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel laugh trace summary')))

    def test_control_held_34_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel weep trace summary')))

    def test_control_held_35_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel moan trace summary')))

    def test_control_held_36_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel groan trace summary')))

    def test_control_held_37_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel scream trace summary')))

    def test_control_held_38_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel shout trace summary')))

    def test_control_held_39_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel clap trace summary')))

    def test_control_held_40_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel wave trace summary')))

    def test_control_held_41_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel flee trace summary')))

    def test_control_held_42_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel hide trace summary')))

    def test_control_held_43_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel seek trace summary')))

    def test_control_held_44_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel watch trace summary')))

    def test_control_held_45_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel smell trace summary')))

    def test_control_held_46_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel feel trace summary')))

    def test_control_held_47_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel think trace summary')))

    def test_control_held_48_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel dream trace summary')))

    def test_control_held_49_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel doze trace summary')))

    def test_control_held_50_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel nap trace summary')))

    def test_control_held_51_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel wake trace summary')))

    def test_control_held_52_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel rise trace summary')))

    def test_control_held_53_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel sit trace summary')))

    def test_control_held_54_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel stand trace summary')))

    def test_control_held_55_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel lie trace summary')))

    def test_control_held_56_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel lean trace summary')))

    def test_control_held_57_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel bend trace summary')))

    def test_control_held_58_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel stretch trace summary')))

    def test_control_held_59_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel reach trace summary')))

    def test_control_held_60_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel grasp trace summary')))

    def test_control_held_61_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel hold trace summary')))

    def test_control_held_62_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel carry trace summary')))

    def test_control_held_63_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel lift trace summary')))

    def test_control_held_64_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel push trace summary')))

    def test_control_held_65_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel pull trace summary')))

    def test_control_held_66_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel drag trace summary')))

    def test_control_held_67_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel throw trace summary')))

    def test_control_held_68_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel catch trace summary')))

    def test_control_held_69_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel kick trace summary')))

    def test_control_held_70_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel strike trace summary')))

    def test_control_held_71_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel smirk trace summary')))

    def test_control_held_72_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Panel sob trace summary')))

    def test_control_sign_00_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a50 trace summary')))

    def test_control_sign_01_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a51 trace summary')))

    def test_control_sign_02_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a52 trace summary')))

    def test_control_sign_03_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a53 trace summary')))

    def test_control_sign_04_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a54 trace summary')))

    def test_control_sign_05_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a55 trace summary')))

    def test_control_sign_06_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a56 trace summary')))

    def test_control_sign_07_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a57 trace summary')))

    def test_control_sign_08_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a58 trace summary')))

    def test_control_sign_09_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a59 trace summary')))

    def test_control_sign_10_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a5a trace summary')))

    def test_control_sign_11_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a5b trace summary')))

    def test_control_sign_12_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a5c trace summary')))

    def test_control_sign_13_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a5d trace summary')))

    def test_control_sign_14_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a5e trace summary')))

    def test_control_sign_15_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a5f trace summary')))

    def test_control_sign_16_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a60 trace summary')))

    def test_control_sign_17_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a61 trace summary')))

    def test_control_sign_18_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a62 trace summary')))

    def test_control_sign_19_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a63 trace summary')))

    def test_control_sign_20_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a64 trace summary')))

    def test_control_sign_21_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a65 trace summary')))

    def test_control_sign_22_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a66 trace summary')))

    def test_control_sign_23_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a67 trace summary')))

    def test_control_sign_24_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a68 trace summary')))

    def test_control_sign_25_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a69 trace summary')))

    def test_control_sign_26_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a6a trace summary')))

    def test_control_sign_27_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a6b trace summary')))

    def test_control_sign_28_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a6c trace summary')))

    def test_control_sign_29_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a6d trace summary')))

    def test_control_sign_30_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a6e trace summary')))

    def test_control_sign_31_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2a6f trace summary')))

    def test_control_comb_00_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u20ea trace summary')))

    def test_control_comb_01_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u20eb trace summary')))

    def test_control_comb_02_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u20ec trace summary')))

    def test_control_comb_03_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u20ed trace summary')))

    def test_control_comb_04_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u20ee trace summary')))

    def test_control_comb_05_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u20ef trace summary')))

    def test_control_comb_06_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u20f0 trace summary')))

    def test_control_comb_07_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\u20ea trace summary')))

    def test_control_comb_08_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\u20eb trace summary')))

    def test_control_comb_09_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\u20ec trace summary')))

    def test_control_comb_10_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\u20ed trace summary')))

    def test_control_comb_11_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\u20ee trace summary')))

    def test_control_comb_12_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\u20ef trace summary')))

    def test_control_comb_13_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger x\u20f0 trace summary')))

    def test_control_aside_00_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e47panel\u2e48 trace summary')))

    def test_control_aside_01_missing(self):
            self._assert_q4_missing(self._q4_alone(
                _prose('Ledger \u2e5dpanel\u2e5e trace summary')))

    def test_control_governed_00_governed(self):
            self._candidate_governed(_bad('Trace summary'), _read('Trace summary'))

    def test_control_governed_01_governed(self):
            self._candidate_governed(_bad('Summary trace'), _read('Summary trace'))

    def test_control_governed_02_governed(self):
            self._candidate_governed(_bad('Tracesummary'), _read('Tracesummary'))

    def test_control_governed_03_governed(self):
            self._candidate_governed(_bad('Boardtracesummary'), _read('Boardtracesummary'))

    def test_control_governed_04_governed(self):
            self._candidate_governed(_bad('Trace board summary'), _read('Trace board summary'))

    def test_control_governed_05_governed(self):
            self._candidate_governed(_bad('Trace board gate summary'), _read('Trace board gate summary'))

    def test_control_governed_06_governed(self):
            self._candidate_governed(_bad('Alpha beta gamma delta epsilon trace summary'), _read('Alpha beta gamma delta epsilon trace summary'))

    def test_control_governed_07_governed(self):
            self._candidate_governed(_bad('Round\'s trace summary'), _read('Round\'s trace summary'))

    # Held governed forms of R16-36-01, standing governed: the governed neighbours of both papers.

    def test_control_underheld_000_governed(self):
        self._candidate(_bad('Breviarytally'), _read('Breviarytally'))

    def test_control_underheld_001_governed(self):
        self._candidate(_bad('Psaltertally'), _read('Psaltertally'))

    def test_control_underheld_002_governed(self):
        self._candidate(_bad('Lectionarytally'), _read('Lectionarytally'))

    def test_control_underheld_003_governed(self):
        self._candidate(_bad('Missaltally'), _read('Missaltally'))

    def test_control_underheld_004_governed(self):
        self._candidate(_bad('Diurnaltallies'), _read('Diurnaltallies'))

    def test_control_underheld_005_governed(self):
        self._candidate(_bad('Gradualtally'), _read('Gradualtally'))

    def test_control_underheld_006_governed(self):
        self._candidate(_bad('Diurnaltally'), _read('Diurnaltally'))

    def test_control_underheld_007_governed(self):
        self._candidate(_bad('Boardbreviarytallye'), _read('Boardbreviarytallye'))

    def test_control_underheld_008_governed(self):
        self._candidate(_bad('Tallye11'), _read('Tallye11'))

    def test_control_underheld_009_governed(self):
        self._candidate(_bad('Boardtallye11'), _read('Boardtallye11'))

    def test_control_underheld_010_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary'))

    def test_control_underheld_011_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatetrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatetrace'))

    def test_control_underheld_012_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary'))

    def test_control_underheld_013_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel summary'))

    def test_control_underheld_014_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel trace'))

    def test_control_underheld_015_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel for step 2'))

    def test_control_underheld_016_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseseseseseseses'))

    def test_control_underheld_017_governed(self):
        self._candidate(_bad('Trace summarisingeseseseseseseseseseseseseseseseses'), _read('Trace summarisingeseseseseseseseseseseseseseseseses'))

    def test_control_underheld_018_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseseseseseses'))

    def test_control_underheld_019_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseseseseseses'))

    def test_control_underheld_020_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseseseseseses'))

    def test_control_underheld_021_governed(self):
        self._candidate(_bad('Trace summaryeseseseseseseseseseseseseseseseseses'), _read('Trace summaryeseseseseseseseseseseseseseseseseses'))

    def test_control_underheld_022_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseseseseseses'))

    def test_control_underheld_023_governed(self):
        self._candidate(_bad('Boardtracesummarisereseseseseseseseseseseseseseseseses'), _read('Boardtracesummarisereseseseseseseseseseseseseseseseses'))

    def test_control_underheld_024_governed(self):
        self._candidate(_bad('Tracessummarieseseseseseseseseseseseseseseseseses'), _read('Tracessummarieseseseseseseseseseseseseseseseseses'))

    def test_control_underheld_025_governed(self):
        self._candidate(_bad('Boardtracesummarisedeseseseseseseseseseseseseseseseses'), _read('Boardtracesummarisedeseseseseseseseseseseseseseseseses'))

    def test_control_underheld_026_governed(self):
        self._candidate(_bad('Tracessummaryeseseseseseseseseseseseseseseseseses'), _read('Tracessummaryeseseseseseseseseseseseseseseseseses'))

    def test_control_underheld_027_governed(self):
        self._candidate(_bad('Board Ȼally'), _read('Board Ȼally'))

    def test_control_underheld_028_governed(self):
        self._candidate(_bad('Trace summaȻise'), _read('Trace summaȻise'))

    def test_control_underheld_029_governed(self):
        self._candidate(_bad('Board taȻy'), _read('Board taȻy'))

    def test_control_underheld_030_governed(self):
        self._candidate(_bad('Board ƚally'), _read('Board ƚally'))

    def test_control_underheld_031_governed(self):
        self._candidate(_bad('Trace summaƚise'), _read('Trace summaƚise'))

    def test_control_underheld_032_governed(self):
        self._candidate(_bad('Trace suǲmarise'), _read('Trace suǲmarise'))



if __name__ == "__main__":
    import unittest
    unittest.main()
