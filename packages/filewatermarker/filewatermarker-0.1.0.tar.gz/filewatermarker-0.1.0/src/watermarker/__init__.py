"""
Watermarker - A versatile tool for adding text or image watermarks to PDF documents and images.

This package provides functionality to:
- Add text or image watermarks to PDF files and images
- Control watermark position, opacity, size, and angle
- Process multiple files in batch
- Use through both command-line and GUI interfaces
"""

import warnings

# Suppress specific warnings we don't control
warnings.filterwarnings("ignore", message="ast.NameConstant is deprecated", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="PyPDF2 is deprecated", category=DeprecationWarning)

__version__ = "0.1.0"

from .core import Watermarker
from .utils import suppress_warnings

__all__ = ["Watermarker", "suppress_warnings"]
