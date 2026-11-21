# Painted scenes for the 13 card pictures: one small illustration each.
#
# Every scene is drawn with plain Pillow shapes on a fixed virtual
# canvas of 200 by 110, then resized into the card's picture box. The
# virtual canvas keeps every painter honest: no shape can spill past
# the picture box onto the card's text, whatever box size the layout
# hands the scene. No scene holds any text. The dispatcher at the
# bottom maps the scene key from the data file to its painter, and a
# missing key falls back to a plain skyline so a card never ships empty.

import math

from PIL import Image, ImageDraw

from draw import (
    draw_building_row,
    draw_moon_disc,
    draw_soft_sky,
    draw_sun_disc,
    draw_wave_band,
)

VIRTUAL_WIDE = 200
VIRTUAL_HIGH = 110


def _burst(pen, cx, cy, radius, paint):
    points = []
    spikes = 12
    for step in range(spikes * 2):
        angle = math.pi * step / spikes
        reach = radius
        if step % 2 == 1:
            reach = radius * 0.45
        points.append((cx + reach * math.cos(angle), cy + reach * math.sin(angle)))
    pen.polygon(points, fill=paint)


def _flag_panel(pen, x0, y0, wide, high, field, cross=None, dots=None):
    pen.rectangle([x0, y0, x0 + wide, y0 + high], fill=field, outline=(60, 56, 48), width=1)
    if cross is not None:
        pen.rectangle([x0, y0 + high // 2 - 3, x0 + wide, y0 + high // 2 + 3], fill=cross)
        pen.rectangle([x0 + wide // 2 - 3, y0, x0 + wide // 2 + 3, y0 + high], fill=cross)
    if dots is not None:
        for angle in range(12):
            rad = math.pi * 2 * angle / 12
            dot_x = x0 + wide // 2 + int((wide // 3) * math.cos(rad))
            dot_y = y0 + high // 2 + int((high // 3) * math.sin(rad))
            pen.ellipse([dot_x - 2, dot_y - 2, dot_x + 2, dot_y + 2], fill=dots)


def scene_kyiv_bridges(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (38, 42, 78), (150, 90, 70))
    draw_moon_disc(pen, x0 + 40, y0 + 26, 13)
    draw_building_row(pen, x0 + 6, y1 - 34, [16, 12, 20, 14, 18], [30, 42, 26, 38, 32], (24, 26, 44))
    river_top = y1 - 34
    pen.rectangle([x0, river_top, x1, y1], fill=(52, 84, 120))
    bridge_y = river_top + 8
    for span in range(3):
        span_x = x0 + 14 + span * 62
        pen.arc([span_x, bridge_y - 14, span_x + 56, bridge_y + 14], 180, 360, fill=(220, 220, 210), width=3)
        pen.line([(span_x, bridge_y + 2), (span_x + 56, bridge_y + 2)], fill=(220, 220, 210), width=2)
    _burst(pen, x0 + 62, bridge_y - 6, 12, (245, 160, 60))
    _burst(pen, x0 + 150, bridge_y - 2, 9, (245, 190, 80))
    pen.ellipse([x0 + 96, y0 + 18, x0 + 128, y0 + 34], fill=(120, 110, 100))


def scene_akvan_spiral(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (120, 150, 170), (200, 205, 190))
    mid_x = x0 + (x1 - x0) * 3 // 4
    mid_y = y0 + (y1 - y0) // 2 - 6
    for ring in range(1, 7):
        radius = ring * 9
        pen.arc(
            [mid_x - radius, mid_y - radius, mid_x + radius, mid_y + radius],
            20 + ring * 40,
            300 + ring * 40,
            fill=(255, 255, 255),
            width=4,
        )
    pen.ellipse([mid_x - 6, mid_y - 6, mid_x + 6, mid_y + 6], fill=(240, 240, 230))
    coast_y = y1 - 26
    pen.polygon([(x0, coast_y + 12), (x0 + 60, coast_y), (x0 + 120, coast_y + 8), (x0, y1), (x1, y1)], fill=(190, 170, 120))
    pen.rectangle([x0 + 14, coast_y - 12, x0 + 34, coast_y], fill=(150, 90, 60))
    pen.polygon([(x0 + 12, coast_y - 12), (x0 + 24, coast_y - 20), (x0 + 36, coast_y - 12)], fill=(120, 60, 40))
    draw_wave_band(pen, x0, y1 - 12, x1, 3, (60, 110, 150))
    for drop in range(10):
        drop_x = x0 + 8 + drop * 18
        pen.line([(drop_x, y0 + 8), (drop_x - 4, y0 + 22)], fill=(230, 235, 240), width=2)


def scene_market_slide(pen, box):
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=(16, 24, 44))
    for grid in range(1, 4):
        grid_y = y0 + (y1 - y0) * grid // 4
        pen.line([(x0, grid_y), (x1, grid_y)], fill=(40, 56, 84), width=1)
    candles = [(18, 30), (26, 44), (34, 58), (46, 72), (58, 86), (70, 100)]
    for index in range(len(candles)):
        top, bottom = candles[index]
        candle_x = x0 + 18 + index * 30
        paint = (200, 60, 50)
        if index == 2:
            paint = (60, 180, 110)
        pen.rectangle([candle_x, y0 + top, candle_x + 12, y0 + bottom], fill=paint)
        pen.line([(candle_x + 6, y0 + top - 6), (candle_x + 6, y0 + bottom + 6)], fill=paint, width=2)
    pen.line([(x0 + 12, y0 + 26), (x1 - 12, y1 - 18)], fill=(240, 90, 70), width=3)
    pen.polygon([(x1 - 26, y1 - 26), (x1 - 10, y1 - 18), (x1 - 26, y1 - 10)], fill=(240, 90, 70))


def scene_reset_table(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (210, 220, 230), (170, 180, 190))
    _flag_panel(pen, x0 + 14, y0 + 14, 62, 40, (30, 60, 120), cross=(200, 200, 200))
    _flag_panel(pen, x1 - 76, y0 + 14, 62, 40, (20, 40, 110), dots=(240, 220, 60))
    table_y = y0 + 74
    pen.rectangle([x0 + 8, table_y, x1 - 8, table_y + 6], fill=(120, 80, 40))
    pen.rectangle([x0 + 22, y0 + 66, x0 + 78, table_y], fill=(245, 240, 225), outline=(90, 84, 70), width=1)
    pen.rectangle([x1 - 78, y0 + 66, x1 - 22, table_y], fill=(245, 240, 225), outline=(90, 84, 70), width=1)
    pen.line([(x0 + 30, y0 + 70), (x0 + 70, y0 + 70)], fill=(150, 140, 120), width=1)
    pen.line([(x1 - 70, y0 + 70), (x1 - 30, y0 + 70)], fill=(150, 140, 120), width=1)


def scene_cop31_hall(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (70, 130, 110), (200, 220, 200))
    draw_sun_disc(pen, x0 + 34, y0 + 24, 16, (240, 200, 90))
    pen.rectangle([x0 + 60, y0 + 40, x1 - 14, y0 + 52], fill=(60, 90, 90))
    pen.rectangle([x0 + 66, y0 + 52, x1 - 20, y0 + 58], fill=(90, 120, 110))
    for row in range(3):
        for seat in range(9):
            seat_x = x0 + 18 + seat * 19
            seat_y = y0 + 68 + row * 16
            head = (200, 90, 70)
            if (row + seat) % 3 == 1:
                head = (70, 110, 170)
            if (row + seat) % 3 == 2:
                head = (90, 140, 90)
            pen.ellipse([seat_x, seat_y, seat_x + 9, seat_y + 9], fill=head)
            pen.rectangle([seat_x - 1, seat_y + 10, seat_x + 10, seat_y + 14], fill=(60, 60, 60))


def scene_hormuz_tanker(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (240, 200, 130), (220, 150, 90))
    draw_sun_disc(pen, x1 - 36, y0 + 26, 15, (250, 210, 100))
    sea_y = y1 - 30
    pen.rectangle([x0, sea_y, x1, y1], fill=(40, 90, 130))
    hull_x = x0 + 22
    pen.polygon(
        [(hull_x, sea_y - 16), (hull_x + 120, sea_y - 16), (hull_x + 110, sea_y + 8), (hull_x + 10, sea_y + 8)],
        fill=(140, 40, 30),
    )
    pen.rectangle([hull_x + 84, sea_y - 30, hull_x + 104, sea_y - 16], fill=(230, 230, 220))
    pen.rectangle([hull_x + 12, sea_y - 30, hull_x + 34, sea_y - 16], fill=(60, 120, 90))
    pen.rectangle([hull_x + 38, sea_y - 30, hull_x + 60, sea_y - 16], fill=(200, 160, 60))
    pen.rectangle([hull_x + 64, sea_y - 30, hull_x + 80, sea_y - 16], fill=(90, 90, 160))
    draw_wave_band(pen, x0, sea_y + 10, x1, 3, (70, 130, 170))
    pen.line([(x0 + 8, y0 + 40), (x0 + 8, sea_y - 6)], fill=(60, 60, 60), width=3)
    pen.line([(x0 + 2, y0 + 44), (x0 + 16, y0 + 52)], fill=(60, 60, 60), width=2)


def scene_senate_dome(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (200, 215, 230), (230, 225, 205))
    mid_x = (x0 + x1) // 2
    pen.pieslice([mid_x - 34, y0 + 8, mid_x + 34, y0 + 76], 180, 360, fill=(240, 240, 230), outline=(90, 84, 70), width=1)
    pen.rectangle([mid_x - 3, y0 + 2, mid_x + 3, y0 + 10], fill=(200, 170, 90))
    pen.rectangle([x0 + 18, y0 + 44, x1 - 18, y0 + 50], fill=(235, 235, 220), outline=(90, 84, 70), width=1)
    for column in range(6):
        col_x = x0 + 26 + column * 26
        pen.rectangle([col_x, y0 + 50, col_x + 10, y0 + 78], fill=(245, 245, 235), outline=(90, 84, 70), width=1)
    bar_y = y1 - 18
    pen.rectangle([x0 + 12, bar_y, x0 + 84, bar_y + 10], fill=(60, 110, 170))
    pen.rectangle([x0 + 88, bar_y, x0 + 178, bar_y + 10], fill=(180, 60, 50))
    pen.rectangle([x0 + 12, bar_y - 4, x0 + 12, bar_y + 14], fill=(40, 40, 40))


def scene_jakarta_beijing(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (250, 210, 140), (200, 160, 120))
    draw_sun_disc(pen, (x0 + x1) // 2, y0 + 30, 18, (250, 200, 90))
    draw_building_row(pen, x0 + 8, y1 - 8, [18, 14, 22, 12], [40, 56, 34, 48], (90, 60, 60))
    draw_building_row(pen, x0 + 104, y1 - 8, [16, 20, 14, 18], [52, 36, 60, 42], (60, 70, 100))
    pen.rectangle([x0 + 40, y0 + 16, x0 + 62, y0 + 44], fill=(200, 40, 40))
    pen.rectangle([x1 - 62, y0 + 16, x1 - 40, y0 + 44], fill=(200, 40, 40))
    pen.ellipse([x0 + 46, y0 + 22, x0 + 56, y0 + 32], fill=(250, 220, 80))
    pen.ellipse([x1 - 56, y0 + 22, x1 - 46, y0 + 32], fill=(250, 220, 80))


def scene_hague_court(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (215, 220, 225), (190, 185, 170))
    mid_x = (x0 + x1) // 2
    pen.polygon([(mid_x - 56, y0 + 34), (mid_x, y0 + 10), (mid_x + 56, y0 + 34)], fill=(200, 195, 180), outline=(90, 84, 70))
    for column in range(5):
        col_x = x0 + 30 + column * 28
        pen.rectangle([col_x, y0 + 36, col_x + 12, y0 + 78], fill=(245, 242, 230), outline=(90, 84, 70), width=1)
    pen.rectangle([x0 + 22, y0 + 78, x1 - 22, y0 + 84], fill=(200, 195, 180))
    scale_x = mid_x
    pen.line([(scale_x, y0 + 44), (scale_x, y0 + 62)], fill=(120, 90, 40), width=2)
    pen.line([(scale_x - 16, y0 + 48), (scale_x + 16, y0 + 48)], fill=(120, 90, 40), width=2)
    pen.polygon([(scale_x - 22, y0 + 52), (scale_x - 10, y0 + 52), (scale_x - 16, y0 + 62)], fill=(180, 140, 60))
    pen.polygon([(scale_x + 10, y0 + 52), (scale_x + 22, y0 + 52), (scale_x + 16, y0 + 62)], fill=(180, 140, 60))


def scene_gaza_line(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (230, 215, 180), (190, 170, 130))
    ground_y = y1 - 24
    pen.rectangle([x0, ground_y, x1, y1], fill=(200, 180, 130))
    pen.polygon([(x0 + 16, ground_y - 18), (x0 + 44, ground_y - 18), (x0 + 30, ground_y - 34)], fill=(220, 210, 180))
    pen.polygon([(x0 + 60, ground_y - 14), (x0 + 92, ground_y - 14), (x0 + 76, ground_y - 30)], fill=(210, 200, 170))
    pen.line([(x0, y0 + 40), (x1, y0 + 40)], fill=(90, 80, 60), width=2)
    for post in range(8):
        post_x = x0 + 8 + post * 24
        pen.line([(post_x, y0 + 30), (post_x, y0 + 52)], fill=(90, 80, 60), width=2)
    pen.ellipse([x1 - 52, y0 + 12, x1 - 28, y0 + 28], fill=(150, 140, 130))
    pen.ellipse([x1 - 44, y0 + 20, x1 - 20, y0 + 36], fill=(170, 160, 148))


def scene_cricket_pitch(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (140, 190, 220), (200, 225, 200))
    pen.rectangle([x0, y1 - 34, x1, y1], fill=(90, 150, 80))
    pen.rectangle([x0 + 30, y1 - 44, x1 - 30, y1 - 20], fill=(210, 190, 140))
    for stump in range(3):
        stump_x = x0 + 40 + stump * 8
        pen.rectangle([stump_x, y0 + 22, stump_x + 4, y0 + 44], fill=(220, 180, 90))
    pen.rectangle([x0 + 40, y0 + 19, x0 + 60, y0 + 22], fill=(200, 160, 70))
    pen.line([(x1 - 70, y0 + 60), (x1 - 40, y0 + 30)], fill=(180, 130, 70), width=6)
    pen.ellipse([x1 - 84, y0 + 62, x1 - 74, y0 + 72], fill=(190, 50, 40))
    pen.arc([x0 + 60, y0 + 8, x0 + 150, y0 + 90], 300, 60, fill=(255, 255, 255), width=2)


def scene_gta_city(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (250, 140, 90), (120, 60, 120))
    draw_sun_disc(pen, (x0 + x1) // 2, y0 + 34, 20, (255, 220, 120))
    draw_building_row(pen, x0 + 6, y1 - 10, [18, 14, 24, 16, 20], [46, 62, 38, 56, 48], (40, 30, 60))
    pen.rectangle([x0, y1 - 10, x1, y1], fill=(50, 45, 60))
    pen.line([(x0, y1 - 5), (x1, y1 - 5)], fill=(240, 200, 60), width=1)
    for palm in range(2):
        palm_x = x0 + 24 + palm * 120
        pen.line([(palm_x, y1 - 34), (palm_x, y1 - 12)], fill=(30, 50, 30), width=3)
        pen.arc([palm_x - 14, y1 - 44, palm_x + 14, y1 - 28], 180, 360, fill=(40, 90, 50), width=3)


def scene_tokyo_yen(pen, box):
    x0, y0, x1, y1 = box
    draw_soft_sky(pen, box, (200, 220, 235), (235, 230, 210))
    draw_building_row(pen, x0 + 8, y1 - 8, [20, 16, 24, 18], [36, 52, 30, 44], (90, 100, 120))
    points = [(x0 + 14, y1 - 30), (x0 + 56, y1 - 44), (x0 + 98, y1 - 36), (x0 + 140, y1 - 58), (x1 - 14, y1 - 70)]
    pen.line(points, fill=(180, 50, 40), width=3, joint="curve")
    pen.polygon([(x1 - 30, y1 - 78), (x1 - 10, y1 - 70), (x1 - 30, y1 - 62)], fill=(180, 50, 40))
    for coin in range(3):
        coin_x = x0 + 30 + coin * 34
        pen.ellipse([coin_x, y1 - 26, coin_x + 18, y1 - 8], fill=(220, 180, 80), outline=(160, 120, 40), width=1)


SCENE_PAINTERS = {
    "kyiv_bridges": scene_kyiv_bridges,
    "akvan_spiral": scene_akvan_spiral,
    "market_slide": scene_market_slide,
    "reset_table": scene_reset_table,
    "cop31_hall": scene_cop31_hall,
    "hormuz_tanker": scene_hormuz_tanker,
    "senate_dome": scene_senate_dome,
    "jakarta_beijing": scene_jakarta_beijing,
    "hague_court": scene_hague_court,
    "gaza_line": scene_gaza_line,
    "cricket_pitch": scene_cricket_pitch,
    "gta_city": scene_gta_city,
    "tokyo_yen": scene_tokyo_yen,
}


def paint_scene(page, scene_key, box):
    painter = SCENE_PAINTERS.get(scene_key)
    known = painter is not None
    if known:
        canvas = Image.new("RGB", (VIRTUAL_WIDE, VIRTUAL_HIGH), (255, 255, 255))
        canvas_pen = ImageDraw.Draw(canvas)
        painter(canvas_pen, (0, 0, VIRTUAL_WIDE, VIRTUAL_HIGH))
        target_wide = box[2] - box[0]
        target_high = box[3] - box[1]
        scaled = canvas.resize((target_wide, target_high), Image.LANCZOS)
        page.paste(scaled, (box[0], box[1]))
    if known is False:
        canvas = Image.new("RGB", (VIRTUAL_WIDE, VIRTUAL_HIGH), (200, 210, 225))
        canvas_pen = ImageDraw.Draw(canvas)
        draw_soft_sky(canvas_pen, (0, 0, VIRTUAL_WIDE, VIRTUAL_HIGH), (200, 210, 225), (230, 225, 205))
        draw_building_row(canvas_pen, 8, VIRTUAL_HIGH - 8, [18, 14, 20, 16], [34, 48, 30, 42], (90, 90, 100))
        target_wide = box[2] - box[0]
        target_high = box[3] - box[1]
        scaled = canvas.resize((target_wide, target_high), Image.LANCZOS)
        page.paste(scaled, (box[0], box[1]))
