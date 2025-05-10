#!/usr/bin/env python3
# wordnet_db_migrator/steps/step010_test_sqlite_connection.py
"""
Step 1: Test SQLite Database Connection

This module tests the connection to the SQLite database and gathers basic
information about the database structure.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from ..config import config
from ..utils.db_utils import connect_sqlite, execute_query, fetch_all, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def run() -> bool:
    """
    Test connection to the SQLite database and gather table information.
    
    Returns:
        bool: True if the connection test was successful, False otherwise.
    """
    logger.info("Starting SQLite connection test")
    
    # Connect to SQLite database
    conn, error_msg = connect_sqlite()
    if not conn:
        logger.error(f"Failed to connect to SQLite database: {error_msg}")
        print(f"❌ SQLite connection error: {error_msg}")
        config.success = False
        return False
    
    try:
        # Get database cursor
        cursor = conn.cursor()
        
        # Get SQLite version
        success, error_msg = execute_query(cursor, "SELECT sqlite_version()")
        if not success:
            logger.error(f"Failed to get SQLite version: {error_msg}")
            print(f"❌ Failed to get SQLite version: {error_msg}")
            config.success = False
            return False
            
        version = cursor.fetchone()[0]
        logger.info(f"SQLite version: {version}")
        
        # Get table list
        tables_query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        tables_result, error_msg = fetch_all(cursor, tables_query)
        
        if not tables_result:
            logger.error(f"Failed to get table list: {error_msg}")
            print(f"❌ Failed to get table list: {error_msg}")
            config.success = False
            return False
            
        tables = [row[0] for row in tables_result]
        logger.info(f"Found {len(tables)} tables in SQLite database")
        
        # Save result to JSON file
        result = {
            "sqlite_version": version,
            "tables_count": len(tables),
            "tables": tables,
            "path": config.SQLITE_PATH
        }
        
        output_path = config.output_dir / "sqlite_tables.json"
        try:
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
            logger.info(f"Saved SQLite database information to {output_path}")
        except Exception as error:
            logger.error(f"Failed to save SQLite database information: {error}")
            print(f"❌ Failed to save results: {error}")
            config.success = False
            return False
        
        # Print success messages
        print(f"✅ SQLite version: {version}")
        print(f"✅ Found {len(tables)} tables")
        print(f"✅ Results saved to {output_path}")
        
        return True
        
    except Exception as error:
        logger.exception("Unexpected error during SQLite connection test")
        print(f"❌ Unexpected error: {error}")
        config.success = False
        return False
    finally:
        # Always close the connection
        if conn:
            close_connection(conn)
            logger.debug("SQLite connection closed")
