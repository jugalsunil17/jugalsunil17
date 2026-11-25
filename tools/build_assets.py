"""Generate the light/dark SVG assets for the GitHub profile README.

Run:  python3 tools/build_assets.py
Writes assets/light/*.svg, assets/dark/*.svg and assets/avatar.svg.
All SVGs are drawn on an 840px wide canvas, close to GitHub's README column,
so font sizes here are roughly the sizes people actually see.
"""
import math
import os
import random
import textwrap
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = 840

THEMES = {
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", accent="#4f46e5", teal="#0f766e", chip="#eef2ff",
                  chipb="#c7d2fe", grid="#e6e9ee", warm="#d9480f"),
    "dark": dict(bg="#0d1117", card="#161b22", border="#30363d", text="#e6edf3",
                 muted="#8d96a0", accent="#818cf8", teal="#2dd4bf", chip="#1c2240",
                 chipb="#3b4380", grid="#1b2129", warm="#ff8a4c"),
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', 'Hiragino Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def e(s):
    return escape(s)


def svg(w, h, body, t=None):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<style>
.sans{{font-family:{SANS};}}
.mono{{font-family:{MONO};}}
</style>
{body}
</svg>
'''


def fade_in(delay, dur=0.3):
    """Fade in after `delay` seconds. Base opacity stays 1, so viewers that do not
    play SVG animation still show the content."""
    total = delay + dur
    k = delay / total
    return (f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{k:.3f};1" '
            f'dur="{total:.2f}s" fill="freeze"/>')


def chip(x, y, label, t, size=13):
    w = len(label) * size * 0.62 + 20
    h = size + 13
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2:.1f}" '
            f'fill="{t["chip"]}" stroke="{t["chipb"]}"/>'
            f'<text x="{x + w/2:.1f}" y="{y + h/2 + size*0.36:.1f}" text-anchor="middle" '
            f'class="mono" font-size="{size}" fill="{t["accent"]}">{e(label)}</text>'), w


def card(x, y, w, h, t, rx=14):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{t["card"]}" stroke="{t["border"]}"/>'


# ---------------------------------------------------------------- avatar
def avatar_body(cx=256, cy=256, scale=1.0, clip_circle=True, uid="av"):
    """Half human / half robot portrait on a 512x512 canvas (dark, serious style)."""
    rnd = random.Random(7)

    seam_pts = [(256, 60), (258, 96), (252, 128), (260, 160), (251, 196), (259, 236), (252, 272),
                (261, 306), (253, 344), (259, 384), (254, 420), (258, 452), (256, 512)]
    seam = " ".join(f"{x},{y}" for x, y in seam_pts)
    left_clip = f"0,0 {seam} 0,512"
    right_clip = f"512,0 {seam} 512,512"

    head = ("M256,100 C318,100 362,140 368,205 C372,245 371,282 366,318 C360,356 350,380 334,400 "
            "C314,424 290,442 256,444 C222,442 198,424 178,400 C162,380 152,356 146,318 "
            "C141,282 140,245 144,205 C150,140 194,100 256,100 Z")
    beard = ("M140,262 C150,300 176,326 214,342 L220,354 C228,372 242,378 256,378 L256,452 "
             "C220,450 194,432 174,406 C158,386 148,352 144,318 Z")
    moustache = ("M256,332 C243,330 229,334 217,345 C214,349 216,353 221,352 C232,346 244,344 256,346 Z")

    # beard texture: short strokes, denser and darker lower down
    strokes = []
    for _ in range(520):
        x = rnd.uniform(140, 256)
        y = rnd.uniform(270, 452)
        ang = rnd.uniform(1.2, 1.9)
        ln = rnd.uniform(4, 9)
        x2 = x + math.cos(ang) * ln * (1 if x < 200 else 0.6)
        y2 = y + math.sin(ang) * ln
        op = 0.25 + 0.5 * (y - 270) / 182
        col = "#2b221c" if rnd.random() < 0.6 else "#0a0807"
        strokes.append(f'<path d="M{x:.1f},{y:.1f} L{x2:.1f},{y2:.1f}" stroke="{col}" stroke-opacity="{op:.2f}"/>')

    # hair strands following the curtain flow (part at centre, sweeping out and back)
    strands = []
    for i in range(22):
        k = i / 21
        sx = 257 - k * 3
        sy = 96 + k * 12
        ex = 124 + k * 30 + rnd.uniform(-3, 3)
        ey = 150 + k * 80
        c1x, c1y = 226 - k * 10, 60 + k * 40
        c2x, c2y = 150 + k * 10, 70 + k * 70
        col = "#2e2622" if i % 3 == 0 else "#1c1715"
        strands.append(f'<path d="M{sx:.1f},{sy:.1f} C{c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {ex:.1f},{ey:.1f}" '
                       f'stroke="{col}" stroke-width="{1.0 if i % 3 else 1.4}" fill="none" stroke-linecap="round" opacity="0.7"/>')

    return f'''
<defs>
  <radialGradient id="{uid}bg" cx="50%" cy="40%" r="75%">
    <stop offset="0" stop-color="#1b1f27"/><stop offset="0.55" stop-color="#0c0e13"/><stop offset="1" stop-color="#030405"/>
  </radialGradient>
  <linearGradient id="{uid}skin" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#6e4329"/><stop offset="0.18" stop-color="#a8704c"/><stop offset="0.55" stop-color="#b98159"/><stop offset="1" stop-color="#8a5a3c"/>
  </linearGradient>
  <linearGradient id="{uid}skinv" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="0.7" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.35"/>
  </linearGradient>
  <linearGradient id="{uid}beardfade" x1="0" y1="0" x2="0.35" y2="1">
    <stop offset="0" stop-color="#16110e" stop-opacity="0.25"/><stop offset="0.28" stop-color="#16110e" stop-opacity="0.75"/><stop offset="0.55" stop-color="#120e0c" stop-opacity="0.95"/><stop offset="1" stop-color="#0d0a08" stop-opacity="1"/>
  </linearGradient>
  <linearGradient id="{uid}hair" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1c1715"/><stop offset="1" stop-color="#0b0908"/>
  </linearGradient>
  <linearGradient id="{uid}metal" x1="0" y1="0" x2="1" y2="0.4">
    <stop offset="0" stop-color="#8a939e"/><stop offset="0.35" stop-color="#4b535d"/><stop offset="0.75" stop-color="#262b32"/><stop offset="1" stop-color="#14171b"/>
  </linearGradient>
  <linearGradient id="{uid}metal2" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#6b737d"/><stop offset="1" stop-color="#1d2127"/>
  </linearGradient>
  <linearGradient id="{uid}cloth" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#262a31"/><stop offset="1" stop-color="#07080a"/>
  </linearGradient>
  <radialGradient id="{uid}eye" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#fff2e8"/><stop offset="0.22" stop-color="#ff5a3c"/><stop offset="0.6" stop-color="#d4141c"/><stop offset="1" stop-color="#4a0508"/>
  </radialGradient>
  <radialGradient id="{uid}eyeglow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#ff2a1f" stop-opacity="0.55"/><stop offset="1" stop-color="#ff2a1f" stop-opacity="0"/>
  </radialGradient>
  <filter id="{uid}blur" filterUnits="userSpaceOnUse" x="0" y="0" width="512" height="512"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="{uid}haze" filterUnits="userSpaceOnUse" x="-200" y="-200" width="912" height="912"><feGaussianBlur stdDeviation="45"/></filter>
  <filter id="{uid}soft" filterUnits="userSpaceOnUse" x="0" y="0" width="512" height="512"><feGaussianBlur stdDeviation="1.2"/></filter>
  <clipPath id="{uid}L"><polygon points="{left_clip}"/></clipPath>
  <clipPath id="{uid}R"><polygon points="{right_clip}"/></clipPath>
  <clipPath id="{uid}C"><circle cx="256" cy="256" r="256"/></clipPath>
  <clipPath id="{uid}H"><path d="M258,104 C244,84 206,76 172,92 C142,108 126,142 126,180 C126,214 130,250 142,292 C143,262 146,228 152,204 C160,180 176,160 198,144 C216,130 238,118 258,116 Z"/></clipPath>
  <clipPath id="{uid}E"><path d="M180,264 C194,255 214,252 232,258 C216,266 196,268 180,264 Z"/></clipPath>
  <clipPath id="{uid}B"><path d="{beard}"/></clipPath>
</defs>
<g transform="translate({cx - 256*scale},{cy - 256*scale}) scale({scale})">
<g {'clip-path="url(#' + uid + 'C)"' if clip_circle else ''}>
  <rect width="512" height="512" fill="url(#{uid}bg)"/>
  <ellipse cx="470" cy="250" rx="120" ry="220" fill="#ff2a1f" opacity="0.16" filter="url(#{uid}haze)"/>
  <ellipse cx="40" cy="250" rx="110" ry="220" fill="#5eead4" opacity="0.08" filter="url(#{uid}haze)"/>

  <!-- ===== HUMAN (left) ===== -->
  <g clip-path="url(#{uid}L)">
    <path d="M186,404 C190,430 186,452 176,470 L256,478 L256,420 Z" fill="#7d5034"/>
    <path d="M206,432 C218,452 232,466 248,476" stroke="#4a2c1c" stroke-width="5" stroke-opacity="0.5" fill="none" filter="url(#{uid}soft)"/>
    <path d="M186,418 C176,438 152,444 122,446 L188,458 Z" fill="#1e2126"/>
    <path d="M0,512 L0,458 C48,442 104,436 150,442 C168,445 180,452 188,458 L256,468 L256,512 Z" fill="url(#{uid}cloth)"/>
    <path d="M0,458 C48,442 104,436 150,442" stroke="#4a515b" stroke-width="2" fill="none"/>
    <path d="M166,482 C196,474 228,472 256,472 M160,496 C192,488 226,486 256,486" stroke="#24282e" stroke-width="2" fill="none"/>
    <ellipse cx="139" cy="288" rx="13" ry="27" fill="#8a5a3c"/>
    <path d="M136,272 C132,284 134,298 140,306" stroke="#5a3624" stroke-width="3" fill="none"/>
    <path d="{head}" fill="url(#{uid}skin)"/>
    <path d="{head}" fill="url(#{uid}skinv)"/>
    <path d="M150,300 C168,318 196,326 224,322" stroke="#5a3624" stroke-opacity="0.2" stroke-width="10" fill="none" filter="url(#{uid}soft)"/>
    <g clip-path="url(#{uid}B)">
      <path d="{beard}" fill="url(#{uid}beardfade)"/>
      <g stroke-width="1.3" stroke-linecap="round">{''.join(strokes)}</g>
    </g>
    <path d="M228,366 C236,365 246,364 256,364" stroke="#5c2f25" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M232,372 C240,374 248,374 256,373" stroke="#7a4434" stroke-width="2" fill="none" opacity="0.7"/>
    <path d="{moustache}" fill="#0f0b09"/>
    <path d="M248,252 C247,272 244,296 238,314 C236,320 240,324 246,324" stroke="#5a3624" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M232,318 C226,320 226,328 234,330 C240,332 248,330 256,330" stroke="#4a2c1c" stroke-width="2.6" fill="none"/>
    <path d="M252,300 C254,306 254,312 252,316" stroke="#d8a27a" stroke-width="3" opacity="0.5" fill="none"/>
    <path d="M180,264 C194,255 214,252 232,258 C216,266 196,268 180,264 Z" fill="#b3a89c"/>
    <g clip-path="url(#{uid}E)"><circle cx="208" cy="259" r="9" fill="#2a170d"/><circle cx="208" cy="259" r="3.4" fill="#050302"/>
      <path d="M180,258 C196,252 216,250 232,256 L232,250 L180,250 Z" fill="#000" opacity="0.35"/></g>
    <circle cx="211" cy="256.5" r="1.6" fill="#fff" opacity="0.85"/>
    <path d="M176,262 C190,252 214,248 236,256" stroke="#0d0907" stroke-width="4.2" fill="none" stroke-linecap="round"/>
    <path d="M182,268 C198,273 216,271 230,263" stroke="#4a2c1c" stroke-width="2" fill="none" opacity="0.8"/>
    <path d="M160,243 C180,231 206,228 222,232 C234,235 242,242 247,251 C234,245 220,241 206,241 C190,241 174,243 160,243 Z" fill="#0c0908"/>
    <path d="M258,104 C244,84 206,76 172,92 C142,108 126,142 126,180 C126,214 130,250 142,292 C143,262 146,228 152,204 C160,180 176,160 198,144 C216,130 238,118 258,116 Z" fill="url(#{uid}hair)"/>
    <g clip-path="url(#{uid}H)">{''.join(strands)}</g>

  </g>

  <!-- ===== ROBOT (right) ===== -->
  <g clip-path="url(#{uid}R)">
    <path d="M256,452 L336,446 C400,456 460,472 512,488 L512,512 L256,512 Z" fill="#14171b"/>
    <path d="M330,452 L420,470 L470,500 L512,505 M300,470 L380,490 L420,512" stroke="#3a4048" stroke-width="3" fill="none"/>
    <path d="M300,458 L392,472" stroke="#ff2a1f" stroke-opacity="0.35" stroke-width="1.5"/>
    <g>
      <rect x="252" y="398" width="66" height="72" fill="#1b1f24"/>
      <path d="M262,402 V466 M276,402 V466 M290,402 V466 M304,402 V466" stroke="#3d444d" stroke-width="5"/>
      <path d="M268,410 C280,430 270,450 284,466" stroke="#0b0d10" stroke-width="6" fill="none"/>
      <path d="M296,410 C306,432 298,452 310,466" stroke="#0b0d10" stroke-width="6" fill="none"/>
    </g>
    <circle cx="372" cy="288" r="20" fill="url(#{uid}metal2)" stroke="#0d0f12" stroke-width="3"/>
    <circle cx="372" cy="288" r="8" fill="#0d0f12"/><circle cx="372" cy="288" r="3" fill="#ff2a1f"/>
    <path d="{head}" fill="url(#{uid}metal)"/>
    <path d="M256,100 C318,100 362,140 368,205" fill="none" stroke="#c9d1da" stroke-opacity="0.45" stroke-width="2.5"/>
    <path d="M268,118 C300,112 330,124 346,146" fill="none" stroke="#e6ebf0" stroke-opacity="0.25" stroke-width="6" filter="url(#{uid}soft)"/>
    <g fill="none" stroke="#0e1114" stroke-width="2.4">
      <path d="M256,170 H330 L356,190"/>
      <path d="M300,100 L292,170"/>
      <path d="M356,214 L340,300 L362,330"/>
      <path d="M256,290 H284 L300,282"/>
    </g>
    <g fill="#0e1114"><path d="M320,140 h22 v3 h-22z M322,148 h22 v3 h-22z M324,156 h22 v3 h-22z"/></g>
    <path d="M300,300 C320,300 338,312 344,330 L336,402 C322,420 296,436 266,440 L262,380 C286,372 300,350 300,330 Z" fill="#101317"/>
    <g stroke="#59616b" stroke-width="5" stroke-linecap="round">
      <path d="M316,312 L304,396"/><path d="M332,320 L322,394"/>
    </g>
    <g stroke="#8a939e" stroke-width="2"><path d="M316,312 L310,352"/><path d="M332,320 L327,354"/></g>
    <path d="M257,355 L313,351 L313,374 L257,377 Z" fill="#050607"/>
    <g fill="#7a838d"><path d="M259,359 h8 v11 h-8z M270,358.6 h8 v11 h-8z M281,358.2 h8 v11 h-8z M292,357.8 h8 v11 h-8z M303,357.4 h8 v11 h-8z"/></g>
    <path d="M258,300 L272,326 L258,330 Z" fill="#050607"/>
    <ellipse cx="308" cy="262" rx="34" ry="24" fill="#050607"/>
    <circle cx="308" cy="262" r="34" fill="url(#{uid}eyeglow)"/>
    <circle cx="308" cy="262" r="12" fill="url(#{uid}eye)">
      <animate attributeName="r" values="11;13;11" dur="2.6s" repeatCount="indefinite"/>
    </circle>
    <circle cx="304" cy="258" r="2.4" fill="#fff"/>
    <path d="M266,244 C282,236 310,230 348,236 L350,246 C318,242 290,244 268,252 Z" fill="#2a3037" stroke="#0b0d10" stroke-width="1.5"/>
    <path d="M268,244 C290,236 318,233 346,237" stroke="#9aa3ad" stroke-width="1.2" fill="none" opacity="0.7"/>
    <g fill="#0b0d10"><circle cx="350" cy="198" r="3.5"/><circle cx="356" cy="330" r="3.5"/><circle cx="276" cy="140" r="3.5"/><circle cx="330" cy="408" r="3.5"/></g>
  </g>

  <!-- seam: torn skin edge + red glow -->
  <polyline points="{" ".join(f"{x-2},{y}" for x, y in seam_pts[1:-1])}" fill="none" stroke="#3b1f14" stroke-width="3" stroke-linejoin="round"/>
  <polyline points="{" ".join(f"{x+1},{y}" for x, y in seam_pts[1:-1])}" fill="none" stroke="#ff2a1f" stroke-width="1.6" stroke-linejoin="round" opacity="0.8" filter="url(#{uid}soft)">
    <animate attributeName="opacity" values="0.5;0.95;0.5" dur="3s" repeatCount="indefinite"/>
  </polyline>
</g>
<circle cx="256" cy="256" r="244" fill="none" stroke="#2b3038" stroke-width="3"/>
</g>
'''


def build_avatar():
    # square full-bleed version for the GitHub profile picture (GitHub crops it to a circle)
    return svg(512, 512, avatar_body(clip_circle=False, uid="ava"))


# ---------------------------------------------------------------- header
def build_header(t):
    H = 260
    phrases = [
        "building agentic AI for real users",
        "RAG, multi-agent, MCP tool servers",
        "GenAI on AWS Bedrock and GCP",
    ]
    tx, ty, fs = 236, 200, 16
    parts = []
    n = len(phrases)
    for i, p in enumerate(phrases):
        w = len(p) * fs * 0.6
        a, b = i / n, (i + 1) / n
        typed = a + 0.11
        kt_op = f"0;{max(a-0.001,0):.3f};{a:.3f};{b-0.002:.3f};{b:.3f};1" if i else f"0;{b-0.002:.3f};{b:.3f};1"
        v_op = "0;0;1;1;0;0" if i else "1;1;0;0"
        parts.append(f'''
<clipPath id="tp{i}"><rect x="{tx}" y="{ty-20}" width="{w if i == 0 else 0:.0f}" height="28">
  <animate attributeName="width" values="0;0;{w:.0f};{w:.0f}" keyTimes="0;{a:.3f};{typed:.3f};1" dur="12s" repeatCount="indefinite"/>
</rect></clipPath>
<g opacity="{1 if i == 0 else 0}">
  <animate attributeName="opacity" values="{v_op}" keyTimes="{kt_op}" dur="12s" repeatCount="indefinite"/>
  <text x="{tx}" y="{ty}" class="mono" font-size="{fs}" fill="{t['teal']}" clip-path="url(#tp{i})">{e(p)}</text>
  <rect x="{tx + (w if i == 0 else 0) + 3:.0f}" y="{ty-14}" width="9" height="18" fill="{t['teal']}">
    <animate attributeName="x" values="{tx+3};{tx+3};{tx+w+3:.0f};{tx+w+3:.0f}" keyTimes="0;{a:.3f};{typed:.3f};1" dur="12s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
  </rect>
</g>''')

    gx, gy = 724, 128
    nodes = [("LLM", 0, -78), ("RAG", 78, -30), ("MCP", 66, 58), ("tools", -40, 82), ("guardrails", -60, -40)]
    graph = []
    for i, (lab, dx, dy) in enumerate(nodes):
        graph.append(f'<line x1="{gx}" y1="{gy}" x2="{gx+dx}" y2="{gy+dy}" stroke="{t["accent"]}" stroke-opacity="0.55" stroke-width="1.6" stroke-dasharray="4 6">'
                     f'<animate attributeName="stroke-dashoffset" values="20;0" dur="{1.2+0.25*i:.2f}s" repeatCount="indefinite"/></line>')
    for i, (lab, dx, dy) in enumerate(nodes):
        x2, y2 = gx + dx, gy + dy
        w = len(lab) * 12 * 0.62 + 20
        graph.append(f'<rect x="{x2-w/2:.1f}" y="{y2-12}" width="{w:.1f}" height="24" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>'
                     f'<text x="{x2}" y="{y2+4}" text-anchor="middle" class="mono" font-size="12" fill="{t["text"]}">{lab}</text>'
                     f'<circle cx="{x2-w/2+1:.1f}" cy="{y2}" r="3" fill="{t["teal"]}"><animate attributeName="opacity" values="0.2;1;0.2" dur="2s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/></circle>')
    graph.append(f'<circle cx="{gx}" cy="{gy}" r="27" fill="none" stroke="{t["teal"]}" stroke-width="2">'
                 f'<animate attributeName="r" values="26;40;26" dur="3s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values="0.7;0;0.7" dur="3s" repeatCount="indefinite"/></circle>')
    graph.append(f'<circle cx="{gx}" cy="{gy}" r="26" fill="{t["accent"]}"/>'
                 f'<text x="{gx}" y="{gy+4.5}" text-anchor="middle" class="mono" font-size="13" font-weight="700" fill="#ffffff">agent</text>')

    body = f'''
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{t['bg']}" stroke="{t['border']}"/>
<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{t['grid']}"/></pattern></defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="url(#dots)"/>
<svg x="30" y="45" width="170" height="170" viewBox="0 0 512 512">{avatar_body(uid='hd')}</svg>
<text x="222" y="78" class="mono" font-size="13" fill="{t['muted']}">~/jugalsunil17 $ ./hello.sh</text>
<text x="220" y="128" class="sans" font-size="46" font-weight="800" fill="{t['text']}">Jugal Sunil</text>
<text x="222" y="160" class="sans" font-size="18" fill="{t['muted']}">AI Engineer <tspan fill="{t['accent']}">/</tspan> Tokyo, Japan</text>
<text x="222" y="200" class="mono" font-size="{fs}" fill="{t['accent']}">&gt;</text>
{''.join(parts)}
{''.join(graph)}
'''
    return svg(W, H, body)


# ---------------------------------------------------------------- section heading
def build_heading(t, num, title, sub):
    H = 64
    tw = len(title) * 22 * 0.56
    lx = 52 + tw + 14
    body = f'''
<rect x="0" y="4" width="{W}" height="{H-6}" rx="10" fill="{t['bg']}"/>
<text x="8" y="34" class="mono" font-size="14" fill="{t['accent']}">{num}</text>
<text x="40" y="35" class="sans" font-size="22" font-weight="700" fill="{t['text']}">{e(title)}</text>
<line x1="{lx:.0f}" y1="28" x2="{W-6}" y2="28" stroke="{t['border']}" stroke-width="1.5"/>
<line x1="{lx:.0f}" y1="28" x2="{lx+70:.0f}" y2="28" stroke="{t['accent']}" stroke-width="2.5">
  <animate attributeName="x1" values="{lx:.0f};{W-76};{lx:.0f}" dur="8s" repeatCount="indefinite"/>
  <animate attributeName="x2" values="{lx+70:.0f};{W-6};{lx+70:.0f}" dur="8s" repeatCount="indefinite"/>
</line>
<text x="40" y="55" class="mono" font-size="12.5" fill="{t['muted']}">{e(sub)}</text>
'''
    return svg(W, H, body)


# ---------------------------------------------------------------- whoami terminal
def build_whoami(t):
    lines = [
        ("cmd", "whoami"),
        ("out", "Jugal Sunil, AI Engineer at Akatsuki AI Technologies (Tokyo)"),
        ("cmd", "cat focus.txt"),
        ("li", "Agentic AI: multi-agent pipelines, MCP tool servers, ACP, browser agents"),
        ("li", "RAG: vector search, grounded answers with sources"),
        ("li", "GenAI in production: guardrails, human approval steps, spend caps"),
        ("li", "Cloud: AWS (Bedrock, Terraform, OIDC), Google Cloud (Cloud Run, Vertex AI)"),
        ("cmd", "cat background.txt"),
        ("out", "MSc Computer Science (India) and MSc IT (Kyoto)."),
        ("out", "Before AI: Python data engineering, Flask backends, technical training."),
        ("cmd", "cat certs.txt"),
        ("out", "Microsoft Azure Fundamentals (AZ-900)  |  JLPT N3"),
        ("cmd", "cat languages.txt"),
        ("out", "English (fluent)  |  Japanese (business level)  |  Malayalam (native)"),
    ]
    top, lh, fs = 70, 24, 13.5
    H = top + len(lines) * lh + 18
    rows = []
    for i, (kind, s) in enumerate(lines):
        y = top + i * lh
        if kind == "cmd":
            inner = f'<tspan fill="{t["teal"]}">jugal@tokyo</tspan><tspan fill="{t["muted"]}"> ~ $ </tspan><tspan fill="{t["text"]}" font-weight="700">{e(s)}</tspan>'
        elif kind == "li":
            inner = f'<tspan fill="{t["accent"]}">&gt; </tspan><tspan fill="{t["text"]}">{e(s)}</tspan>'
        else:
            inner = f'<tspan fill="{t["text"]}">{e(s)}</tspan>'
        rows.append(f'<text x="26" y="{y}" class="mono" font-size="{fs}">{inner}{fade_in(0.2*i)}</text>')
    body = f'''
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{t['card']}" stroke="{t['border']}"/>
<path d="M1,15 a14,14 0 0 1 14,-14 H{W-15} a14,14 0 0 1 14,14 V38 H1 Z" fill="{t['bg']}" stroke="{t['border']}"/>
<circle cx="24" cy="20" r="6" fill="#ff5f57"/><circle cx="44" cy="20" r="6" fill="#febc2e"/><circle cx="64" cy="20" r="6" fill="#28c840"/>
<text x="{W/2}" y="25" text-anchor="middle" class="mono" font-size="12.5" fill="{t['muted']}">zsh: ~/about</text>
{''.join(rows)}
'''
    return svg(W, H, body)


# ---------------------------------------------------------------- work cards
WORK = [
    ("Agentic Marketing AI Platform",
     "Production multi-agent platform for an enterprise marketing team: modular agent pipelines, one LLM broker for Gemini, Claude and GPT-4o, RAG on BigQuery and Vertex AI.",
     "14+ agent pipelines, in production", ["GCP", "FastAPI", "React", "MCP"]),
    ("Agentic HR Automation",
     "Multi-user agent that does sourcing, outreach and pipeline work in a real logged-in browser for recruiters, with human approval before anything is sent.",
     "8 recruiters, 10 h/week saved", ["Claude", "ACP", "MCP", "CDP"]),
    ("GenAI Campaign Generator (PoC)",
     "Turns raw, unstructured event data into email campaigns, subject-line variants and targeting. The LLM writes copy only; every fact is checked in Python.",
     "extract > validate > generate > guardrail", ["Claude", "Gemini", "FastAPI"]),
    ("Real-Time Speech Translation",
     "Streams live speech translation to the browser: voice activity detection, Whisper Large V3 on MLX and a 4-bit Llama 3 8B, plus a FAISS glossary for business terms.",
     "400-900 ms latency threshold", ["WebSockets", "Whisper", "Llama 3"]),
    ("Sales AI Agent Infrastructure",
     "Sole engineer on the AWS foundation for a sales-automation agent platform: Terraform with remote state, CI/CD with GitHub Actions and OIDC, AI layer on Bedrock.",
     "solo build, infra as code", ["AWS", "Terraform", "Bedrock"]),
    ("Retail Shelf Proposal AI",
     "Pipeline that turns social trends into weekly store-shelf proposals with AI-generated images. I work on requirements analysis and AI output quality checks.",
     "ongoing", ["Gemini 2.5 Pro", "Gemini 3 Pro Image"]),
]


def build_work(t):
    cols, gap, ch = 2, 16, 236
    cw = (W - 2 - gap) / 2
    rows = (len(WORK) + cols - 1) // cols
    H = rows * ch + (rows - 1) * gap + 2
    out = []
    for i, (title, desc, metric, tags) in enumerate(WORK):
        x = 1 + (i % cols) * (cw + gap)
        y = 1 + (i // cols) * (ch + gap)
        lines = textwrap.wrap(desc, 50, break_on_hyphens=False)
        txt = "".join(f'<tspan x="{x+22:.1f}" dy="{0 if j == 0 else 21}">{e(l)}</tspan>' for j, l in enumerate(lines))
        cx = x + 22
        chips = []
        for tag in tags:
            c, w = chip(cx, y + ch - 44, tag, t, size=12.5)
            chips.append(c)
            cx += w + 8
        out.append(f'''
<g>{fade_in(0.15*i, 0.5)}
{card(f"{x:.1f}", y, f"{cw:.1f}", ch, t)}
<rect x="{x:.1f}" y="{y+18}" width="4" height="28" rx="2" fill="{t['accent']}"/>
<text x="{x+22:.1f}" y="{y+40}" class="sans" font-size="18" font-weight="700" fill="{t['text']}">{e(title)}</text>
<text x="{x+22:.1f}" y="{y+70}" class="sans" font-size="14.5" fill="{t['muted']}">{txt}</text>
<text x="{x+22:.1f}" y="{y+ch-60}" class="mono" font-size="13" fill="{t['teal']}">{e(metric)}</text>
{''.join(chips)}
</g>''')
    return svg(W, H, "".join(out))


# ---------------------------------------------------------------- internal tools (Akatsuki, description only)
INTERNAL = [
    ("Akatsuki Artifacts",
     "Workspace where reports and pages made with Claude are saved, versioned and shared by link, with an MCP server so Claude can update them later. Main contributor.",
     ["Next.js", "MCP", "Cloud Run"]),
    ("Daily Report Tracker",
     "Checks daily reports in Slack for about 40 staff in Japan and India, logs them to Google Sheets, sends reminders and an HR summary, plus a Gemini review of each report.",
     ["Apps Script", "Slack", "Gemini"]),
    ("Akatsuki Workbench",
     "Internal tracker for team projects, APIs and tasks, with login, role-based access and an in-browser page editor. Prototype, not deployed yet.",
     ["Next.js", "Prisma", "better-auth"]),
]


def build_internal(t):
    gap, ch, top = 12, 222, 34
    cw = (W - 2 - 2 * gap) / 3
    H = top + ch + 2
    out = [f'<rect x="0" y="2" width="360" height="26" rx="6" fill="{t["bg"]}"/>'
           f'<text x="4" y="20" class="mono" font-size="13" fill="{t["muted"]}">internal tools for Akatsuki AI Technologies</text>']
    for i, (title, desc, tags) in enumerate(INTERNAL):
        x = 1 + i * (cw + gap)
        y = top
        lines = textwrap.wrap(desc, 36, break_on_hyphens=False)
        txt = "".join(f'<tspan x="{x+18:.1f}" dy="{0 if j == 0 else 19}">{e(l)}</tspan>' for j, l in enumerate(lines))
        cx, chips = x + 18, []
        for tag in tags:
            c, w = chip(cx, y + ch - 40, tag, t, size=11.5)
            chips.append(c)
            cx += w + 6
        out.append(f'''
<g>{fade_in(0.15*i, 0.5)}
{card(f"{x:.1f}", y, f"{cw:.1f}", ch, t)}
<rect x="{x:.1f}" y="{y+16}" width="4" height="26" rx="2" fill="{t['teal']}"/>
<text x="{x+18:.1f}" y="{y+36}" class="sans" font-size="16.5" font-weight="700" fill="{t['text']}">{e(title)}</text>
<text x="{x+18:.1f}" y="{y+64}" class="sans" font-size="13.5" fill="{t['muted']}">{txt}</text>
{''.join(chips)}
</g>''')
    return svg(W, H, "".join(out))


# ---------------------------------------------------------------- personal project cards (one SVG each so each can be a link)
PROJECTS = {
    "pharmaiq": ("PharmaIQ", "in progress",
                 "Early stage. Building a RAG + multi-agent research assistant over public drug data (openFDA, ClinicalTrials.gov) with cited answers. Planned stack:",
                 ["Databricks", "LangGraph", "AutoGen", "Bedrock"]),
    "drone": ("Drone Show 3D Generation", "personal",
              "Turns a 2D image into 3D flight data for a drone show with local AI models; each drone's position and depth are calculated automatically.",
              ["Hunyuan3D", "TripoSR", "Python"]),
    "go2": ("Unitree Go2 Object Detection", "repo",
            "Real-time object detection for the Unitree Go2 robot: multi-threaded YOLOv8 inference with an FPS, CPU and RAM overlay.",
            ["YOLOv8", "OpenCV", "Apple MPS"]),
    "taskmgr": ("Task Manager API", "repo",
                "REST API for task management (create, read, update, delete) with Flask, SQLAlchemy and SQLite.",
                ["Flask", "SQLAlchemy", "SQLite"]),
    "slack": ("Slack Watcher Agent", "personal",
              "Polls Slack, a small Claude model triages each message, a simple router picks the right model, and an agent loop handles it with tools. Alerts go to Telegram.",
              ["Claude API", "Slack SDK", "Telegram"]),
    "docskills": ("Document Skills for Agents", "personal",
                  "Agent skills for DOCX, PDF, PPTX and XLSX: create, inspect, redact, merge, render and check documents, built on open-source Python libraries.",
                  ["python-docx", "pypdf", "Python"]),
    "sheetmail": ("Sheet-to-Email Agent", "personal",
                  "Practice agent on Google ADK: reads a row from Google Sheets, drafts an email grounded in a local knowledge base (RAG), and sends only after human approval.",
                  ["Google ADK", "Gemini", "ChromaDB"]),
}


def build_project(t, key, wide=False):
    title, status, desc, tags = PROJECTS[key]
    CW, H, PAD = 412, 196, 10  # PAD: transparent space under each card so rows do not touch
    if wide:
        CW, H = W, 160
    lines = textwrap.wrap(desc, 100 if wide else 48, break_on_hyphens=False)
    txt = "".join(f'<tspan x="20" dy="{0 if j == 0 else 20}">{e(l)}</tspan>' for j, l in enumerate(lines))
    cx = 20
    chips = []
    for tag in tags:
        c, w = chip(cx, H - 44, tag, t, size=12)
        chips.append(c)
        cx += w + 7
    sw = len(status) * 11.5 * 0.62 + 20 + (10 if status == "in progress" else 0)
    sx = CW - 18 - sw
    dot = (f'<circle cx="{sx+12:.1f}" cy="32" r="4" fill="{t["warm"]}"><animate attributeName="opacity" values="1;0.2;1" dur="1.6s" repeatCount="indefinite"/></circle>'
           if status == "in progress" else "")
    body = f'''
{card(1, 1, CW-2, H-2, t)}
<text x="20" y="38" class="sans" font-size="17.5" font-weight="700" fill="{t['text']}">{e(title)}</text>
<rect x="{sx:.1f}" y="20" width="{sw:.1f}" height="24" rx="12" fill="none" stroke="{t['border']}"/>
{dot}
<text x="{sx + sw/2 + (5 if dot else 0):.1f}" y="36" text-anchor="middle" class="mono" font-size="11.5" fill="{t['muted']}">{status}</text>
<text x="20" y="72" class="sans" font-size="14" fill="{t['muted']}">{txt}</text>
{''.join(chips)}
'''
    return svg(CW, H + PAD, body)


# ---------------------------------------------------------------- stack
STACK = [
    ("GenAI & Agents", ["Claude", "GPT-4o", "Gemini", "Llama 3", "LangChain", "LangGraph", "AutoGen", "RAG", "MCP", "Whisper"]),
    ("Cloud & Infra", ["AWS Bedrock", "Google Cloud", "Vertex AI", "Azure OpenAI", "Terraform", "Docker", "GitHub Actions"]),
    ("Backend & Frontend", ["Python", "TypeScript", "FastAPI", "Flask", "Node.js", "React", "Next.js", "Vite", "WebSockets"]),
    ("Data & ML", ["Databricks", "Delta Lake", "BigQuery", "PostgreSQL", "FAISS", "scikit-learn", "YOLO", "MLX"]),
]


def build_stack(t):
    x0, maxx, size, rowh = 22, W - 20, 13, 36
    y = 18
    out = []
    for r, (cat, items) in enumerate(STACK):
        out.append(f'<text x="22" y="{y+16}" class="sans" font-size="15" font-weight="700" fill="{t["text"]}">{e(cat)}</text>')
        y += 28
        cx = x0
        for it in items:
            w = len(it) * size * 0.62 + 20
            if cx + w > maxx:
                cx = x0
                y += rowh
            c, w = chip(cx, y, it, t, size=size)
            out.append(c)
            cx += w + 9
        y += rowh
        if r < len(STACK) - 1:
            out.append(f'<line x1="22" y1="{y+2}" x2="{W-22}" y2="{y+2}" stroke="{t["border"]}" stroke-dasharray="3 5"/>')
            y += 14
    H = y + 8
    return svg(W, H, card(1, 1, W - 2, H - 2, t) + "".join(out))


# ---------------------------------------------------------------- career (vertical timeline, newest first)
CAREER = [
    ("2026 - now", "AI Engineer", "Akatsuki AI Technologies, Tokyo", "work"),
    ("2025", "Technical Trainer", "Woven by Toyota, Japan", "work"),
    ("2023 - 2025", "MSc Information Technology", "KCGI, Kyoto (moved to Japan)", "study"),
    ("2021 - 2022", "Operations Analyst", "Anytimemoney, India", "work"),
    ("2020 - 2021", "Junior Software Engineer", "Bridcodes Global, India", "work"),
    ("2019 - 2021", "MSc Computer Science", "Christ University, Bengaluru", "study"),
    ("2016 - 2019", "BCA", "St Aloysius College, Mangaluru", "study"),
]


def build_career(t):
    top, step = 40, 58
    lx = 150
    H = top + (len(CAREER) - 1) * step + 46
    y_end = top + (len(CAREER) - 1) * step
    L = y_end - top
    out = [card(1, 1, W - 2, H - 2, t),
           f'<line x1="{lx}" y1="{top}" x2="{lx}" y2="{y_end}" stroke="{t["border"]}" stroke-width="3"/>',
           f'<line x1="{lx}" y1="{top}" x2="{lx}" y2="{y_end}" stroke="{t["accent"]}" stroke-width="3" stroke-dasharray="{L}" stroke-dashoffset="0">'
           f'<animate attributeName="stroke-dashoffset" values="{L};0" dur="2s" fill="freeze"/></line>']
    for i, (yr, role, org, kind) in enumerate(CAREER):
        y = top + i * step
        col = t["teal"] if kind == "work" else t["accent"]
        out.append(f'<g>{fade_in(0.25*i, 0.35)}'
                   f'<text x="{lx-22}" y="{y+5}" text-anchor="end" class="mono" font-size="13" font-weight="700" fill="{col}">{yr}</text>'
                   f'<circle cx="{lx}" cy="{y}" r="8" fill="{t["card"]}" stroke="{col}" stroke-width="3"/>'
                   f'<circle cx="{lx}" cy="{y}" r="3.5" fill="{col}"/>'
                   f'<text x="{lx+24}" y="{y+1}" class="sans" font-size="15.5" font-weight="700" fill="{t["text"]}">{e(role)}</text>'
                   f'<text x="{lx+24}" y="{y+21}" class="sans" font-size="13.5" fill="{t["muted"]}">{e(org)}</text>'
                   f'<text x="{W-24}" y="{y+5}" text-anchor="end" class="mono" font-size="11.5" fill="{t["muted"]}">{kind}</text></g>')
        if i == 0:
            out.append(f'<circle cx="{lx}" cy="{y}" r="8" fill="none" stroke="{col}" stroke-width="2">'
                       f'<animate attributeName="r" values="8;18;8" dur="2.5s" repeatCount="indefinite"/>'
                       f'<animate attributeName="stroke-opacity" values="0.8;0;0.8" dur="2.5s" repeatCount="indefinite"/></circle>')
    return svg(W, H, "".join(out))


# ---------------------------------------------------------------- hobbies
def icon(kind, cx, cy, c):
    def st(w=3):
        return f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
    s = st()
    if kind == "camera":
        return (f'<g {s}><rect x="{cx-26}" y="{cy-16}" width="52" height="36" rx="7"/>'
                f'<path d="M{cx-10},{cy-16} L{cx-5},{cy-24} H{cx+7} L{cx+12},{cy-16}"/>'
                f'<circle cx="{cx}" cy="{cy+2}" r="11"/><circle cx="{cx+18}" cy="{cy-8}" r="1.5" fill="{c}"/></g>'
                f'<circle cx="{cx}" cy="{cy+2}" r="5" fill="{c}"><animate attributeName="r" values="5;2;5" dur="3s" repeatCount="indefinite"/></circle>')
    if kind == "mountain":
        return (f'<g {s}><path d="M{cx-30},{cy+20} L{cx-8},{cy-14} L{cx+4},{cy+4} L{cx+14},{cy-8} L{cx+30},{cy+20} Z"/>'
                f'<path d="M{cx-14},{cy-5} L{cx-8},{cy-1} L{cx-3},{cy-6}"/></g>'
                f'<circle cx="{cx+20}" cy="{cy-20}" r="5" fill="{c}"><animate attributeName="cy" values="{cy-16};{cy-24};{cy-16}" dur="4s" repeatCount="indefinite"/></circle>')
    if kind == "ball":
        pent = f"{cx},{cy-8} {cx+7.6},{cy-2.5} {cx+4.7},{cy+6.5} {cx-4.7},{cy+6.5} {cx-7.6},{cy-2.5}"
        return (f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="8s" repeatCount="indefinite"/>'
                f'<circle cx="{cx}" cy="{cy}" r="24" {s}/>'
                f'<polygon points="{pent}" fill="{c}"/>'
                f'<g {st(2.5)}><path d="M{cx},{cy-8} V{cy-24} M{cx+7.6},{cy-2.5} L{cx+22},{cy-7} M{cx+4.7},{cy+6.5} L{cx+13},{cy+19} '
                f'M{cx-4.7},{cy+6.5} L{cx-13},{cy+19} M{cx-7.6},{cy-2.5} L{cx-22},{cy-7}"/></g></g>')
    if kind == "plane":
        plane = ("M0,-12 L2,-4 L12,2 L12,4.5 L2,1.5 L1.5,8 L4.5,10.5 L4.5,12 L0,11 "
                 "L-4.5,12 L-4.5,10.5 L-1.5,8 L-2,1.5 L-12,4.5 L-12,2 L-2,-4 Z")
        return (f'<circle cx="{cx}" cy="{cy}" r="15" {s}/>'
                f'<path d="M{cx-15},{cy} H{cx+15} M{cx},{cy-15} C{cx-9},{cy-6} {cx-9},{cy+6} {cx},{cy+15} '
                f'M{cx},{cy-15} C{cx+9},{cy-6} {cx+9},{cy+6} {cx},{cy+15}" {st(2)}/>'
                f'<circle cx="{cx}" cy="{cy}" r="27" {st(1.5)} stroke-dasharray="3 5"/>'
                f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="9s" repeatCount="indefinite"/>'
                f'<path transform="translate({cx},{cy-27}) rotate(90) scale(0.85)" d="{plane}" fill="{c}"/></g>')
    return ""


def build_hobbies(t):
    H = 132
    items = [("camera", "Photography"), ("mountain", "Hiking"), ("ball", "Football"), ("plane", "Travel")]
    gap = 12
    cw = (W - 2 - 3 * gap) / 4
    out = []
    for i, (k, title) in enumerate(items):
        x = 1 + i * (cw + gap)
        col = [t["accent"], t["teal"], t["warm"], t["accent"]][i]
        out.append(card(f"{x:.1f}", 1, f"{cw:.1f}", H - 2, t) +
                   icon(k, x + cw / 2, 52, col) +
                   f'<text x="{x+cw/2:.1f}" y="110" text-anchor="middle" class="sans" font-size="16" font-weight="700" fill="{t["text"]}">{title}</text>')
    return svg(W, H, "".join(out))


def main():
    with open(os.path.join(ROOT, "assets", "avatar.svg"), "w") as f:
        f.write(build_avatar())
    heads = {
        "h1": ("01", "whoami", "who I am and what I work on"),
        "h2": ("02", "work projects", "built at work, code is private"),
        "h3": ("03", "personal projects", "things I build on my own time"),
        "h4": ("04", "stack", "tools I work with"),
        "h5": ("05", "career", "India to Japan, data to AI"),
        "h6": ("06", "off the clock", "outside work"),
    }
    for name, t in THEMES.items():
        d = os.path.join(ROOT, "assets", name)
        for old in os.listdir(d):
            if old.endswith(".svg"):
                os.remove(os.path.join(d, old))
        files = {
            "header.svg": build_header(t),
            "whoami.svg": build_whoami(t),
            "work.svg": build_work(t),
            "stack.svg": build_stack(t),
            "career.svg": build_career(t),
            "hobbies.svg": build_hobbies(t),
        }
        files["internal.svg"] = build_internal(t)
        for k in PROJECTS:
            files[f"project-{k}.svg"] = build_project(t, k, wide=(k == "pharmaiq"))
        for k, (n, ti, sub) in heads.items():
            files[f"{k}.svg"] = build_heading(t, n, ti, sub)
        for fn, content in files.items():
            with open(os.path.join(d, fn), "w") as f:
                f.write(content)
    print("ok")


if __name__ == "__main__":
    main()
