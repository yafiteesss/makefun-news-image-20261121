#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news image (1024x1024 PNG).

Fresh build for make.fun news-image-20261121. Run:
    python3 build_image.py            # writes entry.png next to this file
Everything is drawn with Pillow primitives; no network, no photos.
"""
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 33, 61)
NAVY = (20, 33, 61)
SCARLET = (193, 39, 45)
GOLD = (197, 148, 52)
CARD = (255, 255, 255)
MUTED = (92, 96, 110)
TEAL = (15, 118, 110)
RUST = (178, 84, 32)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

F_TITLE = font("DejaVuSans-Bold.ttf", 54)
F_TITLE2 = font("DejaVuSans-Bold.ttf", 34)
F_DATE_BIG = font("DejaVuSans-Bold.ttf", 28)
F_DATE_SM = font("DejaVuSans-Bold.ttf", 20)
F_KICK = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_HEAD_SM = font("DejaVuSans-Bold.ttf", 24)
F_BODY = font("DejaVuSans.ttf", 21)
F_BODY_SM = font("DejaVuSans.ttf", 19)
F_NUM = font("DejaVuSans-Bold.ttf", 84)
F_FOOT = font("DejaVuSans.ttf", 17)

def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width; returns list of lines."""
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    out.append(line)
                line = word
        if line:
            out.append(line)
    return out

def para(draw, xy, text, fnt, width, fill, leading=28):
    x, y = xy
    for ln in wrap(draw, text, fnt, width):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def card(draw, box, accent):
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=(205, 198, 182), width=2)
    draw.rectangle([box[0], box[1], box[0] + 8, box[3]], fill=accent)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead -------------------------------------------------------------
d.rectangle([0, 0, W, 132], fill=NAVY)
d.rectangle([0, 132, W, 138], fill=GOLD)
d.text((28, 22), "THE WORLD", font=F_TITLE, fill=(255, 255, 255))
d.text((28, 82), "IN ONE IMAGE", font=F_TITLE2, fill=GOLD)
d.rectangle([648, 18, 996, 114], outline=GOLD, width=2)
d.text((672, 28), "SATURDAY", font=F_DATE_SM, fill=GOLD)
d.text((672, 58), "21 NOVEMBER 2026", font=F_DATE_BIG, fill=(255, 255, 255))

# ---- lead story: Peru quake ----------------------------------------------
LX, LY, RX, RY = 16, 154, 1008, 404
card(d, (LX, LY, RX, RY), SCARLET)
d.text((44, 172), "LEAD  ·  LATIN AMERICA", font=F_KICK, fill=SCARLET)
d.text((44, 200), "PERU SHAKEN BY", font=F_TITLE, fill=INK)
d.text((44, 258), "A 6.8 QUAKE", font=F_TITLE, fill=INK)
para(d, (44, 326), "A magnitude 6.8 earthquake struck the\nJunín region of central Peru; tremors\nwere felt 320 km away in Lima.",
     F_BODY, 500, INK, leading=26)
# seismograph panel, right side: big number top-left, trace below it
d.rectangle([600, 172, 980, 388], outline=(205, 198, 182), width=2, fill=(250, 247, 240))
d.text((622, 182), "M 6.8", font=F_NUM, fill=SCARLET)
d.text((622, 276), "Junín, Peru", font=F_BODY_SM, fill=MUTED)
pts = []
x = 612
while x < 972:
    t = (x - 612) / 360.0
    amp = 5 + 26 * math.exp(-((t - 0.45) ** 2) / 0.02) * abs(math.sin(t * 40))
    y = 340 + (amp if int(t * 90) % 2 == 0 else -amp) * (1 if (int(t * 90) % 4) < 2 else -1)
    pts.append((x, max(306, min(376, y))))
    x += 6
d.line([612, 340, 972, 340], fill=(205, 198, 182), width=1)
d.line(pts, fill=SCARLET, width=3, joint="curve")

# ---- story grid: 3 columns x 2 rows ---------------------------------------
GX = [16, 352, 688]
GY = [420, 704]
GW, GH = 320, 268

stories = [
    ("CLIMATE  ·  TURKEY", "COP31 DRAGS INTO OVERTIME",
     "Fossil-fuel talks deadlock in Turkey as the climate summit runs past its close.",
     TEAL, "sun"),
    ("MIDDLE EAST", "IRAN SEEKS A WAY OUT",
     "Tehran says it wants diplomacy to end the war; Trump calls the terms unacceptable.",
     NAVY, "dove"),
    ("WAR IN UKRAINE", "STRIKE HITS KRYVYI RIH",
     "A Russian strike kills two and injures 42, among them four children.",
     SCARLET, "burst"),
    ("UNITED STATES", "RIKERS TO CLOSE BY 2032",
     "New York mayor Mamdani unveils a plan to shut the Rikers Island jail complex.",
     RUST, "bars"),
    ("SPORT  ·  CRICKET", "RAHUL COMPLETES THE SET",
     "KL Rahul's Wellington hundred makes him the first Indian opener with Test tons in all four SENA nations.",
     TEAL, "bat"),
]

def pictogram(cx, cy, kind, color):
    """Small glyph drawn top-right of a story card (fits a ~64px box)."""
    if kind == "sun":
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], outline=color, width=4)
        for a in range(0, 360, 45):
            x1 = cx + 21 * math.cos(math.radians(a)); y1 = cy + 21 * math.sin(math.radians(a))
            x2 = cx + 29 * math.cos(math.radians(a)); y2 = cy + 29 * math.sin(math.radians(a))
            d.line([x1, y1, x2, y2], fill=color, width=3)
    elif kind == "dove":
        d.ellipse([cx - 19, cy - 8, cx + 6, cy + 9], fill=color)
        d.polygon([(cx - 5, cy - 5), (cx + 22, cy - 17), (cx + 19, cy - 1)], fill=color)
        d.polygon([(cx - 18, cy + 1), (cx + 4, cy + 14), (cx + 8, cy + 1)], fill=color)
    elif kind == "burst":
        for a in range(0, 360, 30):
            x1 = cx + 5 * math.cos(math.radians(a)); y1 = cy + 5 * math.sin(math.radians(a))
            x2 = cx + 22 * math.cos(math.radians(a)); y2 = cy + 22 * math.sin(math.radians(a))
            d.line([x1, y1, x2, y2], fill=color, width=3)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)
    elif kind == "bars":
        for i in range(5):
            x = cx - 20 + i * 10
            d.line([x, cy - 19, x, cy + 19], fill=color, width=3)
        d.line([cx - 24, cy - 19, cx + 24, cy - 19], fill=color, width=3)
        d.line([cx - 24, cy + 19, cx + 24, cy + 19], fill=color, width=3)
    elif kind == "bat":
        d.line([cx - 19, cy + 18, cx + 11, cy - 14], fill=color, width=6)
        d.ellipse([cx + 8, cy - 22, cx + 26, cy - 4], outline=color, width=3)

for i, (kicker, head, body, color, icon) in enumerate(stories):
    col, row = i % 3, i // 3
    x0, y0 = GX[col], GY[row]
    card(d, (x0, y0, x0 + GW, y0 + GH), color)
    d.rectangle([x0, y0, x0 + GW, y0 + 6], fill=color)
    pictogram(x0 + GW - 40, y0 + 34, icon, color)
    d.text((x0 + 22, y0 + 18), kicker, font=F_KICK, fill=color)
    para(d, (x0 + 22, y0 + 66), head, F_HEAD_SM, GW - 44, INK, leading=29)
    para(d, (x0 + 22, y0 + 138), body, F_BODY_SM, GW - 44, MUTED, leading=25)

# ---- in-brief card (bottom right) -----------------------------------------
x0, y0 = GX[2], GY[1]
card(d, (x0, y0, x0 + GW, y0 + GH), GOLD)
d.rectangle([x0, y0, x0 + GW, y0 + 6], fill=GOLD)
d.text((x0 + 22, y0 + 18), "IN BRIEF", font=F_KICK, fill=GOLD)
briefs = [
    ("ICJ RULES ON ROHINGYA", "Myanmar found guilty of genocide against the Rohingya."),
    ("INDIA INFLOWS RECORD", "Record ₹1.22 lakh crore flows into Indian shares."),
    ("CYCLONE AKVAN LANDFALL", "Storm crosses the Odisha coast with heavy rain."),
]
yy = y0 + 46
F_BRIEF_H = font("DejaVuSans-Bold.ttf", 18)
F_BRIEF_B = font("DejaVuSans.ttf", 18)
for h, b in briefs:
    d.text((x0 + 22, yy), "▸ " + h, font=F_BRIEF_H, fill=INK)
    yy += 22
    yy = para(d, (x0 + 38, yy), b, F_BRIEF_B, GW - 60, MUTED, leading=20) + 6

# ---- footer ----------------------------------------------------------------
d.text((16, 986), "Compiled from reports published 21 November 2026  ·  NYT · Reuters · Al Jazeera · BBC",
       font=F_FOOT, fill=MUTED)

img.save("entry.png", optimize=True)
print("wrote entry.png")
