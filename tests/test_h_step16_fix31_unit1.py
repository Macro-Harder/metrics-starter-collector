"""Step 16 fix pass 31 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-31-02 (Medium, B31-C02
and B31-B02) of Step 16 round 31. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-31-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head read what
stands before the closing words through the standing test
of fix pass 30 Unit 1 as restated, which reads a main verb
in its base form and its irregular forms only where the
word stands in the widened closed constant
_MAIN_VERB_WORDS, beside the ed and ing ending test and
the s ending read in general, and reads a prose run join
only in the token shapes the earlier passes and fix pass
30 landed and a prose aside only in the shapes those
passes landed, and a clause break only in the comma,
semicolon and colon shapes, so prose standing before a
direct or fused closing in the shapes of this round takes
a tally statement head and stands present but not
derivable, against the restated boundary of fix pass 30
itself in its stated terms, which states the main verb
limb in terms as any inflection of a main verb and the
join and aside limbs in terms as a prose run join or a
prose aside standing before the closing words. Two
hundred and eighteen distinct alone forms stand driven
in three subfamilies: (a) prose sentences whose closing
words stand in the direct trace summary form, sixty seven
forms, each carrying a bare noun subject and a main verb
standing before the closing words in a base form or an
irregular form the widened constant does not name,
carrying no ed ending, no ing ending and no s ending the
test reads; (b) prose sentences whose last word stands
in a fused trace summary form, twenty two forms in the
same verb shapes, two of them standing only at counts
the widening of fix pass 30 admitted; and (c) prose
standing before a governed closing inside one statement,
one hundred and twenty nine forms, prose runs joined to
the closing by a n-ary sign, a squared sign, a coproduct
sign, a set minus sign, a semidirect product sign, a
reversed tilde sign, a relation sign, a square image
sign, a n-ary logical sign, a wreath sign, an asymptotic
sign, a letterlike sign token, a fraction sign token, a
superscript sign token, a per ten thousand sign token,
an estimated sign token, an ohm sign token or a
combining sign standing as its own token, a prose run
carrying an aside in the bracket and mark shapes the
register disposition names, and verb first prose clauses
in the same verb shapes. One form stands driven in both
papers in the same words and stands counted once in this
pinning, as the register disposition states: the aside
in left and right vertical bar with quill marks of
subfamily (c). The Panel grin trace summary line stands
joined by a gate ruling form and a beside form, each
alone form standing present but not derivable on the
entering bytes, naming Step 2 and the feeder piece. The
twenty seven converse assertions of the round 31 breaker
exhibit stand adopted in this module: the twenty four
alone forms of B31-B02 stand among the defect tests of
the subfamilies above in their driven words, and the
gate ruling assertion, the beside assertion and the code
level assertion of that exhibit stand as defect tests
here in the forms the exhibit names them. The defect
stands bounded in the open by its held controls: the
cured verb candidates clap and twist standing missing in
the fresh shapes, each standing read in the widened
constant; the s, ed and ing forms of the fresh verb
standing missing; the candidate verb forms bleed and
sling standing missing, their verbs standing read on
their ed and ing endings; the eighteen word fused
between prose sentence in the fresh verb shape standing
missing; the join token forms in the congruent and
approximately equal shapes standing missing; the aside
forms in the top and bottom parenthesis, mathematical
white tortoise shell bracket, ceiling and heavy angle
quotation shapes standing missing; the verb first ed
form and the cured verb form standing missing; the
combining enclosing leftward arrow sign token form of
the breaker paper standing missing; the held join forms
of the breaker paper, the double backslash token form,
the double pipe token form and the asterisk token form,
standing missing; the lari, bitcoin and lira sign token
forms of the breaker paper standing missing; the
inserted prose tails of the breaker paper standing
missing; the article carrying fused between forms of
the breaker paper standing missing; the candidate verb
forms clap and tap of the breaker paper standing
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


class TestStep16Fix31Unit1(FixtureTestCase):


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
    # Defect forms of R16-31-02, subfamily (a): the sixty
    # seven direct prose sentences.
    # ------------------------------------------------------

    def test_r16_31_02_direct_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew trace summary')))

    def test_r16_31_02_direct_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk pray summary trace')))

    def test_r16_31_02_direct_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team bow trace summary')))

    def test_r16_31_02_direct_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grin summary trace')))

    def test_r16_31_02_direct_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk sob trace summary')))

    def test_r16_31_02_direct_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team wink summary trace')))

    def test_r16_31_02_direct_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lick trace summary')))

    def test_r16_31_02_direct_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk peek summary trace')))

    def test_r16_31_02_direct_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team peer trace summary')))

    def test_r16_31_02_direct_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel squint summary trace')))

    def test_r16_31_02_direct_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk snore trace summary')))

    def test_r16_31_02_direct_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team giggle summary trace')))

    def test_r16_31_02_direct_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chuckle trace summary')))

    def test_r16_31_02_direct_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk sniff summary trace')))

    def test_r16_31_02_direct_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team burp trace summary')))

    def test_r16_31_02_direct_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hiccup summary trace')))

    def test_r16_31_02_direct_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk tremble trace summary')))

    def test_r16_31_02_direct_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team wobble summary trace')))

    def test_r16_31_02_direct_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel drool trace summary')))

    def test_r16_31_02_direct_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk shudder summary trace')))

    def test_r16_31_02_direct_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team murmur trace summary')))

    def test_r16_31_02_direct_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glow summary trace')))

    def test_r16_31_02_direct_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk glare trace summary')))

    def test_r16_31_02_direct_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team arise summary trace')))

    def test_r16_31_02_direct_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel awake trace summary')))

    def test_r16_31_02_direct_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk behold summary trace')))

    def test_r16_31_02_direct_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team dwell trace summary')))

    def test_r16_31_02_direct_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel flee summary trace')))

    def test_r16_31_02_direct_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk grind trace summary')))

    def test_r16_31_02_direct_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team lean summary trace')))

    def test_r16_31_02_direct_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lie trace summary')))

    def test_r16_31_02_direct_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk light summary trace')))

    def test_r16_31_02_direct_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team plead trace summary')))

    def test_r16_31_02_direct_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel prove summary trace')))

    def test_r16_31_02_direct_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk spring trace summary')))

    def test_r16_31_02_direct_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stride summary trace')))

    def test_r16_31_02_direct_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel strive trace summary')))

    def test_r16_31_02_direct_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk tread summary trace')))

    def test_r16_31_02_direct_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team weave trace summary')))

    def test_r16_31_02_direct_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wind summary trace')))

    def test_r16_31_02_direct_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk shiver trace summary')))

    def test_r16_31_02_direct_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team arose summary trace')))

    def test_r16_31_02_direct_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel awoke trace summary')))

    def test_r16_31_02_direct_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk befell summary trace')))

    def test_r16_31_02_direct_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team beheld trace summary')))

    def test_r16_31_02_direct_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel besought summary trace')))

    def test_r16_31_02_direct_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk bade trace summary')))

    def test_r16_31_02_direct_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team dwelt summary trace')))

    def test_r16_31_02_direct_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel ground trace summary')))

    def test_r16_31_02_direct_49_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk leant summary trace')))

    def test_r16_31_02_direct_50_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team lay trace summary')))

    def test_r16_31_02_direct_51_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lit summary trace')))

    def test_r16_31_02_direct_52_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk proven trace summary')))

    def test_r16_31_02_direct_53_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team slung summary trace')))

    def test_r16_31_02_direct_54_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sprang trace summary')))

    def test_r16_31_02_direct_55_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk strode summary trace')))

    def test_r16_31_02_direct_56_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team strove trace summary')))

    def test_r16_31_02_direct_57_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel trod summary trace')))

    def test_r16_31_02_direct_58_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk wove trace summary')))

    def test_r16_31_02_direct_59_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team wound summary trace')))

    def test_r16_31_02_direct_60_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel forsook trace summary')))

    def test_r16_31_02_direct_61_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grin trace summary')))

    def test_r16_31_02_direct_62_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk sip summary trace')))

    def test_r16_31_02_direct_63_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team sob trace summary')))

    def test_r16_31_02_direct_64_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel arose summary trace')))

    def test_r16_31_02_direct_65_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk dove trace summary')))

    def test_r16_31_02_direct_66_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team strode summary trace')))
    # ------------------------------------------------------
    # Defect forms of R16-31-02, subfamily (b): the twenty
    # two fused prose sentences.
    # ------------------------------------------------------

    def test_r16_31_02_fused_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew tracesummary')))

    def test_r16_31_02_fused_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew boardtracesummary')))

    def test_r16_31_02_fused_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatesummary')))

    def test_r16_31_02_fused_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelsummary')))

    def test_r16_31_02_fused_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardsummary')))

    def test_r16_31_02_fused_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatesummary')))

    def test_r16_31_02_fused_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewsummary')))

    def test_r16_31_02_fused_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_r16_31_02_fused_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_r16_31_02_fused_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_r16_31_02_fused_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_r16_31_02_fused_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_r16_31_02_fused_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary')))

    def test_r16_31_02_fused_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_r16_31_02_fused_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel arose tracesummary')))

    def test_r16_31_02_fused_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk awoke summarytrace')))

    def test_r16_31_02_fused_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grin tracesummary')))

    def test_r16_31_02_fused_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk sip summarytrace')))

    def test_r16_31_02_fused_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team sob boardtracesummary')))

    def test_r16_31_02_fused_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel arose traceboardgatesummary')))

    def test_r16_31_02_fused_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk dove traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_r16_31_02_fused_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team grin tracesummarisationeseseseseseseseseseseseses')))
    # ------------------------------------------------------
    # Defect forms of R16-31-02, subfamily (c): the eighty
    # join forms.
    # ------------------------------------------------------

    def test_r16_31_02_join_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋂ trace summary')))

    def test_r16_31_02_join_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋃ trace summary')))

    def test_r16_31_02_join_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋄ trace summary')))

    def test_r16_31_02_join_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋈ trace summary')))

    def test_r16_31_02_join_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⟂ trace summary')))

    def test_r16_31_02_join_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊜ trace summary')))

    def test_r16_31_02_join_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊝ trace summary')))

    def test_r16_31_02_join_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊞ trace summary')))

    def test_r16_31_02_join_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊟ trace summary')))

    def test_r16_31_02_join_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊠ trace summary')))

    def test_r16_31_02_join_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊡ trace summary')))

    def test_r16_31_02_join_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∐ trace summary')))

    def test_r16_31_02_join_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∔ trace summary')))

    def test_r16_31_02_join_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∕ trace summary')))

    def test_r16_31_02_join_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∖ trace summary')))

    def test_r16_31_02_join_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ∛ trace summary')))

    def test_r16_31_02_join_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋊ trace summary')))

    def test_r16_31_02_join_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋋ trace summary')))

    def test_r16_31_02_join_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋌ trace summary')))

    def test_r16_31_02_join_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋍ trace summary')))

    def test_r16_31_02_join_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≢ trace summary')))

    def test_r16_31_02_join_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≣ trace summary')))

    def test_r16_31_02_join_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊄ trace summary')))

    def test_r16_31_02_join_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊅ trace summary')))

    def test_r16_31_02_join_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊆ trace summary')))

    def test_r16_31_02_join_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊇ trace summary')))

    def test_r16_31_02_join_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊈ trace summary')))

    def test_r16_31_02_join_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊉ trace summary')))

    def test_r16_31_02_join_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊊ trace summary')))

    def test_r16_31_02_join_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊋ trace summary')))

    def test_r16_31_02_join_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊍ trace summary')))

    def test_r16_31_02_join_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊎ trace summary')))

    def test_r16_31_02_join_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊏ trace summary')))

    def test_r16_31_02_join_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊐ trace summary')))

    def test_r16_31_02_join_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊑ trace summary')))

    def test_r16_31_02_join_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⊒ trace summary')))

    def test_r16_31_02_join_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋀ trace summary')))

    def test_r16_31_02_join_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⋁ trace summary')))

    def test_r16_31_02_join_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≀ trace summary')))

    def test_r16_31_02_join_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≁ trace summary')))

    def test_r16_31_02_join_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≂ trace summary')))

    def test_r16_31_02_join_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≃ trace summary')))

    def test_r16_31_02_join_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≄ trace summary')))

    def test_r16_31_02_join_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≆ trace summary')))

    def test_r16_31_02_join_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≇ trace summary')))

    def test_r16_31_02_join_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≉ trace summary')))

    def test_r16_31_02_join_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≊ trace summary')))

    def test_r16_31_02_join_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≋ trace summary')))

    def test_r16_31_02_join_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≌ trace summary')))

    def test_r16_31_02_join_49_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≍ trace summary')))

    def test_r16_31_02_join_50_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≎ trace summary')))

    def test_r16_31_02_join_51_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≏ trace summary')))

    def test_r16_31_02_join_52_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≐ trace summary')))

    def test_r16_31_02_join_53_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≑ trace summary')))

    def test_r16_31_02_join_54_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger № trace summary')))

    def test_r16_31_02_join_55_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℗ trace summary')))

    def test_r16_31_02_join_56_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℥ trace summary')))

    def test_r16_31_02_join_57_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℔ trace summary')))

    def test_r16_31_02_join_58_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℀ trace summary')))

    def test_r16_31_02_join_59_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℅ trace summary')))

    def test_r16_31_02_join_60_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℆ trace summary')))

    def test_r16_31_02_join_61_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⅍ trace summary')))

    def test_r16_31_02_join_62_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⅎ trace summary')))

    def test_r16_31_02_join_63_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ↯ trace summary')))

    def test_r16_31_02_join_64_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ¼ trace summary')))

    def test_r16_31_02_join_65_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ¾ trace summary')))

    def test_r16_31_02_join_66_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⅓ trace summary')))

    def test_r16_31_02_join_67_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⅔ trace summary')))

    def test_r16_31_02_join_68_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ¹ trace summary')))

    def test_r16_31_02_join_69_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⁴ trace summary')))

    def test_r16_31_02_join_70_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⁰ trace summary')))

    def test_r16_31_02_join_71_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ‱ trace summary')))

    def test_r16_31_02_join_72_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ℮ trace summary')))

    def test_r16_31_02_join_73_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger Ω trace summary')))

    def test_r16_31_02_join_74_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃑ trace summary')))

    def test_r16_31_02_join_75_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃖ trace summary')))

    def test_r16_31_02_join_76_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃗ trace summary')))

    def test_r16_31_02_join_77_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃡ trace summary')))

    def test_r16_31_02_join_78_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃥ trace summary')))

    def test_r16_31_02_join_79_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃛ trace summary')))
    # ------------------------------------------------------
    # Defect forms of R16-31-02, subfamily (c): the forty
    # four aside forms.
    # ------------------------------------------------------

    def test_r16_31_02_aside_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸠panel⸡ trace summary')))

    def test_r16_31_02_aside_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸮panel⸮ trace summary')))

    def test_r16_31_02_aside_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ᚛panel᚜ trace summary')))

    def test_r16_31_02_aside_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ꧄panel꧅ trace summary')))

    def test_r16_31_02_aside_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ꧞panel꧟ trace summary')))

    def test_r16_31_02_aside_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸐panel⸑ trace summary')))

    def test_r16_31_02_aside_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸔panel⸕ trace summary')))

    def test_r16_31_02_aside_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸘panel⸙ trace summary')))

    def test_r16_31_02_aside_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸚panel⸛ trace summary')))

    def test_r16_31_02_aside_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸞panel⸟ trace summary')))

    def test_r16_31_02_aside_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸎panel⸏ trace summary')))

    def test_r16_31_02_aside_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌠panel⌡ trace summary')))

    def test_r16_31_02_aside_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⎡panel⎤ trace summary')))

    def test_r16_31_02_aside_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⎣panel⎦ trace summary')))

    def test_r16_31_02_aside_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⎧panel⎫ trace summary')))

    def test_r16_31_02_aside_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⏞panel⏟ trace summary')))

    def test_r16_31_02_aside_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⏜panel⏝ trace summary')))

    def test_r16_31_02_aside_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦀panel⦀ trace summary')))

    def test_r16_31_02_aside_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧗panel⧖ trace summary')))

    def test_r16_31_02_aside_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧜panel⧝ trace summary')))

    def test_r16_31_02_aside_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧞panel⧟ trace summary')))

    def test_r16_31_02_aside_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧠panel⧡ trace summary')))

    def test_r16_31_02_aside_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧢panel⧣ trace summary')))

    def test_r16_31_02_aside_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧤panel⧥ trace summary')))

    def test_r16_31_02_aside_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧦panel⧧ trace summary')))

    def test_r16_31_02_aside_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧨panel⧩ trace summary')))

    def test_r16_31_02_aside_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧪panel⧪ trace summary')))

    def test_r16_31_02_aside_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧫panel⧫ trace summary')))

    def test_r16_31_02_aside_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧬panel⧬ trace summary')))

    def test_r16_31_02_aside_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧮panel⧮ trace summary')))

    def test_r16_31_02_aside_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧰panel⧰ trace summary')))

    def test_r16_31_02_aside_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧱panel⧱ trace summary')))

    def test_r16_31_02_aside_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧲panel⧲ trace summary')))

    def test_r16_31_02_aside_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧴panel⧴ trace summary')))

    def test_r16_31_02_aside_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧵panel⧵ trace summary')))

    def test_r16_31_02_aside_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧶panel⧶ trace summary')))

    def test_r16_31_02_aside_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧸panel⧸ trace summary')))

    def test_r16_31_02_aside_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧹panel⧹ trace summary')))

    def test_r16_31_02_aside_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧺panel⧺ trace summary')))

    def test_r16_31_02_aside_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⧻panel⧻ trace summary')))

    def test_r16_31_02_aside_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⦓panel⦔ trace summary')))

    def test_r16_31_02_aside_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ［panel］ trace summary')))

    def test_r16_31_02_aside_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ＜panel＞ trace summary')))

    def test_r16_31_02_aside_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ‟panel‟ trace summary')))
    # ------------------------------------------------------
    # Defect forms of R16-31-02, subfamily (c): the five
    # verb first clause forms.
    # ------------------------------------------------------

    def test_r16_31_02_verbfirst_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Chew panel trace summary')))

    def test_r16_31_02_verbfirst_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Pray panel trace summary')))

    def test_r16_31_02_verbfirst_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Arose panel summary trace')))

    def test_r16_31_02_verbfirst_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Awoke panel summary trace')))

    def test_r16_31_02_verbfirst_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Grin ledger trace summary')))
    # ------------------------------------------------------
    # Adopted assertions of the round 31 breaker exhibit:
    # the gate ruling form, the beside form and the code
    # level form of B31-B02, in the words the exhibit
    # names them. The twenty four alone form assertions of
    # that exhibit stand as the defect tests above over
    # the breaker forms of the three subfamilies.
    # ------------------------------------------------------

    def test_b31_prose_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose("Panel grin trace summary"), ruling=True))

    def test_b31_prose_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            "Panel grin trace summary"))

    def test_b31_code_level_prose_no_head(self):
        for run in ('Panel grin trace summary', 'Clerk sip summary trace', 'Panel grin tracesummary', 'Clerk dove traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary', 'Ledger ⃑ trace summary', 'Ledger ⃖ trace summary', 'Ledger ⦓panel⦔ trace summary'):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)
    # ------------------------------------------------------
    # Held controls of R16-31-02, standing missing in the
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
            _prose('Panel bleed trace summary')))

    def test_control_held_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sling trace summary')))

    def test_control_held_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≅ trace summary')))

    def test_control_held_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ≈ trace summary')))

    def test_control_held_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⸜panel⸝ trace summary')))

    def test_control_held_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⟬panel⟭ trace summary')))

    def test_control_held_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⌈panel⌉ trace summary')))

    def test_control_held_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ❮panel❯ trace summary')))

    def test_control_held_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Grabbed panel trace summary')))

    def test_control_held_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sat trace summary')))

    def test_control_held_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ⃀ trace summary')))

    def test_control_held_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap trace summary')))

    def test_control_held_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tap trace summary')))

    def test_control_held_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist trace summary')))

    def test_control_held_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap tracesummary')))

    def test_control_held_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap boardtracesummary')))

    def test_control_held_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatesummary')))

    def test_control_held_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelsummary')))

    def test_control_held_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardsummary')))

    def test_control_held_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatesummary')))

    def test_control_held_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_held_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_held_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary')))

    def test_control_held_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist tracesummary')))

    def test_control_held_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist boardtracesummary')))

    def test_control_held_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatesummary')))

    def test_control_held_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelsummary')))

    def test_control_held_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardsummary')))

    def test_control_held_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatesummary')))

    def test_control_held_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_held_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_control_held_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexsummary')))

    def test_control_held_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardsummary')))

    def test_control_held_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twist traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatesummary')))

    def test_control_held_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \\\\ trace summary')))

    def test_control_held_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger || trace summary')))

    def test_control_held_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger * trace summary')))

    def test_control_held_49_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ₾ trace summary')))

    def test_control_held_50_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ₿ trace summary')))

    def test_control_held_51_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger ₺ trace summary')))

    def test_control_held_52_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace board gate summary')))

    def test_control_held_53_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace board gate summary')))

    def test_control_held_54_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yank trace board gate summary')))

    def test_control_held_55_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bore trace board gate summary')))

    def test_control_held_56_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk rode summary board gate trace')))

    def test_control_held_57_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fled trace board gate summary')))

    def test_control_held_58_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sought trace board gate summary')))

    def test_control_held_59_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel paid trace board gate summary')))

    def test_control_held_60_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chose trace board gate summary')))

    def test_control_held_61_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel reviewed trace board gate summary')))

    def test_control_held_62_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel logs trace board gate summary')))

    def test_control_held_63_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel bore traceboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held_64_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel chose traceboardgatereviewannexpanelsummary')))

    def test_control_held_65_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel reviewed the traceboardgatereviewannexsummary')))
    # ------------------------------------------------------
    # Held governed controls: the governed closings of the
    # breaker paper of this round, standing governed beside
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
