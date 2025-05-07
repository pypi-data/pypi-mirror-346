"""
HTTP server for the watermarker GUI.
"""

import http.server
import json
import socketserver
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

class WatermarkHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for the watermark GUI."""
    
    def __init__(self, *args, **kwargs):
        self.temp_dir = kwargs.pop('temp_dir', None)
        super().__init__(*args, directory=self.temp_dir, **kwargs)
    
    def do_POST(self) -> None:
        """Handle POST requests to the /api/process endpoint."""
        if self.path == '/api/process':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Process the watermarking request
                # Parse the data but we don't use it in this placeholder function
                json.loads(post_data)
                # Placeholder for future functionality
                result = {"status": "success", "message": "Processing complete"}
                self._send_json_response(200, result)
            except Exception as e:
                self._send_json_response(500, {"status": "error", "message": str(e)})
        else:
            self.send_error(404, "Not Found")
    
    def _send_json_response(self, status_code: int, data: Dict[str, Any]) -> None:
        """Send a JSON response with the given status code and data."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


def start_server(port: int = 8000, temp_dir: Optional[Path] = None) -> None:
    """Start the GUI HTTP server.
    
    Args:
        port: Port to run the server on
        temp_dir: Directory to serve static files from
    """
    if temp_dir is None:
        temp_dir = Path(tempfile.mkdtemp())
    
    def handler_factory(*args, **kwargs):
        return WatermarkHTTPHandler(*args, temp_dir=temp_dir, **kwargs)
    
    with socketserver.TCPServer(("", port), handler_factory) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()
