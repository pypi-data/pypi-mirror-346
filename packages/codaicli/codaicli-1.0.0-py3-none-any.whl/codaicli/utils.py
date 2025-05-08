"""Utility functions for CodaiCLI."""

import os
import re
import sys
from pathlib import Path


def get_project_name(project_path):
    """Get the name of the project from path."""
    return Path(project_path).name


def truncate_string(string, max_length=100):
    """Truncate a string to a maximum length."""
    if len(string) <= max_length:
        return string
    return string[:max_length-3] + "..."


def find_git_root(path):
    """Find the git root directory from a given path."""
    current = Path(path).absolute()
    
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    
    return None


def parse_diff(diff_text):
    """Parse a unified diff text into structured data."""
    result = {
        "file": None,
        "chunks": []
    }
    
    lines = diff_text.splitlines()
    current_chunk = None
    
    for line in lines:
        if line.startswith("---"):
            result["file"] = line[4:].strip()
        elif line.startswith("@@"):
            # Parse chunk header
            match = re.match(r"@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@", line)
            if match:
                current_chunk = {
                    "start_line": int(match.group(1)),
                    "lines": []
                }
                result["chunks"].append(current_chunk)
        elif current_chunk is not None:
            if line.startswith("+") or line.startswith("-") or line.startswith(" "):
                current_chunk["lines"].append(line)
    
    return result