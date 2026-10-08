#!/usr/bin/env python3
"""Generate index.html from index.template.html + variants.json.

The download rows are plain static HTML. Run from the repo root (dpx/):
    python3 tools/build.py
Pass --check to fail if the committed index.html is out of date.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "<!-- @@DOWNLOAD_SECTIONS@@ -->"
ZIP_ICON = '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" class="icon-inline"><path d="M6 1V8M6 8L3 5M6 8L9 5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 10.5H10" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>'
# (label, css class, folder, file suffix) in display order
BUTTONS = [("SVG", "dl-btn-svg", "svg", ".svg"), ("PNG", "dl-btn-png", "png", ".png"),
           ("PNG 2x", "dl-btn-png", "png", "@2x.png"), ("PDF", "dl-btn-pdf", "docs", ".pdf"),
           ("AI", "dl-btn-ai", "source", ".ai")]


def row(item):
    f = item["file"]
    buttons = "".join(f'<a class="dl-btn {cls}" href="assets/{folder}/{f}{ext}" download>{label}</a>'
                      for label, cls, folder, ext in BUTTONS)
    # alt="" is intentional: the visible name next to the thumbnail describes it
    return (f'    <div class="dl-row"><div class="dl-left"><div class="dl-preview dl-preview-{item["preview"]}">'
            f'<img src="assets/png/{f}.png" alt=""></div>'
            f'<div class="dl-info"><span class="dl-name">{item["name"]}</span>'
            f'<span class="dl-desc">{item["desc"]}</span></div></div>'
            f'<div class="dl-buttons">{buttons}</div></div>\n')


def section(sec):
    head = (f'  <div class="section-title section-title-with-action" id="{sec["id"]}"><span>{sec["title"]}</span>'
            f'<div class="section-title-actions"><a class="section-title-zip" href="assets/packages/{sec["zip"]}" download>'
            f'Download ZIP{ZIP_ICON}</a></div></div>\n  <div class="dl-section-card">\n')
    return head + "".join(row(r) for r in sec["rows"]) + "  </div>\n"


def build():
    data = json.loads((ROOT / "variants.json").read_text())
    template = (ROOT / "index.template.html").read_text()
    assert template.count(MARKER) == 1, "template must contain exactly one marker"
    return template.replace("  " + MARKER + "\n", "\n".join(section(s) for s in data["sections"]))


if __name__ == "__main__":
    html = build()
    target = ROOT / "index.html"
    if "--check" in sys.argv:
        sys.exit(0 if target.read_text() == html else "index.html is out of date; run tools/build.py")
    target.write_text(html)
    print(f"wrote {target.name} ({len(html) // 1024} KB)")
