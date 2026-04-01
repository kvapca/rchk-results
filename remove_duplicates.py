#!/usr/bin/env python3
"""
Remove duplicate lines from glcheck files that are already in R.bin.glcheck
"""

import os
import sys
from pathlib import Path

FOLDER = 'glcheck_new'

def load_file_lines(filepath):
    """Load all lines from a file as a set"""
    lines = set()
    try:
        with open(filepath, 'r') as f:
            for line in f:
                lines.add(line.rstrip('\n'))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return lines

def get_all_glcheck_files(base_path):
    """Get all .glcheck files from FOLDER directory"""
    files = []
    dirpath = os.path.join(base_path, FOLDER)
    if os.path.isdir(dirpath):
        for filename in os.listdir(dirpath):
            if filename.endswith('.glcheck'):
                filepath = os.path.join(dirpath, filename)
                files.append(filepath)
    return files

def remove_duplicates_from_file(filepath, lines_to_remove, dry_run=False):
    """Remove lines from a file that are in lines_to_remove set"""
    if not os.path.exists(filepath):
        return 0

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
            if dry_run:
                print(f"  [DRY RUN] Would remove {removed_count} lines from {os.path.basename(filepath)}")
            else:
                with open(filepath, 'w') as f:
                    f.writelines(new_lines)
                print(f"  Removed {removed_count} lines from {os.path.basename(filepath)}")
        
        return removed_count
    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
        return 0

def main():
    base_path = '/home/kvasa/Documents/programming/FIT/BAP_testing/llvm'
    
    # Determine if dry-run mode
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    # Get the reference file (R.bin.glcheck)
    reference_file = os.path.join(base_path, FOLDER, 'R.bin.glcheck')
    
    if not os.path.exists(reference_file):
        print(f"Error: Reference file not found: {reference_file}")
        sys.exit(1)
    
    # Load reference file lines
    print(f"Loading reference file: {reference_file}")
    reference_lines = load_file_lines(reference_file)
    print(f"  Found {len(reference_lines)} lines\n")
    
    # Get all glcheck files to process
    all_files = get_all_glcheck_files(base_path)
    
    # Exclude the reference file itself
    files_to_process = [f for f in all_files if os.path.basename(f) != 'R.bin.glcheck']
    
    print(f"Processing {len(files_to_process)} other glcheck files...")
    if dry_run:
        print("(DRY RUN MODE - no changes will be made)\n")
    else:
        print()
    
    total_removed = 0
    for filepath in sorted(files_to_process):
        removed = remove_duplicates_from_file(filepath, reference_lines, dry_run)
        total_removed += removed
    
    print(f"\nTotal lines removed: {total_removed}")
    
    if dry_run:
        print("\nTo apply changes, run without --dry-run flag:")
        print(f"  python3 {sys.argv[0]}")

if __name__ == '__main__':
    main()
