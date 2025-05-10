#!/usr/bin/env python3
# wordnet_db_migrator/steps/step065_generate_foreign_keys.py
"""
Step 9: Generate Foreign Key Scripts

This module generates PostgreSQL ALTER TABLE statements to add foreign key
constraints based on the SQLite metadata extracted in a previous step.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Set

from ..config import config

# Set up logging
logger = logging.getLogger(__name__)

def generate_fk_sql(table_name: str, fks: List[Dict[str, Any]]) -> str:
    """
    Generate ALTER TABLE statements for foreign keys.
    
    Args:
        table_name: Name of the table to add foreign keys to
        fks: List of foreign key metadata dictionaries
        
    Returns:
        str: SQL statements to add foreign key constraints
    """
    logger.info(f"Generating foreign key SQL for table: {table_name}")
    
    statements = []
    for i, fk in enumerate(fks):
        constraint_name = f"{table_name}_fk_{i}"
        
        sql = (
            f"ALTER TABLE {table_name} "
            f"ADD CONSTRAINT {constraint_name} FOREIGN KEY ({fk['from']}) "
            f"REFERENCES {fk['table']}({fk['to']}) "
        )

        # Optional clauses
        if fk["on_update"] and fk["on_update"] != "NO ACTION":
            sql += f"ON UPDATE {fk['on_update']} "
            logger.debug(f"Added ON UPDATE {fk['on_update']} clause")
            
        if fk["on_delete"] and fk["on_delete"] != "NO ACTION":
            sql += f"ON DELETE {fk['on_delete']} "
            logger.debug(f"Added ON DELETE {fk['on_delete']} clause")

        statements.append(sql.strip() + ";")
        logger.debug(f"Generated foreign key constraint: {constraint_name}")

    result = "\n".join(statements)
    logger.debug(f"Generated {len(statements)} foreign key constraints for {table_name}")
    return result

def run() -> bool:
    """
    Generate foreign key ALTER TABLE scripts.
    
    This function reads the SQLite metadata from the JSON file created in a
    previous step, generates PostgreSQL ALTER TABLE statements to add foreign
    key constraints for each table, and saves them to individual SQL files.
    
    Returns:
        bool: True if scripts were successfully generated and saved,
              False if an error occurred
    """
    logger.info("Starting foreign key script generation step")
    
    # Make sure the foreign_keys directory exists
    fk_dir = config.sql_dir / "foreign_keys"
    fk_dir.mkdir(exist_ok=True)
    logger.info(f"Ensuring foreign keys directory exists: {fk_dir}")
    
    # Clean old FK files in the foreign_keys directory
    if fk_dir.exists():
        logger.info("Cleaning old foreign key files")
        for file in fk_dir.glob("*.sql"):
            logger.debug(f"Removing old file: {file}")
            file.unlink()
    
    structure_path = config.schemas_dir / "sqlite_structure.json"

    try:
        # Read the SQLite metadata
        logger.info(f"Reading SQLite structure from {structure_path}")
        with open(structure_path, "r", encoding="utf-8") as f:
            structure = json.load(f)
        
        logger.info(f"Found {len(structure)} tables to process")

        print("✅ Generating foreign key constraint scripts...\n")

        # Generate foreign key scripts for each table
        tables_with_fks = 0
        for table_name, table_meta in structure.items():
            fks = table_meta.get("foreign_keys", [])
            
            if not fks:
                logger.debug(f"Table {table_name} has no foreign keys, skipping")
                continue
                
            logger.info(f"Processing foreign keys for table: {table_name}")
            tables_with_fks += 1
            
            # Generate the foreign key SQL
            fk_sql = generate_fk_sql(table_name, fks)

            # Write to the foreign_keys subdirectory
            output_file = fk_dir / f"fk_{table_name}.sql"
            logger.info(f"Writing foreign key script to {output_file}")
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(fk_sql + "\n")

            print(f"✅ {table_name} → {output_file.name}")

        logger.info(f"Generated foreign key scripts for {tables_with_fks} tables")
        print("\n✅ All foreign key scripts generated.")
        return True

    except Exception as error:
        logger.exception("Failed to generate foreign key scripts")
        print(f"❌ Failed to generate foreign key scripts: {error}")
        config.success = False
        return False
