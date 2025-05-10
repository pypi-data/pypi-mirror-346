#!/usr/bin/env python3
# wordnet_db_migrator/steps/step068_generate_indexes.py
"""
Step 11: Generate Index Scripts

This module generates PostgreSQL CREATE INDEX scripts based on the SQLite
metadata extracted in a previous step. It handles both regular and unique
indexes.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

from ..config import config

# Set up logging
logger = logging.getLogger(__name__)

def generate_index_sql(index: Dict[str, Any]) -> str:
    """
    Generate a CREATE INDEX or CREATE UNIQUE INDEX SQL statement.
    
    Args:
        index: Dictionary containing index metadata
        
    Returns:
        str: SQL statement to create the index
    """
    logger.debug(f"Generating SQL for index: {index['name']}")
    
    index_type = "CREATE UNIQUE INDEX" if index.get("unique") else "CREATE INDEX"
    index_name = index["name"]
    table_name = index.get("table")  # Injected by the caller
    columns = ", ".join(index["columns"])
    
    sql = f"{index_type} {index_name} ON {table_name} ({columns});"
    
    logger.debug(f"Generated SQL: {sql}")
    return sql

def run() -> bool:
    """
    Generate PostgreSQL index scripts.
    
    This function reads the SQLite metadata from the JSON file created in a
    previous step, generates PostgreSQL CREATE INDEX statements for each index,
    and saves them to individual SQL files.
    
    Returns:
        bool: True if scripts were successfully generated and saved,
              False if an error occurred
    """
    logger.info("Starting index script generation step")
    
    # Ensure target directory exists
    target_dir = config.sql_dir / "indexes"
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensuring indexes directory exists: {target_dir}")
    
    # Clean old index scripts if directory exists
    if target_dir.exists():
        logger.info("Cleaning old index scripts")
        for file in target_dir.glob("*.sql"):
            logger.debug(f"Removing old file: {file}")
            file.unlink()
    
    structure_path = config.schemas_dir / "sqlite_structure.json"

    try:
        # Read the SQLite metadata
        logger.info(f"Reading SQLite structure from {structure_path}")
        with open(structure_path, "r", encoding="utf-8") as f:
            structure = json.load(f)
        
        logger.info(f"Found {len(structure)} tables to process")
        print("✅ Generating PostgreSQL index scripts...\n")

        # Generate index scripts for each table
        count = 0
        for table_name, table_meta in structure.items():
            logger.info(f"Processing indexes for table: {table_name}")
            
            indexes = table_meta.get("indexes", [])
            if not indexes:
                logger.debug(f"No indexes found for table: {table_name}")
                continue
                
            logger.debug(f"Found {len(indexes)} indexes for table: {table_name}")
            
            # Generate script for each index
            for index in indexes:
                logger.debug(f"Processing index: {index['name']}")
                
                # Inject table name for SQL generation
                index["table"] = table_name
                
                # Generate the index SQL
                index_sql = generate_index_sql(index)
                
                # Write to file
                index_file = target_dir / f"index_{index['name']}.sql"
                logger.info(f"Writing index script to {index_file}")
                
                with open(index_file, "w", encoding="utf-8") as f:
                    f.write(index_sql + "\n")

                print(f"✅ {index['name']} → {index_file.name}")
                count += 1

        logger.info(f"Generated {count} index scripts")
        print(f"\n✅ Generated {count} index scripts.")
        return True

    except Exception as error:
        logger.exception("Failed to generate index scripts")
        print(f"❌ Failed to generate index scripts: {error}")
        config.success = False
        return False
