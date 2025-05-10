#!/usr/bin/env python3
# wordnet_db_migrator/config.py
"""
Configuration module for WordNet DB Migrator.

This module defines the configuration settings for the WordNet DB Migrator application,
including database connection settings, file paths, and application state.
It supports loading configuration from YAML files and command-line arguments.
"""
import getpass
import os
import logging
import json
import yaml  # Keep yaml for backward compatibility
from pathlib import Path
from typing import Optional, Dict, Any, Union, List, Tuple

# Configure logging
# Set up the root logger with no handlers initially
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "sqlite": {
        "path": os.environ.get("WORDNET_SQLITE_PATH", "/Users/davidlong/.wn_data/wn.db")
    },
    "postgres": {
        "host": os.environ.get("PGHOST", "localhost"),
        "port": int(os.environ.get("PGPORT", "5432")),
        "database": os.environ.get("PGDATABASE", "wordnet")
        # Note: username and password are not stored in config
    },
    "output": {
        "directory": "./output",
        "log_level": "info",
        "show_console_logs": False,
        "show_db_name": False
    },
    "application": {
        "batch_size": 1000,
        "max_login_attempts": 3,
        "force_mode": False
    },
    "last_confirmed": None
}

class Config:
    """
    Configuration class for WordNet DB Migrator application.
    
    This class manages all configuration settings, including database connections,
    file paths, and application state. It supports loading configuration from
    YAML files and command-line arguments.
    """
    
    def __init__(self):
        """Initialize configuration with default values and load from files."""
        # Set up configuration directories
        self.user_config_dir: Path = Path.home() / ".wordnet_db_migrator"
        self.user_config_file: Path = self.user_config_dir / "config.json"
        self.legacy_user_config_file: Path = self.user_config_dir / "config.yaml"  # For backward compatibility
        self.project_dir: Path = Path(__file__).parent
        self.project_config_file: Path = self.project_dir / "config.yaml"
        
        # Load configuration
        self.settings: Dict[str, Any] = DEFAULT_CONFIG.copy()
        self._load_config()
        
        # State tracking
        self.success: bool = True
        
        # PostgreSQL credentials (not stored in config file)
        self.pg_user: Optional[str] = None
        self.pg_password: Optional[str] = None
        
        # Set up paths
        self._setup_paths()
        
        # Configure file logging
        self._setup_file_logging()
    
    def _load_config(self) -> None:
        """
        Load configuration from files.
        
        Loads configuration from the following sources in order:
        1. Project config file (wordnet_db_migrator/config.yaml)
        2. Legacy user config file (~/.wordnet_db_migrator/config.yaml) - for backward compatibility
        3. User config file (~/.wordnet_db_migrator/config.json)
        """
        try:
            # Load project config if it exists (YAML)
            if self.project_config_file.exists():
                logger.debug(f"Loading project config from {self.project_config_file}")
                with open(self.project_config_file, 'r') as f:
                    project_config = yaml.safe_load(f)
                    if project_config:
                        self._update_nested_dict(self.settings, project_config)
            
            # Load legacy user config if it exists (YAML) - for backward compatibility
            if self.legacy_user_config_file.exists() and not self.user_config_file.exists():
                logger.debug(f"Loading legacy user config from {self.legacy_user_config_file}")
                with open(self.legacy_user_config_file, 'r') as f:
                    legacy_user_config = yaml.safe_load(f)
                    if legacy_user_config:
                        # Convert from old format to new format
                        if "databases" in legacy_user_config:
                            if "sqlite" in legacy_user_config["databases"]:
                                self.settings["sqlite"] = legacy_user_config["databases"]["sqlite"]
                            if "postgres" in legacy_user_config["databases"]:
                                pg_config = legacy_user_config["databases"]["postgres"]
                                # Only copy host, port, and database (not user/password)
                                if "host" in pg_config:
                                    self.settings["postgres"]["host"] = pg_config["host"]
                                if "port" in pg_config:
                                    self.settings["postgres"]["port"] = pg_config["port"]
                                if "database" in pg_config:
                                    self.settings["postgres"]["database"] = pg_config["database"]
                        
                        # Copy other sections directly
                        if "output" in legacy_user_config:
                            self.settings["output"] = legacy_user_config["output"]
                        if "application" in legacy_user_config:
                            self.settings["application"] = legacy_user_config["application"]
                
                # Save in new JSON format
                self.save_config()
                logger.info(f"Converted legacy YAML config to new JSON format")
            
            # Load user config if it exists (JSON)
            if self.user_config_file.exists():
                logger.debug(f"Loading user config from {self.user_config_file}")
                with open(self.user_config_file, 'r') as f:
                    user_config = json.load(f)
                    if user_config:
                        self._update_nested_dict(self.settings, user_config)
        
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            print(f"⚠️ Error loading configuration: {e}")
    
    def _update_nested_dict(self, d: Dict[str, Any], u: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a nested dictionary with values from another dictionary.
        
        Args:
            d: The dictionary to update
            u: The dictionary with new values
            
        Returns:
            The updated dictionary
        """
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._update_nested_dict(d[k], v)
            else:
                d[k] = v
        return d
    
    def detect_environment_variables(self) -> Dict[str, Any]:
        """
        Detect PostgreSQL settings from environment variables.
        
        Returns:
            Dict containing detected PostgreSQL settings
        """
        detected = {}
        
        # Check for SQLite path
        sqlite_path = os.environ.get("WORDNET_SQLITE_PATH")
        if sqlite_path:
            detected["sqlite_path"] = sqlite_path
        
        # Check for PostgreSQL host
        pg_host = os.environ.get("PGHOST") or os.environ.get("POSTGRES_HOST")
        if pg_host:
            detected["pg_host"] = pg_host
        
        # Check for PostgreSQL port
        pg_port_str = os.environ.get("PGPORT") or os.environ.get("POSTGRES_PORT")
        if pg_port_str:
            try:
                detected["pg_port"] = int(pg_port_str)
            except ValueError:
                logger.warning(f"Invalid PostgreSQL port in environment: {pg_port_str}")
        
        # Check for PostgreSQL database
        pg_db = os.environ.get("PGDATABASE") or os.environ.get("POSTGRES_DB")
        if pg_db:
            detected["pg_database"] = pg_db
        
        # Check for PostgreSQL user (for display only, not stored)
        pg_user = os.environ.get("PGUSER") or os.environ.get("POSTGRES_USER")
        if pg_user:
            detected["pg_user"] = pg_user
        
        return detected
    
    def _setup_paths(self) -> None:
        """Set up paths based on configuration."""
        # Create user config directory if it doesn't exist
        os.makedirs(self.user_config_dir, exist_ok=True)
        
        # Get output directory from settings
        output_dir_str = self.settings["output"]["directory"]
        output_dir = Path(output_dir_str)
        
        # Make relative paths relative to the project directory
        if not output_dir.is_absolute():
            output_dir = self.project_dir / output_dir
        
        # Set up paths
        self.output_dir: Path = output_dir
        self.sql_dir: Path = self.output_dir / "sql"
        self.logs_dir: Path = self.output_dir / "logs"
        self.schemas_dir: Path = self.output_dir / "schemas"
        self.sql_tables_dir: Path = self.sql_dir / "tables"
        self.sql_indexes_dir: Path = self.sql_dir / "indexes"
        self.sql_foreign_keys_dir: Path = self.sql_dir / "foreign_keys"
        self.sql_fk_validate_dir: Path = self.sql_dir / "fk_validate"
        
        # Create directories
        for directory in [self.output_dir, self.sql_dir, self.logs_dir, 
                         self.schemas_dir, self.sql_tables_dir, 
                         self.sql_indexes_dir, self.sql_foreign_keys_dir, 
                         self.sql_fk_validate_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def _setup_file_logging(self) -> None:
        """Set up file logging for the application."""
        try:
            # Get log level from settings
            log_level_str = self.settings["output"]["log_level"].upper()
            log_level = getattr(logging, log_level_str, logging.INFO)
            
            # Set root logger level
            logging.getLogger().setLevel(log_level)
            
            # Add file handler to root logger
            file_handler = logging.FileHandler(
                self.logs_dir / "wordnet_db_migrator.log", 
                mode='a'
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logging.getLogger().addHandler(file_handler)
            
            logger.info("File logging configured")
        except Exception as error:
            print(f"⚠️ Failed to set up file logging: {error}")
            
    def setup_console_logging(self) -> None:
        """
        Set up console logging if show_console_logs is True.
        
        This method adds a console handler to the root logger if show_console_logs is True.
        """
        if self.settings["output"]["show_console_logs"]:
            # Add console handler to root logger
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logging.getLogger().addHandler(console_handler)
            logger.info("Console logging configured")

    def _format_yaml(self, data, indent=0):
        """
        Format data as YAML with proper indentation.
        
        Args:
            data: The data to format
            indent: The indentation level
            
        Returns:
            The formatted YAML string
        """
        result = ""
        spaces = " " * indent
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    result += f"{spaces}{key}:\n"
                    result += self._format_yaml(value, indent + 2)
                elif value is None:
                    result += f"{spaces}{key}: null\n"
                elif isinstance(value, bool):
                    result += f"{spaces}{key}: {str(value).lower()}\n"
                elif isinstance(value, (int, float)):
                    result += f"{spaces}{key}: {value}\n"
                else:
                    result += f"{spaces}{key}: \"{value}\"\n"
        
        return result
    
    def _write_yaml_file(self, file):
        """
        Write the entire YAML file with proper formatting.
        
        Args:
            file: The file to write to
        """
        # Create a manually formatted YAML string
        yaml_content = "sqlite:\n"
        
        # Manually format the sqlite section with proper indentation
        yaml_content += f"  path: \"{self.settings['sqlite']['path']}\"\n"
        
        # Manually format the postgres section with proper indentation
        yaml_content += "\npostgres:\n"
        yaml_content += f"  host: \"{self.settings['postgres']['host']}\"\n"
        yaml_content += f"  port: {self.settings['postgres']['port']}\n"
        yaml_content += f"  database: \"{self.settings['postgres']['database']}\"\n"
        
        # Output section
        yaml_content += "\noutput:\n"
        for key, value in self.settings["output"].items():
            if isinstance(value, bool):
                yaml_content += f"  {key}: {str(value).lower()}\n"
            elif value is None:
                yaml_content += f"  {key}: null\n"
            elif isinstance(value, (int, float)):
                yaml_content += f"  {key}: {value}\n"
            else:
                yaml_content += f"  {key}: \"{value}\"\n"
        
        # Application section
        yaml_content += "\napplication:\n"
        for key, value in self.settings["application"].items():
            if isinstance(value, bool):
                yaml_content += f"  {key}: {str(value).lower()}\n"
            elif value is None:
                yaml_content += f"  {key}: null\n"
            elif isinstance(value, (int, float)):
                yaml_content += f"  {key}: {value}\n"
            else:
                yaml_content += f"  {key}: \"{value}\"\n"
        
        # Write the content to the file
        file.write(yaml_content)
    
    def save_config(self) -> bool:
        """
        Save current configuration to user config file.
        
        Returns:
            bool: True if configuration was saved successfully, False otherwise.
        """
        try:
            # Create user config directory if it doesn't exist
            os.makedirs(self.user_config_dir, exist_ok=True)
            
            # Create a clean config dictionary without credentials
            clean_config = {
                "sqlite": self.settings["sqlite"],
                "postgres": {
                    "host": self.settings["postgres"]["host"],
                    "port": self.settings["postgres"]["port"],
                    "database": self.settings["postgres"]["database"]
                    # Explicitly not including user and password
                },
                "output": self.settings["output"],
                "application": self.settings["application"],
                "last_confirmed": self.settings["last_confirmed"]
            }
            
            # Save configuration to user config file as JSON
            with open(self.user_config_file, 'w') as f:
                json.dump(clean_config, f, indent=2)
            
            logger.info(f"Configuration saved to {self.user_config_file}")
            print(f"✅ Configuration saved to {self.user_config_file}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            print(f"❌ Error saving configuration: {e}")
            return False

    def prompt_for_configuration(self, force: bool = False) -> bool:
        """
        Prompt user for configuration settings.
        
        Args:
            force: If True, skip confirmation prompts
            
        Returns:
            bool: True if configuration was successfully updated, False otherwise
        """
        print("\n📋 WordNet DB Migrator Configuration")
        
        # Check if this is first run
        first_run = not self.user_config_file.exists()
        
        # Detect environment variables
        detected = self.detect_environment_variables()
        
        # SQLite database path
        if first_run or not force:
            current_sqlite_path = self.settings["sqlite"]["path"]
            detected_sqlite_path = detected.get("sqlite_path")
            
            if detected_sqlite_path:
                print(f"\nDetected SQLite database path: {detected_sqlite_path}")
                use_detected = input("Use this path? (Y/n): ").strip().lower() != 'n'
                if use_detected:
                    self.settings["sqlite"]["path"] = detected_sqlite_path
                else:
                    self._prompt_for_sqlite_path()
            else:
                print(f"\nCurrent SQLite database path: {current_sqlite_path}")
                if first_run or input("Change this path? (y/N): ").strip().lower() == 'y':
                    self._prompt_for_sqlite_path()
        
        # PostgreSQL connection details
        if first_run or not force:
            self._prompt_for_postgres_settings(detected)
        
        # Save configuration
        if self.save_config():
            self.settings["last_confirmed"] = self._get_timestamp()
            return True
        return False
    
    def _prompt_for_sqlite_path(self) -> None:
        """Prompt user for SQLite database path."""
        while True:
            sqlite_path = input("Enter path to SQLite WordNet database (wn.db): ").strip()
            if not sqlite_path:
                print("❌ Path cannot be empty")
                continue
            
            path = Path(sqlite_path)
            if not path.exists():
                print(f"⚠️ Warning: File {sqlite_path} does not exist")
                if input("Use this path anyway? (y/N): ").strip().lower() != 'y':
                    continue
            
            self.settings["sqlite"]["path"] = sqlite_path
            break
    
    def _prompt_for_postgres_settings(self, detected: Dict[str, Any]) -> None:
        """
        Prompt user for PostgreSQL connection settings.
        
        Args:
            detected: Dictionary of detected PostgreSQL settings from environment variables
        """
        print("\n🐘 PostgreSQL Connection Settings")
        
        # Host
        current_host = self.settings["postgres"]["host"]
        detected_host = detected.get("pg_host")
        
        if detected_host:
            print(f"Detected PostgreSQL host: {detected_host}")
            use_detected = input("Use this host? (Y/n): ").strip().lower() != 'n'
            if use_detected:
                self.settings["postgres"]["host"] = detected_host
            else:
                self.settings["postgres"]["host"] = input(f"Enter PostgreSQL host [{current_host}]: ").strip() or current_host
        else:
            self.settings["postgres"]["host"] = input(f"Enter PostgreSQL host [{current_host}]: ").strip() or current_host
        
        # Port
        current_port = self.settings["postgres"]["port"]
        detected_port = detected.get("pg_port")
        
        if detected_port:
            print(f"Detected PostgreSQL port: {detected_port}")
            use_detected = input("Use this port? (Y/n): ").strip().lower() != 'n'
            if use_detected:
                self.settings["postgres"]["port"] = detected_port
            else:
                port_str = input(f"Enter PostgreSQL port [{current_port}]: ").strip() or str(current_port)
                try:
                    self.settings["postgres"]["port"] = int(port_str)
                except ValueError:
                    print(f"⚠️ Invalid port number: {port_str}, using default: {current_port}")
                    self.settings["postgres"]["port"] = current_port
        else:
            port_str = input(f"Enter PostgreSQL port [{current_port}]: ").strip() or str(current_port)
            try:
                self.settings["postgres"]["port"] = int(port_str)
            except ValueError:
                print(f"⚠️ Invalid port number: {port_str}, using default: {current_port}")
                self.settings["postgres"]["port"] = current_port
        
        # Database
        current_db = self.settings["postgres"]["database"]
        detected_db = detected.get("pg_database")
        
        if detected_db:
            print(f"Detected PostgreSQL database: {detected_db}")
            use_detected = input("Use this database? (Y/n): ").strip().lower() != 'n'
            if use_detected:
                self.settings["postgres"]["database"] = detected_db
            else:
                self.settings["postgres"]["database"] = input(f"Enter PostgreSQL database [{current_db}]: ").strip() or current_db
        else:
            self.settings["postgres"]["database"] = input(f"Enter PostgreSQL database [{current_db}]: ").strip() or current_db
        
        # Note about credentials
        detected_user = detected.get("pg_user")
        if detected_user:
            print(f"\nDetected PostgreSQL username: {detected_user}")
            print("Note: PostgreSQL username and password will be prompted for at runtime and not stored in configuration.")
        else:
            print("\nNote: PostgreSQL username and password will be prompted for at runtime and not stored in configuration.")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def prompt_credentials(self) -> bool:
        """
        Prompt for PostgreSQL credentials.
        
        Returns:
            bool: True if credentials were successfully obtained, False otherwise.
        """
        return self.ensure_pg_credentials()

    def ensure_pg_credentials(self) -> bool:
        """
        Ensure PostgreSQL credentials are available, prompting if necessary.
        
        Returns:
            bool: True if credentials are available, False otherwise.
        """
        # Check if credentials are already in instance variables
        if self.pg_user and self.pg_password:
            logger.debug("Using PostgreSQL credentials from instance variables")
            return True
            
        try:
            # Try to use the dedicated credentials module
            from .steps import step020_postgres_credentials
            logger.info("Getting PostgreSQL credentials from credentials module")
            return step020_postgres_credentials.get_credentials()
        except ImportError:
            logger.warning("Could not import credentials module, using fallback prompt")
            print("⚠️ Could not import credentials module")

            # Fallback prompt
            print("\n🔐 PostgreSQL Connection")
            user = input("PostgreSQL username: ").strip()
            password = getpass.getpass("PostgreSQL password: ")

            if not user:
                logger.error("PostgreSQL username cannot be empty")
                self.success = False
                return False
            
            # Store credentials in instance variables (not in settings)
            self.pg_user = user
            self.pg_password = password

            logger.info("PostgreSQL credentials obtained via fallback prompt")
            return True
    
    # Property getters and setters for backward compatibility
    
    @property
    def SQLITE_PATH(self) -> str:
        """Get SQLite database path."""
        return self.settings["sqlite"]["path"]
    
    @SQLITE_PATH.setter
    def SQLITE_PATH(self, path: str) -> None:
        """Set SQLite database path."""
        self.settings["sqlite"]["path"] = path
    
    @property
    def PG_HOST(self) -> str:
        """Get PostgreSQL host."""
        return self.settings["postgres"]["host"]
    
    @PG_HOST.setter
    def PG_HOST(self, host: str) -> None:
        """Set PostgreSQL host."""
        self.settings["postgres"]["host"] = host
    
    @property
    def PG_PORT(self) -> int:
        """Get PostgreSQL port."""
        return self.settings["postgres"]["port"]
    
    @PG_PORT.setter
    def PG_PORT(self, port: int) -> None:
        """Set PostgreSQL port."""
        self.settings["postgres"]["port"] = port
    
    @property
    def PG_DATABASE(self) -> str:
        """Get PostgreSQL database name."""
        return self.settings["postgres"]["database"]
    
    @PG_DATABASE.setter
    def PG_DATABASE(self, database: str) -> None:
        """Set PostgreSQL database name."""
        self.settings["postgres"]["database"] = database
    
    @property
    def SHOW_DB_NAME(self) -> bool:
        """Get show database name setting."""
        return self.settings["output"]["show_db_name"]
    
    @SHOW_DB_NAME.setter
    def SHOW_DB_NAME(self, value: bool) -> None:
        """Set show database name setting."""
        self.settings["output"]["show_db_name"] = value
    
    @property
    def SHOW_LOGGING(self) -> bool:
        """Get show logging setting."""
        return self.settings["output"]["show_console_logs"]
    
    @SHOW_LOGGING.setter
    def SHOW_LOGGING(self, value: bool) -> None:
        """Set show logging setting."""
        self.settings["output"]["show_console_logs"] = value
    
    @property
    def MAX_LOGIN_ATTEMPTS(self) -> int:
        """Get maximum login attempts."""
        return self.settings["application"]["max_login_attempts"]
    
    @MAX_LOGIN_ATTEMPTS.setter
    def MAX_LOGIN_ATTEMPTS(self, value: int) -> None:
        """Set maximum login attempts."""
        self.settings["application"]["max_login_attempts"] = value
    
    @property
    def BATCH_SIZE(self) -> int:
        """Get batch size."""
        return self.settings["application"]["batch_size"]
    
    @BATCH_SIZE.setter
    def BATCH_SIZE(self, value: int) -> None:
        """Set batch size."""
        self.settings["application"]["batch_size"] = value
    
    @property
    def force_mode(self) -> bool:
        """Get force mode setting."""
        return self.settings["application"]["force_mode"]
    
    @force_mode.setter
    def force_mode(self, value: bool) -> None:
        """Set force mode setting."""
        self.settings["application"]["force_mode"] = value

# Expose the instance directly
config = Config()
