"""
FML Server - A simple web server for previewing FML files
"""
import os
import http.server
import socketserver
import webbrowser
from urllib.parse import parse_qs, urlparse
import json
import click

from fml.parser import FMLParser, FMLError
from fml.continuous_parser import FMLContinuousParser
from fml.renderer import FMLRenderer


class FMLHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for the FML preview server."""
    
    # Class variable to track continuous mode
    continuous_mode = False
    
    @classmethod
    def set_continuous_mode(cls, continuous):
        """Set the continuous mode for the handler."""
        cls.continuous_mode = continuous
    
    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        # Parse URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Serve the editor page
        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            # Read the editor HTML template
            continuous_mode_status = "enabled" if self.continuous_mode else "disabled"
            
            # Define the HTML template as a regular string
            editor_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>FML Editor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        header {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            text-align: center;
        }
        .container {
            display: flex;
            flex: 1;
        }
        .editor-pane {
            flex: 1;
            padding: 10px;
            display: flex;
            flex-direction: column;
        }
        .preview-pane {
            flex: 1;
            padding: 10px;
            border-left: 1px solid #ccc;
            overflow: auto;
        }
        textarea {
            width: 100%;
            height: 100%;
            font-family: monospace;
            font-size: 14px;
            padding: 10px;
            box-sizing: border-box;
            border: 1px solid #ccc;
        }
        .status {
            padding: 10px;
            margin-top: 10px;
            background-color: #f8f8f8;
            border: 1px solid #ccc;
        }
        .valid {
            background-color: #dff0d8;
            color: #3c763d;
            border-color: #d6e9c6;
        }
        .invalid {
            background-color: #f2dede;
            color: #a94442;
            border-color: #ebccd1;
        }
        .fml-line { margin: 0; }
        .fml-indent-0 { margin-left: 0em; }
        .fml-indent-1 { margin-left: 1em; }
        .fml-indent-2 { margin-left: 2em; }
        .fml-indent-3 { margin-left: 3em; }
        .fml-indent-5 { margin-left: 5em; }
        .fml-indent-8 { margin-left: 8em; }
        .fml-indent-13 { margin-left: 13em; }
        .fml-indent-21 { margin-left: 21em; }
        .fml-indent-34 { margin-left: 34em; }
        .fml-indent-55 { margin-left: 55em; }
        .fml-indent-89 { margin-left: 89em; }
        .fibonacci-helper {
            margin-top: 10px;
            font-family: monospace;
            background-color: #f8f8f8;
            padding: 5px;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <header>
        <h1>FML: Fibonacci Markup Language Editor</h1>
        <div style="font-size: 14px; margin-top: -10px; color: #eee;">Continuous Mode: CONTINUOUS_MODE_STATUS</div>
    </header>
    <div class="container">
        <div class="editor-pane">
            <h2>Editor</h2>
            <textarea id="editor" placeholder="Enter your FML code here...">Welcome to Fibonacci Markup Language!
 This line has 1 space of indentation
 This is also at the 1-space level
  Here we have 2 spaces
   Now we're at 3 spaces
     This line jumps to 5 spaces
        And now we're at 8 spaces
             This impressive indentation has 13 spaces
                     This massive indentation has 21 spaces</textarea>
            <div class="status" id="status">Status: Ready</div>
            <div class="fibonacci-helper">
                Fibonacci Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144
            </div>
        </div>
        <div class="preview-pane">
            <h2>Preview</h2>
            <div id="preview"></div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const editor = document.getElementById('editor');
            const preview = document.getElementById('preview');
            const status = document.getElementById('status');
            
            function updatePreview() {
                const content = editor.value;
                
                // Clear previous errors
                status.textContent = 'Status: Processing...';
                status.className = 'status';
                
                // Send content to server for validation and rendering
                fetch('/validate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ content: content }),
                    credentials: 'same-origin'
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Server responded with status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Server response:', data);
                    if (data.valid) {
                        status.textContent = 'Status: Valid FML document';
                        status.className = 'status valid';
                        preview.innerHTML = data.html;
                    } else {
                        // Display the full error message including indentation details
                        console.log('Error message:', data.error);
                        status.textContent = 'Status: ' + data.error;
                        status.className = 'status invalid';
                    }
                })
                .catch(error => {
                    console.error('Error during fetch operation:', error);
                    status.textContent = 'Status: Connection error. Please check if the server is running.';
                    status.className = 'status invalid';
                });
            }
            
            // Initial preview
            updatePreview();
            
            // Update preview when content changes
            editor.addEventListener('input', updatePreview);
        });
    </script>
</body>
</html>"""
            
            # Replace the placeholder with the actual value
            editor_html = editor_html.replace("CONTINUOUS_MODE_STATUS", continuous_mode_status)
            
            self.wfile.write(editor_html.encode())
            return
        
        # Handle API requests
        if path == "/validate":
            # For GET requests to /validate, return a JSON response indicating the endpoint is available
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "message": "Use POST for validation"}).encode())
            return
            
        # Serve static files
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        """Handle POST requests."""
        # Parse URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Handle validation requests
        if path == "/validate":
            # Move all error handling to a single try-except block
            try:
                # Get content length
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    # Handle empty request
                    response = {
                        'valid': False,
                        'error': 'Empty request received'
                    }
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                    return
                
                # Read and parse request data
                post_data = self.rfile.read(content_length).decode('utf-8')
                try:
                    data = json.loads(post_data)
                except json.JSONDecodeError:
                    # Handle invalid JSON
                    response = {
                        'valid': False,
                        'error': 'Invalid JSON received'
                    }
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                    return
                
                content = data.get('content', '')
                
                # Select parser based on mode
                if self.continuous_mode:
                    parser = FMLContinuousParser()
                else:
                    parser = FMLParser()
                renderer = FMLRenderer()
                
                # Parse the FML content and generate response
                try:
                    parsed = parser.parse(content)
                    html = renderer.to_html(parsed)
                    
                    response = {
                        'valid': True,
                        'html': html
                    }
                except FMLError as e:
                    # Get the full error message with all details
                    error_msg = str(e)
                    
                    # Debug print to server console
                    print(f"FML Error: {error_msg}")
                    
                    # Ensure the error message is properly formatted for display
                    # Remove the "Line X: " prefix if present to make the error message cleaner
                    if error_msg.startswith("Line ") and ": " in error_msg:
                        line_prefix, main_error = error_msg.split(": ", 1)
                        error_msg = main_error
                    
                    response = {
                        'valid': False,
                        'error': error_msg
                    }
                
                # Always send a 200 OK response for validation requests, even if there's an error
                # This ensures the client can display the error message properly
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                return
                
            except Exception as e:
                # Catch any other exceptions and return a helpful error
                print(f"Error processing request: {str(e)}")
                response = {
                    'valid': False,
                    'error': f'Server error: {str(e)}'
                }
                self.send_response(200)  # Changed from 500 to 200 to ensure client can display the error
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                return
            
            return
        
        # Default response for unknown POST requests
        self.send_response(404)
        self.end_headers()


def run_server(port=8000, open_browser=True, continuous=False):
    """Run the FML preview server."""
    # Set continuous mode
    FMLHandler.set_continuous_mode(continuous)
    
    handler = FMLHandler
    
    # Try to use the requested port, or find an available one
    while True:
        try:
            httpd = socketserver.TCPServer(("", port), handler)
            break
        except OSError:
            port += 1
    
    print(f"FML preview server running at http://localhost:{port}/")
    
    if open_browser:
        webbrowser.open(f"http://localhost:{port}/")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        httpd.server_close()


@click.command()
@click.option('--port', '-p', default=8000, help='Port to run the server on')
@click.option('--no-browser', is_flag=True, help='Do not open browser automatically')
@click.option('--continuous', '-c', is_flag=True, help='Use continuous Fibonacci indentation rules')
def main(port, no_browser, continuous):
    """Run the FML preview server."""
    run_server(port=port, open_browser=not no_browser, continuous=continuous)


if __name__ == '__main__':
    main()
