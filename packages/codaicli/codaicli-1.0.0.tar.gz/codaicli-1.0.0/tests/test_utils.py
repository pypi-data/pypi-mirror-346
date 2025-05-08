"""Unit tests for utility functions."""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from codaicli.utils import (
    get_project_name,
    truncate_string,
    find_git_root,
    parse_diff
)

class TestGetProjectName:
    """Tests for get_project_name function."""
    
    def test_basic_path(self):
        """Test getting project name from basic path."""
        assert get_project_name("/path/to/project") == "project"
        assert get_project_name("project") == "project"
    
    def test_path_with_trailing_slash(self):
        """Test getting project name from path with trailing slash."""
        assert get_project_name("/path/to/project/") == "project"
    
    def test_empty_path(self):
        """Test getting project name from empty path."""
        assert get_project_name("") == ""
    
    def test_path_with_dots(self):
        """Test getting project name from path with dots."""
        assert get_project_name("/path/to/my.project") == "my.project"
        assert get_project_name("/path/to/..") == ".."
    
    def test_relative_path(self):
        """Test getting project name from relative path."""
        assert get_project_name("./project") == "project"
        assert get_project_name("../project") == "project"

class TestTruncateString:
    """Tests for truncate_string function."""
    
    def test_short_string(self):
        """Test truncating a short string."""
        assert truncate_string("hello") == "hello"
    
    def test_long_string(self):
        """Test truncating a long string."""
        long_str = "x" * 150
        result = truncate_string(long_str)
        assert len(result) == 100
        assert result.endswith("...")
    
    def test_exact_length(self):
        """Test string at exact max length."""
        exact_str = "x" * 100
        assert truncate_string(exact_str) == exact_str
    
    def test_custom_max_length(self):
        """Test truncating with custom max length."""
        assert truncate_string("hello world", max_length=5) == "he..."
    
    def test_empty_string(self):
        """Test truncating empty string."""
        assert truncate_string("") == ""

class TestFindGitRoot:
    """Tests for find_git_root function."""
    
    def test_find_git_root_success(self, tmp_path):
        """Test finding git root successfully."""
        # Create a git repository structure
        git_root = tmp_path / "project"
        git_root.mkdir()
        (git_root / ".git").mkdir()
        
        # Test from subdirectory
        subdir = git_root / "src" / "subdir"
        subdir.mkdir(parents=True)
        
        assert find_git_root(subdir) == git_root
    
    def test_find_git_root_not_found(self, tmp_path):
        """Test when git root is not found."""
        # Create a directory structure without .git
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        
        assert find_git_root(project_dir) is None
    
    def test_find_git_root_at_root(self, tmp_path):
        """Test finding git root when already at root."""
        git_root = tmp_path / "project"
        git_root.mkdir()
        (git_root / ".git").mkdir()
        
        assert find_git_root(git_root) == git_root

class TestParseDiff:
    """Tests for parse_diff function."""
    
    def test_parse_simple_diff(self):
        """Test parsing a simple diff."""
        diff = """--- a/test.py
+++ b/test.py
@@ -1,3 +1,4 @@
 line1
-line2
+new line
 line3
+line4"""
        
        result = parse_diff(diff)
        
        assert result["file"] == "a/test.py"
        assert len(result["chunks"]) == 1
        chunk = result["chunks"][0]
        assert chunk["start_line"] == 1
        assert len(chunk["lines"]) == 5  # Fixed: 5 lines total
        assert chunk["lines"] == [" line1", "-line2", "+new line", " line3", "+line4"]
    
    def test_parse_multiple_chunks(self):
        """Test parsing diff with multiple chunks."""
        diff = """--- a/test.py
+++ b/test.py
@@ -1,2 +1,3 @@
 line1
+new line
@@ -3,2 +4,3 @@
 line3
-line4
+new line4
+line5"""
        
        result = parse_diff(diff)
        
        assert result["file"] == "a/test.py"
        assert len(result["chunks"]) == 2
        assert result["chunks"][0]["start_line"] == 1
        assert result["chunks"][1]["start_line"] == 3
    
    def test_parse_empty_diff(self):
        """Test parsing empty diff."""
        result = parse_diff("")
        assert result["file"] is None
        assert result["chunks"] == []
    
    def test_parse_diff_without_chunks(self):
        """Test parsing diff without chunks."""
        diff = """--- a/test.py
+++ b/test.py"""
        
        result = parse_diff(diff)
        assert result["file"] == "a/test.py"
        assert result["chunks"] == []
    
    def test_parse_diff_with_invalid_chunk(self):
        """Test parsing diff with invalid chunk header."""
        diff = """--- a/test.py
+++ b/test.py
@@ invalid @@
line1
line2"""
        
        result = parse_diff(diff)
        assert result["file"] == "a/test.py"
        assert result["chunks"] == []
    
    def test_parse_diff_with_context_lines(self):
        """Test parsing diff with context lines."""
        diff = """--- a/test.py
+++ b/test.py
@@ -1,5 +1,6 @@
 line1
 line2
+new line
 line3
 line4
+line5"""
        
        result = parse_diff(diff)
        assert len(result["chunks"]) == 1
        chunk = result["chunks"][0]
        assert all(line.startswith(" ") or line.startswith("+") for line in chunk["lines"]) 