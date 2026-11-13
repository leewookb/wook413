"""Write about/index.html: hero + interactive timeline (work / education /
certifications).

    python build_about.py

Edit NODES below and re-run (order doesn't matter, they're sorted by `at`).
One straight lane per kind (work / edu / cert); nodes sit in evenly spaced
date-ordered columns shared by all lanes, and a node's `span` is drawn as a
colored segment of its lane's line, placed by interpolating between node
dates.
"""
import datetime as dt
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
from site_common import LISTING_CSS, NAV_CSS, THEME_SCRIPT, FONT_LINKS, icon_links_html, nav_html

LOGO = "../assets/logo/"
O = "../OSCP/"
TODAY = dt.date(2026, 11, 12)
D = dt.date.fromisoformat


def ext(href, text):
    return f'<a href="{href}" target="_blank" rel="noopener">{text}</a>'


# kind: work | edu | cert.  `at` places the node; `span` draws a period bar.
NODES = [
    dict(k="gsu", kind="edu", at="2021-08-01", logo="gsu_logo.png", alt="Georgia State University",
         title="B.S. Computer Science", org="Georgia State University", when="Aug 2021 – May 2024",
         span=("2021-08-01", "2024-05-01")),
    dict(k="tmobile", kind="work", at="2022-05-01", logo="t_mobile_logo.png", alt="T-Mobile",
         title="Software Engineer Intern", org="T-Mobile", when="May 2022 – Aug 2022 · Atlanta, GA",
         span=("2022-05-01", "2022-08-01")),
    dict(k="sk", kind="work", at="2024-08-01", logo="sk_on_tennessee_logo.png", alt="SK On Tennessee",
         title="Cyber Security Specialist", org="BlueOval SK → SK On Tennessee",
         when="Aug 2024 – Aug 2026 · Stanton, TN",
         note="BlueOval SK was rebranded as SK On Tennessee in May 2026.",
         span=("2024-08-01", "2026-08-01")),
    dict(k="oscp", kind="cert", at="2026-03-02", logo="offensive_security_logo.png", alt="OffSec",
         title="OSCP+ &amp; OSCP", org="OffSec", when="Issued Mar 2026 · OSCP+ valid until Mar 2029",
         links=[ext("https://credentials.offsec.com/f66586b1-cbb7-4a10-b9b2-ecf5648573c2", "Verify OSCP+ ↗"),
                ext("https://credentials.offsec.com/63b7fb02-b876-4ed2-8729-61b0f05828b8", "Verify OSCP ↗"),
                f'<a href="{O}OSCP 후기.html">OSCP 후기</a>',
                ext(f"{O}Wook OSCP Approach.svg", "Approach map"),
                ext("https://www.notion.so/leewookb/Wook-s-OSCP-Notes-2e256e0e1b6a8031a771c93385658fe9?source=copy_link",
                    "Notes ↗")]),
    dict(k="absolics", kind="work", at="2026-08-01", logo="absolics_logo.png", alt="Absolics",
         title="Cyber Security Engineer", org="Absolics Inc.", when="Aug 2026 – Nov 2026 · Covington, GA",
         span=("2026-08-01", "2026-11-01")),
    dict(k="13cubed", kind="cert", at="2026-10-13", logo="13cubed_logo.png", alt="13Cubed",
         title="Investigating Windows Endpoints (Gold)", org="13Cubed", when="Issued Oct 2026",
         links=[ext("https://credsverse.com/credentials/21136ab8-91ca-4d14-9ba3-b35d076910a6", "Verify ↗")]),
    dict(k="vertex", kind="work", at="2026-11-01", logo="vertex_inc_logo.png", alt="Vertex",
         title="Security Operations Engineer", org="Vertex Inc.", when="Nov 2026 – Present", now=True,
         span=("2026-11-01", None)),
    dict(k="aws", kind="cert", at="2021-12-01", logo="amazon_web_services_logo.png", alt="AWS",
         title="AWS Certified Cloud Practitioner", org="Amazon Web Services", when="Issued Dec 2021",
         links=[ext("https://www.credly.com/badges/da0ff6b1-edbb-4d80-8e16-914d2e229fd7", "Verify ↗")]),
    dict(k="google", kind="cert", at="2024-04-01", logo="coursera_logo.png", alt="Coursera",
         title="Google Cybersecurity Certificate", org="Google · Coursera", when="Issued Apr 2024",
         links=[ext("https://www.credly.com/badges/5e61d274-3755-4aa6-a915-35880db6f655", "Verify ↗")]),
    dict(k="secplus", kind="cert", at="2024-06-01", logo="comptia_logo.png", alt="CompTIA",
         title="Security+", org="CompTIA", when="Issued Jun 2024",
         links=[ext("https://www.credly.com/badges/81f57b79-5097-4546-897b-61bebe8b4363/public_url", "Verify ↗")]),
]
NODES.sort(key=lambda nd: nd["at"])

# --- positions: nodes evenly spaced; dates in between interpolated --------
PAD = 4.0
n = len(NODES)
xs = [PAD + i * (100 - 2 * PAD) / (n - 1) for i in range(n)]
ds = [D(nd["at"]) for nd in NODES]


def x_of(d):
    if d <= ds[0]:
        return xs[0]
    for i in range(n - 1):
        if ds[i] <= d <= ds[i + 1]:
            f = (d - ds[i]).days / max((ds[i + 1] - ds[i]).days, 1)
            return xs[i] + f * (xs[i + 1] - xs[i])
    return 100.0


def pop(nd):
    now = '<span class="now" title="Current"></span>' if nd.get("now") else ""
    out = [f'<div class="pop" role="tooltip"><div class="kind">{KIND_LABEL[nd["kind"]]}</div>'
           f'<div class="t">{nd["title"]}{now}</div>',
           f'<div class="o">{nd["org"]}</div><div class="d">{nd["when"]}</div>']
    if nd.get("note"):
        out.append(f'<div class="note">{nd["note"]}</div>')
    if nd.get("links"):
        out.append('<div class="links">' + "".join(nd["links"]) + "</div>")
    out.append("</div>")
    return "".join(out)


LANES = [("work", "Work", "Work"), ("edu", "Education", "Edu"), ("cert", "Certifications", "Cert")]
KIND_LABEL = {"work": "Work", "edu": "Education", "cert": "Certification"}
LANE_TOP = {k: 40 + i * 62 for i, (k, _, _) in enumerate(LANES)}  # px; lane line sits 20px below
TRACK_H = LANE_TOP[LANES[-1][0]] + 48

heads_html, nodes_html = [], []
bars_html = {k: [] for k, _, _ in LANES}
prev_year = None
for nd, x in zip(NODES, xs):
    d = D(nd["at"])
    yr = f"<b>{d.year}</b>" if d.year != prev_year else "<b></b>"
    prev_year = d.year
    heads_html.append(f'<span class="hd" style="--x:{x:.2f}%">{yr}{d:%b}</span>')
    # popovers near either end anchor to that side so they never overflow
    edge = " first" if x < 25 else (" last" if x > 75 else "")
    nodes_html.append(
        f'<div class="node {nd["kind"]}{edge}" style="--x:{x:.2f}%;--y:{LANE_TOP[nd["kind"]]}px" '
        f'data-k="{nd["k"]}" tabindex="0">'
        f'<img class="logo" src="{LOGO}{nd["logo"]}" alt="{nd["alt"]} logo" width="40" height="40">'
        f'{pop(nd)}</div>')
    if nd.get("span"):
        a = x_of(D(nd["span"][0]))
        b = x_of(D(nd["span"][1])) if nd["span"][1] else 100.0
        bars_html[nd["kind"]].append(
            f'<span class="bar" data-k="{nd["k"]}" style="left:{a:.2f}%;width:{max(b - a, 0.8):.2f}%"></span>')

lanes_html = "".join(
    f'<div class="lane {k}" style="--y:{LANE_TOP[k]}px"><span class="lbl">'
    f'<span class="full">{label}</span><span class="short">{short}</span></span>'
    f'<div class="line">{"".join(bars_html[k])}</div></div>'
    for k, label, short in LANES)


CSS = """
:root {
    --c-work: #6db2ff;
    --c-edu: #b99cf5;
    --c-cert: #4cc277;
}
:root[data-theme="light"] {
    --c-work: #0f5fae;
    --c-edu: #7a4fd0;
    --c-cert: #1a7f37;
}

.hero h1 { margin: 0; }
.hero .role { margin: 14px 0 0; font-size: 1.05rem; font-weight: 600; }
.hero .blurb { margin: 8px 0 0; color: var(--muted); max-width: 560px; text-wrap: pretty; }
.hero .nowline {
    display: inline-flex; align-items: center; gap: 8px; margin: 14px 0 0;
    padding: 4px 12px; border: 1px solid var(--border); border-radius: 999px;
    font-size: 0.78rem; font-weight: 600; color: var(--muted);
}
.hero .nowline .dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #3fb950; box-shadow: 0 0 0 3px rgba(63, 185, 80, 0.18);
}
.hero .links { display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0 0; }
.hero .links a {
    font-size: 0.82rem; font-weight: 600; padding: 7px 14px; border-radius: 999px;
    border: 1px solid var(--border); color: var(--text); text-decoration: none;
    transition: border-color 0.15s ease, color 0.15s ease;
}
.hero .links a:hover { border-color: var(--link); color: var(--link); }

h2 { margin-top: 56px; margin-bottom: 18px; }

.logo {
    display: block; width: 40px; height: 40px; border-radius: 10px; object-fit: cover;
    outline: 1px solid rgba(255, 255, 255, 0.07); outline-offset: -1px;
}
:root[data-theme="light"] .logo { outline-color: rgba(0, 0, 0, 0.07); }

/* -- swimlane timeline: one straight line per kind, shared time columns -- */
.tl { --label-w: 104px; position: relative; margin: 0 0 190px; }
.tl .track { position: relative; margin-left: var(--label-w); height: """ + str(TRACK_H) + """px; }

.hd {
    position: absolute; left: var(--x); top: 0; transform: translateX(-50%);
    display: flex; flex-direction: column; align-items: center;
    font-size: 0.72rem; color: var(--muted); line-height: 1.3;
}
.hd b { height: 1.3em; font-weight: 700; letter-spacing: 0.04em; color: var(--text); opacity: 0.7; }

.lane { position: absolute; left: calc(-1 * var(--label-w)); right: 0; top: var(--y); height: 40px; }
.lane .lbl {
    position: absolute; left: 0; top: 50%; transform: translateY(-50%);
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted);
}
.lane .line { position: absolute; left: var(--label-w); right: 0; top: 50%; height: 1px; background: var(--border); }
/* periods: colored stretches of the lane's own line */
.bar {
    position: absolute; top: -1px; height: 3px; border-radius: 999px;
    opacity: 0.5; transition: opacity 0.15s ease, height 0.15s ease, top 0.15s ease;
}
.lane.work .bar { background: var(--c-work); }
.lane.edu .bar { background: var(--c-edu); }
.bar.on { opacity: 1; top: -2px; height: 5px; }

.lane .lbl .short { display: none; }

/* node is centered on its lane line (line sits 20px below --y) */
.node {
    position: absolute; left: var(--x); top: calc(var(--y) + 20px); transform: translate(-50%, -50%);
    outline: none; cursor: pointer; z-index: 1;
}
.node .logo { box-shadow: 0 0 0 3px var(--bg), 0 0 0 4px var(--border); transition: transform 0.15s ease, box-shadow 0.15s ease; }
.node:focus-within, .node.open { z-index: 5; }
.node:focus-visible .logo, .node.open .logo {
    transform: translateY(-2px); box-shadow: 0 0 0 3px var(--bg), 0 0 0 4px var(--muted);
}
@media (hover: hover) {
    .node:hover { z-index: 5; }
    .node:hover .logo { transform: translateY(-2px); box-shadow: 0 0 0 3px var(--bg), 0 0 0 4px var(--muted); }
    .node:hover .pop { opacity: 1; visibility: visible; pointer-events: auto; transform: translate(-50%, 0); }
    .node.first:hover .pop, .node.last:hover .pop { transform: translate(0, 0); }
}

/* --shift is set by JS so the popover never leaves the viewport */
.pop {
    position: absolute; top: 100%; left: 50%; width: min(270px, calc(100vw - 32px));
    translate: var(--shift, 0px) 0;
    transform: translate(-50%, 6px);
    padding: 14px 16px; margin-top: 10px;
    background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
    text-align: left; font-size: 0.85rem; line-height: 1.5;
    opacity: 0; visibility: hidden; pointer-events: none;
    transition: opacity 0.15s ease, transform 0.15s ease, visibility 0.15s;
}
.pop::before { content: ""; position: absolute; left: 0; right: 0; top: -18px; height: 18px; }
.node.first .pop { left: 0; transform: translate(0, 6px); }
.node.last .pop { left: auto; right: 0; transform: translate(0, 6px); }
.node:focus-within .pop, .node.open .pop {
    opacity: 1; visibility: visible; pointer-events: auto; transform: translate(-50%, 0);
}
.node.first:focus-within .pop, .node.first.open .pop,
.node.last:focus-within .pop, .node.last.open .pop { transform: translate(0, 0); }
.pop .kind { font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
.node.work .kind { color: var(--c-work); }
.node.edu .kind { color: var(--c-edu); }
.node.cert .kind { color: var(--c-cert); }
.pop .t { font-weight: 700; font-size: 0.95rem; color: var(--text); }
.pop .o { color: var(--text); }
.pop .d, .pop .note { color: var(--muted); font-size: 0.8rem; }
.pop .note { margin-top: 4px; }
.pop .links { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.pop .links a {
    font-size: 0.75rem; font-weight: 600; padding: 4px 10px; border-radius: 999px;
    border: 1px solid var(--border); color: var(--text); text-decoration: none;
}
.pop .links a:hover { border-color: var(--link); color: var(--link); }
.now {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%; margin-left: 8px; vertical-align: 2px;
    background: #3fb950; box-shadow: 0 0 0 3px rgba(63, 185, 80, 0.18);
}

/* -- phones: same swimlane timeline, just compacted to fit -- */
@media (max-width: 640px) {
    .tl { --label-w: 40px; }
    .lane .lbl { font-size: 0.6rem; letter-spacing: 0.06em; }
    .lane .lbl .full { display: none; }
    .lane .lbl .short { display: inline; }
    .hd { font-size: 0.6rem; }
    .hd b { letter-spacing: 0.02em; }
    .node .logo {
        width: 24px; height: 24px; border-radius: 6px;
        box-shadow: 0 0 0 2px var(--bg), 0 0 0 3px var(--border);
    }
    .node:focus-visible .logo, .node.open .logo { box-shadow: 0 0 0 2px var(--bg), 0 0 0 3px var(--muted); }
    .pop .links a { padding: 6px 11px; }
}
"""

JS = """<script>
(function () {
    var tl = document.getElementById("tl");
    var bars = tl.querySelectorAll(".bar");
    function light(k) {
        bars.forEach(function (b) { b.classList.toggle("on", b.dataset.k === k); });
    }
    function closeAll() {
        tl.querySelectorAll(".node.open").forEach(function (o) { o.classList.remove("open"); });
        var a = document.activeElement;
        if (a && tl.contains(a)) a.blur();
    }
    // nudge the popover sideways so it stays inside the viewport
    function place(n) {
        var p = n.querySelector(".pop");
        p.style.setProperty("--shift", "0px");
        var r = p.getBoundingClientRect(), vw = document.documentElement.clientWidth, m = 12, s = 0;
        if (r.left < m) s = m - r.left;
        else if (r.right > vw - m) s = vw - m - r.right;
        p.style.setProperty("--shift", s + "px");
    }
    tl.querySelectorAll(".node").forEach(function (n) {
        n.addEventListener("mouseenter", function () { place(n); light(n.dataset.k); });
        n.addEventListener("mouseleave", function () { light(null); });
        n.addEventListener("focusin", function () { place(n); light(n.dataset.k); });
        n.addEventListener("focusout", function () { light(null); });
        // touch / click: pin the popover open, tap again to close
        n.addEventListener("click", function (e) {
            if (e.target.closest("a")) return;
            var was = n.classList.contains("open");
            closeAll();
            if (!was) { place(n); n.classList.add("open"); n.focus(); light(n.dataset.k); }
            else light(null);
        });
    });
    document.addEventListener("click", function (e) {
        if (!e.target.closest("#tl .node")) closeAll();
    });
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            closeAll();
            if (document.activeElement && tl.contains(document.activeElement)) document.activeElement.blur();
        }
    });
})();
</script>"""

body = f"""<section class="hero">
<h1>Wook Lee</h1>
<p class="role">Security Operations Engineer</p>
<p class="blurb">DFIR, threat hunting and detection engineering.</p>
<p class="nowline"><span class="dot"></span>Now: studying for GCFA</p>
<div class="links"><a href="https://www.linkedin.com/in/leewookb" target="_blank" rel="noopener">LinkedIn ↗</a><a href="mailto:leewookb@gmail.com">leewookb@gmail.com</a></div>
</section>

<h2>Timeline</h2>
<div class="tl" id="tl">
<div class="track">
{"".join(heads_html)}
{lanes_html}
{chr(10).join(nodes_html)}
</div>
</div>
{JS}
"""

out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
{THEME_SCRIPT}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{icon_links_html("about/index.html")}
{FONT_LINKS}
<title>About · wook413</title>
<style>{LISTING_CSS}{NAV_CSS}{CSS}</style>
</head>
<body>
{nav_html("about/index.html")}

{body}
<footer>&copy; 2026 wook413.</footer>
</body>
</html>
"""
open("about/index.html", "w", encoding="utf-8", newline="\n").write(out)
print("about ok")
