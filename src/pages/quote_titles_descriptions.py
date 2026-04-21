#!/usr/bin/env python3
"""
Wrap title and description values in double quotes in markdown front matter.
Processes all .md files recursively from the script's directory.
"""

import re
from pathlib import Path

def quote_yaml_values(file_path):
    """Read a markdown file, wrap title and description values in quotes, and save."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match title and description lines in YAML front matter
        # Matches: title: value or description: value (with or without existing quotes)
        def add_quotes(match):
            key = match.group(1)
            value = match.group(2).strip()
            # Remove existing quotes if any
            value = value.strip('"').strip("'")
            return f'{key}: "{value}"'
        
        # Replace title and description lines within the front matter section
        modified = re.sub(
            r'^(title|description):\s*(.+?)$',
            add_quotes,
            content,
            flags=re.MULTILINE
        )
        
        if modified != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    script_dir = Path(__file__).parent
    md_files = list(script_dir.rglob('*.md'))
    
    modified_count = 0
    for md_file in md_files:
        if quote_yaml_values(md_file):
            modified_count += 1
            print(f"Updated: {md_file.name}")
    
    print(f"\nProcessed {len(md_files)} files")
    print(f"Modified {modified_count} files")

if __name__ == '__main__':
    main()
