"""Fixture factory and report harness for the suite.

One builder builds every synthetic tree: build_case, driven by a
compact case table for each fixture. A case table is plain data only:
strings, bytes, tuples, and dicts. No callable and no conditional
stands inside a case; a case that needs a conditional gets its own
builder passage in this module instead, and a new subcase is a new
table entry, not a new builder.

Case table form. A case is a dict with these keys:

  name: the case name, a plain string. The built tree root is the
    caller supplied root joined with this name, so a test names its
    tree by the case name and reads the built root as the return
    value of build_case or build_cases.
  features: a tuple of feature tokens, each one a member of the
    closed enumerated vocabulary in FEATURE_VOCABULARY below. A token
    outside the vocabulary is refused.
  files: a dict mapping a tree relative path to the text or bytes to
    place in that file. Paths are relative to the built tree root,
    which is the design root the tool is pointed at.
  malformations: a tuple of malformation switch dicts, each naming
    its switch, its target piece by path and by kind, and its state,
    in the form MALFORMATION_SWITCHES states. Corrected and repaired
    cases also name the correcting or repaired piece and the
    citation the assertion checks.
  f11: an F-11 limit spec dict, present on F-11 cases only, naming
    one figure of F11_SETTINGS and one position, at-limit or
    one-over. An F-11 case carries no files: its tree holds filler
    only, in the form the F-11 stating entry states.
  dirs: a tuple of tree relative paths of empty directories to make.
  links: a dict mapping a tree relative link path to the tree
    relative path it points at.

How a test invokes a build. The test makes a temporary directory at
run time, for example with tracked_tempdir from this module, passes
it as the root, and calls build_case(case, root) for one tree or
build_cases(cases, root) for a set of trees standing side by side.
build_case returns the built tree root as a Path; build_cases
returns a dict mapping each case name to its built tree root. The
test then runs the tool or the capture seam against that root. Pair
cases and invocation cases stand outside the factory in prose form
in their test modules; the factory supports them only through
build_cases building each tree of a pair from its own case table.

The file writing passage, the run harness, and the report reading
helpers that the standing suite modules import stand below the
factory section of this module, unchanged in form.
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

# ------------------------------------------------------------------
# Factory section: the closed vocabulary, the switches, the limits.
# ------------------------------------------------------------------

# Piece kinds, in the shortened names the factory enumeration uses,
# each mapped to the kind it names. GF and AD carry no completeness
# signal as a malformation target in any family.
PIECE_KINDS = {
    "PL": "path ledger",
    "MR": "metrics record",
    "SR": "step record",
    "GF": "gate file",
    "AP": "audit paper",
    "RG": "register",
    "CL": "cost ledger",
    "DQ": "decision queue file",
    "TR": "trace record",
    "CR": "correcting record",
    "AD": "adjudication",
}

# The three internal completeness signals a valid text file with no
# truncation marker is tested by, in the forms the plan states.
COMPLETENESS_SIGNALS = ("signal-one", "signal-two", "signal-three")

# Which signals each piece kind carries as a malformation target,
# under the verified factory enumeration. Kinds absent from a tuple
# carry that signal in no family.
SIGNAL_TARGETS = {
    "signal-one": ("PL", "MR", "SR", "AP", "RG", "CL", "DQ", "TR"),
    "signal-two": ("MR", "SR", "AP", "RG", "CL", "DQ"),
    "signal-three": ("MR", "SR", "AP", "RG"),
}

# The closed enumerated feature vocabulary, family by family in
# scope: content settings stand beside tree shape settings. A case
# names its features from this vocabulary only, and the vocabulary
# grows only by a recorded design act, never inside a case.
FEATURE_VOCABULARY = {
    "content": (
        "scale-naming",
        "parts-fail-sum",
        "unreconciled-figure",
        "named-governing-correction",
        "recycle-pointer",
        "proxy-label",
        "figure-credited-to-other-step",
        "full-clock-timestamps",
        "date-only-timestamps",
        "flow-scale-breakdowns",
        "commissioned-scale-breakdowns",
        "decision-items-full-timestamps",
        "decision-items-date-only-raised",
        "origin-step-on-register-entries",
        "first-ruling-outcome-per-step",
        "first-trace-per-counted-step",
        "placeholder-zero",
        "measured-zero",
        "printed-zero",
        "whole-build-money-statement",
        "per-step-money-figures",
        "token-figures-in-ledger",
        "unknown-definitions-version",
        "halt-statement-recognised",
        "halt-wording-unrecognised",
        "additions-over-base-stated",
        "total-only-step",
        "banked-entries-with-duration",
        "banked-entries-no-duration",
    ),
    "tree-shape": (
        "single-page-metrics-record",
        "split-metrics-record",
        "cost-ledger-inside-root",
        "queue-file-inside-root",
        "decision-table-inside-root",
        "queue-governs-over-table",
        "gate-record-name",
        "gate-ruling-name",
        "gate-adjudication-evidence",
        "near-match-name",
        "duplicate-identity-two-paths",
        "restart-instance",
        "recycled-instance",
        "open-build",
        "closed-build",
        "empty-round-tables",
        "step-rows-to-step-18",
        "second-shape-habits",
    ),
}
FEATURES = frozenset(
    token for group in FEATURE_VOCABULARY.values() for token in group)

# Malformation switches, closed. Each switch names the target piece,
# its state, and, where the form is a corrected or a repaired case,
# the correcting or repaired piece and the citation the assertion
# checks. required names the fields a switch dict must carry beside
# switch, target, target_kind, and state; forbidden names the fields
# it must not carry.
MALFORMATION_SWITCHES = {
    "M-01": {
        "form": "malformed piece, not valid text",
        "states": ("not-valid-text",),
        "required": (),
        "forbidden": ("correcting_piece", "repaired_piece", "citation",
                      "signal"),
    },
    "M-02": {
        "form": "marked truncated piece, no correcting record",
        "states": ("marked-truncated",),
        "required": (),
        "forbidden": ("correcting_piece", "repaired_piece", "citation",
                      "signal"),
    },
    "M-03": {
        "form": "marked truncated piece, with a correcting record",
        "states": ("marked-truncated",),
        "required": ("correcting_piece", "citation"),
        "forbidden": ("repaired_piece", "signal"),
    },
    "M-04": {
        "form": "repaired truncation, repair cited in the piece",
        "states": ("repaired-truncated",),
        "required": ("repaired_piece", "citation"),
        "forbidden": ("correcting_piece", "signal"),
    },
    "M-05": {
        "form": "unmarked truncation, one completeness signal failed",
        "states": ("signal-failed",),
        "required": ("signal",),
        "forbidden": ("correcting_piece", "repaired_piece", "citation"),
    },
    "M-06": {
        "form": "correcting record itself failing or truncated",
        "states": ("correcting-record-fails-signal",
                   "correcting-record-truncated"),
        "required": ("correcting_piece", "citation"),
        "forbidden": ("repaired_piece",),
    },
}

TRUNCATION_MARKER = "TRUNCATED"
MALFORMED_BYTES = b"\xff\xfe\xfd malformed piece, not valid text\n"

# The F-11 limits as separate settings with exact counts: four
# settings carrying five figures. largest-file carries one figure;
# the tree setting carries two figures, total bytes and file count,
# stated as two settings here so each figure stands as its own exact
# count; longest-line carries one figure; whole-walk carries one
# figure. Filler used to reach a count carries no recognisable piece
# and no figure: filler content is the letter x repeated, filler
# names match no closed name pattern and stand as no near match.
F11_SETTINGS = {
    "largest-file-bytes": 1000000,
    "tree-total-bytes": 25000000,
    "tree-file-count": 2000,
    "longest-line-bytes": 65536,
    "whole-walk-entries": 10000,
}
F11_POSITIONS = ("at-limit", "one-over")

# The F-10 pair position: the affected metric and the unaffected
# metric for family F-10, as the verified stating entry states them.
F10_AFFECTED_METRIC = "Q-1"
F10_UNAFFECTED_METRIC = "E-1"


def _filler_stem(index):
    """Return the letters only sequence for filler entry index."""
    letters = ""
    n = index
    while True:
        letters = chr(ord("a") + (n % 26)) + letters
        n = n // 26 - 1
        if n < 0:
            return "filler" + letters


def _check_rel_path(rel):
    path = Path(rel)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError("case path is not a tree relative path: %r"
                         % (rel,))
    return path


def _validate_case(case):
    if not isinstance(case, dict):
        raise ValueError("a case is a dict of plain data")
    name = case.get("name")
    if not isinstance(name, str) or not name or "/" in name \
            or "\\" in name or name in (".", ".."):
        raise ValueError("a case names its tree with a plain name")
    for key in case:
        if key not in ("name", "features", "files", "malformations",
                       "f11", "dirs", "links"):
            raise ValueError("case key outside the case form: %r"
                             % (key,))
    for token in case.get("features", ()):
        if token not in FEATURES:
            raise ValueError("feature outside the closed vocabulary: "
                             "%r" % (token,))
    files = case.get("files", {})
    if not isinstance(files, dict):
        raise ValueError("case files stand as a dict of path to content")
    for rel, content in files.items():
        _check_rel_path(rel)
        if not isinstance(content, (str, bytes)):
            raise ValueError("case file content is text or bytes only, "
                             "with no callable inside a case: %r" % (rel,))
    for rel in case.get("dirs", ()):
        _check_rel_path(rel)
    for rel, target in case.get("links", {}).items():
        _check_rel_path(rel)
        _check_rel_path(target)
    if "f11" in case and files:
        raise ValueError("an F-11 case holds filler only and no files")
    if "f11" in case:
        spec = case["f11"]
        if spec.get("figure") not in F11_SETTINGS:
            raise ValueError("F-11 figure outside the five figures: %r"
                             % (spec.get("figure"),))
        if spec.get("position") not in F11_POSITIONS:
            raise ValueError("F-11 position is at-limit or one-over")
    for switch in case.get("malformations", ()):
        _validate_switch(switch, files)


def _validate_switch(switch, files):
    if not isinstance(switch, dict):
        raise ValueError("a malformation switch stands as a dict")
    form = MALFORMATION_SWITCHES.get(switch.get("switch"))
    if form is None:
        raise ValueError("malformation switch outside the closed set: "
                         "%r" % (switch.get("switch"),))
    target = switch.get("target")
    if not isinstance(target, str) or target not in files:
        raise ValueError("a switch names its target piece among the "
                         "case files: %r" % (target,))
    if switch.get("target_kind") not in PIECE_KINDS:
        raise ValueError("a switch names its target kind: %r"
                         % (switch.get("target_kind"),))
    if switch.get("state") not in form["states"]:
        raise ValueError("switch state outside its form: %r"
                         % (switch.get("state"),))
    for field in form["required"]:
        if not switch.get(field):
            raise ValueError("switch %s requires the field %s"
                             % (switch["switch"], field))
    for field in form["forbidden"]:
        if switch.get(field):
            raise ValueError("switch %s forbids the field %s"
                             % (switch["switch"], field))
    for field in ("correcting_piece", "repaired_piece"):
        piece = switch.get(field)
        if piece and piece not in files:
            raise ValueError("the %s stands among the case files: %r"
                             % (field, piece))
    if switch["switch"] == "M-05":
        signal = switch.get("signal")
        if signal not in COMPLETENESS_SIGNALS:
            raise ValueError("M-05 names one completeness signal")
        if switch["target_kind"] not in SIGNAL_TARGETS[signal]:
            raise ValueError("kind %s carries no %s as a target"
                             % (switch["target_kind"], signal))
        if switch.get("exception"):
            raise ValueError("an M-05 row with an exception standing "
                             "is not an unmarked truncation row")
    if switch["switch"] in ("M-03", "M-04", "M-06"):
        holder = switch.get("correcting_piece") \
            or switch.get("repaired_piece")
        content = files[holder]
        if isinstance(content, bytes):
            content = content.decode("utf-8", "replace")
        if switch["citation"] not in content:
            raise ValueError("the citation stands in the correcting "
                             "or repaired piece it names")


def _apply_switch(root, switch):
    target = root / switch["target"]
    kind = switch["switch"]
    if kind == "M-01":
        target.write_bytes(MALFORMED_BYTES)
    elif kind in ("M-02", "M-03"):
        text = target.read_text(encoding="utf-8")
        if not text.endswith("\n"):
            text += "\n"
        target.write_text(text + TRUNCATION_MARKER + "\n",
                          encoding="utf-8")
    elif kind == "M-06" \
            and switch["state"] == "correcting-record-truncated":
        piece = root / switch["correcting_piece"]
        text = piece.read_text(encoding="utf-8")
        if not text.endswith("\n"):
            text += "\n"
        piece.write_text(text + TRUNCATION_MARKER + "\n",
                         encoding="utf-8")
    # M-04, M-05, and the M-06 signal form change no bytes: the case
    # file content itself carries the repair citation, the failed
    # signal, or the failing correcting record, in its stated form.


def _filler_line_file(root, name, lines, extra_byte):
    text = ("x" * 999 + "\n") * lines
    if extra_byte:
        text += "x"
    (root / name).write_text(text, encoding="utf-8")


def _build_f11(root, spec):
    figure = spec["figure"]
    over = spec["position"] == "one-over"
    if figure == "largest-file-bytes":
        _filler_line_file(root, _filler_stem(0), 1000, over)
    elif figure == "tree-total-bytes":
        for index in range(25):
            _filler_line_file(root, _filler_stem(index), 1000, False)
        if over:
            (root / _filler_stem(25)).write_text("x", encoding="utf-8")
    elif figure == "tree-file-count":
        count = 2001 if over else 2000
        for index in range(count):
            (root / _filler_stem(index)).write_bytes(b"")
    elif figure == "longest-line-bytes":
        size = 65537 if over else 65536
        (root / _filler_stem(0)).write_text("x" * size,
                                            encoding="utf-8")
    elif figure == "whole-walk-entries":
        count = 10001 if over else 10000
        for index in range(count):
            (root / _filler_stem(index)).mkdir()


def build_case(case, root):
    """Build one fixture tree from a case table under a root.

    root is the caller supplied directory, made by the caller in a
    temporary directory at test run time. The built tree root is
    root joined with the case name, and that Path is returned. The
    build is deterministic: files stand in sorted path order, and
    no timestamp, random value, or run fact enters any file.
    """
    _validate_case(case)
    tree = Path(root) / case["name"]
    if tree.exists():
        raise ValueError("the case tree root already stands: %s"
                         % (tree,))
    tree.mkdir(parents=True)
    files = case.get("files", {})
    for rel in sorted(files):
        target = tree / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        content = files[rel]
        if isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding="utf-8")
    for rel in case.get("dirs", ()):
        (tree / rel).mkdir(parents=True, exist_ok=True)
    for rel in sorted(case.get("links", {})):
        link = tree / rel
        link.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(str(tree / case["links"][rel]), str(link))
    for switch in case.get("malformations", ()):
        _apply_switch(tree, switch)
    if "f11" in case:
        _build_f11(tree, case["f11"])
    return tree


def build_cases(cases, root):
    """Build a set of case tables side by side under one root.

    Returns a dict mapping each case name to its built tree root.
    Pair cases authored in prose in a test module build their two
    trees through this entry, one case table per tree.
    """
    built = {}
    for case in cases:
        built[case["name"]] = build_case(case, root)
    return built


def measure_tree(root):
    """Measure a built tree: counts a test or a check can assert.

    Returns a dict with file count, directory count under the root,
    entries in all (files plus directories under the root), total
    bytes over files, and the longest line in bytes over files.
    """
    root = Path(root)
    files = 0
    dirs = 0
    total = 0
    longest = 0
    for path in root.rglob("*"):
        if path.is_symlink():
            continue
        if path.is_dir():
            dirs += 1
        elif path.is_file():
            files += 1
            data = path.read_bytes()
            total += len(data)
            for line in data.split(b"\n"):
                if len(line) > longest:
                    longest = len(line)
    return {"files": files, "dirs": dirs, "entries": files + dirs,
            "total_bytes": total, "longest_line": longest}


def single_page_metrics_record_files(text):
    """Named case fragment: the metrics record in single page form."""
    return {"wiki/wiki/synthesis/build-metrics-record.md": text}


def split_metrics_record_files(page_texts):
    """Named case fragment: the metrics record split across pages.

    page_texts stands in page order; page one takes the single page
    path and each later page takes the next page path beside it.
    """
    files = {}
    for index, text in enumerate(page_texts):
        if index == 0:
            rel = "wiki/wiki/synthesis/build-metrics-record.md"
        else:
            rel = "wiki/wiki/synthesis/build-metrics-record-page-%d.md" \
                % (index + 1)
        files[rel] = text
    return files


# The ten F-11 case tables: five figures, each at its limit and at
# one unit over it, in four settings, as the verified F-11 stating
# entry states them. Built counts, whole tree, filler only:
# largest-file-bytes 1000000 and 1000001 bytes in one file;
# tree-total-bytes 25000000 bytes in 25 files and 25000001 bytes in
# 26 files; tree-file-count 2000 and 2001 empty files;
# longest-line-bytes 65536 and 65537 bytes in one single line file;
# whole-walk-entries 10000 and 10001 empty directories.
F11_CASES = tuple(
    {"name": "f11-%s-%s" % (figure, position), "features": (),
     "f11": {"figure": figure, "position": position}}
    for figure in F11_SETTINGS for position in F11_POSITIONS)


def _f10_files(malformed):
    files = {
        "steps/step-01-record.md": (
            "# Step 1 record\n\nBuild: metrics fixture build.\n"
            "Base: 2. Team staffed: 2 agents. Total spins: 4.\n"),
        "steps/step-01-roster.md": (
            "# Step 1 roster\n\nNamed agents: 2. Base: 2.\n"
            "Roster additions over base: 0.\n"),
        "audit/step-01-round-record.md": (
            "# Round record, step 1\n\nPost triage severity breakdown, "
            "flow scale: Critical 0, High 1, Medium 2, Low 3.\n"
            "Citation: round record for step 1 stands as the Q-1 "
            "feeder.\n"),
        "PATH-LEDGER.md": (
            "# Path ledger\n\nSteps stated: 1.\n\n## Transitions\n\n"
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 "
            "17:00.\n"),
    }
    return files


def f10_cases():
    """Return the F-10 pair of case tables, sound and malformed.

    The two trees differ only in the Q-1 feeder, the round record:
    sound in the first, malformed under switch M-01 in the second.
    The affected metric is Q-1 and the unaffected metric is E-1, as
    F10_AFFECTED_METRIC and F10_UNAFFECTED_METRIC state; the E-1
    feeders, the step record and the roster, stand identical in
    both trees. The pair relation itself stands in prose in its
    test module; this passage builds the two trees only.
    """
    sound = {"name": "f10-sound",
             "features": ("flow-scale-breakdowns",),
             "files": _f10_files(False)}
    malformed = {"name": "f10-malformed",
                 "features": ("flow-scale-breakdowns",),
                 "files": _f10_files(True),
                 "malformations": (
                     {"switch": "M-01",
                      "target": "audit/step-01-round-record.md",
                      "target_kind": "AP",
                      "state": "not-valid-text"},)}
    return (sound, malformed)


def f16_miniature_case():
    """Return the F-16 miniature case table, at its stated counts.

    The copy carries 57 files in all, in five groups: 1 path ledger
    file in the root group; 23 step record files, 23 roster
    artifacts, 4 gate variant files, and 1 trace record file in the
    steps group; 2 audit papers in the audit group; 2 register
    files in the registers group; and 1 metrics record page in the
    synthesis group. Every count stands as the verified F-16
    stating entry states it; the kept numbers stand at their
    governed values and no count here shrinks one of them.
    """
    files = {}
    transitions = []
    for step in range(1, 19):
        transitions.append("Step %d closed 2026-11-01." % step)
    transitions.append("BANKED entry one, no duration stated.")
    transitions.append("BANKED entry two, no duration stated.")
    files["PATH-LEDGER.md"] = (
        "# Path ledger\n\nSteps stated: 1 to 18.\n\n## Transitions\n\n"
        + "\n".join(transitions) + "\n")
    for step in range(1, 24):
        body = "# Step %d record\n\nBuild: metrics fixture build.\n" \
            % step
        if step in (3, 5):
            body += "Roster additions over base: 1.\n"
        if step == 3:
            body += ("Budget position: money 0 external spend for the "
                     "whole build; agent count ceiling of 10 "
                     "documented units on a labelled proxy basis; "
                     "tokens NOT RECORDED.\n")
        if step == 23:
            body += ("Final position: 8 of 10 documented units on a "
                     "labelled proxy basis; money nil; tokens NOT "
                     "RECORDED.\n")
        files["steps/step-%02d-record.md" % step] = body
        roster = "# Step %d roster\n\nNamed agents: 2.\n" % step
        if step <= 18:
            roster += "Base: 2.\n"
        files["steps/step-%02d-roster.md" % step] = roster
    files["steps/step-06-gate-record.md"] = (
        "# Step 6 gate record\n\nClosure state: CLOSED-PASS.\n"
        "First trace for step 6: 2 LANDED of 2 items checked, "
        "0 PARTIAL, 0 CONTRADICTED.\n")
    files["steps/step-08-gate-record.md"] = (
        "# Step 8 gate record\n\nClosure state: CLOSED-PASS.\n"
        "First trace for step 8: 2 LANDED of 2 items checked, "
        "0 PARTIAL, 0 CONTRADICTED.\n")
    files["steps/step-08-gate-adjudication.md"] = (
        "# Step 8 gate adjudication\n\nEvidence beside the step 8 "
        "gate record; counted as a gate file in no count.\n")
    files["steps/step-20-gate-ruling.md"] = (
        "# Step 20 gate ruling\n\nClosure state: CLOSED-PASS.\n"
        "First trace for step 20, summarised here: 2 LANDED of 2 "
        "items checked, 0 PARTIAL, 0 CONTRADICTED.\n")
    files["steps/step-13-trace-record.md"] = (
        "# Step 13 first trace record\n\nParts: 2 LANDED, 1 PARTIAL, "
        "0 CONTRADICTED. Stated total: 2 items checked.\n")
    files["audit/step-17-audit-paper.md"] = (
        "# Step 17 audit paper\n\nFindings stand in part.\n"
        + TRUNCATION_MARKER + "\n")
    files["audit/step-19-purple-audit-paper.md"] = (
        "# Step 19 Purple audit paper\n\nFirst trace for step 19: "
        "2 LANDED of 2 items checked, 0 PARTIAL, 0 CONTRADICTED.\n")
    files["registers/fix-register.md"] = (
        "# Fix register\n\nEntry one: a fix entry carrying no origin "
        "step field.\n")
    files["registers/defect-register.md"] = (
        "# Defect register\n\nEntry one: a defect entry carrying no "
        "origin step field.\n")
    step_rows = "\n".join(
        "Step %d row." % step for step in range(1, 19))
    closing = "\n".join(
        "Closing entry for step %d, dated 2026-11-01." % step
        for step in range(1, 19))
    metrics = (
        "# Build metrics record\n\n## Build header\n\nBuild: metrics "
        "fixture build.\n\n## Record change statement\n\nNo change.\n"
        "\n## Step table\n\n" + step_rows + "\nQ-3 column printed "
        "zero: 0\n\n## Loop round table\n\nNo rows.\n\n## Decision "
        "table\n\n| Item | Origin step | Raised | Presented | Ruled |"
        "\n| --- | --- | --- | --- | --- |\n| Item one | 3 | "
        "2026-11-01 |  |  |\n| Item two | 3 | 2026-11-01 |  |  |\n"
        "Latency on each item: not yet countable.\n\n## Audit round "
        "table\n\nNo rows.\n\n## Admission review table\n\nNo rows.\n"
        "\n## Build summary\n\nNo computed figure stands here.\n\n"
        "## Corrections\n\nNo corrections.\n\n## Dated closing "
        "entries\n\n" + closing + "\n")
    files.update(single_page_metrics_record_files(metrics))
    return {
        "name": "f16-miniature",
        "features": (
            "date-only-timestamps", "single-page-metrics-record",
            "decision-table-inside-root", "gate-record-name",
            "gate-ruling-name", "gate-adjudication-evidence",
            "empty-round-tables", "step-rows-to-step-18",
            "banked-entries-no-duration", "printed-zero",
            "proxy-label", "additions-over-base-stated",
            "whole-build-money-statement",
            "first-trace-per-counted-step", "parts-fail-sum"),
        "files": files,
    }


F16_FILE_COUNT = 57


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
