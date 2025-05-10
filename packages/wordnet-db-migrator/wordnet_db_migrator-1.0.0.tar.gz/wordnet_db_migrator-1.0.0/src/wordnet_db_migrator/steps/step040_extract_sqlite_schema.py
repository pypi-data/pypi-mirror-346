#!/usr/bin/env python3
# wordnet_db_migrator/steps/step040_extract_sqlite_schema.py
"""
Step 5: Extract SQLite Schema

This module extracts the CREATE TABLE statements from the SQLite database
and saves them to a file for later analysis and conversion to PostgreSQL.
"""
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from ..config import config
from ..utils.db_utils import connect_sqlite, execute_query, fetch_all, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def extract_table_schemas() -> Tuple[Optional[List[Tuple[str, str]]], str]:
    """
    Extract CREATE TABLE statements from SQLite database.
    
    Returns:
        Tuple containing:
            - List of tuples (table_name, create_statement) or None if extraction failed
            - Error message if extraction failed, empty string otherwise
    """
    logger.info("Extracting table schemas from SQLite database")
    
    # Connect to SQLite database
    conn, error_msg = connect_sqlite()
    if not conn:
        logger.error(f"Failed to connect to SQLite database: {error_msg}")
        return None, error_msg
    
    try:
        cursor = conn.cursor()
        
        # Query to get table schemas
        query = """
            SELECT name, sql FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
        """
        
        tables_result, error_msg = fetch_all(cursor, query)
        
        if not tables_result:
            if error_msg:
                logger.error(f"Failed to fetch table schemas: {error_msg}")
                return None, f"Failed to fetch table schemas: {error_msg}"
            else:
                logger.warning("No tables found in the SQLite database")
                return None, "No tables found in the SQLite database"
        
        logger.info(f"Successfully extracted {len(tables_result)} table schemas")
        return tables_result, ""
        
    except Exception as error:
        error_msg = f"Unexpected error extracting table schemas: {error}"
        logger.exception(error_msg)
        return None, error_msg
    finally:
        if conn:
            close_connection(conn)
            logger.debug("SQLite connection closed")

def save_schemas_to_file(tables: List[Tuple[str, str]]) -> Tuple[bool, str]:
    """
    Save extracted table schemas to a file.
    
    Args:
        tables: List of tuples (table_name, create_statement)
        
    Returns:
        Tuple containing:
            - Boolean indicating success or failure
            - Error message if failed, empty string otherwise
    """
    logger.info("Saving table schemas to file")
    
    output_file = config.schemas_dir / "sqlite_schema.sql"
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for name, ddl in tables:
                f.write(f"-- Table: {name} --\n")
                f.write(f"{ddl.strip()};\n\n")
        
        logger.info(f"Successfully saved table schemas to {output_file}")
        return True, ""
    except Exception as error:
        error_msg = f"Failed to save schemas to file: {error}"
        logger.error(error_msg)
        return False, error_msg

def run() -> bool:
    """
    Extract CREATE TABLE statements from SQLite and save to file.
    
    This function connects to the SQLite database, extracts the CREATE TABLE
    statements for all tables, and saves them to a file for later analysis.
    
    Returns:
        bool: True if schemas were successfully extracted and saved,
              False if an error occurred
    """
    logger.info("Starting SQLite schema extraction step")
    
    print("✅ Connecting to SQLite database...")
    
    # Extract table schemas
    tables, error_msg = extract_table_schemas()
    
    if not tables:
        print(f"❌ {error_msg}")
        config.success = False
        return False
    
    print(f"✅ Fetched {len(tables)} table schemas...")
    
    # Save schemas to file
    success, error_msg = save_schemas_to_file(tables)
    
    if not success:
        print(f"❌ {error_msg}")
        config.success = False
        return False
    
    output_file = config.schemas_dir / "sqlite_schema.sql"
    print(f"✅ Extracted {len(tables)} table schemas")
    print(f"✅ Saved to {output_file}")
    
    logger.info("SQLite schema extraction completed successfully")
    return True
