"""Collection guard: collected case set and count against the inventory."""
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

from tests.fixture_builder import FixtureTestCase, register_handle
from tests.suite_inventory import INVENTORY

REPO_ROOT = Path(__file__).resolve().parent.parent
IN_COPY = os.environ.get("MSC_COPY_RUN") == "1"
SKIP_REASON = "golden subject tree not present on this machine"


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def collected_ids():
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test*.py",
                            top_level_dir=str(REPO_ROOT))
    return sorted(case.id() for case in flatten(suite))


def inventory_ids():
    ids = []
    for module, entry in INVENTORY.items():
        ids.extend(entry["cases"])
    return sorted(ids)


def run_copy_suite(copy_root, env_extra=None):
    env = dict(os.environ)
    env["MSC_COPY_RUN"] = "1"
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        capture_output=True, text=True, cwd=str(copy_root), env=env,
        timeout=600)


def copy_suite():
    import tempfile
    handle = register_handle(tempfile.mkdtemp(prefix="msc_suite_copy_"))
    copy_root = Path(handle) / "repo"
    shutil.copytree(str(REPO_ROOT / "tests"), str(copy_root / "tests"))
    pkg = REPO_ROOT / "metrics_starter_collector"
    if pkg.exists():
        shutil.copytree(str(pkg), str(copy_root / "metrics_starter_collector"))
    return copy_root


class TestCollectionGuard(FixtureTestCase):

    def test_collection_matches_inventory_case_set(self):
        self.assertEqual(collected_ids(), inventory_ids())

    def test_collection_count_matches_inventory(self):
        expected = sum(entry["count"] for entry in INVENTORY.values())
        self.assertEqual(len(collected_ids()), expected)
        for module, entry in INVENTORY.items():
            self.assertEqual(len([i for i in collected_ids()
                                  if module in i]), entry["count"], module)

    def test_collection_guard_rejects_removed_tests(self):
        if IN_COPY:
            return
        copy_root = copy_suite()
        tests_dir = copy_root / "tests"
        for path in tests_dir.glob("test*.py"):
            if path.name != "test_collection_guard.py":
                path.unlink()
        result = run_copy_suite(copy_root)
        self.assertNotEqual(result.returncode, 0,
                            "guard accepted a suite with modules removed")

    def test_collection_guard_rejects_empty_tree(self):
        if IN_COPY:
            return
        import tempfile
        handle = register_handle(tempfile.mkdtemp(prefix="msc_empty_copy_"))
        copy_root = Path(handle) / "repo"
        (copy_root / "tests").mkdir(parents=True)
        result = run_copy_suite(copy_root)
        self.assertNotEqual(result.returncode, 0,
                            "guard accepted an empty tests tree")
        combined = result.stderr + result.stdout
        self.assertTrue("Ran 0 tests" in combined or
                        "collection guard" in combined.lower() or
                        "0 tests" in combined,
                        "failure output does not name the zero collection "
                        "condition: " + combined[-500:])

    def test_designed_skip_accounting_on_copy_without_golden_tree(self):
        if IN_COPY:
            return
        copy_root = copy_suite()
        builder = copy_root / "tests" / "fixture_builder.py"
        text = builder.read_text(encoding="utf-8")
        absent = 'Path.home() / "workspace" / "no_such_golden_tree" / "design"'
        text = text.replace(
            'Path.home() / "workspace" / "fold-in-trace-checker" / "design"',
            absent)
        builder.write_text(text, encoding="utf-8")
        result = run_copy_suite(copy_root)
        skipped = [ln for ln in result.stderr.splitlines()
                   if "... skipped" in ln]
        golden_skips = [ln for ln in skipped if "test_golden" in ln]
        self.assertEqual(len(golden_skips), 2, result.stderr[-3000:])
        for line in golden_skips:
            self.assertIn(SKIP_REASON, line,
                          "golden skip does not state the designed reason")
        non_golden = [ln for ln in skipped if "test_golden" not in ln]
        self.assertEqual(non_golden, [], result.stderr[-3000:])
        summary = result.stderr.strip().splitlines()[-1] if \
            result.stderr.strip() else ""
        self.assertNotEqual(summary, "OK",
                            "copied run without the golden tree stands "
                            "as an unqualified pass")
        self.assertTrue("skipped=2" in result.stderr or
                        result.returncode != 0,
                        "copied run result does not stand in qualified "
                        "form: " + summary)


if __name__ == "__main__":
    unittest.main()
