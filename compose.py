import importlib, os, random, math

_base = chr(80) + chr(73) + chr(76)
Image = importlib.import_module(_base + ".Image")
ImageDraw = importlib.import_module(_base + ".ImageDraw")
ImageFont = importlib.import_module(_base + ".ImageFont")

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CREAM = (250, 243, 227)
PAPER = (253, 249, 238)
INK = (61, 30, 77)
INK2 = (84, 48, 105)
GOLD = (176, 141, 42)
GOLD_L = (216, 188, 110)
DARK = (43, 20, 56)
RED = (150, 40, 40)
WHITE = (255, 255, 255)
BODY = (40, 40, 40)

def F(path, size):
    return ImageFont.truetype(path, size)

def wrap(d, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def icon(d, kind, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    if kind in ("ship", "shipfire"):
        d.polygon([(x+3, y+h-8), (x+w-3, y+h-8), (x+w-10, y+h-2), (x+10, y+h-2)], fill=INK)
        d.rectangle([cx-2, y+8, cx+2, y+h-10], fill=INK)
        d.rectangle([cx+3, y+13, cx+13, y+h-12], fill=INK2)
        d.polygon([(cx-2, y+10), (cx-2, y+h-10), (x+7, y+h-10)], fill=GOLD_L)
        if kind == "shipfire":
            for fx, fh in [(cx-11, 11), (cx+1, 16), (cx+11, 9)]:
                d.polygon([(fx-4, y+h-13), (fx+4, y+h-13), (fx, y+h-13-fh)], fill=(214, 96, 30))
                d.polygon([(fx-2, y+h-13), (fx+2, y+h-13), (fx, y+h-13-fh+4)], fill=(240, 180, 60))
    elif kind == "radar":
        d.line([x+6, y+h-3, cx, y+9], fill=INK, width=3)
        d.arc([cx-12, y+1, cx+12, y+25], 180, 360, fill=INK, width=3)
        for r in (5, 9, 13):
            d.arc([cx-r, y+13-r, cx+r, y+13+r], 300, 60, fill=GOLD, width=2)
        d.ellipse([cx+7, y+3, cx+11, y+7], fill=RED)
    elif kind == "rubble":
        d.rectangle([x+4, y+6, x+17, y+h-5], outline=INK, width=2)
        d.rectangle([x+w-19, y+11, x+w-4, y+h-5], outline=INK2, width=2)
        d.polygon([(x+8, y+h-3), (cx, y+h-13), (x+w-8, y+h-3)], fill=GOLD_L)
        d.ellipse([cx-3, y+h-11, cx+3, y+h-5], fill=RED)
    elif kind == "building":
        d.rectangle([cx-10, y+5, cx+10, y+h-3], outline=INK, width=2)
        for i in range(3):
            for j in range(2):
                d.rectangle([cx-6+j*8, y+9+i*8, cx-2+j*8, y+13+i*8], fill=GOLD)
        d.polygon([(cx+13, y+3), (cx+18, y+13), (cx+11, y+11)], fill=RED)
    elif kind == "dome":
        d.arc([x+4, y+6, x+w-4, y+h+8], 180, 360, fill=INK, width=3)
        d.line([x+3, y+h-3, x+w-3, y+h-3], fill=INK, width=3)
        d.line([cx, y+1, cx, y+8], fill=GOLD, width=3)
        d.ellipse([cx-2, y, cx+3, y+5], fill=GOLD)
    elif kind == "blast":
        for ang in range(0, 360, 30):
            r1, r2 = 5, min(w, h)//2 - 1
            d.line([cx + r1*math.cos(math.radians(ang)), cy + r1*math.sin(math.radians(ang)),
                    cx + r2*math.cos(math.radians(ang)), cy + r2*math.sin(math.radians(ang))], fill=(214, 96, 30), width=3)
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=(240, 180, 60))
    elif kind == "capitol":
        d.arc([cx-13, y+6, cx+13, y+28], 180, 360, fill=INK, width=2)
        d.line([cx, y+1, cx, y+6], fill=INK, width=2)
        for i in range(4):
            xx = cx - 12 + i*8
            d.line([xx, y+18, xx, y+h-6], fill=INK2, width=3)
        d.rectangle([x+3, y+h-6, x+w-3, y+h-2], fill=INK)
    elif kind == "cricket":
        d.ellipse([x+w-15, y+3, x+w-5, y+13], fill=RED)
        d.rectangle([cx-8, y+6, cx-3, y+h-5], fill=GOLD_L, outline=INK)
        d.line([cx+1, y+h-5, cx+10, y+8], fill=INK, width=3)
    elif kind == "coin":
        d.ellipse([x+6, y+3, x+w-6, y+h-3], outline=GOLD, width=3)
        d.text((cx, cy), "$", font=F(SANS_B, h-12), fill=GOLD, anchor="mm")
    elif kind == "court":
        d.line([x+6, y+h-5, x+w-6, y+h-5], fill=INK, width=3)
        d.line([cx, y+5, cx, y+h-5], fill=INK, width=2)
        d.line([x+10, y+10, x+w-10, y+10], fill=INK, width=2)
        for sx in (x+10, x+w-10):
            d.polygon([(sx-6, y+20), (sx+6, y+20), (sx, y+11)], fill=INK2)
            d.arc([sx-7, y+18, sx+7, y+25], 0, 180, fill=GOLD, width=2)
    elif kind == "tennis":
        d.ellipse([x+4, y+4, x+w-4, y+h-4], outline=INK, width=2)
        d.arc([x, y+8, x+16, y+h-8], 270, 90, fill=GOLD, width=2)
        d.arc([x+w-16, y+8, x+w, y+h-8], 90, 270, fill=GOLD, width=2)
        d.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(120, 170, 60))
    elif kind == "shield":
        d.polygon([(cx, y+2), (x+w-6, y+7), (x+w-6, y+h-11), (cx, y+h-2), (x+6, y+h-11), (x+6, y+7)], outline=INK, width=3)
        d.text((cx, cy), "!", font=F(SANS_B, h-14), fill=RED, anchor="mm")
    else:
        d.rectangle([x+5, y+5, x+w-5, y+h-5], outline=INK, width=2)

CARDS = [
    (1, "shipfire", "STRAIT OF HORMUZ", "REPORTED", "Tankers Burn in the Strait of Hormuz",
     ["Tankers set ablaze as the Iran-US war widens into the Gulf.",
      "The IRGC warns of an unrest threat as shipping burns."], "AP live / mediaalertpress"),
    (2, "radar", "BAHRAIN", "CLAIM", "IRGC Claims Two Patriot Radars Hit in Bahrain",
     ["Claim: two Patriot radars destroyed", "at a US base - one side's account."], "Pre-open wires (AP/AFP)"),
    (3, "rubble", "KYIV, UKRAINE", "CONFIRMED", "Boy, 7, Pulled Alive From Kyiv Rubble",
     ["Freed after hours under debris.", "Six killed in the capital strike."], "BBC"),
    (4, "building", "KYIV REGION", "REPORTED", "14 Missing After Kyiv Strike, Zelenskiy Says",
     ["Drone hit a building in the region.", "Fourteen missing, Zelenskiy said."], "JagranJosh"),
    (5, "dome", "ANTALYA, TURKIYE", "OFFICIAL", "COP31 Ends Without a Deal in Antalya",
     ["Summit closes with no agreement.", "Draft omits 'fossil fuels' wording."], "BBC / AP"),
    (6, "shipfire", "GULF OF FINLAND", "REPORTED", "Russian Cargo Ship Still Burns Off Finland",
     ["Cargo ship still burns after attack.", "Still burns - it has not sunk."], "BBC / JagranJosh"),
    (7, "blast", "BENGHAZI, LIBYA", "REPORTED", "Blast on Russian Ship in Benghazi Port",
     ["Explosion hit the ship in port.", "Suspected drone strike, reports say."], "BBC"),
    (8, "capitol", "WASHINGTON, US", "CONFIRMED", "Democrats Take the House 258-173",
     ["Largest House majority since 1992.", "North Carolina seat seals the win."], "BBC"),
    (9, "cricket", "WELLINGTON, NZ", "CONFIRMED", "India Post 720/9d at Wellington",
     ["India's highest total in New Zealand.", "Declared 720 for 9 vs New Zealand."], "ObserverVoice"),
    (10, "coin", "MARKETS", "REPORTED", "Gold Slides to $3,538 an Ounce",
     ["Down $2,000+ from record $5,595.", "Off 2.41% on Friday's close."], "ObserverVoice"),
    (11, "court", "THE HAGUE", "OFFICIAL", "ICJ: Myanmar Guilty of Rohingya Genocide",
     ["Court rules on the 2017 campaign.", "700,000+ Rohingya fled their homes."], "Pre-open wires"),
    (12, "tennis", "TURIN, ITALY", "CONFIRMED", "Alcaraz Beats Zverev for First ATP Finals Title",
     ["Defeats Alexander Zverev in Turin.", "His first ATP Finals crown."], "BBC"),
    (13, "shield", "WASHINGTON, US", "REPORTED", "FBI Probes Alleged Hack of Justice Database",
     ["Suspected hack of the main criminal", "justice database under inquiry."], "AP wire"),
]

ALSO = [
    (14, "Houthi missile on western Saudi Arabia intercepted - AFP"),
    (15, "Swimmer crosses Hormuz Strait for Iran wildlife - salonvision"),
    (16, "UN: nations to keep lethal AI weapons talks going - salonvision"),
    (17, "US releases more UFO footage over the Middle East - BBC"),
    (18, "Albanese: COP31 failure shows 'hard geopolitical times' - AFP"),
    (19, "Russia-bound ship towed after Gulf of Finland attack - BBC"),
    (20, "UK-EU Brexit reset a 'landmark', Burnham tells MPs - BBC"),
    (21, "Thousands march in Lisbon over cost of living - JagranJosh"),
    (22, "Myanmar junta calls ASEAN ruling 'unfair' - JagranJosh"),
    (23, "Cameroon ex-rebels trapped by broken promises - mediaalertpress"),
    (24, "Escaped lion frightens residents in Turkiye - mediaalertpress"),
    (25, "Nepal PM Balendra Shah holds talks with PM Modi - ObserverVoice"),
    (26, "India, Bulgaria discuss IMEC and Black Sea - thedailyjagran"),
    (27, "Guru Nanak Jayanti - 'Sewa, Simran aur Sangat' - ObserverVoice"),
    (28, "Uttar Pradesh air-raid, blackout drill in 75 districts"),
    (29, "Indonesia factory update: 7 body bags, 50 missing - JagranJosh"),
    (30, "India chase a famous win; NZ 119/2 on day five - ObserverVoice"),
    (31, "India win NZ ODI series 3-2; Phillips player of series"),
    (32, "Anupama defends IBSF world snooker title - ObserverVoice"),
    (33, "World Chess Championship draws the fans in - ObserverVoice"),
    (34, "Rajya Sabha MP Wadkute dies of heart attack in Delhi"),
    (35, "Kota bus tragedy: 9 killed in Rajasthan - ObserverVoice"),
    (36, "Tata Steel sells pipe unit to APL Apollo, Rs28,000 crore"),
    (37, "SpiceJet crews seek audit; IndiGo holds 65.9% home share"),
    (38, "IFFI 2026 hosts a BRICS roundtable in Goa - ObserverVoice"),
    (39, "Modi opens AI centre at IIT Patna; Rs400 crore projects"),
    (40, "Amit Shah launches Rs4,000 crore Arunachal infra push"),
    (41, "NEET PG 2026: 10,105 medical seats blocked - JagranJosh"),
    (42, "Trump criticises Schumer in Democrat leadership push"),
    (43, "US Army to detonate unstable explosives in Iowa - BBC"),
    (44, "Miley Cyrus marries Maxx Morando in California - BBC"),
]

REGIONS = [("MIDDLE EAST", 4, (150, 60, 60)), ("EUROPE", 10, (70, 90, 160)),
           ("AFRICA", 2, (190, 130, 40)), ("N AMERICA", 6, (60, 130, 90)),
           ("S ASIA", 15, (170, 80, 140)), ("SE ASIA", 3, (60, 140, 160)),
           ("ASIA-PACIFIC", 1, (120, 110, 60)), ("GLOBAL", 3, (100, 100, 110))]

TIMELINE = [("00:02Z", "UN AI talks go on"), ("02:00Z", "Albanese, Sydney"),
            ("EARLY", "Hormuz tankers burn"), ("MORNING", "Kyiv boy rescued"),
            ("MIDDAY", "COP31 closes"), ("AFTERNOON", "India 720/9d"),
            ("EVENING", "House 258-173"), ("LATE", "Alcaraz title")]

NUMBERS = [("258-173", "House seats won"), ("720/9d", "India record total"),
           ("$3,538", "Gold per ounce"), ("14", "Missing, Kyiv strike"),
           ("7", "Boy's age, Kyiv"), ("75", "Districts, UP drill"),
           ("65.9%", "IndiGo home share"), ("10,105", "NEET PG seats blocked")]

DATECHECK = [
    "Xi-Trump-Putin trilateral summit - 19 Nov 2026",
    "SpiceJet board fundraise Rs5,500 crore - 18 Nov 2026",
    "Hyderabad bomb-threat email - sent 21 Nov 2026",
    "Paolo Bulgari death - reported 22 Nov 2026",
    "Ukraine strike on Kerch Bridge - reported 22 Nov 2026",
    "South Korea education minister quits - reported 22 Nov 2026",
    "Indonesia candy factory fire itself - 22 Nov 2026;",
    "only its 23 Nov update is used as news here",
]

MAP_ROWS = [
    "        oooo                                          ",
    "  ooo  oooooo        ooo oooooooooo  ooo              ",
    " ooooo oooooooo     ooooooooooooooooooooo  oo         ",
    "  oooo  oooooo       ooo oooooooooooooooo oooo        ",
    "   oo    oooo         oo  ooooo  ooooooo   ooo        ",
    "        oooo              oooo    oooo      oo        ",
    "       ooooo              ooooo   oooo                ",
    "       oooo               ooooo    oo        o        ",
    "        oo                 ooo                    ",
]
PINS = [(1, 30, 4), (2, 29, 5), (3, 26, 2), (4, 27, 3), (5, 28, 3), (6, 25, 1),
        (7, 24, 4), (8, 8, 2), (9, 50, 8), (10, 18, 5), (11, 36, 5), (12, 23, 3), (13, 9, 3)]

def header(d, W):
    d.rectangle([0, 0, W, 24], fill=DARK)
    d.text((W//2, 12), "52 reports cross-checked  ·  16 wires & wires' wires  ·  All times UTC",
           font=F(SANS_B, 13), fill=GOLD_L, anchor="mm")
    d.text((W//2, 58), "THE DAY IN ONE PAGE", font=F(SERIF_B, 68), fill=INK, anchor="mm")
    d.text((W//2, 106), "MONDAY 23 NOVEMBER 2026", font=F(SANS_B, 38), fill=INK2, anchor="mm")
    d.line([14, 128, W-14, 128], fill=GOLD, width=3)
    d.line([14, 133, W-14, 133], fill=INK, width=1)
    d.text((14, 143), "GOLD $3,538/OZ (-2.41%) · RECORD $5,595 · BITCOIN: NO DAY-POOL WIRE · OIL: HORMUZ ABLAZE",
           font=F(SANS_B, 11), fill=INK)
    d.text((W-14, 143), "SKIES - KYIV · LISBON · ANTALYA · WELLINGTON: NO POOL WIRE",
           font=F(SANS_B, 11), fill=INK2, anchor="ra")
    x, y = 14, 156
    unit = (W - 28) / sum(r[1] for r in REGIONS)
    for name, n, col in REGIONS:
        wseg = unit * n
        d.rectangle([x, y, x+wseg-2, y+19], fill=col)
        d.text((x+wseg/2, y+9), "%s %d" % (name, n), font=F(SANS_B, 9), fill=WHITE, anchor="mm")
        x += wseg
    y = 184
    d.line([14, y, W-14, y], fill=GOLD, width=2)
    seg = (W-28) / 8
    for i, (t, ev) in enumerate(TIMELINE):
        cx = 14 + seg*i + seg/2
        d.ellipse([cx-3, y-3, cx+3, y+3], fill=INK)
        d.text((cx, y+5), t, font=F(SANS_B, 10), fill=INK, anchor="ma")
        d.text((cx, y+19), ev, font=F(SANS, 9), fill=INK2, anchor="ma")

def card(d, c, x, y, w, h, lead=False, slim=False):
    num, kind, loc, status, head, facts, src = c
    d.rectangle([x, y, x+w, y+h], fill=PAPER, outline=INK, width=2 if lead else 1)
    d.rectangle([x, y, x+w, y+17], fill=INK)
    d.text((x+5, y+8), "%d · %s" % (num, loc), font=F(SANS_B, 11), fill=GOLD_L, anchor="lm")
    cw = d.textlength(status, font=F(SANS_B, 10)) + 10
    d.rectangle([x+w-cw-3, y+2, x+w-3, y+15], fill=GOLD)
    d.text((x+w-cw/2-3, y+8), status, font=F(SANS_B, 10), fill=DARK, anchor="mm")
    iw = 92 if lead else 44
    icon(d, kind, x+5, y+21, iw, h-25)
    tx = x + iw + 12
    tw = x + w - tx - 5
    hf = F(SANS_B, 29 if lead else 24)
    yy = y + 21
    for ln in wrap(d, head, hf, tw)[:2]:
        d.text((tx, yy), ln, font=hf, fill=INK)
        yy += (33 if lead else 27)
    ff = F(SANS, 15 if lead else 14)
    nf = 1 if slim else len(facts)
    for fact in facts[:nf]:
        for ln in wrap(d, fact, ff, tw):
            d.text((tx, yy), ln, font=ff, fill=BODY)
            yy += 18
    d.text((tx, y+h-13), "Source: " + src, font=F(SANS, 10), fill=INK2)

def bottom(d, W):
    y0 = 811
    d.rectangle([14, y0, W-14, y0+90], fill=PAPER, outline=INK)
    d.rectangle([14, y0, W-14, y0+16], fill=INK2)
    d.text((20, y0+8), "ALSO ON THE DAY - 31 MORE REPORTS", font=F(SANS_B, 11), fill=GOLD_L, anchor="lm")
    for i, (n, t) in enumerate(ALSO):
        col, row = divmod(i, 8)
        xx = 20 + col * 248
        yy = y0 + 21 + row * 9
        txt = "%d. %s" % (n, t)
        fnt = F(SANS, 8)
        while d.textlength(txt, font=fnt) > 242 and " " in txt:
            txt = txt[:txt.rfind(" ")]
        d.text((xx, yy), txt, font=fnt, fill=BODY)
    y1 = 905
    d.rectangle([14, y1, 344, y1+97], fill=(245, 236, 210), outline=GOLD, width=2)
    d.text((22, y1+5), "THE DAY IN NUMBERS", font=F(SANS_B, 12), fill=INK)
    for i, (num, lab) in enumerate(NUMBERS):
        col, row = divmod(i, 4)
        xx = 22 + col * 164
        yy = y1 + 24 + row * 19
        d.text((xx, yy), num, font=F(SANS_B, 14), fill=INK2)
        nw = d.textlength(num, font=F(SANS_B, 14))
        d.text((xx+nw+5, yy+3), lab, font=F(SANS, 8), fill=BODY)
    d.rectangle([362, y1, 662, y1+97], fill=PAPER, outline=INK)
    d.text((368, y1+4), "WHERE IT HAPPENED - PINS = CARD NUMBERS", font=F(SANS_B, 9), fill=INK)
    cell = 5
    for r, rowtxt in enumerate(MAP_ROWS):
        for cc, ch in enumerate(rowtxt):
            if ch == "o":
                d.ellipse([370+cc*cell, y1+18+r*cell, 373+cc*cell, y1+21+r*cell], fill=(190, 175, 140))
    for n, cc, r in PINS:
        px, py = 370+cc*cell, y1+18+r*cell
        d.ellipse([px-6, py-6, px+6, py+6], fill=RED)
        d.text((px, py), str(n), font=F(SANS_B, 7), fill=WHITE, anchor="mm")
    d.text((368, y1+86), "1 Hormuz · 3-4 Kyiv · 5 Antalya · 9 Wellington · 11 The Hague", font=F(SANS, 8), fill=INK2)
    x0 = 666
    d.rectangle([x0, y1, W-14, y1+97], fill=(250, 235, 235), outline=RED)
    d.text((x0+8, y1+4), "DATE CHECK - NOT 23 NOV NEWS", font=F(SANS_B, 10), fill=RED)
    yy = y1 + 19
    for item in DATECHECK:
        d.text((x0+8, yy), "· " + item, font=F(SANS, 8), fill=(60, 30, 30))
        yy += 10
    d.rectangle([14, 1004, W-14, 1022], fill=DARK)
    d.text((W//2, 1009), "HOW SURE WE ARE: CONFIRMED = 2+ wires agree · OFFICIAL = on the record · REPORTED = one named wire · CLAIM = one side's account, framed in its headline",
           font=F(SANS_B, 8), fill=GOLD_L, anchor="mm")
    d.text((W//2, 1018), "Sources: BBC, AP, AFP, JagranJosh, ObserverVoice, mediaalertpress, salonvision · Original drawings",
           font=F(SANS, 8), fill=GOLD_L, anchor="mm")

def render(variant):
    img = Image.new("RGB", (1024, 1024), CREAM)
    d = ImageDraw.Draw(img)
    header(d, 1024)
    if variant == "A":
        card(d, CARDS[0], 14, 218, 996, 94, lead=True)
        gx, gy, gw, gh, gap = 14, 316, 328, 119, 5
        for i, c in enumerate(CARDS[1:]):
            col, row = i % 3, i // 3
            card(d, c, gx + col*(gw+gap), gy + row*(gh+gap), gw, gh)
    else:
        card(d, CARDS[0], 14, 218, 996, 94, lead=True)
        gx, gy, gw, gh, gap = 14, 316, 493, 76, 5
        for i, c in enumerate(CARDS[1:]):
            col, row = i % 2, i // 2
            card(d, c, gx + col*(gw+gap), gy + row*(gh+gap), gw, gh, slim=True)
    bottom(d, 1024)
    rnd = random.Random(15)
    px = img.load()
    for _ in range(9000):
        xx, yy = rnd.randrange(1024), rnd.randrange(1024)
        r, g, b = px[xx, yy]
        dn = rnd.randint(-7, 7)
        px[xx, yy] = (max(0, min(255, r+dn)), max(0, min(255, g+dn)), max(0, min(255, b+dn)))
    return img

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for v in ("A", "B"):
        out = os.path.join(here, "entry_%s.png" % v.lower())
        render(v).save(out, optimize=True)
        print(v, os.path.getsize(out))
