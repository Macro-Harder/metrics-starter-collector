"""Step 16 fix pass 36 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-36-02 (Medium, B36-C02
and B36-B02) of Step 16 round 36. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-36-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head read what
stands before the closing words through the standing test
of fix pass 35 Unit 1 as restated, which reads a main verb
in its base form and its irregular forms only where the
word stands in the widened closed constant
_MAIN_VERB_WORDS at eight hundred and twenty seven forms,
beside the ed and ing ending test and the s ending read
in general, and reads a prose run join only in the token
shapes the earlier passes and fix pass 35 landed and a
prose aside only in the shapes those passes landed, and
a clause break only in the comma, semicolon and colon
shapes, so prose standing before a direct or fused
closing in the shapes of this round takes a tally
statement head and stands present but not derivable,
against the restated boundary of fix pass 35 Unit 1
itself in its stated terms, which states the main verb
limb in terms as any inflection of a main verb and the
join and aside limbs in terms as a prose run join or a
prose aside standing before the closing words. Three
hundred and fourteen distinct alone forms stand driven
in three subfamilies: (a) prose sentences whose closing
words stand in the direct trace summary form, forty two
forms, thirty seven of the correctness paper over the
verbs march, stumble, tumble, teeter, sway, twirl,
crouch, hop, skip, crawl, roll, bounce, wheeze, pant,
blush, yell, cheer, point, beckon, salute, curtsy,
sidestep, backtrack, wander, stroll, saunter, trudge,
plod, dash, sprint, race, chase, listen, taste, touch,
grip and hit with the Panel subject, and six of the
breaker paper over wheeze, keel, reel, stagger, totter
and teeter in their own subjects and closing orders, the
direct form over the verb wheeze in its Panel subject
shape standing shared, overlaps 1 in this subfamily; (b)
prose sentences whose last word stands in a fused trace
summary form, forty two forms, thirty seven of the
correctness paper in the plain fused form over the same
thirty seven verbs and six of the breaker paper standing
as the direct fused form, the reversed fused form, the
fused form behind a prefix, the fused between form with
two governed words fused between the closing words, the
fused between form at twenty two governed words fused
between the closing words, the count fix pass 35 Unit 2
widened to, and the fused form built on a summary form
that widening admitted, the plain fused form over the
verb wheeze standing shared, overlaps 1 in this
subfamily; and (c) prose standing before a governed
closing inside one statement, two hundred and thirty
forms, two hundred and twenty five of the correctness
paper standing as one hundred and forty four prose runs
joined by a sign token standing as its own token at
codepoints U+2A70 through U+2AFF, thirty two prose runs
joined by a combining ligature half token at codepoints
U+FE20 through U+FE2F, sixteen standing as their own
token and sixteen standing on their host letter, twelve
prose runs carrying an aside in further supplement
punctuation marks at the mark pairs U+2E30 and U+2E31,
U+2E32 and U+2E33, U+2E34 and U+2E35, U+2E36 and U+2E37,
U+2E38 and U+2E39, U+2E3A and U+2E3B, U+2E3C and U+2E3D,
U+2E40 and U+2E41, U+2E42 and U+2E43, U+2E49 and U+2E4A,
U+2E4B and U+2E4C, and U+2E4D and U+2E4E, and thirty
seven prose clauses in verb first form over the panel
subject in the base verb shapes of subfamily (a), and
eight of the breaker paper standing as one prose run
joined by a sign token at codepoint U+2A70, standing
shared with the sign forms of the correctness paper, one
prose run joined by a sign token at codepoint U+29D2,
one prose run joined by a sign token at codepoint
U+2B32, one prose run joined by a combining enclosing
sign token standing as its own token at codepoint
U+20F1, one prose run joined by a combining enclosing
sign token standing on its host letter at codepoint
U+20F2, two prose runs carrying an aside in supplement
punctuation bracket marks at codepoints U+2E49 and
U+2E4A and at codepoints U+2E4D and U+2E4E, standing
shared with the aside forms of the correctness paper,
overlaps 3 in this subfamily, and one prose clause in
verb first form over the ledger subject. Gross three
hundred and nineteen driven forms, overlaps 5, three
hundred and fourteen distinct alone forms in all. The
Panel march trace summary line of the correctness paper
stands joined by a gate ruling form and a beside form,
and the Panel wheeze trace summary line of the breaker
paper stands joined by a gate ruling form and a beside
form, each alone form standing present but not derivable
on the entering bytes, naming Step 2 and the feeder
piece. The twenty three converse assertions of the round
36 breaker exhibit stand adopted in this module: the
twenty alone forms of B36-B02 stand among the defect
tests of the subfamilies above in their driven words,
and the gate ruling assertion, the beside assertion and
the code level assertion of that exhibit stand as defect
tests here in the forms the exhibit names them. The
defect stands bounded in the open by its held controls:
the seventy one candidate verbs of the correctness paper
standing read as main verbs in the same screening drive,
snore, chuckle, giggle, stare and strike among them,
standing missing in their driven sentences; the prose
sentences of the breaker paper over the verbs smirk,
chuckle, giggle, sob, weep and moan standing missing in
their driven shapes; the sign joins at codepoints
U+2A50 through U+2A6F of the breaker paper standing in
no defect form of this round, each returning no head;
the combining signs at codepoints U+20EA through U+20F0
of that paper in their driven positions standing in no
defect form of this round; the aside pairs of that paper
at codepoints U+2E47 and U+2E48 and at U+2E5D and U+2E5E
standing in no defect form of this round; and every
governed neighbour standing at its recorded standing.
Locus: derivation_core.py, _tally_statement_head, its
direct trace summary closing limb and its fused closing
limb read through _fused_trace_summary and
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


class TestStep16Fix36Unit1(FixtureTestCase):


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
    # Defect forms of R16-36-02, subfamily (a): the
    # forty two direct prose sentences.
    # ------------------------------------------------------

    def test_r16_36_02_direct_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel march trace summary')))

    def test_r16_36_02_direct_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stumble trace summary')))

    def test_r16_36_02_direct_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tumble trace summary')))

    def test_r16_36_02_direct_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel teeter trace summary')))

    def test_r16_36_02_direct_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sway trace summary')))

    def test_r16_36_02_direct_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twirl trace summary')))

    def test_r16_36_02_direct_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel crouch trace summary')))

    def test_r16_36_02_direct_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hop trace summary')))

    def test_r16_36_02_direct_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel skip trace summary')))

    def test_r16_36_02_direct_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel crawl trace summary')))

    def test_r16_36_02_direct_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel roll trace summary')))

    def test_r16_36_02_direct_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bounce trace summary')))

    def test_r16_36_02_direct_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wheeze trace summary')))

    def test_r16_36_02_direct_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel pant trace summary')))

    def test_r16_36_02_direct_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel blush trace summary')))

    def test_r16_36_02_direct_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yell trace summary')))

    def test_r16_36_02_direct_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cheer trace summary')))

    def test_r16_36_02_direct_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel point trace summary')))

    def test_r16_36_02_direct_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel beckon trace summary')))

    def test_r16_36_02_direct_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel salute trace summary')))

    def test_r16_36_02_direct_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel curtsy trace summary')))

    def test_r16_36_02_direct_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sidestep trace summary')))

    def test_r16_36_02_direct_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel backtrack trace summary')))

    def test_r16_36_02_direct_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wander trace summary')))

    def test_r16_36_02_direct_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stroll trace summary')))

    def test_r16_36_02_direct_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel saunter trace summary')))

    def test_r16_36_02_direct_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel trudge trace summary')))

    def test_r16_36_02_direct_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel plod trace summary')))

    def test_r16_36_02_direct_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel dash trace summary')))

    def test_r16_36_02_direct_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sprint trace summary')))

    def test_r16_36_02_direct_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel race trace summary')))

    def test_r16_36_02_direct_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chase trace summary')))

    def test_r16_36_02_direct_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel listen trace summary')))

    def test_r16_36_02_direct_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel taste trace summary')))

    def test_r16_36_02_direct_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel touch trace summary')))

    def test_r16_36_02_direct_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grip trace summary')))

    def test_r16_36_02_direct_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hit trace summary')))

    def test_r16_36_02_direct_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk keel summary trace')))

    def test_r16_36_02_direct_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team reel trace summary')))

    def test_r16_36_02_direct_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stagger summary trace')))

    def test_r16_36_02_direct_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk totter trace summary')))

    def test_r16_36_02_direct_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team teeter summary trace')))


    # ------------------------------------------------------
    # Defect forms of R16-36-02, subfamily (b): the
    # forty two fused prose sentences.
    # ------------------------------------------------------

    def test_r16_36_02_fused_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel march tracesummary')))

    def test_r16_36_02_fused_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stumble tracesummary')))

    def test_r16_36_02_fused_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tumble tracesummary')))

    def test_r16_36_02_fused_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel teeter tracesummary')))

    def test_r16_36_02_fused_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sway tracesummary')))

    def test_r16_36_02_fused_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twirl tracesummary')))

    def test_r16_36_02_fused_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel crouch tracesummary')))

    def test_r16_36_02_fused_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hop tracesummary')))

    def test_r16_36_02_fused_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel skip tracesummary')))

    def test_r16_36_02_fused_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel crawl tracesummary')))

    def test_r16_36_02_fused_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel roll tracesummary')))

    def test_r16_36_02_fused_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bounce tracesummary')))

    def test_r16_36_02_fused_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wheeze tracesummary')))

    def test_r16_36_02_fused_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel pant tracesummary')))

    def test_r16_36_02_fused_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel blush tracesummary')))

    def test_r16_36_02_fused_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yell tracesummary')))

    def test_r16_36_02_fused_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cheer tracesummary')))

    def test_r16_36_02_fused_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel point tracesummary')))

    def test_r16_36_02_fused_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel beckon tracesummary')))

    def test_r16_36_02_fused_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel salute tracesummary')))

    def test_r16_36_02_fused_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel curtsy tracesummary')))

    def test_r16_36_02_fused_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sidestep tracesummary')))

    def test_r16_36_02_fused_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel backtrack tracesummary')))

    def test_r16_36_02_fused_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wander tracesummary')))

    def test_r16_36_02_fused_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stroll tracesummary')))

    def test_r16_36_02_fused_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel saunter tracesummary')))

    def test_r16_36_02_fused_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel trudge tracesummary')))

    def test_r16_36_02_fused_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel plod tracesummary')))

    def test_r16_36_02_fused_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel dash tracesummary')))

    def test_r16_36_02_fused_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sprint tracesummary')))

    def test_r16_36_02_fused_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel race tracesummary')))

    def test_r16_36_02_fused_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chase tracesummary')))

    def test_r16_36_02_fused_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel listen tracesummary')))

    def test_r16_36_02_fused_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel taste tracesummary')))

    def test_r16_36_02_fused_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel touch tracesummary')))

    def test_r16_36_02_fused_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grip tracesummary')))

    def test_r16_36_02_fused_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hit tracesummary')))

    def test_r16_36_02_fused_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk keel summarytrace')))

    def test_r16_36_02_fused_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team reel boardtracesummary')))

    def test_r16_36_02_fused_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stagger traceboardgatesummary')))

    def test_r16_36_02_fused_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk wheeze traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_r16_36_02_fused_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team keel tracesummarisationeseseseseseseseseseseseseseseseseses')))


    # ------------------------------------------------------
    # Defect forms of R16-36-02, subfamily (c): the
    # one hundred and forty four sign token join
    # forms of the correctness paper.
    # ------------------------------------------------------

    def test_r16_36_02_join_000_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a70 trace summary')))

    def test_r16_36_02_join_001_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a71 trace summary')))

    def test_r16_36_02_join_002_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a72 trace summary')))

    def test_r16_36_02_join_003_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a73 trace summary')))

    def test_r16_36_02_join_004_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a74 trace summary')))

    def test_r16_36_02_join_005_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a75 trace summary')))

    def test_r16_36_02_join_006_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a76 trace summary')))

    def test_r16_36_02_join_007_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a77 trace summary')))

    def test_r16_36_02_join_008_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a78 trace summary')))

    def test_r16_36_02_join_009_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a79 trace summary')))

    def test_r16_36_02_join_010_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a7a trace summary')))

    def test_r16_36_02_join_011_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a7b trace summary')))

    def test_r16_36_02_join_012_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a7c trace summary')))

    def test_r16_36_02_join_013_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a7d trace summary')))

    def test_r16_36_02_join_014_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a7e trace summary')))

    def test_r16_36_02_join_015_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a7f trace summary')))

    def test_r16_36_02_join_016_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a80 trace summary')))

    def test_r16_36_02_join_017_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a81 trace summary')))

    def test_r16_36_02_join_018_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a82 trace summary')))

    def test_r16_36_02_join_019_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a83 trace summary')))

    def test_r16_36_02_join_020_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a84 trace summary')))

    def test_r16_36_02_join_021_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a85 trace summary')))

    def test_r16_36_02_join_022_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a86 trace summary')))

    def test_r16_36_02_join_023_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a87 trace summary')))

    def test_r16_36_02_join_024_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a88 trace summary')))

    def test_r16_36_02_join_025_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a89 trace summary')))

    def test_r16_36_02_join_026_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a8a trace summary')))

    def test_r16_36_02_join_027_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a8b trace summary')))

    def test_r16_36_02_join_028_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a8c trace summary')))

    def test_r16_36_02_join_029_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a8d trace summary')))

    def test_r16_36_02_join_030_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a8e trace summary')))

    def test_r16_36_02_join_031_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a8f trace summary')))

    def test_r16_36_02_join_032_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a90 trace summary')))

    def test_r16_36_02_join_033_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a91 trace summary')))

    def test_r16_36_02_join_034_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a92 trace summary')))

    def test_r16_36_02_join_035_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a93 trace summary')))

    def test_r16_36_02_join_036_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a94 trace summary')))

    def test_r16_36_02_join_037_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a95 trace summary')))

    def test_r16_36_02_join_038_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a96 trace summary')))

    def test_r16_36_02_join_039_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a97 trace summary')))

    def test_r16_36_02_join_040_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a98 trace summary')))

    def test_r16_36_02_join_041_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a99 trace summary')))

    def test_r16_36_02_join_042_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a9a trace summary')))

    def test_r16_36_02_join_043_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a9b trace summary')))

    def test_r16_36_02_join_044_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a9c trace summary')))

    def test_r16_36_02_join_045_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a9d trace summary')))

    def test_r16_36_02_join_046_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a9e trace summary')))

    def test_r16_36_02_join_047_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a9f trace summary')))

    def test_r16_36_02_join_048_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aa0 trace summary')))

    def test_r16_36_02_join_049_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aa1 trace summary')))

    def test_r16_36_02_join_050_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aa2 trace summary')))

    def test_r16_36_02_join_051_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aa3 trace summary')))

    def test_r16_36_02_join_052_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aa4 trace summary')))

    def test_r16_36_02_join_053_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aa5 trace summary')))

    def test_r16_36_02_join_054_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aa6 trace summary')))

    def test_r16_36_02_join_055_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aa7 trace summary')))

    def test_r16_36_02_join_056_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aa8 trace summary')))

    def test_r16_36_02_join_057_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aa9 trace summary')))

    def test_r16_36_02_join_058_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aaa trace summary')))

    def test_r16_36_02_join_059_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aab trace summary')))

    def test_r16_36_02_join_060_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aac trace summary')))

    def test_r16_36_02_join_061_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aad trace summary')))

    def test_r16_36_02_join_062_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aae trace summary')))

    def test_r16_36_02_join_063_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aaf trace summary')))

    def test_r16_36_02_join_064_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ab0 trace summary')))

    def test_r16_36_02_join_065_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ab1 trace summary')))

    def test_r16_36_02_join_066_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ab2 trace summary')))

    def test_r16_36_02_join_067_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ab3 trace summary')))

    def test_r16_36_02_join_068_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ab4 trace summary')))

    def test_r16_36_02_join_069_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ab5 trace summary')))

    def test_r16_36_02_join_070_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ab6 trace summary')))

    def test_r16_36_02_join_071_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ab7 trace summary')))

    def test_r16_36_02_join_072_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ab8 trace summary')))

    def test_r16_36_02_join_073_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ab9 trace summary')))

    def test_r16_36_02_join_074_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aba trace summary')))

    def test_r16_36_02_join_075_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2abb trace summary')))

    def test_r16_36_02_join_076_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2abc trace summary')))

    def test_r16_36_02_join_077_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2abd trace summary')))

    def test_r16_36_02_join_078_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2abe trace summary')))

    def test_r16_36_02_join_079_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2abf trace summary')))

    def test_r16_36_02_join_080_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ac0 trace summary')))

    def test_r16_36_02_join_081_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ac1 trace summary')))

    def test_r16_36_02_join_082_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ac2 trace summary')))

    def test_r16_36_02_join_083_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ac3 trace summary')))

    def test_r16_36_02_join_084_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ac4 trace summary')))

    def test_r16_36_02_join_085_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ac5 trace summary')))

    def test_r16_36_02_join_086_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ac6 trace summary')))

    def test_r16_36_02_join_087_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ac7 trace summary')))

    def test_r16_36_02_join_088_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ac8 trace summary')))

    def test_r16_36_02_join_089_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ac9 trace summary')))

    def test_r16_36_02_join_090_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aca trace summary')))

    def test_r16_36_02_join_091_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2acb trace summary')))

    def test_r16_36_02_join_092_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2acc trace summary')))

    def test_r16_36_02_join_093_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2acd trace summary')))

    def test_r16_36_02_join_094_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ace trace summary')))

    def test_r16_36_02_join_095_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2acf trace summary')))

    def test_r16_36_02_join_096_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ad0 trace summary')))

    def test_r16_36_02_join_097_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ad1 trace summary')))

    def test_r16_36_02_join_098_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ad2 trace summary')))

    def test_r16_36_02_join_099_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ad3 trace summary')))

    def test_r16_36_02_join_100_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ad4 trace summary')))

    def test_r16_36_02_join_101_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ad5 trace summary')))

    def test_r16_36_02_join_102_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ad6 trace summary')))

    def test_r16_36_02_join_103_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ad7 trace summary')))

    def test_r16_36_02_join_104_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ad8 trace summary')))

    def test_r16_36_02_join_105_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ad9 trace summary')))

    def test_r16_36_02_join_106_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ada trace summary')))

    def test_r16_36_02_join_107_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2adb trace summary')))

    def test_r16_36_02_join_108_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2adc trace summary')))

    def test_r16_36_02_join_109_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2add trace summary')))

    def test_r16_36_02_join_110_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ade trace summary')))

    def test_r16_36_02_join_111_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2adf trace summary')))

    def test_r16_36_02_join_112_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ae0 trace summary')))

    def test_r16_36_02_join_113_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ae1 trace summary')))

    def test_r16_36_02_join_114_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ae2 trace summary')))

    def test_r16_36_02_join_115_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ae3 trace summary')))

    def test_r16_36_02_join_116_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ae4 trace summary')))

    def test_r16_36_02_join_117_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ae5 trace summary')))

    def test_r16_36_02_join_118_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ae6 trace summary')))

    def test_r16_36_02_join_119_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ae7 trace summary')))

    def test_r16_36_02_join_120_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ae8 trace summary')))

    def test_r16_36_02_join_121_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2ae9 trace summary')))

    def test_r16_36_02_join_122_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aea trace summary')))

    def test_r16_36_02_join_123_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aeb trace summary')))

    def test_r16_36_02_join_124_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aec trace summary')))

    def test_r16_36_02_join_125_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aed trace summary')))

    def test_r16_36_02_join_126_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aee trace summary')))

    def test_r16_36_02_join_127_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aef trace summary')))

    def test_r16_36_02_join_128_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2af0 trace summary')))

    def test_r16_36_02_join_129_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2af1 trace summary')))

    def test_r16_36_02_join_130_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2af2 trace summary')))

    def test_r16_36_02_join_131_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2af3 trace summary')))

    def test_r16_36_02_join_132_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2af4 trace summary')))

    def test_r16_36_02_join_133_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2af5 trace summary')))

    def test_r16_36_02_join_134_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2af6 trace summary')))

    def test_r16_36_02_join_135_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2af7 trace summary')))

    def test_r16_36_02_join_136_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2af8 trace summary')))

    def test_r16_36_02_join_137_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2af9 trace summary')))

    def test_r16_36_02_join_138_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2afa trace summary')))

    def test_r16_36_02_join_139_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2afb trace summary')))

    def test_r16_36_02_join_140_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2afc trace summary')))

    def test_r16_36_02_join_141_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2afd trace summary')))

    def test_r16_36_02_join_142_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2afe trace summary')))

    def test_r16_36_02_join_143_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2aff trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-36-02, subfamily (c): the
    # sixteen combining ligature half forms standing
    # as their own token.
    # ------------------------------------------------------

    def test_r16_36_02_join_144_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe20 trace summary')))

    def test_r16_36_02_join_145_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe21 trace summary')))

    def test_r16_36_02_join_146_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe22 trace summary')))

    def test_r16_36_02_join_147_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe23 trace summary')))

    def test_r16_36_02_join_148_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe24 trace summary')))

    def test_r16_36_02_join_149_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe25 trace summary')))

    def test_r16_36_02_join_150_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe26 trace summary')))

    def test_r16_36_02_join_151_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe27 trace summary')))

    def test_r16_36_02_join_152_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe28 trace summary')))

    def test_r16_36_02_join_153_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe29 trace summary')))

    def test_r16_36_02_join_154_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe2a trace summary')))

    def test_r16_36_02_join_155_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe2b trace summary')))

    def test_r16_36_02_join_156_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe2c trace summary')))

    def test_r16_36_02_join_157_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe2d trace summary')))

    def test_r16_36_02_join_158_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe2e trace summary')))

    def test_r16_36_02_join_159_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe2f trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-36-02, subfamily (c): the
    # sixteen combining ligature half forms standing
    # on their host letter.
    # ------------------------------------------------------

    def test_r16_36_02_join_160_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe20 trace summary')))

    def test_r16_36_02_join_161_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe21 trace summary')))

    def test_r16_36_02_join_162_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe22 trace summary')))

    def test_r16_36_02_join_163_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe23 trace summary')))

    def test_r16_36_02_join_164_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe24 trace summary')))

    def test_r16_36_02_join_165_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe25 trace summary')))

    def test_r16_36_02_join_166_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe26 trace summary')))

    def test_r16_36_02_join_167_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe27 trace summary')))

    def test_r16_36_02_join_168_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe28 trace summary')))

    def test_r16_36_02_join_169_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe29 trace summary')))

    def test_r16_36_02_join_170_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe2a trace summary')))

    def test_r16_36_02_join_171_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe2b trace summary')))

    def test_r16_36_02_join_172_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe2c trace summary')))

    def test_r16_36_02_join_173_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe2d trace summary')))

    def test_r16_36_02_join_174_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe2e trace summary')))

    def test_r16_36_02_join_175_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\ufe2f trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-36-02, subfamily (c): the
    # four further join forms of the breaker paper,
    # two sign tokens and two combining enclosing
    # sign forms in their driven constructions.
    # ------------------------------------------------------

    def test_r16_36_02_join_176_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29d2 trace summary')))

    def test_r16_36_02_join_177_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b32 trace summary')))

    def test_r16_36_02_join_178_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20f1 trace summary')))

    def test_r16_36_02_join_179_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20f2 trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-36-02, subfamily (c): the
    # twelve aside forms in further supplement
    # punctuation marks.
    # ------------------------------------------------------

    def test_r16_36_02_aside_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e30panel\u2e31 trace summary')))

    def test_r16_36_02_aside_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e32panel\u2e33 trace summary')))

    def test_r16_36_02_aside_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e34panel\u2e35 trace summary')))

    def test_r16_36_02_aside_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e36panel\u2e37 trace summary')))

    def test_r16_36_02_aside_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e38panel\u2e39 trace summary')))

    def test_r16_36_02_aside_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e3apanel\u2e3b trace summary')))

    def test_r16_36_02_aside_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e3cpanel\u2e3d trace summary')))

    def test_r16_36_02_aside_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e40panel\u2e41 trace summary')))

    def test_r16_36_02_aside_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e42panel\u2e43 trace summary')))

    def test_r16_36_02_aside_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e49panel\u2e4a trace summary')))

    def test_r16_36_02_aside_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e4bpanel\u2e4c trace summary')))

    def test_r16_36_02_aside_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e4dpanel\u2e4e trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-36-02, subfamily (c): the
    # thirty eight verb first prose clauses.
    # ------------------------------------------------------

    def test_r16_36_02_verbfirst_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('March panel trace summary')))

    def test_r16_36_02_verbfirst_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Stumble panel trace summary')))

    def test_r16_36_02_verbfirst_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Tumble panel trace summary')))

    def test_r16_36_02_verbfirst_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Teeter panel trace summary')))

    def test_r16_36_02_verbfirst_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Sway panel trace summary')))

    def test_r16_36_02_verbfirst_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Twirl panel trace summary')))

    def test_r16_36_02_verbfirst_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Crouch panel trace summary')))

    def test_r16_36_02_verbfirst_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Hop panel trace summary')))

    def test_r16_36_02_verbfirst_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Skip panel trace summary')))

    def test_r16_36_02_verbfirst_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Crawl panel trace summary')))

    def test_r16_36_02_verbfirst_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Roll panel trace summary')))

    def test_r16_36_02_verbfirst_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Bounce panel trace summary')))

    def test_r16_36_02_verbfirst_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Wheeze panel trace summary')))

    def test_r16_36_02_verbfirst_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Pant panel trace summary')))

    def test_r16_36_02_verbfirst_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Blush panel trace summary')))

    def test_r16_36_02_verbfirst_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Yell panel trace summary')))

    def test_r16_36_02_verbfirst_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Cheer panel trace summary')))

    def test_r16_36_02_verbfirst_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Point panel trace summary')))

    def test_r16_36_02_verbfirst_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Beckon panel trace summary')))

    def test_r16_36_02_verbfirst_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Salute panel trace summary')))

    def test_r16_36_02_verbfirst_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Curtsy panel trace summary')))

    def test_r16_36_02_verbfirst_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Sidestep panel trace summary')))

    def test_r16_36_02_verbfirst_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Backtrack panel trace summary')))

    def test_r16_36_02_verbfirst_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Wander panel trace summary')))

    def test_r16_36_02_verbfirst_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Stroll panel trace summary')))

    def test_r16_36_02_verbfirst_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Saunter panel trace summary')))

    def test_r16_36_02_verbfirst_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Trudge panel trace summary')))

    def test_r16_36_02_verbfirst_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Plod panel trace summary')))

    def test_r16_36_02_verbfirst_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Dash panel trace summary')))

    def test_r16_36_02_verbfirst_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Sprint panel trace summary')))

    def test_r16_36_02_verbfirst_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Race panel trace summary')))

    def test_r16_36_02_verbfirst_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Chase panel trace summary')))

    def test_r16_36_02_verbfirst_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Listen panel trace summary')))

    def test_r16_36_02_verbfirst_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Taste panel trace summary')))

    def test_r16_36_02_verbfirst_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Touch panel trace summary')))

    def test_r16_36_02_verbfirst_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Grip panel trace summary')))

    def test_r16_36_02_verbfirst_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Hit panel trace summary')))

    def test_r16_36_02_verbfirst_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Wheeze ledger trace summary')))


    # ------------------------------------------------------
    # Defect forms of R16-36-02: the gate ruling form
    # and the beside form of the first direct form of
    # the correctness paper.
    # ------------------------------------------------------

    def test_r16_36_02_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel march trace summary'), ruling=True))

    def test_r16_36_02_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            'Panel march trace summary'))


    # ------------------------------------------------------
    # Adopted assertions of the round 36 breaker exhibit:
    # the gate ruling, beside and code level assertions
    # of B36-B02, in the forms the exhibit names them.
    # ------------------------------------------------------

    def test_b36_prose_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wheeze trace summary'), ruling=True))

    def test_b36_prose_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            'Panel wheeze trace summary'))

    def test_b36_code_level_prose_no_head(self):
        for run in ("Panel wheeze trace summary",
                    "Clerk keel summary trace",
                    "Panel wheeze tracesummary",
                    'Ledger \u2a70 trace summary',
                    'Ledger \u20f1 trace summary',
                    'Ledger \u2e49panel\u2e4a trace summary',
                    "Wheeze ledger trace summary"):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)


    # ------------------------------------------------------
    # Held controls of R16-36-02, standing missing in the
    # papers of this round in the same constructions, one
    # test per held form the register names: the seventy
    # one candidate verbs of the correctness paper in the
    # direct form.
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Held controls of R16-36-02: the prose sentences of
    # the breaker paper over the verbs smirk and sob in
    # the direct form, the verbs chuckle, giggle, weep
    # and moan of that paper standing among the seventy
    # one candidate verbs above in the same form.
    # ------------------------------------------------------

    def test_control_held_71_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel smirk trace summary')))

    def test_control_held_72_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sob trace summary')))


    # ------------------------------------------------------
    # Held controls of R16-36-02: the sign joins at
    # codepoints U+2A50 through U+2A6F of the breaker
    # paper, standing as their own token.
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Held controls of R16-36-02: the combining signs
    # at codepoints U+20EA through U+20F0 of the breaker
    # paper, standing as their own token and standing
    # on their host letter.
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Held controls of R16-36-02: the aside pairs of
    # the breaker paper at codepoints U+2E47 and U+2E48
    # and at U+2E5D and U+2E5E.
    # ------------------------------------------------------

    def test_control_aside_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e47panel\u2e48 trace summary')))

    def test_control_aside_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e5dpanel\u2e5e trace summary')))


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

