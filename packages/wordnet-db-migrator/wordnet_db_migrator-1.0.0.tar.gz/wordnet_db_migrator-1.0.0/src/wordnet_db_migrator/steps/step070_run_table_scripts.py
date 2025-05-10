#!/usr/bin/env python3
# wordnet_db_migrator/steps/step070_run_table_scripts.py
"""
Step 12: Run Table Creation Scripts

This module executes the PostgreSQL CREATE TABLE scripts generated in a previous
step. It follows the dependency order determined by the topological sort and
handles existing tables by either dropping them or skipping them based on user
input.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Set

from ..config import config
from ..utils.db_utils import connect_postgres, execute_query, execute_sql_file, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def table_exists(cursor: Any, table_name: str) -> bool:
    """
    Check if a given table exists in PostgreSQL (case-insensitive).
    
    Args:
        cursor: PostgreSQL database cursor
        table_name: Name of the table to check
        
    Returns:
        bool: True if the table exists, False otherwise
    """
    logger.debug(f"Checking if table exists: {table_name}")
    
    lower_name = table_name.lower()
    query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = %s
        )
    """
    
    success, error_msg = execute_query(cursor, query, (lower_name,))
    
    if not success:
        logger.error(f"Failed to check if table exists: {error_msg}")
        return False
    
    result = cursor.fetchone()[0]
    logger.debug(f"Table {lower_name} exists: {result}")
    print(f"🔍 CHECK: {lower_name} → {result}")
    return result

def run() -> bool:
    """
    Execute all CREATE TABLE scripts based on dependency order.
    
    This function connects to the PostgreSQL database, checks for existing
    tables, and executes the CREATE TABLE scripts in the order determined
    by the topological sort in a previous step.
    
    Returns:
        bool: True if all tables were successfully created or skipped,
              False if an error occurred
    """
    logger.info("Starting table script execution step")
    
    sql_dir = config.sql_dir
    table_order_path = config.schemas_dir / "table_order.json"

    # Ensure we have PostgreSQL credentials
    if not config.ensure_pg_credentials():
        logger.error("PostgreSQL credentials required")
        config.success = False
        return False

    try:
        # Read the table order from the JSON file
        logger.info(f"Reading table order from {table_order_path}")
        with open(table_order_path, "r", encoding="utf-8") as f:
            table_order = json.load(f)["table_order"]
        
        logger.info(f"Found {len(table_order)} tables to process")

        # Connect to PostgreSQL
        conn, error_msg = connect_postgres()
        if not conn:
            logger.error(f"Failed to connect to PostgreSQL: {error_msg}")
            print(f"❌ Failed to connect to PostgreSQL: {error_msg}")
            config.success = False
            return False
        
        cursor = conn.cursor()
        
        # Check for existing tables
        logger.info("Checking for existing tables")
        existing_tables = [t for t in table_order if table_exists(cursor, t)]
        
        drop_mode = "all"  # Default: create all tables
        
        if existing_tables:
            logger.info(f"Found {len(existing_tables)} existing tables")
            
            if config.force_mode:
                logger.info("Force mode enabled, dropping all existing tables")
                drop_mode = "all"
                print("⚠️ Existing tables found, but config.force_mode=True. Dropping all.")
            else:
                logger.info("Asking user for confirmation to drop existing tables")
                print("⚠️ The following tables already exist:")
                for t in existing_tables:
                    print(f"   - {t}")
                    
                choice = input("\nDo you want to drop all and recreate? [y/N]: ").strip().lower()
                drop_mode = "all" if choice == "y" else "skip"
                
                if drop_mode == "all":
                    logger.info("User chose to drop all existing tables")
                else:
                    logger.info("User chose to skip existing tables")

            # Drop existing tables if requested
            if drop_mode == "all":
                logger.info("Dropping existing tables")
                for t in existing_tables:
                    logger.info(f"Dropping table: {t}")
                    print(f"✅ Dropping: {t}")
                    
                    drop_query = f'DROP TABLE IF EXISTS "{t}" CASCADE'
                    success, error_msg = execute_query(cursor, drop_query)
                    
                    if not success:
                        logger.error(f"Failed to drop table {t}: {error_msg}")
                        print(f"❌ Failed to drop table {t}: {error_msg}")
                        config.success = False
                        return False
        else:
            logger.info("No existing tables found")

        # Run CREATE TABLE scripts
        logger.info("Executing CREATE TABLE scripts")
        print("\n✅ Executing CREATE TABLE scripts...")
        
        created_tables = 0
        skipped_tables = 0

        for table in table_order:
            if drop_mode == "skip" and table in existing_tables:
                logger.info(f"Skipping existing table: {table}")
                print(f"⏭️  Skipping existing table: {table}")
                skipped_tables += 1
                continue

            path = config.sql_tables_dir / f"create_{table}.sql"
            
            if path.exists():
                logger.info(f"Creating table: {table}")
                print(f"✅ Creating: {table}")
                
                success, error_msg = execute_sql_file(cursor, str(path))
                
                if not success:
                    logger.error(f"Failed to create table {table}: {error_msg}")
                    print(f"❌ Failed to create table {table}: {error_msg}")
                    config.success = False
                    return False
                    
                created_tables += 1
            else:
                logger.warning(f"CREATE script missing for table: {table}")
                print(f"⚠️ CREATE script missing for: {table}")

        # Commit changes and clean up
        conn.commit()
        cursor.close()
        close_connection(conn)
        logger.debug("PostgreSQL connection closed")

        # Print summary
        logger.info("Table creation complete")
        logger.info(f"Tables created: {created_tables}, Tables skipped: {skipped_tables}")
        
        print("\n✅ Table creation complete.")
        print(f"\n📋 Summary:")
        print(f"   Tables created: {created_tables}")
        print(f"   Tables skipped: {skipped_tables}")
        print(f"   Total in table_order: {len(table_order)}")

        return True

    except Exception as error:
        logger.exception("Error during schema execution")
        print(f"❌ Error during schema execution: {error}")
        config.success = False
        return False
