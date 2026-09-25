#!/usr/bin/env python3
"""Convert a Wiki.js 2.x export into MkDocs Material sources.

Input:
  --db      JSON dump of the Wiki.js SQLite tables (pages, tags, nav, assets, folders)
  --assets  directory with Wiki.js asset files (the "disk" storage export)
Output:
  docs/     markdown pages and referenced assets
  nav.yml   navigation derived from the Wiki.js site navigation

Wiki.js-specific markdown handled:
  > text {.is-info}           -> !!! info ""   (also is-warning / is-success / is-danger)
  ### Title {.tabset}         -> content tabs from the following sub-headings
  - [..](..)\n{.links-list}   -> Material grid cards
  ![](img.png =35%x)          -> ![](img.png){ style="width:35%" }
  /path and /en/path links    -> relative links to .md files / assets
"""
import argparse
import json
import os
import posixpath
import re
import shutil
import sys

import markdownify
import yaml

SKIP_PAGES = {
    "test-stream",        # test page with an iframe, not documentation
    "app/nix_workflow",   # unpublished in Wiki.js
}
CALLOUT = {"is-info": "info", "is-warning": "warning", "is-success": "success", "is-danger": "danger"}
FENCE = re.compile(r"^\s*(```|~~~)")
# list items linking to pages that are not migrated (skipped pages, Wiki.js sitemap)
# known broken markup in the Wiki.js sources: (page, old, new)
CONTENT_FIXES = [
    ("slurm/interactive_slurm_cli_session", "[partition](Slurm partitions)", "partition"),
]
DROP_LINE = re.compile(r"^\s*[-*] .*\]\((/en)?/(test-stream|sitemap\(1\)\.xml)\)\s*$")


def out_path(page_path):
    return "index.md" if page_path == "home" else page_path + ".md"


def split_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:]
    return text


class Converter:
    def __init__(self, pages, asset_files):
        self.pages = {p["path"]: p for p in pages}
        self.asset_files = asset_files
        self.used_assets = set()
        self.warnings = []

    # ---- links -------------------------------------------------------------
    def resolve(self, target, src_page):
        """Map an absolute Wiki.js URL to a path relative to the source page."""
        if not target.startswith("/") or target.startswith("//"):
            return None
        path, _, frag = target.partition("#")
        path = re.sub(r"^/en(?=/|$)", "", path).strip("/")
        path = re.sub(r"^t/", "", path)
        src_dir = posixpath.dirname(out_path(src_page))
        if path in ("", "home"):
            dest = "index.md"
        elif path in self.pages and path not in SKIP_PAGES:
            dest = out_path(path)
        elif path in self.asset_files:
            dest = path
            self.used_assets.add(path)
        else:
            self.warnings.append(f"{src_page}: unresolved link {target}")
            return None
        rel = posixpath.relpath(dest, src_dir or ".")
        return rel + ("#" + frag if frag else "")

    def fix_links(self, line, src):
        def md_link(m):
            label, target, rest = m.group(1), m.group(2), m.group(3) or ""
            size = re.match(r"\s*=(\d+%?)x(\d+%?)?\s*$", rest)
            new = self.resolve(target, src) or target
            out = f"({new})"
            if size:
                style = f"width:{size.group(1)}" if size.group(1) else ""
                if size.group(2):
                    style += f";height:{size.group(2)}"
                out += '{ style="' + style + '" }'
            elif rest.strip():
                out = f"({new}{rest})"
            return label + out

        line = re.sub(r"(\])\(([^)\s]+)((?:\s+[^)]*)?)\)", md_link, line)
        # raw HTML is not rewritten by MkDocs, so keep site-absolute URLs there
        def html_attr(m):
            target = m.group(2)
            if self.resolve(target, src) is not None:
                target = re.sub(r"^/en(?=/)", "", target)
            return m.group(1) + target + m.group(3)

        line = re.sub(r'((?:src|href)=")(/[^"]*)(")', html_attr, line)
        return line

    # ---- block transforms --------------------------------------------------
    @staticmethod
    def demote_headings(text):
        """Wiki.js renders the page title itself and pages use # for sections.
        MkDocs needs the title as the only H1, so shift every heading one level down."""
        out, in_code = [], False
        for line in text.split("\n"):
            if FENCE.match(line):
                in_code = not in_code
            elif not in_code and re.match(r"^#{1,5} ", line):
                line = "#" + line
            out.append(line)
        return "\n".join(out)

    def convert_markdown(self, text, src):
        if re.search(r"^# ", re.sub(r"(?ms)^```.*?^```", "", text), re.M):
            text = self.demote_headings(text)
        lines = text.split("\n")
        out, i, in_code = [], 0, False
        tab_level = None  # heading level of the active tabset
        tab_open = False

        def emit(s):
            out.append(("    " + s if s.strip() else s) if tab_open else s)

        while i < len(lines):
            line = lines[i]
            if FENCE.match(line):
                in_code = not in_code
                emit(line)
                i += 1
                continue
            if in_code:
                emit(line)
                i += 1
                continue
            if DROP_LINE.match(line):
                i += 1
                continue

            h = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
            # end of tabset
            if tab_level and h and len(h.group(1)) <= tab_level:
                tab_level, tab_open = None, False
            if h and re.search(r"\{\.tabset\}\s*$", h.group(2)):
                tab_level = len(h.group(1))
                out.append("")
                i += 1
                continue
            if tab_level and h and len(h.group(1)) == tab_level + 1:
                tab_open = False
                out.append(f'=== "{h.group(2)}"')
                out.append("")
                tab_open = True
                i += 1
                continue

            # blockquote callouts: collect the quote, look for {.is-*}
            if line.startswith(">"):
                block = []
                while i < len(lines) and lines[i].startswith(">"):
                    block.append(re.sub(r"^> ?", "", lines[i]))
                    i += 1
                kind = None
                m = re.search(r"\s*\{\.(is-\w+)\}\s*$", block[-1])
                if m:
                    kind = m.group(1)
                    block[-1] = block[-1][:m.start()]
                elif i < len(lines) and re.fullmatch(r"\s*\{\.(is-\w+)\}\s*", lines[i]):
                    kind = re.fullmatch(r"\s*\{\.(is-\w+)\}\s*", lines[i]).group(1)
                    i += 1
                if kind in CALLOUT:
                    emit(f'!!! {CALLOUT[kind]} ""')
                    for b in block:
                        emit("    " + self.fix_links(b, src) if b.strip() else "")
                else:
                    for b in block:
                        emit("> " + self.fix_links(b, src))
                continue

            # {.links-list} after a list -> grid cards
            if re.fullmatch(r"\s*\{\.links-list\}\s*", line):
                j = len(out) - 1
                while j >= 0 and re.match(r"^\s*[-*] ", out[j].strip() and out[j] or "x"):
                    j -= 1
                items = [re.sub(r"^\s*[-*]\s+", "", l) for l in out[j + 1:]]
                del out[j + 1:]
                out.append('<div class="grid cards" markdown>')
                out.append("")
                out.extend(f"-   {it}" for it in items)
                out.append("")
                out.append("</div>")
                i += 1
                continue

            emit(self.fix_links(line, src))
            i += 1
        return "\n".join(out)

    @staticmethod
    def figures_to_markdown(html):
        """<figure style="width:X%"><img src alt><figcaption>..</figcaption></figure>
        -> markdown image with width and an italic caption (markdownify drops both)."""
        def fig(m):
            attrs, inner = m.group(1), m.group(2)
            img = re.search(r"<img[^>]*>", inner)
            if not img:
                return m.group(0)
            src_ = re.search(r'src="([^"]+)"', img.group(0)).group(1)
            alt = re.search(r'alt="([^"]*)"', img.group(0))
            alt = alt.group(1) if alt else ""
            width = re.search(r"width:\s*([\d.]+%)", attrs)
            cap = re.search(r"<figcaption>(.*?)</figcaption>", inner, re.S)
            md = f"![{alt}]({src_})"
            if width:
                md += '{ style="width:' + width.group(1) + '" }'
            out = f"\n<p>WIKIJSFIG{md}</p>\n"
            if cap:
                out += f"<p><em>{cap.group(1).strip()}</em></p>\n"
            return out
        return re.sub(r"<figure([^>]*)>(.*?)</figure>", fig, html, flags=re.S)

    def convert_html(self, html, src):
        html = self.figures_to_markdown(html)
        html = re.sub(r'<pre[^>]*><code class="language-([^"]*)"[^>]*>',
                      lambda m: f'<pre><code class="language-{m.group(1) or "text"}">', html)
        md = markdownify.markdownify(
            html, heading_style="ATX", bullets="-",
            code_language_callback=lambda el: (el.get("class") or ["language-text"])[0].removeprefix("language-") or "text",
        )
        md = re.sub(r"WIKIJSFIG(.*)", lambda m: m.group(1).replace("\\_", "_").replace("\\*", "*"), md)
        md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
        # the page title comes from front matter; drop a leading H1 that repeats it
        md = re.sub(r"^# .*\n+", "", md, count=1)
        return "\n".join(self.fix_links(l, src) for l in md.split("\n"))

    # ---- driver ------------------------------------------------------------
    def page(self, p):
        body = split_frontmatter(p["content"]) if p["editorKey"] == "markdown" else p["content"]
        for page, old, new in CONTENT_FIXES:
            if page == p["path"]:
                body = body.replace(old, new)
        body = self.convert_markdown(body, p["path"]) if p["editorKey"] == "markdown" \
            else self.convert_html(body, p["path"])
        fm = ["---", f"title: {json.dumps(p['title'], ensure_ascii=False)}"]
        if (p.get("description") or "").strip():
            fm.append(f"description: {json.dumps(p['description'].strip(), ensure_ascii=False)}")
        if p.get("tags"):
            fm.append("tags:")
            fm += [f"  - {json.dumps(t, ensure_ascii=False)}" for t in p["tags"]]
        fm.append("---")
        return "\n".join(fm) + "\n\n# " + p["title"].strip() + "\n\n" + body.strip() + "\n"


def build_nav(nav_items, pages):
    """Wiki.js nav (headers + links) -> MkDocs nav list."""
    nav, section = [], None
    for it in nav_items:
        kind = it["kind"]
        if kind == "header":
            section = {it["label"].strip(): []}
            nav.append(section)
        elif kind == "link":
            target = it.get("target") or "/"
            path = re.sub(r"^/en(?=/|$)", "", target).strip("/") or "home"
            if path not in pages:
                continue
            entry = {it["label"].strip(): out_path(path)}
            (list(section.values())[0] if section else nav).append(entry)
        elif kind == "divider":
            section = None
    return [n for n in nav if not (isinstance(n, dict) and list(n.values())[0] == [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--assets", required=True)
    ap.add_argument("--out", default="docs")
    a = ap.parse_args()

    d = json.load(open(a.db))
    tags = {}
    for t in d["tags"]:
        tags.setdefault(t["path"], []).append(t["tag"])
    pages = [dict(p, tags=sorted(tags.get(p["path"], []))) for p in d["pages"]]

    asset_files = set()
    for root, _, files in os.walk(a.assets):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), a.assets)
            if not rel.endswith((".md", ".html")) and not rel.startswith("_daily"):
                asset_files.add(rel)

    conv = Converter(pages, asset_files)
    os.makedirs(a.out, exist_ok=True)
    written = 0
    for p in pages:
        if p["path"] in SKIP_PAGES:
            print(f"skip  {p['path']}", file=sys.stderr)
            continue
        dest = os.path.join(a.out, out_path(p["path"]))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w") as f:
            f.write(conv.page(p))
        written += 1

    for rel in sorted(conv.used_assets):
        dest = os.path.join(a.out, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(os.path.join(a.assets, rel), dest)

    nav = build_nav(json.loads(d["nav"][0]["config"])[0]["items"], {p["path"] for p in pages} - SKIP_PAGES)
    with open("nav.yml", "w") as f:
        f.write("# generated by tools/convert_wikijs.py from the Wiki.js site navigation\n")
        yaml.safe_dump({"nav": nav}, f, allow_unicode=True, sort_keys=False)

    unused = sorted(asset_files - conv.used_assets)
    print(f"pages written: {written}, assets copied: {len(conv.used_assets)}, unused assets: {len(unused)}", file=sys.stderr)
    for u in unused:
        print(f"unused asset  {u}", file=sys.stderr)
    for w in conv.warnings:
        print(f"WARN  {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
