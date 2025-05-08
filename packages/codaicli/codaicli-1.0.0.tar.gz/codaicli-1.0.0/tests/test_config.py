"""Unit tests for Config class."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from codaicli.config import Config

@pytest.fixture
def mock_home_dir(tmp_path):
    """Create a temporary home directory for testing."""
    with patch("pathlib.Path.home") as mock_home:
        mock_home.return_value = tmp_path
        yield tmp_path

@pytest.fixture
def config_with_mock_home(mock_home_dir):
    """Create a Config instance with mocked home directory."""
    return Config()

def test_init_creates_config_dir(mock_home_dir):
    """Test that __init__ creates the config directory if it doesn't exist."""
    config_dir = mock_home_dir / ".codaicli"
    assert not config_dir.exists()
    
    Config()
    assert config_dir.exists()
    assert config_dir.is_dir()

def test_init_uses_existing_config_dir(mock_home_dir):
    """Test that __init__ uses existing config directory."""
    config_dir = mock_home_dir / ".codaicli"
    config_dir.mkdir(parents=True)
    
    Config()
    assert config_dir.exists()
    assert config_dir.is_dir()

def test_load_config_empty_file(config_with_mock_home):
    """Test loading configuration from an empty file."""
    config_file = config_with_mock_home.config_file
    config_file.write_text("{}")
    
    config = Config()
    assert config.config == {}

def test_load_config_with_data(config_with_mock_home):
    """Test loading configuration with actual data."""
    config_file = config_with_mock_home.config_file
    test_config = {
        "openai_api_key": "test_key",
        "default_provider": "openai",
        "max_tokens": 1000
    }
    config_file.write_text(json.dumps(test_config))
    
    config = Config()
    assert config.config == test_config

def test_load_config_invalid_json(config_with_mock_home):
    """Test loading configuration with invalid JSON."""
    config_file = config_with_mock_home.config_file
    config_file.write_text("invalid json")
    
    config = Config()
    assert config.config == {}

def test_save_config(config_with_mock_home):
    """Test saving configuration to file."""
    config = config_with_mock_home
    test_config = {
        "openai_api_key": "test_key",
        "default_provider": "openai",
        "max_tokens": 1000
    }
    config.config = test_config
    config.save()
    
    # Read the file directly to verify contents
    saved_config = json.loads(config.config_file.read_text())
    assert saved_config == test_config

def test_get_existing_key(config_with_mock_home):
    """Test getting an existing configuration value."""
    config = config_with_mock_home
    config.config = {"test_key": "test_value"}
    assert config.get("test_key") == "test_value"

def test_get_missing_key(config_with_mock_home):
    """Test getting a missing configuration value."""
    config = config_with_mock_home
    assert config.get("missing_key") is None
    assert config.get("missing_key", "default") == "default"

def test_set_new_key(config_with_mock_home):
    """Test setting a new configuration value."""
    config = config_with_mock_home
    config.set("new_key", "new_value")
    assert config.config["new_key"] == "new_value"

def test_set_existing_key(config_with_mock_home):
    """Test updating an existing configuration value."""
    config = config_with_mock_home
    config.config = {"existing_key": "old_value"}
    config.set("existing_key", "new_value")
    assert config.config["existing_key"] == "new_value"

def test_save_creates_parent_dirs(mock_home_dir):
    """Test that save creates parent directories if they don't exist."""
    # Create a Config instance first to ensure the directory exists
    config = Config()
    config_dir = mock_home_dir / ".codaicli"
    
    # Remove both the config file and directory
    if config.config_file.exists():
        config.config_file.unlink()
    if config_dir.exists():
        config_dir.rmdir()
    
    # Now test that save creates the directory and file
    config.set("test_key", "test_value")
    config.save()
    
    assert config_dir.exists()
    assert config_dir.is_dir()
    assert config.config_file.exists()
    assert config.config_file.is_file()

def test_save_error_handling(config_with_mock_home):
    """Test error handling when saving fails."""
    config = config_with_mock_home
    
    # Mock open to raise an error
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = IOError("Test error")
        
        with pytest.raises(IOError):
            config.save()

def test_config_file_permissions(mock_home_dir):
    """Test that config file is created with correct permissions."""
    config = Config()
    config.set("test_key", "test_value")
    config.save()
    
    # Check that the file exists and has read/write permissions for the user
    assert config.config_file.exists()
    assert config.config_file.stat().st_mode & 0o600 == 0o600  # User read/write 