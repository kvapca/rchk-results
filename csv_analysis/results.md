# How were these results processed?
Notes about result `llvm14-packages.csv` and `llvm22-packages.csv` generation are in thesis itself.

## Running
Running:
```bash
cd csv_analysis
python3 analyze_llvm_benchmarks.py
```
produces `median_by_package.csv` and `summary_by_tool.csv`.

Required packages are listed in `requirements.txt`.

### Input
Input files are semicolon-separated `llvm14-packages.csv` and `llvm22-packages.csv` with header:

```csv
run;pkg_name;tool;time;max_rss_kb
```

- `time`: wall seconds (as in GNU `time` `%e`).
- `max_rss_kb`: maximum resident set size in kB (as in GNU `time` `%M`).

## Cleaning
Rows with non-float `time` and `max_rss_kb` are dropped.
`base64enc;fficheck` has exited with error code 1 and doesn't have any values.

`processx` has two bitcode rows per `(run, pkg_name, tool)`; they are summed before aggregation.

## Per package (`median_by_package.csv`)
Rows are grouped by `(pkg_name, tool)`; median time and median RSS over runs.
Joined on groups present in both LLVM builds. Per-package speedup:
```
speedup_median = llvm14_median_time_s / llvm22_median_time_s
```

Header:
```csv
pkg_name;tool;llvm14_median_time_s;llvm22_median_time_s;llvm14_median_rss_kb;llvm22_median_rss_kb;speedup_median
```

## Per tool (`summary_by_tool.csv`)
Within each iteration, sum wall-clock time across packages for each tool and build.
`fficheck` excludes `base64enc` (29 packages; others use 30).
Reported runtime is the median of those ten iteration totals.
Tool speedup: `llvm14_median_time_s / llvm22_median_time_s` (>1 means LLVM 22 faster).

Bootstrap resamples the ten iteration totals (`BOOTSTRAP_B` times) for `ci_low` / `ci_high`.
`llvm14_median_rss_kb` and `llvm22_median_rss_kb` are the median across packages of per-package median RSS.

`summary_by_tool.csv` header:
```csv
tool;llvm14_median_time_s;llvm22_median_time_s;n_packages;median_speedup;ci_low;ci_high;llvm14_median_rss_kb;llvm22_median_rss_kb
```
