#!/usr/bin/env python3
"""
Pair LLVM 14 vs LLVM 22 package benchmark CSVs, aggregate with medians,
write median_by_package.csv and summary_by_tool.csv.

Input columns (semicolon-separated): run;pkg_name;tool;time;max_rss_kb
Speedup: llvm14_median_time_s / llvm22_median_time_s (>1 means LLVM 22 faster).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import sys

# Fixed paths (same directory as this script)
_BASE = Path(__file__).resolve().parent
LLVM14_CSV = _BASE / "llvm14-packages.csv"
LLVM22_CSV = _BASE / "llvm22-packages.csv"
OUT_MEDIAN_BY_PACKAGE = _BASE / "median_by_package.csv"
OUT_SUMMARY_BY_TOOL = _BASE / "summary_by_tool.csv"

# Bootstrap
BOOTSTRAP_B = 10_000
RNG_SEED = 42

# Require at least this many runs per (pkg_name, tool) per LLVM file (median over all runs).
MIN_RUNS_PER_GROUP = 10

CSV_SEP = ";"

# loads the CSV file and checks if the expected columns are present
def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=CSV_SEP)
    expected = {"run", "pkg_name", "tool", "time", "max_rss_kb"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["time"] = pd.to_numeric(df["time"], errors="coerce")
    df["max_rss_kb"] = pd.to_numeric(df["max_rss_kb"], errors="coerce")

    # Warn and exclude invalid 'time' or 'max_rss_kb' rows
    keep_mask = df["time"].notna() & df["max_rss_kb"].notna()
    dropped = int((~keep_mask).sum())
    if dropped > 0:
        print(f"WARNING [{path.name}]: dropping {dropped} rows with non-float time or max_rss_kb", file=sys.stderr)
    df = df.loc[keep_mask].copy()
    return df

# calucates median time and median RSS for each package and tool
def summarize_one_side(df: pd.DataFrame, side_label: str) -> pd.DataFrame:
    g = df.groupby(["pkg_name", "tool"], sort=True)
    counts = g.size()
    bad = counts[counts != MIN_RUNS_PER_GROUP]
    if len(bad) > 0:
        # Keep output readable: these group counts are small in your dataset (e.g. 12 groups).
        print(
            f"WARNING [{side_label}]: {len(bad)} (pkg_name, tool) groups with run count != {MIN_RUNS_PER_GROUP}.",
            file=sys.stderr,
        )
        bad_lines = [f"  - {pkg}:{tool} -> {n}" for (pkg, tool), n in bad.items()]
        print("\n".join(bad_lines), file=sys.stderr)
    agg = (
        df.groupby(["pkg_name", "tool"], sort=True)
        .agg(
            median_time_s=("time", "median"),
            median_rss_kb=("max_rss_kb", "median"),
        )
        .reset_index()
    )
    return agg.rename(
        columns={
            "median_time_s": f"{side_label}_median_time_s",
            "median_rss_kb": f"{side_label}_median_rss_kb",
        }
    )


def main() -> None:
    rng = np.random.default_rng(RNG_SEED)

    d14 = load(LLVM14_CSV)
    d22 = load(LLVM22_CSV)
    # One row per (run, pkg, tool); sum when a package has multiple bitcodes in one run.
    collapse = lambda df: (
        df.groupby(["run", "pkg_name", "tool"], sort=True)
        .agg(time=("time", "sum"), max_rss_kb=("max_rss_kb", "max"))
        .reset_index()
    )
    d14c, d22c = collapse(d14), collapse(d22)

    s14 = summarize_one_side(d14c, "llvm14")
    s22 = summarize_one_side(d22c, "llvm22")

    merged = pd.merge(
        s14,
        s22,
        on=["pkg_name", "tool"],
        how="inner",
        validate="one_to_one",
    )

    # Calculate speedup median
    merged["speedup_median"] = (
        merged["llvm14_median_time_s"] / merged["llvm22_median_time_s"]
    )

    out_pkg = merged[
        [
            "pkg_name",
            "tool",
            "llvm14_median_time_s",
            "llvm22_median_time_s",
            "llvm14_median_rss_kb",
            "llvm22_median_rss_kb",
            "speedup_median",
        ]
    ]
    out_pkg.to_csv(OUT_MEDIAN_BY_PACKAGE, index=False, sep=CSV_SEP)

    rows = []
    for tool, grp in merged.groupby("tool", sort=True):
        rss14 = grp["llvm14_median_rss_kb"].to_numpy(dtype=float)
        rss22 = grp["llvm22_median_rss_kb"].to_numpy(dtype=float)
        n = len(grp)

        sub14 = d14c[d14c["tool"] == tool]
        sub22 = d22c[d22c["tool"] == tool]
        totals14 = sub14.groupby("run", sort=True)["time"].sum().to_numpy(dtype=float)
        totals22 = sub22.groupby("run", sort=True)["time"].sum().to_numpy(dtype=float)
        med_time14 = float(np.median(totals14))
        med_time22 = float(np.median(totals22))
        med_speed = med_time14 / med_time22
        med_r14 = float(np.median(rss14))
        med_r22 = float(np.median(rss22))

        # Bootstrap speedup from iteration totals (not per-package speedups)
        idx = rng.integers(0, len(totals14), size=(BOOTSTRAP_B, len(totals14)))
        boot_speed = np.median(totals14[idx], axis=1) / np.median(totals22[idx], axis=1)
        ci_low, ci_high = np.percentile(boot_speed, [2.5, 97.5])

        rows.append(
            {
                "tool": tool,
                "llvm14_median_time_s": med_time14,
                "llvm22_median_time_s": med_time22,
                "n_packages": n,
                "median_speedup": med_speed,
                "ci_low": float(ci_low),
                "ci_high": float(ci_high),
                "llvm14_median_rss_kb": med_r14,
                "llvm22_median_rss_kb": med_r22,
            }
        )

    summary = pd.DataFrame(rows).sort_values("tool").reset_index(drop=True)
    summary.to_csv(OUT_SUMMARY_BY_TOOL, index=False, sep=CSV_SEP)

    print(f"Wrote {OUT_MEDIAN_BY_PACKAGE} ({len(out_pkg)} rows)")
    print(f"Wrote {OUT_SUMMARY_BY_TOOL} ({len(summary)} rows)")


if __name__ == "__main__":
    main()
