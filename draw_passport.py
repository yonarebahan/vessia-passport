#!/usr/bin/env python3
"""Draw the open passport spread of the Republic of Vessia, entirely in code.

Renders entry.png (1024x724) beside this file. Deterministic: no randomness.
The data page (right) and the visas page (left) share one typographic system:
small grey bilingual labels, bold black values, thin rules between rows.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 724

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

# ---- palette -------------------------------------------------------------
COVER = (96, 22, 36)          # deep burgundy cover
COVER_EDGE = (70, 14, 26)
CREAM = (248, 244, 231)       # data page
VISAPAGE = (232, 237, 241)    # visas page, pale blue-grey
INK = (22, 22, 22)
LABEL = (104, 104, 100)
RULE = (178, 172, 156)
NAVY = (26, 44, 92)
BLUE_INK = (32, 54, 128)
BURG_INK = (122, 30, 48)
GREEN_INK = (18, 62, 40)


def f(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, font):
    return draw.textlength(s, font=font)


def star_points(cx, cy, r_out, r_in):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---- emblem ---------------------------------------------------------------
def draw_emblem(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    draw.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5],
                 outline=NAVY, width=1)
    # mountain: a triangle with a snow cap, sitting on a ground line
    top = (cx, cy - r + 16)
    left = (cx - r + 14, cy + r - 15)
    right = (cx + r - 14, cy + r - 15)
    draw.polygon([top, left, right], outline=NAVY, width=2)
    cap = [(cx - 6, cy - r + 27), (cx + 6, cy - r + 27),
           (cx + 3, cy - r + 21), (cx, cy - r + 25), (cx - 3, cy - r + 21)]
    draw.polygon([top] + cap, fill=NAVY)
    draw.line([cx - r + 10, cy + r - 15, cx + r - 10, cy + r - 15],
              fill=NAVY, width=2)
    # star above the peak
    draw.polygon(star_points(cx, cy - r - 2, 6, 2.5), fill=NAVY)


# ---- portrait --------------------------------------------------------------
def draw_portrait(base, x, y, w, h):
    """Engraved-style printed portrait inside the box at (x, y, w, h)."""
    p = Image.new("RGB", (w, h), (206, 213, 221))
    d = ImageDraw.Draw(p, "RGBA")
    cx = w // 2
    # shoulders / dark jacket
    d.polygon([(cx - 62, h), (cx - 54, h - 52), (cx - 20, h - 66),
               (cx + 20, h - 66), (cx + 54, h - 52), (cx + 62, h)],
              fill=(52, 54, 66))
    # shirt V
    d.polygon([(cx - 13, h - 64), (cx + 13, h - 64), (cx, h - 34)],
              fill=(226, 228, 230))
    # neck
    d.rectangle([cx - 11, h - 84, cx + 11, h - 58], fill=(219, 178, 146))
    # hair, pulled back: a dark shape behind the face, plus a small bun
    d.ellipse([cx - 45, 14, cx + 45, 124], fill=(56, 42, 36))
    d.ellipse([cx - 12, 2, cx + 12, 24], fill=(56, 42, 36))
    # face
    d.ellipse([cx - 39, 30, cx + 39, 138], fill=(233, 197, 168))
    # soft shading on the cheeks
    d.ellipse([cx - 34, 92, cx - 8, 122], fill=(224, 178, 146, 90))
    d.ellipse([cx + 8, 92, cx + 34, 122], fill=(224, 178, 146, 90))
    # brows and eyes
    for sgn in (-1, 1):
        ex = cx + sgn * 19
        d.line([ex - 10, 74, ex + 10, 73], fill=(70, 52, 44), width=3)
        d.ellipse([ex - 7, 82, ex + 7, 88], fill=(46, 38, 34))
    # nose
    d.line([cx + 1, 88, cx - 2, 106], fill=(196, 152, 118), width=2)
    d.line([cx - 6, 109, cx + 6, 109], fill=(196, 152, 118), width=2)
    # mouth
    d.arc([cx - 12, 112, cx + 12, 126], start=15, end=165,
          fill=(168, 96, 92), width=3)
    # fine horizontal print lines over the whole portrait
    for ly in range(0, h, 3):
        d.line([0, ly, w, ly], fill=(30, 30, 40, 26), width=1)
    base.paste(p, (x, y))
    ImageDraw.Draw(base).rectangle([x, y, x + w, y + h],
                                   outline=(90, 90, 90), width=2)


def draw_signature(draw, x, y):
    """A quick ink squiggle: the holder's signature."""
    pts = []
    for i in range(61):
        t = i / 60.0
        px = x + t * 118
        py = y + 10 * math.sin(t * 9.0) * (1 - t * 0.4) + 6 * math.sin(t * 23.0)
        pts.append((px, py))
    draw.line(pts, fill=(28, 40, 110), width=2)
    pts2 = [(x + 8 + i * 1.6, y + 16 - 9 * math.sin(i / 7.0))
            for i in range(30)]
    draw.line(pts2, fill=(28, 40, 110), width=2)


# ---- field system ------------------------------------------------------------
def field(draw, x, y, w, label, value, vfont, rule=True):
    draw.text((x, y), label, font=f(SANS, 11), fill=LABEL)
    draw.text((x, y + 14), value, font=vfont, fill=INK)
    if rule:
        draw.line([x, y + 42, x + w, y + 42], fill=RULE, width=1)


# ---- stamps ------------------------------------------------------------------
def stamp_layer(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def paste_rotated(base, layer, cx, cy, angle):
    rot = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(rot, (int(cx - rot.width / 2), int(cy - rot.height / 2)))


def stamp_round(cx, cy, r, angle, lines):
    lay = stamp_layer(2 * r + 8, 2 * r + 8)
    d = ImageDraw.Draw(lay)
    c = r + 4
    col = BLUE_INK + (205,)
    d.ellipse([4, 4, 2 * r + 4, 2 * r + 4], outline=col, width=3)
    d.ellipse([11, 11, 2 * r - 3, 2 * r - 3], outline=col, width=1)
    fonts = [f(SANSB, 13), f(SANS, 10), f(SANSB, 14)]
    total = 13 + 6 + 10 + 6 + 14
    ty = c - total / 2
    for (txt, fo, dy) in zip(lines, fonts, (13, 10, 14)):
        tw = d.textlength(txt, font=fo)
        d.text((c - tw / 2, ty), txt, font=fo, fill=col)
        ty += dy + 6
    return lay, angle


def stamp_rect(w, h, angle, colour, lines, fonts_sizes):
    lay = stamp_layer(w + 8, h + 8)
    d = ImageDraw.Draw(lay)
    col = colour + (205,)
    d.rectangle([4, 4, w + 4, h + 4], outline=col, width=3)
    d.rectangle([10, 10, w - 2, h - 2], outline=col, width=1)
    total = sum(s for _, s in fonts_sizes) + 5 * (len(lines) - 1)
    ty = (h + 8 - total) / 2
    for txt, size in fonts_sizes:
        fo = f(SANSB if size >= 14 else SANS, size)
        tw = d.textlength(txt, font=fo)
        d.text(((w + 8 - tw) / 2, ty), txt, font=fo, fill=col)
        ty += size + 5
    return lay, angle


def stamp_oval(w, h, angle, lines):
    lay = stamp_layer(w + 8, h + 8)
    d = ImageDraw.Draw(lay)
    col = BLUE_INK + (205,)
    d.ellipse([4, 4, w + 4, h + 4], outline=col, width=3)
    d.ellipse([11, 11, w - 3, h - 3], outline=col, width=1)
    sizes = (15, 11, 11, 16)
    total = sum(sizes) + 5 * 3
    ty = (h + 8 - total) / 2
    for txt, size in zip(lines, sizes):
        fo = f(SANSB if size >= 14 else SANS, size)
        tw = d.textlength(txt, font=fo)
        d.text(((w + 8 - tw) / 2, ty), txt, font=fo, fill=col)
        ty += size + 5
    return lay, angle


# ---- pages -------------------------------------------------------------------
def guilloche(draw, x0, y0, x1, y1):
    """Many thin pale sine curves across the data page."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for k in range(16):
        base_y = y0 + 12 + k * ((y1 - y0 - 24) / 15.0)
        col = (168, 186, 218, 52) if k % 2 == 0 else (224, 186, 182, 52)
        pts = []
        for px in range(x0 + 6, x1 - 6, 6):
            py = base_y + 9 * math.sin((px - x0) / 46.0 + k * 1.35)
            pts.append((px, py))
        od.line(pts, fill=col, width=1)
    for k in range(10):
        base_x = x0 + 14 + k * ((x1 - x0 - 28) / 9.0)
        col = (190, 200, 222, 36) if k % 2 == 0 else (226, 198, 190, 36)
        pts = []
        for py in range(y0 + 8, y1 - 8, 6):
            px = base_x + 7 * math.sin((py - y0) / 52.0 + k * 1.1)
            pts.append((px, py))
        od.line(pts, fill=col, width=1)
    return overlay


def build():
    img = Image.new("RGB", (W, H), COVER)
    d = ImageDraw.Draw(img)
    # cover edge shading
    d.rectangle([0, 0, W - 1, H - 1], outline=COVER_EDGE, width=3)

    LX, RX = 14, 519           # page left edges
    PT, PB = 14, 710           # page top / bottom
    LW, RW = 491, 491          # page widths

    # pages
    d.rectangle([LX, PT, LX + LW, PB], fill=VISAPAGE)
    d.rectangle([RX, PT, RX + RW, PB], fill=CREAM)
    # centre seam shadow
    seam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seam)
    for i in range(16):
        a = int(70 * (1 - i / 16.0))
        sd.line([505 + i, PT, 505 + i, PB], fill=(40, 30, 30, a))
        sd.line([518 - i, PT, 518 - i, PB], fill=(40, 30, 30, a // 2))
    img = Image.alpha_composite(img.convert("RGBA"), seam)
    d = ImageDraw.Draw(img)

    # ================= LEFT PAGE: visas =================
    d.text((LX + 26, PT + 24), "VISAS · VIISUMIT",
           font=f(SERIF, 21), fill=NAVY)
    d.line([LX + 26, PT + 58, LX + LW - 26, PT + 58], fill=NAVY, width=2)
    # faint grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for gx in range(LX + 24, LX + LW - 10, 28):
        gd.line([gx, PT + 74, gx, PB - 16], fill=(196, 206, 214, 90), width=1)
    for gy in range(PT + 88, PB - 10, 28):
        gd.line([LX + 12, gy, LX + LW - 12, gy], fill=(196, 206, 214, 90), width=1)
    img = Image.alpha_composite(img, grid)
    d = ImageDraw.Draw(img)

    lay, ang = stamp_round(150, 235, 60, -6,
                           ["ALDERVIK INTL", "DEPARTURE", "12 MAY 2023"])
    paste_rotated(img, lay, 128, 232, ang)
    lay, ang = stamp_rect(196, 108, 4, BURG_INK,
                          ["KHAROVIA", "BRANIK BORDER", "ARRIVAL", "12 MAY 2023"],
                          [("KHAROVIA", 16), ("BRANIK BORDER", 11),
                           ("ARRIVAL", 11), ("12 MAY 2023", 15)])
    paste_rotated(img, lay, 348, 222, ang)
    lay, ang = stamp_oval(204, 118, -3,
                          ["OSTREM", "PORT SABLE", "ARRIVAL", "28 NOV 2023"])
    paste_rotated(img, lay, 140, 428, ang)
    lay, ang = stamp_rect(186, 104, 7, BURG_INK,
                          ["OSTREM", "PORT SABLE", "DEPARTURE", "03 DEC 2023"],
                          [("OSTREM", 16), ("PORT SABLE", 11),
                           ("DEPARTURE", 11), ("03 DEC 2023", 15)])
    paste_rotated(img, lay, 356, 436, ang)
    lay, ang = stamp_rect(258, 62, -2, GREEN_INK,
                          ["HIGH PASS", "WINTER CROSSING PERMITTED"],
                          [("HIGH PASS", 16), ("WINTER CROSSING PERMITTED", 11)])
    paste_rotated(img, lay, 258, 596, ang)
    d = ImageDraw.Draw(img)

    # ================= RIGHT PAGE: data page =================
    img.alpha_composite(guilloche(d, RX, PT, RX + RW, PB))
    d = ImageDraw.Draw(img)

    # header
    draw_emblem(d, RX + 62, PT + 62, 30)
    d.text((RX + 108, PT + 34), "REPUBLIC OF VESSIA",
           font=f(SERIF, 28), fill=NAVY)
    sub = "P A S S P O R T   ·   P A S S I"
    d.text((RX + 109, PT + 72), sub, font=f(SANS, 15), fill=LABEL)
    d.line([RX + 24, PT + 112, RX + RW - 24, PT + 112], fill=NAVY, width=2)
    d.line([RX + 24, PT + 116, RX + RW - 24, PT + 116], fill=NAVY, width=1)

    # portrait + signature
    PX, PY, PW, PH = RX + 28, PT + 138, 150, 210
    draw_portrait(img, PX, PY, PW, PH)
    d = ImageDraw.Draw(img)
    draw_signature(d, PX + 8, PY + PH + 14)

    # fields right of the portrait
    FX = RX + 198
    FW = RX + RW - 24 - FX
    v17 = f(SANSB, 17)
    field(d, FX, 152, 92, "TYPE", "P", v17, rule=False)
    field(d, FX + 108, 152, 92, "CODE", "VES", v17, rule=False)
    d.line([FX, 194, FX + FW, 194], fill=RULE, width=1)
    field(d, FX, 206, FW, "PASSPORT No · PASSIN NRO", "V48291063", v17)
    field(d, FX, 258, FW, "SURNAME / SUKUNIMI", "ILVES", v17)
    field(d, FX, 310, FW, "GIVEN NAMES / ETUNIMET", "MARA", v17)
    field(d, FX, 362, FW, "NATIONALITY / KANSALAISUUS", "VESSIAN", v17)

    # fields below the portrait, two columns
    AX, AW = RX + 28, 212
    BX, BW = RX + 262, 201
    field(d, AX, 440, AW, "DATE OF BIRTH / SYNTYMÄPÄIVÄ", "14 MAR 1991", v17)
    field(d, BX, 440, BW, "SEX", "F", v17)
    field(d, AX, 492, AW, "PLACE OF BIRTH / SYNTYMÄPAIKKA", "ALDERVIK", v17)
    field(d, BX, 492, BW, "DATE OF ISSUE / ANTOPÄIVÄ", "02 JUN 2022", v17)
    field(d, AX, 544, AW, "DATE OF EXPIRY / VOIMASSA ASTI", "02 JUN 2032", v17)
    field(d, BX, 544, BW, "AUTHORITY / VIRANOMAINEN",
          "ALDERVIK PASSPORT OFFICE", f(SANSB, 12))

    # MRZ band
    d.rectangle([RX, 614, RX + RW, PB], fill=(233, 227, 206))
    d.line([RX, 614, RX + RW, 614], fill=RULE, width=1)
    line1 = "P<VESILVES<<MARA"
    line1 = line1 + "<" * (44 - len(line1))
    line2 = "V482910631VES9103145F3206026"
    line2 = line2 + "<" * (44 - len(line2) - 2) + "04"
    assert len(line1) == 44 and len(line2) == 44
    mrz = f(MONO, 16)
    for i, line in enumerate((line1, line2)):
        tw = text_w(d, line, mrz)
        d.text((RX + (RW - tw) / 2, 632 + i * 34), line, font=mrz, fill=INK)

    img.convert("RGB").save(OUT, optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
