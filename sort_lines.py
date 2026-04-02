#!/usr/bin/env python3
"""
Sort lines in all files inside a folder lexicographically, while keeping duplicate lines.

Usage:
  python3 sort_lines.py --folder glcheck
"""

import os
import argparse

BASE_PATH = '/home/kvasa/Documents/programming/FIT/BAP_testing/llvm'


def parse_args():
    parser = argparse.ArgumentParser(description='Sort lines in files.')
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

def sort_lines_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_lines = f.readlines()

        sorted_lines = sorted(original_lines)

        if sorted_lines == original_lines:
            return False

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(sorted_lines)
        print(f"  Sorted: {os.path.basename(filepath)}")

        return True
    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
        return False


def main():
    args = parse_args()

    dirpath = os.path.join(BASE_PATH, args.folder)
    if not os.path.isdir(dirpath):
        print(f"Error: Folder not found: {dirpath}")
        return

    files = sorted(get_all_files(BASE_PATH, args.folder))
    print(f"Target folder: {dirpath}")
    print(f"Found {len(files)} files")
    print()

    changed_count = 0
    for filepath in files:
        if sort_lines_in_file(filepath):
            changed_count += 1

    print(f"\nFiles changed: {changed_count}/{len(files)}")

if __name__ == '__main__':
    main()
