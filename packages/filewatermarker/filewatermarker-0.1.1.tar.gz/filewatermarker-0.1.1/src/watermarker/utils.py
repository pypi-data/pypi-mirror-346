"""
Utility functions for the watermarker package.
"""

import contextlib
import warnings
from pathlib import Path
from typing import Union, Iterator, Any


def ensure_path(path: Union[str, Path]) -> Path:
    """Ensure the input is a Path object.
    
    Args:
        path: Input path as string or Path object
        
    Returns:
        Path object
    """
    if isinstance(path, str):
        return Path(path)
    return path


def is_image_file(path: Union[str, Path]) -> bool:
    """Check if a file is an image based on its extension.
    
    Args:
        path: Path to the file
        
    Returns:
        bool: True if the file is an image, False otherwise
    """
    path = ensure_path(path)
    return path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}


def is_pdf_file(path: Union[str, Path]) -> bool:
    """Check if a file is a PDF based on its extension.
    
    Args:
        path: Path to the file
        
    Returns:
        bool: True if the file is a PDF, False otherwise
    """
    path = ensure_path(path)
    return path.suffix.lower() == '.pdf'


@contextlib.contextmanager
def suppress_warnings(category: Any = Warning, message: str = "") -> Iterator[None]:
    """Context manager to suppress specific warnings.
    
    Args:
        category: Warning category to filter (default: all warnings)
        message: Specific warning message substring to filter (default: all messages)
        
    Yields:
        None
    
    Example:
        ```python
        # Suppress specific deprecation warning
        with suppress_warnings(DeprecationWarning, "ast.NameConstant is deprecated"):
            # Code that would generate the warning
            import reportlab
        ```
    """
    # Save the original showwarning function
    original_showwarning = warnings.showwarning
    
    def custom_showwarning(warning_message, warning_category, filename, lineno, *args, **kwargs):
        # If no message filter specified or message not in warning, show it
        if not message or message not in str(warning_message):
            # If no category filter or warning is not an instance of the category, show it
            if category is Warning or not issubclass(warning_category, category):
                original_showwarning(warning_message, warning_category, filename, lineno, *args, **kwargs)
    
    # Replace the showwarning function
    warnings.showwarning = custom_showwarning
    
    try:
        yield
    finally:
        # Restore the original showwarning function
        warnings.showwarning = original_showwarning
