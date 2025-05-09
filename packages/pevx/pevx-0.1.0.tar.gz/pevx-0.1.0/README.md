# Prudentia CLI (pevx)

A development CLI tool for Prudentia internal developers.

## Installation

### From PyPI (when published)

```bash
pip install pevx
```

### Development Mode

Clone the repository and install in development mode using Poetry:

```bash
git clone [repository-url]
cd pevx
poetry install
```

## Usage

After installation, you can use the CLI with the `pevx` command:

```bash
# Show help
pevx --help

# Authenticate poetry with AWS CodeArtifact
pevx auth-poetry
```

## Available Commands

- `auth-poetry`: Authenticate poetry with AWS CodeArtifact
  - Configures poetry to use Prudentia's private Python package repository
  - Uses AWS credentials to obtain authentication token

## Command Options

### auth-poetry

```bash
# Customize CodeArtifact settings
pevx auth-poetry --domain custom-domain --domain-owner 123456789 --repo custom-repo --region us-west-2
```

Default values:
- Domain: prudentia-sciences
- Domain Owner: 728222516696
- Repository: pypi-store
- Region: us-east-1

## Development

### Project Structure

```
pevx/
├── pevx/                     # Python package
│   ├── __init__.py           # Package init with version
│   ├── cli.py                # Entry point for CLI
│   ├── commands/             # Subcommands organized here
│   │   ├── __init__.py
│   │   └── auth.py           # Authentication commands
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   └── config.py         # Configuration utilities
│   └── core/                 # Business logic
│       ├── __init__.py
│       └── engine.py         # Core functionality
├── tests/
│   ├── __init__.py
│   └── test_cli.py
├── pyproject.toml            # Poetry configuration
└── README.md
```

### Adding New Commands

1. Create a new file in the `pevx/commands/` directory for your command group
2. Implement your command using Click
3. Import and register your command in `pevx/cli.py`

Example:

```python
# In pevx/commands/my_command.py
import click

@click.command()
def my_command():
    """Command description."""
    click.echo("Running my command")

# In pevx/cli.py, add:
from pevx.commands.my_command import my_command
cli.add_command(my_command)
```

### CI/CD and Versioning

This project uses a comprehensive CI/CD pipeline with semantic-release:

1. **Automated Testing**
   - Runs tests on multiple Python versions (3.9, 3.10, 3.11, 3.12)
   - Generates code coverage reports

2. **Semantic Versioning**
   - Automatically determines the next version number based on commit messages
   - Creates GitHub releases with generated changelogs

3. **Automated Publishing to PyPI**
   - When a new version is detected, automatically builds and publishes to PyPI

#### Required Secrets

To use the CI/CD pipeline, add this secret to your GitHub repository:

- `PYPI_API_TOKEN`: API token for PyPI

#### Commit Message Format

For semantic-release to work properly, use conventional commit messages:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Common types:
- `fix`: Bug fixes (triggers PATCH version bump)
- `feat`: New features (triggers MINOR version bump)
- `feat!`, `fix!`, `refactor!`, etc.: Breaking changes (triggers MAJOR version bump)

Once published to PyPI, team members can install the CLI tool with:

```bash
pip install pevx
```