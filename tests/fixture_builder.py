"""Fixture construction and report harness for the suite.

One builder builds every synthetic tree. A case is a compact table that
names the files to write and the text or bytes to place in each file.
A case that needs a conditional gets its own builder passage instead.

Every tree and suite copy built through this module is registered for
removal: FixtureTestCase removes, at the end of each test, every handle
created since that test began, and an exit hook removes any handle a
test class did not claim, so repeated full runs leave nothing behind.
"""
import atexit
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_ROOT = Path.home() / "workspace" / "fold-in-trace-checker" / "design"
STARTER_ORDER = ["T-1", "T-2", "T-4", "T-7", "E-1", "E-2", "E-3", "E-4",
                 "F-2", "Q-1", "Q-3", "Q-4", "D-1", "B-1", "B-2", "B-3", "B-4"]
REASON_CODES = ["missing-field", "no-feeder-record", "date-only-form",
                "no-post-triage-breakdown", "no-measurement-basis",
                "truncated-no-correcting-record", "record-disagrees",
                "unreconciled-figure", "unknown-definitions-version",
                "no-named-rule", "partial-span", "governing-scale-conflict",
                "over-limit-piece", "malformed-piece", "unreadable-piece"]
VERDICTS = ("present but not derivable", "present", "missing")

_CREATED_HANDLES = []


def _remove_handle(handle):
    shutil.rmtree(handle, ignore_errors=True)


def _cleanup_all_handles():
    for handle in list(_CREATED_HANDLES):
        _remove_handle(handle)
    del _CREATED_HANDLES[:]


atexit.register(_cleanup_all_handles)


def register_handle(handle):
    """Register a temporary directory handle for removal."""
    _CREATED_HANDLES.append(str(handle))
    return handle


def tracked_tempdir(prefix):
    """Create a temporary directory that is registered for removal."""
    return Path(register_handle(tempfile.mkdtemp(prefix=prefix)))


class FixtureTestCase(unittest.TestCase):
    """Base class that removes every fixture handle a test created."""

    def setUp(self):
        self._handle_mark = len(_CREATED_HANDLES)

    def tearDown(self):
        created = _CREATED_HANDLES[self._handle_mark:]
        del _CREATED_HANDLES[self._handle_mark:]
        for handle in created:
            _remove_handle(handle)


def build_tree(case_table):
    """Build one synthetic tree from a case table and return its root."""
    handle = register_handle(tempfile.mkdtemp(prefix="msc_fixture_"))
    root = Path(handle) / "design"
    root.mkdir()
    for rel, content in case_table.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding="utf-8")
    return root


def link_tree(case_table, links):
    """Build a tree and then add the links a case table names."""
    root = build_tree(case_table)
    for rel, target_rel in links.items():
        link = root / rel
        link.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(str(root / target_rel), str(link))
    return root


def run_tool(root, extra=(), env_extra=None, cwd=None):
    """Run the product through the module entry route as a subprocess."""
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    cmd = [sys.executable, "-m", "metrics_starter_collector", str(root)]
    cmd.extend(extra)
    return subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(cwd or REPO_ROOT), env=env, timeout=120)


def run_tool_no_root(extra=()):
    env = dict(os.environ)
    cmd = [sys.executable, "-m", "metrics_starter_collector"]
    cmd.extend(extra)
    return subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(REPO_ROOT), env=env, timeout=120)


def _normalised(line):
    return line.strip().lstrip("|").strip().lstrip("#-*>" ).strip()


def _row_start_code(line):
    """Return the starter code a line opens a row for, or None.

    One row extraction rule, tied to the settled report row form: a row
    opens on a line whose text, after any Markdown prefix characters
    (pipe, heading marks, list marks) are stripped, begins with one
    starter code followed by a delimiter, and whose line carries one of
    the three verdicts as a delimited field. Any other line, including
    a header or inventory line that merely mentions a code, opens no
    row, and a row ends at the next row opening line or at the next
    section heading line.
    """
    text = _normalised(line)
    for code in STARTER_ORDER:
        if text == code or text.startswith(code + " ") or \
                text.startswith(code + "|") or text.startswith(code + ":") or \
                text.startswith(code + "\t"):
            if row_verdict(line) is not None:
                return code
            return None
    return None


def row_verdict(text):
    """Return the first verdict standing as a delimited field, or None.

    The three verdicts are matched as whole fields so that present,
    missing and present but not derivable are mutually exclusive: a
    bare present match never fires on a present but not derivable
    field, because the longer field is matched first and the present
    pattern carries a negative lookahead for the longer form.
    """
    best = None
    best_at = None
    patterns = (
        ("present but not derivable",
         r"(?<![A-Za-z])present but not derivable(?![A-Za-z])"),
        ("present", r"(?<![A-Za-z])present(?!\s+but\s+not\s+derivable)"
                    r"(?![A-Za-z])"),
        ("missing", r"(?<![A-Za-z])missing(?![A-Za-z])"),
    )
    for verdict, pattern in patterns:
        match = re.search(pattern, text)
        if match and (best_at is None or match.start() < best_at):
            best = verdict
            best_at = match.start()
    return best


def assert_verdict(test, block, expected, code=""):
    """Assert a row block carries exactly the expected verdict."""
    test.assertTrue(block, "empty row block for " + (code or expected))
    test.assertEqual(row_verdict(block), expected,
                     "row %s verdict is not %r in block: %s"
                     % (code, expected, block[:400]))


def row_block(report, code):
    """Return the report text that belongs to one metric row."""
    lines = report.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if _row_start_code(line) == code:
            start = idx
            break
    if start is None:
        return ""
    end = len(lines)
    for idx in range(start + 1, len(lines)):
        if _row_start_code(lines[idx]) is not None:
            end = idx
            break
        stripped = lines[idx].strip()
        if stripped.startswith("#") and _normalised(stripped)[:1].isalpha() \
                and _row_start_code(lines[idx]) is None \
                and any(word in stripped.lower() for word in
                        ("data quality", "piece inventory", "coverage")):
            end = idx
            break
    return "\n".join(lines[start:end])


def row_order(report):
    """Return the starter codes in the order their rows first stand."""
    found = []
    for line in report.splitlines():
        stripped = line.strip().lstrip("#-*|> ").strip()
        for code in STARTER_ORDER:
            if stripped.startswith(code) and code not in found:
                found.append(code)
    return found


def statement_segment(block):
    """Return the statement line segment of a row block, or empty.

    The segment runs from the statement line label to the end of the
    row block. A block with no statement line label yields an empty
    segment, so an assertion on the segment fails where the marking
    does not stand in a statement line at all.
    """
    lowered = block.lower()
    at = lowered.find("statement line")
    if at < 0:
        return ""
    return block[at:]


def header_region(report):
    """Return the report text before the first metric row."""
    lines = report.splitlines()
    for idx, line in enumerate(lines):
        if _row_start_code(line) is not None:
            return "\n".join(lines[:idx])
    return report


def coverage_statement(report):
    """Return the header coverage statement text, or empty.

    The coverage statement is the part of the header that follows the
    coverage statement label and precedes the piece inventory and the
    first metric row.
    """
    head = header_region(report)
    lowered = head.lower()
    at = lowered.find("coverage statement")
    if at < 0:
        at = lowered.find("coverage")
    if at < 0:
        return ""
    tail = head[at:]
    tail_lower = tail.lower()
    cut = tail_lower.find("piece inventory")
    if cut > 0:
        tail = tail[:cut]
    return tail


def data_quality_section(report):
    """Return the data quality section text, or empty."""
    lines = report.splitlines()
    for idx, line in enumerate(lines):
        if "data quality" in line.lower() and _row_start_code(line) is None:
            return "\n".join(lines[idx:])
    return ""


def data_quality_entry_for(report, name):
    """Return the data quality entry naming a piece, with its window."""
    section = data_quality_section(report)
    lines = section.splitlines()
    for idx, line in enumerate(lines):
        if name in line:
            return "\n".join(lines[idx:idx + 4])
    return ""


def piece_entry_for(report, name):
    """Return the piece inventory entry naming a piece, with window."""
    lines = report.splitlines()
    for idx, line in enumerate(lines):
        if name in line and _row_start_code(line) is None:
            return "\n".join(lines[idx:idx + 3])
    return ""


def split_two_part(text):
    """Split a two part form text at its labels.

    Returns (first_part, second_part, shows_at, follows_at) where the
    parts are the text after each label and the positions are the
    label offsets inside the text, so label order is checkable by
    index rather than true by construction.
    """
    lowered = text.lower()
    shows_at = lowered.find("what the record shows")
    follows_at = lowered.find("what follows")
    if shows_at < 0 or follows_at < 0:
        return "", "", shows_at, follows_at
    first = text[shows_at:follows_at] if follows_at > shows_at else ""
    second = text[follows_at:]
    return first, second, shows_at, follows_at


def second_part_body(second):
    """Return the second part text after its label and colon."""
    body = second
    lowered = body.lower()
    at = lowered.find("what follows")
    if at >= 0:
        body = body[at + len("what follows"):]
    body = body.strip()
    if body.lower().startswith("under the stated rule"):
        body = body[len("under the stated rule"):]
    return body.strip().lstrip(":").strip()


def assert_two_part_form(test, text, expected_start, label=""):
    """Assert the A7-10 two part form on one reason line or entry.

    First part before second part by index, first part free of every
    reason code, and the second part beginning with the expected code
    or with the words that no code fits, as expected_start states.
    """
    first, second, shows_at, follows_at = split_two_part(text)
    test.assertTrue(0 <= shows_at < follows_at,
                    "two part labels out of order or absent: " + label)
    for code in REASON_CODES:
        test.assertNotIn(code, first.lower(),
                         "code in first part: " + label)
    test.assertNotIn("no code fits", first.lower(),
                     "no code fits wording in first part: " + label)
    body = second_part_body(second)
    test.assertTrue(body.lower().startswith(expected_start.lower()),
                    "second part does not begin with %r: %s"
                    % (expected_start, label))


def manifest(root):
    """Return a manifest of relative paths and SHA-256 hashes."""
    result = {}
    for path in sorted(Path(root).rglob("*")):
        if path.is_file() and not path.is_symlink():
            result[str(path.relative_to(root))] = hashlib.sha256(
                path.read_bytes()).hexdigest()
    return result


def _find_callable(module, names):
    for name in names:
        fn = getattr(module, name, None)
        if callable(fn):
            return fn
    return None


def capture_derive_render(test, root):
    """Capture once, then derive and render from that capture only.

    Uses the capture seam the product exposes at its contract
    boundary: the shell capture function that produces the one
    CapturedRead, the core derivation that consumes a CapturedRead
    and no other input, and the renderer that prints the model.
    Where the product package does not stand, the test fails in the
    designed red form rather than erroring.
    """
    try:
        import metrics_starter_collector.derivation_core as core
        import metrics_starter_collector.report_renderer as renderer
        import metrics_starter_collector.shell_reader as shell
    except ImportError:
        test.fail("product package absent: the capture seam the "
                  "Contract 1 proof needs does not stand")
    capture_fn = _find_callable(
        shell, ("capture_read", "capture", "read_tree", "build_capture"))
    derive_fn = _find_callable(
        core, ("derive_report", "derive", "build_report", "derive_all"))
    render_fn = _find_callable(
        renderer, ("render_report", "render", "render_text", "print_report"))
    if capture_fn is None or derive_fn is None or render_fn is None:
        test.fail("product does not expose the capture, derive and "
                  "render seam Contract 1 names")
    return capture_fn, derive_fn, render_fn


def assert_reads_capture_only(test, root, count_reads=False):
    """Assert a family derives from the one capture and nothing else.

    The capture is taken first. The tree is then removed outright, so
    any later read of the tree must fail or change the report. The
    report derived from the capture after the removal must equal the
    capture based report derived before it. Where count_reads holds,
    filesystem reads under the root during the second derivation are
    counted and asserted zero. The counter covers every read form a
    derivation can use: builtins open, io.open, os.open, os.listdir,
    os.scandir, and the pathlib read forms Path.read_text,
    Path.read_bytes and Path.open. A read is recorded before it is
    attempted, so a rereading derivation that falls back to the
    captured text when the removed tree read fails is still caught.
    """
    import builtins
    import io
    capture_fn, derive_fn, render_fn = capture_derive_render(test, root)
    captured = capture_fn(root)
    baseline = render_fn(derive_fn(captured))
    test.assertTrue(baseline)
    root_path = Path(root).resolve()
    shutil.rmtree(str(root))
    reads = []

    def record(path):
        try:
            resolved = Path(str(path)).resolve()
            if resolved == root_path or root_path in resolved.parents:
                reads.append(str(path))
        except Exception:
            pass

    real_builtin_open = builtins.open
    real_io_open = io.open
    real_os_open = os.open
    real_listdir = os.listdir
    real_scandir = os.scandir
    real_path_read_text = Path.read_text
    real_path_read_bytes = Path.read_bytes
    real_path_open = Path.open

    def counting_builtin_open(file, *args, **kwargs):
        record(file)
        return real_builtin_open(file, *args, **kwargs)

    def counting_io_open(file, *args, **kwargs):
        record(file)
        return real_io_open(file, *args, **kwargs)

    def counting_os_open(path, *args, **kwargs):
        record(path)
        return real_os_open(path, *args, **kwargs)

    def counting_listdir(path="."):
        record(path)
        return real_listdir(path)

    def counting_scandir(path="."):
        record(path)
        return real_scandir(path)

    def counting_read_text(self, *args, **kwargs):
        record(self)
        return real_path_read_text(self, *args, **kwargs)

    def counting_read_bytes(self, *args, **kwargs):
        record(self)
        return real_path_read_bytes(self, *args, **kwargs)

    def counting_path_open(self, *args, **kwargs):
        record(self)
        return real_path_open(self, *args, **kwargs)

    if count_reads:
        builtins.open = counting_builtin_open
        io.open = counting_io_open
        os.open = counting_os_open
        os.listdir = counting_listdir
        os.scandir = counting_scandir
        Path.read_text = counting_read_text
        Path.read_bytes = counting_read_bytes
        Path.open = counting_path_open
    try:
        after = render_fn(derive_fn(captured))
    finally:
        builtins.open = real_builtin_open
        io.open = real_io_open
        os.open = real_os_open
        os.listdir = real_listdir
        os.scandir = real_scandir
        Path.read_text = real_path_read_text
        Path.read_bytes = real_path_read_bytes
        Path.open = real_path_open
    test.assertEqual(after, baseline)
    if count_reads:
        test.assertEqual(reads, [],
                         "reads outside the capture: %s" % reads[:3])


def step_record(step, base=2, team=3, total_spins=4, additions=None,
                closure_note="", extra=""):
    additions_line = ""
    if additions is not None:
        additions_line = "Roster additions over base: %d.\n" % additions
    return ("# Step %d record\n\nBuild: metrics fixture build.\n"
            "Base: %d. Team staffed: %d agents. Total spins: %d.\n%s%s\n%s\n"
            % (step, base, team, total_spins, additions_line, closure_note, extra))


def gate_record(step, closure="CLOSED-PASS", extra=""):
    return ("# Step %d gate record\n\nClosure state: %s.\n%s\n"
            % (step, closure, extra))


def gate_ruling(step, closure="CLOSED-PASS", extra=""):
    return ("# Step %d gate ruling\n\nClosure state: %s.\n%s\n"
            % (step, closure, extra))


def path_ledger(transitions="", steps="1, 2, 3", extra=""):
    return ("# Path ledger\n\nSteps stated: %s.\n\n## Transitions\n\n%s\n%s\n"
            % (steps, transitions, extra))


def metrics_record(body="", header_version=None, decision_table="",
                   split_pages=None):
    version_line = ""
    if header_version is not None:
        version_line = "Definitions version: %s\n" % header_version
    return ("# Build metrics record\n\nBuild: metrics fixture build.\n%s\n%s\n%s\n"
            % (version_line, body, decision_table))


def decision_table(rows):
    lines = ["## Decision table", "",
             "| Item | Origin step | Raised | Presented | Ruled |",
             "| --- | --- | --- | --- | --- |"]
    lines.extend(rows)
    return "\n".join(lines) + "\n"


def queue_file(rows):
    lines = ["# Decision queue", "",
             "| Item | Origin step | Raised | Presented | Ruled |",
             "| --- | --- | --- | --- | --- |"]
    lines.extend(rows)
    return "\n".join(lines) + "\n"


def base_case(steps=(1, 2, 3)):
    """A small complete tree: one case table with no form fault."""
    table = {}
    transitions = []
    for n in steps:
        table["steps/step-%02d-record.md" % n] = step_record(n)
        table["steps/step-%02d-gate-record.md" % n] = gate_record(n)
        transitions.append(
            "Step %d IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00." % n)
    table["PATH-LEDGER.md"] = path_ledger("\n".join(transitions),
                                          ", ".join(str(s) for s in steps))
    table["TIER-RECORD.md"] = "# Tier record\n\nTier: Low. Base: 2.\n"
    table["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
        body="Step table stands complete for the fixture steps.")
    return table
