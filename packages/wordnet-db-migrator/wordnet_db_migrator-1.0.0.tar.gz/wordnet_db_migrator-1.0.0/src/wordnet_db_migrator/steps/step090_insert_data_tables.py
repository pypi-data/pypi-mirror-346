#!/usr/bin/env python3
# wordnet_db_migrator/steps/step090_insert_data_tables.py
"""
Step 14: Insert Data into Tables

This module handles the migration of data from SQLite to PostgreSQL.
It reads data from the SQLite database and inserts it into the corresponding
PostgreSQL tables, handling type conversions and batching for performance.
"""
import json
import logging
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Set

import psycopg2.extras
from tqdm import tqdm

from ..config import config
from ..utils.db_utils import connect_sqlite, connect_postgres, execute_query, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def list_tables() -> None:
    """
    List all loadable data tables and exit.
    
    This function reads the table order from the JSON file and prints
    a list of all tables that can be loaded with data.
    """
    logger.info("Listing available tables to insert")
    
    table_order_path = config.schemas_dir / "table_order.json"
    
    try:
        with open(table_order_path, "r", encoding="utf-8") as f:
            order = json.load(f)["table_order"]
        
        logger.info(f"Found {len(order)} tables")
        print("\n📋 Available tables to insert:")
        for name in order:
            print(f"  - {name}")
            
        sys.exit(0)
        
    except Exception as error:
        logger.exception(f"Failed to list tables: {error}")
        print(f"❌ Failed to list tables: {error}")
        sys.exit(1)

def run_single_table(table_name: str) -> bool:
    """
    Load data for a single table from SQLite to PostgreSQL.
    
    Args:
        table_name: Name of the table to load data for
        
    Returns:
        bool: True if data was successfully loaded, False otherwise
    """
    logger.info(f"Loading data for table: {table_name}")
    
    sqlite_conn = None
    pg_conn = None
    
    try:
        # Connect to SQLite
        logger.info("Connecting to SQLite database")
        sqlite_conn, error_msg = connect_sqlite()
        
        if not sqlite_conn:
            logger.error(f"Failed to connect to SQLite database: {error_msg}")
            print(f"❌ Failed to connect to SQLite database: {error_msg}")
            return False
            
        sqlite_conn.row_factory = lambda cursor, row: {
            col[0]: row[idx] for idx, col in enumerate(cursor.description)
        }
        sqlite_cursor = sqlite_conn.cursor()

        # Fetch all rows and columns
        logger.info(f"Fetching data from SQLite table: {table_name}")
        query = f"SELECT * FROM {table_name}"
        sqlite_cursor.execute(query)
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            logger.warning(f"No rows found in {table_name}")
            print(f"\n⚠️  No rows found in {table_name}")
            return True  # Not an error
        
        logger.info(f"Fetched {len(rows)} rows from {table_name}")
        
        # Get column names from the first row
        columns = rows[0].keys()
        col_names = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))

        # Get column types from SQLite PRAGMA
        logger.info(f"Getting column types for {table_name}")
        # Create a new cursor with default row factory for PRAGMA query
        pragma_cursor = sqlite_conn.cursor()
        # Reset row factory to default for this cursor
        sqlite_conn.row_factory = sqlite3.Row
        pragma_cursor.execute(f"PRAGMA table_info({table_name})")
        col_types = {row['name']: row['type'].upper() for row in pragma_cursor.fetchall()}
        pragma_cursor.close()
        # Restore the custom row factory for the main cursor
        sqlite_conn.row_factory = lambda cursor, row: {
            col[0]: row[idx] for idx, col in enumerate(cursor.description)
        }
        sqlite_cursor = sqlite_conn.cursor()
        logger.debug(f"Column types: {col_types}")

        # Define inline type-safe value converter
        def convert_value(value: Any, pg_type: str) -> Any:
            """Convert SQLite value to appropriate PostgreSQL type"""
            if pg_type == "BOOLEAN":
                return bool(value) if value is not None else None
            return value

        # Apply type conversions per row
        logger.info("Converting data types")
        data = [
            tuple(convert_value(row[col], col_types[col]) for col in columns)
            for row in rows
        ]

        # Ensure we have PostgreSQL credentials
        logger.info("Ensuring PostgreSQL credentials")
        if not config.ensure_pg_credentials():
            logger.error("PostgreSQL credentials required")
            print("❌ PostgreSQL credentials required")
            return False

        # Connect to PostgreSQL
        logger.info("Connecting to PostgreSQL database")
        pg_conn, error_msg = connect_postgres()
        
        if not pg_conn:
            logger.error(f"Failed to connect to PostgreSQL: {error_msg}")
            print(f"❌ Failed to connect to PostgreSQL: {error_msg}")
            return False
            
        pg_cursor = pg_conn.cursor()

        # Prepare insert statement
        insert_sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
        logger.debug(f"Insert SQL: {insert_sql}")

        print(f"\n✅ Inserting {len(rows)} rows into {table_name}...")

        # Progress bar tracking rows, not chunks
        progress_bar = tqdm(total=len(data), desc=table_name, unit="rows")

        # Insert data in batches
        batch_size = 1000
        for i in range(0, len(data), batch_size):
            chunk = data[i:i + batch_size]
            logger.debug(f"Inserting batch {i//batch_size + 1} ({len(chunk)} rows)")
            psycopg2.extras.execute_batch(pg_cursor, insert_sql, chunk, page_size=batch_size)
            pg_conn.commit()
            progress_bar.update(len(chunk))

        progress_bar.close()

        logger.info(f"Successfully inserted {len(rows)} rows into {table_name}")
        print(f"✅ Done with {table_name} ({len(rows)} rows)")

        return True

    except Exception as error:
        logger.exception(f"Failed to insert table {table_name}: {error}")
        print(f"❌ Failed to insert table {table_name}: {error}")
        config.success = False
        return False
        
    finally:
        # Close connections
        if 'sqlite_cursor' in locals() and sqlite_cursor:
            sqlite_cursor.close()
            
        if sqlite_conn:
            close_connection(sqlite_conn)
            logger.debug("SQLite connection closed")
            
        if 'pg_cursor' in locals() and pg_cursor:
            pg_cursor.close()
            
        if pg_conn:
            close_connection(pg_conn)
            logger.debug("PostgreSQL connection closed")

def run() -> bool:
    """
    Insert data into PostgreSQL tables from SQLite.
    
    This function handles the migration of data from SQLite to PostgreSQL.
    It can either insert data for all tables or for a specific table if
    specified via command-line arguments.
    
    Returns:
        bool: True if data was successfully inserted, False otherwise
    """
    logger.info("Starting data insertion step")
    
    # Handle --list_data_tables
    if "--list_data_tables" in sys.argv:
        logger.info("List tables mode detected")
        list_tables()
        # list_tables() will exit the program

    # Handle --insert_data_table <table>
    if "--insert_data_table" in sys.argv:
        logger.info("Single table insertion mode detected")
        try:
            idx = sys.argv.index("--insert_data_table")
            table_name = sys.argv[idx + 1]
            logger.info(f"Inserting data for table: {table_name}")
        except IndexError:
            logger.error("No table name specified after --insert_data_table")
            print("❌ Please specify a table name after --insert_data_table")
            sys.exit(1)
        
        success = run_single_table(table_name)
        if not success:
            logger.error(f"Failed to insert data for table: {table_name}")
            print(f"\n❌ Failed to insert data for table: {table_name}")
            sys.exit(1)
        return True

    # Otherwise, insert data for all tables
    logger.info("Full table migration mode detected")
    
    table_order_path = config.schemas_dir / "table_order.json"
    
    try:
        with open(table_order_path, "r", encoding="utf-8") as f:
            table_order = json.load(f)["table_order"]
        
        logger.info(f"Found {len(table_order)} tables to process")
        print(f"\n✅ Beginning full table migration ({len(table_order)} tables)")

        for table in table_order:
            logger.info(f"Processing table: {table}")
            success = run_single_table(table)
            if not success:
                logger.error(f"Aborting migration due to error in table: {table}")
                print(f"\n❌ Aborting migration due to error in table: {table}")
                sys.exit(1)

        logger.info("All tables loaded successfully")
        print("\n✅ All tables loaded successfully.")
        return True
        
    except Exception as error:
        logger.exception(f"Failed to run data insertion: {error}")
        print(f"❌ Failed to run data insertion: {error}")
        config.success = False
        return False
