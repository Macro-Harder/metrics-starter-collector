"""Step 16 fix pass 33 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-33-02 (Medium, B33-C02
and B33-B02) of Step 16 round 33. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-33-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head read what
stands before the closing words through the standing test
of fix pass 32 Unit 1 as restated, which reads a main verb
in its base form and its irregular forms only where the
word stands in the widened closed constant
_MAIN_VERB_WORDS, beside the ed and ing ending test and
the s ending read in general, and reads a prose run join
only in the token shapes the earlier passes and fix pass
32 landed and a prose aside only in the shapes those
passes landed, and a clause break only in the comma,
semicolon and colon shapes, so prose standing before a
direct or fused closing in the shapes of this round takes
a tally statement head and stands present but not
derivable, against the restated boundary of fix pass 32
itself in its stated terms, which states the main verb
limb in terms as any inflection of a main verb and the
join and aside limbs in terms as a prose run join or a
prose aside standing before the closing words. Sixty
five distinct alone forms stand driven in three
subfamilies: (a) prose sentences whose closing words
stand in the direct trace summary form, nine forms, each
carrying a bare noun subject and a main verb standing
before the closing words in a base form the widened
constant does not name, over the verbs smirk, laugh and
stretch of the correctness paper and pout, mumble,
stammer, quiver, hobble and limp of the breaker paper;
(b) prose sentences whose last word stands in a fused
trace summary form, nine forms in the same verb shapes,
three of the correctness paper in its plain and reversed
plain fused forms and six of the breaker paper standing
as the direct fused form, the reversed fused form, the
fused form behind a prefix, the fused between form with
two governed words fused between the closing words, the
fused between form at nineteen governed words fused
between the closing words, the count fix pass 32 Unit 2
widened to, and the fused form built on a summary form
that widening admitted; and (c) prose standing before a
governed closing inside one statement, forty seven
forms, thirty six prose runs joined by a bowtie like,
n-ary summation like, arc, diameter, electric arrow, APL
like, ground or circled cross like sign token of the
correctness paper, six prose runs joined by a combining
left right arrow above, combining right arrow above,
combining three dots above, combining enclosing circle,
combining enclosing square or combining enclosing
diamond sign token of the breaker paper, one prose run
carrying an aside in supplement punctuation bracket
marks, and four verb first prose clauses in the same
verb shapes, over smirk, laugh and stretch of the
correctness paper and pout of the breaker paper. The
aside form stands pinned in the driven form of the
breaker exhibit, at codepoints U+2E55 and U+2E56, as the
scope settling of the unit report records in the open:
the quoted marks of the two papers and of the register
stand at codepoints U+2E15 and U+2E16 against the prose
naming of those papers at U+2E55 and U+2E56, and the
driven form governs this pinning. The two papers lists
stand disjoint in every subfamily, overlaps 0, as the
register disposition states. The Panel smirk trace
summary line of the correctness paper stands joined by
a gate ruling form and a beside form, and the Panel pout
trace summary line of the breaker paper stands joined
by a gate ruling form and a beside form, each alone form
standing present but not derivable on the entering
bytes, naming Step 2 and the feeder piece. The twenty
three converse assertions of the round 33 breaker
exhibit stand adopted in this module: the twenty alone
forms of B33-B02 stand among the defect tests of the
subfamilies above in their driven words, and the gate
ruling assertion, the beside assertion and the code
level assertion of that exhibit stand as defect tests
here in the forms the exhibit names them. The defect
stands bounded in the open by its held controls: the
fifty candidate verbs of the correctness paper standing
read as main verbs in the same screening drive, sigh,
blink, wink, shrug, cough, sneeze, stare, gaze, frown,
nod, hum, sob, weep, chuckle, giggle, snore, yawn,
kneel, bow, wave, clap, chew, sip, gulp and doze in
their base forms and sang, swam, froze, chose, spoke,
woke, wore, tore, hid, bit, fled, bled, fed, led, sped,
shone, shook, stole, broke, drove, rode, wrote, rose
and fell in their irregular forms, each standing
missing in its driven sentence; the candidate verbs of
the breaker paper, sigh, sob, blink, wink, cough,
stare, glare, grin, frown, shrug, sneeze, whisper,
murmur, tremble, shiver and wobble in their base forms
and froze, broke, spoke, woke, stole, shook, sang,
sank, swam, rang, wove, tore and wore in their irregular
forms, standing read as main verbs in their driven
sentences; the join token forms at codepoints U+22C8,
U+22CA, U+22CB and U+22CC of the correctness paper
standing missing; the six candidate aside shapes of the
correctness paper standing missing, the mathematical
double bracket shape, the curly bracket like shape, the
angle quotation like shape, the bracket like shape, the
angle bracket shape of R16-32-02 standing cured, and
the double angle bracket shape; the combining sign
token forms at codepoints U+20D1, U+20D6, U+20D7,
U+20DB, U+20E1 and U+20E5 of the breaker paper standing
missing, each standing read as a join by the standing
test in its landed form, beside the forms at U+20D0,
U+20D2 and U+20E2 standing missing at this standing
under the cure of fix pass 32; the candidate aside pairs
of the breaker paper standing read as asides in their
probed forms; the held join forms of the breaker paper,
the double backslash token form, the double pipe token
form and the asterisk token form, standing missing in
their recorded forms; the inserted prose tails of the
breaker paper standing missing in the verb shapes of
the earlier rounds as that paper records them; the
article carrying fused between forms of the breaker
paper standing missing in their recorded forms; and
every governed neighbour standing at its recorded
standing. Locus: derivation_core.py,
_tally_statement_head, its direct trace summary closing
limb and its fused closing limb read through
_fused_trace_summary and _before_closing_stands_as_head
with the constants _SENTENCE_FUNCTION_WORDS,
_MAIN_VERB_WORDS and _NAMING_WORDS_WITH_VERB_ENDINGS and
the helper _word_stands_as_main_verb. The cure these
tests pin restates what a direct or fused closing is in
standing: what stands before the closing words in the
statement must stand wholly as head words, naming words
carrying no sentence function word, no main verb form in
any inflection, its base form, its s form, its ed form,
its ing form or an irregular form of it, no clause break
and no prose run join or aside in any of its shapes
before the closing, so a prose sentence, prose clause or
prose run of the driven shapes takes no tally statement
head in any position, while every governed closing keeps
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


class TestStep16Fix33Unit1(FixtureTestCase):


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
    # Defect forms of R16-33-02, subfamily (a): the
    # nine direct prose sentences.
    # ------------------------------------------------------

    def test_r16_33_02_direct_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel smirk trace summary')))

    def test_r16_33_02_direct_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk laugh summary trace')))

    def test_r16_33_02_direct_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stretch trace summary')))

    def test_r16_33_02_direct_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel pout trace summary')))

    def test_r16_33_02_direct_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk mumble summary trace')))

    def test_r16_33_02_direct_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stammer trace summary')))

    def test_r16_33_02_direct_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel quiver summary trace')))

    def test_r16_33_02_direct_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk hobble trace summary')))

    def test_r16_33_02_direct_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team limp summary trace')))

    # ------------------------------------------------------
    # Defect forms of R16-33-02, subfamily (b): the
    # nine fused prose sentences.
    # ------------------------------------------------------

    def test_r16_33_02_fused_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel smirk tracesummary')))

    def test_r16_33_02_fused_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk laugh summarytrace')))

    def test_r16_33_02_fused_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stretch tracesummary')))

    def test_r16_33_02_fused_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel pout tracesummary')))

    def test_r16_33_02_fused_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk mumble summarytrace')))

    def test_r16_33_02_fused_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stammer boardtracesummary')))

    def test_r16_33_02_fused_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel quiver traceboardgatesummary')))

    def test_r16_33_02_fused_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk pout traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_r16_33_02_fused_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team mumble tracesummarisationeseseseseseseseseseseseseseses')))

    # ------------------------------------------------------
    # Defect forms of R16-33-02, subfamily (c): the
    # thirty six join forms of the correctness paper.
    # ------------------------------------------------------

    def test_r16_33_02_join_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋉ trace summary')))

    def test_r16_33_02_join_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨝ trace summary')))

    def test_r16_33_02_join_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨞ trace summary')))

    def test_r16_33_02_join_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨟ trace summary')))

    def test_r16_33_02_join_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨠ trace summary')))

    def test_r16_33_02_join_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨡ trace summary')))

    def test_r16_33_02_join_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨢ trace summary')))

    def test_r16_33_02_join_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨣ trace summary')))

    def test_r16_33_02_join_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨤ trace summary')))

    def test_r16_33_02_join_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨥ trace summary')))

    def test_r16_33_02_join_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨦ trace summary')))

    def test_r16_33_02_join_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨧ trace summary')))

    def test_r16_33_02_join_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨨ trace summary')))

    def test_r16_33_02_join_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨩ trace summary')))

    def test_r16_33_02_join_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨪ trace summary')))

    def test_r16_33_02_join_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨫ trace summary')))

    def test_r16_33_02_join_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨬ trace summary')))

    def test_r16_33_02_join_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨭ trace summary')))

    def test_r16_33_02_join_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨮ trace summary')))

    def test_r16_33_02_join_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨯ trace summary')))

    def test_r16_33_02_join_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨰ trace summary')))

    def test_r16_33_02_join_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨱ trace summary')))

    def test_r16_33_02_join_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨲ trace summary')))

    def test_r16_33_02_join_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨳ trace summary')))

    def test_r16_33_02_join_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨴ trace summary')))

    def test_r16_33_02_join_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨵ trace summary')))

    def test_r16_33_02_join_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌒ trace summary')))

    def test_r16_33_02_join_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌀ trace summary')))

    def test_r16_33_02_join_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌁ trace summary')))

    def test_r16_33_02_join_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⍟ trace summary')))

    def test_r16_33_02_join_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⎕ trace summary')))

    def test_r16_33_02_join_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⏚ trace summary')))

    def test_r16_33_02_join_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧀ trace summary')))

    def test_r16_33_02_join_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧁ trace summary')))

    def test_r16_33_02_join_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧂ trace summary')))

    def test_r16_33_02_join_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧃ trace summary')))

    # ------------------------------------------------------
    # Defect forms of R16-33-02, subfamily (c): the
    # six combining join forms of the breaker paper.
    # ------------------------------------------------------

    def test_r16_33_02_join_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d4 trace summary')))

    def test_r16_33_02_join_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d5 trace summary')))

    def test_r16_33_02_join_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20dc trace summary')))

    def test_r16_33_02_join_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20dd trace summary')))

    def test_r16_33_02_join_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20de trace summary')))

    def test_r16_33_02_join_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20df trace summary')))

    # ------------------------------------------------------
    # Defect forms of R16-33-02, subfamily (c): the
    # one aside form, in its driven form at
    # codepoints U+2E55 and U+2E56.
    # ------------------------------------------------------

    def test_r16_33_02_aside_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e55panel\u2e56 trace summary')))

    # ------------------------------------------------------
    # Defect forms of R16-33-02, subfamily (c): the
    # four verb first prose clauses.
    # ------------------------------------------------------

    def test_r16_33_02_verbfirst_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Smirk panel trace summary')))

    def test_r16_33_02_verbfirst_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Laugh panel summary trace')))

    def test_r16_33_02_verbfirst_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Stretch panel trace summary')))

    def test_r16_33_02_verbfirst_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Pout ledger trace summary')))

    # ------------------------------------------------------
    # Defect forms of R16-33-02: the gate ruling form
    # and the beside form of the first direct form of
    # the correctness paper.
    # ------------------------------------------------------

    def test_r16_33_02_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel smirk trace summary'), ruling=True))

    def test_r16_33_02_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            'Panel smirk trace summary'))

    # ------------------------------------------------------
    # Adopted assertions of the round 33 breaker exhibit:
    # the gate ruling, beside and code level assertions
    # of B33-B02, in the forms the exhibit names them.
    # ------------------------------------------------------

    def test_b33_prose_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel pout trace summary"), ruling=True))

    def test_b33_prose_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            "Panel pout trace summary"))

    def test_b33_code_level_prose_no_head(self):
        for run in ("Panel pout trace summary",
                    "Clerk mumble summary trace",
                    "Panel pout tracesummary",
                    'Clerk pout traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary',
                    "Ledger \u20d4 trace summary",
                    "Ledger \u20dc trace summary",
                    "Ledger \u2e55panel\u2e56 trace summary",
                    "Pout ledger trace summary"):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)

    # ------------------------------------------------------
    # Held controls of R16-33-02, standing missing in the
    # papers of this round in the same constructions, one
    # test per held form the register names.
    # ------------------------------------------------------

    def test_control_held_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sigh trace summary')))

    def test_control_held_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel blink trace summary')))

    def test_control_held_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wink trace summary')))

    def test_control_held_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace summary')))

    def test_control_held_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cough trace summary')))

    def test_control_held_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sneeze trace summary')))

    def test_control_held_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stare trace summary')))

    def test_control_held_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gaze trace summary')))

    def test_control_held_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel frown trace summary')))

    def test_control_held_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace summary')))

    def test_control_held_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hum trace summary')))

    def test_control_held_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sob trace summary')))

    def test_control_held_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel weep trace summary')))

    def test_control_held_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chuckle trace summary')))

    def test_control_held_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel giggle trace summary')))

    def test_control_held_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snore trace summary')))

    def test_control_held_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yawn trace summary')))

    def test_control_held_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel kneel trace summary')))

    def test_control_held_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bow trace summary')))

    def test_control_held_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wave trace summary')))

    def test_control_held_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap trace summary')))

    def test_control_held_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew trace summary')))

    def test_control_held_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sip trace summary')))

    def test_control_held_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp trace summary')))

    def test_control_held_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel doze trace summary')))

    def test_control_held_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sang trace summary')))

    def test_control_held_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel swam trace summary')))

    def test_control_held_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel froze trace summary')))

    def test_control_held_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chose trace summary')))

    def test_control_held_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel spoke trace summary')))

    def test_control_held_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel woke trace summary')))

    def test_control_held_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wore trace summary')))

    def test_control_held_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tore trace summary')))

    def test_control_held_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hid trace summary')))

    def test_control_held_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bit trace summary')))

    def test_control_held_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fled trace summary')))

    def test_control_held_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bled trace summary')))

    def test_control_held_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fed trace summary')))

    def test_control_held_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel led trace summary')))

    def test_control_held_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sped trace summary')))

    def test_control_held_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shone trace summary')))

    def test_control_held_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shook trace summary')))

    def test_control_held_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stole trace summary')))

    def test_control_held_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel broke trace summary')))

    def test_control_held_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel drove trace summary')))

    def test_control_held_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel rode trace summary')))

    def test_control_held_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wrote trace summary')))

    def test_control_held_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel rose trace summary')))

    def test_control_held_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fell trace summary')))

    def test_control_held_49_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sigh trace summary')))

    def test_control_held_50_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk sob summary trace')))

    def test_control_held_51_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team blink trace summary')))

    def test_control_held_52_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wink trace summary')))

    def test_control_held_53_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cough trace summary')))

    def test_control_held_54_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stare trace summary')))

    def test_control_held_55_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glare trace summary')))

    def test_control_held_56_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grin trace summary')))

    def test_control_held_57_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel frown trace summary')))

    def test_control_held_58_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace summary')))

    def test_control_held_59_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sneeze trace summary')))

    def test_control_held_60_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whisper trace summary')))

    def test_control_held_61_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel murmur trace summary')))

    def test_control_held_62_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tremble trace summary')))

    def test_control_held_63_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shiver trace summary')))

    def test_control_held_64_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wobble trace summary')))

    def test_control_held_65_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel froze trace summary')))

    def test_control_held_66_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel broke trace summary')))

    def test_control_held_67_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel spoke trace summary')))

    def test_control_held_68_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel woke trace summary')))

    def test_control_held_69_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stole trace summary')))

    def test_control_held_70_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shook trace summary')))

    def test_control_held_71_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sang trace summary')))

    def test_control_held_72_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sank trace summary')))

    def test_control_held_73_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel swam trace summary')))

    def test_control_held_74_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel rang trace summary')))

    def test_control_held_75_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wove trace summary')))

    def test_control_held_76_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tore trace summary')))

    def test_control_held_77_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wore trace summary')))

    def test_control_held_78_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22c8 trace summary')))

    def test_control_held_79_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22ca trace summary')))

    def test_control_held_80_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22cb trace summary')))

    def test_control_held_81_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22cc trace summary')))

    def test_control_held_82_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u27e6panel\u27e7 trace summary')))

    def test_control_held_83_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2774panel\u2775 trace summary')))

    def test_control_held_84_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2039panel\u203a trace summary')))

    def test_control_held_85_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u298bpanel\u298c trace summary')))

    def test_control_held_86_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u27e8panel\u27e9 trace summary')))

    def test_control_held_87_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u300apanel\u300b trace summary')))

    def test_control_held_88_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d1 trace summary')))

    def test_control_held_89_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d6 trace summary')))

    def test_control_held_90_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d7 trace summary')))

    def test_control_held_91_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20db trace summary')))

    def test_control_held_92_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e1 trace summary')))

    def test_control_held_93_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e5 trace summary')))

    def test_control_held_94_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d0 trace summary')))

    def test_control_held_95_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d2 trace summary')))

    def test_control_held_96_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e2 trace summary')))

    def test_control_held_97_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2768panel\u2769 trace summary')))

    def test_control_held_98_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u276apanel\u276b trace summary')))

    def test_control_held_99_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u276cpanel\u276d trace summary')))

    def test_control_held_100_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u276epanel\u276f trace summary')))

    def test_control_held_101_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2770panel\u2771 trace summary')))

    def test_control_held_102_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2774panel\u2775 trace summary')))

    def test_control_held_103_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2987panel\u2988 trace summary')))

    def test_control_held_104_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2989panel\u298a trace summary')))

    def test_control_held_105_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u298bpanel\u298c trace summary')))

    def test_control_held_106_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u298dpanel\u298e trace summary')))

    def test_control_held_107_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u298fpanel\u2990 trace summary')))

    def test_control_held_108_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2991panel\u2992 trace summary')))

    def test_control_held_109_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2993panel\u2994 trace summary')))

    def test_control_held_110_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2995panel\u2996 trace summary')))

    def test_control_held_111_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2997panel\u2998 trace summary')))

    def test_control_held_112_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29fcpanel\u29fd trace summary')))

    def test_control_held_113_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \uff5fpanel\uff60 trace summary')))

    def test_control_held_114_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u301apanel\u301b trace summary')))

    def test_control_held_115_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u3014panel\u3015 trace summary')))

    def test_control_held_116_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u3016panel\u3017 trace summary')))

    def test_control_held_117_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u3018panel\u3019 trace summary')))

    def test_control_held_118_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u00abpanel\u00bb trace summary')))

    def test_control_held_119_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2039panel\u203a trace summary')))

    def test_control_held_120_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u3008panel\u3009 trace summary')))

    def test_control_held_121_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u300apanel\u300b trace summary')))

    def test_control_held_122_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u201cpanel\u201d trace summary')))

    def test_control_held_123_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2018panel\u2019 trace summary')))

    def test_control_held_124_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e20panel\u2e21 trace summary')))

    def test_control_held_125_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2308panel\u2309 trace summary')))

    def test_control_held_126_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u230apanel\u230b trace summary')))

    def test_control_held_127_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u27c5panel\u27c6 trace summary')))

    def test_control_held_128_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \\ trace summary')))

    def test_control_held_129_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger || trace summary')))

    def test_control_held_130_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger * trace summary')))

    def test_control_held_131_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace board gate summary')))

    def test_control_held_132_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace board gate summary')))

    def test_control_held_133_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yank trace board gate summary')))

    def test_control_held_134_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bore trace board gate summary')))

    def test_control_held_135_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk rode summary board gate trace')))

    def test_control_held_136_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fled trace board gate summary')))

    def test_control_held_137_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sought trace board gate summary')))

    def test_control_held_138_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel paid trace board gate summary')))

    def test_control_held_139_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chose trace board gate summary')))

    def test_control_held_140_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel reviewed trace board gate summary')))

    def test_control_held_141_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel logs trace board gate summary')))

    def test_control_held_142_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel bore traceboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held_143_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel chose traceboardgatereviewannexpanelsummary')))

    def test_control_held_144_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel reviewed the traceboardgatereviewannexsummary')))

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
        self._candidate_governed(_bad("Round's trace summary"), _read("Round's trace summary"))

