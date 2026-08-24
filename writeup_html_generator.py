import os
import re
import sys
import markdown

from site_common import FONT_LINKS, NAV_CSS, nav_html, breadcrumb_html

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

CSS = """
:root {
    --bg: #ffffff;
    --text: #1a1a1a;
    --muted: #666666;
    --link: #0066cc;
    --border: #e5e5e5;
    --code-bg: #131a24;
    --code-text: #dce6f0;
    --code-accent: #0066cc;
    --inline-code-bg: #f0f4f9;
    --inline-code-text: #a3193d;
}

* { box-sizing: border-box; }

body {
    font-family: "Manrope", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 48px 20px 80px;
    line-height: 1.7;
}

.page {
    max-width: 760px;
    margin: 0 auto;
    overflow-wrap: break-word;
}

.byline {
    color: var(--muted);
    font-size: 0.9rem;
    margin-bottom: 4px;
}

h1 {
    font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 1.6rem;
    border-bottom: 2px solid var(--text);
    padding-bottom: 14px;
    margin: 8px 0 28px;
    line-height: 1.35;
}

h2, h3, h4 {
    font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    margin-top: 2.2em;
    margin-bottom: 0.8em;
    line-height: 1.35;
}

h3 { font-size: 1.25rem; }

p { margin: 1em 0; }

strong { font-weight: 650; }

a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }

hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2.5em 0;
}

ul, ol { padding-left: 1.4em; margin: 1em 0; }
li { margin: 0.35em 0; }

/* inline code */
code {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    background: var(--inline-code-bg);
    color: var(--inline-code-text);
    padding: 0.15em 0.4em;
    border-radius: 4px;
    font-size: 0.88em;
}

/* fenced code blocks */
pre {
    position: relative;
    background: var(--code-bg);
    color: var(--code-text);
    border-radius: 10px;
    padding: 18px 20px;
    margin: 1.6em 0;
    overflow-x: auto;
    border-left: 4px solid var(--code-accent);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
}

pre code {
    background: none;
    color: inherit;
    padding: 0;
    border-radius: 0;
    font-size: 0.85rem;
    line-height: 1.6;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

/* images */
img {
    display: block;
    max-width: 100%;
    height: auto;
    margin: 1.8em auto;
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

p:has(> img:only-child) { text-align: center; }

footer {
    margin-top: 60px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
    font-size: 0.8rem;
    color: var(--muted);
    text-align: center;
}

@media (max-width: 600px) {
    body { padding: 28px 16px 60px; }
    h1 { font-size: 1.3rem; }
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg: #12151b;
        --text: #eaeaea;
        --muted: #9aa1ab;
        --link: #5b9dff;
        --border: #2a2e37;
        --code-bg: #0b0e14;
        --code-text: #dce6f0;
        --code-accent: #5b9dff;
        --inline-code-bg: #232732;
        --inline-code-text: #ff8aa8;
    }
}

:root[data-theme="dark"] {
    --bg: #12151b;
    --text: #eaeaea;
    --muted: #9aa1ab;
    --link: #5b9dff;
    --border: #2a2e37;
    --code-bg: #0b0e14;
    --code-text: #dce6f0;
    --code-accent: #5b9dff;
    --inline-code-bg: #232732;
    --inline-code-text: #ff8aa8;
}

:root[data-theme="light"] {
    --bg: #ffffff;
    --text: #1a1a1a;
    --muted: #666666;
    --link: #0066cc;
    --border: #e5e5e5;
    --code-bg: #131a24;
    --code-text: #dce6f0;
    --code-accent: #0066cc;
    --inline-code-bg: #f0f4f9;
    --inline-code-text: #a3193d;
}
"""

# reading-optimized, light-only alternative: warmer paper background,
# one clean casual sans-serif throughout, cooler light code panels
# instead of a dark block so the whole page stays light.
from site_common import FONT_STACK, HEADING_FONT_STACK

CSS_LIGHT = """
:root {
    --bg: #fdfbf7;
    --text: #201d1a;
    --muted: #837b70;
    --link: #0f5fae;
    --border: #ece5d8;
    --code-bg: #eef3f8;
    --code-border: #d3e1ee;
    --code-text: #1f2937;
    --code-accent: #2563eb;
    --inline-code-bg: #eef3f8;
    --inline-code-text: #a3271e;
}

* { box-sizing: border-box; }

body {
    font-family: """ + FONT_STACK + """;
    background: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 56px 20px 90px;
    line-height: 1.75;
    font-size: 1.05rem;
}

.page {
    max-width: 700px;
    margin: 0 auto;
    overflow-wrap: break-word;
}

.byline {
    color: var(--muted);
    font-size: 0.85rem;
    letter-spacing: 0.02em;
    margin-bottom: 6px;
}

h1 {
    font-family: """ + HEADING_FONT_STACK + """;
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    border-bottom: 2px solid var(--text);
    padding-bottom: 16px;
    margin: 2.4em 0 32px;
    line-height: 1.35;
}

/* first heading on the page sits right under the byline, not floating mid-page */
.page > h1:first-of-type { margin-top: 10px; }

.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: -18px 0 32px;
}

.tag {
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--muted);
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    padding: 3px 11px;
    border-radius: 999px;
}

h2, h3, h4 {
    font-family: """ + HEADING_FONT_STACK + """;
    font-weight: 700;
    margin-top: 2.4em;
    margin-bottom: 0.9em;
    line-height: 1.4;
}

h3 { font-size: 1.2rem; }

blockquote {
    margin: 1.6em 0;
    padding: 0.3em 1.3em;
    border-left: 4px solid var(--border);
    color: var(--muted);
    font-style: italic;
}

blockquote p { margin: 0.6em 0; }

mark {
    background: #fbe89f;
    color: inherit;
    padding: 0.05em 0.2em;
    border-radius: 2px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.8em 0;
    font-size: 0.92rem;
}

th, td {
    padding: 8px 14px;
    border-bottom: 1px solid var(--border);
    text-align: left;
    vertical-align: top;
}

thead th { border-bottom: 2px solid var(--text); font-weight: 700; }

/* [TOC] rendered nav */
.toc {
    font-size: 0.9rem;
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    border-radius: 8px;
    padding: 16px 22px;
    margin: 1.8em 0;
}

.toc ul { list-style: none; padding-left: 1.1em; margin: 0.3em 0; }
.toc > ul { padding-left: 0; }
.toc li { margin: 0.3em 0; }
.toc a { color: var(--text); text-decoration: none; }
.toc a:hover { color: var(--link); text-decoration: underline; }

p { margin: 1.1em 0; }

strong { font-weight: 700; }

a { color: var(--link); text-decoration: underline; text-decoration-color: rgba(15, 95, 174, 0.35); text-underline-offset: 2px; }
a:hover { text-decoration-color: currentColor; }

hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2.8em 0;
}

ul, ol { padding-left: 1.5em; margin: 1.1em 0; }
li { margin: 0.4em 0; }

ul.task-list {
    list-style: none;
    padding-left: 0;
}

.task-list-item input[type="checkbox"] {
    margin: 0 6px 0 0;
    accent-color: var(--code-accent);
    vertical-align: -2px;
}

.task-list-item del { color: var(--muted); }

/* inline code */
code {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    background: var(--inline-code-bg);
    color: var(--inline-code-text);
    padding: 0.15em 0.4em;
    border-radius: 4px;
    font-size: 0.82em;
    border: 1px solid var(--code-border);
}

/* fenced code blocks: light panel, not a dark box, but still clearly set apart */
pre {
    background: var(--code-bg);
    color: var(--code-text);
    border: 1px solid var(--code-border);
    border-left: 4px solid var(--code-accent);
    border-radius: 8px;
    padding: 18px 20px;
    margin: 1.8em 0;
    overflow-x: auto;
    box-shadow: 0 1px 3px rgba(37, 99, 235, 0.06);
}

pre code {
    background: none;
    color: inherit;
    padding: 0;
    border: none;
    font-size: 0.86rem;
    line-height: 1.65;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

/* images */
img {
    display: block;
    max-width: 100%;
    height: auto;
    margin: 2em auto;
    border: 1px solid var(--border);
    border-radius: 6px;
    box-shadow: 0 3px 10px rgba(38, 34, 32, 0.08);
}

p:has(> img:only-child) { text-align: center; }

footer {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    margin-top: 64px;
    padding-top: 22px;
    border-top: 1px solid var(--border);
    font-size: 0.8rem;
    color: var(--muted);
    text-align: center;
}

@media (max-width: 600px) {
    body { padding: 32px 16px 64px; font-size: 1.03rem; }
    h1 { font-size: 1.3rem; }
}
"""


def convert_md_to_html(md_path, title=None, style="mono"):
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    byline = ""
    m = re.match(r"^\s*Write-?up by (.+?)\s*\n", text, re.IGNORECASE)
    if m:
        byline = m.group(1).strip()
        text = text[m.end():]

    # Typora-style tag lines like "#very-easy #linux" (no space after #) are
    # metadata, not headings -- pull them out before markdown sees them, or
    # its lenient ATX parser turns them into a spurious <h1>.
    tags = []
    def _pull_tags(match):
        tags.extend(t.lstrip("#") for t in match.group(1).split())
        return ""
    text = re.sub(r"^((?:#[\w-]+\s*)+)$", _pull_tags, text, count=1, flags=re.MULTILINE)

    md = markdown.Markdown(extensions=[
        "fenced_code", "tables", "sane_lists", "nl2br", "toc",
        "pymdownx.mark", "pymdownx.tilde", "pymdownx.tasklist",
    ], extension_configs={
        "pymdownx.tasklist": {"clickable_checkbox": False},
    })
    body_html = md.convert(text)

    if not title:
        title = os.path.splitext(os.path.basename(md_path))[0]

    byline_html = f'<div class="byline">Write-up by {byline}</div>' if byline else ""
    if tags:
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
        body_html = re.sub(r"(</h1>)", r"\1" + f'<div class="tags">{tags_html}</div>', body_html, count=1)
    css = (CSS_LIGHT if style == "read" else CSS) + NAV_CSS
    # depth must be computed from the repo root regardless of cwd, or the
    # nav/breadcrumb links end up with the wrong number of "../" when this
    # script is run from inside a lab's own directory (e.g. `lab2.md`
    # instead of the full writeups/.../lab2/lab2.md path)
    repo_relative_path = os.path.relpath(os.path.abspath(md_path), REPO_ROOT)
    nav = nav_html(repo_relative_path)
    breadcrumb = breadcrumb_html(repo_relative_path)

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{FONT_LINKS}
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{nav}
<div class="page">
{breadcrumb}
{byline_html}
{body_html}
<footer>&copy; 2026 wook413.</footer>
</div>
</body>
</html>
"""
    return html


if __name__ == "__main__":
    md_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(md_path)[0] + ".html"
    style = sys.argv[3] if len(sys.argv) > 3 else "read"
    html = convert_md_to_html(md_path, style=style)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {out_path}")
