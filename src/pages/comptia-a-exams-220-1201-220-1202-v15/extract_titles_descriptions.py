#!/usr/bin/env python3
"""
Extract title and description from markdown files with YAML front matter.
Scans all subdirectories recursively and outputs results to a JSON file.
"""

import os
import json
import re
from pathlib import Path

def extract_front_matter(file_path):
    """Extract title and description from markdown file front matter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match YAML front matter between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None
        
        yaml_content = match.group(1)
        
        # Extract title and description using regex
        title_match = re.search(r'^title:\s*(.+)$', yaml_content, re.MULTILINE)
        desc_match = re.search(r'^description:\s*(.+)$', yaml_content, re.MULTILINE)
        
        title = title_match.group(1).strip().strip('"').strip("'") if title_match else None
        description = desc_match.group(1).strip().strip('"').strip("'") if desc_match else None
        
        return {
            'title': title,
            'description': description,
            'file': str(file_path)
        }
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # Find all .md files recursively
    md_files = list(script_dir.rglob('*.md'))
    
    results = []
    for md_file in md_files:
        data = extract_front_matter(md_file)
        if data and data['title'] and data['description']:
            results.append(data)
    
    # Sort by filename for consistent output
    results.sort(key=lambda x: x['file'])
    
    # Write to JSON file
    output_file = script_dir / 'extracted_titles_descriptions.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(results)} entries to {output_file}")
    
    # Also print a summary
    for item in results:
        print(f"\nFile: {Path(item['file']).name}")
        print(f"Title: {item['title']}")
        print(f"Description: {item['description'][:80]}...")

if __name__ == '__main__':
    main()
