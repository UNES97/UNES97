"""
Scene "card": the whole profile in one calm, animated card (title + stats + call to action).

    python assets/src/scene_card.py      # -> assets/card-light.svg, assets/card-dark.svg

Motion is soft on purpose: masked rises, gentle fades and slow fills (ease-out), then only quiet loops
(a slowly marching frame around the portrait, a nudging arrow, a blinking caret).
Every element's resting state is its final state, so with animations off (or reduced motion) the card is complete.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import THEMES, W, Metrics, esc, font_css, photo_duotone, write  # noqa: E402

H = 600
PAD = 40
EASE = "cubic-bezier(.22,1,.36,1)"

# ───────────────────────── content (facts only) ─────────────────────────
HANDLE = "UNES97"
EP = "EP. 06+  ·  THE LEAD ENGINEER ARC"
NAME1, NAME2 = "YOUNES", "NOUFAIR"
KANA = "ユネス"
ROLE_A, ROLE_B, ROLE_C = "Lead Software Engineer @ ", "Maxmind.ma", "  ·  Casablanca"
TAG = [("I", "ink"), ("build", "ink"), ("software", "ink"), ("that", "ink"), ("connects", "ink"),
       ("ideas", "cobalt"), ("to", "ink"), ("reality.", "cobalt")]
STATS_T, MOVES_T = "STATS", "SPECIAL MOVES"
STATS = [("PHP", 80), ("JAVASCRIPT", 80), ("REST APIS", 80), ("SQL", 80), ("PYTHON", 70)]
MOVES = [
    ("Ideas → Reality", "Full-stack · web apps & APIs"),
    ("Schema Slash", "MySQL · PostgreSQL · MongoDB"),
    ("Deploy Dash", "Docker · Linux · Apache"),
    ("Prompt Combo", "LangChain · LLMs · RAG"),
]
TBC, TBC_JP = "TO BE CONTINUED", "つづく"
CTA = "PRESS START TO COLLABORATE"

ALL_TEXT = "".join([HANDLE, EP, NAME1, NAME2, KANA, ROLE_A, ROLE_B, ROLE_C, *[w for w, _ in TAG],
                    STATS_T, MOVES_T, *[s for s, _ in STATS], *[a + b for a, b in MOVES], TBC, TBC_JP, CTA, "0123456789"])

MX, MS = Metrics("JX"), Metrics("JS")

# ───────────────────────── layout ─────────────────────────
NAME_SIZE, NAME_TRACK = 84, -2.0
Y_NAME1, Y_NAME2 = 168, 248
Y_ROLE, Y_TAG = 290, 326
TAG_SIZE = 20
PH_X, PH_Y, PH_S = 586, 92, 204       # portrait square
DIV1, DIV2 = 362, 526
SEC_Y = 396                            # section labels
ROW0, STAT_STEP, MOVE_STEP = 426, 21, 24
BAR_X0, BAR_X1 = 150, 352
COL2 = 440


def anim(name: str, dur: float, delay: float, extra: str = "") -> str:
    return f'style="animation:{name} {dur}s {EASE} {delay:.2f}s both{extra}"'


def build(theme: str) -> str:
    t = THEMES[theme]
    photo = photo_duotone(theme, PH_S * 2)
    css = font_css(ALL_TEXT, ("JX", "JS", "JP")) + f"""
@keyframes fade{{from{{opacity:0}}}}
@keyframes up{{from{{opacity:0;transform:translateY(10px)}}}}
@keyframes rise{{from{{transform:translateY(96px)}}}}
@keyframes photo{{from{{opacity:0;transform:scale(1.08)}}}}
@keyframes fill{{from{{transform:scaleX(0)}}}}
@keyframes draw{{from{{stroke-dashoffset:var(--len)}}}}
@keyframes march{{to{{stroke-dashoffset:-200}}}}
@keyframes nudge{{0%,60%,100%{{transform:translateX(0)}}30%{{transform:translateX(6px)}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.ph{{transform-origin:{PH_X + PH_S / 2}px {PH_Y + PH_S / 2}px}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">',
         f'<title>Younes Noufair · Lead Software Engineer @ Maxmind.ma</title><style>{css}</style>',
         "<defs>",
         f'<clipPath id="n1"><rect x="0" y="{Y_NAME1 - 76}" width="580" height="96"/></clipPath>',
         f'<clipPath id="n2"><rect x="0" y="{Y_NAME2 - 76}" width="580" height="96"/></clipPath>',
         f'<clipPath id="ph"><rect x="{PH_X}" y="{PH_Y}" width="{PH_S}" height="{PH_S}" rx="18"/></clipPath>',
         f'<pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{t["grid"]}"/></pattern>',
         "</defs>"]

    # card
    o.append(f'<g {anim("fade", .7, 0)}>'
             f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="22" fill="{t["bg"]}" stroke="{t["line"]}"/>'
             f'<rect x="0.5" y="0.5" width="{W - 1}" height="{DIV1}" rx="22" fill="url(#dots)"/></g>')

    # top bar
    hw = MX.width(HANDLE, 11, 2.2) + 34
    o.append(f'<g {anim("up", .8, .15)}>'
             f'<rect x="{PAD}" y="38" width="{hw:.1f}" height="26" rx="13" fill="{t["ink"]}"/>'
             f'<circle cx="{PAD + 14}" cy="51" r="3.5" fill="{t["green"]}"/>'
             f'<text x="{PAD + 24}" y="55" class="jx" font-size="11" letter-spacing="2.2" fill="{t["bg"]}">{HANDLE}</text>'
             f'<text x="{W - PAD}" y="55" class="jx" font-size="11" letter-spacing="2.2" text-anchor="end" fill="{t["ink3"]}">{esc(EP)}</text></g>')

    # name: rises out of a mask
    o.append(f'<g clip-path="url(#n1)"><text x="{PAD - 3}" y="{Y_NAME1}" class="jx" font-size="{NAME_SIZE}" '
             f'letter-spacing="{NAME_TRACK}" fill="{t["ink"]}" {anim("rise", 1.1, .3)}>{NAME1}</text></g>')
    o.append(f'<g clip-path="url(#n2)"><text x="{PAD - 3}" y="{Y_NAME2}" class="jx" font-size="{NAME_SIZE}" '
             f'letter-spacing="{NAME_TRACK}" fill="none" stroke="{t["cobalt"]}" stroke-width="1.6" '
             f'{anim("rise", 1.1, .45)}>{NAME2}</text></g>')

    # role
    xa = PAD + MS.width(ROLE_A, 16)
    xb = xa + MX.width(ROLE_B, 16)
    o.append(f'<g {anim("up", .9, .85)}>'
             f'<text x="{PAD}" y="{Y_ROLE}" class="js" font-size="16" fill="{t["ink2"]}">{esc(ROLE_A)}</text>'
             f'<text x="{xa:.1f}" y="{Y_ROLE}" class="jx" font-size="16" fill="{t["ink"]}">{ROLE_B}</text>'
             f'<text x="{xb:.1f}" y="{Y_ROLE}" class="js" font-size="16" fill="{t["ink2"]}" xml:space="preserve">{esc(ROLE_C)}</text></g>')

    # tagline: word by word
    x, space = PAD, MX.width(" ", TAG_SIZE)
    for i, (word, col) in enumerate(TAG):
        o.append(f'<text x="{x:.1f}" y="{Y_TAG}" class="jx" font-size="{TAG_SIZE}" fill="{t[col]}" '
                 f'{anim("up", .7, 1.05 + i * .07)}>{esc(word)}</text>')
        x += MX.width(word, TAG_SIZE) + space

    # portrait + slowly marching frame + kana chip
    g = 10
    per = 2 * (PH_S + 2 * g) * 2
    o.append(f'<rect x="{PH_X - g}" y="{PH_Y - g}" width="{PH_S + 2 * g}" height="{PH_S + 2 * g}" rx="26" fill="none" '
             f'stroke="{t["ink3"]}" stroke-opacity=".55" stroke-width="1" stroke-dasharray="3 7" '
             f'style="animation:fade 1s ease .6s both,march 24s linear 1.6s infinite"/>')
    o.append(f'<g clip-path="url(#ph)"><image class="ph" href="{photo}" x="{PH_X}" y="{PH_Y}" width="{PH_S}" height="{PH_S}" '
             f'{anim("photo", 1.4, .25)}/></g>')
    kw = 74
    o.append(f'<g {anim("up", .8, 1.0)}>'
             f'<rect x="{PH_X + 14}" y="{PH_Y + PH_S - 20}" width="{kw}" height="34" rx="17" fill="{t["cobalt"]}"/>'
             f'<text x="{PH_X + 14 + kw / 2}" y="{PH_Y + PH_S + 3}" class="jp" font-size="17" text-anchor="middle" '
             f'fill="{t["on_cobalt"]}" letter-spacing="1">{KANA}</text></g>')

    # dividers (draw in)
    for y, d in ((DIV1, 1.2), (DIV2, 2.0)):
        ln = W - 2 * PAD
        o.append(f'<line x1="{PAD}" y1="{y}" x2="{W - PAD}" y2="{y}" stroke="{t["line"]}" stroke-dasharray="{ln}" '
                 f'style="--len:{ln};animation:draw 1.2s {EASE} {d}s both"/>')

    # section labels
    o.append(f'<g {anim("fade", .8, 1.35)}>'
             f'<text x="{PAD}" y="{SEC_Y}" class="jx" font-size="10" letter-spacing="2.6" fill="{t["ink3"]}">{STATS_T}</text>'
             f'<text x="{COL2}" y="{SEC_Y}" class="jx" font-size="10" letter-spacing="2.6" fill="{t["ink3"]}">{MOVES_T}</text></g>')

    # stats: slow fills
    for i, (lab, val) in enumerate(STATS):
        y = ROW0 + i * STAT_STEP
        d = 1.5 + i * .12
        bw = (BAR_X1 - BAR_X0) * val / 100
        o.append(f'<g {anim("fade", .6, d)}>'
                 f'<text x="{PAD}" y="{y}" class="jx" font-size="11" letter-spacing="1.2" fill="{t["ink2"]}">{lab}</text>'
                 f'<rect x="{BAR_X0}" y="{y - 7}" width="{BAR_X1 - BAR_X0}" height="6" rx="3" fill="{t["line"]}"/>'
                 f'<text x="{BAR_X1 + 46}" y="{y}" class="jx" font-size="11" text-anchor="end" fill="{t["ink"]}">{val}</text></g>')
        o.append(f'<rect x="{BAR_X0}" y="{y - 7}" width="{bw:.1f}" height="6" rx="3" fill="{t["cobalt"]}" '
                 f'style="transform-origin:{BAR_X0}px {y}px;animation:fill 1.4s {EASE} {d + .1:.2f}s both"/>')

    # special moves
    for i, (name, detail) in enumerate(MOVES):
        y = ROW0 + i * MOVE_STEP
        o.append(f'<g {anim("up", .8, 1.6 + i * .1)}>'
                 f'<text x="{COL2}" y="{y}" class="jx" font-size="11" fill="{t["cobalt"]}">0{i + 1}</text>'
                 f'<text x="{COL2 + 26}" y="{y}" class="jx" font-size="14" fill="{t["ink"]}">{esc(name)}</text>'
                 f'<text x="{W - PAD}" y="{y}" class="js" font-size="12" text-anchor="end" fill="{t["ink3"]}">{esc(detail)}</text></g>')

    # footer: to be continued → / press start
    fy = 570
    tw = MX.width(TBC, 13, 2.6)
    ax = PAD + tw + 16
    chev = "".join(f'<path d="M{ax + k * 9:.1f} {fy - 10} l5 5 l-5 5" fill="none" stroke="{t["cobalt"]}" stroke-width="2" '
                   f'stroke-linecap="round" stroke-linejoin="round" opacity="{1 - k * .3:.1f}"/>' for k in range(3))
    o.append(f'<g {anim("up", .9, 2.3)}>'
             f'<text x="{PAD}" y="{fy}" class="jx" font-size="13" letter-spacing="2.6" fill="{t["ink"]}">{TBC}</text>'
             f'<g style="animation:nudge 2.4s ease-in-out 3.2s infinite">{chev}</g>'
             f'<text x="{ax + 40:.1f}" y="{fy + 1}" class="jp" font-size="14" fill="{t["ink3"]}">{TBC_JP}</text></g>')
    cw = MX.width(CTA, 12, 2.2)
    cx = W - PAD - 12
    o.append(f'<g {anim("up", .9, 2.45)}>'
             f'<text x="{cx - 4}" y="{fy}" class="jx" font-size="12" letter-spacing="2.2" text-anchor="end" fill="{t["cobalt"]}">{CTA}</text>'
             f'<rect x="{cx + 2}" y="{fy - 12}" width="8" height="14" rx="1.5" fill="{t["cobalt"]}" '
             f'style="animation:blink 1.1s steps(1) 3s infinite"/></g>')
    assert PAD + MX.width(NAME2, NAME_SIZE, NAME_TRACK) < PH_X - 20, "name runs into the portrait"
    assert ax + 40 + 60 < cx - 4 - cw, "footer overlaps"

    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    write("card", {th: build(th) for th in THEMES})
