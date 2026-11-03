#!/usr/bin/env python3
"""
Remove duplicate lines from files in a folder that are already in a reference file.

Usage:
    python3 remove_duplicates.py --folder glcheck --suffix .glcheck
"""

import os
import argparse

BASE_PATH = '/home/kvasa/Documents/programming/FIT/BAP/testing/llvm'

def parse_args():
        parser = argparse.ArgumentParser(description='Remove duplicate lines from files.')
        parser.add_argument('--folder', help='Folder under BASE_PATH to process')
        parser.add_argument('--suffix', help='Only process files ending with this suffix')
        return parser.parse_args()

def load_file_lines(filepath) -> set:
    lines = set()
    try:
        with open(filepath, 'r') as f:
            for line in f:
                lines.add(line.rstrip('\n'))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return lines

def get_all_files(base_path, folder):
    files = []
    dirpath = os.path.join(base_path, folder)
    if os.path.isdir(dirpath):
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                files.append(filepath)
    return files

def remove_duplicates_from_file(filepath, lines_to_remove):
    try:
        with open(filepath, 'r') as f:
            original_lines = f.readlines()
        
        removed_count = 0
        new_lines = []
        for line in original_lines:
            line_stripped = line.rstrip('\n')
            if line_stripped in lines_to_remove:
                removed_count += 1
            else:
                new_lines.append(line)
        
        if removed_count > 0:
            with open(filepath, 'w') as f:
                f.writelines(new_lines)
            print(f"  Removed {removed_count} lines from {os.path.basename(filepath)}")
        
        return removed_count
    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
        return 0

def main():
    args = parse_args()
    folder = args.folder
    suffix = args.suffix

    # Load reference
    reference_file = os.path.join(BASE_PATH, folder, f'R.bin{suffix}')
    
    if not os.path.exists(reference_file):
        print(f"Error: Reference file not found: {reference_file}")
        return
    
    print(f"Loading reference file: {reference_file}")
    reference_lines = load_file_lines(reference_file)
    print(f"  Found {len(reference_lines)} lines\n")
    
    # Process
    all_files = get_all_files(BASE_PATH, folder)
    files_to_process = [f for f in all_files if os.path.basename(f) != f'R.bin{suffix}']
    
    print(f"Processing {len(files_to_process)} other files...")
    print()
    
    total_removed = 0
    for filepath in sorted(files_to_process):
        removed = remove_duplicates_from_file(filepath, reference_lines)
        total_removed += removed
    
    print(f"\nTotal lines removed: {total_removed}")

if __name__ == '__main__':
    main()
