"""Flat-illustration scenes for the thirteen story cards.

Each scene is drawn fresh on its own canvas at the size the layout
asks for, using simple shapes: skies, seas, skylines, vehicles,
figures and symbols. No photographs, no external assets, and no
text inside any scene: every label lives in the card below it, so
nothing inside a picture can garble or overlap.
"""

import math
import random

from PIL import Image, ImageDraw


def blank_scene(width, height, sky_top, sky_bottom):
    scene_img = Image.new("RGB", (width, height), sky_top)
    scene_draw = ImageDraw.Draw(scene_img)
    band_index = 0
    band_count = 24
    while band_index < band_count:
        frac = band_index / band_count
        mix_r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * frac)
        mix_g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * frac)
        mix_b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * frac)
        band_y0 = int(height * band_index / band_count)
        band_y1 = int(height * (band_index + 1) / band_count) + 1
        scene_draw.rectangle((0, band_y0, width, band_y1), fill=(mix_r, mix_g, mix_b))
        band_index = band_index + 1
    return scene_img, scene_draw


def draw_sun(scene_draw, cx, cy, radius, fill):
    sun_box = (cx - radius, cy - radius, cx + radius, cy + radius)
    scene_draw.ellipse(sun_box, fill=fill)
    return sun_box


def draw_cloud(scene_draw, cx, cy, scale, fill):
    puff_offsets = [(-1.6, 0.2), (-0.7, -0.3), (0.3, -0.45), (1.2, -0.1), (1.9, 0.25)]
    for puff_dx, puff_dy in puff_offsets:
        puff_r = scale * (0.62 - abs(puff_dy) * 0.3)
        puff_box = (cx + puff_dx * scale - puff_r, cy + puff_dy * scale - puff_r,
                    cx + puff_dx * scale + puff_r, cy + puff_dy * scale + puff_r)
        scene_draw.ellipse(puff_box, fill=fill)
    return scale


def draw_rain(scene_draw, width, height, seed, count, color):
    rain_rng = random.Random(seed)
    drop_index = 0
    while drop_index < count:
        drop_x = rain_rng.randint(0, width)
        drop_y = rain_rng.randint(0, height)
        drop_len = rain_rng.randint(10, 26)
        scene_draw.line((drop_x, drop_y, drop_x - 5, drop_y + drop_len), fill=color, width=2)
        drop_index = drop_index + 1
    return count


def draw_palm(scene_draw, base_x, base_y, palm_h, trunk_fill, frond_fill):
    scene_draw.line((base_x, base_y, base_x + 14, base_y - palm_h), fill=trunk_fill, width=5)
    frond_angle = 0
    while frond_angle < 6:
        frond_rad = math.radians(150 + frond_angle * 26)
        frond_x2 = base_x + 14 + int(math.cos(frond_rad) * 26)
        frond_y2 = base_y - palm_h + int(math.sin(frond_rad) * 15) + 8
        scene_draw.line((base_x + 14, base_y - palm_h, frond_x2, frond_y2), fill=frond_fill, width=4)
        frond_angle = frond_angle + 1
    return palm_h


def scene_kyiv(width, height):
    img, dr = blank_scene(width, height, (58, 56, 88), (196, 128, 92))
    river_y = int(height * 0.74)
    dr.rectangle((0, river_y, width, height), fill=(64, 84, 110))
    skyline_rng = random.Random(7)
    tower_x = 6
    while tower_x < width - 20:
        tower_w = skyline_rng.randint(18, 34)
        tower_h = skyline_rng.randint(28, 74)
        tower_top = river_y - tower_h
        dr.rectangle((tower_x, tower_top, tower_x + tower_w, river_y), fill=(52, 50, 66))
        win_y = tower_top + 5
        while win_y < river_y - 6:
            win_x = tower_x + 4
            while win_x < tower_x + tower_w - 5:
                lit_roll = skyline_rng.random()
                if lit_roll > 0.45:
                    dr.rectangle((win_x, win_y, win_x + 3, win_y + 4), fill=(250, 205, 120))
                win_x = win_x + 8
            win_y = win_y + 9
        tower_x = tower_x + tower_w + skyline_rng.randint(2, 8)
    deck_y = int(height * 0.60)
    span_edges = [(0.02, 0.335), (0.355, 0.66), (0.68, 0.985)]
    span_index = 0
    for span_fx0, span_fx1 in span_edges:
        span_x0 = int(width * span_fx0)
        span_x1 = int(width * span_fx1)
        dr.line((span_x0, deck_y, span_x1, deck_y), fill=(30, 30, 38), width=7)
        dr.arc((span_x0, deck_y - 34, span_x1, deck_y + 30), 180, 360, fill=(30, 30, 38), width=4)
        pylon_x = (span_x0 + span_x1) // 2
        dr.line((pylon_x, deck_y - 44, pylon_x, deck_y), fill=(30, 30, 38), width=5)
        span_broken = span_index == 1
        if span_broken:
            gap_x0 = pylon_x + 8
            gap_x1 = pylon_x + int(width * 0.09)
            dr.line((gap_x0, deck_y, gap_x1, deck_y + 12), fill=(196, 128, 92), width=8)
            dr.line((gap_x1, deck_y + 12, gap_x1 + 14, deck_y + 26), fill=(30, 30, 38), width=5)
            burst_cx = pylon_x + int(width * 0.05)
            burst_cy = deck_y - 6
            dr.ellipse((burst_cx - 16, burst_cy - 16, burst_cx + 16, burst_cy + 16), fill=(250, 180, 80))
            dr.ellipse((burst_cx - 8, burst_cy - 8, burst_cx + 8, burst_cy + 8), fill=(255, 230, 150))
        span_index = span_index + 1
    smoke_cx = int(width * 0.52)
    smoke_cy = int(height * 0.30)
    smoke_puff = 0
    while smoke_puff < 6:
        smoke_r = 12 + smoke_puff * 6
        smoke_x = smoke_cx + smoke_puff * 16
        smoke_y = smoke_cy - smoke_puff * 12
        smoke_box = (smoke_x - smoke_r, smoke_y - smoke_r, smoke_x + smoke_r, smoke_y + smoke_r)
        dr.ellipse(smoke_box, fill=(88, 84, 96))
        smoke_puff = smoke_puff + 1
    trail_specs = [(0.10, 0.06, 0.30, 0.42), (0.88, 0.04, 0.60, 0.40), (0.70, 0.02, 0.50, 0.38)]
    for trail_fx0, trail_fy0, trail_fx1, trail_fy1 in trail_specs:
        trail_pts = []
        trail_step = 0
        while trail_step <= 12:
            trail_t = trail_step / 12
            trail_x = width * (trail_fx0 + (trail_fx1 - trail_fx0) * trail_t)
            trail_y = height * (trail_fy0 + (trail_fy1 - trail_fy0) * trail_t) + math.sin(trail_t * 3.0) * 6
            trail_pts.append((trail_x, trail_y))
            trail_step = trail_step + 1
        dr.line(trail_pts, fill=(255, 226, 170), width=3)
        head_x, head_y = trail_pts[-1]
        dr.ellipse((head_x - 5, head_y - 5, head_x + 5, head_y + 5), fill=(255, 240, 200))
    return img


def scene_akvan(width, height):
    img, dr = blank_scene(width, height, (96, 116, 138), (168, 188, 198))
    land_pts = [(0, 0), (int(width * 0.34), 0), (int(width * 0.30), int(height * 0.55)),
                (int(width * 0.22), int(height * 0.72)), (0, int(height * 0.66))]
    dr.polygon(land_pts, fill=(196, 186, 148))
    sea_y = int(height * 0.66)
    dr.rectangle((int(width * 0.22), sea_y, width, height), fill=(52, 96, 118))
    wave_row = 0
    while wave_row < 4:
        wave_y = sea_y + 8 + wave_row * int(height * 0.075)
        wave_x = int(width * 0.30) + wave_row * 13
        while wave_x < width:
            dr.arc((wave_x, wave_y, wave_x + 44, wave_y + 16), 180, 360, fill=(210, 232, 238), width=3)
            wave_x = wave_x + 52
        wave_row = wave_row + 1
    swirl_cx = int(width * 0.70)
    swirl_cy = int(height * 0.34)
    swirl_turn = 0
    while swirl_turn < 5:
        swirl_r = 16 + swirl_turn * 17
        swirl_box = (swirl_cx - swirl_r, swirl_cy - swirl_r * 0.8, swirl_cx + swirl_r, swirl_cy + swirl_r * 0.8)
        dr.arc(swirl_box, 300 + swirl_turn * 24, 300 + swirl_turn * 24 + 235, fill=(238, 244, 246), width=6)
        swirl_turn = swirl_turn + 1
    draw_sun(dr, swirl_cx, swirl_cy, 9, (250, 250, 246))
    house_specs = [(0.04, 0.50, 54, 34), (0.16, 0.55, 44, 28)]
    for house_fx, house_fy, house_w, house_h in house_specs:
        house_x = int(width * house_fx)
        house_y = int(height * house_fy)
        dr.rectangle((house_x, house_y, house_x + house_w, house_y + house_h), fill=(214, 196, 158))
        roof_pts = [(house_x - 6, house_y), (house_x + house_w // 2, house_y - 16), (house_x + house_w + 6, house_y)]
        dr.polygon(roof_pts, fill=(146, 74, 52))
    draw_palm(dr, int(width * 0.10), int(height * 0.62), 40, (84, 66, 44), (62, 110, 62))
    draw_palm(dr, int(width * 0.20), int(height * 0.64), 34, (84, 66, 44), (62, 110, 62))
    draw_rain(dr, width, height, 41, 130, (226, 238, 242))
    return img


def scene_selloff(width, height):
    img = Image.new("RGB", (width, height), (24, 30, 46))
    dr = ImageDraw.Draw(img)
    grid_x = int(width * 0.08)
    while grid_x < width:
        dr.line((grid_x, 0, grid_x, height), fill=(44, 54, 76), width=1)
        grid_x = grid_x + int(width * 0.115)
    grid_y = int(height * 0.10)
    while grid_y < height:
        dr.line((0, grid_y, width, grid_y), fill=(44, 54, 76), width=1)
        grid_y = grid_y + int(height * 0.16)
    chart_rng = random.Random(11)
    candle_x = int(width * 0.07)
    candle_index = 0
    while candle_index < 9:
        candle_h = chart_rng.randint(16, 40)
        candle_down = int(height * 0.16) + candle_index * int(height * 0.062)
        candle_fill = (216, 64, 56)
        candle_is_up = candle_index == 4
        if candle_is_up:
            candle_fill = (72, 178, 110)
            candle_down = candle_down - 14
        dr.rectangle((candle_x, candle_down, candle_x + 15, candle_down + candle_h), fill=candle_fill)
        dr.line((candle_x + 7, candle_down - 6, candle_x + 7, candle_down + candle_h + 6), fill=candle_fill, width=2)
        candle_x = candle_x + int(width * 0.052)
        candle_index = candle_index + 1
    trend_pts = [(int(width * 0.05), int(height * 0.18)), (int(width * 0.30), int(height * 0.34)),
                 (int(width * 0.48), int(height * 0.30)), (int(width * 0.70), int(height * 0.58)),
                 (int(width * 0.95), int(height * 0.82))]
    dr.line(trend_pts, fill=(240, 92, 76), width=5)
    arrow_tip = trend_pts[-1]
    dr.polygon([(arrow_tip[0], arrow_tip[1]), (arrow_tip[0] - 22, arrow_tip[1] - 4), (arrow_tip[0] - 6, arrow_tip[1] - 20)], fill=(240, 92, 76))
    return img


def scene_ukeu(width, height):
    img, dr = blank_scene(width, height, (214, 222, 232), (238, 234, 226))
    flag_w = int(width * 0.40)
    flag_h = int(height * 0.52)
    flag_y = int(height * 0.22)
    uk_x = int(width * 0.05)
    dr.rectangle((uk_x, flag_y, uk_x + flag_w, flag_y + flag_h), fill=(28, 48, 110))
    dr.rectangle((uk_x, flag_y + flag_h // 2 - 8, uk_x + flag_w, flag_y + flag_h // 2 + 8), fill=(246, 246, 244))
    dr.rectangle((uk_x + flag_w // 2 - 8, flag_y, uk_x + flag_w // 2 + 8, flag_y + flag_h), fill=(246, 246, 244))
    dr.rectangle((uk_x, flag_y + flag_h // 2 - 4, uk_x + flag_w, flag_y + flag_h // 2 + 4), fill=(196, 44, 40))
    dr.rectangle((uk_x + flag_w // 2 - 4, flag_y, uk_x + flag_w // 2 + 4, flag_y + flag_h), fill=(196, 44, 40))
    eu_x = int(width * 0.55)
    dr.rectangle((eu_x, flag_y, eu_x + flag_w, flag_y + flag_h), fill=(28, 48, 110))
    star_index = 0
    while star_index < 12:
        star_rad = math.radians(star_index * 30 - 90)
        star_cx = eu_x + flag_w // 2 + int(math.cos(star_rad) * flag_h * 0.32)
        star_cy = flag_y + flag_h // 2 + int(math.sin(star_rad) * flag_h * 0.32)
        dr.ellipse((star_cx - 4, star_cy - 4, star_cx + 4, star_cy + 4), fill=(250, 214, 90))
        star_index = star_index + 1
    arc_box = (int(width * 0.08), int(height * 0.02), int(width * 0.92), int(height * 0.98))
    dr.arc(arc_box, 200, 340, fill=(196, 150, 52), width=5)
    desk_y = int(height * 0.86)
    dr.rectangle((0, desk_y, width, height), fill=(120, 110, 96))
    return img


def scene_cop31(width, height):
    img, dr = blank_scene(width, height, (226, 216, 188), (206, 190, 158))
    globe_cx = int(width * 0.50)
    globe_cy = int(height * 0.40)
    globe_r = int(height * 0.30)
    dr.ellipse((globe_cx - globe_r, globe_cy - globe_r, globe_cx + globe_r, globe_cy + globe_r), fill=(96, 138, 168))
    blob_specs = [(-0.45, -0.30, 0.30), (0.10, -0.42, 0.24), (0.42, 0.05, 0.28), (-0.15, 0.28, 0.34), (0.30, 0.48, 0.18)]
    for blob_dx, blob_dy, blob_frac in blob_specs:
        blob_r = int(globe_r * blob_frac)
        blob_cx = globe_cx + int(globe_r * blob_dx)
        blob_cy = globe_cy + int(globe_r * blob_dy)
        dr.ellipse((blob_cx - blob_r, blob_cy - blob_r * 0.7, blob_cx + blob_r, blob_cy + blob_r * 0.7), fill=(96, 148, 92))
    doc_x0 = int(width * 0.06)
    doc_y0 = int(height * 0.14)
    doc_x1 = int(width * 0.34)
    doc_y1 = int(height * 0.62)
    dr.rectangle((doc_x0, doc_y0, doc_x1, doc_y1), fill=(250, 247, 238), outline=(120, 110, 90), width=2)
    doc_line_y = doc_y0 + 14
    doc_line = 0
    while doc_line < 5:
        line_w = (doc_x1 - doc_x0) - 24 - (doc_line % 2) * 26
        dr.rectangle((doc_x0 + 12, doc_line_y, doc_x0 + 12 + line_w, doc_line_y + 5), fill=(150, 144, 128))
        doc_line_y = doc_line_y + 15
        doc_line = doc_line + 1
    strike_y = doc_line_y + int(height * 0.055)
    dr.line((doc_x0 + 8, strike_y, doc_x1 - 8, strike_y - 6), fill=(196, 52, 40), width=5)
    desk_y = int(height * 0.80)
    dr.rectangle((0, desk_y, width, height), fill=(122, 92, 62))
    delegate_fx = [0.16, 0.34, 0.52, 0.70, 0.88]
    for seat_fx in delegate_fx:
        seat_x = int(width * seat_fx)
        head_box = (seat_x - 11, desk_y - 52, seat_x + 11, desk_y - 30)
        dr.ellipse(head_box, fill=(216, 172, 138))
        dr.pieslice((seat_x - 20, desk_y - 34, seat_x + 20, desk_y + 8), 180, 360, fill=(70, 84, 110))
        dr.rectangle((seat_x - 26, desk_y - 6, seat_x + 26, desk_y + 8), fill=(250, 247, 238), outline=(120, 110, 90))
    thermo_x = int(width * 0.90)
    thermo_top = int(height * 0.12)
    thermo_bot = int(height * 0.55)
    dr.rectangle((thermo_x - 6, thermo_top, thermo_x + 6, thermo_bot), fill=(250, 247, 238), outline=(120, 110, 90), width=2)
    dr.rectangle((thermo_x - 4, int(height * 0.30), thermo_x + 4, thermo_bot), fill=(214, 84, 52))
    dr.ellipse((thermo_x - 13, thermo_bot - 4, thermo_x + 13, thermo_bot + 22), fill=(214, 84, 52))
    return img


def scene_hormuz(width, height):
    img, dr = blank_scene(width, height, (240, 205, 150), (250, 228, 178))
    sea_y = int(height * 0.52)
    dr.rectangle((0, sea_y, width, height), fill=(58, 108, 128))
    draw_sun(dr, int(width * 0.82), int(height * 0.20), int(height * 0.11), (250, 214, 130))
    cliff_left = [(0, sea_y), (0, int(height * 0.30)), (int(width * 0.16), int(height * 0.38)), (int(width * 0.20), sea_y)]
    cliff_right = [(width, sea_y), (width, int(height * 0.26)), (int(width * 0.84), int(height * 0.36)), (int(width * 0.80), sea_y)]
    dr.polygon(cliff_left, fill=(168, 128, 88))
    dr.polygon(cliff_right, fill=(158, 118, 80))
    ship_cx = int(width * 0.50)
    ship_y = int(height * 0.60)
    hull_pts = [(ship_cx - 110, ship_y), (ship_cx + 110, ship_y), (ship_cx + 88, ship_y + 22), (ship_cx - 88, ship_y + 22)]
    dr.polygon(hull_pts, fill=(52, 56, 64))
    dr.rectangle((ship_cx - 104, ship_y - 12, ship_cx + 104, ship_y), fill=(196, 70, 52))
    container_colors = [(64, 110, 160), (216, 150, 60), (84, 140, 96), (160, 84, 120)]
    container_i = 0
    while container_i < 8:
        cont_x = ship_cx - 96 + (container_i % 4) * 48
        cont_y = ship_y - 12 - (container_i // 4 + 1) * 15
        dr.rectangle((cont_x, cont_y, cont_x + 44, cont_y + 13), fill=container_colors[container_i % 4])
        container_i = container_i + 1
    dr.rectangle((ship_cx + 62, ship_y - 58, ship_cx + 88, ship_y - 12), fill=(228, 224, 214))
    dr.rectangle((ship_cx + 68, ship_y - 50, ship_cx + 82, ship_y - 42), fill=(90, 130, 160))
    mine_specs = [(0.30, 0.80), (0.68, 0.86), (0.44, 0.92)]
    for mine_fx, mine_fy in mine_specs:
        mine_x = int(width * mine_fx)
        mine_y = int(height * mine_fy)
        dr.ellipse((mine_x - 10, mine_y - 10, mine_x + 10, mine_y + 10), fill=(40, 44, 52))
        spike_angle = 0
        while spike_angle < 8:
            spike_rad = math.radians(spike_angle * 45)
            spike_x2 = mine_x + int(math.cos(spike_rad) * 16)
            spike_y2 = mine_y + int(math.sin(spike_rad) * 16)
            dr.line((mine_x, mine_y, spike_x2, spike_y2), fill=(40, 44, 52), width=3)
            spike_angle = spike_angle + 1
    route_pts = [(int(width * 0.24), int(height * 0.97)), (int(width * 0.42), int(height * 0.72)), (int(width * 0.60), int(height * 0.97))]
    dr.line(route_pts, fill=(240, 240, 230), width=2)
    return img


def scene_senate(width, height):
    img, dr = blank_scene(width, height, (206, 216, 228), (232, 234, 236))
    ground_y = int(height * 0.86)
    dr.rectangle((0, ground_y, width, height), fill=(148, 152, 148))
    capitol_cx = int(width * 0.30)
    base_w = int(width * 0.42)
    base_x0 = capitol_cx - base_w // 2
    base_y = int(height * 0.52)
    dr.rectangle((base_x0, base_y, base_x0 + base_w, ground_y), fill=(238, 236, 230))
    col_x = base_x0 + 12
    while col_x < base_x0 + base_w - 10:
        dr.rectangle((col_x, base_y + 10, col_x + 7, ground_y - 8), fill=(206, 202, 192))
        col_x = col_x + 20
    dr.rectangle((base_x0 - 8, base_y - 8, base_x0 + base_w + 8, base_y), fill=(220, 216, 206))
    dome_box = (capitol_cx - int(base_w * 0.30), base_y - int(height * 0.30), capitol_cx + int(base_w * 0.30), base_y + 6)
    dr.pieslice(dome_box, 180, 360, fill=(120, 138, 152))
    dr.rectangle((capitol_cx - 3, base_y - int(height * 0.36), capitol_cx + 3, base_y - int(height * 0.28)), fill=(90, 104, 118))
    dr.polygon([(capitol_cx, base_y - int(height * 0.42)), (capitol_cx - 6, base_y - int(height * 0.35)), (capitol_cx + 6, base_y - int(height * 0.35))], fill=(196, 60, 48))
    panel_x0 = int(width * 0.56)
    panel_y0 = int(height * 0.16)
    panel_x1 = int(width * 0.97)
    panel_y1 = int(height * 0.66)
    dr.rectangle((panel_x0, panel_y0, panel_x1, panel_y1), fill=(34, 44, 66))
    bar_y = panel_y1 - int(height * 0.20)
    dr.rectangle((panel_x0 + 20, bar_y, panel_x0 + 20 + int((panel_x1 - panel_x0 - 40) * 0.485), bar_y + 10), fill=(96, 150, 220))
    dr.rectangle((panel_x0 + 20 + int((panel_x1 - panel_x0 - 40) * 0.485), bar_y, panel_x1 - 20, bar_y + 10), fill=(220, 96, 84))
    bar2_y = bar_y + 18
    dr.rectangle((panel_x0 + 20, bar2_y, panel_x1 - 20, bar2_y + 4), fill=(120, 132, 156))
    return img


def scene_jakarta(width, height):
    img, dr = blank_scene(width, height, (214, 224, 214), (236, 230, 206))
    wall_panel = (int(width * 0.06), int(height * 0.10), int(width * 0.94), int(height * 0.58))
    dr.rectangle(wall_panel, fill=(168, 196, 198), outline=(110, 130, 128), width=2)
    island_specs = [(0.24, 0.30, 26), (0.38, 0.36, 18), (0.55, 0.26, 22), (0.70, 0.38, 15), (0.30, 0.46, 12)]
    for island_fx, island_fy, island_r in island_specs:
        island_x = int(width * island_fx)
        island_y = int(height * island_fy)
        dr.ellipse((island_x - island_r, island_y - island_r // 2, island_x + island_r, island_y + island_r // 2), fill=(110, 152, 104))
    table_y = int(height * 0.80)
    dr.rectangle((int(width * 0.16), table_y, int(width * 0.84), table_y + 14), fill=(110, 78, 52))
    figure_specs = [(0.34, (178, 52, 44)), (0.66, (206, 44, 40))]
    for figure_fx, figure_fill in figure_specs:
        figure_x = int(width * figure_fx)
        head_box = (figure_x - 13, table_y - 62, figure_x + 13, table_y - 36)
        dr.ellipse(head_box, fill=(216, 172, 138))
        dr.pieslice((figure_x - 24, table_y - 42, figure_x + 24, table_y + 6), 180, 360, fill=figure_fill)
    flag_left_x = int(width * 0.10)
    flag_right_x = int(width * 0.82)
    flag_top = int(height * 0.08)
    dr.rectangle((flag_left_x, flag_top, flag_left_x + 52, flag_top + 17), fill=(206, 44, 40))
    dr.rectangle((flag_left_x, flag_top + 17, flag_left_x + 52, flag_top + 34), fill=(246, 246, 244))
    dr.rectangle((flag_right_x, flag_top, flag_right_x + 52, flag_top + 34), fill=(206, 44, 40))
    dr.ellipse((flag_right_x + 6, flag_top + 5, flag_right_x + 14, flag_top + 13), fill=(250, 214, 90))
    dr.ellipse((flag_right_x + 18, flag_top + 4, flag_right_x + 23, flag_top + 9), fill=(250, 214, 90))
    dr.ellipse((flag_right_x + 19, flag_top + 12, flag_right_x + 24, flag_top + 17), fill=(250, 214, 90))
    paper_y = table_y - 8
    dr.rectangle((int(width * 0.44), paper_y, int(width * 0.56), paper_y + 8), fill=(250, 248, 240), outline=(130, 120, 100))
    return img


def scene_hague(width, height):
    img, dr = blank_scene(width, height, (206, 214, 224), (234, 232, 224))
    ground_y = int(height * 0.88)
    dr.rectangle((0, ground_y, width, height), fill=(150, 148, 138))
    hall_cx = int(width * 0.36)
    hall_w = int(width * 0.52)
    hall_x0 = hall_cx - hall_w // 2
    hall_top = int(height * 0.30)
    dr.rectangle((hall_x0, hall_top + 18, hall_x0 + hall_w, ground_y), fill=(240, 237, 228))
    pediment_pts = [(hall_x0 - 10, hall_top + 18), (hall_cx, hall_top - 16), (hall_x0 + hall_w + 10, hall_top + 18)]
    dr.polygon(pediment_pts, fill=(206, 200, 186))
    dr.ellipse((hall_cx - 9, hall_top - 2, hall_cx + 9, hall_top + 16), outline=(120, 114, 100), width=3)
    col_x = hall_x0 + 14
    while col_x < hall_x0 + hall_w - 12:
        dr.rectangle((col_x, hall_top + 26, col_x + 9, ground_y - 10), fill=(214, 208, 194))
        col_x = col_x + 30
    dr.rectangle((hall_x0 - 6, ground_y - 10, hall_x0 + hall_w + 6, ground_y), fill=(196, 190, 174))
    scales_cx = int(width * 0.80)
    scales_top = int(height * 0.16)
    dr.line((scales_cx, scales_top, scales_cx, int(height * 0.66)), fill=(70, 66, 58), width=5)
    dr.line((scales_cx - 52, scales_top + 14, scales_cx + 52, scales_top + 14), fill=(70, 66, 58), width=4)
    for pan_dx in (-52, 52):
        pan_cx = scales_cx + pan_dx
        pan_y = scales_top + 44
        dr.line((pan_cx, scales_top + 14, pan_cx - 16, pan_y), fill=(70, 66, 58), width=2)
        dr.line((pan_cx, scales_top + 14, pan_cx + 16, pan_y), fill=(70, 66, 58), width=2)
        dr.pieslice((pan_cx - 20, pan_y - 6, pan_cx + 20, pan_y + 14), 0, 180, fill=(176, 140, 62))
    dr.ellipse((scales_cx - 8, scales_top - 8, scales_cx + 8, scales_top + 8), fill=(176, 140, 62))
    dr.rectangle((scales_cx - 26, int(height * 0.66), scales_cx + 26, int(height * 0.70)), fill=(70, 66, 58))
    return img


def scene_gaza(width, height):
    img, dr = blank_scene(width, height, (232, 214, 178), (240, 226, 196))
    draw_sun(dr, int(width * 0.86), int(height * 0.16), int(height * 0.09), (246, 222, 160))
    ground_y = int(height * 0.90)
    ruin_rng = random.Random(31)
    ruin_x = int(width * 0.03)
    while ruin_x < int(width * 0.94):
        ruin_w = ruin_rng.randint(30, 52)
        ruin_h = ruin_rng.randint(40, 96)
        ruin_top = ground_y - ruin_h
        ruin_fill = (178, 168, 152)
        if ruin_x % 2 == 0:
            ruin_fill = (168, 158, 142)
        dr.rectangle((ruin_x, ruin_top, ruin_x + ruin_w, ground_y), fill=ruin_fill)
        notch_w = ruin_rng.randint(8, 18)
        notch_x = ruin_x + ruin_rng.randint(0, max(1, ruin_w - notch_w))
        dr.rectangle((notch_x, ruin_top, notch_x + notch_w, ruin_top + ruin_rng.randint(8, 22)), fill=(232, 214, 178))
        hole_y = ruin_top + 14
        while hole_y < ground_y - 12:
            hole_x = ruin_x + 6
            while hole_x < ruin_x + ruin_w - 8:
                hole_roll = ruin_rng.random()
                if hole_roll > 0.4:
                    dr.rectangle((hole_x, hole_y, hole_x + 6, hole_y + 8), fill=(104, 98, 88))
                hole_x = hole_x + 13
            hole_y = hole_y + 16
        ruin_x = ruin_x + ruin_w + ruin_rng.randint(2, 7)
    dr.rectangle((0, ground_y, width, height), fill=(186, 172, 148))
    line_y = int(height * 0.68)
    dash_x = 0
    while dash_x < width:
        dr.rectangle((dash_x, line_y, dash_x + 26, line_y + 6), fill=(238, 196, 40))
        dash_x = dash_x + 40
    dust_specs = [(0.20, 0.30, 20), (0.55, 0.22, 26), (0.78, 0.34, 16)]
    for dust_fx, dust_fy, dust_scale in dust_specs:
        draw_cloud(dr, int(width * dust_fx), int(height * dust_fy), dust_scale, (222, 208, 182))
    return img


def scene_cricket(width, height):
    img = Image.new("RGB", (width, height), (84, 140, 74))
    dr = ImageDraw.Draw(img)
    band_i = 0
    while band_i < 6:
        band_y0 = int(height * band_i / 6)
        band_y1 = int(height * (band_i + 1) / 6)
        band_fill = (80, 134, 70)
        if band_i % 2 == 1:
            band_fill = (92, 148, 80)
        dr.rectangle((0, band_y0, width, band_y1), fill=band_fill)
        band_i = band_i + 1
    pitch_x0 = int(width * 0.40)
    pitch_x1 = int(width * 0.60)
    dr.rectangle((pitch_x0, int(height * 0.10), pitch_x1, int(height * 0.92)), fill=(216, 198, 156))
    for stump_fy in (0.16, 0.82):
        stump_y = int(height * stump_fy)
        stump_i = 0
        while stump_i < 3:
            stump_x = int(width * 0.475) + stump_i * 9
            dr.rectangle((stump_x, stump_y, stump_x + 4, stump_y + 18), fill=(240, 220, 170))
            stump_i = stump_i + 1
    bat_cx = int(width * 0.50)
    bat_cy = int(height * 0.60)
    dr.ellipse((bat_cx - 9, bat_cy - 40, bat_cx + 9, bat_cy - 22), fill=(216, 172, 138))
    dr.line((bat_cx, bat_cy - 22, bat_cx - 12, bat_cy + 12), fill=(246, 246, 244), width=7)
    dr.line((bat_cx, bat_cy - 22, bat_cx + 14, bat_cy + 10), fill=(246, 246, 244), width=7)
    dr.line((bat_cx - 12, bat_cy + 12, bat_cx - 16, bat_cy + 38), fill=(246, 246, 244), width=7)
    dr.line((bat_cx + 14, bat_cy + 10, bat_cx + 22, bat_cy + 36), fill=(246, 246, 244), width=7)
    dr.line((bat_cx + 10, bat_cy - 14, bat_cx + 30, bat_cy + 16), fill=(150, 104, 62), width=6)
    dr.ellipse((int(width * 0.30), int(height * 0.30), int(width * 0.30) + 10, int(height * 0.30) + 10), fill=(196, 44, 40))
    dr.ellipse((int(width * 0.68), int(height * 0.70), int(width * 0.68) + 10, int(height * 0.70) + 10), fill=(250, 240, 210))
    crowd_y = int(height * 0.94)
    crowd_rng = random.Random(53)
    crowd_x = 4
    while crowd_x < width - 6:
        crowd_pick = crowd_rng.randint(0, 3)
        crowd_color = (214, 96, 84)
        if crowd_pick == 1:
            crowd_color = (240, 230, 210)
        if crowd_pick == 2:
            crowd_color = (96, 130, 190)
        if crowd_pick == 3:
            crowd_color = (240, 200, 90)
        dr.ellipse((crowd_x, crowd_y + crowd_rng.randint(-3, 3), crowd_x + 7, crowd_y + 7), fill=crowd_color)
        crowd_x = crowd_x + 10
    return img


def scene_gtavi(width, height):
    img, dr = blank_scene(width, height, (66, 40, 96), (238, 110, 120))
    horizon_y = int(height * 0.72)
    draw_sun(dr, int(width * 0.50), int(height * 0.52), int(height * 0.20), (250, 176, 110))
    skyline_rng = random.Random(61)
    tower_x = 4
    while tower_x < width - 14:
        tower_w = skyline_rng.randint(16, 34)
        tower_h = skyline_rng.randint(24, 84)
        tower_top = horizon_y - tower_h
        dr.rectangle((tower_x, tower_top, tower_x + tower_w, horizon_y), fill=(44, 30, 62))
        win_y = tower_top + 5
        while win_y < horizon_y - 6:
            win_x = tower_x + 4
            while win_x < tower_x + tower_w - 5:
                win_roll = skyline_rng.random()
                if win_roll > 0.5:
                    dr.rectangle((win_x, win_y, win_x + 3, win_y + 4), fill=(255, 214, 140))
                win_x = win_x + 8
            win_y = win_y + 10
        tower_x = tower_x + tower_w + skyline_rng.randint(2, 7)
    dr.rectangle((0, horizon_y, width, height), fill=(30, 24, 44))
    draw_palm(dr, int(width * 0.08), int(height * 0.98), 74, (16, 12, 24), (16, 12, 24))
    draw_palm(dr, int(width * 0.90), int(height * 0.98), 84, (16, 12, 24), (16, 12, 24))
    car_y = int(height * 0.90)
    car_pts = [(int(width * 0.36), car_y), (int(width * 0.42), car_y - 14), (int(width * 0.58), car_y - 14), (int(width * 0.66), car_y), (int(width * 0.64), car_y + 8), (int(width * 0.38), car_y + 8)]
    dr.polygon(car_pts, fill=(14, 10, 20))
    dr.ellipse((int(width * 0.40), car_y + 2, int(width * 0.40) + 14, car_y + 16), fill=(8, 6, 12))
    dr.ellipse((int(width * 0.58), car_y + 2, int(width * 0.58) + 14, car_y + 16), fill=(8, 6, 12))
    dr.rectangle((int(width * 0.365), car_y + 2, int(width * 0.39), car_y + 5), fill=(255, 120, 120))
    dr.rectangle((int(width * 0.615), car_y + 2, int(width * 0.64), car_y + 5), fill=(255, 240, 190))
    return img


def scene_f1(width, height):
    img, dr = blank_scene(width, height, (26, 26, 44), (52, 48, 74))
    track_pts = [(0, int(height * 0.98)), (int(width * 0.30), int(height * 0.62)), (int(width * 0.55), int(height * 0.60)), (int(width * 0.78), int(height * 0.78)), (width, int(height * 0.70)), (width, height), (0, height)]
    dr.polygon(track_pts, fill=(86, 88, 98))
    edge_pts_top = [(0, int(height * 0.98)), (int(width * 0.30), int(height * 0.62)), (int(width * 0.55), int(height * 0.60)), (int(width * 0.78), int(height * 0.78)), (width, int(height * 0.70))]
    dr.line(edge_pts_top, fill=(238, 238, 240), width=4)
    neon_specs = [(0.06, 0.10, (255, 110, 180)), (0.24, 0.06, (110, 220, 255)), (0.62, 0.08, (255, 196, 90)), (0.82, 0.14, (170, 130, 255))]
    for neon_fx, neon_fy, neon_fill in neon_specs:
        neon_x = int(width * neon_fx)
        neon_y = int(height * neon_fy)
        dr.rectangle((neon_x, neon_y, neon_x + 64, neon_y + 26), outline=neon_fill, width=3)
        dr.rectangle((neon_x + 8, neon_y + 8, neon_x + 56, neon_y + 18), fill=neon_fill)
    tower_specs = [(0.44, 0.30, 90), (0.52, 0.24, 110), (0.90, 0.36, 70)]
    for tower_fx, tower_fy, tower_h in tower_specs:
        tower_x = int(width * tower_fx)
        tower_base = int(height * 0.60)
        dr.rectangle((tower_x, tower_base - tower_h, tower_x + 22, tower_base), fill=(20, 20, 34))
        win_y = tower_base - tower_h + 6
        while win_y < tower_base - 8:
            dr.rectangle((tower_x + 5, win_y, tower_x + 9, win_y + 4), fill=(255, 224, 150))
            dr.rectangle((tower_x + 13, win_y, tower_x + 17, win_y + 4), fill=(170, 220, 255))
            win_y = win_y + 11
    car_cx = int(width * 0.40)
    car_cy = int(height * 0.80)
    car_body = [(car_cx - 74, car_cy + 12), (car_cx - 40, car_cy - 4), (car_cx + 6, car_cy - 10), (car_cx + 52, car_cy + 2), (car_cx + 76, car_cy + 12)]
    dr.polygon(car_body, fill=(206, 44, 40))
    dr.rectangle((car_cx - 84, car_cy + 6, car_cx - 60, car_cy + 14), fill=(30, 30, 38))
    dr.rectangle((car_cx + 58, car_cy - 6, car_cx + 84, car_cy + 2), fill=(30, 30, 38))
    dr.ellipse((car_cx - 52, car_cy + 8, car_cx - 30, car_cy + 26), fill=(12, 12, 16))
    dr.ellipse((car_cx + 30, car_cy + 8, car_cx + 52, car_cy + 26), fill=(12, 12, 16))
    spray_rng = random.Random(71)
    spray_i = 0
    while spray_i < 60:
        spray_x = car_cx - 90 + spray_rng.randint(-16, 30)
        spray_y = car_cy + spray_rng.randint(-8, 22)
        dr.ellipse((spray_x, spray_y, spray_x + 3, spray_y + 3), fill=(210, 224, 236))
        spray_i = spray_i + 1
    draw_rain(dr, width, height, 73, 150, (168, 190, 214))
    return img


def scene_cpi(width, height):
    img, dr = blank_scene(width, height, (226, 220, 200), (238, 232, 214))
    base_y = int(height * 0.86)
    dr.rectangle((0, base_y, width, height), fill=(196, 186, 164))
    bar_specs = [(0.10, 0.30), (0.26, 0.38), (0.42, 0.48), (0.58, 0.58), (0.74, 0.74)]
    for bar_fx, bar_frac in bar_specs:
        bar_x = int(width * bar_fx)
        bar_w = int(width * 0.11)
        bar_top = base_y - int((base_y - int(height * 0.12)) * bar_frac)
        bar_fill = (120, 128, 138)
        if bar_frac > 0.7:
            bar_fill = (196, 52, 40)
        dr.rectangle((bar_x, bar_top, bar_x + bar_w, base_y), fill=bar_fill)
    arrow_pts = [(int(width * 0.08), int(height * 0.55)), (int(width * 0.30), int(height * 0.46)),
                 (int(width * 0.52), int(height * 0.36)), (int(width * 0.78), int(height * 0.18))]
    dr.line(arrow_pts, fill=(196, 52, 40), width=5)
    arrow_tip = arrow_pts[-1]
    dr.polygon([(arrow_tip[0], arrow_tip[1]), (arrow_tip[0] - 20, arrow_tip[1] + 2), (arrow_tip[0] - 10, arrow_tip[1] + 18)], fill=(196, 52, 40))
    coin_x = int(width * 0.86)
    coin_y = int(height * 0.30)
    coin_i = 0
    while coin_i < 3:
        coin_box = (coin_x - 14, coin_y - 14 + coin_i * 5, coin_x + 14, coin_y + 14 + coin_i * 5)
        dr.ellipse(coin_box, fill=(214, 178, 90), outline=(150, 118, 52), width=2)
        coin_i = coin_i + 1
    return img


SCENE_BUILDERS = {
    "akvan": scene_akvan,
    "kyiv": scene_kyiv,
    "selloff": scene_selloff,
    "ukeu": scene_ukeu,
    "cop31": scene_cop31,
    "hormuz": scene_hormuz,
    "senate": scene_senate,
    "jakarta": scene_jakarta,
    "hague": scene_hague,
    "gaza": scene_gaza,
    "cricket": scene_cricket,
    "gtavi": scene_gtavi,
    "f1": scene_f1,
    "cpi": scene_cpi,
}


def build_scene(scene_key, width, height):
    builder_fn = SCENE_BUILDERS[scene_key]
    scene_img = builder_fn(width, height)
    return scene_img
