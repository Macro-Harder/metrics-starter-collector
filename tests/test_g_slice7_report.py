"""Slice 7 tests: report completeness and proof hardening.

This module owns no metric row. It proves the assembled product:
Contract 2, the full set of 17 rows in starter set order; the report
plain text line grammar stated by the spin 775 entry, line by line in
report order, with the D-1 Statement part in the place the spin 794
supplementary entry states, in the full form only, after the
Reconciliation part where one stands, before the Reason part where
one stands, with the Pointer part last; the command grammar of plan
Section 9; the disagreements block, on the spin 778 block ownership
for the unclassifiable disagreement failure form and the spin 774
entry identity as supplemented by the spin 782 pick, one entry per
metric or unit touched; the WV2-21 cross shape comparison cases the
test design record, Part 1, places in this module; and the
determinism cases, A8R-06 in its slice form and EC-48 at report
level. Every WV2-21 case states the EC point numbers it asserts in
its first line, in the record citation form. Fixture trees are built
through the fixture builder into tracked temporary directories, and
the product is invoked through the pre install invocation route, a
subprocess running python3 -m metrics_starter_collector from the
public repo root, with the root argument first.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

from tests.fixture_builder import (
    FixtureTestCase, REPO_ROOT, STARTER_ORDER, build_case, build_cases,
    make_case,
    decision_table, f16_miniature_case, gate_record, gate_ruling,
    manifest, metrics_record, path_ledger, queue_file, row_block,
    row_verdict,
    run_tool, split_metrics_record_files, statement_segment,
    step_record, tracked_tempdir)

ROW_NAMES = {
    "T-1": "Step elapsed time", "T-2": "Step active time",
    "T-4": "Wait on a decision", "T-7": "Loop rounds",
    "E-1": "Agents staffed against base", "E-2": "Spin-ups per step",
    "E-3": "Tokens per step", "E-4": "Money cost per step",
    "F-2": "First-time approval rate",
    "Q-1": "Findings per audit round, by severity",
    "Q-3": "Escaped defects",
    "Q-4": "Fold-in trace landed at first trace",
    "D-1": "Decision latency",
    "B-1": "Total build elapsed and active time",
    "B-2": "Total cost against budget", "B-3": "Slowest three steps",
    "B-4": "Fastest three steps",
}
GOVERNING_WORDINGS = (
    "governed with the pattern named",
    "restatement with its correction named",
    "ungoverned with no verdict depending on it")
GROUP_RESTATEMENTS = "restatements settled by a governing correction"
GROUP_BLOCKING = "contradictions that block or weaken a metric"
DQ_KINDS = ("missing record", "missing field", "wrong form",
            "unreconciled", "not producible")
RULED_ITEM = ("| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
              "2026-11-01 13:00 |")


def base_files(steps=(1, 2, 3)):
    """Return the files dict of a small complete tree, as plain data."""
    files = {}
    transitions = []
    for n in steps:
        files["steps/step-%02d-record.md" % n] = step_record(n)
        files["steps/step-%02d-gate-record.md" % n] = gate_record(n)
        transitions.append(
            "Step %d IN PROGRESS 2026-11-01 09:00, closed "
            "2026-11-01 17:00." % n)
    files["PATH-LEDGER.md"] = path_ledger(
        "\n".join(transitions), ", ".join(str(s) for s in steps))
    files["TIER-RECORD.md"] = "# Tier record\n\nTier: Low. Base: 2.\n"
    files["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
        body="Step table stands complete for the fixture steps.")
    return files


def run_case(case):
    """Build one case under a tracked temporary root and run the tool."""
    root = tracked_tempdir("msc_slice7_")
    built = build_case(case, root)
    return run_tool(built), built


def run_argv(args):
    """Run the module entry route with an exact argument list."""
    cmd = [sys.executable, "-m", "metrics_starter_collector"]
    cmd.extend(str(a) for a in args)
    return subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(REPO_ROOT), timeout=120)


def row_lines(report):
    """Return the verdict row lines of a report, in report order."""
    found = []
    for line in report.splitlines():
        for code in STARTER_ORDER:
            if line.startswith(code + " " + ROW_NAMES[code]):
                found.append(line)
                break
    return found


def row_line(report, code):
    """Return the one verdict row line for a code, or empty."""
    for line in row_lines(report):
        if line.startswith(code + " "):
            return line
    return ""


def row_codes(report):
    """Return the metric codes of the verdict row lines, in order."""
    codes = []
    for line in row_lines(report):
        codes.append(line.split(" ", 1)[0])
    return codes


def parts_of(line):
    """Split a row line into its labelled parts, label to value."""
    parts = {}
    order = []
    for chunk in line.split(" | "):
        chunk = chunk.strip()
        if ": " in chunk:
            label, value = chunk.split(": ", 1)
            parts[label.strip()] = value.strip()
            order.append(label.strip())
        elif chunk:
            order.append(chunk)
    return parts, order


def section_text(report, heading):
    """Return the text from a standalone heading line to the next one."""
    lines = report.splitlines()
    heads = ("Disagreements", "Data quality", "Record cost", "Terms")
    for idx, line in enumerate(lines):
        if line.strip() == heading:
            end = len(lines)
            for later in range(idx + 1, len(lines)):
                if lines[later].strip() in heads:
                    end = later
                    break
            return "\n".join(lines[idx:end])
    return ""


def disagreements_block(report):
    """Return the disagreements block text, or empty."""
    return section_text(report, "Disagreements")


def block_entries(report):
    """Return entry line texts inside the disagreements block."""
    entries = []
    for line in disagreements_block(report).splitlines():
        if line.startswith("Records:"):
            entries.append(line)
    return entries


def assert_usage_error(test, result):
    """Assert the usage error form: exit 2, usage on stderr, no report."""
    test.assertEqual(result.returncode, 2,
                     "exit is not 2: %r, stderr: %s"
                     % (result.returncode, result.stderr[:300]))
    test.assertIn("usage", result.stderr.lower())
    test.assertNotIn("Verdict:", result.stdout)


class TestSlice7Report(FixtureTestCase):

    # Contract 2 and the floor families F-01, F-08, F-09, F-15.

    def test_contract2_full_set_17_rows_starter_order_clean_tree(self):
        """Contract 2; EC-04, EC-41. F-01 clean tree, full set in order."""
        result, built = run_case(make_case("s7-clean", base_files()))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(row_codes(result.stdout), STARTER_ORDER)
        self.assertEqual(len(row_lines(result.stdout)), 17)
        for line in row_lines(result.stdout):
            parts, order = parts_of(line)
            self.assertIn("Verdict", parts)
            self.assertIn("Pointer", parts)
            self.assertEqual(order[-1], "Pointer")

    def test_contract2_full_set_holds_when_rows_are_not_present(self):
        """Contract 2. No row is omitted for a missing verdict."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-01.\n"
            "Step 2 IN PROGRESS 2026-11-01, closed 2026-11-01.\n"
            "Step 3 IN PROGRESS 2026-11-01, closed 2026-11-01.",
            "1, 2, 3")
        result, built = run_case(make_case(
            "s7-not-present", files, features=("date-only-timestamps",)))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(row_codes(result.stdout), STARTER_ORDER)
        block = row_line(result.stdout, "T-1")
        self.assertEqual(row_verdict(block), "missing")
        parts, order = parts_of(block)
        self.assertIn("Reason", parts)
        self.assertEqual(order[-1], "Pointer")

    def test_f08_empty_directory_no_usable_records(self):
        """Floor form. An empty directory gets no verdict rows, exit 0."""
        root = tracked_tempdir("msc_slice7_")
        empty = root / "s7-empty"
        empty.mkdir()
        result = run_tool(empty)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(row_lines(result.stdout), [])
        lines = result.stdout.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].startswith("Root: "))
        self.assertTrue(lines[1].startswith("Build identity: "))
        self.assertTrue(lines[2].startswith("No usable records: "))

    def test_f08_unrecognised_files_only_no_usable_records(self):
        """Floor form. Unrecognised files alone stay under the floor."""
        case = make_case("s7-unrecognised", {
            "notes.txt": "Plain notes with no record piece.\n",
            "random.md": "# Notes\n\nNothing recognisable stands here.\n"})
        result, built = run_case(case)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(row_lines(result.stdout), [])
        self.assertIn("No usable records: ", result.stdout)

    def test_floor_renderer_listing_failure_note_names_no_crossing(self):
        """Fix pass 2 unit 14. The renderer floor form states truly.

        A model handed to the renderer in the floor form, whose
        coverage carries a walk note stating only a directory
        listing failure and no bound crossing, and whose floor
        line names no walk position at all: the renderer floor
        form appends the note from the coverage. It must name
        no walk crossing on such a note, because no bound was
        crossed; it states the note as a walk note, in the
        words the coverage statement uses, with the listing
        failure sentence standing in it truly.
        """
        import metrics_starter_collector.derivation_core as core
        import metrics_starter_collector.report_renderer as renderer
        model = core.ReportModel(
            header_lines=["Root: /floor-renderer-listing",
                          "Build identity: no build identity was "
                          "found inside the tree"],
            coverage=("Coverage statement: step universe 0 steps "
                      "evidenced (none); 0 pieces recognised in "
                      "the capture; 17 rows in starter set order; "
                      "walk note: the directory audit could not "
                      "be listed: list the directory audit: forced "
                      "listing failure; its subtree was not "
                      "visited"),
            inventory_lines=[], results=[], data_quality=[],
            no_usable=True)
        report = renderer.render_report(model)
        lines = report.splitlines()
        self.assertEqual(len(lines), 3)
        floor = lines[2]
        self.assertTrue(floor.startswith("No usable records: "))
        self.assertNotIn("walk crossing", floor)
        self.assertIn("walk note: ", floor)
        self.assertIn("could not be listed", floor)
        self.assertIn("forced listing failure", floor)

    def test_floor_renderer_walk_bound_note_keeps_crossing_wording(self):
        """Fix pass 2 unit 14 control. The renderer keeps a crossing.

        A model handed to the renderer in the floor form, whose
        coverage carries a walk note stating the bound
        crossing, and whose floor line names no walk position
        at all: the renderer floor form appends the crossing
        from the coverage, keeping the walk crossing wording
        and the whole walk bound sentence, as the unit 8 floor
        ground states.
        """
        import metrics_starter_collector.derivation_core as core
        import metrics_starter_collector.report_renderer as renderer
        model = core.ReportModel(
            header_lines=["Root: /floor-renderer-bound",
                          "Build identity: no build identity was "
                          "found inside the tree"],
            coverage=("Coverage statement: step universe 0 steps "
                      "evidenced (none); 0 pieces recognised in "
                      "the capture; 17 rows in starter set order; "
                      "walk note: the whole walk bound of 10000 "
                      "entries was reached and entries beyond it "
                      "were not visited"),
            inventory_lines=[], results=[], data_quality=[],
            no_usable=True)
        report = renderer.render_report(model)
        lines = report.splitlines()
        self.assertEqual(len(lines), 3)
        floor = lines[2]
        self.assertTrue(floor.startswith("No usable records: "))
        self.assertIn("walk crossing: ", floor)
        self.assertIn("whole walk bound", floor)
        self.assertIn("was reached", floor)

    def test_f09_one_recognisable_piece_full_set_partial_marking(self):
        """EC-42. One recognisable piece earns 17 rows, partial marked."""
        case = make_case("s7-just-over-floor", {
            "PATH-LEDGER.md": path_ledger(
                "Step 1 IN PROGRESS 2026-11-01 09:00, closed "
                "2026-11-01 17:00.", "1")})
        result, built = run_case(case)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(row_codes(result.stdout), STARTER_ORDER)
        self.assertIn("Coverage partial: partial report",
                      result.stdout)
        run_cost = [ln for ln in result.stdout.splitlines()
                    if ln.startswith("Run cost: ")]
        self.assertEqual(len(run_cost), 1)

    def test_f15_split_record_same_rows_as_single_page(self):
        """EC-06. The split form yields the same rows as the single page."""
        single = base_files()
        split_files = base_files()
        del split_files["wiki/wiki/synthesis/build-metrics-record.md"]
        split_files.update(split_metrics_record_files([
            "# Build metrics record\n\nPage order: 1.\n\n"
            "Step table stands complete for the fixture steps.\n",
            "# Build metrics record page 2\n\nPage order: 2.\n\n"
            "Closing part of the record.\n"]))
        root = tracked_tempdir("msc_slice7_")
        built = build_cases([
            make_case("s7-single", single,
                      features=("single-page-metrics-record",)),
            make_case("s7-split", split_files,
                      features=("split-metrics-record",))], root)
        first = run_tool(built["s7-single"])
        second = run_tool(built["s7-split"])
        self.assertEqual(first.returncode, 0, first.stderr[:300])
        self.assertEqual(second.returncode, 0, second.stderr[:300])
        self.assertEqual(row_codes(second.stdout), STARTER_ORDER)
        for code in STARTER_ORDER:
            self.assertEqual(
                row_verdict(row_line(first.stdout, code)),
                row_verdict(row_line(second.stdout, code)),
                "row %s differs between the two physical forms" % code)

    def test_f15_single_page_precedence_where_both_forms_stand(self):
        """EC-06. Where both forms stand, the single page governs.

        Row content stands asserted against the single page form on
        the row the split page could touch, as the Slice 1 counterpart
        does: the split page plants a D-1 figure of 4242 hours, and
        the D-1 row must carry the single page form's verdict and
        median, with the planted figure nowhere in the row.
        """
        files = base_files()
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(decision_table=decision_table([RULED_ITEM])))
        files["wiki/wiki/synthesis/build-metrics-record-page-2.md"] = (
            "# Build metrics record page 2\n\nPage order: 2.\n\n"
            "Split copy states the D-1 figure as 4242 hours.\n")
        result, built = run_case(make_case(
            "s7-both-forms", files,
            features=("single-page-metrics-record",
                      "split-metrics-record",
                      "decision-table-inside-root",
                      "decision-items-full-timestamps")))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(row_codes(result.stdout), STARTER_ORDER)
        block = row_line(result.stdout, "D-1")
        self.assertEqual(row_verdict(block), "present",
                         "D-1 verdict is not the single page form's "
                         "verdict in block: %s" % block[:400])
        self.assertRegex(block, r"median[^\d]*4(?!\d)(?!\.\d)")
        self.assertNotIn("4242", block)

    # Brief family F-16 done condition, CA2-12 pair, F-25 CA2-04
    # corrected form, and the F-21 report search form.

    def test_f16_done_condition_all_17_rows_on_miniature_copy(self):
        """Brief family F-16 done condition; plan Section 15 duty 3.

        One case runs the product over the f16 miniature copy and
        asserts all 17 rows against the established split: present
        E-1, E-2, Q-4; present but not derivable T-4, T-7, E-4, F-2,
        Q-1, Q-3, D-1, B-2; missing T-1, T-2, E-3, B-1, B-3, B-4.
        Any one row differing fails the test; no partial pass stands.
        """
        expected = {
            "E-1": "present", "E-2": "present", "Q-4": "present",
            "T-4": "present but not derivable",
            "T-7": "present but not derivable",
            "E-4": "present but not derivable",
            "F-2": "present but not derivable",
            "Q-1": "present but not derivable",
            "Q-3": "present but not derivable",
            "D-1": "present but not derivable",
            "B-2": "present but not derivable",
            "T-1": "missing", "T-2": "missing", "E-3": "missing",
            "B-1": "missing", "B-3": "missing", "B-4": "missing",
        }
        self.assertEqual(sorted(expected), sorted(STARTER_ORDER))
        result, built = run_case(f16_miniature_case())
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(row_codes(result.stdout), STARTER_ORDER)
        for code in STARTER_ORDER:
            self.assertEqual(
                row_verdict(row_line(result.stdout, code)),
                expected[code],
                "row %s differs from the established F-16 split on "
                "the miniature copy" % code)

    def _ca2_12_files(self, dressed):
        """Return one tree of the CA2-12 pair, sound or dressed.

        The two trees share every feeder for the unseparable rows
        byte for byte. The dressed tree differs only in the feeders
        for the separable rows: a staffed count its roster does not
        recount, an unreconciled spin figure, a trace whose parts do
        not sum to its stated total, a governing queue figure the
        decision derivation must recompute from, token figures
        offered only in estimator form outside the ledger feeders,
        and per step figures for B-1, B-3 and B-4 stated in the
        metrics record in the settled cross check form, which do
        not recompute from the feeder figures the two trees share.
        """
        files = base_files()
        # Corrected at Step 15 round 1, item R15-01: the gate
        # records of both trees now state a first ruling
        # outcome, so the F-2 present verdict on the pair rests
        # on that outcome and not on closing states alone. The
        # same text stands in both trees, so the unseparable
        # feeder sharing this docstring states stands unchanged.
        for n in (1, 2, 3):
            files["steps/step-%02d-gate-record.md" % n] = gate_record(
                n, "CLOSED-PASS",
                extra="First ruling outcome: Go, closes the step, "
                      "no send back before closure.")
        transitions = []
        for n in (1, 2, 3):
            extra = ""
            if n == 1:
                extra = ("Loop step. Board ruling held inside this "
                         "record: the board closes Round 1 of this "
                         "step. Work record for Round 1 stands in "
                         "audit/step-01-work.md.")
            if dressed and n == 1:
                files["steps/step-%02d-record.md" % n] = step_record(
                    n, team=9, additions=1, extra=extra)
            elif dressed and n == 3:
                files["steps/step-%02d-record.md" % n] = step_record(
                    n, total_spins=12, additions=1,
                    extra="Total spins for Step 3: 12.")
            else:
                files["steps/step-%02d-record.md" % n] = step_record(
                    n, additions=1, extra=extra)
            files["steps/step-%02d-roster.md" % n] = (
                "# Step %d roster\n\nNamed agents: 3. Base: 2.\n"
                "Roster additions over base: 1.\n" % n)
            transitions.append(
                "Step %d IN PROGRESS 2026-11-01 09:00, closed "
                "2026-11-01 17:00." % n)
        transitions.append("Step 1 BANKED duration 2 hours on Q-1.")
        files["PATH-LEDGER.md"] = path_ledger(
            "\n".join(transitions), "1, 2, 3")
        body = "Step table stands complete for the fixture steps."
        if dressed:
            body = ("Step table stands complete for the fixture "
                    "steps. Total spins through Step 3: 999, stated "
                    "with no correction. Metrics record states B-1 "
                    "for Step 1 as 99 hours. Metrics record states "
                    "B-3 for Step 1 as 99 hours. Metrics record "
                    "states B-4 for Step 1 as 99 hours.")
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(body=body,
                           decision_table=decision_table([RULED_ITEM])))
        files["audit/step-01-work.md"] = (
            "# Round 1 work record\n\nThe work Round 1 disposed "
            "of stands stated here.\n")
        files["audit/step-01-round-record.md"] = (
            "# Round record, step 1\n\nPost triage severity "
            "breakdown, flow scale: Critical 0, High 1, Medium 2, "
            "Low 3.\n")
        if dressed:
            files["steps/step-01-trace.md"] = (
                "# First trace, step 1\n\nParts: 2 LANDED, "
                "1 PARTIAL, 0 CONTRADICTED. Stated total: 2 items "
                "checked.\n")
        else:
            files["steps/step-01-trace.md"] = (
                "# First trace, step 1\n\nParts: 4 LANDED, "
                "0 PARTIAL, 0 CONTRADICTED. Stated total: 4 items "
                "checked.\n")
        files["registers/fix-register.md"] = (
            "# Fix register\n\nEntry one. Origin step: 1.\n")
        files["registers/defect-register.md"] = (
            "# Defect register\n\nEscaped defects: 0. Measurement "
            "basis: every register entry was triaged in full on "
            "2026-11-02 and no entry escaped. Entry D-1: origin "
            "step Step 1, as judged at triage.\n")
        money = ("Step 1: money 10.\nStep 2: money 20.\n"
                 "Step 3: money 30.\nBudget: money 100.\n")
        if dressed:
            files["registers/cost-ledger.md"] = (
                "# Cost ledger\n\n" + money)
            files["notes/token-estimate.md"] = (
                "# Token estimate\n\nEstimated tokens for Step 1: "
                "1000. Estimated tokens for Step 2: 2000. "
                "Estimated tokens for Step 3: 3000. Token budget "
                "estimate: 10000.\n")
            files["DECISION-QUEUE.md"] = queue_file([
                "| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
                "2026-11-02 13:00 |"])
        else:
            files["registers/cost-ledger.md"] = (
                "# Cost ledger\n\nStep 1: money 10, tokens 1000.\n"
                "Step 2: money 20, tokens 2000.\n"
                "Step 3: money 30, tokens 3000.\n"
                "Budget: money 100, tokens 10000.\n")
        return files

    def test_ca2_12_adversarial_pair_all_17_rows_against_marks(self):
        """CA2-12 adversarial pair; plan Section 15 duty 3 supplement.

        A dressed tree and a sound tree stand built through the
        fixture builder's pair support, build_cases. All 17 rows
        stand compared between the two trees against the expectation
        marks hand copied here from the golden authoring record's
        CA2-12 marks: separable 10 (E-1, E-2, Q-4, T-4, D-1, E-3,
        B-1, B-2, B-3, B-4), unseparable 7 (T-1, T-2, T-7, E-4, F-2,
        Q-1, Q-3). On an unseparable row the tool reports the two
        trees identically and the row stands present in both trees,
        the named limit of the gaming defences. The falsifier stands
        as the failure form: if the tool reports the two trees
        identically on a separable row, this test fails.
        """
        separable = ("E-1", "E-2", "Q-4", "T-4", "D-1", "E-3",
                     "B-1", "B-2", "B-3", "B-4")
        unseparable = ("T-1", "T-2", "T-7", "E-4", "F-2", "Q-1",
                       "Q-3")
        self.assertEqual(len(separable), 10)
        self.assertEqual(len(unseparable), 7)
        self.assertEqual(sorted(separable + unseparable),
                         sorted(STARTER_ORDER))
        root = tracked_tempdir("msc_slice7_")
        built = build_cases([
            make_case("s7-ca2-12-sound", self._ca2_12_files(False),
                      features=("single-page-metrics-record",
                                "decision-table-inside-root",
                                "cost-ledger-inside-root",
                                "full-clock-timestamps",
                                "decision-items-full-timestamps",
                                "banked-entries-with-duration",
                                "origin-step-on-register-entries")),
            make_case("s7-ca2-12-dressed", self._ca2_12_files(True),
                      features=("single-page-metrics-record",
                                "decision-table-inside-root",
                                "queue-file-inside-root",
                                "queue-governs-over-table",
                                "cost-ledger-inside-root",
                                "full-clock-timestamps",
                                "decision-items-full-timestamps",
                                "banked-entries-with-duration",
                                "origin-step-on-register-entries",
                                "unreconciled-figure",
                                "parts-fail-sum"))], root)
        sound = run_tool(built["s7-ca2-12-sound"])
        dressed = run_tool(built["s7-ca2-12-dressed"])
        self.assertEqual(sound.returncode, 0, sound.stderr[:300])
        self.assertEqual(dressed.returncode, 0, dressed.stderr[:300])
        self.assertEqual(row_codes(sound.stdout), STARTER_ORDER)
        self.assertEqual(row_codes(dressed.stdout), STARTER_ORDER)
        for code in STARTER_ORDER:
            sound_line = row_line(sound.stdout, code)
            dressed_line = row_line(dressed.stdout, code)
            if code in unseparable:
                self.assertEqual(
                    row_verdict(sound_line), "present",
                    "unseparable row %s is not present on the sound "
                    "tree" % code)
                self.assertEqual(
                    row_verdict(dressed_line), "present",
                    "unseparable row %s is not present on the "
                    "dressed tree" % code)
                self.assertEqual(
                    dressed_line, sound_line,
                    "unseparable row %s differs between the dressed "
                    "tree and the sound tree" % code)
            elif code == "T-4":
                self.assertEqual(
                    dressed_line, sound_line,
                    "separable row T-4 row lines stand equal between "
                    "the dressed tree and the sound tree")
                self.assertIn(
                    "degraded form: the row is shown without its "
                    "queue cross check",
                    row_block(sound.stdout, code).lower(),
                    "separable row T-4 sound row block carries no "
                    "degraded form statement line")
                self.assertNotIn(
                    "degraded form",
                    row_block(dressed.stdout, code).lower(),
                    "separable row T-4 dressed row block carries "
                    "the degraded form words")
                self.assertNotEqual(
                    row_block(dressed.stdout, code),
                    row_block(sound.stdout, code),
                    "CA2-12 falsifier: row T-4 stands marked "
                    "separable in the expectation marks, and the "
                    "tool reports the two trees identically on it "
                    "in row block form")
            elif code == "B-1":
                self.assertEqual(
                    dressed_line, sound_line,
                    "separable row B-1 row lines stand equal between "
                    "the dressed tree and the sound tree")
                self.assertNotIn(
                    "record disagrees",
                    statement_segment(row_block(sound.stdout, code)),
                    "separable row B-1 sound row block statement "
                    "segment carries the record disagrees words")
                self.assertIn(
                    "record disagrees",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-1 dressed row block statement "
                    "segment carries no record disagrees qualifier")
                self.assertIn(
                    "build-metrics-record.md",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-1 dressed row block statement "
                    "segment does not name build-metrics-record.md")
                self.assertIn(
                    "99 hours",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-1 dressed row block statement "
                    "segment does not carry the words 99 hours")
                self.assertIn(
                    "8 hours",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-1 dressed row block statement "
                    "segment does not carry the Step 1 feeder "
                    "elapsed figure of 8 hours")
                self.assertIn(
                    "feeder figure stands",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-1 dressed row block statement "
                    "segment does not carry the words feeder figure "
                    "stands")
                self.assertNotEqual(
                    row_block(dressed.stdout, code),
                    row_block(sound.stdout, code),
                    "CA2-12 falsifier: row B-1 stands marked "
                    "separable in the expectation marks, and the "
                    "tool reports the two trees identically on it "
                    "in row block form")
            elif code == "B-3":
                self.assertEqual(
                    dressed_line, sound_line,
                    "separable row B-3 row lines stand equal between "
                    "the dressed tree and the sound tree")
                self.assertNotIn(
                    "record disagrees",
                    statement_segment(row_block(sound.stdout, code)),
                    "separable row B-3 sound row block statement "
                    "segment carries the record disagrees words")
                self.assertIn(
                    "record disagrees",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-3 dressed row block statement "
                    "segment carries no record disagrees qualifier")
                self.assertIn(
                    "build-metrics-record.md",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-3 dressed row block statement "
                    "segment does not name build-metrics-record.md")
                self.assertIn(
                    "99 hours",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-3 dressed row block statement "
                    "segment does not carry the words 99 hours")
                self.assertIn(
                    "8 hours",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-3 dressed row block statement "
                    "segment does not carry the Step 1 feeder "
                    "elapsed figure of 8 hours")
                self.assertIn(
                    "feeder figure stands",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-3 dressed row block statement "
                    "segment does not carry the words feeder figure "
                    "stands")
                self.assertNotEqual(
                    row_block(dressed.stdout, code),
                    row_block(sound.stdout, code),
                    "CA2-12 falsifier: row B-3 stands marked "
                    "separable in the expectation marks, and the "
                    "tool reports the two trees identically on it "
                    "in row block form")
            elif code == "B-4":
                self.assertEqual(
                    dressed_line, sound_line,
                    "separable row B-4 row lines stand equal between "
                    "the dressed tree and the sound tree")
                self.assertNotIn(
                    "record disagrees",
                    statement_segment(row_block(sound.stdout, code)),
                    "separable row B-4 sound row block statement "
                    "segment carries the record disagrees words")
                self.assertIn(
                    "record disagrees",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-4 dressed row block statement "
                    "segment carries no record disagrees qualifier")
                self.assertIn(
                    "build-metrics-record.md",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-4 dressed row block statement "
                    "segment does not name build-metrics-record.md")
                self.assertIn(
                    "99 hours",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-4 dressed row block statement "
                    "segment does not carry the words 99 hours")
                self.assertIn(
                    "8 hours",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-4 dressed row block statement "
                    "segment does not carry the Step 1 feeder "
                    "active figure of 8 hours")
                self.assertIn(
                    "feeder figure stands",
                    statement_segment(row_block(dressed.stdout, code)),
                    "separable row B-4 dressed row block statement "
                    "segment does not carry the words feeder figure "
                    "stands")
                self.assertNotEqual(
                    row_block(dressed.stdout, code),
                    row_block(sound.stdout, code),
                    "CA2-12 falsifier: row B-4 stands marked "
                    "separable in the expectation marks, and the "
                    "tool reports the two trees identically on it "
                    "in row block form")
            else:
                self.assertNotEqual(
                    dressed_line, sound_line,
                    "CA2-12 falsifier: row %s stands marked "
                    "separable in the expectation marks, and the "
                    "tool reports the two trees identically on it"
                    % code)

    def test_f25_ca2_04_corrected_form_counts_on_miniature_copy(self):
        """F-25 CA2-04 corrected form; plan Section 15 duty 2, line 600.

        A run over the f16 miniature copy: the data quality section
        lists missing field count 5, for T-4, D-1, E-4, B-2 and Q-3,
        and wrong form count 3, for T-7, F-2 and Q-1. Any differing
        kind count fails the test.
        """
        missing_field = ("T-4", "D-1", "E-4", "B-2", "Q-3")
        wrong_form = ("T-7", "F-2", "Q-1")
        result, built = run_case(f16_miniature_case())
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        section = section_text(result.stdout, "Data quality")
        self.assertTrue(section, "no data quality section stands")
        self.assertRegex(section, r"(?m)^missing field: 5$")
        self.assertRegex(section, r"(?m)^wrong form: 3$")
        for code in missing_field:
            line = row_line(result.stdout, code)
            self.assertIn("missing field", line,
                          "row %s does not carry the missing field "
                          "kind its count stands on" % code)
        for code in wrong_form:
            line = row_line(result.stdout, code)
            self.assertIn("wrong form", line,
                          "row %s does not carry the wrong form "
                          "kind its count stands on" % code)

    def test_f21_report_search_no_estimated_figure_no_estimated_mark(self):
        """F-21 report search form; plan Section 15 duty 2, line 604.

        The tree holds the F-21 offers: a labelled proxy figure and
        a figure in estimator form offered outside the ledger
        feeders. The whole report stands searched for an estimated
        figure in any form and for the ESTIMATED mark beside a
        verdict, and the search finds neither; any find fails.
        """
        files = base_files()
        files["steps/step-01-record.md"] = step_record(
            1, extra="Agent count ceiling of 10 documented units "
                     "on a labelled proxy basis: 4242 documented "
                     "units. Tokens estimated for Step 1: 7777, in "
                     "estimator form.")
        files["notes/money-estimate.md"] = (
            "# Money estimate\n\nEstimated money for Step 1: 8888, "
            "offered in estimator form outside the ledger "
            "feeders.\n")
        result, built = run_case(make_case(
            "s7-f21-search", files, features=("proxy-label",)))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(row_codes(result.stdout), STARTER_ORDER)
        report = result.stdout
        self.assertNotIn("estimated", report.lower(),
                         "an estimated figure in some form stands "
                         "in the report")
        for figure in ("7777", "8888"):
            self.assertNotIn(figure, report,
                             "the estimator figure %s offered "
                             "outside the ledger feeders stands in "
                             "the report" % figure)
        for line in row_lines(report):
            parts, order = parts_of(line)
            self.assertNotIn("ESTIMATED", line,
                             "the ESTIMATED mark stands beside a "
                             "verdict on the row: %s" % line[:200])
            self.assertNotIn("estimated",
                             parts.get("Verdict", "").lower())

    # The plain text line grammar, spin 775, line by line in order.

    def test_grammar_no_blank_lines_single_trailing_lf_utf8(self):
        """Line grammar. No blank lines; last line ends with one LF."""
        result, built = run_case(make_case("s7-grammar-form",
                                           base_files()))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        text = result.stdout
        self.assertNotIn("\n\n", text)
        self.assertNotIn("\r", text)
        self.assertTrue(text.endswith("\n"))
        self.assertFalse(text.endswith("\n\n"))
        for line in text.splitlines():
            self.assertTrue(line.strip(), "a blank line stands")

    def test_grammar_first_two_lines_root_then_build_identity(self):
        """Line grammar. Root identity first, build identity second."""
        result, built = run_case(make_case("s7-grammar-head",
                                           base_files()))
        lines = result.stdout.splitlines()
        self.assertTrue(lines[0].startswith("Root: "))
        self.assertIn(str(built), lines[0])
        self.assertTrue(lines[1].startswith("Build identity: "))
        self.assertIn("metrics fixture build", lines[1])

    def test_grammar_coverage_lines_before_rows_in_order(self):
        """Line grammar; EC-41, EC-42. Coverage lines stand in order."""
        result, built = run_case(make_case("s7-grammar-coverage",
                                           base_files()))
        lines = result.stdout.splitlines()
        taken = [i for i, ln in enumerate(lines)
                 if ln.startswith("Coverage taken set: ")]
        smaller = [i for i, ln in enumerate(lines)
                   if ln.startswith("Coverage smaller set: ")]
        uncovered = [i for i, ln in enumerate(lines)
                     if ln.startswith("Coverage uncovered steps: ")]
        first_row = lines.index(row_lines(result.stdout)[0])
        self.assertEqual(len(taken), 1)
        self.assertEqual(len(uncovered), 1)
        self.assertLess(taken[0], first_row)
        self.assertLess(uncovered[0], first_row)
        for idx in smaller:
            self.assertLess(taken[0], idx)
            self.assertLess(idx, uncovered[0])

    def test_grammar_reading_moment_line_form_and_place(self):
        """Line grammar. The reading moment line stands in its form."""
        result, built = run_case(make_case("s7-grammar-moment",
                                           base_files()))
        lines = result.stdout.splitlines()
        moment = [ln for ln in lines if ln.startswith("Record state")]
        self.assertEqual(len(moment), 1)
        line = moment[0]
        self.assertIn("whole build report", line)
        uncovered = [i for i, ln in enumerate(lines)
                     if ln.startswith("Coverage uncovered steps: ")][0]
        first_row = lines.index(row_lines(result.stdout)[0])
        self.assertLess(uncovered, lines.index(line))
        self.assertLess(lines.index(line), first_row)

    def test_grammar_coverage_piece_line_for_piece_not_read_in_full(self):
        """Line grammar; EC-42. One coverage piece line per such piece."""
        files = base_files()
        case = make_case("s7-grammar-piece", files, malformations=({
            "switch": "M-01", "target": "steps/step-01-record.md",
            "target_kind": "SR", "state": "not-valid-text"},))
        result, built = run_case(case)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        lines = result.stdout.splitlines()
        piece = [ln for ln in lines
                 if ln.startswith("Coverage piece not read in full: ")]
        self.assertTrue(piece, "no coverage piece line stands")
        self.assertIn("step-01-record", piece[0])
        first_row = lines.index(row_lines(result.stdout)[0])
        self.assertLess(lines.index(piece[0]), first_row)

    def test_grammar_version2_trigger_line_exact_words(self):
        """Line grammar. The trigger line stands whole, in exact words."""
        files = base_files()
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(
                body="Step table covers Steps 1 to 3, every step "
                     "to close."))
        result, built = run_case(make_case("s7-grammar-trigger", files))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        exact = ("Version 2 trigger state found: the metrics record "
                 "covers every step to close.")
        lines = result.stdout.splitlines()
        self.assertIn(exact, lines)
        first_row = lines.index(row_lines(result.stdout)[0])
        self.assertLess(lines.index(exact), first_row)

    def test_grammar_present_row_part_order_pointer_last(self):
        """Line grammar. Present row parts stand in the stated order."""
        result, built = run_case(make_case("s7-grammar-present",
                                           base_files()))
        line = row_line(result.stdout, "E-1")
        self.assertEqual(row_verdict(line), "present")
        parts, order = parts_of(line)
        self.assertNotIn("Reason", parts)
        self.assertLess(order.index("Verdict"), order.index("Value"))
        self.assertLess(order.index("Value"),
                        order.index("Row coverage"))
        self.assertLess(order.index("Row coverage"),
                        order.index("Reconciled against"))
        self.assertLess(order.index("Reconciled against"),
                        order.index("Pointer"))
        self.assertEqual(order[-1], "Pointer")
        self.assertTrue(line.startswith("E-1 " + ROW_NAMES["E-1"]))

    def test_grammar_reason_line_anatomy_three_named_parts(self):
        """Line grammar. Reason holds broken link, required, held."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-01.\n"
            "Step 2 IN PROGRESS 2026-11-01, closed 2026-11-01.\n"
            "Step 3 IN PROGRESS 2026-11-01, closed 2026-11-01.",
            "1, 2, 3")
        result, built = run_case(make_case(
            "s7-grammar-reason", files,
            features=("date-only-timestamps",)))
        line = row_line(result.stdout, "T-1")
        parts, order = parts_of(line)
        self.assertIn("Reason", parts)
        self.assertNotIn("Reconciled against", parts)
        self.assertNotIn("Value", parts)
        reason = parts["Reason"]
        self.assertLess(reason.index("broken link,"),
                        reason.index("form required,"))
        self.assertLess(reason.index("form required,"),
                        reason.index("form held,"))
        self.assertEqual(reason.count("; "), 2)
        self.assertEqual(order[-1], "Pointer")
        self.assertLess(order.index("Reason"), order.index("Pointer"))

    def test_grammar_bound_part_three_subparts_in_order(self):
        """Line grammar. Bound holds excepted, link excepted, cleared by."""
        result, built = run_case(f16_miniature_case())
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        line = row_line(result.stdout, "Q-4")
        parts, order = parts_of(line)
        self.assertIn("Bound", parts)
        bound = parts["Bound"]
        self.assertLess(bound.index("excepted,"),
                        bound.index("link excepted,"))
        self.assertLess(bound.index("link excepted,"),
                        bound.index("cleared by,"))
        self.assertIn("Step 13", bound)
        self.assertEqual(order[-1], "Pointer")

    def test_grammar_d1_statement_part_before_reason_pointer_last(self):
        """Line grammar; spin 794. D-1 Statement before Reason, full form."""
        result, built = run_case(f16_miniature_case())
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        line = row_line(result.stdout, "D-1")
        parts, order = parts_of(line)
        self.assertIn("Statement", parts)
        self.assertIn("decision table", parts["Statement"].lower())
        self.assertLess(order.index("Statement"),
                        order.index("Reason"))
        self.assertEqual(order[-1], "Pointer")
        for code in STARTER_ORDER:
            if code != "D-1":
                other, other_order = parts_of(
                    row_line(result.stdout, code))
                self.assertNotIn("Statement", other,
                                 "Statement part stands on " + code)

    def test_grammar_d1_statement_part_after_reconciliation_present(self):
        """Line grammar; spin 794. On a present D-1 row, after Reconciled."""
        files = base_files()
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(decision_table=decision_table([RULED_ITEM])))
        result, built = run_case(make_case(
            "s7-grammar-d1-present", files,
            features=("decision-items-full-timestamps",
                      "decision-table-inside-root")))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        line = row_line(result.stdout, "D-1")
        self.assertEqual(row_verdict(line), "present")
        parts, order = parts_of(line)
        self.assertIn("Statement", parts)
        self.assertNotIn("Reason", parts)
        self.assertLess(order.index("Reconciled against"),
                        order.index("Statement"))
        self.assertLess(order.index("Statement"),
                        order.index("Pointer"))
        self.assertEqual(order[-1], "Pointer")

    def test_grammar_no_score_grade_digest_or_estimated_figure(self):
        """Line grammar; EC-49. Closed report content stands absent."""
        result, built = run_case(make_case("s7-grammar-closed",
                                           base_files()))
        lowered = result.stdout.lower()
        for word in ("score:", "grade:", "digest", "estimated"):
            self.assertNotIn(word, lowered)
        q3 = row_line(result.stdout, "Q-3")
        self.assertNotIn("Value: 0", q3)

    def test_grammar_data_quality_five_lines_in_order_no_total(self):
        """Line grammar; EC-44. Five kind lines, in order, no total line."""
        result, built = run_case(make_case("s7-grammar-dq", base_files()))
        section = section_text(result.stdout, "Data quality")
        self.assertTrue(section, "no data quality section stands")
        positions = []
        for kind in DQ_KINDS:
            match = re.search(r"(?m)^%s: \d+$" % re.escape(kind),
                              section)
            self.assertIsNotNone(match, "no count line for " + kind)
            positions.append(match.start())
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("total", section.lower())

    def test_grammar_record_cost_budget_line_and_proxy_line(self):
        """Line grammar; EC-45. Budget line and proxy line forms."""
        result, built = run_case(f16_miniature_case())
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        section = section_text(result.stdout, "Record cost")
        self.assertTrue(section, "no record cost section stands")
        budget = [ln for ln in section.splitlines()
                  if ln.startswith("Budget position: ")]
        self.assertEqual(len(budget), 1)
        if re.search(r"\d", budget[0]):
            self.assertNotIn("cap", budget[0].lower())
        restated = [ln for ln in section.splitlines()
                    if "documented units" in ln]
        for line in restated:
            self.assertIn("proxy", line.lower())

    def test_record_cost_heading_word_is_not_a_budget_position(self):
        """R15-13; D4R-27. A gate heading word is no budget position."""
        files = base_files()
        files["steps/step-01-gate-record.md"] = gate_record(
            1, extra="### 5. Budget position: LANDED\n\n"
                     "Money: \"0 external spend for the whole "
                     "build.\" Agent count: whole build ceiling "
                     "260 spins.\n")
        result, built = run_case(make_case(
            "s7-record-cost-heading", files))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        section = section_text(result.stdout, "Record cost")
        self.assertTrue(section, "no record cost section stands")
        budget = [ln for ln in section.splitlines()
                  if ln.startswith("Budget position: ")]
        self.assertEqual(len(budget), 1)
        self.assertEqual(
            budget[0],
            "Budget position: absent, no budget position stands "
            "recorded in the tree")
        self.assertNotIn("LANDED", section)
        self.assertNotIn('"0 external spend', section)
        for line in section.splitlines():
            self.assertFalse(line.startswith("Money:"),
                             "a garbled money line stands: " + line)

    def test_record_cost_proxy_final_position_governs(self):
        """R15-13; D4R-27. Successive proxy shares, final governs."""
        files = base_files()
        files["steps/step-01-record.md"] = step_record(
            1, extra="Position at this step close: 244 of 260 "
                     "documented units on a labelled proxy basis.")
        files["steps/step-02-record.md"] = step_record(
            2, extra="Position at this step close: 245 of 260 "
                     "documented units on a labelled proxy basis.")
        files["steps/step-03-gate-ruling.md"] = gate_ruling(
            3, extra="Final figure for the build: 248 of 260 "
                     "documented units used. The ceiling held on "
                     "the labelled proxy basis: the figure is a "
                     "documented unit count used as a proxy for "
                     "spend.")
        result, built = run_case(make_case(
            "s7-record-cost-proxy-final", files,
            features=("proxy-label",)))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        section = section_text(result.stdout, "Record cost")
        self.assertTrue(section, "no record cost section stands")
        proxy = [ln for ln in section.splitlines()
                 if ln.startswith("Proxy figure: ")]
        self.assertEqual(len(proxy), 1, section)
        self.assertIn("248 of 260 documented units", proxy[0])
        self.assertIn("proxy", proxy[0].lower())
        self.assertIn("step-03-gate-ruling.md", proxy[0])
        self.assertNotIn("244 of 260", section)
        self.assertNotIn("245 of 260", section)
        b2 = row_line(result.stdout, "B-2")
        self.assertIn("248 of 260", b2)
        block = disagreements_block(result.stdout)
        entries = block_entries(result.stdout)
        proxy_entries = [e for e in entries if "proxy" in e.lower()]
        self.assertEqual(len(proxy_entries), 1, block)
        entry_parts, entry_order = parts_of(proxy_entries[0])
        self.assertEqual(entry_parts["Metric"], "B-2")
        self.assertEqual(entry_parts["Governing position"],
                         "governed with the pattern named")
        for figure in ("244 of 260", "245 of 260", "248 of 260"):
            self.assertIn(figure, entry_parts["Figures"])
        first_lines = [ln for ln in block.splitlines()
                       if ln.startswith("Blocked metric: ")]
        self.assertTrue(any(
            "B-2" in ln and "no verdict was withheld" in ln.lower()
            for ln in first_lines), block)

    def test_record_cost_budget_position_statement_line_carried(self):
        """R15-13; D4R-27. A stated budget position stands carried."""
        files = base_files()
        files["steps/step-01-record.md"] = step_record(
            1, extra="Budget position: money 0 external spend for "
                     "the whole build; tokens NOT RECORDED.")
        result, built = run_case(make_case(
            "s7-record-cost-budget-stated", files))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        section = section_text(result.stdout, "Record cost")
        budget = [ln for ln in section.splitlines()
                  if ln.startswith("Budget position: ")]
        self.assertEqual(len(budget), 1)
        self.assertIn("money 0 external spend for the whole build",
                      budget[0])
        self.assertIn("step-01-record.md", budget[0])
        self.assertNotIn("cap", budget[0].lower())

    def test_grammar_run_cost_line_parts_in_order(self):
        """Line grammar; EC-47. Run cost parts stand in stated order."""
        result, built = run_case(make_case("s7-grammar-runcost",
                                           base_files()))
        lines = [ln for ln in result.stdout.splitlines()
                 if ln.startswith("Run cost: ")]
        self.assertEqual(len(lines), 1)
        line = lines[0]
        labels = ("Files visited", "Files opened", "Bytes read",
                  "Entries visited", "Limit", "Reading")
        positions = [line.index(label + ":") for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Reading: full", line)

    def test_grammar_partial_reading_stated_in_both_places(self):
        """Line grammar; EC-42, EC-47. Partial stands in both places."""
        files = base_files()
        case = make_case("s7-grammar-partial", files, malformations=({
            "switch": "M-01", "target": "steps/step-02-record.md",
            "target_kind": "SR", "state": "not-valid-text"},))
        result, built = run_case(case)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertIn("Coverage partial: partial report", result.stdout)
        run_cost = [ln for ln in result.stdout.splitlines()
                    if ln.startswith("Run cost: ")][0]
        self.assertIn("Reading: partial", run_cost)

    def test_grammar_terms_section_last_explains_reason_terms(self):
        """Line grammar. Terms stands last, one line per term used."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-01.\n"
            "Step 2 IN PROGRESS 2026-11-01, closed 2026-11-01.\n"
            "Step 3 IN PROGRESS 2026-11-01, closed 2026-11-01.",
            "1, 2, 3")
        result, built = run_case(make_case(
            "s7-grammar-terms", files,
            features=("date-only-timestamps",)))
        lines = result.stdout.splitlines()
        self.assertIn("Terms", lines)
        terms_at = lines.index("Terms")
        run_cost_at = [i for i, ln in enumerate(lines)
                       if ln.startswith("Run cost: ")][0]
        self.assertLess(run_cost_at, terms_at)
        for line in lines[terms_at + 1:]:
            self.assertIn(": ", line)
            self.assertFalse(line.startswith("Verdict"))

    def test_grammar_sections_stand_in_report_order(self):
        """Line grammar; EC-43, EC-44, EC-45. Sections follow the rows."""
        result, built = run_case(make_case("s7-grammar-order",
                                           base_files()))
        lines = result.stdout.splitlines()
        last_row = lines.index(row_lines(result.stdout)[-1])
        order = [lines.index(head) for head in
                 ("Disagreements", "Data quality", "Record cost",
                  "Terms")]
        self.assertLess(last_row, order[0])
        self.assertEqual(order, sorted(order))
        run_cost = [i for i, ln in enumerate(lines)
                    if ln.startswith("Run cost: ")][0]
        self.assertLess(order[2], run_cost)
        self.assertLess(run_cost, order[3])


    # The command grammar of plan Section 9.

    def test_cmd_completed_report_to_stdout_exits_0(self):
        """Command grammar. A completed report to stdout exits 0."""
        result, built = run_case(make_case("s7-cmd-stdout",
                                           base_files()))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(row_codes(result.stdout), STARTER_ORDER)

    def test_cmd_report_two_word_form_writes_named_file(self):
        """Command grammar. The two word report form writes its file."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-cmd-file", base_files()), root)
        dest = root / "report-out.txt"
        result = run_argv([built, "--report", dest])
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertTrue(dest.is_file())
        text = dest.read_text(encoding="utf-8")
        self.assertEqual(row_codes(text), STARTER_ORDER)
        self.assertTrue(text.endswith("\n"))
        self.assertNotIn("\r", text)

    def test_cmd_no_argument_is_usage_error_exit_2(self):
        """Command grammar. No argument is a usage error, exit 2."""
        assert_usage_error(self, run_argv([]))

    def test_cmd_extra_argument_is_usage_error_exit_2(self):
        """Command grammar. An extra argument is a usage error, exit 2."""
        result, built = run_case(make_case("s7-cmd-base", base_files()))
        assert_usage_error(self, run_argv([built, "extra"]))

    def test_cmd_unknown_option_is_usage_error_exit_2(self):
        """Command grammar. An unknown option is a usage error, exit 2."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-cmd-unknown", base_files()),
                           root)
        assert_usage_error(self, run_argv([built, "--frobnicate"]))

    def test_cmd_report_equals_form_is_usage_error_exit_2(self):
        """Command grammar. No equals form stands for the report argument."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-cmd-equals", base_files()),
                           root)
        dest = root / "report-out.txt"
        assert_usage_error(self, run_argv(
            [built, "--report=%s" % dest]))
        self.assertFalse(dest.exists())

    def test_cmd_report_short_form_is_usage_error_exit_2(self):
        """Command grammar. No short form stands for the report argument."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-cmd-short", base_files()), root)
        dest = root / "report-out.txt"
        assert_usage_error(self, run_argv([built, "-r", dest]))
        self.assertFalse(dest.exists())

    def test_cmd_report_missing_path_is_usage_error_exit_2(self):
        """Command grammar. A report argument with no path exits 2."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-cmd-nopath", base_files()),
                           root)
        assert_usage_error(self, run_argv([built, "--report"]))

    def test_cmd_repeated_report_is_usage_error_exit_2(self):
        """Command grammar. A repeated report argument exits 2."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-cmd-repeat", base_files()),
                           root)
        first = root / "one.txt"
        second = root / "two.txt"
        assert_usage_error(self, run_argv(
            [built, "--report", first, "--report", second]))
        self.assertFalse(first.exists())
        self.assertFalse(second.exists())

    def test_cmd_help_form_barred_in_version_1(self):
        """Command grammar. The help form is barred in version 1."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-cmd-help", base_files()), root)
        assert_usage_error(self, run_argv([built, "--help"]))
        assert_usage_error(self, run_argv(["--help"]))

    def test_cmd_version_form_barred_in_version_1(self):
        """Command grammar. The version form is barred in version 1."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-cmd-version", base_files()),
                           root)
        assert_usage_error(self, run_argv([built, "--version"]))
        assert_usage_error(self, run_argv(["--version"]))

    def test_cmd_step_count_argument_takes_usage_error_path(self):
        """Command grammar; F-24. No operator step count argument stands."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-cmd-count", base_files()), root)
        assert_usage_error(self, run_argv([built, "18"]))

    def test_cmd_unreadable_input_missing_root_exits_1(self):
        """Command grammar. Unreadable input exits 1, with no report."""
        root = tracked_tempdir("msc_slice7_")
        missing = root / "no-such-tree"
        result = run_argv([missing])
        self.assertEqual(result.returncode, 1,
                         "exit is not 1: %r" % (result.returncode,))
        self.assertNotIn("Verdict:", result.stdout)
        self.assertTrue(result.stderr.strip())

    def test_cmd_unreadable_input_root_is_a_file_exits_1(self):
        """Command grammar. A root that is a file is unreadable, exit 1."""
        root = tracked_tempdir("msc_slice7_")
        plain = root / "plain.txt"
        plain.write_text("Not a tree.\n", encoding="utf-8")
        result = run_argv([plain])
        self.assertEqual(result.returncode, 1,
                         "exit is not 1: %r" % (result.returncode,))
        self.assertNotIn("Verdict:", result.stdout)

    def test_version_rule_first_release_is_1_0_0_three_part(self):
        """Command grammar; plan Section 9, decision 2. Version 1.0.0."""
        text = (REPO_ROOT / "pyproject.toml").read_text(
            encoding="utf-8")
        match = re.search(r'(?m)^version = "([^"]+)"$', text)
        self.assertIsNotNone(match, "no version stands in pyproject")
        version = match.group(1)
        self.assertEqual(version, "1.0.0")
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")

    # The disagreements block: spin 774, spin 778, spin 782.

    def _disagreement_files(self, kind):
        """Return files holding one disagreement of the named kind."""
        files = base_files()
        if kind == "ungoverned":
            files["wiki/wiki/synthesis/build-metrics-record.md"] = (
                metrics_record(
                    body="Step table stands. Total spins through "
                         "Step 3: 999, stated with no correction."))
            files["steps/step-03-record.md"] = step_record(
                3, total_spins=12,
                extra="Total spins for Step 3: 12.")
        elif kind == "restatement":
            files["wiki/wiki/synthesis/build-metrics-record.md"] = (
                metrics_record(
                    body="Step table stands. Total spins through "
                         "Step 3: 999. Correction C-1 governs: the "
                         "step record figure of 12 stands."))
            files["steps/step-03-record.md"] = step_record(
                3, total_spins=12,
                extra="Total spins for Step 3: 12. Correction C-1 "
                      "names this figure as governing.")
        elif kind == "governed":
            files["wiki/wiki/synthesis/build-metrics-record.md"] = (
                metrics_record(
                    body="Step table stands. Closure state for "
                         "Step 1: CLOSED-PASS, under the gate "
                         "pattern named for gate records."))
            files["steps/step-01-record.md"] = step_record(
                1, closure_note="Closure state: CLOSED-PASS.")
        elif kind == "unclassifiable":
            files["wiki/wiki/synthesis/build-metrics-record.md"] = (
                metrics_record(
                    body="Step table stands. A figure stands in a "
                         "form no class in the record names."))
            files["steps/step-02-record.md"] = step_record(
                2, extra="A figure stands in an unnamed form.")
        return files

    def test_disagreements_ungoverned_entry_blocking_group_first_line(self):
        """EC-43. F-17 ungoverned variant: blocking group, first line."""
        result, built = run_case(make_case(
            "s7-dis-ungoverned", self._disagreement_files("ungoverned"),
            features=("unreconciled-figure",)))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        block = disagreements_block(result.stdout)
        self.assertTrue(block, "no disagreements block stands")
        entries = block_entries(result.stdout)
        self.assertTrue(entries, "no block entry stands")
        entry_parts, entry_order = parts_of(entries[0])
        self.assertEqual(entry_parts["Governing position"],
                         "ungoverned with no verdict depending on it")
        self.assertLess(block.index("Group: " + GROUP_BLOCKING),
                        block.index(entries[0]))
        first_lines = [ln for ln in block.splitlines()
                       if ln.startswith("Blocked metric: ")]
        self.assertTrue(first_lines,
                        "no blocking group first line stands")
        self.assertIn(entry_parts["Metric"], first_lines[0])

    def test_disagreements_restatement_entry_carries_no_first_line(self):
        """EC-43. A restatement group entry carries no first line."""
        result, built = run_case(make_case(
            "s7-dis-restatement",
            self._disagreement_files("restatement"),
            features=("named-governing-correction",)))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        block = disagreements_block(result.stdout)
        entries = block_entries(result.stdout)
        self.assertTrue(entries, "no block entry stands")
        entry_parts, entry_order = parts_of(entries[0])
        self.assertEqual(entry_parts["Governing position"],
                         "restatement with its correction named")
        self.assertLess(block.index("Group: " + GROUP_RESTATEMENTS),
                        block.index(entries[0]))
        segment = block[block.index("Group: " + GROUP_RESTATEMENTS):
                        block.index(entries[0])]
        self.assertNotIn("Blocked metric:", segment)

    def test_disagreements_governed_case_no_verdict_withheld(self):
        """EC-43. The pure governed case states no verdict was withheld."""
        result, built = run_case(make_case(
            "s7-dis-governed", self._disagreement_files("governed")))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        block = disagreements_block(result.stdout)
        entries = block_entries(result.stdout)
        self.assertTrue(entries, "no block entry stands")
        entry_parts, entry_order = parts_of(entries[0])
        self.assertEqual(entry_parts["Governing position"],
                         "governed with the pattern named")
        first_lines = [ln for ln in block.splitlines()
                       if ln.startswith("Blocked metric: ")]
        self.assertTrue(first_lines)
        self.assertIn("no verdict was withheld", first_lines[0].lower())

    def test_disagreements_unclassifiable_failure_form_never_omitted(self):
        """EC-43; spin 778. An unclassifiable disagreement is never omitted."""
        result, built = run_case(make_case(
            "s7-dis-unclassifiable",
            self._disagreement_files("unclassifiable")))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        block = disagreements_block(result.stdout)
        self.assertTrue(block, "no disagreements block stands")
        entries = block_entries(result.stdout)
        self.assertTrue(
            entries,
            "the unclassifiable disagreement was omitted from the "
            "block: Slice 7 is answerable in final form for this "
            "failure form")
        entry_parts, entry_order = parts_of(entries[0])
        self.assertEqual(entry_parts["Governing position"],
                         "ungoverned with no verdict depending on it")
        self.assertLess(block.index("Group: " + GROUP_BLOCKING),
                        block.index(entries[0]))
        first_lines = [ln for ln in block.splitlines()
                       if ln.startswith("Blocked metric: ")]
        self.assertTrue(first_lines)

    def test_disagreements_one_entry_per_metric_touched(self):
        """EC-43; spin 782. One entry per metric a disagreement touches."""
        files = base_files()
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(
                body="Step table stands. Total spins through Step 3: "
                     "999, stated with no correction, bearing on "
                     "E-2 and on B-2."))
        files["steps/step-03-record.md"] = step_record(
            3, total_spins=12, extra="Total spins for Step 3: 12.")
        result, built = run_case(make_case(
            "s7-dis-two-metrics", files,
            features=("unreconciled-figure",)))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        entries = block_entries(result.stdout)
        metrics_named = []
        for entry in entries:
            entry_parts, entry_order = parts_of(entry)
            metrics_named.append(entry_parts.get("Metric", ""))
        self.assertIn("E-2", metrics_named)
        self.assertIn("B-2", metrics_named)
        self.assertEqual(len(entries), len(set(entries)) or len(entries))
        e2 = [e for e in entries if "Metric: E-2" in e]
        b2 = [e for e in entries if "Metric: B-2" in e]
        self.assertEqual(len(e2), 1)
        self.assertEqual(len(b2), 1)
        first, first_order = parts_of(e2[0])
        second, second_order = parts_of(b2[0])
        self.assertEqual(first["Records"], second["Records"])
        self.assertEqual(first["Figures"], second["Figures"])

    def test_disagreements_entry_fields_in_order_wording_closed(self):
        """EC-43. Entry parts stand in order; wording is one of three."""
        result, built = run_case(make_case(
            "s7-dis-fields", self._disagreement_files("ungoverned"),
            features=("unreconciled-figure",)))
        entries = block_entries(result.stdout)
        self.assertTrue(entries, "no block entry stands")
        for entry in entries:
            entry_parts, entry_order = parts_of(entry)
            self.assertEqual(
                entry_order,
                ["Records", "Figures", "Metric", "Governing position"])
            self.assertIn(entry_parts["Governing position"],
                          GOVERNING_WORDINGS)

    def test_disagreements_row_and_block_two_places_together(self):
        """EC-43. A contradiction lives in its row reason and the block."""
        result, built = run_case(make_case(
            "s7-dis-two-places", self._disagreement_files("ungoverned"),
            features=("unreconciled-figure",)))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        entries = block_entries(result.stdout)
        self.assertTrue(entries, "no block entry stands")
        entry_parts, entry_order = parts_of(entries[0])
        row = row_line(result.stdout, entry_parts["Metric"])
        self.assertTrue(row, "no row stands for the blocked metric")
        self.assertIn("999", row)
        self.assertIn("999", entry_parts["Figures"])
        self.assertIn("12", entry_parts["Figures"])

    def test_disagreements_groups_stand_restatements_first(self):
        """Line grammar; EC-43. The block stands composed group first."""
        files = self._disagreement_files("restatement")
        files["steps/step-02-record.md"] = step_record(
            2, total_spins=9,
            extra="Total spins for Step 2: 9, against a metrics "
                  "record figure of 555 with no correction.")
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(
                body="Step table stands. Total spins through Step 3: "
                     "999. Correction C-1 governs: the step record "
                     "figure of 12 stands. Total spins for Step 2: "
                     "555, stated with no correction."))
        result, built = run_case(make_case(
            "s7-dis-groups", files,
            features=("named-governing-correction",
                      "unreconciled-figure")))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        block = disagreements_block(result.stdout)
        self.assertIn("Group: " + GROUP_RESTATEMENTS, block)
        self.assertIn("Group: " + GROUP_BLOCKING, block)
        self.assertLess(block.index("Group: " + GROUP_RESTATEMENTS),
                        block.index("Group: " + GROUP_BLOCKING))

    # Determinism: A8R-06 in slice form, and EC-48 at report level.

    def test_determinism_two_runs_byte_identical(self):
        """A8R-06. Two runs on one unchanged tree are byte identical."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-det-two", base_files()), root)
        first = run_tool(built)
        second = run_tool(built)
        self.assertEqual(first.returncode, 0, first.stderr[:300])
        self.assertEqual(second.returncode, 0, second.stderr[:300])
        self.assertEqual(first.stdout, second.stdout)

    def test_determinism_different_timezone_byte_identical(self):
        """A8R-06. A run under a different timezone is byte identical."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-det-tz", base_files()), root)
        first = run_tool(built, env_extra={"TZ": "UTC"})
        second = run_tool(built,
                          env_extra={"TZ": "Pacific/Kiritimati"})
        self.assertEqual(first.returncode, 0, first.stderr[:300])
        self.assertEqual(second.returncode, 0, second.stderr[:300])
        self.assertEqual(first.stdout, second.stdout)

    def test_determinism_c_locale_byte_identical(self):
        """A8R-06. A run under the C locale is byte identical."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-det-locale", base_files()),
                           root)
        first = run_tool(built, env_extra={"LC_ALL": "C.UTF-8"})
        second = run_tool(built, env_extra={"LC_ALL": "C"})
        self.assertEqual(first.returncode, 0, first.stderr[:300])
        self.assertEqual(second.returncode, 0, second.stderr[:300])
        self.assertEqual(first.stdout, second.stdout)

    def test_determinism_report_level_same_rows_every_run(self):
        """EC-48. The same unchanged tree gives the same rows every run."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(f16_miniature_case(), root)
        runs = [run_tool(built) for _ in range(3)]
        for result in runs:
            self.assertEqual(result.returncode, 0,
                             result.stderr[:300])
        baseline = [row_line(runs[0].stdout, code)
                    for code in STARTER_ORDER]
        for result in runs[1:]:
            self.assertEqual(
                [row_line(result.stdout, code) for code in STARTER_ORDER],
                baseline)

    # Read only proof surface and delivery failure forms.

    def test_read_only_manifest_unchanged_stdout_run(self):
        """EC-47. A stdout run leaves the tree byte for byte unchanged."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-ro-stdout", base_files()),
                           root)
        before = manifest(built)
        result = run_tool(built)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(manifest(built), before)

    def test_read_only_manifest_unchanged_named_file_outside_tree(self):
        """EC-47. A named file run outside the tree leaves it unchanged."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-ro-file", base_files()), root)
        before = manifest(built)
        dest = root / "outside-report.txt"
        result = run_argv([built, "--report", dest])
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(manifest(built), before)

    def test_inside_tree_destination_refused_relative_form(self):
        """D-17. A relative destination inside the tree exits 2."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-inside-rel", base_files()),
                           root)
        result = subprocess.run(
            [sys.executable, "-m", "metrics_starter_collector",
             ".", "--report", "report.txt"],
            capture_output=True, text=True, cwd=str(built),
            timeout=120)
        self.assertEqual(result.returncode, 2,
                         "exit is not 2: %r" % (result.returncode,))
        self.assertFalse((built / "report.txt").exists())

    def test_inside_tree_destination_refused_parent_segments(self):
        """D-17. A parent segment form resolving inside exits 2."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-inside-parent", base_files()),
                           root)
        sneaky = built / "steps" / ".." / "report.txt"
        result = run_argv([built, "--report", sneaky])
        self.assertEqual(result.returncode, 2,
                         "exit is not 2: %r" % (result.returncode,))
        self.assertFalse((built / "report.txt").exists())

    def test_inside_tree_destination_refused_through_link(self):
        """D-17. A destination through a link into the tree exits 2."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-inside-link", base_files()),
                           root)
        link = root / "into-tree"
        os.symlink(str(built), str(link))
        dest = link / "report.txt"
        result = run_argv([built, "--report", dest])
        self.assertEqual(result.returncode, 2,
                         "exit is not 2: %r" % (result.returncode,))
        self.assertFalse((built / "report.txt").exists())

    def test_inside_tree_destination_refused_root_itself(self):
        """D-17. The root itself given as the destination exits 2."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-inside-root", base_files()),
                           root)
        before = manifest(built)
        result = run_argv([built, "--report", built])
        self.assertEqual(result.returncode, 2,
                         "exit is not 2: %r" % (result.returncode,))
        self.assertEqual(manifest(built), before)

    def test_delivery_failure_parent_directory_does_not_stand(self):
        """Delivery failure. Missing parent: exit 2, nothing created."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-deliver-parent", base_files()),
                           root)
        dest = root / "no-such-dir" / "report.txt"
        result = run_argv([built, "--report", dest])
        self.assertEqual(result.returncode, 2,
                         "exit is not 2: %r" % (result.returncode,))
        self.assertFalse(dest.exists())
        self.assertFalse((root / "no-such-dir").exists())
        self.assertTrue(result.stderr.strip())
        self.assertNotIn("Verdict:", result.stdout)

    def test_delivery_failure_destination_cannot_be_written(self):
        """Delivery failure. An unwritable destination exits 2, intact."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-deliver-blocked", base_files()),
                           root)
        dest = root / "blocked"
        dest.mkdir()
        marker = dest / "kept.txt"
        marker.write_text("kept\n", encoding="utf-8")
        result = run_argv([built, "--report", dest])
        self.assertEqual(result.returncode, 2,
                         "exit is not 2: %r" % (result.returncode,))
        self.assertEqual(marker.read_text(encoding="utf-8"), "kept\n")
        self.assertNotIn("Verdict:", result.stdout)

    def test_delivery_failure_stdout_closes_during_printing(self):
        """Delivery failure. A stdout that closes mid print exits 2."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-deliver-stdout", base_files()),
                           root)
        proc = subprocess.Popen(
            [sys.executable, "-m", "metrics_starter_collector",
             str(built)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=str(REPO_ROOT))
        proc.stdout.close()
        stderr = proc.stderr.read().decode("utf-8", "replace")
        proc.wait(timeout=120)
        self.assertEqual(proc.returncode, 2,
                         "exit is not 2: %r, stderr: %s"
                         % (proc.returncode, stderr[:300]))

    def test_delivery_directory_destination_still_fails_cleanly(self):
        """Delivery failure. A directory destination exits 2, intact."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-deliver-dir", base_files()),
                           root)
        dest = root / "dest-dir"
        dest.mkdir()
        marker = dest / "kept.txt"
        marker.write_text("kept\n", encoding="utf-8")
        result = run_argv([built, "--report", dest])
        self.assertEqual(result.returncode, 2,
                         "exit is not 2: %r" % (result.returncode,))
        self.assertTrue(dest.is_dir())
        self.assertEqual(marker.read_text(encoding="utf-8"), "kept\n")
        self.assertTrue(result.stderr.strip())
        self.assertNotIn("Verdict:", result.stdout)

    def test_delivery_named_regular_destination_writes_exact_bytes(self):
        """Delivery. A named regular destination gets the exact bytes."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-deliver-exact", base_files()),
                           root)
        plain = run_tool(built)
        self.assertEqual(plain.returncode, 0, plain.stderr[:300])
        dest = root / "report.txt"
        result = run_argv([built, "--report", dest])
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(dest.read_bytes(),
                         plain.stdout.encode("utf-8"))
        self.assertFalse((root / "report.txt.tmp-msc").exists())

    def test_delivery_pipe_destination_no_reader_exits_two(self):
        """Delivery failure. A pipe with no reader exits 2, bounded."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-deliver-pipe", base_files()),
                           root)
        dest = root / "report-pipe"
        os.mkfifo(str(dest))
        result = subprocess.run(
            [sys.executable, "-m", "metrics_starter_collector",
             str(built), "--report", str(dest)],
            capture_output=True, text=True, cwd=str(REPO_ROOT),
            timeout=20)
        self.assertEqual(result.returncode, 2,
                         "exit is not 2: %r" % (result.returncode,))
        self.assertTrue(result.stderr.strip())
        self.assertNotIn("Verdict:", result.stdout)

    def test_delivery_staging_link_not_written_through(self):
        """Delivery. A link at the old staging path is never used."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-deliver-stage-link",
                                     base_files()), root)
        sentinel = root / "sentinel.txt"
        sentinel.write_text("sentinel stands\n", encoding="utf-8")
        dest = root / "report.txt"
        staging = root / "report.txt.tmp-msc"
        os.symlink(str(sentinel), str(staging))
        result = run_argv([built, "--report", dest])
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(sentinel.read_text(encoding="utf-8"),
                         "sentinel stands\n")
        self.assertTrue(staging.is_symlink())
        self.assertEqual(os.readlink(str(staging)), str(sentinel))
        self.assertFalse(dest.is_symlink())
        self.assertIn("Verdict:", dest.read_text(encoding="utf-8"))

    def test_delivery_staging_regular_file_left_unchanged(self):
        """Delivery. A regular file at the old staging path stands."""
        root = tracked_tempdir("msc_slice7_")
        built = build_case(make_case("s7-deliver-stage-file",
                                     base_files()), root)
        dest = root / "report.txt"
        staging = root / "report.txt.tmp-msc"
        staging.write_text("staging stands\n", encoding="utf-8")
        result = run_argv([built, "--report", dest])
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertTrue(staging.is_file())
        self.assertFalse(staging.is_symlink())
        self.assertEqual(staging.read_text(encoding="utf-8"),
                         "staging stands\n")
        self.assertIn("Verdict:", dest.read_text(encoding="utf-8"))

    # Header positions and the WV-4 disputed count rerun.

    def test_header_build_identity_conflict_states_each_and_conflict(self):
        """EC-01. Conflicting identities are each stated, none settled."""
        files = base_files()
        files["steps/step-01-record.md"] = step_record(
            1, extra="Build: a different fixture build.")
        result, built = run_case(make_case("s7-header-conflict", files))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        line = result.stdout.splitlines()[1]
        self.assertTrue(line.startswith("Build identity: "))
        self.assertIn("conflict", line.lower())
        self.assertIn("metrics fixture build", line)
        self.assertIn("a different fixture build", line)

    def test_header_no_identity_found_states_absence(self):
        """EC-01. No identity inside the tree states that none was found."""
        case = make_case("s7-header-none", {
            "PATH-LEDGER.md": path_ledger(
                "Step 1 IN PROGRESS 2026-11-01 09:00, closed "
                "2026-11-01 17:00.", "1")})
        result, built = run_case(case)
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        line = result.stdout.splitlines()[1]
        self.assertTrue(line.startswith("Build identity: "))
        self.assertIn("no build identity was found", line.lower())

    def test_wv4_disputed_count_rerun_against_completed_header(self):
        """EC-42. WV-4 disputed count in the completed header form.

        Both counts and the word disagrees stand asserted in the
        completed header, as the Slice 3 WV-4 case asserts them in
        the coverage statement: the metrics record states the step
        universe as 5 steps, the other records state 3 steps, and
        neither count is picked over the other.
        """
        files = base_files(steps=(1, 2, 3))
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(
                body="Metrics record states the step universe "
                     "as 5 steps."))
        result, built = run_case(make_case("s7-wv4-rerun", files))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        self.assertEqual(row_codes(result.stdout), STARTER_ORDER)
        lines = result.stdout.splitlines()
        first_row = lines.index(row_lines(result.stdout)[0])
        head = "\n".join(lines[:first_row])
        self.assertIn("Coverage taken set: ", head)
        self.assertIn("build-metrics-record.md", head)
        self.assertRegex(head, r"(?<!\d)5 steps\b")
        self.assertRegex(head, r"(?<!\d)3 steps\b")
        self.assertIn("disagrees", head.lower())
        e1 = row_line(result.stdout, "E-1")
        parts, order = parts_of(e1)
        self.assertIn("Row coverage", parts)

    def test_f25_report_sections_present_on_clean_tree(self):
        """EC-41 to EC-47. Every report section stands on a clean tree."""
        result, built = run_case(make_case("s7-f25-sections",
                                           base_files()))
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        for heading in ("Disagreements", "Data quality", "Record cost",
                        "Terms"):
            self.assertTrue(section_text(result.stdout, heading),
                            "section stands missing: " + heading)
        self.assertTrue(any(
            ln.startswith("Piece inventory")
            or "piece inventory" in ln.lower()
            for ln in result.stdout.splitlines()),
            "no piece inventory position stands")

    # WV2-21 cross shape comparison, EC-01 to EC-49, in this module.

    def _shape_files(self, second):
        """Return one shape of the WV2-21 pair, substance held equal."""
        files = {}
        transitions = []
        items = [RULED_ITEM]
        for n in (1, 2, 3):
            files["steps/step-%02d-record.md" % n] = step_record(
                n, additions=0)
            files["steps/step-%02d-roster.md" % n] = (
                "# Step %d roster\n\nNamed agents: 2. Base: 2.\n"
                "Roster additions over base: 0.\n" % n)
            if second:
                files["steps/step-%02d-gate-ruling.md" % n] = (
                    gate_ruling(n))
            else:
                files["steps/step-%02d-gate-record.md" % n] = (
                    gate_record(n))
            transitions.append(
                "Step %d IN PROGRESS 2026-11-01 09:00, closed "
                "2026-11-01 17:00." % n)
        files["PATH-LEDGER.md"] = path_ledger(
            "\n".join(transitions), "1, 2, 3")
        files["registers/fix-register.md"] = (
            "# Fix register\n\nEntry one. Origin step: 1.\n")
        files["registers/defect-register.md"] = (
            "# Defect register\n\nEntry one. Origin step: 2.\n")
        table = decision_table(items)
        if second:
            del_files = split_metrics_record_files([
                "# Build metrics record\n\nPage order: 1.\n\n"
                "Step table stands complete for the fixture steps.\n",
                "# Build metrics record page 2\n\nPage order: 2.\n\n"
                + table])
            files.update(del_files)
            files["DECISION-QUEUE.md"] = queue_file(items)
            files["registers/cost-ledger.md"] = (
                "# Cost ledger\n\nNo token figure stands in this "
                "ledger. No money figure stands in this ledger.\n")
        else:
            files["wiki/wiki/synthesis/build-metrics-record.md"] = (
                metrics_record(
                    body="Step table stands complete for the fixture "
                         "steps.",
                    decision_table=table))
        return files

    def _shape_cases(self):
        """Return the two shape case tables, first shape first."""
        first = make_case(
            "s7-shape-one", self._shape_files(False),
            features=("single-page-metrics-record",
                      "decision-table-inside-root", "gate-record-name",
                      "full-clock-timestamps",
                      "decision-items-full-timestamps",
                      "origin-step-on-register-entries"))
        second = make_case(
            "s7-shape-two", self._shape_files(True),
            features=("split-metrics-record",
                      "decision-table-inside-root",
                      "queue-file-inside-root",
                      "queue-governs-over-table",
                      "cost-ledger-inside-root", "gate-ruling-name",
                      "full-clock-timestamps",
                      "decision-items-full-timestamps",
                      "origin-step-on-register-entries",
                      "second-shape-habits"))
        return (first, second)

    def _run_shapes(self):
        """Build both shapes side by side and run the tool on each."""
        root = tracked_tempdir("msc_slice7_")
        built = build_cases(list(self._shape_cases()), root)
        first = run_tool(built["s7-shape-one"])
        second = run_tool(built["s7-shape-two"])
        self.assertEqual(first.returncode, 0, first.stderr[:300])
        self.assertEqual(second.returncode, 0, second.stderr[:300])
        return first.stdout, second.stdout

    def _row_substance(self, report, code):
        """Return the EC-04 compared parts of one row, normalised."""
        line = row_line(report, code)
        parts, order = parts_of(line)
        substance = {"verdict": row_verdict(line)}
        for label in ("Value", "Numerator", "Denominator",
                      "Row coverage", "Reason", "Pointer"):
            if label in parts:
                value = parts[label].lower()
                value = value.replace("gate ruling", "gate file")
                value = value.replace("gate record", "gate file")
                substance[label] = re.sub(r"\s+", " ", value).strip()
        return substance

    def _shape_substance(self, report, code):
        """Return the row substance scoped to the common substance.

        The Pointer part stands removed where the code is E-3,
        E-4, B-2, or D-1, the Reason part stands removed where the
        code is E-3, E-4, or B-2, and the verdict stands removed
        where the code is E-4. Those limbs turn on the ledger
        standing, absent in the first shape and standing with no
        figures in the second, and stand asserted shape by shape
        under _assert_ledger_limbs. Every other code returns the
        substance unchanged.
        """
        substance = dict(self._row_substance(report, code))
        if code in ("E-3", "E-4", "B-2", "D-1"):
            substance.pop("Pointer", None)
        if code in ("E-3", "E-4", "B-2"):
            substance.pop("Reason", None)
        if code == "E-4":
            substance.pop("verdict", None)
        return substance

    def _assert_ledger_limbs(self, first, second):
        """Assert the ledger standing limbs shape by shape."""
        one_e3 = self._row_substance(first, "E-3")
        two_e3 = self._row_substance(second, "E-3")
        self.assertEqual(one_e3["verdict"], "missing")
        self.assertEqual(two_e3["verdict"], "missing")
        self.assertIn("cost ledger record inside the root",
                      one_e3["Reason"])
        self.assertIn("no cost ledger stands in the tree",
                      one_e3["Reason"])
        self.assertIn("cost ledger token figure field",
                      two_e3["Reason"])
        self.assertIn("the cost ledger stands in the tree",
                      two_e3["Reason"])
        self.assertIn("no token figure stands in it",
                      two_e3["Reason"])
        self.assertIn("looked for and not found", one_e3["Pointer"])
        self.assertIn("registers/cost-ledger.md", one_e3["Pointer"])
        self.assertEqual(two_e3["Pointer"], "registers/cost-ledger.md")
        one_e4 = self._row_substance(first, "E-4")
        two_e4 = self._row_substance(second, "E-4")
        self.assertEqual(one_e4["verdict"], "missing")
        self.assertEqual(two_e4["verdict"],
                         "present but not derivable")
        self.assertIn("no cost ledger piece and no step record",
                      one_e4["Reason"])
        self.assertIn("per step money figure field", two_e4["Reason"])
        self.assertIn("missing-field", two_e4["Reason"])
        self.assertEqual(one_e4["Pointer"], "registers/cost-ledger.md")
        self.assertIn("steps/step-01-record.md", two_e4["Pointer"])
        one_b2 = self._row_substance(first, "B-2")
        two_b2 = self._row_substance(second, "B-2")
        self.assertEqual(one_b2["verdict"],
                         "present but not derivable")
        self.assertEqual(two_b2["verdict"],
                         "present but not derivable")
        self.assertIn("no cost ledger stands in the tree",
                      one_b2["Reason"])
        self.assertIn(
            "no figure stands for either limb where no cost ledger "
            "stands", one_b2["Reason"])
        self.assertIn(
            "a cost ledger stands in the tree and it carries no "
            "spent or budget figure for either side", two_b2["Reason"])
        self.assertIn(
            "where no figure stands in the ledger for either side",
            two_b2["Reason"])
        self.assertIn("looked for and not found", one_b2["Pointer"])
        self.assertEqual(two_b2["Pointer"], "registers/cost-ledger.md")
        one_d1 = self._row_substance(first, "D-1")
        two_d1 = self._row_substance(second, "D-1")
        self.assertEqual(one_d1["Pointer"],
                         "wiki/wiki/synthesis/build-metrics-record.md")
        self.assertEqual(two_d1["Pointer"], "decision-queue.md")

    def _assert_rows_equivalent(self, first, second):
        """Assert EC-04 row by row equivalence, naming any difference."""
        self.assertEqual(row_codes(first), STARTER_ORDER)
        self.assertEqual(row_codes(second), STARTER_ORDER)
        for code in STARTER_ORDER:
            one = self._shape_substance(first, code)
            two = self._shape_substance(second, code)
            self.assertEqual(
                one, two,
                "row %s differed between shapes: first shape %r, "
                "second shape %r; shape difference: split record, "
                "ledger inside root, governing queue file, ruling "
                "name gate files" % (code, one, two))
        self._assert_ledger_limbs(first, second)

    def test_wv21_cross_shape_full_set_rows_equivalent(self):
        """EC-01 to EC-49. Full 17 row comparison across the two shapes."""
        first, second = self._run_shapes()
        self._assert_rows_equivalent(first, second)

    def test_wv21_cross_shape_framing_and_habit_points(self):
        """EC-01, EC-02, EC-03, EC-05, EC-06, EC-07, EC-08, EC-09."""
        first, second = self._run_shapes()
        for report in (first, second):
            lines = report.splitlines()
            self.assertTrue(lines[1].startswith("Build identity: "))
            self.assertIn("metrics fixture build", lines[1])
            self.assertNotIn("Definitions version", report)
        self._assert_rows_equivalent(first, second)

    def test_wv21_cross_shape_content_points(self):
        """EC-10 to EC-23. Feeder substance stands the same in both."""
        first, second = self._run_shapes()
        self._assert_rows_equivalent(first, second)
        for code in ("T-1", "E-1", "E-2", "Q-3", "D-1", "B-2"):
            self.assertEqual(self._shape_substance(first, code),
                             self._shape_substance(second, code),
                             "content point row %s differed" % code)

    def test_wv21_cross_shape_row_points(self):
        """EC-24 to EC-40. One equivalence assertion per metric row."""
        first, second = self._run_shapes()
        for code in STARTER_ORDER:
            self.assertEqual(
                self._shape_substance(first, code),
                self._shape_substance(second, code),
                "row point for %s differed between shapes" % code)
        self._assert_ledger_limbs(first, second)

    def test_wv21_cross_shape_report_level_points(self):
        """EC-41 to EC-49. Header, sections and closed content agree.

        Corrected at Step 15 round 1, items R15-01 and R15-04:
        the missing field counts move by two in each shape.
        The F-2 row of each shape, whose gate files state no
        first ruling outcome, now stands present but not
        derivable on the missing field form instead of present
        on closing states alone, and the T-4 row of each shape,
        whose ledger holds no BANKED entry, now stands present
        but not derivable on the missing field form instead of
        missing on the no feeder record form. Each change adds
        one missing field entry to its shape count.
        """
        first, second = self._run_shapes()
        for report in (first, second):
            lines = report.splitlines()
            self.assertTrue(lines[0].startswith("Root: "))
            self.assertTrue(lines[1].startswith("Build identity: "))
            for heading in ("Disagreements", "Data quality",
                            "Record cost", "Terms"):
                self.assertTrue(section_text(report, heading),
                                "section missing: " + heading)
            lowered = report.lower()
            for word in ("score:", "grade:", "digest", "estimated"):
                self.assertNotIn(word, lowered)
            dq_one = section_text(report, "Data quality")
            self.assertTrue(dq_one)
        self.assertEqual(
            "\n".join(
                ln for ln in section_text(first, "Data quality")
                .splitlines()
                if not ln.strip().lower().startswith("missing field:")),
            "\n".join(
                ln for ln in section_text(second, "Data quality")
                .splitlines()
                if not ln.strip().lower().startswith("missing field:")),
            "data quality section differed between shapes")
        self.assertIn("missing field: 4",
                      section_text(first, "Data quality"))
        self.assertIn("missing field: 5",
                      section_text(second, "Data quality"))
        self.assertEqual(
            disagreements_block(first), disagreements_block(second),
            "disagreements block differed between shapes")
        self._assert_rows_equivalent(first, second)

    def test_wv21_cross_shape_determinism_within_each_shape(self):
        """EC-48. Each shape repeats byte identically on its own tree."""
        root = tracked_tempdir("msc_slice7_")
        built = build_cases(list(self._shape_cases()), root)
        for name in ("s7-shape-one", "s7-shape-two"):
            one = run_tool(built[name])
            two = run_tool(built[name])
            self.assertEqual(one.returncode, 0, one.stderr[:300])
            self.assertEqual(one.stdout, two.stdout,
                             "shape %s differed between its own runs"
                             % name)
