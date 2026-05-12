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

The tool also warns about rows with too many runs per (`pkg_name`, `tool`) group.
`processx` package has 20 runs per (`pkg_name`, `tool`) group because it has 2 different bitcode files.


## Medians
Rows are grouped by `(pkg_name, tool)`.
Median time and median RSS are calculated over all runs in that group.
Results are then joined on group.
Only pairs present in **both** runs get a row in `median_by_package.csv`.
Speedup median is calculated as:
```
speedup_median = llvm14_median_time_s / llvm22_median_time_s
```

Header of `median_by_package.csv`:
```csv
pkg_name;tool;llvm14_median_time_s;llvm22_median_time_s;llvm14_median_rss_kb;llvm22_median_rss_kb;speedup_median
```

## Median bootstrapping
Bootstrapping is done by resampling `speedup_median` with replacement `BOOTSTRAP_B` times.
This is done to get a confidence interval for the median speedup (`ci_low` and `ci_high`).
`n_packages` is the number of packages available for bootstrapping (fficheck has 29, the rest 30).
`llvm14_median_rss_kb` and `llvm22_median_rss_kb` are the median across packages of the per-package median RSS columns (median of package-level medians).

`summary_by_tool.csv` header:
```csv
tool;n_packages;median_speedup;ci_low;ci_high;llvm14_median_rss_kb;llvm22_median_rss_kb
```
