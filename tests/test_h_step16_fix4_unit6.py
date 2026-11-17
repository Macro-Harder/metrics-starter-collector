"""Step 16 fix pass 4 unit 6 tests: the remainder unit.

Pinning tests for register items R16-4-10 (Low, B4-08) and
the staffing parts of R16-4-12 (Low, B4-10) of Step 16
round 4. The governing rule of the pass: a piece not read
in full, for whatever reason, is not read.

R16-4-10: a Round 1 round record read in full carrying
Critical 0, High 1, Medium 2, Low 3, beside a Round 2 round
record carrying Critical 5, High 5, Medium 5, Low 5, padded
over the file limit and unread. Q-1 stands present in the
bounded form naming Round 1 alone in its population, and
no clause on the row names the unread record or its round.
The cure these tests pin: the present row population names
every feeder piece standing not read in full whose round
it omits, with the bound or the state, in a clause of the
row itself, so the population reads as bounded by the
named piece and not as the whole population.

R16-4-12, staffing parts: every step record and roster
artifact of Steps 1 to 3 damaged by a TRUNCATED marker
line, their figures standing in the visible bytes above
the marker, no piece over any limit. E-1 and E-2 each
stand present but not derivable, the correct verdict
class, and each record shows text asserts contents over
the damaged pieces: E-1 that no step carries both a
staffed count and a base count, E-2 that none of the
records states an additions over base figure or a total
spins figure, both false of the visible bytes. The cure
these tests pin: the shows text of a governed E-1 or E-2
row asserts nothing over a piece not read in full; for
such a piece the row states the piece and its state and
nothing it holds. The Q-3 part of R16-4-12 was cured by
Unit 2 of this pass and is not in this module.

Held controls stand pinned beside them, byte for byte:
the fix pass 2 Unit 1 staffing branches in their cured
over limit forms for E-1 and E-2; the read staffing rows;
the Q-1 single unread feeder form, present but not
derivable naming the paper and the over limit state; a
Q-1 form with every population record read; and the Q-1
form where no round record stands at all, the population
empty, in its governed missing form.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, row_block, run_tool,
    step_record)
from tests.test_h_step16_fix2_unit1 import READ_E1, READ_E2
from tests.test_h_step16_fix3_unit1 import _clean_files
from tests.test_h_step16_unit1 import _padded, _write_tree

ROUND1_TEXT = ("# Round 1\n\nPost triage breakdown: Critical 0, "
               "High 1, Medium 2, Low 3.\n")
ROUND2_TEXT = ("# Round 2\n\nPost triage breakdown: Critical 5, "
               "High 5, Medium 5, Low 5.\n")
ROUND1_PATH = "audit/step-01-round-record.md"
ROUND2_PATH = "audit/step-02-round-record.md"

READ_Q1 = (
    "Q-1 Findings per audit round, by severity | Verdict: "
    "present | Value: bounded form: population, the rounds "
    "with records standing: Round 1, Round 2; excluded: "
    "none; qualifying round counts: Round 1: Critical 0, "
    "High 1, Medium 2, Low 3, scale flow scale, record form "
    "round record; Round 2: Critical 5, High 5, Medium 5, "
    "Low 5, scale flow scale, record form round record | "
    "Row coverage: denominator step universe 3 steps | "
    "Reconciled against: the metric carries no total to "
    "reconcile against | Pointer: the round record, or a "
    "record the round record names, for each round counted "
    "(audit/step-01-round-record.md)")

SINGLE_UNREAD_Q1 = (
    "Q-1 Findings per audit round, by severity | Verdict: "
    "present but not derivable | Reason: What the record "
    "shows: the audit paper audit/step-01-round-record.md "
    "stands over limit in the capture and supplies no "
    "breakdown What follows: over-limit-piece the feeder "
    "piece is not read in full, so no figure stands for "
    "the round it feeds (not producible) | Pointer: the "
    "round record, or a record the round record names, for "
    "each round counted (audit/step-01-round-record.md)")

EMPTY_POPULATION_Q1 = (
    "Q-1 Findings per audit round, by severity | Verdict: "
    "missing | Reason: What the record shows: no audit "
    "round record stands in the capture for this metric "
    "What follows: no-feeder-record no feeder record for "
    "the metric exists in the tree, so the row is missing "
    "(missing record) | Pointer: the round record, or a "
    "record the round record names, for each round counted "
    "(audit/step-01-audit-paper.md)")

_LIMIT_NAMING = (
    ", which stands not read past a limit: the file limit "
    "of 1000000 bytes was crossed")
_STAFFING_PATHS = tuple(
    path for n in (1, 2, 3) for path in (
        "steps/step-%02d-record.md" % n,
        "steps/step-%02d-roster-artifact.md" % n))
_STAFFING_NAMING = "; ".join(
    path + _LIMIT_NAMING for path in _STAFFING_PATHS)

CURED_OVER_LIMIT_E1 = (
    "E-1 Agents staffed against base | Verdict: present "
    "but not derivable | Reason: What the record shows: "
    "broken link, the staffed and base pair field for "
    "Steps 1, 2 and 3, which stands in a piece not read "
    "past the limit named in its capture reason (not "
    "producible); form required, a step record or roster "
    "artifact read in full, stating a staffed count and a "
    "base count for the same step; form held, the staffing "
    "pieces stand in the tree at " + _STAFFING_NAMING +
    " What follows: over-limit-piece the row rests on "
    "pieces that were not read past the bound named, so "
    "the row is present but not derivable; no step is "
    "claimed to carry no pair, and no pair figure is "
    "claimed absent from a piece that was not read | "
    "Pointer: the step record and roster for each step "
    "counted (steps/step-01-record.md)")

CURED_OVER_LIMIT_E2 = (
    "E-2 Spin-ups per step | Verdict: present but not "
    "derivable | Reason: What the record shows: broken "
    "link, the additions over base and total spins fields "
    "for Steps 1, 2 and 3, which stand in a piece not read "
    "past the limit named in its capture reason (not "
    "producible); form required, a step record or roster "
    "artifact read in full, stating an additions over "
    "base figure or a total spins figure; form held, the "
    "staffing pieces stand in the tree at " +
    _STAFFING_NAMING +
    " What follows: over-limit-piece the row rests on "
    "pieces that were not read past the bound named, so "
    "the row is present but not derivable; neither "
    "labelled quantity is claimed absent from a piece "
    "that was not read | Pointer: the roster and the step "
    "record for each step counted "
    "(steps/step-01-record.md)")


def _roster_text(n):
    return ("# Step %d roster artifact\n\nNamed agents: 2. "
            "Base: 2.\nRoster additions over base: 0.\n" % n)


def _truncated_staffing_files():
    files = _clean_files()
    for n in (1, 2, 3):
        files["steps/step-%02d-record.md" % n] = \
            step_record(n) + "TRUNCATED\n"
        files["steps/step-%02d-roster-artifact.md" % n] = \
            _roster_text(n) + "TRUNCATED\n"
    return files


def _over_limit_staffing_files():
    files = _clean_files()
    for n in (1, 2, 3):
        files["steps/step-%02d-record.md" % n] = _padded(
            step_record(n), 1200097)
        files["steps/step-%02d-roster-artifact.md" % n] = \
            _padded(_roster_text(n), 1200097)
    return files


class TestStep16Fix4Unit6(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    # ------------------------------------------------------
    # Defect forms: R16-4-10, the Q-1 population
    # ------------------------------------------------------

    def test_r16_4_10_q1_population_names_unread_round_record(self):
        """B4-08 form: Round 2 record unread past the file limit."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ROUND2_PATH] = _padded(ROUND2_TEXT, 1200097)
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "population, the rounds with records standing: "
            "Round 1", q1)
        self.assertIn(
            "Round 1: Critical 0, High 1, Medium 2, Low 3", q1)
        self.assertIn(
            "population bound: the population stands bounded "
            "by audit/step-02-round-record.md, which stands "
            "not read past a limit: the file limit of 1000000 "
            "bytes was crossed", q1)
        self.assertNotIn("Round 2: Critical 5", q1)
        self.assertNotIn(
            "records standing: Round 1, Round 2", q1)

    def test_r16_4_10_q1_population_names_truncated_round_record(self):
        """B4-08 damage form: the Round 2 record stands truncated."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ROUND2_PATH] = ROUND2_TEXT + "TRUNCATED\n"
        report = self._run(files)
        q1 = row_block(report, "Q-1")
        assert_verdict(self, q1, "present", "Q-1")
        self.assertIn(
            "population bound: the population stands bounded "
            "by audit/step-02-round-record.md", q1)
        self.assertIn("truncation marker", q1)
        self.assertNotIn("Round 2: Critical 5", q1)

    def test_r16_4_10_q1_read_control_byte_for_byte(self):
        """Read control: both round records read in full."""
        files = _clean_files()
        files[ROUND1_PATH] = ROUND1_TEXT
        files[ROUND2_PATH] = ROUND2_TEXT
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"), READ_Q1)

    # ------------------------------------------------------
    # Defect forms: R16-4-12 staffing parts, the shows text
    # ------------------------------------------------------

    def test_r16_4_12_e1_shows_over_truncated_staffing(self):
        """B4-10 part two: E-1 shows text over truncated pieces."""
        report = self._run(_truncated_staffing_files())
        e1 = row_block(report, "E-1")
        assert_verdict(self, e1, "present but not derivable", "E-1")
        for path in _STAFFING_PATHS:
            self.assertIn(path, e1)
        self.assertIn("truncation marker", e1)
        self.assertIn("not read in full", e1)
        self.assertNotIn(
            "no step carries both a staffed count and a base "
            "count for the same step", e1)

    def test_r16_4_12_e2_shows_over_truncated_staffing(self):
        """B4-10 part three: E-2 shows text over truncated pieces."""
        report = self._run(_truncated_staffing_files())
        e2 = row_block(report, "E-2")
        assert_verdict(self, e2, "present but not derivable", "E-2")
        for path in _STAFFING_PATHS:
            self.assertIn(path, e2)
        self.assertIn("truncation marker", e2)
        self.assertIn("not read in full", e2)
        self.assertNotIn(
            "none states an additions over base figure or a "
            "total spins figure", e2)

    def test_r16_4_12_staffing_read_controls_byte_for_byte(self):
        """Read control: the same staffing pieces read in full."""
        report = self._run(_clean_files())
        self.assertEqual(row_block(report, "E-1"), READ_E1)
        self.assertEqual(row_block(report, "E-2"), READ_E2)

    # ------------------------------------------------------
    # Held controls
    # ------------------------------------------------------

    def test_r16_4_held_staffing_over_limit_e1_byte_for_byte(self):
        """Held control: fix pass 2 Unit 1 E-1 branch, cured form."""
        report = self._run(_over_limit_staffing_files())
        self.assertEqual(row_block(report, "E-1"),
                         CURED_OVER_LIMIT_E1)

    def test_r16_4_held_staffing_over_limit_e2_byte_for_byte(self):
        """Held control: fix pass 2 Unit 1 E-2 branch, cured form."""
        report = self._run(_over_limit_staffing_files())
        self.assertEqual(row_block(report, "E-2"),
                         CURED_OVER_LIMIT_E2)

    def test_r16_4_held_q1_single_unread_byte_for_byte(self):
        """Held control: Q-1 first form, one round record unread."""
        files = _clean_files()
        files[ROUND1_PATH] = _padded(ROUND1_TEXT, 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-1"),
                         SINGLE_UNREAD_Q1)

    def test_r16_4_held_q1_empty_population_byte_for_byte(self):
        """Held control: no round record stands, population empty."""
        report = self._run(_clean_files())
        self.assertEqual(row_block(report, "Q-1"),
                         EMPTY_POPULATION_Q1)


if __name__ == "__main__":
    import unittest
    unittest.main()
