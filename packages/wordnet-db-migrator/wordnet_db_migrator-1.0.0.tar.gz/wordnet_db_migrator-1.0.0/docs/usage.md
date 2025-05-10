# Usage Guide

This guide provides detailed instructions for using WordNet DB Migrator.

## Basic Usage

The simplest way to use WordNet DB Migrator is:

```bash
wordnet-db-migrator --sqlite-path /path/to/wordnet.db
```

This will:
1. Connect to the SQLite database
2. Prompt for PostgreSQL credentials
3. Create a new PostgreSQL database
4. Migrate the schema and data
5. Validate the migration

## Configuration

### Command-Line Options

WordNet DB Migrator supports the following command-line options:

| Option | Description | Default |
|--------|-------------|---------|
| `--help` | Show help message and exit | - |
| `--force` | Skip confirmation prompts | False |
| `--show_db_name` | Show which PostgreSQL database is being worked on in each step | False |
| `--show_logging` | Display logging messages in the terminal | False |
| `--list_steps` | Show a list of all available steps and exit | - |
| `--select_step` | Manually select which step to start from | - |
| `--start_step N` | Start from step number N | 1 |
| `--end_step M` | End after step number M | Last step |
| `--only_step N` | Run only step number N | - |
| `--list_data_tables` | Show list of tables that can be inserted | - |
| `--insert_data_table X` | Load data into just the given table | - |

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

You can run specific steps using the `--only-step`, `--start-step`, and `--end-step` options.

## Examples

### Basic Migration

```bash
wordnet-db-migrator
```

This will use the SQLite path from the configuration file or prompt for it if not set.

### Specifying SQLite Path via Environment Variable

```bash
export WORDNET_SQLITE_PATH=/path/to/wordnet.db
wordnet-db-migrator
```

### Running Specific Steps

```bash
# List all steps
wordnet-db-migrator --list_steps

# Run only step 5
wordnet-db-migrator --only_step 5

# Start from step 3
wordnet-db-migrator --start_step 3

# Run steps 2 through 5
wordnet-db-migrator --start_step 2 --end_step 5
```

### Forcing Operations

```bash
wordnet-db-migrator --force
```

This will skip confirmation prompts, such as when dropping a database.

### Showing Database Name

```bash
wordnet-db-migrator --show_db_name
```

This will show which PostgreSQL database is being worked on in each step.

### Showing Logging Messages

```bash
wordnet-db-migrator --show_logging
```

This will display logging messages in the terminal.

### Data Management

```bash
# List all tables
wordnet-db-migrator --list_data_tables

# Insert data into a specific table
wordnet-db-migrator --insert_data_table synsets
```

## Troubleshooting

### Common Issues

#### SQLite Database Not Found

If you see an error like:

```
Error: SQLite database not found: /path/to/wordnet.db
```

Make sure the path to your SQLite database is correct and the file exists.

#### PostgreSQL Connection Failed

If you see an error like:

```
Error: Could not connect to PostgreSQL server
```

Make sure your PostgreSQL server is running and the credentials are correct.

#### Permission Denied

If you see an error like:

```
Error: Permission denied when creating database
```

Make sure the PostgreSQL user has the necessary permissions to create databases.

### Getting Help

If you encounter any issues not covered in this guide, please:

1. Check the [GitHub Issues](https://github.com/onareach/wordnet-db-migrator/issues) to see if someone else has reported the same problem
2. If not, create a new issue with a detailed description of the problem

## Next Steps

After successfully migrating your WordNet database to PostgreSQL, you can:

1. Connect to the PostgreSQL database using your favorite client
2. Explore the data using SQL queries
3. Use the database in your applications
