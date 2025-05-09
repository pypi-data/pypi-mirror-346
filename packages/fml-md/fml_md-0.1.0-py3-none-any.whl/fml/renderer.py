"""
FML Renderer - Converts parsed FML documents to HTML or other formats
"""
import re
import markdown
from typing import List, Dict, Any, Optional


class FMLRenderer:
    """Renderer for Fibonacci Markup Language."""
    
    def __init__(self):
        """Initialize the FML renderer."""
        self.in_code_block = False
        self.code_block_content = []
        self.code_language = None
    
    def to_html(self, parsed_content: List[Dict[str, Any]]) -> str:
        """
        Convert parsed FML content to HTML.
        
        Args:
            parsed_content: The parsed FML content
            
        Returns:
            HTML representation of the FML content
        """
        if not parsed_content:
            return ""
        
        html = ["<!DOCTYPE html>", "<html>", "<head>", 
                "<meta charset=\"UTF-8\">",
                "<title>FML Document</title>", 
                "<style>",
                "body { font-family: Arial, sans-serif; line-height: 1.6; }",
                ".fml-line { margin: 0; }",
                ".fml-indent-0 { margin-left: 0em; }",
                ".fml-indent-1 { margin-left: 1em; }",
                ".fml-indent-2 { margin-left: 2em; }",
                ".fml-indent-3 { margin-left: 3em; }",
                ".fml-indent-5 { margin-left: 5em; }",
                ".fml-indent-8 { margin-left: 8em; }",
                ".fml-indent-13 { margin-left: 13em; }",
                ".fml-indent-21 { margin-left: 21em; }",
                ".fml-indent-34 { margin-left: 34em; }",
                ".fml-indent-55 { margin-left: 55em; }",
                ".fml-indent-89 { margin-left: 89em; }",
                "</style>",
                "</head>", 
                "<body>"]
        
        code_block_lines = []
        current_code_language = None
        current_indent_class = None
        in_code_block = False
        
        for i, line in enumerate(parsed_content):
            # Handle code blocks
            if line.get('is_code_block', False):
                if not in_code_block:  # Start of code block
                    in_code_block = True
                    current_code_language = line.get('code_language', '')
                    current_indent_class = f"fml-indent-{line['indentation']}"
                    code_block_lines = []
                else:  # End of code block
                    # Process the collected code block
                    code_content = "\n".join(code_block_lines)
                    
                    # Use markdown to render the code with syntax highlighting
                    md_content = f"```{current_code_language}\n{code_content}\n```"
                    html_content = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite'])
                    
                    # Add the proper indentation class
                    html_content = html_content.replace('<pre>', f'<pre class="{current_indent_class}">')
                    
                    html.append(html_content)
                    
                    # Reset code block state
                    in_code_block = False
                    code_block_lines = []
                    current_code_language = None
                    current_indent_class = None
            elif line.get('in_code_block', False):  # Inside a code block
                code_block_lines.append(line['content'])
            else:  # Regular line
                indent_class = f"fml-indent-{line['indentation']}"
                html.append(f"<p class=\"fml-line {indent_class}\">{line['content']}</p>")
        
        # Handle unclosed code block
        if self.in_code_block and self.code_block_content:
            code_content = "\n".join(self.code_block_content)
            indent_class = f"fml-indent-0"  # Default indentation
            
            # Use markdown to render the code with syntax highlighting
            md_content = f"```{self.code_language}\n{code_content}\n```"
            html_content = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite'])
            
            # Add the proper indentation class
            html_content = html_content.replace('<pre>', f'<pre class="{indent_class}">')
            
            html.append(html_content)
            
            # Reset code block state
            self.in_code_block = False
            self.code_block_content = []
            self.code_language = None
        
        # Add CSS for syntax highlighting
        html[5] += """
        /* Syntax highlighting styles */
        .codehilite { background: #f8f8f8; overflow: auto; }
        .codehilite .hll { background-color: #ffffcc }
        .codehilite .c { color: #408080; font-style: italic } /* Comment */
        .codehilite .k { color: #008000; font-weight: bold } /* Keyword */
        .codehilite .o { color: #666666 } /* Operator */
        .codehilite .cm { color: #408080; font-style: italic } /* Comment.Multiline */
        .codehilite .cp { color: #BC7A00 } /* Comment.Preproc */
        .codehilite .c1 { color: #408080; font-style: italic } /* Comment.Single */
        .codehilite .cs { color: #408080; font-style: italic } /* Comment.Special */
        .codehilite .gd { color: #A00000 } /* Generic.Deleted */
        .codehilite .ge { font-style: italic } /* Generic.Emph */
        .codehilite .gr { color: #FF0000 } /* Generic.Error */
        .codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */
        .codehilite .gi { color: #00A000 } /* Generic.Inserted */
        .codehilite .go { color: #888888 } /* Generic.Output */
        .codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
        .codehilite .gs { font-weight: bold } /* Generic.Strong */
        .codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
        .codehilite .gt { color: #0044DD } /* Generic.Traceback */
        .codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
        .codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
        .codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
        .codehilite .kp { color: #008000 } /* Keyword.Pseudo */
        .codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
        .codehilite .kt { color: #B00040 } /* Keyword.Type */
        .codehilite .m { color: #666666 } /* Literal.Number */
        .codehilite .s { color: #BA2121 } /* Literal.String */
        """
        
        html.extend(["</body>", "</html>"])
        
        return "\n".join(html)
    
    def to_markdown(self, parsed_content: List[Dict[str, Any]]) -> str:
        """
        Convert parsed FML content to Markdown.
        
        Args:
            parsed_content: The parsed FML content
            
        Returns:
            Markdown representation of the FML content
        """
        if not parsed_content:
            return ""
        
        markdown_lines = []
        
        for line in parsed_content:
            # Convert indentation to spaces in markdown
            spaces = " " * line['indentation']
            markdown_lines.append(f"{spaces}{line['content']}")
        
        return "\n".join(markdown_lines)
    
    def to_text(self, parsed_content: List[Dict[str, Any]]) -> str:
        """
        Convert parsed FML content to plain text with proper indentation.
        
        Args:
            parsed_content: The parsed FML content
            
        Returns:
            Text representation of the FML content
        """
        if not parsed_content:
            return ""
        
        text_lines = []
        
        for line in parsed_content:
            # Preserve original indentation
            spaces = " " * line['indentation']
            text_lines.append(f"{spaces}{line['content']}")
        
        return "\n".join(text_lines)
