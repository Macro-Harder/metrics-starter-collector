"""Step 16 fix pass 4 unit 5 tests: the F-2 unit.

Pinning tests for register item R16-4-05 (Medium, C4-02) of
Step 16 round 4. The governing rule of the pass: a piece not
read in full, for whatever reason, is not read. Where a gate
piece for a step stands not read in full, the F-2 form held
text names the piece and the bound or the state and states
no closure state position for that step; the none stated
statement stands only for a gate piece read in full carrying
no closure state.

The defect forms stand pinned exactly as spin 1136 built
them at section 3 of its paper: the clean tree with all
three gate records padded over the file limit and unread,
each carrying at its top its closure state, CLOSED-PASS;
and the same construction on the line limit route, each
gate record carrying one line of 70,000 characters below
its closure statement and unread past the line limit. On
both routes F-2 stood present but not derivable, the
correct verdict form, and its form held text stated for
each step that the step stands with recorded closure state
none stated, naming no bound, piece or limit. Two further
defect forms stand on the same branch under the register
cure form, which names any bound or damage state: gate
records damaged by a TRUNCATED marker, and gate records
standing as invalid UTF-8 bytes. The spin 1137 Attack 3
form stands pinned beside them: one unread gate between
two read gates carrying first ruling outcomes, where the
unread step took the same none stated problem clause.

Held controls stand pinned beside them, byte for byte:
the read control of the defect forms (the same gates read
in full, F-2 stating the recorded closure states in its
standing form, with the Q-4 row of the same report standing
in its fix pass 4 Unit 1 read form); a gate record read in
full stating no closure state, the none stated statement
standing true; a step with no gate record anywhere, in its
standing present form and in the all gates absent missing
form; the read control of the one unread gate form, all
three gates read carrying first ruling outcomes, F-2
present at first time approval rate 3 of 3 approved; and
the exact limit control, a gate record at exactly
1,000,000 bytes read in full.

Trees are written through the Unit 1 module helpers of fix
pass 1, because the constructions turn on exact byte
counts. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, row_block,
    run_tool)
from tests.test_h_step16_fix3_unit1 import (
    READ_Q4, _clean_files, _trace_gate_files)
from tests.test_h_step16_unit1 import _padded, _write_tree

GO_EXTRA = ("First ruling outcome: Go, closes the step, "
            "no send back before closure.")
MALFORMED_BYTES = b"\xff\xfe\xfd gate record, not valid text\n"
GATE_PATHS = tuple("steps/step-%02d-gate-record.md" % n
                   for n in (1, 2, 3))

READ_F2 = (
    "F-2 First-time approval rate | Verdict: present but not "
    "derivable | Reason: What the record shows: broken link, "
    "the first ruling outcome field recorded per step in one "
    "named place (missing field); form required, a first "
    "ruling outcome recorded per step in one named place, in "
    "the Auditor approval row form; form held, no rate is "
    "derived from final closing states; plain closures 3 and "
    "qualified closures 0 stand counted on the steps whose "
    "first ruling stands in a named form; no first ruling "
    "outcome is recorded per step in one named place for the "
    "steps the row spans; a ruling for Step 1 stands in a "
    "gate record or gate ruling with a closing state alone "
    "and no first ruling outcome recorded for the step, and "
    "the step is excluded from the numerator and from the "
    "denominator alike; a ruling for Step 2 stands in a gate "
    "record or gate ruling with a closing state alone and no "
    "first ruling outcome recorded for the step, and the step "
    "is excluded from the numerator and from the denominator "
    "alike; a ruling for Step 3 stands in a gate record or "
    "gate ruling with a closing state alone and no first "
    "ruling outcome recorded for the step, and the step is "
    "excluded from the numerator and from the denominator "
    "alike What follows: missing-field the first ruling "
    "outcome field the row requires does not stand, so no "
    "rate figure stands | Pointer: the gate record or gate "
    "ruling carrying each first ruling counted "
    "(steps/step-01-gate-record.md)")

NO_CLOSURE_F2 = (
    "F-2 First-time approval rate | Verdict: present but not "
    "derivable | Reason: What the record shows: broken link, "
    "the first ruling outcome field recorded per step in one "
    "named place (missing field); form required, a first "
    "ruling outcome recorded per step in one named place, in "
    "the Auditor approval row form; form held, no rate is "
    "derived from final closing states; Step 1 stands with "
    "recorded closure state none stated, which matches no "
    "named closure form in the hardened closure state "
    "vocabulary; Step 2 stands with recorded closure state "
    "none stated, which matches no named closure form in the "
    "hardened closure state vocabulary; Step 3 stands with "
    "recorded closure state none stated, which matches no "
    "named closure form in the hardened closure state "
    "vocabulary What follows: missing-field the first ruling "
    "outcome field the row requires does not stand, so no "
    "rate figure stands | Pointer: the gate record or gate "
    "ruling carrying each first ruling counted "
    "(steps/step-01-gate-record.md)")

ABSENT_F2 = (
    "F-2 First-time approval rate | Verdict: missing | "
    "Reason: What the record shows: no gate record, gate "
    "ruling or gate adjudication stands in the capture for "
    "this metric What follows: no-feeder-record no feeder "
    "record for the metric exists in the tree, so the row is "
    "missing (missing record) | Pointer: "
    "steps/step-01-gate-record.md")

MIXED_NO_GATE_F2 = (
    "F-2 First-time approval rate | Verdict: present | "
    "Value: first-time approval rate: 1 of 1 approved, plain "
    "closures 1, qualified closures 0 | Numerator: 1 | "
    "Denominator: 1 | Row coverage: denominator: 1 steps "
    "ruled on; steps counted: Step 1; Step 3 stands with no "
    "gate record or gate ruling and is not counted in the "
    "denominator; a ruling for Step 2 stands in a gate record "
    "or gate ruling with a closing state alone and no first "
    "ruling outcome recorded for the step, and the step is "
    "excluded from the numerator and from the denominator "
    "alike | Reconciled against: the metric carries no total "
    "to reconcile against | Pointer: the gate record or gate "
    "ruling carrying each first ruling counted "
    "(steps/step-01-gate-record.md)")

GO_READ_F2 = (
    "F-2 First-time approval rate | Verdict: present | "
    "Value: first-time approval rate: 3 of 3 approved, plain "
    "closures 3, qualified closures 0 | Numerator: 3 | "
    "Denominator: 3 | Row coverage: denominator: 3 steps "
    "ruled on; steps counted: Step 1, Step 2, Step 3 | "
    "Reconciled against: the metric carries no total to "
    "reconcile against | Pointer: the gate record or gate "
    "ruling carrying each first ruling counted "
    "(steps/step-01-gate-record.md)")


def _go_gate_files():
    files = _clean_files()
    for n in (1, 2, 3):
        files[GATE_PATHS[n - 1]] = gate_record(n, extra=GO_EXTRA)
    return files


class TestStep16Fix4Unit5(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _assert_cured(self, report, bound_word, paths=GATE_PATHS):
        f2 = row_block(report, "F-2")
        assert_verdict(self, f2, "present but not derivable", "F-2")
        for path in paths:
            self.assertIn(path, f2)
        self.assertIn(bound_word, f2)
        self.assertNotIn("none stated", f2)
        self.assertNotIn("stands with recorded closure state", f2)
        self.assertNotIn("first-time approval rate:", f2)
        return f2

    # ------------------------------------------------------
    # Defect forms
    # ------------------------------------------------------

    def test_r16_4_05_gates_unread_over_file_limit(self):
        """C4-02 file route: all gates unread, CLOSED-PASS at top."""
        files = _clean_files()
        for n in (1, 2, 3):
            files[GATE_PATHS[n - 1]] = _padded(
                gate_record(n), 1200097)
        report = self._run(files)
        self._assert_cured(report, "file limit")

    def test_r16_4_05_gates_unread_past_line_limit(self):
        """C4-02 line route: all gates unread past the line limit."""
        files = _clean_files()
        for n in (1, 2, 3):
            files[GATE_PATHS[n - 1]] = gate_record(n) + \
                ("x" * 70000) + "\n"
        report = self._run(files)
        self._assert_cured(report, "line limit")

    def test_r16_4_05_gates_truncated(self):
        """C4-02 damage form: gate records damaged by truncation."""
        files = _clean_files()
        for n in (1, 2, 3):
            files[GATE_PATHS[n - 1]] = gate_record(n) + \
                "TRUNCATED\n"
        report = self._run(files)
        self._assert_cured(report, "truncated")

    def test_r16_4_05_gates_malformed_bytes(self):
        """C4-02 damage form: gate records do not decode."""
        files = _clean_files()
        for n in (1, 2, 3):
            files[GATE_PATHS[n - 1]] = MALFORMED_BYTES
        report = self._run(files)
        self._assert_cured(report, "malformed")

    def test_r16_4_05_one_unread_gate_between_read_gates(self):
        """Attack 3 form: one unread gate, two read, outcomes stand."""
        files = _go_gate_files()
        files[GATE_PATHS[1]] = _padded(
            gate_record(2, extra=GO_EXTRA), 1200097)
        report = self._run(files)
        f2 = self._assert_cured(report, "file limit",
                                paths=(GATE_PATHS[1],))
        self.assertIn("plain closures 2", f2)

    # ------------------------------------------------------
    # Read controls of the defect forms
    # ------------------------------------------------------

    def test_r16_4_05_read_control_byte_for_byte(self):
        """Read control: the same gates read in full.

        The F-2 row states the recorded closure states in its
        standing form, and the Q-4 row of the same report
        stands in its fix pass 4 Unit 1 read form, byte for
        byte.
        """
        files = _trace_gate_files(lambda text: text)
        report = self._run(files)
        self.assertEqual(row_block(report, "F-2"), READ_F2)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_4_held_go_read_control_byte_for_byte(self):
        """Read control: all gates read with outcomes, 3 of 3."""
        report = self._run(_go_gate_files())
        self.assertEqual(row_block(report, "F-2"), GO_READ_F2)

    # ------------------------------------------------------
    # Held controls
    # ------------------------------------------------------

    def test_r16_4_held_no_closure_read_byte_for_byte(self):
        """Held control: read gates stating no closure state."""
        files = _clean_files()
        for n in (1, 2, 3):
            files[GATE_PATHS[n - 1]] = gate_record(n).replace(
                "Closure state: CLOSED-PASS.\n", "")
        report = self._run(files)
        self.assertEqual(row_block(report, "F-2"), NO_CLOSURE_F2)

    def test_r16_4_held_step_no_gate_record_byte_for_byte(self):
        """Held control: a step with no gate record anywhere."""
        files = _clean_files()
        files[GATE_PATHS[0]] = gate_record(1, extra=GO_EXTRA)
        del files[GATE_PATHS[2]]
        report = self._run(files)
        self.assertEqual(row_block(report, "F-2"),
                         MIXED_NO_GATE_F2)

    def test_r16_4_held_all_gates_absent_byte_for_byte(self):
        """Held control: no gate record anywhere in the tree."""
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "F-2"), ABSENT_F2)

    def test_r16_4_held_gate_exactly_at_file_limit(self):
        """Held control: a gate at exactly 1,000,000 bytes reads."""
        files = _go_gate_files()
        files[GATE_PATHS[1]] = _padded(
            gate_record(2, extra=GO_EXTRA), 1000000)
        report = self._run(files)
        self.assertIn(
            "Piece steps/step-02-gate-record.md | gate record "
            "| 1000000 bytes | read in full", report)
        self.assertEqual(row_block(report, "F-2"), GO_READ_F2)


if __name__ == "__main__":
    import unittest
    unittest.main()
