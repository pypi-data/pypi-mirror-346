"""Unit tests for FileManager and GitStylePatternMatcher classes."""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from codaicli.file_manager import FileManager, GitStylePatternMatcher

@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory for testing."""
    return tmp_path

@pytest.fixture
def file_manager(temp_project_dir):
    """Create a FileManager instance with a temporary project directory."""
    return FileManager(temp_project_dir)

@pytest.fixture
def pattern_matcher(temp_project_dir):
    """Create a GitStylePatternMatcher instance."""
    return GitStylePatternMatcher(temp_project_dir)

class TestGitStylePatternMatcher:
    """Tests for GitStylePatternMatcher class."""
    
    def test_empty_pattern(self, pattern_matcher):
        """Test handling of empty patterns."""
        pattern_matcher.add_pattern("")
        assert not pattern_matcher.matches("test.txt")
    
    def test_comment_pattern(self, pattern_matcher):
        """Test handling of comment patterns."""
        pattern_matcher.add_pattern("# comment")
        assert not pattern_matcher.matches("test.txt")
    
    def test_simple_pattern(self, pattern_matcher):
        """Test simple pattern matching."""
        pattern_matcher.add_pattern("*.txt")
        assert pattern_matcher.matches("test.txt")
        assert pattern_matcher.matches("dir/test.txt")
        assert not pattern_matcher.matches("test.py")
    
    def test_directory_pattern(self, pattern_matcher, temp_project_dir):
        """Test directory pattern matching."""
        pattern_matcher.add_pattern("node_modules/")
        
        # Create test directory structure
        node_modules = temp_project_dir / "node_modules"
        node_modules.mkdir()
        test_file = node_modules / "test.txt"
        test_file.touch()
        
        # Directory pattern should match both the directory and its contents
        assert pattern_matcher.matches("node_modules")  # Directory name without trailing slash
        assert pattern_matcher.matches("node_modules/test.txt")  # Files inside directory
        assert not pattern_matcher.matches("other/test.txt")
    
    def test_negation_pattern(self, pattern_matcher):
        """Test negation pattern matching."""
        pattern_matcher.add_pattern("*.txt")
        pattern_matcher.add_pattern("!important.txt")
        
        assert pattern_matcher.matches("test.txt")
        assert not pattern_matcher.matches("important.txt")
    
    def test_double_star_pattern(self, pattern_matcher):
        """Test ** pattern matching."""
        pattern_matcher.add_pattern("**/test")
        
        # **/test should match test in any directory
        assert pattern_matcher.matches("dir/test")  # Test in subdirectory
        assert pattern_matcher.matches("dir/subdir/test")  # Test in nested directory
        assert not pattern_matcher.matches("test")  # Not at root level
    
    def test_anchored_pattern(self, pattern_matcher):
        """Test patterns with leading slash."""
        pattern_matcher.add_pattern("/root.txt")
        
        assert pattern_matcher.matches("root.txt")
        assert not pattern_matcher.matches("dir/root.txt")

class TestFileManager:
    """Tests for FileManager class."""
    
    def test_init_creates_pattern_matcher(self, file_manager):
        """Test that FileManager creates a pattern matcher on init."""
        assert file_manager.pattern_matcher is not None
        assert isinstance(file_manager.pattern_matcher, GitStylePatternMatcher)
    
    def test_load_ignore_patterns_default(self, file_manager):
        """Test loading default ignore patterns."""
        # Check some default patterns
        assert file_manager._is_ignored(file_manager.project_path / ".git")  # Directory
        assert file_manager._is_ignored(file_manager.project_path / "node_modules")  # Directory
        assert file_manager._is_ignored(file_manager.project_path / "test.pyc")  # File
    
    def test_load_ignore_patterns_custom(self, temp_project_dir):
        """Test loading custom ignore patterns from .codaiignore."""
        # Create .codaiignore file
        ignore_file = temp_project_dir / ".codaiignore"
        ignore_file.write_text("custom.txt\n!important.txt")
        
        manager = FileManager(temp_project_dir)
        
        assert manager._is_ignored(temp_project_dir / "custom.txt")
        assert not manager._is_ignored(temp_project_dir / "important.txt")
    
    def test_is_ignored_large_file(self, file_manager, temp_project_dir):
        """Test that large files are ignored."""
        large_file = temp_project_dir / "large.txt"
        
        # Create a mock stat result
        mock_stat_result = MagicMock()
        mock_stat_result.st_size = 2 * 1024 * 1024  # 2MB
        mock_stat_result.st_mode = 0o100644  # Regular file mode
        
        # Mock both is_file and stat
        with patch.object(Path, "is_file", return_value=True) as mock_is_file, \
             patch.object(Path, "stat", return_value=mock_stat_result) as mock_stat:
            assert file_manager._is_ignored(large_file)
            mock_is_file.assert_called_once()
            mock_stat.assert_called_once()
    
    def test_load_files(self, file_manager, temp_project_dir):
        """Test loading files from project."""
        # Create test files
        test_py = temp_project_dir / "test.py"
        test_py.write_text("print('hello')")
        
        ignored_file = temp_project_dir / "test.pyc"
        ignored_file.write_text("binary data")
        
        files = file_manager.load_files()
        assert "test.py" in files
        assert files["test.py"] == "print('hello')"
        assert "test.pyc" not in files
    
    def test_is_binary_file(self, file_manager, temp_project_dir):
        """Test binary file detection."""
        # Create test files
        text_file = temp_project_dir / "text.txt"
        text_file.write_text("Hello, World!")
        
        binary_file = temp_project_dir / "binary"
        binary_file.write_bytes(b'\x00\x01\x02\x03')
        
        assert not file_manager._is_binary(text_file)
        assert file_manager._is_binary(binary_file)
    
    def test_apply_diff(self, file_manager, temp_project_dir):
        """Test applying diffs to files."""
        # Create original file
        test_file = temp_project_dir / "test.txt"
        test_file.write_text("line1\nline2\nline3\n")
        
        # Apply diff
        diff = """@@ -1,3 +1,4 @@
 line1
-line2
+new line
 line3
+line4"""
        
        file_manager.apply_diff("test.txt", diff)
        
        # Verify result
        result = test_file.read_text()
        assert result == "line1\nnew line\nline3\nline4"
    
    def test_create_file(self, file_manager, temp_project_dir):
        """Test creating new files."""
        file_manager.create_file("new/test.txt", "content")
        
        new_file = temp_project_dir / "new" / "test.txt"
        assert new_file.exists()
        assert new_file.read_text() == "content"
    
    def test_delete_file(self, file_manager, temp_project_dir):
        """Test deleting files."""
        # Create test file
        test_file = temp_project_dir / "test.txt"
        test_file.write_text("content")
        
        file_manager.delete_file("test.txt")
        assert not test_file.exists()
    
    def test_run_command(self, file_manager):
        """Test running shell commands."""
        # Test successful command
        result = file_manager.run_command("echo test")
        assert "test" in result
        
        # Test failed command
        result = file_manager.run_command("nonexistent_command")
        # The error message might be localized, so just check that we got some output
        assert result.strip()  # Should not be empty
        assert len(result) > 0
    
    def test_load_files_with_errors(self, file_manager, temp_project_dir):
        """Test handling of errors during file loading."""
        # Create a file that raises an error when read
        test_file = temp_project_dir / "test.txt"
        test_file.write_text("content")
        
        with patch("builtins.open") as mock_open:
            mock_open.side_effect = IOError("Test error")
            files = file_manager.load_files()
            assert not files  # Should return empty dict
    
    def test_apply_diff_new_file(self, file_manager, temp_project_dir):
        """Test applying diff to create a new file."""
        diff = """@@ -0,0 +1,2 @@
+line1
+line2"""
        
        file_manager.apply_diff("new.txt", diff)
        
        new_file = temp_project_dir / "new.txt"
        assert new_file.exists()
        assert new_file.read_text() == "line1\nline2"
    
    def test_apply_diff_complex(self, file_manager, temp_project_dir):
        """Test applying complex diffs with multiple hunks."""
        # Create original file
        test_file = temp_project_dir / "test.txt"
        test_file.write_text("1\n2\n3\n4\n5\n")
        
        # Apply complex diff
        diff = """@@ -1,3 +1,4 @@
 1
+1.5
 2
 3
@@ -3,3 +4,3 @@
 3
-4
+4.5
 5"""
        
        file_manager.apply_diff("test.txt", diff)
        
        # Verify result
        result = test_file.read_text()
        assert result == "1\n1.5\n2\n3\n4.5\n5" 