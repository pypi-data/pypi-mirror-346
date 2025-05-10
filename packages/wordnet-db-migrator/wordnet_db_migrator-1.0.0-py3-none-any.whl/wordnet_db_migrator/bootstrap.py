#!/usr/bin/env python3
# wordnet_db_migrator/bootstrap.py
"""
Bootstrap module for WordNet DB Migrator.

This module handles environment setup, dependency checking, and directory creation
for the WordNet DB Migrator application.
"""
import os
import sys
import sqlite3
import platform
import subprocess
import logging
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional, Union

from .config import config

# Set up logging
logger = logging.getLogger(__name__)

def check_python_version() -> Tuple[bool, str]:
    """
    Check that Python version is 3.6 or higher.
    
    Returns:
        Tuple containing:
            - Boolean indicating if Python version is sufficient
            - String with the Python version information
    """
    version_info = sys.version_info
    version_str = f"Python {version_info.major}.{version_info.minor}.{version_info.micro}"
    
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 6):
        logger.error(f"Insufficient Python version: {version_str}")
        return False, version_str
        
    logger.info(f"Python version check passed: {version_str}")
    return True, version_str

def check_dependency(module_name: str) -> bool:
    """
    Check if a Python module is installed.
    
    Args:
        module_name: Name of the module to check
        
    Returns:
        bool: True if the module is installed, False otherwise
    """
    try:
        __import__(module_name)
        logger.info(f"Dependency check passed: {module_name} is installed")
        return True
    except ImportError:
        logger.error(f"Dependency check failed: {module_name} is not installed")
        return False

def check_psql() -> Tuple[bool, Optional[str]]:
    """
    Check if PostgreSQL command-line tools are installed.
    
    Returns:
        Tuple containing:
            - Boolean indicating if psql is installed
            - String with the psql version information, or None if not installed
    """
    try:
        result = subprocess.run(
            ["psql", "--version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            logger.info(f"PostgreSQL CLI check passed: {version}")
            return True, version
        else:
            logger.warning("PostgreSQL CLI check failed: Command returned non-zero exit code")
            return False, None
            
    except FileNotFoundError:
        logger.warning("PostgreSQL CLI check failed: psql command not found")
        return False, None

def setup() -> bool:
    """
    Set up the required directory structure and validate environment.
    
    Returns:
        bool: True if setup was successful, False otherwise
    """
    logger.info("Starting environment setup")
    
    # Check Python version
    py_ok, py_version = check_python_version()
    if py_ok:
        print(f"✅ {py_version} detected")
    else:
        print(f"❌ {py_version} detected - Python 3.6 or higher is required")
        config.success = False
        return False
    
    # Check PostgreSQL Python drivers
    psycopg2_ok = check_dependency("psycopg2")
    if psycopg2_ok:
        print("✅ PostgreSQL Python driver (psycopg2) installed")
    else:
        print("❌ PostgreSQL Python driver not found")
        print("   Please run: pip install psycopg2-binary")
        config.success = False
        return False
    
    # Check PostgreSQL command-line tools
    psql_ok, psql_version = check_psql()
    if psql_ok:
        print(f"✅ PostgreSQL command-line tools installed: {psql_version}")
    else:
        print("⚠️ PostgreSQL command-line tools not found in PATH")
        print("   This is not required but may be helpful for debugging")
    
    # Check if running in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        print("✅ Running in a virtual environment")
    else:
        print("⚠️ Not running in a virtual environment")
        print("   It's recommended to use a virtual environment for this project")
    
    # Set up directories
    folders = [
        config.output_dir,
        config.sql_dir,
        config.sql_tables_dir,
        config.sql_indexes_dir,
        config.sql_foreign_keys_dir,
        config.sql_fk_validate_dir,
        config.logs_dir,
        config.schemas_dir
    ]

    print("\nCreating required directories...")
    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            logger.info(f"Created directory: {folder}")
            print(f"✅ Ensured folder exists: {folder}")
        except Exception as error:
            logger.error(f"Failed to create directory {folder}: {error}")
            print(f"❌ Failed to create folder: {folder}")
            config.success = False
            return False
    
    # Output system information
    system_info = {
        "Operating System": f"{platform.system()} {platform.release()}",
        "Python Path": sys.executable,
        "Project Directory": str(config.project_dir),
        "SQLite Database": config.SQLITE_PATH
    }
    
    logger.info(f"System information: {system_info}")
    
    print("\nSystem Information:")
    for key, value in system_info.items():
        print(f"• {key}: {value}")
    
    logger.info("Environment setup completed successfully")
    print("\n✅ Environment setup complete!")
    return True

def print_header(title: str) -> None:
    """
    Print a formatted section header.
    
    Args:
        title: The title text to display in the header
    """
    header = "\n" + "=" * 60 + f"\n{title}\n" + "=" * 60 + "\n"
    logger.info(f"Section: {title}")
    print(header)

def maybe_print_db_name(cursor_or_connection: Any) -> None:
    """
    If SHOW_DB_NAME is set, print the active connected database.
    
    Args:
        cursor_or_connection: A PostgreSQL cursor or connection object
    """
    if config.SHOW_DB_NAME:
        try:
            if hasattr(cursor_or_connection, "connection"):
                db_name = cursor_or_connection.connection.get_dsn_parameters()["dbname"]
            else:
                db_name = cursor_or_connection.get_dsn_parameters()["dbname"]
                
            logger.info(f"Connected to PostgreSQL database: {db_name}")
            print(f"🛢️  Connected to PostgreSQL database: {db_name}")
        except Exception as error:
            logger.error(f"Failed to get database name: {error}")
