"""UI components for CodaiCLI."""

import os
import re
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm
from rich.progress import Progress


class UI:
    """Manages UI components and output formatting."""
    
    def __init__(self):
        """Initialize UI components."""
        self.console = Console()
    
    def clear(self):
        """Clear the console."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self, project_path):
        """Show welcome message."""
        self.clear()
        self.console.print(Panel.fit(
            "[bold blue]CodaiCLI[/bold blue] - [italic]AI-powered CLI assistant for code projects[/italic]\n\n"
            f"Project: [green]{project_path}[/green]\n\n"
            "Type your query in natural language. For example:\n"
            "- \"What does this code do?\"\n"
            "- \"How can I optimize this function?\"\n"
            "- \"Create a new config file\"\n\n"
            "Commands:\n"
            "- [bold]use openai/gemini/claude[/bold] - Switch AI provider\n"
            "- [bold]help[/bold] - Show help\n"
            "- [bold]clear[/bold] - Clear screen\n"
            "- [bold]exit[/bold] - Exit CodaiCLI",
            title="Welcome",
            border_style="blue",
            padding=(1, 2)
        ))
    
    def show_help(self):
        """Show help information."""
        help_text = """
# CodaiCLI Help

## Commands
- `use openai/gemini/claude` - Switch AI provider
- `help` - Show this help
- `clear` - Clear screen
- `exit`, `quit`, `q` - Exit CodaiCLI

## Query Examples
- "What does this code do?"
- "How can I optimize this function?"
- "Find security vulnerabilities in my code"
- "Create a new config file"
- "Add error handling to function X"
- "Refactor this class to use dependency injection"
- "How can I improve the performance of this algorithm?"
- "Initialize a new git repository"

## Features
- AI-powered code analysis and improvements
- File creation, modification, and deletion
- Command execution (with confirmation)
- Support for multiple AI providers

## .codaiignore
CodaiCLI uses a `.codaiignore` file similar to `.gitignore` to specify files and directories to ignore.
You can create this file in your project root with patterns like:

```
# Comment
node_modules/
*.log
/dist
build/           # Trailing slash matches directories only
!important.log   # Include this file even if it matches previous patterns
```

- Lines starting with # are comments
- Blank lines are ignored
- Leading and trailing spaces are ignored
- Add ! to negate a pattern
- * matches any string except /
- ? matches any single character except /
- ** matches any number of directories
- / at the beginning matches from the repository root
- / at the end matches directories only
"""
        
        self.console.print(Markdown(help_text))
    
    def get_input(self):
        """Get user input."""
        self.console.print()
        return Prompt.ask("[bold blue]>[/bold blue]")
    
    def show_loading(self, message="Working..."):
        """Show a loading indicator."""
        return Progress()
    
    def show_response(self, response, elapsed):
        """Format and display AI response."""
        self.console.print(
            f"\n[dim]Response time: {elapsed:.2f}s[/dim]\n"
        )
        
        # Process response to highlight code blocks
        parts = re.split(r'(```[\s\S]*?```)', response)
        
        for part in parts:
            if part.startswith('```') and part.endswith('```'):
                # Code block
                language = part.split('\n')[0].replace('```', '').strip()
                code = '\n'.join(part.split('\n')[1:-1])
                
                if language == 'diff':
                    # Display diff with syntax highlighting
                    self.console.print(Syntax(code, "diff", theme="monokai"))
                else:
                    # Display other code with syntax highlighting
                    try:
                        self.console.print(Syntax(code, language or "text", theme="monokai"))
                    except Exception:
                        self.console.print(Syntax(code, "text", theme="monokai"))
            else:
                # Regular text
                if part.strip():
                    self.console.print(Markdown(part))
    
    def confirm_diff(self, file_path, diff_content):
        """Ask for confirmation to apply diff."""
        self.console.print(Panel.fit(
            f"[bold]Apply changes to:[/bold] [green]{file_path}[/green]\n\n",
            title="Confirm Changes",
            border_style="yellow"
        ))
        
        # Display the diff with syntax highlighting
        self.console.print(Syntax(diff_content, "diff", theme="monokai"))
        
        return Confirm.ask("Apply these changes?")
    
    def confirm_create(self, file_path, content):
        """Ask for confirmation to create file."""
        self.console.print(Panel.fit(
            f"[bold]Create new file:[/bold] [green]{file_path}[/green]\n\n"
            "[bold]Content:[/bold]",
            title="Confirm File Creation",
            border_style="yellow"
        ))
        
        # Try to detect language from file extension
        extension = Path(file_path).suffix.lstrip('.')
        language_map = {
            'py': 'python', 'js': 'javascript', 'ts': 'typescript',
            'html': 'html', 'css': 'css', 'json': 'json', 
            'md': 'markdown', 'txt': 'text', 'sh': 'bash'
        }
        language = language_map.get(extension, 'text')
        
        # Display the content with syntax highlighting
        self.console.print(Syntax(content, language, theme="monokai"))
        
        return Confirm.ask("Create this file?")
    
    def confirm_delete(self, file_path):
        """Ask for confirmation to delete file."""
        self.console.print(Panel.fit(
            f"[bold red]Delete file:[/bold red] [green]{file_path}[/green]",
            title="Confirm File Deletion",
            border_style="red"
        ))
        
        return Confirm.ask("Delete this file?")
    
    def confirm_run(self, command):
        """Ask for confirmation to run command."""
        self.console.print(Panel.fit(
            f"[bold]Execute command:[/bold] [green]{command}[/green]",
            title="Confirm Command Execution",
            border_style="yellow"
        ))
        
        return Confirm.ask("Execute this command?")