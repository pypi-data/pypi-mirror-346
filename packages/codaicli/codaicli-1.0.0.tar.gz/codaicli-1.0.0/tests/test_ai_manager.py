"""Unit tests for AIManager class."""

import pytest
from unittest.mock import patch, MagicMock
from codaicli.ai_manager import AIManager

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
        "temperature": 0.7
    }

@pytest.fixture
def ai_manager(mock_config):
    """Create an AIManager instance with mock config."""
    return AIManager(mock_config)

def test_init_default_provider(mock_config):
    """Test initialization with default provider."""
    manager = AIManager(mock_config)
    assert manager.provider == "openai"
    assert manager.model == mock_config["openai_model"]
    assert manager.max_tokens == mock_config["max_tokens"]
    assert manager.temperature == mock_config["temperature"]

def test_init_custom_provider(mock_config):
    """Test initialization with custom provider."""
    manager = AIManager(mock_config, provider="gemini")
    assert manager.provider == "gemini"
    assert manager.model == mock_config["gemini_model"]

def test_init_missing_api_key(mock_config):
    """Test initialization with missing API key."""
    del mock_config["openai_api_key"]
    with pytest.raises(ValueError, match="OpenAI API key not configured"):
        AIManager(mock_config)

@patch("openai.chat.completions.create")
def test_call_openai(mock_create, ai_manager):
    """Test OpenAI API call."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
    mock_create.return_value = mock_response

    result = ai_manager._call_openai("test prompt")
    assert result == "Test response"
    mock_create.assert_called_once()

@patch("google.generativeai")
def test_call_gemini(mock_genai, mock_config):
    """Test Gemini API call."""
    # Mock the GenerativeModel class
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Test response"
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model

    # Create AIManager with Gemini provider after mocking
    ai_manager = AIManager(mock_config, provider="gemini")
    result = ai_manager._call_gemini("test prompt")
    assert result == "Test response"
    mock_genai.GenerativeModel.assert_called_once()

@patch("anthropic.Anthropic")
def test_call_claude(mock_anthropic, mock_config):
    """Test Claude API call."""
    # Mock the client and its methods
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Test response")]
    mock_client.messages.create.return_value = mock_response
    mock_anthropic.return_value = mock_client

    # Create AIManager with Claude provider after mocking
    ai_manager = AIManager(mock_config, provider="claude")
    result = ai_manager._call_claude("test prompt")
    assert result == "Test response"
    mock_client.messages.create.assert_called_once()

def test_build_prompt(ai_manager):
    """Test prompt building with files."""
    query = "test query"
    files = {
        "test.py": "print('hello')",
        "test2.py": "print('world')"
    }
    
    prompt = ai_manager._build_prompt(query, files)
    assert "test query" in prompt
    assert "test.py" in prompt
    assert "test2.py" in prompt
    assert "print('hello')" in prompt
    assert "print('world')" in prompt

def test_extract_actions(ai_manager):
    """Test extraction of actions from AI response."""
    response = """
    Here's what we need to do:
    
    ```diff
    --- test.py
    +++ test.py
    @@ -1,1 +1,2 @@
    - old line
    + new line
    ```
    
    CREATE new_file.py
    print('new file')
    
    DELETE old_file.py
    
    RUN pip install new-package
    """
    
    actions = ai_manager.extract_actions(response)
    assert len(actions) == 4
    
    # Check diff action
    diff_action = next(a for a in actions if a["type"] == "diff")
    assert diff_action["file"] == "test.py"
    assert "old line" in diff_action["diff"]
    assert "new line" in diff_action["diff"]
    
    # Check create action
    create_action = next(a for a in actions if a["type"] == "create")
    assert create_action["file"] == "new_file.py"
    assert create_action["content"] == "print('new file')"
    
    # Check delete action
    delete_action = next(a for a in actions if a["type"] == "delete")
    assert delete_action["file"] == "old_file.py"
    
    # Check run action
    run_action = next(a for a in actions if a["type"] == "run")
    assert run_action["command"] == "pip install new-package"

def test_extract_actions_error_response(ai_manager):
    """Test extraction of actions from error response."""
    response = "Error calling OpenAI API: Invalid API key"
    actions = ai_manager.extract_actions(response)
    assert len(actions) == 0

def test_set_provider(ai_manager):
    """Test changing provider."""
    assert ai_manager.set_provider("gemini")
    assert ai_manager.provider == "gemini"
    assert ai_manager.model == ai_manager.config["gemini_model"]

def test_set_provider_same_provider(ai_manager):
    """Test setting same provider."""
    original_provider = ai_manager.provider
    assert ai_manager.set_provider(original_provider)
    assert ai_manager.provider == original_provider

@patch("google.generativeai")
def test_set_provider_invalid(mock_genai, mock_config):
    """Test setting invalid provider."""
    ai_manager = AIManager(mock_config)
    original_provider = ai_manager.provider
    original_model = ai_manager.model
    
    # Test setting invalid provider
    assert not ai_manager.set_provider("invalid_provider")
    
    # Verify error message was printed
    # Note: We could capture stdout and verify the exact message if needed
    
    # Verify provider and model remain unchanged
    assert ai_manager.provider == original_provider
    assert ai_manager.model == original_model 