"""Step 16 fix pass 35 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-35-02 (Medium, B35-C02
and B35-B02) of Step 16 round 35. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-35-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head read what
stands before the closing words through the standing test
of fix pass 34 Unit 1 as restated, which reads a main verb
in its base form and its irregular forms only where the
word stands in the widened closed constant
_MAIN_VERB_WORDS at seven hundred and sixty five forms,
beside the ed and ing ending test and the s ending read
in general, and reads a prose run join only in the token
shapes the earlier passes and fix pass 34 landed and a
prose aside only in the shapes those passes landed, and
a clause break only in the comma, semicolon and colon
shapes, so prose standing before a direct or fused
closing in the shapes of this round takes a tally
statement head and stands present but not derivable,
against the restated boundary of fix pass 34 Unit 1
itself in its stated terms, which states the main verb
limb in terms as any inflection of a main verb and the
join and aside limbs in terms as a prose run join or a
prose aside standing before the closing words. One
hundred and fifty distinct alone forms stand driven in
three subfamilies: (a) prose sentences whose closing
words stand in the direct trace summary form, thirty two
forms, twenty seven of the correctness paper over the
verbs snort, grunt, wail, bawl, sniffle, cry, howl,
shriek, squeal, beam, sulk, brood, wonder, whinny, neigh,
bellow, roar, growl, bark, purr, cluck, quack, honk,
chirp, warble, croak and buzz with the Panel subject, and
six of the breaker paper over snort, scoff, jeer, wail,
fumble and hesitate in their own subjects and closing
orders, the direct form over the verb snort in its Panel
subject shape standing shared, overlaps 1 in this
subfamily; (b) prose sentences whose last word stands in
a fused trace summary form, thirty two forms, twenty
seven of the correctness paper in the plain fused form
over the same twenty seven verbs and six of the breaker
paper standing as the direct fused form, the reversed
fused form, the fused form behind a prefix, the fused
between form with two governed words fused between the
closing words, the fused between form at twenty one
governed words fused between the closing words, the
count fix pass 34 Unit 2 widened to, and the fused form
built on a summary form that widening admitted, the plain
fused form over the verb snort standing shared, overlaps
1 in this subfamily; and (c) prose standing before a
governed closing inside one statement, eighty six forms,
eighty five of the correctness paper standing as forty
two prose runs joined by a sign token standing as its
own token at codepoints U+2A50 through U+2A6F, U+29CC
through U+29D1, U+2314, U+23E1, U+2B30 and U+2B31,
fourteen prose runs joined by a combining sign token at
codepoints U+20EA through U+20F0, seven standing as
their own token and seven standing on their host letter,
two prose runs carrying an aside in further supplement
punctuation bracket marks at the mark pairs U+2E47 and
U+2E48 and U+2E5D and U+2E5E, and twenty seven prose
clauses in verb first form over the panel subject in the
base verb shapes of subfamily (a), and eight of the
breaker paper standing as five prose runs joined by a
sign token at codepoints U+2A50, U+2A53, U+2A54, U+2314
and U+23E1, standing shared with the sign forms of the
correctness paper, one prose run joined by a combining
sign token standing as its own token at codepoint
U+20EA, standing shared in the same form, one prose run
carrying an aside in supplement punctuation bracket
marks at codepoints U+2E5D and U+2E5E, standing shared
with the second aside form of the correctness paper,
overlaps 7 in this subfamily, and one prose clause in
verb first form over the ledger subject. Gross one
hundred and fifty nine driven forms, overlaps 9, one
hundred and fifty distinct alone forms in all. The
Panel snort trace summary line of the correctness paper
stands joined by a gate ruling form and a beside form,
and the Panel snort trace summary line of the breaker
paper stands joined by a gate ruling form and a beside
form, each alone form standing present but not derivable
on the entering bytes, naming Step 2 and the feeder
piece. The twenty three converse assertions of the round
35 breaker exhibit stand adopted in this module: the
twenty alone forms of B35-B02 stand among the defect
tests of the subfamilies above in their driven words,
and the gate ruling assertion, the beside assertion and
the code level assertion of that exhibit stand as defect
tests here in the forms the exhibit names them. The
defect stands bounded in the open by its held controls:
the candidate verb of the correctness paper standing
read as a main verb in the same screening drive, hum in
its base form, standing missing in its driven sentence;
the join token forms at codepoints U+22C8, U+22CA,
U+22CB and U+22CC and at U+29C8 and U+29C9 of the
correctness paper standing missing; the candidate aside
pairs of the correctness paper standing missing, the
pairs at U+2985 and U+2986, at U+27E6 and U+27E7, at
U+FF08 and U+FF09, at U+2E15 and U+2E16 and at U+2045
and U+2046; the candidate combining token of the
correctness paper at codepoint U+20D4 standing as its
own token, standing missing in its driven run; the
combining sign joins of the breaker paper at codepoints
U+20D0 through U+20E5 in their driven positions standing
in no defect form of this round, each returning no head;
the aside pairs of the breaker paper at codepoints
U+2E57 and U+2E58 and at U+2E59 and U+2E5A standing in
no defect form of this round; and every governed
neighbour standing at its recorded standing. Locus:
derivation_core.py, _tally_statement_head, its direct
trace summary closing limb and its fused closing limb
read through _fused_trace_summary and
_before_closing_stands_as_head with the constants
_SENTENCE_FUNCTION_WORDS, _MAIN_VERB_WORDS and
_NAMING_WORDS_WITH_VERB_ENDINGS and the helper
_word_stands_as_main_verb. The cure these tests pin
restates what a direct or fused closing is in standing:
what stands before the closing words in the statement
must stand wholly as head words, naming words carrying
no sentence function word, no main verb form in any
inflection, its base form, its s form, its ed form, its
ing form or an irregular form of it, no clause break and
no prose run join or aside in any of its shapes before
the closing, so a prose sentence, prose clause or prose
run of the driven shapes takes no tally statement head
in any position, while every governed closing keeps
standing governed in every driven position.
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


class TestStep16Fix35Unit1(FixtureTestCase):


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
    # Defect forms of R16-35-02, subfamily (a): the
    # thirty two direct prose sentences.
    # ------------------------------------------------------

    def test_r16_35_02_direct_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snort trace summary')))

    def test_r16_35_02_direct_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grunt trace summary')))

    def test_r16_35_02_direct_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wail trace summary')))

    def test_r16_35_02_direct_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bawl trace summary')))

    def test_r16_35_02_direct_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sniffle trace summary')))

    def test_r16_35_02_direct_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cry trace summary')))

    def test_r16_35_02_direct_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel howl trace summary')))

    def test_r16_35_02_direct_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shriek trace summary')))

    def test_r16_35_02_direct_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel squeal trace summary')))

    def test_r16_35_02_direct_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel beam trace summary')))

    def test_r16_35_02_direct_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sulk trace summary')))

    def test_r16_35_02_direct_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel brood trace summary')))

    def test_r16_35_02_direct_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wonder trace summary')))

    def test_r16_35_02_direct_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whinny trace summary')))

    def test_r16_35_02_direct_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel neigh trace summary')))

    def test_r16_35_02_direct_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bellow trace summary')))

    def test_r16_35_02_direct_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel roar trace summary')))

    def test_r16_35_02_direct_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel growl trace summary')))

    def test_r16_35_02_direct_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bark trace summary')))

    def test_r16_35_02_direct_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel purr trace summary')))

    def test_r16_35_02_direct_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cluck trace summary')))

    def test_r16_35_02_direct_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel quack trace summary')))

    def test_r16_35_02_direct_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel honk trace summary')))

    def test_r16_35_02_direct_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chirp trace summary')))

    def test_r16_35_02_direct_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel warble trace summary')))

    def test_r16_35_02_direct_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel croak trace summary')))

    def test_r16_35_02_direct_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel buzz trace summary')))

    def test_r16_35_02_direct_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk scoff summary trace')))

    def test_r16_35_02_direct_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team jeer trace summary')))

    def test_r16_35_02_direct_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wail summary trace')))

    def test_r16_35_02_direct_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk fumble trace summary')))

    def test_r16_35_02_direct_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team hesitate summary trace')))


    # ------------------------------------------------------
    # Defect forms of R16-35-02, subfamily (b): the
    # thirty two fused prose sentences.
    # ------------------------------------------------------

    def test_r16_35_02_fused_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snort tracesummary')))

    def test_r16_35_02_fused_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grunt tracesummary')))

    def test_r16_35_02_fused_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wail tracesummary')))

    def test_r16_35_02_fused_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bawl tracesummary')))

    def test_r16_35_02_fused_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sniffle tracesummary')))

    def test_r16_35_02_fused_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cry tracesummary')))

    def test_r16_35_02_fused_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel howl tracesummary')))

    def test_r16_35_02_fused_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shriek tracesummary')))

    def test_r16_35_02_fused_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel squeal tracesummary')))

    def test_r16_35_02_fused_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel beam tracesummary')))

    def test_r16_35_02_fused_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sulk tracesummary')))

    def test_r16_35_02_fused_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel brood tracesummary')))

    def test_r16_35_02_fused_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wonder tracesummary')))

    def test_r16_35_02_fused_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whinny tracesummary')))

    def test_r16_35_02_fused_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel neigh tracesummary')))

    def test_r16_35_02_fused_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bellow tracesummary')))

    def test_r16_35_02_fused_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel roar tracesummary')))

    def test_r16_35_02_fused_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel growl tracesummary')))

    def test_r16_35_02_fused_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bark tracesummary')))

    def test_r16_35_02_fused_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel purr tracesummary')))

    def test_r16_35_02_fused_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cluck tracesummary')))

    def test_r16_35_02_fused_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel quack tracesummary')))

    def test_r16_35_02_fused_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel honk tracesummary')))

    def test_r16_35_02_fused_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chirp tracesummary')))

    def test_r16_35_02_fused_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel warble tracesummary')))

    def test_r16_35_02_fused_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel croak tracesummary')))

    def test_r16_35_02_fused_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel buzz tracesummary')))

    def test_r16_35_02_fused_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk scoff summarytrace')))

    def test_r16_35_02_fused_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team jeer boardtracesummary')))

    def test_r16_35_02_fused_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wail traceboardgatesummary')))

    def test_r16_35_02_fused_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk snort traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary')))

    def test_r16_35_02_fused_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team scoff tracesummarisationeseseseseseseseseseseseseseseseses')))


    # ------------------------------------------------------
    # Defect forms of R16-35-02, subfamily (c): the
    # forty two sign token join forms of the
    # correctness paper.
    # ------------------------------------------------------

    def test_r16_35_02_join_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a50 trace summary')))

    def test_r16_35_02_join_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a51 trace summary')))

    def test_r16_35_02_join_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a52 trace summary')))

    def test_r16_35_02_join_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a53 trace summary')))

    def test_r16_35_02_join_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a54 trace summary')))

    def test_r16_35_02_join_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a55 trace summary')))

    def test_r16_35_02_join_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a56 trace summary')))

    def test_r16_35_02_join_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a57 trace summary')))

    def test_r16_35_02_join_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a58 trace summary')))

    def test_r16_35_02_join_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a59 trace summary')))

    def test_r16_35_02_join_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a5a trace summary')))

    def test_r16_35_02_join_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a5b trace summary')))

    def test_r16_35_02_join_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a5c trace summary')))

    def test_r16_35_02_join_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a5d trace summary')))

    def test_r16_35_02_join_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a5e trace summary')))

    def test_r16_35_02_join_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a5f trace summary')))

    def test_r16_35_02_join_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a60 trace summary')))

    def test_r16_35_02_join_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a61 trace summary')))

    def test_r16_35_02_join_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a62 trace summary')))

    def test_r16_35_02_join_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a63 trace summary')))

    def test_r16_35_02_join_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a64 trace summary')))

    def test_r16_35_02_join_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a65 trace summary')))

    def test_r16_35_02_join_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a66 trace summary')))

    def test_r16_35_02_join_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a67 trace summary')))

    def test_r16_35_02_join_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a68 trace summary')))

    def test_r16_35_02_join_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a69 trace summary')))

    def test_r16_35_02_join_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a6a trace summary')))

    def test_r16_35_02_join_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a6b trace summary')))

    def test_r16_35_02_join_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a6c trace summary')))

    def test_r16_35_02_join_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a6d trace summary')))

    def test_r16_35_02_join_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a6e trace summary')))

    def test_r16_35_02_join_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a6f trace summary')))

    def test_r16_35_02_join_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29cc trace summary')))

    def test_r16_35_02_join_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29cd trace summary')))

    def test_r16_35_02_join_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29ce trace summary')))

    def test_r16_35_02_join_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29cf trace summary')))

    def test_r16_35_02_join_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29d0 trace summary')))

    def test_r16_35_02_join_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29d1 trace summary')))

    def test_r16_35_02_join_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2314 trace summary')))

    def test_r16_35_02_join_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u23e1 trace summary')))

    def test_r16_35_02_join_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b30 trace summary')))

    def test_r16_35_02_join_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b31 trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-35-02, subfamily (c): the
    # seven combining sign forms standing as their
    # own token.
    # ------------------------------------------------------

    def test_r16_35_02_join_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20ea trace summary')))

    def test_r16_35_02_join_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20eb trace summary')))

    def test_r16_35_02_join_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20ec trace summary')))

    def test_r16_35_02_join_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20ed trace summary')))

    def test_r16_35_02_join_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20ee trace summary')))

    def test_r16_35_02_join_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20ef trace summary')))

    def test_r16_35_02_join_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20f0 trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-35-02, subfamily (c): the
    # seven combining sign forms standing on their
    # host letter.
    # ------------------------------------------------------

    def test_r16_35_02_join_49_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20ea trace summary')))

    def test_r16_35_02_join_50_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20eb trace summary')))

    def test_r16_35_02_join_51_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20ec trace summary')))

    def test_r16_35_02_join_52_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20ed trace summary')))

    def test_r16_35_02_join_53_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20ee trace summary')))

    def test_r16_35_02_join_54_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20ef trace summary')))

    def test_r16_35_02_join_55_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20f0 trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-35-02, subfamily (c): the
    # two aside forms in further supplement
    # punctuation bracket marks.
    # ------------------------------------------------------

    def test_r16_35_02_aside_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e47panel\u2e48 trace summary')))

    def test_r16_35_02_aside_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e5dpanel\u2e5e trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-35-02, subfamily (c): the
    # twenty eight verb first prose clauses.
    # ------------------------------------------------------

    def test_r16_35_02_verbfirst_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Snort panel trace summary')))

    def test_r16_35_02_verbfirst_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Grunt panel trace summary')))

    def test_r16_35_02_verbfirst_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Wail panel trace summary')))

    def test_r16_35_02_verbfirst_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Bawl panel trace summary')))

    def test_r16_35_02_verbfirst_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Sniffle panel trace summary')))

    def test_r16_35_02_verbfirst_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Cry panel trace summary')))

    def test_r16_35_02_verbfirst_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Howl panel trace summary')))

    def test_r16_35_02_verbfirst_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Shriek panel trace summary')))

    def test_r16_35_02_verbfirst_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Squeal panel trace summary')))

    def test_r16_35_02_verbfirst_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Beam panel trace summary')))

    def test_r16_35_02_verbfirst_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Sulk panel trace summary')))

    def test_r16_35_02_verbfirst_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Brood panel trace summary')))

    def test_r16_35_02_verbfirst_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Wonder panel trace summary')))

    def test_r16_35_02_verbfirst_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Whinny panel trace summary')))

    def test_r16_35_02_verbfirst_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Neigh panel trace summary')))

    def test_r16_35_02_verbfirst_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Bellow panel trace summary')))

    def test_r16_35_02_verbfirst_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Roar panel trace summary')))

    def test_r16_35_02_verbfirst_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Growl panel trace summary')))

    def test_r16_35_02_verbfirst_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Bark panel trace summary')))

    def test_r16_35_02_verbfirst_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Purr panel trace summary')))

    def test_r16_35_02_verbfirst_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Cluck panel trace summary')))

    def test_r16_35_02_verbfirst_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Quack panel trace summary')))

    def test_r16_35_02_verbfirst_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Honk panel trace summary')))

    def test_r16_35_02_verbfirst_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Chirp panel trace summary')))

    def test_r16_35_02_verbfirst_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Warble panel trace summary')))

    def test_r16_35_02_verbfirst_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Croak panel trace summary')))

    def test_r16_35_02_verbfirst_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Buzz panel trace summary')))

    def test_r16_35_02_verbfirst_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Snort ledger trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-35-02: the gate ruling form
    # and the beside form of the first direct form of
    # the correctness paper.
    # ------------------------------------------------------

    def test_r16_35_02_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snort trace summary'), ruling=True))

    def test_r16_35_02_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            'Panel snort trace summary'))


    # ------------------------------------------------------
    # Adopted assertions of the round 35 breaker exhibit:
    # the gate ruling, beside and code level assertions
    # of B35-B02, in the forms the exhibit names them.
    # ------------------------------------------------------

    def test_b35_prose_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snort trace summary'), ruling=True))

    def test_b35_prose_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            'Panel snort trace summary'))

    def test_b35_code_level_prose_no_head(self):
        for run in ('Panel snort trace summary',
                    'Clerk scoff summary trace',
                    'Panel snort tracesummary',
                    'Ledger \u2a50 trace summary',
                    'Ledger \u20ea trace summary',
                    'Ledger \u2e5dpanel\u2e5e trace summary',
                    'Snort ledger trace summary'):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)


    # ------------------------------------------------------
    # Held controls of R16-35-02, standing missing in the
    # papers of this round in the same constructions, one
    # test per held form the register names.
    # ------------------------------------------------------

    def test_control_held_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hum trace summary')))

    def test_control_held_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22c8 trace summary')))

    def test_control_held_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22ca trace summary')))

    def test_control_held_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22cb trace summary')))

    def test_control_held_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22cc trace summary')))

    def test_control_held_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29c8 trace summary')))

    def test_control_held_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29c9 trace summary')))

    def test_control_held_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2985panel\u2986 trace summary')))

    def test_control_held_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u27e6panel\u27e7 trace summary')))

    def test_control_held_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \uff08panel\uff09 trace summary')))

    def test_control_held_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e15panel\u2e16 trace summary')))

    def test_control_held_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2045panel\u2046 trace summary')))

    def test_control_held_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d4 trace summary')))

    def test_control_held_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d0 trace summary')))

    def test_control_held_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d1 trace summary')))

    def test_control_held_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d2 trace summary')))

    def test_control_held_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d3 trace summary')))

    def test_control_held_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d4 trace summary')))

    def test_control_held_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d5 trace summary')))

    def test_control_held_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d6 trace summary')))

    def test_control_held_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d7 trace summary')))

    def test_control_held_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d8 trace summary')))

    def test_control_held_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d9 trace summary')))

    def test_control_held_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20da trace summary')))

    def test_control_held_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20db trace summary')))

    def test_control_held_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20dc trace summary')))

    def test_control_held_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20dd trace summary')))

    def test_control_held_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20de trace summary')))

    def test_control_held_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20df trace summary')))

    def test_control_held_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e0 trace summary')))

    def test_control_held_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e1 trace summary')))

    def test_control_held_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e2 trace summary')))

    def test_control_held_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e3 trace summary')))

    def test_control_held_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e4 trace summary')))

    def test_control_held_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e5 trace summary')))

    def test_control_held_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e57panel\u2e58 trace summary')))

    def test_control_held_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e59panel\u2e5a trace summary')))


    # ------------------------------------------------------
    # Held governed controls: the governed closings of
    # the papers of this round, standing governed beside
    # their counted siblings, one test per held form.
    # ------------------------------------------------------

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

