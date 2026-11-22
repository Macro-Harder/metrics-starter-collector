"""Step 16 fix pass 32 unit 2 tests: the Q-4 closing unit.

Pinning tests for register items R16-32-01 (Medium,
B32-C01 and B32-B01) and R16-32-03 (Medium, the single
form Songbookstallies) of Step 16 round 32. The
governing rule of the pass, in its extended form: a
piece not read in full, for whatever reason, is not
read, and its converse: a piece that is no feeder
flips nothing.

R16-32-01: malformed tally statement heads standing
unread past the restated boundary of fix pass 31, on
the counted pattern head agnosticism ground alone: the
pattern standing counted over a plain whole word
pattern, so a malformed head whose counted sibling
counts stands missing in the row although it stands as
a feeder statement in a form the row cannot parse.
Four hundred and twenty eight distinct alone forms
stand driven in ten subfamilies: (a) tally forms fused
behind record words no widening has named and behind
the plurals of record words in the same position,
thirty three forms; (b) composite openings built on
those forms, ten forms; (c) a variant spelling in that
composite opening position built on those words, three
forms; (d) the variant spellings past the widened
variant sets of eighty five and eighty six, eighteen
forms; (e) the summary word in further forms past the
one hundred and twenty six, ten forms; (f) the fused
closings built on those forms, six forms; (g) the
fused closings with nineteen governed words of subject
between, three forms; (h) the inserted closings with
twenty two words of subject between in their wide,
middle swap and full swap shapes in both directions,
six forms; (i) the for step closing with twenty two
words of subject between, one form; and (j) further
Latin and kindred letters past the widened fold set,
each standing in a position the folding does not read,
three hundred and thirty eight forms, the correctness
forms of that subfamily standing in their exact driven
strings as the probe logs of the correctness staging
record them and the breaker forms standing in the
words the breaker paper names. R16-32-03: the single
form Songbookstallies, standing missing at code level
in every plain drive against its governed recording,
the plural s of songbooks standing between the book
block and the tallies form, standing as a named single
form defect test beside the subfamilies above. The
fifty four underreach assertions of the round 32
breaker exhibit stand adopted in this module: the
fifty alone form assertions of B32-B01 stand among the
defect tests of the subfamilies above in their driven
words, and the beside assertions, the gate ruling
assertion and the code level assertion of that exhibit
stand as defect tests here in the forms the exhibit
names them. The defect stands bounded in the open by
its held controls: every form of R16-32-02 standing
missing, every held form of that item standing missing
in its recorded form, every governed closing of that
item standing governed, and on the underreach side the
governed neighbours of both papers standing governed,
the governed forms of subfamily (a) of the correctness
paper standing governed through the governed words and
blocks at the close of their fused forms, the book
singulars among them, Songbooktally among them standing
governed through the book block in its own form, the
governed composite openings and the governed variant
composite openings of that paper standing governed,
Boarddictionarytallye and Gatevocabularytalliez among
them, the governed summarisation forms standing
governed in the widened enumeration at their family
positions, the governed letter forms of subfamily (j)
of the correctness paper standing governed at their
positions, Datatally of the breaker paper standing
governed, Boarddictionarytally standing governed
through the further position limb, the candidate
record words of the breaker paper standing governed,
the fused and inserted closings standing at their
governed counts, the eighteen word fused between
closing, the twenty one word forward and reversed
inserted closings and the twenty one word for step
closing standing governed, and the plain Latin
spellings standing at their standings. Locus:
derivation_core.py, _tally_statement_head and its
standing helpers and constants. The cure these tests
pin widens what a malformed tally statement head is in
standing: the governed fused prefix set widened by the
record words and plural stems of this round and by the
songbooks stem of R16-32-03, the variant sets widened
by the spellings of this round, the summary word set
widened by the further forms of this round, the fused
between reach widened to nineteen governed words, the
inserted closings standing at twenty two words
forward, twenty two words reversed and twenty two
words in the for step form under the wide test, and
the folding widened by the whole word readings of this
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


class TestStep16Fix32Unit2(FixtureTestCase):

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
    # Defect forms of R16-32-01, subfamily (a):
    # fused record words and the plurals of record words.
    # ------------------------------------------------------

    def test_r16_32_01_a_00_governed(self):
        self._candidate(_bad('Chapbookstallies'), _read('Chapbookstallies'))

    def test_r16_32_01_a_01_governed(self):
        self._candidate(_bad('Daybookstallies'), _read('Daybookstallies'))

    def test_r16_32_01_a_02_governed(self):
        self._candidate(_bad('Workbookstallies'), _read('Workbookstallies'))

    def test_r16_32_01_a_03_governed(self):
        self._candidate(_bad('Textbookstallies'), _read('Textbookstallies'))

    def test_r16_32_01_a_04_governed(self):
        self._candidate(_bad('Yearbookstallies'), _read('Yearbookstallies'))

    def test_r16_32_01_a_05_governed(self):
        self._candidate(_bad('Cookbookstallies'), _read('Cookbookstallies'))

    def test_r16_32_01_a_06_governed(self):
        self._candidate(_bad('Handbookstallies'), _read('Handbookstallies'))

    def test_r16_32_01_a_07_governed(self):
        self._candidate(_bad('Logbookstallies'), _read('Logbookstallies'))

    def test_r16_32_01_a_08_governed(self):
        self._candidate(_bad('Guestbookstallies'), _read('Guestbookstallies'))

    def test_r16_32_01_a_09_governed(self):
        self._candidate(_bad('Scrapbookstallies'), _read('Scrapbookstallies'))

    def test_r16_32_01_a_10_governed(self):
        self._candidate(_bad('Anthemtally'), _read('Anthemtally'))

    def test_r16_32_01_a_11_governed(self):
        self._candidate(_bad('Anthemstallies'), _read('Anthemstallies'))

    def test_r16_32_01_a_12_governed(self):
        self._candidate(_bad('Broadsidetally'), _read('Broadsidetally'))

    def test_r16_32_01_a_13_governed(self):
        self._candidate(_bad('Broadsidestallies'), _read('Broadsidestallies'))

    def test_r16_32_01_a_14_governed(self):
        self._candidate(_bad('Diurnaltally'), _read('Diurnaltally'))

    def test_r16_32_01_a_15_governed(self):
        self._candidate(_bad('Diurnalstallies'), _read('Diurnalstallies'))

    def test_r16_32_01_a_16_governed(self):
        self._candidate(_bad('Octavotally'), _read('Octavotally'))

    def test_r16_32_01_a_17_governed(self):
        self._candidate(_bad('Octavostallies'), _read('Octavostallies'))

    def test_r16_32_01_a_18_governed(self):
        self._candidate(_bad('Quartotally'), _read('Quartotally'))

    def test_r16_32_01_a_19_governed(self):
        self._candidate(_bad('Quartostallies'), _read('Quartostallies'))

    def test_r16_32_01_a_20_governed(self):
        self._candidate(_bad('Gradualtally'), _read('Gradualtally'))

    def test_r16_32_01_a_21_governed(self):
        self._candidate(_bad('Gradualstallies'), _read('Gradualstallies'))

    def test_r16_32_01_a_22_governed(self):
        self._candidate(_bad('Vesperstally'), _read('Vesperstally'))

    def test_r16_32_01_a_23_governed(self):
        self._candidate(_bad('Heraldtally'), _read('Heraldtally'))

    def test_r16_32_01_a_24_governed(self):
        self._candidate(_bad('Chroniclettally'), _read('Chroniclettally'))

    def test_r16_32_01_a_25_governed(self):
        self._candidate(_bad('Analysistally'), _read('Analysistally'))

    def test_r16_32_01_a_26_governed(self):
        self._candidate(_bad('Crisistally'), _read('Crisistally'))

    def test_r16_32_01_a_27_governed(self):
        self._candidate(_bad('Oasistally'), _read('Oasistally'))

    def test_r16_32_01_a_28_governed(self):
        self._candidate(_bad('Heraldstallies'), _read('Heraldstallies'))

    def test_r16_32_01_a_29_governed(self):
        self._candidate(_bad('Thesesstallies'), _read('Thesesstallies'))

    def test_r16_32_01_a_30_governed(self):
        self._candidate(_bad('Analysesstallies'), _read('Analysesstallies'))

    def test_r16_32_01_a_31_governed(self):
        self._candidate(_bad('Oasesstallies'), _read('Oasesstallies'))

    def test_r16_32_01_a_32_governed(self):
        self._candidate(_bad('Crisesstallies'), _read('Crisesstallies'))

    # ------------------------------------------------------
    # Defect forms of R16-32-01, subfamily (b):
    # composite openings built on those forms.
    # ------------------------------------------------------

    def test_r16_32_01_b_00_governed(self):
        self._candidate(_bad('Boardchapbookstallies'), _read('Boardchapbookstallies'))

    def test_r16_32_01_b_01_governed(self):
        self._candidate(_bad('Boardhandbookstallies'), _read('Boardhandbookstallies'))

    def test_r16_32_01_b_02_governed(self):
        self._candidate(_bad('Boardanthemtally'), _read('Boardanthemtally'))

    def test_r16_32_01_b_03_governed(self):
        self._candidate(_bad('Gatebroadsidetally'), _read('Gatebroadsidetally'))

    def test_r16_32_01_b_04_governed(self):
        self._candidate(_bad('Boardyearbookstallies'), _read('Boardyearbookstallies'))

    def test_r16_32_01_b_05_governed(self):
        self._candidate(_bad('Boarddiurnaltally'), _read('Boarddiurnaltally'))

    def test_r16_32_01_b_06_governed(self):
        self._candidate(_bad('Boardheraldtally'), _read('Boardheraldtally'))

    def test_r16_32_01_b_07_governed(self):
        self._candidate(_bad('Gatechroniclettally'), _read('Gatechroniclettally'))

    def test_r16_32_01_b_08_governed(self):
        self._candidate(_bad('Reviewchroniclettally'), _read('Reviewchroniclettally'))

    def test_r16_32_01_b_09_governed(self):
        self._candidate(_bad('Boardanalysistally'), _read('Boardanalysistally'))

    # ------------------------------------------------------
    # Defect forms of R16-32-01, subfamily (c):
    # a variant spelling in that composite position.
    # ------------------------------------------------------

    def test_r16_32_01_c_00_governed(self):
        self._candidate(_bad('Boardanthemtallye'), _read('Boardanthemtallye'))

    def test_r16_32_01_c_01_governed(self):
        self._candidate(_bad('Boardheraldtallye'), _read('Boardheraldtallye'))

    def test_r16_32_01_c_02_governed(self):
        self._candidate(_bad('Gatechroniclettalliez'), _read('Gatechroniclettalliez'))

    # ------------------------------------------------------
    # Defect forms of R16-32-01, subfamily (d):
    # the variant spellings past the widened sets.
    # ------------------------------------------------------

    def test_r16_32_01_d_00_governed(self):
        self._candidate(_bad('Tallya9'), _read('Tallya9'))

    def test_r16_32_01_d_01_governed(self):
        self._candidate(_bad('Tallyo8'), _read('Tallyo8'))

    def test_r16_32_01_d_02_governed(self):
        self._candidate(_bad('Tallyu8'), _read('Tallyu8'))

    def test_r16_32_01_d_03_governed(self):
        self._candidate(_bad('Tallyai8'), _read('Tallyai8'))

    def test_r16_32_01_d_04_governed(self):
        self._candidate(_bad('Tallyez7'), _read('Tallyez7'))

    def test_r16_32_01_d_05_governed(self):
        self._candidate(_bad('Tallyaz7'), _read('Tallyaz7'))

    def test_r16_32_01_d_06_governed(self):
        self._candidate(_bad('Tallyeo10'), _read('Tallyeo10'))

    def test_r16_32_01_d_07_governed(self):
        self._candidate(_bad('Tallyia2'), _read('Tallyia2'))

    def test_r16_32_01_d_08_governed(self):
        self._candidate(_bad('Boardtallya9'), _read('Boardtallya9'))

    def test_r16_32_01_d_09_governed(self):
        self._candidate(_bad('Boardtallyo8'), _read('Boardtallyo8'))

    def test_r16_32_01_d_10_governed(self):
        self._candidate(_bad('Boardtallyu8'), _read('Boardtallyu8'))

    def test_r16_32_01_d_11_governed(self):
        self._candidate(_bad('Boardtallyai8'), _read('Boardtallyai8'))

    def test_r16_32_01_d_12_governed(self):
        self._candidate(_bad('Boardtallyez7'), _read('Boardtallyez7'))

    def test_r16_32_01_d_13_governed(self):
        self._candidate(_bad('Boardtallyaz7'), _read('Boardtallyaz7'))

    def test_r16_32_01_d_14_governed(self):
        self._candidate(_bad('Boardtallyeo10'), _read('Boardtallyeo10'))

    def test_r16_32_01_d_15_governed(self):
        self._candidate(_bad('Boardtallyia2'), _read('Boardtallyia2'))

    def test_r16_32_01_d_16_governed(self):
        self._candidate(_bad('Tallye8'), _read('Tallye8'))

    def test_r16_32_01_d_17_governed(self):
        self._candidate(_bad('Boardtallye8'), _read('Boardtallye8'))

    # ------------------------------------------------------
    # Defect forms of R16-32-01, subfamily (e):
    # the summary word in further forms.
    # ------------------------------------------------------

    def test_r16_32_01_e_00_governed(self):
        self._candidate(_bad('Trace summarisereseseseseseseseseseseseseses'), _read('Trace summarisereseseseseseseseseseseseseses'))

    def test_r16_32_01_e_01_governed(self):
        self._candidate(_bad('Trace summarisingeseseseseseseseseseseseseses'), _read('Trace summarisingeseseseseseseseseseseseseses'))

    # Correction in place, recorded in the standing form.
    # The coordinator ruling on the stop of this unit, as
    # carried in design/steps/step-16r-fix32-unit2-report.md,
    # holds that the driven record governs the pins where
    # the register text stands one es repetition short of
    # the driven forms. The register text at this place
    # stands one es repetition short, and the form on that
    # text derives on the entering code. This test keeps
    # its identity and its place; its expectation stands
    # corrected in place to the entering truth, the form
    # derives on the entering code, and it stands as a
    # control in place. The driven form, Trace summarieseseseseseseseseseseseseseses,
    # stands pinned elsewhere in this module as
    # test_r16_32_01_e_06_governed, so the form is not cured twice
    # and not dropped.
    def test_r16_32_01_e_02_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseses'))

    # Correction in place, recorded in the standing form.
    # The coordinator ruling on the stop of this unit, as
    # carried in design/steps/step-16r-fix32-unit2-report.md,
    # holds that the driven record governs the pins where
    # the register text stands one es repetition short of
    # the driven forms. The register text at this place
    # stands one es repetition short, and the form on that
    # text derives on the entering code. This test keeps
    # its identity and its place; its expectation stands
    # corrected in place to the entering truth, the form
    # derives on the entering code, and it stands as a
    # control in place. The driven form, Trace summarisedeseseseseseseseseseseseseses,
    # stands pinned elsewhere in this module as
    # test_r16_32_01_e_07_governed, so the form is not cured twice
    # and not dropped.
    def test_r16_32_01_e_03_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseses'))

    # Correction in place, recorded in the standing form.
    # The coordinator ruling on the stop of this unit, as
    # carried in design/steps/step-16r-fix32-unit2-report.md,
    # holds that the driven record governs the pins where
    # the register text stands one es repetition short of
    # the driven forms. The register text at this place
    # stands one es repetition short, and the form on that
    # text derives on the entering code. This test keeps
    # its identity and its place; its expectation stands
    # corrected in place to the entering truth, the form
    # derives on the entering code, and it stands as a
    # control in place. The driven form, Trace summariseeseseseseseseseseseseseseseses,
    # stands pinned elsewhere in this module as
    # test_r16_32_01_e_08_governed, so the form is not cured twice
    # and not dropped.
    def test_r16_32_01_e_04_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseses'))

    def test_r16_32_01_e_05_governed(self):
        self._candidate(_bad('Trace summaryeseseseseseseseseseseseseseses'), _read('Trace summaryeseseseseseseseseseseseseseses'))

    def test_r16_32_01_e_06_governed(self):
        self._candidate(_bad('Trace summarieseseseseseseseseseseseseseses'), _read('Trace summarieseseseseseseseseseseseseseses'))

    def test_r16_32_01_e_07_governed(self):
        self._candidate(_bad('Trace summarisedeseseseseseseseseseseseseses'), _read('Trace summarisedeseseseseseseseseseseseseses'))

    def test_r16_32_01_e_08_governed(self):
        self._candidate(_bad('Trace summariseeseseseseseseseseseseseseseses'), _read('Trace summariseeseseseseseseseseseseseseseses'))

    def test_r16_32_01_e_09_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseseses'))

    # ------------------------------------------------------
    # Defect forms of R16-32-01, subfamily (f):
    # the fused closings built on those forms.
    # ------------------------------------------------------

    def test_r16_32_01_f_00_governed(self):
        self._candidate(_bad('Boardtracesummarisereseseseseseseseseseseseseses'), _read('Boardtracesummarisereseseseseseseseseseseseseses'))

    # Correction in place, recorded in the standing form.
    # The coordinator ruling on the stop of this unit, as
    # carried in design/steps/step-16r-fix32-unit2-report.md,
    # holds that the driven record governs the pins where
    # the register text stands one es repetition short of
    # the driven forms. The register text at this place
    # stands one es repetition short, and the driven form
    # Tracessummarieseseseseseseseseseseseseseses stands
    # in no pin of this module. This test keeps its
    # identity and its place; its string stands corrected
    # in place to the driven string, and it stands as a
    # defect test.
    def test_r16_32_01_f_01_governed(self):
        self._candidate(_bad('Tracessummarieseseseseseseseseseseseseseses'), _read('Tracessummarieseseseseseseseseseseseseseses'))

    # Correction in place, recorded in the standing form.
    # The coordinator ruling on the stop of this unit, as
    # carried in design/steps/step-16r-fix32-unit2-report.md,
    # holds that the driven record governs the pins where
    # the register text stands one es repetition short of
    # the driven forms. The register text at this place
    # stands one es repetition short, and the form on that
    # text derives on the entering code. This test keeps
    # its identity and its place; its expectation stands
    # corrected in place to the entering truth, the form
    # derives on the entering code, and it stands as a
    # control in place. The driven form, Boardtracesummarisedeseseseseseseseseseseseseses,
    # stands pinned elsewhere in this module as
    # test_r16_32_01_f_04_governed, so the form is not cured twice
    # and not dropped.
    def test_r16_32_01_f_02_governed(self):
        self._candidate(_bad('Boardtracesummarisedeseseseseseseseseseseseses'), _read('Boardtracesummarisedeseseseseseseseseseseseses'))

    # Correction in place, recorded in the standing form.
    # The coordinator ruling on the stop of this unit, as
    # carried in design/steps/step-16r-fix32-unit2-report.md,
    # holds that the driven record governs the pins where
    # the register text stands one es repetition short of
    # the driven forms. The register text at this place
    # stands one es repetition short, and the form on that
    # text derives on the entering code. This test keeps
    # its identity and its place; its expectation stands
    # corrected in place to the entering truth, the form
    # derives on the entering code, and it stands as a
    # control in place. The driven form, Tracessummaryeseseseseseseseseseseseseseses,
    # stands pinned elsewhere in this module as
    # test_r16_32_01_f_05_governed, so the form is not cured twice
    # and not dropped.
    def test_r16_32_01_f_03_governed(self):
        self._candidate(_bad('Tracessummaryeseseseseseseseseseseseseses'), _read('Tracessummaryeseseseseseseseseseseseseses'))

    def test_r16_32_01_f_04_governed(self):
        self._candidate(_bad('Boardtracesummarisedeseseseseseseseseseseseseses'), _read('Boardtracesummarisedeseseseseseseseseseseseseses'))

    def test_r16_32_01_f_05_governed(self):
        self._candidate(_bad('Tracessummaryeseseseseseseseseseseseseseses'), _read('Tracessummaryeseseseseseseseseseseseseseses'))

    # ------------------------------------------------------
    # Defect forms of R16-32-01, subfamily (g):
    # the fused closings at nineteen governed words between.
    # ------------------------------------------------------

    def test_r16_32_01_g_00_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary'))

    def test_r16_32_01_g_01_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannextrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannextrace'))

    def test_r16_32_01_g_02_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary'))

    # ------------------------------------------------------
    # Defect forms of R16-32-01, subfamily (h):
    # the inserted closings at twenty two words between.
    # ------------------------------------------------------

    def test_r16_32_01_h_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate summary'))

    def test_r16_32_01_h_01_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate summary'), _read('Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate summary'))

    def test_r16_32_01_h_02_governed(self):
        self._candidate(_bad('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate summary'), _read('Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate summary'))

    def test_r16_32_01_h_03_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate trace'))

    def test_r16_32_01_h_04_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate trace'), _read('Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex panel board gate trace'))

    def test_r16_32_01_h_05_governed(self):
        self._candidate(_bad('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate trace'), _read('Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review panel board gate trace'))

    # ------------------------------------------------------
    # Defect forms of R16-32-01, subfamily (i):
    # the for step closing at twenty two words between.
    # ------------------------------------------------------

    def test_r16_32_01_i_00_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate for step 2'))

    # ------------------------------------------------------
    # Defect forms of R16-32-01, subfamily (j):
    # further letters past the widened fold set.
    # ------------------------------------------------------

    def test_r16_32_01_j_00_governed(self):
        self._candidate(_bad('Board ɩally'), _read('Board ɩally'))

    def test_r16_32_01_j_01_governed(self):
        self._candidate(_bad('Board ɫally'), _read('Board ɫally'))

    def test_r16_32_01_j_02_governed(self):
        self._candidate(_bad('Board ɬally'), _read('Board ɬally'))

    def test_r16_32_01_j_03_governed(self):
        self._candidate(_bad('Board ɮally'), _read('Board ɮally'))

    def test_r16_32_01_j_04_governed(self):
        self._candidate(_bad('Board ɯally'), _read('Board ɯally'))

    def test_r16_32_01_j_05_governed(self):
        self._candidate(_bad('Board ɰally'), _read('Board ɰally'))

    def test_r16_32_01_j_06_governed(self):
        self._candidate(_bad('Board ɱally'), _read('Board ɱally'))

    def test_r16_32_01_j_07_governed(self):
        self._candidate(_bad('Board ɲally'), _read('Board ɲally'))

    def test_r16_32_01_j_08_governed(self):
        self._candidate(_bad('Board ɳally'), _read('Board ɳally'))

    def test_r16_32_01_j_09_governed(self):
        self._candidate(_bad('Board ɴally'), _read('Board ɴally'))

    def test_r16_32_01_j_10_governed(self):
        self._candidate(_bad('Board ɵally'), _read('Board ɵally'))

    def test_r16_32_01_j_11_governed(self):
        self._candidate(_bad('Board ɶally'), _read('Board ɶally'))

    def test_r16_32_01_j_12_governed(self):
        self._candidate(_bad('Board ɷally'), _read('Board ɷally'))

    def test_r16_32_01_j_13_governed(self):
        self._candidate(_bad('Board Ɔally'), _read('Board Ɔally'))

    def test_r16_32_01_j_14_governed(self):
        self._candidate(_bad('Board Ƌally'), _read('Board Ƌally'))

    def test_r16_32_01_j_15_governed(self):
        self._candidate(_bad('Board ƌally'), _read('Board ƌally'))

    def test_r16_32_01_j_16_governed(self):
        self._candidate(_bad('Board Əally'), _read('Board Əally'))

    def test_r16_32_01_j_17_governed(self):
        self._candidate(_bad('Board Ɛally'), _read('Board Ɛally'))

    def test_r16_32_01_j_18_governed(self):
        self._candidate(_bad('Board Ɠally'), _read('Board Ɠally'))

    def test_r16_32_01_j_19_governed(self):
        self._candidate(_bad('Board Ɩally'), _read('Board Ɩally'))

    def test_r16_32_01_j_20_governed(self):
        self._candidate(_bad('Board Ƙally'), _read('Board Ƙally'))

    def test_r16_32_01_j_21_governed(self):
        self._candidate(_bad('Board Ɯally'), _read('Board Ɯally'))

    def test_r16_32_01_j_22_governed(self):
        self._candidate(_bad('Board Ɲally'), _read('Board Ɲally'))

    def test_r16_32_01_j_23_governed(self):
        self._candidate(_bad('Board ƞally'), _read('Board ƞally'))

    def test_r16_32_01_j_24_governed(self):
        self._candidate(_bad('Board Ɵally'), _read('Board Ɵally'))

    def test_r16_32_01_j_25_governed(self):
        self._candidate(_bad('Board Ơally'), _read('Board Ơally'))

    def test_r16_32_01_j_26_governed(self):
        self._candidate(_bad('Board ơally'), _read('Board ơally'))

    def test_r16_32_01_j_27_governed(self):
        self._candidate(_bad('Board Ƣally'), _read('Board Ƣally'))

    def test_r16_32_01_j_28_governed(self):
        self._candidate(_bad('Board Ƥally'), _read('Board Ƥally'))

    def test_r16_32_01_j_29_governed(self):
        self._candidate(_bad('Board Ʀally'), _read('Board Ʀally'))

    def test_r16_32_01_j_30_governed(self):
        self._candidate(_bad('Board Ƨally'), _read('Board Ƨally'))

    def test_r16_32_01_j_31_governed(self):
        self._candidate(_bad('Board ƨally'), _read('Board ƨally'))

    def test_r16_32_01_j_32_governed(self):
        self._candidate(_bad('Board ƪally'), _read('Board ƪally'))

    def test_r16_32_01_j_33_governed(self):
        self._candidate(_bad('Board Ưally'), _read('Board Ưally'))

    def test_r16_32_01_j_34_governed(self):
        self._candidate(_bad('Board ưally'), _read('Board ưally'))

    def test_r16_32_01_j_35_governed(self):
        self._candidate(_bad('Board Ʋally'), _read('Board Ʋally'))

    def test_r16_32_01_j_36_governed(self):
        self._candidate(_bad('Board Ƴally'), _read('Board Ƴally'))

    def test_r16_32_01_j_37_governed(self):
        self._candidate(_bad('Board ƴally'), _read('Board ƴally'))

    def test_r16_32_01_j_38_governed(self):
        self._candidate(_bad('Board Ƶally'), _read('Board Ƶally'))

    def test_r16_32_01_j_39_governed(self):
        self._candidate(_bad('Board ƶally'), _read('Board ƶally'))

    def test_r16_32_01_j_40_governed(self):
        self._candidate(_bad('Board Ʒally'), _read('Board Ʒally'))

    def test_r16_32_01_j_41_governed(self):
        self._candidate(_bad('Board Ƹally'), _read('Board Ƹally'))

    def test_r16_32_01_j_42_governed(self):
        self._candidate(_bad('Board ƹally'), _read('Board ƹally'))

    def test_r16_32_01_j_43_governed(self):
        self._candidate(_bad('Board ƺally'), _read('Board ƺally'))

    def test_r16_32_01_j_44_governed(self):
        self._candidate(_bad('Board ƻally'), _read('Board ƻally'))

    def test_r16_32_01_j_45_governed(self):
        self._candidate(_bad('Board Ƽally'), _read('Board Ƽally'))

    def test_r16_32_01_j_46_governed(self):
        self._candidate(_bad('Board ƽally'), _read('Board ƽally'))

    def test_r16_32_01_j_47_governed(self):
        self._candidate(_bad('Board ƾally'), _read('Board ƾally'))

    def test_r16_32_01_j_48_governed(self):
        self._candidate(_bad('Board ƿally'), _read('Board ƿally'))

    def test_r16_32_01_j_49_governed(self):
        self._candidate(_bad('Board ǀally'), _read('Board ǀally'))

    def test_r16_32_01_j_50_governed(self):
        self._candidate(_bad('Board ǁally'), _read('Board ǁally'))

    def test_r16_32_01_j_51_governed(self):
        self._candidate(_bad('Board ǂally'), _read('Board ǂally'))

    def test_r16_32_01_j_52_governed(self):
        self._candidate(_bad('Board ǃally'), _read('Board ǃally'))

    def test_r16_32_01_j_53_governed(self):
        self._candidate(_bad('Board taɩly'), _read('Board taɩly'))

    def test_r16_32_01_j_54_governed(self):
        self._candidate(_bad('Board taɯly'), _read('Board taɯly'))

    def test_r16_32_01_j_55_governed(self):
        self._candidate(_bad('Board taɰly'), _read('Board taɰly'))

    def test_r16_32_01_j_56_governed(self):
        self._candidate(_bad('Board taɱly'), _read('Board taɱly'))

    def test_r16_32_01_j_57_governed(self):
        self._candidate(_bad('Board taɲly'), _read('Board taɲly'))

    def test_r16_32_01_j_58_governed(self):
        self._candidate(_bad('Board taɴly'), _read('Board taɴly'))

    def test_r16_32_01_j_59_governed(self):
        self._candidate(_bad('Board taɵly'), _read('Board taɵly'))

    def test_r16_32_01_j_60_governed(self):
        self._candidate(_bad('Board taɶly'), _read('Board taɶly'))

    def test_r16_32_01_j_61_governed(self):
        self._candidate(_bad('Board taɷly'), _read('Board taɷly'))

    def test_r16_32_01_j_62_governed(self):
        self._candidate(_bad('Board taƄly'), _read('Board taƄly'))

    def test_r16_32_01_j_63_governed(self):
        self._candidate(_bad('Board taƆly'), _read('Board taƆly'))

    def test_r16_32_01_j_64_governed(self):
        self._candidate(_bad('Board taƉly'), _read('Board taƉly'))

    def test_r16_32_01_j_65_governed(self):
        self._candidate(_bad('Board taƊly'), _read('Board taƊly'))

    def test_r16_32_01_j_66_governed(self):
        self._candidate(_bad('Board taƋly'), _read('Board taƋly'))

    def test_r16_32_01_j_67_governed(self):
        self._candidate(_bad('Board taƌly'), _read('Board taƌly'))

    def test_r16_32_01_j_68_governed(self):
        self._candidate(_bad('Board taƎly'), _read('Board taƎly'))

    def test_r16_32_01_j_69_governed(self):
        self._candidate(_bad('Board taƏly'), _read('Board taƏly'))

    def test_r16_32_01_j_70_governed(self):
        self._candidate(_bad('Board taƐly'), _read('Board taƐly'))

    def test_r16_32_01_j_71_governed(self):
        self._candidate(_bad('Board taƓly'), _read('Board taƓly'))

    def test_r16_32_01_j_72_governed(self):
        self._candidate(_bad('Board taƖly'), _read('Board taƖly'))

    def test_r16_32_01_j_73_governed(self):
        self._candidate(_bad('Board taƘly'), _read('Board taƘly'))

    def test_r16_32_01_j_74_governed(self):
        self._candidate(_bad('Board taƜly'), _read('Board taƜly'))

    def test_r16_32_01_j_75_governed(self):
        self._candidate(_bad('Board taƝly'), _read('Board taƝly'))

    def test_r16_32_01_j_76_governed(self):
        self._candidate(_bad('Board taƞly'), _read('Board taƞly'))

    def test_r16_32_01_j_77_governed(self):
        self._candidate(_bad('Board taƟly'), _read('Board taƟly'))

    def test_r16_32_01_j_78_governed(self):
        self._candidate(_bad('Board taƠly'), _read('Board taƠly'))

    def test_r16_32_01_j_79_governed(self):
        self._candidate(_bad('Board taơly'), _read('Board taơly'))

    def test_r16_32_01_j_80_governed(self):
        self._candidate(_bad('Board taƢly'), _read('Board taƢly'))

    def test_r16_32_01_j_81_governed(self):
        self._candidate(_bad('Board taƦly'), _read('Board taƦly'))

    def test_r16_32_01_j_82_governed(self):
        self._candidate(_bad('Board taƧly'), _read('Board taƧly'))

    def test_r16_32_01_j_83_governed(self):
        self._candidate(_bad('Board taƨly'), _read('Board taƨly'))

    def test_r16_32_01_j_84_governed(self):
        self._candidate(_bad('Board taƪly'), _read('Board taƪly'))

    def test_r16_32_01_j_85_governed(self):
        self._candidate(_bad('Board taƫly'), _read('Board taƫly'))

    def test_r16_32_01_j_86_governed(self):
        self._candidate(_bad('Board taƬly'), _read('Board taƬly'))

    def test_r16_32_01_j_87_governed(self):
        self._candidate(_bad('Board taƭly'), _read('Board taƭly'))

    def test_r16_32_01_j_88_governed(self):
        self._candidate(_bad('Board taƯly'), _read('Board taƯly'))

    def test_r16_32_01_j_89_governed(self):
        self._candidate(_bad('Board taưly'), _read('Board taưly'))

    def test_r16_32_01_j_90_governed(self):
        self._candidate(_bad('Board taƲly'), _read('Board taƲly'))

    def test_r16_32_01_j_91_governed(self):
        self._candidate(_bad('Board taƳly'), _read('Board taƳly'))

    def test_r16_32_01_j_92_governed(self):
        self._candidate(_bad('Board taƴly'), _read('Board taƴly'))

    def test_r16_32_01_j_93_governed(self):
        self._candidate(_bad('Board taƵly'), _read('Board taƵly'))

    def test_r16_32_01_j_94_governed(self):
        self._candidate(_bad('Board taƶly'), _read('Board taƶly'))

    def test_r16_32_01_j_95_governed(self):
        self._candidate(_bad('Board taƷly'), _read('Board taƷly'))

    def test_r16_32_01_j_96_governed(self):
        self._candidate(_bad('Board taƸly'), _read('Board taƸly'))

    def test_r16_32_01_j_97_governed(self):
        self._candidate(_bad('Board taƹly'), _read('Board taƹly'))

    def test_r16_32_01_j_98_governed(self):
        self._candidate(_bad('Board taƺly'), _read('Board taƺly'))

    def test_r16_32_01_j_99_governed(self):
        self._candidate(_bad('Board taƻly'), _read('Board taƻly'))

    def test_r16_32_01_j_100_governed(self):
        self._candidate(_bad('Board taƼly'), _read('Board taƼly'))

    def test_r16_32_01_j_101_governed(self):
        self._candidate(_bad('Board taƽly'), _read('Board taƽly'))

    def test_r16_32_01_j_102_governed(self):
        self._candidate(_bad('Board taƾly'), _read('Board taƾly'))

    def test_r16_32_01_j_103_governed(self):
        self._candidate(_bad('Board taƿly'), _read('Board taƿly'))

    def test_r16_32_01_j_104_governed(self):
        self._candidate(_bad('Board taǀly'), _read('Board taǀly'))

    def test_r16_32_01_j_105_governed(self):
        self._candidate(_bad('Board taǁly'), _read('Board taǁly'))

    def test_r16_32_01_j_106_governed(self):
        self._candidate(_bad('Board taǂly'), _read('Board taǂly'))

    def test_r16_32_01_j_107_governed(self):
        self._candidate(_bad('Board taǃly'), _read('Board taǃly'))

    def test_r16_32_01_j_108_governed(self):
        self._candidate(_bad('Trace sɩmmarise'), _read('Trace sɩmmarise'))

    def test_r16_32_01_j_109_governed(self):
        self._candidate(_bad('Trace sɫmmarise'), _read('Trace sɫmmarise'))

    def test_r16_32_01_j_110_governed(self):
        self._candidate(_bad('Trace sɬmmarise'), _read('Trace sɬmmarise'))

    def test_r16_32_01_j_111_governed(self):
        self._candidate(_bad('Trace sɮmmarise'), _read('Trace sɮmmarise'))

    def test_r16_32_01_j_112_governed(self):
        self._candidate(_bad('Trace sɱmmarise'), _read('Trace sɱmmarise'))

    def test_r16_32_01_j_113_governed(self):
        self._candidate(_bad('Trace sɲmmarise'), _read('Trace sɲmmarise'))

    def test_r16_32_01_j_114_governed(self):
        self._candidate(_bad('Trace sɳmmarise'), _read('Trace sɳmmarise'))

    def test_r16_32_01_j_115_governed(self):
        self._candidate(_bad('Trace sɴmmarise'), _read('Trace sɴmmarise'))

    def test_r16_32_01_j_116_governed(self):
        self._candidate(_bad('Trace sɵmmarise'), _read('Trace sɵmmarise'))

    def test_r16_32_01_j_117_governed(self):
        self._candidate(_bad('Trace sɶmmarise'), _read('Trace sɶmmarise'))

    def test_r16_32_01_j_118_governed(self):
        self._candidate(_bad('Trace sɷmmarise'), _read('Trace sɷmmarise'))

    def test_r16_32_01_j_119_governed(self):
        self._candidate(_bad('Trace sƄmmarise'), _read('Trace sƄmmarise'))

    def test_r16_32_01_j_120_governed(self):
        self._candidate(_bad('Trace sƆmmarise'), _read('Trace sƆmmarise'))

    def test_r16_32_01_j_121_governed(self):
        self._candidate(_bad('Trace sƉmmarise'), _read('Trace sƉmmarise'))

    def test_r16_32_01_j_122_governed(self):
        self._candidate(_bad('Trace sƊmmarise'), _read('Trace sƊmmarise'))

    def test_r16_32_01_j_123_governed(self):
        self._candidate(_bad('Trace sƋmmarise'), _read('Trace sƋmmarise'))

    def test_r16_32_01_j_124_governed(self):
        self._candidate(_bad('Trace sƌmmarise'), _read('Trace sƌmmarise'))

    def test_r16_32_01_j_125_governed(self):
        self._candidate(_bad('Trace sƎmmarise'), _read('Trace sƎmmarise'))

    def test_r16_32_01_j_126_governed(self):
        self._candidate(_bad('Trace sƏmmarise'), _read('Trace sƏmmarise'))

    def test_r16_32_01_j_127_governed(self):
        self._candidate(_bad('Trace sƐmmarise'), _read('Trace sƐmmarise'))

    def test_r16_32_01_j_128_governed(self):
        self._candidate(_bad('Trace sƓmmarise'), _read('Trace sƓmmarise'))

    def test_r16_32_01_j_129_governed(self):
        self._candidate(_bad('Trace sƖmmarise'), _read('Trace sƖmmarise'))

    def test_r16_32_01_j_130_governed(self):
        self._candidate(_bad('Trace sƘmmarise'), _read('Trace sƘmmarise'))

    def test_r16_32_01_j_131_governed(self):
        self._candidate(_bad('Trace sƝmmarise'), _read('Trace sƝmmarise'))

    def test_r16_32_01_j_132_governed(self):
        self._candidate(_bad('Trace sƞmmarise'), _read('Trace sƞmmarise'))

    def test_r16_32_01_j_133_governed(self):
        self._candidate(_bad('Trace sƟmmarise'), _read('Trace sƟmmarise'))

    def test_r16_32_01_j_134_governed(self):
        self._candidate(_bad('Trace sƠmmarise'), _read('Trace sƠmmarise'))

    def test_r16_32_01_j_135_governed(self):
        self._candidate(_bad('Trace sơmmarise'), _read('Trace sơmmarise'))

    def test_r16_32_01_j_136_governed(self):
        self._candidate(_bad('Trace sƢmmarise'), _read('Trace sƢmmarise'))

    def test_r16_32_01_j_137_governed(self):
        self._candidate(_bad('Trace sƤmmarise'), _read('Trace sƤmmarise'))

    def test_r16_32_01_j_138_governed(self):
        self._candidate(_bad('Trace sƦmmarise'), _read('Trace sƦmmarise'))

    def test_r16_32_01_j_139_governed(self):
        self._candidate(_bad('Trace sƧmmarise'), _read('Trace sƧmmarise'))

    def test_r16_32_01_j_140_governed(self):
        self._candidate(_bad('Trace sƨmmarise'), _read('Trace sƨmmarise'))

    def test_r16_32_01_j_141_governed(self):
        self._candidate(_bad('Trace sƪmmarise'), _read('Trace sƪmmarise'))

    def test_r16_32_01_j_142_governed(self):
        self._candidate(_bad('Trace sƫmmarise'), _read('Trace sƫmmarise'))

    def test_r16_32_01_j_143_governed(self):
        self._candidate(_bad('Trace sƬmmarise'), _read('Trace sƬmmarise'))

    def test_r16_32_01_j_144_governed(self):
        self._candidate(_bad('Trace sƭmmarise'), _read('Trace sƭmmarise'))

    def test_r16_32_01_j_145_governed(self):
        self._candidate(_bad('Trace sƳmmarise'), _read('Trace sƳmmarise'))

    def test_r16_32_01_j_146_governed(self):
        self._candidate(_bad('Trace sƴmmarise'), _read('Trace sƴmmarise'))

    def test_r16_32_01_j_147_governed(self):
        self._candidate(_bad('Trace sƵmmarise'), _read('Trace sƵmmarise'))

    def test_r16_32_01_j_148_governed(self):
        self._candidate(_bad('Trace sƶmmarise'), _read('Trace sƶmmarise'))

    def test_r16_32_01_j_149_governed(self):
        self._candidate(_bad('Trace sƷmmarise'), _read('Trace sƷmmarise'))

    def test_r16_32_01_j_150_governed(self):
        self._candidate(_bad('Trace sƸmmarise'), _read('Trace sƸmmarise'))

    def test_r16_32_01_j_151_governed(self):
        self._candidate(_bad('Trace sƹmmarise'), _read('Trace sƹmmarise'))

    def test_r16_32_01_j_152_governed(self):
        self._candidate(_bad('Trace sƺmmarise'), _read('Trace sƺmmarise'))

    def test_r16_32_01_j_153_governed(self):
        self._candidate(_bad('Trace sƻmmarise'), _read('Trace sƻmmarise'))

    def test_r16_32_01_j_154_governed(self):
        self._candidate(_bad('Trace sƼmmarise'), _read('Trace sƼmmarise'))

    def test_r16_32_01_j_155_governed(self):
        self._candidate(_bad('Trace sƽmmarise'), _read('Trace sƽmmarise'))

    def test_r16_32_01_j_156_governed(self):
        self._candidate(_bad('Trace sƾmmarise'), _read('Trace sƾmmarise'))

    def test_r16_32_01_j_157_governed(self):
        self._candidate(_bad('Trace sƿmmarise'), _read('Trace sƿmmarise'))

    def test_r16_32_01_j_158_governed(self):
        self._candidate(_bad('Trace sǀmmarise'), _read('Trace sǀmmarise'))

    def test_r16_32_01_j_159_governed(self):
        self._candidate(_bad('Trace sǁmmarise'), _read('Trace sǁmmarise'))

    def test_r16_32_01_j_160_governed(self):
        self._candidate(_bad('Trace sǂmmarise'), _read('Trace sǂmmarise'))

    def test_r16_32_01_j_161_governed(self):
        self._candidate(_bad('Trace sǃmmarise'), _read('Trace sǃmmarise'))

    def test_r16_32_01_j_162_governed(self):
        self._candidate(_bad('Trace sumɩarise'), _read('Trace sumɩarise'))

    def test_r16_32_01_j_163_governed(self):
        self._candidate(_bad('Trace sumɫarise'), _read('Trace sumɫarise'))

    def test_r16_32_01_j_164_governed(self):
        self._candidate(_bad('Trace sumɬarise'), _read('Trace sumɬarise'))

    def test_r16_32_01_j_165_governed(self):
        self._candidate(_bad('Trace sumɭarise'), _read('Trace sumɭarise'))

    def test_r16_32_01_j_166_governed(self):
        self._candidate(_bad('Trace sumɮarise'), _read('Trace sumɮarise'))

    def test_r16_32_01_j_167_governed(self):
        self._candidate(_bad('Trace sumɯarise'), _read('Trace sumɯarise'))

    def test_r16_32_01_j_168_governed(self):
        self._candidate(_bad('Trace sumɰarise'), _read('Trace sumɰarise'))

    def test_r16_32_01_j_169_governed(self):
        self._candidate(_bad('Trace sumɳarise'), _read('Trace sumɳarise'))

    def test_r16_32_01_j_170_governed(self):
        self._candidate(_bad('Trace sumɵarise'), _read('Trace sumɵarise'))

    def test_r16_32_01_j_171_governed(self):
        self._candidate(_bad('Trace sumɷarise'), _read('Trace sumɷarise'))

    def test_r16_32_01_j_172_governed(self):
        self._candidate(_bad('Trace sumƄarise'), _read('Trace sumƄarise'))

    def test_r16_32_01_j_173_governed(self):
        self._candidate(_bad('Trace sumƆarise'), _read('Trace sumƆarise'))

    def test_r16_32_01_j_174_governed(self):
        self._candidate(_bad('Trace sumƉarise'), _read('Trace sumƉarise'))

    def test_r16_32_01_j_175_governed(self):
        self._candidate(_bad('Trace sumƊarise'), _read('Trace sumƊarise'))

    def test_r16_32_01_j_176_governed(self):
        self._candidate(_bad('Trace sumƋarise'), _read('Trace sumƋarise'))

    def test_r16_32_01_j_177_governed(self):
        self._candidate(_bad('Trace sumƌarise'), _read('Trace sumƌarise'))

    def test_r16_32_01_j_178_governed(self):
        self._candidate(_bad('Trace sumƎarise'), _read('Trace sumƎarise'))

    def test_r16_32_01_j_179_governed(self):
        self._candidate(_bad('Trace sumƏarise'), _read('Trace sumƏarise'))

    def test_r16_32_01_j_180_governed(self):
        self._candidate(_bad('Trace sumƐarise'), _read('Trace sumƐarise'))

    def test_r16_32_01_j_181_governed(self):
        self._candidate(_bad('Trace sumƓarise'), _read('Trace sumƓarise'))

    def test_r16_32_01_j_182_governed(self):
        self._candidate(_bad('Trace sumƖarise'), _read('Trace sumƖarise'))

    def test_r16_32_01_j_183_governed(self):
        self._candidate(_bad('Trace sumƘarise'), _read('Trace sumƘarise'))

    def test_r16_32_01_j_184_governed(self):
        self._candidate(_bad('Trace sumƜarise'), _read('Trace sumƜarise'))

    def test_r16_32_01_j_185_governed(self):
        self._candidate(_bad('Trace sumƞarise'), _read('Trace sumƞarise'))

    def test_r16_32_01_j_186_governed(self):
        self._candidate(_bad('Trace sumƟarise'), _read('Trace sumƟarise'))

    def test_r16_32_01_j_187_governed(self):
        self._candidate(_bad('Trace sumƠarise'), _read('Trace sumƠarise'))

    def test_r16_32_01_j_188_governed(self):
        self._candidate(_bad('Trace sumơarise'), _read('Trace sumơarise'))

    def test_r16_32_01_j_189_governed(self):
        self._candidate(_bad('Trace sumƢarise'), _read('Trace sumƢarise'))

    def test_r16_32_01_j_190_governed(self):
        self._candidate(_bad('Trace sumƤarise'), _read('Trace sumƤarise'))

    def test_r16_32_01_j_191_governed(self):
        self._candidate(_bad('Trace sumƦarise'), _read('Trace sumƦarise'))

    def test_r16_32_01_j_192_governed(self):
        self._candidate(_bad('Trace sumƧarise'), _read('Trace sumƧarise'))

    def test_r16_32_01_j_193_governed(self):
        self._candidate(_bad('Trace sumƨarise'), _read('Trace sumƨarise'))

    def test_r16_32_01_j_194_governed(self):
        self._candidate(_bad('Trace sumƪarise'), _read('Trace sumƪarise'))

    def test_r16_32_01_j_195_governed(self):
        self._candidate(_bad('Trace sumƫarise'), _read('Trace sumƫarise'))

    def test_r16_32_01_j_196_governed(self):
        self._candidate(_bad('Trace sumƬarise'), _read('Trace sumƬarise'))

    def test_r16_32_01_j_197_governed(self):
        self._candidate(_bad('Trace sumƭarise'), _read('Trace sumƭarise'))

    def test_r16_32_01_j_198_governed(self):
        self._candidate(_bad('Trace sumƯarise'), _read('Trace sumƯarise'))

    def test_r16_32_01_j_199_governed(self):
        self._candidate(_bad('Trace sumưarise'), _read('Trace sumưarise'))

    def test_r16_32_01_j_200_governed(self):
        self._candidate(_bad('Trace sumƲarise'), _read('Trace sumƲarise'))

    def test_r16_32_01_j_201_governed(self):
        self._candidate(_bad('Trace sumƳarise'), _read('Trace sumƳarise'))

    def test_r16_32_01_j_202_governed(self):
        self._candidate(_bad('Trace sumƴarise'), _read('Trace sumƴarise'))

    def test_r16_32_01_j_203_governed(self):
        self._candidate(_bad('Trace sumƵarise'), _read('Trace sumƵarise'))

    def test_r16_32_01_j_204_governed(self):
        self._candidate(_bad('Trace sumƶarise'), _read('Trace sumƶarise'))

    def test_r16_32_01_j_205_governed(self):
        self._candidate(_bad('Trace sumƷarise'), _read('Trace sumƷarise'))

    def test_r16_32_01_j_206_governed(self):
        self._candidate(_bad('Trace sumƸarise'), _read('Trace sumƸarise'))

    def test_r16_32_01_j_207_governed(self):
        self._candidate(_bad('Trace sumƹarise'), _read('Trace sumƹarise'))

    def test_r16_32_01_j_208_governed(self):
        self._candidate(_bad('Trace sumƺarise'), _read('Trace sumƺarise'))

    def test_r16_32_01_j_209_governed(self):
        self._candidate(_bad('Trace sumƻarise'), _read('Trace sumƻarise'))

    def test_r16_32_01_j_210_governed(self):
        self._candidate(_bad('Trace sumƼarise'), _read('Trace sumƼarise'))

    def test_r16_32_01_j_211_governed(self):
        self._candidate(_bad('Trace sumƽarise'), _read('Trace sumƽarise'))

    def test_r16_32_01_j_212_governed(self):
        self._candidate(_bad('Trace sumƾarise'), _read('Trace sumƾarise'))

    def test_r16_32_01_j_213_governed(self):
        self._candidate(_bad('Trace sumƿarise'), _read('Trace sumƿarise'))

    def test_r16_32_01_j_214_governed(self):
        self._candidate(_bad('Trace sumǀarise'), _read('Trace sumǀarise'))

    def test_r16_32_01_j_215_governed(self):
        self._candidate(_bad('Trace sumǁarise'), _read('Trace sumǁarise'))

    def test_r16_32_01_j_216_governed(self):
        self._candidate(_bad('Trace sumǂarise'), _read('Trace sumǂarise'))

    def test_r16_32_01_j_217_governed(self):
        self._candidate(_bad('Trace sumǃarise'), _read('Trace sumǃarise'))

    def test_r16_32_01_j_218_governed(self):
        self._candidate(_bad('Trace summariɩe'), _read('Trace summariɩe'))

    def test_r16_32_01_j_219_governed(self):
        self._candidate(_bad('Trace summariɫe'), _read('Trace summariɫe'))

    def test_r16_32_01_j_220_governed(self):
        self._candidate(_bad('Trace summariɬe'), _read('Trace summariɬe'))

    def test_r16_32_01_j_221_governed(self):
        self._candidate(_bad('Trace summariɭe'), _read('Trace summariɭe'))

    def test_r16_32_01_j_222_governed(self):
        self._candidate(_bad('Trace summariɮe'), _read('Trace summariɮe'))

    def test_r16_32_01_j_223_governed(self):
        self._candidate(_bad('Trace summariɯe'), _read('Trace summariɯe'))

    def test_r16_32_01_j_224_governed(self):
        self._candidate(_bad('Trace summariɰe'), _read('Trace summariɰe'))

    def test_r16_32_01_j_225_governed(self):
        self._candidate(_bad('Trace summariɱe'), _read('Trace summariɱe'))

    def test_r16_32_01_j_226_governed(self):
        self._candidate(_bad('Trace summariɲe'), _read('Trace summariɲe'))

    def test_r16_32_01_j_227_governed(self):
        self._candidate(_bad('Trace summariɳe'), _read('Trace summariɳe'))

    def test_r16_32_01_j_228_governed(self):
        self._candidate(_bad('Trace summariɴe'), _read('Trace summariɴe'))

    def test_r16_32_01_j_229_governed(self):
        self._candidate(_bad('Trace summariɵe'), _read('Trace summariɵe'))

    def test_r16_32_01_j_230_governed(self):
        self._candidate(_bad('Trace summariɶe'), _read('Trace summariɶe'))

    def test_r16_32_01_j_231_governed(self):
        self._candidate(_bad('Trace summariɷe'), _read('Trace summariɷe'))

    def test_r16_32_01_j_232_governed(self):
        self._candidate(_bad('Trace summariƄe'), _read('Trace summariƄe'))

    def test_r16_32_01_j_233_governed(self):
        self._candidate(_bad('Trace summariƆe'), _read('Trace summariƆe'))

    def test_r16_32_01_j_234_governed(self):
        self._candidate(_bad('Trace summariƉe'), _read('Trace summariƉe'))

    def test_r16_32_01_j_235_governed(self):
        self._candidate(_bad('Trace summariƊe'), _read('Trace summariƊe'))

    def test_r16_32_01_j_236_governed(self):
        self._candidate(_bad('Trace summariƋe'), _read('Trace summariƋe'))

    def test_r16_32_01_j_237_governed(self):
        self._candidate(_bad('Trace summariƌe'), _read('Trace summariƌe'))

    def test_r16_32_01_j_238_governed(self):
        self._candidate(_bad('Trace summariƎe'), _read('Trace summariƎe'))

    def test_r16_32_01_j_239_governed(self):
        self._candidate(_bad('Trace summariƏe'), _read('Trace summariƏe'))

    def test_r16_32_01_j_240_governed(self):
        self._candidate(_bad('Trace summariƐe'), _read('Trace summariƐe'))

    def test_r16_32_01_j_241_governed(self):
        self._candidate(_bad('Trace summariƓe'), _read('Trace summariƓe'))

    def test_r16_32_01_j_242_governed(self):
        self._candidate(_bad('Trace summariƖe'), _read('Trace summariƖe'))

    def test_r16_32_01_j_243_governed(self):
        self._candidate(_bad('Trace summariƘe'), _read('Trace summariƘe'))

    def test_r16_32_01_j_244_governed(self):
        self._candidate(_bad('Trace summariƜe'), _read('Trace summariƜe'))

    def test_r16_32_01_j_245_governed(self):
        self._candidate(_bad('Trace summariƝe'), _read('Trace summariƝe'))

    def test_r16_32_01_j_246_governed(self):
        self._candidate(_bad('Trace summariƞe'), _read('Trace summariƞe'))

    def test_r16_32_01_j_247_governed(self):
        self._candidate(_bad('Trace summariƟe'), _read('Trace summariƟe'))

    def test_r16_32_01_j_248_governed(self):
        self._candidate(_bad('Trace summariƠe'), _read('Trace summariƠe'))

    def test_r16_32_01_j_249_governed(self):
        self._candidate(_bad('Trace summariơe'), _read('Trace summariơe'))

    def test_r16_32_01_j_250_governed(self):
        self._candidate(_bad('Trace summariƢe'), _read('Trace summariƢe'))

    def test_r16_32_01_j_251_governed(self):
        self._candidate(_bad('Trace summariƤe'), _read('Trace summariƤe'))

    def test_r16_32_01_j_252_governed(self):
        self._candidate(_bad('Trace summariƪe'), _read('Trace summariƪe'))

    def test_r16_32_01_j_253_governed(self):
        self._candidate(_bad('Trace summariƫe'), _read('Trace summariƫe'))

    def test_r16_32_01_j_254_governed(self):
        self._candidate(_bad('Trace summariƬe'), _read('Trace summariƬe'))

    def test_r16_32_01_j_255_governed(self):
        self._candidate(_bad('Trace summariƭe'), _read('Trace summariƭe'))

    def test_r16_32_01_j_256_governed(self):
        self._candidate(_bad('Trace summariƯe'), _read('Trace summariƯe'))

    def test_r16_32_01_j_257_governed(self):
        self._candidate(_bad('Trace summariưe'), _read('Trace summariưe'))

    def test_r16_32_01_j_258_governed(self):
        self._candidate(_bad('Trace summariƲe'), _read('Trace summariƲe'))

    def test_r16_32_01_j_259_governed(self):
        self._candidate(_bad('Trace summariƳe'), _read('Trace summariƳe'))

    def test_r16_32_01_j_260_governed(self):
        self._candidate(_bad('Trace summariƴe'), _read('Trace summariƴe'))

    def test_r16_32_01_j_261_governed(self):
        self._candidate(_bad('Trace summariƵe'), _read('Trace summariƵe'))

    def test_r16_32_01_j_262_governed(self):
        self._candidate(_bad('Trace summariƶe'), _read('Trace summariƶe'))

    def test_r16_32_01_j_263_governed(self):
        self._candidate(_bad('Trace summariƸe'), _read('Trace summariƸe'))

    def test_r16_32_01_j_264_governed(self):
        self._candidate(_bad('Trace summariƹe'), _read('Trace summariƹe'))

    def test_r16_32_01_j_265_governed(self):
        self._candidate(_bad('Trace summariƺe'), _read('Trace summariƺe'))

    def test_r16_32_01_j_266_governed(self):
        self._candidate(_bad('Trace summariƻe'), _read('Trace summariƻe'))

    def test_r16_32_01_j_267_governed(self):
        self._candidate(_bad('Trace summariƼe'), _read('Trace summariƼe'))

    def test_r16_32_01_j_268_governed(self):
        self._candidate(_bad('Trace summariƽe'), _read('Trace summariƽe'))

    def test_r16_32_01_j_269_governed(self):
        self._candidate(_bad('Trace summariƾe'), _read('Trace summariƾe'))

    def test_r16_32_01_j_270_governed(self):
        self._candidate(_bad('Trace summariƿe'), _read('Trace summariƿe'))

    def test_r16_32_01_j_271_governed(self):
        self._candidate(_bad('Trace summariǀe'), _read('Trace summariǀe'))

    def test_r16_32_01_j_272_governed(self):
        self._candidate(_bad('Trace summariǁe'), _read('Trace summariǁe'))

    def test_r16_32_01_j_273_governed(self):
        self._candidate(_bad('Trace summariǂe'), _read('Trace summariǂe'))

    def test_r16_32_01_j_274_governed(self):
        self._candidate(_bad('Trace summariǃe'), _read('Trace summariǃe'))

    def test_r16_32_01_j_275_governed(self):
        self._candidate(_bad('Trace summarisɩ'), _read('Trace summarisɩ'))

    def test_r16_32_01_j_276_governed(self):
        self._candidate(_bad('Trace summarisɫ'), _read('Trace summarisɫ'))

    def test_r16_32_01_j_277_governed(self):
        self._candidate(_bad('Trace summarisɬ'), _read('Trace summarisɬ'))

    def test_r16_32_01_j_278_governed(self):
        self._candidate(_bad('Trace summarisɭ'), _read('Trace summarisɭ'))

    def test_r16_32_01_j_279_governed(self):
        self._candidate(_bad('Trace summarisɮ'), _read('Trace summarisɮ'))

    def test_r16_32_01_j_280_governed(self):
        self._candidate(_bad('Trace summarisɯ'), _read('Trace summarisɯ'))

    def test_r16_32_01_j_281_governed(self):
        self._candidate(_bad('Trace summarisɰ'), _read('Trace summarisɰ'))

    def test_r16_32_01_j_282_governed(self):
        self._candidate(_bad('Trace summarisɱ'), _read('Trace summarisɱ'))

    def test_r16_32_01_j_283_governed(self):
        self._candidate(_bad('Trace summarisɲ'), _read('Trace summarisɲ'))

    def test_r16_32_01_j_284_governed(self):
        self._candidate(_bad('Trace summarisɳ'), _read('Trace summarisɳ'))

    def test_r16_32_01_j_285_governed(self):
        self._candidate(_bad('Trace summarisɴ'), _read('Trace summarisɴ'))

    def test_r16_32_01_j_286_governed(self):
        self._candidate(_bad('Trace summarisɶ'), _read('Trace summarisɶ'))

    def test_r16_32_01_j_287_governed(self):
        self._candidate(_bad('Trace summarisɷ'), _read('Trace summarisɷ'))

    def test_r16_32_01_j_288_governed(self):
        self._candidate(_bad('Trace summarisƄ'), _read('Trace summarisƄ'))

    def test_r16_32_01_j_289_governed(self):
        self._candidate(_bad('Trace summarisƆ'), _read('Trace summarisƆ'))

    def test_r16_32_01_j_290_governed(self):
        self._candidate(_bad('Trace summarisƉ'), _read('Trace summarisƉ'))

    def test_r16_32_01_j_291_governed(self):
        self._candidate(_bad('Trace summarisƋ'), _read('Trace summarisƋ'))

    def test_r16_32_01_j_292_governed(self):
        self._candidate(_bad('Trace summarisƌ'), _read('Trace summarisƌ'))

    def test_r16_32_01_j_293_governed(self):
        self._candidate(_bad('Trace summarisƎ'), _read('Trace summarisƎ'))

    def test_r16_32_01_j_294_governed(self):
        self._candidate(_bad('Trace summarisƏ'), _read('Trace summarisƏ'))

    def test_r16_32_01_j_295_governed(self):
        self._candidate(_bad('Trace summarisƓ'), _read('Trace summarisƓ'))

    def test_r16_32_01_j_296_governed(self):
        self._candidate(_bad('Trace summarisƖ'), _read('Trace summarisƖ'))

    def test_r16_32_01_j_297_governed(self):
        self._candidate(_bad('Trace summarisƘ'), _read('Trace summarisƘ'))

    def test_r16_32_01_j_298_governed(self):
        self._candidate(_bad('Trace summarisƜ'), _read('Trace summarisƜ'))

    def test_r16_32_01_j_299_governed(self):
        self._candidate(_bad('Trace summarisƝ'), _read('Trace summarisƝ'))

    def test_r16_32_01_j_300_governed(self):
        self._candidate(_bad('Trace summarisƞ'), _read('Trace summarisƞ'))

    def test_r16_32_01_j_301_governed(self):
        self._candidate(_bad('Trace summarisƠ'), _read('Trace summarisƠ'))

    def test_r16_32_01_j_302_governed(self):
        self._candidate(_bad('Trace summarisơ'), _read('Trace summarisơ'))

    def test_r16_32_01_j_303_governed(self):
        self._candidate(_bad('Trace summarisƢ'), _read('Trace summarisƢ'))

    def test_r16_32_01_j_304_governed(self):
        self._candidate(_bad('Trace summarisƤ'), _read('Trace summarisƤ'))

    def test_r16_32_01_j_305_governed(self):
        self._candidate(_bad('Trace summarisƦ'), _read('Trace summarisƦ'))

    def test_r16_32_01_j_306_governed(self):
        self._candidate(_bad('Trace summarisƧ'), _read('Trace summarisƧ'))

    def test_r16_32_01_j_307_governed(self):
        self._candidate(_bad('Trace summarisƨ'), _read('Trace summarisƨ'))

    def test_r16_32_01_j_308_governed(self):
        self._candidate(_bad('Trace summarisƪ'), _read('Trace summarisƪ'))

    def test_r16_32_01_j_309_governed(self):
        self._candidate(_bad('Trace summarisƫ'), _read('Trace summarisƫ'))

    def test_r16_32_01_j_310_governed(self):
        self._candidate(_bad('Trace summarisƬ'), _read('Trace summarisƬ'))

    def test_r16_32_01_j_311_governed(self):
        self._candidate(_bad('Trace summarisƭ'), _read('Trace summarisƭ'))

    def test_r16_32_01_j_312_governed(self):
        self._candidate(_bad('Trace summarisƯ'), _read('Trace summarisƯ'))

    def test_r16_32_01_j_313_governed(self):
        self._candidate(_bad('Trace summarisư'), _read('Trace summarisư'))

    def test_r16_32_01_j_314_governed(self):
        self._candidate(_bad('Trace summarisƲ'), _read('Trace summarisƲ'))

    def test_r16_32_01_j_315_governed(self):
        self._candidate(_bad('Trace summarisƳ'), _read('Trace summarisƳ'))

    def test_r16_32_01_j_316_governed(self):
        self._candidate(_bad('Trace summarisƴ'), _read('Trace summarisƴ'))

    def test_r16_32_01_j_317_governed(self):
        self._candidate(_bad('Trace summarisƵ'), _read('Trace summarisƵ'))

    def test_r16_32_01_j_318_governed(self):
        self._candidate(_bad('Trace summarisƶ'), _read('Trace summarisƶ'))

    def test_r16_32_01_j_319_governed(self):
        self._candidate(_bad('Trace summarisƷ'), _read('Trace summarisƷ'))

    def test_r16_32_01_j_320_governed(self):
        self._candidate(_bad('Trace summarisƸ'), _read('Trace summarisƸ'))

    def test_r16_32_01_j_321_governed(self):
        self._candidate(_bad('Trace summarisƹ'), _read('Trace summarisƹ'))

    def test_r16_32_01_j_322_governed(self):
        self._candidate(_bad('Trace summarisƺ'), _read('Trace summarisƺ'))

    def test_r16_32_01_j_323_governed(self):
        self._candidate(_bad('Trace summarisƻ'), _read('Trace summarisƻ'))

    def test_r16_32_01_j_324_governed(self):
        self._candidate(_bad('Trace summarisƼ'), _read('Trace summarisƼ'))

    def test_r16_32_01_j_325_governed(self):
        self._candidate(_bad('Trace summarisƽ'), _read('Trace summarisƽ'))

    def test_r16_32_01_j_326_governed(self):
        self._candidate(_bad('Trace summarisƾ'), _read('Trace summarisƾ'))

    def test_r16_32_01_j_327_governed(self):
        self._candidate(_bad('Trace summarisƿ'), _read('Trace summarisƿ'))

    def test_r16_32_01_j_328_governed(self):
        self._candidate(_bad('Trace summarisǀ'), _read('Trace summarisǀ'))

    def test_r16_32_01_j_329_governed(self):
        self._candidate(_bad('Trace summarisǁ'), _read('Trace summarisǁ'))

    def test_r16_32_01_j_330_governed(self):
        self._candidate(_bad('Trace summarisǂ'), _read('Trace summarisǂ'))

    def test_r16_32_01_j_331_governed(self):
        self._candidate(_bad('Trace summarisǃ'), _read('Trace summarisǃ'))

    def test_r16_32_01_j_332_governed(self):
        self._candidate(_bad('Trace suƆmarise'), _read('Trace suƆmarise'))

    def test_r16_32_01_j_333_governed(self):
        self._candidate(_bad('Board taƌy'), _read('Board taƌy'))

    def test_r16_32_01_j_334_governed(self):
        self._candidate(_bad('Board ƒally'), _read('Board ƒally'))

    def test_r16_32_01_j_335_governed(self):
        self._candidate(_bad('Trace suƒmarise'), _read('Trace suƒmarise'))

    def test_r16_32_01_j_336_governed(self):
        self._candidate(_bad('Board ƙally'), _read('Board ƙally'))

    def test_r16_32_01_j_337_governed(self):
        self._candidate(_bad('Trace summaƙise'), _read('Trace summaƙise'))

    # ------------------------------------------------------
    # Defect form of R16-32-03, the single form item:
    # Songbookstallies, standing beside R16-32-01.
    # ------------------------------------------------------

    def test_r16_32_03_songbookstallies_governed(self):
        self._candidate(_bad('Songbookstallies'), _read('Songbookstallies'))

    # ------------------------------------------------------
    # Adopted assertions of the round 32 breaker exhibit:
    # the beside, gate ruling and code level assertions
    # of B32-B01, in the forms the exhibit names them.
    # ------------------------------------------------------

    def test_b32_heraldtally_beside(self):
        q4 = self._beside(_bad("Heraldtally"))
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_b32_summarised_beside(self):
        q4 = self._beside(_bad('Trace summarisedeseseseseseseseseseseseseses'))
        assert_verdict(self, q4, "present", "Q-4")
        self.assertIn("totals 4 LANDED", q4)
        self.assertIn("Step 2", q4)
        self.assertIn("uncounted", q4)

    def test_b32_heraldtally_gate_ruling(self):
        report = self._q4_alone(_bad("Heraldtally"), ruling=True)
        self._assert_q4_governed(report, path=RULING_2)

    def test_b32_code_level_underreach_forms(self):
        for word in ("heraldtally", "heraldstallies", "boardheraldtally",
                     "tallye8", "boardtallyez7"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ('summarisedeseseseseseseseseseseseseses', 'summaryeseseseseseseseseseseseseseses'):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ('boardtracesummarisedeseseseseseseseseseseseseses', 'traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary'):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        for head in ("Heraldtally",
                     'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board gate summary',
                     'Trace summarisedeseseseseseseseseseseseseses'):
            line = head + ": items checked stand here"
            self.assertTrue(_tally_statement_head(line), head)
        self.assertEqual(_fold_word("\u0186ally"), "tally")
        self.assertEqual(_fold_word("su\u0186marise"), "summarise")
        self.assertEqual(_fold_word("\u018cally"), "tally")
        self.assertEqual(_fold_word("ta\u018cy"), "tally")
        self.assertEqual(_fold_word("\u0192ally"), "tally")
        self.assertEqual(_fold_word("su\u0192marise"), "summarise")
        self.assertEqual(_fold_word("\u0199ally"), "tally")
        self.assertEqual(_fold_word("summa\u0199ise"), "summarise")

    # ------------------------------------------------------
    # Held controls of R16-32-02, standing missing in the
    # cure of this unit: every distinct converse form of
    # the register, one test per form.
    # ------------------------------------------------------

    def test_control_converse_000_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp trace summary')))

    def test_control_converse_001_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk gasp summary trace')))

    def test_control_converse_002_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team moan trace summary')))

    def test_control_converse_003_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel groan summary trace')))

    def test_control_converse_004_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk whistle trace summary')))

    def test_control_converse_005_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team drank summary trace')))

    def test_control_converse_006_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel meant trace summary')))

    def test_control_converse_007_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel doze trace summary')))

    def test_control_converse_008_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk yodel summary trace')))

    def test_control_converse_009_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team grovel trace summary')))

    def test_control_converse_010_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel meant summary trace')))

    def test_control_converse_011_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk snivel trace summary')))

    def test_control_converse_012_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team cower summary trace')))

    def test_control_converse_013_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp tracesummary')))

    def test_control_converse_014_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp boardtracesummary')))

    def test_control_converse_015_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp traceboardgatesummary')))

    def test_control_converse_016_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_converse_017_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk gasp summarytrace')))

    def test_control_converse_018_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel drank tracesummary')))

    def test_control_converse_019_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel doze tracesummary')))

    def test_control_converse_020_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk yodel summarytrace')))

    def test_control_converse_021_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team grovel boardtracesummary')))

    def test_control_converse_022_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel meant traceboardgatesummary')))

    def test_control_converse_023_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk doze traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_converse_024_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team yodel tracesummarisationeseseseseseseseseseseseses')))

    def test_control_converse_025_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∮ trace summary')))

    def test_control_converse_026_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∯ trace summary')))

    def test_control_converse_027_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∰ trace summary')))

    def test_control_converse_028_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∱ trace summary')))

    def test_control_converse_029_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∲ trace summary')))

    def test_control_converse_030_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∳ trace summary')))

    def test_control_converse_031_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨀ trace summary')))

    def test_control_converse_032_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨁ trace summary')))

    def test_control_converse_033_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨂ trace summary')))

    def test_control_converse_034_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨄ trace summary')))

    def test_control_converse_035_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨅ trace summary')))

    def test_control_converse_036_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨆ trace summary')))

    def test_control_converse_037_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨇ trace summary')))

    def test_control_converse_038_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨈ trace summary')))

    def test_control_converse_039_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨉ trace summary')))

    def test_control_converse_040_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨊ trace summary')))

    def test_control_converse_041_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋐ trace summary')))

    def test_control_converse_042_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋑ trace summary')))

    def test_control_converse_043_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋒ trace summary')))

    def test_control_converse_044_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋓ trace summary')))

    def test_control_converse_045_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋔ trace summary')))

    def test_control_converse_046_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋕ trace summary')))

    def test_control_converse_047_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋬ trace summary')))

    def test_control_converse_048_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋩ trace summary')))

    def test_control_converse_049_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋪ trace summary')))

    def test_control_converse_050_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋫ trace summary')))

    def test_control_converse_051_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋮ trace summary')))

    def test_control_converse_052_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋯ trace summary')))

    def test_control_converse_053_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℈ trace summary')))

    def test_control_converse_054_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℇ trace summary')))

    def test_control_converse_055_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℊ trace summary')))

    def test_control_converse_056_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℋ trace summary')))

    def test_control_converse_057_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℌ trace summary')))

    def test_control_converse_058_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℍ trace summary')))

    def test_control_converse_059_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℏ trace summary')))

    def test_control_converse_060_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℐ trace summary')))

    def test_control_converse_061_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℘ trace summary')))

    def test_control_converse_062_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℨ trace summary')))

    def test_control_converse_063_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger K trace summary')))

    def test_control_converse_064_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℬ trace summary')))

    def test_control_converse_065_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℹ trace summary')))

    def test_control_converse_066_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger − trace summary')))

    def test_control_converse_067_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∓ trace summary')))

    def test_control_converse_068_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∜ trace summary')))

    def test_control_converse_069_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∝ trace summary')))

    def test_control_converse_070_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∟ trace summary')))

    def test_control_converse_071_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∠ trace summary')))

    def test_control_converse_072_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∡ trace summary')))

    def test_control_converse_073_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∢ trace summary')))

    def test_control_converse_074_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∣ trace summary')))

    def test_control_converse_075_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∤ trace summary')))

    def test_control_converse_076_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∥ trace summary')))

    def test_control_converse_077_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∦ trace summary')))

    def test_control_converse_078_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∧ trace summary')))

    def test_control_converse_079_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∨ trace summary')))

    def test_control_converse_080_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∬ trace summary')))

    def test_control_converse_081_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∭ trace summary')))

    def test_control_converse_082_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃒ trace summary')))

    def test_control_converse_083_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃘ trace summary')))

    def test_control_converse_084_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃚ trace summary')))

    def test_control_converse_085_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃠ trace summary')))

    def test_control_converse_086_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃣ trace summary')))

    def test_control_converse_087_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃧ trace summary')))

    def test_control_converse_088_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⟨panel⟩ trace summary')))

    def test_control_converse_089_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Gulp panel trace summary')))

    def test_control_converse_090_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Drank panel summary trace')))

    def test_control_converse_091_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Doze ledger trace summary')))

    # ------------------------------------------------------
    # Held controls of R16-32-02 named in the register,
    # standing missing in their recorded forms.
    # ------------------------------------------------------

    def test_control_held32_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chews trace summary')))

    def test_control_held32_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chewed trace summary')))

    def test_control_held32_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chewing trace summary')))

    def test_control_held32_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yawn trace summary')))

    def test_control_held32_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel took trace summary')))

    def test_control_held32_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap trace summary')))

    def test_control_held32_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap tracesummary')))

    def test_control_held32_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap summarytrace')))

    def test_control_held32_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap boardtracesummary')))

    def test_control_held32_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatesummary')))

    def test_control_held32_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held32_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held32_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap tracesummarisationeseseseseseseseseseseseses')))

    def test_control_held32_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew trace summary')))

    def test_control_held32_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew tracesummary')))

    def test_control_held32_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew summarytrace')))

    def test_control_held32_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew boardtracesummary')))

    def test_control_held32_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatesummary')))

    def test_control_held32_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held32_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew tracesummarisationeseseseseseseseseseseseses')))

    def test_control_held32_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist trace summary')))

    def test_control_held32_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist tracesummary')))

    def test_control_held32_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist summarytrace')))

    def test_control_held32_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist boardtracesummary')))

    def test_control_held32_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatesummary')))

    def test_control_held32_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held32_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held32_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist tracesummarisationeseseseseseseseseseseseses')))

    def test_control_held32_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team wept trace summary')))

    def test_control_held32_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk swept trace summary')))

    def test_control_held32_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team leapt summary trace')))

    def test_control_held32_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel knelt summary trace')))

    def test_control_held32_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel crept trace summary')))

    def test_control_held32_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held32_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_held32_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≅ trace summary')))

    def test_control_held32_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≈ trace summary')))

    def test_control_held32_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∏ trace summary')))

    def test_control_held32_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∐ trace summary')))

    def test_control_held32_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∑ trace summary')))

    def test_control_held32_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∞ trace summary')))

    def test_control_held32_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∫ trace summary')))

    def test_control_held32_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸢panel⸣ trace summary')))

    def test_control_held32_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger 〈panel〉 trace summary')))

    def test_control_held32_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sat trace summary')))

    def test_control_held32_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃐ trace summary')))

    def test_control_held32_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃢ trace summary')))

    def test_control_held32_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \\ trace summary')))

    def test_control_held32_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger || trace summary')))

    def test_control_held32_49_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger * trace summary')))

    def test_control_held32_50_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace board gate summary')))

    def test_control_held32_51_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace board gate summary')))

    def test_control_held32_52_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yank trace board gate summary')))

    def test_control_held32_53_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bore trace board gate summary')))

    def test_control_held32_54_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk rode summary board gate trace')))

    def test_control_held32_55_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fled trace board gate summary')))

    def test_control_held32_56_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sought trace board gate summary')))

    def test_control_held32_57_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel paid trace board gate summary')))

    def test_control_held32_58_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chose trace board gate summary')))

    def test_control_held32_59_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel reviewed trace board gate summary')))

    def test_control_held32_60_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel logs trace board gate summary')))

    def test_control_held32_61_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel bore traceboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held32_62_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel chose traceboardgatereviewannexpanelsummary')))

    def test_control_held32_63_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel reviewed the traceboardgatereviewannexsummary')))

    # ------------------------------------------------------
    # Governed closings of R16-32-02, standing governed
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
    # Held governed controls of R16-32-01 and of
    # R16-32-03 named in the register, standing governed
    # in the cure.
    # ------------------------------------------------------

    def test_control_underheld_00_governed(self):
        self._candidate(_bad('Broadsheettally'), _read('Broadsheettally'))

    def test_control_underheld_01_governed(self):
        self._candidate(_bad('Broadsheetstallies'), _read('Broadsheetstallies'))

    def test_control_underheld_02_governed(self):
        self._candidate(_bad('Newssheettally'), _read('Newssheettally'))

    def test_control_underheld_03_governed(self):
        self._candidate(_bad('Newssheetstallies'), _read('Newssheetstallies'))

    def test_control_underheld_04_governed(self):
        self._candidate(_bad('Chapbooktally'), _read('Chapbooktally'))

    def test_control_underheld_05_governed(self):
        self._candidate(_bad('Daybooktally'), _read('Daybooktally'))

    def test_control_underheld_06_governed(self):
        self._candidate(_bad('Workbooktally'), _read('Workbooktally'))

    def test_control_underheld_07_governed(self):
        self._candidate(_bad('Textbooktally'), _read('Textbooktally'))

    def test_control_underheld_08_governed(self):
        self._candidate(_bad('Yearbooktally'), _read('Yearbooktally'))

    def test_control_underheld_09_governed(self):
        self._candidate(_bad('Cookbooktally'), _read('Cookbooktally'))

    def test_control_underheld_10_governed(self):
        self._candidate(_bad('Handbooktally'), _read('Handbooktally'))

    def test_control_underheld_11_governed(self):
        self._candidate(_bad('Logbooktally'), _read('Logbooktally'))

    def test_control_underheld_12_governed(self):
        self._candidate(_bad('Guestbooktally'), _read('Guestbooktally'))

    def test_control_underheld_13_governed(self):
        self._candidate(_bad('Scrapbooktally'), _read('Scrapbooktally'))

    def test_control_underheld_14_governed(self):
        self._candidate(_bad('Songbooktally'), _read('Songbooktally'))

    def test_control_underheld_15_governed(self):
        self._candidate(_bad('Billboardtally'), _read('Billboardtally'))

    def test_control_underheld_16_governed(self):
        self._candidate(_bad('Billboardstallies'), _read('Billboardstallies'))

    def test_control_underheld_17_governed(self):
        self._candidate(_bad('Boardbroadsheettally'), _read('Boardbroadsheettally'))

    def test_control_underheld_18_governed(self):
        self._candidate(_bad('Boardtextbooktally'), _read('Boardtextbooktally'))

    def test_control_underheld_19_governed(self):
        self._candidate(_bad('Gateworkbooktally'), _read('Gateworkbooktally'))

    def test_control_underheld_20_governed(self):
        self._candidate(_bad('Reviewlogbooktally'), _read('Reviewlogbooktally'))

    def test_control_underheld_21_governed(self):
        self._candidate(_bad('Boardbroadsheettallye'), _read('Boardbroadsheettallye'))

    def test_control_underheld_22_governed(self):
        self._candidate(_bad('Boardtextbooktalliez'), _read('Boardtextbooktalliez'))

    def test_control_underheld_23_governed(self):
        self._candidate(_bad('Boardchapbooktallye'), _read('Boardchapbooktallye'))

    def test_control_underheld_24_governed(self):
        self._candidate(_bad('Gateworkbooktallye'), _read('Gateworkbooktallye'))

    def test_control_underheld_25_governed(self):
        self._candidate(_bad('Boardhandbooktallye'), _read('Boardhandbooktallye'))

    def test_control_underheld_26_governed(self):
        self._candidate(_bad('Boarddictionarytallye'), _read('Boarddictionarytallye'))

    def test_control_underheld_27_governed(self):
        self._candidate(_bad('Gatevocabularytalliez'), _read('Gatevocabularytalliez'))

    def test_control_underheld_28_governed(self):
        self._candidate(_bad('Trace summarisationeseseseseseseseseseseseseses'), _read('Trace summarisationeseseseseseseseseseseseseses'))

    def test_control_underheld_29_governed(self):
        self._candidate(_bad('Board ɭally'), _read('Board ɭally'))

    def test_control_underheld_30_governed(self):
        self._candidate(_bad('Board Ƅally'), _read('Board Ƅally'))

    def test_control_underheld_31_governed(self):
        self._candidate(_bad('Board Ɖally'), _read('Board Ɖally'))

    def test_control_underheld_32_governed(self):
        self._candidate(_bad('Board Ɗally'), _read('Board Ɗally'))

    def test_control_underheld_33_governed(self):
        self._candidate(_bad('Board Ǝally'), _read('Board Ǝally'))

    def test_control_underheld_34_governed(self):
        self._candidate(_bad('Board Ɣally'), _read('Board Ɣally'))

    def test_control_underheld_35_governed(self):
        self._candidate(_bad('Board ƫally'), _read('Board ƫally'))

    def test_control_underheld_36_governed(self):
        self._candidate(_bad('Board Ƭally'), _read('Board Ƭally'))

    def test_control_underheld_37_governed(self):
        self._candidate(_bad('Board ƭally'), _read('Board ƭally'))

    def test_control_underheld_38_governed(self):
        self._candidate(_bad('Board Ʈally'), _read('Board Ʈally'))

    def test_control_underheld_39_governed(self):
        self._candidate(_bad('Board Ʊally'), _read('Board Ʊally'))

    def test_control_underheld_40_governed(self):
        self._candidate(_bad('Board taɫly'), _read('Board taɫly'))

    def test_control_underheld_41_governed(self):
        self._candidate(_bad('Board taɬly'), _read('Board taɬly'))

    def test_control_underheld_42_governed(self):
        self._candidate(_bad('Board taɭly'), _read('Board taɭly'))

    def test_control_underheld_43_governed(self):
        self._candidate(_bad('Board taɮly'), _read('Board taɮly'))

    def test_control_underheld_44_governed(self):
        self._candidate(_bad('Board taɳly'), _read('Board taɳly'))

    def test_control_underheld_45_governed(self):
        self._candidate(_bad('Board taƔly'), _read('Board taƔly'))

    def test_control_underheld_46_governed(self):
        self._candidate(_bad('Board taƤly'), _read('Board taƤly'))

    def test_control_underheld_47_governed(self):
        self._candidate(_bad('Board taƮly'), _read('Board taƮly'))

    def test_control_underheld_48_governed(self):
        self._candidate(_bad('Board taƱly'), _read('Board taƱly'))

    def test_control_underheld_49_governed(self):
        self._candidate(_bad('Trace sɭmmarise'), _read('Trace sɭmmarise'))

    def test_control_underheld_50_governed(self):
        self._candidate(_bad('Trace sɯmmarise'), _read('Trace sɯmmarise'))

    def test_control_underheld_51_governed(self):
        self._candidate(_bad('Trace sɰmmarise'), _read('Trace sɰmmarise'))

    def test_control_underheld_52_governed(self):
        self._candidate(_bad('Trace sƔmmarise'), _read('Trace sƔmmarise'))

    def test_control_underheld_53_governed(self):
        self._candidate(_bad('Trace sƜmmarise'), _read('Trace sƜmmarise'))

    def test_control_underheld_54_governed(self):
        self._candidate(_bad('Trace sƮmmarise'), _read('Trace sƮmmarise'))

    def test_control_underheld_55_governed(self):
        self._candidate(_bad('Trace sƯmmarise'), _read('Trace sƯmmarise'))

    def test_control_underheld_56_governed(self):
        self._candidate(_bad('Trace sưmmarise'), _read('Trace sưmmarise'))

    def test_control_underheld_57_governed(self):
        self._candidate(_bad('Trace sƱmmarise'), _read('Trace sƱmmarise'))

    def test_control_underheld_58_governed(self):
        self._candidate(_bad('Trace sƲmmarise'), _read('Trace sƲmmarise'))

    def test_control_underheld_59_governed(self):
        self._candidate(_bad('Trace sumɱarise'), _read('Trace sumɱarise'))

    def test_control_underheld_60_governed(self):
        self._candidate(_bad('Trace sumɲarise'), _read('Trace sumɲarise'))

    def test_control_underheld_61_governed(self):
        self._candidate(_bad('Trace sumɴarise'), _read('Trace sumɴarise'))

    def test_control_underheld_62_governed(self):
        self._candidate(_bad('Trace sumɶarise'), _read('Trace sumɶarise'))

    def test_control_underheld_63_governed(self):
        self._candidate(_bad('Trace sumƔarise'), _read('Trace sumƔarise'))

    def test_control_underheld_64_governed(self):
        self._candidate(_bad('Trace sumƝarise'), _read('Trace sumƝarise'))

    def test_control_underheld_65_governed(self):
        self._candidate(_bad('Trace sumƮarise'), _read('Trace sumƮarise'))

    def test_control_underheld_66_governed(self):
        self._candidate(_bad('Trace sumƱarise'), _read('Trace sumƱarise'))

    def test_control_underheld_67_governed(self):
        self._candidate(_bad('Trace summariƔe'), _read('Trace summariƔe'))

    def test_control_underheld_68_governed(self):
        self._candidate(_bad('Trace summariƦe'), _read('Trace summariƦe'))

    def test_control_underheld_69_governed(self):
        self._candidate(_bad('Trace summariƧe'), _read('Trace summariƧe'))

    def test_control_underheld_70_governed(self):
        self._candidate(_bad('Trace summariƨe'), _read('Trace summariƨe'))

    def test_control_underheld_71_governed(self):
        self._candidate(_bad('Trace summariƮe'), _read('Trace summariƮe'))

    def test_control_underheld_72_governed(self):
        self._candidate(_bad('Trace summariƱe'), _read('Trace summariƱe'))

    def test_control_underheld_73_governed(self):
        self._candidate(_bad('Trace summariƷe'), _read('Trace summariƷe'))

    def test_control_underheld_74_governed(self):
        self._candidate(_bad('Trace summarisɵ'), _read('Trace summarisɵ'))

    def test_control_underheld_75_governed(self):
        self._candidate(_bad('Trace summarisƊ'), _read('Trace summarisƊ'))

    def test_control_underheld_76_governed(self):
        self._candidate(_bad('Trace summarisƐ'), _read('Trace summarisƐ'))

    def test_control_underheld_77_governed(self):
        self._candidate(_bad('Trace summarisƔ'), _read('Trace summarisƔ'))

    def test_control_underheld_78_governed(self):
        self._candidate(_bad('Trace summarisƟ'), _read('Trace summarisƟ'))

    def test_control_underheld_79_governed(self):
        self._candidate(_bad('Trace summarisƮ'), _read('Trace summarisƮ'))

    def test_control_underheld_80_governed(self):
        self._candidate(_bad('Trace summarisƱ'), _read('Trace summarisƱ'))

    def test_control_underheld_81_governed(self):
        self._candidate(_bad('Datatally'), _read('Datatally'))

    def test_control_underheld_82_governed(self):
        self._candidate(_bad('Boarddictionarytally'), _read('Boarddictionarytally'))

    def test_control_underheld_83_governed(self):
        self._candidate(_bad('Almanactally'), _read('Almanactally'))

    def test_control_underheld_84_governed(self):
        self._candidate(_bad('Gazettetally'), _read('Gazettetally'))

    def test_control_underheld_85_governed(self):
        self._candidate(_bad('Digesttally'), _read('Digesttally'))

    def test_control_underheld_86_governed(self):
        self._candidate(_bad('Dossiertally'), _read('Dossiertally'))

    def test_control_underheld_87_governed(self):
        self._candidate(_bad('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'), _read('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'))

    def test_control_underheld_88_governed(self):
        self._candidate(_bad('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewtrace'), _read('Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewtrace'))

    def test_control_underheld_89_governed(self):
        self._candidate(_bad('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'), _read('Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary'))

    def test_control_underheld_90_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board summary'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board summary'))

    def test_control_underheld_91_governed(self):
        self._candidate(_bad('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board trace'), _read('Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board trace'))

    def test_control_underheld_92_governed(self):
        self._candidate(_bad('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board for step 2'), _read('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex panel board for step 2'))
