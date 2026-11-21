"""Step 16 fix pass 29 unit 2 tests: the Q-4 widening unit.

Pinning tests for register item R16-29-01 (Medium, B29-C01
and B29-B01) of Step 16 round 29. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-29-01: malformed tally statement heads the restated
boundary of fix pass 28 still does not reach, in one
hundred and twenty four distinct alone forms in ten
subfamilies: (a) tally forms fused behind record words,
their plurals, and head words in the inverse positions,
twenty forms; (b) composite openings, eight forms; (c)
variant composite openings, four forms; (d) variant
spellings past the widened variant sets, fourteen forms;
(e) the summary word in further forms past the one
hundred and five, seven forms, the correctness
summarisation string standing as a distinct form of the
subfamily beside the breaker summarisation string
standing governed in the widened enumeration; (f) fused
closings built on those further forms, four forms; (g)
fused closings with sixteen governed words fused between
the closing words, three forms; (h) inserted closings
past the widened counts, seven forms, the correctness
string at twenty words and the breaker string at twenty
one words standing as two distinct forms of the
subfamily in the reversed full swap place; (i) the for
step closing past the widened inserted reach, one form;
and (j) further phi, theta, eth, eng and kindred letters
in unread positions, fifty six forms. The beside forms
stand driven in the Manuscripttally head, in the Tallyo5
head and in the Trace summariser head of the correctness
paper and in the Brochuretally head and the Trace
summarised head of the breaker paper, and the gate ruling
forms stand driven in the Manuscripttally head, in the
Tallyo5 head and in the Trace summariser head in the
correctness paper and in the Brochuretally head in the
breaker paper. Locus: derivation_core.py, _fold_word,
_tally_word and the constants _TALLY_WORD_FORMS,
_TOTALLY_FAMILY, _GOVERNED_FUSED_PREFIXES,
_TALLY_WORD_VARIANT_FORMS and
_TALLY_WORD_VARIANT_FUSED_FORMS, _summary_word and the
constant _SUMMARY_WORD_FORMS, _fused_trace_summary with
_fused_between_closing, and _tally_statement_head,
against _trace_candidates and the shared constant
_TALLY_COUNTED_PATTERN, which carries no head test.

Held controls stand pinned beside the defect forms, in
full: every form of R16-29-02 standing missing in its
cured form, as Unit 1 of this pass left it; every form of
R16-28-01 standing governed in its cured form and every
form of R16-28-02 standing missing in its cured form;
every form of R16-27-02 standing missing in its cured
form, and every form of R16-27-01 standing governed in
its cured form; every form of R16-26-02 standing missing
in its cured form, and every form of R16-26-01 standing
governed in its cured form; every form of R16-25-02
standing missing in its cured form, and every form of
R16-25-01 standing governed in its cured form; the
bounding controls of this item standing governed, as
stated in the bounding test of this unit; every form of
R16-24-02 standing missing in its cured form, and every
form of R16-24-01 standing governed in its cured form;
every form of R16-23-02 standing missing in its cured
form, and every form of R16-23-01 standing governed in
its cured form; every form of R16-22-02, R16-21-02,
R16-20-02, R16-19-02, R16-18-02 and R16-17-02 standing
missing in its cured form; the governed fused prefix
forms and the variant forms behind their governed
prefixes standing governed; the mixed inserted runs and
the prose order runs past the widened reach standing
missing; the seven enumerated family adverbs and tallyho
standing missing, the fused family forms standing
missing, and the twelve prose adverbs of R16-14-02
standing missing; the Board talli boundary control
standing missing; the folded round 10 prose sentence
record standing governed; the four folded marker shape
records standing present but not derivable; the golden
prose lines standing unflipped; and the read and absent
feeder controls byte for byte.
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


class TestStep16Fix29Unit2(FixtureTestCase):

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
    # R16-29-01 defect forms, subfamily (a): tally forms
    # fused behind record words, their plurals, and head
    # words in the inverse positions past the one hundred
    # and eighty six governed fused prefixes
    # ------------------------------------------------------

    def test_r16_29_01_subfamily_a_governed(self):
        for head in (                     'Stepstallies',
                     'Minutetally',
                     'Notetally',
                     'Sliptally',
                     'Manuscripttally',
                     'Typescripttally',
                     'Periodicaltally',
                     'Magazinetally',
                     'Brochuretally',
                     'Leaflettally',
                     'Annalstallies',
                     'Handouttally',
                     'Bannertally',
                     'Postertally',
                     'Brochurestallies',
                     'Leafletstallies',
                     'Handoutstallies',
                     'Bannertallies',
                     'Posterstallies',
                     'Noticestallies'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-29-01 defect forms, subfamily (b): composite
    # openings, a governed prefix in the opening position
    # with an unnamed word immediately before the tally
    # form
    # ------------------------------------------------------

    def test_r16_29_01_subfamily_b_governed(self):
        for head in (                     'Boardmanuscripttally',
                     'Boardperiodicaltally',
                     'Boardstepstallies',
                     'Boardminutetally',
                     'Boardbrochuretally',
                     'Gateleaflettally',
                     'Reviewhandouttally',
                     'Boardpostertally'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-29-01 defect forms, subfamily (c): variant
    # composite openings, a variant spelling standing
    # behind an unnamed word that itself stands behind a
    # governed prefix in the opening position
    # ------------------------------------------------------

    def test_r16_29_01_subfamily_c_governed(self):
        for head in (                     'Boardmanuscripttallye',
                     'Boardperiodicaltalliez',
                     'Boardbrochuretallye',
                     'Gateleaflettalliez'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-29-01 defect forms, subfamily (d): variant
    # spellings past the widened variant sets of sixty
    # three and sixty four, alone and behind a governed
    # prefix
    # ------------------------------------------------------

    def test_r16_29_01_subfamily_d_governed(self):
        for head in (                     'Tallyo5',
                     'Tallyu5',
                     'Tallyai5',
                     'Tallyez4',
                     'Tallyaz4',
                     'Tallya6',
                     'Tallyeo7',
                     'Boardtallyo5',
                     'Boardtallyu5',
                     'Boardtallyai5',
                     'Boardtallyez4',
                     'Boardtallyaz4',
                     'Boardtallya6',
                     'Boardtallyeo7'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-29-01 defect forms, subfamily (e): the summary
    # word in further forms past the one hundred and
    # five, each built on a form the widening of fix
    # pass 28 admitted with one further es repetition,
    # and the summarisation form of the correctness
    # paper standing as its own distinct form
    # ------------------------------------------------------

    def test_r16_29_01_subfamily_e_governed(self):
        for head in (                     'Trace summarisereseseseseseseseseseses',
                     'Trace summarisingeseseseseseseseseseses',
                     'Trace summarieseseseseseseseseseseses',
                     'Trace summarisedeseseseseseseseseseses',
                     'Trace summariseeseseseseseseseseseseses',
                     'Trace summaryeseseseseseseseseseseses',
                     'Trace summarisationeseseseseseseseseseseses'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-29-01 defect forms, subfamily (f): fused
    # closings built on those further summary forms
    # ------------------------------------------------------

    def test_r16_29_01_subfamily_f_governed(self):
        for head in (                     'Boardtracesummarisereseseseseseseseseseses',
                     'Tracessummarieseseseseseseseseseseses',
                     'Boardtracesummarisedeseseseseseseseses',
                     'Tracessummaryeseseseseseseseseseseses'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-29-01 defect forms, subfamily (g): fused
    # closings with sixteen governed words fused between
    # the closing words
    # ------------------------------------------------------

    def test_r16_29_01_subfamily_g_governed(self):
        for head in (                     'Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary',
                     'Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardtrace',
                     'Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-29-01 defect forms, subfamily (h): inserted
    # closings past the widened counts, nineteen words
    # standing between in the forward order and eighteen
    # in the reversed order, with the breaker reversed
    # full swap form standing as its own distinct form
    # at nineteen words standing between and twenty one
    # words in all
    # ------------------------------------------------------

    def test_r16_29_01_subfamily_h_governed(self):
        for head in (                     'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex summary',
                     'Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review annex summary',
                     'Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review summary',
                     'Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate review trace',
                     'Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate review trace',
                     'Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex trace',
                     'Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review trace'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-29-01 defect forms, subfamily (i): the for
    # step closing past the widened inserted reach,
    # nineteen words standing between the trace word and
    # the for step words
    # ------------------------------------------------------

    def test_r16_29_01_subfamily_i_governed(self):
        for head in ('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex for step 2',):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-29-01 defect forms, subfamily (j): further
    # phi, theta, eth, eng and kindred letters in unread
    # positions, each letter standing read elsewhere in
    # the fold readings the earlier passes landed
    # ------------------------------------------------------

    def test_r16_29_01_subfamily_j_governed(self):
        for head in (                     'Board tɸlly',
                     'Trace suɸmarise',
                     'Board tθlly',
                     'Trace suθmarise',
                     'Board tðlly',
                     'Trace suðmarise',
                     'Board tŋlly',
                     'Trace suŋmarise',
                     'Board tɲlly',
                     'Board tɳlly',
                     'Trace suɳmarise',
                     'Board tɽlly',
                     'Trace suɽmarise',
                     'Board tɾlly',
                     'Board tʁlly',
                     'Trace suʁmarise',
                     'Board tɢlly',
                     'Trace suɢmarise',
                     'Board tɪlly',
                     'Trace suɪmarise',
                     'Board tʏlly',
                     'Trace suʏmarise',
                     'Board tɨlly',
                     'Trace suɨmarise',
                     'Board tɵlly',
                     'Trace suɵmarise',
                     'Board tʆlly',
                     'Trace suʆmarise',
                     'Board tʍlly',
                     'Trace suʍmarise',
                     'Board tʎlly',
                     'Trace suʎmarise',
                     'Board tɘlly',
                     'Trace suɘmarise',
                     'Trace suɜmarise',
                     'Board tʃlly',
                     'Trace suʃmarise',
                     'Board tʧlly',
                     'Trace suʧmarise',
                     'Board tʤlly',
                     'Trace suʤmarise',
                     'Board tʇlly',
                     'Trace suʇmarise',
                     'Board ɸally',
                     'Trace ɸummarise',
                     'Board talɸy',
                     'Board ŋally',
                     'Trace ŋummarise',
                     'Board talʁy',
                     'Board taɸy',
                     'Board θally',
                     'Board taθy',
                     'Board taƚy',
                     'Trace summaɽise',
                     'Trace sʃmmarise',
                     'Trace summaʃise'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-29-01 beside and gate ruling forms: the beside
    # forms standing present over Step 3 with Step 2 named
    # uncounted after the cure, and the gate ruling forms
    # standing governed in the ruling form
    # ------------------------------------------------------

    def test_r16_29_01_beside_forms_uncounted(self):
        for head in (                     'Manuscripttally',
                     'Tallyo5',
                     'Trace summarisereseseseseseseseseseses',
                     'Brochuretally',
                     'Trace summarisedeseseseseseseseseseses'):
            self._beside_step2_uncounted(_bad(head))

    def test_r16_29_01_gate_ruling_forms_governed(self):
        for head in (                     'Manuscripttally',
                     'Tallyo5',
                     'Trace summarisereseseseseseseseseseses',
                     'Brochuretally'):
            report = self._q4_alone(_bad(head), ruling=True)
            self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # R16-29-01 code level forms: the driven words under
    # the word tests, the driven heads under the head
    # test, and the fifty six defect letters under the
    # fold
    # ------------------------------------------------------

    def test_r16_29_01_code_level_forms(self):
        for word in (                     'stepstallies',
                     'minutetally',
                     'notetally',
                     'sliptally',
                     'manuscripttally',
                     'typescripttally',
                     'periodicaltally',
                     'magazinetally',
                     'brochuretally',
                     'leaflettally',
                     'annalstallies',
                     'handouttally',
                     'bannertally',
                     'postertally',
                     'brochurestallies',
                     'leafletstallies',
                     'handoutstallies',
                     'bannertallies',
                     'posterstallies',
                     'noticestallies',
                     'boardmanuscripttally',
                     'boardperiodicaltally',
                     'boardstepstallies',
                     'boardminutetally',
                     'boardbrochuretally',
                     'gateleaflettally',
                     'reviewhandouttally',
                     'boardpostertally',
                     'boardmanuscripttallye',
                     'boardperiodicaltalliez',
                     'boardbrochuretallye',
                     'gateleaflettalliez',
                     'tallyo5',
                     'tallyu5',
                     'tallyai5',
                     'tallyez4',
                     'tallyaz4',
                     'tallya6',
                     'tallyeo7',
                     'boardtallyo5',
                     'boardtallyu5',
                     'boardtallyai5',
                     'boardtallyez4',
                     'boardtallyaz4',
                     'boardtallya6',
                     'boardtallyeo7'):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in (                     'summarisereseseseseseseseseseses',
                     'summarisingeseseseseseseseseseses',
                     'summarieseseseseseseseseseseses',
                     'summarisedeseseseseseseseseseses',
                     'summariseeseseseseseseseseseseses',
                     'summaryeseseseseseseseseseseses',
                     'summarisationeseseseseseseseseseseses'):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in (                     'boardtracesummarisereseseseseseseseseseses',
                     'tracessummarieseseseseseseseseseseses',
                     'boardtracesummarisedeseseseseseseseses',
                     'tracessummaryeseseseseseseseseseseses',
                     'traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary',
                     'summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardtrace',
                     'tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary'):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        line = 'Manuscripttally: items checked stand here'
        self.assertTrue(_tally_statement_head(line), 'Manuscripttally')
        line = 'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex summary: items checked stand here'
        self.assertTrue(_tally_statement_head(line), 'Trace board gate review annex ')
        line = 'Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate annex review trace: items checked stand here'
        self.assertTrue(_tally_statement_head(line), 'Summary board gate annex revie')
        line = 'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review annex for step 2: items checked stand here'
        self.assertTrue(_tally_statement_head(line), 'Trace board gate review annex ')
        line = 'Trace summarisedeseseseseseseseseseses: items checked stand here'
        self.assertTrue(_tally_statement_head(line), 'Trace summarisedeseseseseseses')
        self.assertEqual(_fold_word('tɸlly'), "tally")
        self.assertEqual(_fold_word('suɸmarise'), "summarise")
        self.assertEqual(_fold_word('tθlly'), "tally")
        self.assertEqual(_fold_word('suθmarise'), "summarise")
        self.assertEqual(_fold_word('tðlly'), "tally")
        self.assertEqual(_fold_word('suðmarise'), "summarise")
        self.assertEqual(_fold_word('tŋlly'), "tally")
        self.assertEqual(_fold_word('suŋmarise'), "summarise")
        self.assertEqual(_fold_word('tɲlly'), "tally")
        self.assertEqual(_fold_word('tɳlly'), "tally")
        self.assertEqual(_fold_word('suɳmarise'), "summarise")
        self.assertEqual(_fold_word('tɽlly'), "tally")
        self.assertEqual(_fold_word('suɽmarise'), "summarise")
        self.assertEqual(_fold_word('tɾlly'), "tally")
        self.assertEqual(_fold_word('tʁlly'), "tally")
        self.assertEqual(_fold_word('suʁmarise'), "summarise")
        self.assertEqual(_fold_word('tɢlly'), "tally")
        self.assertEqual(_fold_word('suɢmarise'), "summarise")
        self.assertEqual(_fold_word('tɪlly'), "tally")
        self.assertEqual(_fold_word('suɪmarise'), "summarise")
        self.assertEqual(_fold_word('tʏlly'), "tally")
        self.assertEqual(_fold_word('suʏmarise'), "summarise")
        self.assertEqual(_fold_word('tɨlly'), "tally")
        self.assertEqual(_fold_word('suɨmarise'), "summarise")
        self.assertEqual(_fold_word('tɵlly'), "tally")
        self.assertEqual(_fold_word('suɵmarise'), "summarise")
        self.assertEqual(_fold_word('tʆlly'), "tally")
        self.assertEqual(_fold_word('suʆmarise'), "summarise")
        self.assertEqual(_fold_word('tʍlly'), "tally")
        self.assertEqual(_fold_word('suʍmarise'), "summarise")
        self.assertEqual(_fold_word('tʎlly'), "tally")
        self.assertEqual(_fold_word('suʎmarise'), "summarise")
        self.assertEqual(_fold_word('tɘlly'), "tally")
        self.assertEqual(_fold_word('suɘmarise'), "summarise")
        self.assertEqual(_fold_word('suɜmarise'), "summarise")
        self.assertEqual(_fold_word('tʃlly'), "tally")
        self.assertEqual(_fold_word('suʃmarise'), "summarise")
        self.assertEqual(_fold_word('tʧlly'), "tally")
        self.assertEqual(_fold_word('suʧmarise'), "summarise")
        self.assertEqual(_fold_word('tʤlly'), "tally")
        self.assertEqual(_fold_word('suʤmarise'), "summarise")
        self.assertEqual(_fold_word('tʇlly'), "tally")
        self.assertEqual(_fold_word('suʇmarise'), "summarise")
        self.assertEqual(_fold_word('ɸally'), "tally")
        self.assertEqual(_fold_word('ɸummarise'), "summarise")
        self.assertEqual(_fold_word('talɸy'), "tally")
        self.assertEqual(_fold_word('ŋally'), "tally")
        self.assertEqual(_fold_word('ŋummarise'), "summarise")
        self.assertEqual(_fold_word('talʁy'), "tally")
        self.assertEqual(_fold_word('taɸy'), "tally")
        self.assertEqual(_fold_word('θally'), "tally")
        self.assertEqual(_fold_word('taθy'), "tally")
        self.assertEqual(_fold_word('taƚy'), "tally")
        self.assertEqual(_fold_word('summaɽise'), "summarise")
        self.assertEqual(_fold_word('sʃmmarise'), "summarise")
        self.assertEqual(_fold_word('summaʃise'), "summarise")

    # ------------------------------------------------------
    # Control forms of R16-28-01 standing governed in
    # their cured form, subfamily (a): tally forms
    # fused behind record words and their plurals past the
    # one hundred and sixty seven governed fused prefixes
    # ------------------------------------------------------

    def test_control_fix28_subfamily_a_governed(self):
        for head in ('Cataloguestallies',
                     'Encyclopediastallies',
                     'Indexestallies',
                     'Logstallies',
                     'Passestallies',
                     'Registriestallies',
                     'Censusestallies',
                     'Gatetally',
                     'Steptally',
                     'Dictionarytally',
                     'Vocabularytally',
                     'Inventorytally',
                     'Calendartally',
                     'Syllabustally',
                     'Dictionariestallies',
                     'Vocabulariestallies',
                     'Inventoriestallies',
                     'Calendarstallies',
                     'Syllabusestallies'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Control forms of R16-28-01 standing governed in
    # their cured form, subfamily (b): composite
    # openings, a governed prefix in the opening position
    # with an unnamed plural or an unnamed record word
    # immediately before the tally form
    # ------------------------------------------------------

    def test_control_fix28_subfamily_b_governed(self):
        for head in ('Boardcataloguestallies',
                     'Boardencyclopediastallies',
                     'Boardindexestallies',
                     'Boardlogstallies',
                     'Boarddictionarytally',
                     'Gatevocabularytally',
                     'Reviewinventorytally',
                     'Boardcalendartally'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Control forms of R16-28-01 standing governed in
    # their cured form, subfamily (c): variant
    # composite openings, a variant spelling standing
    # behind an unnamed plural or an unnamed record word
    # that itself stands behind a governed prefix in the
    # opening position
    # ------------------------------------------------------

    def test_control_fix28_subfamily_c_governed(self):
        for head in ('Boardcataloguestallye',
                     'Boardencyclopediastallye',
                     'Boarddictionarytallye',
                     'Gatevocabularytalliez'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Control forms of R16-28-01 standing governed in
    # their cured form, subfamily (d): variant
    # spellings past the widened variant sets of fifty six
    # and fifty seven, standing alone and behind a
    # governed prefix
    # ------------------------------------------------------

    def test_control_fix28_subfamily_d_governed(self):
        for head in ('Tallyo4',
                     'Tallyu4',
                     'Tallyai4',
                     'Tallyez3',
                     'Tallyaz3',
                     'Tallya5',
                     'Tallyeo6',
                     'Boardtallyo4',
                     'Boardtallyu4',
                     'Boardtallyai4',
                     'Boardtallyez3',
                     'Boardtallyaz3',
                     'Boardtallya5',
                     'Boardtallyeo6'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Control forms of R16-28-01 standing governed in
    # their cured form, subfamily (e): the summary
    # word in further forms past the ninety eight, each
    # built on a form the widening of fix pass 27 admitted
    # with one further es repetition, the breaker paper
    # summarise string standing in the loop in its own
    # shorter form beside the correctness string
    # ------------------------------------------------------

    def test_control_fix28_subfamily_e_governed(self):
        for head in ('Trace summarisereseseseseseseseseses',
                     'Trace summarisingeseseseseseseseseses',
                     'Trace summarieseseseseseseseseseses',
                     'Trace summarisedeseseseseseseseseses',
                     'Trace summariseeseseseseseseseseseses',
                     'Trace summariseeseseseseseseseseses',
                     'Trace summaryeseseseseseseseseseses',
                     'Trace summarisationeseseseseseseseseseses'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Control forms of R16-28-01 standing governed in
    # their cured form, subfamily (f): fused
    # closings built on those further forms
    # ------------------------------------------------------

    def test_control_fix28_subfamily_f_governed(self):
        for head in ('Boardtracesummarisereseseseseseseseseses',
                     'Tracessummarieseseseseseseseseseses',
                     'Boardtracesummarisedeseseseseseseseseses',
                     'Tracessummaryeseseseseseseseseseses'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Control forms of R16-28-01 standing governed in
    # their cured form, subfamily (g): fused
    # closings with fifteen governed words fused between
    # the closing words
    # ------------------------------------------------------

    def test_control_fix28_subfamily_g_governed(self):
        for head in ('Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary',
                     'Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpaneltrace',
                     'Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Control forms of R16-28-01 standing governed in
    # their cured form, subfamily (h): inserted
    # closings past the widened counts, eighteen words
    # forward and seventeen words reversed, in the wide
    # form, the middle swap form and the full swap form,
    # with the breaker forward swap form beside them
    # ------------------------------------------------------

    def test_control_fix28_subfamily_h_governed(self):
        for head in ('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review summary',
                     'Trace board gate review annex panel board annex gate review panel board gate review annex panel board gate review summary',
                     'Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate annex summary',
                     'Trace board gate annex review panel board gate annex review panel board gate annex review panel board gate review summary',
                     'Summary board gate review annex panel board gate review annex panel board gate review annex panel board gate trace',
                     'Summary board gate review annex panel board annex gate review panel board gate review annex panel board gate trace',
                     'Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate trace'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Control forms of R16-28-01 standing governed in
    # their cured form, subfamily (i): the for step
    # closing past the widened inserted reach, eighteen
    # words standing between the trace word and the for
    # step words
    # ------------------------------------------------------

    def test_control_fix28_subfamily_i_governed(self):
        for head in ('Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review for step 2',):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Control forms of R16-28-01 standing governed in
    # their cured form, subfamily (j): further hook,
    # small capital and kindred letters in unread
    # positions, thirty nine forms of the correctness
    # paper and eight forms of the breaker paper, the two
    # papers driving disjoint letter sets at disjoint
    # positions
    # ------------------------------------------------------

    def test_control_fix28_subfamily_j_governed(self):
        for head in ('Board tʛlly',
                     'Board tʜlly',
                     'Board tʐlly',
                     'Board talʑy',
                     'Board tʚlly',
                     'Board tɺlly',
                     'Board tʓlly',
                     'Board tʙlly',
                     'Board tʀlly',
                     'Board tɴlly',
                     'Board ɖally',
                     'Board tʄlly',
                     'Board talʅy',
                     'Board tʉlly',
                     'Board tʊlly',
                     'Board tʋlly',
                     'Board tʒlly',
                     'Board tʔlly',
                     'Board talʕy',
                     'Board tʗlly',
                     'Board tʘlly',
                     'Board tʝlly',
                     'Board ɗally',
                     'Trace suʛmarise',
                     'Trace suʐmarise',
                     'Trace suʑmarise',
                     'Trace suʚmarise',
                     'Trace suɺmarise',
                     'Trace summʓrise',
                     'Trace suʙmarise',
                     'Trace suʀmarise',
                     'Trace suʈmarise',
                     'Trace suɖmarise',
                     'Trace ʄummarise',
                     'Trace suʋmarise',
                     'Trace suʕmarise',
                     'Trace suʗmarise',
                     'Trace suʝmarise',
                     'Trace suɗmarise',
                     'Board ʄally',
                     'Board taʐy',
                     'Board taʑy',
                     'Board taɀy',
                     'Board taʅy',
                     'Trace ʆummarise',
                     'Trace summʊrise',
                     'Trace summaʋise'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Control beside and gate ruling forms of R16-28-01: the beside
    # forms standing present over Step 3 with Step 2 named
    # uncounted after the cure, and the gate ruling forms
    # standing governed in the ruling form
    # ------------------------------------------------------

    def test_control_fix28_beside_forms_uncounted(self):
        for head in ("Cataloguestallies",
                     "Tallyo4",
                     'Trace summarisereseseseseseseseseses',
                     "Dictionarytally",
                     'Trace summarisedeseseseseseseseseses'):
            self._beside_step2_uncounted(_bad(head))

    def test_control_fix28_gate_ruling_forms_governed(self):
        for head in ("Cataloguestallies",
                     "Tallyo4",
                     'Trace summarisereseseseseseseseseses',
                     "Dictionarytally"):
            report = self._q4_alone(_bad(head), ruling=True)
            self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # Control code level forms of R16-28-01: the driven words under
    # the word tests, the driven heads under the head test,
    # and the forty seven defect letters under the fold
    # ------------------------------------------------------

    def test_control_fix28_code_level_forms(self):
        for word in ('cataloguestallies',
                     'encyclopediastallies',
                     'indexestallies',
                     'logstallies',
                     'passestallies',
                     'registriestallies',
                     'censusestallies',
                     'gatetally',
                     'steptally',
                     'dictionarytally',
                     'vocabularytally',
                     'inventorytally',
                     'calendartally',
                     'syllabustally',
                     'dictionariestallies',
                     'vocabulariestallies',
                     'inventoriestallies',
                     'calendarstallies',
                     'syllabusestallies',
                     'boardcataloguestallies',
                     'boardencyclopediastallies',
                     'boardindexestallies',
                     'boardlogstallies',
                     'boarddictionarytally',
                     'gatevocabularytally',
                     'reviewinventorytally',
                     'boardcalendartally',
                     'boardcataloguestallye',
                     'boardencyclopediastallye',
                     'boarddictionarytallye',
                     'gatevocabularytalliez',
                     'tallyo4',
                     'tallyu4',
                     'tallyai4',
                     'tallyez3',
                     'tallyaz3',
                     'tallya5',
                     'tallyeo6',
                     'boardtallyo4',
                     'boardtallyu4',
                     'boardtallyai4',
                     'boardtallyez3',
                     'boardtallyaz3',
                     'boardtallya5',
                     'boardtallyeo6'):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ('summarisereseseseseseseseseses',
                     'summarisingeseseseseseseseseses',
                     'summarieseseseseseseseseseses',
                     'summarisedeseseseseseseseseses',
                     'summariseeseseseseseseseseseses',
                     'summariseeseseseseseseseseses',
                     'summaryeseseseseseseseseseses',
                     'summarisationeseseseseseseseseseses'):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ('boardtracesummarisereseseseseseseseseses',
                     'tracessummarieseseseseseseseseseses',
                     'boardtracesummarisedeseseseseseseseseses',
                     'tracessummaryeseseseseseseseseseses',
                     'traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary',
                     'summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpaneltrace',
                     'tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary'):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        line = 'Cataloguestallies: items checked stand here'
        self.assertTrue(_tally_statement_head(line), 'Cataloguestallies')
        line = 'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review summary: items checked stand here'
        self.assertTrue(_tally_statement_head(line), 'Trace board gate review annex panel bo')
        line = 'Summary board gate annex review panel board gate annex review panel board gate annex review panel board gate trace: items checked stand here'
        self.assertTrue(_tally_statement_head(line), 'Summary board gate annex review panel ')
        line = 'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review for step 2: items checked stand here'
        self.assertTrue(_tally_statement_head(line), 'Trace board gate review annex panel bo')
        line = 'Trace summarisedeseseseseseseseseses: items checked stand here'
        self.assertTrue(_tally_statement_head(line), 'Trace summarisedeseseseseseseseseses')
        self.assertEqual(_fold_word('tʛlly'), "tally")
        self.assertEqual(_fold_word('tʜlly'), "tally")
        self.assertEqual(_fold_word('tʐlly'), "tally")
        self.assertEqual(_fold_word('talʑy'), "tally")
        self.assertEqual(_fold_word('tʚlly'), "tally")
        self.assertEqual(_fold_word('tɺlly'), "tally")
        self.assertEqual(_fold_word('tʓlly'), "tally")
        self.assertEqual(_fold_word('tʙlly'), "tally")
        self.assertEqual(_fold_word('tʀlly'), "tally")
        self.assertEqual(_fold_word('tɴlly'), "tally")
        self.assertEqual(_fold_word('ɖally'), "tally")
        self.assertEqual(_fold_word('tʄlly'), "tally")
        self.assertEqual(_fold_word('talʅy'), "tally")
        self.assertEqual(_fold_word('tʉlly'), "tally")
        self.assertEqual(_fold_word('tʊlly'), "tally")
        self.assertEqual(_fold_word('tʋlly'), "tally")
        self.assertEqual(_fold_word('tʒlly'), "tally")
        self.assertEqual(_fold_word('tʔlly'), "tally")
        self.assertEqual(_fold_word('talʕy'), "tally")
        self.assertEqual(_fold_word('tʗlly'), "tally")
        self.assertEqual(_fold_word('tʘlly'), "tally")
        self.assertEqual(_fold_word('tʝlly'), "tally")
        self.assertEqual(_fold_word('ɗally'), "tally")
        self.assertEqual(_fold_word('ʄally'), "tally")
        self.assertEqual(_fold_word('taʐy'), "tally")
        self.assertEqual(_fold_word('taʑy'), "tally")
        self.assertEqual(_fold_word('taɀy'), "tally")
        self.assertEqual(_fold_word('taʅy'), "tally")
        self.assertEqual(_fold_word('suʛmarise'), "summarise")
        self.assertEqual(_fold_word('suʐmarise'), "summarise")
        self.assertEqual(_fold_word('suʑmarise'), "summarise")
        self.assertEqual(_fold_word('suʚmarise'), "summarise")
        self.assertEqual(_fold_word('suɺmarise'), "summarise")
        self.assertEqual(_fold_word('summʓrise'), "summarise")
        self.assertEqual(_fold_word('suʙmarise'), "summarise")
        self.assertEqual(_fold_word('suʀmarise'), "summarise")
        self.assertEqual(_fold_word('suʈmarise'), "summarise")
        self.assertEqual(_fold_word('suɖmarise'), "summarise")
        self.assertEqual(_fold_word('ʄummarise'), "summarise")
        self.assertEqual(_fold_word('suʋmarise'), "summarise")
        self.assertEqual(_fold_word('suʕmarise'), "summarise")
        self.assertEqual(_fold_word('suʗmarise'), "summarise")
        self.assertEqual(_fold_word('suʝmarise'), "summarise")
        self.assertEqual(_fold_word('suɗmarise'), "summarise")
        self.assertEqual(_fold_word('ʆummarise'), "summarise")
        self.assertEqual(_fold_word('summʊrise'), "summarise")
        self.assertEqual(_fold_word('summaʋise'), "summarise")

    # ------------------------------------------------------
    # Held controls: every form of R16-28-02 standing
    # missing in its cured form, as Unit 1 of this pass
    # left it, its direct forms, its fused forms and its
    # run, aside and clause forms, in full
    # ------------------------------------------------------

    def test_r16_28_02_held_direct_forms_missing(self):
        for run in ('Panel shove trace summary',
                    'Panel tug trace summary',
                    'Panel heave trace summary',
                    'Panel yank trace summary',
                    'Panel snatch trace summary',
                    'Panel leave trace summary',
                    'Clerk bit summary trace',
                    'Panel beat trace summary',
                    'Team lost summary trace',
                    'Clerk fed summary trace',
                    'Clerk forgot summary trace',
                    'Team lost trace summary',
                    'Panel shot summary trace',
                    'Clerk fed trace summary',
                    'Team trim summary trace'):
            self._assert_q4_missing(self._q4_alone(_prose(run)))
    def test_r16_28_02_held_fused_forms_missing(self):
        for run in ('Panel shove tracesummary',
                    'Panel shove boardtracesummary',
                    'Panel shove traceboardgatesummary',
                    'Panel shove traceboardgatereviewannexpanelsummary',
                    'Panel shove traceboardgatereviewannexpanelboardsummary',
                    'Panel shove traceboardgatereviewannexpanelboardgatesummary',
                    'Panel shove traceboardgatereviewannexpanelboardgatereviewsummary',
                    'Panel shove traceboardgatereviewannexpanelboardgatereviewannexsummary',
                    'Panel shove traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary',
                    'Panel shove traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary',
                    'Panel shove traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary',
                    'Panel beat tracesummary',
                    'Clerk bit summarytrace',
                    'Panel yank tracesummary',
                    'Clerk forgot summarytrace',
                    'Team lost boardtracesummary',
                    'Panel shot traceboardgatesummary',
                    'Clerk fed traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary',
                    'Team yank tracesummarisedeseseseseseseseses'):
            self._assert_q4_missing(self._q4_alone(_prose(run)))
    def test_r16_28_02_held_run_and_clause_forms_missing(self):
        for run in ('Ledger ₣ trace summary',
                    'Ledger ₧ trace summary',
                    'Ledger ₯ trace summary',
                    'Ledger ₰ trace summary',
                    'Ledger ₢ trace summary',
                    'Ledger ₠ trace summary',
                    'Ledger ₥ trace summary',
                    'Ledger ₨ trace summary',
                    'Ledger ؋ trace summary',
                    'Ledger ৳ trace summary',
                    'Ledger ៛ trace summary',
                    'Ledger ﷼ trace summary',
                    'Ledger ⦃panel⦄ trace summary',
                    'Ledger ⧼panel⧽ trace summary',
                    'Ledger ⸤panel⸥ trace summary',
                    'Ledger ⸢panel⸣ trace summary',
                    'Ledger ﹝panel﹞ trace summary',
                    'Ledger ⟬panel⟭ trace summary',
                    'Ledger ❰panel❱ trace summary',
                    'Ledger ﹛panel﹜ trace summary',
                    'Ledger ⦑panel⦒ trace summary',
                    'Shove panel trace summary',
                    'Bit panel summary trace',
                    'Beat panel trace summary',
                    'Yank ledger trace summary'):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_28_02_held_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel yank trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger \u2983panel\u2984 trace summary"),
            ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger \u20a3 trace summary"), ruling=True))
        self._beside_step2_nowhere(_prose(
            "Panel yank trace summary"))
        self._beside_step2_nowhere(_prose(
            "Ledger \u2983panel\u2984 trace summary"))
        self._beside_step2_nowhere(_prose(
            "Ledger \u20a3 trace summary"))

    def test_r16_28_02_held_code_level_prose_no_head(self):
        for run in ('Panel yank trace summary',
                    'Clerk forgot summary trace',
                    'Panel yank tracesummary',
                    'Clerk fed traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary',
                    'Ledger ؋ trace summary',
                    'Ledger ﷼ trace summary',
                    'Ledger ⟬panel⟭ trace summary'):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)


    # ------------------------------------------------------
    # Held controls: every form of R16-29-02 standing
    # missing in its cured form, as Unit 1 of this pass
    # left it, its direct forms, its fused forms and its
    # run, aside and clause forms, in full
    # ------------------------------------------------------

    def test_r16_29_02_held_direct_forms_missing(self):
        for run in (                     'Panel twist trace summary',
                     'Panel wrench trace summary',
                     'Panel squeeze trace summary',
                     'Panel hoist trace summary',
                     'Panel grasp trace summary',
                     'Clerk wrung summary trace',
                     'Panel flung trace summary',
                     'Team clung summary trace',
                     'Clerk forgave summary trace',
                     'Panel shrug trace summary',
                     'Clerk blink summary trace',
                     'Team cough trace summary',
                     'Panel slid summary trace',
                     'Clerk stung trace summary',
                     'Team shrank summary trace'):
            self._assert_q4_missing(self._q4_alone(_prose(run)))
    def test_r16_29_02_held_fused_forms_missing(self):
        for run in (                     'Panel twist tracesummary',
                     'Panel twist boardtracesummary',
                     'Panel twist traceboardgatesummary',
                     'Panel twist traceboardgatereviewannexpanelsummary',
                     'Panel twist traceboardgatereviewannexpanelboardsummary',
                     'Panel twist traceboardgatereviewannexpanelboardgatesummary',
                     'Panel twist traceboardgatereviewannexpanelboardgatereviewsummary',
                     'Panel twist traceboardgatereviewannexpanelboardgatereviewannexsummary',
                     'Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary',
                     'Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary',
                     'Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary',
                     'Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary',
                     'Panel flung tracesummary',
                     'Clerk wrung summarytrace',
                     'Panel shrug tracesummary',
                     'Clerk blink summarytrace',
                     'Team cough boardtracesummary',
                     'Panel slid traceboardgatesummary',
                     'Clerk stung traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary',
                     'Team shrug tracesummarisedeseseseseseseseses'):
            self._assert_q4_missing(self._q4_alone(_prose(run)))
    def test_r16_29_02_held_run_and_clause_forms_missing(self):
        for run in (                     'Ledger ₳ trace summary',
                     'Ledger ₵ trace summary',
                     'Ledger ₶ trace summary',
                     'Ledger ₷ trace summary',
                     'Ledger ₻ trace summary',
                     'Ledger ⃀ trace summary',
                     'Ledger ❪panel❫ trace summary',
                     'Ledger ❬panel❭ trace summary',
                     'Ledger ⟅panel⟆ trace summary',
                     'Ledger ﹙panel﹚ trace summary',
                     'Ledger ｛panel｝ trace summary',
                     'Ledger ༺panel༻ trace summary',
                     'Ledger ﹃panel﹄ trace summary',
                     'Ledger ⦗panel⦘ trace summary',
                     'Ledger （panel） trace summary',
                     'Ledger 〘panel〙 trace summary',
                     'Ledger ⦋panel⦌ trace summary',
                     'Twist panel trace summary',
                     'Wrung panel summary trace',
                     'Flung panel trace summary',
                     'Shrug ledger trace summary'):
            self._assert_q4_missing(self._q4_alone(_prose(run)))
    def test_r16_29_02_held_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel twist trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger \u20b3 trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger \u276apanel\u276b trace summary"),
            ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel shrug trace summary"), ruling=True))
        self._beside_step2_nowhere(_prose(
            "Panel twist trace summary"))
        self._beside_step2_nowhere(_prose(
            "Ledger \u20b3 trace summary"))
        self._beside_step2_nowhere(_prose(
            "Ledger \u276apanel\u276b trace summary"))
        self._beside_step2_nowhere(_prose(
            "Panel shrug trace summary"))

    def test_r16_29_02_held_code_level_prose_no_head(self):
        for run in ('Panel twist trace summary',
                    'Clerk wrung summary trace',
                    'Panel twist tracesummary',
                    'Clerk stung traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary',
                    'Ledger \u20b3 trace summary',
                    'Ledger \u20c0 trace summary',
                    'Ledger \uff08panel\uff09 trace summary',
                    'Ledger \u276apanel\u276b trace summary',
                    'Shrug ledger trace summary'):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)

    # ------------------------------------------------------
    # R16-29-01 bounding forms standing governed in their
    # exact forms: the plain fused forms standing governed
    # through a governed word at the close of the fused
    # form or through the card block, the variant
    # composite candidates, the breaker summarisation
    # form in its enumerated standing, the closings at
    # the counts fix pass 28 reached, and the candidate
    # letters folding to their words
    # ------------------------------------------------------

    def test_r16_29_01_bounding_forms_governed(self):
        for head in (                     'Daybooktally',
                     'Logbooktally',
                     'Placardtally',
                     'Placardstallies',
                     'Portfoliostallies',
                     'Handbooktally',
                     'Gazetteerstallies',
                     'Boarddictionarytallye',
                     'Gatevocabularytalliez',
                     'Trace summarisationeseseseseseseseseses',
                     'Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary',
                     'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review summary',
                     'Trace board gate review annex panel board gate review annex panel board gate review annex panel board gate review for step 2',
                     'Trace summarisereseseseseseseseseses',
                     'Boardtracesummarisereseseseseseseseses',
                     'Trace suɲmarise',
                     'Trace suɾmarise',
                     'Board tɜlly',
                     'Board talŋy',
                     'Board ʁally',
                     'Trace ʁummarise',
                     'Board ƭally',
                     'Board ȶally',
                     'Trace ʃummarise',
                     'Trace summɑrise',
                     'Trace summarɪse',
                     'Trace summarɨse'):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-28-01 bounding forms standing governed in their
    # exact forms: the plain fused forms standing governed
    # through a governed word or the book prefix, the
    # variant composite candidates, the breaker
    # summarisation form in its enumerated standing, the
    # closings at the counts fix pass 27 reached, and the
    # candidate letters folding to their words
    # ------------------------------------------------------

    def test_r16_28_01_bounding_forms_governed(self):
        for head in ("Portfoliostallies",
                     "Handbooktally",
                     "Gazetteerstallies",
                     "Workbooktally",
                     "Gatecataloguetalliez",
                     "Boardencyclopediatallyes",
                     "Trace summarisationeseseseseseseseseses"):
            self._candidate_governed(_bad(head), _read(head))
        for head in ("Board \u0287ally", "Board \u0288ally",
                     "Board \u029bally", "Board t\u0252lly",
                     "Trace s\u0289mmarise", "Trace summar\u0268se",
                     "Trace summaris\u0207", "Trace ʜummarise",
                     "Trace su\u0274marise", "Trace s\u028ammarise",
                     "Trace \u0292ummarise", "Trace \u0294ummarise",
                     "Board \u02a3ally", "Trace s\u0263mmarise"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Held controls: every form of R16-27-02 standing
    # missing in its cured form, as Unit 1 of this pass
    # left it, its direct forms, its fused forms and its
    # run, aside and clause forms, in full
    # ------------------------------------------------------

    def test_r16_27_02_held_direct_forms_missing(self):
        for run in ("Panel grab trace summary",
                    "Panel drag trace summary",
                    "Panel haul trace summary",
                    "Panel kick trace summary",
                    "Clerk began summary trace",
                    "Panel sat trace summary",
                    "Clerk felt summary trace",
                    "Panel stuck trace summary",
                    "Team fought summary trace",
                    "Clerk crept trace summary",
                    "Panel swept trace summary",
                    "Team dealt summary trace",
                    "Panel rang trace summary",
                    "Clerk rose summary trace",
                    "Team sat trace summary",
                    "Panel spun summary trace",
                    "Clerk struck trace summary",
                    "Team drag trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_27_02_held_fused_forms_missing(self):
        for run in ("Panel grab tracesummary",
                    "Panel grab boardtracesummary",
                    "Panel grab traceboardgatesummary",
                    "Panel grab traceboardgatereviewannexpanelsummary",
                    "Panel grab traceboardgatereviewannexpanelboardsummary",
                    "Panel grab traceboardgatereviewannexpanelboardgatesummary",
                    "Panel grab traceboardgatereviewannexpanelboardgatereviewsummary",
                    "Panel grab traceboardgatereviewannexpanelboardgatereviewannexsummary",
                    "Panel grab traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary",
                    "Panel grab traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary",
                    "Panel sat tracesummary",
                    "Clerk began summarytrace",
                    "Panel rang tracesummary",
                    "Clerk rose summarytrace",
                    "Team sat boardtracesummary",
                    "Panel spun traceboardgatesummary",
                    "Clerk struck traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary",
                    "Team drag tracesummarisedeseseseseseseses"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_27_02_held_run_and_clause_forms_missing(self):
        for run in ("Ledger ¤ trace summary",
                    "Ledger ₭ trace summary",
                    "Ledger ₱ trace summary",
                    "Ledger ₮ trace summary",
                    "Ledger ֏ trace summary",
                    "Ledger ₲ trace summary",
                    "Ledger ฿ trace summary",
                    "Ledger ₪ trace summary",
                    "Ledger ₡ trace summary",
                    "Ledger ₤ trace summary",
                    "Ledger ⌊panel⌋ trace summary",
                    "Ledger ⦅panel⦆ trace summary",
                    "Ledger 《panel》 trace summary",
                    "Ledger 〔panel〕 trace summary",
                    "Ledger ⟮panel⟯ trace summary",
                    "Ledger ❴panel❵ trace summary",
                    "Ledger ﹟panel﹠ trace summary",
                    "Grab panel trace summary",
                    "Began panel summary trace",
                    "Sat panel trace summary",
                    "Ledger ₫ trace summary",
                    "Ledger ₼ trace summary",
                    "Ledger ₾ trace summary",
                    "Ledger 〖panel〗 trace summary",
                    "Ledger ⸉panel⸊ trace summary",
                    "Ledger ⧘panel⧙ trace summary",
                    "Ledger ⧈panel⧉ trace summary",
                    "Drag ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_27_02_held_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel grab trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger \u230apanel\u230b trace summary"),
            ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel rang trace summary"), ruling=True))
        self._beside_step2_nowhere(_prose("Panel grab trace summary"))
        self._beside_step2_nowhere(
            _prose("Ledger \u230apanel\u230b trace summary"))
        self._beside_step2_nowhere(_prose("Panel rang trace summary"))

    def test_r16_27_02_held_code_level_prose_no_head(self):
        for run in ("Panel grab trace summary",
                    "Clerk began summary trace",
                    "Panel grab tracesummary",
                    "Clerk struck "
                    "traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary",
                    "Ledger \u00a4 trace summary",
                    "Ledger \u20aa trace summary",
                    "Ledger \u230apanel\u230b trace summary"):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)

    def test_r16_27_02_held_bounding_fresh_shapes_missing(self):
        for run in ("Panel grabs trace summary",
                    "Panel grabbed trace summary",
                    "Panel grabbing trace summary",
                    "Panel grab traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary",
                    "Ledger * trace summary",
                    "Ledger § trace summary",
                    "Ledger ¶ trace summary",
                    "Ledger ⟦panel⟧ trace summary",
                    "Ledger ﴾panel﴿ trace summary",
                    "Ledger ₺ trace summary",
                    "Panel rang trace board gate summary",
                    "Clerk rose summary trace board gate"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the bounding forms of R16-27-01 in
    # the forms the register states, the singular
    # gazetteers fused form, the plain fused form on the
    # singular anthology prefix, the variant composite
    # candidates, the breaker summarisation form in its
    # enumerated standing and the turned v summary form
    # ------------------------------------------------------

    def test_r16_27_01_bounding_forms_governed(self):
        for head in ("Gazetteerstallies", "Anthologytallies",
                     "Gateprospectustalliez",
                     "Boardthesaurustallyes",
                     "Trace summarisationeseseseseseseseses",
                     "Trace summʌrise"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured forms held as controls, subfamily (a): tally forms
    # fused behind record words no widening has named, and
    # tally forms fused behind the plurals of the record
    # words the widening of fix pass 25 named in their
    # singular forms
    # ------------------------------------------------------

    def test_control_fix26_subfamily_a_governed(self):
        for head in ("Anthologytally",
                     "Gazetteertally",
                     "Prospectustally",
                     "Thesaurustally",
                     "Tomestallies",
                     "Memoirstallies",
                     "Dispatchestallies",
                     "Treatisestallies",
                     "Monographstallies",
                     "Pamphletstallies",
                     "Bulletinstallies"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured forms held as controls, subfamily (b): composite
    # openings, a governed prefix in the opening position
    # with an unnamed record word or an unnamed plural
    # immediately before the tally form
    # ------------------------------------------------------

    def test_control_fix26_subfamily_b_governed(self):
        for head in ("Boardanthologytally",
                     "Gategazetteertally",
                     "Reviewprospectustally",
                     "Boardthesaurustally",
                     "Boardmemoirstallies"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured forms held as controls, subfamily (c): variant
    # spellings in that composite opening position, the
    # subfamily standing empty in the correctness paper
    # in this round
    # ------------------------------------------------------

    def test_control_fix26_subfamily_c_governed(self):
        for head in ("Boardanthologytallye",
                     "Gategazetteerstalliez"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured forms held as controls, subfamily (d): variant
    # spellings past the widened variant sets of forty
    # two and forty five
    # ------------------------------------------------------

    def test_control_fix26_subfamily_d_governed(self):
        for head in ("Tallyo2",
                     "Tallyu2",
                     "Tallyai2",
                     "Tallyez",
                     "Tallyaz",
                     "Tallya3",
                     "Tallyeo4",
                     "Boardtallyo2",
                     "Boardtallyu2",
                     "Boardtallyai2",
                     "Boardtallyez",
                     "Boardtallya3",
                     "Boardtallyeo4"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured forms held as controls, subfamily (e): the summary
    # word in further forms past the eighty four
    # ------------------------------------------------------

    def test_control_fix26_subfamily_e_governed(self):
        for head in ("Trace summarisereseseseseseseses",
                     "Trace summarisingeseseseseseseses",
                     "Trace summarieseseseseseseseses",
                     "Trace summarisedeseseseseseseses",
                     "Trace summariseeseseseseseseseses",
                     "Trace summaryeseseseseseseseses",
                     "Trace summarisationeseseseseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured forms held as controls, subfamily (f): fused trace
    # summary closings built on those further forms, the
    # two papers building on different members of the
    # subfamily (e) set and sharing no form, as the
    # register states in the open
    # ------------------------------------------------------

    def test_control_fix26_subfamily_f_governed(self):
        for head in ("Boardtracesummarisereseseseseseseses",
                     "Tracessummarieseseseseseseseses",
                     "Boardtracesummarisedeseseseseseseses",
                     "Tracessummaryeseseseseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured forms held as controls, subfamily (g): fused
    # closings with thirteen governed words fused between
    # the closing words
    # ------------------------------------------------------

    def test_control_fix26_subfamily_g_governed(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewtrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured forms held as controls, subfamily (h): inserted
    # word closings at sixteen words forward and fifteen
    # words reversed, in the wide form, in the middle swap
    # form of the correctness paper and in the full swap
    # form of the breaker paper
    # ------------------------------------------------------

    def test_control_fix26_subfamily_h_governed(self):
        for head in ("Trace board gate review annex panel board gate review annex panel board gate review annex panel board summary",
                     "Trace board gate review annex panel board annex gate review panel board gate review annex panel board summary",
                     "Trace board gate annex review panel board gate annex review panel board gate annex review panel board summary",
                     "Summary board gate review annex panel board gate review annex panel board gate review annex panel trace",
                     "Summary board gate review annex panel board annex gate review panel board gate review annex panel trace",
                     "Summary board gate annex review panel board gate annex review panel board gate annex review panel trace"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured forms held as controls, subfamily (i): the for step
    # closing at sixteen inserted words
    # ------------------------------------------------------

    def test_control_fix26_subfamily_i_governed(self):
        for head in ("Trace board gate review annex panel board gate review annex panel board gate review annex panel board for step 2",):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured forms held as controls, subfamily (j): further
    # stroke and hook letters in unread positions, the
    # breaker letters first and the correctness letters
    # after, no letter form of the one paper standing in
    # the other paper in this subfamily at all, as the
    # register states in the open.
    # ------------------------------------------------------

    def test_control_fix26_subfamily_j_governed(self):
        for head in ("Board ʣally",
                     "Board ʨally",
                     "Board taɽy",
                     "Board ʖally",
                     "Trace summaɹise",
                     "Trace summaɾise",
                     "Trace summarisɜ",
                     "Trace sɣmmarise",
                     "Board tʂlly",
                     "Trace sʡmmarise",
                     "Board tallʞ",
                     "Trace summarʞse",
                     "Board ʢally",
                     "Trace ʢummarise",
                     "Board taʠy",
                     "Trace summɭise",
                     "Board ɭally"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # R16-26-01 cured beside and gate ruling forms: the beside
    # forms standing present over Step 3 with Step 2 named
    # uncounted after the cure, and the gate ruling forms
    # standing governed in the ruling form
    # ------------------------------------------------------

    def test_control_fix26_beside_forms_uncounted(self):
        for head in ("Memoirstallies", "Tallyo2",
                     "Trace summarisereseseseseseseses",
                     "Anthologytally",
                     "Trace summarisedeseseseseseseses"):
            self._beside_step2_uncounted(_bad(head))

    def test_control_fix26_gate_ruling_forms_governed(self):
        for head in ("Memoirstallies", "Tallyo2",
                     "Anthologytally"):
            report = self._q4_alone(_bad(head), ruling=True)
            self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # R16-26-01 cured code level forms: the driven words under
    # the word tests, the driven heads under the head test,
    # and the seventeen defect letters under the fold
    # ------------------------------------------------------

    def test_control_fix26_code_level_forms(self):
        for word in ("anthologytally",
                     "gazetteertally",
                     "prospectustally",
                     "thesaurustally",
                     "tomestallies",
                     "memoirstallies",
                     "dispatchestallies",
                     "treatisestallies",
                     "monographstallies",
                     "pamphletstallies",
                     "bulletinstallies",
                     "boardanthologytally",
                     "gategazetteertally",
                     "reviewprospectustally",
                     "boardthesaurustally",
                     "boardmemoirstallies",
                     "boardanthologytallye",
                     "gategazetteerstalliez",
                     "tallyo2",
                     "tallyu2",
                     "tallyai2",
                     "tallyez",
                     "tallyaz",
                     "tallya3",
                     "tallyeo4",
                     "boardtallyo2",
                     "boardtallyu2",
                     "boardtallyai2",
                     "boardtallyez",
                     "boardtallya3",
                     "boardtallyeo4"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ("summarisereseseseseseseses",
                     "summarisingeseseseseseseses",
                     "summarieseseseseseseseses",
                     "summarisedeseseseseseseses",
                     "summariseeseseseseseseseses",
                     "summaryeseseseseseseseses",
                     "summarisationeseseseseseseseses"):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ("boardtracesummarisereseseseseseseses",
                     "tracessummarieseseseseseseseses",
                     "boardtracesummarisedeseseseseseseses",
                     "tracessummaryeseseseseseseseses",
                     "traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary",
                     "summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewtrace",
                     "tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary"):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        for head in ("Anthologytally",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate review annex panel board summary",
                     "Summary board gate annex review panel board "
                     "gate annex review panel board gate annex review trace",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate review "
                     "annex panel board for step 2",
                     "Trace summarisedeseseseseseseses"):
            line = head + ": items checked stand here"
            self.assertTrue(_tally_statement_head(line), head)
        self.assertEqual(_fold_word("\u02a3ally"), "tally")
        self.assertEqual(_fold_word("\u02a8ally"), "tally")
        self.assertEqual(_fold_word("ta\u027dy"), "tally")
        self.assertEqual(_fold_word("\u0296ally"), "tally")
        self.assertEqual(_fold_word("summa\u0279ise"), "summarise")
        self.assertEqual(_fold_word("summa\u027eise"), "summarise")
        self.assertEqual(_fold_word("summaris\u025c"), "summarise")
        self.assertEqual(_fold_word("s\u0263mmarise"), "summarise")
        self.assertEqual(_fold_word("t\u0282lly"), "tally")
        self.assertEqual(_fold_word("s\u02a1mmarise"), "summarise")
        self.assertEqual(_fold_word("tall\u029e"), "tally")
        self.assertEqual(_fold_word("summar\u029ese"), "summarise")
        self.assertEqual(_fold_word("\u02a2ally"), "tally")
        self.assertEqual(_fold_word("\u02a2ummarise"), "summarise")
        self.assertEqual(_fold_word("ta\u02a0y"), "tally")
        self.assertEqual(_fold_word("summ\u026dise"), "summarise")
        self.assertEqual(_fold_word("\u026dally"), "tally")

    # ------------------------------------------------------
    # Held controls: every form of R16-25-01 standing
    # governed in its cured form, as fix pass 25 left it,
    # its ten subfamily loops, its beside and gate ruling
    # forms and its code level forms
    # ------------------------------------------------------

    def test_control_fix25_subfamily_a_governed(self):
        for head in ("Bulletintally",
                     "Tometally",
                     "Memoirtally",
                     "Dispatchtally",
                     "Atlasestallies",
                     "Beaconstallies",
                     "Digeststallies",
                     "Chroniclestallies",
                     "Workgroupstallies",
                     "Appendicestallies",
                     "Treatisetally",
                     "Manualtally",
                     "Monographtally",
                     "Pamphlettally",
                     "Codexestallies",
                     "Bookletstallies"):
            self._candidate_governed(_bad(head), _read(head))


    def test_control_fix25_subfamily_b_governed(self):
        for head in ("Boardbulletintally",
                     "Gatememoirtallies",
                     "Reviewdispatchtally",
                     "Boardatlasestallies",
                     "Boardtreatisetally",
                     "Gatemanualtally",
                     "Reviewbeaconstally",
                     "Boardchroniclestally"):
            self._candidate_governed(_bad(head), _read(head))


    def test_control_fix25_subfamily_c_governed(self):
        for head in ("Boardbulletintallyed",
                     "Gatememoirtallyes",
                     "Boardtreatisetallye",
                     "Gatemanualstalliez"):
            self._candidate_governed(_bad(head), _read(head))


    def test_control_fix25_subfamily_d_governed(self):
        for head in ("Tallyo",
                     "Tallyu",
                     "Tallyai",
                     "Boardtallyo",
                     "Boardtallyu",
                     "Boardtallyai",
                     "Tallya2",
                     "Tallyeo3",
                     "Boardtallya2",
                     "Boardtallyeo3"):
            self._candidate_governed(_bad(head), _read(head))


    def test_control_fix25_subfamily_e_governed(self):
        for head in ("Trace summarisereseseseseseses",
                     "Trace summarisingeseseseseseses",
                     "Trace summarieseseseseseseses",
                     "Trace summarisedeseseseseseses",
                     "Trace summariseeseseseseseseses",
                     "Trace summaryeseseseseseseses",
                     "Trace summarisationeseseseseseseses"):
            self._candidate_governed(_bad(head), _read(head))


    def test_control_fix25_subfamily_f_governed(self):
        for head in ("Boardtracesummarisereseseseseseses",
                     "Tracessummarieseseseseseseses",
                     "Boardtracesummarisedeseseseseseses",
                     "Tracessummaryeseseseseseseses"):
            self._candidate_governed(_bad(head), _read(head))


    def test_control_fix25_subfamily_g_governed(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatetrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary"):
            self._candidate_governed(_bad(head), _read(head))


    def test_control_fix25_subfamily_h_governed(self):
        for head in ("Trace board gate review annex panel board gate review annex panel board gate review annex panel summary",
                     "Trace board gate review annex panel board annex gate review panel board gate review annex panel summary",
                     "Trace board gate annex review panel board gate annex review panel board gate annex review panel summary",
                     "Summary board gate review annex panel board gate review annex panel board gate review annex trace",
                     "Summary board gate review annex panel board annex gate review panel board gate review annex trace",
                     "Summary board gate annex review panel board gate annex review panel board gate annex review trace"):
            self._candidate_governed(_bad(head), _read(head))


    def test_control_fix25_subfamily_i_governed(self):
        for head in ("Trace board gate review annex panel board gate review annex panel board gate review annex panel for step 2",):
            self._candidate_governed(_bad(head), _read(head))


    def test_control_fix25_subfamily_j_governed(self):
        for head in ("Trace summarisʂ",
                     "Board tallʡ",
                     "Trace summariseʡ",
                     "Board ʌally",
                     "Trace ʔummarise",
                     "Board ʛally",
                     "Board ʠally",
                     "Board taɭy",
                     "Board ʞally",
                     "Trace sʛmmarise",
                     "Trace summaʞise",
                     "Trace summarisʢ",
                     "Trace ʔummarised"):
            self._candidate_governed(_bad(head), _read(head))


    def test_control_fix25_beside_forms_uncounted(self):
        for head in ("Bulletintally", "Treatisetally",
                     "Trace summarisereseseseseseses",
                     "Trace summarisedeseseseseseses"):
            self._beside_step2_uncounted(_bad(head))


    def test_control_fix25_gate_ruling_forms_governed(self):
        for head in ("Bulletintally", "Treatisetally",
                     "Trace summarisereseseseseseses"):
            report = self._q4_alone(_bad(head), ruling=True)
            self._assert_q4_governed(report, path=RULING_2)


    def test_control_fix25_code_level_forms(self):
        for word in ("bulletintally",
                     "tometally",
                     "memoirtally",
                     "dispatchtally",
                     "atlasestallies",
                     "beaconstallies",
                     "digeststallies",
                     "chroniclestallies",
                     "workgroupstallies",
                     "appendicestallies",
                     "treatisetally",
                     "manualtally",
                     "monographtally",
                     "pamphlettally",
                     "codexestallies",
                     "bookletstallies",
                     "boardbulletintally",
                     "gatememoirtallies",
                     "reviewdispatchtally",
                     "boardatlasestallies",
                     "boardtreatisetally",
                     "gatemanualtally",
                     "reviewbeaconstally",
                     "boardchroniclestally",
                     "boardbulletintallyed",
                     "gatememoirtallyes",
                     "boardtreatisetallye",
                     "gatemanualstalliez",
                     "tallyo",
                     "tallyu",
                     "tallyai",
                     "boardtallyo",
                     "boardtallyu",
                     "boardtallyai",
                     "tallya2",
                     "tallyeo3",
                     "boardtallya2",
                     "boardtallyeo3"):
            self.assertTrue(_tally_word(_fold_word(word)), word)
        for word in ("summarisereseseseseseses",
                     "summarisingeseseseseseses",
                     "summarieseseseseseseses",
                     "summarisedeseseseseseses",
                     "summariseeseseseseseseses",
                     "summaryeseseseseseseses",
                     "summarisationeseseseseseseses"):
            self.assertTrue(_summary_word(_fold_word(word)), word)
        for word in ("boardtracesummarisereseseseseseses",
                     "tracessummarieseseseseseseses",
                     "boardtracesummarisedeseseseseseses",
                     "tracessummaryeseseseseseseses",
                     "traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary",
                     "summaryboardgatereviewannexpanelboardgatereviewannexpanelboardgatetrace",
                     "tracesboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary"):
            self.assertTrue(_fused_trace_summary(
                _fold_word(word)), word)
        for head in ("Bulletintally",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate review annex panel summary",
                     "Summary board gate annex review panel board "
                     "gate annex review panel board gate annex review trace",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate review "
                     "annex panel for step 2",
                     "Trace summarisedeseseseseseses"):
            line = head + ": items checked stand here"
            self.assertTrue(_tally_statement_head(line), head)
        self.assertEqual(_fold_word("summarisʂ"), "summarise")
        self.assertEqual(_fold_word("tallʡ"), "tally")
        self.assertEqual(_fold_word("summariseʡ"), "summarised")
        self.assertEqual(_fold_word("ʌally"), "tally")
        self.assertEqual(_fold_word("ʔummarise"), "summarise")
        self.assertEqual(_fold_word("ʛally"), "tally")
        self.assertEqual(_fold_word("ʠally"), "tally")
        self.assertEqual(_fold_word("taɭy"), "tally")
        self.assertEqual(_fold_word("ʞally"), "tally")
        self.assertEqual(_fold_word("sʛmmarise"), "summarise")
        self.assertEqual(_fold_word("summaʞise"), "summarise")
        self.assertEqual(_fold_word("summarisʢ"), "summarise")
        self.assertEqual(_fold_word("ʔummarised"), "summarised")


    # ------------------------------------------------------
    # Held controls: every form of R16-25-02 standing
    # missing in its prose form, as Unit 1 of this pass
    # left it, its direct forms
    # ------------------------------------------------------

    def test_r16_25_02_held_direct_forms_missing(self):
        for run in ("Panel dance trace summary",
                    "Clerk jump summary trace",
                    "Panel climb trace summary",
                    "Team help summary trace",
                    "Panel fell trace summary",
                    "Clerk ate summary trace",
                    "Panel rode trace summary",
                    "Panel bore trace summary",
                    "Clerk won summary trace",
                    "Team dug trace summary",
                    "Panel met summary trace",
                    "Clerk rode trace summary",
                    "Team swung summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the fused forms of R16-25-02
    # standing missing in the same way
    # ------------------------------------------------------

    def test_r16_25_02_held_fused_forms_missing(self):
        for run in ("Panel dance tracesummary",
                    "Panel dance boardtracesummary",
                    "Panel dance traceboardgatesummary",
                    "Panel dance traceboardgatereviewannexpanelsummary",
                    "Panel dance traceboardgatereviewannexpanelboardsummary",
                    "Panel dance traceboardgatereviewannexpanelboardgatesummary",
                    "Panel dance traceboardgatereviewannexpanelboardgatereviewsummary",
                    "Panel dance traceboardgatereviewannexpanelboardgatereviewannexsummary",
                    "Panel dance traceboardgatereviewannexpanelboardgatereviewannexpanelboardsummary",
                    "Panel bore tracesummary",
                    "Clerk won summarytrace",
                    "Team dug boardtracesummary",
                    "Panel met traceboardgatesummary",
                    "Clerk rode traceboardgatereviewannexpanelboardgatereviewannexpanelsummary",
                    "Team swung tracesummarisedeseseseses"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the run join, aside and verb first
    # clause forms of R16-25-02 standing missing in the
    # same way
    # ------------------------------------------------------

    def test_r16_25_02_held_run_and_clause_forms_missing(self):
        for run in ("Ledger ¶ trace summary",
                    "Ledger · trace summary",
                    "Ledger ™ trace summary",
                    "Ledger ′panel′ trace summary",
                    "Ledger ″panel″ trace summary",
                    "Dance panel trace summary",
                    "Fell panel summary trace",
                    "Ledger ₹ trace summary",
                    "Ledger ₽ trace summary",
                    "Ledger ※ trace summary",
                    "Ledger ₺ trace summary",
                    "Ledger ｢panel｣ trace summary",
                    "Ledger ⟦panel⟧ trace summary",
                    "Ledger ﴾panel﴿ trace summary",
                    "Bore panel summary trace",
                    "Won ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_25_02_held_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel dance trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger ′panel′ trace summary"),
            ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel bore trace summary"), ruling=True))
        self._beside_step2_nowhere(_prose("Panel dance trace summary"))
        self._beside_step2_nowhere(
            _prose("Ledger ′panel′ trace summary"))
        self._beside_step2_nowhere(_prose("Panel bore trace summary"))

    def test_r16_25_02_held_code_level_prose_no_head(self):
        for run in ("Panel dance trace summary",
                    "Clerk jump summary trace",
                    "Panel climb trace summary",
                    "Team help summary trace",
                    "Panel fell trace summary",
                    "Clerk ate summary trace",
                    "Panel rode trace summary",
                    "Panel bore trace summary",
                    "Clerk won summary trace",
                    "Team dug trace summary",
                    "Panel met summary trace",
                    "Clerk rode trace summary",
                    "Team swung summary trace",
                    "Panel dance tracesummary",
                    "Panel dance boardtracesummary",
                    "Panel dance traceboardgatesummary",
                    "Panel dance traceboardgatereviewannexpanelsummary",
                    "Panel dance traceboardgatereviewannexpanelboardsummary",
                    "Panel dance traceboardgatereviewannexpanelboardgatesummary",
                    "Panel dance traceboardgatereviewannexpanelboardgatereviewsummary",
                    "Panel dance traceboardgatereviewannexpanelboardgatereviewannexsummary",
                    "Panel dance traceboardgatereviewannexpanelboardgatereviewannexpanelboardsummary",
                    "Panel bore tracesummary",
                    "Clerk won summarytrace",
                    "Team dug boardtracesummary",
                    "Panel met traceboardgatesummary",
                    "Clerk rode traceboardgatereviewannexpanelboardgatereviewannexpanelsummary",
                    "Team swung tracesummarisedeseseseses",
                    "Ledger ¶ trace summary",
                    "Ledger · trace summary",
                    "Ledger ™ trace summary",
                    "Ledger ′panel′ trace summary",
                    "Ledger ″panel″ trace summary",
                    "Dance panel trace summary",
                    "Fell panel summary trace",
                    "Ledger ₹ trace summary",
                    "Ledger ₽ trace summary",
                    "Ledger ※ trace summary",
                    "Ledger ₺ trace summary",
                    "Ledger ｢panel｣ trace summary",
                    "Ledger ⟦panel⟧ trace summary",
                    "Ledger ﴾panel﴿ trace summary",
                    "Bore panel summary trace",
                    "Won ledger trace summary"):
            self.assertFalse(_tally_statement_head(
                run + ": LANDED figures stand here, "
                "no counts stated"), run)

    # ------------------------------------------------------
    # Held controls: the bounding forms of R16-25-02, the
    # inserted prose tails in the verb shapes of this
    # item, the article carrying fused between forms, the
    # held join forms, the cured join forms, the read verb
    # shapes and the twelve word fused between prose
    # sentence in the fresh verb shape
    # ------------------------------------------------------

    def test_r16_25_02_held_bounding_inserted_tails_missing(self):
        for run in ("Panel bore trace board gate summary",
                    "Clerk rode summary board gate trace",
                    "Panel fled trace board gate summary",
                    "Panel sought trace board gate summary",
                    "Panel paid trace board gate summary",
                    "Panel chose trace board gate summary",
                    "Panel reviewed trace board gate summary",
                    "Panel logs trace board gate summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_25_02_held_bounding_article_and_held_joins_missing(self):
        for run in ("The panel bore "
                    "traceboardgatereviewannexpanelboardgatereviewannexpanelsummary",
                    "The panel chose "
                    "traceboardgatereviewannexpanelsummary",
                    "The panel reviewed the "
                    "traceboardgatereviewannexsummary",
                    "Ledger \\ trace summary",
                    "Ledger || trace summary",
                    "Ledger * trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_25_02_held_bounding_cured_joins_missing(self):
        for run in ("Ledger * trace summary",
                    "Ledger § trace summary",
                    "Ledger £ trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_25_02_held_bounding_read_verbs_and_inflections_missing(self):
        for run in ("Panel walk trace summary",
                    "Panel talk trace summary",
                    "Panel blew trace summary",
                    "Panel sang trace summary",
                    "Panel dances trace summary",
                    "Panel danced trace summary",
                    "Panel dancing trace summary",
                    "Panel drew trace summary",
                    "Panel told trace summary",
                    "Drew panel summary trace",
                    "Saw ledger trace summary",
                    "Kept ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_25_02_held_bounding_twelve_word_fused_between_missing(self):
        self._assert_q4_missing(self._q4_alone(_prose(
            "Panel dance "
            "traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary")))

    # ------------------------------------------------------
    # Held controls: every form of R16-24-02 standing
    # missing in its prose form, as Unit 1 of fix pass 24
    # left it, its direct forms
    # ------------------------------------------------------

    def test_r16_24_02_held_direct_forms_missing(self):
        for run in ("Panel walk trace summary",
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
                    "Team sang summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_24_02_held_fused_forms_missing(self):
        for run in ("Panel walk tracesummary",
                    "Panel walk boardtracesummary",
                    "Panel walk traceboardgatesummary",
                    "Panel walk traceboardgatereviewannexpanelsummary",
                    "Panel walk "
                    "traceboardgatereviewannexpanelboardsummary",
                    "Panel walk "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "Panel walk "
                    "traceboardgatereviewannexpanelboardgatereviewsummary",
                    "Panel walk "
                    "traceboardgatereviewannexpanelboardgatereviewannexsummary",
                    "Panel blew tracesummary",
                    "Clerk flew summarytrace",
                    "Team grew boardtracesummary",
                    "Panel knew traceboardgatesummary",
                    "Clerk threw "
                    "traceboardgatereviewannexpanelboardgatereviewpanelsummary",
                    "Team sang tracesummarisedeseseseses"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_24_02_held_run_and_clause_forms_missing(self):
        for run in ("Ledger ‘panel’ trace summary",
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
                    "Flew ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_24_02_held_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel walk trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger ‘panel’ trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel blew trace summary"), ruling=True))
        self._beside_step2_nowhere(_prose("Panel walk trace summary"))
        self._beside_step2_nowhere(_prose("Panel blew trace summary"))

    def test_r16_24_02_held_code_level_prose_no_head(self):
        for run in ("Panel walk trace summary",
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
                    "Panel walk "
                    "traceboardgatereviewannexpanelboardsummary",
                    "Panel walk "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "Panel walk "
                    "traceboardgatereviewannexpanelboardgatereviewsummary",
                    "Panel walk "
                    "traceboardgatereviewannexpanelboardgatereviewannexsummary",
                    "Panel blew tracesummary",
                    "Clerk flew summarytrace",
                    "Team grew boardtracesummary",
                    "Panel knew traceboardgatesummary",
                    "Clerk threw "
                    "traceboardgatereviewannexpanelboardgatereviewpanelsummary",
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
                    "Flew ledger trace summary"):
            self.assertFalse(_tally_statement_head(
                run + ": LANDED figures stand here, "
                "no counts stated"), run)

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
                    "Panel sought trace summary",
                    "Panel grant tracesummary",
                    "Ledger $ trace summary",
                    "Sought panel summary trace"):
            self.assertFalse(_tally_statement_head(
                run + ": LANDED figures stand here, "
                "no counts stated"), run)

    def test_r16_23_02_bounding_controls_missing(self):
        for run in ("Panel grant trace board gate summary",
                    "Panel sought trace board gate summary",
                    "Clerk taught summary board gate trace",
                    "Panel edit trace board gate summary",
                    "Panel paid trace board gate summary",
                    "Clerk brought summary board gate trace",
                    "The panel sought "
                    "traceboardgatereviewannexpanelboardgatesummary",
                    "The panel grant "
                    "traceboardgatereviewannexpanelsummary",
                    "The panel reviewed the "
                    "traceboardgatereviewannexsummary",
                    "Ledger - trace summary",
                    "Ledger (panel) trace summary",
                    "Ledger [panel] trace summary",
                    "Ledger § trace summary",
                    "Ledger 'panel' trace summary",
                    "Ledger * trace summary",
                    "Ledger @ trace summary",
                    "Ledger # trace summary",
                    "Ledger % trace summary",
                    "Ledger ^ trace summary",
                    "Ledger & trace summary",
                    "Ledger `panel` trace summary",
                    "Ledger «panel» trace summary",
                    "Reviews filing trace summary",
                    "Filing reviews trace summary",
                    "Panel grants trace summary",
                    "Panel granted trace summary",
                    "Panel granting trace summary",
                    "Panel seeks trace summary",
                    "Clerk teaches summary trace",
                    "Panel sleeps trace summary",
                    "Team wepted summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

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

    # ------------------------------------------------------
    # Held controls: the generic bounding forms of the
    # earlier passes standing missing
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
    # Held controls: the cured underreach forms of fix
    # pass 24 Unit 2 standing governed in their exact
    # forms, subfamily by subfamily
    # ------------------------------------------------------

    def test_control_fix24_subfamily_a_governed(self):
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

    def test_control_fix24_subfamily_b_governed(self):
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

    def test_control_fix24_subfamily_c_governed(self):
        for head in ("Boardatlastallyed",
                     "Gatebeacontallyes",
                     "Boardatlastallye",
                     "Gatecodexstalliez"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix24_subfamily_d_governed(self):
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

    def test_control_fix24_subfamily_e_governed(self):
        for head in ("Trace summarisereseseseseses",
                     "Trace summarisingeseseseseses",
                     "Trace summarieseseseseseses",
                     "Trace summarisedeseseseseses",
                     "Trace summariseeseseseseseses",
                     "Trace summaryeseseseseseses",
                     "Trace summarisationeseseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix24_subfamily_f_governed(self):
        for head in ("Boardtracesummarisereseseseseses",
                     "Tracessummarieseseseseseses",
                     "Boardtracesummarisedeseseseseses",
                     "Tracessummaryeseseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix24_subfamily_g_governed(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewannexpanelboardsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewannexpanelboardtrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewannexpanelboardsummary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix24_subfamily_h_governed(self):
        for head in ("Trace board gate review annex panel board gate review annex panel board gate review annex summary",
                     "Trace board gate annex review panel board gate annex review panel board gate annex review summary",
                     "Summary board gate review annex panel board gate review annex panel board gate review trace",
                     "Summary board gate annex review panel board gate annex review panel board gate annex trace",
                     "Trace board gate review annex panel board gate review annex panel board gate review board summary",
                     "Trace board gate annex review panel board gate annex review panel board gate review board summary",
                     "Summary board gate review annex panel board gate review annex panel board gate review trace",
                     "Summary board gate annex review panel board gate annex review panel board gate review trace"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix24_subfamily_i_governed(self):
        for head in ("Trace board gate review annex panel board gate review annex panel board gate review annex for step 2",
                     "Trace board gate review annex panel board gate review annex panel board gate review board for step 2"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix24_subfamily_j_governed(self):
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

    def test_control_fix24_beside_and_gate_ruling_governed(self):
        self._beside_step2_uncounted(_bad("Atlastally"))
        self._assert_q4_governed(
            self._q4_alone(_bad("Atlastally"), ruling=True),
            path=RULING_2)

    def test_held_candidate_forms_governed(self):
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
    # Held controls: the cured underreach forms of fix
    # pass 23 Unit 2 standing governed in their exact
    # forms, subfamily by subfamily
    # ------------------------------------------------------

    def test_control_fix23_subfamily_a_governed(self):
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

    def test_control_fix23_subfamily_b_governed(self):
        for head in ("Boardchesttally", "Gateshelftally",
                     "Reviewcratetally", "Boardtrunktally",
                     "Gatechesttallies", "Boardportfoliotaly",
                     "Gatealmanactally", "Reviewcompendiumtallies",
                     "Boarddocketstally", "Gatecatalogstally",
                     "Reviewfoliostallies", "Boardscrollstally"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix23_subfamily_c_governed(self):
        for head in ("Boardchesttallyed", "Gateshelftallyes",
                     "Boardportfoliotalye", "Gatedocketstalliez"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix23_subfamily_d_governed(self):
        for head in ("Tallyou", "Tallyuo", "Talleou",
                     "Boardtallyou", "Boardtallyue"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix23_subfamily_e_governed(self):
        for head in ("Trace summarisereseseseses",
                     "Trace summarisingeseseseses",
                     "Trace summarieseseseseses",
                     "Trace summarisedeseseseses",
                     "Trace summariseeseseseseses",
                     "Trace summaryeseseseseses",
                     "Trace summarisationeseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix23_subfamily_f_governed(self):
        for head in ("Boardtracesummarisereseseseses",
                     "Tracessummarieseseseseses",
                     "Boardtracesummarisedeseseseses",
                     "Tracessummaryeseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix23_subfamily_g_governed(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewannexpanelsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewannexpaneltrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewannexpanelsummary"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix23_subfamily_h_governed(self):
        for head in ("Trace board gate review annex panel board "
                     "gate review annex panel board gate review summary",
                     "Trace board gate annex review panel board "
                     "gate annex review panel board gate review summary",
                     "Summary board gate review annex panel board "
                     "gate review annex panel board gate trace",
                     "Summary board gate annex review panel board "
                     "gate annex review panel board gate trace"):
            self._candidate_governed(_bad(head), _read(head))

    def test_control_fix23_subfamily_i_governed(self):
        self._candidate_governed(
            _bad("Trace board gate review annex panel board "
                 "gate review annex panel board gate review "
                 "for step 2"),
            _read("Trace board gate review annex panel board "
                  "gate review annex panel board gate review "
                  "for step 2"))

    def test_control_fix23_subfamily_j_governed(self):
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

    def test_control_fix23_beside_forms_uncounted(self):
        for head in ("Portfoliotaly", "Chesttally",
                     "Trace summarisedeseseseses"):
            self._beside_step2_uncounted(_bad(head))

    def test_control_fix23_gate_ruling_forms_governed(self):
        for head in ("Portfoliotaly", "Chesttally",
                     "Trace summarisedeseseseses"):
            report = self._q4_alone(_bad(head), ruling=True)
            self._assert_q4_governed(report, path=RULING_2)

    # ------------------------------------------------------
    # Held controls: the cured underreach forms of fix
    # passes 22, 21, 20 and 19 standing governed in their
    # exact forms
    # ------------------------------------------------------

    def test_control_fix22_underreach_forms_governed(self):
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
                     "Notebookstallies",
                     "Boardcabinettally",
                     "Gatevaulttally",
                     "Reviewdrawertally",
                     "Boardexhibittally",
                     "Gateattachmenttally",
                     "Reviewsupplementtallies",
                     "Boardagendastally",
                     "Gatereportstally",
                     "Reviewbriefstallies",
                     "Boardprotocolstally",
                     "Boardcabinettallyed",
                     "Gatevaulttallyes",
                     "Boardagendastallye",
                     "Gatereportstalliez",
                     "Tallyeu",
                     "Tallyau",
                     "Boardtallyeu",
                     "Boardtallyau",
                     "Tallyui",
                     "Talleui",
                     "Boardtallyui",
                     "Boardtallyuo",
                     "Trace summarisereseseses",
                     "Trace summarisingeseseses",
                     "Trace summarieseseseses",
                     "Trace summarisedeseseses",
                     "Trace summariseeseseseses",
                     "Trace summaryeseseseses",
                     "Trace summarisationeseseseses",
                     "Boardtracesummarisereseseses",
                     "Tracessummarieseseseses",
                     "Boardtracesummarisedeseseses",
                     "Tracessummaryeseseseses",
                     "Traceboardgatereviewannexpanelboardgatereviewannexsummary",
                     "Summaryboardgatereviewannexpanelboardgatereviewannextrace",
                     "Tracesboardgatereviewannexpanelboardgatereviewannexsummary",
                     "Trace board gate review annex panel board gate review "
                     "annex panel board gate summary",
                     "Trace board gate annex review panel board gate annex "
                     "review panel board gate summary",
                     "Summary board gate review annex panel board gate "
                     "review annex panel board trace",
                     "Summary board gate annex review panel board gate "
                     "annex review panel board trace",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate for step 2",
                     "Trace ʍummarise",
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
    # positions, with the governed tally forms
    # ------------------------------------------------------

    def test_governed_direct_closings_governed(self):
        for head in ("Trace summary", "Summary trace",
                     "Trace summaries", "Trace summarisers",
                     "Trace summarizers", "Trace summarisings",
                     "Trace summarys",
                     "Alpha beta gamma delta epsilon trace summary",
                     "Round's trace summary"):
            self._candidate_governed(_bad(head), _read(head))
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
        for head in ("Logbooktally", "Clipboardtally",
                     "Worksheettally", "Handbooktally",
                     "Drawertallies", "Boardtallyuo",
                     "Trace summarieseses",
                     "Trace ʃummarise", "Board ʈally",
                     "Pagetallies"):
            self._candidate_governed(_bad(head), _read(head))

    def test_held_r16_25_01_standing_forms_governed(self):
        for head in ("Traceboardgatereviewannexpanelboardgatereviewannexpanelsummary",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate review summary",
                     "Trace board gate review annex panel board "
                     "gate review annex panel board gate review "
                     "annex for step 2",
                     "Trace summarisereseseseseses",
                     "Boardtracesummarisereseseseseses",
                     "Trace summaryeseseseseseses",
                     "Summary board gate review annex panel board "
                     "gate review annex panel board gate review trace",
                     "Trace summarisationeseseseseseses"):
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
    # Held controls: every form of R16-26-02 standing
    # missing in its prose form, as Unit 1 of this pass
    # left it, its direct forms
    # ------------------------------------------------------

    def test_r16_26_02_held_direct_forms_missing(self):
        for run in ("Panel lift trace summary",
                     "Panel push trace summary",
                     "Panel pull trace summary",
                     "Panel shout trace summary",
                     "Clerk lent summary trace",
                     "Panel spent trace summary",
                     "Clerk bent summary trace",
                     "Panel hid trace summary",
                     "Team shook summary trace",
                     "Clerk knelt trace summary",
                     "Panel leapt trace summary",
                     "Team dreamt summary trace",
                     "Panel came trace summary",
                     "Clerk sank summary trace",
                     "Team lent trace summary",
                     "Panel spent summary trace",
                     "Clerk led trace summary",
                     "Team heard summary trace"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the fused forms of R16-26-02
    # standing missing in the same way
    # ------------------------------------------------------

    def test_r16_26_02_held_fused_forms_missing(self):
        for run in ("Panel lift tracesummary",
                     "Panel lift boardtracesummary",
                     "Panel lift traceboardgatesummary",
                     "Panel lift traceboardgatereviewannexpanelsummary",
                     "Panel lift traceboardgatereviewannexpanelboardsummary",
                     "Panel lift traceboardgatereviewannexpanelboardgatesummary",
                     "Panel lift traceboardgatereviewannexpanelboardgatereviewsummary",
                     "Panel lift traceboardgatereviewannexpanelboardgatereviewannexsummary",
                     "Panel lift traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary",
                     "Panel shook tracesummary",
                     "Clerk lent summarytrace",
                     "Panel came tracesummary",
                     "Clerk sank summarytrace",
                     "Team lent boardtracesummary",
                     "Panel spent traceboardgatesummary",
                     "Clerk led traceboardgatereviewannexpanelboardgatereviewannexpanelsummary",
                     "Team heard tracesummarisedeseseseseseses"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the run join, aside and verb first
    # clause forms of R16-26-02 standing missing in the
    # same way
    # ------------------------------------------------------

    def test_r16_26_02_held_run_and_clause_forms_missing(self):
        for run in ("Ledger ₩ trace summary",
                     "Ledger ₴ trace summary",
                     "Ledger ₸ trace summary",
                     "Ledger ® trace summary",
                     "Ledger ‰ trace summary",
                     "Ledger ⁂ trace summary",
                     "Ledger ₦ trace summary",
                     "Ledger ｟panel｠ trace summary",
                     "Ledger ⸨panel⸩ trace summary",
                     "Ledger ⟪panel⟫ trace summary",
                     "Ledger ❨panel❩ trace summary",
                     "Ledger ⁅panel⁆ trace summary",
                     "Ledger ⌈panel⌉ trace summary",
                     "Ledger ⦈panel⦉ trace summary",
                     "Lift panel trace summary",
                     "Lent panel summary trace",
                     "Shook panel trace summary",
                     "Ledger ₿ trace summary",
                     "Ledger 【panel】 trace summary",
                     "Ledger 〚panel〛 trace summary",
                     "Ledger ‴panel‴ trace summary",
                     "Came panel summary trace",
                     "Sank ledger trace summary"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    def test_r16_26_02_held_gate_ruling_and_beside_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel lift trace summary"), ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Ledger ｟panel｠ trace summary"),
            ruling=True))
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel came trace summary"), ruling=True))
        self._beside_step2_nowhere(_prose("Panel lift trace summary"))
        self._beside_step2_nowhere(
            _prose("Ledger ｟panel｠ trace summary"))
        self._beside_step2_nowhere(_prose("Panel came trace summary"))

    def test_r16_26_02_held_code_level_prose_no_head(self):
        for run in ("Panel lift trace summary",
                     "Panel push trace summary",
                     "Panel pull trace summary",
                     "Panel shout trace summary",
                     "Clerk lent summary trace",
                     "Panel spent trace summary",
                     "Clerk bent summary trace",
                     "Panel hid trace summary",
                     "Team shook summary trace",
                     "Clerk knelt trace summary",
                     "Panel leapt trace summary",
                     "Team dreamt summary trace",
                     "Panel came trace summary",
                     "Clerk sank summary trace",
                     "Team lent trace summary",
                     "Panel spent summary trace",
                     "Clerk led trace summary",
                     "Team heard summary trace",
                     "Panel lift tracesummary",
                     "Panel lift boardtracesummary",
                     "Panel lift traceboardgatesummary",
                     "Panel lift traceboardgatereviewannexpanelsummary",
                     "Panel lift traceboardgatereviewannexpanelboardsummary",
                     "Panel lift traceboardgatereviewannexpanelboardgatesummary",
                     "Panel lift traceboardgatereviewannexpanelboardgatereviewsummary",
                     "Panel lift traceboardgatereviewannexpanelboardgatereviewannexsummary",
                     "Panel lift traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary",
                     "Panel shook tracesummary",
                     "Clerk lent summarytrace",
                     "Panel came tracesummary",
                     "Clerk sank summarytrace",
                     "Team lent boardtracesummary",
                     "Panel spent traceboardgatesummary",
                     "Clerk led traceboardgatereviewannexpanelboardgatereviewannexpanelsummary",
                     "Team heard tracesummarisedeseseseseseses",
                     "Ledger ₩ trace summary",
                     "Ledger ₴ trace summary",
                     "Ledger ₸ trace summary",
                     "Ledger ® trace summary",
                     "Ledger ‰ trace summary",
                     "Ledger ⁂ trace summary",
                     "Ledger ₦ trace summary",
                     "Ledger ｟panel｠ trace summary",
                     "Ledger ⸨panel⸩ trace summary",
                     "Ledger ⟪panel⟫ trace summary",
                     "Ledger ❨panel❩ trace summary",
                     "Ledger ⁅panel⁆ trace summary",
                     "Ledger ⌈panel⌉ trace summary",
                     "Ledger ⦈panel⦉ trace summary",
                     "Lift panel trace summary",
                     "Lent panel summary trace",
                     "Shook panel trace summary",
                     "Ledger ₿ trace summary",
                     "Ledger 【panel】 trace summary",
                     "Ledger 〚panel〛 trace summary",
                     "Ledger ‴panel‴ trace summary",
                     "Came panel summary trace",
                     "Sank ledger trace summary"):
            self.assertFalse(_tally_statement_head(
                run + ": LANDED figures stand here, "
                "no counts stated"), run)

    # ------------------------------------------------------
    # Held controls: the bounding fresh shapes of
    # R16-26-02 standing missing in the same way
    # ------------------------------------------------------

    def test_r16_26_02_held_bounding_fresh_shapes_missing(self):
        for run in ("Panel lifts trace summary",
                     "Panel lifted trace summary",
                     "Panel lifting trace summary",
                     "Panel lift traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary",
                     "Ledger * trace summary",
                     "Ledger § trace summary",
                     "Ledger ¶ trace summary",
                     "Ledger ⟦panel⟧ trace summary",
                     "Ledger ﴾panel﴿ trace summary",
                     "Ledger ₺ trace summary",
                     "Panel dance trace board gate summary",
                     "Clerk came summary trace board gate"):
            self._assert_q4_missing(self._q4_alone(_prose(run)))

    # ------------------------------------------------------
    # Held controls: the standing forms of the papers of
    # this round standing governed in their exact forms,
    # the Monographtallies control among them, distinct
    # in its letters from the defect form
    # Monographstallies
    # ------------------------------------------------------

    def test_control_fix26_standing_forms_governed(self):
        for head in ("Monographtallies",
                     "Boardhandbooktallyed", "Gateworkbooktallyes",
                     "Trace summaryeseseseseseses"):
            self._candidate_governed(_bad(head), _read(head))

    # ------------------------------------------------------
    # Held controls: the golden prose lines, the settled
    # positions and the folded records standing in their
    # exact forms
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
