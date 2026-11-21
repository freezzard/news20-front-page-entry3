# Drawing helpers for the front page: fonts, wrapping, palette, boxes.
#
# Everything here is pure Pillow. No text is drawn inside the painted
# scenes; the helpers in this file only set type for headlines, decks,
# labels and captions, and measure it so nothing overflows its card.
# Fonts are loaded once and cached by kind and size.

from PIL import ImageDraw, ImageFont

PAPER = (250, 246, 235)
PAPER_SOFT = (244, 238, 222)
INK = (26, 24, 20)
INK_SOFT = (70, 66, 58)
MUTED = (120, 114, 102)
RULE = (60, 56, 48)
CARD = (255, 252, 244)
CARD_EDGE = (180, 172, 152)
RED = (178, 38, 30)
RED_SOFT = (214, 90, 78)
BLUE = (31, 93, 140)
TEAL = (30, 120, 130)
GOLD = (176, 132, 40)
SCENE_EDGE = (90, 84, 70)
CHIP_BG = (232, 222, 200)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_PATH = FONT_DIR + "/DejaVuSerif.ttf"
SERIF_BOLD_PATH = FONT_DIR + "/DejaVuSerif-Bold.ttf"
SERIF_ITALIC_PATH = FONT_DIR + "/DejaVuSerif-Italic.ttf"
SANS_PATH = FONT_DIR + "/DejaVuSans.ttf"
SANS_BOLD_PATH = FONT_DIR + "/DejaVuSans-Bold.ttf"

_font_cache = {}


def _load_font_file(path, size):
    loaded = ImageFont.truetype(path, size)
    return loaded


def load_font(kind, size):
    key = (kind, size)
    cached = _font_cache.get(key)
    hit = cached is not None
    resolved = cached
    if hit is False:
        path = SERIF_PATH
        if kind == "serif_bold":
            path = SERIF_BOLD_PATH
        if kind == "sans":
            path = SANS_PATH
        if kind == "sans_bold":
            path = SANS_BOLD_PATH
        if kind == "serif_italic":
            path = SERIF_ITALIC_PATH
        try: resolved = _load_font_file(path, size)
        except OSError as loadProblem:
            fallback = SERIF_PATH
            if kind == "sans":
                fallback = SANS_PATH
            if kind == "sans_bold":
                fallback = SANS_BOLD_PATH
            resolved = _load_font_file(fallback, size)
            _ = loadProblem
        _font_cache[key] = resolved
    return resolved


def text_width_px(text, font):
    left, top, right, bottom = font.getbbox(text)
    span = right - left
    _ = (top, bottom)
    return span


def text_height_px(text, font):
    left, top, right, bottom = font.getbbox(text)
    span = bottom - top
    _ = (left, right)
    return span


def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        trial = word
        if current:
            trial = current + " " + word
        trial_wide = text_width_px(trial, font) > max_width
        if trial_wide and current:
            lines.append(current)
            current = word
        if trial_wide is False:
            current = trial
        if text_width_px(word, font) > max_width:
            chunk = ""
            for glyph in word:
                trial_chunk = chunk + glyph
                if text_width_px(trial_chunk, font) > max_width:
                    lines.append(chunk)
                    chunk = glyph
                if text_width_px(trial_chunk, font) <= max_width:
                    chunk = trial_chunk
            current = chunk
    if current:
        lines.append(current)
    return lines


def fit_font_size(text, kind, max_width, start_size, floor_size):
    size = start_size
    fitted = load_font(kind, size)
    while text_width_px(text, fitted) > max_width and size > floor_size:
        size -= 1
        fitted = load_font(kind, size)
    return fitted


def draw_rule(pen, x, y, width, weight=2, paint=RULE):
    pen.line([(x, y), (x + width, y)], fill=paint, width=weight)


def draw_wrapped(pen, x, y, lines, font, paint=INK, leading=4):
    pen_y = y
    for line in lines:
        pen.text((x, pen_y), line, font=font, fill=paint)
        pen_y += text_height_px(line, font) + leading
    return pen_y


def draw_centered(pen, cx, y, text, font, paint=INK):
    wide = text_width_px(text, font)
    pen.text((cx - wide // 2, y), text, font=font, fill=paint)


def draw_chip(pen, x, y, label):
    font = load_font("sans_bold", 11)
    pad_x = 6
    pad_y = 3
    label_wide = text_width_px(label, font)
    label_high = text_height_px(label, font)
    box_wide = label_wide + pad_x * 2
    box_high = label_high + pad_y * 2
    pen.rounded_rectangle(
        [x, y, x + box_wide, y + box_high], radius=3, fill=CHIP_BG, outline=RED, width=1
    )
    pen.text((x + pad_x, y + pad_y - 1), label, font=font, fill=RED)
    return box_wide


def draw_number_badge(pen, cx, cy, number, radius=11):
    pen.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=RED,
        outline=(255, 255, 255),
        width=2,
    )
    font = load_font("sans_bold", 13)
    label = str(number)
    wide = text_width_px(label, font)
    high = text_height_px(label, font)
    pen.text((cx - wide // 2, cy - high // 2 - 1), label, font=font, fill=(255, 255, 255))


def draw_card_frame(pen, box, fill=CARD, edge=CARD_EDGE, width=1):
    x0, y0, x1, y1 = box
    pen.rectangle([x0, y0, x1, y1], fill=fill, outline=edge, width=width)


def draw_soft_sky(pen, box, top_paint, bottom_paint, bands=24):
    x0, y0, x1, y1 = box
    height = y1 - y0
    band_high = height / bands
    for band in range(bands):
        mix = band / (bands - 1)
        red = int(top_paint[0] + (bottom_paint[0] - top_paint[0]) * mix)
        green = int(top_paint[1] + (bottom_paint[1] - top_paint[1]) * mix)
        blue = int(top_paint[2] + (bottom_paint[2] - top_paint[2]) * mix)
        top_y = int(y0 + band * band_high)
        bottom_y = int(y0 + (band + 1) * band_high) + 1
        pen.rectangle([x0, top_y, x1, bottom_y], fill=(red, green, blue))


def draw_sun_disc(pen, cx, cy, radius, paint=(240, 200, 90)):
    pen.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=paint,
        outline=(200, 150, 40),
        width=1,
    )


def draw_moon_disc(pen, cx, cy, radius, paint=(235, 230, 210)):
    pen.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=paint,
        outline=(180, 175, 150),
        width=1,
    )


def draw_wave_band(pen, x0, y, x1, amplitude, paint, step=14):
    points = []
    wave_x = x0
    while wave_x <= x1:
        wave_y = y + amplitude * (((wave_x // step) % 2) * 2 - 1)
        points.append((wave_x, wave_y))
        wave_x += step
    points.append((x1, y + amplitude + 6))
    points.append((x0, y + amplitude + 6))
    pen.polygon(points, fill=paint)


def draw_building_row(pen, x0, base_y, widths, heights, paint, lit=(250, 210, 110)):
    pen_x = x0
    for index in range(len(widths)):
        wide = widths[index]
        high = heights[index]
        pen.rectangle([pen_x, base_y - high, pen_x + wide, base_y], fill=paint)
        lit_on = index % 2 == 0
        if lit_on:
            pen.rectangle(
                [pen_x + wide // 4, base_y - high + 4, pen_x + wide // 2, base_y - high + 10],
                fill=lit,
            )
        pen_x += wide + 3
    return pen_x


def count_lines_needed(text, font, max_width):
    lines = wrap_text(text, font, max_width)
    total = len(lines)
    return total
