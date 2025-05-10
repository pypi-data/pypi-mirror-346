# Coaxial PIP Packager

A streamlined tool to automate the packaging and releasing of Python packages to PyPI.

## Features

- **Automatic Version Management**: Detects current version and suggests increments
- **Smart Version Updates**: Updates version strings in all relevant project files
- **Git Integration**: Commits and pushes version changes
- **PyPI Publishing**: Builds and uploads packages to PyPI
- **Revert Support**: Can revert version changes if needed
- **Test Mode**: Preview changes without modifying files

## Installation

```bash
pip install coaxial-pip-packager
```

## Usage

```bash
# Basic usage - interactive mode
coaxial-pip-packager

# Skip git and publishing steps
coaxial-pip-packager --no-upload

# Only upload existing build
coaxial-pip-packager --only-upload

# Test mode to see what would change
coaxial-pip-packager --test

# Revert the last version update
coaxial-pip-packager --revert

# Create a default configuration file
coaxial-pip-packager --create-config
```

## Requirements

- Python 3.7 or higher
- Git (for version control operations)
- PyPI account with token (for publishing)

## Configuration

Create a default configuration file:

```bash
coaxial-pip-packager --create-config
```

This creates a configuration file at `~/.coaxial-pip-packager/config.toml` where you can:
- Customize file patterns for version detection
- Configure directories to exclude from processing
- Set default preferences for confirmations and automation

## Environment Variables

- `GITHUB_TOKEN`: GitHub token for git operations
- `PYPI_TOKEN`: PyPI token for publishing

## License

MIT