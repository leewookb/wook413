"""Rebuild everything on the site that's derived from the set of posts.

    python build_site.py

- projects/index.html + each projects/<slug>/index.html: project cards and part lists
- writeups/index.html: one archive page listing every writeup (newest first),
  with platform / sub-category filter chips and a search box
- index.html: the "Most Recent" list (between the <!--recent--> markers)
- every writeup / project post: a date + category line under the <h1>, and
  previous / next links within the same collection, above the footer
- every page: the top nav bar and breadcrumb, re-rendered from site_common

A post's date is the day its .html was first committed (git, carried
across renames); posts not committed yet get today's date. Safe to re-run: every
injected block sits between marker comments and is replaced, not appended.
"""
import datetime
import glob
import html
import os
import re
import subprocess

from site_common import (BRAND_CSS, FONT_LINKS, LABELS, icon_links_html, LISTING_CSS, NAV_CSS, THEME_SCRIPT,
                         breadcrumb_html, nav_html, prettify)

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def L(slug):
    return LABELS.get(slug, prettify(slug))


def read(path):
    with open(os.path.join(REPO_ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(os.path.join(REPO_ROOT, path), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


_ADD_DATES = None
_ADD_SEQ = {}  # path -> commit index, to order same-day posts


def first_commit_date(path):
    """Day `path` was first committed, carried across plain renames/moves.
    One `git log` pass for the whole repo (oldest commit first) instead of a
    `--follow` per file -- `--follow` also chases *copies*, and since every
    post shares the same HTML template it would attribute a new post to
    some older, unrelated one."""
    global _ADD_DATES
    if _ADD_DATES is None:
        _ADD_DATES = {}
        log = subprocess.run(
            ["git", "-c", "core.quotepath=off", "log", "--reverse", "-M", "--name-status",
             "--diff-filter=AR", "--format=@%as"],
            cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8").stdout
        day, seq = None, 0
        for line in log.splitlines():
            if line.startswith("@"):
                day, seq = line[1:], seq + 1
            elif line.startswith("A\t"):
                if line[2:] not in _ADD_DATES:
                    _ADD_DATES[line[2:]], _ADD_SEQ[line[2:]] = day, seq
            elif line.startswith("R"):
                _, old, new = line.split("\t")
                _ADD_DATES[new] = _ADD_DATES.pop(old, day)
                _ADD_SEQ[new] = _ADD_SEQ.pop(old, seq)
    return _ADD_DATES.get(path, datetime.date.today().isoformat())


def natural_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def fmt_long(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d:%b} {d.day}, {d.year}"


def fmt_short(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d:%b} {d.day}"


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


# --- collect posts -------------------------------------------------------

class Post:
    def __init__(self, path):
        self.path = path                       # repo-relative, forward slashes
        parts = path.split("/")
        self.kind = parts[0]                   # "writeups" | "projects"
        self.dir_parts = parts[1:-1]
        text = re.sub(r"<!--post-title-->.*?<!--/post-title-->", "", read(path), flags=re.S)
        h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", text, re.S)
        # several <h1>s led by a short one means the source markdown used them
        # as section headings ("Recon", "Enumeration", ...) and has no title of
        # its own -- take it from the lab's folder name and inject a real title
        # heading. (Long first <h1>s like "Lab: Blind SQL injection ..." are
        # real titles that just happen to be followed by h1 sections.)
        self.needs_title = self.kind == "writeups" and (
            not h1s or (len(h1s) > 1 and len(strip_tags(h1s[0]).split()) <= 2))
        if self.needs_title:
            self.title = L(self.dir_parts[-1])
        else:
            self.title = strip_tags(h1s[0]) if h1s else L(os.path.splitext(parts[-1])[0])
        self.tags = re.findall(r'<span class="tag">([^<]+)</span>', text)
        self.date = first_commit_date(path)
        self.seq = _ADD_SEQ.get(path, float("inf"))
        if self.kind == "writeups":
            self.platform = self.dir_parts[0]
            # writeups/<platform>/<lab>/<lab>.html            -> no sub-category
            # writeups/<platform>/<sub>/<lab>/<lab>.html      -> sub-category
            self.sub = self.dir_parts[1] if len(self.dir_parts) >= 3 else ""
            self.group = (self.platform, self.sub)
        else:
            self.platform = self.dir_parts[0]
            self.sub = ""
            self.group = ("projects", self.platform)
            # project parts use <h1> for their own sections, so the first one
            # isn't a title -- name them from the path instead
            self.title = f"{L(self.platform)} · {L(os.path.splitext(parts[-1])[0])}"

    @property
    def crumb(self):
        bits = [L(self.platform)] + ([L(self.sub)] if self.sub else [])
        return " · ".join(bits)


def collect():
    posts = []
    for kind in ("writeups", "projects"):
        for p in glob.glob(f"{kind}/**/*.html", root_dir=REPO_ROOT, recursive=True):
            p = p.replace("\\", "/")
            if os.path.basename(p) != "index.html":
                posts.append(Post(p))
    return posts


def rel(from_path, to_path):
    return os.path.relpath(to_path, os.path.dirname(from_path) or ".").replace("\\", "/")


# --- per-post blocks -----------------------------------------------------

POST_CSS = """<style id="post-extras">
.post-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px 10px;
    margin: -4px 0 28px;
    font-size: 0.85rem;
    color: var(--muted);
}
.post-title { font-size: 2.1rem; margin-bottom: 14px; }
.post-meta a { color: var(--muted); text-decoration: none; border-bottom: 1px solid var(--border); }
.post-meta a:hover { color: var(--link); border-color: var(--link); }
.post-nav {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 56px 0 0;
    padding-top: 24px;
    border-top: 1px solid var(--border);
}
.post-nav a {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 14px 16px;
    border: 1px solid var(--border);
    border-radius: 12px;
    text-decoration: none;
    color: var(--text);
    transition: border-color 0.15s ease, transform 0.15s ease;
}
.post-nav a:hover { border-color: var(--link); transform: translateY(-1px); }
.post-nav .next { grid-column: 2; text-align: right; }
.post-nav .dir { font-size: 0.75rem; color: var(--muted); }
.post-nav .pt { font-weight: 700; font-size: 0.92rem; }
@media (max-width: 600px) {
    .post-nav { grid-template-columns: 1fr; }
    .post-nav .next { grid-column: 1; }
}
</style>"""


def post_meta_html(post):
    archive = rel(post.path, f"{post.kind}/index.html")
    if post.kind == "writeups":
        cat = f'<a href="{archive}?p={post.platform}">{L(post.platform)}</a>'
        if post.sub:
            cat += f'<span>·</span><a href="{archive}?p={post.platform}&amp;s={post.sub}">{L(post.sub)}</a>'
    else:
        cat = f'<a href="{rel(post.path, f"projects/{post.platform}/index.html")}">{L(post.platform)}</a>'
    return (f'<!--post-meta--><div class="post-meta"><time datetime="{post.date}">{fmt_long(post.date)}</time>'
            f'<span>·</span>{cat}</div><!--/post-meta-->')


def post_nav_html(post, prev, nxt):
    if not prev and not nxt:
        return ""
    out = ['<!--post-nav--><nav class="post-nav">']
    if prev:
        out.append(f'<a class="prev" href="{rel(post.path, prev.path)}"><span class="dir">← Previous</span>'
                   f'<span class="pt">{html.escape(prev.title)}</span></a>')
    if nxt:
        out.append(f'<a class="next" href="{rel(post.path, nxt.path)}"><span class="dir">Next →</span>'
                   f'<span class="pt">{html.escape(nxt.title)}</span></a>')
    out.append("</nav><!--/post-nav-->")
    return "".join(out)


def update_post(post, prev, nxt):
    text = read(post.path)
    text = re.sub(r'<style id="post-extras">.*?</style>\n?', "", text, flags=re.S)
    text = text.replace("</head>", POST_CSS + "\n</head>", 1)
    text = re.sub(r"<!--post-meta-->.*?<!--/post-meta-->", "", text, flags=re.S)
    text = re.sub(r"<!--post-nav-->.*?<!--/post-nav-->\n?", "", text, flags=re.S)
    text = re.sub(r"<!--post-title-->.*?<!--/post-title-->\n?", "", text, flags=re.S)
    if post.needs_title:
        block = (f'<!--post-title--><h1 class="post-title">{html.escape(post.title)}</h1>'
                 f'{post_meta_html(post)}<!--/post-title-->\n')
        text = re.sub(r'(<div class="breadcrumb">.*?</div>\n?)', lambda m: m.group(1) + block, text, count=1)
    else:
        text = re.sub(r"(</h1>)", lambda m: m.group(1) + post_meta_html(post), text, count=1)
    nav = post_nav_html(post, prev, nxt)
    if nav:
        text = text.replace("<footer>", nav + "\n<footer>", 1)
    # last breadcrumb crumb: the post's real title instead of a prettified slug
    text = re.sub(r'(<div class="breadcrumb">.*)<span>[^<]*</span></div>',
                  lambda m: m.group(1) + f"<span>{html.escape(post.title)}</span></div>", text, count=1)
    write(post.path, text)


# --- writeups archive ----------------------------------------------------

ARCHIVE_CSS = """
.lede { color: var(--muted); margin: -18px 0 28px; font-size: 0.95rem; }

.search {
    width: 100%;
    padding: 12px 16px;
    font: inherit;
    font-size: 0.95rem;
    color: var(--text);
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    outline: none;
    transition: border-color 0.15s ease;
}
.search:focus { border-color: var(--link); }

.chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 0; }
.chips[hidden] { display: none; }
.chip {
    font: inherit;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 6px 12px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: transparent;
    color: var(--muted);
    cursor: pointer;
    transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease;
}
.chip:hover { color: var(--text); }
.chip .n { opacity: 0.6; margin-left: 4px; font-weight: 500; }
.chip.on { color: var(--link); border-color: var(--link); background: var(--row-hover); }
.chips.sub .chip { font-size: 0.75rem; padding: 4px 10px; }

ul.archive { list-style: none; padding: 0; margin: 28px 0 0; border-top: 1px solid var(--border); }
ul.archive li { border-bottom: 1px solid var(--border); }
ul.archive li[hidden] { display: none; }
ul.archive a {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 16px;
    padding: 14px 8px;
    text-decoration: none;
    color: var(--text);
    border-radius: 8px;
    transition: background 0.15s ease;
}
ul.archive a:hover { background: var(--row-hover); }
ul.archive a:hover .t { color: var(--link); }
ul.archive .main { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
ul.archive .t { font-weight: 700; transition: color 0.15s ease; }
ul.archive .m { font-size: 0.8rem; color: var(--muted); }
ul.archive time { font-size: 0.8rem; color: var(--muted); white-space: nowrap; font-variant-numeric: tabular-nums; }
.empty { color: var(--muted); text-align: center; margin: 32px 0; }

@media (max-width: 600px) {
    ul.archive a { flex-direction: column; gap: 2px; padding: 12px 4px; }
}
"""

ARCHIVE_JS = """<script>
(function () {
    var list = document.getElementById("list");
    var rows = Array.prototype.slice.call(list.children);
    var q = document.getElementById("q");
    var platforms = document.getElementById("platforms");
    var subs = document.getElementById("subs");
    var empty = document.getElementById("empty");
    var params = new URLSearchParams(location.search);
    var state = { p: params.get("p") || "", s: params.get("s") || "", q: params.get("q") || "" };
    q.value = state.q;

    function render() {
        var words = state.q.toLowerCase().split(/\\s+/).filter(Boolean);
        var shown = 0;
        rows.forEach(function (li) {
            var ok = (!state.p || li.dataset.p === state.p) &&
                     (!state.s || li.dataset.s === state.s) &&
                     words.every(function (w) { return li.dataset.t.indexOf(w) !== -1; });
            li.hidden = !ok;
            if (ok) shown++;
        });
        empty.hidden = shown > 0;
        Array.prototype.forEach.call(platforms.children, function (b) {
            b.classList.toggle("on", b.dataset.p === state.p);
        });
        var anySub = false;
        Array.prototype.forEach.call(subs.children, function (b) {
            var mine = b.dataset.p === state.p;
            b.hidden = !mine;
            if (mine) anySub = true;
            b.classList.toggle("on", mine && b.dataset.s === state.s);
        });
        subs.hidden = !anySub;
        var out = new URLSearchParams();
        if (state.p) out.set("p", state.p);
        if (state.s) out.set("s", state.s);
        if (state.q) out.set("q", state.q);
        var qs = out.toString();
        history.replaceState(null, "", location.pathname + (qs ? "?" + qs : ""));
    }

    platforms.addEventListener("click", function (e) {
        var b = e.target.closest(".chip");
        if (!b) return;
        state.p = b.dataset.p;
        state.s = "";
        render();
    });
    subs.addEventListener("click", function (e) {
        var b = e.target.closest(".chip");
        if (!b) return;
        state.s = state.s === b.dataset.s ? "" : b.dataset.s;
        render();
    });
    q.addEventListener("input", function () { state.q = q.value.trim(); render(); });
    render();
})();
</script>"""


def page_shell(path, title, css, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
{THEME_SCRIPT}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{icon_links_html(path)}
{FONT_LINKS}
<title>{title}</title>
<style>{LISTING_CSS}{NAV_CSS}{css}</style>
</head>
<body>
{nav_html(path)}

{body}
<footer>&copy; 2026 wook413.</footer>
</body>
</html>
"""


def build_archive(writeups):
    posts = sorted(writeups, key=lambda p: (p.date, p.seq, natural_key(p.path)), reverse=True)

    # platform chips ordered by most recent activity
    latest = {}
    counts = {}
    sub_counts = {}
    for p in posts:
        latest.setdefault(p.platform, p.date)
        counts[p.platform] = counts.get(p.platform, 0) + 1
        if p.sub:
            sub_counts.setdefault(p.platform, {})
            sub_counts[p.platform][p.sub] = sub_counts[p.platform].get(p.sub, 0) + 1
    order = sorted(counts, key=lambda k: latest[k], reverse=True)

    chips = [f'<button type="button" class="chip" data-p="">All<span class="n">{len(posts)}</span></button>']
    chips += [f'<button type="button" class="chip" data-p="{k}">{L(k)}<span class="n">{counts[k]}</span></button>'
              for k in order]
    sub_chips = []
    for k in order:
        subs = sub_counts.get(k, {})
        if len(subs) < 2:
            continue  # a lone sub-category is the same list as its platform
        for s in sorted(subs, key=lambda s: L(s)):
            sub_chips.append(f'<button type="button" class="chip" data-p="{k}" data-s="{s}" hidden>'
                             f'{L(s)}<span class="n">{subs[s]}</span></button>')

    rows = []
    for p in posts:
        haystack = " ".join([p.title, L(p.platform), L(p.sub) if p.sub else "", " ".join(p.tags)]).lower()
        rows.append(
            f'<li data-p="{p.platform}" data-s="{p.sub}" data-t="{html.escape(haystack)}">'
            f'<a href="{rel("writeups/index.html", p.path)}"><span class="main"><span class="t">{html.escape(p.title)}</span>'
            f'<span class="m">{p.crumb}</span></span><time datetime="{p.date}">{fmt_long(p.date)}</time></a></li>')

    body = (
        '<h1>Writeups</h1>\n'
        f'<p class="lede">{len(posts)} writeups from CTF platforms and practice labs, newest first.</p>\n'
        '<input type="search" id="q" class="search" placeholder="Search by title, platform or tag…" autocomplete="off">\n'
        '<div class="chips" id="platforms">' + "".join(chips) + '</div>\n'
        '<div class="chips sub" id="subs" hidden>' + "".join(sub_chips) + '</div>\n'
        '<ul class="archive" id="list">\n' + "\n".join(rows) + '\n</ul>\n'
        '<p class="empty" id="empty" hidden>No writeups match.</p>\n' + ARCHIVE_JS
    )
    write("writeups/index.html", page_shell("writeups/index.html", "Writeups · wook413", ARCHIVE_CSS, body))


# --- projects ------------------------------------------------------------

# one-line summary per project; falls back to the first paragraph of part 1
PROJECT_BLURBS = {
    "splunk-detection-lab": "A home lab where I simulate attacks, collect the telemetry in Splunk, "
                            "and write detections against it.",
}

PROJECTS_CSS = """
.lede { color: var(--muted); margin: -18px 0 28px; font-size: 0.95rem; }

ul.projects { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
ul.projects a {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 20px 22px;
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    text-decoration: none;
    color: var(--text);
    transition: transform 0.15s ease, border-color 0.15s ease;
}
ul.projects a:hover { transform: translateY(-2px); border-color: var(--link); }
ul.projects .t { font-weight: 700; font-size: 1.1rem; }
ul.projects .desc { color: var(--muted); font-size: 0.92rem; }
ul.projects .m { font-size: 0.78rem; color: var(--muted); margin-top: 4px; }
""" + ARCHIVE_CSS


def date_range(posts):
    a, b = posts[0].date, posts[-1].date
    if a == b:
        return fmt_long(a)
    da, db = datetime.date.fromisoformat(a), datetime.date.fromisoformat(b)
    left = fmt_short(a) if da.year == db.year else fmt_long(a)
    return f"{left} – {fmt_long(b)}"


def project_blurb(slug, parts):
    if slug in PROJECT_BLURBS:
        return PROJECT_BLURBS[slug]
    m = re.search(r"</h1>.*?<p>(.*?)</p>", read(parts[0].path), re.S)
    return strip_tags(m.group(1)) if m else ""


def build_projects(projects):
    by_slug = {}
    for p in projects:
        by_slug.setdefault(p.platform, []).append(p)
    cards = []
    for slug, parts in sorted(by_slug.items(), key=lambda kv: max(p.date for p in kv[1]), reverse=True):
        parts.sort(key=lambda p: (p.date, p.seq, natural_key(p.path)))
        blurb = html.escape(project_blurb(slug, parts))
        n = f"{len(parts)} part{'s' if len(parts) != 1 else ''}"
        cards.append(
            f'<li><a href="./{slug}/index.html"><span class="t">{L(slug)}</span>'
            f'<span class="desc">{blurb}</span><span class="m">{n} · {date_range(parts)}</span></a></li>')

        series_path = f"projects/{slug}/index.html"
        rows = [
            f'<li><a href="{rel(series_path, p.path)}"><span class="main">'
            f'<span class="t">{L(os.path.splitext(os.path.basename(p.path))[0])}</span></span>'
            f'<time datetime="{p.date}">{fmt_long(p.date)}</time></a></li>'
            for p in parts]
        body = (f'{breadcrumb_html(series_path)}\n<h1>{L(slug)}</h1>\n<p class="lede">{blurb}</p>\n'
                '<ul class="archive">\n' + "\n".join(rows) + "\n</ul>")
        write(series_path, page_shell(series_path, f"{L(slug)} · wook413", PROJECTS_CSS, body))

    body = ('<h1>Projects</h1>\n<p class="lede">Hands-on builds, written up as multi-part series.</p>\n'
            '<ul class="projects">\n' + "\n".join(cards) + "\n</ul>")
    write("projects/index.html", page_shell("projects/index.html", "Projects · wook413", PROJECTS_CSS, body))


# --- home "Most Recent" --------------------------------------------------

def build_recent(posts, n=5):
    recent = sorted(posts, key=lambda p: (p.date, p.seq, natural_key(p.path)), reverse=True)[:n]
    items = []
    for p in recent:
        badge = ('<span class="badge badge-writeup">Writeup</span>' if p.kind == "writeups"
                 else '<span class="badge badge-project">Project</span>')
        sub = p.crumb if p.kind == "writeups" else L(p.platform)
        items.append(
            f'<li><a href="./{p.path}">\n'
            f'<span class="main"><span class="title">{html.escape(p.title)}</span><span class="sub">{sub}</span></span>\n'
            f'<span class="side">{badge}<span class="date">{fmt_short(p.date)}</span><span class="arrow">→</span></span>\n'
            f'</a></li>')
    text = read("index.html")
    block = '<!--recent--><ul class="recent">\n' + "\n".join(items) + "\n</ul><!--/recent-->"
    text = re.sub(r"<!--recent-->.*?<!--/recent-->", lambda m: block, text, flags=re.S)
    write("index.html", text)


# --- site-wide nav + breadcrumb -----------------------------------------

def refresh_chrome():
    for p in glob.glob("**/*.html", root_dir=REPO_ROOT, recursive=True):
        p = p.replace("\\", "/")
        text = read(p)
        if 'class="site-nav"' not in text:
            continue  # redirect stubs etc.
        new = re.sub(r'<nav class="site-nav">.*?</nav>', lambda m: nav_html(p), text, count=1, flags=re.S)
        new = re.sub(r'<div class="breadcrumb">.*?</div>', lambda m: breadcrumb_html(p), new, count=1, flags=re.S)
        # pages rendered before BRAND_CSS joined NAV_CSS carry their own copy
        brand = f'<style id="brand-css">{BRAND_CSS}</style>'
        if '<style id="brand-css">' in new:
            new = re.sub(r'<style id="brand-css">.*?</style>', lambda m: brand, new, count=1, flags=re.S)
        elif ".site-nav a.brand" not in new:
            new = new.replace("</head>", brand + "\n</head>", 1)
        # one standard set of icon links per page (pages used to carry none,
        # or root-absolute ones that break when opened from disk)
        if "<!--icons-->" in new:
            new = re.sub(r"<!--icons-->.*?<!--/icons-->", lambda m: icon_links_html(p), new, count=1, flags=re.S)
        else:
            new = re.sub(r'[ \t]*<link rel="(?:icon|apple-touch-icon|manifest)"[^>]*>\n?', "", new)
            new = new.replace("</head>", icon_links_html(p) + "\n</head>", 1)
        if new != text:
            write(p, new)


def main():
    refresh_chrome()
    posts = collect()
    groups = {}
    for p in posts:
        groups.setdefault(p.group, []).append(p)
    for members in groups.values():
        members.sort(key=lambda p: (p.date, p.seq, natural_key(p.path)))
        for i, p in enumerate(members):
            update_post(p, members[i - 1] if i else None, members[i + 1] if i + 1 < len(members) else None)
    build_archive([p for p in posts if p.kind == "writeups"])
    build_projects([p for p in posts if p.kind == "projects"])
    build_recent(posts)
    print(f"built: {len(posts)} posts, {len(groups)} collections")


if __name__ == "__main__":
    main()
