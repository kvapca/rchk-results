#!/usr/bin/env bash

SCRIPT_DIR="/home/kvasa/Documents/programming/FIT/BAP_testing"
LLVM_DIR="$SCRIPT_DIR/llvm"

DEDUP="$SCRIPT_DIR/remove_duplicates.py"
SORT="$SCRIPT_DIR/sort_lines.py"
PATH_NORM="$SCRIPT_DIR/normalize_paths.py"

main() {
  # alloccheck
  python3 "$SORT" --folder "alloccheck"

  # bcheck
  python3 "$PATH_NORM" --folder "bcheck"

  # cgcheck

  # csfpcheck
  python3 "$PATH_NORM" --folder "csfpcheck"

  # errcheck
  python3 "$PATH_NORM" --folder "errcheck"

  # fficheck

  # glcheck
  python3 "$DEDUP" --folder "glcheck" --suffix ".glcheck"

  # maacheck
  python3 "$PATH_NORM" --folder "maacheck"

  # sfpcheck
  python3 "$PATH_NORM" --folder "sfpcheck"

  # symcheck
  python3 "$DEDUP" --folder "symcheck" --suffix ".symcheck"
  python3 "$SORT" --folder "symcheck"

  # ueacheck
  python3 "$PATH_NORM" --folder "ueacheck"

  # veccheck
  python3 "$DEDUP" --folder "veccheck" --suffix ".veccheck"
  python3 "$SORT" --folder "veccheck"
}

main "$@"
