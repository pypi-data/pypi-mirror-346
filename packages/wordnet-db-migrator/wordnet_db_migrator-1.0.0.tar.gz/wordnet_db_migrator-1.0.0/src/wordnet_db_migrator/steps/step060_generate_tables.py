#!/usr/bin/env python3
# wordnet_db_migrator/steps/step060_generate_tables.py
"""
Step 8: Generate Table Scripts

This module generates PostgreSQL CREATE TABLE scripts based on the SQLite
metadata extracted in the previous step. It maps SQLite data types to
PostgreSQL data types and handles primary keys and default values.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Set

from ..config import config

# Set up logging
logger = logging.getLogger(__name__)

# Mapping of SQLite types to PostgreSQL types
SQLITE_TO_POSTGRES_TYPES = {
    "INTEGER": "INTEGER",
    "TEXT": "TEXT",
    "REAL": "REAL",
    "BLOB": "BYTEA",
    "NUMERIC": "NUMERIC",
    "BOOLEAN": "BOOLEAN",
    # Extend as needed
}

def convert_type(sqlite_type: str) -> str:
    """
    Map SQLite data types to PostgreSQL data types.
    
    Args:
        sqlite_type: SQLite data type to convert
        
    Returns:
        str: Corresponding PostgreSQL data type
    """
    logger.debug(f"Converting SQLite type: {sqlite_type}")
    
    sqlite_type = sqlite_type.upper()
    for key in SQLITE_TO_POSTGRES_TYPES:
        if key in sqlite_type:
            pg_type = SQLITE_TO_POSTGRES_TYPES[key]
            logger.debug(f"Mapped {sqlite_type} to {pg_type}")
            return pg_type
    
    logger.warning(f"No mapping found for SQLite type: {sqlite_type}, using TEXT as fallback")
    return "TEXT"  # fallback

def generate_create_table_sql(table_name: str, table_meta: Dict[str, Any]) -> str:
    """
    Generate PostgreSQL CREATE TABLE SQL for a table.
    
    Args:
        table_name: Name of the table
        table_meta: Metadata for the table (columns, foreign keys, indexes)
        
    Returns:
        str: PostgreSQL CREATE TABLE SQL statement
    """
    logger.info(f"Generating CREATE TABLE SQL for {table_name}")
    
    lines = [f"CREATE TABLE {table_name} ("]
    col_lines = []

    # Process each column
    for col in table_meta["columns"]:
        name = col["name"]
        dtype = convert_type(col["type"])
        not_null = "NOT NULL" if col["notnull"] else ""
        default_val = col['default']
        
        # Handle default values
        if default_val is not None:
            dtype = convert_type(col["type"])
            if dtype == "BOOLEAN":
                if default_val in ("0", 0):
                    default = "DEFAULT FALSE"
                elif default_val in ("1", 1):
                    default = "DEFAULT TRUE"
                else:
                    default = f"DEFAULT {default_val}"
            else:
                default = f"DEFAULT {default_val}"
        else:
            default = ""

        col_lines.append(f"    {name} {dtype} {default} {not_null}".strip())
        logger.debug(f"Added column: {name} {dtype} {default} {not_null}")

    # Primary key (may be composite)
    pk_cols = [col["name"] for col in table_meta["columns"] if col["primary_key"]]
    if pk_cols:
        pk_clause = f"    PRIMARY KEY ({', '.join(pk_cols)})"
        col_lines.append(pk_clause)
        logger.debug(f"Added primary key: {pk_clause}")

    lines.extend(",\n".join(col_lines).splitlines())
    lines.append(");")

    sql = "\n".join(lines)
    logger.debug(f"Generated SQL for {table_name}:\n{sql}")
    return sql

def run() -> bool:
    """
    Generate PostgreSQL CREATE TABLE scripts.
    
    This function reads the SQLite metadata from the JSON file created in the
    previous step, generates PostgreSQL CREATE TABLE scripts for each table,
    and saves them to individual SQL files.
    
    Returns:
        bool: True if scripts were successfully generated and saved,
              False if an error occurred
    """
    logger.info("Starting table script generation step")
    
    # Make sure the tables directory exists
    tables_dir = config.sql_dir / "tables"
    tables_dir.mkdir(exist_ok=True)
    logger.info(f"Ensuring tables directory exists: {tables_dir}")
    
    # Clean old table DDL files (only in the tables directory)
    if tables_dir.exists():
        logger.info("Cleaning old table DDL files")
        for file in tables_dir.glob("*.sql"):
            logger.debug(f"Removing old file: {file}")
            file.unlink()

    structure_path = config.schemas_dir / "sqlite_structure.json"

    try:
        # Read the SQLite metadata
        logger.info(f"Reading SQLite structure from {structure_path}")
        with open(structure_path, "r", encoding="utf-8") as f:
            structure = json.load(f)
        
        logger.info(f"Found {len(structure)} tables to process")

        print("✅ Generating PostgreSQL CREATE TABLE scripts...\n")
        
        # Generate CREATE TABLE scripts for each table
        for table_name, table_meta in structure.items():
            logger.info(f"Processing table: {table_name}")
            
            # Generate the CREATE TABLE SQL
            ddl = generate_create_table_sql(table_name, table_meta)

            # Write to the tables subdirectory
            output_file = tables_dir / f"create_{table_name}.sql"
            logger.info(f"Writing CREATE TABLE script to {output_file}")
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(ddl + "\n")

            print(f"✅ {table_name} → {output_file.name}")

        print("\n✅ All CREATE TABLE scripts generated.")
        logger.info("Table script generation completed successfully")
        return True

    except Exception as error:
        logger.exception("Failed to generate CREATE TABLE scripts")
        print(f"❌ Failed to generate CREATE TABLE scripts: {error}")
        config.success = False
        return False
