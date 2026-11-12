"""Golden tests on the real subject tree, read in place, run last."""
import re
import unittest
from pathlib import Path

from tests.fixture_builder import (FixtureTestCase, GOLDEN_ROOT,
                                     assert_verdict, row_block, run_tool)

EXPECTED_IDENTITY = {"files": 309, "bytes": 6747042}
SKIP_REASON = "golden subject tree not present on this machine"
HERE = Path(__file__).resolve().parent
PRESENT_ROWS = ("E-1", "E-2", "Q-4")


def load_expected(name):
    rows = {}
    for line in (HERE / name).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split(" | ")]
        rows[parts[0]] = parts
    return rows


def check_identity(test):
    if not GOLDEN_ROOT.exists():
        test.skipTest(SKIP_REASON)
    files = [p for p in GOLDEN_ROOT.rglob("*") if p.is_file()]
    total = sum(p.stat().st_size for p in files)
    test.assertEqual(len(files), EXPECTED_IDENTITY["files"],
                     "golden identity failed: file count")
    test.assertEqual(total, EXPECTED_IDENTITY["bytes"],
                     "golden identity failed: tree size in bytes")


def _numbers(text):
    return re.findall(r"\d[\d,]*", text)


def _assert_field_atoms(test, block, field, code, label):
    """Assert the checkable content of one expected field in a row.

    Short segments are asserted whole. Longer segments are asserted
    through every number, file name and step name they state, and
    through any step range they state, expanded step by step, so a
    wrong figure, a wrong denominator or a wrong coverage naming in
    the printed row fails the comparison.
    """
    for segment in field.split(";"):
        segment = segment.strip()
        if not segment or segment == "refusal-form":
            continue
        range_match = re.search(r"Steps (\d+) to (\d+)", segment)
        if len(segment) <= 60 and not range_match:
            test.assertIn(segment, block, "%s %s: %s" % (code, label, segment))
            continue
        for name in re.findall(r"[\w./-]+\.md", segment):
            test.assertIn(Path(name).name, block,
                          "%s %s file: %s" % (code, label, name))
        if range_match:
            test.assertIn("Steps %s to %s" % (range_match.group(1),
                                              range_match.group(2)), block,
                          "%s %s range: %s" % (code, label, segment))
        for number in _numbers(segment):
            if range_match and number in (range_match.group(1),
                                          range_match.group(2)):
                continue
            test.assertIn(number.replace(",", ""), block.replace(",", ""),
                          "%s %s number: %s" % (code, label, number))
        for step_name in re.findall(r"Step \d+", segment):
            if range_match:
                continue
            test.assertIn(step_name, block,
                          "%s %s: %s" % (code, label, step_name))


def _assert_reason_basis(test, block, basis, code):
    """Assert the two part reason basis of one full file row."""
    lowered = block.lower()
    if basis.lower().startswith("present under"):
        for atom in ("coverage",):
            test.assertIn(atom, lowered, "%s basis: %s" % (code, atom))
        _assert_field_atoms(test, block, basis, code, "basis")
        return
    shows_at = lowered.find("what the record shows")
    follows_at = lowered.find("what follows")
    test.assertTrue(0 <= shows_at < follows_at,
                    "%s basis label order" % code)
    _assert_field_atoms(test, block, basis, code, "basis")


def compare(test, expected_name, full):
    check_identity(test)
    expected = load_expected(expected_name)
    test.assertEqual(len(expected), 17)
    result = run_tool(GOLDEN_ROOT)
    test.assertEqual(result.returncode, 0, result.stderr)
    for code, parts in expected.items():
        verdict, reason_code, pointer = parts[1], parts[2], parts[3]
        figures, denominator = parts[4], parts[5]
        block = row_block(result.stdout, code)
        test.assertTrue(block, code)
        assert_verdict(test, block, verdict, code)
        if reason_code == "no code fits":
            test.assertIn("no code fits", block.lower(), code)
        elif reason_code != "none":
            test.assertIn(reason_code, block, code)
        test.assertIn(Path(pointer).name, block, code)
        if code in PRESENT_ROWS:
            _assert_field_atoms(test, block, figures, code, "figure")
            _assert_field_atoms(test, block, denominator, code,
                                "denominator")
        if full:
            _assert_field_atoms(test, block, figures, code, "figure")
            _assert_field_atoms(test, block, denominator, code,
                                "denominator and coverage")
            _assert_reason_basis(test, block, parts[6], code)
    q4 = row_block(result.stdout, "Q-4")
    test.assertRegex(q4, r"(?<!\d)(?<!\d\.)105(?!\d)(?!\.\d)")
    test.assertRegex(q4, r"(?<!\d)(?<!\d\.)106(?!\d)(?!\.\d)")
    test.assertNotIn("record disagrees", q4.lower())


class TestGolden(FixtureTestCase):

    def test_golden_comparison_limited(self):
        compare(self, "golden_expected_limited.txt", full=False)

    def test_golden_comparison_full(self):
        compare(self, "golden_expected_full.txt", full=True)


if __name__ == "__main__":
    unittest.main()
