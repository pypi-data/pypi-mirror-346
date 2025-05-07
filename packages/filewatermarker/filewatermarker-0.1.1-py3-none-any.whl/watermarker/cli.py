"""
Command-line interface for the watermarker package.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .core import Watermarker


def parse_arguments(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.
    
    Args:
        args: List of command-line arguments. If None, uses sys.argv[1:].
        
    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Add watermarks to PDFs and images"
    )
    
    # GUI mode
    parser.add_argument(
        "--gui", 
        action="store_true",
        help="Launch the graphical user interface"
    )
    
    # Input/output
    parser.add_argument(
        "input",
        nargs="*",  # Changed from '+' to '*' to make it optional with GUI
        help="Input file(s) or directory"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file or directory"
    )
    
    # Watermark type
    group = parser.add_mutually_exclusive_group(required=False)  # Changed to false to allow GUI mode
    group.add_argument(
        "-t", "--text",
        help="Text watermark"
    )
    group.add_argument(
        "-l", "--logo",
        type=Path,
        help="Image file to use as watermark"
    )
    
    # Watermark options
    parser.add_argument(
        "--position",
        default="center",
        choices=["center", "topleft", "topright", "bottomleft", "bottomright"],
        help="Position of the watermark"
    )
    parser.add_argument(
        "--opacity",
        type=int,
        default=160,
        help="Opacity (0-255)"
    )
    parser.add_argument(
        "--angle",
        type=float,
        default=45,
        help="Rotation angle in degrees"
    )
    
    # Batch processing
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process directories recursively"
    )
    
    return parser.parse_args(args)


def main(args=None):
    """Main entry point for the command-line interface."""
    if args is None:
        args = parse_arguments()
    
    if args.gui:
        # When in GUI mode, directly use the original watermarker.py script for UI
        try:
            # Find the original watermarker.py file
            import os
            from pathlib import Path
            root_dir = Path(__file__).resolve().parent.parent.parent
            watermarker_path = os.path.join(root_dir, 'watermarker.py')
            
            if os.path.exists(watermarker_path):
                # Import and use the original GUI server function
                import importlib.util
                spec = importlib.util.spec_from_file_location("watermarker", watermarker_path)
                watermarker_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(watermarker_module)
                
                # Call the original start_gui_server function
                if hasattr(watermarker_module, 'start_gui_server'):
                    watermarker_module.start_gui_server()
                else:
                    raise ImportError("Could not find start_gui_server function in watermarker.py")
            else:
                # Fallback to the package version if original file not found
                from .gui.server import start_gui_server
                start_gui_server()
        except Exception as e:
            print(f"Error starting GUI: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        return
    
    # CLI mode - validate required arguments
    if not args.text and not args.logo:
        print("Error: Either --text or --logo must be specified")
        sys.exit(1)
    
    try:
        # Initialize the watermarker
        watermarker = Watermarker(
            text=args.text,
            logo=args.logo,
            position=args.position,
            opacity=args.opacity,
            angle=args.angle,
        )
        
        # Process files
        for input_path in args.input:
            input_path = Path(input_path)
            
            if input_path.is_file():
                output_path = args.output or input_path.parent / f"watermarked_{input_path.name}"
                watermarker.process_file(input_path, output_path)
            elif input_path.is_dir():
                output_dir = Path(args.output) if args.output else input_path / "watermarked"
                output_dir.mkdir(exist_ok=True)
                watermarker.process_batch(input_path, output_dir)
            else:
                print(f"Error: {input_path} is not a valid file or directory")
                sys.exit(1)
                
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
