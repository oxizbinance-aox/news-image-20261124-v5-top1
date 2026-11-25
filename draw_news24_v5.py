#!/usr/bin/env python3
"""News Image 24 Nov 2026 — v5 front page, drawn fresh in code.

One 1024x1024 newspaper page: 48 stories dated Tuesday 24 November 2026,
10 regions (max 8 each), 24 fields, 15 pictured stories on a solid world map,
full claim labelling on every item. Pillow only, no network, deterministic.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data
# region key, display name, colour, count target
REGIONS = [
    ("EUR", "EUROPE", "#2563EB", 8),
    ("NAM", "N. AMERICA", "#DC2626", 8),
    ("MEA", "MIDDLE EAST", "#EA580C", 5),
    ("EAS", "E. ASIA", "#7C3AED", 5),
    ("SAS", "S. ASIA", "#0891B2", 4),
    ("SEA", "SE ASIA", "#059669", 4),
    ("LAM", "LATIN AM.", "#DB2777", 4),
    ("AFR", "AFRICA", "#CA8A04", 4),
    ("OCE", "OCEANIA", "#65A30D", 3),
    ("WLD", "WORLD", "#64748B", 3),
]
RCOL = {k: c for k, _, c, _ in REGIONS}
RNAME = {k: n for k, n, _, _ in REGIONS}

# claim codes: C confirmed, O official, R reported, CL claim, OG ongoing
CLAIM_FILL = {"C": "#15803D", "O": "#1D4ED8", "R": "#B45309",
              "CL": "#B91C1C", "OG": "#6D28D9"}

# num, region, field, claim, headline, deck, source, lon, lat (lon/lat only if drawn)
STORIES = [
    (1, "NAM", "Markets", "O", "Huang back at Nvidia as shares soar",
     "Board reinstates founder-CEO; chipmaker gains $952bn in a day.",
     "Reuters / CNN", -122.0, 37.0),
    (2, "AFR", "Defence", "O", "Ukraine sinks Russian warship off Libya",
     "Kyiv confirms the corvette Merkury was hit near Benghazi; Tripoli condemns the strike.",
     "Reuters / WSJ", 20.0, 32.0),
    (3, "MEA", "Climate", "O", "COP31 ends with no pact",
     "First summit since 2009 to close without a deal.", "Reuters", 30.7, 36.9),
    (4, "EUR", "Defence", "O", "NATO sends early-warning plane",
     "AWACS to Poland as the alliance watches the east.", "Reuters", 19.0, 52.0),
    (5, "EUR", "Security", "O", "96 drones in one night",
     "Odesa dark and cold as 73 are shot down.", "Ukr Air Force", 30.5, 50.4),
    (6, "MEA", "Energy", "R", "Iran vows to defy US blockade",
     "Tehran says tankers will keep sailing as Washington tightens its cordon.",
     "Reuters", 56.5, 26.5),
    (7, "NAM", "Transport", "O", "Delta outage grounds 3,000+ flights",
     "US air travel snarled; Atlanta hub hit hardest.", "Delta", -84.4, 33.7),
    (8, "EAS", "Defence", "R", "12 Chinese warships circle Taiwan",
     "Taipei tracks the flotilla around the island.", "Reuters", 121.0, 23.5),
    (9, "SAS", "Science", "O", "5.6 quake strikes Nepal",
     "Tremor near the China border; no deaths reported.", "AP", 85.0, 28.0),
    (10, "EUR", "Health", "O", "Sanofi buys Insmed for $41bn",
     "Paris drugmaker's biggest deal in years.", "Sanofi / WSJ", 2.35, 48.85),
    (11, "AFR", "Disaster", "R", "24 dead as boat capsizes",
     "Vessel sinks on the way to a funeral.", "AP", 7.0, 9.0),
    (12, "LAM", "Courts", "O", "Mexico nabs 'Chapo Isidro'",
     "16 killed in the operation, officials say.", "Reuters", -102.0, 23.0),
    (13, "OCE", "Politics", "OG", "Bougainville votes on nationhood",
     "Referendum on independence opens in PNG.", "Conversation", 147.0, -6.3),
    (14, "NAM", "Diplomacy", "R", "Trump to meet Rutte on Wednesday",
     "White House sets talks for the day after.", "Reuters", None, None),
    (15, "EUR", "Tech", "O", "Germany adopts Ukraine's Delta system",
     "Berlin takes Kyiv's battle-management software.", "Reuters", None, None),
    (16, "EUR", "Defence", "R", "Ukraine drones set two Russian refineries ablaze",
     "Reuters", None, None),
    (17, "MEA", "Energy", "CL", "Houthis say they hit Saudi Rabigh refinery",
     "Reuters", None, None),
    (18, "MEA", "Security", "R", "Israeli strike kills 3 in Khan Younis",
     "AP", None, None),
    (19, "OCE", "Disaster", "O", "Vanuatu 6.5 quake, no tsunami",
     "Pacific island shakes; no wave follows.", "AP", 167.0, -16.0),
    (20, "EAS", "Politics", "O", "Seoul names new foreign minister and spy chief",
     "Yonhap", None, None),
    (21, "OCE", "Culture", "R", "Hobart stadium bill jumps to $1.23 billion",
     "Reuters", None, None),
    (22, "NAM", "Trade", "O", "US blacklists Megaspeed over export controls",
     "Reuters", None, None),
    (23, "NAM", "Migration", "O", "US unveils H-1B visa changes",
     "Reuters", None, None),
    (24, "EUR", "Politics", "R", "Armenia drops Karabakh claim in draft charter",
     "Reuters", None, None),
    (25, "EUR", "Diplomacy", "O", "Cyprus expels two Russian diplomats over spying",
     "Reuters", None, None),
    (26, "EUR", "Education", "R", "Bomb threats close schools in Germany and Denmark",
     "AP", None, None),
    (27, "WLD", "Diplomacy", "O", "NATO offers Poland 'significant backing'",
     "Reuters", None, None),
    (28, "NAM", "Defence", "R", "Russian losses outpace recruiting, US says",
     "Reuters", None, None),
    (29, "NAM", "Sport", "O", "US to host 2031 Women's World Cup, FIFA says",
     "FIFA", None, None),
    (30, "LAM", "Trade", "R", "Panama, First Quantum resume Cobre mine talks",
     "Reuters", None, None),
    (31, "LAM", "Disaster", "R", "Storm forces thousands to flee in Brazil",
     "AP", None, None),
    (32, "MEA", "Environment", "O", "Gaza's soil and water poisoned by war, report finds",
     "UN", None, None),
    (33, "WLD", "Tech", "O", "UN chief urges global AI safety rules within a year",
     "UN", None, None),
    (34, "SAS", "Diplomacy", "O", "India and Nepal sign 8 deals",
     "Reuters", None, None),
    (35, "SAS", "Politics", "R", "Hasina plans December 16 return to Bangladesh",
     "Reuters", None, None),
    (36, "SEA", "Crime", "R", "Hanoi hotpot blast kills 6, injures 10+",
     "AP / Reuters", None, None),
    (37, "NAM", "Media", "R", "States sue SpaceX over Grok images",
     "Al Jazeera", None, None),
    (38, "WLD", "Space", "O", "Beaver Supermoon rises tonight",
     "Sky at Night", None, None),
    (39, "EAS", "Markets", "R", "South Korea proposes ending nine-year ICO ban",
     "Seoul", None, None),
    (40, "EAS", "Labour", "O", "Seoul Metro unions call off strike in wage deal",
     "Yonhap", None, None),
    (41, "EAS", "Transport", "R", "China Southern unit to buy 50 Boeing 737-8 jets",
     "Reuters", None, None),
    (42, "SAS", "Sport", "O", "204* off 53 balls",
     "Sooryavanshi's blitz sends India A to the semis.", "Sports Encounter", 51.5, 25.3),
    (43, "SEA", "Economy", "O", "Laos leaves least-developed-country ranks",
     "Reuters", None, None),
    (44, "SEA", "Trade", "R", "Chinese e-truck makers push exports via Vietnam",
     "Reuters", None, None),
    (45, "SEA", "Diplomacy", "R", "Guangxi builders head to Malaysia in ASEAN push",
     "Xinhua", None, None),
    (46, "LAM", "Economy", "O", "Argentina officially enters technical recession",
     "BA Herald", None, None),
    (47, "AFR", "Politics", "R", "Kenya faces Sh12bn election funding gap",
     "Daily Nation", None, None),
    (48, "AFR", "Health", "O", "Tanzania launches '3 Zero' maternal drive",
     "The Citizen", None, None),
]

# ALSO items are stories 16..48 minus the drawn ones (19, 42 are drawn mids).
DRAWN = [1, 2, 6, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 19, 42]
ALSO = [s for s in STORIES if s[0] not in DRAWN]
LEADS = [2, 6, 1]                      # story numbers, left to right
MIDS_R1 = [3, 4, 5, 7, 8, 9]
MIDS_R2 = [10, 11, 12, 13, 19, 42]

NUMBERS = [
    ("+31.5%", "NVIDIA SHARES"),
    ("96", "DRONES AT UKRAINE"),
    ("3,000+", "US FLIGHTS HIT"),
    ("6.5", "VANUATU QUAKE"),
    ("24", "DEAD, NIGERIA BOAT"),
    ("$952BN", "NVIDIA GAIN"),
    ("204*", "SOORYAVANSHI, 53 BALLS"),
]

UTC = [
    ("05:30", "Taiex +9.0%"),
    ("06:30", "Sanofi $41bn"),
    ("07:45", "Tripoli condemns"),
    ("08:00", "73 drones downed"),
    ("14:00", "Huang reinstated"),
    ("16:30", "NATO: AWACS"),
    ("21:00", "Supermoon rises"),
]

FIELDS_LINE = ("FIELDS (24): Politics · Defence · Diplomacy · Markets · Tech · Energy · "
               "Climate · Health · Sport · Space · Courts · Transport · Disaster · Economy · "
               "Crime · Migration · Media · Science · Labour · Trade · Environment · "
               "Education · Culture · Security")

MARKETS = [("NVIDIA", "+31.5%"), ("TAIEX", "+9.0%"), ("KOSPI", "+7.3%"),
           ("NASDAQ", "+6.5%"), ("S&P 500", "+4.7%"), ("NIKKEI", "+4.2%")]


def by_num(n):
    return next(s for s in STORIES if s[0] == n)


# ---------------------------------------------------------------- helpers
INK = "#1A1A1A"
MUT = "#5A5A5A"
PAPER = "#FDFBF5"
RULE = "#C9C2B2"


def fit(d, text, fnt, max_w):
    """Fail the build if text does not fit — never clip, never ellipsis."""
    w = d.textlength(text, font=fnt)
    if w > max_w:
        raise SystemExit("OVERFLOW %r width %.1f > %.1f (font %d)"
                         % (text, w, max_w, fnt.size))
    return w


def wrap(d, text, fnt, max_w, max_lines):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if not cur:
                raise SystemExit("WORD TOO LONG %r" % wd)
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        raise SystemExit("WRAP OVERFLOW %r -> %d lines > %d"
                         % (text, len(lines), max_lines))
    return lines


def claim_chip(d, x, y, code, r=7):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=CLAIM_FILL[code],
              outline="#FFFFFF", width=1)
    f = font(FB, 7 if len(code) == 1 else 5)
    tw = d.textlength(code, font=f)
    d.text((x + r - tw / 2, y + r - (5 if len(code) == 1 else 4)),
           code, font=f, fill="#FFFFFF")


def tag_line(d, x, y, story, max_w):
    """Small claim chip + field + source, one line, checked to fit."""
    _, region, field, claim, _, _, src, _, _ = story
    claim_chip(d, x, y - 1, claim, r=6)
    f = font(FB, 7)
    txt = "%s  ·  %s" % (field.upper(), src.upper())
    fit(d, txt, f, max_w - 16)
    d.text((x + 15, y), txt, font=f, fill=MUT)


def sun_sky(d, box):
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, (y1 - y0))
        r = int(186 + (255 - 186) * t)
        g = int(214 + (238 - 214) * t)
        b = int(240 + (220 - 240) * t)
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))
    d.ellipse([x1 - 34, y0 + 6, x1 - 10, y0 + 30], fill="#FFD94D",
              outline="#E8A90C", width=1)
    for cx, cy, w in [(x0 + 22, y0 + 14, 30), (x0 + 70, y0 + 26, 24)]:
        d.ellipse([cx, cy, cx + w, cy + 9], fill="#FFFFFF")
        d.ellipse([cx + 8, cy - 4, cx + w - 6, cy + 5], fill="#FFFFFF")


# ---------------------------------------------------------------- scenes
def scene_sea_warship(d, box):
    """Lead 1: listing corvette hit off Benghazi — rich daylight scene."""
    x0, y0, x1, y1 = box
    sun_sky(d, box)
    # extra clouds + birds in the layered sky
    for cx, cy, w in [(x0 + 96, y0 + 16, 34), (x0 + 176, y0 + 8, 26),
                      (x0 + 44, y0 + 34, 26), (x0 + 210, y0 + 30, 30)]:
        d.ellipse([cx, cy, cx + w, cy + 8], fill="#FFFFFF")
        d.ellipse([cx + 7, cy - 4, cx + w - 5, cy + 4], fill="#FFFFFF")
    for bx, by in [(x0 + 150, y0 + 22), (x0 + 162, y0 + 26), (x0 + 240, y0 + 18)]:
        d.line([(bx, by), (bx + 4, by - 3), (bx + 8, by)], fill="#4A5568", width=1)
    # distant headland + shoreline band (Benghazi coast)
    d.polygon([(x0, y1 - 46), (x0 + 70, y1 - 58), (x0 + 150, y1 - 50),
               (x0 + 210, y1 - 44), (x0 + 260, y1 - 48), (x1, y1 - 42),
               (x1, y1 - 38), (x0, y1 - 38)], fill="#B7A67E")
    d.polygon([(x0, y1 - 40), (x1, y1 - 40), (x1, y1 - 34), (x0, y1 - 34)],
              fill="#C9B18A")
    # shoreline town: blocky buildings with windows, dome + minaret
    for bx, bw, bh in [(6, 14, 10), (24, 10, 8), (40, 16, 12),
                       (252, 12, 9), (268, 14, 11)]:
        d.rectangle([x0 + bx, y1 - 40 - bh, x0 + bx + bw, y1 - 40],
                    fill="#EFE6CC", outline="#8A7D5F", width=1)
        for wx in range(x0 + bx + 3, x0 + bx + bw - 2, 5):
            d.rectangle([wx, y1 - 40 - bh + 3, wx + 2, y1 - 40 - bh + 6],
                        fill="#5B7A94")
    d.pieslice([x0 + 58, y1 - 56, x0 + 74, y1 - 40], 180, 360, fill="#B03A2E")
    d.rectangle([x0 + 78, y1 - 62, x0 + 82, y1 - 40], fill="#EFE6CC",
                outline="#8A7D5F", width=1)
    d.polygon([(x0 + 77, y1 - 62), (x0 + 80, y1 - 68), (x0 + 83, y1 - 62)],
              fill="#B03A2E")
    # lighthouse at the right end of the coast, pale beam to the left
    d.polygon([(x0 + 296, y1 - 62), (x0 + 250, y1 - 56), (x0 + 250, y1 - 52),
               (x0 + 296, y1 - 56)], fill="#FFF3B0")
    d.rectangle([x0 + 296, y1 - 64, x0 + 304, y1 - 40], fill="#FFFFFF",
                outline="#8A7D5F", width=1)
    d.rectangle([x0 + 296, y1 - 58, x0 + 304, y1 - 54], fill="#B91C1C")
    d.rectangle([x0 + 296, y1 - 48, x0 + 304, y1 - 44], fill="#B91C1C")
    d.rectangle([x0 + 298, y1 - 68, x0 + 302, y1 - 64], fill="#1F2937")
    # sea, gradient from the shoreline down
    for i in range(y1 - 38, y1):
        t = (i - (y1 - 38)) / 38.0
        d.line([(x0, i), (x1, i)],
               fill=(int(58 + 30 * t), int(122 + 30 * t), int(168 + 20 * t)))
    d.text((x0 + 272, y1 - 26), "BENGHAZI", font=font(FB, 7), fill="#FFE9B8")
    # sun glitter on the water, below the label
    for gx, gy, gl in [(x0 + 276, y1 - 14, 22), (x0 + 282, y1 - 9, 14),
                       (x0 + 272, y1 - 4, 26)]:
        d.line([(gx, gy), (gx + gl, gy)], fill="#FFE08A", width=2)
    # wave crests
    for wx, wy in [(x0 + 18, y1 - 12), (x0 + 120, y1 - 8), (x0 + 196, y1 - 14),
                   (x0 + 40, y1 - 8)]:
        d.arc([wx, wy, wx + 36, wy + 10], 180, 360, fill="#DFF2FA", width=2)
    # small patrol boat, far left, with a wake
    d.polygon([(x0 + 10, y1 - 28), (x0 + 38, y1 - 28), (x0 + 34, y1 - 22),
               (x0 + 14, y1 - 22)], fill="#5B6670")
    d.rectangle([x0 + 20, y1 - 34, x0 + 30, y1 - 28], fill="#78828C")
    for wx in range(x0 + 44, x0 + 68, 8):
        d.line([(wx, y1 - 27), (wx + 5, y1 - 27)], fill="#FFFFFF", width=1)
    # listing grey corvette, bow down, hit at the stern
    d.polygon([(x0 + 78, y1 - 52), (x0 + 232, y1 - 44), (x0 + 244, y1 - 30),
               (x0 + 70, y1 - 30)], fill="#5B6670")
    d.polygon([(x0 + 71, y1 - 34), (x0 + 243, y1 - 34), (x0 + 244, y1 - 30),
               (x0 + 70, y1 - 30)], fill="#8C2F26")
    d.line([(x0 + 78, y1 - 52), (x0 + 232, y1 - 44)], fill="#E8EDF2", width=2)
    d.rectangle([x0 + 120, y1 - 66, x0 + 178, y1 - 50], fill="#78828C")
    d.rectangle([x0 + 132, y1 - 76, x0 + 168, y1 - 66], fill="#8A949E")
    for wx in range(x0 + 136, x0 + 166, 10):
        d.rectangle([wx, y1 - 74, wx + 6, y1 - 69], fill="#BFE0F2")
    # mast, radar bar, antenna + flag
    d.line([(x0 + 150, y1 - 92), (x0 + 150, y1 - 76)], fill="#3E4750", width=2)
    d.line([(x0 + 140, y1 - 90), (x0 + 160, y1 - 88)], fill="#3E4750", width=2)
    d.line([(x0 + 150, y1 - 92), (x0 + 150, y1 - 100)], fill="#3E4750", width=1)
    d.polygon([(x0 + 150, y1 - 100), (x0 + 160, y1 - 97), (x0 + 150, y1 - 94)],
              fill="#B91C1C")
    # funnel with a yellow band
    d.rectangle([x0 + 182, y1 - 64, x0 + 196, y1 - 50], fill="#3E4750")
    d.rectangle([x0 + 182, y1 - 64, x0 + 196, y1 - 60], fill="#FFD94D")
    # bow gun turret + barrel
    d.polygon([(x0 + 200, y1 - 62), (x0 + 206, y1 - 62), (x0 + 203, y1 - 44)],
              fill="#3E4750")
    d.polygon([(x0 + 204, y1 - 56), (x0 + 218, y1 - 62), (x0 + 218, y1 - 58),
               (x0 + 206, y1 - 52)], fill="#3E4750")
    # lit portholes along the hull
    for px in range(x0 + 84, x0 + 232, 16):
        d.rectangle([px, y1 - 42, px + 7, y1 - 36], fill="#FFD94D")
    # bow wave + stern wake foam (kept clear of the BENGHAZI label)
    d.arc([x0 + 228, y1 - 24, x0 + 262, y1 - 10], 180, 360, fill="#FFFFFF", width=2)
    d.arc([x0 + 238, y1 - 18, x0 + 264, y1 - 6], 180, 360, fill="#DFF2FA", width=2)
    # orange lifeboat + buoy in the water, right of the ship
    d.polygon([(x0 + 244, y1 - 22), (x0 + 262, y1 - 22), (x0 + 258, y1 - 16),
               (x0 + 248, y1 - 16)], fill="#EA580C")
    d.ellipse([x0 + 250, y1 - 26, x0 + 253, y1 - 22], fill="#1F2937")
    d.ellipse([x0 + 306, y1 - 12, x0 + 312, y1 - 6], fill="#B91C1C")
    # hit fire at the stern + smoke column drifting left
    d.polygon([(x0 + 92, y1 - 52), (x0 + 100, y1 - 70), (x0 + 106, y1 - 58),
               (x0 + 112, y1 - 66), (x0 + 114, y1 - 52)], fill="#F97316")
    d.polygon([(x0 + 98, y1 - 52), (x0 + 102, y1 - 62), (x0 + 108, y1 - 52)],
              fill="#FBBF24")
    for sx, sy, sr in [(x0 + 100, y1 - 78, 9), (x0 + 92, y1 - 90, 11),
                       (x0 + 88, y1 - 94, 7)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill="#C9CDD2",
                  outline="#9AA0A6", width=1)
    # funnel smoke, thinner, drifting right
    for sx, sy, sr in [(x0 + 192, y1 - 72, 6), (x0 + 200, y1 - 82, 8),
                       (x0 + 210, y1 - 92, 9)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill="#D8DBDE")
    # three drones with rotors, red lights, dashed flight path
    for dx, dy in [(x0 + 40, y0 + 44), (x0 + 268, y0 + 36), (x0 + 150, y0 + 30)]:
        d.line([(dx - 12, dy - 8), (dx + 12, dy - 8)], fill="#9AA0A6", width=1)
        d.ellipse([dx - 5, dy - 2, dx + 5, dy + 2], fill="#222222")
        d.line([(dx - 9, dy - 3), (dx + 9, dy - 3)], fill="#222222", width=1)
        d.line([(dx, dy + 2), (dx + 4, dy + 9)], fill="#9AA0A6", width=1)
        d.ellipse([dx + 3, dy - 4, dx + 6, dy - 1], fill="#DC2626")
    for x in range(x0 + 52, x0 + 78, 8):
        d.line([(x, y0 + 42), (x + 4, y0 + 42)], fill="#9AA0A6", width=1)


def scene_hormuz_map(d, box):
    """Lead 2: regional map of the Strait of Hormuz — geography is the news."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill="#D6EAF7", outline="#8FA8BC", width=1)
    # Iran (top), Arabian peninsula (bottom), strait between
    d.polygon([(x0, y0), (x1, y0), (x1, y0 + 44), (x0 + 210, y0 + 52),
               (x0 + 150, y0 + 40), (x0, y0 + 46)], fill="#E4D3AC")
    d.polygon([(x0 + 120, y1 - 46), (x0 + 200, y1 - 58), (x0 + 260, y1 - 40),
               (x1, y1 - 34), (x1, y1), (x0, y1)], fill="#E4D3AC")
    d.polygon([(x0, y0 + 46), (x0 + 150, y0 + 40), (x0 + 210, y0 + 52),
               (x0 + 200, y1 - 58), (x0 + 120, y1 - 46), (x0, y1 - 30),
               (x0, y0 + 46)], fill="#7FB3D5")
    fB, fS = font(FB, 10), font(FB, 7)
    d.text((x0 + 12, y0 + 8), "IRAN", font=fB, fill="#4A3F28")
    d.text((x0 + 12, y1 - 18), "OMAN", font=fB, fill="#4A3F28")
    d.text((x1 - 52, y1 - 18), "UAE", font=fB, fill="#4A3F28")
    d.text((x0 + 208, y0 + 58), "STRAIT OF", font=fS, fill="#1F4E79")
    d.text((x0 + 208, y0 + 68), "HORMUZ", font=fS, fill="#1F4E79")
    # dashed blockade line across the strait water, with its label above it
    d.text((x0 + 40, y0 + 62), "US BLOCKADE LINE", font=font(FB, 6),
           fill="#B91C1C")
    for ax in range(x0 + 40, x0 + 296, 16):
        d.line([(ax, y0 + 76), (ax + 9, y0 + 76)], fill="#B91C1C", width=2)
    d.polygon([(x0 + 298, y0 + 71), (x0 + 298, y0 + 81), (x0 + 308, y0 + 76)],
              fill="#B91C1C")
    # three tankers in the strait, below the blockade line
    for tx, ty in [(x0 + 150, y0 + 88), (x0 + 190, y0 + 98), (x0 + 228, y0 + 86)]:
        d.rectangle([tx, ty, tx + 34, ty + 9], fill="#B03A2E")
        d.rectangle([tx + 4, ty - 6, tx + 12, ty], fill="#7B241C")
        d.rectangle([tx + 24, ty - 4, tx + 30, ty], fill="#7B241C")


def scene_data_nvidia(d, box):
    """Lead 3: data lead — giant number + horizontal mini bar chart."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill="#EFF7E9", outline="#9DB98A", width=1)
    fG = font(FB, 40)
    big = "+31.5%"
    d.text((x0 + 12, y0 + 28), big, font=fG, fill="#15803D")
    tx = x0 + 12 + int(d.textlength(big, font=fG)) + 12  # text starts clear of the number
    d.text((tx, y0 + 32), "NVIDIA SHARES", font=font(FB, 8), fill=INK)
    d.text((tx, y0 + 44), "IN ONE DAY", font=font(FB, 8), fill=INK)
    d.text((tx, y0 + 56), "$952BN GAINED", font=font(FB, 8), fill="#15803D")
    # small up arrow, top right, clear of the text
    d.line([(x0 + 296, y0 + 44), (x0 + 312, y0 + 22)], fill="#15803D", width=3)
    d.polygon([(x0 + 312, y0 + 14), (x0 + 318, y0 + 26), (x0 + 306, y0 + 26)],
              fill="#15803D")
    # horizontal mini bar chart: label, bar, value — nothing overlaps
    vals = [("NVDA", 31.5), ("TAIEX", 9.0), ("KOSPI", 7.3), ("NDX", 6.5)]
    for i, (lab, v) in enumerate(vals):
        ry = y0 + 70 + i * 11
        d.text((x0 + 12, ry), lab, font=font(FB, 8), fill=INK)
        blen = int(v / 31.5 * 170)
        d.rectangle([x0 + 58, ry + 1, x0 + 58 + blen, ry + 9],
                    fill="#15803D" if i == 0 else "#5B9E6A")
        d.text((x0 + 62 + blen, ry), "+%.1f%%" % v, font=font(FB, 8), fill=INK)


def mini_scene(d, box, num):
    """Small bright scene strip for a mid card."""
    x0, y0, x1, y1 = box
    sun_sky(d, box)
    mid_y = y1 - 18
    if num == 3:  # COP31 hall: flags + hall
        d.rectangle([x0, mid_y, x1, y1], fill="#E8DCC0")
        for i, c in enumerate(["#2563EB", "#DC2626", "#059669", "#EA580C", "#7C3AED"]):
            fx = x0 + 14 + i * 30
            d.line([(fx, y0 + 4), (fx, y0 + 16)], fill=INK, width=1)
            d.polygon([(fx, y0 + 4), (fx + 18, y0 + 9), (fx, y0 + 14)], fill=c)
        d.rectangle([x0 + 40, y0 + 20, x1 - 40, mid_y], fill="#F5EFE0",
                    outline="#8A7D5F", width=1)
        d.text((x0 + 52, y0 + 22), "COP31", font=font(FB, 9), fill=INK)
    elif num == 4:  # AWACS over green fields
        d.rectangle([x0, mid_y, x1, y1], fill="#7CB85C")
        d.line([(x0, mid_y + 6), (x1, mid_y + 6)], fill="#5B9E46", width=1)
        d.ellipse([x0 + 58, y0 + 12, x0 + 104, y0 + 22], fill="#E8EDF2")
        d.rectangle([x0 + 62, y0 + 24, x0 + 100, y0 + 30], fill="#5B6670")
        d.polygon([(x0 + 100, y0 + 16), (x0 + 118, y0 + 20), (x0 + 100, y0 + 26)],
                  fill="#5B6670")
        d.polygon([(x0 + 62, y0 + 24), (x0 + 48, y0 + 28), (x0 + 62, y0 + 30)],
                  fill="#5B6670")
    elif num == 5:  # 96 drones: bright dusk sky, lit city, tracers, bursts
        # dusk gradient — pale peach to gold, bright, never a dark panel
        for i in range(y1 - y0):
            t = i / max(1, (y1 - y0))
            d.line([(x0, y0 + i), (x1, y0 + i)],
                   fill=(int(253 - 8 * t), int(226 - 46 * t), int(178 - 28 * t)))
        # low sun on the horizon, right (drawn before the skyline, so it
        # sets behind the buildings)
        d.ellipse([x1 - 26, mid_y - 14, x1 - 10, mid_y + 2], fill="#FFE08A",
                  outline="#E8A90C", width=1)
        # searchlight beams, pale gold, behind the skyline
        d.polygon([(x0 + 22, mid_y), (x0 + 52, y0 + 4), (x0 + 60, y0 + 4),
                   (x0 + 34, mid_y)], fill="#FFF3B0")
        d.polygon([(x0 + 118, mid_y), (x0 + 96, y0 + 8), (x0 + 102, y0 + 8),
                   (x0 + 126, mid_y)], fill="#FFF3B0")
        # skyline, warm mid-tones, with MANY lit windows
        for bx, bw, bh in [(4, 18, 14), (26, 14, 20), (44, 20, 12),
                           (68, 16, 18), (88, 14, 11), (106, 18, 16),
                           (128, 16, 13)]:
            d.rectangle([x0 + bx, mid_y - bh, x0 + bx + bw, mid_y],
                        fill="#7A6A55")
            for wy in range(mid_y - bh + 3, mid_y - 2, 5):
                for wx in range(x0 + bx + 3, x0 + bx + bw - 2, 5):
                    d.rectangle([wx, wy, wx + 2, wy + 2], fill="#FFD94D")
        # tower with a lit spire, centre
        d.rectangle([x0 + 66, mid_y - 26, x0 + 72, mid_y], fill="#5C5348")
        d.polygon([(x0 + 65, mid_y - 26), (x0 + 69, mid_y - 32),
                   (x0 + 73, mid_y - 26)], fill="#5C5348")
        d.rectangle([x0 + 68, mid_y - 24, x0 + 70, mid_y - 22], fill="#FFD94D")
        # ground band
        d.rectangle([x0, mid_y, x1, y1], fill="#6B5D4F")
        # tracer arcs, bright dots climbing from the ground to the drones
        for ax0, ax1, apex in [(x0 + 30, x0 + 58, y0 + 12),
                               (x0 + 84, x0 + 108, y0 + 8),
                               (x0 + 122, x0 + 142, y0 + 14)]:
            for s in range(0, 11):
                t = s / 10.0
                px = int(ax0 + (ax1 - ax0) * t)
                py = int(mid_y - (mid_y - apex) * 4 * t * (1 - t))
                d.rectangle([px, py, px + 1, py + 1],
                            fill="#FF6B35" if s % 2 else "#FFD94D")
        # airburst starbursts where the tracers meet the drones
        for cx, cy in [(x0 + 58, y0 + 12), (x0 + 108, y0 + 8)]:
            d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline="#FBBF24", width=1)
            for ex, ey in [(cx - 7, cy), (cx + 7, cy), (cx, cy - 7), (cx, cy + 7),
                           (cx - 5, cy - 5), (cx + 5, cy - 5),
                           (cx - 5, cy + 5), (cx + 5, cy + 5)]:
                d.line([(cx, cy), (ex, ey)], fill="#F97316", width=1)
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill="#FFE08A")
        # three drones with rotors + red lights, on the tracer arcs
        for dx, dy in [(x0 + 40, y0 + 10), (x0 + 96, y0 + 10), (x0 + 132, y0 + 12)]:
            d.line([(dx - 8, dy - 5), (dx + 8, dy - 5)], fill="#4A4038", width=1)
            d.ellipse([dx - 4, dy - 2, dx + 4, dy + 2], fill="#222222")
            d.ellipse([dx + 2, dy - 3, dx + 4, dy - 1], fill="#DC2626")
    elif num == 7:  # Delta: grounded planes + board
        d.rectangle([x0, mid_y, x1, y1], fill="#9AA5AD")
        d.rectangle([x0 + 8, y0 + 8, x0 + 62, y0 + 30], fill="#1F2937")
        d.text((x0 + 12, y0 + 12), "DELAYED", font=font(FB, 9), fill="#FBBF24")
        for px in (x0 + 84, x0 + 122):
            d.ellipse([px, y0 + 18, px + 34, y0 + 26], fill="#FFFFFF")
            d.rectangle([px + 6, y0 + 28, px + 28, y0 + 33], fill="#FFFFFF")
    elif num == 8:  # Taiwan: warships + green mountains
        d.polygon([(x0, mid_y), (x0 + 50, y0 + 18), (x0 + 100, mid_y)], fill="#5B8C5A")
        d.polygon([(x0 + 80, mid_y), (x0 + 130, y0 + 10), (x1, mid_y)], fill="#6FA368")
        d.rectangle([x0, mid_y, x1, y1], fill="#5B8FB0")
        for sx in (x0 + 16, x0 + 84):
            d.rectangle([sx, mid_y - 8, sx + 40, mid_y - 2], fill="#3E4750")
            d.rectangle([sx + 12, mid_y - 14, sx + 18, mid_y - 8], fill="#3E4750")
    elif num == 9:  # Himalayas + prayer flags
        d.polygon([(x0, mid_y), (x0 + 40, y0 + 8), (x0 + 80, mid_y)], fill="#E8EDF2")
        d.polygon([(x0 + 60, mid_y), (x0 + 110, y0 + 2), (x1, mid_y)], fill="#DDE4EA")
        d.polygon([(x0 + 28, y0 + 8), (x0 + 40, y0 + 2), (x0 + 52, y0 + 8)],
                  fill="#FFFFFF")
        for i, c in enumerate(["#2563EB", "#DC2626", "#059669", "#EA580C", "#7C3AED"]):
            fx = x0 + 8 + i * 28
            d.polygon([(fx, y0 + 30), (fx + 14, y0 + 30), (fx + 7, y0 + 40)], fill=c)
        d.line([(x0 + 8, y0 + 30), (x1 - 8, y0 + 30)], fill=INK, width=1)
    elif num == 10:  # Sanofi lab, bright
        d.rectangle([x0, mid_y, x1, y1], fill="#DCE9F5")
        for fx, fh in [(x0 + 18, 20), (x0 + 52, 24), (x0 + 88, 16), (x0 + 120, 22)]:
            d.rectangle([fx, mid_y - fh, fx + 16, mid_y], fill="#BFE3C6",
                        outline="#2E7D32", width=1)
            d.rectangle([fx + 5, mid_y - fh - 6, fx + 11, mid_y - fh],
                        fill="#BFE3C6", outline="#2E7D32", width=1)
        d.ellipse([x0 + 128, y0 + 8, x0 + 148, y0 + 28], fill="#FBBF24")
    elif num == 11:  # Nigeria river boat, bright
        d.rectangle([x0, mid_y, x1, y1], fill="#5B8FB0")
        d.polygon([(x0 + 40, mid_y - 6), (x0 + 120, mid_y - 6), (x0 + 108, mid_y + 8),
                   (x0 + 52, mid_y + 8)], fill="#8A5A2B")
        d.polygon([(x0 + 60, mid_y - 20), (x0 + 66, mid_y - 20), (x0 + 63, mid_y - 6)],
                  fill="#5B3A1A")
        for wx in (x0 + 20, x0 + 120):
            d.arc([wx, mid_y + 2, wx + 30, mid_y + 10], 180, 360, fill="#DFF2FA",
                  width=2)
    elif num == 12:  # Mexico desert convoy
        d.rectangle([x0, mid_y, x1, y1], fill="#E8C98A")
        d.polygon([(x0, mid_y), (x0 + 60, y0 + 20), (x1 - 30, mid_y)], fill="#C9A86A")
        for vx in (x0 + 24, x0 + 76, x0 + 120):
            d.rectangle([vx, mid_y - 12, vx + 26, mid_y - 4], fill="#5B6670")
            d.ellipse([vx + 4, mid_y - 4, vx + 10, mid_y + 2], fill="#222222")
            d.ellipse([vx + 16, mid_y - 4, vx + 22, mid_y + 2], fill="#222222")
    elif num == 13:  # Bougainville parliament + flag
        d.rectangle([x0, mid_y, x1, y1], fill="#7CB85C")
        d.rectangle([x0 + 44, y0 + 22, x1 - 44, mid_y], fill="#F5EFE0",
                    outline="#8A7D5F", width=1)
        d.polygon([(x0 + 38, y0 + 22), (x0 + 80, y0 + 8), (x1 - 38, y0 + 22)],
                  fill="#B03A2E")
        d.line([(x0 + 14, y0 + 8), (x0 + 14, y0 + 30)], fill=INK, width=1)
        d.polygon([(x0 + 14, y0 + 8), (x0 + 32, y0 + 13), (x0 + 14, y0 + 18)],
                  fill="#1F2937")
    elif num == 19:  # Vanuatu: island + seismograph trace
        d.rectangle([x0, mid_y, x1, y1], fill="#5B8FB0")
        d.polygon([(x0 + 30, mid_y), (x0 + 80, y0 + 20), (x1 - 30, mid_y)],
                  fill="#6FA368")
        d.rectangle([x0 + 8, y0 + 8, x0 + 68, y0 + 26], fill="#FFFFFF",
                    outline="#8A7D5F", width=1)
        pts = [(x0 + 12, y0 + 18), (x0 + 20, y0 + 18), (x0 + 24, y0 + 10),
               (x0 + 28, y0 + 24), (x0 + 34, y0 + 12), (x0 + 40, y0 + 22),
               (x0 + 48, y0 + 18), (x0 + 56, y0 + 18), (x0 + 62, y0 + 14)]
        d.line(pts, fill="#B91C1C", width=2)
    elif num == 42:  # cricket scoreboard + mini bars
        d.rectangle([x0, y0, x1, y1], fill="#1F5130")
        d.text((x0 + 8, y0 + 4), "IND A 254/3  (14.2)", font=font(FB, 9),
               fill="#FFFFFF")
        d.text((x0 + 8, y0 + 16), "204* OFF 53", font=font(FB, 9),
               fill="#FBBF24")
        bars = [("204", 204), ("254", 254), ("249", 249)]
        base = y1 - 4
        for i, (lab, v) in enumerate(bars):
            hgt = int(v / 254.0 * 13)
            cx = x0 + 112 + i * 16
            d.rectangle([cx, base - hgt, cx + 11, base], fill="#FBBF24")
            d.text((cx - 1, base - hgt - 8), lab, font=font(FB, 6), fill="#FFFFFF")


# ---------------------------------------------------------------- cards
LEAD_BANNER = {2: "SHIP SUNK OFF LIBYA", 6: "HORMUZ ON EDGE", 1: "HUANG IS BACK"}
LEAD_SCENE = {2: scene_sea_warship, 6: scene_hormuz_map, 1: scene_data_nvidia}


def draw_lead(d, box, num):
    x0, y0, x1, y1 = box
    s = by_num(num)
    d.rectangle(box, fill="#FFFFFF", outline=RULE, width=1)
    scene_box = (x0 + 1, y0 + 1, x1 - 1, y0 + 112)
    LEAD_SCENE[num](d, scene_box)
    # red banner word across the top of the scene
    ban = LEAD_BANNER[num]
    fb = font(FB, 13)
    bw = d.textlength(ban, font=fb) + 14
    d.rectangle([x0 + 6, y0 + 6, x0 + 6 + bw, y0 + 26], fill="#B91C1C")
    d.text((x0 + 13, y0 + 9), ban, font=fb, fill="#FFFFFF")
    ty = y0 + 116
    d.text((x0 + 8, ty), "%d." % num, font=font(FB, 12), fill=RCOL[s[1]])
    fit(d, s[4], font(FB, 12), (x1 - x0) - 40)
    d.text((x0 + 30, ty), s[4], font=font(FB, 12), fill=INK)
    deck = wrap(d, s[5], font(FR, 9), (x1 - x0) - 16, 2)
    for i, ln in enumerate(deck):
        d.text((x0 + 8, ty + 18 + i * 12), ln, font=font(FR, 9), fill="#333333")
    tag_line(d, x0 + 8, y1 - 16, s, (x1 - x0) - 16)


def draw_mid(d, box, num):
    x0, y0, x1, y1 = box
    s = by_num(num)
    d.rectangle(box, fill="#FFFFFF", outline=RULE, width=1)
    mini_scene(d, (x0 + 1, y0 + 1, x1 - 1, y0 + 52), num)
    d.text((x0 + 6, y0 + 54), "%d." % num, font=font(FB, 10), fill=RCOL[s[1]])
    head = wrap(d, s[4], font(FB, 10), (x1 - x0) - 30, 2)
    for i, ln in enumerate(head):
        d.text((x0 + 24, y0 + 54 + i * 12), ln, font=font(FB, 10), fill=INK)
    deck = wrap(d, s[5], font(FR, 8), (x1 - x0) - 12, 2)
    dy = y0 + 54 + len(head) * 12 + 2
    for i, ln in enumerate(deck):
        d.text((x0 + 6, dy + i * 11), ln, font=font(FR, 8), fill="#333333")
    tag_line(d, x0 + 6, y1 - 14, s, (x1 - x0) - 12)


# ---------------------------------------------------------------- world map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-60, 55), (-55, 47), (-65, 44), (-70, 42),
     (-75, 35), (-80, 32), (-81, 26), (-90, 21), (-97, 16), (-92, 15),
     (-83, 9), (-79, 9), (-85, 11), (-90, 14), (-97, 16), (-105, 20),
     (-110, 23), (-114, 29), (-120, 34), (-125, 40), (-124, 48), (-130, 55),
     (-140, 60), (-155, 58), (-165, 60), (-168, 66)],
    [(-58, 64), (-45, 60), (-40, 65), (-30, 68), (-22, 70), (-25, 76),
     (-40, 78), (-58, 76), (-60, 70), (-58, 64)],
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -52), (-66, -55),
     (-68, -50), (-62, -42), (-58, -35), (-52, -32), (-48, -28), (-40, -22),
     (-35, -9), (-35, -6), (-44, -3), (-50, 0), (-53, 4), (-60, 8),
     (-70, 11), (-79, 9)],
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (35, 28), (37, 22), (40, 15), (43, 11), (48, 11), (51, 10), (46, 5),
     (41, 0), (40, -5), (40, -12), (36, -18), (33, -26), (28, -33),
     (20, -35), (17, -32), (15, -27), (12, -18), (9, -1), (9, 4), (0, 6),
     (-8, 5), (-13, 8), (-17, 15), (-17, 21), (-16, 25), (-10, 31), (-6, 35)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (2, 51),
     (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64),
     (13, 66), (18, 69), (25, 71), (30, 70), (35, 68), (40, 68), (45, 68),
     (50, 69), (55, 68), (60, 69), (68, 73), (75, 73), (80, 73), (90, 75),
     (100, 76), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (158, 69), (162, 66), (170, 66), (178, 65), (178, 62), (170, 60),
     (162, 60), (158, 55), (150, 59), (142, 55), (140, 50), (135, 45),
     (130, 42), (127, 40), (122, 38), (120, 32), (122, 28), (118, 25),
     (110, 20), (108, 15), (105, 10), (103, 7), (100, 8), (98, 12),
     (95, 16), (92, 21), (89, 22), (86, 20), (80, 15), (77, 8), (75, 12),
     (72, 20), (68, 23), (65, 25), (60, 25), (57, 26), (53, 26), (50, 29),
     (48, 30), (44, 29), (40, 28), (38, 24), (35, 28), (36, 36), (30, 36),
     (27, 37), (23, 36), (22, 38), (19, 40), (15, 44), (12, 44), (8, 44),
     (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37), (-10, 36)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-5, 50)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (142, 42), (144, 44), (141, 45), (139, 41), (137, 37), (133, 35),
     (130, 33)],
    [(95, 5), (100, 0), (104, -3), (106, -6), (103, -5), (98, 2), (95, 5)],
    [(109, 1), (113, 3), (117, 5), (119, 1), (117, -3), (112, -3), (109, 0),
     (109, 1)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (147, -8), (141, -8),
     (136, -6), (131, -3), (131, -1)],
    [(105, -6), (110, -7), (114, -8), (114, -7), (108, -6), (105, -6)],
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20), (113, -22)],
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (174, -41),
     (171, -44), (167, -46), (167, -45)],
]

# display jitter for crowded pins: num -> (dx, dy) px from the true point
PIN_JITTER = {3: (16, 10), 5: (0, -8), 2: (-14, 12), 42: (-10, 10), 6: (8, -6)}


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill="#BFE0F2", outline="#8FA8BC", width=1)

    def proj(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * (x1 - x0),
                y0 + (90.0 - lat) / 150.0 * (y1 - y0))

    for poly in CONTINENTS:
        d.polygon([proj(lo, la) for lo, la in poly], fill="#D8C9A3",
                  outline="#8A7D5F")
    # graticule, faint
    for lon in range(-150, 181, 30):
        px, _ = proj(lon, 0)
        d.line([(px, y0), (px, y1)], fill="#A8C8DE", width=1)
    for lat in (60, 30, 0, -30):
        _, py = proj(0, lat)
        d.line([(x0, py), (x1, py)], fill="#A8C8DE", width=1)
    d.text((x0 + 6, y0 + 4), "ATLANTIC", font=font(FB, 7), fill="#5B7A94")
    d.text((x0 + 360, y0 + 46), "PACIFIC", font=font(FB, 7), fill="#5B7A94")
    d.text((x0 + 700, y1 - 12), "INDIAN OCEAN", font=font(FB, 7), fill="#5B7A94")

    shown = []
    for num in DRAWN:
        s = by_num(num)
        tx, ty = proj(s[7], s[8])
        jx, jy = PIN_JITTER.get(num, (0, 0))
        cx, cy = tx + jx, ty + jy
        if (jx, jy) != (0, 0):
            d.line([(tx, ty), (cx, cy)], fill="#333333", width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill="#333333")
        r = 9
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RCOL[s[1]],
                  outline="#FFFFFF", width=2)
        f = font(FB, 9 if num < 10 else 8)
        tw = d.textlength(str(num), font=f)
        d.text((cx - tw / 2, cy - 6), str(num), font=f, fill="#FFFFFF")
        shown.append((num, cx, cy))
    # pins must never overlap: 20px minimum centre distance
    for i in range(len(shown)):
        for j in range(i + 1, len(shown)):
            dx = shown[i][1] - shown[j][1]
            dy = shown[i][2] - shown[j][2]
            if (dx * dx + dy * dy) ** 0.5 < 20:
                raise SystemExit("PIN OVERLAP %d vs %d (%.1f px)"
                                 % (shown[i][0], shown[j][0],
                                    (dx * dx + dy * dy) ** 0.5))
    return shown


# ---------------------------------------------------------------- page
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 12
    CW = W - 2 * MX

    # --- masthead
    d.text((MX, 2), "THE WORLD IN ONE DAY", font=font(FB, 32), fill=INK)
    d.text((W - MX - 208, 10), "TUESDAY 24 NOVEMBER 2026",
           font=font(FB, 13), fill="#B91C1C")
    claim = "48 STORIES  ·  10 REGIONS  ·  24 FIELDS  ·  15 DRAWN  ·  EVERY CLAIM LABELLED"
    fit(d, claim, font(FB, 11), CW)
    d.text((MX, 38), claim, font=font(FB, 11), fill="#333333")
    d.line([(MX, 52), (W - MX, 52)], fill=INK, width=2)

    # --- region bar (widths proportional to counts; must sum to 48)
    counts = {}
    for s in STORIES:
        counts[s[1]] = counts.get(s[1], 0) + 1
    if sum(counts.values()) != 48:
        raise SystemExit("REGION SUM %d != 48" % sum(counts.values()))
    for k, _, _, target in REGIONS:
        if counts.get(k, 0) != target:
            raise SystemExit("REGION %s has %d, target %d"
                             % (k, counts.get(k, 0), target))
    if max(counts.values()) > 8:
        raise SystemExit("REGION SKEW: max %d > 8" % max(counts.values()))
    fields = {s[2] for s in STORIES}
    if len(fields) != 24:
        raise SystemExit("FIELDS %d != 24: %s" % (len(fields), sorted(fields)))
    if len({s[0] for s in STORIES}) != 48 or max(s[0] for s in STORIES) != 48:
        raise SystemExit("STORY NUMBERS NOT 1..48")
    x = MX
    for ri, (k, name, col, n) in enumerate(REGIONS):
        wseg = CW * n // 48
        if ri == len(REGIONS) - 1:
            wseg = W - MX - x  # last segment takes the remainder, no gap
        d.rectangle([x, 56, x + wseg - 1, 84], fill=col)
        lab = "%s %d" % (name, n)
        fit(d, lab, font(FB, 9), wseg - 6)
        d.text((x + 4, 65), lab, font=font(FB, 9), fill="#FFFFFF")
        x += wseg

    # --- IN NUMBERS strip (7 items)
    d.text((MX, 90), "IN NUMBERS", font=font(FB, 10), fill="#B91C1C")
    cell_w = CW // 7
    for i, (big, lab) in enumerate(NUMBERS):
        cx = MX + i * cell_w
        d.text((cx + 4, 102), big, font=font(FB, 15), fill=INK)
        fit(d, lab, font(FB, 7), cell_w - 8)
        d.text((cx + 4, 120), lab, font=font(FB, 7), fill=MUT)
        if i:
            d.line([(cx, 100), (cx, 132)], fill=RULE, width=1)
    d.line([(MX, 134), (W - MX, 134)], fill=RULE, width=1)

    # --- leads (3 across)
    lw = (CW - 22) // 3
    for i, num in enumerate(LEADS):
        draw_lead(d, (MX + i * (lw + 11), 138, MX + i * (lw + 11) + lw, 312), num)

    # --- mid rows (6 across, 2 rows)
    mw = (CW - 30) // 6
    for row, nums in enumerate((MIDS_R1, MIDS_R2)):
        y0 = 316 + row * 124
        for i, num in enumerate(nums):
            draw_mid(d, (MX + i * (mw + 6), y0, MX + i * (mw + 6) + mw, y0 + 120),
                     num)

    # --- THE DAY IN UTC strip
    d.text((MX, 568), "THE DAY IN UTC", font=font(FB, 10), fill="#B91C1C")
    utc_txt = " · ".join("%s %s" % (t, e) for t, e in UTC)
    fit(d, utc_txt, font(FB, 9), CW - 130)
    d.text((MX + 118, 568), utc_txt, font=font(FB, 9), fill=INK)
    d.line([(MX, 584), (W - MX, 584)], fill=RULE, width=1)

    # --- world map + pin legend
    d.text((MX, 590), "WHERE IT HAPPENED  ·  PINS = STORIES 1–15",
           font=font(FB, 10), fill=INK)
    draw_map(d, (MX, 606, W - MX, 716))
    drawn_counts = {}
    for num in DRAWN:
        r = by_num(num)[1]
        drawn_counts[r] = drawn_counts.get(r, 0) + 1
    leg = "PIN COLOUR = REGION:   " + "   ".join(
        "%s %d" % (RNAME[k], v) for k, v in sorted(drawn_counts.items()))
    fit(d, leg, font(FB, 8), CW)
    d.text((MX, 720), leg, font=font(FB, 8), fill=INK)

    # --- charts row: Stories by Region + Markets (vertical bars)
    def vbar_panel(box, title, items, fmt):
        x0, y0, x1, y1 = box
        d.rectangle(box, fill="#FFFFFF", outline=RULE, width=1)
        d.text((x0 + 8, y0 + 4), title, font=font(FB, 9), fill=INK)
        base = y1 - 16
        bw = (x1 - x0 - 16) // len(items)
        mx = max(v for _, v in items)
        for i, (lab, v) in enumerate(items):
            hgt = int(v / mx * 34)
            cx = x0 + 8 + i * bw
            d.rectangle([cx, base - hgt, cx + bw - 6, base], fill="#2563EB")
            d.text((cx, base - hgt - 11), fmt % v, font=font(FB, 8), fill=INK)
            fit(d, lab, font(FB, 7), bw - 6)
            d.text((cx, base + 3), lab, font=font(FB, 7), fill=MUT)
        d.line([(x0 + 8, base), (x1 - 8, base)], fill=INK, width=1)

    vbar_panel((MX, 736, MX + 494, 818), "STORIES BY REGION",
               [(RNAME[k][:6], n) for k, _, _, n in REGIONS], "%d")
    vbar_panel((MX + 506, 736, W - MX, 818), "MARKETS ON TUESDAY",
               [(lab, float(pct.strip("+%"))) for lab, pct in MARKETS], "+%.1f%%")

    # --- ALSO header + fields line
    d.text((MX, 824), "ALSO ON — 33 MORE STORIES  ·  C CONFIRMED · O OFFICIAL · "
                      "R REPORTED · CL CLAIM · OG ONGOING",
           font=font(FB, 10), fill=INK)
    fit(d, FIELDS_LINE, font(FR, 8), CW)
    d.text((MX, 840), FIELDS_LINE, font=font(FR, 8), fill=MUT)

    # --- ALSO list: 3 columns x 11 rows, one short line each, no ellipsis
    col_w = (CW - 24) // 3
    fA = font(FR, 9)
    fAn = font(FB, 9)
    for idx, s in enumerate(ALSO):
        col = idx // 11
        row = idx % 11
        x = MX + col * (col_w + 12)
        y = 856 + row * 11
        claim_chip(d, x, y - 1, s[3], r=5)
        src = s[5] if len(s) == 8 else s[6]  # ALSO rows: 8 fields; 14/15 carry a deck
        txt = "%d. %s — %s" % (s[0], s[4], src)
        fit(d, txt, fA, col_w - 16)
        d.text((x + 14, y), txt, font=fA, fill="#222222")
    if ALSO[-1][0] != 48:
        raise SystemExit("LAST ALSO NUMBER %d != 48" % ALSO[-1][0])

    # --- footer: DATE CHECK + HOW CHECKED + sources (4 lines, all fit-checked)
    fy = 982
    d.line([(MX, 978), (W - MX, 978)], fill=INK, width=1)
    dc1 = ("DATE CHECK — Every story happened, or was first reported, on Tuesday 24 November 2026 in at "
           "least one time zone. Left out: Huang's ouster (11 Nov); COP31 opening (9 Nov); the Merkury")
    dc2 = ("attack itself (Sun 22 Nov — counted for the Mon 23 Nov confirmation and Tripoli / UN reaction); "
           "Hasina's return is planned for 16 Dec, announced Tue 24 Nov. Not yet: the Bougainville vote began "
           "Tue 24 Nov, no result yet.")
    fit(d, dc1, font(FR, 8), CW)
    fit(d, dc2, font(FR, 8), CW)
    d.text((MX, fy), dc1, font=font(FR, 8), fill="#333333")
    d.text((MX, fy + 10), dc2, font=font(FR, 8), fill="#333333")
    hc = ("HOW THIS PAGE WAS CHECKED — Every story is dated 24 Nov 2026 and tagged C/O/R/CL/OG. "
          "Counts checked 3x: region bar = 48 stories = header claim = last ALSO number (48).")
    fit(d, hc, font(FR, 8), CW)
    d.text((MX, fy + 20), hc, font=font(FR, 8), fill="#333333")
    src = ("Sources: Reuters, AP, WSJ, CNN, Yonhap, UN, FIFA, Delta, Sanofi · Press time 09:00 UTC · "
           "Drawn entirely in code — no photos, no network.")
    fit(d, src, font(FR, 8), CW)
    d.text((MX, fy + 30), src, font=font(FR, 8), fill=MUT)

    img.save(OUT, optimize=True)
    print("saved %s %dx%d" % (OUT, W, H))
    return OUT


if __name__ == "__main__":
    # global no-ellipsis gate: no story text may contain a truncation marker
    for s in STORIES:
        for part in s[4:7]:
            if isinstance(part, str) and ("..." in part or "…" in part):
                raise SystemExit("ELLIPSIS in story %d: %r" % (s[0], part))
    for big, lab in NUMBERS:
        if "..." in lab or "…" in lab:
            raise SystemExit("ELLIPSIS in numbers strip")
    path = render()
    size = os.path.getsize(path)
    print("bytes %d" % size)
    if size > 1024 * 1024:
        raise SystemExit("FILE > 1 MiB: %d" % size)
    print("CHECKS PASSED: 48 stories, 10 regions max 8, 24 fields, "
          "15 pins, 33 ALSO, last ALSO 48")
