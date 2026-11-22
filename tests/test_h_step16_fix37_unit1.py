"""Step 16 fix pass 37 unit 1 tests: the Q-4 closing unit.

Pinning tests for register item R16-37-02 (Medium, B37-C02
and B37-B02) of Step 16 round 37. The governing rule of
the pass, in its extended form: a piece not read in full,
for whatever reason, is not read, and its converse: a
piece that is no feeder flips nothing.

R16-37-02: the direct trace summary closing limb and the
fused closing limb of _tally_statement_head read what
stands before the closing words through the standing test
of fix pass 36 Unit 1 as restated, which reads a main verb
in its base form and its irregular forms only where the
word stands in the widened closed constant
_MAIN_VERB_WORDS at nine hundred and nine forms,
beside the ed and ing ending test and the s ending read
in general, and reads a prose run join only in the token
shapes the earlier passes and fix pass 36 landed and a
prose aside only in the shapes those passes landed, and
a clause break only in the comma, semicolon and colon
shapes, so prose standing before a direct or fused
closing in the shapes of this round takes a tally
statement head and stands present but not derivable,
against the restated boundary of fix pass 36 Unit 1
itself in its stated terms, which states the main verb
limb in terms as any inflection of a main verb and the
join and aside limbs in terms as a prose run join or a
prose aside standing before the closing words. Two
hundred and sixty six distinct alone forms stand driven
in three subfamilies: (a) prose sentences whose closing
words stand in the direct trace summary form, forty two
forms, thirty seven of the correctness paper over the
verbs glance, amble, vault, nudge, poke, flinch, rock,
snap, chant, recite, declare, announce, proclaim,
inscribe, dodge, plunge, lunge, surge, drift, float,
glide, slither, wriggle, squirm, fidget, twitch, jerk,
jolt, bump, trip, glower, peep, ogle, gawk, gape, slumber
and snooze with the Panel subject, and six of the
breaker paper over flinch, cringe, amble, dodge, plunge
and recoil in their own subjects and closing orders, the
direct form over the verb flinch in its Panel subject
shape standing shared, overlaps 1 in this subfamily; (b)
prose sentences whose last word stands in a fused trace
summary form, forty two forms, thirty seven of the
correctness paper in the plain fused form over the same
thirty seven verbs and six of the breaker paper standing
as the direct fused form, the reversed fused form, the
fused form behind a prefix, the fused between form with
two governed words fused between the closing words, the
fused between form at twenty three governed words fused
between the closing words, the count fix pass 36 Unit 2
widened to, and the fused form built on a summary form
that widening admitted, the plain fused form over the
verb flinch standing shared, overlaps 1 in this
subfamily; and (c) prose standing before a governed
closing inside one statement, one hundred and eighty two
forms, one hundred and seventy eight of the correctness
paper standing as ninety three prose runs joined by a
sign token standing as its own token at codepoints
U+2B00 through U+2B5F, standing past the three tokens of
that range the cure of fix pass 36 read at U+2B30,
U+2B31 and U+2B32, thirty two prose runs joined by a
combining diacritical extended token at codepoints
U+1AB0 through U+1ABF, sixteen standing as their own
token and sixteen standing on their host letter, sixteen
prose runs carrying an aside in further supplement
punctuation marks at the mark pairs U+2E60 and U+2E61,
U+2E62 and U+2E63, U+2E64 and U+2E65, U+2E66 and U+2E67,
U+2E68 and U+2E69, U+2E6A and U+2E6B, U+2E6C and U+2E6D,
U+2E6E and U+2E6F, U+2E70 and U+2E71, U+2E72 and U+2E73,
U+2E74 and U+2E75, U+2E76 and U+2E77, U+2E78 and U+2E79,
U+2E7A and U+2E7B, U+2E7C and U+2E7D, and U+2E7E and
U+2E7F, and thirty seven prose clauses in verb first form
over the panel subject in the base verb shapes of
subfamily (a), and eight of the breaker paper standing
as three prose runs joined by a sign token at codepoints
U+2B00, U+2B03 and U+2B35, standing shared with the sign
forms of the correctness paper, one prose run joined by
a combining enclosing sign token standing as its own
token at codepoint U+20F3, one prose run joined by a
combining enclosing sign token standing on its host
letter at codepoint U+20F4, one prose run joined by a
presentation form sign token standing as its own token
at codepoint U+FE30, one prose run carrying an aside in
supplement punctuation bracket marks at codepoints
U+2E60 and U+2E61, standing shared with the aside forms
of the correctness paper, overlaps 4 in this subfamily,
and one prose clause in verb first form over the ledger
subject. Gross two hundred and seventy two driven forms,
overlaps 6, two hundred and sixty six distinct alone
forms in all. The Panel glance trace summary line of the
correctness paper stands joined by a gate ruling form and
a beside form, and the Panel flinch trace summary line of
the breaker paper stands joined by a gate ruling form and
a beside form, each alone form standing present but not
derivable on the entering bytes, naming Step 2 and the
feeder piece. The twenty three converse assertions of the
round 37 breaker exhibit stand adopted in this module:
the twenty alone forms of B37-B02 stand among the defect
tests of the subfamilies above in their driven words,
and the gate ruling assertion, the beside assertion and
the code level assertion of that exhibit stand as defect
tests here in the forms the exhibit names them. The
defect stands bounded in the open by its held controls:
the ninety candidate verbs of the correctness paper
standing read as main verbs in the same screening drive,
whisper, murmur, mutter, gasp, sigh and strike among
them, standing missing in their driven sentences; the
prose sentences of the breaker paper over the verbs
tremble, shiver, quiver and wobble standing missing in
their driven shapes, the tremble sentence standing among
the candidate verbs above in the same form; the sign
joins at codepoints U+2B30, U+2B31 and U+2B32 of the
correctness paper standing in no defect form of this
round, each standing missing in its regrade drives; the
aside pairs of the breaker paper at codepoints U+2E50
and U+2E51, at U+2E52 and U+2E53, at U+2E59 and U+2E5A
and at U+2E5B and U+2E5C standing in no defect form of
this round; and every governed neighbour standing at its
recorded standing.
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


class TestStep16Fix37Unit1(FixtureTestCase):


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
    # Defect forms of R16-37-02, subfamily (a): the
    # forty two direct prose sentences.
    # ------------------------------------------------------

    def test_r16_37_02_direct_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glance trace summary')))

    def test_r16_37_02_direct_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel amble trace summary')))

    def test_r16_37_02_direct_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel vault trace summary')))

    def test_r16_37_02_direct_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nudge trace summary')))

    def test_r16_37_02_direct_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel poke trace summary')))

    def test_r16_37_02_direct_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel flinch trace summary')))

    def test_r16_37_02_direct_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel rock trace summary')))

    def test_r16_37_02_direct_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snap trace summary')))

    def test_r16_37_02_direct_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chant trace summary')))

    def test_r16_37_02_direct_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel recite trace summary')))

    def test_r16_37_02_direct_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel declare trace summary')))

    def test_r16_37_02_direct_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel announce trace summary')))

    def test_r16_37_02_direct_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel proclaim trace summary')))

    def test_r16_37_02_direct_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel inscribe trace summary')))

    def test_r16_37_02_direct_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel dodge trace summary')))

    def test_r16_37_02_direct_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel plunge trace summary')))

    def test_r16_37_02_direct_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lunge trace summary')))

    def test_r16_37_02_direct_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel surge trace summary')))

    def test_r16_37_02_direct_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel drift trace summary')))

    def test_r16_37_02_direct_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel float trace summary')))

    def test_r16_37_02_direct_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glide trace summary')))

    def test_r16_37_02_direct_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel slither trace summary')))

    def test_r16_37_02_direct_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wriggle trace summary')))

    def test_r16_37_02_direct_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel squirm trace summary')))

    def test_r16_37_02_direct_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fidget trace summary')))

    def test_r16_37_02_direct_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twitch trace summary')))

    def test_r16_37_02_direct_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel jerk trace summary')))

    def test_r16_37_02_direct_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel jolt trace summary')))

    def test_r16_37_02_direct_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bump trace summary')))

    def test_r16_37_02_direct_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel trip trace summary')))

    def test_r16_37_02_direct_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glower trace summary')))

    def test_r16_37_02_direct_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel peep trace summary')))

    def test_r16_37_02_direct_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel ogle trace summary')))

    def test_r16_37_02_direct_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gawk trace summary')))

    def test_r16_37_02_direct_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gape trace summary')))

    def test_r16_37_02_direct_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel slumber trace summary')))

    def test_r16_37_02_direct_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snooze trace summary')))

    def test_r16_37_02_direct_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk cringe summary trace')))

    def test_r16_37_02_direct_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team amble trace summary')))

    def test_r16_37_02_direct_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel dodge summary trace')))

    def test_r16_37_02_direct_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk plunge trace summary')))

    def test_r16_37_02_direct_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team recoil summary trace')))



    # ------------------------------------------------------
    # Defect forms of R16-37-02, subfamily (b): the
    # forty two fused prose sentences.
    # ------------------------------------------------------

    def test_r16_37_02_fused_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glance tracesummary')))

    def test_r16_37_02_fused_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel amble tracesummary')))

    def test_r16_37_02_fused_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel vault tracesummary')))

    def test_r16_37_02_fused_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nudge tracesummary')))

    def test_r16_37_02_fused_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel poke tracesummary')))

    def test_r16_37_02_fused_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel flinch tracesummary')))

    def test_r16_37_02_fused_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel rock tracesummary')))

    def test_r16_37_02_fused_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snap tracesummary')))

    def test_r16_37_02_fused_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chant tracesummary')))

    def test_r16_37_02_fused_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel recite tracesummary')))

    def test_r16_37_02_fused_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel declare tracesummary')))

    def test_r16_37_02_fused_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel announce tracesummary')))

    def test_r16_37_02_fused_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel proclaim tracesummary')))

    def test_r16_37_02_fused_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel inscribe tracesummary')))

    def test_r16_37_02_fused_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel dodge tracesummary')))

    def test_r16_37_02_fused_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel plunge tracesummary')))

    def test_r16_37_02_fused_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lunge tracesummary')))

    def test_r16_37_02_fused_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel surge tracesummary')))

    def test_r16_37_02_fused_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel drift tracesummary')))

    def test_r16_37_02_fused_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel float tracesummary')))

    def test_r16_37_02_fused_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glide tracesummary')))

    def test_r16_37_02_fused_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel slither tracesummary')))

    def test_r16_37_02_fused_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wriggle tracesummary')))

    def test_r16_37_02_fused_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel squirm tracesummary')))

    def test_r16_37_02_fused_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel fidget tracesummary')))

    def test_r16_37_02_fused_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twitch tracesummary')))

    def test_r16_37_02_fused_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel jerk tracesummary')))

    def test_r16_37_02_fused_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel jolt tracesummary')))

    def test_r16_37_02_fused_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bump tracesummary')))

    def test_r16_37_02_fused_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel trip tracesummary')))

    def test_r16_37_02_fused_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glower tracesummary')))

    def test_r16_37_02_fused_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel peep tracesummary')))

    def test_r16_37_02_fused_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel ogle tracesummary')))

    def test_r16_37_02_fused_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gawk tracesummary')))

    def test_r16_37_02_fused_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gape tracesummary')))

    def test_r16_37_02_fused_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel slumber tracesummary')))

    def test_r16_37_02_fused_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel snooze tracesummary')))

    def test_r16_37_02_fused_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk cringe summarytrace')))

    def test_r16_37_02_fused_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team amble boardtracesummary')))

    def test_r16_37_02_fused_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel dodge traceboardgatesummary')))

    def test_r16_37_02_fused_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk flinch traceboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewannexpanelboardgatereviewsummary')))

    def test_r16_37_02_fused_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team cringe tracesummarisationeseseseseseseseseseseseseseseseseses')))



    # ------------------------------------------------------
    # Defect forms of R16-37-02, subfamily (c): the
    # ninety three sign token join forms of the
    # correctness paper.
    # ------------------------------------------------------

    def test_r16_37_02_join_000_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b00 trace summary')))

    def test_r16_37_02_join_001_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b01 trace summary')))

    def test_r16_37_02_join_002_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b02 trace summary')))

    def test_r16_37_02_join_003_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b03 trace summary')))

    def test_r16_37_02_join_004_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b04 trace summary')))

    def test_r16_37_02_join_005_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b05 trace summary')))

    def test_r16_37_02_join_006_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b06 trace summary')))

    def test_r16_37_02_join_007_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b07 trace summary')))

    def test_r16_37_02_join_008_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b08 trace summary')))

    def test_r16_37_02_join_009_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b09 trace summary')))

    def test_r16_37_02_join_010_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b0a trace summary')))

    def test_r16_37_02_join_011_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b0b trace summary')))

    def test_r16_37_02_join_012_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b0c trace summary')))

    def test_r16_37_02_join_013_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b0d trace summary')))

    def test_r16_37_02_join_014_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b0e trace summary')))

    def test_r16_37_02_join_015_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b0f trace summary')))

    def test_r16_37_02_join_016_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b10 trace summary')))

    def test_r16_37_02_join_017_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b11 trace summary')))

    def test_r16_37_02_join_018_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b12 trace summary')))

    def test_r16_37_02_join_019_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b13 trace summary')))

    def test_r16_37_02_join_020_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b14 trace summary')))

    def test_r16_37_02_join_021_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b15 trace summary')))

    def test_r16_37_02_join_022_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b16 trace summary')))

    def test_r16_37_02_join_023_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b17 trace summary')))

    def test_r16_37_02_join_024_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b18 trace summary')))

    def test_r16_37_02_join_025_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b19 trace summary')))

    def test_r16_37_02_join_026_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b1a trace summary')))

    def test_r16_37_02_join_027_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b1b trace summary')))

    def test_r16_37_02_join_028_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b1c trace summary')))

    def test_r16_37_02_join_029_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b1d trace summary')))

    def test_r16_37_02_join_030_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b1e trace summary')))

    def test_r16_37_02_join_031_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b1f trace summary')))

    def test_r16_37_02_join_032_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b20 trace summary')))

    def test_r16_37_02_join_033_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b21 trace summary')))

    def test_r16_37_02_join_034_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b22 trace summary')))

    def test_r16_37_02_join_035_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b23 trace summary')))

    def test_r16_37_02_join_036_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b24 trace summary')))

    def test_r16_37_02_join_037_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b25 trace summary')))

    def test_r16_37_02_join_038_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b26 trace summary')))

    def test_r16_37_02_join_039_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b27 trace summary')))

    def test_r16_37_02_join_040_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b28 trace summary')))

    def test_r16_37_02_join_041_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b29 trace summary')))

    def test_r16_37_02_join_042_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b2a trace summary')))

    def test_r16_37_02_join_043_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b2b trace summary')))

    def test_r16_37_02_join_044_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b2c trace summary')))

    def test_r16_37_02_join_045_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b2d trace summary')))

    def test_r16_37_02_join_046_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b2e trace summary')))

    def test_r16_37_02_join_047_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b2f trace summary')))

    def test_r16_37_02_join_048_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b33 trace summary')))

    def test_r16_37_02_join_049_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b34 trace summary')))

    def test_r16_37_02_join_050_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b35 trace summary')))

    def test_r16_37_02_join_051_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b36 trace summary')))

    def test_r16_37_02_join_052_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b37 trace summary')))

    def test_r16_37_02_join_053_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b38 trace summary')))

    def test_r16_37_02_join_054_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b39 trace summary')))

    def test_r16_37_02_join_055_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b3a trace summary')))

    def test_r16_37_02_join_056_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b3b trace summary')))

    def test_r16_37_02_join_057_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b3c trace summary')))

    def test_r16_37_02_join_058_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b3d trace summary')))

    def test_r16_37_02_join_059_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b3e trace summary')))

    def test_r16_37_02_join_060_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b3f trace summary')))

    def test_r16_37_02_join_061_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b40 trace summary')))

    def test_r16_37_02_join_062_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b41 trace summary')))

    def test_r16_37_02_join_063_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b42 trace summary')))

    def test_r16_37_02_join_064_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b43 trace summary')))

    def test_r16_37_02_join_065_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b44 trace summary')))

    def test_r16_37_02_join_066_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b45 trace summary')))

    def test_r16_37_02_join_067_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b46 trace summary')))

    def test_r16_37_02_join_068_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b47 trace summary')))

    def test_r16_37_02_join_069_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b48 trace summary')))

    def test_r16_37_02_join_070_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b49 trace summary')))

    def test_r16_37_02_join_071_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b4a trace summary')))

    def test_r16_37_02_join_072_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b4b trace summary')))

    def test_r16_37_02_join_073_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b4c trace summary')))

    def test_r16_37_02_join_074_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b4d trace summary')))

    def test_r16_37_02_join_075_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b4e trace summary')))

    def test_r16_37_02_join_076_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b4f trace summary')))

    def test_r16_37_02_join_077_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b50 trace summary')))

    def test_r16_37_02_join_078_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b51 trace summary')))

    def test_r16_37_02_join_079_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b52 trace summary')))

    def test_r16_37_02_join_080_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b53 trace summary')))

    def test_r16_37_02_join_081_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b54 trace summary')))

    def test_r16_37_02_join_082_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b55 trace summary')))

    def test_r16_37_02_join_083_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b56 trace summary')))

    def test_r16_37_02_join_084_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b57 trace summary')))

    def test_r16_37_02_join_085_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b58 trace summary')))

    def test_r16_37_02_join_086_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b59 trace summary')))

    def test_r16_37_02_join_087_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b5a trace summary')))

    def test_r16_37_02_join_088_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b5b trace summary')))

    def test_r16_37_02_join_089_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b5c trace summary')))

    def test_r16_37_02_join_090_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b5d trace summary')))

    def test_r16_37_02_join_091_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b5e trace summary')))

    def test_r16_37_02_join_092_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b5f trace summary')))



    # ------------------------------------------------------
    # Defect forms of R16-37-02, subfamily (c): the
    # thirty two combining diacritical extended
    # join forms of the correctness paper, sixteen
    # standing as their own token and sixteen
    # standing on their host letter.
    # ------------------------------------------------------

    def test_r16_37_02_join_093_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1ab0 trace summary')))

    def test_r16_37_02_join_094_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1ab1 trace summary')))

    def test_r16_37_02_join_095_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1ab2 trace summary')))

    def test_r16_37_02_join_096_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1ab3 trace summary')))

    def test_r16_37_02_join_097_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1ab4 trace summary')))

    def test_r16_37_02_join_098_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1ab5 trace summary')))

    def test_r16_37_02_join_099_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1ab6 trace summary')))

    def test_r16_37_02_join_100_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1ab7 trace summary')))

    def test_r16_37_02_join_101_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1ab8 trace summary')))

    def test_r16_37_02_join_102_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1ab9 trace summary')))

    def test_r16_37_02_join_103_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1aba trace summary')))

    def test_r16_37_02_join_104_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1abb trace summary')))

    def test_r16_37_02_join_105_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1abc trace summary')))

    def test_r16_37_02_join_106_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1abd trace summary')))

    def test_r16_37_02_join_107_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1abe trace summary')))

    def test_r16_37_02_join_108_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u1abf trace summary')))

    def test_r16_37_02_join_109_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1ab0 trace summary')))

    def test_r16_37_02_join_110_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1ab1 trace summary')))

    def test_r16_37_02_join_111_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1ab2 trace summary')))

    def test_r16_37_02_join_112_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1ab3 trace summary')))

    def test_r16_37_02_join_113_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1ab4 trace summary')))

    def test_r16_37_02_join_114_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1ab5 trace summary')))

    def test_r16_37_02_join_115_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1ab6 trace summary')))

    def test_r16_37_02_join_116_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1ab7 trace summary')))

    def test_r16_37_02_join_117_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1ab8 trace summary')))

    def test_r16_37_02_join_118_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1ab9 trace summary')))

    def test_r16_37_02_join_119_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1aba trace summary')))

    def test_r16_37_02_join_120_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1abb trace summary')))

    def test_r16_37_02_join_121_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1abc trace summary')))

    def test_r16_37_02_join_122_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1abd trace summary')))

    def test_r16_37_02_join_123_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1abe trace summary')))

    def test_r16_37_02_join_124_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u1abf trace summary')))



    # ------------------------------------------------------
    # Defect forms of R16-37-02, subfamily (c): the
    # three further join forms of the breaker paper,
    # the combining enclosing sign at codepoint
    # U+20F3 standing as its own token, the combining
    # enclosing sign at codepoint U+20F4 standing on
    # its host letter, and the presentation form
    # sign at codepoint U+FE30 standing as its own
    # token.
    # ------------------------------------------------------

    def test_r16_37_02_join_125_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u20f3 trace summary')))

    def test_r16_37_02_join_126_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger x\u20f4 trace summary')))

    def test_r16_37_02_join_127_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \ufe30 trace summary')))



    # ------------------------------------------------------
    # Defect forms of R16-37-02, subfamily (c): the
    # sixteen aside forms in further supplement
    # punctuation bracket marks.
    # ------------------------------------------------------

    def test_r16_37_02_aside_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e60panel\u2e61 trace summary')))

    def test_r16_37_02_aside_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e62panel\u2e63 trace summary')))

    def test_r16_37_02_aside_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e64panel\u2e65 trace summary')))

    def test_r16_37_02_aside_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e66panel\u2e67 trace summary')))

    def test_r16_37_02_aside_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e68panel\u2e69 trace summary')))

    def test_r16_37_02_aside_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e6apanel\u2e6b trace summary')))

    def test_r16_37_02_aside_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e6cpanel\u2e6d trace summary')))

    def test_r16_37_02_aside_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e6epanel\u2e6f trace summary')))

    def test_r16_37_02_aside_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e70panel\u2e71 trace summary')))

    def test_r16_37_02_aside_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e72panel\u2e73 trace summary')))

    def test_r16_37_02_aside_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e74panel\u2e75 trace summary')))

    def test_r16_37_02_aside_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e76panel\u2e77 trace summary')))

    def test_r16_37_02_aside_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e78panel\u2e79 trace summary')))

    def test_r16_37_02_aside_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e7apanel\u2e7b trace summary')))

    def test_r16_37_02_aside_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e7cpanel\u2e7d trace summary')))

    def test_r16_37_02_aside_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e7epanel\u2e7f trace summary')))



    # ------------------------------------------------------
    # Defect forms of R16-37-02, subfamily (c): the
    # thirty eight verb first prose clauses.
    # ------------------------------------------------------

    def test_r16_37_02_verbfirst_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Glance panel trace summary')))

    def test_r16_37_02_verbfirst_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Amble panel trace summary')))

    def test_r16_37_02_verbfirst_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Vault panel trace summary')))

    def test_r16_37_02_verbfirst_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Nudge panel trace summary')))

    def test_r16_37_02_verbfirst_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Poke panel trace summary')))

    def test_r16_37_02_verbfirst_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Flinch panel trace summary')))

    def test_r16_37_02_verbfirst_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Rock panel trace summary')))

    def test_r16_37_02_verbfirst_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Snap panel trace summary')))

    def test_r16_37_02_verbfirst_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Chant panel trace summary')))

    def test_r16_37_02_verbfirst_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Recite panel trace summary')))

    def test_r16_37_02_verbfirst_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Declare panel trace summary')))

    def test_r16_37_02_verbfirst_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Announce panel trace summary')))

    def test_r16_37_02_verbfirst_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Proclaim panel trace summary')))

    def test_r16_37_02_verbfirst_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Inscribe panel trace summary')))

    def test_r16_37_02_verbfirst_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Dodge panel trace summary')))

    def test_r16_37_02_verbfirst_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Plunge panel trace summary')))

    def test_r16_37_02_verbfirst_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Lunge panel trace summary')))

    def test_r16_37_02_verbfirst_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Surge panel trace summary')))

    def test_r16_37_02_verbfirst_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Drift panel trace summary')))

    def test_r16_37_02_verbfirst_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Float panel trace summary')))

    def test_r16_37_02_verbfirst_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Glide panel trace summary')))

    def test_r16_37_02_verbfirst_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Slither panel trace summary')))

    def test_r16_37_02_verbfirst_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Wriggle panel trace summary')))

    def test_r16_37_02_verbfirst_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Squirm panel trace summary')))

    def test_r16_37_02_verbfirst_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Fidget panel trace summary')))

    def test_r16_37_02_verbfirst_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Twitch panel trace summary')))

    def test_r16_37_02_verbfirst_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Jerk panel trace summary')))

    def test_r16_37_02_verbfirst_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Jolt panel trace summary')))

    def test_r16_37_02_verbfirst_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Bump panel trace summary')))

    def test_r16_37_02_verbfirst_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Trip panel trace summary')))

    def test_r16_37_02_verbfirst_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Glower panel trace summary')))

    def test_r16_37_02_verbfirst_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Peep panel trace summary')))

    def test_r16_37_02_verbfirst_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ogle panel trace summary')))

    def test_r16_37_02_verbfirst_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Gawk panel trace summary')))

    def test_r16_37_02_verbfirst_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Gape panel trace summary')))

    def test_r16_37_02_verbfirst_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Slumber panel trace summary')))

    def test_r16_37_02_verbfirst_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Snooze panel trace summary')))

    def test_r16_37_02_verbfirst_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Flinch ledger trace summary')))



    # ------------------------------------------------------
    # Defect forms of R16-37-02: the gate ruling form
    # and the beside form of the first direct form of
    # the correctness paper.
    # ------------------------------------------------------

    def test_r16_37_02_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel glance trace summary'), ruling=True))

    def test_r16_37_02_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            'Panel glance trace summary'))



    # ------------------------------------------------------
    # Adopted assertions of the round 37 breaker exhibit:
    # the gate ruling, beside and code level assertions
    # of B37-B02, in the forms the exhibit names them.
    # ------------------------------------------------------

    def test_b37_prose_direct_gate_ruling(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel flinch trace summary'), ruling=True))

    def test_b37_prose_direct_beside(self):
        self._beside_step2_nowhere(_prose(
            'Panel flinch trace summary'))

    def test_b37_code_level_prose_no_head(self):
        for run in ("Panel flinch trace summary",
                    "Clerk cringe summary trace",
                    "Panel flinch tracesummary",
                    'Ledger \u2b00 trace summary',
                    'Ledger \u20f3 trace summary',
                    'Ledger \u2e60panel\u2e61 trace summary',
                    "Flinch ledger trace summary"):
            line = run + ": LANDED figures stand here"
            self.assertFalse(_tally_statement_head(line), run)


    # ------------------------------------------------------
    # Held controls of R16-37-02, standing missing in the
    # papers of this round in the same constructions, one
    # test per held form the register names: the ninety
    # candidate verbs of the correctness paper in the
    # direct form.
    # ------------------------------------------------------

    def test_control_held_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whisper trace summary')))

    def test_control_held_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel murmur trace summary')))

    def test_control_held_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel mutter trace summary')))

    def test_control_held_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gasp trace summary')))

    def test_control_held_04_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sigh trace summary')))

    def test_control_held_05_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sob trace summary')))

    def test_control_held_06_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel smirk trace summary')))

    def test_control_held_07_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel frown trace summary')))

    def test_control_held_08_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel peer trace summary')))

    def test_control_held_09_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel squint trace summary')))

    def test_control_held_10_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel stroll trace summary')))

    def test_control_held_11_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel limp trace summary')))

    def test_control_held_12_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel toss trace summary')))

    def test_control_held_13_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel catch trace summary')))

    def test_control_held_14_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tap trace summary')))

    def test_control_held_15_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wave trace summary')))

    def test_control_held_16_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel beckon trace summary')))

    def test_control_held_17_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel kneel trace summary')))

    def test_control_held_18_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel crouch trace summary')))

    def test_control_held_19_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wince trace summary')))

    def test_control_held_20_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shudder trace summary')))

    def test_control_held_21_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tremble trace summary')))

    def test_control_held_22_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sway trace summary')))

    def test_control_held_23_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel spin trace summary')))

    def test_control_held_24_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel twirl trace summary')))

    def test_control_held_25_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bow trace summary')))

    def test_control_held_26_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel nod trace summary')))

    def test_control_held_27_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel clap trace summary')))

    def test_control_held_28_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel whistle trace summary')))

    def test_control_held_29_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hum trace summary')))

    def test_control_held_30_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel record trace summary')))

    def test_control_held_31_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel count trace summary')))

    def test_control_held_32_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel mark trace summary')))

    def test_control_held_33_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel note trace summary')))

    def test_control_held_34_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel list trace summary')))

    def test_control_held_35_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel enter trace summary')))

    def test_control_held_36_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel file trace summary')))

    def test_control_held_37_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel seal trace summary')))

    def test_control_held_38_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sign trace summary')))

    def test_control_held_39_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel attest trace summary')))

    def test_control_held_40_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel verify trace summary')))

    def test_control_held_41_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel audit trace summary')))

    def test_control_held_42_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel check trace summary')))

    def test_control_held_43_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel review trace summary')))

    def test_control_held_44_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel dive trace summary')))

    def test_control_held_45_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel falter trace summary')))

    def test_control_held_46_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel pout trace summary')))

    def test_control_held_47_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grin trace summary')))

    def test_control_held_48_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel grimace trace summary')))

    def test_control_held_49_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel scowl trace summary')))

    def test_control_held_50_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel peek trace summary')))

    def test_control_held_51_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel blow trace summary')))

    def test_control_held_52_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sniff trace summary')))

    def test_control_held_53_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel chew trace summary')))

    def test_control_held_54_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel bite trace summary')))

    def test_control_held_55_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lick trace summary')))

    def test_control_held_56_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sip trace summary')))

    def test_control_held_57_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel gulp trace summary')))

    def test_control_held_58_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel eat trace summary')))

    def test_control_held_59_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel drink trace summary')))

    def test_control_held_60_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel hear trace summary')))

    def test_control_held_61_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel squeeze trace summary')))

    def test_control_held_62_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel dig trace summary')))

    def test_control_held_63_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sweep trace summary')))

    def test_control_held_64_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel open trace summary')))

    def test_control_held_65_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel shut trace summary')))

    def test_control_held_66_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel close trace summary')))

    def test_control_held_67_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel call trace summary')))

    def test_control_held_68_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel ask trace summary')))

    def test_control_held_69_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel tell trace summary')))

    def test_control_held_70_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel say trace summary')))

    def test_control_held_71_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel speak trace summary')))

    def test_control_held_72_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel talk trace summary')))

    def test_control_held_73_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel read trace summary')))

    def test_control_held_74_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel write trace summary')))

    def test_control_held_75_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel sing trace summary')))

    def test_control_held_76_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wait trace summary')))

    def test_control_held_77_missing(self):
        self._assert_q4_governed(self._q4_alone(
            _prose('Panel stay trace summary')))

    def test_control_held_78_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel leave trace summary')))

    def test_control_held_79_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel pass trace summary')))

    def test_control_held_80_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel cross trace summary')))

    def test_control_held_81_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel follow trace summary')))

    def test_control_held_82_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lead trace summary')))

    def test_control_held_83_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel pull trace summary')))

    def test_control_held_84_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel push trace summary')))

    def test_control_held_85_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel lift trace summary')))

    def test_control_held_86_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel carry trace summary')))

    def test_control_held_87_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel throw trace summary')))

    def test_control_held_88_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel kick trace summary')))

    def test_control_held_89_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel strike trace summary')))



    # ------------------------------------------------------
    # Held controls of R16-37-02: the prose sentences of
    # the breaker paper over the verbs shiver, quiver
    # and wobble in their driven shapes, the verb
    # tremble of that paper standing among the ninety
    # candidate verbs above in the same form.
    # ------------------------------------------------------

    def test_control_held_90_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Clerk shiver summary trace')))

    def test_control_held_91_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Team quiver trace summary')))

    def test_control_held_92_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Panel wobble summary trace')))



    # ------------------------------------------------------
    # Held controls of R16-37-02: the sign joins at
    # codepoints U+2B30, U+2B31 and U+2B32 of the
    # correctness paper, standing as their own token.
    # ------------------------------------------------------

    def test_control_sign_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b30 trace summary')))

    def test_control_sign_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b31 trace summary')))

    def test_control_sign_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2b32 trace summary')))



    # ------------------------------------------------------
    # Held controls of R16-37-02: the aside pairs of
    # the breaker paper at codepoints U+2E50 and
    # U+2E51, at U+2E52 and U+2E53, at U+2E59 and
    # U+2E5A and at U+2E5B and U+2E5C.
    # ------------------------------------------------------

    def test_control_aside_00_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e50panel\u2e51 trace summary')))

    def test_control_aside_01_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e52panel\u2e53 trace summary')))

    def test_control_aside_02_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e59panel\u2e5a trace summary')))

    def test_control_aside_03_missing(self):
        self._assert_q4_missing(self._q4_alone(
            _prose('Ledger \u2e5bpanel\u2e5c trace summary')))



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

