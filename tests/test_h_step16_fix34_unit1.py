"""Step 16 fix pass 34 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-34-02 (Medium, B34-C02
and B34-B02) of Step 16 round 34. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-34-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head read what
stands before the closing words through the standing test
of fix pass 33 Unit 1 as restated, which reads a main verb
in its base form and its irregular forms only where the
word stands in the widened closed constant
_MAIN_VERB_WORDS at seven hundred and thirty one forms,
beside the ed and ing ending test and the s ending read
in general, and reads a prose run join only in the token
shapes the earlier passes and fix pass 33 landed and a
prose aside only in the shapes those passes landed, and
a clause break only in the comma, semicolon and colon
shapes, so prose standing before a direct or fused
closing in the shapes of this round takes a tally
statement head and stands present but not derivable,
against the restated boundary of fix pass 33 Unit 1
itself in its stated terms, which states the main verb
limb in terms as any inflection of a main verb and the
join and aside limbs in terms as a prose run join or a
prose aside standing before the closing words. Ninety
nine distinct alone forms stand driven in three
subfamilies: (a) prose sentences whose closing words
stand in the direct trace summary form, nineteen forms,
fourteen of the correctness paper over the verbs snicker,
chortle, guffaw, wince, grimace, scowl, whimper, whine,
mutter, stutter, blubber, cackle, snigger and titter with
the Panel subject, and six of the breaker paper over
whimper, mutter, stutter, falter, babble and waver, the
direct form and the plain fused form over the verb
whimper in their Panel subject shapes standing shared,
overlaps 1 in this subfamily; (b) prose sentences whose
last word stands in a fused trace summary form, nineteen
forms, fourteen of the correctness paper in the plain
fused form over the same fourteen verbs and six of the
breaker paper standing as the direct fused form, the
reversed fused form, the fused form behind a prefix, the
fused between form with two governed words fused between
the closing words, the fused between form at twenty
governed words fused between the closing words, the
count fix pass 33 Unit 2 widened to, and the fused form
built on a summary form that widening admitted, the plain
fused form over the verb whimper standing shared,
overlaps 1 in this subfamily; and (c) prose standing
before a governed closing inside one statement, sixty one
forms, fifty four of the correctness paper standing as
thirty two prose runs joined by a sign token of the
n-ary, circled, sector or electrical families at
codepoints U+2A36 through U+2A4F, U+29C4 through U+29C7,
U+2313 and U+23E0, two prose runs joined by a combining
sign token standing on its host letter at codepoints
U+20D3 and U+20E4, six prose runs carrying an aside in
further supplement punctuation bracket marks at the six
mark pairs the disposition names, and fourteen prose
clauses in verb first form over the panel subject in the
base verb shapes of subfamily (a), and eight of the
breaker paper standing as six prose runs joined by a
combining sign token standing as its own token at
codepoints U+20D3, U+20D9, U+20E4, U+20E6, U+20E8 and
U+20E9, one prose run carrying an aside in square bracket
with double stroke marks at codepoints U+2E57 and U+2E58,
standing shared with the first aside form of the
correctness paper, overlaps 1 in this subfamily, and one
prose clause in verb first form over the ledger subject.
The stated counts of the correctness paper stand at
seventy six forms against its driven forms at eighty two
in the difference the round 34 register records in the
open; the driven forms govern this pinning exactly as
the register carries them, gross 102 driven forms,
overlaps 3, ninety nine distinct alone forms in all. The
Panel snicker trace summary line of the correctness
paper stands joined by a gate ruling form and a beside
form, and the Panel whimper trace summary line of the
breaker paper stands joined by a gate ruling form and a
beside form, each alone form standing present but not
derivable on the entering bytes, naming Step 2 and the
feeder piece. The twenty three converse assertions of
the round 34 breaker exhibit stand adopted in this
module: the twenty alone forms of B34-B02 stand among
the defect tests of the subfamilies above in their driven
words, and the gate ruling assertion, the beside
assertion and the code level assertion of that exhibit
stand as defect tests here in the forms the exhibit
names them. The defect stands bounded in the open by
its held controls: the candidate verbs of the
correctness paper standing read as main verbs in the
same screening drive, sigh, sob, gulp, gasp, whisper,
murmur and tremble in their base forms, each standing
missing in its driven sentence; the candidate verbs of
the breaker paper, shudder, cower, grovel and snivel in
their base forms, standing read as main verbs in their
driven sentences; the join token forms at codepoints
U+22C8, U+22CA, U+22CB and U+22CC and at U+29C8 and
U+29C9 of the correctness paper standing missing; the
candidate aside pairs of the correctness paper standing
missing, the pairs at U+2985 and U+2986, at U+27E6 and
U+27E7, at U+FF08 and U+FF09, and the quoted pair at
U+2E15 and U+2E16 standing as the quoted paper form of
the cured aside; the candidate combining tokens of the
correctness paper at codepoints U+20D4, U+20D8 and
U+20E3 standing missing, each standing read as a join
by the standing test in its landed form; the combining
sign token forms at codepoints U+20D8, U+20DA, U+20E0,
U+20E3 and U+20E7 of the breaker paper standing missing,
beside the forms at U+20D4, U+20D5, U+20DC, U+20DD,
U+20DE and U+20DF standing missing at this standing
under the cure of fix pass 33; the candidate aside pair
of the breaker paper at codepoints U+2045 and U+2046
standing read as an aside in its probed form; the held
join forms of the breaker paper, the double backslash
token form, the double pipe token form and the asterisk
token form, standing missing in their recorded forms;
the inserted prose tails of the breaker paper standing
missing in the verb shapes of the earlier rounds as that
paper records them; the article carrying fused between
forms of the breaker paper standing missing in their
recorded forms; and every governed neighbour standing
at its recorded standing. Locus: derivation_core.py,
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


class TestStep16Fix34Unit1(FixtureTestCase):


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
    # Defect forms of R16-34-02, subfamily (a): the
    # nineteen direct prose sentences.
    # ------------------------------------------------------

    def test_r16_34_02_direct_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snicker trace summary')))

    def test_r16_34_02_direct_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chortle trace summary')))

    def test_r16_34_02_direct_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel guffaw trace summary')))

    def test_r16_34_02_direct_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wince trace summary')))

    def test_r16_34_02_direct_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grimace trace summary')))

    def test_r16_34_02_direct_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel scowl trace summary')))

    def test_r16_34_02_direct_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whimper trace summary')))

    def test_r16_34_02_direct_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whine trace summary')))

    def test_r16_34_02_direct_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel mutter trace summary')))

    def test_r16_34_02_direct_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stutter trace summary')))

    def test_r16_34_02_direct_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel blubber trace summary')))

    def test_r16_34_02_direct_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cackle trace summary')))

    def test_r16_34_02_direct_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snigger trace summary')))

    def test_r16_34_02_direct_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel titter trace summary')))

    def test_r16_34_02_direct_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk mutter summary trace')))

    def test_r16_34_02_direct_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stutter trace summary')))

    def test_r16_34_02_direct_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel falter summary trace')))

    def test_r16_34_02_direct_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk babble trace summary')))

    def test_r16_34_02_direct_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team waver summary trace')))

    # ------------------------------------------------------
    # Defect forms of R16-34-02, subfamily (b): the
    # nineteen fused prose sentences.
    # ------------------------------------------------------

    def test_r16_34_02_fused_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snicker tracesummary')))

    def test_r16_34_02_fused_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chortle tracesummary')))

    def test_r16_34_02_fused_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel guffaw tracesummary')))

    def test_r16_34_02_fused_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wince tracesummary')))

    def test_r16_34_02_fused_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grimace tracesummary')))

    def test_r16_34_02_fused_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel scowl tracesummary')))

    def test_r16_34_02_fused_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whimper tracesummary')))

    def test_r16_34_02_fused_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whine tracesummary')))

    def test_r16_34_02_fused_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel mutter tracesummary')))

    def test_r16_34_02_fused_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stutter tracesummary')))

    def test_r16_34_02_fused_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel blubber tracesummary')))

    def test_r16_34_02_fused_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cackle tracesummary')))

    def test_r16_34_02_fused_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snigger tracesummary')))

    def test_r16_34_02_fused_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel titter tracesummary')))

    def test_r16_34_02_fused_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk mutter summarytrace')))

    def test_r16_34_02_fused_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team stutter boardtracesummary')))

    def test_r16_34_02_fused_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel falter traceboardgatesummary')))

    def test_r16_34_02_fused_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk whimper traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_r16_34_02_fused_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team mutter tracesummarisationeseseseseseseseseseseseseseseses')))

    # ------------------------------------------------------
    # Defect forms of R16-34-02, subfamily (c): the
    # thirty two sign token join forms of the
    # correctness paper.
    # ------------------------------------------------------

    def test_r16_34_02_join_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a36 trace summary')))

    def test_r16_34_02_join_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a37 trace summary')))

    def test_r16_34_02_join_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a38 trace summary')))

    def test_r16_34_02_join_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a39 trace summary')))

    def test_r16_34_02_join_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a3a trace summary')))

    def test_r16_34_02_join_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a3b trace summary')))

    def test_r16_34_02_join_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a3c trace summary')))

    def test_r16_34_02_join_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a3d trace summary')))

    def test_r16_34_02_join_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a3e trace summary')))

    def test_r16_34_02_join_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a3f trace summary')))

    def test_r16_34_02_join_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a40 trace summary')))

    def test_r16_34_02_join_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a41 trace summary')))

    def test_r16_34_02_join_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a42 trace summary')))

    def test_r16_34_02_join_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a43 trace summary')))

    def test_r16_34_02_join_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a44 trace summary')))

    def test_r16_34_02_join_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a45 trace summary')))

    def test_r16_34_02_join_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a46 trace summary')))

    def test_r16_34_02_join_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a47 trace summary')))

    def test_r16_34_02_join_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a48 trace summary')))

    def test_r16_34_02_join_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a49 trace summary')))

    def test_r16_34_02_join_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a4a trace summary')))

    def test_r16_34_02_join_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a4b trace summary')))

    def test_r16_34_02_join_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a4c trace summary')))

    def test_r16_34_02_join_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a4d trace summary')))

    def test_r16_34_02_join_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a4e trace summary')))

    def test_r16_34_02_join_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2a4f trace summary')))

    def test_r16_34_02_join_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29c4 trace summary')))

    def test_r16_34_02_join_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29c5 trace summary')))

    def test_r16_34_02_join_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29c6 trace summary')))

    def test_r16_34_02_join_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29c7 trace summary')))

    def test_r16_34_02_join_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2313 trace summary')))

    def test_r16_34_02_join_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u23e0 trace summary')))

    # ------------------------------------------------------
    # Defect forms of R16-34-02, subfamily (c): the
    # two combining sign forms of the correctness
    # paper, standing on their host letter.
    # ------------------------------------------------------

    def test_r16_34_02_join_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20d3 trace summary')))

    def test_r16_34_02_join_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20e4 trace summary')))

    # ------------------------------------------------------
    # Defect forms of R16-34-02, subfamily (c): the
    # six combining sign forms of the breaker paper,
    # standing as their own token.
    # ------------------------------------------------------

    def test_r16_34_02_join_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d3 trace summary')))

    def test_r16_34_02_join_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d9 trace summary')))

    def test_r16_34_02_join_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e4 trace summary')))

    def test_r16_34_02_join_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e6 trace summary')))

    def test_r16_34_02_join_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e8 trace summary')))

    def test_r16_34_02_join_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e9 trace summary')))

    # ------------------------------------------------------
    # Defect forms of R16-34-02, subfamily (c): the
    # six aside forms in further supplement
    # punctuation bracket marks.
    # ------------------------------------------------------

    def test_r16_34_02_aside_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e57panel\u2e58 trace summary')))

    def test_r16_34_02_aside_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e59panel\u2e5a trace summary')))

    def test_r16_34_02_aside_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e5bpanel\u2e5c trace summary')))

    def test_r16_34_02_aside_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e50panel\u2e51 trace summary')))

    def test_r16_34_02_aside_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e52panel\u2e53 trace summary')))

    def test_r16_34_02_aside_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e53panel\u2e54 trace summary')))

    # ------------------------------------------------------
    # Defect forms of R16-34-02, subfamily (c): the
    # fifteen verb first prose clauses.
    # ------------------------------------------------------

    def test_r16_34_02_verbfirst_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Snicker panel trace summary')))

    def test_r16_34_02_verbfirst_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Chortle panel trace summary')))

    def test_r16_34_02_verbfirst_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Guffaw panel trace summary')))

    def test_r16_34_02_verbfirst_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Wince panel trace summary')))

    def test_r16_34_02_verbfirst_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Grimace panel trace summary')))

    def test_r16_34_02_verbfirst_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Scowl panel trace summary')))

    def test_r16_34_02_verbfirst_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Whimper panel trace summary')))

    def test_r16_34_02_verbfirst_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Whine panel trace summary')))

    def test_r16_34_02_verbfirst_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Mutter panel trace summary')))

    def test_r16_34_02_verbfirst_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Stutter panel trace summary')))

    def test_r16_34_02_verbfirst_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Blubber panel trace summary')))

    def test_r16_34_02_verbfirst_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Cackle panel trace summary')))

    def test_r16_34_02_verbfirst_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Snigger panel trace summary')))

    def test_r16_34_02_verbfirst_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Titter panel trace summary')))

    def test_r16_34_02_verbfirst_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Whimper ledger trace summary')))

    # ------------------------------------------------------
    # Defect forms of R16-34-02: the gate ruling form
    # and the beside form of the first direct form of
    # the correctness paper.
    # ------------------------------------------------------

    def test_r16_34_02_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snicker trace summary'), ruling=True))

    def test_r16_34_02_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            'Panel snicker trace summary'))

    # ------------------------------------------------------
    # Adopted assertions of the round 34 breaker exhibit:
    # the gate ruling, beside and code level assertions
    # of B34-B02, in the forms the exhibit names them.
    # ------------------------------------------------------

    def test_b34_prose_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whimper trace summary'), ruling=True))

    def test_b34_prose_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            'Panel whimper trace summary'))

    def test_b34_code_level_prose_no_head(self):
        for run in ('Panel whimper trace summary',
                    'Clerk mutter summary trace',
                    'Panel whimper tracesummary',
                    'Clerk whimper traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelsummary',
                    'Ledger \u20d3 trace summary',
                    'Ledger \u20e9 trace summary',
                    'Ledger \u2e57panel\u2e58 trace summary',
                    'Whimper ledger trace summary'):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)

    # ------------------------------------------------------
    # Held controls of R16-34-02, standing missing in the
    # papers of this round in the same constructions, one
    # test per held form the register names.
    # ------------------------------------------------------

    def test_control_held_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sigh trace summary')))

    def test_control_held_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sob trace summary')))

    def test_control_held_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp trace summary')))

    def test_control_held_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gasp trace summary')))

    def test_control_held_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whisper trace summary')))

    def test_control_held_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel murmur trace summary')))

    def test_control_held_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tremble trace summary')))

    def test_control_held_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shudder trace summary')))

    def test_control_held_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk cower summary trace')))

    def test_control_held_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team grovel trace summary')))

    def test_control_held_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snivel trace summary')))

    def test_control_held_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22c8 trace summary')))

    def test_control_held_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22ca trace summary')))

    def test_control_held_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22cb trace summary')))

    def test_control_held_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u22cc trace summary')))

    def test_control_held_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29c8 trace summary')))

    def test_control_held_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u29c9 trace summary')))

    def test_control_held_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2985panel\u2986 trace summary')))

    def test_control_held_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u27e6panel\u27e7 trace summary')))

    def test_control_held_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \uff08panel\uff09 trace summary')))

    def test_control_held_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e15panel\u2e16 trace summary')))

    def test_control_held_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d4 trace summary')))

    def test_control_held_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d5 trace summary')))

    def test_control_held_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20d8 trace summary')))

    def test_control_held_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20da trace summary')))

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
            _prose('Ledger \u20e3 trace summary')))

    def test_control_held_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20e7 trace summary')))

    def test_control_held_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2045panel\u2046 trace summary')))

    def test_control_held_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \\\\ trace summary')))

    def test_control_held_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger || trace summary')))

    def test_control_held_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger * trace summary')))

    def test_control_held_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace board gate summary')))

    def test_control_held_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shrug trace board gate summary')))

    def test_control_held_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel yank trace board gate summary')))

    def test_control_held_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bore trace board gate summary')))

    def test_control_held_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk rode summary board gate trace')))

    def test_control_held_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fled trace board gate summary')))

    def test_control_held_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sought trace board gate summary')))

    def test_control_held_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel paid trace board gate summary')))

    def test_control_held_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chose trace board gate summary')))

    def test_control_held_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel reviewed trace board gate summary')))

    def test_control_held_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel logs trace board gate summary')))

    def test_control_held_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel bore traceboardgatereviewannexpanelboardgatereviewannexpanelsummary')))

    def test_control_held_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('The panel chose traceboardgatereviewannexpanelsummary')))

    def test_control_held_49_missing(self):
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
        self._candidate_governed(_bad('Round\'s trace summary'), _read('Round\'s trace summary'))

