# FML: Fibonacci Markup Language

A humorous markup language where indentation levels must follow the Fibonacci sequence (0, 1, 1, 2, 3, 5, 8, 13, 21, etc.) — or else!

## What is FML?

FML is a markup language that enforces mathematical harmony in your documents by requiring all indentation levels to follow the Fibonacci sequence. If your indentation doesn't match a Fibonacci number, the parser will reject it with a snarky error message.

FML can be used in two modes:
- **Standard mode**: Any Fibonacci number indentation is allowed at any point
- **Continuous mode**: Indentation must follow a continuous progression through the Fibonacci sequence

## Purpose

FML serves multiple purposes:

1. **Educational**: Demonstrates markup language concepts, parsing techniques, and the Fibonacci sequence in an interactive way

2. **Creative Programming**: Shows how mathematical constraints can be applied to document formatting in a novel manner

3. **Versatile Tool**: Works as a command-line utility, Python library, or web application

4. **Programming Portfolio**: Showcases package development, error handling, and API design skills

While created with humor, FML is a fully functional markup language that can be used for documentation, presentations, educational settings, or anywhere you want to add mathematical structure to your text.

## Example

```fml
This line has 0 spaces of indentation
 This line has 1 space of indentation
 This line also has 1 space of indentation
  This line has 2 spaces of indentation
   This line has 3 spaces of indentation
     This line has 5 spaces of indentation
        This line has 8 spaces of indentation
             This line has 13 spaces of indentation
                          This line has 21 spaces of indentation
```

## Features

- Enforces Fibonacci sequence indentation (0, 1, 1, 2, 3, 5, 8, 13, 21, etc.)
- Supports both standard and continuous Fibonacci indentation modes
- Converts valid FML documents to HTML or Markdown formats
- Provides humorous error messages for non-compliant indentation
- Includes a CLI tool for validating and converting FML files
- Features an interactive web server with live preview
- Supports code blocks with proper indentation validation

## Installation

```bash
pip install fml-md
```

Or install from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ fml-md
```

## Usage

### Command Line Interface

```bash
# Validate an FML file
fml validate path/to/your/file.fml

# Convert an FML file to HTML
fml convert path/to/your/file.fml output.html

# Start the FML preview server
fml serve

# Use continuous mode (where indentation must follow continuous Fibonacci rules)
fml serve --continuous
```

### Python API

```python
from fml.parser import FMLParser
from fml.renderer import FMLRenderer

# Parse FML content
parser = FMLParser()
content = """Welcome to FML
 This line has 1 space indentation
  This line has 2 spaces
   This line has 3 spaces
     This line has 5 spaces
"""

# Parse the content
parsed = parser.parse(content)

# Render to HTML
renderer = FMLRenderer()
html = renderer.to_html(parsed)
print(html)

# Or render to markdown
markdown = renderer.to_markdown(parsed)
print(markdown)
```

## Web Interface

Start the web server and edit FML documents in your browser:

```bash
fml serve
```

Then open your browser to http://localhost:8000/

## Web Interface Screenshots

The FML web interface provides a live editor and preview:

![FML Web Interface](https://raw.githubusercontent.com/OwPor/fml-md/main/assets/images/web.png)

![FML Web Interface with Valid Document](https://raw.githubusercontent.com/OwPor/fml-md/main/assets/images/web1.png)

![FML Web Interface with Error](https://raw.githubusercontent.com/OwPor/fml-md/main/assets/images/web2.png)

## Why FML?

Because regular markup languages are too predictable. Embrace the mathematical harmony of Fibonacci in your documents!
