#!/usr/bin/env python3
"""
Hardened Builds LLC — static site generator.

Single source of truth for all site content and markup. Emits dependency-free
static HTML/CSS/JS into ./dist, portable to any static host. No runtime
dependencies; standard library only.
"""

import html
import math
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")

COMPANY = "Hardened Builds LLC"
TAGLINE = "Application Development & AI Engineering"

# ---------------------------------------------------------------------------
# Service data — the single source of truth.
#   number  : sequence position in the lifecycle
#   name    : display name
#   slug    : URL slug (page file name)
#   summary : one-sentence description shown beneath the node
#   bubble  : short specifics surfaced on hover / click in the process diagram
#   intro   : opening paragraph on the service page
#   delivers: formal list of deliverables and activities for the phase
# ---------------------------------------------------------------------------

SERVICES = [
    {
        "number": 1,
        "name": "Business Requirements",
        "slug": "business-requirements",
        "summary": "Elicitation and formalization of stakeholder objectives.",
        "bubble": [
            "Structured stakeholder interviews and workshops",
            "Functional and non-functional requirements documentation",
            "Defined, testable acceptance criteria",
            "Requirements traceability matrix",
        ],
        "intro": (
            "The Business Requirements phase establishes a precise and shared "
            "understanding of the objectives the solution is required to satisfy. "
            "Hardened Builds LLC conducts structured elicitation with stakeholders "
            "and translates business intent into unambiguous, verifiable requirements "
            "that govern every subsequent phase of the engagement."
        ),
        "delivers": [
            "Structured stakeholder interviews and facilitated requirements workshops.",
            "A documented set of functional and non-functional requirements.",
            "Defined, measurable, and testable acceptance criteria for each requirement.",
            "A requirements traceability matrix linking requirements to their origin and verification.",
            "Identification of regulatory, security, and compliance constraints at the outset.",
        ],
    },
    {
        "number": 2,
        "name": "Solution Architecture",
        "slug": "solution-architecture",
        "summary": "Definition of system structure, technology, and security strategy.",
        "bubble": [
            "Architecture and component diagrams",
            "Technology selection and integration strategy",
            "Security and compliance design",
            "Token-efficient artificial intelligence design",
        ],
        "intro": (
            "The Solution Architecture phase defines the structural and technical "
            "strategy of the system. Hardened Builds LLC designs architectures that "
            "are secure by default, maintainable over their operational life, and "
            "portable across hosting environments. Where artificial intelligence "
            "components are present, the architecture is designed to minimize model "
            "token consumption while preserving durable and consistent results."
        ),
        "delivers": [
            "Architecture, component, and data-flow diagrams.",
            "Technology selection with documented justification and trade-off analysis.",
            "Security architecture incorporating default-deny authorization and defense in depth.",
            "Integration strategy for internal systems and third-party services.",
            (
                "Token-minimization strategy for artificial intelligence components, "
                "favoring retrieval-augmented generation with vector search, response "
                "caching, deterministic short-circuits, schema-constrained model calls, "
                "and routing to smaller models in preference to transmitting large context."
            ),
        ],
    },
    {
        "number": 3,
        "name": "AI/App Design",
        "slug": "ai-app-design",
        "summary": "Detailed design of interfaces, data, and model interactions.",
        "bubble": [
            "Interface and interaction design",
            "Data modeling and schema definition",
            "Model and prompt design specifications",
            "Detailed design documentation",
        ],
        "intro": (
            "The Design phase converts the approved architecture into detailed, "
            "implementable specifications. Hardened Builds LLC produces designs for "
            "user interfaces, data structures, and, where applicable, model and "
            "prompt behavior, each specified with sufficient precision to govern "
            "implementation without ambiguity."
        ),
        "delivers": [
            "User interface and interaction design specifications.",
            "Data models, schema definitions, and validation rules.",
            "Model interaction and prompt design specifications for artificial intelligence features.",
            "Interface contracts for application programming interfaces and integrations.",
            "Detailed design documentation sufficient to direct implementation.",
        ],
    },
    {
        "number": 4,
        "name": "AI/App Development",
        "slug": "ai-app-development",
        "summary": "Implementation of the approved design.",
        "bubble": [
            "Secure coding practices applied throughout",
            "Version control and peer code review",
            "Automated testing during development",
            "Continuous integration of changes",
        ],
        "intro": (
            "The Development phase implements the approved design. Hardened Builds LLC "
            "applies secure coding practices, enforced version control, and peer review "
            "from the first commit. Authentication, authorization, and data protection "
            "controls are implemented as foundational properties of the system rather "
            "than as subsequent additions."
        ),
        "delivers": [
            "Implementation of the solution in accordance with the approved design.",
            "Secure coding practices enforced throughout the development process.",
            "Version control with mandatory peer code review prior to integration.",
            "Automated unit and integration testing developed alongside the implementation.",
            "Continuous integration, with each change merged, verified, and deployed to a testable endpoint.",
        ],
    },
    {
        "number": 5,
        "name": "QA Testing",
        "slug": "qa-testing",
        "summary": "Independent verification of quality and correctness.",
        "bubble": [
            "Documented test planning and strategy",
            "Functional and regression testing",
            "Security and performance verification",
            "Structured defect management",
        ],
        "intro": (
            "The Quality Assurance phase provides independent verification that the "
            "implemented solution satisfies its requirements. Hardened Builds LLC "
            "executes documented test plans encompassing functional correctness, "
            "regression, security, and performance, and manages identified defects "
            "through a structured resolution process."
        ),
        "delivers": [
            "A documented test plan and test strategy derived from the defined requirements.",
            "Functional testing against acceptance criteria.",
            "Regression testing to confirm that existing functionality remains intact.",
            "Security and performance verification appropriate to the system.",
            "Structured defect identification, prioritization, tracking, and resolution.",
        ],
    },
    {
        "number": 6,
        "name": "UAT Testing Support",
        "slug": "uat-testing-support",
        "summary": "Support of user acceptance activities.",
        "bubble": [
            "User acceptance test planning",
            "Preparation of test scenarios and data",
            "Defect triage during acceptance",
            "Facilitation of formal sign-off",
        ],
        "intro": (
            "The User Acceptance Testing Support phase assists stakeholders in "
            "verifying that the solution satisfies business objectives under realistic "
            "conditions. Hardened Builds LLC prepares acceptance materials, supports "
            "users throughout execution, and facilitates the formal acceptance decision."
        ),
        "delivers": [
            "User acceptance test planning aligned to business objectives.",
            "Preparation of acceptance test scenarios and representative test data.",
            "Direct support to business users throughout the acceptance period.",
            "Triage and resolution coordination for defects identified during acceptance.",
            "Facilitation of formal, documented user acceptance sign-off.",
        ],
    },
    {
        "number": 7,
        "name": "Deployment Support",
        "slug": "deployment-support",
        "summary": "Controlled release to the production environment.",
        "bubble": [
            "Documented release planning",
            "Controlled deployment execution",
            "Defined rollback procedures",
            "Post-release verification",
        ],
        "intro": (
            "The Deployment Support phase governs the controlled release of the "
            "solution to the production environment. Hardened Builds LLC plans and "
            "executes deployment through established, repeatable procedures, with "
            "defined rollback provisions and verification of the released system."
        ),
        "delivers": [
            "A documented release and deployment plan.",
            "Controlled execution of the deployment through established procedures.",
            "Defined and tested rollback procedures to address release failure.",
            "Verification that the deployed system operates as intended.",
            "Coordination with stakeholders throughout the release window.",
        ],
    },
    {
        "number": 8,
        "name": "Post-deployment Testing Support",
        "slug": "post-deployment-testing-support",
        "summary": "Verification of system behavior in production.",
        "bubble": [
            "Production smoke testing",
            "Validation of monitoring and alerting",
            "Performance verification under live load",
            "Resolution of production-identified issues",
        ],
        "intro": (
            "The Post-deployment Testing Support phase verifies that the solution "
            "operates correctly within the production environment following release. "
            "Hardened Builds LLC confirms system behavior, validates monitoring, and "
            "coordinates resolution of any issues observed under live conditions."
        ),
        "delivers": [
            "Smoke testing of critical functionality in the production environment.",
            "Validation that monitoring, logging, and alerting operate as designed.",
            "Verification of system performance under live operating load.",
            "Identification and coordinated resolution of issues observed in production.",
        ],
    },
    {
        "number": 9,
        "name": "Post-deployment HyperCare",
        "slug": "post-deployment-hypercare",
        "summary": "Heightened support during the stabilization period.",
        "bubble": [
            "Dedicated response team",
            "Priority incident management",
            "Expedited defect resolution",
            "Regular stabilization reporting",
        ],
        "intro": (
            "The HyperCare phase provides heightened, time-bounded support during the "
            "critical period immediately following deployment. Hardened Builds LLC "
            "assigns a dedicated response team to ensure rapid identification and "
            "resolution of issues while the solution stabilizes in production."
        ),
        "delivers": [
            "A dedicated response team for the defined stabilization period.",
            "Priority incident management with expedited response commitments.",
            "Expedited resolution of defects affecting production operation.",
            "Regular reporting on system stability and outstanding items.",
            "A documented transition from HyperCare to ongoing support.",
        ],
    },
    {
        "number": 10,
        "name": "Post-deployment Support",
        "slug": "post-deployment-support",
        "summary": "Ongoing maintenance and operational support.",
        "bubble": [
            "Ongoing corrective maintenance",
            "Enhancements and change management",
            "Service-level-based support",
            "Continuous monitoring and reporting",
        ],
        "intro": (
            "The Post-deployment Support phase sustains the solution over its "
            "operational life. Hardened Builds LLC provides corrective maintenance, "
            "managed enhancements, and service-level-based support, with continuous "
            "monitoring to preserve performance, security, and availability."
        ),
        "delivers": [
            "Ongoing corrective maintenance to address defects and operational issues.",
            "Managed enhancements and change control for evolving requirements.",
            "Support governed by defined service-level agreements.",
            "Continuous monitoring of performance, security, and availability.",
            "Periodic reporting and review of system health and support activity.",
        ],
    },
]


# ---------------------------------------------------------------------------
# Radial SDLC wheel (self-contained SVG; inlined Lucide icons, ISC licensed)
# ---------------------------------------------------------------------------

WHEEL_ICONS = {
    "clipboard-list": "<rect width=\"8\" height=\"4\" x=\"8\" y=\"2\" rx=\"1\" ry=\"1\" /> <path d=\"M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2\" /> <path d=\"M12 11h4\" /> <path d=\"M12 16h4\" /> <path d=\"M8 11h.01\" /> <path d=\"M8 16h.01\" />",
    "network": "<rect x=\"16\" y=\"16\" width=\"6\" height=\"6\" rx=\"1\" /> <rect x=\"2\" y=\"16\" width=\"6\" height=\"6\" rx=\"1\" /> <rect x=\"9\" y=\"2\" width=\"6\" height=\"6\" rx=\"1\" /> <path d=\"M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3\" /> <path d=\"M12 12V8\" />",
    "panels-top-left": "<rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\" /> <path d=\"M3 9h18\" /> <path d=\"M9 21V9\" />",
    "code-xml": "<path d=\"m18 16 4-4-4-4\" /> <path d=\"m6 8-4 4 4 4\" /> <path d=\"m14.5 4-5 16\" />",
    "test-tubes": "<path d=\"M9 2v17.5A2.5 2.5 0 0 1 6.5 22A2.5 2.5 0 0 1 4 19.5V2\" /> <path d=\"M20 2v17.5a2.5 2.5 0 0 1-2.5 2.5a2.5 2.5 0 0 1-2.5-2.5V2\" /> <path d=\"M3 2h7\" /> <path d=\"M14 2h7\" /> <path d=\"M9 16H4\" /> <path d=\"M20 16h-5\" />",
    "user-check": "<path d=\"m16 11 2 2 4-4\" /> <path d=\"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2\" /> <circle cx=\"9\" cy=\"7\" r=\"4\" />",
    "package-check": "<path d=\"M12 22V12\" /> <path d=\"m16 17 2 2 4-4\" /> <path d=\"M21 11.127V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.729l7 4a2 2 0 0 0 2 .001l1.32-.753\" /> <path d=\"M3.29 7 12 12l8.71-5\" /> <path d=\"m7.5 4.27 8.997 5.148\" />",
    "scan-check": "<path d=\"m8 11 2 2 4-4\" /> <circle cx=\"11\" cy=\"11\" r=\"8\" /> <path d=\"m21 21-4.3-4.3\" />",
    "activity": "<path d=\"M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2\" />",
    "headset": "<path d=\"M3 11h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5Zm0 0a9 9 0 1 1 18 0m0 0v5a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3Z\" /> <path d=\"M21 16v2a4 4 0 0 1-4 4h-5\" />",
}

# (number, short label, lucide icon key, service slug, detail description)
WHEEL_PHASES = [
    ("01", "Requirements",        "clipboard-list",  "business-requirements",
     "Business requirements gathering: define outcomes, scope, and acceptance criteria."),
    ("02", "Architecture",        "network",         "solution-architecture",
     "Solutions architecture: define the solution, data flows, integrations, and security."),
    ("03", "App design",          "panels-top-left", "ai-app-design",
     "App design: define user journeys, interfaces, data models, and components."),
    ("04", "Development",         "code-xml",        "ai-app-development",
     "App development: implement features, APIs, integrations, and build pipelines."),
    ("05", "App testing",         "test-tubes",      "qa-testing",
     "App testing: verify functionality, integrations, security, and performance."),
    ("06", "UAT support",         "user-check",      "uat-testing-support",
     "UAT support: help business users validate agreed acceptance criteria."),
    ("07", "Pre-deploy",          "package-check",   "deployment-support",
     "Pre-deploy support: prepare release readiness, rollback, and handover."),
    ("08", "Post-deploy testing", "scan-check",      "post-deployment-testing-support",
     "Post-deploy testing: validate production journeys and integrations."),
    ("09", "Hypercare",           "activity",        "post-deployment-hypercare",
     "Post-deploy hypercare: enhanced monitoring, rapid triage, and stabilization."),
    ("10", "Ongoing support",     "headset",         "post-deployment-support",
     "Post-deploy support: ongoing incident management, maintenance, and updates."),
]

_W_NAVY = "#01234e"; _W_BLUE = "#0072fe"; _W_SEG = "#dceafe"; _W_SEGINK = "#1b3b63"
_W_LABEL = "#33425a"; _W_HUB = "#eef3f9"; _W_HUBLINE = "#d7e0ec"
_W_CX, _W_CY = 430.0, 340.0
_W_R0, _W_R1 = 128.0, 212.0
_W_RM = (_W_R0 + _W_R1) / 2
_W_GAP = 1.6
_W_POINT = 5.0
_W_LBLR = 250.0
_W_WIDTH, _W_HEIGHT = 860, 720


def _w_pol(r, deg):
    a = math.radians(deg)
    return (_W_CX + r * math.cos(a), _W_CY + r * math.sin(a))


def _w_seg_path(a0, a1):
    g = _W_GAP / 2
    a0s, a1s = a0 + g, a1 - g
    b = _w_pol(_W_R1, a0s); c = _w_pol(_W_R1, a1s)
    d = _w_pol(_W_RM, a1s + _W_POINT); e = _w_pol(_W_R0, a1s)
    a_ = _w_pol(_W_R0, a0s); n = _w_pol(_W_RM, a0s - _W_POINT)
    f = lambda p: f"{p[0]:.2f} {p[1]:.2f}"
    return (f"M {f(b)} A {_W_R1:.1f} {_W_R1:.1f} 0 0 1 {f(c)} L {f(d)} L {f(e)} "
            f"A {_W_R0:.1f} {_W_R0:.1f} 0 0 0 {f(a_)} L {f(n)} Z")


def _w_icon(name, x, y, size, color, cls=""):
    inner = WHEEL_ICONS[name]
    s = size / 24.0
    c = f' class="{cls}"' if cls else ""
    return (f'<g{c} transform="translate({x - size/2:.2f},{y - size/2:.2f}) scale({s:.3f})" '
            f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{inner}</g>')


def build_wheel(interactive=True, active=0, prefix=""):
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_W_WIDTH} {_W_HEIGHT}" '
        f'font-family="Calibri, Segoe UI, sans-serif" '
        f'{"class=\"wheel__svg\" " if interactive else ""}role="img" '
        f'aria-label="Hardened Builds LLC application development lifecycle: ten sequential phases">'
    ]
    if not interactive:
        p.append(f'<rect width="{_W_WIDTH}" height="{_W_HEIGHT}" fill="#ffffff"/>')
    for k, (num, label, icon, slug, tip) in enumerate(WHEEL_PHASES):
        a0 = -90 + k * 36; a1 = a0 + 36; mid = a0 + 18
        d = _w_seg_path(a0, a1)
        is_active = (k == active) and not interactive
        fill = _W_BLUE if is_active else _W_SEG
        ink = "#ffffff" if is_active else _W_SEGINK
        nx, ny = _w_pol(_W_RM + 26, mid)
        numx, numy = _w_pol(_W_RM - 14, mid)
        lx, ly = _w_pol(_W_LBLR, mid)
        anchor = "middle"
        if lx > _W_CX + 20: anchor = "start"
        elif lx < _W_CX - 20: anchor = "end"
        words = label.split()
        if len(label) > 11 and len(words) > 1:
            cut = 1 if words[0] in ("Post-deploy", "Ongoing", "UAT", "App") and len(words) == 2 else (len(words) + 1) // 2
            lines = [" ".join(words[:cut]), " ".join(words[cut:])]
        else:
            lines = [label]
        ly0 = ly - (len(lines) - 1) * 9
        tspans = "".join(
            f'<tspan x="{lx:.1f}" y="{ly0 + i*18:.1f}">{html.escape(ln)}</tspan>'
            for i, ln in enumerate(lines)
        )
        shape = (
            f'<path class="wseg__shape" d="{d}" fill="{fill}" stroke="#ffffff" stroke-width="2"/>'
            f'{_w_icon(icon, nx, ny, 22, ink, cls="wseg__icon")}'
            f'<text class="wseg__num" x="{numx:.1f}" y="{numy+5:.1f}" text-anchor="middle" '
            f'font-size="17" font-weight="700" fill="{ink}">{num}</text>'
        )
        lbl = (f'<text class="wseg__label" text-anchor="{anchor}" font-size="15.5" '
               f'font-weight="600" fill="{_W_LABEL}">{tspans}</text>')
        if interactive:
            p.append(
                f'<a class="wseg" href="{prefix}services/{slug}.html" data-phase="{k}" '
                f'data-num="{num}" data-label="{html.escape(label, quote=True)}" '
                f'data-tip="{html.escape(tip, quote=True)}" '
                f'aria-label="Phase {num}, {html.escape(label, quote=True)}: {html.escape(tip, quote=True)}">'
                f'{shape}{lbl}</a>'
            )
        else:
            p.append(f'<g>{shape}{lbl}</g>')
    p.append(f'<circle cx="{_W_CX}" cy="{_W_CY}" r="{_W_R0-14:.1f}" fill="{_W_HUB}" stroke="{_W_HUBLINE}" stroke-width="1.5"/>')
    p.append(f'<text x="{_W_CX}" y="{_W_CY-24:.1f}" text-anchor="middle" font-size="12.5" font-weight="700" letter-spacing="1.5" fill="{_W_LABEL}">HARDENED BUILDS</text>')
    p.append(f'<text x="{_W_CX}" y="{_W_CY+8:.1f}" text-anchor="middle" font-size="34" font-weight="700" fill="{_W_NAVY}">SDLC</text>')
    p.append(f'<text x="{_W_CX}" y="{_W_CY+34:.1f}" text-anchor="middle" font-size="14" fill="{_W_LABEL}">Application lifecycle</text>')
    p.append("</svg>")
    return "\n".join(p)


# ---------------------------------------------------------------------------
# Shared markup helpers
# ---------------------------------------------------------------------------

CSP = (
    "default-src 'self'; "
    "img-src 'self' data:; "
    "style-src 'self'; "
    "script-src 'self'; "
    "font-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'none'"
)


def e(text):
    return html.escape(text, quote=True)


def head(title, description, depth):
    """depth: number of directories below site root (0 for index)."""
    prefix = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="description" content="{e(description)}">
<title>{e(title)}</title>
<link rel="stylesheet" href="{prefix}styles.css">
<link rel="icon" type="image/png" href="{prefix}assets/favicon.png">
<link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png">
</head>
<body>"""


def header(depth):
    prefix = "../" * depth
    nav_links = "".join(
        f'<li><a href="{prefix}services/{s["slug"]}.html">{e(s["name"])}</a></li>'
        for s in SERVICES
    )
    return f"""
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="{prefix}index.html" aria-label="Hardened Builds LLC — home">
      <img class="brand__mark" src="{prefix}assets/logo-mark.png" width="44" height="20" alt="" aria-hidden="true">
      <span class="brand__name">Hardened Builds<span class="brand__llc"> LLC</span></span>
    </a>
    <nav class="site-nav" aria-label="Primary">
      <button class="nav-toggle" aria-expanded="false" aria-controls="primary-menu">Menu</button>
      <ul id="primary-menu" class="nav-menu">
        <li><a href="{prefix}index.html">Home</a></li>
        <li class="has-sub">
          <a href="{prefix}index.html#services">Services</a>
          <ul class="sub-menu">{nav_links}</ul>
        </li>
        <li><a href="{prefix}index.html#process">Process</a></li>
        <li><a href="{prefix}index.html#contact">Contact</a></li>
      </ul>
    </nav>
  </div>
</header>"""


def footer(depth):
    prefix = "../" * depth
    cols = ""
    half = (len(SERVICES) + 1) // 2
    for group in (SERVICES[:half], SERVICES[half:]):
        items = "".join(
            f'<li><a href="{prefix}services/{s["slug"]}.html">{e(s["name"])}</a></li>'
            for s in group
        )
        cols += f'<ul class="footer__list">{items}</ul>'
    return f"""
<footer class="site-footer" id="contact">
  <div class="container footer__inner">
    <div class="footer__brand">
      <span class="footer__wordmark">Hardened Builds<span class="brand__llc"> LLC</span></span>
      <p class="footer__tagline">Application development and artificial intelligence engineering across the complete software development lifecycle.</p>
      <p class="footer__contact">Correspondence: <a href="mailto:contact@hardenedbuilds.example">contact@hardenedbuilds.example</a></p>
    </div>
    <nav class="footer__nav" aria-label="Services">
      <h2 class="footer__heading">Services</h2>
      <div class="footer__cols">{cols}</div>
    </nav>
  </div>
  <div class="container footer__legal">
    <p>&copy; 2026 Hardened Builds LLC. All rights reserved.</p>
  </div>
</footer>
<script src="{prefix}site.js"></script>
</body>
</html>"""


def process_diagram(depth):
    """Interactive radial SDLC wheel: self-contained SVG, hover/focus + click to service."""
    prefix = "../" * depth
    wheel = build_wheel(interactive=True, prefix=prefix)
    first = WHEEL_PHASES[0]
    return f"""
<section class="process" id="process" aria-labelledby="process-heading">
  <div class="container">
    <h2 id="process-heading">Application Development Lifecycle</h2>
    <p class="section-lead">
      Hardened Builds LLC delivers the complete application development lifecycle as a
      governed, sequential process. Position the pointer over a phase, or move to it by
      keyboard, to review its activities. Select a phase to open its detailed description.
    </p>
    <div class="wheel">
      <div class="wheel__diagram">{wheel}</div>
      <p class="wheel__detail" id="wheel-detail" aria-live="polite" aria-atomic="true">
        <span class="wheel__detail-name">{e(first[0])} &middot; {e(first[1])}</span>
        <span class="wheel__detail-text"> &mdash; {e(first[4])}</span>
      </p>
    </div>
    <p class="process__hint">Each phase links to a dedicated service page.</p>
    <p class="process__download">
      <a href="{prefix}assets/process-overview.svg" download>Download the lifecycle diagram (SVG)</a>
    </p>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def build_index():
    cards = ""
    for s in SERVICES:
        cards += f"""
      <li class="svc-card">
        <a href="services/{s['slug']}.html">
          <span class="svc-card__num">{s['number']:02d}</span>
          <span class="svc-card__name">{e(s['name'])}</span>
          <span class="svc-card__summary">{e(s['summary'])}</span>
        </a>
      </li>"""

    body = f"""
<main id="main">
  <section class="hero" aria-labelledby="hero-heading">
    <div class="container hero__inner">
      <img class="hero__logo" src="assets/logo-full.png" alt="Hardened Builds LLC" width="620" height="275">
      <p class="hero__eyebrow">Secure by Default. Durable by Design.</p>
      <h1 id="hero-heading">Application Development &amp; Artificial Intelligence Engineering</h1>
      <p class="hero__sub">
        Hardened Builds LLC designs, develops, and supports artificial intelligence and
        application solutions across the complete software development lifecycle.
        Security, maintainability, and portability are foundational properties of every
        engagement rather than subsequent considerations.
      </p>
      <p class="hero__actions">
        <a class="btn btn--primary" href="#process">Review Our Process</a>
        <a class="btn btn--ghost" href="#services">View Services</a>
      </p>
    </div>
  </section>

  {process_diagram(0)}

  <section class="services" id="services" aria-labelledby="services-heading">
    <div class="container">
      <h2 id="services-heading">Services</h2>
      <p class="section-lead">
        The following services constitute the complete lifecycle delivered by
        Hardened Builds LLC. Each service is available as part of a full engagement
        or as a discrete contribution to an existing program.
      </p>
      <ul class="svc-grid">{cards}
      </ul>
    </div>
  </section>

  <section class="principles" aria-labelledby="principles-heading">
    <div class="container">
      <h2 id="principles-heading">Governing Principles</h2>
      <ul class="principle-list">
        <li>
          <h3>Security by Default</h3>
          <p>Authentication and authorization follow a default-deny model. Data protection
             and secure configuration are established at inception, not retrofitted.</p>
        </li>
        <li>
          <h3>Durable, Low-Maintenance Solutions</h3>
          <p>Solutions are constructed for long-term maintainability and for portability
             to the client's own platform, minimizing operational burden over time.</p>
        </li>
        <li>
          <h3>Efficient Artificial Intelligence</h3>
          <p>Artificial intelligence architectures minimize model token consumption through
             retrieval, caching, and deterministic processing, while preserving consistent results.</p>
        </li>
        <li>
          <h3>Verified Outcomes</h3>
          <p>Work is considered complete only when the requested outcome has been implemented
             and independently verified through executed tests and observable results.</p>
        </li>
      </ul>
    </div>
  </section>
</main>"""
    return head(COMPANY, TAGLINE, 0) + header(0) + body + footer(0)


def build_service(index):
    s = SERVICES[index]
    prev_s = SERVICES[index - 1] if index > 0 else None
    next_s = SERVICES[index + 1] if index < len(SERVICES) - 1 else None

    delivers = "".join(f"<li>{e(d)}</li>" for d in s["delivers"])
    bubble = "".join(f"<li>{e(b)}</li>" for b in s["bubble"])

    nav_prev = (
        f'<a class="phase-nav__link phase-nav__prev" href="{prev_s["slug"]}.html">'
        f'<span class="phase-nav__dir">Previous phase</span>'
        f'<span class="phase-nav__name">{e(prev_s["name"])}</span></a>'
        if prev_s else '<span class="phase-nav__spacer"></span>'
    )
    nav_next = (
        f'<a class="phase-nav__link phase-nav__next" href="{next_s["slug"]}.html">'
        f'<span class="phase-nav__dir">Next phase</span>'
        f'<span class="phase-nav__name">{e(next_s["name"])}</span></a>'
        if next_s else '<span class="phase-nav__spacer"></span>'
    )

    body = f"""
<main id="main" class="service-page">
  <section class="svc-hero" aria-labelledby="svc-heading">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="../index.html">Home</a>
        <span aria-hidden="true">/</span>
        <a href="../index.html#services">Services</a>
        <span aria-hidden="true">/</span>
        <span aria-current="page">{e(s['name'])}</span>
      </nav>
      <p class="svc-hero__phase">Lifecycle Phase {s['number']:02d} of {len(SERVICES):02d}</p>
      <h1 id="svc-heading">{e(s['name'])}</h1>
      <p class="svc-hero__summary">{e(s['summary'])}</p>
    </div>
  </section>

  <section class="svc-body">
    <div class="container svc-body__grid">
      <div class="svc-body__main">
        <h2>Overview</h2>
        <p>{e(s['intro'])}</p>

        <h2>Activities and Deliverables</h2>
        <ul class="deliver-list">{delivers}</ul>
      </div>
      <aside class="svc-body__aside" aria-label="Phase specifics">
        <div class="aside-card">
          <h2 class="aside-card__title">Phase Specifics</h2>
          <ul class="aside-card__list">{bubble}</ul>
        </div>
        <div class="aside-card aside-card--muted">
          <h2 class="aside-card__title">Engagement</h2>
          <p>This phase is available as part of a complete lifecycle engagement or as a
             discrete service.</p>
          <a class="btn btn--primary btn--block" href="../index.html#contact">Request Information</a>
        </div>
      </aside>
    </div>
  </section>

  <nav class="phase-nav" aria-label="Adjacent phases">
    <div class="container phase-nav__inner">
      {nav_prev}
      <a class="phase-nav__all" href="../index.html#process">All phases</a>
      {nav_next}
    </div>
  </nav>
</main>"""
    title = f"{s['name']} — {COMPANY}"
    desc = f"{s['name']}: {s['summary']} A service of Hardened Builds LLC."
    return head(title, desc, 1) + header(1) + body + footer(1)


# ---------------------------------------------------------------------------
# Stylesheet
# ---------------------------------------------------------------------------

STYLES = r"""
:root{
  --bg:#ffffff; --bg-2:#f3f6fb; --bg-3:#eaf1fb;
  --panel:#ffffff; --panel-2:#f7f9fd;
  --navy:#01234e; --navy-2:#0a2f63; --blue:#0072fe; --blue-ink:#0063db;
  --ink:#11213a; --ink-2:#33425a; --ink-dim:#5b6b84; --line:#d7e0ec; --line-2:#c3d2e6;
  --accent:#0072fe; --accent-navy:#01234e; --focus:#0072fe;
  --radius:12px; --maxw:1160px; --step:#f3f7fd;
  --shadow-sm:0 1px 2px rgba(1,35,78,.06), 0 2px 8px rgba(1,35,78,.05);
  --shadow-md:0 10px 30px rgba(1,35,78,.10);
  --shadow-lg:0 22px 50px rgba(1,35,78,.16);
  --font:'Calibri','Segoe UI',Candara,'Trebuchet MS',system-ui,-apple-system,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; font-family:var(--font); font-size:17px; line-height:1.6;
  color:var(--ink); background:var(--bg); -webkit-font-smoothing:antialiased;
}
.container{width:100%; max-width:var(--maxw); margin:0 auto; padding:0 24px}
.hero,.process,.services,.principles,.site-footer,.svc-hero{scroll-margin-top:80px}
a{color:var(--blue-ink); text-decoration:none}
a:hover{text-decoration:underline}
h1,h2,h3{line-height:1.18; color:var(--navy); font-weight:700; letter-spacing:-.01em}
h1{font-size:2.6rem; margin:.1em 0 .3em}
h2{font-size:1.7rem; margin:1.6em 0 .6em}
h3{font-size:1.2rem; margin:0 0 .3em}
p{margin:0 0 1em}
:focus-visible{outline:3px solid var(--focus); outline-offset:2px; border-radius:4px}

.skip-link{position:absolute; left:-999px; top:0; background:var(--navy); color:#fff;
  padding:10px 16px; z-index:100; border-radius:0 0 8px 0; font-weight:700}
.skip-link:focus{left:0}

/* Header */
.site-header{position:sticky; top:0; z-index:50; background:rgba(255,255,255,.92);
  backdrop-filter:blur(8px); border-bottom:1px solid var(--line)}
.site-header__inner{display:flex; align-items:center; justify-content:space-between; min-height:68px}
.brand{display:inline-flex; align-items:center; gap:11px; color:var(--navy); font-weight:700; font-size:1.18rem}
.brand:hover{text-decoration:none}
.brand__mark{height:26px; width:auto; display:block}
.brand__llc{color:var(--ink-dim); font-weight:600}
.site-nav{display:flex; align-items:center}
.nav-toggle{display:none; background:var(--bg-2); color:var(--navy); border:1px solid var(--line);
  padding:8px 14px; border-radius:8px; font-family:inherit; font-size:1rem; cursor:pointer}
.nav-menu{list-style:none; display:flex; gap:4px; margin:0; padding:0; align-items:center}
.nav-menu>li>a{display:block; padding:10px 13px; color:var(--ink-2); border-radius:8px; font-size:1rem; font-weight:600}
.nav-menu>li>a:hover{color:var(--navy); background:var(--bg-2); text-decoration:none}
.has-sub{position:relative}
.sub-menu{list-style:none; margin:0; padding:8px; position:absolute; top:100%; left:0;
  background:#fff; border:1px solid var(--line); border-radius:12px; min-width:280px;
  box-shadow:var(--shadow-md); display:none; z-index:60}
.sub-menu li a{display:block; padding:9px 12px; color:var(--ink-2); border-radius:7px; font-size:.97rem; font-weight:600}
.sub-menu li a:hover{color:var(--navy); background:var(--bg-2); text-decoration:none}
.has-sub:hover .sub-menu,.has-sub:focus-within .sub-menu{display:block}

/* Hero */
.hero{background:
  radial-gradient(900px 440px at 82% -12%, rgba(0,114,254,.10), transparent 62%),
  linear-gradient(180deg,#ffffff,var(--bg-2)); border-bottom:1px solid var(--line)}
.hero__inner{padding:64px 24px 72px; max-width:900px}
.hero__logo{display:block; width:min(560px,86%); height:auto; margin:0 0 30px}
.hero__eyebrow{text-transform:uppercase; letter-spacing:.16em; font-size:.84rem; font-weight:700;
  color:var(--blue-ink); margin:0 0 12px}
.hero h1{font-size:2.5rem; max-width:760px}
.hero__sub{font-size:1.1rem; color:var(--ink-2); max-width:720px; margin-top:.2em}
.hero__actions{display:flex; gap:14px; flex-wrap:wrap; margin-top:28px}

.btn{display:inline-block; padding:13px 26px; border-radius:9px; font-weight:700; font-size:1rem;
  border:2px solid transparent; cursor:pointer; transition:transform .05s ease, box-shadow .15s}
.btn:hover{text-decoration:none; transform:translateY(-1px)}
.btn--primary{background:var(--blue); color:#fff; box-shadow:0 6px 18px rgba(0,114,254,.28)}
.btn--primary:hover{background:var(--blue-ink)}
.btn--ghost{background:#fff; color:var(--navy); border-color:var(--line-2)}
.btn--ghost:hover{background:var(--bg-2); border-color:var(--blue)}
.btn--block{display:block; text-align:center; width:100%}

.section-lead{font-size:1.1rem; color:var(--ink-2); max-width:770px}

/* Process diagram — radial SDLC wheel */
.process{padding:76px 0; background:#fff}
.wheel{margin-top:26px}
.wheel__diagram{max-width:760px; margin:0 auto}
.wheel__svg{width:100%; height:auto; display:block; overflow:visible}
.wseg{cursor:pointer; outline:none}
.wseg .wseg__shape{transition:fill .15s ease}
.wseg .wseg__num,.wseg .wseg__icon{transition:fill .15s ease, stroke .15s ease}
.wseg:hover .wseg__shape,.wseg:focus-visible .wseg__shape,.wseg.is-active .wseg__shape{fill:var(--blue)}
.wseg:hover .wseg__num,.wseg:focus-visible .wseg__num,.wseg.is-active .wseg__num{fill:#fff}
.wseg:hover .wseg__icon,.wseg:focus-visible .wseg__icon,.wseg.is-active .wseg__icon{stroke:#fff}
.wseg:focus-visible .wseg__shape{stroke:var(--navy); stroke-width:3}
.wseg__label{pointer-events:none}
.wheel__detail{max-width:720px; margin:18px auto 0; text-align:center; color:var(--ink-2);
  font-size:1.06rem; line-height:1.55; min-height:3.2em}
.wheel__detail-name{font-weight:700; color:var(--navy); white-space:nowrap}
.process__hint{margin-top:18px; color:var(--ink-dim); font-size:.95rem; text-align:center}
.process__download{margin-top:4px; font-size:.95rem; text-align:center}

/* Services grid */
.services{padding:76px 0; background:var(--bg-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line)}
.svc-grid{list-style:none; margin:30px 0 0; padding:0;
  display:grid; grid-template-columns:repeat(auto-fill,minmax(244px,1fr)); gap:16px}
.svc-card a{display:block; height:100%; background:#fff; border:1px solid var(--line);
  border-radius:var(--radius); padding:20px; color:var(--ink); box-shadow:var(--shadow-sm);
  transition:border-color .15s, transform .05s, box-shadow .15s}
.svc-card a:hover{text-decoration:none; border-color:var(--blue); transform:translateY(-2px); box-shadow:var(--shadow-md)}
.svc-card__num{display:block; font-size:.84rem; font-weight:700; color:var(--blue-ink); letter-spacing:.06em; margin-bottom:8px}
.svc-card__name{display:block; font-weight:700; font-size:1.08rem; margin-bottom:6px; color:var(--navy)}
.svc-card__summary{display:block; font-size:.93rem; color:var(--ink-dim); line-height:1.45}

/* Principles */
.principles{padding:76px 0; background:#fff}
.principle-list{list-style:none; margin:30px 0 0; padding:0;
  display:grid; grid-template-columns:repeat(auto-fit,minmax(262px,1fr)); gap:20px}
.principle-list li{background:var(--bg-2); border:1px solid var(--line); border-left:4px solid var(--blue);
  border-radius:var(--radius); padding:22px}
.principle-list h3{color:var(--navy)}
.principle-list p{margin:0; color:var(--ink-2); font-size:.97rem}

/* Service page */
.svc-hero{background:linear-gradient(180deg,#ffffff,var(--bg-2)); border-bottom:1px solid var(--line); padding:38px 0 44px}
.breadcrumb{font-size:.9rem; color:var(--ink-dim); margin-bottom:18px; display:flex; gap:8px; flex-wrap:wrap}
.breadcrumb a{color:var(--ink-dim)} .breadcrumb a:hover{color:var(--blue-ink)}
.svc-hero__phase{text-transform:uppercase; letter-spacing:.14em; font-size:.84rem; font-weight:700; color:var(--blue-ink); margin:0 0 10px}
.svc-hero__summary{font-size:1.2rem; color:var(--ink-2); max-width:760px; margin:0}
.svc-body{padding:52px 0}
.svc-body__grid{display:grid; grid-template-columns:1fr 340px; gap:40px; align-items:start}
.svc-body__main h2{color:var(--navy)}
.svc-body__main p{color:var(--ink-2)}
.deliver-list{margin:0; padding:0; list-style:none}
.deliver-list li{position:relative; padding:0 0 14px 30px; color:var(--ink-2); line-height:1.55}
.deliver-list li::before{content:""; position:absolute; left:4px; top:9px; width:10px; height:10px;
  border:2px solid var(--blue); border-radius:2px; transform:rotate(45deg)}
.aside-card{background:var(--bg-2); border:1px solid var(--line); border-radius:var(--radius);
  padding:22px; margin-bottom:18px; position:sticky; top:86px}
.aside-card--muted{position:static; background:var(--navy); border-color:var(--navy)}
.aside-card__title{font-size:1.05rem; margin:0 0 12px; color:var(--navy)}
.aside-card__list{margin:0; padding-left:18px}
.aside-card__list li{margin-bottom:8px; color:var(--ink-2); font-size:.96rem; line-height:1.45}
.aside-card--muted .aside-card__title{color:#fff}
.aside-card--muted p{color:#c6d6ee; font-size:.95rem}

.phase-nav{border-top:1px solid var(--line); background:var(--bg-2)}
.phase-nav__inner{display:flex; align-items:center; justify-content:space-between; gap:16px; padding:22px 24px}
.phase-nav__link{display:flex; flex-direction:column; color:var(--navy); max-width:40%}
.phase-nav__next{text-align:right; align-items:flex-end}
.phase-nav__dir{font-size:.84rem; text-transform:uppercase; letter-spacing:.1em; color:var(--ink-dim)}
.phase-nav__name{font-weight:700}
.phase-nav__all{color:var(--ink-dim); font-size:.92rem}
.phase-nav__spacer{flex:1}

/* Footer */
.site-footer{background:var(--navy); color:#d6e2f3; padding:48px 0 0; margin-top:0}
.footer__inner{display:grid; grid-template-columns:1.2fr 2fr; gap:40px; padding-bottom:36px}
.footer__wordmark{font-weight:700; font-size:1.22rem; color:#fff; letter-spacing:-.01em}
.footer__wordmark .brand__llc{color:#8fb6ec; font-weight:600}
.footer__tagline{color:#b7c8e2; font-size:.95rem; max-width:340px; margin-top:.7em}
.footer__contact{color:#b7c8e2; font-size:.95rem}
.footer__contact a{color:#9fc2ff}
.footer__heading{font-size:1rem; margin:0 0 14px; color:#fff}
.footer__cols{display:grid; grid-template-columns:1fr 1fr; gap:10px 28px}
.footer__list{list-style:none; margin:0; padding:0}
.footer__list li{margin-bottom:9px}
.footer__list a{color:#b7c8e2; font-size:.94rem}
.footer__list a:hover{color:#fff}
.footer__legal{border-top:1px solid rgba(255,255,255,.14); padding:18px 24px}
.footer__legal p{margin:0; color:#9fb0cc; font-size:.88rem}

/* Responsive */
@media (max-width:980px){
  .process__flow{grid-template-columns:repeat(2,1fr)}
  .pstep::after,.pstep::before{display:none}
  .pstep:nth-child(2n) .pstep__bubble{left:auto; right:0}
  .pstep:nth-child(2n) .pstep__bubble::before{left:auto; right:28px}
  .pstep .pstep__bubble{width:280px}
  .svc-body__grid{grid-template-columns:1fr}
  .aside-card{position:static}
  .footer__inner{grid-template-columns:1fr}
}
@media (max-width:720px){
  h1,.hero h1{font-size:2.05rem}
  .nav-toggle{display:block}
  .nav-menu{position:absolute; top:68px; left:0; right:0; flex-direction:column; align-items:stretch;
    background:#fff; border-bottom:1px solid var(--line); padding:10px 16px; gap:2px; display:none;
    box-shadow:var(--shadow-md)}
  .nav-menu.is-open{display:flex}
  .sub-menu{position:static; display:block; border:none; box-shadow:none; background:transparent; padding:0 0 6px 12px; min-width:0}
  .has-sub:hover .sub-menu{display:block}
  .wheel__detail{font-size:1rem}
  .phase-nav__link{max-width:46%}
}
"""

# ---------------------------------------------------------------------------
# Client script — progressive enhancement only (CSP: script-src 'self')
# ---------------------------------------------------------------------------

SITE_JS = r"""(function () {
  "use strict";
  // Mobile navigation toggle.
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("primary-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  // SDLC wheel: hovering or focusing a phase updates the detail line beneath
  // it. Clicking a phase navigates to its service page (native link behavior).
  var detail = document.getElementById("wheel-detail");
  var segs = document.querySelectorAll(".wseg");
  function setActive(seg) {
    Array.prototype.forEach.call(segs, function (s) { s.classList.remove("is-active"); });
    if (!seg) { return; }
    seg.classList.add("is-active");
    if (detail) {
      var name = seg.getAttribute("data-num") + " · " + seg.getAttribute("data-label");
      var tip = seg.getAttribute("data-tip") || "";
      detail.innerHTML = "";
      var ns = document.createElement("span");
      ns.className = "wheel__detail-name";
      ns.textContent = name;
      var ts = document.createElement("span");
      ts.className = "wheel__detail-text";
      ts.textContent = " — " + tip;
      detail.appendChild(ns);
      detail.appendChild(ts);
    }
  }
  Array.prototype.forEach.call(segs, function (seg) {
    seg.addEventListener("mouseenter", function () { setActive(seg); });
    seg.addEventListener("focus", function () { setActive(seg); });
  });
})();
"""


# ---------------------------------------------------------------------------
# Downloadable process-overview image (real, scalable SVG)
# ---------------------------------------------------------------------------

def build_process_svg():
    """Downloadable lifecycle image: the static radial SDLC wheel (phase 01 active)."""
    return build_wheel(interactive=False, active=0)


# ---------------------------------------------------------------------------
# Security headers (canonical, server-set) and documented public allowlist
# ---------------------------------------------------------------------------

HEADERS_FILE = f"""# Security response headers for Hardened Builds LLC (static site).
# Format: netlify / Fine Structure style `_headers`. These are the canonical,
# server-set headers. Equivalent <meta> directives are embedded in each page as
# defense in depth, but HSTS and X-Content-Type-Options MUST be set here (HTTP
# headers only). Apply equivalent configuration on the destination host when the
# site is migrated to the client platform.
/*
  Content-Security-Policy: {CSP}
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Cross-Origin-Opener-Policy: same-origin
"""

ROUTES_ALLOWLIST = """{
  "_comment": "Single source of truth for route authorization policy. This is a public marketing website: it holds no user data and exposes no authenticated surface or API. The authorization model is therefore default-deny with an explicit public allowlist, where every served route is enumerated below as public. When an authenticated surface is later added (for example, a client portal), it MUST NOT be added to this allowlist; it must sit behind authentication, with unauthenticated page requests redirected to login and unauthenticated API requests answered with HTTP 401, and authenticated-but-unauthorized requests answered with HTTP 403.",
  "policy": "default-deny",
  "public_routes": [
    "/",
    "/index.html",
    "/styles.css",
    "/site.js",
    "/assets/process-overview.svg",
    "/assets/logo-full.png",
    "/assets/logo-mark.png",
    "/assets/favicon.png",
    "/assets/apple-touch-icon.png",
    "/services/business-requirements.html",
    "/services/solution-architecture.html",
    "/services/ai-app-design.html",
    "/services/ai-app-development.html",
    "/services/qa-testing.html",
    "/services/uat-testing-support.html",
    "/services/deployment-support.html",
    "/services/post-deployment-testing-support.html",
    "/services/post-deployment-hypercare.html",
    "/services/post-deployment-support.html"
  ],
  "authenticated_routes": [],
  "responses": {
    "unauthenticated_page_request": "302 redirect to /login",
    "unauthenticated_api_request": "401 Unauthorized",
    "authenticated_unauthorized_request": "403 Forbidden"
  },
  "data_exposure": "No user data is present in initial HTML, client bundles, or error messages."
}
"""

ROBOTS = "User-agent: *\nAllow: /\n"


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    write("index.html", build_index())
    for i in range(len(SERVICES)):
        write(f"services/{SERVICES[i]['slug']}.html", build_service(i))
    write("styles.css", STYLES)
    write("site.js", SITE_JS)
    write("assets/process-overview.svg", build_process_svg())
    write("_headers", HEADERS_FILE)
    write("routes.config.json", ROUTES_ALLOWLIST)
    write("robots.txt", ROBOTS)

    # Copy static brand assets (logo lockup, emblem mark, icons) from source.
    assets_src = os.path.join(ROOT, "assets_src")
    os.makedirs(os.path.join(DIST, "assets"), exist_ok=True)
    for name in ("logo-full.png", "logo-mark.png", "favicon.png", "apple-touch-icon.png"):
        shutil.copyfile(os.path.join(assets_src, name), os.path.join(DIST, "assets", name))

    pages = 1 + len(SERVICES)
    print(f"Generated {pages} HTML pages + assets into {DIST}")


if __name__ == "__main__":
    main()
