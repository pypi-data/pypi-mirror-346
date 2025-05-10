#!/usr/bin/env python3
# wordnet_db_migrator/main.py
"""
WordNet DB Migrator - SQLite to PostgreSQL Migration Utility

This is the main entry point for the WordNet DB Migrator application, which
coordinates the step-by-step process of migrating a WordNet SQLite database
to PostgreSQL.
"""
import sys
import logging
from typing import List, Tuple, Callable, Optional, Any, Dict, Union

from .bootstrap import setup, print_header
from .config import config
from .cli import validate_cli_args, parse_cli_args, show_help

# Set up logging
logger = logging.getLogger(__name__)

# Import all steps
from .steps import (
    step010_test_sqlite_connection,
    step020_postgres_credentials,
    step030_create_postgres_database,
    step035_purge_directories,
    step040_extract_sqlite_schema,
    step045_analyze_dependencies,
    step050_extract_sqlite_metadata,
    step060_generate_tables,
    step065_generate_foreign_keys,
    step067_generate_foreign_key_validators,
    step068_generate_indexes,
    step070_run_table_scripts,
    step080_run_index_scripts,
    step090_insert_data_tables,
    step095_validate_foreign_key_data,
    step100_apply_foreign_keys
)

# Type alias for a step function
StepFunction = Callable[[], bool]
# Type alias for a step definition (description and function)
StepDefinition = Tuple[str, StepFunction]

def main() -> None:
    """
    Main function to coordinate the WordNet migration process.
    
    This function:
    1. Processes command-line arguments
    2. Sets up the environment
    3. Executes the selected migration steps
    4. Reports on the success or failure of the migration
    """
    logger.info("Starting WordNet DB Migrator")
    
    # Validate command-line arguments
    logger.info("Validating command-line arguments")
    validate_cli_args()
    
    # Define all steps with descriptions
    ALL_STEPS: List[StepDefinition] = [
        ("Step 1:  Test SQLite Database Connection", step010_test_sqlite_connection.run),
        ("Step 2:  Login to PostgreSQL", step020_postgres_credentials.run),
        ("Step 3:  Create WordNet Database in PostgreSQL", step030_create_postgres_database.run),
        ("Step 4:  Purge Directories", step035_purge_directories.run),
        ("Step 5:  Extract SQLite Schema", step040_extract_sqlite_schema.run),
        ("Step 6:  Analyze Dependencies", step045_analyze_dependencies.run),
        ("Step 7:  Extract SQLite Metadata", step050_extract_sqlite_metadata.run),
        ("Step 8:  Generate Table Scripts", step060_generate_tables.run),
        ("Step 9:  Generate Foreign Key Scripts", step065_generate_foreign_keys.run),
        ("Step 10: Generate Foreign Key Validators", step067_generate_foreign_key_validators.run),
        ("Step 11: Generate Index Scripts", step068_generate_indexes.run),
        ("Step 12: Run Table Creation Scripts", step070_run_table_scripts.run),
        ("Step 13: Run Index Creation Scripts", step080_run_index_scripts.run),
        ("Step 14: Insert Data into Tables", step090_insert_data_tables.run),
        ("Step 15: Validate Foreign Key Data", step095_validate_foreign_key_data.run),
        ("Step 16: Apply Foreign Keys", step100_apply_foreign_keys.run),
    ]
    
    # Parse command-line arguments to determine which steps to run
    logger.info("Parsing command-line arguments to determine steps to run")
    start_index, end_index, only_step = parse_cli_args(ALL_STEPS)
    
    # Setup environment first
    logger.info("Setting up environment")
    print_header("Setting up environment...")
    setup()
    if not config.success:
        logger.error("Bootstrap failed")
        exit("❌ Bootstrap failed - please fix the issues before continuing.")
    
    # Check if this is the first run and configuration is needed
    if not config.user_config_file.exists() and "--configure" not in sys.argv:
        logger.info("First run detected, prompting for configuration")
        print_header("First Run Configuration")
        print("This appears to be the first time you're running WordNet DB Migrator.")
        print("Let's set up your database paths.")
        
        if config.prompt_for_configuration(force=config.force_mode):
            print("✅ Configuration saved successfully")
        else:
            print("❌ Failed to save configuration")
            exit(1)
    
    # Check if configuration needs to be confirmed (if not first run and not forced)
    elif config.user_config_file.exists() and not config.force_mode and "--configure" not in sys.argv:
        # Check if configuration was confirmed recently
        last_confirmed = config.settings.get("last_confirmed")
        if not last_confirmed:
            logger.info("Configuration needs confirmation")
            print_header("Configuration Confirmation")
            print("Please confirm your database configuration:")
            
            print(f"\nSQLite database path: {config.settings['sqlite']['path']}")
            print(f"PostgreSQL host: {config.settings['postgres']['host']}")
            print(f"PostgreSQL port: {config.settings['postgres']['port']}")
            print(f"PostgreSQL database: {config.settings['postgres']['database']}")
            
            if input("\nIs this configuration correct? (Y/n): ").strip().lower() == 'n':
                if config.prompt_for_configuration(force=False):
                    print("✅ Configuration updated successfully")
                else:
                    print("❌ Failed to update configuration")
                    exit(1)
            else:
                # Update last_confirmed timestamp
                config.settings["last_confirmed"] = config._get_timestamp()
                config.save_config()
    
    # Run the selected steps
    if only_step is not None:
        # Run only one specific step
        step_desc = ALL_STEPS[only_step][0]
        step_func = ALL_STEPS[only_step][1]
        
        logger.info(f"Running single step: {step_desc}")
        print_header(f"Running {step_desc}")
        
        step_func()
        
        if not config.success:
            logger.error(f"Step failed: {step_desc}")
    else:
        # Run a range of steps
        logger.info(f"Running steps {start_index+1} through {end_index}")
        
        for i, (step_desc, step_func) in enumerate(ALL_STEPS[start_index:end_index], start=start_index+1):
            logger.info(f"Starting step {i}: {step_desc}")
            print_header(f"{step_desc}")
            
            step_func()
            
            if not config.success:
                logger.error(f"Step {i} failed: {step_desc}")
                print(f"\n❌ Stopping after {step_desc} due to error.")
                exit(1)
            
            logger.info(f"Completed step {i}: {step_desc}")
    
    # Report final status
    if config.success:
        logger.info("All selected steps completed successfully")
        print("\n✅ All selected steps completed successfully!")
    else:
        logger.error("One or more steps failed")
        print("\n❌ One or more steps failed. See above for details.")
        exit(1)

if __name__ == "__main__":
    main()
