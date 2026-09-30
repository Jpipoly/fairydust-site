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
MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

import hashlib
def ver(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()[:8]

def page(slug, title, desc, body):
    def nav_link(href, label, key):
        cur = ' aria-current="page"' if key == slug else ''
        return f'<a href="{href}"{cur}>{label}</a>'
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
<body>
  <header class="nav">
    <div class="wrap">
      <div class="nav-pill">
        <a href="/" aria-label="fairydust ventures home">{LOGO}</a>
        <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="menu">{MENU}</button>
        <nav class="nav-links" id="menu">
          {nav_link("/", "Home", "home")}
          {nav_link("investors", "For Investors", "investors")}
          {nav_link("founders", "For Founders", "founders")}
        </nav>
      </div>
    </div>
  </header>

  <main>
{body}
  </main>

  <footer>
    <div class="wrap">
      <div class="foot">
        {LOGO}
        <div class="foot-info">
          1700 Montgomery Street Suite 108,<br />San Francisco, CA 94111<br />
          <a href="mailto:ohhey@fairydust.vc">ohhey@fairydust.vc</a>
        </div>
        <nav class="foot-nav"><a href="/">Home</a><a href="investors">For Investors</a><a href="founders">For Founders</a></nav>
      </div>
      <p class="copyright">© 2026 Fairydust. All rights reserved. On Tuesdays, we make millionaires.</p>
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

import random
_rng = random.Random(7)
_colors = ["var(--rose)", "var(--pink)", "var(--orange)", "var(--blush)"]
_spots = []
for i in range(22):
    # keep most stars toward the edges so the headline stays clean
    x = _rng.choice([_rng.uniform(1, 18), _rng.uniform(55, 98), _rng.uniform(1, 98)])
    y = _rng.uniform(4, 94)
    _spots.append(
        f'<span class="hs" style="left:{x:.1f}%;top:{y:.1f}%;--s:{_rng.uniform(12, 34):.0f}px;'
        f'--c:{_rng.choice(_colors)};--d:{_rng.uniform(3.5, 7.5):.1f}s;--dl:-{_rng.uniform(0, 7):.1f}s;'
        f'--dx:{_rng.uniform(-14, 14):.0f}px;--dy:{_rng.uniform(-22, -6):.0f}px">{STAR1}</span>')
HERO_SPARKLES = '<div class="hero-sparkles" aria-hidden="true">' + "".join(_spots) + "</div>"

MARQUEE = "".join(f"<span>{n}</span><i>{SPARK}</i>" for n, _ in WORK * 4)

home = f'''    <section class="hero" data-sparkle>
      {HERO_SPARKLES}
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <h1>On Tuesdays<br />we make<br /><span class="shimmer">millionaires</span></h1>
          <div class="hero-ctas">
            <a href="founders" class="btn btn-brown">For Founders</a>
            <a href="investors" class="btn btn-outline">For Investors</a>
          </div>
        </div>
        <div class="hero-mark" aria-hidden="true">
          <span class="mark-lg">{SPARK}</span>
          <span class="wordmark-lg"><span class="wm">fairydust<span class="wm-v">ventures</span></span></span>
        </div>
      </div>
    </section>

    <div class="marquee" aria-hidden="true"><div class="marquee-track">{MARQUEE}</div></div>

    <section class="magic" id="magic">
      <div class="wrap magic-grid">
        <h2 class="h2 reveal">The Magic Logic</h2>
        <div class="magic-body reveal">
          <p class="first">Yes. We inject capital.</p>
          <p class="lead">But we don't just inject capital; we sprinkle the operational magic required to scale.</p>
          <p>Our team of operators handles the legal, finance, and PR heavy lifting, allowing your startup to focus on the vision while we handle the boring work.</p>
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
          <a href="founders" class="btn btn-pink">Initiate Magic</a>
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
          <form data-mailto="ohhey@fairydust.vc" data-subject="Get on the Fairydust deals list" style="margin-top:28px">
            <div class="field"><label for="em">Email address *</label><input id="em" name="Email address" type="email" autocomplete="email" inputmode="email" required /></div>
            <button class="btn btn-pink" type="submit">Join the list</button>
            <p class="form-ok">Your email app should now open with a message ready to send.</p>
          </form>
        </div>
      </div>
    </section>

''' + motto_inv

founders = '''    <section class="page-hero">
      <div class="wrap">
        <h1>We want your vision, not your money.</h1>
        <p class="lead">Share your ideas so we can provide the capital and expert operational backing you need to scale.</p>
        <div class="hero-ctas"><a href="#pitch" class="btn btn-brown">Get in Touch</a></div>
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
          <form data-mailto="ohhey@fairydust.vc" data-subject="Share your idea — Fairydust" style="margin-top:28px">
            <div class="field"><label for="n">Name *</label><input id="n" name="Name" autocomplete="name" required /></div>
            <div class="field"><label for="e">Email *</label><input id="e" name="Email" type="email" autocomplete="email" inputmode="email" required /></div>
            <div class="field"><label for="i">Idea *</label><textarea id="i" name="Idea" required></textarea></div>
            <div class="field"><label for="d">Pitch deck</label><input id="d" name="Pitch deck" type="url" inputmode="url" placeholder="Link to your deck" /></div>
            <button class="btn btn-pink" type="submit">Send</button>
            <p class="form-ok">Your email app should now open with your idea ready to send.</p>
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
