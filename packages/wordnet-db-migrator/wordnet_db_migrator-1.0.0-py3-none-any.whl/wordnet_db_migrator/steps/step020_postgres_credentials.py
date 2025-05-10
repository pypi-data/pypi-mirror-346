#!/usr/bin/env python3
# wordnet_db_migrator/steps/step020_postgres_credentials.py
"""
Step 2: PostgreSQL Credentials

This module handles obtaining and validating PostgreSQL credentials.
It prompts the user for their PostgreSQL username and password,
then tests the connection to ensure the credentials are valid.
"""
import getpass
import logging
from typing import Tuple, Optional, Dict, Any

from ..config import config
from ..utils.db_utils import connect_postgres, close_connection

# Set up logging
logger = logging.getLogger(__name__)

def test_connection(username: str, password: str) -> bool:
    """
    Test PostgreSQL connection using 'postgres' database (admin db).
    
    Args:
        username: PostgreSQL username
        password: PostgreSQL password
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    logger.info(f"Testing PostgreSQL connection for user '{username}'")
    
    # Temporarily store credentials in config
    original_user = config.pg_user
    original_password = config.pg_password
    
    config.pg_user = username
    config.pg_password = password
    
    try:
        # Connect to the postgres admin database
        conn, error_msg = connect_postgres("postgres")
        
        if not conn:
            logger.error(f"PostgreSQL connection test failed: {error_msg}")
            print(f"❌ Connection failed: {error_msg}")
            return False
            
        logger.info("PostgreSQL connection test successful")
        
        # Close the connection
        close_connection(conn)
        return True
        
    except Exception as error:
        logger.exception("Unexpected error during PostgreSQL connection test")
        print(f"❌ Connection failed: {error}")
        return False
    finally:
        # Restore original credentials if test fails
        if not config.success:
            config.pg_user = original_user
            config.pg_password = original_password

def get_credentials() -> bool:
    """
    Prompt for PostgreSQL credentials, test them, and store if valid.
    
    Returns:
        bool: True if valid credentials were obtained, False otherwise
    """
    logger.info("Prompting for PostgreSQL credentials")
    
    for attempt in range(1, config.MAX_LOGIN_ATTEMPTS + 1):
        if attempt > 1:
            logger.info(f"Credential attempt {attempt} of {config.MAX_LOGIN_ATTEMPTS}")
            print(f"\nAttempt {attempt} of {config.MAX_LOGIN_ATTEMPTS}:")

        # Get username
        username = input("PostgreSQL Username: ").strip()
        if not username:
            logger.warning("Empty username provided")
            print("❌ Username cannot be empty")
            continue

        # Get password
        password = getpass.getpass("PostgreSQL Password: ")

        # Test the connection
        print("\nTesting connection...", end="", flush=True)
        if test_connection(username, password):
            # Store valid credentials in config
            config.pg_user = username
            config.pg_password = password
            
            logger.info("Valid PostgreSQL credentials obtained")
            print("\n✅ Success!")
            print("\n✅ PostgreSQL login successful")
            return True

        # Handle max attempts reached
        if attempt == config.MAX_LOGIN_ATTEMPTS:
            logger.error(f"Failed to log in after {config.MAX_LOGIN_ATTEMPTS} attempts")
            print(f"\n❌ Failed to log in to PostgreSQL after {config.MAX_LOGIN_ATTEMPTS} attempts.")
            return False

def run() -> bool:
    """
    Run the credential gathering and validation process.
    
    Returns:
        bool: True if credentials were successfully obtained and validated, False otherwise
    """
    logger.info("Starting PostgreSQL credential validation step")
    
    success = get_credentials()
    config.success = success
    
    if success:
        logger.info("PostgreSQL credential step completed successfully")
    else:
        logger.error("PostgreSQL credential step failed")
        
    return success
