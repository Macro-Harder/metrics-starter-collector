"""Step 16 fix unit 1 tests: the over limit feeder family.

Pinning tests for register items R16-01 (High) and R16-02 (Medium)
of Step 16 round 1. R16-01: where a cost ledger stands in the tree
but was not read past a limit, E-3 must stand present but not
derivable, with the reason naming the bound that stopped the
reading and the piece that was not read; it must never stand
missing, missing being reserved for no feeder record in the tree.
R16-02, the companion limbs: E-4 and B-2 on the same unread ledger
must name the bound and must not assert the unread ledger contents;
E-2 must not claim a total spins figure absent where the figure
stands in an unread step record; E-1 must carry a bound naming the
unread piece and the limit where a covered step feeder stands
unread. The two exact limit controls stand held: a piece at
exactly 1,000,000 bytes and a tree at exactly 25,000,000 bytes are
read in full with full verdicts.

Trees are written directly by this module because the
constructions turn on exact byte counts, which the case table
form does not carry. The product is invoked through run_tool,
which runs the module entry route as a subprocess.
"""
from pathlib import Path

from tests.fixture_builder import (
    FixtureTestCase, assert_verdict, gate_record, metrics_record,
    row_block, run_tool, step_record, tracked_tempdir)

LEDGER_FULL = ("# Cost ledger\n\nStep 1: money 10, tokens 1000.\n"
               "Step 2: money 20, tokens 2000.\n"
               "Step 3: money 30, tokens 3000.\n"
               "Budget: money 100, tokens 10000.\n")
LEDGER_PATH = "registers/cost-ledger.md"
METRICS_PATH = "wiki/wiki/synthesis/build-metrics-record.md"
FILE_LIMIT = 1000000
TREE_BYTE_LIMIT = 25000000


def _filler(count):
    """Return filler text of exactly count bytes, in short lines."""
    lines = count // 1000
    text = ("x" * 999 + "\n") * lines + "x" * (count - lines * 1000)
    return text


def _padded(text, size):
    """Return text padded with filler lines to exactly size bytes."""
    return text + _filler(size - len(text.encode("utf-8")))


def _base_files():
    """The small complete tree files, steps 1 to 3, as plain data."""
    files = {}
    transitions = []
    for n in (1, 2, 3):
        files["steps/step-%02d-record.md" % n] = step_record(n)
        files["steps/step-%02d-gate-record.md" % n] = gate_record(n)
        transitions.append(
            "Step %d IN PROGRESS 2026-11-01 09:00, closed "
            "2026-11-01 17:00." % n)
    files["PATH-LEDGER.md"] = (
        "# Path ledger\n\nSteps stated: 1, 2, 3.\n\n"
        "## Transitions\n\n%s\n" % "\n".join(transitions))
    files["TIER-RECORD.md"] = "# Tier record\n\nTier: Low. Base: 2.\n"
    files[METRICS_PATH] = metrics_record(
        body="Step table stands complete for the fixture steps.")
    return files


def _roster_files():
    """Roster artifacts for steps 1 to 3, each stating a pair."""
    files = {}
    for n in (1, 2, 3):
        files["steps/step-%02d-roster-artifact.md" % n] = (
            "# Step %d roster artifact\n\nNamed agents: 2. "
            "Base: 2.\nRoster additions over base: 0.\n" % n)
    return files


def _write_tree(files):
    """Write one tree under a tracked temporary directory."""
    root = tracked_tempdir("msc_step16_unit1_") / "tree"
    for rel in sorted(files):
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        content = files[rel]
        if isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding="utf-8")
    return root


def _add_filler(files, total):
    """Add audit filler files totalling total bytes to a files dict."""
    remaining = total
    index = 0
    while remaining > 0:
        chunk = min(990000, remaining)
        files["audit/filler-%02d.md" % index] = _filler(chunk)
        remaining -= chunk
        index += 1
    return files


class TestStep16Unit1(FixtureTestCase):

    def _run(self, files):
        root = _write_tree(files)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        return result.stdout

    def _assert_unread_ledger_rows(self, report, bound_word):
        e3 = row_block(report, "E-3")
        assert_verdict(self, e3, "present but not derivable", "E-3")
        self.assertIn(LEDGER_PATH, e3)
        self.assertIn(bound_word, e3)
        self.assertNotIn("no feeder record for the metric exists", e3)
        self.assertNotIn("no token figure stands in it", e3)
        b2 = row_block(report, "B-2")
        assert_verdict(self, b2, "present but not derivable", "B-2")
        self.assertIn(LEDGER_PATH, b2)
        self.assertIn(bound_word, b2)
        self.assertNotIn("carries no spent or budget figure", b2)
        e4 = row_block(report, "E-4")
        assert_verdict(self, e4, "present but not derivable", "E-4")
        self.assertIn(LEDGER_PATH, e4)
        self.assertIn(bound_word, e4)
        self.assertNotIn("no feeder states a per step money figure",
                         e4)

    def test_r16_01_ledger_wholly_past_tree_byte_limit(self):
        """R16-01, breaker case 1a: the ledger stands past the cut."""
        files = _base_files()
        files[LEDGER_PATH] = LEDGER_FULL
        _add_filler(files, 26730000)
        report = self._run(files)
        self._assert_unread_ledger_rows(report, "tree byte limit")

    def test_r16_01_ledger_as_the_crossing_piece(self):
        """R16-01, breaker case 1b: the ledger itself crosses."""
        files = _base_files()
        files[LEDGER_PATH] = LEDGER_FULL
        before = sum(len(files[rel].encode("utf-8"))
                     for rel in ("PATH-LEDGER.md", "TIER-RECORD.md"))
        _add_filler(files, 24999930 - before)
        report = self._run(files)
        self._assert_unread_ledger_rows(report, "tree byte limit")

    def test_r16_01_ledger_over_single_piece_limit(self):
        """R16-01, breaker case 1c second form: file limit crossed."""
        files = _base_files()
        files[LEDGER_PATH] = _padded(LEDGER_FULL, 1100000)
        report = self._run(files)
        self._assert_unread_ledger_rows(report, "file limit")

    def test_r16_02_e1_bound_names_unread_step_record(self):
        """R16-02, breaker case 1c first form: the E-1 bound limb."""
        files = _base_files()
        files.update(_roster_files())
        files["steps/step-02-record.md"] = _padded(
            step_record(2), 1200097)
        report = self._run(files)
        block = row_block(report, "E-1")
        assert_verdict(self, block, "present", "E-1")
        self.assertIn("2 of 2", block)
        self.assertIn("Bound:", block)
        bound_at = block.find("Bound:")
        bound = block[bound_at:]
        self.assertIn("steps/step-02-record.md", bound)
        self.assertIn("file limit", bound)

    def test_r16_02_e2_no_absence_claim_over_unread_record(self):
        """R16-02, breaker case 1c first form: the E-2 absence limb."""
        files = _base_files()
        files.update(_roster_files())
        files["steps/step-02-record.md"] = _padded(
            step_record(2), 1200097)
        report = self._run(files)
        block = row_block(report, "E-2")
        assert_verdict(self, block, "present", "E-2")
        self.assertIn("steps/step-02-record.md", block)
        self.assertIn("file limit", block)
        self.assertNotIn("no total spins figure stands for that "
                         "step", block)
        self.assertNotIn("state no total spins figure in any "
                         "record", block)
        self.assertNotIn("no total stands for it", block)

    def test_r16_held_piece_exactly_at_file_limit(self):
        """Held control, breaker case 1d first form: at the limit."""
        files = _base_files()
        files["steps/step-02-record.md"] = _padded(
            step_record(2), FILE_LIMIT)
        root = _write_tree(files)
        placed = Path(root) / "steps" / "step-02-record.md"
        self.assertEqual(placed.stat().st_size, FILE_LIMIT)
        result = run_tool(root)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        report = result.stdout
        self.assertIn(
            "Piece steps/step-02-record.md | step record | "
            "1000000 bytes | read in full", report)
        block = row_block(report, "E-1")
        assert_verdict(self, block, "present", "E-1")
        e2 = row_block(report, "E-2")
        self.assertIn("total spins stand for Step 1, Step 2, "
                      "Step 3", e2)

    def test_r16_held_tree_exactly_at_tree_byte_limit(self):
        """Held control, breaker case 1d second form: at the limit."""
        files = _base_files()
        files[LEDGER_PATH] = LEDGER_FULL
        held = sum(len(text.encode("utf-8"))
                   for text in files.values())
        _add_filler(files, TREE_BYTE_LIMIT - held)
        report = self._run(files)
        self.assertIn("Limit: no limit crossed", report)
        self.assertIn("Reading: full", report)
        e3 = row_block(report, "E-3")
        assert_verdict(self, e3, "present", "E-3")
        self.assertIn("Step 1 tokens 1000", e3)
        self.assertIn("Step 3 tokens 3000", e3)
        e4 = row_block(report, "E-4")
        assert_verdict(self, e4, "present", "E-4")
        b2 = row_block(report, "B-2")
        assert_verdict(self, b2, "present", "B-2")
        self.assertIn("60 percent", b2)


if __name__ == "__main__":
    import unittest
    unittest.main()
