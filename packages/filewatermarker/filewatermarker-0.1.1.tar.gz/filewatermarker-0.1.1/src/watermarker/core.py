"""
Core functionality for the watermarker package.
"""

import io
import os
from concurrent import futures
from pathlib import Path
from typing import List, Optional, Tuple, Union

import pypdf
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from tqdm import tqdm


class Watermarker:
    """
    Core watermarking functionality for both PDFs and images.

    This class provides methods to add watermarks to both PDF and image files,
    with support for text and image watermarks, various positioning options,
    and batch processing capabilities.
    """

    def __init__(self, **kwargs):
        """
        Initialize the watermarker with options.

        Parameters:
        - text: Optional text for watermark
        - logo: Optional path to logo image for watermark
        - color: Color for text watermark (hex without #)
        - pct: Size of watermark as percentage of page width (0.0-1.0)
        - opacity: Opacity of watermark (0-255)
        - position: Position of watermark (center, topleft, topright, bottomleft, bottomright)
        - angle: Angle of rotation for watermark
        - spacing: Spacing between tiled watermarks
        - tiled: Whether to tile the watermark across the page
        - threads: Number of threads for batch processing
        - quality: JPEG quality (0-100)
        - format: Output format for images
        - font: Path to font file for text watermark
        """
        self.text = kwargs.get('text')
        self.logo = kwargs.get('logo')
        self.color = kwargs.get('color', '000000')
        self.pct = float(kwargs.get('pct', 0.2))
        self.opacity = int(kwargs.get('opacity', 160))
        self.position = kwargs.get('position', 'center')
        self.angle = float(kwargs.get('angle', 45))
        self.spacing = int(kwargs.get('spacing', 180))
        self.tiled = kwargs.get('tiled', False)
        self.threads = int(kwargs.get('threads', os.cpu_count() or 4))
        self.quality = int(kwargs.get('quality', 90))
        self.format = kwargs.get('format')
        self.font = kwargs.get('font')
        self.resize = kwargs.get('resize')

        # Validate options
        if not self.text and not self.logo:
            raise ValueError("Either text or logo must be provided")

        if self.logo and not isinstance(self.logo, (str, Path)):
            self.logo = Path(self.logo)

        if self.font and not isinstance(self.font, (str, Path)):
            self.font = Path(self.font)

        # Clean up position format (convert dash-style to no-dash)
        if isinstance(self.position, str) and '-' in self.position:
            self.position = self.position.replace('-', '')
            
    def _load_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Load font for text watermark, falling back to default if necessary.
        
        Args:
            size: Font size in pixels
            
        Returns:
            The loaded font object
        """
        try:
            if self.font:
                return ImageFont.truetype(str(self.font), size=size)
            else:
                # Try to use a nice default font if available
                for font_name in ["Arial.ttf", "Helvetica.ttf", "DejaVuSans.ttf"]:
                    try:
                        return ImageFont.truetype(font_name, size=size)
                    except (OSError, IOError):
                        continue
                        
                # Fall back to default font if no other fonts are available
                return ImageFont.load_default()
        except Exception as e:
            print(f"Font loading error: {str(e)}")
            return ImageFont.load_default()
            
    def _px_from_pct(self, box_size: Tuple[int, int]) -> int:
        """Calculate pixel size from percentage of shorter dimension.
        
        Args:
            box_size: Tuple of (width, height) dimensions
            
        Returns:
            Size in pixels
        """
        return int(min(box_size[0], box_size[1]) * self.pct)
        
    def _locate(self, canvas_size: Tuple[int, int], wm_size: Tuple[int, int]) -> Tuple[int, int]:
        """Calculate position for watermark based on selected position and padding.
        
        Args:
            canvas_size: Size of the canvas (width, height)
            wm_size: Size of the watermark (width, height)
            
        Returns:
            Tuple of (x, y) coordinates for watermark placement
        """
        padding = 20  # pixels from edge
        
        if self.position == 'center':
            return ((canvas_size[0] - wm_size[0]) // 2, 
                    (canvas_size[1] - wm_size[1]) // 2)
        elif self.position == 'topleft':
            return (padding, padding)
        elif self.position == 'topright':
            return (canvas_size[0] - wm_size[0] - padding, padding)
        elif self.position == 'bottomleft':
            return (padding, canvas_size[1] - wm_size[1] - padding)
        elif self.position == 'bottomright':
            return (canvas_size[0] - wm_size[0] - padding, 
                    canvas_size[1] - wm_size[1] - padding)
        else:
            # Default to center if position is not recognized
            return ((canvas_size[0] - wm_size[0]) // 2, 
                    (canvas_size[1] - wm_size[1]) // 2)

    def _make_logo_tile(self, logo_path: Path, target_px: int) -> Image.Image:
        """Create a logo tile with the specified size, opacity, and rotation.
        
        Args:
            logo_path: Path to the logo image file
            target_px: Target size in pixels
            
        Returns:
            Processed logo image as a PIL Image
        """
        try:
            # Open and resize logo
            logo = Image.open(str(logo_path)).convert('RGBA')
            
            # Calculate resize dimensions while maintaining aspect ratio
            original_size = logo.size
            ratio = original_size[0] / original_size[1]
            
            if ratio > 1:  # Landscape
                new_size = (target_px, int(target_px / ratio))
            else:  # Portrait or square
                new_size = (int(target_px * ratio), target_px)
                
            logo = logo.resize(new_size, Image.LANCZOS)
            
            # Apply rotation if needed
            if self.angle != 0:
                logo = logo.rotate(self.angle, expand=True, resample=Image.BICUBIC)
                
            # Apply opacity if needed
            if self.opacity < 255:
                alpha = logo.getchannel('A')
                alpha = alpha.point(lambda p: p * self.opacity // 255)
                logo.putalpha(alpha)
                
            return logo
        except Exception as e:
            print(f"Error creating logo tile: {str(e)}")
            # Return a blank image as fallback
            blank = Image.new('RGBA', (target_px, target_px), (0, 0, 0, 0))
            return blank
    
    def _apply_single_watermark(self, layer: Image.Image, logo_path: Optional[Path] = None) -> None:
        """Apply a single watermark (text or logo) to the overlay layer.
        
        Args:
            layer: The image layer to apply the watermark to
            logo_path: Optional path to the logo image
        """
        if logo_path and logo_path.exists():
            # Logo watermark
            target_px = self._px_from_pct(layer.size)
            logo = self._make_logo_tile(logo_path, target_px)
            position = self._locate(layer.size, logo.size)
            layer.paste(logo, position, logo)
        elif self.text:
            # Text watermark
            draw = ImageDraw.Draw(layer)
            target_px = self._px_from_pct(layer.size)
            font = self._load_font(target_px)
            
            # Get text dimensions and adjust position
            text_size = draw.textlength(self.text, font=font)
            text_height = target_px * 1.5  # Approximate
            position = self._locate(layer.size, (int(text_size), int(text_height)))
            
            # Convert hex color to RGB
            r, g, b = tuple(int(self.color[i:i+2], 16) for i in (0, 2, 4))
            text_color = (r, g, b, self.opacity)
            
            # Draw text with angle
            if self.angle != 0:
                # Create text on a transparent image and rotate it
                text_layer = Image.new('RGBA', layer.size, (0, 0, 0, 0))
                text_draw = ImageDraw.Draw(text_layer)
                text_draw.text(position, self.text, font=font, fill=text_color)
                rotated = text_layer.rotate(self.angle, expand=False, center=position)
                layer.paste(rotated, (0, 0), rotated)
            else:
                # Draw directly on the layer
                draw.text(position, self.text, font=font, fill=text_color)
                
    def _apply_tiled_watermark(self, layer: Image.Image, logo_path: Optional[Path] = None) -> None:
        """Fill the entire layer with tiled watermarks.
        
        Args:
            layer: The image layer to apply the watermark to
            logo_path: Optional path to the logo image
        """
        width, height = layer.size
        spacing = self.spacing
        
        if logo_path and logo_path.exists():
            # Logo watermark tiling
            target_px = self._px_from_pct((spacing, spacing))
            tile = self._make_logo_tile(logo_path, target_px)
            tile_w, tile_h = tile.size
            
            for y in range(0, height + tile_h, spacing):
                for x in range(0, width + tile_w, spacing):
                    layer.paste(tile, (x - tile_w//2, y - tile_h//2), tile)
        elif self.text:
            # Text watermark tiling
            draw = ImageDraw.Draw(layer)
            target_px = self._px_from_pct((spacing, spacing))
            font = self._load_font(target_px)
            
            # Convert hex color to RGB
            r, g, b = tuple(int(self.color[i:i+2], 16) for i in (0, 2, 4))
            text_color = (r, g, b, self.opacity)
            
            for y in range(0, height + spacing, spacing):
                for x in range(0, width + spacing, spacing):
                    if self.angle != 0:
                        # Create text on a transparent image and rotate it
                        text_layer = Image.new('RGBA', (spacing, spacing), (0, 0, 0, 0))
                        text_draw = ImageDraw.Draw(text_layer)
                        text_draw.text((spacing//4, spacing//4), self.text, font=font, fill=text_color)
                        rotated = text_layer.rotate(self.angle, expand=False)
                        layer.paste(rotated, (x - spacing//2, y - spacing//2), rotated)
                    else:
                        # Draw directly on the layer
                        draw.text((x, y), self.text, font=font, fill=text_color)
                        
    def stamp_image(self, src_path: Union[str, Path], dst_path: Union[str, Path]) -> bool:
        """Add a watermark to an image file.
        
        Args:
            src_path: Path to the source image
            dst_path: Path to save the watermarked image
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            src_path = Path(src_path) if not isinstance(src_path, Path) else src_path
            dst_path = Path(dst_path) if not isinstance(dst_path, Path) else dst_path
            
            # Create destination directory if it doesn't exist
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Open and prepare the image
            with Image.open(src_path) as img:
                # Convert to RGBA for transparent watermarks
                img = img.convert('RGBA')
                
                # Create a transparent overlay for the watermark
                overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
                
                # Apply watermark to the overlay
                if self.tiled:
                    self._apply_tiled_watermark(overlay, self.logo)
                else:
                    self._apply_single_watermark(overlay, self.logo)
                
                # Composite the overlay with the original image
                watermarked = Image.alpha_composite(img, overlay)
                
                # Convert back to RGB if saving as JPEG
                if dst_path.suffix.lower() in ('.jpg', '.jpeg'):
                    watermarked = watermarked.convert('RGB')
                
                # Get format from extension
                save_format = self.format or dst_path.suffix.lstrip('.')
                
                # Save the watermarked image
                if save_format.lower() in ('jpg', 'jpeg'):
                    watermarked.save(dst_path, format=save_format.upper(), quality=self.quality)
                else:
                    watermarked.save(dst_path, format=save_format.upper() if save_format else None)
                    
                return True
        except Exception as e:
            print(f"Error processing image {src_path}: {str(e)}")
            return False

    def _create_pdf_watermark(self, page_width: float, page_height: float) -> io.BytesIO:
        """Create a watermark overlay for a PDF page.
        
        Args:
            page_width: Width of the PDF page in points
            page_height: Height of the PDF page in points
            
        Returns:
            BytesIO object containing the watermark PDF
        """
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
        
        if self.logo and Path(self.logo).exists():
            # Logo watermark
            target_px = int(min(page_width, page_height) * self.pct)
            
            try:
                # Use PIL to prepare the logo
                logo = self._make_logo_tile(Path(self.logo), target_px)
                logo_stream = io.BytesIO()
                logo.save(logo_stream, format='PNG')
                logo_stream.seek(0)
                
                if self.tiled:
                    # Tile the logo across the page
                    spacing = self.spacing
                    logo_width, logo_height = logo.size
                    
                    for y in range(0, int(page_height) + logo_height, spacing):
                        for x in range(0, int(page_width) + logo_width, spacing):
                            c.saveState()
                            c.translate(x - logo_width//2, y - logo_height//2)
                            c.drawImage(ImageReader(logo_stream), 0, 0, width=logo_width, height=logo_height)
                            c.restoreState()
                            logo_stream.seek(0)  # Reset for next use
                else:
                    # Single logo watermark
                    logo_width, logo_height = logo.size
                    position = self._locate((int(page_width), int(page_height)), (logo_width, logo_height))
                    
                    c.saveState()
                    c.translate(position[0], position[1])
                    c.drawImage(ImageReader(logo_stream), 0, 0, width=logo_width, height=logo_height)
                    c.restoreState()
            except Exception as e:
                print(f"Error adding logo to PDF: {str(e)}")
        elif self.text:
            # Text watermark
            # Set up text properties
            c.setFillColorRGB(
                int(self.color[0:2], 16) / 255,
                int(self.color[2:4], 16) / 255,
                int(self.color[4:6], 16) / 255,
                self.opacity / 255
            )
            
            font_size = int(min(page_width, page_height) * self.pct)
            c.setFont("Helvetica", font_size)
            
            if self.tiled:
                # Tile the text across the page
                spacing = self.spacing
                for y in range(0, int(page_height) + spacing, spacing):
                    for x in range(0, int(page_width) + spacing, spacing):
                        c.saveState()
                        c.translate(x, y)
                        c.rotate(self.angle)
                        c.drawString(0, 0, self.text)
                        c.restoreState()
            else:
                # Single text watermark
                text_width = c.stringWidth(self.text, "Helvetica", font_size)
                position = self._locate(
                    (int(page_width), int(page_height)),
                    (int(text_width), int(font_size * 1.2))
                )
                
                c.saveState()
                c.translate(position[0] + text_width/2, position[1] + font_size/2)
                c.rotate(self.angle)
                c.drawString(-text_width/2, -font_size/2, self.text)
                c.restoreState()
        
        c.save()
        buffer.seek(0)
        return buffer
    
    def stamp_pdf(self, src_path: Union[str, Path], dst_path: Union[str, Path]) -> bool:
        """Add a watermark to a PDF file.
        
        Args:
            src_path: Path to the source PDF
            dst_path: Path to save the watermarked PDF
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            src_path = Path(src_path) if not isinstance(src_path, Path) else src_path
            dst_path = Path(dst_path) if not isinstance(dst_path, Path) else dst_path
            
            # Create destination directory if it doesn't exist
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Open the source PDF
            with open(src_path, 'rb') as src_file:
                pdf_reader = pypdf.PdfReader(src_file)
                pdf_writer = pypdf.PdfWriter()
                
                # Process each page
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    # Get page dimensions
                    page_width = float(page.mediabox.width)
                    page_height = float(page.mediabox.height)
                    
                    # Create watermark for this page
                    watermark_buffer = self._create_pdf_watermark(page_width, page_height)
                    watermark_reader = pypdf.PdfReader(watermark_buffer)
                    watermark_page = watermark_reader.pages[0]
                    
                    # Merge watermark with page
                    page.merge_page(watermark_page)
                    pdf_writer.add_page(page)
                
                # Write the output file
                with open(dst_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                    
                return True
        except Exception as e:
            print(f"Error processing PDF {src_path}: {str(e)}")
            return False
            
    def process_file(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> bool:
        """Process a single file (either PDF or image).
        
        Args:
            input_path: Path to the input file
            output_path: Path to save the output file
            
        Returns:
            bool: True if successful, False otherwise
        """
        input_path = Path(input_path) if not isinstance(input_path, Path) else input_path
        output_path = Path(output_path) if not isinstance(output_path, Path) else output_path
        
        # Ensure input file exists
        if not input_path.exists():
            print(f"Error: Input file not found: {input_path}")
            return False
            
        # Process based on file type
        suffix = input_path.suffix.lower()
        if suffix == '.pdf':
            return self.stamp_pdf(input_path, output_path)
        elif suffix in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'):
            return self.stamp_image(input_path, output_path)
        else:
            print(f"Error: Unsupported file type: {suffix}")
            return False
            
    def process_batch(self, input_dir: Union[str, Path], output_dir: Union[str, Path],
                      file_types: Optional[List[str]] = None) -> List[Path]:
        """Process multiple files in a directory.
        
        Args:
            input_dir: Path to the input directory
            output_dir: Path to the output directory
            file_types: List of file extensions to process (default: PDFs and images)
            
        Returns:
            List[Path]: List of processed output files
        """
        input_dir = Path(input_dir) if not isinstance(input_dir, Path) else input_dir
        output_dir = Path(output_dir) if not isinstance(output_dir, Path) else output_dir
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define default file types if not specified
        if file_types is None:
            file_types = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
            
        # Filter files by type
        input_files = [f for f in input_dir.glob('*') if f.is_file() and f.suffix.lower() in file_types]
        
        if not input_files:
            print(f"No matching files found in {input_dir}")
            return []
            
        # Process files in parallel
        processed_files = []
        
        # Define worker function for thread pool
        def process_worker(src: Path) -> Optional[Path]:
            dst = output_dir / (src.stem + '_watermarked' + src.suffix)
            if self.process_file(src, dst):
                return dst
            return None
            
        # Use ThreadPoolExecutor for parallel processing
        with futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            # Submit all files for processing
            future_to_file = {executor.submit(process_worker, f): f for f in input_files}
            
            # Process results as they complete
            for future in tqdm(futures.as_completed(future_to_file), total=len(input_files),
                              desc="Processing files", unit="file"):
                result = future.result()
                if result:
                    processed_files.append(result)
                    
        return processed_files
