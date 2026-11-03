#!/usr/bin/env bash

SCRIPT_DIR="/home/kvasa/Documents/programming/FIT/BAP/testing"
LLVM_DIR="$SCRIPT_DIR/llvm"

DEDUP="$SCRIPT_DIR/remove_duplicates.py"
SORT="$SCRIPT_DIR/sort_lines.py"
PATH_NORM="$SCRIPT_DIR/normalize_paths.py"
REMOVE_KNOWN="$SCRIPT_DIR/remove_known.py"

main() {
  # alloccheck
  python3 "$REMOVE_KNOWN" --folder "alloccheck"
  python3 "$SORT" --folder "alloccheck"

  # bcheck
  python3 "$REMOVE_KNOWN" --folder "bcheck"
  python3 "$PATH_NORM" --folder "bcheck"

  # cgcheck
  python3 "$REMOVE_KNOWN" --folder "cgcheck"

  # csfpcheck
  python3 "$REMOVE_KNOWN" --folder "csfpcheck"
  python3 "$PATH_NORM" --folder "csfpcheck"

  # errcheck
  python3 "$REMOVE_KNOWN" --folder "errcheck"
  python3 "$PATH_NORM" --folder "errcheck"

  # fficheck
  python3 "$REMOVE_KNOWN" --folder "fficheck"

  # glcheck
  python3 "$REMOVE_KNOWN" --folder "glcheck"
  python3 "$DEDUP" --folder "glcheck" --suffix ".glcheck"

  # maacheck
  python3 "$REMOVE_KNOWN" --folder "maacheck"
  python3 "$PATH_NORM" --folder "maacheck"

  # sfpcheck
  python3 "$REMOVE_KNOWN" --folder "sfpcheck"
  python3 "$PATH_NORM" --folder "sfpcheck"

  # symcheck
  python3 "$REMOVE_KNOWN" --folder "symcheck"
  python3 "$DEDUP" --folder "symcheck" --suffix ".symcheck"
  python3 "$SORT" --folder "symcheck"

  # ueacheck
  python3 "$REMOVE_KNOWN" --folder "ueacheck"
  python3 "$PATH_NORM" --folder "ueacheck"

  # veccheck
  python3 "$REMOVE_KNOWN" --folder "veccheck"
  python3 "$DEDUP" --folder "veccheck" --suffix ".veccheck"
  python3 "$SORT" --folder "veccheck"
}

main "$@"
