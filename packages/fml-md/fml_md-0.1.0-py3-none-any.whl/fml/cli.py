"""
FML CLI - Command-line interface for the Fibonacci Markup Language
"""
import os
import sys
import click
from typing import Optional

from .parser import FMLParser, FMLError
from .continuous_parser import FMLContinuousParser
from .renderer import FMLRenderer


@click.group()
@click.version_option()
def cli():
    """FML - Fibonacci Markup Language CLI tool."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.argument('output_file', type=click.Path(writable=True), required=False)
@click.option('--format', '-f', type=click.Choice(['html', 'markdown', 'text']), default='html',
              help='Output format (default: html)')
@click.option('--continuous', '-c', is_flag=True, help='Use continuous Fibonacci indentation rules')
def convert(input_file: str, output_file: Optional[str] = None, format: str = 'html', continuous: bool = False):
    """Convert FML file to HTML, Markdown, or plain text."""
    if continuous:
        parser = FMLContinuousParser()
    else:
        parser = FMLParser()
    renderer = FMLRenderer()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the content
        try:
            parsed = parser.parse(content)
        except FMLError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
        
        # Render to the specified format
        if format == 'html':
            output = renderer.to_html(parsed)
        elif format == 'markdown':
            output = renderer.to_markdown(parsed)
        else:  # text
            output = renderer.to_text(parsed)
        
        # Write to output file or stdout
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            click.echo(f"Successfully converted {input_file} to {output_file}")
        else:
            click.echo(output)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.option('--continuous', '-c', is_flag=True, help='Use continuous Fibonacci indentation rules')
def validate(input_file: str, continuous: bool = False):
    """Validate FML file for correct Fibonacci indentation."""
    if continuous:
        parser = FMLContinuousParser()
    else:
        parser = FMLParser()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        is_valid, error = parser.validate(content)
        
        if is_valid:
            click.echo(f"SUCCESS: {input_file} is a valid FML document!")
        else:
            click.echo(f"ERROR: {input_file} is not a valid FML document: {error}", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def fibonacci():
    """Display the Fibonacci sequence for reference."""
    fib_numbers = FMLParser.FIBONACCI_NUMBERS
    click.echo("Fibonacci Sequence (for indentation reference):")
    click.echo(", ".join(str(n) for n in fib_numbers))


@cli.command()
@click.option('--port', '-p', default=8000, help='Port to run the server on')
@click.option('--no-browser', is_flag=True, help='Do not open browser automatically')
@click.option('--continuous', '-c', is_flag=True, help='Use continuous Fibonacci indentation rules')
def serve(port, no_browser, continuous=False):
    """Start a web server with an FML editor and previewer."""
    from .server import run_server
    run_server(port=port, open_browser=not no_browser, continuous=continuous)


if __name__ == '__main__':
    cli()
