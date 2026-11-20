"""
Scene "select": fighting-game character select / stat sheet.

    python assets/src/scene_select.py      # from the repo root -> assets/select-light.svg, assets/select-dark.svg
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import THEMES, W, Metrics, esc, font_css, photo_duotone, write  # noqa: E402

H = 400
MX = Metrics("JX")
MS = Metrics("JS")
EASE = "cubic-bezier(.2,.8,.2,1)"
POP = "cubic-bezier(.3,1.5,.5,1)"

# ───────────────────────── content (facts only) ─────────────────────────
KANA = "ユネス"
HANDLE = "@UNES97"
NAME = "YOUNES NOUFAIR"
INFO = [("CLASS", "LEAD ENGINEER"), ("ORIGIN", "CASABLANCA"), ("LV.", "6+")]
STATS = [("PHP", 80), ("JAVASCRIPT", 80), ("REST APIS", 80), ("SQL", 80), ("PYTHON", 70)]
LIKES = ("LIKES", "Basketball · Video games")
MOVES = [  # inputs (d=down, dr=down-right, r=right, l=left), button, name, detail
    (["d", "dr", "r"], "P", "Ideas → Reality", "Full-stack · web apps & APIs"),
    (["r", "r"], "K", "Schema Slash", "MySQL · PostgreSQL · MongoDB"),
    (["d", "d"], "P", "Deploy Dash", "Docker · Linux · Apache"),
    (["l", "r"], "S", "Prompt Combo", "LangChain · LLMs · RAG"),
]
HDR_P1, HDR_NAME, HDR_MID, HDR_START = "PLAYER 1", "YOUNES", "SELECT YOUR FIGHTER", "PRESS START"
STAMP = "SELECTED"
STATS_T, STATS_R, MOVES_T = "STATS", "RATING / 100", "SPECIAL MOVES"
P1_TAG = "P1"

ALL_TEXT = "".join([KANA, HANDLE, NAME, HDR_P1, HDR_NAME, HDR_MID, HDR_START, STAMP, STATS_T, STATS_R, MOVES_T, P1_TAG,
                    *[a + b for a, b in INFO], *[s for s, _ in STATS], *LIKES, "+%",
                    *[b + n + d for _, b, n, d in MOVES]])

ANGLE = {"r": 0, "dr": 45, "d": 90, "l": 180}


def track_w(m: Metrics, text: str, size: float, tr: float) -> float:
    return m.width(text, size, tr)


def para(x0, y0, x1, y1, sk):
    """Parallelogram leaning right (top edge shifted right by sk)."""
    return f"{x0 + sk},{y0} {x1},{y0} {x1 - sk},{y1} {x0},{y1}"


def build(theme: str) -> str:
    t = THEMES[theme]
    dark_txt = "#0f1013"
    css = [font_css(ALL_TEXT, keys=("JX", "JS", "JP"))]
    css.append(f"""
.a{{animation-fill-mode:both;animation-iteration-count:1}}
.fb{{transform-box:fill-box;transform-origin:50% 50%}}
@keyframes down{{from{{opacity:0;transform:translateY(-10px)}}to{{opacity:1;transform:none}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes inL{{from{{opacity:0;transform:translateX(-28px)}}to{{opacity:1;transform:none}}}}
@keyframes inR{{from{{opacity:0;transform:translateX(18px)}}to{{opacity:1;transform:none}}}}
@keyframes settle{{from{{transform:scale(1.14)}}to{{transform:none}}}}
@keyframes wipe{{from{{transform:translateX(0)}}to{{transform:translateX(250px)}}}}
@keyframes sweep{{0%{{opacity:1;transform:translateX(-60px)}}100%{{opacity:1;transform:translateX(280px)}}}}
@keyframes snap{{from{{opacity:0;transform:scale(1.16)}}to{{opacity:1;transform:none}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
@keyframes stamp{{0%{{opacity:0;transform:scale(1.7)}}60%{{opacity:1}}100%{{opacity:1;transform:none}}}}
@keyframes seg{{from{{opacity:0;transform:scaleX(.2)}}to{{opacity:1;transform:none}}}}
@keyframes on{{from,to{{opacity:1}}}}
@keyframes pop{{from{{opacity:0;transform:scale(.4)}}to{{opacity:1;transform:none}}}}
@keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:.25}}}}
@keyframes flash{{0%{{opacity:0}}20%{{opacity:.9}}100%{{opacity:0}}}}
.num{{opacity:0}}
""")

    def anim(name, dur, delay, ease=EASE, extra=""):
        return f'style="animation:{name} {dur}ms {ease} {delay}ms both{extra}"'

    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'role="img" aria-label="Player 1 select screen: Younes Noufair, Lead Software Engineer">')
    o.append("<style>" + "".join(css) + "</style>")

    # frame geometry
    fx0, fy0, fx1, fy1, sk = 28, 76, 236, 372, 22
    o.append(f'<defs><clipPath id="pf"><polygon points="{para(fx0, fy0, fx1, fy1, sk)}"/></clipPath>'
             f'<clipPath id="card"><rect x="0" y="0" width="{W}" height="{H}" rx="24"/></clipPath></defs>')
    o.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="24" fill="{t["bg"]}" stroke="{t["line"]}"/>')

    # ── header ──
    hy = 38
    pill_w = track_w(MX, HDR_P1, 10.5, 1.6) + 24
    o.append(f'<g {anim("down", 500, 0)}>')
    o.append(f'<rect x="24" y="22" width="{pill_w:.1f}" height="23" rx="11.5" fill="{t["cobalt"]}"/>')
    o.append(f'<text x="{24 + pill_w / 2:.1f}" y="{hy - 0.5}" class="jx" font-size="10.5" letter-spacing="1.6" '
             f'text-anchor="middle" fill="{t["on_cobalt"]}">{HDR_P1}</text>')
    tx = 24 + pill_w + 12
    o.append(f'<path d="M{tx} {hy - 8.5}l7 4.5l-7 4.5z" fill="{t["ink"]}"/>')
    o.append(f'<text x="{tx + 15}" y="{hy}" class="jx" font-size="13" letter-spacing="2.2" fill="{t["ink"]}">{HDR_NAME}</text>')
    o.append(f'<text x="{W / 2}" y="{hy - 0.5}" class="jx" font-size="10.5" letter-spacing="3.4" text-anchor="middle" '
             f'fill="{t["ink3"]}">{HDR_MID}</text>')
    # little divider ticks around the center title
    mw = track_w(MX, HDR_MID, 10.5, 3.4)
    for s in (-1, 1):
        x = W / 2 + s * (mw / 2 + 16)
        o.append(f'<path d="M{x - 6 * (s > 0) - 0 * s} {hy - 4}h6" stroke="{t["line"]}" stroke-width="2" stroke-linecap="round"/>')
    o.append("</g>")
    sw = track_w(MX, HDR_START, 10.5, 2.4)
    sx = W - 26 - sw
    o.append(f'<g {anim("down", 500, 80)}><g style="animation:blink 1.1s steps(1) 600ms infinite">'
             f'<path d="M{sx - 16} {hy - 8}l8.5 4.5l-8.5 4.5z" fill="{t["cobalt"]}"/>'
             f'<text x="{W - 26}" y="{hy - 0.5}" class="jx" font-size="10.5" letter-spacing="2.4" text-anchor="end" '
             f'fill="{t["ink"]}">{HDR_START}</text></g></g>')
    o.append(f'<path d="M24 60.5H{W - 24}" stroke="{t["line"]}"/>')

    # ── portrait ──
    photo = photo_duotone(theme, 440)
    ph = fy1 - fy0
    o.append(f'<g {anim("inL", 650, 120)}>')
    o.append(f'<g clip-path="url(#pf)">')
    o.append(f'<rect x="{fx0}" y="{fy0}" width="{fx1 - fx0}" height="{ph}" fill="{t["cobalt"]}"/>')
    o.append(f'<g class="fb" {anim("settle", 1300, 120)}><image href="{photo}" x="{(fx0 + fx1 - ph) / 2:.1f}" y="{fy0}" '
             f'width="{ph}" height="{ph}" preserveAspectRatio="xMidYMid slice"/></g>')
    # wipe panel (reveals the photo) + impact sweep bar
    o.append(f'<g {anim("wipe", 560, 260, "cubic-bezier(.7,0,.2,1)")}><polygon points="{para(fx0 - 30, fy0, fx1 + 30, fy1, sk)}" '
             f'fill="{t["cobalt"]}"/></g>')
    o.append(f'<g style="opacity:0;animation:sweep 520ms cubic-bezier(.6,0,.3,1) 420ms both">'
             f'<polygon points="{para(fx0 - 20, fy0, fx0 + 6, fy1, sk * 2.2)}" fill="{t["impact"]}"/></g>')
    o.append("</g>")
    o.append(f'<polygon points="{para(fx0, fy0, fx1, fy1, sk)}" fill="none" stroke="{t["ink"]}" stroke-opacity=".12"/>')
    # P1 tag + katakana tag
    o.append(f'<polygon points="{para(fx0 + 20, fy0 + 12, fx0 + 58, fy0 + 32, 4)}" fill="{t["bg"]}"/>')
    o.append(f'<text x="{fx0 + 39}" y="{fy0 + 26.5}" class="jx" font-size="11" letter-spacing="1" text-anchor="middle" '
             f'fill="{t["cobalt"]}">{P1_TAG}</text>')
    o.append("</g>")

    # selection brackets (snap in, then pulse)
    bx0, by0, bx1, by1, L = fx0 - 8, fy0 - 8, fx1 + 8, fy1 + 8, 20
    brk = (f"M{bx0 + sk + 8} {by0 + L}v-{L}h{L} M{bx1 - L} {by0}h{L}v{L} "
           f"M{bx1 - sk - 8} {by1 - L}v{L}h-{L} M{bx0 + L} {by1}h-{L}v-{L}")
    o.append(f'<g class="fb" {anim("snap", 380, 760, POP)}><g style="animation:pulse 2.2s ease-in-out 1.4s infinite">'
             f'<path d="{brk}" fill="none" stroke="{t["cobalt"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
             f"</g></g>")

    # SELECTED stamp
    stw = track_w(MX, STAMP, 14, 3.2) + 30
    scx, scy = (fx0 + fx1) / 2 + 6, fy1 - 30
    o.append(f'<g transform="translate({scx} {scy}) rotate(-6)"><g class="fb" {anim("stamp", 420, 1050, POP)}>'
             f'<rect x="{-stw / 2:.1f}" y="-16" width="{stw:.1f}" height="32" rx="5" fill="{t["impact"]}" '
             f'stroke="{dark_txt}" stroke-width="2"/>'
             f'<text x="0" y="5.3" class="jx" font-size="14" letter-spacing="3.2" text-anchor="middle" fill="{dark_txt}">{STAMP}</text>'
             f"</g></g>")
    # stamp flash ring (one-off)
    o.append(f'<g transform="translate({scx} {scy}) rotate(-6)"><rect x="{-stw / 2 - 8:.1f}" y="-24" width="{stw + 16:.1f}" '
             f'height="48" rx="9" fill="none" stroke="{t["impact"]}" stroke-width="2" '
             f'style="opacity:0;animation:flash 600ms ease-out 1250ms both"/></g>')

    # ── middle column: identity ──
    cx = 266
    o.append(f'<g {anim("rise", 500, 380)}><text x="{cx}" y="92" class="jp" font-size="13" fill="{t["cobalt"]}">{KANA}</text>'
             f'<text x="{cx + 39}" y="92" class="js" font-size="11.5" fill="{t["ink3"]}">'
             f'<tspan dx="10">/</tspan><tspan dx="8">{HANDLE}</tspan></text></g>')
    o.append(f'<g {anim("rise", 520, 460)}><text x="{cx - 1.5}" y="124" class="jx" font-size="28" letter-spacing="-.4" '
             f'fill="{t["ink"]}">{NAME}</text></g>')
    ix = [cx, cx + 128, cx + 240]
    for i, (lab, val) in enumerate(INFO):
        x = ix[i]
        g = [f'<text x="{x}" y="150" class="jx" font-size="9" letter-spacing="1.8" fill="{t["ink3"]}">{lab}</text>',
             f'<text x="{x}" y="168" class="jx" font-size="13" letter-spacing=".4" '
             f'fill="{t["cobalt"] if lab == "LV." else t["ink"]}">{esc(val)}</text>']
        if i:
            g.insert(0, f'<path d="M{x - 13}.5 141v30" stroke="{t["line"]}"/>')
        o.append(f'<g {anim("rise", 500, 560 + i * 70)}>' + "".join(g) + "</g>")

    # stats
    o.append(f'<g {anim("rise", 500, 760)}><path d="M{cx} 188.5H540" stroke="{t["line"]}"/>'
             f'<text x="{cx}" y="210" class="jx" font-size="10" letter-spacing="2.6" fill="{t["ink3"]}">{STATS_T}</text>'
             f'<text x="540" y="210" class="js" font-size="10" letter-spacing="1.2" text-anchor="end" fill="{t["ink3"]}">{STATS_R}</text></g>')
    seg_x0, seg_w, seg_gap, seg_h, seg_sk, nseg = 352, 12, 4, 14, 4, 10
    step = 48
    for r, (lab, val) in enumerate(STATS):
        cy = 232 + r * 28
        t0 = 950 + r * 300
        filled = val // 10
        row = [f'<g {anim("inR", 380, t0 - 200)}><text x="{cx}" y="{cy + 4}" class="jx" font-size="11.5" letter-spacing="1" '
               f'fill="{t["ink2"]}">{lab}</text></g>']
        for k in range(nseg):
            x = seg_x0 + k * (seg_w + seg_gap)
            pts = para(x, cy - seg_h / 2, x + seg_w + seg_sk, cy + seg_h / 2, seg_sk)
            row.append(f'<polygon points="{pts}" fill="{t["line"]}"/>')
            if k < filled:
                fill = t["cobalt"] if k < filled - 1 else t["impact"]
                row.append(f'<polygon class="fb" points="{pts}" fill="{fill}" {anim("seg", 200, t0 + k * step, POP)}/>')
        # counting number: one frame per filled segment
        for k in range(filled + 1):
            v = k * 10
            start = t0 + (k - 1) * step + 60 if k else t0 - 200
            if k < filled:
                end = t0 + k * step + 60
                st = f'style="animation:on {end - start}ms linear {start}ms"'
            else:
                st = f'style="animation:on 10ms linear {start}ms forwards"'
            row.append(f'<text class="num jx" x="540" y="{cy + 4.5}" font-size="13" text-anchor="end" '
                       f'fill="{t["ink"] if k == filled else t["ink3"]}" {st}>{v}</text>')
        o.append("".join(row))
    o.append(f'<g {anim("rise", 500, 2500)}><text x="{cx}" y="{232 + 5 * 28 + 6}" class="jx" font-size="9" letter-spacing="1.8" '
             f'fill="{t["ink3"]}">{LIKES[0]}</text><text x="{cx + 52}" y="{232 + 5 * 28 + 6}" class="js" font-size="11.5" '
             f'fill="{t["ink2"]}">{esc(LIKES[1])}</text></g>')

    # ── right column: special moves ──
    px0, py0, px1, py1 = 562, 76, 816, 372
    o.append(f'<g {anim("inR", 600, 700)}><rect x="{px0 + .5}" y="{py0 + .5}" width="{px1 - px0 - 1}" height="{py1 - py0 - 1}" '
             f'rx="16" fill="{t["panel"]}" stroke="{t["line"]}"/>'
             f'<text x="{px0 + 18}" y="{py0 + 26}" class="jx" font-size="10" letter-spacing="2.6" fill="{t["ink3"]}">{MOVES_T}</text>'
             f'<g style="animation:pulse 2.2s ease-in-out 1.4s infinite"><circle cx="{px1 - 22}" cy="{py0 + 22.5}" r="3.5" fill="{t["cobalt"]}"/></g></g>')
    btn_col = {"P": (t["cobalt"], t["on_cobalt"]), "K": (t["peach"], dark_txt), "S": (t["mint"], dark_txt)}
    for i, (inputs, btn, name, detail) in enumerate(MOVES):
        y = py0 + 32 + i * 66
        t0 = 1500 + i * 260
        row = []
        if i:
            row.append(f'<path d="M{px0 + 18} {y - 8.5}H{px1 - 18}" stroke="{t["line"]}" stroke-dasharray="2 4"/>')
        cyi = y + 22
        # inputs right-aligned: arrows (r=9.5, pitch 22) + "+" + button (20)
        n = len(inputs)
        total = n * 22 - 3 + 15 + 20
        x = px1 - 18 - total + 9.5
        parts = []
        for j, d in enumerate(inputs):
            parts.append(f'<g transform="translate({x} {cyi})"><g class="fb" {anim("pop", 300, t0 + 120 + j * 70, POP)}>'
                         f'<circle r="9.5" fill="{t["bg"]}" stroke="{t["line"]}"/>'
                         f'<path transform="rotate({ANGLE[d]})" d="M-4 0H4M.6 -3.4L4 0L.6 3.4" fill="none" stroke="{t["ink"]}" '
                         f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></g></g>')
            x += 22
        x += -9.5 - 3 + 7.5
        parts.append(f'<g {anim("pop", 300, t0 + 120 + n * 70, POP)} class="fb"><text x="{x}" y="{cyi + 4.3}" class="jx" '
                     f'font-size="12" text-anchor="middle" fill="{t["ink3"]}">+</text></g>')
        x += 7.5 + 10
        bg, fg = btn_col[btn]
        parts.append(f'<g transform="translate({x} {cyi})"><g class="fb" {anim("pop", 320, t0 + 120 + (n + 1) * 70, POP)}>'
                     f'<rect x="-10" y="-10" width="20" height="20" rx="6" fill="{bg}"/>'
                     f'<text y="4" class="jx" font-size="11" text-anchor="middle" fill="{fg}">{btn}</text></g></g>')
        row.append("".join(parts))
        row.append(f'<g {anim("inR", 420, t0 + 120)}><text x="{px0 + 18}" y="{y + 27}" class="jx" font-size="14.5" '
                   f'letter-spacing="-.1" fill="{t["ink"]}">{esc(name)}</text>'
                   f'<text x="{px0 + 18}" y="{y + 45}" class="js" font-size="11" fill="{t["ink3"]}">{esc(detail)}</text></g>')
        o.append(f'<g {anim("rise", 380, t0)}>' + "".join(row) + "</g>")

    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    write("select", {"light": build("light"), "dark": build("dark")})
