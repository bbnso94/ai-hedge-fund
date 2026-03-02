from __future__ import annotations

import math
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT_PDF = DOCS / "peoria_garden_plan_2026.pdf"
PREVIEW = DOCS / "images" / "peoria_garden_plan_preview.png"

PAGE_SIZE = (1654, 2339)  # A4 at 150 DPI
MARGIN = 100


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    font: ImageFont.ImageFont,
    fill: str,
    width_px: int,
    line_spacing: int = 10,
) -> int:
    x, y = xy
    words = text.split()
    line: list[str] = []
    for word in words:
        trial = " ".join([*line, word])
        if draw.textlength(trial, font=font) <= width_px or not line:
            line.append(word)
            continue
        draw.text((x, y), " ".join(line), font=font, fill=fill)
        y += font.size + line_spacing
        line = [word]
    if line:
        draw.text((x, y), " ".join(line), font=font, fill=fill)
        y += font.size + line_spacing
    return y


def flower_tile(title: str, subtitle: str, colors: tuple[str, str], seed_no: str) -> Image.Image:
    tile = Image.new("RGB", (480, 300), "#f5f7fb")
    d = ImageDraw.Draw(tile)
    d.rounded_rectangle((0, 0, 479, 299), radius=26, fill="#ffffff", outline="#d8dfef", width=4)

    d.rounded_rectangle((22, 22, 458, 178), radius=18, fill="#d9ecff")
    d.rectangle((22, 120, 458, 178), fill="#8dcf84")

    center_x = 240
    d.line((center_x, 170, center_x, 84), fill="#4f8f3d", width=8)

    petal, center = colors
    for angle in range(0, 360, 45):
        dx = int(38 * math.cos(math.radians(angle)))
        dy = int(38 * math.sin(math.radians(angle)))
        d.ellipse((center_x - 28 + dx, 70 - 28 + dy, center_x + 28 + dx, 70 + 28 + dy), fill=petal)
    d.ellipse((center_x - 26, 44, center_x + 26, 96), fill=center)

    d.text((24, 196), title, font=get_font(36, bold=True), fill="#15253f")
    d.text((24, 240), subtitle, font=get_font(24), fill="#425270")
    d.rounded_rectangle((375, 206, 461, 274), radius=14, fill="#2f6fe4")
    d.text((390, 228), seed_no, font=get_font(22, bold=True), fill="#ffffff")
    return tile


def create_page_1() -> Image.Image:
    img = Image.new("RGB", PAGE_SIZE, "#ffffff")
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, PAGE_SIZE[0], 430), fill="#133f8c")
    d.polygon([(0, 430), (PAGE_SIZE[0], 300), (PAGE_SIZE[0], 500), (0, 630)], fill="#1f5ec7")

    d.text((MARGIN, 90), "Peoria Garden Plan 2026", fill="#ffffff", font=get_font(74, bold=True))
    d.text((MARGIN, 196), "Seed packets #1-#9 | ZIP 61614", fill="#d7e6ff", font=get_font(34))

    box = (MARGIN, 470, PAGE_SIZE[0] - MARGIN, 850)
    d.rounded_rectangle(box, radius=28, fill="#f5f9ff", outline="#cfdbf2", width=3)
    d.text((box[0] + 30, box[1] + 26), "Frost-date anchors", font=get_font(38, bold=True), fill="#163460")

    y = box[1] + 90
    bullets = [
        "Average last spring frost (<=36F): April 27",
        "Average first fall frost (<=36F): October 14",
        "Safer warm-season planting target: May 11 (about 2 weeks after last frost)",
    ]
    for bullet in bullets:
        d.text((box[0] + 46, y), f"* {bullet}", font=get_font(33), fill="#1e314f")
        y += 72

    tiles = [
        flower_tile("Sunflower", "Direct sow in May", ("#ffd75a", "#6b4f2a"), "#1"),
        flower_tile("Marigold", "Start indoors in March", ("#f6a32d", "#905810"), "#2-3"),
        flower_tile("Beefsteak Tomato", "Indoor start is essential", ("#f77670", "#9d2019"), "#4-5"),
        flower_tile("Zinnia", "Direct sow after warm-up", ("#f07aca", "#6e2f6b"), "#6-7"),
        flower_tile("Nasturtium", "Low-fertility flower champ", ("#ff8f45", "#7d4526"), "#8-9"),
    ]

    x, y = MARGIN, 920
    for index, tile in enumerate(tiles):
        img.paste(tile, (x, y))
        x += tile.width + 30
        if index == 2:
            x = MARGIN
            y += tile.height + 30

    d.text(
        (MARGIN, PAGE_SIZE[1] - 70),
        f"Generated {date.today().isoformat()} | Built for Peoria, Illinois",
        font=get_font(24),
        fill="#5c6f91",
    )
    return img


def create_page_2() -> Image.Image:
    img = Image.new("RGB", PAGE_SIZE, "#fffefb")
    d = ImageDraw.Draw(img)
    d.text((MARGIN, 80), "2026 Planting Calendar", font=get_font(60, bold=True), fill="#273246")

    col_x = [MARGIN, 500, 1020, 1380]
    d.rounded_rectangle((MARGIN, 200, PAGE_SIZE[0] - MARGIN, 1940), radius=20, fill="#ffffff", outline="#d9d9d9", width=3)

    headers = ["#", "Seed type", "Indoor start", "Outdoor window"]
    for hx, text in zip(col_x, headers):
        d.text((hx, 240), text, font=get_font(29, bold=True), fill="#10223d")

    rows = [
        ("1", "Sunflower", "-", "May 1-May 25"),
        ("2-3", "Marigold", "Mar 2-Mar 16", "May 1-May 20"),
        ("4-5", "Beefsteak tomato", "Mar 2-Mar 16", "May 11-May 25"),
        ("6-7", "Zinnia (State Fair Giant)", "Apr 1-Apr 15 (optional)", "May 11-Jun 1"),
        ("8-9", "Nasturtium", "Mar 30-Apr 13 (optional)", "Apr 27-May 20"),
    ]

    y = 340
    for row in rows:
        d.line((MARGIN + 20, y - 20, PAGE_SIZE[0] - MARGIN - 20, y - 20), fill="#edf0f6", width=2)
        for i, text in enumerate(row):
            d.text((col_x[i], y), text, font=get_font(26), fill="#1f3352")
        y += 180

    d.rounded_rectangle((MARGIN, 1320, PAGE_SIZE[0] - MARGIN, 2090), radius=26, fill="#f7fbf4", outline="#cfe7c3", width=3)
    d.text((MARGIN + 30, 1360), "How to succeed in Peoria", font=get_font(34, bold=True), fill="#24451e")

    notes = [
        "Start tomatoes (#4-#5) indoors and transplant only after night temperatures stay above about 50F.",
        "Use full sun for tomato, sunflower, marigold, and zinnia beds.",
        "Late afternoon transplanting reduces stress and wilting.",
        "Harden indoor seedlings for 7-10 days before planting outside.",
        "For longer sunflower blooms, sow small batches every 2 weeks until early July.",
    ]
    ny = 1430
    for n in notes:
        ny = draw_wrapped(d, f"• {n}", (MARGIN + 38, ny), get_font(28), "#24451e", PAGE_SIZE[0] - 2 * MARGIN - 80, line_spacing=8)

    return img


def create_page_3() -> Image.Image:
    img = Image.new("RGB", PAGE_SIZE, "#ffffff")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, PAGE_SIZE[0], 300), fill="#264653")
    d.text((MARGIN, 96), "Packet-by-Packet Quick Guide", font=get_font(56, bold=True), fill="#f1f8f7")

    entries = [
        ("#1 Sunflower", "Direct sow 1 inch deep in May. Best window: May 11+."),
        ("#2-#3 Marigold", "Start indoors in early March for earlier blooms. Space 8-12 inches."),
        ("#4-#5 Beefsteak Tomato", "Start indoors 6-8 weeks before last frost. Transplant deeply in May."),
        ("#6-#7 Zinnia", "Direct sow when warm. Give giant varieties 12-18 inches for airflow."),
        ("#8-#9 Nasturtium", "Soak seed 8-12 hours. Avoid rich fertilizer for more flowers."),
    ]

    y = 380
    for title, desc in entries:
        d.rounded_rectangle((MARGIN, y, PAGE_SIZE[0] - MARGIN, y + 300), radius=24, fill="#f9fafc", outline="#dfe5ee", width=3)
        d.text((MARGIN + 28, y + 28), title, font=get_font(42, bold=True), fill="#1d2f4d")
        draw_wrapped(d, desc, (MARGIN + 32, y + 110), get_font(30), "#314867", PAGE_SIZE[0] - 2 * MARGIN - 60)
        y += 330

    d.text((MARGIN, PAGE_SIZE[1] - 130), "Tip: keep this PDF open on your phone while planting outside.", font=get_font(30), fill="#46505d")
    return img


def main() -> None:
    (DOCS / "images").mkdir(parents=True, exist_ok=True)
    pages = [create_page_1(), create_page_2(), create_page_3()]
    pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], resolution=150)
    pages[0].save(PREVIEW)
    print(f"Wrote {OUT_PDF}")
    print(f"Wrote {PREVIEW}")


if __name__ == "__main__":
    main()
