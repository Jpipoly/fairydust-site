# Builds the three pages from one shared header/footer. Run: python3 build.py
def star(cx, cy, r, k=0.16):
    q = r * k
    return (f"M{cx} {cy-r}Q{cx+q:.2f} {cy-q:.2f} {cx+r} {cy}Q{cx+q:.2f} {cy+q:.2f} {cx} {cy+r}"
            f"Q{cx-q:.2f} {cy+q:.2f} {cx-r} {cy}Q{cx-q:.2f} {cy-q:.2f} {cx} {cy-r}Z")

# Three-star mark: one lead star, two smaller companions
SPARK = ('<svg class="mark" viewBox="0 0 48 48" fill="currentColor" aria-hidden="true">'
         f'<path d="{star(17, 29, 15, .1)}"/><path d="{star(38, 11, 8, .1)}"/><path d="{star(39.5, 38, 4.5, .1)}" opacity=".75"/></svg>')
STAR1 = f'<svg viewBox="-10 -10 20 20" fill="currentColor"><path d="{star(0, 0, 10, .1)}"/></svg>'
LOGO = f'<span class="logo">{SPARK}<span class="wm">fairydust<span class="wm-v">ventures</span></span></span>'
MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path class="l1" d="M4 7h16"/><path class="l2" d="M4 12h16"/><path class="l3" d="M4 17h16"/></svg>'
ARROW = '<span class="btn-ic" aria-hidden="true"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg></span>'

import hashlib

# Form endpoints (e.g. "https://formspree.io/f/abcdwxyz"). Empty = email fallback.
FORMS = {"founders": "", "investors": ""}
def ver(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()[:8]

def page(slug, title, desc, body):
    body = body.replace("{ARROW}", ARROW).replace("{FORM_FOUNDERS}", FORMS["founders"]).replace("{FORM_INVESTORS}", FORMS["investors"])
    def cur(key):
        return ' aria-current="page"' if key == slug else ''
    def links(cls):
        return (f'<a class="nav-link" href="/"{cur("home")}>Home</a>'
                f'<a class="nav-link" href="investors"{cur("investors")}>For Investors</a>')
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#ffaea3" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <link rel="icon" href="favicon.svg?v={ver("favicon.svg")}" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css?v={ver("styles.css")}" />
  <script>document.documentElement.classList.add("js")</script>
</head>
<body id="top">
  <header class="nav">
    <div class="wrap">
      <div class="nav-pill">
        <a class="logo-link" href="/" aria-label="fairydust ventures home">{LOGO}</a>
        <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="menu">{MENU}</button>
        <nav class="nav-links" id="menu" data-ind>
          <span class="nav-ind" aria-hidden="true"></span>
          {links("nav")}
          <a class="btn btn-brown btn-sm" href="founders"{cur("founders")}>For Founders{ARROW}</a>
        </nav>
      </div>
    </div>
  </header>

  <main>
{body}
  </main>

  <footer>
    <div class="wrap">
      <div class="foot-top">
        <div>
          <a class="logo-link" href="/" aria-label="fairydust ventures home">{LOGO}</a><br />
          <a class="foot-mail" href="mailto:ohhey@fairydust.vc">ohhey@fairydust.vc{ARROW}</a>
        </div>
        <nav class="foot-nav" data-ind aria-label="Footer">
          <span class="nav-ind" aria-hidden="true"></span>
          <a class="nav-link" href="/"{cur("home")}>Home</a>
          <a class="nav-link" href="investors"{cur("investors")}>For Investors</a>
          <a class="nav-link" href="founders"{cur("founders")}>For Founders</a>
        </nav>
      </div>
      <div class="foot-bottom">
        <span class="foot-addr">1700 Montgomery Street Suite 108, San Francisco, CA 94111</span>
        <span class="copyright">© 2026 Fairydust. All rights reserved. On Tuesdays, we make millionaires.</span>
        <a class="btn to-top" href="#top" aria-label="Back to top"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 13V3M4 7l4-4 4 4"/></svg></a>
      </div>
    </div>
  </footer>
  <script src="main.js?v={ver("main.js")}" defer></script>
</body>
</html>
'''

WORK = [
    ("Legal", "We handle all the tricky paperwork and red tape so you don’t have to."),
    ("Operations", "We build the scalable systems and processes that keep your rocketship from falling apart mid-flight."),
    ("Finance", "We manage the capital injection and financial modeling, including payroll and FP&amp;A."),
    ("HR", "We handle the people ops and HR management so your team can actually focus on building."),
    ("PR &amp; Branding", "We craft the narrative and the image that makes you the industry powerhouse."),
    ("Marketing", "We plan and execute your marketing from 0–1 or 1–2 so the right people actually hear about you."),
]
TEAM = [
    ("The Finance Nerd", "Turns messy cap tables into clean, investor-ready stories."),
    ("The Policy Worrier", "Spots the regulatory landmines before anyone else does."),
    ("The PR Whisperer", "Makes your story impossible for press and LPs to ignore."),
]

_S1, _S2, _S3 = star(17, 29, 15, .1), star(38, 11, 8, .1), star(39.5, 38, 4.5, .1)
_FLARE = star(0, 0, 2.2, .12)
import math
_dust = "".join(
    f'<circle cx="{24 + r * math.cos(math.radians(a)):.2f}" cy="{24 + r * math.sin(math.radians(a)):.2f}" r="{s}" fill="{c}" style="--o:{o}"/>'
    for a, r, s, c, o in [(15, 21, .55, "#ff7143", .7), (80, 23, .4, "#b35a53", .5), (140, 20, .45, "#ffaea3", .9),
                          (200, 22, .5, "#ff7143", .6), (255, 19, .35, "#b35a53", .6), (320, 23, .4, "#ffaea3", .8)]
)
HERO_MARK = ('<svg viewBox="0 0 48 48" class="hs-svg"><defs>'
  '<linearGradient id="hsg" x1="0" y1="0" x2="1" y2="1">'
  '<stop offset="0" stop-color="#ffaea3"/><stop offset=".5" stop-color="#ff7143"/><stop offset="1" stop-color="#b35a53"/></linearGradient>'
  '<linearGradient id="hsg2" x1="0" y1="0" x2="1" y2="1">'
  '<stop offset="0" stop-color="#ffaea3"/><stop offset="1" stop-color="#ff7143"/></linearGradient>'
  '<linearGradient id="glint" x1="0" y1="0" x2="1" y2="0">'
  '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
  f'<clipPath id="hsclip"><path d="{_S1}"/><path d="{_S2}"/><path d="{_S3}"/></clipPath></defs>'
  f'<g class="dust">{_dust}</g>'
  f'<g class="g1"><path class="s1" fill="url(#hsg)" d="{_S1}"/></g>'
  f'<g class="g2"><path class="s2" fill="url(#hsg2)" d="{_S2}"/></g>'
  f'<g class="g3"><path class="s3" fill="#b35a53" d="{_S3}"/></g>'
  '<g clip-path="url(#hsclip)"><rect class="glint" x="-14" y="-10" width="12" height="70" fill="url(#glint)" transform="rotate(20 24 24)"/></g>'
  f'<path class="flare f1" fill="#fff" d="{_FLARE}" transform="translate(17 14.5)"/>'
  f'<path class="flare f2" fill="#fff" d="{_FLARE}" transform="translate(45.5 11)"/>'
  f'<path class="flare f3" fill="#fff" d="{_FLARE}" transform="translate(32 29)"/>'
  '</svg>')

MARQUEE = f"<i>{SPARK}</i>".join(f"<span>{n}</span>" for n, _ in WORK)

home = f'''    <section class="hero" data-sparkle>
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <h1>On Tuesdays<br />we make<br /><span class="shimmer">millionaires</span></h1>
          <p class="hero-lead"><strong>We inject capital</strong> — and sprinkle the operational magic required to scale.</p>
          <div class="hero-ctas">
            <a href="founders" class="btn btn-brown">For Founders{ARROW}</a>
            <a href="investors" class="btn btn-outline">For Investors{ARROW}</a>
          </div>
        </div>
        <div class="hero-star" aria-hidden="true" data-tilt>
          {HERO_MARK}
        </div>
      </div>
    </section>

    <div class="marquee"><div class="marquee-track">{MARQUEE}</div></div>

    <section class="magic" id="magic">
      <div class="wrap magic-grid">
        <h2 class="h2 reveal">The Magic Logic</h2>
        <div class="magic-body reveal">
          <p class="first">Our team of operators handles the legal, finance, and PR heavy lifting, allowing your startup to focus on the vision while we handle the boring work.</p>
          <p class="quiet">We are the fairydust sprinklers, turning ambitious ideas into industry powerhouses with surgical precision and a sprinkle of mystery.</p>
        </div>
      </div>
    </section>

    <section class="sprinklers" id="sprinklers">
      <div class="wrap">
        <div class="section-head reveal">
          <h2 class="h2">The Sprinklers</h2>
          <p class="lead">Our powerhouse operators who turn ambition into industry leadership through operational magic.</p>
        </div>
        <div class="team">
''' + "\n".join(f'''          <article class="member reveal"><span class="spark">{SPARK}</span><h3>{n}</h3><p>{d}</p></article>''' for n, d in TEAM) + f'''
        </div>
      </div>
    </section>

    <section class="boring" id="boring">
      <div class="wrap">
        <div class="section-head reveal"><h2 class="h2">The Boring Work</h2></div>
        <div class="work-list">
''' + "\n".join(f'''          <div class="work reveal"><span class="work-n">0{i}</span><h3>{n}</h3><p>{d}</p></div>''' for i, (n, d) in enumerate(WORK, 1)) + '''
        </div>
      </div>
    </section>

    <section class="cta-sec">
      <div class="wrap">
        <div class="cta-card reveal">
          <span class="tw tw1" aria-hidden="true">{SPARK}</span><span class="tw tw2" aria-hidden="true">{SPARK}</span>
          <h2 class="h2">Want Some Sprinkles?</h2>
          <a href="founders" class="btn btn-pink">Initiate Magic{ARROW}</a>
        </div>
      </div>
    </section>'''.replace('{SPARK}', SPARK)

motto_inv = '''    <section class="motto">
      <div class="wrap reveal">
        <blockquote>Founders bring the magic. We sprinkle the dust.</blockquote>
        <p class="motto-by">Our Motto</p>
      </div>
    </section>'''

investors = '''    <section class="page-hero">
      <div class="wrap">
        <h1>We utilize deal-by-deal SPVs to provide flexible capital and elite mentorship to startups.</h1>
        <p class="lead">Through proactive partnership, we help early-stage leaders scale efficiently over weeks or months, ensuring lasting impact.</p>
        <p class="lead">Our model <strong>protects equity</strong> while offering founders strategic support to identify growth opportunities and navigate hurdles without upfront costs.</p>
      </div>
    </section>

    <section class="boring" id="list">
      <div class="wrap split">
        <div class="reveal">
          <h2 class="h2">The Fund</h2>
        </div>
        <div class="panel reveal">
          <h3 class="h2">Get on our deals list</h3>
          <p>Receive exclusive updates on the latest Fairydust deal opportunities straight to your inbox.</p>
          <form class="js-form" data-endpoint="{FORM_INVESTORS}" data-mailto="ohhey@fairydust.vc" data-subject="Get on the Fairydust deals list" novalidate style="margin-top:28px">
            <div class="field"><label for="em">Email address *</label><input id="em" name="Email address" type="email" autocomplete="email" inputmode="email" required /></div>
            <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" />
            <button class="btn btn-pink" type="submit">Join the list{ARROW}</button>
            <p class="form-status" role="status" aria-live="polite"></p>
          </form>
        </div>
      </div>
    </section>

''' + motto_inv

founders = '''    <section class="page-hero">
      <div class="wrap">
        <h1>We want your vision, not your money.</h1>
        <p class="lead">Share your ideas so we can provide the capital and expert operational backing you need to scale.</p>
        <div class="hero-ctas"><a href="#pitch" class="btn btn-brown">Get in Touch{ARROW}</a></div>
      </div>
    </section>

    <section class="motto">
      <div class="wrap reveal">
        <blockquote>You bring the magic — we just sprinkle the dust.</blockquote>
        <p class="motto-by">Our Motto</p>
        <p class="body">We think founders should spend less time in front of a laptop doing boring stuff and more time thinking and building.</p>
      </div>
    </section>

    <section class="boring" id="pitch">
      <div class="wrap split">
        <div class="reveal">
          <h2 class="h2">Get in touch with us</h2>
          <p class="aside">So let's both skip the sales pitch shall we?</p>
        </div>
        <div class="panel reveal">
          <h3 class="h2">Get in Touch</h3>
          <p>Share your idea with us and we'll be in touch shortly.</p>
          <form class="js-form" data-endpoint="{FORM_FOUNDERS}" data-mailto="ohhey@fairydust.vc" data-subject="Share your idea — Fairydust" enctype="multipart/form-data" novalidate style="margin-top:28px">
            <div class="field"><label for="n">Name *</label><input id="n" name="Name" autocomplete="name" required /></div>
            <div class="field"><label for="e">Email *</label><input id="e" name="Email" type="email" autocomplete="email" inputmode="email" required /></div>
            <div class="field"><label for="i">Idea *</label><textarea id="i" name="Idea" required></textarea></div>
            <div class="field">
              <span class="label">Pitch deck</span>
              <label class="drop" for="d">
                <input id="d" name="Pitch deck" type="file" accept=".pdf,.ppt,.pptx,.key,.doc,.docx" />
                <span class="drop-ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4M7 9l5-5 5 5M5 20h14"/></svg></span>
                <span class="drop-text"><strong class="drop-name">Upload deck</strong><span class="drop-hint">Please upload a document file (PDF, PPTX, etc.)</span></span>
              </label>
            </div>
            <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" />
            <button class="btn btn-pink" type="submit">Send{ARROW}</button>
            <p class="form-status" role="status" aria-live="polite"></p>
          </form>
        </div>
      </div>
    </section>'''

pages = [
    ("index.html", "home", "Home | fairydust ventures", "On Tuesdays we make millionaires. We inject capital and sprinkle the operational magic required to scale.", home),
    ("investors.html", "investors", "For Investors | fairydust ventures", "We utilize deal-by-deal SPVs to provide flexible capital and elite mentorship to startups.", investors),
    ("founders.html", "founders", "For Founders | fairydust ventures", "We want your vision, not your money. Share your idea with Fairydust.", founders),
]
for fn, slug, title, desc, body in pages:
    open(fn, "w").write(page(slug, title, desc, body))
print("built", [p[0] for p in pages])
