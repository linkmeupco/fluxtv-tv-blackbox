#!/usr/bin/env python3
"""
Generates all required Android image assets for FluxTV TV launcher:
  - tv_banner.png      320x180  (Android TV home screen banner)
  - ic_launcher.png    at hdpi / xhdpi / xxhdpi densities

Pure stdlib — no Pillow needed.
"""
import struct, zlib, os

# ── PNG helpers ──────────────────────────────────────────────────────────────

def _chunk(tag, data):
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', crc)

def write_png(path, width, height, get_pixel):
    """get_pixel(x, y) -> (r, g, b)"""
    raw = b''
    for y in range(height):
        raw += b'\x00'
        for x in range(width):
            r, g, b = get_pixel(x, y)
            raw += bytes([r, g, b])

    ihdr = _chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    idat = _chunk(b'IDAT', zlib.compress(raw, 6))
    iend = _chunk(b'IEND', b'')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' + ihdr + idat + iend)
    print(f'  ✅  {path}  ({width}x{height})')


# ── Colour palette ────────────────────────────────────────────────────────────
BG    = (20,  20,  20)    # #141414  dark background
RED   = (229,  9,  20)    # #E50914  FluxTV brand red
WHITE = (255, 255, 255)
GREY  = (80,  80,  80)


# ── TV Banner  320 × 180 ─────────────────────────────────────────────────────

def make_banner():
    W, H = 320, 180

    # Build pixel map: dark bg + left red accent bar + text block pixels
    pixels = {}

    # Red left accent bar (20 px wide)
    for y in range(H):
        for x in range(20):
            pixels[(x, y)] = RED

    # "FLUXTV" rendered as 5×7 pixel-font blocks, scaled 3×
    # Each letter defined as a list of (col, row) ON pixels in a 5×7 grid
    FONT = {
        'F': [(0,0),(1,0),(2,0),(3,0),(4,0),
              (0,1),(0,2),(1,2),(2,2),(3,2),
              (0,3),(0,4),(0,5),(0,6)],
        'L': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
              (1,6),(2,6),(3,6),(4,6)],
        'U': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),
              (1,6),(2,6),(3,6),
              (4,0),(4,1),(4,2),(4,3),(4,4),(4,5)],
        'X': [(0,0),(4,0),(1,1),(3,1),(2,2),(2,3),(1,3),(3,3),
              (1,5),(3,5),(0,6),(4,6),(2,4)],
        'T': [(0,0),(1,0),(2,0),(3,0),(4,0),
              (2,1),(2,2),(2,3),(2,4),(2,5),(2,6)],
        'V': [(0,0),(4,0),(0,1),(4,1),(0,2),(4,2),
              (1,3),(3,3),(1,4),(3,4),(2,5),(2,6)],
    }

    SCALE = 4        # each font pixel → 4×4 block
    LETTER_GAP = 3   # px between letters
    START_X = 34     # start after the red bar
    START_Y = (H - 7 * SCALE) // 2  # vertically centred

    cx = START_X
    for ch in 'FLUXTV':
        for (fc, fr) in FONT[ch]:
            for dy in range(SCALE):
                for dx in range(SCALE):
                    pixels[(cx + fc * SCALE + dx, START_Y + fr * SCALE + dy)] = WHITE
        cx += 5 * SCALE + LETTER_GAP

    # Add subtle "Watch Free" tagline below
    TAG = "WATCH FREE"
    TAG_Y = START_Y + 7 * SCALE + 8
    TAG_X = START_X
    SMALL_FONT = {
        'W': [(0,0),(4,0),(0,1),(4,1),(0,2),(2,2),(4,2),(1,3),(3,3),(2,4)],
        'A': [(2,0),(1,1),(3,1),(0,2),(4,2),(0,3),(1,3),(2,3),(3,3),(4,3),(0,4),(4,4)],
        'T': [(0,0),(1,0),(2,0),(3,0),(4,0),(2,1),(2,2),(2,3),(2,4)],
        'C': [(1,0),(2,0),(3,0),(0,1),(0,2),(0,3),(1,4),(2,4),(3,4)],
        'H': [(0,0),(4,0),(0,1),(4,1),(0,2),(1,2),(2,2),(3,2),(4,2),(0,3),(4,3),(0,4),(4,4)],
        'F': [(0,0),(1,0),(2,0),(3,0),(4,0),(0,1),(0,2),(1,2),(2,2),(0,3),(0,4)],
        'R': [(0,0),(1,0),(2,0),(3,0),(0,1),(4,1),(0,2),(1,2),(2,2),(3,2),(0,3),(3,3),(0,4),(4,4)],
        'E': [(0,0),(1,0),(2,0),(3,0),(4,0),(0,1),(0,2),(1,2),(2,2),(0,3),(0,4),(1,4),(2,4),(3,4),(4,4)],
        ' ': [],
    }
    S2 = 2
    tx = TAG_X
    for ch in TAG:
        if ch in SMALL_FONT:
            for (fc, fr) in SMALL_FONT[ch]:
                for dy in range(S2):
                    for dx in range(S2):
                        px = (tx + fc * S2 + dx, TAG_Y + fr * S2 + dy)
                        if 0 <= px[0] < W and 0 <= px[1] < H:
                            pixels[px] = GREY
        tx += 5 * S2 + 2

    def get_pixel(x, y):
        return pixels.get((x, y), BG)

    write_png('app/src/main/res/drawable-nodpi/tv_banner.png', W, H, get_pixel)


# ── Launcher icon ─────────────────────────────────────────────────────────────

def make_icon(size, out_path):
    """Circular icon: dark bg, red circle, white 'F' glyph."""
    cx, cy = size / 2, size / 2
    radius = size * 0.45
    inner  = size * 0.30

    # Simple F glyph coords (fraction of size), 3 strokes
    stroke_w = size * 0.08

    def get_pixel(x, y):
        dx, dy2 = x - cx, y - cy
        dist = (dx*dx + dy2*dy2) ** 0.5

        # Outside circle → transparent bg colour
        if dist > radius:
            return BG

        # Red circle background
        col = RED

        # White "F" glyph
        # Vertical stroke
        fx0 = cx - size * 0.18
        fxw = stroke_w
        fy0 = cy - size * 0.32
        fh  = size * 0.64

        if fx0 <= x <= fx0 + fxw and fy0 <= y <= fy0 + fh:
            return WHITE

        # Top horizontal
        th_y0 = fy0
        th_x1 = cx + size * 0.20
        if fx0 <= x <= th_x1 and th_y0 <= y <= th_y0 + stroke_w:
            return WHITE

        # Mid horizontal
        mh_y0 = cy - stroke_w * 0.5
        mh_x1 = cx + size * 0.08
        if fx0 <= x <= mh_x1 and mh_y0 <= y <= mh_y0 + stroke_w:
            return WHITE

        return col

    write_png(out_path, size, size, get_pixel)


# ── Run ───────────────────────────────────────────────────────────────────────

print('\nGenerating FluxTV Android TV assets...\n')
make_banner()

# Launcher icons
# hdpi=72, xhdpi=96, xxhdpi=144, xxxhdpi=192
for density, size in [('hdpi', 72), ('xhdpi', 96), ('xxhdpi', 144), ('xxxhdpi', 192)]:
    make_icon(size, f'app/src/main/res/mipmap-{density}/ic_launcher.png')
    make_icon(size, f'app/src/main/res/mipmap-{density}/ic_launcher_round.png')

print('\nAll assets generated ✅\n')
