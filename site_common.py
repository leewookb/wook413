import os
import re

FONT_STACK = '"Manrope", "Apple SD Gothic Neo", "Malgun Gothic", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif'
HEADING_FONT_STACK = '"Space Grotesk", "Apple SD Gothic Neo", "Malgun Gothic", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif'

FONT_LINKS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">"""

THEME_SCRIPT = """<script>
(function () {
    try {
        var saved = localStorage.getItem("theme");
        if (saved) document.documentElement.setAttribute("data-theme", saved);
    } catch (e) {}
})();
function toggleTheme() {
    var root = document.documentElement;
    var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("theme", next); } catch (e) {}
}
</script>"""

THEME_TOGGLE_HTML = '<button type="button" class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode"><span class="icon-sun">☀️</span><span class="icon-moon">\U0001f319</span></button>'

THEME_TOGGLE_CSS = """
.theme-toggle {
    margin-left: auto;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border: none;
    border-radius: 999px;
    background: transparent;
    color: var(--muted);
    font-size: 1rem;
    line-height: 1;
    cursor: pointer;
    transition: background 0.15s ease;
}

.theme-toggle:hover { background: var(--row-hover, var(--code-bg)); }

.theme-toggle .icon-moon { display: none; }

:root[data-theme="light"] .theme-toggle .icon-sun { display: none; }
:root[data-theme="light"] .theme-toggle .icon-moon { display: inline; }
"""

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
    "cyberdefenders": "CyberDefenders",
    "soc-analyst-tier-1": "SOC Analyst Tier 1",
    "jetbrains": "JetBrains",
    "splunk-detection-lab": "Splunk Detection Lab",
    "splunk-detection-lab-part-1": "Part 1",
    "splunk-detection-lab-part-2": "Part 2",
    "splunk-detection-lab-part-3": "Part 3",
    "OSCP": "OSCP",
    "about": "About",
    "pc": "PC",
    "bullybox": "BullyBox",
    "quackerjack": "QuackerJack",
    "vulnnet-active": "VulnNet: Active",
    "getting-started-with-splunk-for-security": "Getting Started with Splunk for Security",
}


def prettify(slug):
    """Fallback label for a path segment that has no LABELS entry, e.g.
    "vulnnet-active" -> "Vulnnet Active", "lab1" -> "Lab 1"."""
    slug = re.sub(r"(?<=[a-zA-Z])(?=\d)", " ", slug)
    return slug.replace("-", " ").replace("_", " ").title()


NAV_ITEMS = [
    ("Home", "index.html"),
    ("Writeups", "writeups/index.html"),
    ("Projects", "projects/index.html"),
    ("About", "about/index.html"),
]

NAV_CSS = """
body { padding-top: 112px; }

.site-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 50;
    display: flex;
    justify-content: center;
    background: var(--nav-bg, rgba(253, 251, 247, 0.9));
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border);
}

.site-nav-inner {
    display: flex;
    gap: 4px;
    width: 100%;
    max-width: 760px;
    padding: 14px 20px;
}

.site-nav a {
    padding: 7px 15px;
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
    body { padding-top: 98px; }
    .site-nav-inner { padding: 10px 16px; gap: 2px; }
    .site-nav-inner { overflow-x: auto; scrollbar-width: none; }
    .site-nav-inner::-webkit-scrollbar { display: none; }
    .site-nav a { padding: 5px 9px; font-size: 0.78rem; white-space: nowrap; flex-shrink: 0; }
    .theme-toggle { flex-shrink: 0; }
}
""" + THEME_TOGGLE_CSS

# the "413" favicon as a home-link brand mark at the left of the nav bar.
# The glyph is black on transparent, so it's inverted in dark mode.
BRAND_CSS = """
.site-nav-inner { align-items: center; }
.site-nav a.brand { display: inline-flex; align-items: center; padding: 4px 10px 4px 4px; margin-right: 6px; background: none; }
/* reset article pages' generic img rule (margin/border/shadow/brightness) */
.site-nav a.brand img {
    display: block; width: 26px; height: 26px; max-width: none; margin: 0;
    border: 0; border-radius: 0; box-shadow: none;
    filter: invert(0.9); transition: opacity 0.15s ease;
}
:root[data-theme="light"] .site-nav a.brand img { filter: none; }
.site-nav a.brand:hover { background: none; }
.site-nav a.brand:hover img { opacity: 0.7; }
@media (max-width: 600px) {
    .site-nav a.brand { padding: 2px 6px 2px 0; margin-right: 2px; }
    .site-nav a.brand img { width: 22px; height: 22px; }
}
"""
NAV_CSS += BRAND_CSS


def icon_links_html(repo_relative_path):
    """Favicon / touch icon / manifest <link>s with paths relative to the
    page, so the tab icon also shows when a page is opened from disk."""
    depth = depth_from_repo_root(repo_relative_path)
    p = ("../" * depth) if depth else "./"
    return ("<!--icons-->"
            f'<link rel="icon" href="{p}favicon.ico" sizes="48x48">'
            f'<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/favicon_io/favicon-32x32.png">'
            f'<link rel="apple-touch-icon" sizes="180x180" href="{p}assets/favicon_io/apple-touch-icon.png">'
            f'<link rel="manifest" href="{p}assets/favicon_io/site.webmanifest">'
            "<!--/icons-->")

LISTING_CSS = """
:root {
    --bg: #17140f;
    --card-bg: #211d17;
    --text: #ece7de;
    --muted: #a39a8c;
    --link: #6db2ff;
    --border: #332e24;
    --row-hover: #2a2419;
    --nav-bg: rgba(23, 20, 15, 0.85);
}

:root[data-theme="light"] {
    --bg: #fdfbf7;
    --card-bg: #ffffff;
    --text: #201d1a;
    --muted: #837b70;
    --link: #0f5fae;
    --border: #ece5d8;
    --row-hover: #f6f2ea;
    --nav-bg: rgba(253, 251, 247, 0.9);
}

* { box-sizing: border-box; }

body {
    font-family: """ + FONT_STACK + """;
    background: var(--bg);
    color: var(--text);
    padding: 56px 20px 90px;
    max-width: 760px;
    margin: 0 auto;
    line-height: 1.6;
}

h1 {
    font-family: """ + HEADING_FONT_STACK + """;
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0 0 30px;
}

h2 {
    font-family: """ + HEADING_FONT_STACK + """;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin: 40px 0 12px;
}

ul.listing {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

ul.listing a {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    background: var(--card-bg);
    border: 1px solid var(--border);
    color: var(--text);
    text-decoration: none;
    padding: 14px 18px;
    border-radius: 14px;
    font-weight: 700;
    box-shadow: 0 1px 2px rgba(32, 29, 26, 0.03);
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

ul.listing a:hover {
    transform: translateY(-2px);
    border-color: #d8cdb8;
    box-shadow: 0 10px 24px rgba(32, 29, 26, 0.08);
}

ul.listing a:hover .label { color: var(--link); }

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
    body { padding: 32px 16px 64px; }
    h1 { font-size: 1.4rem; }
    ul.listing a { padding: 12px 14px; }
}
"""


def nav_html(repo_relative_path):
    """Fixed top nav bar (Home / Writeups / Projects / About),
    with the current section highlighted."""
    norm = os.path.normpath(repo_relative_path).replace("\\", "/")
    depth = depth_from_repo_root(repo_relative_path)
    prefix = ("../" * depth) if depth else "./"
    top = norm.split("/")[0]
    links = [f'<a class="brand" href="{prefix}index.html" aria-label="wook413 home">'
             f'<img src="{prefix}assets/favicon_io/android-chrome-192x192.png" alt="" width="26" height="26"></a>']
    for label, target in NAV_ITEMS:
        href = prefix + target
        section = target.split("/")[0] if "/" in target else None
        if target == "about/index.html":
            active = top in ("about", "OSCP") or norm in ("README.md", "README.html")
        elif target == "index.html":
            active = norm == "index.html"
        else:
            active = norm == target or bool(section and top == section)
        cls = ' class="active"' if active else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    return '<nav class="site-nav"><div class="site-nav-inner">' + "".join(links) + THEME_TOGGLE_HTML + "</div></nav>"


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
        # writeup categories have no listing pages of their own anymore --
        # they're filters on the single writeups/index.html archive
        if dir_parts[0] == "writeups" and 0 < i <= 2:
            href = "../" * (n - 1) + "index.html?p=" + dir_parts[1]
            if i == 2:
                href += "&amp;s=" + dir_parts[2]
        crumbs.append(f'<a href="{href}">{label}</a>')

    final_key = basename_noext if standalone_file else dir_parts[-1]
    final_label = LABELS.get(final_key, prettify(final_key))
    crumbs.append(f"<span>{final_label}</span>")

    return '<div class="breadcrumb">' + '<span class="sep">/</span>'.join(crumbs) + "</div>"
