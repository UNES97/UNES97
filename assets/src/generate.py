"""
Generates the animated SVGs used in the profile README (light + dark versions).

    python assets/src/generate.py            # run from the repo root; needs fontTools (pip install fonttools)

Fonts (Plus Jakarta Sans, OFL) are read from the `website` branch, subset to the
characters actually used and embedded, so the SVGs look identical everywhere.
"""
import base64
import io
import subprocess
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets"
FONT_PATHS = {"JX": "src/app/fonts/PlusJakartaSans-ExtraBold.ttf", "JS": "src/app/fonts/PlusJakartaSans-SemiBold.ttf"}

THEMES = {
    "light": dict(bg="#f2efe7", panel="#fbfaf6", ink="#0f1013", ink2="#44454d", ink3="#66676f", line="#ddd9cf",
                  grid="rgba(15,16,19,0.07)", cobalt="#2a3bff", on_cobalt="#f2efe7", track="#e3dfd5"),
    "dark": dict(bg="#0f1013", panel="#17181c", ink="#f2efe7", ink2="#c9c7c0", ink3="#9a9aa2", line="#2a2b31",
                 grid="rgba(242,239,231,0.06)", cobalt="#5263ff", on_cobalt="#ffffff", track="#2a2b31"),
}

# ───────────────────────── content ─────────────────────────
META = "Casablanca, Morocco  ·  Lead Software Engineer at Maxmind.ma"
HERO_LINES = ["I build software", "that connects"]
IDEA, REALITY = "ideas", "reality."
SUB = "Full-stack  ·  web apps, business platforms & APIs  ·  from database to deployment"

GROUPS = {  # symbol, name — grouped like element families
    "Backend": [("Ph", "PHP"), ("Sy", "Symfony"), ("Lv", "Laravel"), ("Ci", "CodeIgniter"), ("Nd", "Node.js"), ("Ex", "Express"), ("Py", "Python")],
    "Frontend": [("Js", "JavaScript"), ("Ts", "TypeScript"), ("Re", "React"), ("Nx", "Next.js"), ("Vu", "Vue.js"), ("Tw", "Tailwind")],
    "Data": [("My", "MySQL"), ("Pg", "PostgreSQL"), ("Rd", "Redis"), ("Dr", "Dremio")],
    "DevOps": [("Dk", "Docker"), ("Lx", "Linux"), ("Gt", "Git"), ("Ap", "Apache")],
    "AI": [("Lc", "LangChain"), ("Tf", "Transformers")],
}
GROUP_COLORS = {
    "light": {"Backend": ("#e4e6ff", "#1d2bd6"), "Frontend": ("#ffe5d9", "#b8410c"), "Data": ("#d9f3e4", "#0e7343"),
              "DevOps": ("#ebe6da", "#0f1013"), "AI": ("#ece6ff", "#5b35d5")},
    "dark": {"Backend": ("#1c2150", "#9aa4ff"), "Frontend": ("#3a2419", "#ffab84"), "Data": ("#15301f", "#7fe0a8"),
             "DevOps": ("#26262b", "#f2efe7"), "AI": ("#2a2145", "#c4b2ff")},
}
STAGES = [("Understand", "the problem"), ("Model", "the data"), ("Build", "the backend"), ("Shape", "the interface"), ("Ship", "to production")]
PIPE_TITLE, PIPE_LIVE, PIPE_RIGHT = "HOW I SHIP", "live in production", "idea  →  production"
STACK_TITLE, STACK_NOTE = "THE PERIODIC TABLE OF MY STACK", "23 elements, one engineer"


# ───────────────────────── fonts ─────────────────────────
def load_font_bytes(key):
    return subprocess.run(["git", "show", f"website:{FONT_PATHS[key]}"], cwd=ROOT, capture_output=True, check=True).stdout


def subset_b64(raw, text):
    font = TTFont(io.BytesIO(raw))
    opts = subset.Options()
    opts.flavor = "woff"
    opts.layout_features = ["kern", "liga"]
    sub = subset.Subsetter(opts)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


class Metrics:
    def __init__(self, raw):
        f = TTFont(io.BytesIO(raw))
        self.upm = f["head"].unitsPerEm
        self.cmap = f.getBestCmap()
        self.hmtx = f["hmtx"]

    def width(self, text, size, tracking=0.0):
        units = sum(self.hmtx[self.cmap[ord(ch)]][0] for ch in text if ord(ch) in self.cmap)
        return units / self.upm * size + tracking * max(len(text) - 1, 0)


def font_css(fonts):
    return "".join(f"@font-face{{font-family:{k};src:url(data:font/woff;base64,{v}) format('woff');}}" for k, v in fonts.items())


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ───────────────────────── hero ─────────────────────────
def hero(t, fonts, mx):
    W, H, X = 840, 340, 44
    size, track = 58, -2.2
    idea_w = mx.width(IDEA, size, track)
    real_w = mx.width(REALITY, size, track)
    a0 = X + idea_w + 22  # arrow start
    a1 = a0 + 96
    rx0 = a1 + 20  # reality block
    rb_w = real_w + 34
    y3 = 262
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Younes Noufair — I build software that connects ideas to reality.">
<style>{font_css(fonts)}
.jx{{font-family:JX,sans-serif;font-weight:800;letter-spacing:{track}px}}
.js{{font-family:JS,sans-serif;font-weight:600}}
.up{{animation:up .9s cubic-bezier(.22,1,.36,1) both}}
@keyframes up{{from{{opacity:0;transform:translateY(26px)}}}}
.idea{{fill:none;stroke:{t['ink']};stroke-width:1.6;stroke-dasharray:700;stroke-dashoffset:700;animation:draw 1.6s ease-out .6s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.arrow{{fill:none;stroke:{t['cobalt']};stroke-width:5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:draw .7s ease-in-out 1.7s forwards}}
.head{{opacity:0;animation:fade .2s linear 2.35s forwards}}
@keyframes fade{{to{{opacity:1}}}}
.pop{{transform-box:fill-box;transform-origin:30% 60%;animation:pop .7s cubic-bezier(.34,1.56,.64,1) 2.35s both}}
@keyframes pop{{from{{opacity:0;transform:scale(.55) rotate(-8deg)}}}}
.dot{{animation:blink 2.4s ease-in-out infinite}}
@keyframes blink{{50%{{opacity:.3}}}}
</style>
<defs><pattern id="g" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="{t['grid']}" stroke-width="1"/></pattern>
<radialGradient id="fadeg" cx="35%" cy="45%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#fadeg)"/></mask></defs>
<rect width="{W}" height="{H}" rx="24" fill="{t['bg']}" stroke="{t['line']}" stroke-width="1"/>
<rect width="{W}" height="{H}" rx="24" fill="url(#g)" mask="url(#m)"/>
<g class="up" style="animation-delay:.05s">
  <circle class="dot" cx="{X + 5}" cy="52" r="5" fill="#17b26a"/>
  <text class="js" x="{X + 18}" y="57" font-size="15" fill="{t['ink2']}">{esc(META)}</text>
</g>
<text class="jx up" style="animation-delay:.15s" x="{X}" y="128" font-size="{size}" fill="{t['ink']}">{esc(HERO_LINES[0])}</text>
<text class="jx up" style="animation-delay:.3s" x="{X}" y="194" font-size="{size}" fill="{t['ink']}">{esc(HERO_LINES[1])}</text>
<text class="jx idea" x="{X + 6}" y="{y3}" font-size="{size}" transform="skewX(-10) translate({y3 * 0.176:.1f} 0)">{esc(IDEA)}</text>
<path class="arrow" pathLength="1" d="M{a0:.1f} {y3 - 20} C {a0 + 30:.1f} {y3 - 44}, {a0 + 60:.1f} {y3 + 6}, {a1:.1f} {y3 - 20}"/>
<path class="arrow head" d="M{a1 - 14:.1f} {y3 - 33} L{a1:.1f} {y3 - 20} L{a1 - 15:.1f} {y3 - 8}"/>
<g transform="rotate(-2 {rx0 + rb_w / 2:.1f} {y3 - 20})">
  <g class="pop">
    <rect x="{rx0:.1f}" y="{y3 - 54}" width="{rb_w:.1f}" height="72" rx="14" fill="{t['cobalt']}"/>
    <text class="jx" x="{rx0 + 17:.1f}" y="{y3}" font-size="{size}" fill="{t['on_cobalt']}">{esc(REALITY)}</text>
  </g>
</g>
<text class="js up" style="animation-delay:.6s" x="{X}" y="312" font-size="14.5" fill="{t['ink3']}">{esc(SUB)}</text>
</svg>"""


# ───────────────────────── periodic table ─────────────────────────
def stack(t, theme, fonts):
    W, cols, tile, gap, top = 840, 9, 82, 8, 74
    X = (W - (cols * tile + (cols - 1) * gap)) // 2  # centre the grid
    items = [(g, sym, name) for g, lst in GROUPS.items() for sym, name in lst]
    rows = (len(items) + cols - 1) // cols
    H = top + rows * tile + (rows - 1) * gap + 28
    cells = []
    for i, (g, sym, name) in enumerate(items):
        r, c = divmod(i, cols)
        x, y = X + c * (tile + gap), top + r * (tile + gap)
        bg, fg = GROUP_COLORS[theme][g]
        cells.append(f"""<g class="t" style="animation-delay:{0.15 + i * 0.045:.2f}s">
  <rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="12" fill="{bg}"/>
  <text class="js" x="{x + 9}" y="{y + 17}" font-size="10.5" fill="{fg}" opacity=".75">{i + 1}</text>
  <text class="jx" x="{x + tile / 2}" y="{y + 52}" font-size="30" text-anchor="middle" fill="{fg}">{sym}</text>
  <text class="js" x="{x + tile / 2}" y="{y + 70}" font-size="10" text-anchor="middle" fill="{t['ink2']}">{esc(name)}</text>
</g>""")
    # legend in the empty cells of the last row (like the gap in a real periodic table)
    used = len(items) % cols or cols
    lx = X + used * (tile + gap) + 14
    ly = top + (rows - 1) * (tile + gap) + 12
    legend = []
    for j, g in enumerate(GROUPS):
        bg, fg = GROUP_COLORS[theme][g]
        col, row = divmod(j, 3)
        gx, gy = lx + col * 130, ly + row * 22
        legend.append(f'<rect x="{gx}" y="{gy}" width="14" height="14" rx="4" fill="{bg}" stroke="{fg}" stroke-opacity=".5"/><text class="js" x="{gx + 22}" y="{gy + 11.5}" font-size="12" fill="{t["ink2"]}">{g}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="The periodic table of my stack: {esc(', '.join(n for _, _, n in items))}">
<style>{font_css(fonts)}
.jx{{font-family:JX,sans-serif;font-weight:800;letter-spacing:-1px}}
.js{{font-family:JS,sans-serif;font-weight:600}}
.t{{animation:in .55s cubic-bezier(.22,1,.36,1) both}}
@keyframes in{{from{{opacity:0;transform:translateY(10px)}}}}
</style>
<rect width="{W}" height="{H}" rx="24" fill="{t['bg']}" stroke="{t['line']}" stroke-width="1"/>
<text class="js" x="{X}" y="44" font-size="12.5" letter-spacing="3" fill="{t['cobalt']}">{STACK_TITLE}</text>
<text class="js" x="{W - X}" y="44" font-size="13" text-anchor="end" fill="{t['ink3']}">{STACK_NOTE}</text>
{''.join(cells)}
<g class="t" style="animation-delay:1.3s">{''.join(legend)}</g>
</svg>"""


# ───────────────────────── pipeline ─────────────────────────
def pipeline(t, fonts):
    W, H, X0, X1, Y = 840, 220, 96, 744, 112
    n = len(STAGES)
    xs = [X0 + i * (X1 - X0) / (n - 1) for i in range(n)]
    period = 9.0
    run = 6.0  # seconds for the bar to cross; then hold, then restart
    css, nodes = [], []
    for i, (title, sub) in enumerate(STAGES):
        at = (i / (n - 1)) * run / period * 100  # % of the loop when the bar reaches this node
        on = min(at + 0.5, 99)
        css.append(f"@keyframes n{i}{{0%,{at:.1f}%{{fill:{t['panel']};stroke:{t['line']}}}{on:.1f}%,94%{{fill:{t['cobalt']};stroke:{t['cobalt']}}}100%{{fill:{t['panel']};stroke:{t['line']}}}}}"
                   f"@keyframes c{i}{{0%,{at:.1f}%{{opacity:0}}{on + 1:.1f}%,94%{{opacity:1}}100%{{opacity:0}}}}"
                   f"@keyframes l{i}{{0%,{at:.1f}%{{fill:{t['ink3']}}}{on:.1f}%,94%{{fill:{t['ink']}}}100%{{fill:{t['ink3']}}}}}"
                   f"@keyframes k{i}{{0%,{at:.1f}%{{opacity:1}}{on:.1f}%,94%{{opacity:0}}100%{{opacity:1}}}}")
        x = xs[i]
        nodes.append(f"""<circle cx="{x:.1f}" cy="{Y}" r="22" stroke-width="2" style="animation:n{i} {period}s linear infinite"/>
<text class="jx" x="{x:.1f}" y="{Y + 5}" font-size="13" text-anchor="middle" fill="{t['ink3']}" style="animation:k{i} {period}s linear infinite">{i + 1:02d}</text>
<path d="M{x - 8:.1f} {Y} l5.5 5.5 l10 -11" fill="none" stroke="{t['on_cobalt']}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0;animation:c{i} {period}s linear infinite"/>
<text class="jx" x="{x:.1f}" y="{Y + 52}" font-size="16" text-anchor="middle" style="animation:l{i} {period}s linear infinite">{esc(title)}</text>
<text class="js" x="{x:.1f}" y="{Y + 71}" font-size="12.5" text-anchor="middle" fill="{t['ink3']}">{esc(sub)}</text>""")
    hold = run / period * 100
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="How I ship: understand the problem, model the data, build the backend, shape the interface, ship to production.">
<style>{font_css(fonts)}
.jx{{font-family:JX,sans-serif;font-weight:800;letter-spacing:-.3px}}
.js{{font-family:JS,sans-serif;font-weight:600}}
.bar{{transform-box:fill-box;transform-origin:0 50%;animation:bar {period}s cubic-bezier(.45,0,.55,1) infinite}}
@keyframes bar{{0%{{transform:scaleX(0)}}{hold:.1f}%,94%{{transform:scaleX(1)}}100%{{transform:scaleX(0);opacity:0}}}}
.live{{animation:live {period}s linear infinite}}
@keyframes live{{0%,{hold:.1f}%{{opacity:0}}{hold + 2:.1f}%,94%{{opacity:1}}100%{{opacity:0}}}}
{''.join(css)}
</style>
<rect width="{W}" height="{H}" rx="24" fill="{t['bg']}" stroke="{t['line']}" stroke-width="1"/>
<text class="js" x="40" y="44" font-size="12.5" letter-spacing="3" fill="{t['cobalt']}">{PIPE_TITLE}</text>
<g class="live"><rect x="{W - 214}" y="26" width="174" height="28" rx="14" fill="#17b26a" fill-opacity=".14"/>
<circle cx="{W - 196}" cy="40" r="5" fill="#17b26a"/><text class="js" x="{W - 184}" y="45" font-size="13" fill="#17b26a">{PIPE_LIVE}</text></g>
<rect x="{X0}" y="{Y - 2}" width="{X1 - X0}" height="4" rx="2" fill="{t['track']}"/>
<rect class="bar" x="{X0}" y="{Y - 2}" width="{X1 - X0}" height="4" rx="2" fill="{t['cobalt']}"/>
{''.join(nodes)}
</svg>"""


def main():
    raw = {k: load_font_bytes(k) for k in FONT_PATHS}
    texts = [META, *HERO_LINES, IDEA, REALITY, SUB, STACK_TITLE, STACK_NOTE, PIPE_TITLE, PIPE_LIVE, PIPE_RIGHT,
             *[s + n for lst in GROUPS.values() for s, n in lst], *GROUPS.keys(), *[a + b for a, b in STAGES], "0123456789"]
    charset = "".join(sorted(set("".join(texts))))
    fonts = {k: subset_b64(v, charset) for k, v in raw.items()}
    mx = Metrics(raw["JX"])
    OUT.mkdir(exist_ok=True)
    for theme, t in THEMES.items():
        (OUT / f"hero-{theme}.svg").write_text(hero(t, fonts, mx), encoding="utf-8")
        (OUT / f"stack-{theme}.svg").write_text(stack(t, theme, fonts), encoding="utf-8")
        (OUT / f"pipeline-{theme}.svg").write_text(pipeline(t, fonts), encoding="utf-8")
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.name:24} {p.stat().st_size / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
