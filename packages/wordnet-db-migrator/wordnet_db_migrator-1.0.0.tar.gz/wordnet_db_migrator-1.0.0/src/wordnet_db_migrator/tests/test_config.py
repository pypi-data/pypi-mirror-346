#!/usr/bin/env python3
"""
Tests for the configuration module.

This module contains tests for the configuration handling in WordNet Porter.
"""
import os
import tempfile
from pathlib import Path
import pytest
import yaml

from wordnet_db_migrator.config import Config

@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp_file:
        config_data = {
            "databases": {
                "sqlite": {
                    "path": "/path/to/test/sqlite.db"
                },
                "postgres": {
                    "host": "test-host",
                    "port": 5433,
                    "database": "test-db",
                    "user": "test-user",
                    "password": "test-password"
                }
            },
            "output": {
                "directory": "./test-output",
                "log_level": "debug",
                "show_console_logs": True,
                "show_db_name": True
            },
            "application": {
                "batch_size": 500,
                "force_mode": True
            }
        }
        yaml.dump(config_data, temp_file)
    
    yield Path(temp_file.name)
    
    # Clean up
    os.unlink(temp_file.name)

def test_config_default_values():
    """Test that the configuration has the expected default values."""
    config = Config()
    
    # Check default values
    assert config.settings["databases"]["sqlite"]["path"] is not None
    assert config.settings["databases"]["postgres"]["host"] == "localhost"
    assert config.settings["databases"]["postgres"]["port"] == 5432
    assert config.settings["databases"]["postgres"]["database"] == "wordnet"
    assert config.settings["output"]["log_level"] == "info"
    assert config.settings["application"]["batch_size"] == 1000
    assert config.settings["application"]["force_mode"] is False

def test_config_load_from_file(temp_config_file, monkeypatch):
    """Test loading configuration from a file."""
    # Create a config instance
    config = Config()
    
    # Mock the config file path and settings
    monkeypatch.setattr(config, "user_config_file", temp_config_file)
    
    # Set initial settings
    initial_settings = {
        "databases": {
            "sqlite": {
                "path": None
            },
            "postgres": {
                "host": "localhost",
                "port": 5432,
                "database": "wordnet",
                "user": None,
                "password": None
            }
        },
        "output": {
            "directory": "./output",
            "log_level": "info",
            "show_console_logs": False,
            "show_db_name": False
        },
        "application": {
            "batch_size": 1000,
            "force_mode": False
        }
    }
    monkeypatch.setattr(config, "settings", initial_settings)
    
    # Mock the _load_config method to do nothing
    monkeypatch.setattr(config, "_load_config", lambda: None)
    
    # Manually load the configuration
    with open(temp_config_file, 'r') as f:
        user_config = yaml.safe_load(f)
        config._update_nested_dict(config.settings, user_config)
    
    # Check that the values were loaded correctly
    assert config.settings["databases"]["sqlite"]["path"] == "/path/to/test/sqlite.db"
    assert config.settings["databases"]["postgres"]["host"] == "test-host"
    assert config.settings["databases"]["postgres"]["port"] == 5433
    assert config.settings["databases"]["postgres"]["database"] == "test-db"
    assert config.settings["databases"]["postgres"]["user"] == "test-user"
    assert config.settings["databases"]["postgres"]["password"] == "test-password"
    assert config.settings["output"]["directory"] == "./test-output"
    assert config.settings["output"]["log_level"] == "debug"
    assert config.settings["output"]["show_console_logs"] is True
    assert config.settings["output"]["show_db_name"] is True
    assert config.settings["application"]["batch_size"] == 500
    assert config.settings["application"]["force_mode"] is True

def test_config_properties(monkeypatch):
    """Test the configuration properties."""
    # Create a config instance with mocked settings
    config = Config()
    
    # Use monkeypatch to set the settings directly
    test_settings = {
        "databases": {
            "sqlite": {
                "path": "/path/to/sqlite.db"
            },
            "postgres": {
                "host": "test-host",
                "port": 5433,
                "database": "test-db",
                "user": "test-user",
                "password": "test-password"
            }
        },
        "output": {
            "directory": "./test-output",
            "log_level": "debug",
            "show_console_logs": True,
            "show_db_name": True
        },
        "application": {
            "batch_size": 500,
            "force_mode": True,
            "max_login_attempts": 5
        }
    }
    monkeypatch.setattr(config, "settings", test_settings)
    
    # Test the properties
    assert config.SQLITE_PATH == "/path/to/sqlite.db"
    assert config.PG_HOST == "test-host"
    assert config.PG_PORT == 5433
    assert config.PG_DATABASE == "test-db"
    assert config.pg_user == "test-user"
    assert config.pg_password == "test-password"
    assert config.SHOW_DB_NAME is True
    assert config.SHOW_LOGGING is True
    assert config.BATCH_SIZE == 500
    assert config.force_mode is True
    assert config.MAX_LOGIN_ATTEMPTS == 5
    
    # Test setting properties
    config.SQLITE_PATH = "/new/path/to/sqlite.db"
    assert config.settings["databases"]["sqlite"]["path"] == "/new/path/to/sqlite.db"
    
    config.force_mode = False
    assert config.settings["application"]["force_mode"] is False
