"""Unit tests for CLI module."""

import os
import pytest
from unittest.mock import patch, MagicMock, call
from click.testing import CliRunner
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

from codaicli.cli import cli, configure, interactive_mode
from codaicli.config import Config
from codaicli.file_manager import FileManager
from codaicli.ai_manager import AIManager
from codaicli.ui import UI

@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()

@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    return {
        "openai_api_key": "test_openai_key",
        "gemini_api_key": "test_gemini_key",
        "claude_api_key": "test_claude_key",
        "openai_model": "gpt-4",
        "gemini_model": "gemini-pro",
        "claude_model": "claude-3-sonnet",
        "max_tokens": 1000,
        "temperature": 0.7,
        "default_provider": "openai"
    }

@pytest.fixture
def mock_file_manager():
    """Create a mock file manager."""
    manager = MagicMock(spec=FileManager)
    manager.load_files.return_value = {
        "test.py": "print('hello')",
        "test2.py": "print('world')"
    }
    return manager

@pytest.fixture
def mock_ai_manager():
    """Create a mock AI manager."""
    manager = MagicMock(spec=AIManager)
    manager.process_query.return_value = "Test response"
    manager.extract_actions.return_value = []
    manager.provider = "openai"  # Add provider attribute
    return manager

@pytest.fixture
def mock_ui():
    """Create a mock UI."""
    ui = MagicMock(spec=UI)
    ui.get_input.return_value = "test query"
    ui.console = MagicMock()  # Add console attribute
    return ui

def test_cli_version(runner):
    """Test CLI version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()

def test_cli_no_command(runner):
    """Test CLI without command (should enter interactive mode)."""
    with patch("codaicli.cli.interactive_mode") as mock_interactive:
        result = runner.invoke(cli)
        assert result.exit_code == 0
        mock_interactive.assert_called_once()

@patch("codaicli.cli.Config")
@patch("codaicli.cli.Console")
def test_configure_view(mock_console, mock_config_class, runner):
    """Test configure command with view flag."""
    mock_config = MagicMock()
    mock_config_class.return_value = mock_config
    mock_config.get.side_effect = lambda key, default=None: {
        "default_provider": "openai",
        "openai_api_key": "test_key",
        "gemini_api_key": "test_key",
        "claude_api_key": "test_key",
        "openai_model": "gpt-4",
        "gemini_model": "gemini-pro",
        "claude_model": "claude-3-sonnet",
        "max_tokens": "4000",
        "temperature": "0.2",
        "current_profile": "default"
    }.get(key, default)

    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance

    result = runner.invoke(configure, ["--view"])
    assert result.exit_code == 0
    mock_console_instance.print.assert_called()

@patch("codaicli.cli.Config")
@patch("codaicli.cli.Prompt")
def test_configure_reset(mock_prompt, mock_config_class, runner):
    """Test configure command with reset flag."""
    mock_config = MagicMock()
    mock_config_class.return_value = mock_config
    mock_prompt.ask.return_value = "y"

    result = runner.invoke(configure, ["--reset"])
    assert result.exit_code == 0
    mock_config.config = {}
    mock_config.save.assert_called_once()

@patch("codaicli.cli.Config")
@patch("codaicli.cli.Prompt")
@patch("codaicli.cli.Console")
def test_configure_api_keys(mock_console, mock_prompt, mock_config_class, runner):
    """Test API key configuration."""
    mock_config = MagicMock()
    mock_config_class.return_value = mock_config
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance
    
    # Track the number of times we've been asked for menu selection
    menu_calls = 0
    
    # Mock Prompt.ask for menu selection and confirmations
    def mock_ask(prompt, choices=None, default=None, password=False):
        nonlocal menu_calls
        
        # Handle menu selection
        if "Select an option" in prompt:
            menu_calls += 1
            if menu_calls == 1:
                return "2"  # Select API Keys
            else:
                return "5"  # Save and Exit
        
        # Handle API key configuration prompts
        if "Configure OpenAI API key" in prompt:
            return "y"
        if "Configure Google Gemini API key" in prompt:
            return "y"
        if "Configure Anthropic Claude API key" in prompt:
            return "y"
        
        # Handle API key input prompts
        if "Enter your OpenAI API key" in prompt:
            return "test_openai_key"
        if "Enter your Google AI Studio API key" in prompt:
            return "test_gemini_key"
        if "Enter your Anthropic API key" in prompt:
            return "test_claude_key"
        
        # Handle any other prompts (like exit confirmation)
        if "Are you sure" in prompt:
            return "y"
        
        return default
    
    mock_prompt.ask.side_effect = mock_ask
    
    result = runner.invoke(configure)
    assert result.exit_code == 0
    
    # Verify API keys were set
    assert mock_config.set_api_key.call_count == 3
    mock_config.set_api_key.assert_has_calls([
        call("openai", "test_openai_key"),
        call("gemini", "test_gemini_key"),
        call("claude", "test_claude_key")
    ])
    
    # Verify configuration was saved
    assert mock_config.save.call_count == 2  # Once in _configure_api_keys and once in configure

@patch("codaicli.cli.Config")
@patch("codaicli.cli.Prompt")
@patch("codaicli.cli.Console")
def test_configure_models(mock_console, mock_prompt, mock_config_class, runner):
    """Test model configuration."""
    mock_config = MagicMock()
    mock_config_class.return_value = mock_config
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance
    
    # Track the number of times we've been asked for menu selection
    menu_calls = 0
    
    # Mock Prompt.ask for menu selection and model configuration
    def mock_ask(prompt, choices=None, default=None, password=False):
        nonlocal menu_calls
        
        # Handle menu selection
        if "Select an option" in prompt:
            menu_calls += 1
            if menu_calls == 1:
                return "3"  # Select Models
            else:
                return "5"  # Save and Exit
        
        # Handle model configuration prompts
        if "Which provider's model" in prompt:
            return "openai"
        if "Enter OpenAI model name" in prompt:
            return "gpt-4"
        
        # Handle any other prompts (like exit confirmation)
        if "Are you sure" in prompt:
            return "y"
        
        return default
    
    mock_prompt.ask.side_effect = mock_ask
    
    result = runner.invoke(configure)
    assert result.exit_code == 0
    mock_config.set.assert_called_with("openai_model", "gpt-4")
    assert mock_config.save.call_count == 1  # Only called once in configure

@patch("codaicli.cli.Config")
@patch("codaicli.cli.Prompt")
@patch("codaicli.cli.Console")
def test_configure_advanced(mock_console, mock_prompt, mock_config_class, runner):
    """Test advanced settings configuration."""
    mock_config = MagicMock()
    mock_config_class.return_value = mock_config
    mock_console_instance = MagicMock()
    mock_console.return_value = mock_console_instance
    
    # Track the number of times we've been asked for menu selection
    menu_calls = 0
    
    # Mock Prompt.ask for menu selection and advanced settings
    def mock_ask(prompt, choices=None, default=None, password=False):
        nonlocal menu_calls
        
        # Handle menu selection
        if "Select an option" in prompt:
            menu_calls += 1
            if menu_calls == 1:
                return "4"  # Select Advanced Settings
            else:
                return "5"  # Save and Exit
        
        # Handle advanced settings prompts
        if "Which setting" in prompt:
            return "max_tokens"
        if "Max tokens per response" in prompt:
            return "2000"
        
        # Handle any other prompts (like exit confirmation)
        if "Are you sure" in prompt:
            return "y"
        
        return default
    
    mock_prompt.ask.side_effect = mock_ask
    
    result = runner.invoke(configure)
    assert result.exit_code == 0
    mock_config.set.assert_called_with("max_tokens", 2000)
    assert mock_config.save.call_count == 1  # Only called once in configure

@patch("codaicli.cli.Config")
@patch("codaicli.cli.FileManager")
@patch("codaicli.cli.AIManager")
@patch("codaicli.cli.UI")
@patch("codaicli.cli.Progress")
def test_interactive_mode_exit(mock_progress, mock_ui_class, mock_ai_manager_class, mock_file_manager_class, mock_config_class, mock_config):
    """Test interactive mode exit command."""
    mock_ui = MagicMock(spec=UI)
    mock_ui_class.return_value = mock_ui
    mock_ui.get_input.return_value = "exit"
    mock_ui.console = MagicMock()
    
    mock_progress_instance = MagicMock()
    mock_progress.return_value.__enter__.return_value = mock_progress_instance

    interactive_mode()
    mock_ui.get_input.assert_called_once()

@patch("codaicli.cli.Config")
@patch("codaicli.cli.FileManager")
@patch("codaicli.cli.AIManager")
@patch("codaicli.cli.UI")
@patch("codaicli.cli.Progress")
def test_interactive_mode_help(mock_progress, mock_ui_class, mock_ai_manager_class, mock_file_manager_class, mock_config_class, mock_config):
    """Test interactive mode help command."""
    mock_ui = MagicMock(spec=UI)
    mock_ui_class.return_value = mock_ui
    mock_ui.get_input.side_effect = ["help", "exit"]
    mock_ui.console = MagicMock()
    
    mock_progress_instance = MagicMock()
    mock_progress.return_value.__enter__.return_value = mock_progress_instance

    interactive_mode()
    assert mock_ui.show_help.call_count == 1

@patch("codaicli.cli.Config")
@patch("codaicli.cli.FileManager")
@patch("codaicli.cli.AIManager")
@patch("codaicli.cli.UI")
@patch("codaicli.cli.Progress")
def test_interactive_mode_use_provider(mock_progress, mock_ui_class, mock_ai_manager_class, mock_file_manager_class, mock_config_class, mock_config):
    """Test interactive mode use provider command."""
    mock_ui = MagicMock(spec=UI)
    mock_ui_class.return_value = mock_ui
    mock_ui.get_input.side_effect = ["use gemini", "exit"]
    mock_ui.console = MagicMock()
    
    mock_ai_manager = MagicMock(spec=AIManager)
    mock_ai_manager_class.return_value = mock_ai_manager
    mock_ai_manager.set_provider.return_value = True
    mock_ai_manager.provider = "openai"
    
    mock_progress_instance = MagicMock()
    mock_progress.return_value.__enter__.return_value = mock_progress_instance

    interactive_mode()
    mock_ai_manager.set_provider.assert_called_with("gemini")

@patch("codaicli.cli.Config")
@patch("codaicli.cli.FileManager")
@patch("codaicli.cli.AIManager")
@patch("codaicli.cli.UI")
@patch("codaicli.cli.Progress")
def test_interactive_mode_query(mock_progress, mock_ui_class, mock_ai_manager_class, mock_file_manager_class, mock_config_class, mock_config):
    """Test interactive mode query processing."""
    mock_ui = MagicMock(spec=UI)
    mock_ui_class.return_value = mock_ui
    mock_ui.get_input.side_effect = ["test query", "exit"]
    mock_ui.console = MagicMock()
    
    mock_ai_manager = MagicMock(spec=AIManager)
    mock_ai_manager_class.return_value = mock_ai_manager
    mock_ai_manager.process_query.return_value = "Test response"
    mock_ai_manager.extract_actions.return_value = []
    mock_ai_manager.provider = "openai"
    
    mock_progress_instance = MagicMock()
    mock_progress.return_value.__enter__.return_value = mock_progress_instance

    interactive_mode()
    mock_ai_manager.process_query.assert_called_once()
    mock_ui.show_response.assert_called_once()

@patch("codaicli.cli.Config")
@patch("codaicli.cli.FileManager")
@patch("codaicli.cli.AIManager")
@patch("codaicli.cli.UI")
@patch("codaicli.cli.Progress")
def test_interactive_mode_diff_action(mock_progress, mock_ui_class, mock_ai_manager_class, mock_file_manager_class, mock_config_class, mock_config):
    """Test interactive mode diff action."""
    mock_ui = MagicMock(spec=UI)
    mock_ui_class.return_value = mock_ui
    mock_ui.get_input.side_effect = ["test query", "exit"]
    mock_ui.confirm_diff.return_value = True
    mock_ui.console = MagicMock()
    
    mock_file_manager = MagicMock(spec=FileManager)
    mock_file_manager_class.return_value = mock_file_manager
    
    mock_ai_manager = MagicMock(spec=AIManager)
    mock_ai_manager_class.return_value = mock_ai_manager
    mock_ai_manager.process_query.return_value = "Test response"
    mock_ai_manager.extract_actions.return_value = [{
        "type": "diff",
        "file": "test.py",
        "diff": "test diff"
    }]
    mock_ai_manager.provider = "openai"
    
    mock_progress_instance = MagicMock()
    mock_progress.return_value.__enter__.return_value = mock_progress_instance

    interactive_mode()
    mock_file_manager.apply_diff.assert_called_once_with("test.py", "test diff")

@patch("codaicli.cli.Config")
@patch("codaicli.cli.FileManager")
@patch("codaicli.cli.AIManager")
@patch("codaicli.cli.UI")
@patch("codaicli.cli.Progress")
def test_interactive_mode_create_action(mock_progress, mock_ui_class, mock_ai_manager_class, mock_file_manager_class, mock_config_class, mock_config):
    """Test interactive mode create action."""
    mock_ui = MagicMock(spec=UI)
    mock_ui_class.return_value = mock_ui
    mock_ui.get_input.side_effect = ["test query", "exit"]
    mock_ui.confirm_create.return_value = True
    mock_ui.console = MagicMock()
    
    mock_file_manager = MagicMock(spec=FileManager)
    mock_file_manager_class.return_value = mock_file_manager
    
    mock_ai_manager = MagicMock(spec=AIManager)
    mock_ai_manager_class.return_value = mock_ai_manager
    mock_ai_manager.process_query.return_value = "Test response"
    mock_ai_manager.extract_actions.return_value = [{
        "type": "create",
        "file": "new.py",
        "content": "print('new')"
    }]
    mock_ai_manager.provider = "openai"
    
    mock_progress_instance = MagicMock()
    mock_progress.return_value.__enter__.return_value = mock_progress_instance

    interactive_mode()
    mock_file_manager.create_file.assert_called_once_with("new.py", "print('new')")

@patch("codaicli.cli.Config")
@patch("codaicli.cli.FileManager")
@patch("codaicli.cli.AIManager")
@patch("codaicli.cli.UI")
@patch("codaicli.cli.Progress")
def test_interactive_mode_delete_action(mock_progress, mock_ui_class, mock_ai_manager_class, mock_file_manager_class, mock_config_class, mock_config):
    """Test interactive mode delete action."""
    mock_ui = MagicMock(spec=UI)
    mock_ui_class.return_value = mock_ui
    mock_ui.get_input.side_effect = ["test query", "exit"]
    mock_ui.confirm_delete.return_value = True
    mock_ui.console = MagicMock()
    
    mock_file_manager = MagicMock(spec=FileManager)
    mock_file_manager_class.return_value = mock_file_manager
    
    mock_ai_manager = MagicMock(spec=AIManager)
    mock_ai_manager_class.return_value = mock_ai_manager
    mock_ai_manager.process_query.return_value = "Test response"
    mock_ai_manager.extract_actions.return_value = [{
        "type": "delete",
        "file": "old.py"
    }]
    mock_ai_manager.provider = "openai"
    
    mock_progress_instance = MagicMock()
    mock_progress.return_value.__enter__.return_value = mock_progress_instance

    interactive_mode()
    mock_file_manager.delete_file.assert_called_once_with("old.py")

@patch("codaicli.cli.Config")
@patch("codaicli.cli.FileManager")
@patch("codaicli.cli.AIManager")
@patch("codaicli.cli.UI")
@patch("codaicli.cli.Progress")
def test_interactive_mode_run_action(mock_progress, mock_ui_class, mock_ai_manager_class, mock_file_manager_class, mock_config_class, mock_config):
    """Test interactive mode run action."""
    mock_ui = MagicMock(spec=UI)
    mock_ui_class.return_value = mock_ui
    mock_ui.get_input.side_effect = ["test query", "exit"]
    mock_ui.confirm_run.return_value = True
    mock_ui.console = MagicMock()
    
    mock_file_manager = MagicMock(spec=FileManager)
    mock_file_manager_class.return_value = mock_file_manager
    mock_file_manager.run_command.return_value = "Command output"
    
    mock_ai_manager = MagicMock(spec=AIManager)
    mock_ai_manager_class.return_value = mock_ai_manager
    mock_ai_manager.process_query.return_value = "Test response"
    mock_ai_manager.extract_actions.return_value = [{
        "type": "run",
        "command": "pip install test"
    }]
    mock_ai_manager.provider = "openai"
    
    mock_progress_instance = MagicMock()
    mock_progress.return_value.__enter__.return_value = mock_progress_instance

    interactive_mode()
    mock_file_manager.run_command.assert_called_once_with("pip install test")
    mock_ui.console.print.assert_any_call("Command output") 