"""
Scene "quests": career as an anime arc list / RPG quest log.

    python assets/src/scene_quests.py      # from the repo root → assets/quests-light.svg, assets/quests-dark.svg

A wavy route draws itself left → right through the chapters (stroke-dashoffset, eased), a marker rides the
draw-head (SMIL animateMotion, same easing), each chapter gets cleared with a check stamp + "+EXP" pop while the
EXP bar fills. Then only gentle perpetual motion: the boss-level node pulses, the next arc loads.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import THEMES, W, Metrics, esc, font_css, write  # noqa: E402

H = 380
PAD = 44

# ───────────────────────── content (facts only) ─────────────────────────
TITLE = "QUEST LOG"
JP = "ユネスの冒険"
SAVE = "SAVE FILE: UNES97"
QUESTS = [  # kicker, title, subtitle, extra lines
    ("PROLOGUE", "DTS Software Development", "ISTA NTIC  ·  2017–2019", []),
    ("TRAINING ARC", "Licence Pro Web Development", "Hassan II University  ·  2019–2020", []),
    ("FIRST QUEST", "PHP Developer", "Version Digitale  ·  2020", []),
    ("MAIN QUEST", "Software Engineer", "Maxmind  ·  2021–2023",
     ["Party: Maersk – APM Terminals", "Checkinfo  ·  Forvis Mazars  (via Maxmind)"]),
    ("BOSS LEVEL", "Lead Software Engineer", "Maxmind.ma  ·  2024 → now", []),
    ("NEXT ARC", "AI  ·  LLMs  ·  RAG  ·  agents", "LOADING…", []),
]
CLEARED = "CLEARED"
IN_PROGRESS = "IN PROGRESS"
POP = "+EXP"
EXP_L, EXP_R = "EXP", "6+ YEARS"

# ───────────────────────── geometry ─────────────────────────
XS = [128 + 116 * i for i in range(6)]          # 128 … 708
Y_TOP, Y_BOT = 146, 222
YS = [Y_TOP if i % 2 == 0 else Y_BOT for i in range(6)]
NODES = list(zip(XS, YS))
HANDLE = 116 * 0.52

# timing (s)
DRAW_START, DRAW_DUR = 0.45, 2.75
EASE = (0.42, 0.0, 0.5, 1.0)  # mild ease-in-out for the route + rider


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def segs(a, b):
    out = []
    for i in range(a, b):
        (x0, y0), (x1, y1) = NODES[i], NODES[i + 1]
        out.append(((x0, y0), (x0 + HANDLE, y0), (x1 - HANDLE, y1), (x1, y1)))
    return out


def path_d(a, b):
    s = segs(a, b)
    d = f"M{s[0][0][0]},{s[0][0][1]}"
    for _, c1, c2, p in s:
        d += f" C{c1[0]:.1f},{c1[1]} {c2[0]:.1f},{c2[1]} {p[0]},{p[1]}"
    return d


def seg_len(s, n=400):
    pts = [bez(*s, i / n) for i in range(n + 1)]
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(n))


def cubic_ease(p, x):
    """CSS cubic-bezier(p) evaluated at progress-time x → output progress."""
    x1, y1, x2, y2 = p
    lo, hi = 0.0, 1.0
    for _ in range(60):
        t = (lo + hi) / 2
        bx = 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t * t * x2 + t**3
        lo, hi = (t, hi) if bx < x else (lo, t)
    t = (lo + hi) / 2
    return 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t * t * y2 + t**3


def time_for_progress(p, y):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if cubic_ease(p, m) < y else (lo, m)
    return (lo + hi) / 2


SOLID = segs(0, 4)
LENS = [seg_len(s) for s in SOLID]
L = sum(LENS)
CUM = [0.0]
for ln in LENS:
    CUM.append(CUM[-1] + ln)
T_NODE = [DRAW_START + DRAW_DUR * time_for_progress(EASE, c / L) for c in CUM]  # nodes 1..5
T_NODE[0] = DRAW_START + 0.05
T_NEXT = T_NODE[4] + 0.45  # next arc appears


def build(theme: str) -> str:
    t = THEMES[theme]
    mx, ms = Metrics("JX"), Metrics("JS")
    ink_on_yellow = "#0f1013"
    track = t["line"]
    all_text = TITLE + SAVE + CLEARED + IN_PROGRESS + POP + EXP_L + EXP_R + "0123456789."
    for k, a, b, extra in QUESTS:
        all_text += k + a + b + "".join(extra)

    css = [font_css(all_text, keys=("JX", "JS")), font_css(JP, keys=("JP",)).split(".jx{")[0]]
    e_pop = "cubic-bezier(.34,1.56,.64,1)"
    e_out = "cubic-bezier(.2,.8,.2,1)"
    ease_css = "cubic-bezier({},{},{},{})".format(*EASE)
    css.append(f"""
@keyframes rise{{from{{opacity:0;transform:translateY(7px)}}to{{opacity:1;transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes slideIn{{from{{opacity:0;transform:translateX(-14px)}}to{{opacity:1;transform:none}}}}
@keyframes draw{{from{{stroke-dashoffset:{L:.1f}}}to{{stroke-dashoffset:0}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(.2)}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes stamp{{0%{{opacity:0;transform:scale(1.9) rotate(-18deg)}}60%{{opacity:1}}100%{{opacity:1;transform:scale(1) rotate(0)}}}}
@keyframes check{{from{{stroke-dashoffset:16}}to{{stroke-dashoffset:0}}}}
@keyframes ring{{0%{{opacity:.55;transform:scale(1)}}100%{{opacity:0;transform:scale(1.75)}}}}
@keyframes exp{{0%{{opacity:0;transform:translateY(4px)}}25%{{opacity:1}}70%{{opacity:1}}100%{{opacity:0;transform:translateY(-12px)}}}}
@keyframes march{{to{{stroke-dashoffset:-18}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes seg{{0%,100%{{opacity:.18}}20%{{opacity:1}}45%{{opacity:.18}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes breathe{{0%,100%{{opacity:.35}}50%{{opacity:.9}}}}
@keyframes tri{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(1.2px)}}}}
.k{{font-size:9.5px;letter-spacing:1.6px}}
.ti{{font-size:13.5px;letter-spacing:-.15px}}
.su{{font-size:11px}}
.pt{{font-size:10px}}
.a{{animation:rise .55s {e_out} both}}
.route{{stroke-dasharray:{L:.1f} {L + 10:.1f};animation:draw {DRAW_DUR}s {ease_css} {DRAW_START}s both}}
""")

    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
             f'aria-label="Quest log: DTS Software Development at ISTA NTIC (2017–2019), Licence Pro Web Development at '
             f'Hassan II University (2019–2020), PHP Developer at Version Digitale (2020), Software Engineer at Maxmind '
             f'(2021–2023), Lead Software Engineer at Maxmind.ma (2024 – now), next: AI.">')
    o.append(f"<style>{''.join(css)}</style>")
    o.append(f'<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
             f'<circle cx="11" cy="11" r="0.9" fill="{t["grid"]}"/></pattern></defs>')
    o.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="24" fill="{t["bg"]}" stroke="{t["line"]}"/>')
    o.append(f'<rect x="1" y="66" width="{W - 2}" height="250" fill="url(#dots)"/>')

    # ── header ──
    o.append(f'<g style="animation:slideIn .6s {e_out} both">')
    o.append(f'<text x="{PAD}" y="46" class="jx" font-size="24" letter-spacing="1.5" fill="{t["ink"]}">{TITLE}</text>')
    tw = mx.width(TITLE, 24, 1.5)
    o.append(f'<rect x="{PAD + tw + 14}" y="28" width="2" height="20" rx="1" fill="{t["cobalt"]}"/>')
    o.append(f'<text x="{PAD + tw + 26}" y="44" class="jp" font-size="13" letter-spacing="1" fill="{t["ink3"]}">{JP}</text>')
    o.append("</g>")
    sw = mx.width(SAVE, 10, 1.4)
    px1 = W - PAD
    px0 = px1 - sw - 40
    o.append(f'<g style="animation:fade .6s ease .15s both">')
    o.append(f'<rect x="{px0:.1f}" y="25" width="{px1 - px0:.1f}" height="26" rx="13" fill="{t["panel"]}" stroke="{t["line"]}"/>')
    o.append(f'<rect x="{px0 + 14:.1f}" y="34" width="7" height="8" rx="1.5" fill="{t["cobalt"]}" '
             f'style="animation:blink 1.1s steps(1) infinite"/>')
    o.append(f'<text x="{px0 + 28:.1f}" y="41.6" class="jx" font-size="10" letter-spacing="1.4" fill="{t["ink2"]}">{SAVE}</text>')
    o.append("</g>")

    # ── route ──
    o.append(f'<path d="{path_d(0, 4)}" fill="none" stroke="{track}" stroke-width="2" stroke-linecap="round" '
             f'style="animation:fade .5s ease .1s both"/>')
    o.append(f'<path d="{path_d(4, 5)}" fill="none" stroke="{t["ink3"]}" stroke-width="2" stroke-linecap="round" '
             f'stroke-dasharray="2 7" opacity=".55" style="animation:march 1.2s linear infinite"/>')
    o.append(f'<path class="route" d="{path_d(0, 4)}" fill="none" stroke="{t["cobalt"]}" stroke-width="3" stroke-linecap="round"/>')

    # ── nodes ──
    for i, ((x, y), (kick, title, sub, extra)) in enumerate(zip(NODES, QUESTS)):
        top = y == Y_TOP
        tn = T_NODE[i] if i < 5 else T_NEXT
        # slot (visible from the start)
        o.append(f'<g transform="translate({x},{y})">')
        if i < 4:
            o.append(f'<circle r="13" fill="{t["bg"]}" stroke="{track}" stroke-width="2"/>')
            o.append(f'<g style="animation:stamp .5s {e_out} {tn:.2f}s both">'
                     f'<circle r="13" fill="{t["cobalt"]}"/>'
                     f'<path d="M-5.2,0.4 L-1.6,4 L5.4,-3.6" fill="none" stroke="{t["on_cobalt"]}" stroke-width="2.4" '
                     f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="16" '
                     f'style="animation:check .35s ease-out {tn + .18:.2f}s both"/></g>')
        elif i == 4:
            o.append(f'<circle r="16" fill="{t["bg"]}" stroke="{track}" stroke-width="2"/>')
            for k in range(2):
                o.append(f'<circle r="16" fill="none" stroke="{t["cobalt"]}" stroke-width="2" '
                         f'style="opacity:0;animation:ring 2.2s ease-out {tn + .4 + k * 1.1:.2f}s infinite"/>')
            o.append(f'<g style="animation:pop .55s {e_pop} {tn:.2f}s both">'
                     f'<circle r="16" fill="{t["cobalt"]}"/>'
                     f'<path d="M-3.6,-6 L6.4,0 L-3.6,6 Z" fill="{t["impact"]}" stroke="{t["impact"]}" stroke-width="1.6" '
                     f'stroke-linejoin="round" style="animation:tri 1.1s ease-in-out infinite"/></g>')
        else:
            o.append(f'<g style="animation:fade .6s ease {tn:.2f}s both">'
                     f'<circle r="13" fill="{t["bg"]}" stroke="{t["ink3"]}" stroke-width="1.6" stroke-dasharray="3 3.3"/>'
                     f'<g style="animation:spin 6s linear infinite"><circle r="6" fill="none" stroke="{t["cobalt"]}" '
                     f'stroke-width="2" stroke-linecap="round" stroke-dasharray="9.4 28.3"/></g></g>')
        o.append("</g>")

        # +EXP pop (completed chapters + the boss level reveal)
        if i < 5:
            ey = y + (44 if top else -26) + (2 if i == 4 else 0) * (1 if top else -1)
            o.append(f'<text x="{x}" y="{ey}" text-anchor="middle" class="jx" font-size="10" letter-spacing=".6" '
                     f'fill="{t["cobalt"]}" style="animation:exp 1s {e_out} {tn + .15:.2f}s both">{POP}</text>')

        # label block
        num = f"{i + 1:02d}"
        kw = mx.width(num, 9.5, 1.6) + 8 + mx.width(kick, 9.5, 1.6)
        badge = ""
        badge_w = 0
        if i < 4:
            badge, badge_w = CLEARED, mx.width(CLEARED, 8, 1.2) + 14
        elif i == 4:
            badge, badge_w = IN_PROGRESS, mx.width(IN_PROGRESS, 8, 1.2) + 26
        kline_w = kw + (8 + badge_w if badge else 0)
        lines_w = [kline_w, mx.width(title, 13.5, -.15), ms.width(sub, 11)] + [ms.width(e, 10) for e in extra]
        bw = max(lines_w)
        lx = min(max(x - bw / 2, PAD - 10), W - PAD + 10 - bw)
        if top:
            ky, tyy, sy = y - 61, y - 43, y - 27
        else:
            ky, tyy, sy = y + 36, y + 54, y + 70
        delay = tn + 0.12
        o.append(f'<g class="a" style="animation-delay:{delay:.2f}s">')
        o.append(f'<text x="{lx:.1f}" y="{ky}" class="jx k" fill="{t["cobalt"]}">{num}</text>')
        o.append(f'<text x="{lx + mx.width(num, 9.5, 1.6) + 8:.1f}" y="{ky}" class="jx k" fill="{t["ink3"]}">{esc(kick)}</text>')
        if badge:
            bx = lx + kw + 8
            if i < 4:
                o.append(f'<rect x="{bx:.1f}" y="{ky - 9.5}" width="{badge_w:.1f}" height="13" rx="6.5" fill="{t["cobalt_soft"]}"/>'
                         f'<text x="{bx + 7:.1f}" y="{ky - .2}" class="jx" font-size="8" letter-spacing="1.2" '
                         f'fill="{t["cobalt"] if theme == "light" else t["lilac"]}">{badge}</text>')
            else:
                o.append(f'<rect x="{bx:.1f}" y="{ky - 9.5}" width="{badge_w:.1f}" height="13" rx="6.5" fill="{t["impact"]}"/>'
                         f'<path d="M{bx + 8:.1f},{ky - 5.8} l5,3 l-5,3 z" fill="{ink_on_yellow}" style="animation:breathe 1.4s ease-in-out infinite"/>'
                         f'<text x="{bx + 18:.1f}" y="{ky - .2}" class="jx" font-size="8" letter-spacing="1.2" '
                         f'fill="{ink_on_yellow}">{badge}</text>')
        o.append(f'<text x="{lx:.1f}" y="{tyy}" class="jx ti" fill="{t["ink"]}">{esc(title)}</text>')
        if i == 5:
            # segmented loader + LOADING…
            for s in range(8):
                o.append(f'<rect x="{lx + s * 11:.1f}" y="{sy - 7}" width="8" height="6" rx="1.5" fill="{t["cobalt"]}" '
                         f'style="opacity:.18;animation:seg 1.6s ease-in-out {T_NEXT + .3 + s * .12:.2f}s infinite"/>')
            o.append(f'<text x="{lx + 8 * 11 + 6:.1f}" y="{sy}" class="jx" font-size="9.5" letter-spacing="1.6" '
                     f'fill="{t["ink3"]}">{esc(sub)}</text>')
        else:
            o.append(f'<text x="{lx:.1f}" y="{sy}" class="js su" fill="{t["ink2"]}">{esc(sub)}</text>')
        for j, e in enumerate(extra):
            ey2 = sy + 20 + j * 14
            if j == 0 and e.startswith("Party:"):
                o.append(f'<text x="{lx:.1f}" y="{ey2}" class="js pt" fill="{t["ink3"]}">'
                         f'<tspan class="jx" fill="{t["cobalt"]}">Party:</tspan>{esc(e[6:])}</text>')
            else:
                o.append(f'<text x="{lx:.1f}" y="{ey2}" class="js pt" fill="{t["ink3"]}">{esc(e)}</text>')
        o.append("</g>")

    # rider on the draw head
    o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.04;.94;1" '
             f'dur="{DRAW_DUR}s" begin="{DRAW_START}s" fill="freeze"/><g>'
             f'<animateMotion dur="{DRAW_DUR}s" begin="{DRAW_START}s" fill="freeze" calcMode="spline" keyPoints="0;1" '
             f'keyTimes="0;1" keySplines="{" ".join(str(v) for v in EASE)}" path="{path_d(0, 4)}"/>'
             f'<circle r="6.5" fill="{t["bg"]}" stroke="{t["cobalt"]}" stroke-width="3"/></g></g>')

    # ── EXP bar ──
    by = 352
    o.append(f'<text x="{PAD}" y="{by + 4}" class="jx" font-size="10.5" letter-spacing="1.6" fill="{t["ink"]}">{EXP_L}</text>')
    rw = mx.width(EXP_R, 10.5, 1.6)
    o.append(f'<text x="{W - PAD}" y="{by + 4}" text-anchor="end" class="jx" font-size="10.5" letter-spacing="1.6" '
             f'fill="{t["cobalt"]}">{EXP_R}</text>')
    b0 = PAD + mx.width(EXP_L, 10.5, 1.6) + 16
    b1 = W - PAD - rw - 16
    bw_total = b1 - b0
    o.append(f'<rect x="{b0:.1f}" y="{by - 4}" width="{bw_total:.1f}" height="8" rx="4" fill="{track}"/>')
    # fill: step to k/6 as chapter k clears; 5/6 at the boss level
    steps = []
    T_END = T_NODE[4] + 0.6
    for k in range(5):
        steps.append((T_NODE[k], k / 6, (k + 1) / 6))
    kf = ["0%{transform:scaleX(0)}"]
    for tk, f0, f1 in steps:
        p0 = tk / T_END * 100
        p1 = min((tk + .45) / T_END * 100, 100)
        kf.append(f"{p0:.1f}%{{transform:scaleX({f0:.4f})}}{p1:.1f}%{{transform:scaleX({f1:.4f})}}")
    kf.append("100%{transform:scaleX(.8333)}")
    o.append(f"<style>@keyframes xp{{{''.join(kf)}}}</style>")
    o.append(f'<clipPath id="barclip"><rect x="{b0:.1f}" y="{by - 4}" width="{bw_total:.1f}" height="8" rx="4"/></clipPath>')
    o.append(f'<g clip-path="url(#barclip)">')
    o.append(f'<g transform="translate({b0:.1f},0)"><rect x="0" y="{by - 4}" width="{bw_total:.1f}" height="8" fill="{t["cobalt"]}" '
             f'style="transform-origin:0 0;animation:xp {T_END:.2f}s linear both"/></g>')
    # in-progress sixth segment breathes
    o.append(f'<rect x="{b0 + bw_total * 5 / 6:.1f}" y="{by - 4}" width="{bw_total / 6:.1f}" height="8" fill="{t["cobalt"]}" '
             f'style="opacity:0;animation:breathe 2.2s ease-in-out {T_END:.2f}s infinite"/>')
    # segment gaps
    for k in range(1, 6):
        o.append(f'<rect x="{b0 + bw_total * k / 6 - 1.5:.1f}" y="{by - 5}" width="3" height="10" fill="{t["bg"]}"/>')
    o.append("</g>")
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    write("quests", {"light": build("light"), "dark": build("dark")})
    print("node times", [round(x, 2) for x in T_NODE], "next", round(T_NEXT, 2))
