# WordNet DB Migrator

A utility to migrate WordNet database from SQLite to PostgreSQL.

## Overview

WordNet DB Migrator is a tool designed to help you migrate a WordNet database from SQLite to PostgreSQL. It handles the entire migration process, including:

- Extracting the schema from the SQLite database
- Creating tables in PostgreSQL
- Migrating data
- Setting up indexes and foreign keys
- Validating the migration

## Features

- **Step-by-Step Migration**: The migration process is divided into logical steps that can be run individually or as a complete sequence.
- **Configurable**: Easily configure database connections and migration options.
- **Validation**: Built-in validation to ensure data integrity after migration.
- **Detailed Logging**: Comprehensive logging of the migration process.

## Quick Start

```bash
# Install the package
pip install wordnet-db-migrator

# Run the migration
wordnet-db-migrator --sqlite-path /path/to/wordnet.db
```

For more detailed instructions, see the [Installation](installation.md) and [Usage](usage.md) guides.

## Documentation

- [Installation Guide](installation.md): How to install WordNet DB Migrator
- [Usage Guide](usage.md): How to use WordNet DB Migrator
- [Development Guide](development.md): How to contribute to WordNet DB Migrator
- [API Reference](api_reference.md): Detailed API documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.
