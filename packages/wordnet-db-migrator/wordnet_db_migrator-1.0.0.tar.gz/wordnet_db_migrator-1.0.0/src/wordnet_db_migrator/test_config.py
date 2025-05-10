#!/usr/bin/env python3
"""
Test script for the WordNet DB Migrator configuration system.

This script tests the JSON-based configuration system by:
1. Loading the configuration
2. Displaying the current settings
3. Modifying a setting
4. Saving the configuration
5. Reloading to verify the changes
"""
import os
from pathlib import Path

# Try to import yaml, install if not available
try:
    import yaml
    print("✅ PyYAML is installed")
except ImportError:
    print("⚠️ PyYAML is not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "pyyaml>=6.0"])
    import yaml
    print("✅ PyYAML has been installed")

# Import the configuration module
from wordnet_db_migrator.config import config

def main():
    """Run the configuration system test."""
    print("\n🔍 Testing WordNet DB Migrator Configuration System\n")
    
    # Display current configuration
    print("Current Configuration:")
    print(f"SQLite Path: {config.SQLITE_PATH}")
    print(f"PostgreSQL Host: {config.PG_HOST}")
    print(f"PostgreSQL Port: {config.PG_PORT}")
    print(f"PostgreSQL Database: {config.PG_DATABASE}")
    print(f"Batch Size: {config.BATCH_SIZE}")
    print(f"Force Mode: {config.force_mode}")
    print(f"Show Console Logs: {config.SHOW_LOGGING}")
    print(f"Show DB Name: {config.SHOW_DB_NAME}")
    
    # Check if user config exists
    user_config_file = Path.home() / ".wordnet_db_migrator" / "config.json"
    if user_config_file.exists():
        print(f"\nUser configuration file exists at: {user_config_file}")
        
        # Display user configuration
        with open(user_config_file, 'r') as f:
            user_config = yaml.safe_load(f)
            print("\nUser Configuration Content:")
            print(yaml.dump(user_config, default_flow_style=False))
    else:
        print(f"\nUser configuration file does not exist at: {user_config_file}")
    
    # Modify a setting
    print("\nModifying batch size to 2000...")
    config.BATCH_SIZE = 2000
    
    # Save the configuration
    print("\nSaving configuration...")
    config.save_config()
    
    # Reload the configuration
    print("\nReloading configuration to verify changes...")
    from importlib import reload
    import wordnet_db_migrator.config as config_module
    reload(config_module)
    from wordnet_db_migrator.config import config as new_config
    
    # Verify the changes
    print(f"\nNew Batch Size: {new_config.BATCH_SIZE}")
    if new_config.BATCH_SIZE == 2000:
        print("✅ Configuration was successfully saved and reloaded")
    else:
        print("❌ Configuration was not saved correctly")
    
    print("\n✅ Configuration system test complete")

if __name__ == "__main__":
    main()
