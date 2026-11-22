"""Step 16 fix pass 34 unit 2 tests: the Q-4 closing unit.

Pinning tests for register item R16-34-01 (Medium,
B34-C01 and B34-B01) of Step 16 round 34. The
governing rule of the pass, in its extended form: a
piece not read in full, for whatever reason, is not
read, and its converse: a piece that is no feeder
flips nothing.

R16-34-01: malformed tally statement heads standing
unread past the widened boundary of fix pass 33, on
the counted pattern head agnosticism ground alone:
the pattern standing counted over a plain whole word
pattern, so a malformed head whose counted sibling
counts stands missing in the row although it stands
as a feeder statement in a form the row cannot parse.
One hundred and forty distinct alone forms stand
driven in ten subfamilies: (a) tally forms fused
behind record words no widening has named and behind
the plurals of record words in the same position,
twenty one forms; (b) composite openings built on
those forms, nine forms; (c) a variant spelling in
that composite opening position built on those words,
three forms; (d) the variant spellings past the
widened variant sets of one hundred and three and one
hundred and six, eighteen forms; (e) the summary word
in further forms at the sixteenth and seventeenth es
repetitions of its families, seven forms; (f) the
fused closings built on those forms, four forms; (g)
the fused closings with twenty one governed words
fused between the closing words, three forms; (h) the
inserted closings with twenty four words of subject
between in their wide, middle swap and full swap
shapes in both directions, six forms; (i) the for
step closing with twenty four words of subject
between, one form; and (j) further Latin and kindred
letters past the widened fold set, each standing in a
position the folding does not read, sixty eight
forms, the correctness forms of that subfamily
standing in the template and codepoint form that
paper states, at the positions and codepoints the
register names, and the breaker forms standing in the
words the breaker paper names. The fifty nine
underreach assertions of the round 34 breaker exhibit
stand adopted in this module: the fifty five alone
form assertions of B34-B01 stand among the defect
tests of the subfamilies above in their driven words,
and the beside assertions, the gate ruling assertion
and the code level assertion of that exhibit stand as
defect tests here in the forms the exhibit names
them, in the exhibit test names themselves. The
defect stands bounded in the open by its held
controls: every form of R16-34-02 standing missing,
every held form of that item standing missing in its
recorded form, every governed closing of that item
standing governed, and on the underreach side the
governed neighbours of both papers standing governed,
the governed candidates of subfamily (a) of the
correctness paper standing governed through the
governed stems and blocks at the close of their fused
forms, the governed variant composite opening of that
paper standing governed, the one hundred and thirty
two governed letter forms of subfamily (j) of the
correctness paper standing governed at their
positions, the candidate record words of the breaker
paper standing governed in their probed forms,
Songbooktally and Songbookstallies standing governed
in their present standings, Boarddictionarytally
standing governed through the further position limb,
the widest form of every summary family standing
governed in the widened enumeration at its family
position, the candidate letters of the breaker paper
standing folded to their words, the fused and
inserted closings standing at their governed counts,
the twenty word fused between closing, the twenty
three word forward and reversed inserted closings and
the twenty three word for step closing standing
governed, and the plain Latin spellings standing at
their standings. Locus: derivation_core.py,
_tally_statement_head and its standing helpers and
constants. The cure these tests pin widens what a
malformed tally statement head is in standing: the
governed fused prefix set widened by the record words
and plural stems of this round, the variant sets
widened by the spellings of this round, the summary
word set widened by the further forms of this round,
the fused between reach widened to twenty one
governed words, the inserted closings standing at
twenty four words forward, twenty four words reversed
and twenty four words in the for step form under the
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


class TestStep16Fix34Unit2(FixtureTestCase):

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
    # Defect forms of R16-34-01, subfamily (a):
    # fused record words and the plurals of record words.
    # ------------------------------------------------------

    def test_r16_34_01_a_00_governed(self):
        self._candidate(_bad('Storybookstallies'), _read('Storybookstallies'))

    def test_r16_34_01_a_01_governed(self):
        self._candidate(_bad('Picturebookstallies'), _read('Picturebookstallies'))

    def test_r16_34_01_a_02_governed(self):
        self._candidate(_bad('Ritualtally'), _read('Ritualtally'))

    def test_r16_34_01_a_03_governed(self):
        self._candidate(_bad('Ritualstallies'), _read('Ritualstallies'))

    def test_r16_34_01_a_04_governed(self):
        self._candidate(_bad('Antiphonalstallies'), _read('Antiphonalstallies'))

    def test_r16_34_01_a_05_governed(self):
        self._candidate(_bad('Cashbookstallies'), _read('Cashbookstallies'))

    def test_r16_34_01_a_06_governed(self):
        self._candidate(_bad('Orderbookstallies'), _read('Orderbookstallies'))

    def test_r16_34_01_a_07_governed(self):
        self._candidate(_bad('Minutebookstallies'), _read('Minutebookstallies'))

    def test_r16_34_01_a_08_governed(self):
        self._candidate(_bad('Prayerbookstallies'), _read('Prayerbookstallies'))

    def test_r16_34_01_a_09_governed(self):
        self._candidate(_bad('Hymnbookstallies'), _read('Hymnbookstallies'))

    def test_r16_34_01_a_10_governed(self):
        self._candidate(_bad('Bluebookstallies'), _read('Bluebookstallies'))

    def test_r16_34_01_a_11_governed(self):
        self._candidate(_bad('Redbookstallies'), _read('Redbookstallies'))

    def test_r16_34_01_a_12_governed(self):
        self._candidate(_bad('Nocturntally'), _read('Nocturntally'))

    def test_r16_34_01_a_13_governed(self):
        self._candidate(_bad('Antiphontally'), _read('Antiphontally'))

    def test_r16_34_01_a_14_governed(self):
        self._candidate(_bad('Rubrictally'), _read('Rubrictally'))

    def test_r16_34_01_a_15_governed(self):
        self._candidate(_bad('Ordinaltally'), _read('Ordinaltally'))

    def test_r16_34_01_a_16_governed(self):
        self._candidate(_bad('Homilytally'), _read('Homilytally'))

    def test_r16_34_01_a_17_governed(self):
        self._candidate(_bad('Nocturnstallies'), _read('Nocturnstallies'))

    def test_r16_34_01_a_18_governed(self):
        self._candidate(_bad('Antiphonstallies'), _read('Antiphonstallies'))

    def test_r16_34_01_a_19_governed(self):
        self._candidate(_bad('Rubricstallies'), _read('Rubricstallies'))

    def test_r16_34_01_a_20_governed(self):
        self._candidate(_bad('Fascicletstallies'), _read('Fascicletstallies'))

    # ------------------------------------------------------
    # Defect forms of R16-34-01, subfamily (b):
    # composite openings built on those forms.
    # ------------------------------------------------------

    def test_r16_34_01_b_00_governed(self):
        self._candidate(_bad('Boardstorybookstallies'), _read('Boardstorybookstallies'))

    def test_r16_34_01_b_01_governed(self):
        self._candidate(_bad('Boardritualtally'), _read('Boardritualtally'))

    def test_r16_34_01_b_02_governed(self):
        self._candidate(_bad('Boardcashbookstallies'), _read('Boardcashbookstallies'))

    def test_r16_34_01_b_03_governed(self):
        self._candidate(_bad('Boardnocturntally'), _read('Boardnocturntally'))

    def test_r16_34_01_b_04_governed(self):
        self._candidate(_bad('Gaterubrictally'), _read('Gaterubrictally'))

    def test_r16_34_01_b_05_governed(self):
        self._candidate(_bad('Reviewantiphontally'), _read('Reviewantiphontally'))

    def test_r16_34_01_b_06_governed(self):
        self._candidate(_bad('Boardordinaltally'), _read('Boardordinaltally'))

    def test_r16_34_01_b_07_governed(self):
        self._candidate(_bad('Boardhymnbookstallies'), _read('Boardhymnbookstallies'))

    def test_r16_34_01_b_08_governed(self):
        self._candidate(_bad('Gateprayerbookstallies'), _read('Gateprayerbookstallies'))

    # ------------------------------------------------------
    # Defect forms of R16-34-01, subfamily (c):
    # a variant spelling in that composite opening position.
    # ------------------------------------------------------

    def test_r16_34_01_c_00_governed(self):
        self._candidate(_bad('Boardritualtallye'), _read('Boardritualtallye'))

    def test_r16_34_01_c_01_governed(self):
        self._candidate(_bad('Boardnocturntallye'), _read('Boardnocturntallye'))

    def test_r16_34_01_c_02_governed(self):
        self._candidate(_bad('Gaterubrictalliez'), _read('Gaterubrictalliez'))

    # ------------------------------------------------------
    # Defect forms of R16-34-01, subfamily (d):
    # the variant spellings past the widened variant sets.
    # ------------------------------------------------------

    def test_r16_34_01_d_00_governed(self):
        self._candidate(_bad('Tallya11'), _read('Tallya11'))

    def test_r16_34_01_d_01_governed(self):
        self._candidate(_bad('Tallyo10'), _read('Tallyo10'))

    def test_r16_34_01_d_02_governed(self):
        self._candidate(_bad('Tallyu10'), _read('Tallyu10'))

    def test_r16_34_01_d_03_governed(self):
        self._candidate(_bad('Tallyai10'), _read('Tallyai10'))

    def test_r16_34_01_d_04_governed(self):
        self._candidate(_bad('Tallyez9'), _read('Tallyez9'))

    def test_r16_34_01_d_05_governed(self):
        self._candidate(_bad('Tallyaz9'), _read('Tallyaz9'))

    def test_r16_34_01_d_06_governed(self):
        self._candidate(_bad('Tallyeo12'), _read('Tallyeo12'))

    def test_r16_34_01_d_07_governed(self):
        self._candidate(_bad('Tallyia4'), _read('Tallyia4'))

    def test_r16_34_01_d_08_governed(self):
        self._candidate(_bad('Tallye10'), _read('Tallye10'))

    def test_r16_34_01_d_09_governed(self):
        self._candidate(_bad('Boardtallya11'), _read('Boardtallya11'))

    def test_r16_34_01_d_10_governed(self):
        self._candidate(_bad('Boardtallyo10'), _read('Boardtallyo10'))

    def test_r16_34_01_d_11_governed(self):
        self._candidate(_bad('Boardtallyu10'), _read('Boardtallyu10'))

    def test_r16_34_01_d_12_governed(self):
        self._candidate(_bad('Boardtallyai10'), _read('Boardtallyai10'))

    def test_r16_34_01_d_13_governed(self):
        self._candidate(_bad('Boardtallyez9'), _read('Boardtallyez9'))

    def test_r16_34_01_d_14_governed(self):
        self._candidate(_bad('Boardtallyaz9'), _read('Boardtallyaz9'))

    def test_r16_34_01_d_15_governed(self):
        self._candidate(_bad('Boardtallyeo12'), _read('Boardtallyeo12'))

    def test_r16_34_01_d_16_governed(self):
        self._candidate(_bad('Boardtallyia4'), _read('Boardtallyia4'))

    def test_r16_34_01_d_17_governed(self):
        self._candidate(_bad('Boardtallye10'), _read('Boardtallye10'))

    # ------------------------------------------------------
    # Defect forms of R16-34-01, subfamily (e):
    # the summary word in further forms.
    # ------------------------------------------------------

    def test_r16_34_01_e_00_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseseseseseses'))

    def test_r16_34_01_e_01_governed(self):
        self._candidate(_bad('Trace summarisingeseseseseseseseseseseseseseseses'), _read('Trace summarisingeseseseseseseseseseseseseseseses'))

    def test_r16_34_01_e_02_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseseseseses'))

    def test_r16_34_01_e_03_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseseseseses'))

    def test_r16_34_01_e_04_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseseseseses'))

    def test_r16_34_01_e_05_governed(self):
        self._candidate(_bad('Trace summaryeseseseseseseseseseseseseseseseses'), _read('Trace summaryeseseseseseseseseseseseseseseseses'))

    def test_r16_34_01_e_06_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseseseseses'))

    # ------------------------------------------------------
    # Defect forms of R16-34-01, subfamily (f):
    # the fused closings built on those forms.
    # ------------------------------------------------------

    def test_r16_34_01_f_00_governed(self):
        self._candidate(_bad('Boardtracesummarisereseseseseseseseseseseseseseseses'), _read('Boardtracesummarisereseseseseseseseseseseseseseseses'))

    def test_r16_34_01_f_01_governed(self):
        self._candidate(_bad('Tracessummarieseseseseseseseseseseseseseseseses'), _read('Tracessummarieseseseseseseseseseseseseseseseses'))

    def test_r16_34_01_f_02_governed(self):
        self._candidate(_bad('Boardtracesummarisedeseseseseseseseseseseseseseseses'), _read('Boardtracesummarisedeseseseseseseseseseseseseseseses'))

    def test_r16_34_01_f_03_governed(self):
        self._candidate(_bad('Tracessummaryeseseseseseseseseseseseseseseseses'), _read('Tracessummaryeseseseseseseseseseseseseseseseses'))

    # ------------------------------------------------------
    # Defect forms of R16-34-01, subfamily (g):
    # the fused closings with twenty one governed words fused between.
    # ------------------------------------------------------

    def test_r16_34_01_g_00_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'))

    def test_r16_34_01_g_01_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardtrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardtrace'))

    def test_r16_34_01_g_02_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'))

    # ------------------------------------------------------
    # Defect forms of R16-34-01, subfamily (h):
    # the inserted closings with twenty four words of subject between.
    # ------------------------------------------------------

    def test_r16_34_01_h_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex summary'))

    def test_r16_34_01_h_01_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex summary'), _read('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex summary'))

    def test_r16_34_01_h_02_governed(self):
        self._candidate(_bad('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review summary'), _read('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review summary'))

    def test_r16_34_01_h_03_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex trace'))

    def test_r16_34_01_h_04_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex trace'), _read('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate review annex trace'))

    def test_r16_34_01_h_05_governed(self):
        self._candidate(_bad('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review trace'), _read('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review trace'))

    # ------------------------------------------------------
    # Defect forms of R16-34-01, subfamily (i):
    # the for step closing with twenty four words of subject between.
    # ------------------------------------------------------

    def test_r16_34_01_i_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex for step 2'))

    # ------------------------------------------------------
    # Defect forms of R16-34-01, subfamily (j):
    # further letters past the widened fold set.
    # ------------------------------------------------------

    def test_r16_34_01_j_00_governed(self):
        self._candidate(_bad('Board ɪally'), _read('Board ɪally'))

    def test_r16_34_01_j_01_governed(self):
        self._candidate(_bad('Board ɹally'), _read('Board ɹally'))

    def test_r16_34_01_j_02_governed(self):
        self._candidate(_bad('Board ɺally'), _read('Board ɺally'))

    def test_r16_34_01_j_03_governed(self):
        self._candidate(_bad('Board ɻally'), _read('Board ɻally'))

    def test_r16_34_01_j_04_governed(self):
        self._candidate(_bad('Board ɾally'), _read('Board ɾally'))

    def test_r16_34_01_j_05_governed(self):
        self._candidate(_bad('Board ɿally'), _read('Board ɿally'))

    def test_r16_34_01_j_06_governed(self):
        self._candidate(_bad('Board ʅally'), _read('Board ʅally'))

    def test_r16_34_01_j_07_governed(self):
        self._candidate(_bad('Board ʆally'), _read('Board ʆally'))

    def test_r16_34_01_j_08_governed(self):
        self._candidate(_bad('Board taɪly'), _read('Board taɪly'))

    def test_r16_34_01_j_09_governed(self):
        self._candidate(_bad('Board taɹly'), _read('Board taɹly'))

    def test_r16_34_01_j_10_governed(self):
        self._candidate(_bad('Board taɺly'), _read('Board taɺly'))

    def test_r16_34_01_j_11_governed(self):
        self._candidate(_bad('Board taɻly'), _read('Board taɻly'))

    def test_r16_34_01_j_12_governed(self):
        self._candidate(_bad('Board taɽly'), _read('Board taɽly'))

    def test_r16_34_01_j_13_governed(self):
        self._candidate(_bad('Board taɾly'), _read('Board taɾly'))

    def test_r16_34_01_j_14_governed(self):
        self._candidate(_bad('Board taɿly'), _read('Board taɿly'))

    def test_r16_34_01_j_15_governed(self):
        self._candidate(_bad('Board taʂly'), _read('Board taʂly'))

    def test_r16_34_01_j_16_governed(self):
        self._candidate(_bad('Board taʅly'), _read('Board taʅly'))

    def test_r16_34_01_j_17_governed(self):
        self._candidate(_bad('Board taʆly'), _read('Board taʆly'))

    def test_r16_34_01_j_18_governed(self):
        self._candidate(_bad('Board taʇly'), _read('Board taʇly'))

    def test_r16_34_01_j_19_governed(self):
        self._candidate(_bad('Trace sɪmmarise'), _read('Trace sɪmmarise'))

    def test_r16_34_01_j_20_governed(self):
        self._candidate(_bad('Trace sɹmmarise'), _read('Trace sɹmmarise'))

    def test_r16_34_01_j_21_governed(self):
        self._candidate(_bad('Trace sɺmmarise'), _read('Trace sɺmmarise'))

    def test_r16_34_01_j_22_governed(self):
        self._candidate(_bad('Trace sɻmmarise'), _read('Trace sɻmmarise'))

    def test_r16_34_01_j_23_governed(self):
        self._candidate(_bad('Trace sɽmmarise'), _read('Trace sɽmmarise'))

    def test_r16_34_01_j_24_governed(self):
        self._candidate(_bad('Trace sɾmmarise'), _read('Trace sɾmmarise'))

    def test_r16_34_01_j_25_governed(self):
        self._candidate(_bad('Trace sɿmmarise'), _read('Trace sɿmmarise'))

    def test_r16_34_01_j_26_governed(self):
        self._candidate(_bad('Trace sʂmmarise'), _read('Trace sʂmmarise'))

    def test_r16_34_01_j_27_governed(self):
        self._candidate(_bad('Trace sʅmmarise'), _read('Trace sʅmmarise'))

    def test_r16_34_01_j_28_governed(self):
        self._candidate(_bad('Trace sʆmmarise'), _read('Trace sʆmmarise'))

    def test_r16_34_01_j_29_governed(self):
        self._candidate(_bad('Trace sʇmmarise'), _read('Trace sʇmmarise'))

    def test_r16_34_01_j_30_governed(self):
        self._candidate(_bad('Trace sumɪarise'), _read('Trace sumɪarise'))

    def test_r16_34_01_j_31_governed(self):
        self._candidate(_bad('Trace sumɹarise'), _read('Trace sumɹarise'))

    def test_r16_34_01_j_32_governed(self):
        self._candidate(_bad('Trace sumɺarise'), _read('Trace sumɺarise'))

    def test_r16_34_01_j_33_governed(self):
        self._candidate(_bad('Trace sumɻarise'), _read('Trace sumɻarise'))

    def test_r16_34_01_j_34_governed(self):
        self._candidate(_bad('Trace sumɽarise'), _read('Trace sumɽarise'))

    def test_r16_34_01_j_35_governed(self):
        self._candidate(_bad('Trace sumɾarise'), _read('Trace sumɾarise'))

    def test_r16_34_01_j_36_governed(self):
        self._candidate(_bad('Trace sumɿarise'), _read('Trace sumɿarise'))

    def test_r16_34_01_j_37_governed(self):
        self._candidate(_bad('Trace sumʂarise'), _read('Trace sumʂarise'))

    def test_r16_34_01_j_38_governed(self):
        self._candidate(_bad('Trace sumʅarise'), _read('Trace sumʅarise'))

    def test_r16_34_01_j_39_governed(self):
        self._candidate(_bad('Trace sumʆarise'), _read('Trace sumʆarise'))

    def test_r16_34_01_j_40_governed(self):
        self._candidate(_bad('Trace sumʇarise'), _read('Trace sumʇarise'))

    def test_r16_34_01_j_41_governed(self):
        self._candidate(_bad('Trace summariɪe'), _read('Trace summariɪe'))

    def test_r16_34_01_j_42_governed(self):
        self._candidate(_bad('Trace summariɹe'), _read('Trace summariɹe'))

    def test_r16_34_01_j_43_governed(self):
        self._candidate(_bad('Trace summariɺe'), _read('Trace summariɺe'))

    def test_r16_34_01_j_44_governed(self):
        self._candidate(_bad('Trace summariɻe'), _read('Trace summariɻe'))

    def test_r16_34_01_j_45_governed(self):
        self._candidate(_bad('Trace summariɽe'), _read('Trace summariɽe'))

    def test_r16_34_01_j_46_governed(self):
        self._candidate(_bad('Trace summariɾe'), _read('Trace summariɾe'))

    def test_r16_34_01_j_47_governed(self):
        self._candidate(_bad('Trace summariɿe'), _read('Trace summariɿe'))

    def test_r16_34_01_j_48_governed(self):
        self._candidate(_bad('Trace summariʆe'), _read('Trace summariʆe'))

    def test_r16_34_01_j_49_governed(self):
        self._candidate(_bad('Trace summariʇe'), _read('Trace summariʇe'))

    def test_r16_34_01_j_50_governed(self):
        self._candidate(_bad('Trace summarisɪ'), _read('Trace summarisɪ'))

    def test_r16_34_01_j_51_governed(self):
        self._candidate(_bad('Trace summarisɹ'), _read('Trace summarisɹ'))

    def test_r16_34_01_j_52_governed(self):
        self._candidate(_bad('Trace summarisɺ'), _read('Trace summarisɺ'))

    def test_r16_34_01_j_53_governed(self):
        self._candidate(_bad('Trace summarisɻ'), _read('Trace summarisɻ'))

    def test_r16_34_01_j_54_governed(self):
        self._candidate(_bad('Trace summarisɽ'), _read('Trace summarisɽ'))

    def test_r16_34_01_j_55_governed(self):
        self._candidate(_bad('Trace summarisɾ'), _read('Trace summarisɾ'))

    def test_r16_34_01_j_56_governed(self):
        self._candidate(_bad('Trace summarisɿ'), _read('Trace summarisɿ'))

    def test_r16_34_01_j_57_governed(self):
        self._candidate(_bad('Trace summarisʅ'), _read('Trace summarisʅ'))

    def test_r16_34_01_j_58_governed(self):
        self._candidate(_bad('Trace summarisʆ'), _read('Trace summarisʆ'))

    def test_r16_34_01_j_59_governed(self):
        self._candidate(_bad('Trace summarisʇ'), _read('Trace summarisʇ'))

    def test_r16_34_01_j_60_governed(self):
        self._candidate(_bad('Board ǉally'), _read('Board ǉally'))

    def test_r16_34_01_j_61_governed(self):
        self._candidate(_bad('Trace suǉmarise'), _read('Trace suǉmarise'))

    def test_r16_34_01_j_62_governed(self):
        self._candidate(_bad('Board Ǳally'), _read('Board Ǳally'))

    def test_r16_34_01_j_63_governed(self):
        self._candidate(_bad('Board taǱy'), _read('Board taǱy'))

    def test_r16_34_01_j_64_governed(self):
        self._candidate(_bad('Board Ⱥally'), _read('Board Ⱥally'))

    def test_r16_34_01_j_65_governed(self):
        self._candidate(_bad('Trace summaȺise'), _read('Trace summaȺise'))

    def test_r16_34_01_j_66_governed(self):
        self._candidate(_bad('Board ʐally'), _read('Board ʐally'))

    def test_r16_34_01_j_67_governed(self):
        self._candidate(_bad('Trace summarisʐ'), _read('Trace summarisʐ'))

    # ------------------------------------------------------
    # Adopted assertions of the round 34 breaker exhibit:
    # the beside, gate ruling and code level assertions
    # of B34-B01, in the forms the exhibit names them,
    # standing in the exhibit test names themselves.
    # ------------------------------------------------------

    def test_b34_nocturntally_beside(self):
        q4 = self._beside(_bad("Nocturntally"))
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_b34_summarised_beside(self):
        q4 = self._beside(_bad('Trace summarisedeseseseseseseseseseseseseseseses'))
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_b34_nocturntally_gate_ruling(self):
        report = self._q4_alone(_bad("Nocturntally"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    def test_b34_code_level_underreach_forms(self):
        for word in ("nocturntally", "nocturnstallies",
                     "boardnocturntally", "tallye10", "boardtallyaz9"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ('summarisedeseseseseseseseseseseseseseseses', 'summaryeseseseseseseseseseseseseseseseses'):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ('boardtracesummarisedeseseseseseseseseseseseseseseses',
                     'traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        for head in ("Nocturntally",
                     'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex summary',
                     'Trace summarisedeseseseseseseseseseseseseseseses'):
            line = head + ": items checked stand here"
            self.assertTrue(_tally_statement_head(line), head)
        self.assertEqual(_fold_word("\u01c9ally"), "tally")
        self.assertEqual(_fold_word("su\u01c9marise"), "summarise")

    # ------------------------------------------------------
    # Held controls of R16-34-02, standing missing in the
    # cure of this unit: every distinct converse form of
    # the register, one test per form.
    # ------------------------------------------------------

    def test_control_converse_000_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹗panel⹘ trace summary')))

    def test_control_converse_001_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹙panel⹚ trace summary')))

    def test_control_converse_002_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹛panel⹜ trace summary')))

    def test_control_converse_003_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹐panel⹑ trace summary')))

    def test_control_converse_004_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹒panel⹓ trace summary')))

    def test_control_converse_005_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⹓panel⹔ trace summary')))

    def test_control_converse_006_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snicker trace summary')))

    def test_control_converse_007_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chortle trace summary')))

    def test_control_converse_008_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel guffaw trace summary')))

    def test_control_converse_009_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wince trace summary')))

    def test_control_converse_010_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grimace trace summary')))

    def test_control_converse_011_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel scowl trace summary')))

    def test_control_converse_012_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whimper trace summary')))

    def test_control_converse_013_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whine trace summary')))

    def test_control_converse_014_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel mutter trace summary')))

    def test_control_converse_015_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stutter trace summary')))

    def test_control_converse_016_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel blubber trace summary')))

    def test_control_converse_017_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cackle trace summary')))

    def test_control_converse_018_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snigger trace summary')))

    def test_control_converse_019_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel titter trace summary')))

    def test_control_converse_020_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk mutter summary trace')))

    def test_control_converse_021_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stutter trace summary')))

    def test_control_converse_022_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel falter summary trace')))

    def test_control_converse_023_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk babble trace summary')))

    def test_control_converse_024_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team waver summary trace')))

    def test_control_converse_025_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snicker tracesummary')))

    def test_control_converse_026_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chortle tracesummary')))

    def test_control_converse_027_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel guffaw tracesummary')))

    def test_control_converse_028_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wince tracesummary')))

    def test_control_converse_029_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grimace tracesummary')))

    def test_control_converse_030_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel scowl tracesummary')))

    def test_control_converse_031_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whimper tracesummary')))

    def test_control_converse_032_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whine tracesummary')))

    def test_control_converse_033_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel mutter tracesummary')))

    def test_control_converse_034_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stutter tracesummary')))

    def test_control_converse_035_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel blubber tracesummary')))

    def test_control_converse_036_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cackle tracesummary')))

    def test_control_converse_037_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snigger tracesummary')))

    def test_control_converse_038_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel titter tracesummary')))

    def test_control_converse_039_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk mutter summarytrace')))

    def test_control_converse_040_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stutter boardtracesummary')))

    def test_control_converse_041_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel falter traceboardgatesummary')))

    def test_control_converse_042_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk whimper traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_converse_043_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team mutter tracesummarisationeseseseseseseseseseseseseseseses')))

    def test_control_converse_044_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨶ trace summary')))

    def test_control_converse_045_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨷ trace summary')))

    def test_control_converse_046_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨸ trace summary')))

    def test_control_converse_047_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨹ trace summary')))

    def test_control_converse_048_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨺ trace summary')))

    def test_control_converse_049_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨻ trace summary')))

    def test_control_converse_050_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨼ trace summary')))

    def test_control_converse_051_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨽ trace summary')))

    def test_control_converse_052_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨾ trace summary')))

    def test_control_converse_053_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨿ trace summary')))

    def test_control_converse_054_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩀ trace summary')))

    def test_control_converse_055_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩁ trace summary')))

    def test_control_converse_056_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩂ trace summary')))

    def test_control_converse_057_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩃ trace summary')))

    def test_control_converse_058_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩄ trace summary')))

    def test_control_converse_059_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩅ trace summary')))

    def test_control_converse_060_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩆ trace summary')))

    def test_control_converse_061_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩇ trace summary')))

    def test_control_converse_062_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩈ trace summary')))

    def test_control_converse_063_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩉ trace summary')))

    def test_control_converse_064_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩊ trace summary')))

    def test_control_converse_065_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩋ trace summary')))

    def test_control_converse_066_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩌ trace summary')))

    def test_control_converse_067_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩍ trace summary')))

    def test_control_converse_068_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩎ trace summary')))

    def test_control_converse_069_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⩏ trace summary')))

    def test_control_converse_070_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧄ trace summary')))

    def test_control_converse_071_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧅ trace summary')))

    def test_control_converse_072_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧆ trace summary')))

    def test_control_converse_073_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧇ trace summary')))

    def test_control_converse_074_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌓ trace summary')))

    def test_control_converse_075_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⏠ trace summary')))

    def test_control_converse_076_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x⃓ trace summary')))

    def test_control_converse_077_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x⃤ trace summary')))

    def test_control_converse_078_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃓ trace summary')))

    def test_control_converse_079_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃙ trace summary')))

    def test_control_converse_080_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃤ trace summary')))

    def test_control_converse_081_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃦ trace summary')))

    def test_control_converse_082_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃨ trace summary')))

    def test_control_converse_083_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃩ trace summary')))

    def test_control_converse_084_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Snicker panel trace summary')))

    def test_control_converse_085_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Chortle panel trace summary')))

    def test_control_converse_086_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Guffaw panel trace summary')))

    def test_control_converse_087_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Wince panel trace summary')))

    def test_control_converse_088_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Grimace panel trace summary')))

    def test_control_converse_089_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Scowl panel trace summary')))

    def test_control_converse_090_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Whimper panel trace summary')))

    def test_control_converse_091_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Whine panel trace summary')))

    def test_control_converse_092_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Mutter panel trace summary')))

    def test_control_converse_093_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Stutter panel trace summary')))

    def test_control_converse_094_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Blubber panel trace summary')))

    def test_control_converse_095_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Cackle panel trace summary')))

    def test_control_converse_096_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Snigger panel trace summary')))

    def test_control_converse_097_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Titter panel trace summary')))

    def test_control_converse_098_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Whimper ledger trace summary')))

    # ------------------------------------------------------
    # Held controls of R16-34-02 named in the register,
    # standing missing in their recorded forms.
    # ------------------------------------------------------

    def test_control_held34_000_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sigh trace summary')))

    def test_control_held34_001_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sob trace summary')))

    def test_control_held34_002_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp trace summary')))

    def test_control_held34_003_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gasp trace summary')))

    def test_control_held34_004_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whisper trace summary')))

    def test_control_held34_005_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel murmur trace summary')))

    def test_control_held34_006_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tremble trace summary')))

    def test_control_held34_007_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shudder trace summary')))

    def test_control_held34_008_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk cower summary trace')))

    def test_control_held34_009_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team grovel trace summary')))

    def test_control_held34_010_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snivel trace summary')))

    def test_control_held34_011_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋈ trace summary')))

    def test_control_held34_012_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋊ trace summary')))

    def test_control_held34_013_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋋ trace summary')))

    def test_control_held34_014_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋌ trace summary')))

    def test_control_held34_015_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧈ trace summary')))

    def test_control_held34_016_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧉ trace summary')))

    def test_control_held34_017_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦅panel⦆ trace summary')))

    def test_control_held34_018_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⟦panel⟧ trace summary')))

    def test_control_held34_019_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger （panel） trace summary')))

    def test_control_held34_020_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸕panel⸖ trace summary')))

    def test_control_held34_021_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃔ trace summary')))

    def test_control_held34_022_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃕ trace summary')))

    def test_control_held34_023_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃘ trace summary')))

    def test_control_held34_024_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃚ trace summary')))

    def test_control_held34_025_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃜ trace summary')))

    def test_control_held34_026_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃝ trace summary')))

    def test_control_held34_027_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃞ trace summary')))

    def test_control_held34_028_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃟ trace summary')))

    def test_control_held34_029_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃠ trace summary')))

    def test_control_held34_030_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃣ trace summary')))

    def test_control_held34_031_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃧ trace summary')))

    def test_control_held34_032_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⁅panel⁆ trace summary')))

    def test_control_held34_033_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \\\\ trace summary')))

    def test_control_held34_034_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger || trace summary')))

    def test_control_held34_035_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger * trace summary')))

    def test_control_held34_036_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace board gate summary')))

    def test_control_held34_037_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace board gate summary')))

    def test_control_held34_038_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yank trace board gate summary')))

    def test_control_held34_039_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bore trace board gate summary')))

    def test_control_held34_040_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk rode summary board gate trace')))

    def test_control_held34_041_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fled trace board gate summary')))

    def test_control_held34_042_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sought trace board gate summary')))

    def test_control_held34_043_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel paid trace board gate summary')))

    def test_control_held34_044_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chose trace board gate summary')))

    def test_control_held34_045_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel reviewed trace board gate summary')))

    def test_control_held34_046_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel logs trace board gate summary')))

    def test_control_held34_047_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel bore traceboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held34_048_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel chose traceboardgatereviewannexpanelsummary')))

    def test_control_held34_049_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel reviewed the traceboardgatereviewannexsummary')))

    # ------------------------------------------------------
    # Governed closings of R16-34-02, standing governed
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
    # Held governed forms of R16-34-01, standing governed
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
        self._candidate(_bad('Boardstorybooktallye'), _read('Boardstorybooktallye'))

    def test_control_underheld_014_governed(self):
        self._candidate(_bad('Songbooktally'), _read('Songbooktally'))

    def test_control_underheld_015_governed(self):
        self._candidate(_bad('Songbookstallies'), _read('Songbookstallies'))

    def test_control_underheld_016_governed(self):
        self._candidate(_bad('Appendixtally'), _read('Appendixtally'))

    def test_control_underheld_017_governed(self):
        self._candidate(_bad('Supplementtally'), _read('Supplementtally'))

    def test_control_underheld_018_governed(self):
        self._candidate(_bad('Compendiumtally'), _read('Compendiumtally'))

    def test_control_underheld_019_governed(self):
        self._candidate(_bad('Digesttally'), _read('Digesttally'))

    def test_control_underheld_020_governed(self):
        self._candidate(_bad('Thesaurustally'), _read('Thesaurustally'))

    def test_control_underheld_021_governed(self):
        self._candidate(_bad('Boarddictionarytally'), _read('Boarddictionarytally'))

    def test_control_underheld_022_governed(self):
        self._candidate(_bad('Tallyaz3'), _read('Tallyaz3'))

    def test_control_underheld_023_governed(self):
        self._candidate(_bad('Boardtallyaz3'), _read('Boardtallyaz3'))

    def test_control_underheld_024_governed(self):
        self._candidate(_bad('Boardhymnaltallye'), _read('Boardhymnaltallye'))

    def test_control_underheld_025_governed(self):
        self._candidate(_bad('Boardmissaltalliez'), _read('Boardmissaltalliez'))

    def test_control_underheld_026_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseseseseses'))

    def test_control_underheld_027_governed(self):
        self._candidate(_bad('Trace summarisingeseseseseseseseseseseseseseses'), _read('Trace summarisingeseseseseseseseseseseseseseses'))

    def test_control_underheld_028_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseseseses'))

    def test_control_underheld_029_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseseseses'))

    def test_control_underheld_030_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseseseses'))

    def test_control_underheld_031_governed(self):
        self._candidate(_bad('Trace summaryeseseseseseseseseseseseseseseses'), _read('Trace summaryeseseseseseseseseseseseseseseses'))

    def test_control_underheld_032_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseseseses'))

    def test_control_underheld_033_governed(self):
        self._candidate(_bad('Board ǆally'), _read('Board ǆally'))

    def test_control_underheld_034_governed(self):
        self._candidate(_bad('Trace suǆmarise'), _read('Trace suǆmarise'))

    def test_control_underheld_035_governed(self):
        self._candidate(_bad('Board ǌally'), _read('Board ǌally'))

    def test_control_underheld_036_governed(self):
        self._candidate(_bad('Board taǌy'), _read('Board taǌy'))

    def test_control_underheld_037_governed(self):
        self._candidate(_bad('Board ǎally'), _read('Board ǎally'))

    def test_control_underheld_038_governed(self):
        self._candidate(_bad('Trace summaǎise'), _read('Trace summaǎise'))

    def test_control_underheld_039_governed(self):
        self._candidate(_bad('Board Ǟally'), _read('Board Ǟally'))

    def test_control_underheld_040_governed(self):
        self._candidate(_bad('Trace summarisǞ'), _read('Trace summarisǞ'))

    def test_control_underheld_041_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'))

    def test_control_underheld_042_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpaneltrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpaneltrace'))

    def test_control_underheld_043_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'))

    def test_control_underheld_044_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review summary'))

    def test_control_underheld_045_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review trace'))

    def test_control_underheld_046_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate review for step 2'))

    def test_control_underheld_047_governed(self):
        self._candidate(_bad('Board ɩally'), _read('Board ɩally'))

    def test_control_underheld_048_governed(self):
        self._candidate(_bad('Board ɫally'), _read('Board ɫally'))

    def test_control_underheld_049_governed(self):
        self._candidate(_bad('Board ɬally'), _read('Board ɬally'))

    def test_control_underheld_050_governed(self):
        self._candidate(_bad('Board ɭally'), _read('Board ɭally'))

    def test_control_underheld_051_governed(self):
        self._candidate(_bad('Board ɮally'), _read('Board ɮally'))

    def test_control_underheld_052_governed(self):
        self._candidate(_bad('Board ɯally'), _read('Board ɯally'))

    def test_control_underheld_053_governed(self):
        self._candidate(_bad('Board ɰally'), _read('Board ɰally'))

    def test_control_underheld_054_governed(self):
        self._candidate(_bad('Board ɱally'), _read('Board ɱally'))

    def test_control_underheld_055_governed(self):
        self._candidate(_bad('Board ɲally'), _read('Board ɲally'))

    def test_control_underheld_056_governed(self):
        self._candidate(_bad('Board ɳally'), _read('Board ɳally'))

    def test_control_underheld_057_governed(self):
        self._candidate(_bad('Board ɴally'), _read('Board ɴally'))

    def test_control_underheld_058_governed(self):
        self._candidate(_bad('Board ɵally'), _read('Board ɵally'))

    def test_control_underheld_059_governed(self):
        self._candidate(_bad('Board ɶally'), _read('Board ɶally'))

    def test_control_underheld_060_governed(self):
        self._candidate(_bad('Board ɷally'), _read('Board ɷally'))

    def test_control_underheld_061_governed(self):
        self._candidate(_bad('Board ɸally'), _read('Board ɸally'))

    def test_control_underheld_062_governed(self):
        self._candidate(_bad('Board ɼally'), _read('Board ɼally'))

    def test_control_underheld_063_governed(self):
        self._candidate(_bad('Board ɽally'), _read('Board ɽally'))

    def test_control_underheld_064_governed(self):
        self._candidate(_bad('Board ʀally'), _read('Board ʀally'))

    def test_control_underheld_065_governed(self):
        self._candidate(_bad('Board ʁally'), _read('Board ʁally'))

    def test_control_underheld_066_governed(self):
        self._candidate(_bad('Board ʂally'), _read('Board ʂally'))

    def test_control_underheld_067_governed(self):
        self._candidate(_bad('Board ʃally'), _read('Board ʃally'))

    def test_control_underheld_068_governed(self):
        self._candidate(_bad('Board ʄally'), _read('Board ʄally'))

    def test_control_underheld_069_governed(self):
        self._candidate(_bad('Board ʇally'), _read('Board ʇally'))

    def test_control_underheld_070_governed(self):
        self._candidate(_bad('Board ʈally'), _read('Board ʈally'))

    def test_control_underheld_071_governed(self):
        self._candidate(_bad('Board taɩly'), _read('Board taɩly'))

    def test_control_underheld_072_governed(self):
        self._candidate(_bad('Board taɫly'), _read('Board taɫly'))

    def test_control_underheld_073_governed(self):
        self._candidate(_bad('Board taɬly'), _read('Board taɬly'))

    def test_control_underheld_074_governed(self):
        self._candidate(_bad('Board taɭly'), _read('Board taɭly'))

    def test_control_underheld_075_governed(self):
        self._candidate(_bad('Board taɮly'), _read('Board taɮly'))

    def test_control_underheld_076_governed(self):
        self._candidate(_bad('Board taɯly'), _read('Board taɯly'))

    def test_control_underheld_077_governed(self):
        self._candidate(_bad('Board taɰly'), _read('Board taɰly'))

    def test_control_underheld_078_governed(self):
        self._candidate(_bad('Board taɱly'), _read('Board taɱly'))

    def test_control_underheld_079_governed(self):
        self._candidate(_bad('Board taɲly'), _read('Board taɲly'))

    def test_control_underheld_080_governed(self):
        self._candidate(_bad('Board taɳly'), _read('Board taɳly'))

    def test_control_underheld_081_governed(self):
        self._candidate(_bad('Board taɴly'), _read('Board taɴly'))

    def test_control_underheld_082_governed(self):
        self._candidate(_bad('Board taɵly'), _read('Board taɵly'))

    def test_control_underheld_083_governed(self):
        self._candidate(_bad('Board taɶly'), _read('Board taɶly'))

    def test_control_underheld_084_governed(self):
        self._candidate(_bad('Board taɷly'), _read('Board taɷly'))

    def test_control_underheld_085_governed(self):
        self._candidate(_bad('Board taɸly'), _read('Board taɸly'))

    def test_control_underheld_086_governed(self):
        self._candidate(_bad('Board taɼly'), _read('Board taɼly'))

    def test_control_underheld_087_governed(self):
        self._candidate(_bad('Board taʀly'), _read('Board taʀly'))

    def test_control_underheld_088_governed(self):
        self._candidate(_bad('Board taʁly'), _read('Board taʁly'))

    def test_control_underheld_089_governed(self):
        self._candidate(_bad('Board taʃly'), _read('Board taʃly'))

    def test_control_underheld_090_governed(self):
        self._candidate(_bad('Board taʄly'), _read('Board taʄly'))

    def test_control_underheld_091_governed(self):
        self._candidate(_bad('Board taʈly'), _read('Board taʈly'))

    def test_control_underheld_092_governed(self):
        self._candidate(_bad('Trace sɩmmarise'), _read('Trace sɩmmarise'))

    def test_control_underheld_093_governed(self):
        self._candidate(_bad('Trace sɫmmarise'), _read('Trace sɫmmarise'))

    def test_control_underheld_094_governed(self):
        self._candidate(_bad('Trace sɬmmarise'), _read('Trace sɬmmarise'))

    def test_control_underheld_095_governed(self):
        self._candidate(_bad('Trace sɭmmarise'), _read('Trace sɭmmarise'))

    def test_control_underheld_096_governed(self):
        self._candidate(_bad('Trace sɮmmarise'), _read('Trace sɮmmarise'))

    def test_control_underheld_097_governed(self):
        self._candidate(_bad('Trace sɯmmarise'), _read('Trace sɯmmarise'))

    def test_control_underheld_098_governed(self):
        self._candidate(_bad('Trace sɰmmarise'), _read('Trace sɰmmarise'))

    def test_control_underheld_099_governed(self):
        self._candidate(_bad('Trace sɱmmarise'), _read('Trace sɱmmarise'))

    def test_control_underheld_100_governed(self):
        self._candidate(_bad('Trace sɲmmarise'), _read('Trace sɲmmarise'))

    def test_control_underheld_101_governed(self):
        self._candidate(_bad('Trace sɳmmarise'), _read('Trace sɳmmarise'))

    def test_control_underheld_102_governed(self):
        self._candidate(_bad('Trace sɴmmarise'), _read('Trace sɴmmarise'))

    def test_control_underheld_103_governed(self):
        self._candidate(_bad('Trace sɵmmarise'), _read('Trace sɵmmarise'))

    def test_control_underheld_104_governed(self):
        self._candidate(_bad('Trace sɶmmarise'), _read('Trace sɶmmarise'))

    def test_control_underheld_105_governed(self):
        self._candidate(_bad('Trace sɷmmarise'), _read('Trace sɷmmarise'))

    def test_control_underheld_106_governed(self):
        self._candidate(_bad('Trace sɸmmarise'), _read('Trace sɸmmarise'))

    def test_control_underheld_107_governed(self):
        self._candidate(_bad('Trace sɼmmarise'), _read('Trace sɼmmarise'))

    def test_control_underheld_108_governed(self):
        self._candidate(_bad('Trace sʀmmarise'), _read('Trace sʀmmarise'))

    def test_control_underheld_109_governed(self):
        self._candidate(_bad('Trace sʁmmarise'), _read('Trace sʁmmarise'))

    def test_control_underheld_110_governed(self):
        self._candidate(_bad('Trace sʃmmarise'), _read('Trace sʃmmarise'))

    def test_control_underheld_111_governed(self):
        self._candidate(_bad('Trace sʄmmarise'), _read('Trace sʄmmarise'))

    def test_control_underheld_112_governed(self):
        self._candidate(_bad('Trace sʈmmarise'), _read('Trace sʈmmarise'))

    def test_control_underheld_113_governed(self):
        self._candidate(_bad('Trace sumɩarise'), _read('Trace sumɩarise'))

    def test_control_underheld_114_governed(self):
        self._candidate(_bad('Trace sumɫarise'), _read('Trace sumɫarise'))

    def test_control_underheld_115_governed(self):
        self._candidate(_bad('Trace sumɬarise'), _read('Trace sumɬarise'))

    def test_control_underheld_116_governed(self):
        self._candidate(_bad('Trace sumɭarise'), _read('Trace sumɭarise'))

    def test_control_underheld_117_governed(self):
        self._candidate(_bad('Trace sumɮarise'), _read('Trace sumɮarise'))

    def test_control_underheld_118_governed(self):
        self._candidate(_bad('Trace sumɯarise'), _read('Trace sumɯarise'))

    def test_control_underheld_119_governed(self):
        self._candidate(_bad('Trace sumɰarise'), _read('Trace sumɰarise'))

    def test_control_underheld_120_governed(self):
        self._candidate(_bad('Trace sumɱarise'), _read('Trace sumɱarise'))

    def test_control_underheld_121_governed(self):
        self._candidate(_bad('Trace sumɲarise'), _read('Trace sumɲarise'))

    def test_control_underheld_122_governed(self):
        self._candidate(_bad('Trace sumɳarise'), _read('Trace sumɳarise'))

    def test_control_underheld_123_governed(self):
        self._candidate(_bad('Trace sumɴarise'), _read('Trace sumɴarise'))

    def test_control_underheld_124_governed(self):
        self._candidate(_bad('Trace sumɵarise'), _read('Trace sumɵarise'))

    def test_control_underheld_125_governed(self):
        self._candidate(_bad('Trace sumɶarise'), _read('Trace sumɶarise'))

    def test_control_underheld_126_governed(self):
        self._candidate(_bad('Trace sumɷarise'), _read('Trace sumɷarise'))

    def test_control_underheld_127_governed(self):
        self._candidate(_bad('Trace sumɸarise'), _read('Trace sumɸarise'))

    def test_control_underheld_128_governed(self):
        self._candidate(_bad('Trace sumɼarise'), _read('Trace sumɼarise'))

    def test_control_underheld_129_governed(self):
        self._candidate(_bad('Trace sumʀarise'), _read('Trace sumʀarise'))

    def test_control_underheld_130_governed(self):
        self._candidate(_bad('Trace sumʁarise'), _read('Trace sumʁarise'))

    def test_control_underheld_131_governed(self):
        self._candidate(_bad('Trace sumʃarise'), _read('Trace sumʃarise'))

    def test_control_underheld_132_governed(self):
        self._candidate(_bad('Trace sumʄarise'), _read('Trace sumʄarise'))

    def test_control_underheld_133_governed(self):
        self._candidate(_bad('Trace sumʈarise'), _read('Trace sumʈarise'))

    def test_control_underheld_134_governed(self):
        self._candidate(_bad('Trace summariɩe'), _read('Trace summariɩe'))

    def test_control_underheld_135_governed(self):
        self._candidate(_bad('Trace summariɫe'), _read('Trace summariɫe'))

    def test_control_underheld_136_governed(self):
        self._candidate(_bad('Trace summariɬe'), _read('Trace summariɬe'))

    def test_control_underheld_137_governed(self):
        self._candidate(_bad('Trace summariɭe'), _read('Trace summariɭe'))

    def test_control_underheld_138_governed(self):
        self._candidate(_bad('Trace summariɮe'), _read('Trace summariɮe'))

    def test_control_underheld_139_governed(self):
        self._candidate(_bad('Trace summariɯe'), _read('Trace summariɯe'))

    def test_control_underheld_140_governed(self):
        self._candidate(_bad('Trace summariɰe'), _read('Trace summariɰe'))

    def test_control_underheld_141_governed(self):
        self._candidate(_bad('Trace summariɱe'), _read('Trace summariɱe'))

    def test_control_underheld_142_governed(self):
        self._candidate(_bad('Trace summariɲe'), _read('Trace summariɲe'))

    def test_control_underheld_143_governed(self):
        self._candidate(_bad('Trace summariɳe'), _read('Trace summariɳe'))

    def test_control_underheld_144_governed(self):
        self._candidate(_bad('Trace summariɴe'), _read('Trace summariɴe'))

    def test_control_underheld_145_governed(self):
        self._candidate(_bad('Trace summariɵe'), _read('Trace summariɵe'))

    def test_control_underheld_146_governed(self):
        self._candidate(_bad('Trace summariɶe'), _read('Trace summariɶe'))

    def test_control_underheld_147_governed(self):
        self._candidate(_bad('Trace summariɷe'), _read('Trace summariɷe'))

    def test_control_underheld_148_governed(self):
        self._candidate(_bad('Trace summariɸe'), _read('Trace summariɸe'))

    def test_control_underheld_149_governed(self):
        self._candidate(_bad('Trace summariɼe'), _read('Trace summariɼe'))

    def test_control_underheld_150_governed(self):
        self._candidate(_bad('Trace summariʀe'), _read('Trace summariʀe'))

    def test_control_underheld_151_governed(self):
        self._candidate(_bad('Trace summariʁe'), _read('Trace summariʁe'))

    def test_control_underheld_152_governed(self):
        self._candidate(_bad('Trace summariʂe'), _read('Trace summariʂe'))

    def test_control_underheld_153_governed(self):
        self._candidate(_bad('Trace summariʃe'), _read('Trace summariʃe'))

    def test_control_underheld_154_governed(self):
        self._candidate(_bad('Trace summariʄe'), _read('Trace summariʄe'))

    def test_control_underheld_155_governed(self):
        self._candidate(_bad('Trace summariʅe'), _read('Trace summariʅe'))

    def test_control_underheld_156_governed(self):
        self._candidate(_bad('Trace summariʈe'), _read('Trace summariʈe'))

    def test_control_underheld_157_governed(self):
        self._candidate(_bad('Trace summarisɩ'), _read('Trace summarisɩ'))

    def test_control_underheld_158_governed(self):
        self._candidate(_bad('Trace summarisɫ'), _read('Trace summarisɫ'))

    def test_control_underheld_159_governed(self):
        self._candidate(_bad('Trace summarisɬ'), _read('Trace summarisɬ'))

    def test_control_underheld_160_governed(self):
        self._candidate(_bad('Trace summarisɭ'), _read('Trace summarisɭ'))

    def test_control_underheld_161_governed(self):
        self._candidate(_bad('Trace summarisɮ'), _read('Trace summarisɮ'))

    def test_control_underheld_162_governed(self):
        self._candidate(_bad('Trace summarisɯ'), _read('Trace summarisɯ'))

    def test_control_underheld_163_governed(self):
        self._candidate(_bad('Trace summarisɰ'), _read('Trace summarisɰ'))

    def test_control_underheld_164_governed(self):
        self._candidate(_bad('Trace summarisɱ'), _read('Trace summarisɱ'))

    def test_control_underheld_165_governed(self):
        self._candidate(_bad('Trace summarisɲ'), _read('Trace summarisɲ'))

    def test_control_underheld_166_governed(self):
        self._candidate(_bad('Trace summarisɳ'), _read('Trace summarisɳ'))

    def test_control_underheld_167_governed(self):
        self._candidate(_bad('Trace summarisɴ'), _read('Trace summarisɴ'))

    def test_control_underheld_168_governed(self):
        self._candidate(_bad('Trace summarisɵ'), _read('Trace summarisɵ'))

    def test_control_underheld_169_governed(self):
        self._candidate(_bad('Trace summarisɶ'), _read('Trace summarisɶ'))

    def test_control_underheld_170_governed(self):
        self._candidate(_bad('Trace summarisɷ'), _read('Trace summarisɷ'))

    def test_control_underheld_171_governed(self):
        self._candidate(_bad('Trace summarisɸ'), _read('Trace summarisɸ'))

    def test_control_underheld_172_governed(self):
        self._candidate(_bad('Trace summarisɼ'), _read('Trace summarisɼ'))

    def test_control_underheld_173_governed(self):
        self._candidate(_bad('Trace summarisʀ'), _read('Trace summarisʀ'))

    def test_control_underheld_174_governed(self):
        self._candidate(_bad('Trace summarisʁ'), _read('Trace summarisʁ'))

    def test_control_underheld_175_governed(self):
        self._candidate(_bad('Trace summarisʂ'), _read('Trace summarisʂ'))

    def test_control_underheld_176_governed(self):
        self._candidate(_bad('Trace summarisʃ'), _read('Trace summarisʃ'))

    def test_control_underheld_177_governed(self):
        self._candidate(_bad('Trace summarisʄ'), _read('Trace summarisʄ'))

    def test_control_underheld_178_governed(self):
        self._candidate(_bad('Trace summarisʈ'), _read('Trace summarisʈ'))
