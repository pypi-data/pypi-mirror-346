#!/usr/bin/env python3
# wordnet_db_migrator/steps/step035_purge_directories.py
"""
Step 4: Purge Output Directories

This module handles the purging of output directories before generating new content.
It removes all files and subdirectories in the specified directories without
deleting the directories themselves.
"""
import logging
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Union, Dict, Any, Tuple, Set

from ..config import config

# Set up logging
logger = logging.getLogger(__name__)

def purge_directory(directory: Path) -> bool:
    """
    Remove all files and subdirectories in a directory without deleting the directory itself.
    
    Args:
        directory: Path to the directory to purge
        
    Returns:
        bool: True if purge was successful, False otherwise
    """
    logger.info(f"Purging directory: {directory}")
    
    if not directory.exists():
        logger.info(f"Directory does not exist, skipping: {directory}")
        return True
    
    try:
        # Remove all contents
        for item in directory.iterdir():
            if item.is_dir():
                logger.debug(f"Removing subdirectory: {item}")
                shutil.rmtree(item)
            else:
                logger.debug(f"Removing file: {item}")
                item.unlink()
        
        logger.info(f"Successfully purged directory: {directory}")
        print(f"✅ Purged directory: {directory}")
        return True
    except Exception as error:
        logger.error(f"Failed to purge directory {directory}: {error}")
        return False

def run(force: Optional[bool] = None) -> bool:
    """
    Purge output directories if force flag is set or user confirms.
    
    This function identifies directories that need to be purged, asks for user
    confirmation (unless force mode is enabled), and then purges each directory.
    
    Args:
        force: Override the global force mode setting if provided
        
    Returns:
        bool: True if all directories were purged successfully or if purge was skipped,
              False if an error occurred
    """
    logger.info("Starting directory purge step")
    
    # Use passed parameter if provided, otherwise use global config
    force_mode = force if force is not None else config.force_mode
    logger.info(f"Force mode: {force_mode}")
    
    # Directories to purge
    directories = [
        config.sql_dir,
        config.logs_dir,
        config.schemas_dir
    ]
    
    # Add subdirectories of sql_dir if they exist
    sql_subdirs = [
        config.sql_dir / "tables",
        config.sql_dir / "indexes",
        config.sql_dir / "foreign_keys",
        config.sql_dir / "fk_validate"
    ]
    
    all_dirs = [d for d in directories + sql_subdirs if d.exists()]
    
    if not all_dirs:
        logger.info("No directories to purge - they don't exist yet")
        print("No directories to purge - they don't exist yet.")
        return True
    
    if force_mode:
        logger.info("Force mode enabled - purging directories automatically")
        print("⚠️ Force mode enabled - purging directories automatically...")
        should_purge = True
    else:
        # Ask for confirmation
        logger.info("Asking user for confirmation to purge directories")
        print("⚠️ This will delete all files in the following directories:")
        for directory in all_dirs:
            print(f"  - {directory}")
        
        response = input("\nProceed with purge? [n/Y]: ").strip().lower()
        should_purge = response in ['y', 'yes', '']  # Empty string means user just pressed Enter (default Y)
        
        if should_purge:
            logger.info("User confirmed directory purge")
        else:
            logger.info("User declined directory purge")
    
    if not should_purge:
        print("⏭️ Skipping directory purge")
        return True
    
    # Purge each directory
    try:
        all_successful = True
        
        for directory in all_dirs:
            success = purge_directory(directory)
            if not success:
                all_successful = False
                print(f"❌ Failed to purge directory: {directory}")
        
        if all_successful:
            logger.info("All directories purged successfully")
            print("\n✅ All directories purged successfully")
            return True
        else:
            logger.error("Failed to purge one or more directories")
            print("\n⚠️ Failed to purge one or more directories")
            config.success = False
            return False
            
    except Exception as error:
        logger.exception("Unexpected error during directory purge")
        print(f"❌ Failed to purge directories: {error}")
        config.success = False
        return False
