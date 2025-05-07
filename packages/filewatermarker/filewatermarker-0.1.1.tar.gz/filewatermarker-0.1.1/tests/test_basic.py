"""Basic tests for the watermarker package."""

import pytest
from pathlib import Path

from watermarker import Watermarker


def test_watermarker_initialization():
    """Test that Watermarker initializes with default parameters."""
    # Should raise ValueError if neither text nor logo is provided
    with pytest.raises(ValueError):
        Watermarker()
    
    # Should initialize with text
    wm = Watermarker(text="Test")
    assert wm.text == "Test"
    assert wm.opacity == 160  # Default value
    
    # Should initialize with logo
    wm = Watermarker(logo="path/to/logo.png")
    assert str(wm.logo) == "path/to/logo.png"


def test_watermarker_parameters():
    """Test that Watermarker parameters are set correctly."""
    wm = Watermarker(
        text="Test",
        position="topleft",
        opacity=200,
        angle=30,
        pct=0.3,
    )
    
    assert wm.position == "topleft"
    assert wm.opacity == 200
    assert wm.angle == 30
    assert wm.pct == 0.3
