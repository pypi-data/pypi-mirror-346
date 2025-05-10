#!/usr/bin/env python3
# wordnet_db_migrator/cli.py
"""
Command-line interface module for WordNet DB Migrator.

This module handles command-line argument parsing and validation for the
WordNet DB Migrator application.
"""
import sys
import logging
from typing import List, Tuple, Optional, Any, Dict, Set, Union

from .config import config

# Set up logging
logger = logging.getLogger(__name__)

def show_help() -> None:
    """
    Display help information and exit.
    
    This function prints usage information and available command-line options,
    then exits the program.
    """
    logger.info("Displaying help information")
    print("""
📘 WordNet Database Migration Tool

Available options:

  General:
  --help                 Show this help message and exit
  --force                Skip confirmation prompts (e.g., when dropping a database)
  --show_db_name         Show which PostgreSQL database is being worked on in each step
  --show_logging         Display logging messages in the terminal (default: off)
  --configure            Run the configuration wizard to set up database paths

  Database Paths:
  --sqlite-path PATH     Path to the SQLite WordNet database (wn.db)
  --postgres-host HOST   PostgreSQL server hostname
  --postgres-port PORT   PostgreSQL server port
  --postgres-db NAME     PostgreSQL database name

  Step Control:
  --list_steps           Show a list of all available steps and exit
  --select_step          Manually select which step to start from
  --start_step N         Start from step number N (e.g., --start_step 4)
  --end_step M           End after step number M (e.g., --end_step 10)
  --only_step N          Run only step number N

  Data Management:
  --list_data_tables     Show list of tables that can be inserted
  --insert_data_table X  Load data into just the given table

Example usage:

  python3 -m wordnet_db_migrator.main --list_steps
  python3 -m wordnet_db_migrator.main --start_step 5 --end_step 9
  python3 -m wordnet_db_migrator.main --only_step 6 --force
  python3 -m wordnet_db_migrator.main --configure
  python3 -m wordnet_db_migrator.main --sqlite-path /path/to/wn.db --postgres-host localhost
""")
    sys.exit(0)

def validate_cli_args() -> None:
    """
    Validate command-line arguments.
    
    This function checks that all provided command-line arguments are valid,
    sets appropriate configuration flags, and handles special global flags
    that short-circuit normal execution.
    
    Raises:
        SystemExit: If invalid arguments are provided or if a short-circuit
                    flag like --help, --list_steps, or --list_data_tables is used.
    """
    logger.info("Validating command-line arguments")
    
    # Define valid command-line flags
    VALID_FLAGS: Set[str] = {
        "--help",
        "--list_steps",
        "--select_step",
        "--start_step",
        "--end_step",
        "--only_step",
        "--force",
        "--list_data_tables",
        "--insert_data_table",
        "--show_db_name",
        "--show_logging",
        "--configure",
        "--sqlite-path",
        "--postgres-host",
        "--postgres-port",
        "--postgres-db"
    }

    # Validate all command-line arguments
    for i, arg in enumerate(sys.argv[1:]):
        if arg.startswith("--"):
            flag = arg.split("=")[0]
            if flag not in VALID_FLAGS:
                logger.error(f"Unrecognized option: {arg}")
                print(f"🚫 Unrecognized option: {arg}")
                print("💡 Use `--help` to see available options.")
                sys.exit(1)
        elif arg.startswith("-"):
            logger.error(f"Invalid single-dash flag: {arg}")
            print(f"🚫 Invalid single-dash flag: {arg}")
            print("💡 All options must begin with '--'. Did you mean '--" + arg[1:] + "'?")
            sys.exit(1)

    # Set configuration flags based on command-line arguments
    config.force_mode = "--force" in sys.argv
    if config.force_mode:
        logger.info("Force mode enabled")
    
    config.SHOW_DB_NAME = "--show_db_name" in sys.argv
    if config.SHOW_DB_NAME:
        logger.info("Database name display enabled")
    
    # Set up logging first so that it's available for all subsequent operations
    config.SHOW_LOGGING = "--show_logging" in sys.argv
    if config.SHOW_LOGGING:
        logger.info("Logging display enabled")
        config.setup_console_logging()
    
    # Handle database path arguments
    if "--sqlite-path" in sys.argv:
        try:
            idx = sys.argv.index("--sqlite-path")
            sqlite_path = sys.argv[idx + 1]
            config.settings["sqlite"]["path"] = sqlite_path
            logger.info(f"SQLite path set to {sqlite_path}")
        except IndexError:
            logger.error("Missing value for --sqlite-path")
            print("🚫 Missing value for --sqlite-path")
            sys.exit(1)
    
    if "--postgres-host" in sys.argv:
        try:
            idx = sys.argv.index("--postgres-host")
            pg_host = sys.argv[idx + 1]
            config.settings["postgres"]["host"] = pg_host
            logger.info(f"PostgreSQL host set to {pg_host}")
        except IndexError:
            logger.error("Missing value for --postgres-host")
            print("🚫 Missing value for --postgres-host")
            sys.exit(1)
    
    if "--postgres-port" in sys.argv:
        try:
            idx = sys.argv.index("--postgres-port")
            pg_port_str = sys.argv[idx + 1]
            try:
                pg_port = int(pg_port_str)
                config.settings["postgres"]["port"] = pg_port
                logger.info(f"PostgreSQL port set to {pg_port}")
            except ValueError:
                logger.error(f"Invalid port number: {pg_port_str}")
                print(f"🚫 Invalid port number: {pg_port_str}")
                sys.exit(1)
        except IndexError:
            logger.error("Missing value for --postgres-port")
            print("🚫 Missing value for --postgres-port")
            sys.exit(1)
    
    if "--postgres-db" in sys.argv:
        try:
            idx = sys.argv.index("--postgres-db")
            pg_db = sys.argv[idx + 1]
            config.settings["postgres"]["database"] = pg_db
            logger.info(f"PostgreSQL database set to {pg_db}")
        except IndexError:
            logger.error("Missing value for --postgres-db")
            print("🚫 Missing value for --postgres-db")
            sys.exit(1)
    
    # Handle configuration wizard
    if "--configure" in sys.argv:
        logger.info("Running configuration wizard")
        if config.prompt_for_configuration(force=config.force_mode):
            print("✅ Configuration saved successfully")
        else:
            print("❌ Failed to save configuration")
            sys.exit(1)
        
    # Handle short-circuit global flags
    if "--help" in sys.argv:
        logger.info("Help requested, showing help message")
        show_help()
        
    if "--list_data_tables" in sys.argv:
        logger.info("Listing data tables and exiting")
        from .steps.step090_insert_data_tables import list_tables
        list_tables()

def parse_cli_args(all_steps: List[Tuple[str, Any]]) -> Tuple[int, int, Optional[int]]:
    """
    Parse command-line arguments and determine which steps to run.
    
    This function processes command-line arguments to determine the range of steps
    to execute or a single step to run.
    
    Args:
        all_steps: List of step definitions (description, function pairs)
        
    Returns:
        Tuple containing:
            - start_index: Index of the first step to run
            - end_index: Index after the last step to run
            - only_step: Index of a single step to run, or None if running a range
            
    Raises:
        SystemExit: If invalid arguments are provided or if a short-circuit
                    flag like --list_steps is used.
    """
    logger.info("Parsing command-line arguments")
    
    # Initialize defaults
    start_index: int = 0
    end_index: int = len(all_steps)
    only_step: Optional[int] = None

    # Show step list if requested
    if "--list_steps" in sys.argv:
        logger.info("Displaying step list")
        print("\n📋 Available Steps:")
        for i, (label, _) in enumerate(all_steps, start=1):
            print(f"  {i:2}. {label}")
        sys.exit(0)

    # Manual step selection mode
    if "--select_step" in sys.argv:
        logger.info("Manual step selection mode activated")
        print("\n🛠️  Manual Step Selection Mode:")
        for i, (label, _) in enumerate(all_steps, start=1):
            print(f"  {i}: {label}")
        try:
            choice = int(input("\n🔢 Enter the step number to start from: "))
            if not (1 <= choice <= len(all_steps)):
                logger.error(f"Invalid step number selected: {choice}")
                raise ValueError(f"Step number must be between 1 and {len(all_steps)}")
                
            start_index = choice - 1
            logger.info(f"Selected to start from step {choice}")
            
        except (ValueError, IndexError) as error:
            logger.error(f"Invalid step selection: {error}")
            print("🚫 Invalid step number. Exiting.")
            sys.exit(1)

    # Start from specific step
    if "--start_step" in sys.argv:
        try:
            idx = sys.argv.index("--start_step")
            step_num = int(sys.argv[idx + 1])
            start_index = step_num - 1
            
            if not (0 <= start_index < len(all_steps)):
                logger.error(f"Invalid start step: {step_num}")
                raise ValueError(f"Start step must be between 1 and {len(all_steps)}")
                
            logger.info(f"Starting from step {step_num}")
            
        except (IndexError, ValueError) as error:
            logger.error(f"Invalid --start_step usage: {error}")
            print("🚫 Invalid --start_step usage")
            sys.exit(1)

    # End after specific step
    if "--end_step" in sys.argv:
        try:
            idx = sys.argv.index("--end_step")
            end_index = int(sys.argv[idx + 1])
            
            if not (1 <= end_index <= len(all_steps)):
                logger.error(f"Invalid end step: {end_index}")
                raise ValueError(f"End step must be between 1 and {len(all_steps)}")
                
            logger.info(f"Ending after step {end_index}")
            
        except (IndexError, ValueError) as error:
            logger.error(f"Invalid --end_step usage: {error}")
            print("🚫 Invalid --end_step usage")
            sys.exit(1)

    # Run only a specific step
    if "--only_step" in sys.argv:
        try:
            idx = sys.argv.index("--only_step")
            step_num = int(sys.argv[idx + 1])
            
            if not (1 <= step_num <= len(all_steps)):
                logger.error(f"Invalid only step: {step_num}")
                raise ValueError(f"Step number must be between 1 and {len(all_steps)}")
                
            only_step = step_num - 1
            logger.info(f"Running only step {step_num}")
            
        except (IndexError, ValueError) as error:
            logger.error(f"Invalid --only_step usage: {error}")
            print("🚫 Invalid --only_step usage")
            sys.exit(1)

    # Log the final decision
    if only_step is not None:
        logger.info(f"Will run only step {only_step + 1}")
    else:
        logger.info(f"Will run steps {start_index + 1} through {end_index}")
        
    return start_index, end_index, only_step
