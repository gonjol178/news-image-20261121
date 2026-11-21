"""The Morning Atlas — compositor for news-image-20261121.

Builds entry.png (1024x1024), a one-page broadsheet for Saturday,
21 November 2026, from three photo panels generated in-session plus
typeset headlines. Run:  python3 build_atlas.py [output-path]
Deterministic: same inputs always produce the same bytes.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

W = H = 1024
MARGIN = 30
CONTENT = W - 2 * MARGIN

PAPER = (250, 246, 236)
INK = (26, 26, 22)
TEAL = (13, 77, 74)
TEAL_DARK = (9, 58, 56)
MUTED = (96, 92, 82)
FAINT = (196, 190, 176)

FONTS = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(str(Path(FONTS) / name), size)
    except OSError:
        return ImageFont.load_default(size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    leading = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, width, fill=TEAL, px=2):
    draw.rectangle([x, y, x + width, y + px - 1], fill=fill)


def kicker(draw, x, y, text, size=15):
    fnt = SANS_B(size)
    draw.text((x, y), text.upper(), font=fnt, fill=TEAL)
    return y + int(size * 1.5)


def cover_crop(img, tw, th):
    """Centre-crop to the target aspect, then resize."""
    sw, sh = img.size
    target = tw / th
    if sw / sh > target:
        nw = int(sh * target)
        box = ((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh)
    else:
        nh = int(sw / target)
        box = (0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh)
    return img.crop(box).resize((tw, th), Image.LANCZOS)


def photo(draw, canvas, path, x, y, w, h, caption=None):
    img = Image.open(path).convert("RGB")
    canvas.paste(cover_crop(img, w, h), (x, y))
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=TEAL_DARK, width=2)
    if caption:
        draw.text((x, y + h + 5), caption, font=SERIF_I(13), fill=MUTED)


def build():
    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)

    # ---- Masthead -------------------------------------------------
    rule(d, MARGIN, 22, CONTENT, px=3)
    mast = SERIF_B(58)
    title = "THE MORNING ATLAS"
    d.text(((W - d.textlength(title, font=mast)) / 2, 32), title,
           font=mast, fill=INK)
    date_f = SANS_B(19)
    date_t = "SATURDAY, 21 NOVEMBER 2026"
    sub_f = SANS(19)
    sub_t = "  \u2022  WORLD NEWS IN ONE PAGE"
    total = d.textlength(date_t, font=date_f) + d.textlength(sub_t, font=sub_f)
    x = (W - total) / 2
    d.text((x, 104), date_t, font=date_f, fill=TEAL)
    d.text((x + d.textlength(date_t, font=date_f), 104), sub_t,
           font=sub_f, fill=MUTED)
    rule(d, MARGIN, 134, CONTENT, px=2)
    rule(d, MARGIN, 139, CONTENT, fill=FAINT, px=1)

    # ---- Lead story: photo LEFT, headline column RIGHT -----------
    y = 154
    hague = ASSETS / "media-generation-panel-hague-0-b96087b0-e917-40ba-bb9c-3823207c0891.webp"
    photo(d, canvas, hague, MARGIN, y, 440, 264,
          caption="The Peace Palace, The Hague.")
    rx, rw = 492, 502
    y2 = kicker(d, rx, y, "The Hague \u2014 Lead story")
    y2 = para(d, rx, y2 + 4,
              "World court: Myanmar committed genocidal acts against the Rohingya",
              SERIF_B(33), rw, leading=40)
    y2 = para(d, rx, y2 + 8,
              "The International Court of Justice delivers a landmark verdict "
              "in The Hague. Rohingya rejoice \u2014 and the UK expels Myanmar\u2019s "
              "diplomat and demands accountability.",
              SANS(16), rw, fill=(58, 56, 48), leading=21)

    # ---- Divider --------------------------------------------------
    rule(d, MARGIN, 448, CONTENT, fill=FAINT, px=1)

    # ---- Second row: two photo stories ----------------------------
    y = 462
    col_w = 472
    kyiv = ASSETS / "media-generation-panel-kyiv-0-60b6f2a1-d57b-4bfb-bddb-8fe935c36582.webp"
    london = ASSETS / "media-generation-panel-london-0-073caac3-5391-43a1-a807-eae86c72ca92.webp"
    photo(d, canvas, kyiv, MARGIN, y, col_w, 168)
    photo(d, canvas, london, MARGIN + col_w + 20, y, col_w, 168)
    y2 = y + 168 + 8
    kicker(d, MARGIN, y2, "Kyiv / Warsaw")
    kicker(d, MARGIN + col_w + 20, y2, "London / Brussels")
    hy = y2 + 22
    end_l = para(d, MARGIN, hy, "Mass strike hits three Kyiv bridges",
                 SERIF_B(23), col_w, leading=28)
    end_r = para(d, MARGIN + col_w + 20, hy,
                 "UK and EU strike \u2018landmark\u2019 deal to rebuild ties",
                 SERIF_B(23), col_w, leading=28)
    dy = max(end_l, end_r) + 4
    para(d, MARGIN, dy,
         "A Russian missile crosses into Polish airspace during allied "
         "military exercises. Prime Minister Tusk confirms the incursion.",
         SANS(14), col_w, fill=(58, 56, 48), leading=18)
    para(d, MARGIN + col_w + 20, dy,
         "London and Brussels agree a new pact to rebuild relations after Brexit.",
         SANS(14), col_w, fill=(58, 56, 48), leading=18)

    # ---- Third row: two text stories ------------------------------
    rule(d, MARGIN, 766, CONTENT, fill=FAINT, px=1)
    y = 780
    kicker(d, MARGIN, y, "Washington")
    kicker(d, MARGIN + col_w + 20, y, "Baghdad")
    y += 22
    para(d, MARGIN, y, "\u2018We\u2019ve got time\u2019",
         SERIF_B(21), col_w, leading=26)
    para(d, MARGIN + col_w + 20, y, "Iraqi forces retake Jurf al-Sakhar",
         SERIF_B(21), col_w, leading=26)
    y += 30
    para(d, MARGIN, y, "Trump signals the Iran war could continue into 2027.",
         SANS(14), col_w, fill=(58, 56, 48), leading=18)
    para(d, MARGIN + col_w + 20, y,
         "The town returns to government control after 12 years under "
         "Kataib Hezbollah.",
         SANS(14), col_w, fill=(58, 56, 48), leading=18)

    # ---- In brief --------------------------------------------------
    y = 876
    chip = "IN BRIEF"
    chip_f = SANS_B(15)
    chip_w = d.textlength(chip, font=chip_f) + 20
    d.rectangle([MARGIN, y, MARGIN + chip_w, y + 24], fill=TEAL)
    d.text((MARGIN + 10, y + 4), chip, font=chip_f, fill=PAPER)
    y += 32
    briefs = [
        ("BRUSSELS", "EU adds \u20ac1 billion for Ukrainian drones and air defence."),
        ("COPENHAGEN", "Denmark approves a security agreement with the US and Greenland."),
        ("NEW YORK", "Tech sell-off drags markets as Anthropic shares slide."),
        ("WASHINGTON", "Report: US floats NATO membership for Ukraine in return for territorial concessions."),
    ]
    row_h = 0
    for i, (city, text) in enumerate(briefs):
        bx = MARGIN + (i % 2) * (col_w + 20)
        by = y + (i // 2) * 32
        d.text((bx, by), "\u25aa ", font=SANS_B(13), fill=TEAL)
        cx = bx + 14
        d.text((cx, by), city + " \u2014 ", font=SANS_B(13), fill=INK)
        off = d.textlength(city + " \u2014 ", font=SANS_B(13))
        lines = wrap(d, text, SANS(13), col_w - 14 - off)
        yy = by
        for j, line in enumerate(lines):
            d.text((cx + (off if j == 0 else 0), yy), line,
                   font=SANS(13), fill=(58, 56, 48))
            yy += 16
        row_h = max(row_h, yy - by)

    # ---- Footer ----------------------------------------------------
    rule(d, MARGIN, 976, CONTENT, fill=FAINT, px=1)
    foot = ("Sources: Binder Global News \u2022 La M\u00e9diterran\u00e9e \u2022 "
            "KSPearls \u2022 R\u00e9seau ADSI \u2022 Jabulani Radio international desk")
    ff = SANS(11)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 984), foot,
           font=ff, fill=MUTED)
    tag = "THE MORNING ATLAS \u2014 ONE DAY. ONE PAGE."
    tf = SANS_B(11)
    d.text(((W - d.textlength(tag, font=tf)) / 2, 1000), tag,
           font=tf, fill=TEAL)

    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "entry.png"
    canvas.save(out, "PNG", optimize=True)
    size = out.stat().st_size
    print(f"wrote {out} {size} bytes")
    if size > 1_048_576:
        canvas.save(out, "JPEG", quality=88, optimize=True)
        print(f"PNG over 1 MiB; re-saved as JPEG bytes: {out.stat().st_size}")


if __name__ == "__main__":
    build()
