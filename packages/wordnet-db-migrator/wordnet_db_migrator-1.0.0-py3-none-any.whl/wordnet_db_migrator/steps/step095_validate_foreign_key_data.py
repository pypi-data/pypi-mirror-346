#!/usr/bin/env python3
# wordnet_db_migrator/steps/step095_validate_foreign_key_data.py
"""
Step 15: Validate Foreign Key Data

This module validates foreign key relationships in the PostgreSQL database
before applying constraints. It runs validation queries to identify orphaned
records that would violate foreign key constraints.
"""
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Set

from ..config import config
from ..utils.db_utils import connect_postgres, execute_query, execute_sql_file, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def run() -> bool:
    """
    Validate foreign key relationships in the PostgreSQL database.
    
    This function runs validation queries to identify orphaned records
    that would violate foreign key constraints. It logs the results and
    generates reports for any violations found.
    
    Returns:
        bool: True if validation completed successfully (even if orphans were found),
              False if an error occurred
    """
    logger.info("Starting foreign key validation step")
    
    fk_validate_dir = config.sql_dir / "fk_validate"
    orphan_log_dir = config.logs_dir / "orphans"
    
    # Ensure the orphan log directory exists
    orphan_log_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensuring orphan log directory exists: {orphan_log_dir}")

    # Ensure we have PostgreSQL credentials
    if not config.ensure_pg_credentials():
        logger.error("PostgreSQL credentials missing")
        print("❌ PostgreSQL credentials missing")
        config.success = False
        return False

    try:
        # Connect to PostgreSQL
        logger.info("Connecting to PostgreSQL database")
        conn, error_msg = connect_postgres()
        
        if not conn:
            logger.error(f"Failed to connect to PostgreSQL: {error_msg}")
            print(f"❌ Failed to connect to PostgreSQL: {error_msg}")
            config.success = False
            return False
            
        cursor = conn.cursor()

        # Add debug output for directory validation
        logger.info(f"Looking for validation scripts in: {fk_validate_dir}")
        print(f"Looking for validation scripts in: {fk_validate_dir}")

        # Check if directory exists
        if not fk_validate_dir.exists():
            logger.error(f"Directory does not exist: {fk_validate_dir}")
            print(f"❌ Directory does not exist: {fk_validate_dir}")
            config.success = False
            return False

        # Find validation scripts
        sql_files = sorted(fk_validate_dir.glob("validate_*.sql"))
        logger.info(f"Found {len(sql_files)} validation scripts")
        
        if not sql_files:
            logger.error("No validation scripts matching pattern 'validate_*.sql' found")
            print(f"❌ No validation scripts matching pattern 'validate_*.sql' found.")
            config.success = False
            return False

        print(f"🔍 Running {len(sql_files)} FK validation queries...\n")

        clean_count = 0
        dirty_count = 0

        # Process each validation script
        for path in sql_files:
            logger.info(f"Processing validation script: {path.name}")
            
            # Read and execute the validation query
            with open(path, "r", encoding="utf-8") as f:
                query = f.read()

            success, error_msg = execute_query(cursor, query)
            
            if not success:
                logger.error(f"Failed to execute validation query {path.name}: {error_msg}")
                print(f"❌ Failed to execute {path.name}: {error_msg}")
                continue
                
            orphans = cursor.fetchall()
            
            # Extract table name from filename (removing 'validate_' prefix and '_X.sql' suffix)
            table_part = path.name.replace('validate_', '').rsplit('_', 1)[0]
            
            if not orphans:
                logger.info(f"No orphans found in {table_part}")
                print(f"✅ {table_part}: No orphans")
                clean_count += 1
            else:
                logger.warning(f"Found {len(orphans)} orphans in {table_part}")
                print(f"❌ {table_part}: {len(orphans)} orphan(s) found")
                dirty_count += 1
                
                # Log orphans to file
                log_path = orphan_log_dir / path.name.replace(".sql", ".txt")
                logger.info(f"Writing orphan log to {log_path}")
                
                with open(log_path, "w", encoding="utf-8") as f:
                    for row in orphans:
                        f.write(str(row) + "\n")

        # Print summary
        logger.info(f"FK Validation Summary: {clean_count} clean / {dirty_count} with orphans")
        print(f"\n✅ FK Validation Summary: {clean_count} clean / {dirty_count} with orphans")
        
        if dirty_count > 0:
            logger.warning(f"Orphan logs written to: {orphan_log_dir}")
            print(f"🔎 See orphan logs in: {orphan_log_dir}")
            
        return True

    except Exception as error:
        logger.exception(f"Error running FK validation: {error}")
        print(f"❌ Error running FK validation: {error}")
        config.success = False
        return False

    finally:
        # Clean up resources
        if 'cursor' in locals() and cursor:
            cursor.close()
            logger.debug("Closed PostgreSQL cursor")
            
        if 'conn' in locals() and conn:
            close_connection(conn)
            logger.debug("Closed PostgreSQL connection")
