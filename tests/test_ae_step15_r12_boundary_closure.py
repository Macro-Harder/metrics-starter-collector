"""Step 15 fix round 12 tests: boundary and closure family, F36 seat.

Each charged case pins one fix register item from the
confirmation round 11 papers. F15-96 (C11-1): the positional
closure join over-binds, a verb head (counts, states, shows,
lists), a lowercase name head (reyes noted) or an adverb head
(soon, yesterday) in the joiner position bounds the fragment
and counts a foreign closure, where the settled single
statement naming two steps prints not derivable. F15-97
(CB11-1): the positional join refuses to fire where any
punctuation stands later in its segment, an aside (parenthesis,
quote, bracket, comma) after the foreign Step naming, and a
hyphen inside a word in the rest of the segment. F15-98
(CB11-2): the positional guards defeat genuine joiners,
"provided Step 3 was recorded as" (the following Step guard)
and the multi word joiner "for fear" (the for exclusion), on
both sides. F15-99 (CB11-3): two completions in sequence
("(see Lane) for Step 3") leak the foreign step. F15-100
(CB11-4): et al. at a true sentence end never ends the
sentence, merging sentences and losing the own closure behind
"Yesterday," and digit openers. Control cases pin the
behaviour that must not move: the genuine positional joiners
of round 11 (provided, supposing, assuming, given,
notwithstanding, even though, in case, where), the completed
list joins, the article and capitalised head bounds, the
punctuation bound in the rest of a segment, the for Step
completion ground, the single completion forms, and the
joining abbreviation beside a governed name.
"""
import unittest

from metrics_starter_collector.derivation_core import (
    _dot_ends_sentence)
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, row_block,
                                     run_tool)

NOT_DERIVABLE_FIGURES = ("no rate figure; plain approvals 0; "
                         "qualified approvals 0; steps ruled on 0")
PLAIN_ONE_FIGURES = ("first-time approval rate 100 percent; "
                     "plain approvals 1; qualified approvals 0; "
                     "steps ruled on 1")
NOT_APPROVED_FIGURES = ("first-time approval rate 0 percent; "
                        "plain approvals 0; qualified approvals 0; "
                        "steps ruled on 1; Step 2 ruled and not "
                        "approved")


def record(text):
    return "# Step 2 gate record\n\n" + text + "\n"


def ends_at(text, token):
    pos = text.index(token) + len(token) - 1
    return _dot_ends_sentence(text, pos)


class TestStep15R12BoundaryClosure(FixtureTestCase):

    def _assert_f2_row(self, root, verdict, figures):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, verdict, "F-2")
        first_line = block.splitlines()[0]
        fields = [part.strip() for part in first_line.split("|")]
        self.assertEqual(fields[3], figures)
        return block

    def _f2_root(self, record_text):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = record(record_text)
        return build_tree(table)

    # ------------------------------------------------------------ F15-96

    def test_f15_96_verb_heads_do_not_bind(self):
        for verb in ("counts", "states", "shows", "lists"):
            with self.subTest(verb=verb):
                root = self._f2_root(
                    "The entry recorded as CLOSED-PASS " + verb
                    + " the Step 4 ruling recorded as CLOSED-FAIL.")
                self._assert_f2_row(root, "present but not derivable",
                                    NOT_DERIVABLE_FIGURES)

    def test_f15_96_lowercase_name_heads_do_not_bind(self):
        for head in ("reyes noted", "novak wrote"):
            with self.subTest(head=head):
                root = self._f2_root(
                    "The entry recorded as CLOSED-PASS " + head
                    + " the Step 4 ruling recorded as CLOSED-FAIL.")
                self._assert_f2_row(root, "present but not derivable",
                                    NOT_DERIVABLE_FIGURES)

    def test_f15_96_adverb_heads_do_not_bind(self):
        for adverb in ("soon", "yesterday"):
            with self.subTest(adverb=adverb):
                root = self._f2_root(
                    "The entry recorded as CLOSED-PASS " + adverb
                    + " the Step 4 ruling recorded as CLOSED-FAIL.")
                self._assert_f2_row(root, "present but not derivable",
                                    NOT_DERIVABLE_FIGURES)
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL soon the Step 3 "
            "ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_96_control_genuine_positional_joiners_still_bind(self):
        for join in ("provided", "supposing", "assuming", "given",
                     "notwithstanding", "even though", "in case"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "This record recorded as CLOSED-FAIL " + join
                    + " the Step 3 ruling recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)
        for join in ("provided", "where", "in case"):
            with self.subTest(join=join):
                root = self._f2_root(
                    "Closure state: CLOSED-PASS for Step 3 " + join
                    + " this record recorded as CLOSED-FAIL.")
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_96_control_settled_forms_hold(self):
        root = self._f2_root(
            "This record notes the Step 2 and Step 3 ruling, "
            "recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL since the Step 3 "
            "ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)
        root = self._f2_root(
            "The entry recorded as CLOSED-PASS the Step 4 ruling "
            "recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)
        root = self._f2_root(
            "The entry recorded as CLOSED-PASS Reyes the Step 4 "
            "ruling recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    # ------------------------------------------------------------ F15-97

    def test_f15_97_aside_after_step_naming_still_binds(self):
        frames = (
            "This record recorded as CLOSED-FAIL provided the "
            "Step 3 ruling (see Lane) recorded as CLOSED-PASS.",
            "This record recorded as CLOSED-FAIL provided the "
            "Step 3 ruling \"see Lane\" recorded as CLOSED-PASS.",
            "This record recorded as CLOSED-FAIL provided the "
            "Step 3 ruling [see Lane] recorded as CLOSED-PASS.",
            "This record recorded as CLOSED-FAIL provided the "
            "Step 3 ruling, see Lane, recorded as CLOSED-PASS.",
        )
        for frame in frames:
            with self.subTest(frame=frame):
                root = self._f2_root(frame)
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_97_hyphen_inside_word_still_binds(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL provided the "
            "well-known Step 3 ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)
        root = self._f2_root(
            "Closure state: CLOSED-PASS for Step 3 provided the "
            "well-known ruling of this record recorded as "
            "CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_97_control_punctuation_bound_before_step_governs(self):
        root = self._f2_root(
            "This record notes a ruling recorded as CLOSED-PASS "
            "by Reyes for Step 3, recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL duly noted: the "
            "Step 4 ruling recorded as CLOSED-QUALIFIED.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    # ------------------------------------------------------------ F15-98

    def test_f15_98_provided_step_subject_still_binds(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL provided Step 3 "
            "was recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_98_for_fear_binds_both_sides(self):
        root = self._f2_root(
            "This record recorded as CLOSED-FAIL for fear the "
            "Step 3 ruling recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)
        root = self._f2_root(
            "Closure state: CLOSED-PASS for Step 3 for fear this "
            "record recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_98_control_for_step_completion_is_no_join(self):
        root = self._f2_root("Closure state: CLOSED-PASS for Step 2.")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)
        root = self._f2_root(
            "Closure state: CLOSED-PASS at Step 4 this entry "
            "recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    # ------------------------------------------------------------ F15-99

    def test_f15_99_two_completions_in_sequence_do_not_leak(self):
        frames = (
            "Closure state: CLOSED-PASS (see Lane) for Step 3 "
            "this record recorded as CLOSED-FAIL.",
            "Closure state: CLOSED-PASS [see Lane] for Step 3 "
            "this record recorded as CLOSED-FAIL.",
        )
        for frame in frames:
            with self.subTest(frame=frame):
                root = self._f2_root(frame)
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_99_control_single_completions_hold(self):
        root = self._f2_root(
            "Closure state: CLOSED-PASS [for Step 3] this record "
            "recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)
        root = self._f2_root(
            "Closure state: CLOSED-PASS for Step 3 this record "
            "recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    # ----------------------------------------------------------- F15-100

    def test_f15_100_et_al_sentence_end_direct(self):
        cases = (
            ("filed by Lane et al. Yesterday it stood", "al.", True),
            ("filed by Lane viz. Yesterday it stood", "viz.", True),
            ("filed by Lane a.k.a. Yesterday it stood", "a.k.a.",
             True),
            ("filed by Lane et al. 5 hours later, this record",
             "al.", True),
            # Standing joining forms that must not move.
            ("given by Lane et al. Grant, recorded", "al.", False),
            ("given by Lane et al. grant, recorded", "al.", False),
            ("given by Lane viz. Grant, recorded", "viz.", False),
            ("given by Lane et al.", "al.", True),
        )
        for text, token, expected in cases:
            with self.subTest(text=text, token=token):
                self.assertEqual(ends_at(text, token), expected)

    def test_f15_100_et_al_sentence_end_frames_count_own_fail(self):
        frames = (
            "The Step 3 ruling was filed by Lane et al. Yesterday, "
            "this record was recorded as CLOSED-FAIL.",
            "The Step 3 ruling was filed by Lane et al. 5 hours "
            "later, this record was recorded as CLOSED-FAIL.",
        )
        for frame in frames:
            with self.subTest(frame=frame):
                root = self._f2_root(frame)
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_100_control_joining_beside_name_holds(self):
        root = self._f2_root(
            "This record notes the Step 2 ruling, Lane et al. "
            "Grant, recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)
        root = self._f2_root(
            "This record notes the Step 3 ruling, Lane et al. "
            "Grant, recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)


if __name__ == "__main__":
    unittest.main()
