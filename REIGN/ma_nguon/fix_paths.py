#!/usr/bin/env python3
"""
Script to fix all resource paths from "tai_nguyen" to "../Tai_nguyen"
"""

import os
import re

def fix_paths_in_file(file_path):
    """Fix resource paths in a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace tai_nguyen with ../Tai_nguyen, but be careful about import statements
        # Don't replace in import statements or function names
        original_content = content
        
        # Replace patterns like "tai_nguyen/..." with "../Tai_nguyen/..."
        content = re.sub(r'"tai_nguyen/', r'"../Tai_nguyen/', content)
        content = re.sub(r"'tai_nguyen/", r"'../Tai_nguyen/", content)
        
        # Also fix os.path.join cases
        content = re.sub(r'os\.path\.join\("tai_nguyen"', r'os.path.join("../Tai_nguyen"', content)
        content = re.sub(r"os\.path\.join\('tai_nguyen'", r"os.path.join('../Tai_nguyen'", content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        else:
            print(f"No changes: {file_path}")
            return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix all Python files in the project"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Walk through all Python files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py') and file != 'fix_paths.py':
                file_path = os.path.join(root, file)
                fix_paths_in_file(file_path)

if __name__ == "__main__":
    main()