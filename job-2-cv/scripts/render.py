#!/usr/bin/env python3
"""
Render an HTML CV to PDF using Playwright (headless Chromium).

Usage:
  .venv/bin/python <skill>/scripts/render.py <html_file>

Output: a .pdf file alongside the HTML (same basename).
Respects @page CSS rules (size, margin) via prefer_css_page_size.
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def render(html_path: Path) -> Path:
    html_path = html_path.resolve()
    if not html_path.exists():
        raise FileNotFoundError(html_path)

    pdf_path = html_path.with_suffix(".pdf")
    file_url = html_path.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto(file_url, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.emulate_media(media="print")

        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
        )

        browser.close()

    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: render.py <html_file>", file=sys.stderr)
        sys.exit(2)

    out = render(Path(sys.argv[1]))
    print(f"wrote {out}")
