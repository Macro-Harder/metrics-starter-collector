"""Step 16 fix pass 3 unit 1 tests: the Q-4 missing branch.

Pinning tests for register item R16-3-01 of Step 16 round 3
(spin 1131, finding B3-01, High). Where first trace figures
stand in gate records that were never read past a limit, Q-4
reports missing with the no-feeder-record code, stating that
no first trace record stands in the tree and that no feeder
record exists, and on the file and line routes the unread gate
records carry the first trace statement itself, so the absence
claim is false in fact. The cure these tests pin, in the
WV2-09 form the neighbouring branch of the same derivation
already takes for an unread trace named piece: where a gate
class piece the row rests on stands unread past a limit, Q-4
stands present but not derivable with the bound and the piece
named, and no absence is claimed over the unread piece; where
every feeder stands read and no trace figure stands, the
standing missing form stands exactly as today.

Three defect forms stand pinned, one per proven route of spin
1131 Attack 3: the walk bound construction of round 2 seam 8,
the file limit route, and the line limit route. Held controls
stand pinned beside them: the read control, the same records
as the file route read in full, standing Q-4 present at 8
LANDED of 8 byte for byte; the neighbouring branch for an
unread trace named piece, standing present but not derivable
byte for byte; and a genuinely absent feeder form, no gate
records anywhere in the tree, standing Q-4 missing in its
standing governed form byte for byte.

Trees are written through the Unit 1 module helpers because
the constructions turn on exact byte counts and walk
positions. The product is invoked through run_tool, which
runs the module entry route as a subprocess.
"""
from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, row_block,
    run_tool)
from tests.test_h_step16_unit1 import (
    LEDGER_FULL, LEDGER_PATH, _base_files, _padded,
    _roster_files, _write_tree)

TRACE_2 = ("First trace for step 2: 4 LANDED of 4 items "
           "checked, 0 PARTIAL, 0 CONTRADICTED.")
TRACE_3 = ("First trace for step 3: 4 LANDED of 4 items "
           "checked, 0 PARTIAL, 0 CONTRADICTED.")

READ_Q4 = (
    "Q-4 Fold-in trace landed at first trace | Verdict: "
    "present | Value: first trace LANDED shares for the named "
    "evidence steps: Step 2, 4 LANDED of 4 items checked; "
    "Step 3, 4 LANDED of 4 items checked; totals 8 LANDED, "
    "0 PARTIAL, 0 CONTRADICTED, 8 items checked | Row "
    "coverage: steps with a first trace in the named evidence "
    "set, Steps 2 and 3 | Reconciled against: the sum test "
    "ran per step | Pointer: the first trace record for each "
    "step counted (steps/step-02-gate-record.md)")

NEIGHBOUR_Q4 = (
    "Q-4 Fold-in trace landed at first trace | Verdict: "
    "present but not derivable | Reason: What the record "
    "shows: a trace record stands in the capture and no "
    "totals stand on it in a form the row can count What "
    "follows: missing-field no first trace figure stands on "
    "the feeder record, so no figure stands (missing field) "
    "| Pointer: the first trace record for each step counted "
    "(steps/step-01-trace-record.md)")

ABSENT_Q4 = (
    "Q-4 Fold-in trace landed at first trace | Verdict: "
    "missing | Reason: What the record shows: no first trace "
    "record stands in the tree for this metric What follows: "
    "no-feeder-record no feeder record for the metric exists "
    "in the tree, so the row is missing (missing record) | "
    "Pointer: the first trace record for each step counted "
    "(steps/step-01-gate-record.md)")


def _clean_files():
    files = _base_files()
    files.update(_roster_files())
    files[LEDGER_PATH] = LEDGER_FULL
    return files


def _trace_gate_files(pad):
    files = _clean_files()
    for step, trace in ((2, TRACE_2), (3, TRACE_3)):
        text = gate_record(step, extra=trace)
        files["steps/step-%02d-gate-record.md" % step] = \
            pad(text)
    return files


class TestStep16Fix3Unit1(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _assert_cured_q4(self, report, bound_word):
        q4 = row_block(report, "Q-4")
        assert_verdict(self, q4, "present but not derivable", "Q-4")
        self.assertIn("steps/step-02-gate-record.md", q4)
        self.assertIn("steps/step-03-gate-record.md", q4)
        self.assertIn(bound_word, q4)
        self.assertNotIn("no first trace record stands", q4)
        self.assertNotIn(
            "no feeder record for the metric exists", q4)
        self.assertNotIn("no-feeder-record", q4)

    def test_r16_3_01_walk_bound_gates_not_visited(self):
        """B3-01 route one: seam 8, gates not visited."""
        files = _clean_files()
        for index in range(9993):
            files["zz-filler-%05d.md" % index] = ""
        report = self._run(files)
        self.assertIn(
            "Coverage piece not read in full: "
            "steps/step-02-gate-record.md | gate record | "
            "51 bytes | over limit | over-limit-piece: not "
            "visited: the whole walk bound of 10000 entries "
            "was crossed", report)
        self._assert_cured_q4(report, "whole walk bound")

    def test_r16_3_01_file_limit_gates_carry_trace(self):
        """B3-01 route two: gates carry the trace, unread."""
        files = _trace_gate_files(
            lambda text: _padded(text, 1200097))
        report = self._run(files)
        self.assertIn(
            "Coverage piece not read in full: "
            "steps/step-02-gate-record.md | gate record | "
            "1200097 bytes | over limit | over-limit-piece: "
            "the file limit of 1000000 bytes was crossed",
            report)
        self._assert_cured_q4(report, "file limit")

    def test_r16_3_01_line_limit_gates_carry_trace(self):
        """B3-01 route three: gates unread past the line limit."""
        files = _trace_gate_files(
            lambda text: text + ("x" * 70000) + "\n")
        report = self._run(files)
        self.assertIn(
            "Coverage piece not read in full: "
            "steps/step-02-gate-record.md | gate record | "
            "70131 bytes | over limit | over-limit-piece: "
            "the line limit of 65536 bytes was crossed",
            report)
        self._assert_cured_q4(report, "line limit")

    def test_r16_3_held_read_control_byte_for_byte(self):
        """Held control: the file route records read in full."""
        files = _trace_gate_files(lambda text: text)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), READ_Q4)

    def test_r16_3_held_neighbouring_trace_piece_byte_for_byte(self):
        """Held control: an unread trace named piece branch."""
        files = _clean_files()
        files["steps/step-01-trace-record.md"] = _padded(
            "# Step 1 trace record\n\nParts: 2 LANDED, "
            "1 PARTIAL, 0 CONTRADICTED. Stated total: 2 items "
            "checked.\n", 1200097)
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), NEIGHBOUR_Q4)

    def test_r16_3_held_absent_feeder_byte_for_byte(self):
        """Held control: no gate records anywhere in the tree."""
        files = _clean_files()
        for path in [path for path in files if "gate" in path]:
            del files[path]
        report = self._run(files)
        self.assertEqual(row_block(report, "Q-4"), ABSENT_Q4)


if __name__ == "__main__":
    import unittest
    unittest.main()
