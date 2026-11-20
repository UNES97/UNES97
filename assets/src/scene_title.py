"""
Scene "title": the first frame of an anime opening — focus lines burst, the portrait wipes in,
the name slams onto the card, the katakana rises, and the tagline types itself out.

    python assets/src/scene_title.py      # from the repo root -> assets/title-light.svg, assets/title-dark.svg
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import THEMES, W, Metrics, esc, font_css, photo_duotone, write  # noqa: E402

H = 380
NAME1, NAME2 = "YOUNES", "NOUFAIR"
KANA = "ユネス"
EP, ARC = "EP. 06+", "THE LEAD ENGINEER ARC"
SUB_A, SUB_B, SUB_C = "Lead Software Engineer @ ", "Maxmind.ma", "  ·  Casablanca"
TAG = [("I build software that connects ", "ink"), ("ideas", "cobalt"), (" to ", "ink"), ("reality.", "cobalt")]
TAG_TEXT = "".join(s for s, _ in TAG)
STICKER = "P1 · UNES97"
ALL_TEXT = NAME1 + NAME2 + KANA + EP + ARC + SUB_A + SUB_B + SUB_C + TAG_TEXT + STICKER

MX, MS = Metrics("JX"), Metrics("JS")

# layout
X0 = 40
NAME_SIZE, NAME_TRACK = 96, -2.5
Y_NAME1, Y_NAME2 = 162, 252
Y_SUB, Y_TAG = 292, 338
TAG_SIZE = 20
# portrait parallelogram (slanted like a manga panel)
SKEW = 38
PX_L, PX_R, PY_T, PY_B = 560, 812, 28, 352
POLY = [(PX_L + SKEW, PY_T), (PX_R, PY_T), (PX_R - SKEW, PY_B), (PX_L, PY_B)]
FOCUS = (690, 176)


def pts(p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def rays(seed: int, n: int) -> str:
    """Anime focus lines: thin wedges pointing at FOCUS, starting at a random inner radius."""
    rnd = random.Random(seed)
    cx, cy = FOCUS
    out = []
    for i in range(n):
        a = (i + rnd.uniform(-0.35, 0.35)) / n * 2 * math.pi
        r_in = rnd.uniform(170, 300)
        r_out = 980
        half = math.radians(rnd.uniform(0.18, 0.75))
        tip = (cx + r_in * math.cos(a), cy + r_in * math.sin(a))
        b1 = (cx + r_out * math.cos(a - half), cy + r_out * math.sin(a - half))
        b2 = (cx + r_out * math.cos(a + half), cy + r_out * math.sin(a + half))
        out.append(f"M{tip[0]:.0f} {tip[1]:.0f}L{b1[0]:.0f} {b1[1]:.0f}L{b2[0]:.0f} {b2[1]:.0f}Z")
    return "".join(out)


def burst(cx, cy, r1, r2, n=14) -> str:
    """Comic impact star."""
    p = []
    for i in range(2 * n):
        a = i / (2 * n) * 2 * math.pi - math.pi / 2
        r = r2 if i % 2 == 0 else r1
        r *= 1 + 0.10 * math.sin(i * 2.3)
        p.append((cx + r * math.cos(a) * 1.35, cy + r * math.sin(a)))
    return pts(p)


def type_keyframes() -> tuple[str, float]:
    """Step keyframes revealing TAG_TEXT one character at a time (positions from real font metrics).
    The clip rect rests over the text, so browsers that skip the animation still show the tagline."""
    n = len(TAG_TEXT)
    total = MX.width(TAG_TEXT, TAG_SIZE)
    frames = []
    for i in range(n + 1):
        w = MX.width(TAG_TEXT[:i], TAG_SIZE)
        frames.append(f"{i / n * 100:.2f}%{{transform:translateX({w - total:.1f}px);animation-timing-function:steps(1,end)}}")
    return "".join(frames), total


def scene(theme: str) -> str:
    t = THEMES[theme]
    dark = theme == "dark"
    photo = photo_duotone(theme, size=420)
    kf_type, tag_w = type_keyframes()
    n1_w = MX.width(NAME1, NAME_SIZE, NAME_TRACK)
    n2_w = MX.width(NAME2, NAME_SIZE, NAME_TRACK)
    ray_col = t["ink"]
    ray_op = ".11" if not dark else ".10"
    dot_col = t["cobalt"]
    ep_w = MX.width(EP, 12, 1) + 22
    sticker_w = MX.width(STICKER, 13, 1) + 24

    # katakana column between name and portrait
    k_x = 516
    k_size = 46
    kana = "".join(
        f'<text class="jp kana k{i}" x="{k_x}" y="{108 + i * 56}" font-size="{k_size}" text-anchor="middle" fill="{t["cobalt"]}">{c}</text>'
        for i, c in enumerate(KANA)
    )

    tag_spans = "".join(f'<tspan fill="{t[c]}">{esc(s)}</tspan>' for s, c in TAG)
    css = f"""
{font_css(ALL_TEXT, keys=("JX", "JS", "JP"))}
.a{{animation-fill-mode:both;animation-iteration-count:1}}
@keyframes raysIn{{0%{{opacity:0;transform:scale(1.9)}}35%{{opacity:1}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes raysFade{{0%{{opacity:1}}100%{{opacity:.7}}}}
@keyframes drift{{0%{{transform:rotate(0deg)}}50%{{transform:rotate(2.2deg)}}100%{{transform:rotate(0deg)}}}}
.rays{{transform-origin:{FOCUS[0]}px {FOCUS[1]}px;animation:raysIn .9s cubic-bezier(.16,1,.3,1) both}}
.raysfade{{animation:raysFade 1.4s ease 1s both}}
.raysdrift{{transform-origin:{FOCUS[0]}px {FOCUS[1]}px;animation:drift 14s ease-in-out 2.4s infinite}}
@keyframes slideIn{{0%{{transform:translateX(330px)}}100%{{transform:translateX(0)}}}}
@keyframes slabWipe{{0%{{transform:translateX(330px)}}60%{{transform:translateX(0)}}100%{{transform:translateX(-24px);opacity:0}}}}
.slab{{animation:slabWipe .75s cubic-bezier(.7,0,.2,1) .05s both}}
.photo{{animation:slideIn .8s cubic-bezier(.16,1,.3,1) .22s both}}
@keyframes slam{{0%{{opacity:0;transform:scale(1.45)}}45%{{opacity:1;transform:scale(.97)}}70%{{transform:scale(1.012)}}100%{{opacity:1;transform:scale(1)}}}}
.n1{{transform-origin:{X0 + n1_w / 2:.0f}px {Y_NAME1 - 34}px;animation:slam .42s cubic-bezier(.3,.7,.3,1) .62s both}}
.n2{{transform-origin:{X0 + n2_w / 2:.0f}px {Y_NAME2 - 34}px;animation:slam .42s cubic-bezier(.3,.7,.3,1) .86s both}}
@keyframes flash{{0%{{opacity:0;transform:scale(.35)}}30%{{opacity:1}}100%{{opacity:0;transform:scale(1.15)}}}}
.f1{{transform-origin:{X0 + n1_w / 2:.0f}px {Y_NAME1 - 34}px;animation:flash .5s cubic-bezier(.2,.8,.3,1) .74s both}}
@keyframes shake{{0%,100%{{transform:translate(0,0)}}20%{{transform:translate(5px,-3px)}}40%{{transform:translate(-4px,3px)}}60%{{transform:translate(3px,-1px)}}80%{{transform:translate(-1px,1px)}}}}
.shake1{{animation:shake .2s linear .8s both}}
.shake2{{animation:shake .2s linear 1.04s both}}
@keyframes rise{{0%{{opacity:0;transform:translateY(26px)}}100%{{opacity:1;transform:translateY(0)}}}}
.kana{{animation:rise .55s cubic-bezier(.16,1,.3,1) both}}
.k0{{animation-delay:1.12s}}.k1{{animation-delay:1.2s}}.k2{{animation-delay:1.28s}}
@keyframes wipeR{{0%{{opacity:0;transform:translateX(-22px)}}100%{{opacity:1;transform:translateX(0)}}}}
.ep{{animation:wipeR .55s cubic-bezier(.16,1,.3,1) 1.25s both}}
.sub{{animation:rise .6s cubic-bezier(.16,1,.3,1) 1.4s both}}
@keyframes pop{{0%{{opacity:0;transform:rotate(-6deg) scale(.4)}}60%{{opacity:1;transform:rotate(-6deg) scale(1.08)}}100%{{opacity:1;transform:rotate(-6deg) scale(1)}}}}
.stk{{transform-origin:{PX_L + 14 + sticker_w / 2:.0f}px {PY_B - 22}px;animation:pop .45s cubic-bezier(.3,.7,.3,1) 1.5s both}}
@keyframes dots{{0%{{opacity:0;transform:translateY(-30px)}}100%{{opacity:1;transform:translateY(0)}}}}
.dots{{animation:dots 1s cubic-bezier(.16,1,.3,1) .45s both}}
@keyframes type{{{kf_type}}}
.typ{{animation:type 1.05s linear 1.75s both}}
@keyframes cur{{0%{{opacity:0}}1%{{opacity:1}}100%{{opacity:1}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.curs{{animation:cur .01s linear 1.72s both}}
.blink{{animation:blink 1s steps(1,end) 2.9s infinite}}
"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Younes Noufair, Lead Software Engineer at Maxmind.ma, Casablanca. I build software that connects ideas to reality.">
<style>{css}</style>
<defs>
<clipPath id="card"><rect width="{W}" height="{H}" rx="24"/></clipPath>
<clipPath id="panel"><polygon points="{pts(POLY)}"/></clipPath>
<linearGradient id="rg" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity=".5"/><stop offset=".64" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="rm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#rg)"/></mask>
<pattern id="ht" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="4" cy="4" r="1.5" fill="{dot_col}"/></pattern>
<pattern id="ht2" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="3" cy="3" r="1.25" fill="{t['bg']}"/></pattern>
<linearGradient id="dg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".1"/><stop offset=".3" stop-color="#fff" stop-opacity=".85"/><stop offset=".6" stop-color="#fff" stop-opacity=".85"/><stop offset=".86" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="dm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#dg)"/></mask>
<linearGradient id="pg" x1="0" x2="0" y1="0" y2="1"><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".75"/></linearGradient>
<mask id="pm" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#pg)"/></mask>
<clipPath id="tc"><rect class="typ" x="{X0 - 4:.1f}" y="{Y_TAG - 26}" width="{tag_w + 4:.1f}" height="36"/></clipPath>
</defs>
<rect width="{W}" height="{H}" rx="24" fill="{t['bg']}"/>
<g clip-path="url(#card)">
 <g class="shake1"><g class="shake2">
  <g mask="url(#rm)"><g class="raysfade"><g class="raysdrift"><g class="rays"><path d="{rays(11, 84)}" fill="{ray_col}" fill-opacity="{ray_op}"/></g></g></g></g>
  <g class="dots" mask="url(#dm)"><polygon points="{pts([(512, 0), (600, 0), (540, H), (452, H)])}" fill="url(#ht)" opacity="{'.55' if not dark else '.6'}"/></g>
  <polygon class="slab" points="{pts(POLY)}" fill="{t['cobalt']}"/>
  <g class="photo">
   <g clip-path="url(#panel)">
    <rect x="{PX_L}" y="{PY_T}" width="{PX_R - PX_L}" height="{PY_B - PY_T}" fill="{t['cobalt']}"/>
    <image href="{photo}" x="{(PX_L + PX_R) / 2 - 170:.0f}" y="{PY_T - 6}" width="340" height="340" preserveAspectRatio="xMidYMid slice"/>
    <rect x="{PX_L}" y="{PY_T}" width="{PX_R - PX_L}" height="{PY_B - PY_T}" fill="url(#ht2)" mask="url(#pm)"/>
   </g>
   <polygon points="{pts(POLY)}" fill="none" stroke="{t['ink']}" stroke-width="6" stroke-linejoin="round"/>
  </g>
  <g class="stk"><rect x="{PX_L + 14}" y="{PY_B - 36}" width="{sticker_w:.1f}" height="28" rx="6" fill="{t['impact']}" stroke="#0f1013" stroke-width="2"/><text class="jx" x="{PX_L + 14 + sticker_w / 2:.1f}" y="{PY_B - 17.5}" font-size="13" letter-spacing="1" text-anchor="middle" fill="#0f1013">{esc(STICKER)}</text></g>
  {kana}
  <polygon class="f1" points="{burst(X0 + n1_w / 2, Y_NAME1 - 34, 70, 118)}" fill="{t['impact']}"/>
  <text class="jx n1" x="{X0 - 4}" y="{Y_NAME1}" font-size="{NAME_SIZE}" letter-spacing="{NAME_TRACK}" fill="{t['ink']}">{NAME1}</text>
  <text class="jx n2" x="{X0 - 4}" y="{Y_NAME2}" font-size="{NAME_SIZE}" letter-spacing="{NAME_TRACK}" fill="none" stroke="{t['cobalt']}" stroke-width="2.2" stroke-linejoin="round">{NAME2}</text>
 </g></g>
 <g class="ep">
  <rect x="{X0}" y="38" width="{ep_w:.1f}" height="24" rx="12" fill="{t['cobalt']}"/>
  <text class="jx" x="{X0 + ep_w / 2:.1f}" y="54.5" font-size="12" letter-spacing="1" text-anchor="middle" fill="{t['on_cobalt']}">{esc(EP)}</text>
  <text class="jx" x="{X0 + ep_w + 12:.1f}" y="54.5" font-size="12" letter-spacing="2" fill="{t['ink2']}">{esc(ARC)}</text>
 </g>
 <text class="js sub" x="{X0}" y="{Y_SUB}" font-size="16" fill="{t['ink2']}">{esc(SUB_A)}<tspan class="jx" fill="{t['ink']}">{esc(SUB_B)}</tspan><tspan xml:space="preserve">{esc(SUB_C)}</tspan></text>
 <text class="jx" x="{X0}" y="{Y_TAG}" font-size="{TAG_SIZE}" clip-path="url(#tc)" xml:space="preserve">{tag_spans}</text>
 <g class="curs"><g class="typ"><rect class="blink" x="{X0 + 2}" y="{Y_TAG - 19}" width="3" height="23" rx="1.5" fill="{t['cobalt']}"/></g></g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="24" fill="none" stroke="{t['line']}" stroke-width="1"/>
</svg>"""


if __name__ == "__main__":
    write("title", {"light": scene("light"), "dark": scene("dark")})
