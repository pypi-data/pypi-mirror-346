# Development Guide

This guide provides information for developers who want to contribute to WordNet DB Migrator or modify it for their own needs.

## Project Structure

The WordNet DB Migrator project is organized as follows:

```
wordnet_db_migrator/
├── .github/                    # GitHub-specific files
│   ├── workflows/              # GitHub Actions workflows
│   │   └── ci.yml              # CI/CD configuration
│   └── ISSUE_TEMPLATE/         # Issue templates
├── docs/                       # Documentation
│   ├── installation.md         # Installation guide
│   ├── usage.md                # Usage guide
│   └── development.md          # Development guide (this file)
├── examples/                   # Example usage
├── tests/                      # Test cases
├── src/                        # Source directory
│   └── wordnet_db_migrator/    # Main package
│       ├── __init__.py         # Package initialization
│       ├── cli.py              # Command-line interface
│       ├── config.py           # Configuration handling
│       ├── main.py             # Main entry point
│       ├── steps/              # Individual steps
│       │   ├── __init__.py
│       │   ├── step010_test_sqlite_connection.py
│       │   ├── ...
│       └── utils/              # Utility functions
│           ├── __init__.py
│           └── db_utils.py
├── .gitignore                  # Git ignore file
├── LICENSE                     # License file
├── pyproject.toml              # Modern Python packaging
├── README.md                   # Main README
├── CONTRIBUTING.md             # Contribution guidelines
└── setup.py                    # Setup script
```

## Development Setup

To set up your development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/onareach/wordnet-db-migrator.git
   cd wordnet_db_migrator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Adding a New Step

The migration process is divided into steps, each implemented as a separate module in the `steps` directory. To add a new step:

1. Create a new module in the `steps` directory with a name following the pattern `stepXXX_description.py`, where `XXX` is a three-digit number indicating the order of the step.

2. Implement the step as a function named `run` that returns a boolean indicating success or failure:

   ```python
   # src/wordnet_db_migrator/steps/stepXXX_description.py
   """
   Step XXX: Description of the step.
   
   This module implements step XXX of the WordNet migration process.
   """
   import logging
   from wordnet_db_migrator.config import config
   
   # Set up logging
   logger = logging.getLogger(__name__)
   
   def run() -> bool:
       """
       Run step XXX of the WordNet migration process.
       
       Returns:
           bool: True if the step was successful, False otherwise.
       """
       logger.info("Starting step XXX")
       
       try:
           # Implement the step here
           
           logger.info("Step XXX completed successfully")
           return True
       except Exception as e:
           logger.error(f"Step XXX failed: {e}")
           config.success = False
           return False
   ```

3. Add the step to the `ALL_STEPS` list in `main.py`:

   ```python
   ALL_STEPS: List[StepDefinition] = [
       # ...
       ("Step XXX: Description", stepXXX_description.run),
       # ...
   ]
   ```

## Modifying an Existing Step

To modify an existing step:

1. Locate the step module in the `steps` directory.
2. Make your changes to the `run` function.
3. Test your changes (see the Testing section below).

## Adding a New Command-Line Option

To add a new command-line option:

1. Add the option to the `VALID_FLAGS` set in `cli.py`:

   ```python
   VALID_FLAGS: Set[str] = {
       # ...
       "--new-option",
       # ...
   }
   ```

2. Add the option to the help text in the `show_help` function in `cli.py`.

3. Add code to handle the option in the `validate_cli_args` function in `cli.py`.

## Testing

### Running Tests

Run tests with pytest:

```bash
pytest
```

### Writing Tests

Tests are located in the `tests` directory. To add a new test:

1. Create a new module in the `tests` directory with a name following the pattern `test_*.py`.

2. Implement test functions using pytest:

   ```python
   # tests/test_example.py
   """
   Tests for the example module.
   """
   import pytest
   from wordnet_db_migrator import example
   
   def test_example_function():
       """Test the example function."""
       result = example.function()
       assert result == expected_result
   ```

## Code Style

This project follows PEP 8 style guidelines. We use:

- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

You can run these tools with:

```bash
black .
isort .
flake8
mypy src/wordnet_db_migrator
```

## Documentation

### Docstrings

All modules, classes, and functions should have docstrings following the Google style:

```python
def function(arg1: str, arg2: int) -> bool:
    """
    Short description of the function.
    
    Longer description of the function if needed.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of the return value
        
    Raises:
        ValueError: Description of when this error is raised
    """
    # Function implementation
```

### Markdown Documentation

Documentation files are written in Markdown and located in the `docs` directory. To add a new documentation file:

1. Create a new Markdown file in the `docs` directory.
2. Add a link to the new file in the appropriate place (e.g., in the README.md or another documentation file).

## Releasing a New Version

To release a new version:

1. Update the version number in `src/wordnet_db_migrator/__init__.py`:

   ```python
   __version__ = "X.Y.Z"
   ```

2. Update the CHANGELOG.md file with the changes in the new version.

3. Commit the changes:

   ```bash
   git add src/wordnet_db_migrator/__init__.py CHANGELOG.md
   git commit -m "Bump version to X.Y.Z"
   ```

4. Tag the release:

   ```bash
   git tag -a vX.Y.Z -m "Version X.Y.Z"
   git push origin vX.Y.Z
   ```

5. Build the package:

   ```bash
   python -m build
   ```

6. Upload to PyPI:

   ```bash
   twine upload dist/*
   ```

## Getting Help

If you need help with development, please:

1. Check the documentation in the `docs` directory
2. Look at the code and comments
3. Check the [GitHub Issues](https://github.com/onareach/wordnet-db-migrator/issues)
4. Create a new issue if your question is not answered elsewhere
