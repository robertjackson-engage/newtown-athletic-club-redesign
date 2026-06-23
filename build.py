#!/usr/bin/env python3
# NEWTOWN ATHLETIC CLUB (Bucks County, PA) — static site generator
import os, time, glob as _glob, re as _re

OUT = os.path.join(os.path.dirname(__file__), "docs")
IMG = "assets/img"
V = str(int(time.time()))
CONTENT = os.path.join(os.path.dirname(__file__), "content")
PHONE = "215-968-0600"
PHONE_TEL = "2159680600"


# ============================================================ CMS engine
def _parse_md(path):
    raw = open(path, encoding="utf-8").read()
    meta, body = {}, raw
    m = _re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, _re.S)
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"').strip("'")
        body = m.group(2)
    return meta, _md_to_html(body.strip())


def _md_to_html(md):
    md = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if _re.match(r"^\s*[-*]\s+", ln):
            items = []
            while i < len(lines) and _re.match(r"^\s*[-*]\s+", lines[i]):
                items.append("<li>" + _inline(_re.sub(r"^\s*[-*]\s+", "", lines[i])) + "</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>"); continue
        h = _re.match(r"^(#{1,4})\s+(.*)$", ln)
        if h:
            lvl = len(h.group(1)); out.append(f"<h{lvl+1}>{_inline(h.group(2))}</h{lvl+1}>"); i += 1; continue
        if ln.strip() == "":
            i += 1; continue
        para = [ln]; i += 1
        while i < len(lines) and lines[i].strip() and not _re.match(r"^(#{1,4}\s|\s*[-*]\s)", lines[i]):
            para.append(lines[i]); i += 1
        out.append("<p>" + _inline(" ".join(para)) + "</p>")
    return "\n".join(out)


def _inline(t):
    t = _re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = _re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = _re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


def load_collection(folder):
    items = []
    for p in _glob.glob(os.path.join(CONTENT, folder, "*.md")):
        meta, body = _parse_md(p)
        meta["_slug"] = os.path.splitext(os.path.basename(p))[0]
        meta["_body"] = body
        items.append(meta)
    items.sort(key=lambda m: m.get("date", ""), reverse=True)
    return items


def cms_img(path):
    return (path or "").lstrip("/") or f"{IMG}/General-5-scaled.jpg"


def cms_link(path):
    p = (path or "#").strip()
    if p.startswith(("http", "#", "mailto:", "tel:")):
        return p
    return p.lstrip("/") or "#"


def fmt_date(d):
    months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    m = _re.match(r"(\d{4})-(\d{2})-(\d{2})", d or "")
    return f"{months[int(m.group(2))]} {int(m.group(3))}, {m.group(1)}" if m else (d or "")


# ============================================================ brand + chrome
def brand_logo(cls=""):
    return (f'<span class="brand__lockup {cls}"><img class="brand__logo" src="{IMG}/nac-logo-white.png" alt="">'
            f'<span class="brand__name">Newtown<em>Athletic Club</em></span></span>')


NAV = [
    ("Membership", "membership.html"),
    ("Fitness", "fitness.html"),
    ("Studios", "studios.html"),
    ("Resort", "resort.html"),
    ("Family", "family.html"),
    ("Wellness", "wellness.html"),
]

MENU = [
    ("Home", "index.html"),
    ("Our Story", "about.html"),
    ("Club Facilities", "facilities.html"),
    ("Membership", "membership.html"),
    ("Pricing", "pricing.html"),
    ("NAC Premier", "premier.html"),
    ("Personal Training", "fitness.html"),
    ("Back Gym Weight Room", "weight-room.html"),
    ("FIT 22 Strength Studio", "strength-studio.html"),
    ("Boutique Studios", "studios.html"),
    ("THE PRACTICE — Yoga", "the-practice.html"),
    ("REFORM — Pilates", "reform.html"),
    ("PULSE", "pulse.html"),
    ("REV — Cycling", "rev.html"),
    ("Barre Lab", "barre.html"),
    ("SIX ZONE", "six-zone.html"),
    ("105 Hot Studio", "hot-105.html"),
    ("HYROX", "hyrox.html"),
    ("Swim &amp; Aquatics", "swim.html"),
    ("Escape Resort", "resort.html"),
    ("Stretch &amp; Recovery", "stretch-recovery.html"),
    ("Kids Club &amp; Family", "family.html"),
    ("Camp NAC", "camps.html"),
    ("Gymnastics", "gymnastics.html"),
    ("Youth Performance", "youth-training.html"),
    ("Wellness Services", "wellness.html"),
    ("Functional Medicine", "functional-medicine.html"),
    ("Giving Back", "giving.html"),
    ("Hours", "hours.html"),
    ("FAQ", "faq.html"),
    ("Blog", "blog.html"),
    ("Contact", "contact.html"),
    ("Join Now", "join.html"),
]


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700;800;900&family=PT+Sans:ital,wght@0,400;0,700;1,400&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="{IMG}/nac-mark.svg">
<link rel="stylesheet" href="assets/css/main.css?v={V}">
<script>(function(){{try{{
  if(sessionStorage.getItem("nac-intro"))document.documentElement.classList.add("no-preloader");
  var v=localStorage.getItem("nac-view");
  document.documentElement.setAttribute("data-view", v==="member"?"member":"guest");
  if(v||sessionStorage.getItem("nac-view-skip"))document.documentElement.classList.add("has-view");
}}catch(e){{}}}})();</script>
</head>
<body>
<div class="preloader" aria-hidden="true">
  <div class="preloader__mark"><img class="brand__logo" src="{IMG}/nac-logo-white.png" alt="Newtown Athletic Club"></div>
  <div class="preloader__sub">Your Home for Health</div>
  <div class="preloader__bar"><i></i></div>
  <div class="preloader__count">0</div>
</div>
"""


def header_html(active=""):
    AC = ' class="is-active"'
    links = "".join(f'<a href="{h}"{AC if h==active else ""}>{l}</a>' for l, h in NAV)
    menu_links = "".join(f'<a href="{h}"><span class="idx">{i:02d}</span>{l}</a>' for i, (l, h) in enumerate(MENU, 1))
    return f"""
<header class="site-header">
  <div class="site-header__inner">
    <a class="brand" href="index.html" aria-label="Newtown Athletic Club — home">{brand_logo()}</a>
    <nav class="nav-desktop" aria-label="Primary">{links}</nav>
    <div class="header-cta">
      <div class="view-toggle" role="group" aria-label="View site as">
        <button type="button" data-view-set="guest">Guest</button>
        <button type="button" data-view-set="member">Member</button>
      </div>
      <a class="btn btn--sm only-guest header-pricing" href="join.html#trial">Free Pass</a>
      <a class="btn btn--solid btn--sm only-guest" href="join.html">Join Now</a>
      <a class="btn btn--solid btn--sm only-member" href="studios.html">Class Schedule</a>
      <button class="menu-toggle" aria-expanded="false" aria-label="Open menu">
        <span>Menu</span><span class="menu-toggle__icon"><i></i><i></i></span>
      </button>
    </div>
  </div>
</header>
<div class="menu-overlay" role="dialog" aria-label="Site menu">
  <div class="menu-overlay__grid">
    <nav class="menu-list" aria-label="All pages">{menu_links}</nav>
    <aside class="menu-side">
      <div class="menu-side__pass">
        <p>More than a health club. <em>This is a lifestyle.</em></p>
        <a class="btn btn--solid btn--sm" href="join.html">Join Now <span class="arr">→</span></a>
      </div>
      <div class="menu-side__group">
        <h6>Visit Us</h6>
        <a href="https://maps.google.com/?q=120+Pheasant+Run+Newtown+PA+18940" target="_blank" rel="noopener">120 Pheasant Run, Newtown, PA</a>
        <a href="hours.html">Club hours</a>
      </div>
      <div class="menu-side__group">
        <h6>Talk to us</h6>
        <a href="tel:{PHONE_TEL}">{PHONE}</a>
        <a href="contact.html">Contact &amp; departments</a>
      </div>
    </aside>
  </div>
</div>
<main id="mainContent">
"""


def footer_html():
    return f"""
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__top">
      <div class="site-footer__brand">
        <a class="brand brand--footer" href="index.html">{brand_logo()}</a>
        <p>Named one of the top lifestyle clubs on the globe — right here in Bucks County, Pennsylvania. This is more than a health club. This is a lifestyle.</p>
        <div class="socials">
          <a href="https://www.facebook.com/newtownac/" aria-label="Facebook">FB</a>
          <a href="https://www.instagram.com/newtownac/" aria-label="Instagram">IG</a>
          <a href="https://www.youtube.com/channel/UCAQNPTRquLDNyq47AL9ZF9w" aria-label="YouTube">YT</a>
        </div>
      </div>
      <div>
        <h5>Move</h5>
        <div class="site-footer__links">
          <a href="fitness.html">Personal Training</a>
          <a href="studios.html">Boutique Studios</a>
          <a href="weight-room.html">Back Gym</a>
          <a href="hyrox.html">HYROX</a>
          <a href="swim.html">Swim &amp; Aquatics</a>
          <a href="resort.html">Escape Resort</a>
          <a href="stretch-recovery.html">Stretch &amp; Recovery</a>
        </div>
      </div>
      <div>
        <h5>Club Life</h5>
        <div class="site-footer__links">
          <a href="family.html">Kids &amp; Family</a>
          <a href="camps.html">Camp NAC</a>
          <a href="wellness.html">Wellness &amp; Medical</a>
          <a href="functional-medicine.html">Functional Medicine</a>
          <a href="giving.html">Giving Back</a>
          <a href="about.html">Our Story</a>
          <a href="blog.html">Blog</a>
          <a href="faq.html">FAQ</a>
        </div>
      </div>
      <div class="site-footer__contact">
        <h5>Visit &amp; Join</h5>
        <a class="tel" href="tel:{PHONE_TEL}">{PHONE}</a>
        <a href="https://maps.google.com/?q=120+Pheasant+Run+Newtown+PA+18940" target="_blank" rel="noopener">120 Pheasant Run<br>Newtown, PA 18940</a>
        <a href="membership.html">Membership options</a>
        <form class="news-form" data-demo>
          <input type="email" placeholder="Join our newsletter" aria-label="Email address" required>
          <button type="submit">Join</button>
        </form>
      </div>
    </div>
  </div>
  <div class="site-footer__mega" aria-hidden="true">YOUR HOME FOR HEALTH</div>
  <div class="wrap">
    <div class="site-footer__bottom">
      <span>©2026 Newtown Athletic Club · Newtown, Bucks County, Pennsylvania. Building community since 1978.</span>
      <div class="legal">
        <a href="contact.html">Contact</a>
        <a href="faq.html">FAQ</a>
        <a href="privacy.html">Privacy</a>
        <a href="terms.html">Terms</a>
      </div>
    </div>
  </div>
</footer>
<script src="assets/js/main.js?v={V}"></script>
<script src="assets/js/chat-config.js?v={V}"></script>
<script src="assets/js/chat.js?v={V}" defer></script>
</body>
</html>
"""


# ============================================================ section helpers
def hero(kicker, lines, sub="", img=None, video=None, poster=None, crumb=None, actions=None, meta=None, page=False):
    lns = "".join(f'<span class="ln"><span style="transition-delay:{0.12+i*0.09:.2f}s">{ln}</span></span>' for i, ln in enumerate(lines))
    media = (f'<video src="{video}" poster="{poster or ""}" autoplay muted loop playsinline></video>' if video
             else (f'<img src="{img}" alt="" fetchpriority="high">' if img else ""))
    acts = ""
    if actions:
        acts = '<div class="hero__actions">'
        for a in actions:
            extra = (" " + a[3]) if len(a) > 3 else ""
            cls = ("btn btn--solid" if a[2] else "btn") + extra
            acts += f'<a class="{cls}" href="{a[1]}">{a[0]} <span class="arr">→</span></a>'
        acts += "</div>"
    crumb_html = f'<div class="hero__crumb"><div><a href="index.html">Home</a> &nbsp;/&nbsp; {crumb}</div></div>' if crumb else ""
    meta_html = ('<div class="hero__meta">' + "".join(f"<span>{m}</span>" for m in meta) + "</div>") if meta else ""
    sub_html = f'<p class="hero__sub">{sub}</p>' if sub else ""
    return f"""
<section class="hero{' hero--page' if page else ''}">
  <div class="hero__media">{media}</div>
  {crumb_html}
  <div class="hero__inner">
    <p class="hero__kicker">{kicker}</p>
    <h1 class="hero__title">{lns}</h1>
    {sub_html}{acts}
  </div>
  {meta_html}
  <div class="hero__scroll" aria-hidden="true"></div>
</section>
"""


def marquee(words, accent=False, ghost=False):
    cls = "marquee" + (" marquee--accent" if accent else "") + (" marquee--ghost" if ghost else "")
    seg = "".join(f"<span>{w} <i>●</i></span>" for w in words)
    return f'\n<div class="{cls}" aria-hidden="true"><div class="marquee__track">{seg}</div><div class="marquee__track">{seg}</div></div>\n'


def stats_band(items, light=False):
    cells = "".join(f"""
      <div class="stat"><div class="stat__num"><span data-count="{n}">0</span><span class="sfx">{s}</span></div>
      <div class="stat__label">{l}</div></div>""" for n, s, l in items)
    return f'\n<section class="section--flush{" section--light" if light else ""}"><div class="stats"><div class="wrap" style="padding:0"><div class="stats__grid">{cells}</div></div></div></section>\n'


def split(eyebrow, num, title, paras, img, alt, rev=False, cta=None, tag=None, light=False, wide=False):
    body = "".join(f'<p class="body-copy">{p}</p>' for p in paras)
    cta_html = f'<div class="split__cta"><a class="inline-link" href="{cta[1]}">{cta[0]} →</a></div>' if cta else ""
    tag_html = f'<span class="tag">{tag}</span>' if tag else ""
    return f"""
<section class="section{' section--light' if light else ''}">
  <div class="wrap"><div class="split{' split--rev' if rev else ''}">
    <div class="split__media{' split__media--wide' if wide else ''} reveal-img"><img src="{img}" alt="{alt}" loading="lazy">{tag_html}</div>
    <div class="split__body">
      <p class="eyebrow"><span class="num">{num}</span> {eyebrow}</p>
      <h2 class="h-display" style="font-size:clamp(30px,3.8vw,58px)">{title}</h2>
      <div class="reveal">{body}{cta_html}</div>
    </div>
  </div></div>
</section>
"""


def cta_band(title_html, text, img, primary=("Join Now", "join.html"), secondary=("Free Pass", "join.html#trial")):
    sec = f'<a class="btn" href="{secondary[1]}">{secondary[0]} <span class="arr">→</span></a>' if secondary else ""
    return f"""
<section class="cta-band">
  <div class="cta-band__media"><img src="{img}" alt="" loading="lazy"></div>
  <div class="wrap">
    <h2 class="reveal">{title_html}</h2><p class="reveal">{text}</p>
    <div class="hero__actions reveal"><a class="btn btn--solid" href="{primary[1]}">{primary[0]} <span class="arr">→</span></a>{sec}</div>
  </div>
</section>
"""


def form_section(sec_id, num, eyebrow, title_html, text, btn, light=True, extra="",
                 interests=("Membership &amp; Pricing", "Personal Training", "Boutique Studios", "Swim &amp; Resort", "Family &amp; Youth", "Wellness &amp; Medical")):
    fields = [("text", "first", "First name"), ("text", "last", "Last name"), ("email", "email", "Email address"), ("tel", "phone", "Phone")]
    f_html = "".join(f'<div class="field"><input type="{t}" name="{n}" id="{sec_id}-{n}" placeholder=" " required><label for="{sec_id}-{n}">{l}</label></div>' for t, n, l in fields)
    opts = "".join(f"<option>{o}</option>" for o in interests)
    return f"""
<section class="section{' section--light' if light else ''}" id="{sec_id}">
  <div class="wrap"><div class="intro-grid">
    <div>
      <p class="eyebrow"><span class="num">{num}</span> {eyebrow}</p>
      <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">{title_html}</h2>
      <p class="lede reveal" style="margin-top:28px">{text}</p>{extra}
    </div>
    <div class="intro-grid__right reveal"><form class="form-grid" data-demo>{f_html}
      <div class="field field--full"><select name="interest" id="{sec_id}-interest" aria-label="I'm interested in"><option value="">&nbsp;</option>{opts}</select><label for="{sec_id}-interest">I'm interested in</label></div>
      <button class="btn {'btn--dark' if light else ''} field--full" type="submit" style="justify-content:center">{btn} <span class="arr">→</span></button>
    </form><p class="form-note">We'll follow up by phone, email or text. No commitment — we're just here to help.</p></div>
  </div></div>
</section>
"""


def accordion(items, open_first=True):
    out = '<div class="acc reveal">'
    for i, (q, a) in enumerate(items):
        op = open_first and i == 0
        op_cls = " is-open" if op else ""
        op_style = ' style="max-height:800px"' if op else ""
        out += f'<div class="acc__item{op_cls}"><button class="acc__head" aria-expanded="{str(op).lower()}"><h3>{q}</h3><span class="acc__icon"></span></button><div class="acc__body"{op_style}><div class="acc__body-inner">{a}</div></div></div>'
    return out + "</div>"


def studio_grid(items):
    """items: (label, slug, img, blurb)"""
    cards = ""
    for i, (label, slug, im, blurb) in enumerate(items, 1):
        cards += (f'<a class="card" href="{slug}"><div class="card__media"><img src="{IMG}/{im}" alt="{label}" loading="lazy">'
                  f'<span class="card__num">{i:02d}</span><div class="card__label"><h3>{label}</h3><span class="go">Explore →</span></div></div></a>')
    return cards


def page(filename, title, desc, active, body):
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(head(title, desc) + header_html(active) + body + footer_html())
    print("built", filename)


def page_sub(filename, title, desc, body):
    html = head(title, desc) + header_html("blog.html") + body + footer_html()
    html = _re.sub(r'(href|src)="/(?!/)', r'\1="../', html)
    html = _re.sub(r'(href|src)="assets/', r'\1="../assets/', html)
    html = _re.sub(r'(href)="([a-z0-9-]+\.html)(#[^"]*)?"', r'\1="../\2\3"', html)
    os.makedirs(os.path.join(OUT, "blog"), exist_ok=True)
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(html)
    print("built", filename)


# ============================================================ shared blocks
view_chooser = f"""
<div class="view-chooser" role="dialog" aria-label="Choose your experience">
  <button class="vc-skip" type="button">Just browsing →</button>
  <div class="view-chooser__head"><span class="kicker">Welcome to the Newtown Athletic Club</span><h2>How are you visiting today?</h2></div>
  <div class="view-chooser__panels">
    <button class="vc-panel" type="button" data-choose="guest"><img src="{IMG}/resort_full-2.jpg" alt="">
      <div class="vc-panel__body"><span class="vc-panel__kicker">First time here?</span><h3>I'm <span class="serif">exploring</span></h3><p>Tour the club, the studios and the resort — and grab a complimentary pass.</p><span class="go">Show me around →</span></div></button>
    <button class="vc-panel" type="button" data-choose="member"><img src="{IMG}/fitness-center-weights-nac.jpg" alt="">
      <div class="vc-panel__body"><span class="vc-panel__kicker">Welcome back</span><h3>I'm a <span class="serif">member</span></h3><p>Class schedules, club hours, the resort and your wellness tools.</p><span class="go">Take me in →</span></div></button>
  </div>
</div>
"""

member_strip = """
<div class="member-strip only-member"><div class="wrap">
  <span class="hello">Welcome back.</span>
  <a href="studios.html">Class Schedules</a>
  <a href="hours.html">Club Hours</a>
  <a href="resort.html">Escape Resort</a>
  <a href="stretch-recovery.html">Book Recovery</a>
  <a href="functional-medicine.html">Wellness</a>
</div></div>
"""

# CMS content
EVENTS = load_collection("events")
POSTS = load_collection("blog")


def blog_index_body():
    if not POSTS:
        cards = '<p class="body-copy">No posts yet — check back soon.</p>'
    else:
        cards = ""
        for p in POSTS:
            num = f'<span class="card__num">{fmt_date(p.get("date"))} · {p.get("author","")}</span>'
            cards += (f'<a class="card" href="blog/{p["_slug"]}.html"><div class="card__media card__media--wide">'
                      f'<img src="{cms_img(p.get("image"))}" alt="{p.get("title","")}" loading="lazy">{num}'
                      f'<div class="card__label"><h3>{p.get("title","")}</h3></div></div>'
                      f'<div class="card__below"><p>{p.get("excerpt","")}</p></div></a>')
    return hero(
        "The NAC Blog", ["News &amp; stories from", '<span class="serif">your home for health</span>'],
        "Member spotlights, training tips, wellness science, club news and a little behind-the-scenes fun.",
        img=f"{IMG}/General-5-scaled.jpg", crumb="Blog",
        actions=[("Join the club", "join.html#trial", True)], page=True,
    ) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Latest from the club</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">On the <span class="serif">blog</span></h2></div></div>
  <div class="card-grid" data-stagger>{cards}</div>
</div></section>
""" + cta_band('Come be part of the <span class="serif">community</span>', "There's always something happening at the NAC. Start with a complimentary pass.", f"{IMG}/resort_full-2.jpg")


def blog_post_body(p):
    others = "".join(
        f'<a class="row-item" href="../blog/{o["_slug"]}.html"><span class="row-item__idx">→</span>'
        f'<span class="row-item__title">{o.get("title","")}</span>'
        f'<span class="row-item__desc">{o.get("excerpt","")}</span><span class="row-item__arrow">→</span></a>'
        for o in POSTS if o["_slug"] != p["_slug"])[:3] if len(POSTS) > 1 else ""
    more = f"""
<section class="section section--light"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">02</span> Keep reading</p><h2 class="h-display reveal" style="font-size:clamp(30px,3.4vw,52px)">More from <span class="serif">the blog</span></h2></div>
  <a class="inline-link reveal" href="../blog.html">All posts →</a></div><div class="rows reveal">{others}</div>
</div></section>""" if others else ""
    return f"""
<section class="hero hero--page hero--post">
  <div class="hero__media"><img src="../{cms_img(p.get('image'))}" alt=""></div>
  <div class="hero__crumb"><div><a href="../index.html">Home</a> &nbsp;/&nbsp; <a href="../blog.html">Blog</a></div></div>
  <div class="hero__inner">
    <p class="hero__kicker">{fmt_date(p.get('date'))} &nbsp;·&nbsp; {p.get('author','Newtown Athletic Club')}</p>
    <h1 class="hero__title"><span class="ln"><span style="transition-delay:.12s">{p.get('title','')}</span></span></h1>
  </div>
  <div class="hero__scroll" aria-hidden="true"></div>
</section>
<section class="section section--tight"><div class="wrap" style="max-width:760px">
  <div class="post-body reveal">{p['_body']}</div>
  <div class="reveal" style="margin-top:40px"><a class="btn btn--solid" href="../blog.html">← Back to the blog</a></div>
</div></section>
{more}
""" + cta_band('Your home for <span class="serif">health</span>', "Like what you're reading? Come see it in person with a complimentary pass.", f"../{IMG}/General-5-scaled.jpg")


# ============================================================ HOME
home_body = view_chooser + hero(
    "Your All-Inclusive Gym Membership",
    ["Your home", 'for <span class="serif">health</span>'],
    "Named one of the top lifestyle clubs and health &amp; wellness centers on the globe — located right here in Bucks County, Pennsylvania. With a membership for everyone, start or continue your journey to living your healthiest life.",
    video="assets/video/home-hero.mp4", poster=f"{IMG}/home-hero-poster.jpg",
    actions=[
        ("Get a Free Pass", "join.html#trial", True, "only-guest"),
        ("Explore the Club", "facilities.html", False, "only-guest"),
        ("Class Schedule", "studios.html", True, "only-member"),
        ("Escape Resort", "resort.html", False, "only-member"),
    ],
    meta=["250,000 sq. ft.", "Building community since 1978", "More than a club — a lifestyle"],
) + member_strip + marquee([
    "Boutique Studios", "Personal Training", "HYROX", "Escape Resort", "Functional Medicine",
    "Six Zone", "Yoga", "Pilates", "Cycling", "Swim", "Family &amp; Youth", "Recovery",
]) + f"""
<section class="section">
  <div class="wrap"><div class="intro-grid">
    <div><p class="eyebrow"><span class="num">01</span> Why we exist</p>
      <h2 class="h-display reveal">More than a health club. <span class="serif">A lifestyle.</span></h2></div>
    <div class="intro-grid__right">
      <p class="lede reveal">We've hand-picked the finest amenities, programs, coaches and equipment from all over the globe and brought them together under one roof — for every body, every age and every stage of life.</p>
      <p class="body-copy reveal">From youth to active-aging, young families to empty-nesters, the NAC is where Bucks County comes to train, recover, swim, play and belong. One membership opens all of it.</p>
      <div class="reveal"><a class="inline-link" href="about.html">Our story since 1978 →</a></div>
    </div>
  </div></div>
</section>
""" + stats_band([
    (250000, "", "Square feet of lifestyle"),
    (200, "+", "Group fitness classes weekly"),
    (10, "", "Boutique studios under one roof"),
    (4, "", "Acre outdoor Escape Resort"),
]) + f"""
<section class="section">
  <div class="wrap"><div class="cards-head">
    <div><p class="eyebrow"><span class="num">02</span> One membership, everything</p>
      <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Every way to <span class="serif">move</span></h2></div>
    <a class="inline-link reveal" href="membership.html">See membership →</a></div>
    <div class="card-grid" data-stagger>
      {studio_grid([
        ("Boutique Studios", "studios.html", "studios12.jpg", ""),
        ("Personal Training", "fitness.html", "NAC-Expert-Personal-Training.png", ""),
        ("Back Gym Weights", "weight-room.html", "NAC-Weight-Room-6.jpg", ""),
        ("HYROX &amp; Performance", "hyrox.html", "HYROX-Training-Club-Newtown-PA.png", ""),
        ("Swim &amp; Resort", "resort.html", "resort_full-2.jpg", ""),
        ("Wellness &amp; Medical", "wellness.html", "the-well-lounge-services-newtown-pa.jpg", ""),
      ])}
    </div>
  </div>
</section>
""" + marquee(["The Practice", "Reform", "Pulse", "Rev", "Barre Lab", "Six Zone", "105 Hot Studio", "FIT 22"], ghost=True) + split(
    "An unrivaled studio program", "03", 'A boutique studio for <span class="serif">every mood</span>',
    ["We traveled all over the globe to bring you the most luxurious and comprehensive group fitness training all under one roof — yoga, pilates, cycling, barre, HIIT, hot, dance and strength.",
     "Do anything, or everything, in an unlimited amount. Over 200 classes every week are included with your membership, taught by the best instructors in the region."],
    f"{IMG}/the-practice-1.jpg", "Boutique studios", cta=("Explore the studios", "studios.html"), tag="10 studios"
) + split(
    "Escape Resort", "04", 'A world-class resort in your <span class="serif">neighborhood</span>',
    ["Four acres. Four pools. Two 35-foot water slides, a lazy river, a heated splash pad, private cabanas and a full-service restaurant and bar — the longest outdoor pool season in Bucks County.",
     "Friday Night Live music, poolside karaoke and adult pool parties make it a neighborhood oasis all summer long. And the heated adult pool stays open all winter at over 80°."],
    f"{IMG}/resort_full-2.jpg", "Escape Resort", rev=True, cta=("Tour the resort", "resort.html"), tag="Open May–Oct"
) + split(
    "Wellness &amp; medicine", "05", 'One of the first clubs with an <span class="serif">in-house physician</span>',
    ["Wellness is not one size fits all. Beyond fitness, the NAC brings functional medicine, nutrition, recovery, aesthetics and concierge care together — led by Dr. Meg Zakarewicz, a double board-certified physician.",
     "Optimize your health with real data and real guidance through YOUR.Life Functional Medicine, The Well Lounge Med Spa, and our medical partners."],
    f"{IMG}/dr-meg-newtown-athletic-club-functional-medicine.jpeg", "Functional medicine", cta=("Explore wellness", "wellness.html"), tag="Dr. Meg, MD"
) + f"""
<section class="section section--light">
  <div class="wrap"><div class="cards-head">
    <div><p class="eyebrow"><span class="num">06</span> Always something happening</p>
      <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">This season at <span class="serif">the NAC</span></h2></div>
    <a class="inline-link reveal" href="blog.html">View the blog →</a></div>
    <div class="card-grid" data-stagger>
      {''.join(f'<a class="card" href="{cms_link(e.get("link","blog.html"))}"><div class="card__media card__media--wide"><img src="{cms_img(e.get("image"))}" alt="{e.get("title","")}" loading="lazy"><div class="card__label"><h3>{e.get("title","")}</h3></div></div><div class="card__below"><p>{e.get("_body","")[3:-4][:130]}</p></div></a>' for e in EVENTS[:3]) or '<p class="body-copy">Events calendar coming soon — check back for camps, classes and pool parties.</p>'}
    </div>
  </div>
</section>
""" + cta_band(
    'This is your <span class="serif">healthy place</span>',
    "Come see why members call it part world-class gym, part summer camp, part resort. Start with a complimentary pass and find your fit.",
    f"{IMG}/General-5-scaled.jpg"
)


# ============================================================ MEMBERSHIP
membership_body = hero(
    "About Membership", ["One membership.", '<span class="serif">Everything.</span>'],
    "Recognized globally as a top lifestyle club, we've hand-picked the finest amenities, programs, coaches and equipment and put them in one membership. All memberships are age-based — there's a fit for every stage of life.",
    img=f"{IMG}/General-5-scaled.jpg", crumb="Membership",
    actions=[("See Pricing", "pricing.html", True), ("Join Options", "join.html", False)],
    meta=["Age-based pricing", "Financial assistance available", "HSA / FSA accepted"], page=True,
) + f"""
<section class="section"><div class="wrap"><div class="intro-grid">
  <div><p class="eyebrow"><span class="num">01</span> What's included</p><h2 class="h-display reveal">Everything, under <span class="serif">one roof</span></h2></div>
  <div class="intro-grid__right">
    <p class="lede reveal">A 12,000 sq. ft. cardio and fitness center beaming with natural light, over 200 weekly boutique studio classes, complimentary childcare, resort-style locker rooms with steam and sauna, and the four-acre Escape Resort.</p>
    <p class="body-copy reveal">Add the poolside restaurant and bar — with Friday summer live music and weekday happy hour — and a complimentary Health Strategy Session to start, and you have more than a gym. You have your home for health.</p>
  </div>
</div></div></section>
""" + marquee(["Signature", "Couple", "Family", "Mid-Adult", "Youth Individual", "Military · Police · Fire"], accent=True) + f"""
<section class="section section--light"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">02</span> A membership for everyone</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Find your <span class="serif">fit</span></h2></div>
  <a class="inline-link reveal" href="pricing.html">View pricing →</a></div>
  <div class="rows reveal">
    <div class="row-item"><span class="row-item__idx">01</span><span class="row-item__title">Signature</span><span class="row-item__desc">For the adult individual, age 30 and up — full access to everything the NAC offers.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">02</span><span class="row-item__title">Couple</span><span class="row-item__desc">A spouse, or one parent and one child under 21 — train and recover together.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">03</span><span class="row-item__title">Family</span><span class="row-item__desc">A spouse plus up to two children under 21. Kids fitness classes included.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">04</span><span class="row-item__title">Mid-Adult</span><span class="row-item__desc">A discounted rate for ages 26–29.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">05</span><span class="row-item__title">Youth Individual</span><span class="row-item__desc">A discounted rate for ages 14–25.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">06</span><span class="row-item__title">Active Military · Police · Firefighter</span><span class="row-item__desc">A 25% discount for active, full-time service members and first responders.</span><span class="row-item__arrow">→</span></div>
  </div>
</div></section>
""" + cta_band('This is your <span class="serif">healthy place</span>', "Age-based pricing, financial assistance, HSA/FSA accepted. See your options and start with a complimentary pass.", f"{IMG}/resort_full-2.jpg", primary=("See Pricing", "pricing.html"))

# ============================================================ PRICING
pricing_body = hero(
    "Membership Pricing", ["Pricing that fits", 'your <span class="serif">life</span>'],
    "A membership to the NAC gives you access to a number of fitness, wellness and lifestyle amenities — indoor and outdoor resort-style pools, kid-friendly and family activities, boutique-style fitness classes, and luxury locker rooms. All pricing is age-based.",
    img=f"{IMG}/websiteentrance12_2000x1200.jpg", crumb="Pricing",
    actions=[("Get My Pricing", "#pricing", True), ("Compare options", "join.html", False)],
    meta=["Age-based rates", "No long-term contract", "HSA / FSA accepted"], page=True,
) + form_section(
    "pricing", "01", "See your rate",
    'Get your membership <span class="serif">pricing</span>',
    "Pricing is based on your age and the membership type that fits your household. Share a few details and a membership advisor will send your exact rate, current join offers, and answer any questions — including HSA/FSA eligibility.",
    "Send Me Pricing", light=False,
) + cta_band('Come see it for <span class="serif">yourself</span>', "The best way to understand the value is to walk the floor. Book a tour and a complimentary pass.", f"{IMG}/General-5-scaled.jpg", primary=("Book a Tour", "join.html#trial"), secondary=None)

# ============================================================ JOIN OPTIONS
JOIN_TIERS = [
    ("NAC Lifestyle", "$229", "/mo", "Full-campus access — every weight room, all pools, steam rooms and saunas, all Boutique Studio classes, plus HYROX and CrossFit. The complete NAC.", True),
    ("NPI Membership", "$169", "/mo", "Full access to the Newtown Performance Institute with HYROX and CrossFit classes — or an MMA-only membership. Built for athletes.", False),
    ("NPI Gym Access", "$79", "/mo", "Our most affordable option ever. Gym access at the Newtown Performance Institute — train your way, your schedule.", False),
]
join_body = hero(
    "Join the NAC", ["Your healthiest life", 'starts <span class="serif">here</span>'],
    "Total flexibility — choose gym-only, performance training, or full access across everything the NAC campus provides. Every membership is age-based, with financial assistance available.",
    img=f"{IMG}/fitness-center-weights-nac.jpg", crumb="Join",
    actions=[("Get a Free Pass", "#trial", True), ("See pricing", "pricing.html", False)],
    meta=["3 ways to join", "Age-based pricing", "Financial assistance available"], page=True,
) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Choose your access</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Three ways to <span class="serif">join</span></h2></div></div>
  <div class="price-grid" data-stagger>
    {''.join(f'''<div class="price-card{' price-card--feat' if feat else ''}">
      <h3>{name}</h3><div class="price-card__amt">{amt}<span>{per}</span></div>
      <p>{desc}</p><a class="btn {'btn--solid' if feat else ''}" href="#trial">Get Started <span class="arr">→</span></a>
    </div>''' for name, amt, per, desc, feat in JOIN_TIERS)}
  </div>
  <p class="form-note reveal" style="text-align:center;margin-top:24px">Adult rates shown. All NAC levels are age-based, and financial assistance is available. HSA/FSA accepted.</p>
</div></section>
""" + form_section(
    "trial", "02", "Try it on us",
    'Your complimentary pass is <span class="serif">waiting</span>',
    "Come experience the NAC for yourself — tour the club, take a class, and feel the difference. Tell us what you're interested in and a membership advisor will set up your free pass and answer every question.",
    "Claim My Free Pass", light=True,
) + cta_band('More than a club. <span class="serif">A lifestyle.</span>', "Every membership includes a complimentary Health Strategy Session to start you off right.", f"{IMG}/resort_full-2.jpg", primary=("Get a Free Pass", "#trial"), secondary=None)

# ============================================================ NAC PREMIER
premier_body = hero(
    "NAC Premier", ["Optimize your health,", 'not just your <span class="serif">workout</span>'],
    "NAC Premier is built for members who are serious about actually optimizing their health — with real data and real guidance, not guesswork. An exclusive upgrade for members who want to go further.",
    img=f"{IMG}/the-well-lounge-services-newtown-pa.jpg", crumb='<a href="wellness.html">Wellness</a> &nbsp;/&nbsp; NAC Premier',
    actions=[("Talk to Wellness", "wellness.html#contact", True)],
    meta=["$100/mo per adult add-on", "1-year commitment", "Concierge-level care"], page=True,
) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> What's included</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Concierge health, <span class="serif">optimized</span></h2></div></div>
  <div class="pillars" data-stagger>
    <div class="pillar"><span class="pillar__num">01</span><h3>Concierge Fitness Coach</h3><p>A dedicated coach who knows your goals, your data and your plan.</p></div>
    <div class="pillar"><span class="pillar__num">02</span><h3>Advanced Bloodwork</h3><p>Annual advanced bloodwork plus a functional medicine consultation to read it.</p></div>
    <div class="pillar"><span class="pillar__num">03</span><h3>Advanced Therapies</h3><p>Access to peptides, GLP-1s and HRT when clinically appropriate.</p></div>
    <div class="pillar"><span class="pillar__num">04</span><h3>Ammortal Red Light</h3><p>Red light therapy on the Ammortal chamber, four sessions every month.</p></div>
    <div class="pillar"><span class="pillar__num">05</span><h3>Unlimited Recovery</h3><p>Unlimited cryotherapy and massage chairs whenever you need to reset.</p></div>
    <div class="pillar"><span class="pillar__num">06</span><h3>Member Pricing</h3><p>15% off supplements and IV therapy across our wellness services.</p></div>
  </div>
</div></section>
""" + cta_band('Your health, <span class="serif">elevated</span>', "NAC Premier is $100/month per adult on a one-year commitment. Talk to our wellness team to get started.", f"{IMG}/3O2A5005.jpeg", primary=("Talk to Wellness", "wellness.html#contact"), secondary=None)

# ============================================================ COLLEGE
college_body = hero(
    "College Memberships", ["Home for the", '<span class="serif">break</span>'],
    "Heading home from school? Stay on track over Spring, Summer, Thanksgiving and Winter breaks with a holiday college membership — for students whose college is 25+ miles away, age 24 and under.",
    img=f"{IMG}/group-ex-classes-newtown-athletic-club-newtown-pa-12.jpg", crumb='<a href="membership.html">Membership</a> &nbsp;/&nbsp; College',
    actions=[("Get Started", "join.html#trial", True)],
    meta=["1 mo · $200", "2 mo · $400", "3 mo · $600"], page=True,
) + cta_band('Keep your <span class="serif">momentum</span>', "Train while you're home for the break with full access to the club, studios and resort.", f"{IMG}/General-5-scaled.jpg", primary=("Get Started", "join.html#trial"))

# ============================================================ GUESTS
guests_body = hero(
    "Guests", ["Bring your", '<span class="serif">people</span>'],
    "Some things are better shared. Bring up to two guests per day (age 14+) to experience everything the NAC offers — Monday through Friday during club hours, and weekends after 2pm.",
    img=f"{IMG}/group-ex-classes-newtown-athletic-club-newtown-pa-10.jpg", crumb="Guests",
    actions=[("Plan a Visit", "contact.html", True)],
    meta=["2 guests/day, age 14+", "Adult $40–$50/day", "Youth $30–$40/day"], page=True,
) + f"""
<section class="section"><div class="wrap"><div class="intro-grid">
  <div><p class="eyebrow"><span class="num">01</span> Guest policy</p><h2 class="h-display reveal">Everyone's <span class="serif">welcome</span></h2></div>
  <div class="intro-grid__right">
    <p class="lede reveal">Guests are welcome Monday–Friday during club hours and on weekends after 2pm. Guest fees are $50/day for adults (21+) and $40/day for youth (2–20) from May 1–Sep 30, and $40 / $30 from Oct 1–Apr 30.</p>
    <p class="body-copy reveal">A few member-only days keep the club special: no guests on Memorial Day, July 4th or Labor Day. Out-of-town weekly and monthly guest passes, seasonal six-month memberships, and Horsham Athletic Club reciprocity are all available — just ask.</p>
  </div>
</div></div></section>
""" + cta_band('The more, the <span class="serif">merrier</span>', "Planning to bring friends or family? We'll make sure they have a great visit.", f"{IMG}/resort_full-2.jpg")

# ============================================================ ABOUT
about_body = hero(
    "Our Story", ["Building community", 'since <span class="serif">1978</span>'],
    "What's known today as the Newtown Athletic Club opened in 1978 as the Newtown Racquetball Club — 25,000 square feet and 11 racquetball courts. Today, we're nothing like we used to be.",
    img=f"{IMG}/websiteentrance12_2000x1200.jpg", crumb="About",
    actions=[("Take a Tour", "facilities.html", True), ("Giving Back", "giving.html", False)], page=True,
) + f"""
<section class="section section--tight"><div class="wrap"><div class="intro-grid">
  <div><p class="eyebrow"><span class="num">01</span> Who we are</p><h2 class="h-display reveal">From 11 courts to <span class="serif">a lifestyle</span></h2></div>
  <div class="intro-grid__right">
    <p class="lede reveal">More than 45 years later, the NAC has grown into a 250,000 sq. ft. lifestyle club named one of the top health and wellness centers on the globe — right here in Bucks County.</p>
    <p class="body-copy reveal">Owner Jim Worthington built the club on a simple idea: this should be more than a place to work out. It should be your home for health — for every body, every age and every stage of life. That idea still drives every decision we make, from the studios we build to the community we support.</p>
  </div>
</div></div></section>
""" + split(
    "Our values", "02", 'Charity &amp; advocacy begin at <span class="serif">home</span>',
    ["For over 20 years, the NAC and its Have a Heart Foundation have contributed more than a million dollars a year to the community — funding ALS research, supporting local families, and standing behind our veterans.",
     "We believe a great club gives back. It's woven into who we are."],
    f"{IMG}/jim.jpg", "Community", rev=True, cta=("See our impact", "giving.html"), tag="$1M+ a year"
) + cta_band('Come be part of the <span class="serif">story</span>', "Forty-five years in, we're just getting started. Come see what we've built.", f"{IMG}/General-5-scaled.jpg")

# ============================================================ FACILITIES
facilities_body = hero(
    "Club Facilities", ["Your lifestyle in a", 'luxurious <span class="serif">250,000 sq. ft.</span>'],
    "A 12,000 sq. ft. cardio and fitness center beaming with natural light overlooking the four-acre resort. A boutique studio wing. Resort locker rooms with steam and sauna. A poolside restaurant and bar. This is the NAC.",
    img=f"{IMG}/General-5-scaled.jpg", crumb="Facilities",
    actions=[("Tour the Club", "join.html#trial", True)],
    meta=["250,000 sq. ft.", "12,000 sq. ft. cardio center", "4-acre resort"], page=True,
) + f"""
<section class="section section--flush"><div class="gallery wrap">
  <div class="g-item g-item--a reveal-img"><img src="{IMG}/nac-facilities-4-scaled.jpg" alt="NAC fitness floor" loading="lazy"></div>
  <div class="g-item g-item--b reveal-img"><img src="{IMG}/nac-facilities-8-scaled.jpg" alt="NAC interior" loading="lazy"></div>
  <div class="g-item g-item--c reveal-img"><img src="{IMG}/nac-facilities-10-scaled.jpg" alt="NAC studios" loading="lazy"></div>
</div></section>
""" + split(
    "Cardio &amp; fitness", "01", '12,000 sq. ft. of <span class="serif">natural light</span>',
    ["Our main fitness center beams with natural light and overlooks the resort — top-grade cardio, strength and functional equipment with room to move, never crowded."],
    f"{IMG}/nac-fitness-center-cardio-area.jpg", "Cardio center", cta=("See the Back Gym", "weight-room.html"), tag="Sunlit"
) + split(
    "Resort locker rooms", "02", 'Spa-grade comfort, <span class="serif">towel service</span> included',
    ["Resort-style locker rooms with steam room and sauna, complimentary towel service, and lounges to wind down — designed so every part of your visit feels elevated."],
    f"{IMG}/womens-locker-room-1-scaled.jpg", "Locker rooms", rev=True, tag="Steam · Sauna", light=True
) + split(
    "Dining &amp; social", "03", 'A poolside restaurant &amp; <span class="serif">bar</span>',
    ["Refuel at the poolside restaurant and bar — with weekday happy hour and Friday summer live music. Club life is as much about community as it is about fitness."],
    f"{IMG}/Poolside-Restaurant.png", "Poolside dining", cta=("Explore the resort", "resort.html"), tag="Live music Fridays"
) + cta_band('See it for <span class="serif">yourself</span>', "Photos only go so far. Book a tour and walk the 250,000 square feet in person.", f"{IMG}/websiteentrance12_2000x1200.jpg")


# ============================================================ FITNESS / PERSONAL TRAINING
fitness_body = hero(
    "Personal Training", ["Your plan should be", 'as unique as <span class="serif">you</span>'],
    "Your health journey is unique, and your plan should be too. Every membership includes a complimentary Health Strategy Session — an InBody 770 body composition assessment, a movement screen and a one-on-one consultation that turns into a personalized, actionable plan.",
    img=f"{IMG}/NAC-Expert-Personal-Training.png", crumb="Fitness",
    actions=[("Book a Strategy Session", "join.html#trial", True), ("Training options", "#options", False)],
    meta=["InBody 770 assessment", "Built for you, backed by science", "Every level &amp; goal"], page=True,
) + split(
    "Start here", "01", 'Your complimentary <span class="serif">Health Strategy Session</span>',
    ["Every NAC membership includes a session with a Health Strategy Coach. We measure where you are with an InBody 770 body composition assessment and a movement screen, then sit down to map exactly where you want to go.",
     "You leave with a clear, personalized plan — and a coach who'll help you follow it."],
    f"{IMG}/IMG_4172-scaled-e1618348177540.jpg", "Health Strategy Session", cta=("Book your session", "join.html#trial"), tag="Included"
) + f"""
<section class="section section--light" id="options"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">02</span> Ways to train</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Built for you, backed by <span class="serif">science</span></h2></div></div>
  <div class="rows reveal">
    <div class="row-item"><span class="row-item__idx">01</span><span class="row-item__title">1-on-1 Personal Training</span><span class="row-item__desc">Private sessions with a certified coach, programmed entirely around your goals and progress.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">02</span><span class="row-item__title">Small Group Training</span><span class="row-item__desc">Train in a group of six to eight — coaching and accountability with a little more energy.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">03</span><span class="row-item__title">Partner Training</span><span class="row-item__desc">Bring a friend or partner and split a session — twice the motivation.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">04</span><span class="row-item__title">Private Yoga &amp; Pilates</span><span class="row-item__desc">One-on-one instruction in the studios, at your pace and on your schedule.</span><span class="row-item__arrow">→</span></div>
  </div>
</div></section>
""" + cta_band('Stronger starts with a <span class="serif">plan</span>', "Book your complimentary Health Strategy Session and let's build the plan that fits your life.", f"{IMG}/fitness-center-weights-nac.jpg")

# ============================================================ WEIGHT ROOM (Back Gym)
weight_room_body = hero(
    "Back Gym", ["Discover your", '<span class="serif">strength</span>'],
    "Over 10,000 square feet of collegiate-style strength. Plate-loaded machines, squat racks, free weights, suspension training and turf — outfitted with Arsenal Strength, Rogue, Hammer Strength, TRX and Xult.",
    img=f"{IMG}/NAC-Weight-Room-6.jpg", crumb='<a href="fitness.html">Fitness</a> &nbsp;/&nbsp; Back Gym',
    actions=[("Get a Free Pass", "join.html#trial", True)],
    meta=["10,000+ sq. ft.", "Collegiate-style", "Arsenal · Rogue · Hammer"], page=True,
) + split(
    "Built to train hard", "01", 'Collegiate-style <span class="serif">strength</span>',
    ["The Back Gym is where serious lifters live. Plate-loaded machines — Hack Squat, Viking Press, ISO Flat Press, Incline Fly, Pendulum Squat — alongside squat racks, free weights, benches and a dedicated turf space.",
     "Equipped with the best in the business: Arsenal Strength, Rogue Fitness, Hammer Strength, TRX and Xult. Whatever your program calls for, it's here."],
    f"{IMG}/Arsenal-Strength-Equipment.png", "Back Gym", cta=("See FIT 22", "strength-studio.html"), tag="10,000+ sq. ft."
) + cta_band('Find your <span class="serif">strength</span>', "Come put your hands on the best strength equipment in Bucks County.", f"{IMG}/Back-Gym-Strength.png")

# ============================================================ FIT 22 STRENGTH STUDIO
strength_body = hero(
    "FIT 22", ["The future of strength,", 'in <span class="serif">22 minutes</span>'],
    "Discover the future of strength training with Biocircuit by Technogym. Nine intelligent machines guide your form, load and tempo automatically — a complete, full-body strength workout in just 22 minutes.",
    img=f"{IMG}/FIT-22-Strength-Studio.jpg", crumb='<a href="studios.html">Studios</a> &nbsp;/&nbsp; FIT 22',
    actions=[("Book Onboarding", "join.html#trial", True)],
    meta=["9 machines · 2 rounds", "22-minute workout", "Technogym Biocircuit"], page=True,
) + f"""
<section class="section"><div class="wrap"><div class="intro-grid">
  <div><p class="eyebrow"><span class="num">01</span> How it works</p><h2 class="h-display reveal">9 machines. 45 seconds. <span class="serif">2 rounds.</span></h2></div>
  <div class="intro-grid__right">
    <p class="lede reveal">The Biocircuit guides you from machine to machine, automatically setting your resistance and counting your time — 45 seconds per station, two rounds, 22 minutes total.</p>
    <p class="body-copy reveal">A quick 30-minute onboarding sets your personal profile so every future workout is dialed in the moment you sit down. It's the most efficient strength session in the building.</p>
  </div>
</div></div></section>
""" + cta_band('Strength, <span class="serif">simplified</span>', "Book your onboarding and feel a full-body strength workout in 22 minutes.", f"{IMG}/High-Tech-Fitness-Studio.jpg")

# ============================================================ STRETCH & RECOVERY
stretch_body = hero(
    "Stretch &amp; Recovery", ["Recovery is part of the", '<span class="serif">work</span>'],
    "One of the most overlooked aspects of exercise is recovery. Our recovery services — assisted stretch, compression and percussion therapy — help you move better, bounce back faster and feel great. Open to members and non-members.",
    img=f"{IMG}/STRETCH-45X18-24-x-36-in-1920-x-1080-px.png", crumb='<a href="fitness.html">Fitness</a> &nbsp;/&nbsp; Stretch &amp; Recovery',
    actions=[("Book a Free Stretch Demo", "join.html#trial", True)],
    meta=["1:1 assisted stretch", "NormaTec · Hyperice", "Members &amp; non-members"], page=True,
) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Ways to recover</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Move better, <span class="serif">feel better</span></h2></div></div>
  {accordion([
    ("1:1 Assisted Stretch", "One-on-one assisted stretching with a trained therapist using Hyperice tools — choose a Pliability Stretch or a Fascial Stretch (FST) session to restore range of motion."),
    ("NormaTec Compression", "Dynamic compression sleeves flush the legs and speed recovery after hard training — sit back and let the system do the work."),
    ("Foam Rolling &amp; Percussion", "Self-guided foam rolling and percussion / massage gun therapy to release tension and prep or recover the whole body."),
    ("Free Member Demo", "Members get a complimentary 30-minute stretch demo — the easiest way to feel what dedicated recovery can do for you."),
  ])}
</div></section>
""" + cta_band('Your body has earned <span class="serif">this</span>', "Book a complimentary 30-minute stretch demo and feel the difference recovery makes.", f"{IMG}/Sretch-Therapy-NAC.png")


# ============================================================ STUDIOS HUB
studios_body = hero(
    "Boutique Studio Experience", ["An unrivaled studio", '<span class="serif">fitness program</span>'],
    "We've traveled all over the globe to bring you the most luxurious and comprehensive group fitness training all under one roof. Do anything, or everything, in an unlimited amount — over 200 classes a week, all included.",
    img=f"{IMG}/studios12.jpg", crumb="Studios",
    actions=[("Get a Free Pass", "join.html#trial", True), ("Browse studios", "#studios", False)],
    meta=["10 boutique studios", "200+ classes weekly", "All included"], page=True,
) + f"""
<section class="section" id="studios"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Find your studio</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">A studio for <span class="serif">every mood</span></h2></div></div>
  <div class="card-grid" data-stagger>
    {studio_grid([
      ("THE PRACTICE — Yoga", "the-practice.html", "the-practice-1.jpg", ""),
      ("REFORM — Pilates", "reform.html", "Pilates-Classes-Newtown-PA.png", ""),
      ("PULSE", "pulse.html", "Pulse-1.jpg", ""),
      ("REV — Cycling", "rev.html", "Cycling-Studio-Newtown-PA.png", ""),
      ("Barre Lab", "barre.html", "Barre-Studio-Bucks-County-PA.png", ""),
      ("SIX ZONE", "six-zone.html", "six-zone-HIIT-classes-newtown-pa-newtown-athletic-club.jpg", ""),
      ("105 Hot Studio", "hot-105.html", "105-website1.jpg", ""),
      ("HYROX", "hyrox.html", "HYROX-Training-Classes.png", ""),
    ])}
  </div>
</div></section>
""" + cta_band('Do anything. Or <span class="serif">everything.</span>', "Every studio, every class, unlimited — all included with your membership. Come try one on us.", f"{IMG}/group-ex-classes-newtown-athletic-club-newtown-pa-15.jpg")

# ============================================================ STUDIO PAGE HELPER
def studio_page(kicker, lines, sub, hero_img, crumb, meta, intro_eyebrow, intro_h, intro_lede, intro_body, classes, cta_title, cta_text, cta_img, intro_img=None, intro_tag=None):
    body = hero(kicker, lines, sub, img=f"{IMG}/{hero_img}", crumb=f'<a href="studios.html">Studios</a> &nbsp;/&nbsp; {crumb}',
                actions=[("Take a Class, On Us", "join.html#trial", True), ("The classes", "#classes", False)], meta=meta, page=True)
    if intro_img:
        body += split(intro_eyebrow, "01", intro_h, [intro_lede, intro_body], f"{IMG}/{intro_img}", crumb, cta=("Get a free pass", "join.html#trial"), tag=intro_tag)
    else:
        body += f"""
<section class="section"><div class="wrap"><div class="intro-grid">
  <div><p class="eyebrow"><span class="num">01</span> {intro_eyebrow}</p><h2 class="h-display reveal">{intro_h}</h2></div>
  <div class="intro-grid__right"><p class="lede reveal">{intro_lede}</p><p class="body-copy reveal">{intro_body}</p></div>
</div></div></section>"""
    body += f"""
<section class="section section--light" id="classes"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">02</span> On the schedule</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">The <span class="serif">classes</span></h2></div></div>
  {accordion(classes)}
</div></section>"""
    return body + cta_band(cta_title, cta_text, f"{IMG}/{cta_img}")

# THE PRACTICE — Yoga
the_practice_body = studio_page(
    "THE PRACTICE — Yoga", ["Develop your practice", 'of body &amp; <span class="serif">mind</span>'],
    "Well-being isn't a maybe — it is vital. It is a practice. Step through nine-foot hand-carved mahogany doors onto bamboo flooring, beneath a sky-like mural and a glowing custom medallion, and let your breath lead the way.",
    "the-practice-1.jpg", "The Practice", ["50+ classes weekly", "6am–8:30pm", "Aerial yoga"],
    "A sanctuary for the senses", 'A studio that feels like a <span class="serif">retreat</span>',
    "From sunrise flows to deep evening stretches, The Practice offers more than 50 classes a week — Vinyasa, Ashtanga, Hatha, Gentle Practice, Yoga for Athletes and our signature aerial programs.",
    "Whether you're brand new or deep into your practice, our teachers meet you where you are in one of the most beautiful yoga spaces in the region.",
    [("Vinyasa Flow &amp; Ashtanga", "Dynamic, breath-led movement that builds heat, strength and focus — from beginner flows to a traditional Ashtanga practice."),
     ("Hatha &amp; Gentle Practice", "Slower, foundational classes that build alignment, mobility and calm — perfect for beginners and restorative days."),
     ("Yoga for Athletes &amp; Sculpt", "Targeted mobility and strength for active bodies, plus Yoga Sculpt that adds weights to the flow."),
     ("Aerial Yoga", "Aerial Yoga, Aerial Conditioning and Aerial Dance using suspended silks — decompress, build core strength and play."),
     ("Sunrise Flow &amp; Express Stretch", "Early-morning flows and quick express-stretch sessions to bookend your day.")],
    'Let your breath lead the <span class="serif">way</span>', "Take a yoga class on us and feel why The Practice is a place members return to again and again.",
    "yoga-classes-at-newtown-athletic-club.jpg", intro_img="the-practice-2.jpg", intro_tag="50+ classes/week")

# REFORM — Pilates
reform_body = studio_page(
    "REFORM — Pilates", ["Strengthen, lengthen,", '<span class="serif">control</span>'],
    "Two beautiful Pilates studios at the peak of the club. Reform features 13 Allegro 2 reformers by Balanced Body; our brand-new Sculpt studio adds 17 tower reformers. Strengthen, lengthen and improve posture and control under expert guidance.",
    "Pilates-Classes-Newtown-PA.png", "Reform Pilates", ["30 reformers, 2 studios", "Balanced Body", "Grip socks recommended"],
    "Two studios, one practice", 'Reform &amp; <span class="serif">Sculpt</span>',
    "The Reform studio sits at the peak of the club — 900 sq. ft., 13 Allegro 2 reformers by Balanced Body, 60-minute classes capped at 13. The new Sculpt studio brings 17 tower reformers and 50-minute sessions.",
    "Start with Intro to Reformer — required before other classes — then flow into Reform Flow, Arms/Abs &amp; Booty, Cardio to the Core and more. No shoes; grip socks strongly recommended.",
    [("Intro to Reformer", "The required first class — learn the reformer, the springs and the fundamentals so every class after feels great."),
     ("Reform Flow 1 &amp; 2", "Flowing, full-body reformer classes that build from foundational to more advanced sequencing."),
     ("Arms, Abs &amp; Booty", "Targeted sculpting on the reformer for the areas members ask for most."),
     ("Cardio to the Core", "Jumpboard-based cardio Pilates — low impact, high burn."),
     ("Mat Pilates &amp; Tower Foundations", "Classic mat work and tower-reformer foundations to round out your practice. Reservations open 25 hours prior.")],
    'Find your <span class="serif">center</span>', "Reserve a reformer and feel the difference a focused Pilates practice makes.",
    "Reform-Pilates-Studio.jpg", intro_img="newtown-athletic-club-photos-17.jpg", intro_tag="30 reformers")

# PULSE
pulse_body = studio_page(
    "PULSE", ["Lose yourself in the", '<span class="serif">beat</span>'],
    "Once the lights hit and the beat drops, you'll lose yourself in PULSE — nightclub-quality vibes in a 3,000 sq. ft. studio wrapped in a 165-inch LCD wall. Strength, dance and cardio that never feels like a workout.",
    "Pulse-1.jpg", "Pulse", ["3,000 sq. ft.", "165\" LCD wall", "30+ classes/week"],
    "Exercise in disguise", 'Where the workout feels like a <span class="serif">night out</span>',
    "PULSE brings 30+ classes a week across nine high-energy formats — from Body Pump to Zumba to Just Dance — all under a massive LCD wall and a lighting rig that turns the room into a club.",
    "Come for the energy, stay for the results. Beginners welcome in every class.",
    [("Body Pump &amp; Beginner Body Pump", "Barbell strength to music that hits every major muscle group — with a beginner version to learn the ropes."),
     ("Strength &amp; Conditioning", "Functional strength and conditioning that builds real-world power."),
     ("HIIT &amp; Kick", "High-intensity intervals with a kickboxing edge — cardio that flies by."),
     ("Zumba &amp; Latin Dance Sweat", "Exercise in disguise — Latin rhythms and dance cardio that leave you smiling."),
     ("Dance Sweat &amp; Just Dance", "Pure dance-cardio fun — no experience required, all the energy.")],
    'Turn it <span class="serif">up</span>', "Take a PULSE class on us and find out how good a workout can feel.",
    "pulseeee2.jpg", intro_img="Pulse48.jpg", intro_tag="Nightclub vibes")

# REV — Cycling
rev_body = studio_page(
    "REV — Cycling", ["Ride to the", '<span class="serif">rhythm</span>'],
    "REV is a boutique cycling studio — 2,000 sq. ft., a cinema-scale screen and Stages Cycling bikes for 34 riders. Our signature ride is Les Mills THE TRIP™, a 40-minute immersive journey through cinematic worlds.",
    "Cycling-Studio-Newtown-PA.png", "REV Cycling", ["34 Stages bikes", "Cinema-scale screen", "Les Mills THE TRIP™"],
    "Immersive by design", 'Every ride is a <span class="serif">destination</span>',
    "From rhythm rides to performance climbs, REV pairs Stages bikes with a cinema-scale screen and a sound system built to move you. THE TRIP carries you through fully animated worlds; SPRINT torches calories in 30 focused minutes.",
    "Classes run 45 or 60 minutes. SPD cleats are optional, reservations open 24 hours prior.",
    [("Les Mills THE TRIP™", "A 40-minute immersive ride through cinematic landscapes on the big screen — the closest thing to a video game you can pedal."),
     ("Rhythm &amp; Revolution", "Ride to the beat with choreography and energy, or push your output in a performance-focused class."),
     ("Journey &amp; Spin + Strength", "Endurance-style rides and combo classes that pair cycling with off-the-bike strength."),
     ("LES MILLS SPRINT", "A 30-minute high-intensity interval ride — short, brutal and incredibly effective."),
     ("RPM", "A cardio cycling workout set to motivating music — burn calories and build fitness fast.")],
    'Find your <span class="serif">cadence</span>', "Clip in for a ride on us and feel why REV regulars are hooked.",
    "Les-Mills-The-Trip-Newtown-PA.png", intro_img="Immersive-Cycling-Class-Newtown-Athletic-Club.png", intro_tag="40-min immersive")

# BARRE LAB
barre_body = studio_page(
    "Barre Lab", ["Raise the barre,", 'one pulse at a <span class="serif">time</span>'],
    "Become barre-inspired in Barre Lab — 1,000 sq. ft. of floor-to-ceiling curved glass and mirrors, handcrafted wooden barres and room for 18. Small movements, big results.",
    "Barre-Studio-Bucks-County-PA.png", "Barre Lab", ["1,000 sq. ft.", "18 spots", "45–60 min"],
    "Small moves, big results", 'Lengthen, tone and <span class="serif">pulse</span>',
    "Barre Lab blends ballet-inspired movement with strength and stretch to sculpt long, lean muscle. The curved glass studio is as beautiful as the work is effective.",
    "From Barre Foundations for newcomers to Barre Cardio and TRX Strength, there's a class for every level.",
    [("Barre Foundations", "The perfect intro — learn the positions, the barre and the format before you flow."),
     ("Barre Strength", "Add resistance and tempo for a deeper sculpt across the whole body."),
     ("Barre Cardio", "A higher-energy barre class that keeps the heart rate up."),
     ("Barre Fusion", "A blend of barre, Pilates and stretch for balance, control and grace."),
     ("TRX Strength", "Suspension-based strength that complements your barre practice.")],
    'Find your <span class="serif">poise</span>', "Take a barre class on us and feel the burn in all the right places.",
    "Barre-Classes-Newtown-PA.png", intro_img="Boutique-Barre-Studio-Newtown-PA.png", intro_tag="Curved glass studio")

# SIX ZONE
six_zone_body = studio_page(
    "SIX ZONE", ["High intensity,", 'on your <span class="serif">time</span>'],
    "Science-based interval training designed for your schedule — anytime. Six zones, five minutes each, with a new class starting every five minutes. A 35-minute, heart-rate-driven workout with no sign-up required.",
    "six-zone-HIIT-classes-newtown-pa-newtown-athletic-club.jpg", "Six Zone", ["6 zones · 5 min each", "35-minute class", "Myzone heart rate"],
    "A workout that runs on you", 'Six zones. Thirty-five <span class="serif">minutes</span>.',
    "Rotate through six stations — dumbbells, rowers, kettlebells, battle ropes, treadmills, TRX and bosu — pushing through heart-rate zones tracked on your Myzone belt. A new class kicks off every five minutes, so you train on your schedule.",
    "Monday and Tuesday hit upper body, Wednesday and Thursday lower, and Friday through Sunday go full body. No reservation needed — just show up and go.",
    [("How it works", "Six zones, five minutes each, 35 minutes total. Move when the class moves and let your Myzone belt show you the effort."),
     ("Myzone heart rate", "Color-coded heart-rate zones keep you honest and let you compete with yourself — and the room."),
     ("The weekly split", "Mon/Tue upper body, Wed/Thu lower body, Fri–Sun full body — so you can train smart all week."),
     ("No sign-up", "A new class starts every five minutes. Walk in when it suits you and a coach gets you going.")],
    'Become a <span class="serif">Six Zone junkie</span>', "Members say it's addictive. Take a class on us and see for yourself.",
    "sz046.jpg", intro_img="Six-Zone-Coach.jpg", intro_tag="New class every 5 min")

# 105 HOT STUDIO
hot_body = studio_page(
    "105 Hot Studio", ["105 is coming in", '<span class="serif">hot</span>'],
    "Step into the warmth. The 105 Hot Studio runs between 90 and 105 degrees across 2,500 square feet — heat that loosens muscles, deepens stretch and turns every class into a detoxifying, sweat-soaked reset.",
    "105-website1.jpg", "105 Hot Studio", ["2,500 sq. ft.", "90–105°F", "No shoes"],
    "Turn up the heat", 'Sweat, stretch and <span class="serif">reset</span>',
    "Heat changes everything. In the 105 Hot Studio, warmth helps you move deeper, sweat harder and feel looser — across yoga, sculpt, strength and Pilates formats for 25 to 30 people.",
    "Classes run 45 or 60 minutes. No shoes — just water, a towel and a willingness to sweat.",
    [("Hot Flow &amp; Hot Power Vinyasa", "Heated Vinyasa flows that build heat from the inside and out."),
     ("Hot Sculpt &amp; Hot Yoga Sculpt", "Add weights to the heat for a strength-and-sweat session."),
     ("Hot Strength &amp; Hot Pilates", "Strength and Pilates formats turned up to 105 for a deeper burn."),
     ("Hot Core Express", "A focused, express core class in the heat."),
     ("Hot Yin (Deep Stretch)", "Long-held, deeply restorative stretches in the warmth to open the whole body.")],
    'Come in <span class="serif">hot</span>', "Take a hot class on us and discover what training in the heat can do.",
    "105.png", intro_img="105-website1.jpg", intro_tag="90–105°F")

# HYROX
hyrox_body = hero(
    "HYROX", ["The pinnacle of", 'functional <span class="serif">fitness</span>'],
    "Discover HYROX — the global fitness race that pairs eight 1km runs with eight functional stations. As an official HYROX affiliate training club at the Newtown Performance Institute, we'll get you race-ready, whatever your starting point.",
    img=f"{IMG}/HYROX-Training-Club-Newtown-PA.png", crumb='<a href="studios.html">Studios</a> &nbsp;/&nbsp; HYROX',
    actions=[("Try HYROX", "join.html#trial", True), ("The training", "#classes", False)],
    meta=["Official HYROX affiliate", "114 Pheasant Run · NPI", "Included for members"], page=True,
) + split(
    "Train for the race", "01", 'Eight runs. Eight <span class="serif">stations</span>.',
    ["HYROX combines eight 1km runs with eight functional workout stations — SkiErg, sled push, sled pull, burpee broad jumps, rowing, farmer's carry, sandbag lunges and wall balls. It's the truest test of all-around fitness there is.",
     "Our coached classes — HYROX Endurance and Hybrid Strength — build the engine and the strength to conquer it. Included with NAC membership; non-members train for $120/month on a three-month commitment."],
    f"{IMG}/HYROX-Gym-Bucks-County-PA.png", "HYROX training", cta=("Reserve a class", "join.html#trial"), tag="8 × 1km + 8 stations"
) + f"""
<section class="section section--light" id="classes"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">02</span> The classes</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Built to <span class="serif">compete</span></h2></div></div>
  {accordion([
    ("HYROX Endurance", "Run-focused conditioning that builds the aerobic engine HYROX demands — pacing, transitions and stamina."),
    ("Hybrid Strength", "The strength side of the race — sleds, carries, lunges and wall balls trained with proper load and form."),
    ("For every level", "Brand new or chasing a podium, our coaches scale every session so you train at the right intensity."),
    ("Reservations", "Reserve your spot 24 hours prior through the NAC app. Training happens at the Newtown Performance Institute, 114 Pheasant Run."),
  ])}
</div></section>
""" + cta_band('Find your <span class="serif">limit</span>', "Try a HYROX class on us and discover the pinnacle of functional fitness.", f"{IMG}/HYROX-Training-Classes.png")


# ============================================================ SWIM
swim_body = hero(
    "Swim &amp; Aquatics", ["Made for every", '<span class="serif">swimmer</span>'],
    "Two indoor pools — including a beautifully renovated competition pool — plus the four-acre Escape Resort outdoors. From first bubbles to Masters and triathlon training, the NAC is built for life in the water, year-round.",
    img=f"{IMG}/NAC-Website-Sections-13.jpg", crumb="Aquatics",
    actions=[("Swim Lessons", "swim-lessons.html", True), ("Escape Resort", "resort.html", False)],
    meta=["2 indoor pools", "Year-round swim", "Red Cross certified"], page=True,
) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Year-round programs</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Every way to be in the <span class="serif">water</span></h2></div>
  <a class="inline-link reveal" href="swim-lessons.html">Swim lessons →</a></div>
  <div class="card-grid" data-stagger>
    <a class="card" href="swim-lessons.html"><div class="card__media"><img src="{IMG}/NAC-Website-Sections-11.jpg" alt="Swim lessons" loading="lazy"><div class="card__label"><h3>NAC Swim School</h3><span class="go">Explore →</span></div></div></a>
    <div class="card"><div class="card__media"><img src="{IMG}/NAC-Website-Sections.jpg" alt="AquaFit" loading="lazy"><div class="card__label"><h3>Aqua Fitness</h3></div></div><div class="card__below"><p>Low-impact, high-energy water workouts that are easy on the joints and tough on the calories.</p></div></div>
    <div class="card"><div class="card__media"><img src="{IMG}/NAC-Website-Sections-13.jpg" alt="Lap swim" loading="lazy"><div class="card__label"><h3>Lap &amp; Masters Swim</h3></div></div><div class="card__below"><p>Dedicated lap lanes in the renovated indoor pool, plus Masters and triathlon training for serious swimmers.</p></div></div>
    <a class="card" href="resort.html"><div class="card__media"><img src="{IMG}/Family-Pool-Resort.png" alt="Family swim" loading="lazy"><div class="card__label"><h3>Family &amp; Open Swim</h3><span class="go">Explore →</span></div></div></a>
  </div>
</div></section>
""" + split(
    "Swim all year", "02", 'Renovated, and <span class="serif">always open</span>',
    ["Our indoor pool was beautifully renovated in a $1.5 million project, giving Bucks County a year-round home for laps, lessons and play. For water safety, every swimmer completes a quick swim test before going solo.",
     "Red Cross-certified instructors, lessons from six months old, and a heated outdoor adult pool that stays open all winter — the water's always fine at the NAC."],
    f"{IMG}/Family-Swimming-Pool.png", "Indoor pool", rev=True, cta=("Lifeguard courses", "lifeguarding.html"), tag="$1.5M renovation"
) + cta_band('Dive <span class="serif">in</span>', "Sign up for lessons, swim laps, or just come splash. Everyone's welcome in the water.", f"{IMG}/swim.png")

# ============================================================ SWIM LESSONS
swim_lessons_body = hero(
    "NAC Swim School", ["From first bubbles to", '<span class="serif">first ribbons</span>'],
    "Year-round group swim lessons from six months old, taught by Red Cross-certified instructors in small ratios. Whatever your child's age or ability, we'll meet them at the water's edge and build confidence from there.",
    img=f"{IMG}/NAC-Website-Sections-11.jpg", crumb='<a href="swim.html">Aquatics</a> &nbsp;/&nbsp; Swim School',
    actions=[("Register Online", "contact.html", True)],
    meta=["From 6 months old", "30-minute lessons", "1:4–6 ratios"], page=True,
) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Lessons for every age</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Learn to <span class="serif">swim</span></h2></div></div>
  {accordion([
    ("Parent &amp; Tot / Preschool (ages 3–5)", "Levels 2–3 introduce water comfort, bubbles, floats and the very first strokes in a warm, playful setting."),
    ("School Age (ages 6–13)", "Levels 4–8 build stroke technique, endurance and water safety, progressing toward competitive readiness."),
    ("Private &amp; Semi-Private", "One-on-one or small-group lessons for kids and adults who want focused, faster progress."),
    ("Masters &amp; Triathlon", "Coached training for adult swimmers refining technique or preparing for open-water and triathlon events."),
  ])}
  <p class="form-note reveal" style="margin-top:24px">Register online or email <a href="mailto:swimacademy@newtownathletic.com" style="color:var(--accent)">swimacademy@newtownathletic.com</a>. Lessons run 30 minutes in small 1:4–6 ratios.</p>
</div></section>
""" + cta_band('Confidence starts in the <span class="serif">shallow end</span>', "Register your swimmer today and watch them grow from first bubbles to first ribbons.", f"{IMG}/NAC-Website-Sections-13.jpg", primary=("Register", "contact.html"))

# ============================================================ LIFEGUARDING
lifeguard_body = hero(
    "Certification Courses", ["Get certified at the", '<span class="serif">NAC</span>'],
    "American Red Cross certification courses — open to the public, members and non-members alike. Become a lifeguard, renew your certification, or learn CPR, Basic Life Support and babysitting skills from our certified instructors.",
    img=f"{IMG}/NAC-Website-Sections-13.jpg", crumb='<a href="swim.html">Aquatics</a> &nbsp;/&nbsp; Certifications',
    actions=[("Enroll Now", "contact.html", True)],
    meta=["American Red Cross", "Open to the public", "Lifeguard from age 15"], page=True,
) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Courses &amp; pricing</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Earn your <span class="serif">certification</span></h2></div></div>
  <div class="rows reveal">
    <div class="row-item"><span class="row-item__idx">01</span><span class="row-item__title">Lifeguard Certification</span><span class="row-item__desc">Age 15+, with a 300-yard swim prerequisite. $280 members / $350 public.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">02</span><span class="row-item__title">Lifeguard Review</span><span class="row-item__desc">Renew your current certification efficiently. $200 members / $250 public.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">03</span><span class="row-item__title">CPR &amp; Basic Life Support</span><span class="row-item__desc">Essential life-saving skills for caregivers, coaches and professionals.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">04</span><span class="row-item__title">Babysitting (ages 11–15)</span><span class="row-item__desc">Confidence and skills for young caregivers. $120 members / $150 public.</span><span class="row-item__arrow">→</span></div>
  </div>
  <p class="form-note reveal" style="margin-top:24px">Enroll online or email <a href="mailto:swimacademy@newtownathletic.com" style="color:var(--accent)">swimacademy@newtownathletic.com</a>.</p>
</div></section>
""" + cta_band('Become the one who <span class="serif">saves the day</span>', "Spots fill fast each season. Enroll in a certification course today.", f"{IMG}/NAC-Website-Sections-11.jpg", primary=("Enroll", "contact.html"))

# ============================================================ ESCAPE RESORT
resort_body = hero(
    "Escape Resort", ["A world-class resort", 'in your <span class="serif">neighborhood</span>'],
    "Four acres. Four pools. Two 35-foot water slides, a lazy river, a heated splash pad, private cabanas and a full-service restaurant and bar — your neighborhood oasis, with the longest outdoor pool season in Bucks County.",
    img=f"{IMG}/resort_full-2.jpg", crumb="Resort",
    actions=[("Get a Free Pass", "join.html#trial", True), ("What's here", "#features", False)],
    meta=["4 acres · 4 pools", "Open May–October", "Heated adult pool all winter"], page=True,
) + f"""
<section class="section section--flush"><div class="gallery wrap">
  <div class="g-item g-item--a reveal-img"><img src="{IMG}/Mega-Water-Slides.png" alt="Water slides" loading="lazy"></div>
  <div class="g-item g-item--b reveal-img"><img src="{IMG}/Adult-Pool-Resort.png" alt="Adult pool" loading="lazy"></div>
  <div class="g-item g-item--c reveal-img"><img src="{IMG}/Resort-Restaurant-Bar.png" alt="Resort restaurant and bar" loading="lazy"></div>
</div></section>
""" + f"""
<section class="section" id="features"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> The resort</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Four acres of <span class="serif">escape</span></h2></div></div>
  <div class="card-grid" data-stagger>
    <div class="card"><div class="card__media"><img src="{IMG}/Family-Pool-Resort.png" alt="Family pools" loading="lazy"><div class="card__label"><h3>Four Pools</h3></div></div><div class="card__below"><p>An adults-only pool (21+) and three family pools, plus a heated splash pad for the littlest swimmers.</p></div></div>
    <div class="card"><div class="card__media"><img src="{IMG}/Mega-Water-Slides.png" alt="Water slides and lazy river" loading="lazy"><div class="card__label"><h3>Slides &amp; Lazy River</h3></div></div><div class="card__below"><p>Two 35-foot water slides and a lazy river that winds through the heart of the resort.</p></div></div>
    <div class="card"><div class="card__media"><img src="{IMG}/Adult-Pool-Bar.png" alt="Cabanas" loading="lazy"><div class="card__label"><h3>Private Cabanas</h3></div></div><div class="card__below"><p>Reserve a cabana for 8–12 guests with a dedicated server and a complimentary bottle (21+).</p></div></div>
    <div class="card"><div class="card__media"><img src="{IMG}/Outdoor-Dining-Bucks-County-PA.png" alt="Dining" loading="lazy"><div class="card__label"><h3>Restaurant &amp; Bar</h3></div></div><div class="card__below"><p>A full-service poolside restaurant and bar — eat, drink and never leave the deck.</p></div></div>
  </div>
</div></section>
""" + split(
    "Summer nights", "02", 'The party doesn\'t stop at <span class="serif">sundown</span>',
    ["Happy Hour runs Monday–Friday from 4–6pm, Friday Night Live brings music from 6–10pm (open to the community), poolside karaoke takes over Thursday nights, and select Saturdays turn into adult pool parties from 8pm–1am.",
     "And when the season ends? The heated outdoor adult pool stays open all winter at over 80 degrees — because escape shouldn't be seasonal."],
    f"{IMG}/Swim-Resort-Bar-Newtown-PA-e1687903414718.jpg", "Resort nightlife", rev=True, cta=("See club hours", "hours.html"), tag="Friday Night Live"
) + cta_band('Your neighborhood <span class="serif">oasis</span>', "Spend a day at the resort on us — slides, sun, and a poolside drink with your name on it.", f"{IMG}/Escape-Resort-Newtown-PA.png")


# ============================================================ FAMILY HUB
family_body = hero(
    "Family &amp; Youth", ["A club the whole", 'family <span class="serif">grows up in</span>'],
    "From six weeks old to college-bound, the NAC is built for the whole family. Complimentary childcare while you train, kids fitness and dance, camps, gymnastics, swim, performance training and the easiest birthday parties you'll ever throw.",
    img=f"{IMG}/kids-fitness-classes-family-membership.jpg", crumb="Family",
    actions=[("Request a Family Trial", "join.html#trial", True), ("Explore programs", "#programs", False)],
    meta=["Childcare from 6 weeks", "Camps &amp; classes", "Youth performance"], page=True,
) + f"""
<section class="section" id="programs"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> For every age</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Made for the whole <span class="serif">crew</span></h2></div></div>
  <div class="card-grid" data-stagger>
    {studio_grid([
      ("Kids Club Childcare", "kids-club.html", "kids-fitness-classes-family-membership.jpg", ""),
      ("Kids Fitness &amp; Dance", "kids-fitness.html", "unlimited-dance-classes-newtown-pa.jpg", ""),
      ("Camp NAC", "camps.html", "NAC-Website-Sections-7.jpg", ""),
      ("Gymnastics", "gymnastics.html", "Recreational-Gymnastics.png", ""),
      ("Youth Performance", "youth-training.html", "sports-performance-training-newtown-pa.jpg", ""),
      ("Birthday Parties", "birthday-parties.html", "birthday-parties.jpg", ""),
      ("Newtown Discovery Preschool", "preschool.html", "RAY00006-scaled.jpg", ""),
      ("In-Club Golf", "golf.html", "NAC-Website-Sections-5.jpg", ""),
    ])}
  </div>
</div></section>
""" + cta_band('Where kids actually want to <span class="serif">be</span>', "Request a family trial and let the whole crew experience the NAC.", f"{IMG}/NAC-Website-Sections-8.jpg")

# ============================================================ KIDS CLUB CHILDCARE
kids_club_body = hero(
    "Kids Club", ["Workout in peace,", 'they\'ll have a <span class="serif">blast</span>'],
    "Complimentary childcare for ages six weeks and up, included with your membership — two free hours per day, per child. Drop the little ones with our caring staff and reclaim your workout.",
    img=f"{IMG}/kids-fitness-classes-family-membership.jpg", crumb='<a href="family.html">Family</a> &nbsp;/&nbsp; Kids Club',
    actions=[("Request a Family Trial", "join.html#trial", True)],
    meta=["Ages 6 weeks+", "2 free hours/day per child", "Included with membership"], page=True,
) + split(
    "Happy kids, relaxed parents", "01", 'A warm, safe place to <span class="serif">play</span>',
    ["Our Kids Club welcomes children from six weeks old. While you train, swim or take a class, our caring, trained staff keep your little ones engaged and happy in a bright, supervised space.",
     "Two hours of complimentary childcare per day, per child are included with membership — one guardian check-in per day. It's one of the most-loved perks our families have."],
    f"{IMG}/RAY00002-scaled.jpg", "Kids Club", tag="Included"
) + cta_band('Your workout, <span class="serif">uninterrupted</span>', "Bring the kids — we've got them. Request a family trial today.", f"{IMG}/RAY00029-3-scaled.jpg")

# ============================================================ KIDS FITNESS
kids_fitness_body = hero(
    "Kids Fitness Classes", ["Learn &amp; grow", '<span class="serif">together</span>'],
    "Fitness activities to learn and grow together — promoting healthy bodies and healthy minds. Modeled on the grown-up classes kids see their parents love, from cycling and HIIT to aerial dance, yoga and Zumba.",
    img=f"{IMG}/unlimited-dance-classes-newtown-pa.jpg", crumb='<a href="family.html">Family</a> &nbsp;/&nbsp; Kids Fitness',
    actions=[("See Classes", "contact.html", True)],
    meta=["Included with Family membership", "Modeled on adult classes", "Ages vary by class"], page=True,
) + f"""
<section class="section"><div class="wrap"><div class="intro-grid">
  <div><p class="eyebrow"><span class="num">01</span> Just like the grown-ups</p><h2 class="h-display reveal">Healthy bodies, <span class="serif">healthy minds</span></h2></div>
  <div class="intro-grid__right">
    <p class="lede reveal">Cycling, Power, HIIT &amp; Kick, Sports, Six Zone and Mini Six Zone, Bounce Boot Camp, Aerial Dance, The Trip, Alpha, Yoga, Aerial Yoga, Zumba, TikTok Hip Hop — plus STEAM, art and cooking electives.</p>
    <p class="body-copy reveal">Kids fitness classes are included with a Family Membership. Please note a $15 no-show fee applies. For competitive options on campus — Newtown Performance Institute, PRD Ghost Squad baseball, NAC Sharks swimming and the NAC Gymnastics Team — see our youth programs.</p>
    <div class="reveal"><a class="inline-link" href="youth-training.html">Youth performance training →</a></div>
  </div>
</div></div></section>
""" + cta_band('Movement they\'ll <span class="serif">look forward to</span>', "Family memberships include kids fitness classes. Request a family trial today.", f"{IMG}/dance-classes-newtown-pa-at-newtown-athletic-club.jpg")

# ============================================================ CAMP NAC
camps_body = hero(
    "Camp NAC", ["The best summer of", 'their <span class="serif">year</span>'],
    "Voted the best youth summer camp in Bucks County. For ages 3 to 15, Camp NAC runs out of our 40,000 sq. ft. Sports Training Center — sports, science, cooking, arts and a daily dip in the pool, all under one roof.",
    img=f"{IMG}/NAC-Website-Sections-7.jpg", crumb='<a href="family.html">Family</a> &nbsp;/&nbsp; Camp NAC',
    actions=[("Register for Camp", "contact.html", True)],
    meta=["Ages 3–15", "9am–3pm", "Daily pool time"], page=True,
) + split(
    "Summer, sorted", "01", 'Half-day, full-day &amp; <span class="serif">specialty</span> camps',
    ["Half-day camps for the youngest (ages 3–5), full-day camps, and specialty themed weeks — sports, science and STEM, cooking and arts — keep every interest covered. Every day includes pool time and plenty of fun.",
     "When school's out, our Schools Out Camp (ages 3–12) aligns with the Council Rock, Neshaminy and Pennsbury calendars — open to the public, with a discount for NAC families."],
    f"{IMG}/NAC-Website-Sections-8.jpg", "Camp NAC", rev=True, tag="Best in Bucks County"
) + cta_band('Give them a summer to <span class="serif">remember</span>', "Spots fill fast every year. Register for Camp NAC today.", f"{IMG}/NAC-Website-Sections-7.jpg", primary=("Register", "contact.html"))

# ============================================================ BIRTHDAY PARTIES
birthday_body = hero(
    "Birthday Parties", ["A party venue for", 'every <span class="serif">interest</span>'],
    "250,000 square feet of party possibilities — plus the Village Farm. Pool parties on the four-acre resort, a 65-foot floating obstacle course, themed celebrations, petting zoos and pony rides. The easiest party you'll ever throw.",
    img=f"{IMG}/birthday-parties.jpg", crumb='<a href="family.html">Family</a> &nbsp;/&nbsp; Birthday Parties',
    actions=[("Plan a Party", "contact.html", True)],
    meta=["Pool &amp; resort parties", "65-ft floating obstacle course", "Village Farm options"], page=True,
) + split(
    "Pick your party", "01", 'From pool decks to <span class="serif">pony rides</span>',
    ["Throw a splash on the four-acre resort or take on our 65-foot floating obstacle course with six stations. Prefer dry land? The Village Farm brings a jumping pillow, petting zoo, barn, pony rides — even Goat Yoga and Dinner with Ponies.",
     "Kids themed parties, On The Farm parties and pool parties — you bring the cake, we handle the rest."],
    f"{IMG}/The-Village-Farm-8.png", "Birthday parties", rev=True, cta=("Start planning", "contact.html"), tag="Bring the cake"
) + cta_band('The easiest party you\'ll ever <span class="serif">throw</span>', "Tell us the birthday kid's age and interests and we'll build the perfect party.", f"{IMG}/birthday-parties.jpg", primary=("Plan a Party", "contact.html"))

# ============================================================ GYMNASTICS
gymnastics_body = hero(
    "Gymnastics", ["Tumbling, strength &amp;", '<span class="serif">confidence</span>'],
    "Recreational and competitive gymnastics for ages four and up. From first cartwheels to the USAIGC competition team, our coaches build strength, skill and confidence in a supportive, structured program.",
    img=f"{IMG}/Recreational-Gymnastics.png", crumb='<a href="family.html">Family</a> &nbsp;/&nbsp; Gymnastics',
    actions=[("Join the Program", "contact.html", True)],
    meta=["Ages 4+", "Recreational to competitive", "USAIGC team"], page=True,
) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Find your level</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">From first cartwheel to <span class="serif">competition</span></h2></div></div>
  <div class="rows reveal">
    <div class="row-item"><span class="row-item__idx">01</span><span class="row-item__title">Recreational Team</span><span class="row-item__desc">Ages 4 and up. Mondays or Wednesdays, 5–6:30pm — skills, strength and a whole lot of fun.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">02</span><span class="row-item__title">Pre-Team</span><span class="row-item__desc">Ages 4 and up. Tuesdays and Thursdays, 5–7pm — the bridge toward competitive gymnastics.</span><span class="row-item__arrow">→</span></div>
    <div class="row-item"><span class="row-item__idx">03</span><span class="row-item__title">USAIGC Competition Team</span><span class="row-item__desc">Ages 5 and up, invite-only. Five to seven competitions a season, practicing 2–3 times a week.</span><span class="row-item__arrow">→</span></div>
  </div>
  <p class="form-note reveal" style="margin-top:24px">Questions? Email <a href="mailto:gymnastics@newtownathletic.com" style="color:var(--accent)">gymnastics@newtownathletic.com</a>.</p>
</div></section>
""" + cta_band('Build strength and <span class="serif">confidence</span>', "From recreational classes to the competition team, there's a place for your gymnast.", f"{IMG}/Competitive-Gymnastics-Team-Newtown-PA.png", primary=("Join", "contact.html"))

# ============================================================ YOUTH PERFORMANCE
youth_training_body = hero(
    "Youth Performance", ["Train like the", '<span class="serif">pros</span>'],
    "The Newtown Performance Institute — formerly Parisi Speed School — builds faster, stronger, more confident young athletes from age seven to the pros. It starts with a one-on-one evaluation and a plan built just for them.",
    img=f"{IMG}/sports-performance-training-newtown-pa.jpg", crumb='<a href="family.html">Family</a> &nbsp;/&nbsp; Youth Performance',
    actions=[("Free Speed Pass", "join.html#trial", True), ("Sports programs", "sports-center.html", False)],
    meta=["Ages 7 to Pro", "Newtown Performance Institute", "1-on-1 evaluation"], page=True,
) + split(
    "Speed, strength, confidence", "01", 'A plan built for your <span class="serif">athlete</span>',
    ["Every athlete starts with a one-on-one evaluation, so training meets them exactly where they are. From there, our coaches develop speed, agility, strength and the confidence that carries onto any field, court or mat.",
     "On campus you'll also find USAIGC gymnastics, our 40,000 sq. ft. Sports Training Center, and partner programs across baseball, soccer, field hockey and more."],
    f"{IMG}/top-notch9.jpg", "Youth performance", cta=("Explore the Sports Center", "sports-center.html"), tag="Free Speed Pass"
) + cta_band('Unlock their <span class="serif">potential</span>', "Claim a free Speed Pass and let your athlete experience performance training.", f"{IMG}/Competitive-Gymnastics-Team-Newtown-PA.png", primary=("Free Speed Pass", "join.html#trial"))

# ============================================================ SPORTS CENTER
sports_center_body = hero(
    "Sports Training Center", ["40,000 sq. ft. of", 'indoor <span class="serif">turf</span>'],
    "The Newtown Sports &amp; Events Center is a 40,000 sq. ft. indoor turfed home for travel teams, private lessons, camps and events — baseball, softball, soccer, lacrosse, field hockey and football, all year round.",
    img=f"{IMG}/sports-performance-training-newtown-pa.jpg", crumb='<a href="family.html">Family</a> &nbsp;/&nbsp; Sports Center',
    actions=[("Book the Space", "contact.html", True)],
    meta=["40,000 sq. ft.", "Indoor turf", "Teams · lessons · events"], page=True,
) + f"""
<section class="section"><div class="wrap"><div class="intro-grid">
  <div><p class="eyebrow"><span class="num">01</span> Home of champions</p><h2 class="h-display reveal">Where Bucks County <span class="serif">trains</span></h2></div>
  <div class="intro-grid__right">
    <p class="lede reveal">Home to PRD Ghost Squad travel baseball — with winter training, Parisi speed and agility, Blast Motion and Rapsodo analytics, the Motus sleeve and Baseball IQ classroom sessions — plus the Black Cats Soccer Club for ages 4–18.</p>
    <p class="body-copy reveal">Private baseball and softball lessons, lacrosse, football and field hockey round out the calendar. The space also hosts expos, parties and corporate events for Bucks County and the Princeton, NJ area.</p>
  </div>
</div></div></section>
""" + cta_band('A field, <span class="serif">indoors</span>, all year', "Booking a team practice, a lesson or an event? Let's find your time.", f"{IMG}/top-notch9.jpg", primary=("Inquire", "contact.html"))

# ============================================================ PRESCHOOL
preschool_body = hero(
    "Newtown Discovery Preschool", ["Develop the", 'whole <span class="serif">child</span>'],
    "A year-round preschool that develops the whole child — for ages six weeks to five-plus years. Enrichment powered by the NAC, registered-dietitian-approved meals included, and full or partial schedules to fit your family.",
    img=f"{IMG}/RAY00006-scaled.jpg", crumb='<a href="family.html">Family</a> &nbsp;/&nbsp; Preschool',
    actions=[("Request Info", "contact.html", True)],
    meta=["6 weeks–5+ years", "Year-round, M–F", "Dietitian-approved meals"], page=True,
) + split(
    "More than daycare", "01", 'Learning that comes <span class="serif">alive</span>',
    ["Newtown Discovery Preschool develops the whole child — cognitively, physically, socially and emotionally — with a curriculum enriched by everything the NAC offers, from swim to movement to art.",
     "Open year-round, Monday through Friday, with full and partial-day options. Registered-dietitian-approved meals are included, so kids are fueled to learn and grow."],
    f"{IMG}/RAY00002-scaled.jpg", "Preschool", rev=True, tag="Whole-child learning"
) + cta_band('Where little ones <span class="serif">flourish</span>', "Schedule a visit and see how Newtown Discovery Preschool nurtures the whole child.", f"{IMG}/RAY00029-3-scaled.jpg", primary=("Request Info", "contact.html"))

# ============================================================ IN-CLUB GOLF
golf_body = hero(
    "In-Club Golf", ["Year-round golf,", 'indoors at the <span class="serif">NAC</span>'],
    "Play, practice and improve all year in our indoor golf studio — guided by a full-time PGA Golf Professional. Open to all ages and the public, with a discount for NAC members.",
    img=f"{IMG}/NAC-Website-Sections-5.jpg", crumb='<a href="family.html">Family</a> &nbsp;/&nbsp; In-Club Golf',
    actions=[("Free Intro Session", "contact.html", True)],
    meta=["Year-round, indoors", "PGA Golf Professional", "All ages &amp; the public"], page=True,
) + split(
    "Rain or shine", "01", 'Your game, <span class="serif">all year</span>',
    ["Newtown weather never has to interrupt your game again. Our indoor golf studio lets you play simulated rounds, dial in your swing and take lessons from a full-time PGA Golf Professional — whatever the season.",
     "Membership-based and open to all ages and the public, with a discount for NAC members. Schedule a free introductory session to get started."],
    f"{IMG}/NAC-Website-Sections-5.jpg", "In-Club Golf", cta=("Book your intro", "contact.html"), tag="PGA Professional"
) + cta_band('Tee off, <span class="serif">indoors</span>', "Schedule a free introductory session and swing year-round at the NAC.", f"{IMG}/NAC-Website-Sections-5.jpg", primary=("Free Intro", "contact.html"))


# ============================================================ WELLNESS HUB
wellness_body = hero(
    "Wellness Services", ["Welcome to your", '<span class="serif">healthy place</span>'],
    "Wellness is not one size fits all. Beyond fitness, the NAC brings functional medicine, nutrition, recovery, aesthetics and concierge care together under one roof — so you can optimize your health, not just your workout.",
    img=f"{IMG}/3O2A5005.jpeg", crumb="Wellness",
    actions=[("Talk to Wellness", "#contact", True), ("Functional medicine", "functional-medicine.html", False)],
    meta=["In-house physician", "Concierge care", "NAC Premier upgrade"], page=True,
) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> A full circle of care</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Health, <span class="serif">optimized</span></h2></div></div>
  <div class="card-grid" data-stagger>
    <a class="card" href="functional-medicine.html"><div class="card__media"><img src="{IMG}/dr-meg-newtown-athletic-club-functional-medicine.jpeg" alt="Functional medicine" loading="lazy"><span class="card__num">01</span><div class="card__label"><h3>Functional Medicine</h3><span class="go">Explore →</span></div></div></a>
    <a class="card" href="nutrition.html"><div class="card__media"><img src="{IMG}/the-well-lounge-services-newtown-pa.jpg" alt="Nutrition" loading="lazy"><span class="card__num">02</span><div class="card__label"><h3>Nutrition</h3><span class="go">Explore →</span></div></div></a>
    <a class="card" href="premier.html"><div class="card__media"><img src="{IMG}/IMG_4172-scaled-e1618348177540.jpg" alt="NAC Premier" loading="lazy"><span class="card__num">03</span><div class="card__label"><h3>NAC Premier</h3><span class="go">Explore →</span></div></div></a>
    <a class="card" href="medical-partners.html"><div class="card__media"><img src="{IMG}/NAC-Wellness-Partner.png" alt="Medical partners" loading="lazy"><span class="card__num">04</span><div class="card__label"><h3>Medical Partners</h3><span class="go">Explore →</span></div></div></a>
  </div>
</div></section>
""" + split(
    "Concierge medicine", "02", 'Your physician, on <span class="serif">speed dial</span>',
    ["The NAC is one of the first health clubs in the nation with an in-house physician. Our concierge medicine gives you direct text-and-call access to your doctor from 8am to 8pm — care that fits your life, not the other way around.",
     "Pair it with The Well Lounge Med Spa and our medical partners, and your whole health lives in one place."],
    f"{IMG}/the-well-lounge-services-newtown-pa.jpg", "The Well Lounge", rev=True, cta=("Meet Dr. Meg", "functional-medicine.html"), tag="8am–8pm access"
) + form_section(
    "contact", "03", "Let's talk wellness",
    'Start your wellness <span class="serif">conversation</span>',
    "Whether you're curious about functional medicine, nutrition, recovery or NAC Premier, our wellness team will help you find the right starting point. Members receive a complimentary Health &amp; Wellness Assessment with Dr. Meg — a $300 value.",
    "Connect With Wellness", light=True,
) + cta_band('Optimize your <span class="serif">health</span>', "Real data, real guidance, real results. Start your wellness conversation today.", f"{IMG}/3O2A5005.jpeg", primary=("Talk to Wellness", "#contact"), secondary=None)

# ============================================================ FUNCTIONAL MEDICINE
functional_body = hero(
    "Functional Medicine", ["Your.Life", '<span class="serif">functional medicine</span>'],
    "Led by Dr. Meg Zakarewicz, a double board-certified physician with nearly 20 years of experience, YOUR.Life is the NAC's in-house functional and integrative medicine practice — built to reveal what's really going on and help you optimize it.",
    img=f"{IMG}/dr-meg-newtown-athletic-club-functional-medicine.jpeg", crumb='<a href="wellness.html">Wellness</a> &nbsp;/&nbsp; Functional Medicine',
    actions=[("Book an Assessment", "wellness.html#contact", True), ("The programs", "#programs", False)],
    meta=["Dr. Meg Zakarewicz, MD", "120+ biomarkers", "HSA/FSA accepted"], page=True,
) + split(
    "Meet Dr. Meg", "01", 'Medicine that looks at the <span class="serif">whole you</span>',
    ["The NAC is proud to be one of the first health clubs in the nation with an in-house physician. Dr. Meg and her team go beyond symptoms — using THE INSIDE EDGE™ diagnostics, 120+ biomarkers and genetic testing to understand your body from the inside out.",
     "From there, the YOUR.Life Transformation Method™ — Reveal, Rebuild, Elevate, Empower — guides you through a 3, 6, 9 or 12-month program tracked in the YOUR.Life Insights app."],
    f"{IMG}/3O2A5463-1-scaled.jpg", "Dr. Meg's practice", cta=("Book an assessment", "wellness.html#contact"), tag="Double board-certified"
) + f"""
<section class="section section--light" id="programs"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">02</span> Programs</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Built around <span class="serif">your biology</span></h2></div></div>
  {accordion([
    ("Functional Medicine", "Get to the root cause. Comprehensive diagnostics and a personalized plan to address the why, not just the symptoms."),
    ("Metabolic Weight Loss", "Science-backed, physician-guided weight loss that works with your metabolism and hormones — including GLP-1 protocols when appropriate."),
    ("Men's &amp; Women's Hormone Health", "Optimize energy, sleep, mood and performance with hormone-aware care, including HRT when clinically indicated."),
    ("Longevity &amp; High-Performance Optimization", "Advanced testing and protocols to extend healthspan and push your performance ceiling."),
    ("Peptide Protocols", "Targeted peptide therapies to support recovery, metabolism and longevity goals."),
  ])}
  <p class="form-note reveal" style="margin-top:24px">Members receive a complimentary Health &amp; Wellness Assessment with Dr. Meg — a $300 value. HSA/FSA accepted; no insurance required.</p>
</div></section>
""" + cta_band('Discover your <span class="serif">inside edge</span>', "Start with the Core Clarity Panel and a conversation with Dr. Meg's team.", f"{IMG}/functional-medicine-newtown-pa-at-the-NAC.png", primary=("Book an Assessment", "wellness.html#contact"), secondary=None)

# ============================================================ NUTRITION
nutrition_body = hero(
    "Nutrition", ["Food is", '<span class="serif">foundational</span>'],
    "You can't out-train your plate. Our registered dietitians build realistic, personalized nutrition plans that fit your life and your goals — and the best part: services may be covered by your insurance and are eligible for HSA coverage.",
    img=f"{IMG}/3O2A5005.jpeg", crumb='<a href="wellness.html">Wellness</a> &nbsp;/&nbsp; Nutrition',
    actions=[("Talk to a Dietitian", "wellness.html#contact", True)],
    meta=["Registered dietitians", "May be insurance-covered", "HSA eligible"], page=True,
) + split(
    "Real food, real plans", "01", 'Guidance from registered <span class="serif">dietitians</span>',
    ["Fad diets fade. Our registered dietitians focus on sustainable, personalized nutrition — working with your body composition data, your training and your real life to build a plan you can actually keep.",
     "Many sessions may be covered by your insurance and are eligible for HSA coverage. Pair nutrition with your complimentary Health Strategy Session for a complete picture."],
    f"{IMG}/IMG_4172-scaled-e1618348177540.jpg", "Nutrition coaching", rev=True, cta=("Get started", "wellness.html#contact"), tag="Insurance &amp; HSA"
) + cta_band('Fuel your <span class="serif">results</span>', "Connect with a registered dietitian and build a plan that lasts.", f"{IMG}/the-well-lounge-services-newtown-pa.jpg", primary=("Talk to a Dietitian", "wellness.html#contact"), secondary=None)

# ============================================================ MEDICAL PARTNERS
medical_body = hero(
    "Medical Partners", ["World-class care,", 'right at the <span class="serif">club</span>'],
    "Your health deserves the best — so we've partnered with leading medical providers to bring expert care right to the NAC. VIP booking, on-site concierge support, and a seamless bridge between your fitness and your healthcare.",
    img=f"{IMG}/3O2A5463-1-scaled.jpg", crumb='<a href="wellness.html">Wellness</a> &nbsp;/&nbsp; Medical Partners',
    actions=[("Learn More", "wellness.html#contact", True)],
    meta=["VIP booking", "On-site concierge", "Leading providers"], page=True,
) + f"""
<section class="section"><div class="wrap"><div class="intro-grid">
  <div><p class="eyebrow"><span class="num">01</span> Care, connected</p><h2 class="h-display reveal">Healthcare that meets you <span class="serif">where you train</span></h2></div>
  <div class="intro-grid__right">
    <p class="lede reveal">Our medical partnerships give NAC members a faster, friendlier path to expert care — from orthopedics and physical therapy to a full-service medical center — with VIP booking and on-site concierge support in the club.</p>
    <p class="body-copy reveal">Partners include leading regional providers such as Rothman Orthopaedics, Progress Physical Therapy and St. Mary Medical Center, so the gap between feeling your best and getting great care all but disappears.</p>
    <div class="reveal"><a class="inline-link" href="functional-medicine.html">Explore functional medicine →</a></div>
  </div>
</div></div></section>
""" + cta_band('Your whole health, <span class="serif">in one place</span>', "Learn how our medical partnerships make expert care easier to access.", f"{IMG}/the-well-lounge-services-newtown-pa.jpg", primary=("Learn More", "wellness.html#contact"), secondary=None)


# ============================================================ GIVING BACK
giving_body = hero(
    "Giving Back", ["Charity &amp; advocacy", 'begin at <span class="serif">home</span>'],
    "For over 20 years, the NAC and its Have a Heart Foundation have given more than a million dollars a year back to the community. A great club doesn't just build healthy bodies — it builds a healthier community.",
    img=f"{IMG}/Mended-little-hearts-NAC-Web.jpg", crumb="Giving Back",
    actions=[("Visit the Foundation", "https://nachaveaheart.org", True)],
    meta=["$1M+ a year, 20+ years", "ALS research leaders", "Veterans &amp; local families"], page=True,
) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Where we give</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">A heart for the <span class="serif">community</span></h2></div></div>
  <div class="card-grid" data-stagger>
    <div class="card"><div class="card__media card__media--wide"><img src="{IMG}/Mended-little-hearts-NAC-Web.jpg" alt="ALS research" loading="lazy"><div class="card__label"><h3>ALS Research</h3></div></div><div class="card__below"><p>Through ALS TDI, Augie's Quest and Matt's Mission, the NAC community has raised more than $2 million toward a cure.</p></div></div>
    <div class="card"><div class="card__media card__media--wide"><img src="{IMG}/jim.jpg" alt="52K in 52 Weeks" loading="lazy"><div class="card__label"><h3>52K in 52 Weeks</h3></div></div><div class="card__below"><p>Since January 2022, $1,000+ every week to local charities — over $100K given and $300K+ in goods donated.</p></div></div>
    <div class="card"><div class="card__media card__media--wide"><img src="{IMG}/sports-performance-training-newtown-pa.jpg" alt="Victor 6 veterans" loading="lazy"><div class="card__label"><h3>Victor 6 Veterans</h3></div></div><div class="card__below"><p>A free fitness program for veterans, created with Capt. David A. Christian — strength and community for those who served.</p></div></div>
  </div>
</div></section>
""" + cta_band('Join us in giving <span class="serif">back</span>', "Learn how the Have a Heart Foundation is making a difference — and how you can help.", f"{IMG}/jim.jpg", primary=("Visit the Foundation", "https://nachaveaheart.org"), secondary=None)

# ============================================================ TESTIMONIALS
testimonials_body = hero(
    "Member Stories", ["There's something here", 'for <span class="serif">everyone</span>'],
    "Part world-class gym, part summer camp, part poolside oasis, part training center — all rolled into one. Don't take our word for it. Here's what members say about their home for health.",
    img=f"{IMG}/group-ex-classes-newtown-athletic-club-newtown-pa-17.jpg", crumb="Member Stories",
    actions=[("Become a Member", "join.html", True)], page=True,
) + f"""
<section class="section"><div class="wrap"><div class="pillars" data-stagger>
  <div class="pillar"><span class="pillar__num">01</span><h3>"More than a health club"</h3><p>"This is more than a health club — this is a lifestyle. Best investment I make every month is in myself, and the NAC makes it easy."</p></div>
  <div class="pillar"><span class="pillar__num">02</span><h3>"Something for everyone"</h3><p>"Part world-class gym, part summer camp, part Vegas-poolside oasis, part training center — all rolled into one. There's something here for everyone."</p></div>
  <div class="pillar"><span class="pillar__num">03</span><h3>"A Six Zone junkie"</h3><p>"I came for the pool and stayed for the studios. Now I'm a total Six Zone junkie. The energy in this place is unmatched."</p></div>
</div></div></section>
""" + cta_band('Write your own <span class="serif">story</span>', "Members of 20, 27, even 30+ years agree — there's nowhere quite like the NAC. Come find out why.", f"{IMG}/General-5-scaled.jpg")

# ============================================================ HOURS
hours_body = hero(
    "Hours", ["When we're", '<span class="serif">open</span>'],
    "The club, the pools, the resort and our departments each keep their own schedule. Here's when you can come live your healthiest life.",
    img=f"{IMG}/websiteentrance12_2000x1200.jpg", crumb="Hours",
    actions=[("Plan a Visit", "contact.html", True)], page=True,
) + f"""
<section class="section"><div class="wrap"><div class="sched" data-stagger>
  <div class="sched__col"><h4>The Club</h4><span class="where">Main building</span><dl>
    <div><dt>Mon–Fri</dt><dd>5:00a – 11:00p</dd></div><div><dt>Sat &amp; Sun</dt><dd>6:00a – 9:00p</dd></div></dl></div>
  <div class="sched__col"><h4>Indoor Pool</h4><span class="where">Aquatics</span><dl>
    <div><dt>Club hours</dt><dd>5:00a – close</dd></div><div><dt>Family Swim</dt><dd>Fri–Sun 4–8p</dd></div></dl></div>
  <div class="sched__col"><h4>Kids Club</h4><span class="where">Childcare</span><dl>
    <div><dt>Mon–Fri AM</dt><dd>7:50a – 2:00p</dd></div><div><dt>Mon–Thu PM</dt><dd>4:00p – 7:30p</dd></div><div><dt>Sat &amp; Sun</dt><dd>7:50a – 1:00p</dd></div></dl></div>
  <div class="sched__col"><h4>Escape Resort</h4><span class="where">May–October</span><dl>
    <div><dt>Front Gate</dt><dd>Daily 9:00a – 9:00p</dd></div><div><dt>Slides</dt><dd>Mon–Thu 10–7 · Fri–Sun 11–7</dd></div><div><dt>Adult Pool</dt><dd>All winter, 80°+</dd></div></dl></div>
  <div class="sched__col"><h4>Member Services</h4><span class="where">Front desk</span><dl>
    <div><dt>Mon–Thu</dt><dd>9–1 &amp; 5–7</dd></div><div><dt>Fri &amp; Sat</dt><dd>9:00a – 1:00p</dd></div></dl></div>
  <div class="sched__col"><h4>Membership Sales</h4><span class="where">New members</span><dl>
    <div><dt>Mon–Thu</dt><dd>9:00a – 7:00p</dd></div><div><dt>Fri–Sun</dt><dd>9:00a – 4:00p</dd></div></dl></div>
</div>
<p class="body-copy reveal" style="margin-top:26px">Resort hours are weather-dependent. For café hours, holiday schedules and program-specific times, call <a href="tel:{PHONE_TEL}" style="color:var(--accent)">{PHONE}</a> or ask the front desk.</p>
</div></section>
""" + cta_band('Come live your <span class="serif">healthiest life</span>', "Whatever the hour, your home for health is ready. Start with a complimentary pass.", f"{IMG}/General-5-scaled.jpg")

# ============================================================ CONTACT
contact_body = hero(
    "Contact Us", ["Let's", '<span class="serif">connect</span>'],
    "Questions about membership, a program, an event or a partnership? We're here to help. Reach the right team below, or send us a note and we'll route it to the right person.",
    img=f"{IMG}/websiteentrance12_2000x1200.jpg", crumb="Contact",
    actions=[("Call (215) 968-0600", "tel:2159680600", True)], page=True,
) + f"""
<section class="section section--tight"><div class="wrap"><div class="loc-grid" data-stagger>
  <div class="loc-item"><h4>Visit</h4><a class="phone" href="https://maps.google.com/?q=120+Pheasant+Run+Newtown+PA+18940" target="_blank" rel="noopener">120 Pheasant Run<br>Newtown, PA 18940</a></div>
  <div class="loc-item"><h4>Main Line</h4><a class="phone" href="tel:{PHONE_TEL}">{PHONE}</a></div>
  <div class="loc-item"><h4>Membership</h4><a class="phone" href="tel:2677109228">267-710-9228 ×286</a><a href="mailto:memberadmin@newtownathletic.com" style="color:var(--accent)">memberadmin@newtownathletic.com</a></div>
  <div class="loc-item"><h4>Programs &amp; Kids</h4><a class="phone" href="tel:2159680600">215-968-0600 ×156</a><a href="mailto:programs@newtownathletic.com" style="color:var(--accent)">programs@newtownathletic.com</a></div>
  <div class="loc-item"><h4>Swim &amp; Lifeguarding</h4><a href="mailto:swimacademy@newtownathletic.com" style="color:var(--accent)">swimacademy@newtownathletic.com</a></div>
  <div class="loc-item"><h4>Gymnastics</h4><a href="mailto:gymnastics@newtownathletic.com" style="color:var(--accent)">gymnastics@newtownathletic.com</a></div>
</div></div></section>
""" + form_section(
    "reach", "01", "Send us a note",
    "We're <span class=\"serif\">listening</span>",
    "Tell us what you need and the best way to reach you. Whether it's membership, personal training, the studios, swim, family programs or wellness, we'll connect you with the right team.",
    "Send Message", light=True,
) + cta_band('Come see your <span class="serif">healthy place</span>', "The best way to know the NAC is to walk through the doors. Book a tour today.", f"{IMG}/General-5-scaled.jpg", primary=("Book a Tour", "join.html#trial"))

# ============================================================ FAQ
faq_body = hero(
    "FAQ", ["Frequently (and infrequently)", '<span class="serif">asked</span>'],
    "Everything you might want to know before your first visit — and a few things you didn't know to ask. Still curious? Our team is always happy to help.",
    img=f"{IMG}/General-5-scaled.jpg", crumb="FAQ",
    actions=[("Ask Us Anything", "contact.html", True)], page=True,
) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Good to know</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Your <span class="serif">questions</span></h2></div></div>
  {accordion([
    ("Are memberships age-based?", "Yes — all NAC memberships are age-based, with tiers for youth, mid-adult, adult and senior, plus a 25% discount for active military, police and firefighters. Financial assistance is available, and we accept HSA/FSA."),
    ("What are the age rules?", "Locker rooms are for ages 16 and up. The fitness center is open to ages 12 and up. Group classes, Six Zone and FIT 22 are for ages 14 and up. Younger members have a full slate of kids fitness classes and programs."),
    ("Is childcare really included?", "Yes. Kids Club offers two complimentary hours of childcare per day, per child, for ages six weeks and up — included with membership, with one guardian check-in per day."),
    ("Can I bring guests?", "Members may bring up to two guests per day (age 14+), Monday–Friday during club hours and weekends after 2pm. Guest fees apply, and a few member-only holidays keep the club special."),
    ("Do you welcome breastfeeding?", "Absolutely. Breastfeeding is welcome anywhere in the club, anytime. We're a family club, and we want every parent to feel comfortable and supported."),
    ("How many classes can I take?", "As many as you want — over 200 boutique studio classes a week are included with membership, across ten studios. Do anything, or everything, in an unlimited amount."),
  ])}
</div></section>
""" + cta_band('Still have <span class="serif">questions?</span>', "Our team is here to help — call, email, or just stop by the front desk.", f"{IMG}/websiteentrance12_2000x1200.jpg", primary=("Contact Us", "contact.html"))

# ============================================================ LEGAL
def legal_page(title, intro):
    return hero(title, [title], intro, img=f"{IMG}/General-5-scaled.jpg", crumb=title, page=True) + f"""
<section class="section section--tight"><div class="wrap" style="max-width:820px">
  <p class="body-copy reveal">This is a redesign demonstration of newtownathletic.com. The full {title.lower()} from the Newtown Athletic Club applies to all members and guests. For the complete, current policy, please contact us at <a href="tel:{PHONE_TEL}" style="color:var(--accent)">{PHONE}</a> or visit the front desk at 120 Pheasant Run, Newtown, PA 18940.</p>
  <p class="body-copy reveal">The Newtown Athletic Club is committed to a welcoming, inclusive experience for every member and guest — online and in the club. If you have any trouble using this site or need assistance, we're happy to help.</p>
</div></section>"""
privacy_body = legal_page("Privacy Policy", "How the Newtown Athletic Club collects, uses and protects your information.")
terms_body = legal_page("Terms of Use", "The terms that govern your use of our website and membership.")


# ============================================================ BUILD ALL
N = "Newtown Athletic Club"
PAGES = [
    ("index.html", f"{N} | Your Home for Health | Bucks County, PA", "Named one of the top lifestyle clubs on the globe — 250,000 sq. ft. of fitness, boutique studios, a four-acre resort, wellness, family programs and more in Newtown, PA. Get a free pass.", "", home_body),
    ("membership.html", f"Membership | {N}", "One age-based membership opens everything — 12,000 sq. ft. fitness center, 200+ weekly studio classes, complimentary childcare, resort-style locker rooms and the Escape Resort.", "membership.html", membership_body),
    ("pricing.html", f"Pricing | {N}", "Age-based membership pricing for the NAC — indoor and outdoor resort pools, boutique studios, family activities and luxury locker rooms. HSA/FSA accepted.", "membership.html", pricing_body),
    ("join.html", f"Join | {N}", "Three ways to join — NAC Lifestyle ($229/mo), NPI Membership ($169/mo) or NPI Gym Access ($79/mo). Get a complimentary pass and a free Health Strategy Session.", "", join_body),
    ("premier.html", f"NAC Premier | {N}", "An exclusive wellness upgrade — concierge fitness coach, advanced bloodwork, functional medicine, red light therapy, unlimited recovery and more.", "membership.html", premier_body),
    ("college-memberships.html", f"College Memberships | {N}", "Holiday and seasonal college memberships for students home on break — 1, 2 or 3 months at $200/$400/$600.", "membership.html", college_body),
    ("guests.html", f"Guests | {N}", "Bring up to two guests per day to experience the NAC. Guest policy, fees, out-of-town passes and Horsham Athletic Club reciprocity.", "membership.html", guests_body),
    ("about.html", f"Our Story | {N}", "Building community since 1978. From 11 racquetball courts to a 250,000 sq. ft. lifestyle club named one of the best on the globe.", "", about_body),
    ("facilities.html", f"Club Facilities | {N}", "A luxurious 250,000 sq. ft. — a sunlit 12,000 sq. ft. cardio center, boutique studios, resort locker rooms with steam and sauna, and a poolside restaurant and bar.", "", facilities_body),
    ("fitness.html", f"Personal Training | {N}", "Every membership includes a complimentary Health Strategy Session — InBody 770 assessment, movement screen and a personalized plan. 1-on-1, small group and partner training.", "fitness.html", fitness_body),
    ("weight-room.html", f"Back Gym Weight Room | {N}", "Over 10,000 sq. ft. of collegiate-style strength — Arsenal, Rogue, Hammer Strength, TRX and Xult. Plate-loaded machines, squat racks, free weights and turf.", "fitness.html", weight_room_body),
    ("strength-studio.html", f"FIT 22 Strength Studio | {N}", "A full-body strength workout in 22 minutes on Technogym's Biocircuit — 9 intelligent machines, 45 seconds each, two rounds.", "fitness.html", strength_body),
    ("stretch-recovery.html", f"Stretch &amp; Recovery | {N}", "Assisted stretch, NormaTec compression and percussion therapy to help you move better and recover faster. Free 30-minute demo for members.", "fitness.html", stretch_body),
    ("studios.html", f"Boutique Studios | {N}", "An unrivaled studio fitness program — yoga, pilates, cycling, barre, HIIT, hot, dance and strength across ten studios, 200+ classes a week, all included.", "studios.html", studios_body),
    ("the-practice.html", f"THE PRACTICE — Yoga | {N}", "A stunning yoga studio with 50+ classes a week — Vinyasa, Ashtanga, Hatha, Yoga for Athletes and aerial yoga, under a sky-like mural.", "studios.html", the_practice_body),
    ("reform.html", f"REFORM — Pilates | {N}", "Two Pilates studios and 30 reformers by Balanced Body — Intro to Reformer, Reform Flow, Cardio to the Core and more.", "studios.html", reform_body),
    ("pulse.html", f"PULSE | {N}", "Nightclub-quality energy in a 3,000 sq. ft. studio with a 165-inch LCD wall — Body Pump, Zumba, HIIT, dance and 30+ classes a week.", "studios.html", pulse_body),
    ("rev.html", f"REV — Cycling | {N}", "A boutique cycling studio with Stages bikes and a cinema-scale screen — featuring Les Mills THE TRIP™, SPRINT, RPM and rhythm rides.", "studios.html", rev_body),
    ("barre.html", f"Barre Lab | {N}", "Ballet-inspired strength and stretch in a 1,000 sq. ft. curved-glass studio — Barre Foundations, Strength, Cardio, Fusion and TRX.", "studios.html", barre_body),
    ("six-zone.html", f"SIX ZONE | {N}", "Science-based interval training — six zones, five minutes each, a 35-minute heart-rate-driven workout with a new class starting every five minutes.", "studios.html", six_zone_body),
    ("hot-105.html", f"105 Hot Studio | {N}", "Heated training between 90 and 105 degrees — Hot Flow, Hot Sculpt, Hot Strength, Hot Pilates and Hot Yin.", "studios.html", hot_body),
    ("hyrox.html", f"HYROX | {N}", "Official HYROX affiliate training at the Newtown Performance Institute — eight 1km runs and eight functional stations. HYROX Endurance and Hybrid Strength.", "studios.html", hyrox_body),
    ("swim.html", f"Swim &amp; Aquatics | {N}", "Two indoor pools including a renovated competition pool, swim lessons from six months, AquaFit, lap and Masters swim — plus the four-acre Escape Resort.", "resort.html", swim_body),
    ("swim-lessons.html", f"NAC Swim School | {N}", "Year-round group swim lessons from six months old, taught by Red Cross-certified instructors. Private, semi-private, Masters and triathlon options.", "resort.html", swim_lessons_body),
    ("lifeguarding.html", f"Certification Courses | {N}", "American Red Cross lifeguard, CPR, Basic Life Support and babysitting certifications — open to members and the public.", "resort.html", lifeguard_body),
    ("resort.html", f"Escape Resort | {N}", "A four-acre, four-pool outdoor resort — two 35-foot water slides, a lazy river, cabanas and a full-service bar, with the longest pool season in Bucks County.", "resort.html", resort_body),
    ("family.html", f"Family &amp; Youth | {N}", "Childcare from six weeks, kids fitness and dance, Camp NAC, gymnastics, youth performance training, swim, birthday parties, preschool and in-club golf.", "family.html", family_body),
    ("kids-club.html", f"Kids Club Childcare | {N}", "Complimentary childcare from six weeks old — two free hours per day, per child, included with membership.", "family.html", kids_club_body),
    ("kids-fitness.html", f"Kids Fitness Classes | {N}", "Cycling, HIIT, aerial dance, yoga, Zumba and more — kids fitness classes modeled on the grown-up favorites, included with a Family membership.", "family.html", kids_fitness_body),
    ("camps.html", f"Camp NAC | {N}", "Voted the best youth summer camp in Bucks County — ages 3–15, sports, STEM, cooking, arts and daily pool time in a 40,000 sq. ft. center.", "family.html", camps_body),
    ("birthday-parties.html", f"Birthday Parties | {N}", "Pool parties, a 65-foot floating obstacle course, themed celebrations and Village Farm options — the easiest party you'll ever throw.", "family.html", birthday_body),
    ("gymnastics.html", f"Gymnastics | {N}", "Recreational and competitive gymnastics for ages four and up — recreational team, pre-team and the USAIGC competition team.", "family.html", gymnastics_body),
    ("youth-training.html", f"Youth Performance | {N}", "The Newtown Performance Institute (formerly Parisi Speed School) builds speed, strength and confidence for athletes age 7 to pro.", "family.html", youth_training_body),
    ("sports-center.html", f"Sports Training Center | {N}", "A 40,000 sq. ft. indoor turf center — travel baseball, soccer, lacrosse, field hockey, private lessons, camps and event rentals.", "family.html", sports_center_body),
    ("preschool.html", f"Newtown Discovery Preschool | {N}", "A year-round preschool developing the whole child, ages six weeks to five-plus, with NAC enrichment and dietitian-approved meals included.", "family.html", preschool_body),
    ("golf.html", f"In-Club Golf | {N}", "Year-round indoor golf guided by a full-time PGA Golf Professional — open to all ages and the public, with a member discount.", "family.html", golf_body),
    ("wellness.html", f"Wellness Services | {N}", "Functional medicine, nutrition, recovery, aesthetics and concierge care under one roof — with one of the nation's first in-club physicians.", "wellness.html", wellness_body),
    ("functional-medicine.html", f"Functional Medicine | {N}", "YOUR.Life functional medicine led by Dr. Meg Zakarewicz, MD — THE INSIDE EDGE diagnostics, 120+ biomarkers, hormone health, longevity and peptide protocols.", "wellness.html", functional_body),
    ("nutrition.html", f"Nutrition | {N}", "Registered dietitians build realistic, personalized nutrition plans — many sessions may be insurance-covered and are HSA eligible.", "wellness.html", nutrition_body),
    ("medical-partners.html", f"Medical Partners | {N}", "Leading medical providers — orthopedics, physical therapy and a full-service medical center — with VIP booking and on-site concierge support.", "wellness.html", medical_body),
    ("giving.html", f"Giving Back | {N}", "The Have a Heart Foundation gives $1M+ a year to the community — ALS research, 52K in 52 Weeks, and the Victor 6 Veterans Fitness Program.", "", giving_body),
    ("testimonials.html", f"Member Stories | {N}", "Part world-class gym, part summer camp, part poolside oasis — hear what members say about their home for health.", "", testimonials_body),
    ("hours.html", f"Hours | {N}", "Club, pool, Kids Club, resort and department hours for the Newtown Athletic Club.", "", hours_body),
    ("contact.html", f"Contact | {N}", "Reach the right team at the NAC — membership, programs, swim, gymnastics and more. 120 Pheasant Run, Newtown, PA. (215) 968-0600.", "", contact_body),
    ("faq.html", f"FAQ | {N}", "Membership, age rules, childcare, guests and class questions answered — everything you need before your first visit to the NAC.", "", faq_body),
    ("privacy.html", f"Privacy Policy | {N}", "How the Newtown Athletic Club collects, uses and protects your information.", "", privacy_body),
    ("terms.html", f"Terms of Use | {N}", "The terms that govern your use of our website and membership.", "", terms_body),
    ("blog.html", f"Blog | {N}", "Member spotlights, training tips, wellness science and club news from your home for health.", "blog.html", blog_index_body()),
]

for fn, title, desc, active, body in PAGES:
    page(fn, title, desc, active, body)

for p in POSTS:
    page_sub(f"blog/{p['_slug']}.html",
             f"{p.get('title','Post')} | {N} Blog",
             p.get("excerpt", "")[:160], blog_post_body(p))

print("\nDone:", len(PAGES) + len(POSTS), "pages (", len(POSTS), "blog posts )")
