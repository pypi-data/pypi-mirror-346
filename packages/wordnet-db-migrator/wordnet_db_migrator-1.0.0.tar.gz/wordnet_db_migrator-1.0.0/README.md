# WordNet DB Migrator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)

A utility to migrate WordNet SQLite database to PostgreSQL.

## Overview

WordNet DB Migrator is a tool designed to migrate WordNet databases from SQLite to PostgreSQL. PostgreSQL offers advantages such as multi-user connections and is the default backend database on many platforms like Heroku.

This utility was created to simplify the process of migrating the database whenever a lexicon (a specific dictionary loaded into the WordNet framework) is updated or replaced.

## Features

- Step-by-step migration process with detailed logging
- Automatic schema extraction and conversion
- Foreign key and index preservation
- Data validation during migration
- Progress tracking with estimated time remaining
- Configurable batch sizes for optimal performance

## Requirements

- Python 3.6 or higher
- PostgreSQL server (local or remote)
- **Virtual Environment**: This application is designed to run in a Python virtual environment
- **psycopg2-binary**: The application specifically requires the `psycopg2-binary` package, not the standard `psycopg2` package

## Installation

### Virtual Environment Setup (Recommended)

It is strongly recommended to install and run WordNet DB Migrator in a virtual environment:

```bash
# Create a virtual environment
python -m venv wordnet_db_migrator_venv

# Activate the virtual environment
# On Windows:
wordnet_db_migrator_venv\Scripts\activate
# On macOS/Linux:
source wordnet_db_migrator_venv/bin/activate

# Now install the package
pip install wordnet-db-migrator
```

### Quick Installation

```bash
# Make sure you're in a virtual environment
pip install wordnet-db-migrator
```

### Development Installation

```bash
git clone https://github.com/onareach/wordnet-db-migrator.git
cd wordnet-db-migrator

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

For development with additional tools:

```bash
pip install -e ".[dev]"
```

### Important Note About Dependencies

This project specifically requires `psycopg2-binary` and not the standard `psycopg2` package. Using the standard `psycopg2` package may cause errors. The correct dependency will be installed automatically when you install the package, but if you're installing dependencies manually, make sure to use:

```bash
pip install psycopg2-binary
```

## Quick Start

### 1. Prepare Your WordNet SQLite Database

Ensure you have a WordNet SQLite database file. If you don't have one, you can download it from [WordNet's official website](https://wordnet.princeton.edu/).

### 2. Run the Migration

```bash
wordnet-db-migrator
```

The utility will guide you through the migration process, prompting for:
- SQLite database path
- PostgreSQL credentials
- Other necessary information

### 3. Verify the Migration

After the migration is complete, you can verify the data using the built-in validation tools:

```bash
wordnet-db-migrator --only_step 15
```

## Usage

### Command-Line Options

WordNet DB Migrator supports the following command-line options:

| Option | Description | Default |
|--------|-------------|---------|
| `--help` | Show help message and exit | - |
| `--force` | Skip confirmation prompts | False |
| `--show_db_name` | Show which PostgreSQL database is being worked on in each step | False |
| `--show_logging` | Display logging messages in the terminal | False |
| `--configure` | Run the configuration wizard to set up database paths | - |
| `--sqlite-path PATH` | Path to the SQLite WordNet database | - |
| `--postgres-host HOST` | PostgreSQL server hostname | - |
| `--postgres-port PORT` | PostgreSQL server port | - |
| `--postgres-db NAME` | PostgreSQL database name | - |
| `--list_steps` | Show a list of all available steps and exit | - |
| `--select_step` | Manually select which step to start from | - |
| `--start_step N` | Start from step number N | 1 |
| `--end_step M` | End after step number M | Last step |
| `--only_step N` | Run only step number N | - |
| `--list_data_tables` | Show list of tables that can be inserted | - |
| `--insert_data_table X` | Load data into just the given table | - |

### Examples

```bash
# List all steps
wordnet-db-migrator --list_steps

# Run only step 5
wordnet-db-migrator --only_step 5

# Start from step 3
wordnet-db-migrator --start_step 3

# Run steps 2 through 5
wordnet-db-migrator --start_step 2 --end_step 5

# Skip confirmation prompts
wordnet-db-migrator --force

# Show database name in each step
wordnet-db-migrator --show_db_name

# Show logging messages
wordnet-db-migrator --show_logging

# List all tables
wordnet-db-migrator --list_data_tables

# Insert data into a specific table
wordnet-db-migrator --insert_data_table synsets

# Run the configuration wizard
wordnet-db-migrator --configure

# Specify database paths directly
wordnet-db-migrator --sqlite-path /path/to/wn.db --postgres-host localhost --postgres-port 5432 --postgres-db wordnet
```

## Configuration

### Automatic Configuration

WordNet DB Migrator now features an interactive configuration system:

- On first run, the application will automatically prompt you to configure database paths
- The configuration wizard will detect PostgreSQL settings from environment variables when possible
- PostgreSQL credentials (username and password) are never stored in configuration files
- On subsequent runs, you'll be asked to confirm your configuration

You can also run the configuration wizard manually:

```bash
wordnet-db-migrator --configure
```

### Configuration File

WordNet DB Migrator uses a JSON configuration file located at `~/.wordnet_db_migrator/config.json`. You can modify this file to set default values for various settings:

```json
{
  "sqlite": {
    "path": "/path/to/wordnet/sqlite/database.db"
  },
  "postgres": {
    "host": "localhost",
    "port": 5432,
    "database": "wordnet"
    // Note: username and password are NOT stored
  },
  "output": {
    "directory": "./output",
    "log_level": "info",
    "show_console_logs": false,
    "show_db_name": false
  },
  "application": {
    "batch_size": 1000,
    "force_mode": false
  },
  "last_confirmed": "2025-05-08T12:00:00Z"
}
```

### Environment Variables

WordNet DB Migrator can detect and use the following environment variables:

- `WORDNET_SQLITE_PATH`: Path to the SQLite WordNet database
- `PGHOST` or `POSTGRES_HOST`: PostgreSQL server hostname
- `PGPORT` or `POSTGRES_PORT`: PostgreSQL server port
- `PGDATABASE` or `POSTGRES_DB`: PostgreSQL database name
- `PGUSER` or `POSTGRES_USER`: PostgreSQL username (for display only, not stored)

## Migration Steps

WordNet DB Migrator performs the migration in several steps:

1. Test SQLite database connection
2. Set up PostgreSQL credentials
3. Create WordNet database in PostgreSQL
4. Purge directories (if needed)
5. Extract SQLite schema
6. Analyze dependencies
7. Extract SQLite metadata
8. Generate table scripts
9. Generate foreign key scripts
10. Generate foreign key validators
11. Generate index scripts
12. Run table creation scripts
13. Run index creation scripts
14. Insert data into tables
15. Validate foreign key data
16. Apply foreign keys

## Documentation

For more detailed documentation, see:

- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [Development Guide](docs/development.md)
- [API Reference](docs/api_reference.md)

The full documentation is also available as a searchable website at [https://onareach.github.io/wordnet-db-migrator/](https://onareach.github.io/wordnet-db-migrator/) (powered by MkDocs).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- WordNet for providing the lexical database
- The PostgreSQL team for their excellent database system
- All contributors who have helped with the development of this tool
