"""Step 15 fix round 9 tests: abbreviation classes, F24 seat.

Each charged case pins one fix register item in the boundary
machinery of derivation_core.py. F15-62 (CB8-1, CB8-2, C8-1):
the true end rule at _dot_ends_sentence rested on the closed
_SENTENCE_STARTERS list, so a sentence opening on a word
outside that list (Lane, Will, May, Grant, Finally, Our,
Yesterday, Meanwhile, Recorded) merged with the sentence
before an abbreviation stop and was lost, a surname standing
in the list after a title (Dr. He, Dr. An) made a false end,
and a dotted form whose first component is a multi letter
word (Ph.D., Ed.D., LL.D.) was cut at its own first stop; a
quoted sentence end closed by a parenthesis was no end at
all. F15-63 (C8-2): _clause_fragments broke at semicolons
and at true full stop ends only, so a step named in a
previous sentence ending in a question or exclamation mark
leaked into a mention's own clause part and governed the
T-4 attribution over the mention's own sentence. Control
cases pin the behaviour that must not move: a title before
a name mid sentence still holds its sentence together, an
abbreviation standing last in a passage still ends its
sentence, and the full stop twin of the F15-63 forms still
attributes to the recorded for step.
"""
import unittest

from metrics_starter_collector.derivation_core import (
    _dot_ends_sentence, _t4_banked_durations)
from tests.fixture_builder import (FixtureTestCase, assert_verdict,
                                     base_case, build_tree, gate_record,
                                     path_ledger, row_block, run_tool)

NOT_DERIVABLE_FIGURES = ("no rate figure; plain approvals 0; "
                         "qualified approvals 0; steps ruled on 0")
PLAIN_ONE_FIGURES = ("first-time approval rate 100 percent; "
                     "plain approvals 1; qualified approvals 0; "
                     "steps ruled on 1")
NOT_APPROVED_FIGURES = ("first-time approval rate 0 percent; "
                        "plain approvals 0; qualified approvals 0; "
                        "steps ruled on 1; Step 2 ruled and not "
                        "approved")

DATE_ONLY_LINE = "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.\n"
T4_MISSING_SHOWS = ("no banked state and no decision item count "
                    "stands in the feeder records for this metric")


def capture(root):
    from metrics_starter_collector.shell_reader import capture_read
    return capture_read(root)


def record(text):
    return "# Step 2 gate record\n\n" + text + "\n"


def ends_at(text, token):
    pos = text.index(token) + len(token) - 1
    return _dot_ends_sentence(text, pos)


class TestStep15Round9Boundary(FixtureTestCase):

    # ------------------------------------------------------------ F-2 side

    def _assert_f2_row(self, root, verdict, figures):
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        block = row_block(result.stdout, "F-2")
        assert_verdict(self, block, verdict, "F-2")
        first_line = block.splitlines()[0]
        fields = [part.strip() for part in first_line.split("|")]
        self.assertEqual(fields[3], figures)
        return block

    def _f2_root(self, record_text, adjudication=False):
        table = base_case(steps=(2,))
        table["steps/step-02-gate-record.md"] = record(record_text)
        if adjudication:
            table["steps/step-02-gate-adjudication.md"] = gate_record(
                2, "CLOSED-FAIL")
        return build_tree(table)

    # ------------------------------------------------------------ F15-62

    def test_f15_62_other_abbrev_unlisted_openers_closure_counts_own(self):
        frames = (
            "Lane noted this record was recorded as CLOSED-FAIL.",
            "Will Lane noted this record was recorded as "
            "CLOSED-FAIL.",
            "May Lane noted this record was recorded as CLOSED-FAIL.",
            "Grant Lane noted this record was recorded as "
            "CLOSED-FAIL.",
            "Finally, this record was recorded as CLOSED-FAIL.",
            "Our reviewer noted this record was recorded as "
            "CLOSED-FAIL.",
            "Yesterday, this record was recorded as CLOSED-FAIL.",
            "Meanwhile, this record was recorded as CLOSED-FAIL.",
            "Recorded below, this record was recorded as "
            "CLOSED-FAIL.",
        )
        for frame in frames:
            with self.subTest(frame=frame):
                root = self._f2_root(
                    "The Step 3 ruling was filed for the U.S. "
                    + frame)
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_62_other_abbrev_pm_unlisted_opener_closure_counts_own(self):
        for frame in (
                "Lane noted this record was recorded as CLOSED-FAIL.",
                "Finally, this record was recorded as CLOSED-FAIL."):
            with self.subTest(frame=frame):
                root = self._f2_root(
                    "The Step 3 ruling was filed at 5 p.m. " + frame)
                self._assert_f2_row(root, "present",
                                    NOT_APPROVED_FIGURES)

    def test_f15_62_title_before_starter_surname_closure_foreign(self):
        for naming in ("by Dr. He,", "by Dr. An,", "by Prof. He,",
                       "by Capt. An,"):
            with self.subTest(naming=naming):
                root = self._f2_root(
                    "This record notes the Step 3 ruling " + naming
                    + " recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present but not derivable",
                                    NOT_DERIVABLE_FIGURES)

    def test_f15_62_introducing_abbrev_before_capital_closure_foreign(self):
        for naming in (
                "by Lane, e.g. He was the reviewer,",
                "by Lane, i.e. He filed it,"):
            with self.subTest(naming=naming):
                root = self._f2_root(
                    "This record notes the Step 3 ruling " + naming
                    + " recorded as CLOSED-PASS.")
                self._assert_f2_row(root, "present but not derivable",
                                    NOT_DERIVABLE_FIGURES)

    def test_f15_62_dotted_multi_letter_closure_foreign(self):
        for naming in ("by Lane, Ph.D. recorded as",
                       "by Lane, Ed.D. recorded as",
                       "by Lane, LL.D. recorded as",
                       "by Ph.D. Lane, recorded as",
                       "by A. Lane, Ph.D., recorded as"):
            with self.subTest(naming=naming):
                root = self._f2_root(
                    "This record notes the Step 3 ruling " + naming
                    + " CLOSED-PASS.")
                self._assert_f2_row(root, "present but not derivable",
                                    NOT_DERIVABLE_FIGURES)

    def test_f15_62_dotted_multi_letter_with_fail_adjudication(self):
        root = self._f2_root(
            "This record notes the Step 3 ruling by Lane, Ph.D. "
            "recorded as CLOSED-PASS.", adjudication=True)
        self._assert_f2_row(root, "present but not derivable",
                            NOT_DERIVABLE_FIGURES)

    def test_f15_62_quoted_paren_end_closure_counts_own(self):
        root = self._f2_root(
            "The Step 3 ruling was filed (for the U.S.) This "
            "record was recorded as CLOSED-FAIL.")
        self._assert_f2_row(root, "present", NOT_APPROVED_FIGURES)

    def test_f15_62_class_rule_direct(self):
        cases = (
            # Other abbreviations end before any capitalised token.
            ("Filed for the U.S. Lane noted", "U.S.", True),
            ("Filed for the U.S. Finally, noted", "U.S.", True),
            ("Filed at 5 p.m. Lane noted", "p.m.", True),
            ("Filed for the U.S. office noted", "U.S.", False),
            # Titles never end before a capitalised token.
            ("given by Dr. He, recorded", "Dr.", False),
            ("given by Dr. An, recorded", "Dr.", False),
            ("given by Dr. Lane, recorded", "Dr.", False),
            # Introducing abbreviations do not end in mid passage.
            ("notes, e.g. He said so", "e.g.", False),
            ("notes, i.e. That claim stands", "i.e.", False),
            ("notes, e.g. its outcome", "e.g.", False),
            # Dotted multi letter forms are whole: neither stop
            # of Ph.D. cuts before the name it stands with.
            ("by Ph.D. Lane, recorded", "Ph.", False),
            ("by Ph.D. Lane, recorded", "Ph.D.", False),
            ("by Ed.D. Lane, recorded", "Ed.D.", False),
            # A quoted end closed by a parenthesis still ends.
            ("filed (for the U.S.) This record", "U.S.", True),
            # An abbreviation last in the passage still ends.
            ("withdrawn by Dr.", "Dr.", True),
            ("filed for the U.S.", "U.S.", True),
            # Initials hold together.
            ("by J. P. Lane, recorded", "J.", False),
            ("by J. P. Lane, recorded", "P.", False),
        )
        for text, token, expected in cases:
            with self.subTest(text=text, token=token):
                self.assertEqual(ends_at(text, token), expected)

    # ------------------------------------------------------- duration side

    def _report(self, note_text):
        table = base_case()
        table["PATH-LEDGER.md"] = path_ledger(
            DATE_ONLY_LINE + note_text, steps="1, 2, 3")
        root = build_tree(table)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, result.stdout

    def _assert_banked_stands(self, note_text, expected=None):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)),
                         expected if expected is not None
                         else [(1, 5.0, True)])
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("an interval duration stands in the "
                      "transition log", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "present", "T-4")
        return root, report

    def _assert_taken_out(self, note_text):
        root, report = self._report(note_text)
        self.assertEqual(_t4_banked_durations(capture(root)), [])
        t2 = row_block(report, "T-2")
        assert_verdict(self, t2, "missing", "T-2")
        self.assertIn("date-only-form", t2)
        self.assertIn("no BANKED, SUSPENDED or halt interval "
                      "duration stands", t2)
        t4 = row_block(report, "T-4")
        assert_verdict(self, t4, "missing", "T-4")
        self.assertIn(T4_MISSING_SHOWS, t4)
        self.assertNotIn("banked wait", report)
        return root, report

    def test_f15_62_other_abbrev_unlisted_opener_duration_denial_scopes(self):
        root, report = self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands for "
            "the U.S. Lane noted no interval duration one "
            "hundred hours was recorded for Step 1.")
        t4 = row_block(report, "T-4")
        self.assertIn("Step 1 banked wait 5 hours", t4)

    def test_f15_62_other_abbrev_unlisted_opener_duration_draft_stands(self):
        root, report = self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands for "
            "the U.S. Lane's draft was withdrawn.")
        t4 = row_block(report, "T-4")
        self.assertIn("Step 1 banked wait 5 hours", t4)

    def test_f15_62_other_abbrev_unlisted_opener_duration_finally_stands(self):
        root, report = self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands for "
            "the U.S. Finally, no interval duration one hundred "
            "hours was recorded for Step 1.")
        t4 = row_block(report, "T-4")
        self.assertIn("Step 1 banked wait 5 hours", t4)

    def test_f15_62_introducing_abbrev_duration_before_denial_reaches(self):
        self._assert_taken_out(
            "The duration was withdrawn, e.g. He said so, Step 1 "
            "BANKED interval duration 5 hours stands.")

    def test_f15_62_dotted_multi_letter_duration_denial_reaches(self):
        for title in ("Ph.D.", "Ed.D.", "LL.D."):
            with self.subTest(title=title):
                self._assert_taken_out(
                    "The duration was withdrawn by " + title
                    + " Lane, Step 1 BANKED interval duration "
                    "5 hours stands.")

    def test_f15_62_quoted_paren_end_duration_denial_scopes(self):
        root, report = self._assert_banked_stands(
            "Step 1 BANKED interval duration 5 hours stands "
            "(for the U.S.) Lane noted no interval duration one "
            "hundred hours was recorded for Step 1.")
        t4 = row_block(report, "T-4")
        self.assertIn("Step 1 banked wait 5 hours", t4)

    def test_f15_62_control_title_before_name_retraction_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands. "
            "That claim, Dr. Lane noted, was withdrawn.")

    def test_f15_62_control_passage_end_abbreviation_taken_out(self):
        for note in (
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim was withdrawn by Dr.",
                "Step 1 BANKED interval duration 5 hours stands. "
                "That claim was withdrawn in the U.S."):
            with self.subTest(note=note):
                self._assert_taken_out(note)

    def test_f15_62_control_own_closure_after_title_counts(self):
        root = self._f2_root(
            "This record notes the Step 2 ruling by Dr. Lane, "
            "recorded as CLOSED-PASS.")
        self._assert_f2_row(root, "present", PLAIN_ONE_FIGURES)

    def test_f15_62_control_quoted_paren_retraction_taken_out(self):
        self._assert_taken_out(
            "Step 1 BANKED interval duration 5 hours stands "
            "(for the U.S.) That claim was withdrawn.")

    # ------------------------------------------------------------ F15-63

    def _assert_attributed(self, note_text, step):
        root, report = self._assert_banked_stands(
            note_text, expected=[(step, 5.0, True)])
        t4 = row_block(report, "T-4")
        self.assertIn("Step %d banked wait 5 hours" % step, t4)
        self.assertNotIn(
            "Step %d banked wait" % (1 if step != 1 else 2), t4)
        return root, report

    def test_f15_63_question_previous_sentence_recorded_for_attributes(self):
        self._assert_attributed(
            "Step 1 opened the run? BANKED interval duration "
            "5 hours stands; recorded for Step 2.", 2)

    def test_f15_63_exclamation_previous_sentence_recorded_for(self):
        self._assert_attributed(
            "Step 1 opened the run! BANKED interval duration "
            "5 hours stands; recorded for Step 2.", 2)

    def test_f15_63_question_previous_sentence_plain_part_attributes(self):
        self._assert_attributed(
            "Step 3 opened the run? BANKED interval duration "
            "5 hours stands, Step 2 wait noted.", 2)

    def test_f15_63_exclamation_previous_sentence_plain_part(self):
        self._assert_attributed(
            "Step 3 opened the run! BANKED interval duration "
            "5 hours stands, Step 2 wait noted.", 2)

    def test_f15_63_question_break_denial_in_next_sentence_stands(self):
        for mark in ("?", "!"):
            with self.subTest(mark=mark):
                root, report = self._assert_banked_stands(
                    "Step 1 BANKED interval duration 5 hours "
                    "stands" + mark + " No interval duration was "
                    "recorded for Step 1.")
                t4 = row_block(report, "T-4")
                self.assertIn("Step 1 banked wait 5 hours", t4)

    def test_f15_63_control_full_stop_twin_attributes_step2(self):
        self._assert_attributed(
            "Step 1 opened the run. BANKED interval duration "
            "5 hours stands; recorded for Step 2.", 2)


if __name__ == "__main__":
    unittest.main()
