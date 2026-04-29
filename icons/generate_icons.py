#!/usr/bin/env python3
"""Generate Get Context icon variants for Zoom Marketplace.

Renders 4 SVG-like designs at 512×512 master resolution using Pillow,
then downscales each to 256×256 with high-quality Lanczos resampling.

Output:
  variant_<n>_512.png
  variant_<n>_256.png
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(exist_ok=True)

# Brand colors
COBALT = (44, 92, 255)        # #2C5CFF — landing page accent
CHARCOAL = (17, 17, 17)       # #111
DEEP_NAVY = (15, 23, 41)      # #0F1729 — premium dark
WHITE = (255, 255, 255)

ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"


def rounded_rect(img: Image.Image, radius: int, fill):
    """Apply rounded corners to an image (creates new RGBA)."""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    base = Image.new("RGBA", (w, h), fill + (0,))
    base.paste(img, (0, 0))
    base.putalpha(mask)
    return base


def variant_1_blue_gc():
    """Cobalt blue background, big white 'GC' wordmark."""
    size = 512
    img = Image.new("RGB", (size, size), COBALT)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(ARIAL_BLACK, 290)
    text = "GC"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1] - 8
    draw.text((x, y), text, fill=WHITE, font=font)
    return img


def variant_2_charcoal_blue_gc():
    """Charcoal background, blue 'GC' with white accent dot."""
    size = 512
    img = Image.new("RGB", (size, size), CHARCOAL)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(ARIAL_BLACK, 290)
    text = "GC"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1] - 8
    draw.text((x, y), text, fill=COBALT, font=font)
    # Small accent dot bottom-right
    cx, cy, r = size - 80, size - 80, 18
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=COBALT)
    return img


def variant_3_brackets():
    """White bg, bold blue brackets [•] — captured-context metaphor."""
    size = 512
    img = Image.new("RGB", (size, size), COBALT)
    draw = ImageDraw.Draw(img)
    # Brackets [ ]
    stroke = 36
    bracket_height = 280
    bracket_width = 70
    cx, cy = size // 2, size // 2
    # Left bracket
    lx = cx - 130
    draw.rectangle((lx, cy - bracket_height // 2, lx + stroke, cy + bracket_height // 2), fill=WHITE)
    draw.rectangle((lx, cy - bracket_height // 2, lx + bracket_width, cy - bracket_height // 2 + stroke), fill=WHITE)
    draw.rectangle((lx, cy + bracket_height // 2 - stroke, lx + bracket_width, cy + bracket_height // 2), fill=WHITE)
    # Right bracket
    rx = cx + 130
    draw.rectangle((rx - stroke, cy - bracket_height // 2, rx, cy + bracket_height // 2), fill=WHITE)
    draw.rectangle((rx - bracket_width, cy - bracket_height // 2, rx, cy - bracket_height // 2 + stroke), fill=WHITE)
    draw.rectangle((rx - bracket_width, cy + bracket_height // 2 - stroke, rx, cy + bracket_height // 2), fill=WHITE)
    # Dot in center
    r = 28
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE)
    return img


def variant_4_speech_dot():
    """Navy background, white speech bubble with cobalt center dot."""
    size = 512
    img = Image.new("RGB", (size, size), DEEP_NAVY)
    draw = ImageDraw.Draw(img)
    # Rounded rect speech bubble
    pad = 90
    draw.rounded_rectangle((pad, pad, size - pad, size - pad - 30), radius=60, fill=WHITE)
    # Tail
    tail = [(size // 2 - 30, size - pad - 30), (size // 2 + 30, size - pad - 30), (size // 2, size - pad + 30)]
    draw.polygon(tail, fill=WHITE)
    # Three dots like "..." or a single bigger dot
    cy = size // 2 - 15
    r = 22
    spacing = 70
    for dx in (-spacing, 0, spacing):
        cx = size // 2 + dx
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=COBALT)
    return img


def render_all():
    variants = [
        ("variant_1_blue_gc", variant_1_blue_gc()),
        ("variant_2_charcoal_blue_gc", variant_2_charcoal_blue_gc()),
        ("variant_3_brackets", variant_3_brackets()),
        ("variant_4_speech_dot", variant_4_speech_dot()),
    ]
    for name, img in variants:
        # Save 512×512 master
        path_512 = OUT_DIR / f"{name}_512.png"
        img.save(path_512, "PNG", optimize=True)
        # Downscale to 256×256 with Lanczos
        small = img.resize((256, 256), Image.Resampling.LANCZOS)
        path_256 = OUT_DIR / f"{name}_256.png"
        small.save(path_256, "PNG", optimize=True)
        print(f"  ✓ {name} → {path_512.name} + {path_256.name}")


if __name__ == "__main__":
    print("Generating Get Context icons…")
    render_all()
    print("\nDone. Files in:", OUT_DIR)
