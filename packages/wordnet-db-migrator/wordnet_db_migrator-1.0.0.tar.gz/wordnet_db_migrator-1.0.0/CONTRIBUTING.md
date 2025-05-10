# Contributing to WordNet DB Migrator

Thank you for considering contributing to WordNet DB Migrator! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- Be respectful and inclusive
- Be patient and welcoming
- Be thoughtful
- Be collaborative
- When disagreeing, try to understand why

## How to Contribute

### Reporting Bugs

If you find a bug, please report it by creating an issue on GitHub. When filing an issue, make sure to answer these questions:

1. What version of Python and WordNet DB Migrator are you using?
2. What operating system are you using?
3. What did you do?
4. What did you expect to see?
5. What did you see instead?

### Suggesting Enhancements

If you have an idea for a new feature or an enhancement to an existing feature, please create an issue on GitHub. Be sure to:

1. Clearly describe the feature/enhancement
2. Explain why it would be useful
3. Suggest how it might be implemented

### Pull Requests

If you'd like to contribute code, follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests to ensure they pass
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Pull Request Guidelines

- Update the README.md with details of changes if applicable
- Update the documentation if necessary
- The PR should work for Python 3.6 and higher
- Make sure all tests pass
- Follow the coding style (PEP 8)
- Write or update tests for new features

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

## Testing

Run tests with pytest:

```bash
pytest
```

## Coding Style

This project follows PEP 8 style guidelines. We use:

- Black for code formatting
- isort for import sorting
- flake8 for linting

You can run these tools with:

```bash
black .
isort .
flake8
```

## Documentation

Please update the documentation when necessary. We use:

- Docstrings for function and class documentation
- Markdown files for user guides and tutorials
- MkDocs with Material theme for generating the documentation website

### Working with Documentation

To work on the documentation:

1. Install the documentation dependencies:
   ```bash
   pip install -e ".[docs]"
   ```

2. Run the MkDocs development server:
   ```bash
   mkdocs serve
   ```

3. Open your browser at http://127.0.0.1:8000/ to see the documentation site

4. Edit the Markdown files in the `docs/` directory and see the changes live

5. When you're done, commit your changes and push them to GitHub. The documentation will be automatically built and deployed to GitHub Pages.

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
