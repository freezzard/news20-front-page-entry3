"""Drawing helpers, text fitting and the flat polygon world map.

The map is drawn from simplified continent rings in longitude and
latitude, projected equirectangularly onto the map box. The rings
are deliberately coarse: recognition over precision, at the small
size the map prints. No external geography file is read.
"""

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/noto/"
FONT_FILES = {
    "serif-black": "NotoSerifDisplay-Black.ttf",
    "serif-xbold": "NotoSerifDisplay-ExtraBold.ttf",
    "serif-bold": "NotoSerif-Bold.ttf",
    "serif": "NotoSerif-Regular.ttf",
    "serif-italic": "NotoSerif-Italic.ttf",
    "sans": "NotoSans-Regular.ttf",
    "sans-med": "NotoSans-Medium.ttf",
    "sans-bold": "NotoSans-Bold.ttf",
    "sans-xbold": "NotoSans-ExtraBold.ttf",
}
FONT_CACHE = {}


def load_font(kind, size):
    cache_key = kind + ":" + str(size)
    cached_font = FONT_CACHE.get(cache_key)
    picked_font = cached_font
    if cached_font is None:
        picked_font = ImageFont.truetype(FONT_DIR + FONT_FILES[kind], size)
        FONT_CACHE[cache_key] = picked_font
    return picked_font


def wrap_lines(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        trial_line = word
        if current_line != "":
            trial_line = current_line + " " + word
        trial_width = draw.textlength(trial_line, font=font)
        fits = trial_width <= max_width
        next_line = trial_line
        if fits is False:
            lines.append(current_line)
            next_line = word
        current_line = next_line
    if current_line != "":
        lines.append(current_line)
    return lines


def draw_wrapped(draw, xy, text, font, fill, max_width, line_gap, max_lines):
    lines = wrap_lines(draw, text, font, max_width)
    clipped_lines = lines
    if len(lines) > max_lines:
        clipped_lines = lines[:max_lines]
    pen_y = xy[1]
    for line_text in clipped_lines:
        draw.text((xy[0], pen_y), line_text, font=font, fill=fill)
        pen_y = pen_y + line_gap
    used_height = pen_y - xy[1]
    return used_height


def centered_text(draw, center_x, y, text, font, fill):
    text_width = draw.textlength(text, font=font)
    draw.text((center_x - text_width / 2, y), text, font=font, fill=fill)
    return text_width


def chip(draw, xy, label, fill, text_fill):
    chip_font = load_font("sans-xbold", 19)
    label_width = draw.textlength(label, font=chip_font)
    chip_box = (xy[0], xy[1], xy[0] + label_width + 18, xy[1] + 27)
    draw.rectangle(chip_box, fill=fill)
    draw.text((xy[0] + 9, xy[1] + 3), label, font=chip_font, fill=text_fill)
    return chip_box[2] - chip_box[0]


NORTH_AMERICA = [
    (-168, 66), (-160, 70), (-150, 70), (-140, 70), (-130, 70), (-120, 69),
    (-110, 68), (-100, 68), (-95, 69), (-90, 69), (-85, 66), (-82, 66),
    (-80, 70), (-78, 68), (-75, 69), (-72, 62), (-70, 60), (-68, 58),
    (-65, 60), (-60, 55), (-55, 52), (-58, 50), (-60, 47), (-65, 44),
    (-68, 44), (-70, 41), (-74, 39), (-75, 35), (-76, 35), (-80, 32),
    (-81, 26), (-84, 30), (-86, 30), (-89, 30), (-91, 29), (-94, 29),
    (-97, 26), (-97, 22), (-94, 19), (-92, 16), (-90, 14), (-87, 13),
    (-83, 9), (-79, 9), (-77, 7), (-80, 8), (-82, 9), (-84, 12),
    (-87, 15), (-89, 16), (-91, 18), (-93, 19), (-96, 19), (-97, 22),
    (-97, 25), (-95, 28), (-92, 29), (-90, 29), (-87, 30), (-84, 30),
    (-82, 28), (-81, 25), (-80, 27), (-80, 32), (-76, 35), (-74, 38),
    (-71, 41), (-69, 43), (-66, 44), (-61, 46), (-60, 47), (-56, 50),
    (-60, 52), (-64, 58), (-67, 55), (-70, 58), (-73, 60), (-77, 62),
    (-80, 66), (-85, 66), (-90, 68), (-95, 69), (-105, 68), (-115, 69),
    (-125, 70), (-135, 69), (-145, 70), (-155, 71), (-162, 70),
]

SOUTH_AMERICA = [
    (-77, 8), (-75, 10), (-72, 12), (-68, 11), (-64, 10), (-61, 9),
    (-59, 8), (-55, 6), (-52, 5), (-50, 0), (-48, -2), (-44, -3),
    (-40, -5), (-35, -8), (-35, -10), (-38, -15), (-39, -18), (-41, -22),
    (-46, -24), (-48, -28), (-52, -32), (-57, -38), (-62, -41), (-65, -45),
    (-68, -50), (-68, -54), (-66, -55), (-70, -54), (-73, -50), (-73, -44),
    (-73, -37), (-72, -30), (-70, -23), (-70, -18), (-75, -15), (-79, -9),
    (-81, -6), (-80, -3), (-79, 1), (-77, 4),
]

EURASIA = [
    (-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 46), (-1, 49), (2, 51),
    (4, 53), (7, 54), (8, 57), (10, 59), (12, 57), (18, 56), (21, 55),
    (24, 58), (22, 60), (21, 64), (25, 66), (26, 70), (30, 70), (35, 69),
    (40, 68), (45, 68), (50, 69), (55, 69), (60, 69), (66, 70), (70, 72),
    (75, 73), (80, 73), (85, 74), (90, 75), (95, 76), (100, 77),
    (105, 77), (110, 74), (115, 73), (120, 73), (125, 72), (130, 71),
    (135, 72), (140, 72), (145, 72), (150, 70), (155, 69), (160, 69),
    (162, 66), (165, 65), (170, 66), (178, 65), (178, 62), (172, 62),
    (168, 60), (162, 58), (160, 55), (158, 52), (156, 51), (150, 59),
    (145, 59), (142, 55), (140, 50), (138, 46), (135, 43), (132, 42),
    (130, 42), (127, 40), (126, 38), (122, 38), (120, 34), (122, 30),
    (120, 27), (115, 23), (110, 20), (108, 18), (106, 10), (104, 8),
    (101, 7), (100, 10), (98, 13), (95, 16), (92, 21), (90, 22),
    (87, 21), (85, 20), (82, 17), (80, 13), (77, 8), (75, 11),
    (73, 16), (70, 20), (67, 23), (65, 25), (62, 25), (58, 26),
    (56, 27), (53, 27), (51, 28), (49, 30), (48, 29), (50, 26),
    (54, 26), (56, 25), (58, 23), (58, 20), (55, 17), (53, 16),
    (50, 15), (47, 14), (44, 13), (42, 15), (40, 16), (39, 21),
    (38, 25), (37, 28), (35, 29), (34, 31), (35, 33), (36, 36),
    (33, 36), (30, 36), (27, 37), (26, 38), (24, 38), (22, 37),
    (20, 40), (18, 40), (16, 38), (14, 42), (12, 44), (10, 44),
    (8, 44), (6, 43), (3, 42), (0, 38), (-2, 37), (-5, 36),
    (-8, 37),
]

AFRICA = [
    (-17, 15), (-16, 20), (-15, 24), (-13, 28), (-9, 31), (-6, 34),
    (-2, 35), (3, 37), (9, 37), (11, 34), (15, 32), (20, 32),
    (25, 32), (30, 31), (32, 31), (34, 28), (35, 23), (37, 19),
    (38, 18), (40, 15), (43, 12), (46, 11), (51, 12), (51, 10),
    (48, 7), (45, 4), (42, 0), (41, -4), (40, -8), (38, -12),
    (36, -18), (35, -22), (32, -26), (29, -30), (26, -33), (20, -35),
    (17, -32), (15, -28), (13, -22), (12, -18), (13, -12), (12, -6),
    (9, -2), (9, 4), (6, 4), (2, 6), (-3, 5), (-8, 5), (-12, 8),
    (-15, 11), (-17, 14),
]

AUSTRALIA = [
    (113, -22), (114, -28), (115, -33), (118, -35), (122, -34), (126, -32),
    (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (144, -38),
    (147, -39), (150, -37), (153, -32), (153, -27), (151, -24), (149, -20),
    (146, -19), (143, -15), (142, -11), (139, -15), (136, -12), (135, -15),
    (132, -12), (130, -13), (128, -14), (125, -14), (122, -17), (119, -20),
    (115, -21),
]

ISLAND_RINGS = [
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-2, 50)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (141, 38),
     (141, 41), (143, 42), (144, 44), (142, 45), (140, 43), (139, 39),
     (137, 37), (134, 35), (131, 33)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -37),
     (175, -39), (172, -42), (169, -45)],
    [(-44, 60), (-40, 63), (-35, 66), (-30, 68), (-25, 70), (-20, 70),
     (-22, 74), (-28, 76), (-35, 76), (-42, 75), (-48, 74), (-52, 70),
     (-55, 66), (-52, 63), (-48, 60)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (45, -25),
     (43, -22), (43, -18)],
    [(109, 1), (111, 3), (114, 4), (117, 5), (119, 2), (118, -1),
     (116, -3), (113, -4), (110, -2)],
    [(95, 5), (98, 3), (101, 0), (104, -3), (107, -6), (111, -7),
     (114, -8), (118, -9), (120, -10), (118, -9), (114, -8), (110, -7),
     (106, -6), (102, -4), (99, 1), (96, 4)],
    [(120, 18), (121, 16), (122, 14), (121, 12), (123, 10), (125, 9),
     (126, 7), (124, 9), (122, 11), (120, 14), (120, 17)],
    [(-22, 64), (-18, 63), (-14, 64), (-15, 66), (-19, 66), (-22, 65)],
]

CONTINENT_RINGS = [
    NORTH_AMERICA, SOUTH_AMERICA, EURASIA, AFRICA, AUSTRALIA,
] + ISLAND_RINGS

MAP_LON_MIN = -180.0
MAP_LON_SPAN = 360.0
MAP_LAT_MAX = 84.0
MAP_LAT_SPAN = 148.0


def map_point(lon, lat, box):
    frac_x = (lon - MAP_LON_MIN) / MAP_LON_SPAN
    frac_y = (MAP_LAT_MAX - lat) / MAP_LAT_SPAN
    point_x = box[0] + frac_x * (box[2] - box[0])
    point_y = box[1] + frac_y * (box[3] - box[1])
    return (point_x, point_y)


def draw_world_map(canvas, box, land_fill, sea_fill):
    map_draw = ImageDraw.Draw(canvas)
    map_draw.rectangle(box, fill=sea_fill)
    for ring in CONTINENT_RINGS:
        ring_pts = []
        for ring_lon, ring_lat in ring:
            ring_pts.append(map_point(ring_lon, ring_lat, box))
        map_draw.polygon(ring_pts, fill=land_fill)
    return map_draw


def draw_map_pin(draw, xy, number, fill, ring_fill):
    pin_r = 19
    pin_box = (xy[0] - pin_r, xy[1] - pin_r, xy[0] + pin_r, xy[1] + pin_r)
    draw.ellipse(pin_box, fill=fill, outline=ring_fill, width=3)
    label = str(number)
    label_font = load_font("sans-xbold", 22)
    label_width = draw.textlength(label, font=label_font)
    draw.text((xy[0] - label_width / 2, xy[1] - 12), label, font=label_font, fill=ring_fill)
    return pin_r
