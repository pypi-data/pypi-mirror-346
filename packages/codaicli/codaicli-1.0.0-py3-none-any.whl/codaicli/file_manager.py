"""File operations for CodaiCLI."""

import os
import re
import subprocess
from pathlib import Path


class GitStylePatternMatcher:
    """Handles Git-style pattern matching for .codaiignore files."""
    
    def __init__(self, base_dir):
        """Initialize with base directory."""
        self.base_dir = Path(base_dir)
        self.patterns = []
    
    def add_pattern(self, pattern, negated=False):
        """Add a pattern to the matcher."""
        # Skip empty lines and comments
        if not pattern or pattern.startswith('#'):
            return
            
        # Handle negation patterns
        if pattern.startswith('!'):
            negated = True
            pattern = pattern[1:]
        
        # Store whether this is a directory pattern
        is_dir_pattern = pattern.endswith('/')
        
        # Normalize pattern - remove trailing slash for matching
        pattern = pattern.rstrip('/')
        
        # Add to patterns list
        self.patterns.append({
            'pattern': pattern,
            'negated': negated,
            'directory_only': is_dir_pattern,
            'regex': self._compile_pattern(pattern, is_dir_pattern)
        })
    
    def _compile_pattern(self, pattern, is_dir_pattern=False):
        """Compile a Git-style pattern to regex."""
        # Handle special cases
        if pattern == '*':
            return re.compile(r'^[^/]*$')
        if pattern == '**':
            return re.compile(r'^.*$')
            
        # Escape special regex characters
        escaped = re.escape(pattern)
        
        # Convert ** to match any directory depth
        escaped = escaped.replace(r'\*\*', '.*?')
        
        # Convert * to match any character except /
        escaped = escaped.replace(r'\*', '[^/]*')
        
        # Convert ? to match any single character except /
        escaped = escaped.replace(r'\?', '[^/]')
        
        # Handle directory separator
        if '/' in escaped:
            # Pattern with / is anchored to the base directory
            if escaped.startswith('/'):
                # Leading / means match from the root of the repo
                escaped = '^' + escaped[1:] + ('$' if not is_dir_pattern else '(?:/.*)?$')
            else:
                # Without leading /, match from any directory
                escaped = '.*?' + escaped + ('$' if not is_dir_pattern else '(?:/.*)?$')
        else:
            # Pattern without / matches in any directory
            escaped = '.*?' + escaped + ('$' if not is_dir_pattern else '(?:/.*)?$')
        
        return re.compile(escaped)
    
    def matches(self, path):
        """Check if a path matches any pattern."""
        # Convert to relative path string
        if isinstance(path, Path):
            if path.is_absolute():
                rel_path = path.relative_to(self.base_dir)
            else:
                rel_path = path
            path_str = str(rel_path).replace('\\', '/')
        else:
            path_str = path.replace('\\', '/')
        
        # Remove leading ./
        if path_str.startswith('./'):
            path_str = path_str[2:]
        
        # Check all patterns
        matched = False
        
        for pattern in self.patterns:
            # For directory patterns, we need to check if the path starts with the pattern
            if pattern['directory_only']:
                if path_str == pattern['pattern'] or path_str.startswith(pattern['pattern'] + '/'):
                    matched = not pattern['negated']
                continue
            
            # Check regex match for non-directory patterns
            if pattern['regex'].search(path_str):
                matched = not pattern['negated']
        
        return matched


class FileManager:
    """Manages file operations for the project."""
    
    def __init__(self, project_path):
        """Initialize with project path."""
        self.project_path = Path(project_path)
        self.pattern_matcher = self._load_ignore_patterns()
    
    def _load_ignore_patterns(self):
        """Load ignore patterns from .codaiignore or use defaults."""
        ignore_file = self.project_path / ".codaiignore"
        pattern_matcher = GitStylePatternMatcher(self.project_path)
        
        # Add default patterns
        default_patterns = [
            ".git/",
            ".github/",
            ".venv/",
            "venv/",
            "env/",
            "node_modules/",
            "__pycache__/",
            "*.pyc",
            ".DS_Store",
            "*.jpg",
            "*.jpeg",
            "*.png",
            "*.gif",
            "*.ico",
            "*.svg",
            "*.pdf",
            "*.zip",
            "*.tar.gz",
            "*.rar",
            "*.exe",
            "*.dll",
            "*.class",
            "*.o",
            "*.so",
            "*.dylib",
            "*.jar",
            "*.war"
        ]
        
        for pattern in default_patterns:
            pattern_matcher.add_pattern(pattern)
        
        # Load custom patterns
        if ignore_file.exists():
            try:
                with open(ignore_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            pattern_matcher.add_pattern(line)
            except Exception as e:
                print(f"Warning: Error reading .codaiignore file: {e}")
        
        return pattern_matcher
    
    def _is_ignored(self, path):
        """Check if a path should be ignored."""
        # Convert to relative path
        try:
            rel_path = path.relative_to(self.project_path)
        except ValueError:
            # If path is not relative to project_path, it's not ignored
            return False
        
        # Always ignore files larger than 1MB
        if path.is_file() and path.stat().st_size > 1024 * 1024:
            return True
        
        return self.pattern_matcher.matches(rel_path)
    
    def load_files(self):
        """Load all non-ignored files from the project."""
        files = {}
        
        for root, dirs, filenames in os.walk(self.project_path):
            # Skip ignored directories to improve performance
            dirs_to_remove = []
            for i, directory in enumerate(dirs):
                dir_path = Path(root) / directory
                if self._is_ignored(dir_path):
                    dirs_to_remove.append(i)
            
            # Remove ignored directories in reverse order to avoid index issues
            for i in sorted(dirs_to_remove, reverse=True):
                del dirs[i]
            
            # Process files
            for filename in filenames:
                file_path = Path(root) / filename
                
                # Skip if file is in ignored patterns
                if self._is_ignored(file_path):
                    continue
                
                try:
                    # Skip if file is binary
                    if self._is_binary(file_path):
                        continue
                    
                    # Read file content
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    # Add to files dict with relative path
                    rel_path = str(file_path.relative_to(self.project_path))
                    files[rel_path] = content
                except Exception:
                    # Skip files that can't be read
                    continue
        
        return files
    
    def _is_binary(self, file_path):
        """Check if a file is binary."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\0' in chunk
        except Exception:
            return True
    
    def apply_diff(self, file_path, diff_content):
        """Apply unified diff to a file."""
        full_path = self.project_path / file_path
        
        # Ensure parent directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Parse diff content to get changes
        current_content = ""
        if full_path.exists():
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                current_content = f.read()
        
        # Apply the diff using proper parsing
        patch_lines = diff_content.strip().splitlines()
        result_lines = current_content.splitlines()
        
        line_position = 0
        in_hunk = False
        
        for line in patch_lines:
            # Skip file header lines
            if line.startswith('---') or line.startswith('+++'):
                continue
                
            # Parse hunk header
            if line.startswith('@@'):
                in_hunk = True
                match = re.search(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
                if match:
                    old_start = int(match.group(1))
                    old_count = int(match.group(2)) if match.group(2) else 1
                    new_start = int(match.group(3))
                    new_count = int(match.group(4)) if match.group(4) else 1
                    
                    line_position = new_start - 1  # 0-based index
                continue
            
            if not in_hunk:
                continue
                
            # Process diff lines
            if line.startswith('+'):
                # Add line
                content = line[1:]
                if line_position >= len(result_lines):
                    result_lines.append(content)
                else:
                    result_lines.insert(line_position, content)
                line_position += 1
            elif line.startswith('-'):
                # Remove line
                if 0 <= line_position < len(result_lines):
                    del result_lines[line_position]
            elif line.startswith(' '):
                # Context line
                line_position += 1
            else:
                # Unknown line type
                line_position += 1
        
        # Write back to file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(result_lines))
    
    def create_file(self, file_path, content):
        """Create a new file with content."""
        full_path = self.project_path / file_path
        
        # Ensure parent directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content to file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def delete_file(self, file_path):
        """Delete a file."""
        full_path = self.project_path / file_path
        
        if full_path.exists():
            full_path.unlink()
    
    def run_command(self, command):
        """Run a shell command and return output."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error executing command: {str(e)}"