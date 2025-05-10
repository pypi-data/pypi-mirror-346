#!/usr/bin/env python3
# wordnet_db_migrator/steps/step050_extract_sqlite_metadata.py
"""
Step 7: Extract SQLite Metadata

This module extracts detailed metadata about the SQLite database tables,
including column definitions, foreign key constraints, and indexes.
The metadata is saved to a JSON file for use in later steps.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Set

from ..config import config
from ..utils.db_utils import connect_sqlite, execute_query, fetch_all, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def get_table_info(cursor: Any, table_name: str) -> List[Dict[str, Any]]:
    """
    Get column definitions for a table using PRAGMA table_info.
    
    Args:
        cursor: SQLite database cursor
        table_name: Name of the table to get info for
        
    Returns:
        List of dictionaries containing column metadata
    """
    logger.debug(f"Getting column definitions for table: {table_name}")
    
    query = f"PRAGMA table_info({table_name})"
    rows, error_msg = fetch_all(cursor, query)
    
    if not rows:
        logger.warning(f"No column definitions found for table: {table_name}")
        return []
    
    columns = []
    for row in rows:
        columns.append({
            "cid": row[0],
            "name": row[1],
            "type": row[2],
            "notnull": bool(row[3]),
            "default": row[4],
            "primary_key": bool(row[5]),
        })
    
    logger.debug(f"Found {len(columns)} columns for table: {table_name}")
    return columns

def get_foreign_keys(cursor: Any, table_name: str) -> List[Dict[str, Any]]:
    """
    Get foreign key constraints for a table using PRAGMA foreign_key_list.
    
    Args:
        cursor: SQLite database cursor
        table_name: Name of the table to get foreign keys for
        
    Returns:
        List of dictionaries containing foreign key metadata
    """
    logger.debug(f"Getting foreign key constraints for table: {table_name}")
    
    query = f"PRAGMA foreign_key_list({table_name})"
    rows, error_msg = fetch_all(cursor, query)
    
    if not rows:
        logger.debug(f"No foreign key constraints found for table: {table_name}")
        return []
    
    fkeys = []
    for row in rows:
        fkeys.append({
            "id": row[0],
            "seq": row[1],
            "table": row[2],
            "from": row[3],
            "to": row[4],
            "on_update": row[5],
            "on_delete": row[6],
            "match": row[7],
        })
    
    logger.debug(f"Found {len(fkeys)} foreign key constraints for table: {table_name}")
    return fkeys

def get_indexes(cursor: Any, table_name: str) -> List[Dict[str, Any]]:
    """
    Get index metadata for a table using PRAGMA index_list and index_info.
    
    Args:
        cursor: SQLite database cursor
        table_name: Name of the table to get indexes for
        
    Returns:
        List of dictionaries containing index metadata
    """
    logger.debug(f"Getting indexes for table: {table_name}")
    
    query = f"PRAGMA index_list({table_name})"
    rows, error_msg = fetch_all(cursor, query)
    
    if not rows:
        logger.debug(f"No indexes found for table: {table_name}")
        return []
    
    indexes = []
    for row in rows:
        index_name = row[1]
        unique = bool(row[2])

        index_info_query = f"PRAGMA index_info({index_name})"
        index_info_rows, error_msg = fetch_all(cursor, index_info_query)
        
        if not index_info_rows:
            logger.warning(f"No column information found for index: {index_name}")
            columns = []
        else:
            columns = [r[2] for r in index_info_rows]

        indexes.append({
            "name": index_name,
            "unique": unique,
            "columns": columns
        })
    
    logger.debug(f"Found {len(indexes)} indexes for table: {table_name}")
    return indexes

def run() -> bool:
    """
    Extract detailed metadata about SQLite database tables.
    
    This function reads the table order from the JSON file created in the
    previous step, connects to the SQLite database, extracts metadata about
    each table (columns, foreign keys, indexes), and saves the result to a
    JSON file.
    
    Returns:
        bool: True if metadata was successfully extracted and saved,
              False if an error occurred
    """
    logger.info("Starting SQLite metadata extraction step")
    
    table_order_path = config.schemas_dir / "table_order.json"
    output_path = config.schemas_dir / "sqlite_structure.json"

    try:
        # Read the table order from the JSON file
        logger.info(f"Reading table order from {table_order_path}")
        with open(table_order_path, "r", encoding="utf-8") as f:
            table_order = json.load(f)["table_order"]
        
        logger.info(f"Found {len(table_order)} tables to process")

        # Connect to the SQLite database
        conn, error_msg = connect_sqlite()
        if not conn:
            logger.error(f"Failed to connect to SQLite database: {error_msg}")
            print(f"❌ Failed to connect to SQLite database: {error_msg}")
            config.success = False
            return False
        
        cursor = conn.cursor()
        
        # Extract metadata for each table
        metadata = {}
        logger.info("Extracting metadata for each table")
        
        for table in table_order:
            logger.info(f"Processing table: {table}")
            
            table_meta = {
                "columns": get_table_info(cursor, table),
                "foreign_keys": get_foreign_keys(cursor, table),
                "indexes": get_indexes(cursor, table),
            }
            metadata[table] = table_meta
            
            logger.debug(f"Extracted metadata for table {table}: "
                        f"{len(table_meta['columns'])} columns, "
                        f"{len(table_meta['foreign_keys'])} foreign keys, "
                        f"{len(table_meta['indexes'])} indexes")

        # Save the metadata to a JSON file
        logger.info(f"Writing metadata to {output_path}")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        print(f"✅ SQLite metadata written to {output_path}")
        logger.info("SQLite metadata extraction completed successfully")
        return True

    except Exception as error:
        logger.exception("Failed to extract SQLite metadata")
        print(f"❌ Failed to extract SQLite metadata: {error}")
        config.success = False
        return False

    finally:
        # Clean up resources
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            close_connection(conn)
            logger.debug("SQLite connection closed")
