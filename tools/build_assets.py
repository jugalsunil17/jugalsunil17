"""Generate the light/dark SVG assets for the GitHub profile README.

Run:  python3 tools/build_assets.py
Writes assets/light/*.svg, assets/dark/*.svg and assets/avatar.svg.
All SVGs are drawn on an 840px wide canvas, close to GitHub's README column,
so font sizes here are roughly the sizes people actually see.
"""
import os
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
    """Half human / half robot face, drawn on a 512x512 canvas."""
    seam = "256,60 263,120 251,175 263,230 250,290 262,345 252,400 260,460 256,512"
    left_clip = f"0,0 {seam} 0,512"
    right_clip = f"512,0 {seam} 512,512"
    head = ("M256,112 C330,112 382,160 384,240 C386,300 372,350 340,392 "
            "C315,422 288,436 256,436 C224,436 197,422 172,392 C140,350 126,300 128,240 "
            "C130,160 182,112 256,112 Z")
    g = f'''
<defs>
  <radialGradient id="{uid}bg" cx="35%" cy="30%" r="80%">
    <stop offset="0" stop-color="#1e2a5a"/><stop offset="0.6" stop-color="#0f1b3d"/><stop offset="1" stop-color="#071022"/>
  </radialGradient>
  <linearGradient id="{uid}skin" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#d9a074"/><stop offset="1" stop-color="#b97a52"/>
  </linearGradient>
  <linearGradient id="{uid}metal" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#e3e8ee"/><stop offset="0.55" stop-color="#a9b3bf"/><stop offset="1" stop-color="#6b7684"/>
  </linearGradient>
  <radialGradient id="{uid}lens" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#ffffff"/><stop offset="0.25" stop-color="#7ff5e6"/><stop offset="0.7" stop-color="#14b8a6"/><stop offset="1" stop-color="#0b4f4a"/>
  </radialGradient>
  <filter id="{uid}glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="{uid}L"><polygon points="{left_clip}"/></clipPath>
  <clipPath id="{uid}R"><polygon points="{right_clip}"/></clipPath>
  <clipPath id="{uid}C"><circle cx="256" cy="256" r="256"/></clipPath>
</defs>
<g transform="translate({cx - 256*scale},{cy - 256*scale}) scale({scale})">
<g {'clip-path="url(#' + uid + 'C)"' if clip_circle else ''}>
  <rect width="512" height="512" fill="url(#{uid}bg)"/>
  <g stroke="#2dd4bf" stroke-opacity="0.10" stroke-width="1">
    <path d="M0,96 H512 M0,192 H512 M0,288 H512 M0,384 H512 M96,0 V512 M192,0 V512 M320,0 V512 M416,0 V512"/>
  </g>
  <circle cx="256" cy="256" r="228" fill="none" stroke="#818cf8" stroke-opacity="0.25" stroke-width="2" stroke-dasharray="4 10">
    <animateTransform attributeName="transform" type="rotate" from="0 256 256" to="360 256 256" dur="60s" repeatCount="indefinite"/>
  </circle>

  <!-- ===== HUMAN (left) ===== -->
  <g clip-path="url(#{uid}L)">
    <path d="M150,512 C150,470 190,448 256,446 L256,512 Z" fill="#1f3864"/>
    <path d="M60,512 C66,466 120,446 200,440 L256,446 L256,512 Z" fill="#1f3864"/>
    <path d="M196,440 C214,470 238,478 256,478 L256,446 Z" fill="#162a4d"/>
    <rect x="212" y="392" width="60" height="70" fill="#b97a52"/>
    <ellipse cx="131" cy="276" rx="15" ry="27" fill="#c98b62"/>
    <path d="{head}" fill="url(#{uid}skin)"/>
    <path d="M116,268 C100,170 150,90 252,84 C292,82 304,104 300,120 C270,112 240,118 214,132 C186,148 164,170 152,198 C146,214 142,232 141,248 C139,258 136,266 132,274 C126,274 120,272 116,268 Z" fill="#17120f"/>
    <g stroke="#3a2c22" stroke-width="3" fill="none" stroke-linecap="round"><path d="M132,200 C140,160 170,128 210,114"/><path d="M178,104 C200,96 226,94 248,96"/><path d="M124,236 C124,214 128,196 136,182"/></g>
    <path d="M150,150 C170,110 210,96 250,98" stroke="#3a2c22" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M172,240 Q200,226 234,236" stroke="#1d1410" stroke-width="8" fill="none" stroke-linecap="round"/>
    <path d="M178,264 Q206,247 234,264 Q206,279 178,264 Z" fill="#fbf7f2"/>
    <circle cx="207" cy="263" r="10" fill="#3b2416"/>
    <circle cx="207" cy="263" r="4.5" fill="#0b0705"/>
    <circle cx="210" cy="259" r="2.6" fill="#ffffff"/>
    <path d="M178,264 Q206,247 234,264" stroke="#1d1410" stroke-width="2.5" fill="none"/>
    <path d="M249,272 L238,318 Q246,326 258,322" stroke="#8f5a3c" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M206,356 Q232,374 258,366" stroke="#7a3e2e" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M168,330 C176,380 210,420 256,424" stroke="#9a6545" stroke-opacity="0.35" stroke-width="10" fill="none"/>
  </g>

  <!-- ===== ROBOT (right) ===== -->
  <g clip-path="url(#{uid}R)">
    <path d="M256,446 C330,448 380,466 452,512 L256,512 Z" fill="#3d4652"/>
    <path d="M300,470 L420,500 M290,490 L380,512" stroke="#5b6573" stroke-width="3"/>
    <rect x="240" y="392" width="62" height="74" fill="#59636e"/>
    <g stroke="#3d4652" stroke-width="3"><path d="M240,410 H302 M240,426 H302 M240,442 H302"/></g>
    <circle cx="393" cy="276" r="22" fill="url(#{uid}metal)" stroke="#4b5563" stroke-width="2"/>
    <circle cx="395" cy="276" r="10" fill="none" stroke="#2dd4bf" stroke-width="3" filter="url(#{uid}glow)"/>
    <path d="{head}" fill="url(#{uid}metal)"/>
    <path d="M256,112 C330,112 382,160 384,240" fill="none" stroke="#ffffff" stroke-opacity="0.55" stroke-width="3"/>
    <g fill="none" stroke="#5b6573" stroke-width="2.2">
      <path d="M256,196 H338 L372,222"/>
      <path d="M256,300 H292 L312,318 H368"/>
      <path d="M256,388 H300 L330,410"/>
      <path d="M350,150 L340,196"/>
    </g>
    <path d="M276,236 L340,231" stroke="#3d4652" stroke-width="8" stroke-linecap="round"/>
    <circle cx="307" cy="264" r="25" fill="#0d1117" stroke="#4b5563" stroke-width="3"/>
    <circle cx="307" cy="264" r="15" fill="url(#{uid}lens)" filter="url(#{uid}glow)">
      <animate attributeName="r" values="14;16;14" dur="3s" repeatCount="indefinite"/>
    </circle>
    <circle cx="303" cy="260" r="3.5" fill="#ffffff"/>
    <g stroke="#3d4652" stroke-width="3" stroke-linecap="round">
      <path d="M306,330 H348 M310,340 H346 M316,350 H342"/>
    </g>
    <rect x="256" y="355" width="46" height="18" rx="4" fill="#1f2630"/>
    <g stroke="#2dd4bf" stroke-width="2.5" stroke-linecap="round" opacity="0.9">
      <path d="M266,359 V369 M276,359 V369 M286,359 V369 M296,359 V369"/>
      <animate attributeName="opacity" values="0.4;1;0.4" dur="2.4s" repeatCount="indefinite"/>
    </g>
    <g fill="none" stroke="#2dd4bf" stroke-width="2.5" filter="url(#{uid}glow)">
      <path d="M256,160 H296 L314,142 H336"/>
      <path d="M256,410 H286 L300,396"/>
    </g>
    <g fill="#2dd4bf"><circle cx="338" cy="142" r="4"/><circle cx="302" cy="394" r="4"/></g>
    <g fill="#4b5563"><circle cx="362" cy="214" r="4"/><circle cx="368" cy="302" r="4"/><circle cx="334" cy="388" r="4"/><circle cx="296" cy="130" r="4"/></g>
  </g>

  <!-- seam -->
  <polyline points="256,92 263,120 251,175 263,230 250,290 262,345 252,400 260,446" fill="none" stroke="#2dd4bf" stroke-width="3" stroke-linejoin="round" filter="url(#{uid}glow)">
    <animate attributeName="stroke-opacity" values="0.55;1;0.55" dur="3s" repeatCount="indefinite"/>
  </polyline>
</g>
<circle cx="256" cy="256" r="244" fill="none" stroke="#818cf8" stroke-opacity="0.55" stroke-width="4"/>
</g>
'''
    return g


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
}


def build_project(t, key):
    title, status, desc, tags = PROJECTS[key]
    CW, H, PAD = 412, 196, 10  # PAD: transparent space under each card so rows do not touch
    lines = textwrap.wrap(desc, 48, break_on_hyphens=False)
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
        for k in PROJECTS:
            files[f"project-{k}.svg"] = build_project(t, k)
        for k, (n, ti, sub) in heads.items():
            files[f"{k}.svg"] = build_heading(t, n, ti, sub)
        for fn, content in files.items():
            with open(os.path.join(d, fn), "w") as f:
                f.write(content)
    print("ok")


if __name__ == "__main__":
    main()
