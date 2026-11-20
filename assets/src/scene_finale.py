"""
Scene "finale" — the last frame of the episode, turned into a call to action.

    python assets/src/scene_finale.py      → assets/finale-light.svg, assets/finale-dark.svg

Timeline (s):  0.15–1.0 arrow banner slides in (speed lines trail it) · 1.0–2.3 freeze-frame tone
               · 1.05–1.45 つづく stamps in · 1.5 PRESS START fades in, blinks forever from 2.3
               · 1.8 footer · 2.4–3.7 basketball arcs once and swishes · from 2.5 arrow nudges right (loop).
"""
from lib import THEMES, W, Metrics, esc, font_css, write

H = 220
NAME = "finale"

BANNER = "TO BE CONTINUED"
JP = "つづく"
CTA = "PRESS START TO COLLABORATE"
FOOT_K = "NEXT EPISODE:"
FOOT_V = "your project  ·  linkedin.com/in/younes-noufair-579ab1191  ·  noufair97@gmail.com"
ALL_TEXT = BANNER + JP + CTA + FOOT_K + FOOT_V + "Younes Noufair"

mx = Metrics("JX")
ms = Metrics("JS")

# ── geometry ──
PAD = 32
B_SIZE, B_TRACK = 30, 2.4
b_w = mx.width(BANNER, B_SIZE, B_TRACK)
BODY_Y0, BODY_Y1 = 28, 86            # arrow body
HEAD_Y0, HEAD_Y1 = 16, 98            # arrowhead
CY = (BODY_Y0 + BODY_Y1) / 2
TXT_X = PAD + 30
CHEV_X = TXT_X + b_w + 26            # three small chevrons after the text
BODY_X1 = CHEV_X + 76
HEAD_X1 = BODY_X1 + 44

C_SIZE, C_TRACK = 30, 1.2
c_w = mx.width(CTA, C_SIZE, C_TRACK)
C_Y = 148
TRI_W = 20
C_X = PAD + TRI_W + 14

F_SIZE = 12.5
F_Y = 196
fk_w = mx.width(FOOT_K, F_SIZE, 1.2)

# hoop (right side, below the katakana)
HOOP_CX, HOOP_Y, HOOP_R = 768, 132, 20


def arrow_path():
    x0 = PAD
    # tail notch on the left, long body, sharp head
    return (f"M{x0} {BODY_Y0} L{BODY_X1} {BODY_Y0} L{BODY_X1} {HEAD_Y0} L{HEAD_X1} {CY} "
            f"L{BODY_X1} {HEAD_Y1} L{BODY_X1} {BODY_Y1} L{x0} {BODY_Y1} L{x0 + 14} {CY} Z")


def build(theme: str) -> str:
    t = THEMES[theme]
    css = font_css(ALL_TEXT, keys=("JX", "JS", "JP"))
    E = "cubic-bezier(.16,1,.3,1)"
    tone = "#c89a62" if theme == "light" else "#6b5335"
    tone_op = 0.20 if theme == "light" else 0.22

    style = f"""{css}
*{{transform-box:fill-box}}
.slide{{animation:slide 0.9s {E} 0.15s both}}
@keyframes slide{{0%{{transform:translateX(-{HEAD_X1 + 40}px)}}100%{{transform:translateX(0)}}}}
.nudge{{animation:nudge 1.8s ease-in-out 2.5s infinite}}
@keyframes nudge{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(9px)}}}}
.chev{{animation:chev 1.8s ease-in-out infinite both}}
@keyframes chev{{0%,100%{{opacity:.35}}40%{{opacity:1}}}}
.sl{{stroke-dasharray:260 600;stroke-dashoffset:260;animation:sl 1.1s cubic-bezier(.3,.7,.2,1) both}}
@keyframes sl{{0%{{stroke-dashoffset:260;opacity:1}}60%{{opacity:1}}100%{{stroke-dashoffset:-560;opacity:0}}}}
.freeze{{animation:freeze 2.4s linear both}}
@keyframes freeze{{0%,41%{{opacity:0}}45%{{opacity:1}}80%{{opacity:1}}100%{{opacity:0}}}}
.kick{{animation:kick .5s {E} 0.98s both}}
@keyframes kick{{0%{{transform:scale(1.015)}}100%{{transform:scale(1)}}}}
.stamp{{opacity:0;animation:stamp .45s {E} both;transform-origin:50% 50%}}
@keyframes stamp{{0%{{opacity:0;transform:scale(1.6) rotate(-8deg)}}100%{{opacity:1;transform:scale(1) rotate(0)}}}}
.ul{{stroke-dasharray:200;stroke-dashoffset:200;animation:ul .6s {E} 1.5s both}}
@keyframes ul{{to{{stroke-dashoffset:0}}}}
.cta{{animation:ctaIn .6s {E} 1.5s both}}
@keyframes ctaIn{{0%{{opacity:0;transform:translateY(10px)}}100%{{opacity:1;transform:translateY(0)}}}}
.blink{{animation:blink 1.1s ease-in-out 2.3s infinite}}
@keyframes blink{{0%,52%{{opacity:1}}62%,90%{{opacity:.12}}100%{{opacity:1}}}}
.foot{{animation:fade .7s ease-out 1.8s both}}
@keyframes fade{{0%{{opacity:0;transform:translateY(6px)}}100%{{opacity:1;transform:translateY(0)}}}}
.hoop{{animation:fade .6s ease-out 1.9s both}}
.bx{{animation:bx 1.3s linear 2.4s both}}
@keyframes bx{{0%{{transform:translateX(0)}}72%{{transform:translateX(112px)}}100%{{transform:translateX(112px)}}}}
.by{{animation:by 1.3s 2.4s both}}
@keyframes by{{0%{{transform:translateY(0);animation-timing-function:cubic-bezier(.3,.6,.6,1)}}
36%{{transform:translateY(-60px);animation-timing-function:cubic-bezier(.4,0,.75,.5)}}
72%{{transform:translateY(-32px);animation-timing-function:cubic-bezier(.3,0,.8,.6)}}
100%{{transform:translateY(-2px)}}}}
.bo{{animation:bo 1.3s linear 2.4s both}}
@keyframes bo{{0%{{opacity:0}}6%{{opacity:1}}84%{{opacity:1}}100%{{opacity:0}}}}
.spin{{animation:spin 1.3s linear 2.4s both;transform-origin:50% 50%}}
@keyframes spin{{to{{transform:rotate(-300deg)}}}}
.net{{animation:net .5s ease-out 3.33s both;transform-origin:50% 0}}
@keyframes net{{0%{{transform:scaleY(1)}}35%{{transform:scaleY(1.28) scaleX(.86)}}70%{{transform:scaleY(.94)}}100%{{transform:scaleY(1)}}}}
.swish{{opacity:0;animation:swish .7s ease-out 3.38s both}}
@keyframes swish{{0%{{opacity:0;transform:translateY(4px)}}30%{{opacity:1}}100%{{opacity:0;transform:translateY(-2px)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation-duration:0s!important;animation-delay:0s!important;animation-iteration-count:1!important}}}}
"""

    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
             f'aria-label="To be continued. Press start to collaborate: Younes Noufair on LinkedIn, linkedin.com/in/younes-noufair-579ab1191, noufair97@gmail.com">')
    p.append(f"<style>{style}</style>")
    p.append(f'<defs><clipPath id="card"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="24"/></clipPath>'
             f'<pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="{t["ink"]}" opacity=".16"/></pattern></defs>')
    p.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="24" fill="{t["bg"]}" stroke="{t["line"]}"/>')
    p.append('<g clip-path="url(#card)"><g class="kick">')

    # ── speed lines trailing the arrow ──
    for i, (y, d, wdt) in enumerate([(36, .18, 2), (50, .24, 3), (66, .2, 2), (78, .28, 2.5), (90, .32, 1.5)]):
        p.append(f'<line class="sl" style="animation-delay:{d}s" x1="-40" y1="{y}" x2="{HEAD_X1 - 60}" y2="{y}" '
                 f'stroke="{t["cobalt"] if i % 2 else t["ink3"]}" stroke-width="{wdt}" stroke-linecap="round"/>')

    # ── arrow banner ──
    p.append('<g class="slide"><g class="nudge">')
    p.append(f'<path d="{arrow_path()}" fill="{t["ink"]}" stroke-linejoin="round"/>')
    # thin cobalt rail under the banner text
    p.append(f'<rect x="{PAD + 24}" y="{BODY_Y1 - 7}" width="{BODY_X1 - PAD - 24}" height="2" fill="{t["cobalt"]}"/>')
    p.append(f'<text class="jx" x="{TXT_X}" y="{CY + B_SIZE * 0.36:.1f}" font-size="{B_SIZE}" letter-spacing="{B_TRACK}" '
             f'fill="{t["bg"]}" font-style="normal">{esc(BANNER)}</text>')
    for k in range(3):
        x = CHEV_X + k * 19
        p.append(f'<path class="chev" style="animation-delay:{k * 0.18:.2f}s" d="M{x} {CY - 10} L{x + 10} {CY} L{x} {CY + 10}" '
                 f'fill="none" stroke="{t["impact"] if theme == "light" else t["cobalt"]}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    p.append("</g></g>")

    # ── katakana つづく ──
    jsz = 58
    jx0 = W - PAD - 3 * jsz - 8
    for k, ch in enumerate(JP):
        x = jx0 + k * (jsz + 4)
        p.append(f'<text class="jp stamp" style="animation-delay:{1.05 + k * 0.14:.2f}s" x="{x}" y="{80}" font-size="{jsz}" '
                 f'fill="{t["cobalt"]}">{ch}</text>')

    # ── hoop ──
    hx0, hx1 = HOOP_CX - HOOP_R, HOOP_CX + HOOP_R
    p.append('<g class="hoop">')
    p.append(f'<rect x="{HOOP_CX - 34}" y="{HOOP_Y - 34}" width="68" height="42" rx="5" fill="none" stroke="{t["line"]}" stroke-width="2"/>')
    p.append(f'<rect x="{HOOP_CX - 13}" y="{HOOP_Y - 20}" width="26" height="17" rx="2" fill="none" stroke="{t["line"]}" stroke-width="2"/>')
    net = []
    for k in range(5):
        a = hx0 + 3 + k * (2 * HOOP_R - 6) / 4
        b = HOOP_CX - 12 + k * 6
        net.append(f"M{a:.1f} {HOOP_Y} L{b:.1f} {HOOP_Y + 26}")
    net.append(f"M{hx0 + 6} {HOOP_Y + 9} L{hx1 - 6} {HOOP_Y + 9} M{HOOP_CX - 14} {HOOP_Y + 18} L{HOOP_CX + 14} {HOOP_Y + 18}")
    p.append("</g>")

    # ── basketball (arcs once, swishes) ── start at (650, 176)
    bx0, by0, br = HOOP_CX - 112, HOOP_Y + 30, 8
    p.append(f'<g class="bo"><g class="bx"><g class="by"><g class="spin">'
             f'<circle cx="{bx0}" cy="{by0}" r="{br}" fill="{t["peach"]}" stroke="{t["ink"]}" stroke-width="1.6"/>'
             f'<path d="M{bx0 - br} {by0} L{bx0 + br} {by0} M{bx0} {by0 - br} L{bx0} {by0 + br} '
             f'M{bx0 - 6} {by0 - 7} Q{bx0 - 2} {by0} {bx0 - 6} {by0 + 7} M{bx0 + 6} {by0 - 7} Q{bx0 + 2} {by0} {bx0 + 6} {by0 + 7}" '
             f'fill="none" stroke="{t["ink"]}" stroke-width="1.2"/></g></g></g></g>')
    p.append('<g class="hoop">')
    p.append(f'<g class="net"><path d="{" ".join(net)}" fill="none" stroke="{t["ink3"]}" stroke-width="1.4" stroke-linecap="round"/></g>')
    p.append('</g>')
    # rim drawn over the ball so it passes "through"
    p.append(f'<g class="hoop"><line x1="{hx0 - 2}" y1="{HOOP_Y}" x2="{hx1 + 2}" y2="{HOOP_Y}" stroke="{t["danger"]}" stroke-width="3.5" stroke-linecap="round"/></g>')
    p.append(f'<g class="swish">'
             f'<path d="M{hx1 + 8} {HOOP_Y + 4} l7 -4 M{hx1 + 9} {HOOP_Y + 13} l9 0 M{hx0 - 8} {HOOP_Y + 4} l-7 -4 M{hx0 - 9} {HOOP_Y + 13} l-9 0" '
             f'stroke="{t["cobalt"]}" stroke-width="2.2" stroke-linecap="round"/></g>')

    # ── PRESS START ──
    p.append('<g class="cta"><g class="blink">')
    p.append(f'<path d="M{PAD} {C_Y - 22} L{PAD + TRI_W} {C_Y - 11} L{PAD} {C_Y} Z" fill="{t["cobalt"]}" stroke="{t["cobalt"]}" stroke-width="3" stroke-linejoin="round"/>')
    p.append(f'<text class="jx" x="{C_X}" y="{C_Y}" font-size="{C_SIZE}" letter-spacing="{C_TRACK}" fill="{t["ink"]}">'
             f'PRESS START <tspan fill="{t["cobalt"]}">TO COLLABORATE</tspan></text>')
    p.append("</g></g>")

    # ── footer ──
    p.append('<g class="foot">')
    p.append(f'<line x1="{PAD}" y1="{F_Y - 22}" x2="{W - PAD}" y2="{F_Y - 22}" stroke="{t["line"]}" stroke-width="1"/>')
    p.append(f'<text class="jx" x="{PAD}" y="{F_Y}" font-size="{F_SIZE}" letter-spacing="1.2" fill="{t["cobalt"]}">{esc(FOOT_K)}</text>')
    p.append(f'<text class="js" x="{PAD + fk_w + 8:.1f}" y="{F_Y}" font-size="{F_SIZE}" fill="{t["ink2"]}" xml:space="preserve">{esc(FOOT_V)}</text>')
    p.append("</g>")

    p.append("</g>")  # kick
    # ── freeze-frame tone (sepia-ish wash + halftone) ──
    p.append(f'<g class="freeze"><rect width="{W}" height="{H}" fill="{tone}" opacity="{tone_op}"/>'
             f'<rect width="{W}" height="{H}" fill="url(#dots)" opacity=".5"/></g>')
    p.append("</g>")
    p.append("</svg>")
    return "".join(p)


if __name__ == "__main__":
    print(f"banner w={b_w:.0f} arrow end={HEAD_X1:.0f}  cta w={C_X + c_w:.0f}  foot end={PAD + fk_w + 8 + ms.width(FOOT_V, F_SIZE):.0f}")
    write(NAME, {"light": build("light"), "dark": build("dark")})
