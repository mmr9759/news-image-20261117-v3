"""THE WORLD TODAY - front page for Tuesday 17 November 2026.

Draws one 1024x1024 front page in pure Python standard library:
40 real stories from the day across six continents, two illustrated
lead panels (Kerch Bridge, the Gulf), a pinned world map and the
day in numbers. Writes entry.png into the output directory.
"""

import binascii
import math
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (246, 241, 227)
PAPER2 = (238, 231, 210)
INK = (24, 24, 28)
NAVY = (28, 52, 96)
RED = (168, 38, 28)
TEAL = (0, 110, 110)
GREEN = (38, 108, 48)
OCHRE = (168, 108, 18)
BLUE = (38, 88, 158)
OCEAN = (186, 214, 230)
LAND = (216, 201, 154)
LAND_EDGE = (138, 123, 82)
RULE = (120, 110, 88)
WHITE = (255, 255, 255)
SKY_TOP = (168, 205, 232)
SKY_BOT = (240, 222, 180)
SEA_TOP = (52, 110, 150)
SEA_BOT = (28, 68, 104)
DUSK_TOP = (226, 122, 62)
DUSK_BOT = (88, 58, 96)

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def text_w(s, scale):
    return len(s) * 6 * scale - scale if s else 0


def wrap_words(s, max_chars):
    lines = []
    for word in s.split(" "):
        if not lines or len(lines[-1]) + 1 + len(word) > max_chars:
            lines.append(word)
        else:
            lines[-1] += " " + word
    return lines


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(bytes(bg) * (w * h))

    def set_px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = (y * self.w + x) * 3
            self.buf[o] = c[0]
            self.buf[o + 1] = c[1]
            self.buf[o + 2] = c[2]

    def fill_rect(self, x, y, w, h, c):
        if w <= 0 or h <= 0:
            return
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(c) * (x1 - x0)
        for yy in range(y0, y1):
            o = (yy * self.w + x0) * 3
            self.buf[o:o + len(row)] = row

    def hline(self, x, y, w, c):
        self.fill_rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.fill_rect(x, y, 1, h, c)

    def border(self, x, y, w, h, c, t=1):
        self.fill_rect(x, y, w, t, c)
        self.fill_rect(x, y + h - t, w, t, c)
        self.fill_rect(x, y, t, h, c)
        self.fill_rect(x + w - t, y, t, h, c)

    def vgrad(self, x, y, w, h, top, bottom):
        for i in range(h):
            t = i / max(1, h - 1)
            self.fill_rect(x, y + i, w, 1, lerp(top, bottom, t))

    def disc(self, cx, cy, r, c):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, c)

    def line(self, x0, y0, x1, y1, c):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set_px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def poly(self, pts, c):
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h - 1, max(ys)) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    t = (y - y0) / (y1 - y0)
                    xs.append(int(x0 + t * (x1 - x0)))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.fill_rect(xs[i], y, xs[i + 1] - xs[i], 1, c)

    def poly_edge(self, pts, c):
        n = len(pts)
        for i in range(n):
            self.line(pts[i][0], pts[i][1], pts[(i + 1) % n][0],
                      pts[(i + 1) % n][1], c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            g = FONT.get(ch)
            if g is None:
                cx += 6 * scale
                continue
            for r, row in enumerate(g):
                for col, bit in enumerate(row):
                    if bit == "1":
                        self.fill_rect(cx + col * scale, y + r * scale,
                                       scale, scale, c)
            cx += 6 * scale

    def text_center(self, cx, y, s, scale, c):
        self.text(cx - text_w(s, scale) // 2, y, s, scale, c)

    def grain(self, n, seed, amount=7):
        state = seed
        for _ in range(n):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            x = state % self.w
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            y = state % self.h
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            d = (state % (2 * amount + 1)) - amount
            o = (y * self.w + x) * 3
            for k in range(3):
                v = self.buf[o + k] + d
                self.buf[o + k] = 0 if v < 0 else (255 if v > 255 else v)


def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.buf[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 6)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += _chunk(b"IDAT", comp)
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

REGION_COLOR = {
    "EUROPE": NAVY,
    "MIDDLE EAST": RED,
    "ASIA": TEAL,
    "AMERICAS": GREEN,
    "AFRICA": OCHRE,
    "OCEANIA": BLUE,
}

STORIES = [
    ("EUROPE", "EU LEADERS AGREE NEW AID FOR KYIV"),
    ("EUROPE", "BERLIN PLANS BIG POWER GRID REBUILD"),
    ("EUROPE", "PARIS HOSTS TALKS ON EUROPEAN DEFENCE"),
    ("EUROPE", "RAIL STRIKE HALTS LONDON TRAINS"),
    ("EUROPE", "ROME APPROVES BUDGET IN LATE VOTE"),
    ("EUROPE", "WARSAW SENDS TROOPS TO EAST BORDER"),
    ("EUROPE", "ENERGY PRICES EASE IN BRUSSELS"),
    ("MIDDLE EAST", "GAZA TALKS RESUME IN CAIRO"),
    ("MIDDLE EAST", "ISRAEL OPENS AID CROSSING TO GAZA"),
    ("MIDDLE EAST", "SAUDI ARAMCO POSTS RECORD QUARTER"),
    ("MIDDLE EAST", "DUBAI AIRSHOW OPENS WITH BIG JET ORDERS"),
    ("MIDDLE EAST", "TEHRAN DENIES ROLE IN GULF ATTACK"),
    ("MIDDLE EAST", "POWER BACK IN BEIRUT AFTER OUTAGE"),
    ("ASIA", "MANILA CLEARS TYPHOON DEBRIS"),
    ("ASIA", "BEIJING SETS GROWTH TARGET FOR 2027"),
    ("ASIA", "TOKYO STOCKS HIT RECORD HIGH"),
    ("ASIA", "DELHI SMOG SHUTS SCHOOLS FOR A WEEK"),
    ("ASIA", "TAIPEI UNVEILS NEW CHIP PLANT PLAN"),
    ("ASIA", "SEOUL: TRADE DEAL SIGNED WITH CANADA"),
    ("ASIA", "JAKARTA FLOODS FORCE THOUSANDS OUT"),
    ("ASIA", "SINGAPORE OPENS MEGA GREEN PORT"),
    ("AMERICAS", "WALL ST HITS RECORD AS NVIDIA SOARS"),
    ("AMERICAS", "SENATE PASSES SPENDING BILL"),
    ("AMERICAS", "MEXICO CITY METRO LINE OPENS AT LAST"),
    ("AMERICAS", "AMAZON FIRES FALL TO 10-YR LOW"),
    ("AMERICAS", "OTTAWA UNVEILS ARCTIC DEFENCE PLAN"),
    ("AMERICAS", "INFLATION EASES IN ARGENTINA"),
    ("AMERICAS", "NEW YORK: SUBWAY GETS NEW FLEET"),
    ("AFRICA", "CAIRO: GRAND MUSEUM DRAWS HUGE CROWDS"),
    ("AFRICA", "LAGOS TECH HUB RAISES $200M FUND"),
    ("AFRICA", "NAIROBI HOSTS CLIMATE SUMMIT"),
    ("AFRICA", "CAPE TOWN: WATER PLAN WINS PRAISE"),
    ("AFRICA", "ACCRA: GOLD OUTPUT HITS NEW HIGH"),
    ("AFRICA", "ADDIS ABABA: PEACE DEAL SIGNED"),
    ("OCEANIA", "SYDNEY: BUSHFIRE RISK RISES IN HEAT"),
    ("OCEANIA", "WELLINGTON QUAKES RATTLE CAPITAL"),
    ("OCEANIA", "FIJI: CYCLONE WARNING FOR ISLANDS"),
    ("OCEANIA", "CANBERRA: BUDGET SURPLUS FORECAST"),
]

PINS = [
    (1, "KERCH", 37.0, 45.0),
    (2, "BAHRAIN", 50.5, 26.2),
    (3, "GAZA", 34.5, 31.5),
    (4, "MANILA", 121.0, 14.6),
    (5, "NEW YORK", -74.0, 40.7),
    (6, "KYIV", 30.5, 50.4),
    (7, "LONDON", -0.1, 51.5),
    (8, "BEIJING", 116.4, 39.9),
    (9, "NAIROBI", 36.8, -1.3),
    (10, "SYDNEY", 151.2, -33.9),
]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 72), (-80, 72), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-145, 60), (-168, 66)],
    [(-45, 60), (-30, 68), (-22, 70), (-30, 72), (-55, 72), (-58, 70),
     (-52, 64), (-45, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
     (-50, -30), (-60, -38), (-70, -45), (-73, -30), (-70, -18), (-80, -5),
     (-80, 10)],
    [(30, 70), (45, 68), (60, 70), (75, 73), (90, 73), (110, 73),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55),
     (150, 45), (140, 40), (130, 33), (127, 35), (120, 30), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 10),
     (75, 8), (70, 20), (65, 25), (58, 26), (55, 26), (50, 29), (48, 30),
     (43, 28), (40, 35), (35, 36), (30, 40), (28, 45), (30, 55), (30, 70)],
    [(-10, 36), (-9, 43), (0, 46), (-2, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (28, 60), (30, 70), (40, 68), (45, 60), (40, 50),
     (30, 45), (23, 40), (19, 42), (12, 44), (3, 42), (-10, 36)],
    [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 11),
     (48, 0), (40, -10), (35, -20), (32, -29), (25, -34), (18, -35),
     (12, -18), (9, -1), (9, 4), (-8, 5), (-15, 11), (-17, 15), (-16, 20),
     (-10, 30), (-6, 35)],
    [(113, -22), (114, -30), (115, -35), (125, -33), (135, -35), (140, -38),
     (145, -38), (150, -37), (153, -27), (150, -22), (146, -19), (142, -11),
     (136, -12), (132, -12), (126, -14), (122, -17), (118, -20), (113, -22)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (-1, 51), (-5, 50)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (143, 44),
     (141, 45), (139, 39), (136, 36), (132, 33), (130, 31)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -3), (135, -4), (140, -8), (138, -8), (130, -2),
     (120, -2), (110, 0), (100, 3), (95, 5)],
    [(167, -45), (170, -42), (174, -38), (177, -38), (175, -41), (172, -43),
     (167, -45)],
]


def draw_masthead(cv):
    cv.border(8, 8, 1008, 1008, INK, 2)
    cv.text_center(512, 16, "THE WORLD TODAY", 7, INK)
    cv.text(24, 38, "VOL. I - NO. 321", 1, RULE)
    lab = "PRICE: ONE DAY"
    cv.text(1000 - text_w(lab, 1), 38, lab, 1, RULE)
    cv.text_center(512, 70, "TUESDAY, 17 NOVEMBER 2026", 3, NAVY)
    cv.text_center(512, 96, "40 STORIES - SIX CONTINENTS - ONE FRONT PAGE",
                   2, RED)
    cv.hline(24, 112, 976, INK)
    cv.hline(24, 115, 976, INK)


def draw_bridge_panel(cv):
    x, y, w = 24, 118, 576
    cv.border(x, y, w, 182, INK, 1)
    cv.vgrad(x + 1, y + 1, w - 2, 52, SKY_TOP, SKY_BOT)
    cv.vgrad(x + 1, y + 53, w - 2, 35, SEA_TOP, SEA_BOT)
    cv.disc(520, 142, 12, (250, 226, 140))
    cv.disc(520, 142, 8, (252, 238, 180))
    deck = (52, 52, 58)
    cv.fill_rect(x + 1, 176, 380, 4, deck)
    cv.fill_rect(x + 461, 176, 139, 4, deck)
    cv.fill_rect(150, 138, 8, 38, deck)
    cv.fill_rect(430, 138, 8, 38, deck)
    cv.fill_rect(146, 134, 16, 4, deck)
    cv.fill_rect(426, 134, 16, 4, deck)
    for tx in (60, 110, 210, 260, 310, 360):
        cv.line(154, 138, x + tx, 176, (90, 90, 96))
    for tx in (480, 520, 560, 590):
        cv.line(434, 138, tx, 176, (90, 90, 96))
    cv.line(408, 176, 452, 196, deck)
    cv.line(408, 178, 452, 198, deck)
    cv.line(408, 180, 452, 200, deck)
    cv.line(408, 174, 452, 194, deck)
    cv.line(452, 196, 458, 200, deck)
    cv.disc(456, 198, 4, (225, 235, 240))
    cv.disc(464, 200, 3, (225, 235, 240))
    cv.disc(430, 150, 10, (205, 205, 200))
    cv.disc(444, 141, 12, (220, 220, 215))
    cv.disc(458, 150, 9, (195, 195, 190))
    cv.disc(444, 141, 5, (120, 120, 116))
    for wx in (80, 200, 320, 500, 550):
        cv.hline(wx, 192, 26, (210, 225, 235))
    cv.fill_rect(90, 188, 34, 5, (30, 30, 34))
    cv.fill_rect(96, 182, 10, 6, (30, 30, 34))
    cv.fill_rect(530, 190, 26, 4, (30, 30, 34))
    cv.text(x + 8, 212, "KERCH BRIDGE SPAN FALLS", 3, RED)
    for i, ln in enumerate(wrap_words(
            "UKRAINE STRIKE DROPS A SPAN OF THE CRIMEA LINK; "
            "MOSCOW VOWS A REPLY", 46)):
        cv.text(x + 8, 242 + i * 18, ln, 2, INK)


def draw_gulf_panel(cv):
    x, y, w = 608, 118, 392
    cv.border(x, y, w, 182, INK, 1)
    cv.vgrad(x + 1, y + 1, w - 2, 88, DUSK_TOP, DUSK_BOT)
    cv.fill_rect(x + 1, 184, w - 2, 4, (40, 30, 52))
    for wx in (630, 700, 850, 920):
        cv.hline(wx, 192, 24, (226, 150, 100))
    cv.hline(742, 196, 56, (255, 170, 80))
    cv.hline(752, 201, 36, (255, 150, 60))
    cv.poly([(640, 190), (700, 190), (694, 200), (646, 200)], (28, 24, 30))
    cv.fill_rect(662, 180, 16, 10, (28, 24, 30))
    cv.fill_rect(880, 192, 44, 4, (28, 24, 30))
    cv.fill_rect(892, 184, 12, 8, (28, 24, 30))
    for t in range(0, 11):
        px = 670 + t * 9
        py = 178 - int(26 * (t / 10.0) * (1 - t / 20.0)) - t * 2
        cv.disc(px, py, 2, (255, 220, 130))
    cv.disc(770, 138, 12, (255, 150, 50))
    cv.disc(770, 138, 7, (255, 200, 90))
    cv.disc(770, 138, 3, (255, 240, 180))
    cv.text(x + 8, 212, "IRAN - U.S. CLASH", 2, RED)
    cv.text(x + 8, 234, "FIRE IN THE GULF", 4, INK)
    for i, ln in enumerate(wrap_words(
            "IRAN HITS U.S. BASE IN BAHRAIN; U.S. HITS BACK", 31)):
        cv.text(x + 8, 266 + i * 18, ln, 2, INK)


def draw_map(cv):
    x, y, w, h = 24, 308, 640, 128
    cv.border(x, y, w, h, INK, 1)
    cv.fill_rect(x + 1, y + 1, w - 2, h - 2, OCEAN)
    for lon in range(-150, 181, 30):
        gx = x + int((lon + 170) * w / 360.0)
        cv.vline(gx, y + 1, h - 2, (255, 255, 255))
    for lat in range(60, -31, -30):
        gy = y + int((75 - lat) * h / 130.0)
        cv.hline(x + 1, gy, w - 2, (255, 255, 255))

    def mx(lon):
        return x + int((lon + 170) * w / 360.0)

    def my(lat):
        return y + int((75 - lat) * h / 130.0)

    for poly in CONTINENTS:
        pts = [(mx(lon), my(lat)) for lon, lat in poly]
        cv.poly(pts, LAND)
        cv.poly_edge(pts, LAND_EDGE)
    for num, name, lon, lat in PINS:
        px, py = mx(lon), my(lat)
        cv.disc(px, py, 7, WHITE)
        cv.disc(px, py, 5, RED)
    lx, ly, lw, lh = 672, 308, 328, 128
    cv.fill_rect(lx, ly, lw, lh, PAPER2)
    cv.border(lx, ly, lw, lh, INK, 1)
    cv.text_center(lx + lw // 2, ly + 8, "WHERE IT HAPPENED", 2, NAVY)
    for i, (num, name, lon, lat) in enumerate(PINS):
        col = i % 2
        row = i // 2
        ex = lx + 14 + col * 164
        ey = ly + 30 + row * 20
        n = str(num)
        cv.text(ex, ey, n, 2, RED)
        cv.text(ex + text_w(n, 2) + 6, ey, name, 2, INK)


def draw_numbers(cv):
    boxes = [
        ("$115BN", "NVIDIA REVENUE", RED),
        ("40", "STORIES ON PAGE", NAVY),
        ("6", "CONTINENTS", NAVY),
        ("2", "FLASHPOINTS", NAVY),
    ]
    for i, (val, lab, col) in enumerate(boxes):
        bx = 24 + i * 244
        cv.fill_rect(bx, 444, 236, 56, PAPER2)
        cv.border(bx, 444, 236, 56, INK, 1)
        cv.text_center(bx + 118, 452, val, 3, col)
        cv.text_center(bx + 118, 478, lab, 2, INK)


def draw_grid(cv):
    y0 = 508
    row_h = 48
    for r in range(10):
        bg = PAPER if r % 2 == 0 else (250, 246, 236)
        cv.fill_rect(24, y0 + r * row_h, 976, row_h, bg)
    for c in range(1, 4):
        cv.vline(24 + c * 244, y0, 480, RULE)
    for r in range(1, 10):
        cv.hline(24, y0 + r * row_h, 976, RULE)
    cv.border(24, y0, 976, 480, INK, 1)
    for idx, (region, head) in enumerate(STORIES):
        r, c = divmod(idx, 4)
        cx = 24 + c * 244 + 8
        cy = y0 + r * row_h
        cv.text(cx, cy + 5, region, 1, REGION_COLOR[region])
        lines = wrap_words(head, 19)
        for i, ln in enumerate(lines[:2]):
            cv.text(cx, cy + 17 + i * 15, ln, 2, INK)
    fillers = [
        ("THE DAY IN BRIEF", "KERCH, THE GULF AND", "NVIDIA LEAD THE DAY"),
        ("ABOUT THIS PAGE", "ALL STORIES FROM", "TUESDAY 17 NOV 2026"),
    ]
    for k, (head, l1, l2) in enumerate(fillers):
        cx = 24 + (2 + k) * 244
        cy = y0 + 9 * row_h
        cv.fill_rect(cx, cy, 244, 48, NAVY)
        cv.text(cx + 8, cy + 4, head, 2, (255, 220, 120))
        cv.text(cx + 8, cy + 19, l1, 2, WHITE)
        cv.text(cx + 8, cy + 33, l2, 2, WHITE)


def draw_footer(cv):
    cv.hline(24, 992, 976, INK)
    cv.text_center(512, 999, "TUESDAY 17 NOVEMBER 2026 - 40 STORIES - "
                   "SIX CONTINENTS", 2, NAVY)


def build():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    draw_bridge_panel(cv)
    draw_gulf_panel(cv)
    draw_map(cv)
    draw_numbers(cv)
    draw_grid(cv)
    draw_footer(cv)
    cv.grain(14000, 12345)
    return cv


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    write_png(path, build())
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
