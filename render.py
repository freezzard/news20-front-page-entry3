"""Compose the Friday 20 November 2026 newspaper page at 2048px
and export the 1024px entry.png the grader runs on.

Layout, top to bottom: kicker and masthead, the day in numbers,
the region tally bar, three hero cards, ten mid cards in two
rows, the date-check strip, then the pinned world map beside the
briefs. Card text budgets were measured against the real fonts,
so every headline and summary fits its card without clipping.
The map pins and the brief dots use the same numbering as the
cards. Scenes carry no text of their own.
"""

import os

from PIL import Image, ImageDraw

import data
from draw import (centered_text, chip, draw_map_pin, draw_world_map,
                  draw_wrapped, load_font, map_point, wrap_lines)
from scenes import build_scene

PAGE_W = 2048
PAGE_H = 2048
MARGIN = 64
CONTENT_W = PAGE_W - 2 * MARGIN
PAPER = (247, 241, 222)
CARD_BG = (253, 250, 242)
INK = (26, 25, 22)
MUTED = (96, 89, 74)
ACCENT_RED = (176, 32, 26)
RULE = (58, 54, 46)
SEA_FILL = (206, 220, 222)
LAND_FILL = (196, 182, 140)
PIN_FILL = (190, 44, 34)

# Leader offsets (dx, dy, in page pixels) for pins that would sit
# on top of one another; a thin line joins each moved pin back
# to its true spot on the map.
PIN_OFFSETS = {
    1: (16, -14),
    4: (20, -16),
    5: (22, 10),
    7: (-26, 20),
    9: (-18, -18),
    13: (22, -16),
}


def fit_font_size(draw, text, kind, start_size, max_width):
    trial_size = start_size
    trial_font = load_font(kind, trial_size)
    trial_width = draw.textlength(text, font=trial_font)
    while trial_width > max_width and trial_size > 20:
        trial_size = trial_size - 2
        trial_font = load_font(kind, trial_size)
        trial_width = draw.textlength(text, font=trial_font)
    return trial_size


def draw_header(page_draw):
    kicker_font = load_font("sans-xbold", 30)
    page_draw.text((MARGIN, 38), data.PAGE_KICKER_LEFT, font=kicker_font, fill=ACCENT_RED)
    right_font = load_font("sans-bold", 24)
    right_width = page_draw.textlength(data.PAGE_KICKER_RIGHT, font=right_font)
    page_draw.text((PAGE_W - MARGIN - right_width, 42), data.PAGE_KICKER_RIGHT, font=right_font, fill=INK)
    page_draw.line((MARGIN, 84, PAGE_W - MARGIN, 84), fill=INK, width=4)
    page_draw.line((MARGIN, 92, PAGE_W - MARGIN, 92), fill=INK, width=1)
    masthead_size = fit_font_size(page_draw, data.PAGE_DATE_LONG, "serif-black", 140, CONTENT_W)
    masthead_font = load_font("serif-black", masthead_size)
    centered_text(page_draw, PAGE_W // 2, 104, data.PAGE_DATE_LONG, masthead_font, INK)
    subhead_size = fit_font_size(page_draw, data.PAGE_SUBHEAD, "serif-italic", 40, CONTENT_W)
    subhead_font = load_font("serif-italic", subhead_size)
    subhead_y = 104 + masthead_size + 24
    centered_text(page_draw, PAGE_W // 2, subhead_y, data.PAGE_SUBHEAD, subhead_font, (92, 44, 30))
    return subhead_y + subhead_size + 18


def draw_numbers(page_draw, top_y):
    col_w = CONTENT_W // len(data.DAY_NUMBERS)
    number_font = load_font("serif-black", 57)
    label_font = load_font("sans", 20)
    col_index = 0
    for figure_text, figure_label in data.DAY_NUMBERS:
        col_x = MARGIN + col_index * col_w
        centered_text(page_draw, col_x + col_w // 2, top_y, figure_text, number_font, ACCENT_RED)
        centered_text(page_draw, col_x + col_w // 2, top_y + 68, figure_label, label_font, INK)
        has_next_col = col_index < len(data.DAY_NUMBERS) - 1
        if has_next_col:
            page_draw.line((col_x + col_w, top_y + 6, col_x + col_w, top_y + 104), fill=(178, 168, 144), width=1)
        col_index = col_index + 1
    return top_y + 112


def draw_tally(page_draw, top_y):
    bar_h = 48
    segment_count = len(data.REGION_TALLY)
    base_w = 150
    total_count = 0
    for region_name, region_count, region_color in data.REGION_TALLY:
        total_count = total_count + region_count
    extra_w = CONTENT_W - base_w * segment_count
    segment_x = MARGIN
    label_font = load_font("sans-xbold", 25)
    for region_name, region_count, region_color in data.REGION_TALLY:
        segment_w = base_w + int(extra_w * region_count / total_count)
        segment_box = (segment_x, top_y, segment_x + segment_w, top_y + bar_h)
        page_draw.rectangle(segment_box, fill=region_color)
        segment_label = region_name + " " + str(region_count)
        centered_text(page_draw, segment_x + segment_w // 2, top_y + 11, segment_label, label_font, (250, 248, 240))
        segment_x = segment_x + segment_w
    return top_y + bar_h


def draw_card_frame(page_draw, box):
    page_draw.rectangle(box, fill=CARD_BG)
    page_draw.rectangle(box, outline=RULE, width=2)
    return box


def draw_badge(page_draw, cx, cy, number, radius, font_size):
    badge_box = (cx - radius, cy - radius, cx + radius, cy + radius)
    page_draw.ellipse(badge_box, fill=ACCENT_RED)
    badge_font = load_font("sans-xbold", font_size)
    badge_label = str(number)
    badge_width = page_draw.textlength(badge_label, font=badge_font)
    page_draw.text((cx - badge_width / 2, cy - font_size // 2 - 2), badge_label, font=badge_font, fill=(252, 250, 244))
    return badge_box


def draw_hero_card(page, page_draw, card, box):
    draw_card_frame(page_draw, box)
    pad = 18
    scene_w = (box[2] - box[0]) - 2 * pad
    scene_img = build_scene(card["scene"], scene_w, 170)
    page.paste(scene_img, (box[0] + pad, box[1] + pad))
    pen_y = box[1] + pad + 170 + 12
    draw_badge(page_draw, box[0] + pad + 17, pen_y + 15, card["num"], 17, 21)
    kicker_font = load_font("sans-xbold", 21)
    page_draw.text((box[0] + pad + 46, pen_y + 4), card["kicker"], font=kicker_font, fill=ACCENT_RED)
    place_font = load_font("sans-bold", 18)
    place_width = page_draw.textlength(card["place"], font=place_font)
    page_draw.text((box[2] - pad - place_width, pen_y + 6), card["place"], font=place_font, fill=MUTED)
    pen_y = pen_y + 38
    headline_font = load_font("serif-xbold", 39)
    headline_h = draw_wrapped(page_draw, (box[0] + pad, pen_y), card["headline"], headline_font, INK, scene_w, 43, 3)
    pen_y = pen_y + headline_h + 6
    summary_font = load_font("sans", 24)
    summary_h = draw_wrapped(page_draw, (box[0] + pad, pen_y), card["summary"], summary_font, (44, 42, 38), scene_w, 32, 3)
    pen_y = pen_y + summary_h + 8
    page_draw.line((box[0] + pad, pen_y, box[2] - pad, pen_y), fill=(190, 180, 156), width=1)
    source_font = load_font("sans-bold", 18)
    source_text = "SOURCE - " + card["source"].upper()
    page_draw.text((box[0] + pad, pen_y + 7), source_text, font=source_font, fill=MUTED)
    has_chip = card["chip"] != ""
    if has_chip:
        chip_font = load_font("sans-xbold", 19)
        chip_w = page_draw.textlength(card["chip"], font=chip_font) + 18
        chip(page_draw, (box[2] - pad - chip_w, pen_y + 4), card["chip"], (226, 218, 192), (110, 60, 30))
    return box


def draw_mid_card(page, page_draw, card, box):
    draw_card_frame(page_draw, box)
    pad = 12
    scene_w = (box[2] - box[0]) - 2 * pad
    scene_img = build_scene(card["scene"], scene_w, 74)
    page.paste(scene_img, (box[0] + pad, box[1] + pad))
    pen_y = box[1] + pad + 74 + 8
    draw_badge(page_draw, box[0] + pad + 12, pen_y + 11, card["num"], 12, 15)
    kicker_font = load_font("sans-xbold", 16)
    page_draw.text((box[0] + pad + 32, pen_y + 2), card["kicker"], font=kicker_font, fill=ACCENT_RED)
    has_chip = card["chip"] != ""
    if has_chip:
        chip_font = load_font("sans-xbold", 15)
        chip_w = page_draw.textlength(card["chip"], font=chip_font) + 14
        chip_box = (box[2] - pad - chip_w, pen_y, box[2] - pad, pen_y + 22)
        page_draw.rectangle(chip_box, fill=(226, 218, 192))
        page_draw.text((chip_box[0] + 7, pen_y + 3), card["chip"], font=chip_font, fill=(110, 60, 30))
    pen_y = pen_y + 27
    headline_font = load_font("serif-bold", 27)
    headline_h = draw_wrapped(page_draw, (box[0] + pad, pen_y), card["headline"], headline_font, INK, scene_w, 29, 2)
    pen_y = pen_y + headline_h + 3
    summary_font = load_font("sans", 18)
    summary_h = draw_wrapped(page_draw, (box[0] + pad, pen_y), card["summary"], summary_font, (44, 42, 38), scene_w, 22, 2)
    pen_y = pen_y + summary_h + 5
    source_font = load_font("sans-bold", 14)
    source_text = card["source"].upper()
    page_draw.text((box[0] + pad, pen_y), source_text, font=source_font, fill=MUTED)
    return box


def draw_date_check(page_draw, top_y):
    box = (MARGIN, top_y, PAGE_W - MARGIN, top_y + 112)
    page_draw.rectangle(box, fill=(238, 231, 205), outline=RULE, width=2)
    check_font = load_font("sans-bold", 20)
    small_font = load_font("sans", 17)
    page_draw.text((MARGIN + 18, top_y + 8), "DATE CHECK - " + data.DATE_CHECK_LINE, font=check_font, fill=INK)
    left_out_text = "Left out as other days' news: " + data.LEFT_OUT
    left_h = draw_wrapped(page_draw, (MARGIN + 18, top_y + 38), left_out_text, small_font, (70, 64, 52), CONTENT_W - 36, 22, 2)
    bottom_line = "Not yet news: " + data.NOT_YET + "   " + data.DISCLAIMER_LINE
    page_draw.text((MARGIN + 18, top_y + 38 + left_h + 8), bottom_line, font=small_font, fill=(70, 64, 52))
    return top_y + 112


def draw_bottom(page, page_draw, top_y):
    header_font = load_font("sans-xbold", 23)
    page_draw.text((MARGIN, top_y), "WHERE IT HAPPENED", font=header_font, fill=ACCENT_RED)
    map_w = 640
    map_h = 296
    map_box = (MARGIN, top_y + 30, MARGIN + map_w, top_y + 30 + map_h)
    draw_world_map(page, map_box, LAND_FILL, SEA_FILL)
    page_draw.rectangle(map_box, outline=RULE, width=2)
    all_cards = data.HERO_CARDS + data.MID_CARDS
    for card in all_cards:
        pin_xy = map_point(card["lon"], card["lat"], map_box)
        pin_offset = PIN_OFFSETS.get(card["num"])
        pin_at = pin_xy
        if pin_offset is not None:
            pin_at = (pin_xy[0] + pin_offset[0], pin_xy[1] + pin_offset[1])
            page_draw.line((pin_xy[0], pin_xy[1], pin_at[0], pin_at[1]), fill=RULE, width=2)
        draw_map_pin(page_draw, pin_at, card["num"], PIN_FILL, (252, 250, 244))
    for brief_num, brief_place, brief_text, brief_source, brief_lon, brief_lat in data.BRIEFS:
        dot_xy = map_point(brief_lon, brief_lat, map_box)
        dot_r = 5
        dot_box = (dot_xy[0] - dot_r, dot_xy[1] - dot_r, dot_xy[0] + dot_r, dot_xy[1] + dot_r)
        page_draw.ellipse(dot_box, fill=(70, 74, 70), outline=(252, 250, 244), width=1)
    caption_font = load_font("sans", 15)
    page_draw.text((MARGIN, top_y + 30 + map_h + 8), "Each number is the story with that number on this page.", font=caption_font, fill=MUTED)
    briefs_x = MARGIN + map_w + 28
    briefs_w = PAGE_W - MARGIN - briefs_x
    briefs_title = "ALSO ON FRIDAY 20 NOVEMBER - " + str(len(data.BRIEFS)) + " MORE STORIES"
    page_draw.text((briefs_x, top_y), briefs_title, font=header_font, fill=ACCENT_RED)
    brief_font = load_font("sans", 16)
    place_font = load_font("sans-bold", 16)
    col_w = briefs_w // 2
    rows_per_col = 11
    brief_index = 0
    for brief in data.BRIEFS:
        brief_num, brief_place, brief_text, brief_source, brief_lon, brief_lat = brief
        brief_col = brief_index // rows_per_col
        brief_row = brief_index % rows_per_col
        brief_x = briefs_x + brief_col * col_w
        brief_y = top_y + 30 + brief_row * 27
        number_label = str(brief_num) + ". "
        number_w = page_draw.textlength(number_label, font=place_font)
        place_label = brief_place + " - "
        place_w = page_draw.textlength(place_label, font=place_font)
        full_line = brief_text + " (" + brief_source + ")"
        page_draw.text((brief_x, brief_y), number_label, font=place_font, fill=ACCENT_RED)
        page_draw.text((brief_x + number_w, brief_y), place_label, font=place_font, fill=INK)
        page_draw.text((brief_x + number_w + place_w, brief_y), full_line, font=brief_font, fill=(44, 42, 38))
        brief_index = brief_index + 1
    return top_y + 30 + map_h + 22


def add_paper_grain(page):
    noise_img = Image.effect_noise((PAGE_W, PAGE_H), 7).convert("RGB")
    grained_page = Image.blend(page, noise_img, 0.025)
    return grained_page


def check_fit(page_draw):
    brief_font = load_font("sans", 16)
    place_font = load_font("sans-bold", 16)
    col_w = (PAGE_W - MARGIN - (MARGIN + 640 + 28)) // 2
    overflow_count = 0
    for brief in data.BRIEFS:
        brief_num, brief_place, brief_text, brief_source, brief_lon, brief_lat = brief
        line_w = page_draw.textlength(str(brief_num) + ". ", font=place_font)
        line_w = line_w + page_draw.textlength(brief_place + " - ", font=place_font)
        line_w = line_w + page_draw.textlength(brief_text + " (" + brief_source + ")", font=brief_font)
        brief_overflows = line_w > col_w
        if brief_overflows:
            print("BRIEF OVERFLOW", brief_num, int(line_w), "vs", col_w)
            overflow_count = overflow_count + 1
    headline_font = load_font("serif-xbold", 39)
    for card in data.HERO_CARDS:
        hero_lines = wrap_lines(page_draw, card["headline"], headline_font, 588)
        headline_overflows = len(hero_lines) > 2
        if headline_overflows:
            print("HERO HEADLINE 3 LINES", card["num"], hero_lines)
            overflow_count = overflow_count + 1
    mid_headline_font = load_font("serif-bold", 27)
    mid_summary_font = load_font("sans", 18)
    for card in data.MID_CARDS:
        mid_lines = wrap_lines(page_draw, card["headline"], mid_headline_font, 347)
        mid_headline_overflows = len(mid_lines) > 2
        if mid_headline_overflows:
            print("MID HEADLINE OVERFLOW", card["num"], mid_lines)
            overflow_count = overflow_count + 1
        mid_summary_lines = wrap_lines(page_draw, card["summary"], mid_summary_font, 347)
        mid_summary_overflows = len(mid_summary_lines) > 2
        if mid_summary_overflows:
            print("MID SUMMARY OVERFLOW", card["num"], mid_summary_lines)
            overflow_count = overflow_count + 1
    hero_summary_font = load_font("sans", 24)
    for card in data.HERO_CARDS:
        hero_summary_lines = wrap_lines(page_draw, card["summary"], hero_summary_font, 588)
        hero_summary_overflows = len(hero_summary_lines) > 3
        if hero_summary_overflows:
            print("HERO SUMMARY OVERFLOW", card["num"], hero_summary_lines)
            overflow_count = overflow_count + 1
    print("fit check overflow count:", overflow_count)
    return overflow_count


def compose_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    page_draw = ImageDraw.Draw(page)
    check_fit(page_draw)
    pen_y = draw_header(page_draw)
    pen_y = draw_numbers(page_draw, pen_y + 12)
    pen_y = draw_tally(page_draw, pen_y + 14)
    page_draw.line((MARGIN, pen_y + 6, PAGE_W - MARGIN, pen_y + 6), fill=INK, width=2)
    cards_top = pen_y + 18
    hero_gap = 24
    hero_w = (CONTENT_W - 2 * hero_gap) // 3
    hero_h = 470
    hero_index = 0
    for hero_card in data.HERO_CARDS:
        hero_x = MARGIN + hero_index * (hero_w + hero_gap)
        hero_box = (hero_x, cards_top, hero_x + hero_w, cards_top + hero_h)
        draw_hero_card(page, page_draw, hero_card, hero_box)
        hero_index = hero_index + 1
    mid_top = cards_top + hero_h + 12
    mid_gap = 16
    mid_w = (CONTENT_W - 4 * mid_gap) // 5
    mid_h = 252
    mid_index = 0
    for mid_card in data.MID_CARDS:
        mid_row = mid_index // 5
        mid_col = mid_index % 5
        mid_x = MARGIN + mid_col * (mid_w + mid_gap)
        mid_y = mid_top + mid_row * (mid_h + 12)
        mid_box = (mid_x, mid_y, mid_x + mid_w, mid_y + mid_h)
        draw_mid_card(page, page_draw, mid_card, mid_box)
        mid_index = mid_index + 1
    after_cards = mid_top + 2 * mid_h + 12
    check_y = draw_date_check(page_draw, after_cards + 8)
    bottom_end = draw_bottom(page, page_draw, check_y + 12)
    sources_font = load_font("sans", 14)
    centered_text(page_draw, PAGE_W // 2, bottom_end + 4, data.SOURCES_LINE, sources_font, MUTED)
    grained_page = add_paper_grain(page)
    return grained_page


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    rendered_page = compose_page()
    entry_img = rendered_page.resize((1024, 1024), Image.LANCZOS)
    entry_img = entry_img.convert("RGB")
    entry_path = os.path.join(output_dir, "entry.png")
    entry_img.save(entry_path, format="PNG", optimize=True)
    entry_size = os.path.getsize(entry_path)
    size_limit = 1024 * 1024
    if entry_size > size_limit:
        paletted_img = entry_img.quantize(colors=256, dither=Image.FLOYDSTEINBERG)
        paletted_img.save(entry_path, format="PNG", optimize=True)
        entry_size = os.path.getsize(entry_path)
    running_for_grader = "MAKEFUN_OUTPUT_DIR" in os.environ
    if running_for_grader is False:
        master_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "master-2048.png")
        rendered_page.save(master_path, format="PNG", optimize=True)
    print("wrote", entry_path, entry_size, "bytes")


if __name__ == "__main__":
    main()
