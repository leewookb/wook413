import os
import re

FONT_STACK = '"Nunito", "Apple SD Gothic Neo", "Malgun Gothic", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif'

FONT_LINKS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">"""

HOME_CSS = """
.home-link {
    position: fixed;
    top: 16px;
    left: 16px;
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 6px 14px;
    font-size: 0.85rem;
    color: var(--link);
    text-decoration: none;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    z-index: 10;
}

.home-link:hover {
    background: var(--row-hover, var(--code-bg));
}

@media (max-width: 600px) {
    .home-link { top: 10px; left: 10px; padding: 5px 12px; font-size: 0.8rem; }
}
"""


def depth_from_repo_root(path):
    """How many directories `path` sits below the repo root (0 = root itself)."""
    parent = os.path.dirname(os.path.normpath(path))
    if parent in ("", "."):
        return 0
    return len(parent.split(os.sep))


def home_link_html(path, repo_root_index="index.html", skip_for=("index.html",)):
    """<a> tag pointing back to the repo-root index.html, or "" if `path`
    (relative to the repo root) *is* that root index page."""
    norm = os.path.normpath(path)
    if norm in skip_for:
        return ""
    depth = depth_from_repo_root(path)
    href = ("../" * depth + repo_root_index) if depth else f"./{repo_root_index}"
    return f'<a class="home-link" href="{href}">🏠 Home</a>'


# --- top nav bar + breadcrumb -------------------------------------------

LABELS = {
    "writeups": "Writeups",
    "projects": "Projects",
    "proving-grounds": "Proving Grounds",
    "tryhackme": "TryHackMe",
    "hackthebox": "HackTheBox",
    "starting-point": "Starting Point",
    "web-security-academy": "Web Security Academy",
    "business-logic-vulnerabilities": "Business Logic Vulnerabilities",
    "authentication": "Authentication",
    "command-injection": "Command Injection",
    "path-traversal": "Path Traversal",
    "sql-injection": "SQL Injection",
    "boss-of-the-soc": "Boss of the SOC",
    "splunk-detection-lab": "Splunk Detection Lab",
    "splunk-detection-lab-part-1": "Part 1",
    "OSCP": "OSCP",
}


def prettify(slug):
    """Fallback label for a path segment that has no LABELS entry, e.g.
    "vulnnet-active" -> "Vulnnet Active", "lab1" -> "Lab 1"."""
    slug = re.sub(r"(?<=[a-zA-Z])(?=\d)", " ", slug)
    return slug.replace("-", " ").replace("_", " ").title()


NAV_ITEMS = [
    ("Home", "index.html"),
    ("About", "README.html"),
    ("Writeups", "writeups/index.html"),
    ("Projects", "projects/index.html"),
    ("Certifications", "OSCP/index.html"),
]

NAV_CSS = """
body { padding-top: 108px; }

.site-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 50;
    display: flex;
    justify-content: center;
    background: var(--bg);
    border-bottom: 1px solid var(--border);
}

.site-nav-inner {
    display: flex;
    gap: 4px;
    width: 100%;
    max-width: 760px;
    padding: 12px 20px;
}

.site-nav a {
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--muted);
    text-decoration: none;
    transition: background 0.15s ease, color 0.15s ease;
}

.site-nav a:hover {
    color: var(--link);
    background: var(--row-hover, var(--code-bg));
}

.site-nav a.active {
    color: var(--link);
    background: var(--row-hover, var(--code-bg));
}

.breadcrumb {
    font-size: 0.8rem;
    color: var(--muted);
    margin: 0 0 20px;
}

.breadcrumb a {
    color: var(--muted);
    text-decoration: none;
}

.breadcrumb a:hover {
    color: var(--link);
    text-decoration: underline;
}

.breadcrumb .sep {
    margin: 0 6px;
    opacity: 0.5;
}

@media (max-width: 600px) {
    body { padding-top: 96px; }
    .site-nav-inner { padding: 10px 16px; gap: 2px; }
    .site-nav a { padding: 5px 10px; font-size: 0.8rem; }
}
"""

LISTING_CSS = """
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
    margin: 0 0 28px;
}

h2 {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin: 36px 0 6px;
}

ul.listing {
    list-style: none;
    padding: 0;
    margin: 0;
}

ul.listing li {
    border-bottom: 1px solid var(--border);
}

ul.listing a {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    color: var(--link);
    text-decoration: none;
    padding: 12px 10px;
    border-radius: 6px;
    font-weight: 600;
    transition: background 0.15s ease;
}

ul.listing a:hover {
    background: var(--row-hover);
}

ul.listing a:hover .label { text-decoration: underline; }

ul.listing .count,
ul.listing .badge {
    color: var(--muted);
    font-size: 0.8rem;
    font-weight: 400;
}

ul.listing .badge {
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 1px 9px;
}

footer {
    margin-top: 40px;
    font-size: 0.8rem;
    color: var(--muted);
    text-align: center;
}

@media (max-width: 600px) {
    body { padding: 32px 16px 60px; }
    h1 { font-size: 1.15rem; }
}
"""

HOME_CARD_CSS = """
.home-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    margin-top: 8px;
}

.home-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 36px 16px;
    border: 1px solid var(--border);
    border-radius: 14px;
    color: var(--text);
    text-decoration: none;
    background: var(--bg);
    transition: background 0.15s ease, border-color 0.15s ease;
}

.home-card:hover {
    background: var(--row-hover);
    border-color: var(--link);
}

.home-card-icon {
    font-size: 2.2rem;
    line-height: 1;
}

.home-card-label {
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--link);
}

@media (max-width: 480px) {
    .home-grid { grid-template-columns: 1fr; }
}
"""


def nav_html(repo_relative_path):
    """Fixed top nav bar (Home / About / Writeups / Projects / Certifications),
    with the current section highlighted."""
    norm = os.path.normpath(repo_relative_path).replace("\\", "/")
    depth = depth_from_repo_root(repo_relative_path)
    prefix = ("../" * depth) if depth else "./"
    top = norm.split("/")[0]
    links = []
    for label, target in NAV_ITEMS:
        href = prefix + target
        section = target.split("/")[0] if "/" in target else None
        if target == "README.html":
            active = norm in ("README.md", "README.html")
        elif target == "index.html":
            active = norm == "index.html"
        else:
            active = norm == target or bool(section and top == section)
        cls = ' class="active"' if active else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    return '<nav class="site-nav"><div class="site-nav-inner">' + "".join(links) + "</div></nav>"


def breadcrumb_html(repo_relative_path):
    """Clickable trail (e.g. Writeups / Proving Grounds / Access) built from
    the file's path. Skipped for pages one level or less below the repo
    root, where the nav bar alone is enough context."""
    norm = os.path.normpath(repo_relative_path).replace("\\", "/")
    parts = norm.split("/")
    filename = parts[-1]
    dir_parts = parts[:-1]
    n = len(dir_parts)
    if n < 2:
        return ""

    basename_noext = os.path.splitext(filename)[0]
    is_index = filename == "index.html"
    # a file whose name doesn't match its own directory (e.g. a dated part
    # of a multi-part series living alongside that series' own index.html)
    # gets its directory as a clickable crumb plus one extra unlinked crumb
    # for itself, instead of collapsing into a single "current page" crumb
    standalone_file = (not is_index) and basename_noext.lower() != dir_parts[-1].lower()

    limit = n if standalone_file else n - 1
    crumbs = []
    for i in range(limit):
        label = LABELS.get(dir_parts[i], prettify(dir_parts[i]))
        up = n - 1 - i
        href = ("../" * up + "index.html") if up else "./index.html"
        crumbs.append(f'<a href="{href}">{label}</a>')

    final_key = basename_noext if standalone_file else dir_parts[-1]
    final_label = LABELS.get(final_key, prettify(final_key))
    crumbs.append(f"<span>{final_label}</span>")

    return '<div class="breadcrumb">' + '<span class="sep">/</span>'.join(crumbs) + "</div>"
