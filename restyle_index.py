import re
import sys

from site_common import FONT_LINKS, HOME_CSS, home_link_html

CSS = """
:root {
    --bg: #fdfbf7;
    --text: #262220;
    --muted: #7a736a;
    --link: #0f5fae;
    --border: #e7e1d6;
    --row-hover: #eef3f8;
}

* { box-sizing: border-box; }

body {
    font-family: "Nunito", "Apple SD Gothic Neo", "Malgun Gothic", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    padding: 56px 20px 80px;
    max-width: 760px;
    margin: 0 auto;
    line-height: 1.6;
}

h1 {
    font-size: 1.4rem;
    font-weight: 700;
    border-bottom: 2px solid var(--text);
    padding-bottom: 14px;
    margin: 0 0 28px;
    word-break: break-all;
}

table { width: 100%; border-collapse: collapse; }

td {
    border-bottom: 1px solid var(--border);
    padding: 0;
}

td a {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--link);
    text-decoration: none;
    padding: 12px 10px;
    border-radius: 6px;
    margin: 0 -10px;
}

td a span.label {
    border-radius: 3px;
}

td a:hover {
    background: var(--row-hover);
}

td a:hover span.label { text-decoration: underline; }

footer {
    margin-top: 20px;
    font-size: 0.8rem;
    color: var(--muted);
    text-align: center;
}

@media (max-width: 600px) {
    body { padding: 32px 16px 60px; }
    h1 { font-size: 1.15rem; }
}
"""


def restyle(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    icons_m = re.search(r'<meta name="viewport"[^>]*/?>(.*?)<title>', html, re.S)
    icons = icons_m.group(1).strip() if icons_m else ""
    # drop any Nunito/font-loading tags a previous run already injected here,
    # so re-running this script stays idempotent instead of piling up copies
    icons = re.sub(r'<link[^>]*fonts\.g(?:oogleapis|static)\.com[^>]*>\s*', '', icons)

    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    h1 = h1_m.group(1).strip() if h1_m else "Index"

    # some pages (web-security-academy/index.html) have more than one
    # <table><tbody> in the source -- collect every row from all of them
    # instead of re.search's first-match-only, which silently drops the rest.
    tbody = "\n".join(re.findall(r"<tr>.*?</tr>", html, re.S))

    # some rows have the icon as bare text before the <a> instead of inside
    # it (hand-written pages) -- `td a { display: flex }` then only wraps the
    # label, so the icon renders on its own line above it. Pull it in.
    def _fix_row(m):
        return f'<td><a{m.group("attrs")}><span>{m.group("icon")}</span> <span class="label">{m.group("label")}</span></a></td>'

    tbody = re.sub(
        r'<td>(?P<icon>[^\s<]+)\s*<a(?P<attrs>[^>]*)>(?P<label>[^<]*)</a></td>',
        _fix_row, tbody,
    )

    home_html = home_link_html(path)

    new_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{icons}
{FONT_LINKS}
<title>wook413</title>
<style>{CSS}{HOME_CSS}</style>
</head>
<body>
{home_html}
<h1>{h1}</h1>
<table>
<tbody>
{tbody}
</tbody>
</table>
<footer>&copy; 2026 wook413.</footer>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        restyle(p)
        print(f"restyled {p}")
