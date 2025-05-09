#!/usr/bin/env python3
import click

# Import commands
from pevx.commands.auth import auth_poetry

@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Prudentia CLI - Development tools for Prudentia internal developers."""
    pass

# Add commands
cli.add_command(auth_poetry)

if __name__ == '__main__':
    cli() 