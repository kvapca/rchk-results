#!/usr/bin/env python3
"""
Normalize paths inside files:

1) build paths
  /home/kvasa/Documents/programming/FIT/BAP/rchk/trunk/packages/build/dm9GnB4m/...
    becomes
  /home/kvasa/Documents/programming/FIT/BAP/rchk/trunk/packages/build/BUILD_HASH/...

2) different trunk folders
  /home/kvasa/Documents/programming/FIT/BAP/rchk/trunk22/
    becomes
  /home/kvasa/Documents/programming/FIT/BAP/rchk/trunk/

Usage:
    python3 normalize_paths.py --folder ueacheck
"""

import os
import re
import argparse

BASE_PATH = '/home/kvasa/Documents/programming/FIT/BAP_testing/llvm'
PLACEHOLDER = 'BUILD_HASH'

# (group1)trunk22(group2)
TRUNK22_PATTERN = re.compile(r'(/home/kvasa/Documents/programming/FIT/BAP/rchk/)trunk22(/)')

# (group1)(group2=hash)(group3)
# [^/]+ = matches at least one character except '/'
PATH_PATTERN = re.compile(r'(/home/kvasa/Documents/programming/FIT/BAP/rchk/trunk/packages/build/)([^/]+)(/)')

# rchk14 to rchk
RCHK14_PATTERN = re.compile(r'/home/kvasa/Documents/programming/FIT/BAP/rchk14')


def parse_args():
    parser = argparse.ArgumentParser(description='Normalize paths in files.')
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

def normalize_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_text = f.read()

        replaced_text, rchk14_count = RCHK14_PATTERN.subn(r'/home/kvasa/Documents/programming/FIT/BAP/rchk', original_text)
        replaced_text, trunk_count = TRUNK22_PATTERN.subn(r'\1trunk\2', replaced_text)
        replaced_text, hash_count = PATH_PATTERN.subn(rf'\1{PLACEHOLDER}\3', replaced_text)
        count = trunk_count + hash_count + rchk14_count

        if count == 0:
            return 0

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(replaced_text)
        print(f"  Normalized {count} path(s) in {os.path.basename(filepath)}"
        )

        return count
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
    print(f"Found {len(files)} files")

    replacements = 0
    changed_files = 0
    for filepath in files:
        count = normalize_file(filepath)
        if count > 0:
            changed_files += 1
            replacements += count

    print(f"\nFiles changed: {changed_files}/{len(files)}")
    print(f"Total path replacements: {replacements}")

if __name__ == '__main__':
    main()
