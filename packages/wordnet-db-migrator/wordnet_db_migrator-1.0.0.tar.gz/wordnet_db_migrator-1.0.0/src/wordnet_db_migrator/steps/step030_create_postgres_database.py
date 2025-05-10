#!/usr/bin/env python3
# wordnet_db_migrator/steps/step030_create_postgres_database.py
"""
Step 3: Create PostgreSQL Database

This module handles the creation of the WordNet database in PostgreSQL.
It connects to the 'postgres' admin database, checks if the 'wordnet' database
already exists, and either creates it or prompts the user to drop and recreate it.
"""
import logging
from typing import Optional, Dict, Any, Tuple, List, Union

from ..config import config
from ..utils.db_utils import connect_postgres, execute_query, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def check_database_exists(cursor: Any) -> Tuple[bool, str]:
    """
    Check if the WordNet database already exists.
    
    Args:
        cursor: PostgreSQL database cursor
        
    Returns:
        Tuple containing:
            - Boolean indicating if the database exists
            - Error message if query failed, empty string otherwise
    """
    logger.info("Checking if WordNet database already exists")
    
    query = "SELECT 1 FROM pg_database WHERE datname = 'wordnet'"
    success, error_msg = execute_query(cursor, query)
    
    if not success:
        logger.error(f"Failed to check if database exists: {error_msg}")
        return False, error_msg
        
    exists = cursor.fetchone() is not None
    
    if exists:
        logger.info("WordNet database already exists")
    else:
        logger.info("WordNet database does not exist")
        
    return exists, ""

def drop_database(cursor: Any) -> Tuple[bool, str]:
    """
    Drop the existing WordNet database.
    
    Args:
        cursor: PostgreSQL database cursor
        
    Returns:
        Tuple containing:
            - Boolean indicating success or failure
            - Error message if failed, empty string otherwise
    """
    logger.info("Dropping existing WordNet database")
    
    # First terminate any existing connections
    terminate_query = """
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = 'wordnet'
    """
    success, error_msg = execute_query(cursor, terminate_query)
    
    if not success:
        logger.error(f"Failed to terminate connections to database: {error_msg}")
        return False, error_msg
        
    # Now drop the database
    drop_query = "DROP DATABASE wordnet"
    success, error_msg = execute_query(cursor, drop_query)
    
    if not success:
        logger.error(f"Failed to drop database: {error_msg}")
        return False, error_msg
        
    logger.info("Successfully dropped WordNet database")
    return True, ""

def create_database(cursor: Any) -> Tuple[bool, str]:
    """
    Create a new WordNet database.
    
    Args:
        cursor: PostgreSQL database cursor
        
    Returns:
        Tuple containing:
            - Boolean indicating success or failure
            - Error message if failed, empty string otherwise
    """
    logger.info("Creating new WordNet database")
    
    query = "CREATE DATABASE wordnet TEMPLATE template0"
    success, error_msg = execute_query(cursor, query)
    
    if not success:
        logger.error(f"Failed to create database: {error_msg}")
        return False, error_msg
        
    logger.info("Successfully created WordNet database")
    return True, ""

def run() -> bool:
    """
    Create the WordNet database in PostgreSQL.
    
    This function connects to the PostgreSQL 'postgres' admin database,
    checks if the 'wordnet' database already exists, and either creates it
    or prompts the user to drop and recreate it.
    
    Returns:
        bool: True if the database was successfully created or already exists,
              False if an error occurred
    """
    logger.info("Starting PostgreSQL database creation step")
    
    # Ensure we have PostgreSQL credentials
    if not config.ensure_pg_credentials():
        logger.error("PostgreSQL credentials required")
        print("❌ PostgreSQL credentials required")
        config.success = False
        return False

    try:
        # Connect to the postgres admin database
        conn, error_msg = connect_postgres("postgres")
        
        if not conn:
            logger.error(f"Failed to connect to PostgreSQL: {error_msg}")
            print(f"❌ Failed to connect to PostgreSQL: {error_msg}")
            config.success = False
            return False
            
        # Enable autocommit for database creation
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if the database already exists
        exists, error_msg = check_database_exists(cursor)
        
        if error_msg:
            print(f"❌ Failed to check if database exists: {error_msg}")
            config.success = False
            return False

        if exists:
            print("Database 'wordnet' already exists.")

            if config.force_mode:
                logger.info("Force mode enabled: dropping and recreating without prompt")
                print("⚠️ Force mode enabled: dropping and recreating without prompt.")
                
                success, error_msg = drop_database(cursor)
                if not success:
                    print(f"❌ Failed to drop database: {error_msg}")
                    config.success = False
                    return False
                    
                print("✅ Dropped existing database")
                
                success, error_msg = create_database(cursor)
                if not success:
                    print(f"❌ Failed to create database: {error_msg}")
                    config.success = False
                    return False
                    
                print("✅ Created new wordnet database")

            else:
                recreate = input("Do you want to drop and recreate it? [y/N]: ").lower().strip()
                if recreate == 'y':
                    logger.info("User chose to drop and recreate the database")
                    print("Dropping existing database...")
                    
                    success, error_msg = drop_database(cursor)
                    if not success:
                        print(f"❌ Failed to drop database: {error_msg}")
                        config.success = False
                        return False
                        
                    print("✅ Dropped existing database")
                    
                    success, error_msg = create_database(cursor)
                    if not success:
                        print(f"❌ Failed to create database: {error_msg}")
                        config.success = False
                        return False
                        
                    print("✅ Created new wordnet database")
                else:
                    logger.info("User chose to keep the existing database")
                    print("Keeping existing database")

        else:
            print("Creating new wordnet database...")
            
            success, error_msg = create_database(cursor)
            if not success:
                print(f"❌ Failed to create database: {error_msg}")
                config.success = False
                return False
                
            print("✅ Created wordnet database")

        # Clean up
        cursor.close()
        close_connection(conn)

        # Confirm we're targeting the correct database moving forward
        config.pg_database = "wordnet"
        logger.info(f"PostgreSQL database ready: {config.pg_database}")
        print(f"✅ PostgreSQL database ready: {config.pg_database}")
        return True

    except Exception as error:
        logger.exception("Unexpected error during database creation")
        print(f"❌ Database operation failed: {error}")
        config.success = False
        return False
