"""
HTTP server for the watermarker GUI.
"""

import http.server
import json
import os
import socketserver
import tempfile
import cgi
import urllib.parse
from pathlib import Path
from typing import Dict, Any, Optional

class WatermarkHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for the watermark GUI."""
    
    def __init__(self, *args, **kwargs):
        self.temp_dir = kwargs.pop('temp_dir', None)
        super().__init__(*args, directory=self.temp_dir, **kwargs)
    
    def do_GET(self) -> None:
        """Handle GET requests, serving the HTML template for root requests."""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(get_html_template().encode('utf-8'))
            return
        elif self.path.startswith('/download/'):
            # Handle file downloads
            try:
                filename = os.path.basename(urllib.parse.unquote(self.path[10:]))
                file_path = os.path.join(self.temp_dir, filename)
                
                if os.path.exists(file_path):
                    # Determine content type based on file extension
                    content_type = 'application/octet-stream'  # Default
                    ext = os.path.splitext(filename)[1].lower()
                    if ext == '.pdf':
                        content_type = 'application/pdf'
                    elif ext in ['.jpg', '.jpeg']:
                        content_type = 'image/jpeg'
                    elif ext == '.png':
                        content_type = 'image/png'
                    
                    # Serve the file
                    self.send_response(200)
                    self.send_header('Content-Type', content_type)
                    self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                    self.send_header('Content-Length', str(os.path.getsize(file_path)))
                    self.end_headers()
                    
                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
                    return
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'File not found')
                    return
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'Error serving file: {str(e)}'.encode('utf-8'))
                return
                
        return super().do_GET()
    
    def do_POST(self) -> None:
        """Handle POST requests to the /api/process endpoint."""
        if self.path == '/api/process':
            content_length = int(self.headers['Content-Length'])
            if content_length > 20 * 1024 * 1024:  # 20MB limit
                self._send_json_response(413, {
                    'status': 'error',
                    'message': 'File too large (max 20MB)'
                })
                return
                
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            # Check if file was uploaded
            if 'file' not in form:
                self._send_json_response(400, {
                    'status': 'error',
                    'message': 'No file uploaded'
                })
                return
                
            # Get the uploaded file
            file_item = form['file']
            if not file_item.file:
                self._send_json_response(400, {
                    'status': 'error',
                    'message': 'Invalid file'
                })
                return
                
            # Save the file temporarily
            input_filename = file_item.filename
            temp_input_path = os.path.join(self.temp_dir, input_filename)
            
            with open(temp_input_path, 'wb') as f:
                f.write(file_item.file.read())
                
            # Get watermark parameters
            watermark_type = form.getvalue('watermark_type', 'text')
            position = form.getvalue('position', 'center')
            opacity = int(form.getvalue('opacity', '128'))
            angle = int(form.getvalue('angle', '45'))
            
            try:
                from watermarker.core import Watermarker
                watermarker = Watermarker()
                
                # Generate output filename
                base_name, ext = os.path.splitext(input_filename)
                output_filename = f"{base_name}_watermarked{ext}"
                temp_output_path = os.path.join(self.temp_dir, output_filename)
                
                # Apply watermark based on type
                if watermark_type == 'text':
                    text = form.getvalue('text', 'CONFIDENTIAL')
                    watermarker.add_watermark(
                        input_file=temp_input_path,
                        output_file=temp_output_path,
                        text=text,
                        position=position,
                        opacity=opacity,
                        angle=angle
                    )
                else:  # image watermark
                    if 'logo' not in form:
                        self._send_json_response(400, {
                            'status': 'error',
                            'message': 'No logo uploaded for image watermark'
                        })
                        return
                        
                    logo_item = form['logo']
                    temp_logo_path = os.path.join(self.temp_dir, logo_item.filename)
                    with open(temp_logo_path, 'wb') as f:
                        f.write(logo_item.file.read())
                        
                    watermarker.add_watermark(
                        input_file=temp_input_path,
                        output_file=temp_output_path,
                        image=temp_logo_path,
                        position=position,
                        opacity=opacity,
                        angle=angle
                    )
                    
                # Create a relative URL for downloading the result
                download_url = f"/download/{output_filename}"
                
                self._send_json_response(200, {
                    'status': 'success',
                    'message': 'Watermark applied successfully',
                    'download_url': download_url
                })
                
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


def get_html_template() -> str:
    """Return the HTML template for the GUI."""
    # Import needed packages
    import os.path
    
    # Get the root directory of the project
    root_dir = Path(__file__).resolve().parent.parent.parent.parent
    watermarker_path = os.path.join(root_dir, 'watermarker.py')
    
    # Check if the original watermarker.py file exists and load the template from it
    if os.path.exists(watermarker_path):
        try:
            # Load the original template from watermarker.py
            import importlib.util
            spec = importlib.util.spec_from_file_location("watermarker", watermarker_path)
            watermarker = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(watermarker)
            
            # Get the original HTML template function
            if hasattr(watermarker, 'get_html_template'):
                return watermarker.get_html_template()
        except Exception as e:
            print(f"Error loading original HTML template: {e}")
    
    # Fallback to a default template if the original can't be loaded
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Watermark Tool</title>
    <!-- PDF.js library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.7.107/pdf.min.js"></script>
    <script>
        // Set worker URL
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.7.107/pdf.worker.min.js';
    </script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.5;
            margin: 0;
            padding: 0;
            overflow: hidden;
            color: #333;
        }
        
        /* Custom animations and transitions */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .hidden {
            display: none !important;
        }
        
        .settings-section {
            animation: fadeIn 0.3s ease-out;
            transition: all 0.3s ease;
            margin-bottom: 25px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .preset-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: all 0.2s ease;
        }
        
        .position-button {
            transition: all 0.2s ease;
            padding: 8px 5px;
            text-align: center;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
        }
        
        .position-button:hover {
            background-color: #f0f0f0;
        }
        
        .position-button.selected {
            font-weight: bold;
            background-color: #4a6bff;
            color: white;
        }
    </style>
</head>
<body>
    <!-- Top navigation bar -->
    <div class="navbar" style="background: linear-gradient(to right, #4a6bff, #45009d); color: white; padding: 10px 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); position: fixed; top: 0; left: 0; right: 0; z-index: 1000; display: flex; align-items: center; justify-content: space-between;">
        <div class="navbar-brand">
            <svg class="mr-2" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px;">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>WatermarkTool</span>
        </div>
        
        <!-- Add centered upload button -->
        <div class="center-upload">
            <label for="pdfFile" class="upload-nav-button" style="display: flex; align-items: center; background-color: rgba(255,255,255,0.2); color: white; padding: 8px 16px; border-radius: 4px; cursor: pointer; transition: background-color 0.2s;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                Upload Document
            </label>
        </div>
        
        <a href="https://github.com/michaeljabbour/watermark" target="_blank" style="display: flex; align-items: center; text-decoration: none; color: white; font-size: 0.9rem;">
            <svg height="24" width="24" viewBox="0 0 16 16" version="1.1" fill="white">
                <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
            <span style="margin-left: 8px;">View on GitHub</span>
        </a>
    </div>
    
    <!-- Hidden file input for document upload -->
    <input type="file" id="pdfFile" accept=".pdf,.jpg,.jpeg,.png,.gif,.webp,.bmp,.tiff,.tif" onchange="handleFileChange()" style="display: none;">

    <!-- Main container with fixed navbar height compensation -->
    <div class="app-container" style="display: flex; height: calc(100vh - 64px); margin-top: 64px; overflow: hidden;">
        <!-- Left section (Settings sidebar) - fixed width -->
        <div class="settings-panel" style="width: 350px; background-color: #f8f9fa; padding: 20px; border-right: 1px solid #ddd; overflow-y: auto;">
            <!-- Presets section -->
            <div class="settings-section">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3 style="margin: 0; font-size: 16px;">Presets</h3>
                    <button onclick="saveCurrentAsPreset()" style="background: none; border: none; color: #4a6bff; cursor: pointer; font-size: 14px; display: flex; align-items: center;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 4px;">
                            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                            <polyline points="17 21 17 13 7 13 7 21"></polyline>
                            <polyline points="7 3 7 8 15 8"></polyline>
                        </svg>
                        Save
                    </button>
                </div>
                
                <div class="presets-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;">
                    <button class="preset-button" onclick="applyPreset('confidential')" style="background-color: #FF0000; color: white; border: none; padding: 8px 4px; border-radius: 4px; font-size: 12px; cursor: pointer; text-align: center;">Confidential</button>
                    <button class="preset-button" onclick="applyPreset('draft')" style="background-color: #666666; color: white; border: none; padding: 8px 4px; border-radius: 4px; font-size: 12px; cursor: pointer; text-align: center;">Draft</button>
                    <button class="preset-button" onclick="applyPreset('copy')" style="background-color: #FF6600; color: white; border: none; padding: 8px 4px; border-radius: 4px; font-size: 12px; cursor: pointer; text-align: center;">Do Not Copy</button>
                </div>
            </div>

            <!-- Watermark Options -->
            <div class="settings-section">
                <h3 style="margin: 0 0 15px 0; font-size: 16px;">Watermark Options</h3>
                
                <!-- Text/Image toggle -->
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: 500;">Watermark Type:</label>
                    <div style="display: flex; gap: 10px;">
                        <div style="flex: 1; text-align: center;">
                            <input type="radio" id="textOption" name="watermarkType" value="text" checked>
                            <label for="textOption" style="margin-left: 5px;">Text</label>
                        </div>
                        <div style="flex: 1; text-align: center;">
                            <input type="radio" id="imageOption" name="watermarkType" value="image">
                            <label for="imageOption" style="margin-left: 5px;">Image</label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
    // Initialize watermarking functionality
    document.addEventListener('DOMContentLoaded', function() {
        // Handle file selection from the top navbar button
        function handleFileChange() {
            const fileInput = document.getElementById('pdfFile');
            if (fileInput.files.length > 0) {
                const file = fileInput.files[0];
                // Process the file and show options
                console.log('File selected:', file.name);
                // Show document preview and settings panel
            }
        }
        
        // Make this function available globally
        window.handleFileChange = handleFileChange;
        
        // Apply watermark presets
        window.applyPreset = function(presetName) {
            console.log('Applying preset:', presetName);
            // Apply preset settings based on name
        };
        
        // Save current settings as a preset
        window.saveCurrentAsPreset = function() {
            console.log('Saving current settings as preset');
            // Code to save current settings
        };
    });
    </script>
</body>
</html>"""


def start_gui_server(port: int = 8000, temp_dir: Optional[Path] = None) -> None:
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
