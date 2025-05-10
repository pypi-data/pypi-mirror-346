#!/usr/bin/env python3
# wordnet_db_migrator/steps/step100_apply_foreign_keys.py
"""
Step 16: Apply Foreign Keys

This module applies foreign key constraints to the PostgreSQL database.
It executes the foreign key scripts generated in a previous step, following
the dependency order determined by the topological sort.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Set

from ..config import config
from ..utils.db_utils import connect_postgres, execute_query, execute_sql_file, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def run() -> bool:
    """
    Apply foreign key constraints to the PostgreSQL database.
    
    This function reads the table order from the JSON file, connects to the
    PostgreSQL database, and executes the foreign key scripts for each table
    in the order determined by the topological sort.
    
    Returns:
        bool: True if all foreign key constraints were successfully applied,
              False if an error occurred
    """
    logger.info("Starting foreign key application step")
    
    # Use the foreign_keys directory from config
    fk_dir = config.sql_foreign_keys_dir
    table_order_path = config.schemas_dir / "table_order.json"
    
    logger.info(f"Foreign key scripts directory: {fk_dir}")
    logger.info(f"Table order file: {table_order_path}")

    # Ensure we have PostgreSQL credentials
    if not config.ensure_pg_credentials():
        logger.error("PostgreSQL credentials missing")
        print("❌ PostgreSQL credentials missing")
        config.success = False
        return False

    try:
        # Read the table order from the JSON file
        logger.info("Reading table order from JSON file")
        with open(table_order_path, "r", encoding="utf-8") as f:
            table_order = json.load(f)["table_order"]
        
        logger.info(f"Found {len(table_order)} tables in order")

        # Connect to PostgreSQL
        logger.info("Connecting to PostgreSQL database")
        conn, error_msg = connect_postgres()
        
        if not conn:
            logger.error(f"Failed to connect to PostgreSQL: {error_msg}")
            print(f"❌ Failed to connect to PostgreSQL: {error_msg}")
            config.success = False
            return False
            
        cursor = conn.cursor()
        conn.autocommit = True
        logger.debug("Set autocommit mode for PostgreSQL connection")

        # List all FK scripts found first
        fk_scripts = list(fk_dir.glob("fk_*.sql"))
        logger.info(f"Found {len(fk_scripts)} foreign key scripts in {fk_dir}")
        
        if not fk_scripts:
            logger.error(f"No FK scripts found with pattern 'fk_*.sql' in {fk_dir}")
            print(f"❌ No foreign key scripts found")
            config.success = False
            return False
        
        print(f"\n✅ Applying foreign key constraints ({len(fk_scripts)} scripts)")

        success = True
        applied = 0  # Initialize the 'applied' counter
        skipped = 0
        
        # Apply foreign key constraints for each table
        for table in table_order:
            fk_path = fk_dir / f"fk_{table}.sql"
            
            if fk_path.exists():
                logger.info(f"Applying foreign keys for table: {table}")
                try:
                    print(f"✅ Applying foreign keys for {table}")
                    
                    # Execute the SQL file
                    success_exec, error_msg = execute_sql_file(cursor, str(fk_path))
                    
                    if not success_exec:
                        logger.error(f"Failed to apply foreign keys for {table}: {error_msg}")
                        print(f"❌ Failed to apply foreign keys for {table}: {error_msg}")
                        success = False
                    else:
                        logger.info(f"Successfully applied foreign keys for {table}")
                        applied += 1
                        
                except Exception as error:
                    logger.exception(f"Exception applying foreign keys for {table}: {error}")
                    print(f"❌ Failed to apply foreign keys for {table}: {error}")
                    success = False
            else:
                logger.info(f"No foreign key script for table: {table}")
                skipped += 1

        # Print summary
        if success:
            logger.info("Foreign key application completed successfully")
            print(f"\n✅ All foreign key constraints applied successfully ({applied} tables)")
        else:
            logger.error("Foreign key application incomplete: errors occurred")
            print(f"\n❌ Foreign key application incomplete: errors occurred")

        config.success = success
        return success

    except Exception as error:
        logger.exception(f"Error during foreign key application: {error}")
        print(f"❌ Error during FK application: {error}")
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
