#!/usr/bin/env python3
# wordnet_db_migrator/steps/step067_generate_foreign_key_validators.py
"""
Step 10: Generate Foreign Key Validators

This module generates SQL scripts that validate foreign key relationships
without misreporting NULLs. These scripts are used to check for data integrity
issues before applying foreign key constraints in PostgreSQL.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union

from ..config import config
from ..utils.db_utils import connect_sqlite, execute_query, fetch_all, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def generate_validator_sql(table: str, idx: int, fk: Dict[str, Any]) -> str:
    """
    Generate SQL to validate a foreign key relationship.
    
    Args:
        table: Name of the table containing the foreign key
        idx: Index of the foreign key in the table
        fk: Foreign key metadata dictionary
        
    Returns:
        str: SQL script to validate the foreign key relationship
    """
    logger.debug(f"Generating validator SQL for {table}_fk_{idx}")
    
    from_column = fk["from"]
    to_table = fk["table"]
    to_column = fk["to"]
    
    # Build the SQL script
    sql_lines = [
        f"-- FK CHECK: {table}_fk_{idx}",
        f"SELECT {table}.*",
        f"FROM {table}",
        f"LEFT JOIN {to_table} ON {table}.{from_column} = {to_table}.{to_column}",
        f"WHERE {table}.{from_column} IS NOT NULL",  # This is the important line
        f"  AND {to_table}.{to_column} IS NULL;"
    ]
    
    return "\n".join(sql_lines)

def run() -> bool:
    """
    Generate validation scripts for foreign keys.
    
    This function connects to the SQLite database, extracts foreign key
    information for each table, and generates SQL scripts to validate
    the foreign key relationships before applying constraints in PostgreSQL.
    
    Returns:
        bool: True if scripts were successfully generated and saved,
              False if an error occurred
    """
    logger.info("Starting foreign key validator script generation step")
    
    # Set up output directory
    output_dir = config.sql_dir / "fk_validate"
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensuring foreign key validator directory exists: {output_dir}")
    
    # Clean old validator files
    if output_dir.exists():
        logger.info("Cleaning old validator files")
        for file in output_dir.glob("*.sql"):
            logger.debug(f"Removing old file: {file}")
            file.unlink()
    
    try:
        # Connect to SQLite
        conn, error_msg = connect_sqlite()
        if not conn:
            logger.error(f"Failed to connect to SQLite database: {error_msg}")
            print(f"❌ Failed to connect to SQLite database: {error_msg}")
            config.success = False
            return False
        
        cursor = conn.cursor()
        
        # Load table list from JSON
        table_list_path = config.output_dir / "sqlite_tables.json"
        logger.info(f"Reading table list from {table_list_path}")
        
        with open(table_list_path, "r", encoding="utf-8") as f:
            sqlite_info = json.load(f)
        
        tables = sqlite_info["tables"]
        logger.info(f"Found {len(tables)} tables to process")

        # Generate validator scripts for each table
        fk_count = 0
        
        for table in tables:
            logger.info(f"Processing foreign keys for table: {table}")
            
            # Get foreign key information
            query = f"PRAGMA foreign_key_list({table})"
            fks, error_msg = fetch_all(cursor, query)
            
            if not fks:
                logger.debug(f"No foreign keys found for table: {table}")
                continue
                
            logger.debug(f"Found {len(fks)} foreign keys for table: {table}")
            
            # Generate validator script for each foreign key
            for idx, fk in enumerate(fks):
                logger.debug(f"Processing foreign key {idx} for table: {table}")
                
                # Generate the validator SQL
                sql = generate_validator_sql(table, idx, fk)
                
                # Write to file
                output_file = output_dir / f"validate_{table}_{idx}.sql"
                logger.info(f"Writing validator script to {output_file}")
                
                with open(output_file, "w", encoding="utf-8") as f_out:
                    f_out.write(sql + "\n")
                
                fk_count += 1

        logger.info(f"Generated {fk_count} foreign key validator scripts")
        print(f"✅ Generated {fk_count} foreign key validator scripts in {output_dir}")
        return True

    except Exception as error:
        logger.exception("Failed to generate foreign key validators")
        print(f"❌ Failed to generate FK validators: {error}")
        config.success = False
        return False
        
    finally:
        # Clean up resources
        if 'conn' in locals() and conn:
            close_connection(conn)
            logger.debug("SQLite connection closed")
