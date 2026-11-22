"""Step 16 fix pass 32 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-32-02 (Medium, B32-C02
and B32-B02) of Step 16 round 32. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-32-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head read what
stands before the closing words through the standing test
of fix pass 31 Unit 1 as restated, which reads a main verb
in its base form and its irregular forms only where the
word stands in the widened closed constant
_MAIN_VERB_WORDS, beside the ed and ing ending test and
the s ending read in general, and reads a prose run join
only in the token shapes the earlier passes and fix pass
31 landed and a prose aside only in the shapes those
passes landed, and a clause break only in the comma,
semicolon and colon shapes, so prose standing before a
direct or fused closing in the shapes of this round takes
a tally statement head and stands present but not
derivable, against the restated boundary of fix pass 31
itself in its stated terms, which states the main verb
limb in terms as any inflection of a main verb and the
join and aside limbs in terms as a prose run join or a
prose aside standing before the closing words. Ninety
two distinct alone forms stand driven in three
subfamilies: (a) prose sentences whose closing words
stand in the direct trace summary form, thirteen forms,
each carrying a bare noun subject and a main verb
standing before the closing words in a base form or an
irregular form the widened constant does not name,
carrying no ed ending, no ing ending and no s ending the
test reads; (b) prose sentences whose last word stands
in a fused trace summary form, twelve forms in the same
verb shapes, two of them standing only at counts the
widening of fix pass 31 admitted and one of them standing
only on a summary form that widening admitted; and (c)
prose standing before a governed closing inside one
statement, sixty seven forms, prose runs joined to the
closing by a contour integral sign, a surface integral
sign, a volume integral sign, a clock integral sign, a
contour integral direction sign, a n-ary circled sign, a
n-ary square sign, a n-ary union sign, a subset sign, a
superset sign, a pitchfork sign, a parallel equality
sign, a normal subgroup sign, a triangle negation sign,
an ellipsis sign, a letterlike sign, a minus sign, an
angle sign, a divides sign, a parallel sign, a logical
sign, a double integral sign, a triple integral sign or
a combining sign standing as its own token, a prose run
carrying an aside in left and right angle bracket marks,
and verb first prose clauses in the same verb shapes.
One form stands driven in both papers in the same words
and stands counted once in this pinning, as the register
disposition states: the aside in left and right angle
bracket marks of subfamily (c). The Panel doze trace
summary line stands joined by a gate ruling form and a
beside form, each alone form standing present but not
derivable on the entering bytes, naming Step 2 and the
feeder piece. The twenty three converse assertions of
the round 32 breaker exhibit stand adopted in this
module: the twenty alone forms of B32-B02 stand among
the defect tests of the subfamilies above in their
driven words, and the gate ruling assertion, the beside
assertion and the code level assertion of that exhibit
stand as defect tests here in the forms the exhibit
names them. The defect stands bounded in the open by
its held controls: the cured verb candidates clap, chew
and twist standing missing in the fresh shapes, each
standing read in the widened constant; the s, ed and
ing forms of the fresh verb standing missing; the read
verb shapes yawn and took standing missing; the
candidate verb forms wept, swept, leapt, knelt and
crept of the breaker paper standing missing, each
standing read in the widened constant; the eighteen
word and nineteen word fused between prose sentences
in the fresh verb shape standing missing; the join
token forms in the congruent and approximately equal
shapes standing missing; the candidate join forms built
on the product, coproduct, summation, infinity and
integral signs standing missing; the aside forms in
the corner bracket and single angle quotation shapes
standing missing; the cured verb form standing
missing; the combining sign token forms at codepoints
U+20D0 and U+20E2 of the breaker paper standing
missing, each standing read as a join by the standing
test in its landed form; the held join forms of the
breaker paper, the double backslash token form, the
double pipe token form and the asterisk token form,
standing missing; the inserted prose tails of the
breaker paper standing missing; the article carrying
fused between forms of the breaker paper standing
missing; and every governed neighbour standing at its
recorded standing. Locus: derivation_core.py,
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


class TestStep16Fix32Unit1(FixtureTestCase):


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
    # Defect forms of R16-32-02, subfamily (a): the
    # thirteen direct prose sentences.
    # ------------------------------------------------------

    def test_r16_32_02_direct_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp trace summary')))

    def test_r16_32_02_direct_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk gasp summary trace')))

    def test_r16_32_02_direct_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team moan trace summary')))

    def test_r16_32_02_direct_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel groan summary trace')))

    def test_r16_32_02_direct_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk whistle trace summary')))

    def test_r16_32_02_direct_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team drank summary trace')))

    def test_r16_32_02_direct_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel meant trace summary')))

    def test_r16_32_02_direct_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel doze trace summary')))

    def test_r16_32_02_direct_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk yodel summary trace')))

    def test_r16_32_02_direct_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team grovel trace summary')))

    def test_r16_32_02_direct_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel meant summary trace')))

    def test_r16_32_02_direct_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk snivel trace summary')))

    def test_r16_32_02_direct_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team cower summary trace')))
    # ------------------------------------------------------
    # Defect forms of R16-32-02, subfamily (b): the
    # twelve fused prose sentences.
    # ------------------------------------------------------

    def test_r16_32_02_fused_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp tracesummary')))

    def test_r16_32_02_fused_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp boardtracesummary')))

    def test_r16_32_02_fused_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp traceboardgatesummary')))

    def test_r16_32_02_fused_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_r16_32_02_fused_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk gasp summarytrace')))

    def test_r16_32_02_fused_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel drank tracesummary')))

    def test_r16_32_02_fused_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel doze tracesummary')))

    def test_r16_32_02_fused_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk yodel summarytrace')))

    def test_r16_32_02_fused_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team grovel boardtracesummary')))

    def test_r16_32_02_fused_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel meant traceboardgatesummary')))

    def test_r16_32_02_fused_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk doze traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_r16_32_02_fused_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team yodel tracesummarisationeseseseseseseseseseseseses')))
    # ------------------------------------------------------
    # Defect forms of R16-32-02, subfamily (c): the
    # sixty three join forms.
    # ------------------------------------------------------

    def test_r16_32_02_join_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∮ trace summary')))

    def test_r16_32_02_join_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∯ trace summary')))

    def test_r16_32_02_join_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∰ trace summary')))

    def test_r16_32_02_join_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∱ trace summary')))

    def test_r16_32_02_join_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∲ trace summary')))

    def test_r16_32_02_join_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∳ trace summary')))

    def test_r16_32_02_join_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨀ trace summary')))

    def test_r16_32_02_join_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨁ trace summary')))

    def test_r16_32_02_join_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨂ trace summary')))

    def test_r16_32_02_join_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨄ trace summary')))

    def test_r16_32_02_join_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨅ trace summary')))

    def test_r16_32_02_join_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨆ trace summary')))

    def test_r16_32_02_join_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨇ trace summary')))

    def test_r16_32_02_join_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨈ trace summary')))

    def test_r16_32_02_join_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨉ trace summary')))

    def test_r16_32_02_join_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⨊ trace summary')))

    def test_r16_32_02_join_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋐ trace summary')))

    def test_r16_32_02_join_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋑ trace summary')))

    def test_r16_32_02_join_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋒ trace summary')))

    def test_r16_32_02_join_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋓ trace summary')))

    def test_r16_32_02_join_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋔ trace summary')))

    def test_r16_32_02_join_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋕ trace summary')))

    def test_r16_32_02_join_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋬ trace summary')))

    def test_r16_32_02_join_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋩ trace summary')))

    def test_r16_32_02_join_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋪ trace summary')))

    def test_r16_32_02_join_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋫ trace summary')))

    def test_r16_32_02_join_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋮ trace summary')))

    def test_r16_32_02_join_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋯ trace summary')))

    def test_r16_32_02_join_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℈ trace summary')))

    def test_r16_32_02_join_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℇ trace summary')))

    def test_r16_32_02_join_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℊ trace summary')))

    def test_r16_32_02_join_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℋ trace summary')))

    def test_r16_32_02_join_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℌ trace summary')))

    def test_r16_32_02_join_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℍ trace summary')))

    def test_r16_32_02_join_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℏ trace summary')))

    def test_r16_32_02_join_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℐ trace summary')))

    def test_r16_32_02_join_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℘ trace summary')))

    def test_r16_32_02_join_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℨ trace summary')))

    def test_r16_32_02_join_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger K trace summary')))

    def test_r16_32_02_join_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℬ trace summary')))

    def test_r16_32_02_join_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℹ trace summary')))

    def test_r16_32_02_join_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger − trace summary')))

    def test_r16_32_02_join_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∓ trace summary')))

    def test_r16_32_02_join_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∜ trace summary')))

    def test_r16_32_02_join_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∝ trace summary')))

    def test_r16_32_02_join_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∟ trace summary')))

    def test_r16_32_02_join_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∠ trace summary')))

    def test_r16_32_02_join_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∡ trace summary')))

    def test_r16_32_02_join_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∢ trace summary')))

    def test_r16_32_02_join_49_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∣ trace summary')))

    def test_r16_32_02_join_50_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∤ trace summary')))

    def test_r16_32_02_join_51_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∥ trace summary')))

    def test_r16_32_02_join_52_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∦ trace summary')))

    def test_r16_32_02_join_53_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∧ trace summary')))

    def test_r16_32_02_join_54_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∨ trace summary')))

    def test_r16_32_02_join_55_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∬ trace summary')))

    def test_r16_32_02_join_56_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∭ trace summary')))

    def test_r16_32_02_join_57_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d2 trace summary')))

    def test_r16_32_02_join_58_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d8 trace summary')))

    def test_r16_32_02_join_59_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20da trace summary')))

    def test_r16_32_02_join_60_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e0 trace summary')))

    def test_r16_32_02_join_61_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e3 trace summary')))

    def test_r16_32_02_join_62_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e7 trace summary')))
    # ------------------------------------------------------
    # Defect forms of R16-32-02, subfamily (c): the one
    # aside form, counted once across both papers.
    # ------------------------------------------------------

    def test_r16_32_02_aside_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u27e8panel\u27e9 trace summary')))
    # ------------------------------------------------------
    # Defect forms of R16-32-02, subfamily (c): the
    # three verb first prose clauses.
    # ------------------------------------------------------

    def test_r16_32_02_verbfirst_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Gulp panel trace summary')))

    def test_r16_32_02_verbfirst_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Drank panel summary trace')))

    def test_r16_32_02_verbfirst_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Doze ledger trace summary')))
    # ------------------------------------------------------
    # Adopted assertions of the round 32 breaker exhibit:
    # the gate ruling, beside and code level assertions
    # of B32-B02, in the forms the exhibit names them.
    # ------------------------------------------------------

    def test_b32_prose_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel doze trace summary"), ruling=True))

    def test_b32_prose_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            "Panel doze trace summary"))

    def test_b32_code_level_prose_no_head(self):
        for run in ("Panel doze trace summary",
                    "Clerk yodel summary trace",
                    "Panel doze tracesummary",
                    'Clerk doze traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary',
                    "Ledger \u20d2 trace summary",
                    "Ledger \u20d8 trace summary",
                    "Ledger \u27e8panel\u27e9 trace summary"):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)
    # ------------------------------------------------------
    # Held controls of R16-32-02, standing missing in the
    # papers of this round in the same constructions, one
    # test per held form the register names.
    # ------------------------------------------------------

    def test_control_held_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chews trace summary')))

    def test_control_held_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chewed trace summary')))

    def test_control_held_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chewing trace summary')))

    def test_control_held_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yawn trace summary')))

    def test_control_held_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel took trace summary')))

    def test_control_held_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap trace summary')))

    def test_control_held_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap tracesummary')))

    def test_control_held_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap summarytrace')))

    def test_control_held_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap boardtracesummary')))

    def test_control_held_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatesummary')))

    def test_control_held_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap tracesummarisationeseseseseseseseseseseseses')))

    def test_control_held_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew trace summary')))

    def test_control_held_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew tracesummary')))

    def test_control_held_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew summarytrace')))

    def test_control_held_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew boardtracesummary')))

    def test_control_held_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatesummary')))

    def test_control_held_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew tracesummarisationeseseseseseseseseseseseses')))

    def test_control_held_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist trace summary')))

    def test_control_held_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist tracesummary')))

    def test_control_held_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist summarytrace')))

    def test_control_held_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist boardtracesummary')))

    def test_control_held_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatesummary')))

    def test_control_held_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist tracesummarisationeseseseseseseseseseseseses')))

    def test_control_held_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team wept trace summary')))

    def test_control_held_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk swept trace summary')))

    def test_control_held_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team leapt summary trace')))

    def test_control_held_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel knelt summary trace')))

    def test_control_held_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel crept trace summary')))

    def test_control_held_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_held_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2245 trace summary')))

    def test_control_held_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2248 trace summary')))

    def test_control_held_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u220f trace summary')))

    def test_control_held_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2210 trace summary')))

    def test_control_held_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2211 trace summary')))

    def test_control_held_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u221e trace summary')))

    def test_control_held_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u222b trace summary')))

    def test_control_held_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e22panel\u2e23 trace summary')))

    def test_control_held_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u3008panel\u3009 trace summary')))

    def test_control_held_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sat trace summary')))

    def test_control_held_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d0 trace summary')))

    def test_control_held_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e2 trace summary')))

    def test_control_held_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \\ trace summary')))

    def test_control_held_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger || trace summary')))

    def test_control_held_49_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger * trace summary')))

    def test_control_held_50_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace board gate summary')))

    def test_control_held_51_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace board gate summary')))

    def test_control_held_52_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yank trace board gate summary')))

    def test_control_held_53_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bore trace board gate summary')))

    def test_control_held_54_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk rode summary board gate trace')))

    def test_control_held_55_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fled trace board gate summary')))

    def test_control_held_56_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sought trace board gate summary')))

    def test_control_held_57_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel paid trace board gate summary')))

    def test_control_held_58_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chose trace board gate summary')))

    def test_control_held_59_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel reviewed trace board gate summary')))

    def test_control_held_60_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel logs trace board gate summary')))

    def test_control_held_61_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel bore traceboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held_62_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel chose traceboardgatereviewannexpanelsummary')))

    def test_control_held_63_missing(self):
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

