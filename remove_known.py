#!/usr/bin/env python3
"""
Remove known noisy lines from log files, e.g. BAP/LLVM abstraction overflow messages:

  ERROR: too many states (abstraction error?) in function <name>

Usage:
    python3 remove_known.py --folder glcheck
"""

import os
import re
import argparse

BASE_PATH = '/home/kvasa/Documents/programming/FIT/BAP/testing/llvm'

def parse_args():
    parser = argparse.ArgumentParser(
        description='Remove known (matched) lines from files under a folder.'
    )
    parser.add_argument('--folder', help='Folder under BASE_PATH to process')
    return parser.parse_args()


def get_all_files(base_path, folder):
    files = []
    dirpath = os.path.join(base_path, folder)
    if os.path.isdir(dirpath):
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                files.append(filepath)
    return files


def should_drop_line(line):
    line = line.strip()
    return (
        line == "ERROR: too many states (abstraction error?) in function strptime_internal"
        or line == "ERROR: too many states (abstraction error?) in function bcEval_loop"
        or line == "ERROR: too many states (abstraction error?) in function RunGenCollect"
    )

def remove_known_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_lines = f.readlines()

        removed = 0
        new_lines = []
        for line in original_lines:
            if should_drop_line(line):
                removed += 1
            else:
                new_lines.append(line)

        if removed > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(
                f"  Removed {removed} line(s) from {os.path.basename(filepath)}"
            )

        return removed
    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
        return 0


def main():
    args = parse_args()
    dirpath = os.path.join(BASE_PATH, args.folder)
    if not os.path.isdir(dirpath):
        print(f"Error: Folder not found: {dirpath}")
        return

    files = sorted(get_all_files(BASE_PATH, args.folder))
    print(f"Target folder: {dirpath}")
    print(f"Found {len(files)} files\n")

    total_removed = 0
    changed = 0
    for filepath in files:
        n = remove_known_from_file(filepath)
        if n > 0:
            changed += 1
            total_removed += n

    print(f"\nFiles changed: {changed}/{len(files)}")
    print(f"Total lines removed: {total_removed}")


if __name__ == '__main__':
    main()
