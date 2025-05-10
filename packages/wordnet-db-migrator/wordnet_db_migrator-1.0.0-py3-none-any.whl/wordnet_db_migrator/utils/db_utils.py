#!/usr/bin/env python3
# wordnet_db_migrator/utils/db_utils.py
"""
Database utility functions for WordNet Porter.

This module provides centralized database connection management and standardized
error handling for both SQLite and PostgreSQL database operations.
"""
import sqlite3
import psycopg2
import psycopg2.extras
import logging
from typing import Optional, Tuple, Dict, Any, Union, List
from ..config import config

# Set up logging
logger = logging.getLogger(__name__)

# Connection type aliases for type hints
SQLiteConnection = sqlite3.Connection
SQLiteCursor = sqlite3.Cursor
PGConnection = psycopg2.extensions.connection
PGCursor = psycopg2.extensions.cursor


def connect_sqlite() -> Tuple[Optional[SQLiteConnection], str]:
    """
    Create a connection to the SQLite database.
    
    Returns:
        Tuple containing:
            - SQLite connection object or None if connection failed
            - Error message if connection failed, empty string otherwise
    """
    try:
        conn = sqlite3.connect(config.SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn, ""
    except Exception as error:
        error_msg = f"SQLite connection error: {error}"
        logger.error(error_msg)
        return None, error_msg


def connect_postgres(database: str = None) -> Tuple[Optional[PGConnection], str]:
    """
    Create a connection to the PostgreSQL database.
    
    Args:
        database: Database name to connect to. If None, uses config.PG_DATABASE.
    
    Returns:
        Tuple containing:
            - PostgreSQL connection object or None if connection failed
            - Error message if connection failed, empty string otherwise
    """
    # Ensure we have PostgreSQL credentials
    if not config.ensure_pg_credentials():
        return None, "Failed to get PostgreSQL credentials"
    
    db_name = database if database is not None else config.PG_DATABASE
    
    try:
        conn = psycopg2.connect(
            host=config.PG_HOST,
            port=config.PG_PORT,
            dbname=db_name,
            user=config.pg_user,
            password=config.pg_password
        )
        
        # Print database name if configured to do so
        if config.SHOW_DB_NAME:
            db_params = conn.get_dsn_parameters()
            logger.info(f"Connected to PostgreSQL database: {db_params['dbname']}")
            print(f"🛢️  Connected to PostgreSQL database: {db_params['dbname']}")
            
        return conn, ""
    except Exception as error:
        error_msg = f"PostgreSQL connection error: {error}"
        logger.error(error_msg)
        return None, error_msg


def execute_sql_file(cursor: Union[SQLiteCursor, PGCursor], file_path: str) -> Tuple[bool, str]:
    """
    Execute SQL statements from a file.
    
    Args:
        cursor: Database cursor (SQLite or PostgreSQL)
        file_path: Path to the SQL file
        
    Returns:
        Tuple containing:
            - Boolean indicating success or failure
            - Error message if failed, empty string otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as sql_file:
            sql = sql_file.read()
            cursor.execute(sql)
        return True, ""
    except Exception as error:
        error_msg = f"Failed to execute SQL file {file_path}: {error}"
        logger.error(error_msg)
        return False, error_msg


def execute_query(cursor: Union[SQLiteCursor, PGCursor], query: str, 
                 params: Any = None) -> Tuple[bool, str]:
    """
    Execute a SQL query with error handling.
    
    Args:
        cursor: Database cursor (SQLite or PostgreSQL)
        query: SQL query to execute
        params: Query parameters (optional)
        
    Returns:
        Tuple containing:
            - Boolean indicating success or failure
            - Error message if failed, empty string otherwise
    """
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return True, ""
    except Exception as error:
        error_msg = f"Query execution error: {error}\nQuery: {query}"
        logger.error(error_msg)
        return False, error_msg


def fetch_all(cursor: Union[SQLiteCursor, PGCursor], query: str, 
             params: Any = None) -> Tuple[Optional[List], str]:
    """
    Execute a query and fetch all results with error handling.
    
    Args:
        cursor: Database cursor (SQLite or PostgreSQL)
        query: SQL query to execute
        params: Query parameters (optional)
        
    Returns:
        Tuple containing:
            - List of results or None if query failed
            - Error message if failed, empty string otherwise
    """
    success, error_msg = execute_query(cursor, query, params)
    if not success:
        return None, error_msg
    
    try:
        results = cursor.fetchall()
        return results, ""
    except Exception as error:
        error_msg = f"Error fetching results: {error}"
        logger.error(error_msg)
        return None, error_msg


def close_connection(conn: Union[SQLiteConnection, PGConnection]) -> None:
    """
    Safely close a database connection.
    
    Args:
        conn: Database connection to close
    """
    try:
        if conn:
            conn.close()
    except Exception as error:
        logger.error(f"Error closing connection: {error}")
