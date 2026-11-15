"""Collection guard: the collected case set and count against the inventory.

The guard states the collection guard in the form the plan states at
Margin M3. Discovery over the tests tree must collect every authored
module and every case the suite inventory lists, with no module
silently dropped and no case silently lost. The inventory stands at
tests/suite_inventory.py and lists test case identities per module at
case level, in an INVENTORY mapping from each module name to a count
and the list of its case identities. The guard counts its own cases
in the collected set it checks.

The two named negative cases build their own copy of the suite in a
temporary directory under the home .tmp directory, mutate the copy,
and assert the guard rejects it. They never touch the suite itself.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.suite_inventory import INVENTORY

REPO_ROOT = Path(__file__).resolve().parent.parent
IN_COPY = os.environ.get("MSC_COPY_RUN") == "1"
COPY_TIMEOUT = 120


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def collected_ids():
    loader = unittest.TestLoader()
    suite = loader.discover(str(REPO_ROOT / "tests"), pattern="test*.py",
                            top_level_dir=str(REPO_ROOT))
    return sorted(case.id() for case in flatten(suite))


def inventory_ids():
    ids = []
    for entry in INVENTORY.values():
        ids.extend(entry["cases"])
    return sorted(ids)


def temp_base():
    base = Path.home() / ".tmp"
    base.mkdir(parents=True, exist_ok=True)
    return base


def run_copy_suite(copy_root):
    env = dict(os.environ)
    env["MSC_COPY_RUN"] = "1"
    env["TMPDIR"] = str(temp_base())
    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        capture_output=True, text=True, cwd=str(copy_root), env=env,
        timeout=COPY_TIMEOUT)


class TestCollectionGuard(unittest.TestCase):

    def copy_suite(self):
        handle = Path(tempfile.mkdtemp(prefix="msc_suite_copy_",
                                        dir=str(temp_base())))
        self.addCleanup(shutil.rmtree, str(handle), True)
        copy_root = handle / "repo"
        shutil.copytree(str(REPO_ROOT / "tests"), str(copy_root / "tests"))
        pkg = REPO_ROOT / "metrics_starter_collector"
        if pkg.exists():
            shutil.copytree(str(pkg),
                            str(copy_root / "metrics_starter_collector"))
        return copy_root

    def test_collection_matches_inventory_case_set(self):
        self.assertEqual(collected_ids(), inventory_ids())

    def test_collection_count_matches_inventory(self):
        collected = collected_ids()
        expected = sum(entry["count"] for entry in INVENTORY.values())
        self.assertEqual(len(collected), expected)
        self.assertGreaterEqual(len(collected), expected)
        for module, entry in INVENTORY.items():
            mine = [i for i in collected if i.startswith("tests." + module + ".")]
            self.assertEqual(len(mine), entry["count"], module)

    def test_collection_guard_rejects_removed_tests(self):
        if IN_COPY:
            return
        copy_root = self.copy_suite()
        tests_dir = copy_root / "tests"
        for path in tests_dir.glob("test*.py"):
            if path.name != "test_collection_guard.py":
                path.unlink()
        result = run_copy_suite(copy_root)
        self.assertNotEqual(result.returncode, 0,
                            "guard accepted a suite with test cases removed")
        self.assertIn("FAILED", result.stderr,
                      "copy run does not record a guard failure: "
                      + result.stderr[-500:])

    def test_collection_guard_rejects_empty_tree(self):
        if IN_COPY:
            return
        handle = Path(tempfile.mkdtemp(prefix="msc_empty_copy_",
                                        dir=str(temp_base())))
        self.addCleanup(shutil.rmtree, str(handle), True)
        copy_root = handle / "repo"
        (copy_root / "tests").mkdir(parents=True)
        result = run_copy_suite(copy_root)
        self.assertNotEqual(result.returncode, 0,
                            "guard accepted an empty tests tree")
        combined = result.stderr + result.stdout
        self.assertIn("Ran 0 tests", combined,
                      "failure output does not name the zero collection "
                      "condition: " + combined[-500:])


if __name__ == "__main__":
    unittest.main()
