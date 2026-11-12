#!/usr/bin/env python3
"""Reconstructed offline zine builder, based on the recovered project script."""
import argparse
import html
import json
from pathlib import Path

KINDS = {"flow", "stack", "tags", "papers"}


def text(value, where):
    if not isinstance(value, str):
        raise ValueError(f"{where} must be a string")


def pairs(value, where):
    if not isinstance(value, list):
        raise ValueError(f"{where} must be an array")
    for pair in value:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError(f"{where} entries must be [heading, body] pairs")
        for item in pair:
            text(item, where)


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("root must be an object")
    for key in ("series", "brand"):
        text(data.get(key), key)
    if not isinstance(data.get("pages"), list) or not data["pages"]:
        raise ValueError("pages must be a nonempty array")
    for n, page in enumerate(data["pages"], 1):
        if not isinstance(page, dict):
            raise ValueError(f"page {n} must be an object")
        for key in ("title", "intro", "source"):
            text(page.get(key), f"page {n}.{key}")
        for key in ("sub", "checktitle", "closing"):
            if key in page:
                text(page[key], key)
        pairs(page.get("checks", []), "checks")
        if not isinstance(page.get("blocks"), list):
            raise ValueError("blocks must be an array")
        for block in page["blocks"]:
            if not isinstance(block, dict):
                raise ValueError("block must be an object")
            for key in ("title", "kind", "caption"):
                text(block.get(key), key)
            if block["kind"] not in KINDS:
                raise ValueError("kind must be flow, stack, tags, or papers")
            for key in ("label", "panel"):
                if key in block:
                    text(block[key], key)
            color = block.get("color", 0)
            if type(color) is not int or not 0 <= color <= 5:
                raise ValueError("color must be an integer from 0 through 5")
            for key in ("paras", "items"):
                if not isinstance(block.get(key), list):
                    raise ValueError(f"{key} must be an array")
                for item in block[key]:
                    text(item, key)
            pairs(block.get("rows", []), "rows")
    return data


def escape(value):
    return html.escape(value, quote=True).replace("\n", "<br>")


def element(tag, value, cls):
    return f'<{tag} class="{cls}">{escape(value)}</{tag}>'


def page_html(data, page, number):
    blocks = []
    for block in page["blocks"]:
        label = element("div", block["label"], "label") if block.get("label") else ""
        prose = "".join(element("p", p, "paragraph") for p in block["paras"])
        items = "".join(f'<div class="item"><b>{i:02}</b>{escape(t)}</div>'
                        for i, t in enumerate(block["items"], 1))
        rows = "".join('<div class="panel-row">' + element("div", a, "row-label") +
                       element("div", b, "row-body") + "</div>" for a, b in block.get("rows", []))
        panel = element("div", block.get("panel", "IDEA / STRUCTURE"), "graphic-title")
        blocks.append(f'<section class="block c{block.get("color", 0)}"><div>{label}' +
                      element("h2", block["title"], "block-title") + prose +
                      f'</div><div class="graphic {block["kind"]}">{panel}<div class="items">{items}</div>{rows}' +
                      element("div", block["caption"], "caption") + "</div></section>")
    checks = "".join("<div>" + element("div", a, "check-label") +
                     element("div", b, "check-body") + "</div>" for a, b in page.get("checks", []))
    checklist = (element("h2", page["checktitle"], "checktitle") if page.get("checktitle") else "")
    if checks:
        checklist += f'<div class="checks">{checks}</div>'
    sub = element("div", page["sub"], "section") if page.get("sub") else ""
    closing = element("div", page["closing"], "closing") if page.get("closing") else ""
    body = ('<main class="sheet"><div class="mast">' + element("span", data["series"], "series") +
            element("span", data["brand"], "brand") + "</div>" + sub +
            element("h1", page["title"], "title") + element("div", page["intro"], "intro") +
            "".join(blocks) + checklist + closing + '<footer class="footer">' +
            element("div", page["source"], "source") +
            f'<div class="num">{number:02} <span>/ {len(data["pages"]):02}</span></div></footer></main>')
    return ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">' +
            '<meta name="viewport" content="width=device-width, initial-scale=1">' +
            f'<title>{escape(page["title"])}</title><link rel="stylesheet" href="style.css">' +
            "</head><body>" + body + "</body></html>")


def build(source, out):
    data = validate(json.loads(source.read_text(encoding="utf-8")))
    # A fresh output directory prevents stale page PNG files being mistaken for this build.
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError("--out must be a new or empty directory")
    out.mkdir(parents=True, exist_ok=True)
    css = Path(__file__).resolve().parent.parent / "assets" / "style.css"
    (out / "style.css").write_text(css.read_text(encoding="utf-8"), encoding="utf-8")
    for n, page in enumerate(data["pages"], 1):
        (out / f"page-{n:02}.html").write_text(page_html(data, page, n), encoding="utf-8")
    return len(data["pages"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        count = build(args.content, args.out)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"build: {exc}\n")
    print(f"Built {count} HTML pages in {args.out}")


if __name__ == "__main__":
    main()
