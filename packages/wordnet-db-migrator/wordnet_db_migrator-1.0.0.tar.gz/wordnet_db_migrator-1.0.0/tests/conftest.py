#!/usr/bin/env python3
"""
Pytest configuration for WordNet Porter tests.

This module contains fixtures and configuration for pytest.
"""
import os
import tempfile
from pathlib import Path
import pytest
import yaml

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

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

@pytest.fixture
def mock_sqlite_db(temp_dir):
    """Create a mock SQLite database file for testing."""
    db_path = temp_dir / "test.db"
    
    # Create an empty file
    db_path.touch()
    
    yield db_path
    
    # Clean up is handled by temp_dir fixture

@pytest.fixture
def mock_output_dir(temp_dir):
    """Create a mock output directory for testing."""
    output_dir = temp_dir / "output"
    output_dir.mkdir()
    
    # Create subdirectories
    (output_dir / "sql").mkdir()
    (output_dir / "logs").mkdir()
    (output_dir / "schemas").mkdir()
    (output_dir / "sql" / "tables").mkdir()
    (output_dir / "sql" / "indexes").mkdir()
    (output_dir / "sql" / "foreign_keys").mkdir()
    (output_dir / "sql" / "fk_validate").mkdir()
    
    yield output_dir
    
    # Clean up is handled by temp_dir fixture
