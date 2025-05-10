#!/usr/bin/env python3
# wordnet_db_migrator/steps/step080_run_index_scripts.py
"""
Step 13: Run Index Creation Scripts

This module executes the PostgreSQL CREATE INDEX scripts generated in a previous
step. It connects to the PostgreSQL database and runs each index script in
alphabetical order.
"""
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Set

from ..config import config
from ..utils.db_utils import connect_postgres, execute_sql_file, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def run() -> bool:
    """
    Execute all CREATE INDEX scripts.
    
    This function connects to the PostgreSQL database and executes all the
    CREATE INDEX scripts generated in a previous step.
    
    Returns:
        bool: True if all index scripts were successfully executed,
              False if an error occurred
    """
    logger.info("Starting index script execution step")
    
    sql_dir = config.sql_indexes_dir
    logger.info(f"Index scripts directory: {sql_dir}")

    # Ensure we have PostgreSQL credentials
    if not config.ensure_pg_credentials():
        logger.error("PostgreSQL credentials required")
        print("❌ PostgreSQL credentials required")
        config.success = False
        return False

    try:
        # Connect to PostgreSQL
        conn, error_msg = connect_postgres()
        if not conn:
            logger.error(f"Failed to connect to PostgreSQL: {error_msg}")
            print(f"❌ Failed to connect to PostgreSQL: {error_msg}")
            config.success = False
            return False
        
        cursor = conn.cursor()
        conn.autocommit = True
        logger.debug("Set autocommit mode for PostgreSQL connection")

        # Find all index scripts
        index_files = sorted(sql_dir.glob("index_*.sql"))
        logger.info(f"Found {len(index_files)} index scripts")

        if not index_files:
            logger.info("No index scripts found to run")
            print("ℹ️  No index scripts found to run.")
            return True

        print(f"✅ Executing {len(index_files)} index scripts...\n")

        # Execute each index script
        success_count = 0
        failure_count = 0
        
        for path in index_files:
            logger.info(f"Executing index script: {path.name}")
            
            try:
                print(f"✅ {path.name}")
                success, error_msg = execute_sql_file(cursor, str(path))
                
                if success:
                    logger.debug(f"Successfully executed index script: {path.name}")
                    success_count += 1
                else:
                    logger.error(f"Failed to execute index script {path.name}: {error_msg}")
                    print(f"❌ Failed to execute {path.name}: {error_msg}")
                    failure_count += 1
                    
            except Exception as error:
                logger.exception(f"Exception executing index script {path.name}")
                print(f"❌ Failed to execute {path.name}: {error}")
                failure_count += 1

        # Log summary
        logger.info(f"Index script execution complete: {success_count} succeeded, {failure_count} failed")
        print(f"\n✅ All index scripts processed: {success_count} succeeded, {failure_count} failed.")
        
        return True

    except Exception as error:
        logger.exception("Error executing index scripts")
        print(f"❌ Error executing index scripts: {error}")
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
