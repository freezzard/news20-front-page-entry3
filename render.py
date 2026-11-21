# Renders the Friday 20 November 2026 front page to entry.png.
#
# Layout, top to bottom on a 1024 by 1024 page: kicker rules, giant
# serif masthead date, one-line sub-headline, six-number strip, region
# tally bar, three large hero cards with painted scenes, ten medium
# cards in two rows of five, a date-check box, then the world map with
# numbered pins beside 22 one-line briefs in two columns, and a footer
# attribution line. Every text block is measured before it is drawn;
# anything that would overflow is reported instead of clipped.

import hashlib
import os
import sys

from PIL import Image, ImageDraw

from data import (
    BRIEF_ITEMS,
    BRIEF_REGIONS,
    BRIEFS_HEADING,
    DATE_CHECK_LINES,
    DATE_CHECK_TITLE,
    FOOTER_LINE,
    HERO_STORIES,
    MAP_CAPTION,
    MAP_HEADING,
    MASTHEAD_DATE,
    MASTHEAD_KICKER_LEFT,
    MASTHEAD_KICKER_RIGHT,
    MID_STORIES,
    NUMBER_STRIP,
    REGION_ORDER,
    REGION_PAINT,
    SUBHEAD_LINE,
)
from draw import (
    CARD,
    CARD_EDGE,
    INK,
    INK_SOFT,
    MUTED,
    PAPER,
    RED,
    RULE,
    draw_card_frame,
    draw_chip,
    draw_number_badge,
    draw_rule,
    draw_wrapped,
    fit_font_size,
    load_font,
    text_height_px,
    text_width_px,
    wrap_text,
)
from scenes import paint_scene

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 24
CONTENT_W = PAGE_W - MARGIN * 2
OUTPUT_NAME = "entry.png"
SIZE_CAP = 1048576

OVERFLOW_NOTES = []

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80), (-80, 73), (-75, 62), (-65, 60), (-60, 47), (-70, 42), (-75, 35), (-80, 32), (-85, 30), (-90, 21), (-97, 16), (-94, 17), (-86, 13), (-83, 9), (-79, 9), (-92, 15), (-105, 20), (-110, 24), (-117, 33), (-125, 40), (-124, 48), (-135, 58), (-150, 60), (-165, 60)],
    [(-58, 64), (-45, 60), (-40, 65), (-30, 68), (-22, 70), (-25, 76), (-40, 76), (-55, 74), (-60, 70)],
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -50), (-66, -55), (-68, -52), (-62, -45), (-58, -38), (-52, -33), (-48, -28), (-41, -23), (-35, -9), (-35, -6), (-44, -3), (-50, 0), (-55, 5), (-60, 8), (-68, 11), (-75, 10)],
    [(-17, 15), (-16, 20), (-10, 31), (-5, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (40, 15), (43, 11), (48, 11), (51, 10), (46, 5), (41, -2), (40, -10), (36, -18), (33, -26), (28, -33), (20, -35), (17, -29), (14, -22), (12, -18), (9, -1), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (2, 51), (5, 53), (8, 55), (10, 57), (8, 58), (5, 58), (5, 60), (10, 62), (12, 65), (18, 69), (25, 71), (30, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 70), (170, 67), (178, 65), (178, 62), (170, 60), (162, 56), (158, 52), (150, 59), (142, 54), (141, 50), (140, 45), (135, 43), (130, 42), (127, 40), (126, 38), (122, 38), (120, 35), (115, 32), (110, 30), (108, 22), (105, 18), (103, 12), (100, 8), (98, 10), (95, 15), (92, 21), (89, 22), (86, 20), (82, 17), (80, 13), (77, 8), (75, 12), (72, 20), (68, 23), (66, 25), (62, 25), (58, 26), (56, 27), (54, 26), (52, 25), (50, 26), (48, 29), (48, 30), (50, 29), (54, 28), (56, 26), (57, 25), (52, 24), (50, 24), (48, 22), (44, 20), (42, 15), (39, 13), (35, 17), (33, 19), (30, 22), (28, 26), (27, 31), (26, 35), (22, 37), (19, 38), (16, 38), (12, 40), (8, 38), (3, 38), (-2, 37)],
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32), (132, -32), (135, -35), (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 35), (140, 37), (141, 39), (141, 41), (142, 44), (144, 44), (143, 42), (141, 39), (140, 36), (139, 34), (136, 33), (133, 34), (131, 32)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (174, -41), (172, -43), (168, -46)],
    [(44, -16), (47, -15), (50, -16), (50, -20), (47, -24), (44, -25), (43, -21)],
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -6), (100, -2), (97, 3)],
    [(109, 1), (111, 3), (114, 4), (117, 6), (118, 2), (117, -2), (114, -3), (110, -3), (109, 0)],
    [(131, -1), (135, -2), (138, -4), (141, -5), (145, -6), (147, -7), (150, -9), (146, -8), (141, -8), (136, -4), (132, -2)],
    [(105, -6), (108, -7), (111, -7), (114, -8), (114, -7), (110, -6), (106, -6)],
]

PIN_NUDGE = {1: (0, -4), 4: (-12, -8), 5: (10, 6), 6: (8, 8), 9: (-14, 2)}


def note_overflow(message):
    OVERFLOW_NOTES.append(message)


def tally_counts():
    counts = {}
    for region in REGION_ORDER:
        counts[region] = 0
    for story in HERO_STORIES + MID_STORIES:
        counts[story["region"]] += 1
    for region in BRIEF_REGIONS:
        counts[region] += 1
    return counts


def fit_block(text, kind, max_width, max_lines, start_size, floor_size):
    size = start_size
    font = load_font(kind, size)
    lines = wrap_text(text, font, max_width)
    while len(lines) > max_lines and size > floor_size:
        size -= 1
        font = load_font(kind, size)
        lines = wrap_text(text, font, max_width)
    fitted = (font, lines)
    return fitted


def draw_masthead(pen, y):
    left_font = load_font("sans_bold", 15)
    right_font = load_font("sans_bold", 11)
    pen.text((MARGIN, y), MASTHEAD_KICKER_LEFT, font=left_font, fill=RED)
    right_wide = text_width_px(MASTHEAD_KICKER_RIGHT, right_font)
    pen.text((MARGIN + CONTENT_W - right_wide, y + 3), MASTHEAD_KICKER_RIGHT, font=right_font, fill=INK_SOFT)
    rule_y = y + 24
    draw_rule(pen, MARGIN, rule_y, CONTENT_W, weight=2)
    date_font = fit_font_size(MASTHEAD_DATE, "serif_bold", CONTENT_W, 92, 60)
    date_high = text_height_px(MASTHEAD_DATE, date_font)
    pen.text((MARGIN, rule_y + 6), MASTHEAD_DATE, font=date_font, fill=INK)
    next_y = rule_y + 6 + date_high + 4
    return next_y


def draw_subhead(pen, y):
    font = fit_font_size(SUBHEAD_LINE, "serif_italic", CONTENT_W, 20, 14)
    wide = text_width_px(SUBHEAD_LINE, font)
    pen.text((MARGIN + (CONTENT_W - wide) // 2, y), SUBHEAD_LINE, font=font, fill=INK_SOFT)
    next_y = y + text_height_px(SUBHEAD_LINE, font) + 10
    return next_y


def draw_number_strip(pen, y):
    cell_wide = CONTENT_W // len(NUMBER_STRIP)
    strip_high = 66
    value_font = load_font("serif_bold", 34)
    label_font = load_font("sans", 11)
    for index in range(len(NUMBER_STRIP)):
        value, label = NUMBER_STRIP[index]
        cell_x = MARGIN + index * cell_wide
        value_wide = text_width_px(value, value_font)
        pen.text((cell_x + (cell_wide - value_wide) // 2, y), value, font=value_font, fill=RED)
        label_lines = wrap_text(label, label_font, cell_wide - 14)
        if len(label_lines) > 2:
            note_overflow("strip label too long: " + label)
            label_lines = label_lines[:2]
        line_y = y + 42
        for line in label_lines:
            line_wide = text_width_px(line, label_font)
            pen.text((cell_x + (cell_wide - line_wide) // 2, line_y), line, font=label_font, fill=INK_SOFT)
            line_y += 13
        if index > 0:
            pen.line([(cell_x, y + 4), (cell_x, y + strip_high - 8)], fill=CARD_EDGE, width=1)
    next_y = y + strip_high + 8
    return next_y


def draw_tally_bar(pen, y):
    counts = tally_counts()
    total = 0
    for region in REGION_ORDER:
        total += counts[region]
    raw_widths = {}
    for region in REGION_ORDER:
        raw_widths[region] = counts[region] * CONTENT_W // total
    min_wide = 52
    widths = {}
    for region in REGION_ORDER:
        widths[region] = raw_widths[region]
        if widths[region] < min_wide:
            widths[region] = min_wide
    assigned = 0
    for region in REGION_ORDER:
        assigned += widths[region]
    widths["EUROPE"] += CONTENT_W - assigned
    bar_high = 26
    bar_x = MARGIN
    for region in REGION_ORDER:
        wide = widths[region]
        pen.rectangle([bar_x, y, bar_x + wide, y + bar_high], fill=REGION_PAINT[region])
        label = region + " " + str(counts[region])
        font = load_font("sans_bold", 12)
        if wide < 96:
            font = load_font("sans_bold", 10)
            name_wide = text_width_px(region, font)
            pen.text((bar_x + (wide - name_wide) // 2, y + 2), region, font=font, fill=(255, 255, 255))
            count_text = str(counts[region])
            count_wide = text_width_px(count_text, font)
            pen.text((bar_x + (wide - count_wide) // 2, y + 14), count_text, font=font, fill=(255, 255, 255))
        if wide >= 96:
            label_wide = text_width_px(label, font)
            pen.text((bar_x + (wide - label_wide) // 2, y + 6), label, font=font, fill=(255, 255, 255))
        bar_x += wide
    next_y = y + bar_high + 8
    return next_y


def draw_hero_card(page, pen, box, story):
    x0, y0, x1, y1 = box
    draw_card_frame(pen, box)
    scene_box = (x0 + 6, y0 + 6, x1 - 6, y0 + 114)
    paint_scene(page, story["scene"], scene_box)
    pen.rectangle(scene_box, outline=(90, 84, 70), width=1)
    kicker_y = y0 + 122
    draw_number_badge(pen, x0 + 18, kicker_y + 8, story["num"], radius=11)
    kicker_font = load_font("sans_bold", 11)
    pen.text((x0 + 34, kicker_y), story["kicker"], font=kicker_font, fill=RED)
    dateline_font = load_font("sans_bold", 10)
    dateline_wide = text_width_px(story["dateline"], dateline_font)
    pen.text((x1 - 8 - dateline_wide, kicker_y + 1), story["dateline"], font=dateline_font, fill=INK_SOFT)
    head_font, head_lines = fit_block(story["headline"], "serif_bold", x1 - x0 - 16, 2, 20, 16)
    if len(head_lines) > 2:
        note_overflow("hero headline overflows: " + story["headline"])
        head_lines = head_lines[:2]
    head_y = draw_wrapped(pen, x0 + 8, y0 + 142, head_lines, head_font, leading=2)
    deck_font, deck_lines = fit_block(story["deck"], "sans", x1 - x0 - 16, 3, 12, 10)
    if len(deck_lines) > 3:
        note_overflow("hero deck overflows: " + story["headline"])
        deck_lines = deck_lines[:3]
    deck_y = draw_wrapped(pen, x0 + 8, head_y + 2, deck_lines, deck_font, leading=2)
    source_font = load_font("sans_bold", 9)
    pen.text((x0 + 8, y1 - 14), "SOURCE - " + story["source"], font=source_font, fill=MUTED)
    if story["chip"]:
        chip_wide = draw_chip(pen, x1 - 8 - 62, y1 - 17, story["chip"])
        _ = chip_wide
    _ = deck_y
    return y1


def draw_mid_card(page, pen, box, story):
    x0, y0, x1, y1 = box
    draw_card_frame(pen, box)
    scene_box = (x0 + 5, y0 + 5, x1 - 5, y0 + 51)
    paint_scene(page, story["scene"], scene_box)
    pen.rectangle(scene_box, outline=(90, 84, 70), width=1)
    kicker_y = y0 + 56
    draw_number_badge(pen, x0 + 13, kicker_y + 6, story["num"], radius=9)
    kicker_font = load_font("sans_bold", 9)
    pen.text((x0 + 26, kicker_y), story["kicker"], font=kicker_font, fill=RED)
    if story["chip"]:
        chip_font = load_font("sans_bold", 8)
        chip_wide = text_width_px(story["chip"], chip_font) + 10
        pen.rounded_rectangle(
            [x1 - 6 - chip_wide, kicker_y - 1, x1 - 6, kicker_y + 11],
            radius=2,
            fill=(232, 222, 200),
            outline=RED,
            width=1,
        )
        pen.text((x1 - 6 - chip_wide + 5, kicker_y), story["chip"], font=chip_font, fill=RED)
    head_font, head_lines = fit_block(story["headline"], "serif_bold", x1 - x0 - 12, 2, 14, 11)
    if len(head_lines) > 2:
        note_overflow("mid headline overflows: " + story["headline"])
        head_lines = head_lines[:2]
    head_y = draw_wrapped(pen, x0 + 6, y0 + 70, head_lines, head_font, leading=1)
    deck_font, deck_lines = fit_block(story["deck"], "sans", x1 - x0 - 12, 2, 10, 8)
    if len(deck_lines) > 2:
        note_overflow("mid deck overflows: " + story["headline"])
        deck_lines = deck_lines[:2]
    deck_y = draw_wrapped(pen, x0 + 6, head_y + 1, deck_lines, deck_font, leading=1)
    source_font = load_font("sans", 8)
    pen.text((x0 + 6, y1 - 11), story["source"], font=source_font, fill=MUTED)
    _ = deck_y
    return y1


def draw_date_check(pen, y):
    box = (MARGIN, y, MARGIN + CONTENT_W, y + 46)
    pen.rectangle(box, fill=(244, 238, 222), outline=RULE, width=1)
    title_font = load_font("sans_bold", 11)
    pen.text((MARGIN + 10, y + 5), DATE_CHECK_TITLE, font=title_font, fill=RED)
    line_font = load_font("sans", 11)
    line_y = y + 5
    for line in DATE_CHECK_LINES:
        line_wide = text_width_px(line, line_font)
        if line_wide > CONTENT_W - 20:
            note_overflow("date check line too long")
        pen.text((MARGIN + 92, line_y), line, font=line_font, fill=INK)
        line_y += 14
    next_y = y + 46 + 8
    return next_y


def project_point(lon, lat, box):
    x0, y0, x1, y1 = box
    pad = 4
    span_x = x1 - x0 - pad * 2
    span_y = y1 - y0 - pad * 2
    px = x0 + pad + (lon + 180.0) / 360.0 * span_x
    py = y0 + pad + (78.0 - lat) / 136.0 * span_y
    return (int(px), int(py))


def draw_world_map(pen, box):
    pen.rectangle(box, fill=(232, 238, 240), outline=CARD_EDGE, width=1)
    for shape in CONTINENTS:
        points = []
        for lon, lat in shape:
            points.append(project_point(lon, lat, box))
        pen.polygon(points, fill=(208, 188, 138), outline=(150, 132, 88))
    for brief in BRIEF_ITEMS:
        _, _, _, _, lon, lat = brief
        dot_x, dot_y = project_point(lon, lat, box)
        pen.ellipse([dot_x - 2, dot_y - 2, dot_x + 2, dot_y + 2], fill=(60, 56, 48))
    for story in HERO_STORIES + MID_STORIES:
        pin_x, pin_y = project_point(story["lon"], story["lat"], box)
        nudge = PIN_NUDGE.get(story["num"], (0, 0))
        draw_number_badge(pen, pin_x + nudge[0], pin_y + nudge[1], story["num"], radius=10)


def shrink_brief_line(head, body, tail, font, max_width):
    words = body.split(" ")
    joined = " ".join(words)
    full = head + joined + tail
    while text_width_px(full, font) > max_width and len(words) > 3:
        words = words[:-1]
        joined = " ".join(words) + " \u2026"
        full = head + joined + tail
    return full


def draw_briefs(pen, x0, y, width):
    heading_font = load_font("sans_bold", 12)
    pen.text((x0, y), BRIEFS_HEADING, font=heading_font, fill=RED)
    list_y = y + 18
    col_wide = (width - 10) // 2
    brief_font = load_font("sans", 9)
    for index in range(len(BRIEF_ITEMS)):
        num, city, text, source, _, _ = BRIEF_ITEMS[index]
        column = 0
        row = index
        if index >= 11:
            column = 1
            row = index - 11
        item_x = x0 + column * (col_wide + 10)
        item_y = list_y + row * 13
        head = str(num) + ". " + city + " - "
        tail = " (" + source + ")"
        line = shrink_brief_line(head, text, tail, brief_font, col_wide)
        pen.text((item_x, item_y), line, font=brief_font, fill=INK)
    next_y = list_y + 11 * 13 + 4
    return next_y


def draw_bottom(pen, y):
    map_x0 = MARGIN
    map_wide = 306
    briefs_x0 = MARGIN + map_wide + 12
    briefs_wide = CONTENT_W - map_wide - 12
    heading_font = load_font("sans_bold", 12)
    pen.text((map_x0, y), MAP_HEADING, font=heading_font, fill=RED)
    map_box = (map_x0, y + 18, map_x0 + map_wide, y + 18 + 118)
    draw_world_map(pen, map_box)
    caption_font = load_font("sans", 9)
    pen.text((map_x0, y + 18 + 118 + 4), MAP_CAPTION, font=caption_font, fill=MUTED)
    briefs_end = draw_briefs(pen, briefs_x0, y, briefs_wide)
    next_y = briefs_end
    if map_box[3] + 16 > next_y:
        next_y = map_box[3] + 16
    return next_y


def draw_footer(pen, y):
    font = load_font("sans", 10)
    wide = text_width_px(FOOTER_LINE, font)
    pen.text((MARGIN + (CONTENT_W - wide) // 2, y), FOOTER_LINE, font=font, fill=MUTED)
    return y + 16


def render_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    pen = ImageDraw.Draw(page)
    y = 12
    y = draw_masthead(pen, y)
    y = draw_subhead(pen, y)
    y = draw_number_strip(pen, y)
    y = draw_tally_bar(pen, y)
    hero_high = 246
    hero_wide = (CONTENT_W - 22) // 3
    for index in range(len(HERO_STORIES)):
        card_x = MARGIN + index * (hero_wide + 11)
        draw_hero_card(page, pen, (card_x, y, card_x + hero_wide, y + hero_high), HERO_STORIES[index])
    y += hero_high + 8
    mid_high = 132
    mid_wide = (CONTENT_W - 40) // 5
    for row in range(2):
        for col in range(5):
            story = MID_STORIES[row * 5 + col]
            card_x = MARGIN + col * (mid_wide + 10)
            card_y = y + row * (mid_high + 8)
            draw_mid_card(page, pen, (card_x, card_y, card_x + mid_wide, card_y + mid_high), story)
    y += mid_high * 2 + 8 + 8
    y = draw_date_check(pen, y)
    y = draw_bottom(pen, y)
    y = draw_footer(pen, y + 4)
    if y > PAGE_H - 4:
        note_overflow("page bottom overflows by " + str(y - PAGE_H + 4) + " px")
    return page


def save_page(page, path):
    page.save(path, format="PNG", optimize=True)
    size = os.path.getsize(path)
    return size


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        chunk = handle.read(65536)
        while chunk:
            digest.update(chunk)
            chunk = handle.read(65536)
    return digest.hexdigest()


def main():
    page = render_page()
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, OUTPUT_NAME)
    size = save_page(page, out_path)
    if size > SIZE_CAP:
        reduced = page.convert("P", palette=Image.ADAPTIVE, colors=256)
        reduced.save(out_path, format="PNG", optimize=True)
        size = os.path.getsize(out_path)
    digest = sha256_file(out_path)
    counts = tally_counts()
    total = 0
    for region in REGION_ORDER:
        total += counts[region]
    print("rendered " + OUTPUT_NAME + ": " + str(page.size[0]) + "x" + str(page.size[1]))
    print("bytes " + str(size) + " cap " + str(SIZE_CAP) + " sha256 " + digest)
    print("stories " + str(total) + " overflow " + str(len(OVERFLOW_NOTES)))
    for note in OVERFLOW_NOTES:
        print("OVERFLOW: " + note)
    if len(OVERFLOW_NOTES) > 0:
        sys.exit(1)
    if size > SIZE_CAP:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    try: main()
    except SystemExit as sysExit:
        raise sysExit
    except Exception as renderProblem:
        print("render failed: " + str(renderProblem))
        sys.exit(1)
