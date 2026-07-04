import os

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
