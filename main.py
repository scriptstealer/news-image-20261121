#!/usr/bin/env python3
"""THE WORLD TODAY -- front page summing up Saturday 21 November 2026.

Procedural PIL drawing only. No network, no randomness, no timestamps in
the output: two runs produce byte-identical PNGs.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
GAP = 16

INK = (18, 18, 18)
PAPER = (250, 248, 240)
RED = (178, 24, 24)
DARK_RED = (140, 16, 16)
PANEL = (255, 255, 255)
PANEL_LINE = (120, 120, 120)
MUTED = (90, 90, 90)
BLUE = (28, 84, 150)
SKY = (176, 214, 240)
SEA = (46, 110, 168)
ORANGE = (232, 116, 24)
YELLOW = (246, 196, 52)
GREEN = (46, 130, 72)

# ---------------------------------------------------------------- fonts
# Defensive font loading: try a list of candidate files in a list of
# directories, and if nothing exists fall back to Pillow's built-in font.
# A missing font must NEVER crash the program.
DEFAULT_FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/noto",
    "/usr/share/fonts/truetype/liberation2",
    "/usr/share/fonts",
    "/usr/local/share/fonts",
]
BOLD_NAMES = [
    "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "NotoSans-Bold.ttf",
    "FreeSansBold.ttf", "DejaVuSansCondensed-Bold.ttf",
]
REGULAR_NAMES = [
    "DejaVuSans.ttf", "LiberationSans-Regular.ttf", "NotoSans-Regular.ttf",
    "FreeSans.ttf", "DejaVuSansCondensed.ttf",
]


def _font_dirs():
    override = os.environ.get("MAKEFUN_FONT_DIR")
    if override:
        return [override]
    return DEFAULT_FONT_DIRS


def _find_font(names):
    for directory in _font_dirs():
        for name in names:
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                return path
    return None


def _load(size, bold):
    path = _find_font(BOLD_NAMES if bold else REGULAR_NAMES)
    if path is not None:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


def font(size, bold=False):
    return _load(size, bold)


# ---------------------------------------------------------------- text
def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def text_block(draw, text, fnt, x, y, max_width, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_width)
    return draw_lines(draw, lines, fnt, x, y, fill, leading)


# ---------------------------------------------------------------- pictures
def burst(draw, cx, cy, r, color1, color2):
    """Starburst explosion: alternating long/short spikes."""
    import math
    pts = []
    for i in range(24):
        ang = math.pi * 2 * i / 24
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=color1)
    draw.ellipse([cx - r * 0.42, cy - r * 0.42, cx + r * 0.42, cy + r * 0.42],
                 fill=color2)


def skyline(draw, x, y, w, h, color):
    """Simple city skyline silhouettes with lit windows."""
    import random
    rng = random.Random(7)
    bx = x
    while bx < x + w - 18:
        bw = rng.randint(22, 44)
        bh = rng.randint(int(h * 0.35), h)
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=color)
        for wy in range(y + h - bh + 6, y + h - 6, 12):
            for wx in range(bx + 5, bx + bw - 5, 11):
                if rng.random() < 0.4:
                    draw.rectangle([wx, wy, wx + 4, wy + 5], fill=YELLOW)
        bx += bw + 4


def sea_waves(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    for i, wy in enumerate(range(y + 8, y + h - 4, 14)):
        off = (i % 2) * 12
        for wx in range(x + 6 + off, x + w - 10, 26):
            draw.arc([wx, wy, wx + 16, wy + 10], 180, 360, fill=(255, 255, 255),
                     width=2)


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 160, 210),
                 outline=BLUE, width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=BLUE,
                 width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=BLUE, width=2)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=BLUE,
             width=2)
    draw.ellipse([cx - r * 0.75, cy - r * 0.55, cx - r * 0.15, cy - r * 0.1],
                 fill=GREEN)
    draw.ellipse([cx + r * 0.1, cy + r * 0.1, cx + r * 0.7, cy + r * 0.55],
                 fill=GREEN)


def draw_chart_down(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 240, 244))
    draw.line([x + 14, y + 10, x + 14, y + h - 14], fill=INK, width=2)
    draw.line([x + 14, y + h - 14, x + w - 10, y + h - 14], fill=INK, width=2)
    pts = [(x + 20, y + 22), (x + 55, y + 34), (x + 90, y + 30),
           (x + 125, y + 58), (x + 160, y + 76), (x + 195, y + 96)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    draw.polygon([(x + 195, y + 96), (x + 178, y + 88), (x + 188, y + 108)],
                 fill=RED)


def draw_quake(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
    crack = [(x + 10, y + 8), (x + 40, y + 34), (x + 28, y + 58),
             (x + 62, y + 84), (x + 48, y + 110)]
    draw.line(crack, fill=(90, 60, 30), width=5, joint="curve")
    draw.line([(x + 100, y + 20), (x + 118, y + 40), (x + 132, y + 34),
               (x + 150, y + 62), (x + 168, y + 44), (x + 190, y + 74)],
              fill=RED, width=3, joint="curve")
    draw.rectangle([x + 130, y + 78, x + 196, y + 104], fill=(120, 96, 70))
    draw.polygon([(x + 130, y + 78), (x + 163, y + 58), (x + 196, y + 78)],
                 fill=(150, 60, 50))


def draw_shield(draw, cx, cy, s):
    pts = [(cx, cy - s), (cx + s * 0.85, cy - s * 0.55),
           (cx + s * 0.85, cy + s * 0.25), (cx, cy + s),
           (cx - s * 0.85, cy + s * 0.25), (cx - s * 0.85, cy - s * 0.55)]
    draw.polygon(pts, fill=BLUE, outline=(255, 255, 255), width=3)
    # Five-pointed star in the middle of the shield.
    import math
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = s * 0.42 if i % 2 == 0 else s * 0.18
        star.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(star, fill=(255, 255, 255))


def draw_thermometer(draw, x, y, h):
    draw.rounded_rectangle([x, y, x + 22, y + h], radius=11, fill=(255, 255, 255),
                           outline=RED, width=3)
    draw.ellipse([x - 8, y + h - 16, x + 30, y + h + 6], fill=RED,
                 outline=DARK_RED, width=2)
    draw.rectangle([x + 8, y + 12, x + 14, y + h - 8], fill=RED)
    for i in range(4):
        ty = y + 14 + i * ((h - 30) // 3)
        draw.line([x + 22, ty, x + 30, ty], fill=INK, width=2)


# ---------------------------------------------------------------- layout
def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=PANEL_LINE,
                   width=2)


def story_panel(draw, x, y, w, h, art, headline, sub):
    """A panel: pictorial illustration on top, headline, one sub-line."""
    panel(draw, x, y, w, h)
    art_h = 112
    art(draw, x + 2, y + 2, w - 4, art_h)
    draw.line([x, y + art_h + 2, x + w, y + art_h + 2], fill=PANEL_LINE,
              width=1)
    tx = x + 12
    ty = y + art_h + 12
    tw = w - 24
    hf = font(27, bold=True)
    end_y = text_block(draw, headline, hf, tx, ty, tw, leading=31)
    sf = font(18)
    text_block(draw, sub, sf, tx, end_y + 4, tw, fill=MUTED, leading=20)


def lead_art(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    skyline(draw, x, y + h - 78, w, 78, (70, 80, 96))
    burst(draw, x + w - 90, y + 62, 52, ORANGE, YELLOW)
    burst(draw, x + 90, y + 92, 34, ORANGE, YELLOW)
    draw.line([(x + 30, y + 24), (x + 146, y + 64)], fill=(60, 60, 60),
              width=5)
    draw.ellipse([x + 138, y + 56, x + 154, y + 72], fill=(60, 60, 60))
    draw.polygon([(x + 152, y + 58), (x + 172, y + 70), (x + 150, y + 74)],
                 fill=(60, 60, 60))
    sea_waves(draw, x, y + h - 26, w, 26)


def art_kryvyi(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 214, 190))
    skyline(draw, x, y + h - 70, w, 70, (96, 88, 80))
    burst(draw, x + w // 2, y + 52, 40, ORANGE, YELLOW)
    draw.ellipse([x + w // 2 - 58, y + 22, x + w // 2 - 6, y + 50],
                 fill=(140, 140, 140))
    draw.ellipse([x + w // 2 + 8, y + 14, x + w // 2 + 62, y + 42],
                 fill=(160, 160, 160))


def art_mexico(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 214))
    draw_shield(draw, x + w // 2 - 30, y + h // 2, 44)
    for i in range(4):
        bx = x + w - 78 + i * 16
        draw.rectangle([bx, y + 10, bx + 8, y + h - 10], fill=(60, 60, 60))


def art_cop(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(220, 235, 245))
    draw_globe(draw, x + w // 2 - 40, y + h // 2, 44)
    draw_thermometer(draw, x + w - 58, y + 14, h - 28)


def art_stocks(draw, x, y, w, h):
    draw_chart_down(draw, x + 8, y + 8, w - 16, h - 16)
    draw.rectangle([x + w - 66, y + 10, x + w - 14, y + 34], fill=RED)
    draw.text((x + w - 60, y + 13), "AI", font=font(20, bold=True),
              fill=(255, 255, 255))


def art_quake(draw, x, y, w, h):
    draw_quake(draw, x, y, w, h)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    mast = font(66, bold=True)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=mast)
    draw.text(((W - tw) / 2, 10), title, font=mast, fill=INK)
    draw.line([MARGIN, 92, W - MARGIN, 92], fill=INK, width=3)
    draw.line([MARGIN, 97, W - MARGIN, 97], fill=INK, width=1)

    # Red date band
    draw.rectangle([MARGIN, 106, W - MARGIN, 158], fill=RED)
    date_font = font(42, bold=True)
    date_text = "SATURDAY, 21 NOVEMBER 2026"
    dw = draw.textlength(date_text, font=date_font)
    draw.text(((W - dw) / 2, 114), date_text, font=date_font,
              fill=(255, 255, 255))

    # Lead story: Iran strikes US bases in Bahrain
    lx, ly, lw, lh = MARGIN, 170, W - 2 * MARGIN, 238
    panel(draw, lx, ly, lw, lh)
    lead_art(draw, lx + 2, ly + 2, 372, lh - 4)
    draw.line([lx + 374, ly, lx + 374, ly + lh], fill=PANEL_LINE, width=1)
    tx = lx + 392
    ty = ly + 18
    tw2 = lx + lw - 16 - tx
    kicker = font(19, bold=True)
    draw.text((tx, ty), "MIDDLE EAST  |  LEAD STORY", font=kicker, fill=RED)
    hf = font(38, bold=True)
    end_y = text_block(draw, "IRAN STRIKES U.S. BASES IN BAHRAIN", hf, tx,
                       ty + 30, tw2, leading=44)
    sf = font(20)
    text_block(draw,
               "Tehran says it hit two American positions; Bahrain reports a "
               "fire at a civilian industrial site. No injuries reported.",
               sf, tx, end_y + 8, tw2, fill=MUTED, leading=24)

    # Grid: 5 stories + In Brief
    gy = 424
    gh = 272
    col_w = (W - 2 * MARGIN - 2 * GAP) // 3
    stories = [
        (art_kryvyi, "RUSSIAN MISSILE HITS KRYVYI RIH",
         "Two killed, dozens hurt in Zelensky's hometown."),
        (art_mexico, "MEXICO CAPTURES CARTEL BOSS",
         "FBI most-wanted 'Chapo Isidro' seized; 11 die in violence."),
        (art_cop, "COP31 TALKS RUN PAST DEADLINE",
         "Antalya summit stalls over fossil-fuel language."),
        (art_stocks, "AI SELL-OFF HITS WALL STREET",
         "Stocks fall; worst week since the Covid crash."),
        (art_quake, "QUAKE SHAKES BANDA SEA",
         "Magnitude 6.8 tremor off Timor-Leste."),
    ]
    for i, (art, head, sub) in enumerate(stories):
        row, col = divmod(i, 3)
        x = MARGIN + col * (col_w + GAP)
        y = gy + row * (gh + GAP)
        story_panel(draw, x, y, col_w, gh, art, head, sub)

    # In Brief panel (bottom right of the grid)
    bx = MARGIN + 2 * (col_w + GAP)
    by = gy + gh + GAP
    panel(draw, bx, by, col_w, gh)
    bf = font(22, bold=True)
    draw.text((bx + 12, by + 10), "IN BRIEF", font=bf, fill=RED)
    draw.line([bx + 12, by + 42, bx + col_w - 12, by + 42], fill=PANEL_LINE,
              width=1)
    brief_font = font(18)
    briefs = [
        "Bolsonaro taken to intensive care in Brasilia.",
        "France marches over the cost of living.",
        "France beat Argentina 45-17, reach rugby final.",
    ]
    yy = by + 54
    for item in briefs:
        # Drawn dot, not a bullet glyph: the fallback font may lack U+2022.
        draw.ellipse([bx + 14, yy + 7, bx + 20, yy + 13], fill=INK)
        yy = text_block(draw, item, brief_font, bx + 30, yy, col_w - 42,
                        leading=22)
        yy += 12

    # Footer
    ff = font(15)
    footer = "THE WORLD TODAY  |  Saturday 21 November 2026  |  World news in one page"
    fw = draw.textlength(footer, font=ff)
    draw.text(((W - fw) / 2, 992), footer, font=ff, fill=MUTED)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print("wrote", path, img.size)


if __name__ == "__main__":
    main()
