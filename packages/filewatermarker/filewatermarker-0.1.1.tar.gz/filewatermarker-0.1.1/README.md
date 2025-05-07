# Watermarker

A versatile tool for adding text or image watermarks to PDF documents and images. This tool provides both command-line and GUI interfaces with customizable options.

## Features

### Core Functionality
- **Text Watermarks** - Add customizable text watermarks with control over font, color, and size
- **Image Watermarks** - Use logos or images as watermarks with automatic scaling
- **PDF Support** - Watermark PDF documents with precise positioning and transparency
- **Image Support** - Watermark various image formats (JPG, PNG, WEBP, etc.)

### Watermark Customization
- **Positioning** - Place watermarks at center, corners, or specific coordinates
- **Tiling** - Create repeating patterns across the entire document
- **Opacity** - Control transparency level from fully visible to barely noticeable
- **Rotation** - Apply any angle of rotation to watermarks
- **Scaling** - Size watermarks as a percentage of the document width
- **Spacing** - Adjust distance between tiled watermarks

### Interface Options
- **GUI Mode** - Simple and intuitive graphical interface with real-time preview
- **CLI Mode** - Command-line interface for automation and scripting
- **Batch Processing** - Process multiple files or directories in parallel
- **YAML Configuration** - Load settings from external config files

## Installation

### From PyPI (Recommended)

```bash
pip install filewatermarker  # Note: Package name on PyPI differs from the import name
```

Then import and use as normal:

```python
from watermarker import Watermarker
```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/michaeljabbour/watermark.git
   cd watermark
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

   Or install with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Package Structure

```
watermarker/
├── src/
│   └── watermarker/
│       ├── __init__.py
│       ├── core.py          # Core Watermarker class
│       ├── cli.py          # Command-line interface
│       ├── gui/            # GUI components
│       │   ├── __init__.py
│       │   └── server.py   # HTTP server for GUI
│       └── utils.py        # Utility functions
├── tests/                  # Test files
├── examples/               # Example usage
├── docs/                   # Documentation
├── pyproject.toml          # Modern Python package config
└── README.md
```

## Usage

### GUI Interface

Run the GUI interface for an interactive experience:

```bash
# If installed via pip
watermarker

# Or using the module
python -m watermarker
```

or explicitly:

```bash
# If installed via pip
watermarker --gui

# Or using the module
python -m watermarker --gui
```

The GUI allows you to:
- Upload PDF files or images
- Configure text or image watermarks 
- Preview the watermark on your document in real-time
- Choose from 9 preset watermark styles
- Adjust position, size, opacity, and rotation
- Process and download the watermarked document

### Command-line Usage

For basic watermarking:

```bash
# If installed via pip
watermarker --input input.pdf --output output.pdf --text "CONFIDENTIAL" --color FF0000

# Or using the module
python -m watermarker --input input.pdf --output output.pdf --text "CONFIDENTIAL" --color FF0000
```

Batch processing (handles both PDFs and images):

```bash
watermarker --input input_folder --output output_folder --text "CONFIDENTIAL" --tiled
```

Using a YAML config file:

```bash
watermarker --input input_folder --output output_folder --config settings.yaml
```

Example YAML config file (settings.yaml):
```yaml
text: CONFIDENTIAL
color: FF0000
tiled: true
opacity: 128
position: center
angle: 45
```

## Command-line Options

- `--gui`: Launch the graphical user interface (default if no arguments given)
- `--input`: Input file or directory to watermark
- `--output`: Output file or directory 
- `--text`: Text to use as watermark
- `--logo`: Logo image file for watermark
- `--color`: Color for text watermark (hex without #)
- `--tiled`: Tile the watermark across the page
- `--position`: Position of watermark (center, topleft, topright, bottomleft, bottomright)
- `--pct`: Size of watermark as percentage of page width
- `--opacity`: Opacity of watermark (0-255)
- `--angle`: Angle of rotation for watermark
- `--spacing`: Spacing between tiled watermarks
- `--threads`: Number of threads to use for batch processing
- `--quality`: JPEG quality (0-100) for image outputs
- `--format`: Output format for images (jpeg, png, webp)
- `--config`: YAML config file for default settings

## Output

All watermarked files will be saved to the `Outputs` directory by default when an output path is specified without a directory.

## Architecture

The package follows a modular architecture with clear separation of concerns:

### Core Components

1. **Watermarker Class**: The central engine that handles all watermarking operations.
   - Supports both text and image watermarks
   - Processes both PDF documents and various image formats
   - Provides full control over watermark appearance and positioning

2. **Command Line Interface**: Parses arguments and configures the Watermarker.
   - Handles input validation and help documentation
   - Provides file path resolution and batch processing
   - Supports YAML configuration loading

3. **GUI Server**: Provides a web-based interface.
   - Built with a lightweight HTTP server
   - Handles file uploads/downloads
   - Processes watermarking requests asynchronously
   - OS-agnostic folder navigation

### Dependency Management

The package uses modern Python packaging with pyproject.toml for dependencies:

- **reportlab**: PDF generation and manipulation
- **pypdf**: PDF reading and page operations
- **Pillow**: Image processing and watermarking
- **tqdm**: Progress display for batch operations
- **pyyaml**: Configuration file parsing

The `watermarker.py` script has a modern, modular architecture that provides a clean separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                       watermarker.py                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐        ┌──────────────────────┐   │
│  │  Command Line Int.  │        │     GUI Interface    │   │
│  └──────────┬──────────┘        └──────────┬───────────┘   │
│             │                              │                │
│             └──────────────┬───────────────┘                │
│                            │                                │
│                 ┌──────────▼─────────────┐                  │
│                 │                        │                  │
│                 │   Watermarker Class    │                  │
│                 │                        │                  │
│                 └──────────┬─────────────┘                  │
│                            │                                │
│         ┌─────────────────┬┴────────────────┐               │
│         │                 │                 │               │
│  ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼─────┐         │
│  │   Single    │   │    Batch    │   │   Config   │         │
│  │ Watermarker │   │  Processor  │   │   Loader   │         │
│  └──────┬──────┘   └──────┬──────┘   └──────┬─────┘         │
│         │                 │                 │               │
│  ┌──────┴───────┐  ┌──────┴──────┐   ┌──────┴─────┐         │
│  │ PDF Processor│  │ Parallel    │   │ YAML       │         │
│  │ IMG Processor│  │ Processing  │   │ Parser     │         │
│  └──────────────┘  └─────────────┘   └────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

- **Watermarker Class**: The central component that encapsulates all watermarking logic
  - Handles both PDF and image watermarking
  - Provides a consistent API for all types of watermarking
  - Implements the core watermarking algorithms

- **Interface Layers**:
  - Command Line Interface: Processes arguments and calls the Watermarker class
  - GUI Interface: Provides a web-based interface with live preview capabilities

- **Processing Modules**:
  - Single File Processor: Handles individual PDF or image files
  - Batch Processor: Manages bulk operations on multiple files
  - Configuration Loader: Parses YAML config files and applies settings

### Key Features

- **Unified Design**: Single script with multiple interfaces but shared core logic
- **Consistent API**: Same parameters used across CLI, GUI, and programmatic usage
- **Robust Error Handling**: Multiple fallback mechanisms for reliable processing
- **Parallel Processing**: Thread pools for efficient batch operations
- **Format Conversion**: Automatic handling of different file formats
- **Modular Structure**: Clear separation between UI, logic, and I/O operations

### Modern UI Features

- **Sleek Design**: Modern interface with gradient navigation bar and clean layout
- **Presets System**: 9 built-in watermark presets for quick configuration
- **Intuitive Controls**: Visual toggle for watermark type selection
- **Live Preview**: Real-time preview of watermark changes
- **Interactive Positioning**: Visual position selection grid
- **Responsive Layout**: Two-column design that adapts to different screen sizes
- **User Feedback**: Progress indicators and success messages

## Examples

Here are some examples of what you can do with Watermarker:

### Text Watermarks on PDFs

Add "CONFIDENTIAL" text watermarks to PDF documents, positioned in the bottom right corner:

```bash
watermarker --input test_input/sample.pdf --output output.pdf --text "CONFIDENTIAL" --color FF0000 --position bottomright
```

### Image Logo Watermarks

Add your company logo as a watermark, with 50% opacity:

```bash
watermarker --input test_input/samplelogo.png --output output.jpg --logo logo.png --position center --opacity 200
```

### Tiled Watermark Patterns

Create a repeating pattern of watermarks across the entire document:

```bash
python watermarker.py --input test_input/sample.pdf --output output.pdf --text "DRAFT" --tiled --angle 45 --opacity 80
```

The repository includes sample files in the `test_input` directory that you can use to try out different watermarking options.

## License

MIT License
