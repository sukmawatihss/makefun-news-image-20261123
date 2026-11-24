#!/usr/bin/env python3
"""THE WORLD IN A DAY - NI23 G3 entry composer for akun15 (@sukmawatihss).

Draws a straight newspaper front page for Monday 23 November 2026:
giant Playfair masthead, a strip of the day's numbers, 14 large illustrated
cards (lead: ICJ rules Myanmar guilty of genocide), a dotted_map world map
with numbered pins, a UTC timeline, an ALSO ON run reaching 45 stories, a
red DATE CHECK box of rejected older items, and the verification footer.
All facts and figures come only from the locked NI23 pool.
Usage: python3 compose.py [A|B|C] [out.png]
"""

import math
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width

def F(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

def fb(size):  # headline font (Playfair Bold)
    return ImageFont.truetype(FONT_DIR + "PlayfairDisplay-Bold.ttf", size)

def fr(size):  # deck / fact font (Archivo)
    return ImageFont.truetype(FONT_DIR + "Archivo.ttf", size)

def fsr(size):  # brief font (Archivo)
    return ImageFont.truetype(FONT_DIR + "Archivo.ttf", size)

PF_BLACK = "PlayfairDisplay-Black.ttf"
AR_B = "Archivo-Bold.ttf"

PALETTES = {
    "A": dict(bg=(246, 238, 220), ink=(18, 18, 16), accent=(10, 110, 70),
              soft=(234, 224, 198), strip_bg=(10, 110, 70), strip_fg=(246, 238, 220),
              chip_fg=(246, 238, 220), mast=(18, 18, 16)),
    "B": dict(bg=(251, 248, 241), ink=(20, 20, 18), accent=(8, 96, 62),
              soft=(238, 234, 222), strip_bg=(20, 20, 18), strip_fg=(251, 248, 241),
              chip_fg=(251, 248, 241), mast=(8, 96, 62)),
    "C": dict(bg=(240, 226, 196), ink=(22, 18, 12), accent=(12, 104, 64),
              soft=(229, 211, 174), strip_bg=(22, 18, 12), strip_fg=(240, 226, 196),
              chip_fg=(240, 226, 196), mast=(22, 18, 12)),
}

REGION_COLORS = {
    "SE ASIA": (10, 110, 70), "S ASIA": (146, 96, 16), "EUROPE": (30, 84, 150),
    "MIDEAST": (168, 44, 44), "N AMERICA": (96, 52, 140), "GLOBAL": (70, 70, 70),
    "AFRICA": (176, 110, 20), "ASIA-PAC": (0, 128, 128),
}

NUMS = [
    ("258-173", "US House final count"),
    ("720/9d", "India at Wellington"),
    ("700,000+", "Rohingya fled Myanmar"),
    ("$3,538", "gold, per ounce"),
    ("7 + 50", "found / missing, Indonesia"),
    ("65.9%", "IndiGo domestic share"),
]

TL = [
    ("00:02Z", "UN lethal-AI talks"),
    ("02:00Z", "Albanese on COP31"),
    ("06:00Z", "Kyiv boy found alive"),
    ("12:00Z", "ICJ ruling reported"),
    ("18:00Z", "House settles 258-173"),
]

BRIEFS = [
    "2. IRGC claims 2 Patriot radars hit in Bahrain",
    "3. Houthi missile intercepted over Saudi west",
    "4. Swimmer crosses Hormuz for Iran's wildlife",
    "6. US declassifies more UFO footage",
    "8. Albanese: COP31 failure shows 'hard geopolitics'",
    "10. Russia-bound ship towed after Finland attack",
    "11. Blast hits Russian ship in Benghazi port",
    "13. Zelenskiy says 14 missing after Kyiv strike",
    "14. UK-EU reset deal called a 'landmark'",
    "16. Myanmar junta calls ASEAN ruling 'unfair'",
    "17. Cameroon ex-rebels trapped by broken promises",
    "18. Escaped lion frightens residents in Turkiye",
    "19. Nepal PM Shah holds talks with Modi",
    "20. India, Bulgaria discuss IMEC, Black Sea",
    "21. Guru Nanak Jayanti marked across India",
    "22. UP runs air-raid drills in 75 districts",
    "26. Day 5: India chase famous win, NZ 119/2",
    "27. India win ODI series in NZ 3-2",
    "28. Anupama defends IBSF snooker crown",
    "29. World Chess Championship draws crowds",
    "30. Rajya Sabha MP Wadkute dies in Delhi",
    "31. Kota pilgrim bus tragedy: 9 dead",
    "32. Tata Steel sells pipe arm, Rs28,000 cr",
    "35. IFFI 2026 hosts BRICS roundtable in Goa",
    "36. Modi opens AI Centre at IIT Patna",
    "37. Shah: Rs4,000 cr Arunachal infra push",
    "38. CJI: AI rules a must in legal study",
    "39. JEE Main 2027 registration closes today",
    "40. NEET PG 2026: 10,105 seats flagged",
    "41. Google: $5m into IIT Kharagpur AI",
    "B5. Mets sign A.J. Ewing: $95m, 8 years",
]

dc = ("Xi-Trump-Putin summit, 19 Nov 2026 · SpiceJet Rs5,500 crore fundraise, 18 Nov 2026 · "
      "Paolo Bulgari death, reported 22 Nov 2026 · Bolsonaro stable in ICU, Brasilia 22 Nov 2026 · "
      "24 civilians killed in South Sudan, Juba 22 Nov 2026 · "
      "Indonesia candy-factory fire AS EVENT, 22 Nov 2026")

MAP_ROWS = [
    "..........XXXXXX..............................................",
    "......XXXXXXXXXXXXXXXX..........XXXX....XXXXXXXXXXXXXXXXXX....",
    "....XXXXXXXXXXXXXXXXXX.......XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...",
    ".....XXXXXXXXXXXXXXXX.....XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX....",
    "......XXXXXXXXXXXXXX.......XXXXXXXXXXXXXXXXXXXXXXXXXXXX.......",
    ".......XXXXXXXXXX...........XXXXXXXXXXXXXXXXXXXXXX............",
    "........XXXXXXXX.............XXXXXXXXXXXXXXXXX.......XX.......",
    ".........XXXXXX....X..........XXXXXXXXXXXXXX.........XXXX.....",
    "..........XXXX....XXX..........XXXXXXXXXXXX..........XXXXXX...",
    "..........XXX......XXX..........XXXXXXXXX.............XXXX....",
    "..........XX........XX...........XXXXXXX......................",
    "..........XX......................XXXXX.......................",
    "..........XX.......................XXX..........XX............",
    "..........XX.......................XX..........XXXX...........",
    ".........XXX....................................XX............",
    ".........XX...................................................",
    ".........X....................................................",
    "..............................................................",
]
PINS = {24: (47, 8), 43: (9, 3), 25: (58, 13), 1: (38, 6), 12: (33, 2),
        7: (35, 4), 45: (8, 4), 23: (50, 10), 33: (44, 7), 9: (34, 1),
        15: (28, 5), 47: (5, 5), 5: (29, 3), 34: (31, 2)}

MAP_LEGEND = "Dots mark land, pins numbered"


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def trunc(d, text, font, maxw):
    if d.textlength(text, font=font) <= maxw:
        return text
    s = text
    while d.textlength(s + "..", font=font) > maxw and " " in s:
        s = s.rsplit(" ", 1)[0]
    return s + ".."


def draw_icon(d, kind, x, y, s, col):
    """Tiny original line drawings, one per card, PIL primitives only."""
    if kind == "courthouse":
        d.polygon([(x, y + 6), (x + s, y + 6), (x + s // 2, y - 4)], outline=col, width=2)
        for i in range(4):
            cx = x + 4 + i * (s - 8) // 3
            d.line([(cx, y + 10), (cx, y + s - 6)], fill=col, width=2)
        d.line([(x, y + s - 3), (x + s, y + s - 3)], fill=col, width=3)
    elif kind == "flag":
        d.line([(x + 2, y), (x + 2, y + s)], fill=col, width=2)
        d.polygon([(x + 2, y), (x + s, y + 5), (x + 2, y + 11)], fill=col)
    elif kind == "cricket":
        d.polygon([(x + 6, y + s), (x + 14, y + 8), (x + s - 4, y + 14), (x + s - 12, y + s)], fill=col)
        d.ellipse([x + s - 12, y, x + s - 2, y + 10], outline=col, width=2)
    elif kind == "tanker":
        d.polygon([(x, y + s - 8), (x + s, y + s - 8), (x + s - 8, y + s), (x + 6, y + s)], outline=col, width=2)
        d.polygon([(x + s // 2, y), (x + s // 2 + 7, y + 12), (x + s // 2 - 7, y + 12)], fill=(196, 60, 30))
    elif kind == "rubble":
        d.polygon([(x, y + 12), (x + s // 2, y), (x + s, y + 12)], outline=col, width=2)
        d.line([(x + 4, y + s), (x + 14, y + 16), (x + 24, y + s), (x + s - 2, y + 18)], fill=col, width=2)
    elif kind == "globe":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=col, width=2)
        d.arc([x + 2, y + 2, x + s - 2, y + s - 2], 200, 320, fill=col, width=2)
    elif kind == "goldbars":
        d.polygon([(x + s // 2 - 6, y + 4), (x + s // 2 + 6, y + 4), (x + s // 2 + 10, y + 13), (x + s // 2 - 10, y + 13)], outline=col, width=2)
        d.polygon([(x + 2, y + 16), (x + 14, y + 16), (x + 17, y + 25), (x - 1, y + 25)], outline=col, width=2)
        d.polygon([(x + s - 14, y + 16), (x + s - 2, y + 16), (x + s + 1, y + 25), (x + s - 17, y + 25)], outline=col, width=2)
    elif kind == "explosion":
        cx, cy = x + s // 2, y + s // 2
        pts = []
        for i in range(16):
            r = s // 2 if i % 2 == 0 else s // 5
            a = math.pi * i / 8
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, outline=(196, 60, 30), width=2)
    elif kind == "factory":
        d.rectangle([x, y + 12, x + s - 10, y + s], outline=col, width=2)
        d.polygon([(x + s - 10, y + 12), (x + s - 2, y + 4), (x + s - 2, y + s), (x + s - 10, y + s)], outline=col, width=2)
        d.polygon([(x + 6, y + 2), (x + 11, y + 10), (x + 1, y + 10)], fill=(196, 60, 30))
    elif kind == "plane":
        d.polygon([(x, y + s - 8), (x + s, y + 6), (x + s - 6, y + s - 4), (x + s // 2, y + s - 10)], outline=col, width=2)
    elif kind == "ship":
        d.polygon([(x, y + s - 10), (x + s, y + s - 10), (x + s - 8, y + s - 1), (x + 6, y + s - 1)], outline=col, width=2)
        d.rectangle([x + 10, y + 8, x + 22, y + s - 10], outline=col, width=2)
        d.polygon([(x + 24, y), (x + 30, y + 9), (x + 18, y + 9)], fill=(196, 60, 30))
    elif kind == "crowd":
        for i, cx in enumerate((x + 6, x + s // 2, x + s - 6)):
            cy = y + 8 + (i % 2) * 3
            d.ellipse([cx - 3, cy - 6, cx + 3, cy], outline=col, width=2)
            d.line([(cx, cy), (cx, cy + 12)], fill=col, width=2)
    elif kind == "robot":
        d.rectangle([x + 5, y + 8, x + s - 5, y + s - 4], outline=col, width=2)
        d.line([(x + s // 2, y + 8), (x + s // 2, y + 1)], fill=col, width=2)
        d.ellipse([x + s // 2 - 2, y - 1, x + s // 2 + 2, y + 3], fill=col)
        d.ellipse([x + 11, y + 15, x + 15, y + 19], fill=col)
        d.ellipse([x + s - 15, y + 15, x + s - 11, y + 19], fill=col)
    elif kind == "ring":
        d.ellipse([x + 7, y + 10, x + s - 7, y + s - 2], outline=col, width=3)
        d.polygon([(x + s // 2 - 5, y + 10), (x + s // 2, y + 1), (x + s // 2 + 5, y + 10)], outline=col, width=2)
    else:
        d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=col, width=2)


def _header(d, pal, x, y, w, num, region, src, big=False):
    acc = pal["accent"]
    d.text((x + 8, y + 7), "#%s" % num, font=F(AR_B, 15 if big else 13), fill=acc)
    chip_f = F(AR_B, 11)
    tw = d.textlength(region, font=chip_f)
    col = REGION_COLORS.get(region, acc)
    d.rectangle([x + w - tw - 18, y + 6, x + w - 8, y + 23], fill=col)
    d.text((x + w - tw - 13, y + 8), region, font=chip_f, fill=pal["chip_fg"])
    sx = x + (58 if big else 40)
    maxsrc = (x + w - tw - 26) - sx
    d.text((sx, y + 9), trunc(d, "SRC: " + src.upper(), F(AR_B, 10), maxsrc),
           font=F(AR_B, 10), fill=pal["ink"])


def lead(d, x, y, w, h, num, region, src, head, deck, kind, pal):
    ink, acc = pal["ink"], pal["accent"]
    d.rectangle([x, y, x + w, y + h], fill=pal["soft"], outline=ink, width=2)
    d.rectangle([x, y, x + w, y + 3], fill=acc)
    _header(d, pal, x, y, w, num, region, src, big=True)
    draw_icon(d, kind, x + w - 42, y + 28, 28, ink)
    tf = fb(30)
    ty = y + 26
    for ln in wrap(d, head, tf, w - 60)[:2]:
        d.text((x + 9, ty), ln, font=tf, fill=ink)
        ty += 34
    ff = fr(16)
    fy = ty + 3
    for ln in wrap(d, deck, ff, w - 18)[:3]:
        d.text((x + 9, fy), ln, font=ff, fill=ink)
        fy += 20
    deck_line = "A verdict on the 2017 campaign, delivered in a single day."
    d.text((x + 9, y + h - 40), deck_line,
           font=ImageFont.truetype(FONT_DIR + "PlayfairDisplay-Italic.ttf", 16), fill=ink)
    draw_icon(d, kind, x + w - 66, y + h - 54, 44, acc)


def mini(d, x, y, w, h, num, region, src, head, deck, kind, pal):
    ink, acc = pal["ink"], pal["accent"]
    d.rectangle([x, y, x + w, y + h], fill=pal["bg"], outline=ink, width=1)
    d.rectangle([x, y, x + w, y + 3], fill=acc)
    _header(d, pal, x, y, w, num, region, src)
    draw_icon(d, kind, x + w - 42, y + 28, 28, ink)
    tf = fb(24)
    ty = y + 26
    for ln in wrap(d, head, tf, w - 60)[:2]:
        d.text((x + 9, ty), ln, font=tf, fill=ink)
        ty += 26
    ff = fr(14)
    fy = ty + 3
    for ln in wrap(d, deck, ff, w - 18)[:2]:
        d.text((x + 9, fy), ln, font=ff, fill=ink)
        fy += 16


def draw_dotted_map(d, pal, mx, my, mw, mh):
    ink, acc = pal["ink"], pal["accent"]
    d.rectangle([mx, my, mx + mw, my + mh], fill=pal["bg"], outline=ink, width=1)
    d.rectangle([mx, my, mx + mw, my + 3], fill=acc)
    d.text((mx + 7, my + 6), "THE DAY ON THE MAP", font=F(AR_B, 11), fill=acc)
    cell = 3
    ox, oy = mx + 8, my + 24
    for ri, row in enumerate(MAP_ROWS):
        for ci, ch in enumerate(row):
            if ch == "X":
                d.ellipse([ox + ci * cell, oy + ri * 4, ox + ci * cell + 2, oy + ri * 4 + 2], fill=(150, 138, 110))
    pf = F(AR_B, 9)
    for num, (ci, ri) in PINS.items():
        px, py = ox + ci * cell, oy + ri * 4
        d.ellipse([px - 6, py - 6, px + 7, py + 7], fill=acc)
        t = str(num)
        d.text((px - d.textlength(t, font=pf) / 2, py - 4), t, font=pf, fill=pal["chip_fg"])
    d.text((mx + 7, my + mh - 14), MAP_LEGEND, font=fr(10), fill=ink)


def build(variant):
    pal = PALETTES[variant]
    img = Image.new("RGB", (W, H), pal["bg"])
    d = ImageDraw.Draw(img)
    ink, acc = pal["ink"], pal["accent"]

    # kicker
    kf = F(AR_B, 15)
    kick = "45 STORIES - 7 REGIONS - EVERY ONE FROM 23 NOVEMBER 2026"
    d.text(((W - d.textlength(kick, font=kf)) / 2, 8), kick, font=kf, fill=acc)
    d.line([(MARGIN, 30), (W - MARGIN, 30)], fill=ink, width=2)

    # masthead (PlayfairDisplay-Black)
    mf = ImageFont.truetype(FONT_DIR + "PlayfairDisplay-Black.ttf", 72)
    name = "THE WORLD IN A DAY"
    while d.textlength(name, font=mf) > CW and mf.size > 64:
        mf = ImageFont.truetype(FONT_DIR + "PlayfairDisplay-Black.ttf", mf.size - 2)
    d.text(((W - d.textlength(name, font=mf)) / 2, 30), name, font=mf, fill=pal["mast"])
    df = fb(30)
    date = "Monday 23 November 2026"
    d.text(((W - d.textlength(date, font=df)) / 2, 106), date, font=df, fill=ink)
    sf2 = fr(11)
    side = "FINAL EDITION - No. 23"
    d.text((MARGIN, 112), side, font=sf2, fill=ink)
    d.text((W - MARGIN - d.textlength(side, font=sf2), 112), side, font=sf2, fill=ink)
    d.line([(MARGIN, 142), (W - MARGIN, 142)], fill=ink, width=3)

    # number strip (148-184)
    d.rectangle([MARGIN, 148, W - MARGIN, 184], fill=pal["strip_bg"])
    nf, lf = F(AR_B, 22), fr(10)
    seg = CW // 6
    for i, (n, lab) in enumerate(NUMS):
        cx = MARGIN + i * seg
        d.text((cx + (seg - d.textlength(n, font=nf)) / 2, 150), n, font=nf, fill=pal["strip_fg"])
        d.text((cx + (seg - d.textlength(lab, font=lf)) / 2, 172), lab, font=lf, fill=pal["strip_fg"])
        if i:
            d.line([(cx, 152), (cx, 180)], fill=pal["strip_fg"], width=1)

    # zone A: lead + trio stack (192-412)
    lead(d, MARGIN, 192, 552, 220, 24, "SE ASIA", "ICJ ruling - Guardian/NYT wires",
         "ICJ Finds Myanmar Guilty of Genocide",
         "The ICJ rules Myanmar guilty of genocide over the 2017 campaign against the Rohingya; more than 700,000 people fled their homes.",
         "courthouse", pal)
    mini(d, 596, 192, 400, 106, 43, "N AMERICA", "BBC 23 Nov",
         "Democrats Take the House 258-173",
         "Largest majority since 1992 after the NC flip.", "flag", pal)
    mini(d, 596, 306, 400, 106, 25, "S ASIA", "ObserverVoice 23 Nov",
         "India Post Record 720/9 at Wellington",
         "Highest Test total ever made in New Zealand.", "cricket", pal)
    # zones B and C: 4 across (420-538, 546-664)
    mini(d, MARGIN, 420, 237, 118, 1, "MIDEAST", "AP live",
         "Tankers Burn in Hormuz Strait",
         "Tankers ablaze as the Iran-US war widens into the Gulf.", "tanker", pal)
    mini(d, MARGIN + 245, 420, 237, 118, 12, "EUROPE", "BBC",
         "Kyiv Boy Pulled From Rubble",
         "Boy, 7, pulled out alive after hours in debris; 6 dead.", "rubble", pal)
    mini(d, MARGIN + 490, 420, 237, 118, 7, "EUROPE", "BBC/AP",
         "COP31 Ends, No Deal",
         "COP31 summit in Turkiye closes with no deal agreed.", "globe", pal)
    mini(d, MARGIN + 735, 420, 237, 118, 34, "GLOBAL", "ObserverVoice",
         "Gold Falls to $3,538/oz",
         "Down over $2,000 from the 2026 record $5,595; -2.41% Friday.", "goldbars", pal)
    mini(d, MARGIN, 546, 237, 118, 45, "N AMERICA", "BBC",
         "Army to Detonate Iowa Explosives",
         "US Army will detonate explosives in Iowa despite court order.", "explosion", pal)
    mini(d, MARGIN + 245, 546, 237, 118, 23, "SE ASIA", "JagranJosh",
         "Indonesia: 7 Found, 50 Missing",
         "23 Nov update: 7 body bags recovered, 50 still missing.", "factory", pal)
    mini(d, MARGIN + 490, 546, 237, 118, 33, "S ASIA", "ObserverVoice",
         "IndiGo at 65.9% of India's Skies",
         "SpiceJet pilots seek urgent audit; IndiGo at 65.9%.", "plane", pal)
    mini(d, MARGIN + 735, 546, 237, 118, 9, "EUROPE", "BBC/JagranJosh",
         "Russian Ship Burns Off Finland",
         "Ship still burning off Finland after Gulf of Finland attack.", "ship", pal)
    # zone D: 3 cards + map panel (672-790)
    mini(d, MARGIN, 672, 237, 118, 15, "EUROPE", "JagranJosh",
         "Lisbon Marches on Living Costs",
         "Thousands march through Lisbon over Portugal living costs.", "crowd", pal)
    mini(d, MARGIN + 245, 672, 237, 118, 5, "GLOBAL", "Salonvision",
         "UN Keeps Talking on Killer AI",
         "Nations agree: UN talks on lethal AI weapons go on.", "robot", pal)
    mini(d, MARGIN + 490, 672, 237, 118, 47, "N AMERICA", "BBC",
         "Miley Cyrus Weds Morando",
         "Singer marries Maxx Morando in a California ceremony.", "ring", pal)
    draw_dotted_map(d, pal, MARGIN + 735, 672, 233, 118)

    # timeline (798-820)
    ty = 798
    d.line([(MARGIN, ty), (W - MARGIN, ty)], fill=ink, width=1)
    tf2, bf = F(AR_B, 12), fr(12)
    x = MARGIN
    d.text((x, ty + 6), "UTC DAY:", font=F(AR_B, 13), fill=acc)
    x += 74
    for t, ev in TL:
        s1 = t + " "
        d.text((x, ty + 6), s1, font=tf2, fill=ink)
        x += d.textlength(s1, font=tf2)
        s2 = ev + "   |   "
        d.text((x, ty + 6), s2, font=bf, fill=ink)
        x += d.textlength(s2, font=bf)

    # ALSO ON (826-950)
    ay = 826
    d.text((MARGIN, ay), "ALSO ON THE FRONT PAGE - STORIES 15 TO 45", font=F(AR_B, 14), fill=acc)
    af = fsr(13)
    colw = CW // 4
    per = 8
    for i, s0 in enumerate(BRIEFS):
        cx = MARGIN + (i // per) * colw
        cy = ay + 20 + (i % per) * 13
        d.text((cx, cy), trunc(d, s0, af, colw - 8), font=af, fill=ink)

    # DATE CHECK (956-1000)
    dy = 956
    d.rectangle([MARGIN, dy, W - MARGIN, dy + 44], outline=(178, 30, 30), width=2)
    d.text((MARGIN + 8, dy + 3), "DATE CHECK - REJECTED, NOT 23 NOV:", font=F(AR_B, 11), fill=(178, 30, 30))
    rf = fr(11)
    items = [s.strip() for s in dc.split("·")]
    for li, group in enumerate((items[:3], items[3:])):
        x = MARGIN + 8
        y2 = dy + 17 + li * 13
        for item in group:
            s = item + "   |   "
            d.text((x, y2), s, font=rf, fill=(178, 30, 30))
            x += d.textlength(s, font=rf)

    # footer
    ff2 = fr(11)
    foot = "Every story happened, or was first reported, on Monday 23 November 2026. Contested claims are attributed. - Original drawings."
    d.text(((W - d.textlength(foot, font=ff2)) / 2, 1006), foot, font=ff2, fill=ink)
    return img


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g3-akun15/entry.png"
    build(variant).save(out, optimize=True)
    print("saved", out)
