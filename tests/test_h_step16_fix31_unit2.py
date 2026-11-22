"""Step 16 fix pass 31 unit 2 tests: the Q-4 closing unit.

Pinning tests for register item R16-31-01 (Medium,
B31-C01 and B31-B01) of Step 16 round 31. The governing
rule of the pass, in its extended form: a piece not
read in full, for whatever reason, is not read, and its
converse: a piece that is no feeder flips nothing.

R16-31-01: malformed tally statement heads standing
unread past the restated boundary of fix pass 30, on
the counted pattern head agnosticism ground alone: the
pattern standing counted over a plain whole word
pattern, so a malformed head whose counted sibling
counts stands missing in the row although it stands as
a feeder statement in a form the row cannot parse. Two
hundred and eight distinct alone forms stand driven in
ten subfamilies: (a) tally forms fused behind record
words no widening has named and behind head words in
the inverse positions, forty seven forms; (b)
composite openings built on those forms, fourteen
forms; (c) a variant spelling in that composite
opening position, eight forms; (d) the variant
spellings past the widened variant sets of seventy
eight and seventy nine, fourteen forms; (e) the
summary word in further forms past the one hundred and
nineteen, seven forms; (f) the fused closings built on
those forms, four forms; (g) the fused closings with
eighteen governed words of subject between, three
forms; (h) the inserted closings with twenty one words
of subject between in their wide, middle swap and full
swap shapes in both directions, six forms; (i) the for
step closing with twenty one words of subject between,
one form; and (j) further phi, theta, eth, eng and
kindred letters and further Latin letters past the
widened fold set, each standing in a position the
folding does not read, one hundred and four forms. The
fifty five underreach assertions of the round 31
breaker exhibit stand adopted in this module: the
fifty one alone form assertions of B31-B01 stand among
the defect tests of the subfamilies above in their
driven words, and the beside assertions, the gate
ruling assertion and the code level assertion of that
exhibit stand as defect tests here in the forms the
exhibit names them. The defect stands bounded in the
open by its held controls: every form of R16-31-02
standing missing, every held form of that item standing
missing in its recorded form, every governed closing
of that item standing governed, and on the underreach
side the governed neighbours of both papers standing
governed, the plain fused controls Abstracttally and
Placardtally, the governed variant composite openings
Boarddictionarytallye and Gatevocabularytalliez, the
twenty four governed letter forms of the correctness
paper beside the candidate letter Trace forms,
Songbooktally and Songbookstallies, the widest
summarisation form standing governed in the widened
enumeration, the seventeen word fused between closing,
the twenty word forward and reversed inserted closings
and the twenty word for step closing standing
governed, and the fix pass 30 forms standing governed
in their positions. Locus: derivation_core.py,
_tally_statement_head and its standing helpers and
constants. The cure these tests pin widens what a
malformed tally statement head is in standing: the
governed fused prefix set widened by the record words
of this round, the variant sets widened by the
spellings of this round, the summary word set widened
by the further forms of this round, the fused between
reach widened to eighteen governed words, the inserted
closings standing at twenty one words forward, twenty
one words reversed and twenty one words in the for
step form under the wide test, and the folding widened
by the whole word readings of this round, so every
driven form stands governed beside its counted sibling
while every control stands as it stood.
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


class TestStep16Fix31Unit2(FixtureTestCase):

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
    # Defect forms of R16-31-01, subfamily (a):
    # fused record words and inverse positions.
    # ------------------------------------------------------

    def test_r16_31_01_a_00_governed(self):
        self._candidate(_bad('Tabloidtally'), _read('Tabloidtally'))

    def test_r16_31_01_a_01_governed(self):
        self._candidate(_bad('Tabloidstallies'), _read('Tabloidstallies'))

    def test_r16_31_01_a_02_governed(self):
        self._candidate(_bad('Whitepapertally'), _read('Whitepapertally'))

    def test_r16_31_01_a_03_governed(self):
        self._candidate(_bad('Whitepaperstallies'), _read('Whitepaperstallies'))

    def test_r16_31_01_a_04_governed(self):
        self._candidate(_bad('Playbilltally'), _read('Playbilltally'))

    def test_r16_31_01_a_05_governed(self):
        self._candidate(_bad('Playbillstallies'), _read('Playbillstallies'))

    def test_r16_31_01_a_06_governed(self):
        self._candidate(_bad('Essaytally'), _read('Essaytally'))

    def test_r16_31_01_a_07_governed(self):
        self._candidate(_bad('Essaystallies'), _read('Essaystallies'))

    def test_r16_31_01_a_08_governed(self):
        self._candidate(_bad('Thesistally'), _read('Thesistally'))

    def test_r16_31_01_a_09_governed(self):
        self._candidate(_bad('Screenplaytally'), _read('Screenplaytally'))

    def test_r16_31_01_a_10_governed(self):
        self._candidate(_bad('Hymnaltally'), _read('Hymnaltally'))

    def test_r16_31_01_a_11_governed(self):
        self._candidate(_bad('Missaltally'), _read('Missaltally'))

    def test_r16_31_01_a_12_governed(self):
        self._candidate(_bad('Psaltertally'), _read('Psaltertally'))

    def test_r16_31_01_a_13_governed(self):
        self._candidate(_bad('Breviarytally'), _read('Breviarytally'))

    def test_r16_31_01_a_14_governed(self):
        self._candidate(_bad('Preprinttally'), _read('Preprinttally'))

    def test_r16_31_01_a_15_governed(self):
        self._candidate(_bad('Reprinttally'), _read('Reprinttally'))

    def test_r16_31_01_a_16_governed(self):
        self._candidate(_bad('Offprinttally'), _read('Offprinttally'))

    def test_r16_31_01_a_17_governed(self):
        self._candidate(_bad('Sermontally'), _read('Sermontally'))

    def test_r16_31_01_a_18_governed(self):
        self._candidate(_bad('Lecturetally'), _read('Lecturetally'))

    def test_r16_31_01_a_19_governed(self):
        self._candidate(_bad('Bookmarktally'), _read('Bookmarktally'))

    def test_r16_31_01_a_20_governed(self):
        self._candidate(_bad('Opustally'), _read('Opustally'))

    def test_r16_31_01_a_21_governed(self):
        self._candidate(_bad('Librettotally'), _read('Librettotally'))

    def test_r16_31_01_a_22_governed(self):
        self._candidate(_bad('Memorandatallies'), _read('Memorandatallies'))

    def test_r16_31_01_a_23_governed(self):
        self._candidate(_bad('Phenomenontally'), _read('Phenomenontally'))

    def test_r16_31_01_a_24_governed(self):
        self._candidate(_bad('Phenomenatallies'), _read('Phenomenatallies'))

    def test_r16_31_01_a_25_governed(self):
        self._candidate(_bad('Criteriontally'), _read('Criteriontally'))

    def test_r16_31_01_a_26_governed(self):
        self._candidate(_bad('Criteriatallies'), _read('Criteriatallies'))

    def test_r16_31_01_a_27_governed(self):
        self._candidate(_bad('Erratumtally'), _read('Erratumtally'))

    def test_r16_31_01_a_28_governed(self):
        self._candidate(_bad('Erratatallies'), _read('Erratatallies'))

    def test_r16_31_01_a_29_governed(self):
        self._candidate(_bad('Datumtally'), _read('Datumtally'))

    def test_r16_31_01_a_30_governed(self):
        self._candidate(_bad('Datatallies'), _read('Datatallies'))

    def test_r16_31_01_a_31_governed(self):
        self._candidate(_bad('Forumtally'), _read('Forumtally'))

    def test_r16_31_01_a_32_governed(self):
        self._candidate(_bad('Foratallies'), _read('Foratallies'))

    def test_r16_31_01_a_33_governed(self):
        self._candidate(_bad('Mediumtally'), _read('Mediumtally'))

    def test_r16_31_01_a_34_governed(self):
        self._candidate(_bad('Mediatallies'), _read('Mediatallies'))

    def test_r16_31_01_a_35_governed(self):
        self._candidate(_bad('Epistletally'), _read('Epistletally'))

    def test_r16_31_01_a_36_governed(self):
        self._candidate(_bad('Missivetally'), _read('Missivetally'))

    def test_r16_31_01_a_37_governed(self):
        self._candidate(_bad('Tablettally'), _read('Tablettally'))

    def test_r16_31_01_a_38_governed(self):
        self._candidate(_bad('Plaquetally'), _read('Plaquetally'))

    def test_r16_31_01_a_39_governed(self):
        self._candidate(_bad('Quiretally'), _read('Quiretally'))

    def test_r16_31_01_a_40_governed(self):
        self._candidate(_bad('Epistlestallies'), _read('Epistlestallies'))

    def test_r16_31_01_a_41_governed(self):
        self._candidate(_bad('Missivestallies'), _read('Missivestallies'))

    def test_r16_31_01_a_42_governed(self):
        self._candidate(_bad('Tabletstallies'), _read('Tabletstallies'))

    def test_r16_31_01_a_43_governed(self):
        self._candidate(_bad('Plaquestallies'), _read('Plaquestallies'))

    def test_r16_31_01_a_44_governed(self):
        self._candidate(_bad('Quirestallies'), _read('Quirestallies'))

    def test_r16_31_01_a_45_governed(self):
        self._candidate(_bad('Fasciclestallies'), _read('Fasciclestallies'))

    def test_r16_31_01_a_46_governed(self):
        self._candidate(_bad('Flagtally'), _read('Flagtally'))

    # ------------------------------------------------------
    # Defect forms of R16-31-01, subfamily (b):
    # composite openings.
    # ------------------------------------------------------

    def test_r16_31_01_b_00_governed(self):
        self._candidate(_bad('Boardtabloidtally'), _read('Boardtabloidtally'))

    def test_r16_31_01_b_01_governed(self):
        self._candidate(_bad('Boardessaystallies'), _read('Boardessaystallies'))

    def test_r16_31_01_b_02_governed(self):
        self._candidate(_bad('Boardwhitepapertally'), _read('Boardwhitepapertally'))

    def test_r16_31_01_b_03_governed(self):
        self._candidate(_bad('Boardthesistally'), _read('Boardthesistally'))

    def test_r16_31_01_b_04_governed(self):
        self._candidate(_bad('Gateplaybilltally'), _read('Gateplaybilltally'))

    def test_r16_31_01_b_05_governed(self):
        self._candidate(_bad('Boardphenomenatallies'), _read('Boardphenomenatallies'))

    def test_r16_31_01_b_06_governed(self):
        self._candidate(_bad('Boardmemorandatallies'), _read('Boardmemorandatallies'))

    def test_r16_31_01_b_07_governed(self):
        self._candidate(_bad('Reviewhymnaltally'), _read('Reviewhymnaltally'))

    def test_r16_31_01_b_08_governed(self):
        self._candidate(_bad('Boardcriteriatallies'), _read('Boardcriteriatallies'))

    def test_r16_31_01_b_09_governed(self):
        self._candidate(_bad('Gatedatumtally'), _read('Gatedatumtally'))

    def test_r16_31_01_b_10_governed(self):
        self._candidate(_bad('Boardepistletally'), _read('Boardepistletally'))

    def test_r16_31_01_b_11_governed(self):
        self._candidate(_bad('Gatemissivetally'), _read('Gatemissivetally'))

    def test_r16_31_01_b_12_governed(self):
        self._candidate(_bad('Reviewtablettally'), _read('Reviewtablettally'))

    def test_r16_31_01_b_13_governed(self):
        self._candidate(_bad('Boardplaquetally'), _read('Boardplaquetally'))

    # ------------------------------------------------------
    # Defect forms of R16-31-01, subfamily (c):
    # variant spellings in the composite opening.
    # ------------------------------------------------------

    def test_r16_31_01_c_00_governed(self):
        self._candidate(_bad('Boardtabloidtallye'), _read('Boardtabloidtallye'))

    def test_r16_31_01_c_01_governed(self):
        self._candidate(_bad('Boardwhitepapertalliez'), _read('Boardwhitepapertalliez'))

    def test_r16_31_01_c_02_governed(self):
        self._candidate(_bad('Boardessaytallye'), _read('Boardessaytallye'))

    def test_r16_31_01_c_03_governed(self):
        self._candidate(_bad('Gateplaybilltallye'), _read('Gateplaybilltallye'))

    def test_r16_31_01_c_04_governed(self):
        self._candidate(_bad('Boardphenomenatallye'), _read('Boardphenomenatallye'))

    def test_r16_31_01_c_05_governed(self):
        self._candidate(_bad('Boardmemorandatalliez'), _read('Boardmemorandatalliez'))

    def test_r16_31_01_c_06_governed(self):
        self._candidate(_bad('Boardepistletallye'), _read('Boardepistletallye'))

    def test_r16_31_01_c_07_governed(self):
        self._candidate(_bad('Gatemissivetalliez'), _read('Gatemissivetalliez'))

    # ------------------------------------------------------
    # Defect forms of R16-31-01, subfamily (d):
    # variant spellings past the widened sets.
    # ------------------------------------------------------

    def test_r16_31_01_d_00_governed(self):
        self._candidate(_bad('Tallyo7'), _read('Tallyo7'))

    def test_r16_31_01_d_01_governed(self):
        self._candidate(_bad('Tallyu7'), _read('Tallyu7'))

    def test_r16_31_01_d_02_governed(self):
        self._candidate(_bad('Tallyai7'), _read('Tallyai7'))

    def test_r16_31_01_d_03_governed(self):
        self._candidate(_bad('Tallyez6'), _read('Tallyez6'))

    def test_r16_31_01_d_04_governed(self):
        self._candidate(_bad('Tallyaz6'), _read('Tallyaz6'))

    def test_r16_31_01_d_05_governed(self):
        self._candidate(_bad('Tallya8'), _read('Tallya8'))

    def test_r16_31_01_d_06_governed(self):
        self._candidate(_bad('Tallyeo9'), _read('Tallyeo9'))

    def test_r16_31_01_d_07_governed(self):
        self._candidate(_bad('Boardtallyo7'), _read('Boardtallyo7'))

    def test_r16_31_01_d_08_governed(self):
        self._candidate(_bad('Boardtallyu7'), _read('Boardtallyu7'))

    def test_r16_31_01_d_09_governed(self):
        self._candidate(_bad('Boardtallyai7'), _read('Boardtallyai7'))

    def test_r16_31_01_d_10_governed(self):
        self._candidate(_bad('Boardtallyez6'), _read('Boardtallyez6'))

    def test_r16_31_01_d_11_governed(self):
        self._candidate(_bad('Boardtallyaz6'), _read('Boardtallyaz6'))

    def test_r16_31_01_d_12_governed(self):
        self._candidate(_bad('Boardtallya8'), _read('Boardtallya8'))

    def test_r16_31_01_d_13_governed(self):
        self._candidate(_bad('Boardtallyeo9'), _read('Boardtallyeo9'))

    # ------------------------------------------------------
    # Defect forms of R16-31-01, subfamily (e):
    # summary word further forms.
    # ------------------------------------------------------

    def test_r16_31_01_e_00_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseseses'))

    def test_r16_31_01_e_01_governed(self):
        self._candidate(_bad('Trace summarisingeseseseseseseseseseseseses'), _read('Trace summarisingeseseseseseseseseseseseses'))

    def test_r16_31_01_e_02_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseses'))

    def test_r16_31_01_e_03_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseses'))

    def test_r16_31_01_e_04_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseses'))

    def test_r16_31_01_e_05_governed(self):
        self._candidate(_bad('Trace summaryeseseseseseseseseseseseseses'), _read('Trace summaryeseseseseseseseseseseseseses'))

    def test_r16_31_01_e_06_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseses'))

    # ------------------------------------------------------
    # Defect forms of R16-31-01, subfamily (f):
    # fused closings on those forms.
    # ------------------------------------------------------

    def test_r16_31_01_f_00_governed(self):
        self._candidate(_bad('Boardtracesummarisereseseseseseseseseseseseses'), _read('Boardtracesummarisereseseseseseseseseseseseses'))

    def test_r16_31_01_f_01_governed(self):
        self._candidate(_bad('Tracessummarieseseseseseseseseseseseseses'), _read('Tracessummarieseseseseseseseseseseseseses'))

    def test_r16_31_01_f_02_governed(self):
        self._candidate(_bad('Boardtracesummarisedeseseseseseseseseseseseses'), _read('Boardtracesummarisedeseseseseseseseseseseseses'))

    def test_r16_31_01_f_03_governed(self):
        self._candidate(_bad('Tracessummaryeseseseseseseseseseseseseses'), _read('Tracessummaryeseseseseseseseseseseseseses'))

    # ------------------------------------------------------
    # Defect forms of R16-31-01, subfamily (g):
    # fused closings at eighteen words between.
    # ------------------------------------------------------

    def test_r16_31_01_g_00_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'))

    def test_r16_31_01_g_01_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewtrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewtrace'))

    def test_r16_31_01_g_02_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'))

    # ------------------------------------------------------
    # Defect forms of R16-31-01, subfamily (h):
    # inserted closings at twenty one words between.
    # ------------------------------------------------------

    def test_r16_31_01_h_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board summary'))

    def test_r16_31_01_h_01_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board summary'), _read('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board summary'))

    def test_r16_31_01_h_02_governed(self):
        self._candidate(_bad('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board summary'), _read('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board summary'))

    def test_r16_31_01_h_03_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board trace'))

    def test_r16_31_01_h_04_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board trace'), _read('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board trace'))

    def test_r16_31_01_h_05_governed(self):
        self._candidate(_bad('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board trace'), _read('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board trace'))

    # ------------------------------------------------------
    # Defect forms of R16-31-01, subfamily (i):
    # for step closing at twenty one words between.
    # ------------------------------------------------------

    def test_r16_31_01_i_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board for step 2'))

    # ------------------------------------------------------
    # Defect forms of R16-31-01, subfamily (j):
    # further letters past the widened fold set.
    # ------------------------------------------------------

    def test_r16_31_01_j_00_governed(self):
        self._candidate(_bad('Board ɢally'), _read('Board ɢally'))

    def test_r16_31_01_j_01_governed(self):
        self._candidate(_bad('Board ʕally'), _read('Board ʕally'))

    def test_r16_31_01_j_02_governed(self):
        self._candidate(_bad('Board ɀally'), _read('Board ɀally'))

    def test_r16_31_01_j_03_governed(self):
        self._candidate(_bad('Board ʊally'), _read('Board ʊally'))

    def test_r16_31_01_j_04_governed(self):
        self._candidate(_bad('Board ɕally'), _read('Board ɕally'))

    def test_r16_31_01_j_05_governed(self):
        self._candidate(_bad('Board ɣally'), _read('Board ɣally'))

    def test_r16_31_01_j_06_governed(self):
        self._candidate(_bad('Board ɇally'), _read('Board ɇally'))

    def test_r16_31_01_j_07_governed(self):
        self._candidate(_bad('Board ðally'), _read('Board ðally'))

    def test_r16_31_01_j_08_governed(self):
        self._candidate(_bad('Board ʃally'), _read('Board ʃally'))

    def test_r16_31_01_j_09_governed(self):
        self._candidate(_bad('Board taɸly'), _read('Board taɸly'))

    def test_r16_31_01_j_10_governed(self):
        self._candidate(_bad('Board taθly'), _read('Board taθly'))

    def test_r16_31_01_j_11_governed(self):
        self._candidate(_bad('Board taʁly'), _read('Board taʁly'))

    def test_r16_31_01_j_12_governed(self):
        self._candidate(_bad('Board taɢly'), _read('Board taɢly'))

    def test_r16_31_01_j_13_governed(self):
        self._candidate(_bad('Board taʕly'), _read('Board taʕly'))

    def test_r16_31_01_j_14_governed(self):
        self._candidate(_bad('Board taɀly'), _read('Board taɀly'))

    def test_r16_31_01_j_15_governed(self):
        self._candidate(_bad('Board taʈly'), _read('Board taʈly'))

    def test_r16_31_01_j_16_governed(self):
        self._candidate(_bad('Board taʄly'), _read('Board taʄly'))

    def test_r16_31_01_j_17_governed(self):
        self._candidate(_bad('Board taʊly'), _read('Board taʊly'))

    def test_r16_31_01_j_18_governed(self):
        self._candidate(_bad('Board taʘly'), _read('Board taʘly'))

    def test_r16_31_01_j_19_governed(self):
        self._candidate(_bad('Board taɕly'), _read('Board taɕly'))

    def test_r16_31_01_j_20_governed(self):
        self._candidate(_bad('Board taɣly'), _read('Board taɣly'))

    def test_r16_31_01_j_21_governed(self):
        self._candidate(_bad('Board taƈly'), _read('Board taƈly'))

    def test_r16_31_01_j_22_governed(self):
        self._candidate(_bad('Board taɼly'), _read('Board taɼly'))

    def test_r16_31_01_j_23_governed(self):
        self._candidate(_bad('Board taƗly'), _read('Board taƗly'))

    def test_r16_31_01_j_24_governed(self):
        self._candidate(_bad('Board taɇly'), _read('Board taɇly'))

    def test_r16_31_01_j_25_governed(self):
        self._candidate(_bad('Board taðly'), _read('Board taðly'))

    def test_r16_31_01_j_26_governed(self):
        self._candidate(_bad('Board taʃly'), _read('Board taʃly'))

    def test_r16_31_01_j_27_governed(self):
        self._candidate(_bad('Board taʧly'), _read('Board taʧly'))

    def test_r16_31_01_j_28_governed(self):
        self._candidate(_bad('Trace sɸmmarise'), _read('Trace sɸmmarise'))

    def test_r16_31_01_j_29_governed(self):
        self._candidate(_bad('Trace sθmmarise'), _read('Trace sθmmarise'))

    def test_r16_31_01_j_30_governed(self):
        self._candidate(_bad('Trace sʁmmarise'), _read('Trace sʁmmarise'))

    def test_r16_31_01_j_31_governed(self):
        self._candidate(_bad('Trace sɢmmarise'), _read('Trace sɢmmarise'))

    def test_r16_31_01_j_32_governed(self):
        self._candidate(_bad('Trace sʕmmarise'), _read('Trace sʕmmarise'))

    def test_r16_31_01_j_33_governed(self):
        self._candidate(_bad('Trace sɀmmarise'), _read('Trace sɀmmarise'))

    def test_r16_31_01_j_34_governed(self):
        self._candidate(_bad('Trace sʈmmarise'), _read('Trace sʈmmarise'))

    def test_r16_31_01_j_35_governed(self):
        self._candidate(_bad('Trace sʄmmarise'), _read('Trace sʄmmarise'))

    def test_r16_31_01_j_36_governed(self):
        self._candidate(_bad('Trace sʘmmarise'), _read('Trace sʘmmarise'))

    def test_r16_31_01_j_37_governed(self):
        self._candidate(_bad('Trace sɕmmarise'), _read('Trace sɕmmarise'))

    def test_r16_31_01_j_38_governed(self):
        self._candidate(_bad('Trace sƈmmarise'), _read('Trace sƈmmarise'))

    def test_r16_31_01_j_39_governed(self):
        self._candidate(_bad('Trace sɼmmarise'), _read('Trace sɼmmarise'))

    def test_r16_31_01_j_40_governed(self):
        self._candidate(_bad('Trace sƗmmarise'), _read('Trace sƗmmarise'))

    def test_r16_31_01_j_41_governed(self):
        self._candidate(_bad('Trace sɇmmarise'), _read('Trace sɇmmarise'))

    def test_r16_31_01_j_42_governed(self):
        self._candidate(_bad('Trace sðmmarise'), _read('Trace sðmmarise'))

    def test_r16_31_01_j_43_governed(self):
        self._candidate(_bad('Trace sŋmmarise'), _read('Trace sŋmmarise'))

    def test_r16_31_01_j_44_governed(self):
        self._candidate(_bad('Trace sʧmmarise'), _read('Trace sʧmmarise'))

    def test_r16_31_01_j_45_governed(self):
        self._candidate(_bad('Trace sumʁarise'), _read('Trace sumʁarise'))

    def test_r16_31_01_j_46_governed(self):
        self._candidate(_bad('Trace sumɢarise'), _read('Trace sumɢarise'))

    def test_r16_31_01_j_47_governed(self):
        self._candidate(_bad('Trace sumʕarise'), _read('Trace sumʕarise'))

    def test_r16_31_01_j_48_governed(self):
        self._candidate(_bad('Trace sumɀarise'), _read('Trace sumɀarise'))

    def test_r16_31_01_j_49_governed(self):
        self._candidate(_bad('Trace sumʈarise'), _read('Trace sumʈarise'))

    def test_r16_31_01_j_50_governed(self):
        self._candidate(_bad('Trace sumʄarise'), _read('Trace sumʄarise'))

    def test_r16_31_01_j_51_governed(self):
        self._candidate(_bad('Trace sumʊarise'), _read('Trace sumʊarise'))

    def test_r16_31_01_j_52_governed(self):
        self._candidate(_bad('Trace sumʘarise'), _read('Trace sumʘarise'))

    def test_r16_31_01_j_53_governed(self):
        self._candidate(_bad('Trace sumɕarise'), _read('Trace sumɕarise'))

    def test_r16_31_01_j_54_governed(self):
        self._candidate(_bad('Trace sumɣarise'), _read('Trace sumɣarise'))

    def test_r16_31_01_j_55_governed(self):
        self._candidate(_bad('Trace sumƈarise'), _read('Trace sumƈarise'))

    def test_r16_31_01_j_56_governed(self):
        self._candidate(_bad('Trace sumɼarise'), _read('Trace sumɼarise'))

    def test_r16_31_01_j_57_governed(self):
        self._candidate(_bad('Trace sumƗarise'), _read('Trace sumƗarise'))

    def test_r16_31_01_j_58_governed(self):
        self._candidate(_bad('Trace sumɇarise'), _read('Trace sumɇarise'))

    def test_r16_31_01_j_59_governed(self):
        self._candidate(_bad('Trace sumʃarise'), _read('Trace sumʃarise'))

    def test_r16_31_01_j_60_governed(self):
        self._candidate(_bad('Trace sumʧarise'), _read('Trace sumʧarise'))

    def test_r16_31_01_j_61_governed(self):
        self._candidate(_bad('Trace summariɸe'), _read('Trace summariɸe'))

    def test_r16_31_01_j_62_governed(self):
        self._candidate(_bad('Trace summariθe'), _read('Trace summariθe'))

    def test_r16_31_01_j_63_governed(self):
        self._candidate(_bad('Trace summariʁe'), _read('Trace summariʁe'))

    def test_r16_31_01_j_64_governed(self):
        self._candidate(_bad('Trace summariɢe'), _read('Trace summariɢe'))

    def test_r16_31_01_j_65_governed(self):
        self._candidate(_bad('Trace summariɀe'), _read('Trace summariɀe'))

    def test_r16_31_01_j_66_governed(self):
        self._candidate(_bad('Trace summariʈe'), _read('Trace summariʈe'))

    def test_r16_31_01_j_67_governed(self):
        self._candidate(_bad('Trace summariʄe'), _read('Trace summariʄe'))

    def test_r16_31_01_j_68_governed(self):
        self._candidate(_bad('Trace summariʊe'), _read('Trace summariʊe'))

    def test_r16_31_01_j_69_governed(self):
        self._candidate(_bad('Trace summariʘe'), _read('Trace summariʘe'))

    def test_r16_31_01_j_70_governed(self):
        self._candidate(_bad('Trace summariɣe'), _read('Trace summariɣe'))

    def test_r16_31_01_j_71_governed(self):
        self._candidate(_bad('Trace summariɼe'), _read('Trace summariɼe'))

    def test_r16_31_01_j_72_governed(self):
        self._candidate(_bad('Trace summariƗe'), _read('Trace summariƗe'))

    def test_r16_31_01_j_73_governed(self):
        self._candidate(_bad('Trace summariɇe'), _read('Trace summariɇe'))

    def test_r16_31_01_j_74_governed(self):
        self._candidate(_bad('Trace summariðe'), _read('Trace summariðe'))

    def test_r16_31_01_j_75_governed(self):
        self._candidate(_bad('Trace summariŋe'), _read('Trace summariŋe'))

    def test_r16_31_01_j_76_governed(self):
        self._candidate(_bad('Trace summariʧe'), _read('Trace summariʧe'))

    def test_r16_31_01_j_77_governed(self):
        self._candidate(_bad('Trace summarisɸ'), _read('Trace summarisɸ'))

    def test_r16_31_01_j_78_governed(self):
        self._candidate(_bad('Trace summarisθ'), _read('Trace summarisθ'))

    def test_r16_31_01_j_79_governed(self):
        self._candidate(_bad('Trace summarisʁ'), _read('Trace summarisʁ'))

    def test_r16_31_01_j_80_governed(self):
        self._candidate(_bad('Trace summarisɢ'), _read('Trace summarisɢ'))

    def test_r16_31_01_j_81_governed(self):
        self._candidate(_bad('Trace summarisʕ'), _read('Trace summarisʕ'))

    def test_r16_31_01_j_82_governed(self):
        self._candidate(_bad('Trace summarisɀ'), _read('Trace summarisɀ'))

    def test_r16_31_01_j_83_governed(self):
        self._candidate(_bad('Trace summarisʈ'), _read('Trace summarisʈ'))

    def test_r16_31_01_j_84_governed(self):
        self._candidate(_bad('Trace summarisʄ'), _read('Trace summarisʄ'))

    def test_r16_31_01_j_85_governed(self):
        self._candidate(_bad('Trace summarisʊ'), _read('Trace summarisʊ'))

    def test_r16_31_01_j_86_governed(self):
        self._candidate(_bad('Trace summarisʘ'), _read('Trace summarisʘ'))

    def test_r16_31_01_j_87_governed(self):
        self._candidate(_bad('Trace summarisɕ'), _read('Trace summarisɕ'))

    def test_r16_31_01_j_88_governed(self):
        self._candidate(_bad('Trace summarisɣ'), _read('Trace summarisɣ'))

    def test_r16_31_01_j_89_governed(self):
        self._candidate(_bad('Trace summarisƈ'), _read('Trace summarisƈ'))

    def test_r16_31_01_j_90_governed(self):
        self._candidate(_bad('Trace summarisɼ'), _read('Trace summarisɼ'))

    def test_r16_31_01_j_91_governed(self):
        self._candidate(_bad('Trace summarisƗ'), _read('Trace summarisƗ'))

    def test_r16_31_01_j_92_governed(self):
        self._candidate(_bad('Trace summarisð'), _read('Trace summarisð'))

    def test_r16_31_01_j_93_governed(self):
        self._candidate(_bad('Trace summarisŋ'), _read('Trace summarisŋ'))

    def test_r16_31_01_j_94_governed(self):
        self._candidate(_bad('Trace summarisʃ'), _read('Trace summarisʃ'))

    def test_r16_31_01_j_95_governed(self):
        self._candidate(_bad('Trace summarisʧ'), _read('Trace summarisʧ'))

    def test_r16_31_01_j_96_governed(self):
        self._candidate(_bad('Board ƃally'), _read('Board ƃally'))

    def test_r16_31_01_j_97_governed(self):
        self._candidate(_bad('Board taƃy'), _read('Board taƃy'))

    def test_r16_31_01_j_98_governed(self):
        self._candidate(_bad('Board ƅally'), _read('Board ƅally'))

    def test_r16_31_01_j_99_governed(self):
        self._candidate(_bad('Trace suƅmarise'), _read('Trace suƅmarise'))

    def test_r16_31_01_j_100_governed(self):
        self._candidate(_bad('Board ƍally'), _read('Board ƍally'))

    def test_r16_31_01_j_101_governed(self):
        self._candidate(_bad('Trace summaƍise'), _read('Trace summaƍise'))

    def test_r16_31_01_j_102_governed(self):
        self._candidate(_bad('Board ǝally'), _read('Board ǝally'))

    def test_r16_31_01_j_103_governed(self):
        self._candidate(_bad('Trace suǝmarise'), _read('Trace suǝmarise'))

    # ------------------------------------------------------
    # Adopted assertions of the round 31 breaker exhibit:
    # the beside, gate ruling and code level assertions,
    # in the forms the exhibit names them.
    # ------------------------------------------------------

    def test_b31_epistletally_beside(self):
        q4 = self._beside(_bad("Epistletally"))
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_b31_summarised_beside(self):
        q4 = self._beside(_bad('Trace summarisedeseseseseseseseseseseseses'))
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_b31_epistletally_gate_ruling(self):
        report = self._q4_alone(_bad("Epistletally"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    def test_b31_code_level_underreach_forms(self):
        for word in ("epistletally", "epistlestallies", "boardepistletally",
                     "tallya8", "boardtallyu7"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ('summarisedeseseseseseseseseseseseses', 'summaryeseseseseseseseseseseseseses'):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ('boardtracesummarisedeseseseseseseseseseseseses', 'traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        for head in ("Epistletally",
                     'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board summary',
                     'Trace summarisedeseseseseseseseseseseseses'):
            line = head + ": items checked stand here"
            self.assertTrue(_tally_statement_head(line), head)
        self.assertEqual(_fold_word("\u0183ally"), "tally")
        self.assertEqual(_fold_word("ta\u0183y"), "tally")
        self.assertEqual(_fold_word("\u0185ally"), "tally")
        self.assertEqual(_fold_word("su\u0185marise"), "summarise")
        self.assertEqual(_fold_word("\u018dally"), "tally")
        self.assertEqual(_fold_word("summa\u018dise"), "summarise")
        self.assertEqual(_fold_word("\u01ddally"), "tally")
        self.assertEqual(_fold_word("su\u01ddmarise"), "summarise")

    # ------------------------------------------------------
    # Held controls of R16-31-02, standing missing in the
    # cure of this unit: every distinct converse form of
    # the register, one test per form.
    # ------------------------------------------------------

    def test_control_converse_000_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew trace summary')))

    def test_control_converse_001_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk pray summary trace')))

    def test_control_converse_002_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team bow trace summary')))

    def test_control_converse_003_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grin summary trace')))

    def test_control_converse_004_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk sob trace summary')))

    def test_control_converse_005_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team wink summary trace')))

    def test_control_converse_006_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lick trace summary')))

    def test_control_converse_007_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk peek summary trace')))

    def test_control_converse_008_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team peer trace summary')))

    def test_control_converse_009_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel squint summary trace')))

    def test_control_converse_010_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk snore trace summary')))

    def test_control_converse_011_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team giggle summary trace')))

    def test_control_converse_012_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chuckle trace summary')))

    def test_control_converse_013_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk sniff summary trace')))

    def test_control_converse_014_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team burp trace summary')))

    def test_control_converse_015_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hiccup summary trace')))

    def test_control_converse_016_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk tremble trace summary')))

    def test_control_converse_017_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team wobble summary trace')))

    def test_control_converse_018_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel drool trace summary')))

    def test_control_converse_019_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk shudder summary trace')))

    def test_control_converse_020_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team murmur trace summary')))

    def test_control_converse_021_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glow summary trace')))

    def test_control_converse_022_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk glare trace summary')))

    def test_control_converse_023_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team arise summary trace')))

    def test_control_converse_024_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel awake trace summary')))

    def test_control_converse_025_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk behold summary trace')))

    def test_control_converse_026_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team dwell trace summary')))

    def test_control_converse_027_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel flee summary trace')))

    def test_control_converse_028_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk grind trace summary')))

    def test_control_converse_029_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team lean summary trace')))

    def test_control_converse_030_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lie trace summary')))

    def test_control_converse_031_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk light summary trace')))

    def test_control_converse_032_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team plead trace summary')))

    def test_control_converse_033_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel prove summary trace')))

    def test_control_converse_034_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk spring trace summary')))

    def test_control_converse_035_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stride summary trace')))

    def test_control_converse_036_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel strive trace summary')))

    def test_control_converse_037_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk tread summary trace')))

    def test_control_converse_038_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team weave trace summary')))

    def test_control_converse_039_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wind summary trace')))

    def test_control_converse_040_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk shiver trace summary')))

    def test_control_converse_041_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team arose summary trace')))

    def test_control_converse_042_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel awoke trace summary')))

    def test_control_converse_043_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk befell summary trace')))

    def test_control_converse_044_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team beheld trace summary')))

    def test_control_converse_045_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel besought summary trace')))

    def test_control_converse_046_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk bade trace summary')))

    def test_control_converse_047_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team dwelt summary trace')))

    def test_control_converse_048_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel ground trace summary')))

    def test_control_converse_049_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk leant summary trace')))

    def test_control_converse_050_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team lay trace summary')))

    def test_control_converse_051_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lit summary trace')))

    def test_control_converse_052_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk proven trace summary')))

    def test_control_converse_053_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team slung summary trace')))

    def test_control_converse_054_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sprang trace summary')))

    def test_control_converse_055_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk strode summary trace')))

    def test_control_converse_056_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team strove trace summary')))

    def test_control_converse_057_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel trod summary trace')))

    def test_control_converse_058_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk wove trace summary')))

    def test_control_converse_059_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team wound summary trace')))

    def test_control_converse_060_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel forsook trace summary')))

    def test_control_converse_061_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grin trace summary')))

    def test_control_converse_062_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk sip summary trace')))

    def test_control_converse_063_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team sob trace summary')))

    def test_control_converse_064_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel arose summary trace')))

    def test_control_converse_065_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk dove trace summary')))

    def test_control_converse_066_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team strode summary trace')))

    def test_control_converse_067_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew tracesummary')))

    def test_control_converse_068_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew boardtracesummary')))

    def test_control_converse_069_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatesummary')))

    def test_control_converse_070_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelsummary')))

    def test_control_converse_071_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardsummary')))

    def test_control_converse_072_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatesummary')))

    def test_control_converse_073_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_converse_074_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_converse_075_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_converse_076_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_converse_077_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_converse_078_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_converse_079_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary')))

    def test_control_converse_080_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_converse_081_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel arose tracesummary')))

    def test_control_converse_082_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk awoke summarytrace')))

    def test_control_converse_083_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grin tracesummary')))

    def test_control_converse_084_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk sip summarytrace')))

    def test_control_converse_085_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team sob boardtracesummary')))

    def test_control_converse_086_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel arose traceboardgatesummary')))

    def test_control_converse_087_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk dove traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_converse_088_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team grin tracesummarisationeseseseseseseseseseseseses')))

    def test_control_converse_089_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋂ trace summary')))

    def test_control_converse_090_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋃ trace summary')))

    def test_control_converse_091_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋄ trace summary')))

    def test_control_converse_092_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋈ trace summary')))

    def test_control_converse_093_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⟂ trace summary')))

    def test_control_converse_094_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊜ trace summary')))

    def test_control_converse_095_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊝ trace summary')))

    def test_control_converse_096_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊞ trace summary')))

    def test_control_converse_097_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊟ trace summary')))

    def test_control_converse_098_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊠ trace summary')))

    def test_control_converse_099_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊡ trace summary')))

    def test_control_converse_100_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∐ trace summary')))

    def test_control_converse_101_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∔ trace summary')))

    def test_control_converse_102_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∕ trace summary')))

    def test_control_converse_103_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∖ trace summary')))

    def test_control_converse_104_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∛ trace summary')))

    def test_control_converse_105_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋊ trace summary')))

    def test_control_converse_106_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋋ trace summary')))

    def test_control_converse_107_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋌ trace summary')))

    def test_control_converse_108_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋍ trace summary')))

    def test_control_converse_109_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≢ trace summary')))

    def test_control_converse_110_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≣ trace summary')))

    def test_control_converse_111_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊄ trace summary')))

    def test_control_converse_112_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊅ trace summary')))

    def test_control_converse_113_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊆ trace summary')))

    def test_control_converse_114_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊇ trace summary')))

    def test_control_converse_115_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊈ trace summary')))

    def test_control_converse_116_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊉ trace summary')))

    def test_control_converse_117_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊊ trace summary')))

    def test_control_converse_118_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊋ trace summary')))

    def test_control_converse_119_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊍ trace summary')))

    def test_control_converse_120_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊎ trace summary')))

    def test_control_converse_121_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊏ trace summary')))

    def test_control_converse_122_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊐ trace summary')))

    def test_control_converse_123_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊑ trace summary')))

    def test_control_converse_124_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊒ trace summary')))

    def test_control_converse_125_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋀ trace summary')))

    def test_control_converse_126_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋁ trace summary')))

    def test_control_converse_127_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≀ trace summary')))

    def test_control_converse_128_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≁ trace summary')))

    def test_control_converse_129_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≂ trace summary')))

    def test_control_converse_130_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≃ trace summary')))

    def test_control_converse_131_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≄ trace summary')))

    def test_control_converse_132_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≆ trace summary')))

    def test_control_converse_133_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≇ trace summary')))

    def test_control_converse_134_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≉ trace summary')))

    def test_control_converse_135_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≊ trace summary')))

    def test_control_converse_136_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≋ trace summary')))

    def test_control_converse_137_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≌ trace summary')))

    def test_control_converse_138_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≍ trace summary')))

    def test_control_converse_139_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≎ trace summary')))

    def test_control_converse_140_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≏ trace summary')))

    def test_control_converse_141_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≐ trace summary')))

    def test_control_converse_142_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≑ trace summary')))

    def test_control_converse_143_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger № trace summary')))

    def test_control_converse_144_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℗ trace summary')))

    def test_control_converse_145_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℥ trace summary')))

    def test_control_converse_146_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℔ trace summary')))

    def test_control_converse_147_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℀ trace summary')))

    def test_control_converse_148_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℅ trace summary')))

    def test_control_converse_149_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℆ trace summary')))

    def test_control_converse_150_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⅍ trace summary')))

    def test_control_converse_151_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⅎ trace summary')))

    def test_control_converse_152_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ↯ trace summary')))

    def test_control_converse_153_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ¼ trace summary')))

    def test_control_converse_154_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ¾ trace summary')))

    def test_control_converse_155_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⅓ trace summary')))

    def test_control_converse_156_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⅔ trace summary')))

    def test_control_converse_157_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ¹ trace summary')))

    def test_control_converse_158_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⁴ trace summary')))

    def test_control_converse_159_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⁰ trace summary')))

    def test_control_converse_160_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ‱ trace summary')))

    def test_control_converse_161_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℮ trace summary')))

    def test_control_converse_162_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger Ω trace summary')))

    def test_control_converse_163_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃑ trace summary')))

    def test_control_converse_164_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃖ trace summary')))

    def test_control_converse_165_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃗ trace summary')))

    def test_control_converse_166_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃡ trace summary')))

    def test_control_converse_167_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃥ trace summary')))

    def test_control_converse_168_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃛ trace summary')))

    def test_control_converse_169_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸠panel⸡ trace summary')))

    def test_control_converse_170_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸮panel⸮ trace summary')))

    def test_control_converse_171_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ᚛panel᚜ trace summary')))

    def test_control_converse_172_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ꧄panel꧅ trace summary')))

    def test_control_converse_173_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ꧞panel꧟ trace summary')))

    def test_control_converse_174_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸐panel⸑ trace summary')))

    def test_control_converse_175_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸔panel⸕ trace summary')))

    def test_control_converse_176_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸘panel⸙ trace summary')))

    def test_control_converse_177_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸚panel⸛ trace summary')))

    def test_control_converse_178_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸞panel⸟ trace summary')))

    def test_control_converse_179_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸎panel⸏ trace summary')))

    def test_control_converse_180_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌠panel⌡ trace summary')))

    def test_control_converse_181_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⎡panel⎤ trace summary')))

    def test_control_converse_182_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⎣panel⎦ trace summary')))

    def test_control_converse_183_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⎧panel⎫ trace summary')))

    def test_control_converse_184_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⏞panel⏟ trace summary')))

    def test_control_converse_185_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⏜panel⏝ trace summary')))

    def test_control_converse_186_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦀panel⦀ trace summary')))

    def test_control_converse_187_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧗panel⧖ trace summary')))

    def test_control_converse_188_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧜panel⧝ trace summary')))

    def test_control_converse_189_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧞panel⧟ trace summary')))

    def test_control_converse_190_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧠panel⧡ trace summary')))

    def test_control_converse_191_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧢panel⧣ trace summary')))

    def test_control_converse_192_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧤panel⧥ trace summary')))

    def test_control_converse_193_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧦panel⧧ trace summary')))

    def test_control_converse_194_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧨panel⧩ trace summary')))

    def test_control_converse_195_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧪panel⧪ trace summary')))

    def test_control_converse_196_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧫panel⧫ trace summary')))

    def test_control_converse_197_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧬panel⧬ trace summary')))

    def test_control_converse_198_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧮panel⧮ trace summary')))

    def test_control_converse_199_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧰panel⧰ trace summary')))

    def test_control_converse_200_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧱panel⧱ trace summary')))

    def test_control_converse_201_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧲panel⧲ trace summary')))

    def test_control_converse_202_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧴panel⧴ trace summary')))

    def test_control_converse_203_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧵panel⧵ trace summary')))

    def test_control_converse_204_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧶panel⧶ trace summary')))

    def test_control_converse_205_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧸panel⧸ trace summary')))

    def test_control_converse_206_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧹panel⧹ trace summary')))

    def test_control_converse_207_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧺panel⧺ trace summary')))

    def test_control_converse_208_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧻panel⧻ trace summary')))

    def test_control_converse_209_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦓panel⦔ trace summary')))

    def test_control_converse_210_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ［panel］ trace summary')))

    def test_control_converse_211_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ＜panel＞ trace summary')))

    def test_control_converse_212_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ‟panel‟ trace summary')))

    def test_control_converse_213_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Chew panel trace summary')))

    def test_control_converse_214_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Pray panel trace summary')))

    def test_control_converse_215_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Arose panel summary trace')))

    def test_control_converse_216_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Awoke panel summary trace')))

    def test_control_converse_217_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Grin ledger trace summary')))

    # ------------------------------------------------------
    # Held controls of R16-31-02 named in the register,
    # standing missing in their recorded forms.
    # ------------------------------------------------------

    def test_control_held31_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chews trace summary')))

    def test_control_held31_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chewed trace summary')))

    def test_control_held31_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chewing trace summary')))

    def test_control_held31_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bleed trace summary')))

    def test_control_held31_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sling trace summary')))

    def test_control_held31_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held31_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≅ trace summary')))

    def test_control_held31_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≈ trace summary')))

    def test_control_held31_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸜panel⸝ trace summary')))

    def test_control_held31_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⟬panel⟭ trace summary')))

    def test_control_held31_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌈panel⌉ trace summary')))

    def test_control_held31_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ❮panel❯ trace summary')))

    def test_control_held31_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Grabbed panel trace summary')))

    def test_control_held31_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sat trace summary')))

    def test_control_held31_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃀ trace summary')))

    def test_control_held31_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap trace summary')))

    def test_control_held31_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tap trace summary')))

    def test_control_held31_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist trace summary')))

    def test_control_held31_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap tracesummary')))

    def test_control_held31_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap boardtracesummary')))

    def test_control_held31_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatesummary')))

    def test_control_held31_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelsummary')))

    def test_control_held31_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardsummary')))

    def test_control_held31_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatesummary')))

    def test_control_held31_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held31_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_held31_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held31_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held31_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_held31_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held31_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary')))

    def test_control_held31_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held31_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist tracesummary')))

    def test_control_held31_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist boardtracesummary')))

    def test_control_held31_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatesummary')))

    def test_control_held31_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelsummary')))

    def test_control_held31_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardsummary')))

    def test_control_held31_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatesummary')))

    def test_control_held31_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held31_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_held31_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held31_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held31_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_held31_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held31_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary')))

    def test_control_held31_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held31_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \\\\ trace summary')))

    def test_control_held31_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger || trace summary')))

    def test_control_held31_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger * trace summary')))

    def test_control_held31_49_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ₾ trace summary')))

    def test_control_held31_50_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ₿ trace summary')))

    def test_control_held31_51_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ₺ trace summary')))

    def test_control_held31_52_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace board gate summary')))

    def test_control_held31_53_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace board gate summary')))

    def test_control_held31_54_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yank trace board gate summary')))

    def test_control_held31_55_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bore trace board gate summary')))

    def test_control_held31_56_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk rode summary board gate trace')))

    def test_control_held31_57_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fled trace board gate summary')))

    def test_control_held31_58_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sought trace board gate summary')))

    def test_control_held31_59_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel paid trace board gate summary')))

    def test_control_held31_60_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chose trace board gate summary')))

    def test_control_held31_61_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel reviewed trace board gate summary')))

    def test_control_held31_62_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel logs trace board gate summary')))

    def test_control_held31_63_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel bore traceboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held31_64_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel chose traceboardgatereviewannexpanelsummary')))

    def test_control_held31_65_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel reviewed the traceboardgatereviewannexsummary')))

    # ------------------------------------------------------
    # Governed closings of R16-31-02, standing governed
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
    # Held governed controls of R16-31-01 named in the
    # register, standing governed in the cure.
    # ------------------------------------------------------

    def test_control_underheld_00_governed(self):
        self._candidate(_bad('Abstracttally'), _read('Abstracttally'))

    def test_control_underheld_01_governed(self):
        self._candidate(_bad('Placardtally'), _read('Placardtally'))

    def test_control_underheld_02_governed(self):
        self._candidate(_bad('Boarddictionarytallye'), _read('Boarddictionarytallye'))

    def test_control_underheld_03_governed(self):
        self._candidate(_bad('Gatevocabularytalliez'), _read('Gatevocabularytalliez'))

    def test_control_underheld_04_governed(self):
        self._candidate(_bad('Board ɸally'), _read('Board ɸally'))

    def test_control_underheld_05_governed(self):
        self._candidate(_bad('Board θally'), _read('Board θally'))

    def test_control_underheld_06_governed(self):
        self._candidate(_bad('Board ʁally'), _read('Board ʁally'))

    def test_control_underheld_07_governed(self):
        self._candidate(_bad('Board ʈally'), _read('Board ʈally'))

    def test_control_underheld_08_governed(self):
        self._candidate(_bad('Board ʄally'), _read('Board ʄally'))

    def test_control_underheld_09_governed(self):
        self._candidate(_bad('Board ʘally'), _read('Board ʘally'))

    def test_control_underheld_10_governed(self):
        self._candidate(_bad('Board ƈally'), _read('Board ƈally'))

    def test_control_underheld_11_governed(self):
        self._candidate(_bad('Board ɼally'), _read('Board ɼally'))

    def test_control_underheld_12_governed(self):
        self._candidate(_bad('Board Ɨally'), _read('Board Ɨally'))

    def test_control_underheld_13_governed(self):
        self._candidate(_bad('Board ŋally'), _read('Board ŋally'))

    def test_control_underheld_14_governed(self):
        self._candidate(_bad('Board ʧally'), _read('Board ʧally'))

    def test_control_underheld_15_governed(self):
        self._candidate(_bad('Board taŋly'), _read('Board taŋly'))

    def test_control_underheld_16_governed(self):
        self._candidate(_bad('Trace sʊmmarise'), _read('Trace sʊmmarise'))

    def test_control_underheld_17_governed(self):
        self._candidate(_bad('Trace sɣmmarise'), _read('Trace sɣmmarise'))

    def test_control_underheld_18_governed(self):
        self._candidate(_bad('Trace sʃmmarise'), _read('Trace sʃmmarise'))

    def test_control_underheld_19_governed(self):
        self._candidate(_bad('Trace sumɸarise'), _read('Trace sumɸarise'))

    def test_control_underheld_20_governed(self):
        self._candidate(_bad('Trace sumθarise'), _read('Trace sumθarise'))

    def test_control_underheld_21_governed(self):
        self._candidate(_bad('Trace sumðarise'), _read('Trace sumðarise'))

    def test_control_underheld_22_governed(self):
        self._candidate(_bad('Trace sumŋarise'), _read('Trace sumŋarise'))

    def test_control_underheld_23_governed(self):
        self._candidate(_bad('Trace summariʕe'), _read('Trace summariʕe'))

    def test_control_underheld_24_governed(self):
        self._candidate(_bad('Trace summariɕe'), _read('Trace summariɕe'))

    def test_control_underheld_25_governed(self):
        self._candidate(_bad('Trace summariƈe'), _read('Trace summariƈe'))

    def test_control_underheld_26_governed(self):
        self._candidate(_bad('Trace summariʃe'), _read('Trace summariʃe'))

    def test_control_underheld_27_governed(self):
        self._candidate(_bad('Trace summarisɇ'), _read('Trace summarisɇ'))

    def test_control_underheld_28_governed(self):
        self._candidate(_bad('Trace ƈummarise'), _read('Trace ƈummarise'))

    def test_control_underheld_29_governed(self):
        self._candidate(_bad('Songbooktally'), _read('Songbooktally'))

    # Amendment in place, recorded in the standing form.
    # This test stood corrected in fix pass 31, under the
    # coordinator ruling carried in
    # design/steps/step-16r-fix31-unit2-report.md, to the
    # standing of the form Songbookstallies as missing at
    # code level, on the register31 held listing for that
    # form. That standing now stands reversed: register32
    # superseded the register31 held listing for this one
    # form, and the cure of R16-32-03 in fix pass 32 Unit 2
    # makes the form derive in the plain drive. Under the
    # charge carried to fix pass 32 Unit 3 Act 0 by the
    # coordinator on the Unit 2 report carriage, this test
    # keeps its identity and its place and its expectation
    # stands amended in place to the form present standing:
    # the form derives in the plain drive, governed beside
    # its counted sibling.
    def test_control_underheld_30_governed(self):
        self._candidate(_bad('Songbookstallies'), _read('Songbookstallies'))

    def test_control_underheld_31_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseses'))

    def test_control_underheld_32_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'))

    def test_control_underheld_33_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel summary'))

    def test_control_underheld_34_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel trace'))

    def test_control_underheld_35_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel for step 2'))

    def test_control_underheld_36_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseses'))

    def test_control_underheld_37_governed(self):
        self._candidate(_bad('Boardtracesummarisereseseseseseseseseses'), _read('Boardtracesummarisereseseseseseseseseses'))
