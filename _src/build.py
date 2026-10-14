#!/usr/bin/env python3
"""Builds the static site from _src/pages into the repository root.

Each page file in _src/pages starts with a metadata block:

    <!--
    path: construction-loans
    title: Page title
    description: Meta description
    nav: construction
    -->

Shortcodes available in page bodies:
    {{U:photo-id:width}}   Unsplash image URL at the given width
    {{icon:name}}          Inline SVG icon (see ICONS below)
    {{estimator:program}}  Loan estimator widget preset to a program
    {{cta}}                Closing call-to-action band
    {{year}}               Current year

Run:  python3 _src/build.py
"""
import re, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "_src" / "pages"
SITE = "https://lending.catalystccm.com"  # update to the production domain
YEAR = datetime.date.today().year

PHONE = "(813) 670-3223"
PHONE_TEL = "+18136703223"
EMAIL = "info@catalystcd.com"


def U(pid, w=1600):
    return f"https://images.unsplash.com/{pid}?auto=format&fit=crop&w={w}&q=72"


ICONS = {
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    "shield": '<path d="M12 3 4 6v6c0 4.5 3.4 8.4 8 9 4.6-.6 8-4.5 8-9V6l-8-3z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    "hammer": '<path d="m14 7 3 3"/><path d="M5 21l9.5-9.5"/><path d="M13 4.5 15.5 2 22 8.5 19.5 11z"/><path d="m11 6.5 6.5 6.5"/>',
    "draw": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18"/><path d="M8 14h3"/><path d="M8 17h6"/>',
    "handshake": '<path d="M3 12h3l3-3 3 2 3-2 3 3h3"/><path d="m9 15 2 2 4-4"/><path d="M3 12v4h3"/><path d="M21 12v4h-3"/>',
    "home": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "chart": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="m7 15 4-4 3 3 5-6"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3 13 9 5 9-5"/>',
    "doc": '<path d="M14 3H6v18h12V7l-4-4z"/><path d="M14 3v4h4"/><path d="M9 13h6"/><path d="M9 17h6"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9"/><path d="m17 6 3 3"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
}


def icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


NAV_PROGRAMS = [
    ("/construction-loans/", "Ground-Up Construction", "Spec homes, infill and townhome builds", "photo-1693639767415-27ff64ce4da2"),
    ("/fix-and-flip-loans/", "Fix & Flip", "Acquisition plus rehab for 1–4 family", "photo-1618832515490-e181c4794a45"),
    ("/bridge-loans/", "Bridge", "Acquisition, refinance and entitled land", "photo-1747854805840-9be7d5e360e6"),
    ("/how-it-works/", "Draws & Servicing", "How funds move during your build", "photo-1503387762-592deb58ef4e"),
]


def header(nav):
    def cur(key):
        return ' aria-current="page"' if nav == key else ""
    links = "".join(
        f'<a href="{h}"><img src="{U(img, 200)}" alt="" loading="lazy" width="64" height="52"><div><strong>{t}</strong><span>{d}</span></div></a>'
        for h, t, d, img in NAV_PROGRAMS)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="utility"><div class="wrap">
  <span class="u-note">Business-purpose real estate loans across Florida and the Southeast</span>
  <a href="tel:{PHONE_TEL}">{PHONE}</a>
  <a href="mailto:{EMAIL}">{EMAIL}</a>
  <a class="u-login" href="https://www.catalystccm.com" rel="noopener">CatalystCCM.com</a>
</div></div>
<header class="site-header"><div class="wrap">
  <a class="brand" href="/" aria-label="Catalyst Capital Management home">
    <img src="/assets/img/logo-navy.png" alt="Catalyst" width="168" height="40">
    <span class="brand-sub">Capital<br>Management</span>
  </a>
  <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
  <nav class="nav" id="site-nav" aria-label="Main">
    <div class="dd">
      <button type="button" aria-expanded="false"{' aria-current="page"' if nav in ('construction','flip','bridge') else ''}>Loan Programs</button>
      <div class="dd-panel">{links}<a class="dd-all" href="/#programs">Compare all programs</a></div>
    </div>
    <a href="/how-it-works/"{cur('process')}>How It Works</a>
    <a href="/faq/"{cur('faq')}>FAQ</a>
    <a href="/about/"{cur('about')} class="hide-md">About</a>
    <a href="/contact/"{cur('contact')}>Contact</a>
    <a class="btn btn-gold btn-sm" href="/apply/">Apply Now</a>
  </nav>
</div></header>"""


def footer():
    return f"""<footer class="site-footer"><div class="wrap">
  <div class="f-grid">
    <div>
      <img class="f-logo" src="/assets/img/logo-white.png" alt="Catalyst" width="168" height="45" loading="lazy">
      <p>Catalyst Capital Management provides construction, fix-and-flip and bridge financing to residential builders and real estate investors, funded by Catalyst-managed investment funds and serviced in-house.</p>
      <p>100 S. Ashley Drive, Suite 275<br>Tampa, FL 33602</p>
    </div>
    <div>
      <h4>Loan Programs</h4>
      <ul>
        <li><a href="/construction-loans/">Ground-Up Construction</a></li>
        <li><a href="/fix-and-flip-loans/">Fix &amp; Flip</a></li>
        <li><a href="/bridge-loans/">Bridge</a></li>
        <li><a href="https://www.catalystccm.com/loan-programs" rel="noopener">Commercial, SBA 504 &amp; EB-5</a></li>
      </ul>
    </div>
    <div>
      <h4>Borrowers</h4>
      <ul>
        <li><a href="/apply/">Apply Online</a></li>
        <li><a href="/how-it-works/">How It Works</a></li>
        <li><a href="/how-it-works/#draws">Construction Draws</a></li>
        <li><a href="/faq/">FAQ</a></li>
      </ul>
    </div>
    <div>
      <h4>Company</h4>
      <ul>
        <li><a href="/about/">About Catalyst</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="https://www.linkedin.com/company/catalystcapitalmanagement" rel="noopener">LinkedIn</a></li>
      </ul>
    </div>
  </div>
  <div class="f-legal">
    <p>Catalyst Capital Management makes business-purpose loans secured by non-owner-occupied real estate. Loans are not available for personal, family or household purposes or for owner-occupied residences. Rates, terms, leverage and program availability are indicative, subject to underwriting and credit approval, and may change without notice. Information on this website, including any estimate, is not a commitment to lend.</p>
    <div class="row"><span>&copy; <span data-year>{YEAR}</span> Catalyst Capital Management. All rights reserved.</span>
      <span><a href="https://www.catalystccm.com/_files/ugd/ce4fc5_b355235cc63f482cb231718e84f3e23b.pdf" rel="noopener">Privacy Policy</a><a href="https://www.catalystccm.com/_files/ugd/ce4fc5_26a95487b2dd4bacbb46e064ea534a7f.pdf" rel="noopener">Terms &amp; Conditions</a></span></div>
  </div>
</div></footer>
<div class="m-apply"><a class="btn btn-gold" href="/apply/">Apply Now</a></div>"""


def estimator(program):
    return f"""<div class="estimator reveal" data-estimator data-program="{program}">
  <div class="est-inputs">
    <span class="eyebrow">Loan estimator</span>
    <h3>See how much you could borrow</h3>
    <p class="muted small">Enter your numbers for an indicative maximum loan based on our published leverage.</p>
    <div class="seg" role="group" aria-label="Loan program">
      <button type="button" data-k="construction" aria-pressed="false">Construction</button>
      <button type="button" data-k="flip" aria-pressed="false">Fix &amp; Flip</button>
      <button type="button" data-k="bridge" aria-pressed="false">Bridge</button>
    </div>
    <div class="field"><label for="est-a-{program}" data-lbl="a">Purchase price</label><div class="money"><input id="est-a-{program}" name="est_a" type="text" inputmode="numeric" data-money placeholder="400,000"></div></div>
    <div class="field"><label for="est-b-{program}" data-lbl="b">Budget</label><div class="money"><input id="est-b-{program}" name="est_b" type="text" inputmode="numeric" data-money placeholder="900,000"></div></div>
    <div class="field"><label for="est-v-{program}" data-lbl="v">Value</label><div class="money"><input id="est-v-{program}" name="est_v" type="text" inputmode="numeric" data-money placeholder="1,850,000"></div></div>
  </div>
  <div class="est-out" aria-live="polite">
    <span class="lbl">Indicative maximum loan</span>
    <div class="big" data-out="loan">$0</div>
    <span class="small" data-out="caps"></span>
    <dl>
      <dt>Total project cost</dt><dd data-out="cost">–</dd>
      <dt>Estimated equity required</dt><dd data-out="equity">–</dd>
      <dt>Loan-to-cost</dt><dd data-out="ltc">–</dd>
      <dt>Loan-to-value</dt><dd data-out="ltv">–</dd>
      <dt>Limiting factor</dt><dd data-out="bind">–</dd>
    </dl>
    <div class="warn" data-out="warn" hidden></div>
    <a class="btn btn-gold" data-out="apply" href="/apply/">Apply with these numbers</a>
    <p class="note">Indicative only and not a commitment to lend. Final loan amount depends on appraisal, budget review, sponsor experience, credit and liquidity.</p>
  </div>
</div>"""


CTA = f"""<section class="cta-band">
  <div class="bg"><img src="{U('photo-1503387837-b154d5074bd2', 1800)}" alt="" loading="lazy"></div>
  <div class="wrap">
    <div><h2>Ready to put your next project in motion?</h2>
    <p>The online application takes about ten minutes. A Catalyst lender reviews every request personally and follows up with next steps.</p></div>
    <div class="btn-row"><a class="btn btn-gold" href="/apply/">Start Your Application</a><a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
  </div>
</section>"""


LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{site}/{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og}">
<meta name="theme-color" content="#0E1A3D">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="stylesheet" href="/assets/css/site.css?v={ver}">
</head>
<body class="{bodyclass}">
{header}
<main id="main">
{body}
</main>
{footer}
<script src="/assets/js/site.js?v={ver}" defer></script>
</body>
</html>
"""


def render(text):
    text = re.sub(r"\{\{U:([\w-]+):(\d+)\}\}", lambda m: U(m.group(1), m.group(2)), text)
    text = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: icon(m.group(1)), text)
    text = re.sub(r"\{\{estimator:(\w+)\}\}", lambda m: estimator(m.group(1)), text)
    return text.replace("{{cta}}", CTA).replace("{{year}}", str(YEAR)).replace("{{phone}}", PHONE).replace("{{tel}}", PHONE_TEL).replace("{{email}}", EMAIL)


def main():
    ver = datetime.datetime.now().strftime("%Y%m%d%H%M")
    built = []
    for f in sorted(PAGES.glob("*.html")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--(.*?)-->\s*", raw, re.S)
        meta = dict(re.findall(r"^[ \t]*(\w+):[ \t]*(.*?)[ \t]*$", m.group(1), re.M))
        body = render(raw[m.end():])
        path = meta.get("path", "")
        html = LAYOUT.format(
            title=meta["title"], description=meta["description"], site=SITE,
            path=(path + "/") if path and not path.endswith(".html") else path,
            og=U(meta.get("og", "photo-1603439810849-5e013dc3ce73"), 1200), ver=ver,
            bodyclass=meta.get("bodyclass", "has-m-apply"),
            header=header(meta.get("nav", "")), footer=footer(), body=body)
        if path.endswith(".html"):
            out = ROOT / path
        else:
            out = ROOT / path / "index.html" if path else ROOT / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        built.append(str(out.relative_to(ROOT)))
    print("Built:", ", ".join(built))


if __name__ == "__main__":
    main()
