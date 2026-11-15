"""Slice 4 tests: time and decision family, T-1, T-2, T-4, D-1, B-1, B-3, B-4.

Every case states the EC points and the WV22 fields it asserts in its
first line, in the citation forms the test design record states.
Fixture trees are built through the fixture builder case table form,
with build_case or build_cases into a tracked temporary directory,
and the product is invoked through run_tool, which runs the module
entry route as a subprocess from the repo root with the root argument
first.
"""
import re
import unittest

from tests.fixture_builder import (
    FixtureTestCase, STARTER_ORDER, assert_reads_capture_only,
    d1_case, d1_files, make_case,
    assert_verdict, build_case, build_cases, coverage_statement,
    data_quality_entry_for, decision_table, gate_record, metrics_record,
    path_ledger, queue_file, row_block, row_order, row_verdict,
    run_tool, split_metrics_record_files, statement_segment,
    step_record, tracked_tempdir)

RULED_ROW = ("| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
             "2026-11-01 13:00 |")
RULED_ROW_LATE = ("| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
                  "2026-11-01 19:00 |")
RULED_ROW_2 = ("| Q-2 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | "
               "2026-11-01 11:00 |")
OPEN_ROW = "| Q-3 | 2 | 2026-11-02 09:00 | 2026-11-02 10:00 |  |"
DATE_ONLY_ROW = "| Q-4 | 2 | 2026-11-02 | 2026-11-02 | 2026-11-03 |"


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
    root = tracked_tempdir("msc_slice4_")
    built = build_case(case, root)
    return run_tool(built), built


def assert_foundation(test, block, fragment):
    test.assertIn("foundation", block.lower())
    test.assertIn(fragment, block)


def assert_median(test, block, hours):
    match = re.search(r"median[^\d]*(\d+(?:\.\d+)?)", block)
    test.assertIsNotNone(match, "median figure stands in the D-1 row")
    test.assertEqual(float(match.group(1)), float(hours))


def parts_of(text):
    """Split row or entry text into its labelled parts, label to value."""
    parts = {}
    for chunk in re.split(r"\s*\|\s*|\n", text):
        chunk = chunk.strip()
        if ": " in chunk:
            label, value = chunk.split(": ", 1)
            if label.strip() not in parts:
                parts[label.strip()] = value.strip()
    return parts


def disagreements_block(report):
    """Return the disagreements block text of a report, or empty."""
    lines = report.splitlines()
    heads = ("Disagreements", "Data quality", "Record cost", "Terms")
    for idx, line in enumerate(lines):
        if line.strip() == "Disagreements":
            end = len(lines)
            for later in range(idx + 1, len(lines)):
                if lines[later].strip() in heads:
                    end = later
                    break
            return "\n".join(lines[idx:end])
    return ""


def block_entries(report):
    """Return entry line texts inside the disagreements block."""
    entries = []
    for line in disagreements_block(report).splitlines():
        if line.startswith("Records:"):
            entries.append(line)
    return entries


def row_substance(report, code):
    """Return the EC-04 compared parts of one row, normalised.

    In the form the Slice 7 _row_substance helper shows: verdict,
    and each labelled part the row carries among Value, Numerator,
    Denominator, Row coverage, Reason and Pointer, lowercased with
    whitespace collapsed. The governing feeder file names are
    normalised to one token, as the Slice 7 helper normalises the
    gate file names the habit varies: DECISION-QUEUE.md and the
    metrics record name both stand for the governing feeder here.
    """
    block = row_block(report, code)
    parts = parts_of(block)
    substance = {"verdict": row_verdict(block)}
    for label in ("Value", "Numerator", "Denominator",
                  "Row coverage", "Reason", "Pointer"):
        if label in parts:
            value = parts[label].lower()
            value = value.replace(
                "wiki/wiki/synthesis/build-metrics-record.md",
                "governing feeder")
            value = value.replace("decision-queue.md",
                                  "governing feeder")
            value = value.replace("build-metrics-record.md",
                                  "governing feeder")
            value = value.replace("gate ruling", "gate file")
            value = value.replace("gate record", "gate file")
            substance[label] = re.sub(r"\s+", " ", value).strip()
    return substance


def ranked_files(durations, steps=None):
    """Return files whose steps carry the given elapsed and active hours.

    durations maps a step number to an (elapsed, active) pair in hours.
    The opening stands at 09:00 and the closing is formed from the
    elapsed figure, so the T-1 and T-2 inputs stand in the ledger.
    """
    if steps is None:
        steps = tuple(sorted(durations))
    files = base_files(steps=steps)
    lines = []
    for n in steps:
        elapsed, active = durations[n]
        closing = 9 + elapsed
        lines.append(
            "Step %d IN PROGRESS 2026-11-01 09:00, closed "
            "2026-11-01 %02d:00. Active %d hours." % (n, closing, active))
    files["PATH-LEDGER.md"] = path_ledger(
        "\n".join(lines), ", ".join(str(s) for s in steps))
    return files


class TestSlice4TimeDecision(FixtureTestCase):

    # D-05 lexical boundary, spin 771 grammar as supplemented by spin 782.

    def test_d05_zoned_form_with_seconds_counts(self):
        """EC-24; WV22 T-1 F1, F2. Form 2026-11-09 14:32:07+00:00 counts."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-09 14:32:07+00:00, closed "
            "2026-11-09 17:32:07+00:00.")
        result, _ = run_case(make_case(
            "d05-zoned-seconds", files, ["full-clock-timestamps"]))
        for code in ("T-1", "T-2"):
            assert_verdict(self, row_block(result.stdout, code),
                           "present", code)

    def test_d05_plain_form_without_seconds_or_zone_counts(self):
        """EC-24; WV22 T-1 F1, F2. Form 2026-11-09 14:32 counts."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-09 14:32, closed "
            "2026-11-09 17:32.")
        result, _ = run_case(make_case(
            "d05-plain", files, ["full-clock-timestamps"]))
        for code in ("T-1", "T-2"):
            assert_verdict(self, row_block(result.stdout, code),
                           "present", code)

    def test_d05_weekday_prefix_agreeing_counts(self):
        """EC-24; WV22 T-1 F1, F2. Weekday as prefix only, agreeing form."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS Mon 2026-11-09 14:32, closed "
            "Mon 2026-11-09 17:32.")
        result, _ = run_case(make_case(
            "d05-weekday-agree", files, ["full-clock-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "T-1"),
                       "present", "T-1")

    def test_d05_weekday_prefix_disagreeing_counts(self):
        """EC-24; WV22 T-1 F1, F2. Weekday prefix only, disagreeing counts.

        Spin 782 pick: Fri 2026-11-09 14:32 counts although Fri disagrees
        with the calendar day of 2026-11-09, which is a Monday.
        """
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS Fri 2026-11-09 14:32, closed "
            "Fri 2026-11-09 17:32.")
        result, _ = run_case(make_case(
            "d05-weekday-disagree", files, ["full-clock-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "T-1"),
                       "present", "T-1")

    def test_d05_word_later_is_no_timestamp(self):
        """EC-24; WV22 T-1 F1, F2. The word later counts as neither form."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS later, closed later.")
        result, _ = run_case(make_case(
            "d05-later", files, ["full-clock-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "T-1"),
                       "missing", "T-1")

    def test_d05_time_with_no_date_counts_for_nothing(self):
        """EC-24; WV22 T-1 F1, F2. A clock reading alone forms no interval."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 14:32, closed 17:32.")
        result, _ = run_case(make_case(
            "d05-time-no-date", files, ["full-clock-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "T-1"),
                       "missing", "T-1")

    def test_d05_zoned_time_with_no_date_fails(self):
        """EC-24; WV22 T-1 F1. A zoned time with no date part still fails."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 14:32:07+00:00, closed 17:32:07+00:00.")
        result, _ = run_case(make_case(
            "d05-zoned-no-date", files, ["full-clock-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "T-1"),
                       "missing", "T-1")

    def test_d05_zoned_against_unzoned_compared_as_written(self):
        """EC-25; WV22 T-2 F1, F2. Comparison as clock readings, no conversion.

        Spin 782 pick: opening 09:00 with a +05:00 offset against closing
        17:00 with no offset forms an interval of 8 hours from the clock
        readings as written, with no conversion applied.
        """
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00+05:00, closed "
            "2026-11-01 17:00.")
        result, _ = run_case(make_case(
            "d05-zoned-unzoned", files, ["full-clock-timestamps"]))
        block = row_block(result.stdout, "T-2")
        assert_verdict(self, block, "present", "T-2")
        self.assertRegex(block, r"(?<![\d.])8(?:\.0)?(?![\d.])")

    def test_d05_text_duration_counts_for_t2(self):
        """EC-25; WV22 T-2 F2. A text duration stating amount and unit counts."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 stands with a stated duration of 2 hours.")
        result, _ = run_case(make_case(
            "d05-text-duration-t2", files, ["full-clock-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "T-2"),
                       "present", "T-2")

    def test_d05_text_without_amount_is_no_duration(self):
        """EC-25, EC-26; WV22 T-2 F2, WV22 T-4 F1. Later states no duration."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED entry, duration later, on Q-1.")
        result, _ = run_case(make_case(
            "d05-later-duration", files, ["banked-entries-with-duration"]))
        assert_verdict(self, row_block(result.stdout, "T-4"),
                       "present but not derivable", "T-4")

    def test_f02_date_only_timestamps_t1_and_t2_missing(self):
        """EC-24, EC-25; WV22 T-1 F1, F2, WV22 T-2 F1, F2. F-02 date only."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.")
        result, _ = run_case(make_case(
            "f02-date-only", files, ["date-only-timestamps"]))
        for code in ("T-1", "T-2"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "missing", code)
            self.assertIn("date-only-form", block, code)

    def test_t1_closing_date_only_fails_both_transitions_condition(self):
        """EC-24; WV22 T-1 F2. Opening passes and closing date only fails."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-02.")
        result, _ = run_case(make_case(
            "t1-closing-date-only", files, ["full-clock-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "T-1"),
                       "missing", "T-1")

    def test_t2_pairing_timestamps_of_two_steps_forms_no_interval(self):
        """EC-25; WV22 T-2 F1. Timestamps of two different steps do not pair."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00.\n"
            "Step 2 closed 2026-11-01 17:00.")
        result, _ = run_case(make_case(
            "t2-cross-step-pair", files, ["full-clock-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "T-2"),
                       "missing", "T-2")

    def test_mixed_series_partial_span(self):
        """EC-24, EC-25; WV22 T-1 F1, F2. Mixed series under partial-span."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00, closed 2026-11-01 17:00.\n"
            "Step 2 IN PROGRESS 2026-11-02, closed 2026-11-03.\n"
            "Step 3 stands with no transitions.")
        result, _ = run_case(make_case(
            "mixed-partial-span", files, ["full-clock-timestamps"]))
        block = row_block(result.stdout, "T-1")
        assert_verdict(self, block, "present but not derivable", "T-1")
        self.assertIn("partial-span", block)
        for name in ("Step 1", "Step 2", "Step 3"):
            self.assertIn(name, block)

    # T-4 fields and feeder combinations, Part 3 form.

    def test_t4_banked_count_without_duration_yields_no_figure(self):
        """EC-26; WV22 T-4 F1. A count of BANKED items never counts."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED entries stand, count 2, no duration stated.")
        result, _ = run_case(make_case(
            "t4-count-no-duration", files, ["banked-entries-no-duration"]))
        assert_verdict(self, row_block(result.stdout, "T-4"),
                       "present but not derivable", "T-4")

    def test_t4_queue_combination_item_in_queue_counts(self):
        """EC-26, EC-08; WV22 T-4 F2, F3. Queue governs, item in queue counts."""
        files = base_files()
        files["DECISION-QUEUE.md"] = queue_file([RULED_ROW])
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED duration 2 hours on Q-1.")
        result, _ = run_case(make_case(
            "t4-queue-item-counts", files,
            ["banked-entries-with-duration", "queue-file-inside-root",
             "queue-governs-over-table"]))
        assert_verdict(self, row_block(result.stdout, "T-4"),
                       "present", "T-4")

    def test_t4_queue_combination_table_only_item_fails(self):
        """EC-26, EC-08; WV22 T-4 F2, F3. Table does not rescue a queue miss."""
        files = base_files()
        files["DECISION-QUEUE.md"] = queue_file([RULED_ROW_2])
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(decision_table=decision_table([RULED_ROW])))
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED duration 2 hours on Q-1.")
        result, _ = run_case(make_case(
            "t4-queue-table-only", files,
            ["banked-entries-with-duration", "queue-file-inside-root",
             "decision-table-inside-root", "queue-governs-over-table"]))
        assert_verdict(self, row_block(result.stdout, "T-4"),
                       "present but not derivable", "T-4")

    def test_t4_degraded_combination_table_item_counts_with_marking(self):
        """EC-26; WV22 T-4 F4. No queue, table stands, degraded marking."""
        files = base_files()
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(decision_table=decision_table([RULED_ROW])))
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED duration 2 hours on Q-1.")
        result, _ = run_case(make_case(
            "t4-degraded-table", files,
            ["banked-entries-with-duration", "decision-table-inside-root"]))
        block = row_block(result.stdout, "T-4")
        assert_verdict(self, block, "present", "T-4")
        self.assertIn("degraded", block.lower())

    def test_t4_no_cross_check_combination_no_item_counts(self):
        """EC-26; WV22 T-4 F5. Neither feeder, no item counts, no marking."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED duration 2 hours on Q-1.")
        result, _ = run_case(make_case(
            "t4-no-cross-check", files, ["banked-entries-with-duration"]))
        block = row_block(result.stdout, "T-4")
        assert_verdict(self, block, "present but not derivable", "T-4")
        self.assertNotIn("degraded", statement_segment(block).lower())
        self.assertIn("PATH-LEDGER", block)

    def test_t4_present_row_cross_check_marking_in_statement_line(self):
        """EC-26; WV22 T-4 F3. Record disagrees qualifier in statement line."""
        files = base_files()
        files["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Metrics record states T-4 wait as 99 hours.",
            decision_table=decision_table([RULED_ROW]))
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED duration 2 hours on Q-1.")
        result, _ = run_case(make_case(
            "t4-cross-check-marking", files,
            ["banked-entries-with-duration", "decision-table-inside-root"]))
        block = row_block(result.stdout, "T-4")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("build-metrics-record.md", segment)
        self.assertIn("2 hours", segment)
        self.assertIn("99 hours", segment)

    def test_b_rows_present_row_cross_check_marking_in_statement_line(self):
        """EC-37, EC-39, EC-40; WV22 B-1 F1, F2, WV22 B-3 F1, F2, WV22 B-4 F1, F2.

        Record disagrees qualifier in the statement line of a present
        B row, in the form of the T-4 named marking test. The metrics
        record states a figure of 99 hours for Step 1 for each of
        B-1, B-3 and B-4, against the feeder figures the B derivations
        form from the T-1 and T-2 series for Step 1: elapsed 10 hours
        for B-1 and for B-3, and active 8 hours for B-4. Each affected
        row stands present, its statement line carries the record
        disagrees qualifier with the disagreeing record named, the
        figure each side supports and both figures standing, and the
        feeder figure stands, with the B-1 build totals formed from
        the feeder figures and not from the record figure.
        """
        files = ranked_files({1: (10, 8), 2: (9, 9), 3: (8, 4)})
        files["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Metrics record states B-1 for Step 1 as 99 hours. "
                 "Metrics record states B-3 for Step 1 as 99 hours. "
                 "Metrics record states B-4 for Step 1 as 99 hours.")
        result, _ = run_case(make_case(
            "b-rows-cross-check-marking", files,
            ["full-clock-timestamps"]))
        expected = {"B-1": "10 hours", "B-3": "10 hours",
                    "B-4": "8 hours"}
        for code, feeder in expected.items():
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present", code)
            segment = statement_segment(block)
            self.assertIn("record disagrees", segment, code)
            self.assertIn("build-metrics-record.md", segment, code)
            self.assertIn(feeder, segment, code)
            self.assertIn("99 hours", segment, code)
            self.assertIn("feeder figure stands", segment, code)
        b1 = row_block(result.stdout, "B-1")
        self.assertIn("build elapsed 27 hours", b1)
        self.assertIn("build active 21 hours", b1)

    def test_t4_degraded_row_shown_without_queue_cross_check(self):
        """EC-26; WV22 T-4 F1, F4. Named degraded row test from Section 2."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED interval duration 2 hours. "
            "Step 2 BANKED interval duration 3 hours.")
        result, _ = run_case(make_case(
            "t4-degraded-named", files, ["banked-entries-with-duration"]))
        block = row_block(result.stdout, "T-4")
        assert_verdict(self, block, "present", "T-4")
        self.assertIn("without its queue cross check", block)
        self.assertIn("without its queue cross check",
                      statement_segment(block))

    # F-20 mapping test: feeders inside the root only, Slice 4 form.

    def test_f20_inside_feeders_govern_outside_file_changes_nothing(self):
        """F-20; EC-04, EC-08; WV22 T-4 F3, WV22 D-1 F1, F2. Inside only.

        Plan Section 15 duty 2 supplement, F-20 mapping test: inside
        the root a queue file and a decision table disagree on item
        Q-1, the queue ruling at 13:00 against the table ruling at
        19:00; outside the root a file carries a 99 hour figure for
        T-4 and for D-1, whose inside feeders also stand. The verdicts
        are the verdicts the inside feeders give, unchanged by the
        outside file; the T-4 derivation follows the queue figure;
        the table figure stands in the disagreements block under the
        CA2-02 wording for that item; and no ungoverned wording
        stands for that item.
        """
        files = base_files()
        files["DECISION-QUEUE.md"] = queue_file([RULED_ROW])
        files["wiki/wiki/synthesis/build-metrics-record.md"] = (
            metrics_record(decision_table=decision_table(
                [RULED_ROW_LATE])))
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 BANKED duration 2 hours on Q-1.")
        features = ["banked-entries-with-duration",
                    "queue-file-inside-root",
                    "decision-table-inside-root",
                    "queue-governs-over-table"]
        root = tracked_tempdir("msc_slice4_f20_")
        built = build_cases(
            [make_case("f20-control", dict(files), features),
             make_case("f20-outside", dict(files), features)], root)
        control = run_tool(built["f20-control"])
        self.assertEqual(control.returncode, 0, control.stderr[:300])
        outside_file = root / "outside-root-figure.md"
        outside_file.write_text(
            "Outside figure: T-4 wait stands at 99 hours. "
            "D-1 median stands at 99 hours.\n", encoding="utf-8")
        result = run_tool(built["f20-outside"])
        self.assertEqual(result.returncode, 0, result.stderr[:300])
        for code in STARTER_ORDER:
            self.assertEqual(
                row_verdict(row_block(control.stdout, code)),
                row_verdict(row_block(result.stdout, code)),
                "verdict changed by the outside file: " + code)
        d1 = row_block(result.stdout, "D-1")
        assert_verdict(self, d1, "present", "D-1")
        assert_foundation(self, d1, "DECISION-QUEUE.md")
        assert_median(self, d1, 4)
        self.assertNotIn("99", d1)
        segment = statement_segment(d1)
        self.assertIn("record disagrees", segment)
        self.assertIn("13:00", segment)
        self.assertIn("19:00", segment)
        t4 = row_block(result.stdout, "T-4")
        self.assertEqual(row_verdict(t4),
                         row_verdict(row_block(control.stdout, "T-4")))
        self.assertNotIn("99", t4)
        block = disagreements_block(result.stdout)
        self.assertTrue(block, "no disagreements block stands")
        entries = block_entries(result.stdout)
        self.assertTrue(entries, "no disagreements entry stands")
        table_entries = []
        for entry in entries:
            entry_parts = parts_of(entry)
            if "19:00" in entry_parts.get("Figures", ""):
                table_entries.append(entry_parts)
            if entry_parts.get("Governing position", "") == (
                    "ungoverned with no verdict depending on it"):
                self.assertNotIn("19:00",
                                 entry_parts.get("Figures", ""), entry)
                self.assertNotIn("Q-1", entry)
        self.assertTrue(table_entries,
                        "the table figure stands in no block entry")
        for entry_parts in table_entries:
            self.assertIn("13:00", entry_parts["Figures"])
            self.assertEqual(entry_parts["Governing position"],
                             "governed with the pattern named")

    # D-1 fields, split item sets, and the nine feeder cells.

    def test_d1_ruled_open_and_date_only_items(self):
        """EC-36, EC-17; WV22 D-1 F1, F2, F5, F7. Ruled, open, date only."""
        result, _ = run_case(d1_case(
            "d1-mixed-items", queue_rows=[RULED_ROW, RULED_ROW_2,
                                          OPEN_ROW, DATE_ONLY_ROW]))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        self.assertIn("open", block.lower())
        self.assertIn("Q-3", block)
        self.assertIn("Q-4", block)

    def test_d1_presented_blank_counts_for_headline_not_second(self):
        """EC-36; WV22 D-1 F3, F4. Presented required for second interval only."""
        row = "| Q-9 | 1 | 2026-11-01 09:00 |  | 2026-11-01 13:00 |"
        result, _ = run_case(d1_case("d1-presented-blank",
                                     queue_rows=[row]))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_median(self, block, 4)
        self.assertIn("Q-9", block)

    def test_d1_split_median_and_longest_from_counting_items_alone(self):
        """EC-36; WV22 D-1 F5. Figures formed from counting items alone."""
        rows = [RULED_ROW, RULED_ROW_2, OPEN_ROW, DATE_ONLY_ROW]
        result, _ = run_case(d1_case("d1-split-figures", queue_rows=rows))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_median(self, block, 2)
        self.assertRegex(block, r"longest[^\d]*4(?!\d)")

    def test_d1_even_count_median_is_lower_middle_never_mean(self):
        """EC-36; WV22 D-1 F6. Even count median is the lower middle value."""
        rows = [
            "| Q-1 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | 2026-11-01 11:00 |",
            "| Q-2 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | 2026-11-01 13:00 |",
            "| Q-5 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | 2026-11-01 15:00 |",
            "| Q-6 | 1 | 2026-11-01 09:00 | 2026-11-01 10:00 | 2026-11-01 19:00 |"]
        result, _ = run_case(d1_case("d1-even-median", queue_rows=rows))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_median(self, block, 4)

    def test_d1_no_ruled_item_is_not_derivable_with_coverage(self):
        """EC-36; WV22 D-1 F7. Empty counting set, coverage names the lack."""
        result, _ = run_case(d1_case("d1-no-ruled", queue_rows=[OPEN_ROW]))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present but not derivable", "D-1")
        self.assertIn("open", block.lower())
        self.assertIn("Q-3", block)

    def test_d1_empty_decision_table_is_not_derivable(self):
        """EC-36; WV22 D-1 F7. Table stands and holds no items at all."""
        files = d1_files(table_rows=[])
        result, _ = run_case(make_case(
            "d1-empty-table", files,
            ["decision-items-full-timestamps", "decision-table-inside-root",
             "single-page-metrics-record"]))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present but not derivable", "D-1")
        self.assertIn("no item", block.lower())

    def test_d1_cell_queue_named_complete_single_page(self):
        """EC-36, EC-08, EC-06; WV22 D-1 F1, F2. Cell 1 of 9, queue, single."""
        result, _ = run_case(d1_case(
            "d1-cell-1", queue_rows=[RULED_ROW], table_rows=[RULED_ROW_LATE]))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "DECISION-QUEUE.md")
        assert_median(self, block, 4)

    def test_d1_cell_queue_named_complete_split(self):
        """EC-36, EC-08, EC-06; WV22 D-1 F1, F2. Cell 2 of 9, queue, split."""
        result, _ = run_case(d1_case(
            "d1-cell-2", queue_rows=[RULED_ROW],
            table_rows=[RULED_ROW_LATE], split=True))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "DECISION-QUEUE.md")
        assert_median(self, block, 4)

    def test_d1_cell_queue_named_no_decision_table(self):
        """EC-36, EC-08; WV22 D-1 F1, F2. Cell 3 of 9, queue, no table."""
        result, _ = run_case(d1_case("d1-cell-3", queue_rows=[RULED_ROW]))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "DECISION-QUEUE.md")
        assert_median(self, block, 4)

    def test_d1_cell_no_queue_complete_single_page(self):
        """EC-36, EC-06; WV22 D-1 F1, F2. Cell 4 of 9, no queue, single."""
        result, _ = run_case(d1_case("d1-cell-4", table_rows=[RULED_ROW]))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "decision table")
        assert_median(self, block, 4)

    def test_d1_cell_no_queue_complete_split(self):
        """EC-36, EC-06; WV22 D-1 F1, F2. Cell 5 of 9, no queue, split."""
        result, _ = run_case(d1_case("d1-cell-5", table_rows=[RULED_ROW],
                                     split=True))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "decision table")
        assert_median(self, block, 4)

    def test_d1_cell_no_queue_no_decision_table_missing(self):
        """EC-36; WV22 D-1 F7. Cell 6 of 9, no queue and no table, missing."""
        result, _ = run_case(d1_case("d1-cell-6"))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "missing", "D-1")
        assert_foundation(self, block, "no feeder")

    def test_d1_cell_unusable_queue_complete_single_page(self):
        """EC-36; WV22 D-1 F1, F2. Cell 7 of 9, unusable queue, single."""
        result, _ = run_case(d1_case(
            "d1-cell-7", table_rows=[RULED_ROW], unusable_queue=True))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "decision table")
        entry = data_quality_entry_for(result.stdout, "DECISION-QUEUE.md")
        self.assertTrue(entry, "queue file named in data quality section")
        self.assertIn("not read in full", entry.lower())

    def test_d1_cell_unusable_queue_complete_split(self):
        """EC-36, EC-06; WV22 D-1 F1, F2. Cell 8 of 9, unusable, split."""
        result, _ = run_case(d1_case(
            "d1-cell-8", table_rows=[RULED_ROW], split=True,
            unusable_queue=True))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "decision table")
        entry = data_quality_entry_for(result.stdout, "DECISION-QUEUE.md")
        self.assertTrue(entry, "queue file named in data quality section")
        self.assertIn("not read in full", entry.lower())

    def test_d1_cell_unusable_queue_no_complete_table(self):
        """EC-36; WV22 D-1 F7. Cell 9 of 9, unusable queue, no complete table."""
        result, _ = run_case(d1_case("d1-cell-9", unusable_queue=True))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present but not derivable", "D-1")
        assert_foundation(self, block, "DECISION-QUEUE.md")

    def test_d1_row_rendered_in_full_with_cross_check_marking(self):
        """EC-36, EC-08, EC-04; WV22 D-1 F1, F2. Named full row test."""
        result, _ = run_case(d1_case(
            "d1-full-row", queue_rows=[RULED_ROW],
            table_rows=[RULED_ROW_LATE]))
        block = row_block(result.stdout, "D-1")
        assert_verdict(self, block, "present", "D-1")
        assert_foundation(self, block, "DECISION-QUEUE.md")
        segment = statement_segment(block)
        self.assertIn("record disagrees", segment)
        self.assertIn("decision table", segment.lower())
        self.assertIn("13:00", segment)
        self.assertIn("19:00", segment)
        assert_median(self, block, 4)

    # B-1 fields.

    def test_b1_both_derivation_outputs_stand_present(self):
        """EC-37; WV22 B-1 F1, F2. Elapsed and active outputs for one step."""
        result, _ = run_case(make_case(
            "b1-present", base_files(), ["full-clock-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "B-1"),
                       "present", "B-1")

    def test_b1_feeder_figure_alone_counts_for_nothing(self):
        """EC-37; WV22 B-1 F1, F2. A feeder B-1 figure counts for nothing."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 stands. B-1 elapsed figure stated as 8 hours.")
        files["steps/step-01-record.md"] = step_record(
            1, extra="B-1 elapsed 8 hours, active 8 hours.")
        result, _ = run_case(make_case(
            "b1-feeder-figure", files, ["date-only-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "B-1"),
                       "missing", "B-1")

    def test_a7_9_b1_cross_piece_basis_mismatch_no_code_fits(self):
        """EC-37; WV22 B-1 F1, F2. A7-9 basis mismatch, no code fits."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01 09:00 UTC, first timestamp "
            "stands with its basis stated as UTC.")
        files["steps/step-03-gate-record.md"] = (
            "# Step 3 gate record\n\nClosing ruling at 2026-11-03 17:00 "
            "with no time basis stated.\nClosure state: CLOSED-PASS.\n")
        result, _ = run_case(make_case(
            "b1-basis-mismatch", files, ["full-clock-timestamps"]))
        block = row_block(result.stdout, "B-1")
        assert_verdict(self, block, "present but not derivable", "B-1")
        self.assertIn("no code fits", block.lower())
        self.assertIn("UTC", block)
        self.assertTrue("no time basis" in block.lower()
                        or "no basis" in block.lower(), block[:500])

    # B-3 ranking fields and edges.

    def test_b3_rankable_inputs_and_wait_share(self):
        """EC-39; WV22 B-3 F1, F2, F3. Rankable steps and wait share form."""
        files = ranked_files({1: (10, 8), 2: (9, 9), 3: (8, 4)})
        result, _ = run_case(make_case(
            "b3-wait-share", files, ["full-clock-timestamps"]))
        block = row_block(result.stdout, "B-3")
        assert_verdict(self, block, "present", "B-3")
        self.assertIn("Step 1", block)
        self.assertTrue("wait" in block.lower() and "share" in block.lower(),
                        block[:500])

    def test_b3_ranking_tie_at_third_place_cut_runs_past_three(self):
        """EC-39; WV22 B-3 F4. Tie at the third place cut, all tied named."""
        files = ranked_files({1: (12, 12), 2: (11, 11), 3: (10, 10),
                              4: (10, 10), 5: (9, 9)})
        result, _ = run_case(make_case(
            "b3-tie-cut", files, ["full-clock-timestamps"]))
        block = row_block(result.stdout, "B-3")
        self.assertIn("tied", block.lower())
        for name in ("Step 1", "Step 2", "Step 3", "Step 4"):
            self.assertIn(name, block)
        self.assertTrue("past three" in block.lower()
                        or "runs past" in block.lower(), block[:600])

    def test_b3_tie_order_is_step_universe_order(self):
        """EC-39; WV22 B-3 F5. Tied steps print in step universe order."""
        files = ranked_files({1: (10, 10), 2: (10, 10), 3: (10, 10),
                              4: (10, 10)})
        result, _ = run_case(make_case(
            "b3-tie-order", files, ["full-clock-timestamps"]))
        block = row_block(result.stdout, "B-3")
        positions = [block.find(name) for name in
                     ("Step 1", "Step 2", "Step 3", "Step 4")]
        self.assertTrue(all(p >= 0 for p in positions), block[:600])
        self.assertEqual(positions, sorted(positions))

    def test_b3_fewer_than_three_eligible_steps(self):
        """EC-39; WV22 B-3 F6. Fewer than three rankable, count as bound."""
        result, _ = run_case(make_case(
            "b3-fewer-three", base_files(steps=(1, 2)),
            ["full-clock-timestamps"]))
        block = row_block(result.stdout, "B-3")
        assert_verdict(self, block, "present", "B-3")
        self.assertIn("Step 1", block)
        self.assertIn("Step 2", block)
        self.assertRegex(block, r"eligible[^\d]*2(?!\d)(?!\.\d)")

    def test_b3_no_rankable_step_takes_verdict_from_inputs(self):
        """EC-39; WV22 B-3 F2, F6. No rankable step, no ranking stated."""
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.")
        result, _ = run_case(make_case(
            "b3-none-rankable", files, ["date-only-timestamps"]))
        assert_verdict(self, row_block(result.stdout, "B-3"),
                       "missing", "B-3")

    def test_b3_measured_zero_elapsed_ranked_without_wait_share(self):
        """EC-39; WV22 B-3 F7. Measured zero elapsed, ranked, no wait share."""
        files = ranked_files({1: (10, 8), 2: (9, 9), 3: (0, 0)})
        result, _ = run_case(make_case(
            "b3-zero-elapsed", files,
            ["full-clock-timestamps", "measured-zero"]))
        block = row_block(result.stdout, "B-3")
        assert_verdict(self, block, "present", "B-3")
        self.assertIn("Step 3", block)
        self.assertIn("zero elapsed", block.lower())
        self.assertTrue("no wait share" in block.lower(), block[:600])

    def test_b3_unreconciled_step_excluded_and_named(self):
        """EC-39; WV22 B-3 F8. Active above elapsed is unreconciled."""
        files = ranked_files({1: (10, 8), 2: (9, 9), 3: (8, 10),
                              4: (7, 7)})
        result, _ = run_case(make_case(
            "b3-unreconciled", files, ["full-clock-timestamps",
                                       "unreconciled-figure"]))
        block = row_block(result.stdout, "B-3")
        assert_verdict(self, block, "present", "B-3")
        self.assertIn("Step 3", block)
        self.assertIn("unreconciled", block.lower())
        self.assertNotIn("negative", block.lower())

    def test_b3_unreconciled_exclusion_leaves_fewer_than_three(self):
        """EC-39; WV22 B-3 F8. Exclusion bound sub limb, fewer than three.

        One unreconciled step excluded from three leaves two rankable
        steps, and the ranking counts in the fewer than three bound
        form, with the count of rankable steps as its coverage bound.
        """
        files = ranked_files({1: (10, 8), 2: (9, 9), 3: (8, 10)})
        result, _ = run_case(make_case(
            "b3-unreconciled-fewer", files,
            ["full-clock-timestamps", "unreconciled-figure"]))
        block = row_block(result.stdout, "B-3")
        assert_verdict(self, block, "present", "B-3")
        self.assertIn("Step 3", block)
        self.assertIn("unreconciled", block.lower())
        self.assertIn("fewer than three", block.lower())
        self.assertRegex(block, r"eligible[^\d]*2(?!\d)(?!\.\d)")

    def test_b3_unreconciled_exclusion_leaves_no_rankable_step(self):
        """EC-39; WV22 B-3 F8. Exclusion bound sub limb, none rankable.

        Every step unreconciled leaves no rankable step: the row
        counts under no ranking form and takes its verdict from its
        inputs, present but not derivable, with the unreconciled
        figures named as its reason.
        """
        files = ranked_files({1: (8, 10), 2: (9, 11), 3: (7, 9)})
        result, _ = run_case(make_case(
            "b3-unreconciled-none", files,
            ["full-clock-timestamps", "unreconciled-figure"]))
        block = row_block(result.stdout, "B-3")
        assert_verdict(self, block, "present but not derivable", "B-3")
        self.assertIn("unreconciled", block.lower())
        self.assertNotIn("fewer than three", block.lower())

    # B-4 ranking fields and edges, in the B-4 form.

    def test_b4_rankable_inputs_and_wait_share(self):
        """EC-40; WV22 B-4 F1, F2, F3. Active primary, elapsed beside it."""
        files = ranked_files({1: (10, 8), 2: (9, 9), 3: (8, 4)})
        result, _ = run_case(make_case(
            "b4-wait-share", files, ["full-clock-timestamps"]))
        block = row_block(result.stdout, "B-4")
        assert_verdict(self, block, "present", "B-4")
        self.assertIn("Step 1", block)
        self.assertTrue("wait" in block.lower() and "share" in block.lower(),
                        block[:500])

    def test_b4_ranking_tie_at_third_place_cut_runs_past_three(self):
        """EC-40; WV22 B-4 F4. Tie at the third place cut, in B-4 form."""
        files = ranked_files({1: (12, 12), 2: (11, 11), 3: (10, 10),
                              4: (10, 10), 5: (9, 9)})
        result, _ = run_case(make_case(
            "b4-tie-cut", files, ["full-clock-timestamps"]))
        block = row_block(result.stdout, "B-4")
        self.assertIn("tied", block.lower())
        for name in ("Step 1", "Step 2", "Step 3", "Step 4"):
            self.assertIn(name, block)
        self.assertTrue("past three" in block.lower()
                        or "runs past" in block.lower(), block[:600])

    def test_b4_tie_order_is_step_universe_order(self):
        """EC-40; WV22 B-4 F5. Tied steps print in step universe order."""
        files = ranked_files({1: (10, 10), 2: (10, 10), 3: (10, 10),
                              4: (10, 10)})
        result, _ = run_case(make_case(
            "b4-tie-order", files, ["full-clock-timestamps"]))
        block = row_block(result.stdout, "B-4")
        positions = [block.find(name) for name in
                     ("Step 1", "Step 2", "Step 3", "Step 4")]
        self.assertTrue(all(p >= 0 for p in positions), block[:600])
        self.assertEqual(positions, sorted(positions))

    def test_b4_fewer_than_three_eligible_steps(self):
        """EC-40; WV22 B-4 F6. Fewer than three rankable, in B-4 form."""
        result, _ = run_case(make_case(
            "b4-fewer-three", base_files(steps=(1, 2)),
            ["full-clock-timestamps"]))
        block = row_block(result.stdout, "B-4")
        assert_verdict(self, block, "present", "B-4")
        self.assertIn("Step 1", block)
        self.assertIn("Step 2", block)
        self.assertRegex(block, r"eligible[^\d]*2(?!\d)(?!\.\d)")

    def test_b4_no_rankable_step_takes_verdict_from_inputs(self):
        """EC-40; WV22 B-4 F2, F6. No step rankable, no ranking stated.

        The zero rankable limb of B-4 F6 and of B-4 F2: the active
        input is missing for every step, with elapsed missing on the
        same ground, so no ranking is stated and the row takes its
        verdict from its inputs under the rule at gap DG-06, which
        gives missing where every input is missing.
        """
        files = base_files()
        files["PATH-LEDGER.md"] = path_ledger(
            "Step 1 IN PROGRESS 2026-11-01, closed 2026-11-02.")
        result, _ = run_case(make_case(
            "b4-none-rankable", files, ["date-only-timestamps"]))
        block = row_block(result.stdout, "B-4")
        assert_verdict(self, block, "missing", "B-4")
        self.assertNotIn("fewer than three", block.lower())

    def test_b4_measured_zero_elapsed_no_wait_share(self):
        """EC-40; WV22 B-4 F7. Measured zero elapsed, in B-4 form."""
        files = ranked_files({1: (10, 8), 2: (9, 9), 3: (0, 0)})
        result, _ = run_case(make_case(
            "b4-zero-elapsed", files,
            ["full-clock-timestamps", "measured-zero"]))
        block = row_block(result.stdout, "B-4")
        assert_verdict(self, block, "present", "B-4")
        self.assertIn("Step 3", block)
        self.assertIn("zero elapsed", block.lower())

    def test_b4_unreconciled_step_excluded_and_named(self):
        """EC-40; WV22 B-4 F8. Active above elapsed, in B-4 form."""
        files = ranked_files({1: (10, 8), 2: (9, 9), 3: (8, 10),
                              4: (7, 7)})
        result, _ = run_case(make_case(
            "b4-unreconciled", files, ["full-clock-timestamps",
                                       "unreconciled-figure"]))
        block = row_block(result.stdout, "B-4")
        assert_verdict(self, block, "present", "B-4")
        self.assertIn("Step 3", block)
        self.assertIn("unreconciled", block.lower())

    def test_b4_unreconciled_exclusion_leaves_fewer_than_three(self):
        """EC-40; WV22 B-4 F8. Exclusion bound sub limb, fewer than three.

        In the B-4 form: one unreconciled step excluded from three
        leaves two rankable steps, and the ranking counts in the
        fewer than three bound form, with the count of rankable
        steps stated as its coverage bound.
        """
        files = ranked_files({1: (10, 8), 2: (9, 9), 3: (8, 10)})
        result, _ = run_case(make_case(
            "b4-unreconciled-fewer", files,
            ["full-clock-timestamps", "unreconciled-figure"]))
        block = row_block(result.stdout, "B-4")
        assert_verdict(self, block, "present", "B-4")
        self.assertIn("Step 3", block)
        self.assertIn("unreconciled", block.lower())
        self.assertIn("fewer than three", block.lower())
        self.assertRegex(block, r"eligible[^\d]*2(?!\d)(?!\.\d)")

    def test_b4_unreconciled_exclusion_leaves_no_rankable_step(self):
        """EC-40; WV22 B-4 F8. Exclusion bound sub limb, none rankable.

        In the B-4 form: every step unreconciled leaves no rankable
        step, the row counts under no ranking form and takes its
        verdict from its inputs, present but not derivable, with the
        unreconciled figures named as its reason.
        """
        files = ranked_files({1: (8, 10), 2: (9, 11), 3: (7, 9)})
        result, _ = run_case(make_case(
            "b4-unreconciled-none", files,
            ["full-clock-timestamps", "unreconciled-figure"]))
        block = row_block(result.stdout, "B-4")
        assert_verdict(self, block, "present but not derivable", "B-4")
        self.assertIn("unreconciled", block.lower())
        self.assertNotIn("fewer than three", block.lower())

    # Build state families F-16, F-17, F-19 and the F-18 variant.

    def test_f16_in_progress_tree_open_state_wording(self):
        """EC-02, EC-42; WV22 B-1 F2. F-16 open state naming on a B row."""
        files = base_files()
        del files["steps/step-03-gate-record.md"]
        result, _ = run_case(make_case(
            "f16-open", files, ["open-build", "full-clock-timestamps"]))
        cov = coverage_statement(result.stdout)
        self.assertIn("in progress", cov.lower())
        self.assertIn("closing ruling", cov.lower())
        self.assertRegex(cov.lower(), r"missing piece|not read|absent")
        self.assertIn("step-03", cov.lower())
        self.assertIn("captured read", result.stdout.lower())
        self.assertNotIn("halted", result.stdout.lower())
        present_named = False
        for code in ("B-1", "B-3", "B-4"):
            block = row_block(result.stdout, code)
            self.assertIn("in progress",
                          statement_segment(block).lower(), code)
            if row_verdict(block) == "present" and \
                    "in progress" in statement_segment(block).lower():
                present_named = True
        self.assertTrue(present_named,
                        "one present B row carries the open state naming")

    def test_f17_halted_tree_halt_named_and_full_rows(self):
        """EC-02, EC-42; WV22 B-1 F2. F-17 halt naming and the full 17 rows."""
        files = base_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra="This build stands halted. "
                     "The work is halted by order.")
        result, _ = run_case(make_case(
            "f17-halted", files,
            ["halt-statement-recognised", "full-clock-timestamps"]))
        self.assertEqual(result.returncode, 0, result.stderr)
        cov = coverage_statement(result.stdout)
        self.assertIn("halted", cov.lower())
        self.assertEqual(row_order(result.stdout), STARTER_ORDER)
        present_named = False
        for code in ("B-1", "B-3", "B-4"):
            block = row_block(result.stdout, code)
            self.assertTrue(block, code)
            self.assertIn("halted", statement_segment(block).lower(), code)
            if row_verdict(block) == "present" and \
                    "halted" in statement_segment(block).lower():
                present_named = True
        self.assertTrue(present_named,
                        "one present B row carries the halt naming")

    def test_f19_unrecognised_halt_wording_read_as_in_progress(self):
        """EC-02; WV22 B-1 F2. F-19 halt wording in an unrecognised piece."""
        files = base_files()
        files["notes/random-note.md"] = "Everything halted everywhere.\n"
        result, _ = run_case(make_case(
            "f19-unrecognised-piece", files, ["halt-wording-unrecognised"]))
        self.assertNotIn("halted", result.stdout.lower())
        self.assertIn("in progress", result.stdout.lower())

    def test_f19_non_naming_halt_wording_in_recognised_piece(self):
        """EC-02; WV22 B-1 F2. F-19 wording naming neither build nor work."""
        files = base_files()
        files["steps/step-02-record.md"] = step_record(
            2, extra="Everything halted everywhere.")
        result, _ = run_case(make_case(
            "f19-non-naming", files, ["halt-wording-unrecognised"]))
        self.assertNotIn("halted", result.stdout.lower())
        self.assertIn("in progress", result.stdout.lower())

    def test_f18_unknown_version_slice4_rows(self):
        """EC-03; WV22 T-1 F1, WV22 T-4 F1, WV22 D-1 F1. F-18 Slice 4 variant."""
        files = d1_files(queue_rows=[RULED_ROW])
        files["wiki/wiki/synthesis/build-metrics-record.md"] = metrics_record(
            body="Step table stands.", header_version="unknown-version-999",
            decision_table=decision_table([RULED_ROW]))
        result, _ = run_case(make_case(
            "f18-slice4", files,
            ["unknown-definitions-version", "decision-items-full-timestamps",
             "queue-file-inside-root"]))
        for code in ("T-1", "T-4", "D-1"):
            block = row_block(result.stdout, code)
            assert_verdict(self, block, "present but not derivable", code)
            self.assertIn("unknown-definitions-version", block, code)
            self.assertIn("unknown-version-999", block, code)
        assert_verdict(self, row_block(result.stdout, "T-2"),
                       "missing", "T-2")
        for code in ("B-1", "B-3", "B-4"):
            assert_verdict(self, row_block(result.stdout, code),
                           "missing", code)

    # WV2-21 cross shape equivalence for the Slice 4 habit and rows.

    def test_wv21_queue_habit_equivalent_content_same_d1_row(self):
        """EC-04, EC-08, EC-17, EC-36. Queue habit, same D-1 row both shapes.

        First shape: no queue file, the decision table governs.
        Second shape: a queue file inside the root governs over the
        same decision table, carrying the same items item for item.
        """
        root = tracked_tempdir("msc_slice4_wv21_")
        first = make_case("wv21-first-shape", d1_files(table_rows=[RULED_ROW]),
                          ["decision-table-inside-root",
                           "single-page-metrics-record"])
        second_files = d1_files(queue_rows=[RULED_ROW],
                                table_rows=[RULED_ROW])
        second = make_case("wv21-second-shape", second_files,
                           ["queue-file-inside-root",
                            "decision-table-inside-root",
                            "queue-governs-over-table",
                            "single-page-metrics-record"])
        built = build_cases([first, second], root)
        first_out = run_tool(built["wv21-first-shape"]).stdout
        second_out = run_tool(built["wv21-second-shape"]).stdout
        first_block = row_block(first_out, "D-1")
        second_block = row_block(second_out, "D-1")
        self.assertEqual(row_substance(first_out, "D-1"),
                         row_substance(second_out, "D-1"),
                         "D-1 row parts differ between shapes on "
                         "equivalent content")
        assert_median(self, first_block, 4)
        assert_median(self, second_block, 4)

    def test_wv21_time_rows_equivalent_across_queue_habit(self):
        """EC-04, EC-12, EC-24, EC-25, EC-26, EC-37, EC-39, EC-40.

        The time and decision rows of both shapes stand on the same
        path ledger substance, so their verdicts agree row by row.
        """
        root = tracked_tempdir("msc_slice4_wv21_rows_")
        first = make_case("wv21-rows-first", base_files(),
                          ["full-clock-timestamps"])
        second_files = base_files()
        second_files["DECISION-QUEUE.md"] = queue_file([RULED_ROW])
        second = make_case("wv21-rows-second", second_files,
                           ["full-clock-timestamps", "queue-file-inside-root",
                            "second-shape-habits"])
        built = build_cases([first, second], root)
        first_out = run_tool(built["wv21-rows-first"]).stdout
        second_out = run_tool(built["wv21-rows-second"]).stdout
        for code in ("T-1", "T-2", "T-4", "B-1", "B-3", "B-4"):
            self.assertEqual(
                row_substance(first_out, code),
                row_substance(second_out, code),
                "row parts differ between shapes on equivalent "
                "content: " + code)

    # The one named reread test for Slice 4, from plan Section 5.

    def test_time_family_reads_capture_only(self):
        """EC-04; WV22 T-1 F1. Named reread test, Section 5, Slice 4."""
        root = tracked_tempdir("msc_slice4_reread_")
        built = build_case(make_case("reread-time-family", base_files(),
                                     ["full-clock-timestamps"]), root)
        assert_reads_capture_only(self, built, count_reads=True)


if __name__ == "__main__":
    unittest.main()
