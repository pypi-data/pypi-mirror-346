#!/usr/bin/env python3
"""
Basic Migration Example

This example demonstrates how to use WordNet Porter to migrate a WordNet SQLite
database to PostgreSQL.
"""
import os
import sys
import argparse
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from wordnet_db_migrator.config import config
from wordnet_db_migrator import main

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="WordNet Porter Basic Migration Example",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--sqlite-path",
        help="Path to the WordNet SQLite database",
        type=str,
        required=True
    )
    
    parser.add_argument(
        "--pg-host",
        help="PostgreSQL host (default: localhost)",
        type=str,
        default="localhost"
    )
    
    parser.add_argument(
        "--pg-port",
        help="PostgreSQL port (default: 5432)",
        type=int,
        default=5432
    )
    
    parser.add_argument(
        "--pg-database",
        help="PostgreSQL database name (default: wordnet)",
        type=str,
        default="wordnet"
    )
    
    parser.add_argument(
        "--force",
        help="Skip confirmation prompts",
        action="store_true"
    )
    
    return parser.parse_args()

def run_migration():
    """Run the WordNet migration."""
    # Parse command-line arguments
    args = parse_args()
    
    # Update configuration
    config.settings["databases"]["sqlite"]["path"] = args.sqlite_path
    config.settings["databases"]["postgres"]["host"] = args.pg_host
    config.settings["databases"]["postgres"]["port"] = args.pg_port
    config.settings["databases"]["postgres"]["database"] = args.pg_database
    config.force_mode = args.force
    
    # Set up command-line arguments for main.py
    sys.argv = [sys.argv[0]]  # Clear sys.argv
    
    # Add force mode if specified
    if args.force:
        sys.argv.append("--force")
    
    # Run the migration
    print(f"Starting migration from {args.sqlite_path} to PostgreSQL...")
    main.main()
    
    # Check if migration was successful
    if config.success:
        print("\n✅ Migration completed successfully!")
        print(f"The WordNet database has been migrated to PostgreSQL at {args.pg_host}:{args.pg_port}/{args.pg_database}")
    else:
        print("\n❌ Migration failed. See above for details.")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
