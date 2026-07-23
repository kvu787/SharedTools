#!/usr/bin/env python3
"""Print input-latency statistics from a PresentMon CSV capture.

Uses only the Python standard library and is compatible with Python 3.14.x.
Missing PresentMon values such as "NA" are ignored, not converted to zero.
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import math
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence


METRICS = {
    "all": ("MsAllInputToPhotonLatency", "All input to photon"),
    "click": ("MsClickToPhotonLatency", "Click to photon"),
}


@dataclass(slots=True)
class MetricSamples:
    values: list[float] = field(default_factory=list)
    missing: int = 0
    rejected_negative: int = 0


@dataclass(slots=True)
class GroupSamples:
    rows: int = 0
    metrics: dict[str, MetricSamples] = field(
        default_factory=lambda: {key: MetricSamples() for key in METRICS}
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute input-latency statistics from a PresentMon CSV capture. "
            "NA/blank/non-finite values are ignored."
        )
    )
    parser.add_argument("capture", type=Path, help="PresentMon CSV file")
    parser.add_argument(
        "--metric",
        choices=("both", "all", "click"),
        default="both",
        help="latency metric to report (default: both)",
    )
    parser.add_argument(
        "--group-by",
        choices=("process", "application", "none"),
        default="process",
        help="how to group selected rows (default: process)",
    )
    parser.add_argument(
        "--application",
        metavar="GLOB",
        help='case-insensitive application filter, e.g. "game*.exe"',
    )
    parser.add_argument("--pid", type=int, help="only include this ProcessID")
    parser.add_argument(
        "--swap-chain",
        metavar="ADDRESS",
        help="only include this SwapChainAddress (case-insensitive)",
    )
    parser.add_argument(
        "--start-ms",
        type=float,
        help="include rows at or after this TimeInMs value",
    )
    parser.add_argument(
        "--end-ms",
        type=float,
        help="include rows at or before this TimeInMs value",
    )
    parser.add_argument(
        "--percentiles",
        default="50,90,95,99,99.9",
        metavar="LIST",
        help="comma-separated percentiles in [0,100] (default: 50,90,95,99,99.9)",
    )
    args = parser.parse_args(argv)

    if args.start_ms is not None and args.end_ms is not None:
        if args.start_ms > args.end_ms:
            parser.error("--start-ms cannot be greater than --end-ms")

    try:
        args.percentiles = parse_percentiles(args.percentiles)
    except ValueError as exc:
        parser.error(str(exc))

    return args


def parse_percentiles(text: str) -> list[float]:
    result: list[float] = []
    seen: set[float] = set()
    for item in text.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            value = float(item)
        except ValueError as exc:
            raise ValueError(f"invalid percentile: {item!r}") from exc
        if not math.isfinite(value) or not 0.0 <= value <= 100.0:
            raise ValueError(f"percentile must be between 0 and 100: {item!r}")
        if value not in seen:
            seen.add(value)
            result.append(value)
    if not result:
        raise ValueError("at least one percentile is required")
    return sorted(result)


def parse_finite_float(text: str | None) -> float | None:
    if text is None:
        return None
    try:
        value = float(text.strip())
    except (AttributeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def percentile(sorted_values: Sequence[float], p: float) -> float:
    """Linear interpolation, equivalent to NumPy's default percentile method."""
    if not sorted_values:
        raise ValueError("percentile requires at least one value")
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * (p / 100.0)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    fraction = position - lower
    return (
        sorted_values[lower] * (1.0 - fraction)
        + sorted_values[upper] * fraction
    )


def selected_metric_keys(choice: str) -> tuple[str, ...]:
    return tuple(METRICS) if choice == "both" else (choice,)


def group_key(row: dict[str, str], mode: str) -> str:
    application = row.get("Application", "") or "<unknown application>"
    pid = row.get("ProcessID", "") or "?"
    if mode == "none":
        return "All selected rows"
    if mode == "application":
        return application
    return f"{application} (PID {pid})"


def row_matches(row: dict[str, str], args: argparse.Namespace) -> bool:
    application = row.get("Application", "")
    if args.application and not fnmatch.fnmatch(
        application.casefold(), args.application.casefold()
    ):
        return False

    if args.pid is not None:
        try:
            if int(row.get("ProcessID", "")) != args.pid:
                return False
        except ValueError:
            return False

    if args.swap_chain:
        address = row.get("SwapChainAddress", "")
        if address.casefold() != args.swap_chain.casefold():
            return False

    time_ms = parse_finite_float(row.get("TimeInMs"))
    if args.start_ms is not None and (time_ms is None or time_ms < args.start_ms):
        return False
    if args.end_ms is not None and (time_ms is None or time_ms > args.end_ms):
        return False

    return True


def read_capture(
    path: Path, args: argparse.Namespace
) -> tuple[dict[str, GroupSamples], int, float | None, float | None]:
    metric_keys = selected_metric_keys(args.metric)
    groups: dict[str, GroupSamples] = defaultdict(GroupSamples)
    selected_rows = 0
    first_time: float | None = None
    last_time: float | None = None

    try:
        file = path.open("r", encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise RuntimeError(f"cannot open {path}: {exc}") from exc

    with file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise RuntimeError("the file has no CSV header")

        required = {"Application", "ProcessID", "TimeInMs"}
        required.update(METRICS[key][0] for key in metric_keys)
        missing_columns = sorted(required.difference(reader.fieldnames))
        if missing_columns:
            raise RuntimeError(
                "missing required PresentMon column(s): " + ", ".join(missing_columns)
            )

        for row in reader:
            # Some concatenated captures contain another header in the data.
            if row.get("Application") == "Application":
                continue
            if not row_matches(row, args):
                continue

            selected_rows += 1
            time_ms = parse_finite_float(row.get("TimeInMs"))
            if time_ms is not None:
                first_time = time_ms if first_time is None else min(first_time, time_ms)
                last_time = time_ms if last_time is None else max(last_time, time_ms)

            samples = groups[group_key(row, args.group_by)]
            samples.rows += 1
            for key in metric_keys:
                column, _ = METRICS[key]
                value = parse_finite_float(row.get(column))
                metric = samples.metrics[key]
                if value is None:
                    metric.missing += 1
                elif value < 0.0:
                    metric.rejected_negative += 1
                else:
                    metric.values.append(value)

    return dict(groups), selected_rows, first_time, last_time


def format_ms(value: float) -> str:
    return f"{value:,.4f} ms"


def format_percentile_name(p: float) -> str:
    return f"P{p:g}"


def print_metric(
    title: str,
    metric: MetricSamples,
    group_rows: int,
    percentiles: Iterable[float],
) -> None:
    values = metric.values
    valid = len(values)
    coverage = (100.0 * valid / group_rows) if group_rows else 0.0

    print(f"  {title}")
    print(f"    Valid samples : {valid:,} / {group_rows:,} ({coverage:.2f}%)")
    print(f"    Missing/NA    : {metric.missing:,}")
    if metric.rejected_negative:
        print(f"    Negative skip : {metric.rejected_negative:,}")
    if not values:
        print("    No valid samples.")
        return

    ordered = sorted(values)
    stats: list[tuple[str, float]] = [
        ("Minimum", ordered[0]),
        ("Mean", statistics.fmean(values)),
        ("Median", statistics.median(values)),
        ("Std dev (pop)", statistics.pstdev(values)),
    ]
    stats.extend(
        (format_percentile_name(p), percentile(ordered, p)) for p in percentiles
    )
    stats.append(("Maximum", ordered[-1]))

    width = max(len(name) for name, _ in stats)
    for name, value in stats:
        print(f"    {name:<{width}} : {format_ms(value)}")


def print_report(
    path: Path,
    args: argparse.Namespace,
    groups: dict[str, GroupSamples],
    selected_rows: int,
    first_time: float | None,
    last_time: float | None,
) -> None:
    print(f"PresentMon capture: {path}")
    print(f"Selected rows     : {selected_rows:,}")
    if first_time is not None and last_time is not None:
        print(f"Time range        : {first_time:,.4f} to {last_time:,.4f} ms")
        print(f"Selected duration : {(last_time - first_time) / 1000.0:,.3f} s")

    if not groups:
        print("\nNo rows matched the requested filters.")
        return

    metric_keys = selected_metric_keys(args.metric)
    for name in sorted(groups, key=str.casefold):
        group = groups[name]
        print(f"\n{name}")
        print(f"  Rows: {group.rows:,}")
        for key in metric_keys:
            _, title = METRICS[key]
            print_metric(title, group.metrics[key], group.rows, args.percentiles)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        groups, selected_rows, first_time, last_time = read_capture(
            args.capture, args
        )
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print_report(
        args.capture,
        args,
        groups,
        selected_rows,
        first_time,
        last_time,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
