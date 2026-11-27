#!/usr/bin/env python3
"""Builds the DERMEON static site into ./site from the templates below."""
import os, json, shutil, html
from landing import L

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://dermeon.in"
PHONE = "+91 90749 03650"

NAV = [("about.html", "About"), ("doctors.html", "Doctors"), ("dermatology.html", "Dermatology"),
       ("aesthetics.html", "Aesthetics"), ("technology.html", "Technology"),
       ("hair.html", "Hair"), ("gallery.html", "Gallery"), ("contact.html", "Contact")]

def e(s): return html.escape(s, quote=True)

def head(page, title, desc):
    canon = BASE + "/" + ("" if page == "index.html" else page)
    return f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#1F1D1A">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DERMEON">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/assets/img/og-dermeon.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/emblem.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/emblem.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span>Asramam, Kollam, Kerala</span><span><a data-phone href="tel:+919074903650">{PHONE}</a> &nbsp;·&nbsp; <a data-wa href="#">WhatsApp</a></span></div></div>
<header class="site"><div class="wrap">
<a class="logo" href="index.html" aria-label="DERMEON home"><img src="assets/img/dermeon-logo.png" alt="DERMEON" width="200" height="32"><small>Your Skin, Our Priority</small></a>
<button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mainnav"><span></span><span></span><span></span></button>
<nav class="main" id="mainnav" aria-label="Main"><ul>
''' + "".join(f'<li><a href="{h}"' + (' aria-current="page"' if h == page else "") + f'>{t}</a></li>' for h, t in NAV) + '''
<li><a class="btn btn-gold" href="book.html" style="color:#fff">Book Appointment</a></li>
</ul></nav></div></header>
<main id="main">
'''

FOOT = f'''</main>
<footer class="site"><div class="wrap">
<div class="foot-grid">
<div><a class="logo" href="index.html"><img src="assets/img/dermeon-logo-light.png" alt="DERMEON" width="200" height="32" loading="lazy"><small style="color:#CDB083">Dermatology · Aesthetics · Laser</small></a>
<p style="color:#9E9486;margin-top:18px;font-size:.88rem">Dermeon Clinic (A Unit of Chaithram Healthcare). Advanced dermatology and refined aesthetics in Kollam.</p></div>
<div><h4>Treatments in Kollam</h4><ul><li><a href="acne-treatment-kollam.html">Acne Treatment</a></li><li><a href="pigmentation-melasma-treatment-kollam.html">Pigmentation &amp; Melasma</a></li><li><a href="hair-fall-treatment-kollam.html">Hair Fall Treatment</a></li><li><a href="laser-hair-removal-kollam.html">Laser Hair Removal</a></li><li><a href="anti-wrinkle-treatment-kollam.html">Anti-Wrinkle Injections</a></li><li><a href="treatments.html">All treatments</a></li></ul></div>
<div><h4>Clinic</h4><ul><li><a href="about.html">About DERMEON</a></li><li><a href="doctors.html">Our Doctors</a></li><li><a href="facilities.html">Facilities</a></li><li><a href="gallery.html">Gallery</a></li><li><a href="reviews.html">Find us on Google</a></li></ul></div>
<div><h4>Contact</h4><ul><li><span data-address>Asramam, Kollam, Kerala – 691002</span></li><li><a data-phone href="tel:+919074903650">{PHONE}</a></li><li><a data-wa href="#">WhatsApp us</a></li><li><a data-instagram href="https://www.instagram.com/dermeon_clinic/" target="_blank" rel="noopener">Instagram</a></li><li><a data-facebook href="#" target="_blank" rel="noopener">Facebook</a></li><li><a data-google href="#">Google Business Profile</a></li></ul></div>
</div>
<p class="note" style="color:#8F8678;margin-top:34px">The information on this website is for general awareness only and does not replace a consultation with a qualified doctor. Treatment suitability and results vary from person to person.</p>
<div class="foot-bottom"><span>© <span data-year>2026</span> Dermeon Clinic (A Unit of Chaithram Healthcare)</span><span><a href="privacy.html">Privacy Policy</a> · <a href="terms.html">Terms &amp; Conditions</a></span></div>
</div></footer>
<script src="assets/js/site-data.js"></script>
<script src="assets/js/main.js" defer></script>
</body></html>
'''

def page_hero(crumb, h1, p):
    return f'''<section class="page-hero"><div class="wrap"><div class="crumbs"><a href="index.html">Home</a> / {crumb}</div><h1>{h1}</h1><p>{p}</p></div></section>'''

def ph(label, cls="", mono="D"):
    return f'<div class="ph {cls}"><span class="mono">{mono}</span><span class="ph-label">{label}</span></div>'

def cta(title="Begin with a consultation", text="Every treatment plan at DERMEON starts with a doctor's assessment of your skin or hair."):
    return f'''<section class="section"><div class="wrap"><div class="cta reveal"><div><h2>{title}</h2><p>{text}</p></div>
<div class="btn-row"><a class="btn btn-gold" href="book.html">Book an Appointment</a><a class="btn btn-ghost" data-wa href="#">WhatsApp Us</a></div></div></div></section>'''

# ------------------------------------------------------------------ content
DERM = [
 ("acne", "Acne and Acne Scar Management",
  "Medical assessment and treatment of active acne, the marks it leaves behind and the textural scars that can follow.",
  ["Persistent pimples, blackheads or whiteheads", "Painful cystic or nodular acne", "Dark marks after acne", "Pitted or uneven acne scars"],
  ["Type, severity and pattern of acne", "Skin type and current skin-care routine", "Medicines, hormones or lifestyle factors that may contribute", "Scar type, to decide whether procedures are suitable"]),
 ("pigmentation", "Pigmentation and Melasma",
  "Evaluation of uneven skin tone, dark patches and melasma, with a plan that may combine medical care, sun protection and procedures.",
  ["Brown or grey patches on the face", "Uneven skin tone or tanning", "Dark spots after acne or injury", "Pigmentation around the eyes or neck"],
  ["Pattern and depth of pigmentation", "Triggers such as sun exposure, hormones or products", "Skin sensitivity before any procedure", "Long-term maintenance needs"]),
 ("allergy", "Skin Allergy and Dermatitis",
  "Diagnosis and management of itchy, red or inflamed skin, including eczema and contact dermatitis.",
  ["Itching, redness or rashes", "Dry, scaly or cracked skin", "Reactions to cosmetics, metals or chemicals", "Recurring eczema flares"],
  ["Detailed history of symptoms and triggers", "Examination of the affected skin", "Review of products and exposures", "Tests where clinically needed"]),
 ("hairfall", "Hair Fall and Scalp Disorders",
  "Assessment of increased hair shedding, thinning and conditions affecting the scalp.",
  ["Increased hair fall or thinning", "Widening parting or receding hairline", "Patchy hair loss", "Itchy or painful scalp"],
  ["Pattern and duration of hair loss", "Scalp examination", "Health, nutrition and medicine history", "Blood tests where clinically needed"]),
 ("dandruff", "Dandruff and Scalp Care",
  "Medical care for flaking, itching and oily or dry scalp conditions.",
  ["Persistent flakes", "Itchy or oily scalp", "Redness along the hairline", "Dandruff returning after treatment"],
  ["Type of scaling and scalp condition", "Hair-care habits and products", "Related skin conditions", "Suitable medicated care"]),
 ("rejuvenation", "Skin Rejuvenation",
  "Doctor-guided plans to improve skin texture, glow and early signs of ageing.",
  ["Dull or tired-looking skin", "Fine lines and early ageing", "Uneven texture or open pores", "Preparing skin for an occasion"],
  ["Skin type and concerns", "Lifestyle and sun exposure", "Suitability for peels, lasers or injectables", "A realistic, staged plan"]),
 ("medical", "Other Medical Dermatology Services",
  "Consultation for a wide range of skin, hair and nail conditions.",
  ["Warts, skin tags and moles", "Fungal and bacterial skin infections", "Nail problems", "Psoriasis, vitiligo and other chronic conditions"],
  ["Clinical examination", "History of the condition", "Investigations where needed", "Treatment and follow-up plan"]),
]

# (id, name, what, reasons, evaluation, draft)
AES = [
 ("botox", "Anti-Wrinkle Injections (Botulinum Toxin)", "A prescription injectable used to soften dynamic expression lines, such as forehead lines and crow's feet, by relaxing the targeted muscles.", ["Forehead lines", "Frown lines between the brows", "Crow's feet"], "The doctor reviews facial anatomy, expression lines, medical history and expectations before planning doses and areas.", False),
 ("fillers", "Dermal Fillers", "Injectable gels, commonly hyaluronic-acid based, used to restore volume or refine contours.", ["Under-eye hollows", "Lip definition", "Cheek or chin contour", "Deep folds"], "Facial proportions, skin quality and safety factors are assessed, and the plan is discussed in detail.", False),
 ("skinboosters", "Skin Boosters", "Micro-injections designed to improve skin hydration and quality.", ["Dehydrated skin", "Fine crepey lines", "Dull skin texture"], "Skin type and goals are reviewed to decide whether skin boosters are suitable.", True),
 ("peels", "Chemical Peels", "Controlled application of peeling agents to improve texture, tone and certain acne-related concerns.", ["Uneven tone", "Acne and acne marks", "Rough texture"], "The doctor chooses the peel type and strength after checking skin type, sensitivity and pigmentation risk.", True),
 ("hydrafacial", "HydraFacial", "A multi-step facial that cleanses, exfoliates and hydrates the skin.", ["Congested pores", "Dull skin", "Pre-event skin care"], "Skin condition is checked to make sure the facial is appropriate.", False),
 ("hifu", "HIFU", "High-Intensity Focused Ultrasound, a non-surgical treatment used for skin lifting and tightening.", ["Mild skin laxity", "Jawline definition", "Early sagging"], "The degree of laxity, skin thickness and expectations are assessed before treatment.", False),
 ("mnrf", "MNRF (Microneedling Radiofrequency)", "Combines fine microneedles with radiofrequency energy to stimulate the skin's repair process.", ["Acne scars", "Open pores", "Skin texture"], "Scar type, skin type and downtime are discussed before deciding on sessions.", False),
 ("rf", "RF Skin Tightening", "Radiofrequency energy used to heat deeper skin layers to support firmness.", ["Mild skin laxity", "Skin firmness"], "The doctor assesses skin laxity and suitability.", True),
 ("carbon", "Carbon Laser Peel", "A laser treatment performed over a thin carbon layer, often used for oily skin and dullness.", ["Oily skin", "Dull skin", "Enlarged pores"], "Skin type and pigmentation risk are reviewed before treatment.", False),
 ("pico", "Pico Laser Treatments", "Picosecond laser treatments used for selected pigmentation concerns and skin rejuvenation.", ["Pigmentation", "Uneven tone", "Tattoo removal"], "The type and depth of pigmentation are evaluated to decide on settings and sessions.", False),
 ("co2", "CO2 Fractional Laser", "A fractional ablative laser used for resurfacing, commonly for scars and texture.", ["Acne scars", "Uneven texture", "Fine lines"], "Skin type, downtime and aftercare are discussed carefully before treatment.", False),
 ("laserrejuv", "Laser Skin Rejuvenation", "Laser-based treatments aimed at improving overall skin quality and tone.", ["Dullness", "Uneven tone", "Texture"], "The doctor selects a suitable laser approach after skin assessment.", True),
 ("prp", "PRP (Platelet-Rich Plasma)", "Uses a concentrate prepared from the patient's own blood, applied for selected skin and hair concerns.", ["Hair thinning", "Skin quality"], "Medical history and suitability are reviewed before PRP is advised.", True),
 ("gfc", "GFC (Growth Factor Concentrate)", "A concentrate derived from the patient's own blood, used in selected hair-loss plans.", ["Hair thinning", "Hair fall"], "Hair-loss pattern and cause are assessed before GFC is considered.", True),
 ("exosome", "Exosome Treatments", "A newer category of regenerative skin and hair treatments.", ["Skin quality", "Hair concerns"], "The doctor explains current evidence, suitability and alternatives.", True),
 ("lhr", "Laser Hair Removal", "Laser-based reduction of unwanted hair over a series of sessions.", ["Unwanted facial or body hair", "Ingrown hair", "Frequent shaving or waxing"], "Hair colour, skin type and any hormonal causes are checked before starting.", False),
 ("electrolysis", "Electrolysis", "Treats individual hair follicles with a fine probe; useful for small areas.", ["Fine or light hair", "Small areas"], "The doctor reviews the area and hair type.", True),
 ("tattoo", "Tattoo Removal", "Laser treatment to gradually lighten unwanted tattoos over several sessions.", ["Unwanted tattoos", "Faded or partial tattoos"], "Tattoo colours, age and skin type are evaluated to estimate sessions.", True),
]

TECH = [
 ("diode", "Diode Laser – Diolash Signature 4D", "Laser hair reduction", ["Laser hair removal for face and body"]),
 ("pico", "Pico Laser / Picosecond Laser", "Pigmentation and tattoo care", ["Selected pigmentation concerns", "Tattoo removal", "Skin rejuvenation"]),
 ("co2", "CO2 Fractional Laser", "Skin resurfacing", ["Acne scars", "Skin texture"]),
 ("hifu", "HIFU", "Non-surgical lifting", ["Skin lifting and tightening"]),
 ("mnrf", "MNRF", "Microneedling radiofrequency", ["Acne scars", "Open pores", "Skin texture"]),
]

FAQ = [
 ("Do I need a consultation before a treatment?", "Yes. Every procedure at DERMEON begins with a doctor's consultation, so that the treatment is suitable for your skin, hair and health."),
 ("Is my appointment confirmed when I submit the online form?", "No. The online form sends an appointment request. Our team will call or WhatsApp you to confirm the date and time."),
 ("How many sessions will I need?", "It depends on the condition, skin type and treatment chosen. Your doctor will explain the expected number of sessions after examining you."),
 ("Are results guaranteed?", "No medical or aesthetic treatment can guarantee results. Outcomes vary between individuals, and your doctor will discuss realistic expectations with you."),
 ("Is DERMEON open on Sunday?", "Yes. The clinic is open every day, including Sunday, from 9:30 AM to 7:00 PM. Doctor consultations are from 10:00 AM to 7:00 PM."),
 ("Where is DERMEON located?", "DERMEON is at Asramam, Kollam, Kerala – 691002. You can find directions on our Contact page."),
]

def service_block(sid, name, what, reasons, evals, dept, draft=False):
    draft = False
    tag = '<span class="tag draft">Ask about availability</span>' if draft else ""
    return f'''<article class="service reveal" id="{sid}">
<div>{ph(name.split(" (")[0], "sq", name[0])}</div>
<div>{tag}<h3>{name}</h3><p>{what}</p>
<div class="cols"><div><h4>Common reasons to consult</h4><ul>{"".join(f"<li>{r}</li>" for r in reasons)}</ul></div>
<div><h4>How the doctor evaluates</h4>{"<ul>" + "".join(f"<li>{x}</li>" for x in evals) + "</ul>" if isinstance(evals, list) else f"<p>{evals}</p>"}</div></div>
<p style="margin-top:18px"><a class="btn btn-ghost" href="book.html?dept={dept.replace(" ", "+")}&amp;t={name.split(" (")[0].replace(" ", "+")}">Book consultation</a></p></div></article>'''

def clinic_schema():
    return '''<script type="application/ld+json">''' + json.dumps({
        "@context": "https://schema.org", "@type": "MedicalClinic", "name": "DERMEON Clinic",
        "alternateName": "Dermeon Clinic (A Unit of Chaithram Healthcare)", "url": BASE + "/",
        "telephone": "+91-90749-03650", "email": "info@dermeon.in", "medicalSpecialty": ["Dermatology"], "geo": {"@type": "GeoCoordinates", "latitude": 8.8930449, "longitude": 76.5919402}, "hasMap": "https://maps.google.com/?cid=14195985572850679739", "priceRange": "₹₹", "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "09:30", "closes": "19:00"}],
        "address": {"@type": "PostalAddress", "streetAddress": "Asramam", "addressLocality": "Kollam", "addressRegion": "Kerala", "postalCode": "691002", "addressCountry": "IN"},
        "sameAs": ["https://www.instagram.com/dermeon_clinic/"], "logo": BASE + "/assets/img/dermeon-logo.png", "image": BASE + "/assets/img/og-dermeon.jpg",
        "availableService": [{"@type": "MedicalProcedure", "name": n} for _, n, *_ in AES if True][:0] or None
    }, ensure_ascii=False).replace(', "availableService": null', "") + "</script>\n"

def svc_schema(names):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "ItemList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": n, "provider": {"@type": "MedicalClinic", "name": "DERMEON Clinic", "url": BASE + "/"}, "areaServed": "Kollam, Kerala"}} for i, n in enumerate(names)]}) + "</script>\n"

pages = {}
SHORT = {"acne": "Treatment for active acne, acne marks and acne scars.", "pigmentation": "Care for dark patches, melasma and uneven skin tone.",
         "allergy": "Diagnosis and care of itchy, red or inflamed skin.", "hairfall": "Finding the cause of hair fall and treating the scalp."}

# ------------------------------------------------------------------ HOME
home = head("index.html", "DERMEON | Dermatology &amp; Aesthetic Clinic in Kollam – Asramam",
            "DERMEON is a dermatology, medical cosmetology and aesthetic medicine clinic at Asramam, Kollam. Skin, hair and laser treatments planned by doctors. Book an appointment.")
home += clinic_schema()
home += f'''<section class="hero"><div class="media" aria-hidden="true"></div><img class="hero-emblem" src="assets/img/emblem.png" alt="" aria-hidden="true">
<div class="wrap"><div class="content">
<span class="eyebrow" style="color:#CDB083">Dermatology · Aesthetics · Laser · Kollam</span>
<h1>Your Skin, Our Priority.</h1>
<div class="sub">Advanced Dermatology. Refined Aesthetics.</div>
<p>A doctor-led clinic in Asramam, Kollam for skin, hair and aesthetic care, with treatment plans made around your skin.</p>
<div class="btn-row" style="margin-top:28px"><a class="btn btn-gold" href="book.html">Book an Appointment</a><a class="btn btn-ghost" href="#treatments">Explore Treatments</a></div>
<div class="hero-badges"><div><strong>Doctor-led</strong>Every plan</div><div><strong>Asramam</strong>Central Kollam</div><div><strong>Open all days</strong>Including Sunday</div></div>
</div></div></section>

<section class="section"><div class="wrap split">
<div class="reveal"><span class="eyebrow">Welcome to DERMEON</span><h2>Medical care for skin and hair, with an eye for refined aesthetics.</h2><hr class="rule">
<p class="lead">DERMEON brings together dermatology, medical cosmetology and aesthetic medicine under one roof. Each visit begins with a doctor's assessment, so that the care you receive is suitable for your skin, your health and your goals.</p>
<a class="textlink" href="about.html">About our clinic →</a></div>
<div class="reveal">{ph("Clinic photograph – to be added", "tall")}</div></div></section>

<section class="section alt"><div class="wrap">
<div class="center reveal"><span class="eyebrow">About our clinic</span><h2>Our medical expertise</h2><hr class="rule"><p class="lead">Two dermatologists and an aesthetic physician work together on diagnosis, treatment planning and follow-up.</p></div>
<div class="grid g3" style="margin-top:44px">
<div class="card reveal"><div class="icon">I</div><h3>Dermatology</h3><p>Diagnosis and treatment of skin, hair, scalp and nail conditions.</p><a class="textlink more" href="dermatology.html">Dermatology services</a></div>
<div class="card reveal"><div class="icon">II</div><h3>Aesthetic Medicine</h3><p>Injectables, facials, peels and skin-quality treatments planned by doctors.</p><a class="textlink more" href="aesthetics.html">Aesthetic treatments</a></div>
<div class="card reveal"><div class="icon">III</div><h3>Laser Technology</h3><p>Laser and energy-based devices for hair reduction, pigmentation, scars and skin tightening.</p><a class="textlink more" href="technology.html">Our technology</a></div>
</div></div></section>

<section class="section" id="treatments"><div class="wrap">
<div class="reveal"><span class="eyebrow">Dermatology services</span><h2>Care for common and complex skin concerns</h2><hr class="rule"></div>
<div class="grid g4">''' + "".join(f'<a class="card reveal" style="text-decoration:none" href="dermatology.html#{sid}"><h3 style="font-size:1.3rem">{n}</h3><p style="font-size:.92rem">{SHORT[sid]}</p></a>' for sid, n, w, *_ in DERM[:4]) + '''</div></div></section>

<section class="section dark"><div class="wrap split">
<div class="reveal"><span class="eyebrow" style="color:#CDB083">Aesthetic treatments</span><h2>Refined results begin with a careful plan</h2><hr class="rule">
<p>From anti-wrinkle injections and dermal fillers to HydraFacial, HIFU and MNRF, aesthetic treatments at DERMEON are chosen after a doctor has assessed your skin and discussed what is realistic for you.</p>
<div style="margin:18px 0 26px">''' + "".join(f'<span class="tag" style="color:#CDB083">{n.split(" (")[0]}</span>' for _, n, *_, d in AES if not d) + '''</div>
<a class="btn btn-gold" href="aesthetics.html">View aesthetic treatments</a></div>
<div class="reveal">''' + ph("Treatment room – to be added", "tall") + '''</div></div></section>

<section class="section"><div class="wrap">
<div class="center reveal"><span class="eyebrow">Advanced laser technology</span><h2>Technology chosen for clinical use</h2><hr class="rule"></div>
<div class="grid g3" style="margin-top:40px">''' + "".join(f'<div class="card reveal">{ph("Device photograph – to be added", "wide", n[0])}<h3 style="margin-top:18px">{n}</h3><p>{u}</p></div>' for _, n, u, _a in TECH[:3]) + '''</div>
<p class="center" style="margin-top:30px"><a class="textlink" href="technology.html">See all technology →</a></p></div></section>

<section class="section alt"><div class="wrap split rev">
<div class="reveal"><span class="eyebrow">Hair restoration</span><h2>Understanding hair loss before treating it</h2><hr class="rule">
<p>Hair fall has many causes. Our doctors begin with a scalp assessment and history, then discuss medical treatment and procedures that may suit you.</p>
<a class="btn btn-dark" href="hair.html">Hair restoration</a></div>
<div class="reveal">''' + ph("Scalp assessment – photo to be added", "tall", "H") + '''</div></div></section>

<section class="section"><div class="wrap">
<div class="center reveal"><span class="eyebrow">Our clinical facilities</span><h2>A calm, clinical space</h2><hr class="rule"><p class="lead">Dedicated consultation rooms, treatment rooms and laser rooms in a multispeciality clinical environment.</p></div>
<div class="grid g4" style="margin-top:40px">''' + "".join(f'<div class="reveal">{ph(x, "sq", x[0])}</div>' for x in ["Reception", "Consultation room", "Treatment room", "Laser room"]) + '''</div>
<p class="center" style="margin-top:28px"><a class="textlink" href="facilities.html">Explore our facilities →</a></p></div></section>

<section class="section alt"><div class="wrap">
<div class="center reveal"><span class="eyebrow">Why choose DERMEON?</span><h2>What patients can expect</h2><hr class="rule"></div>
<div class="grid g4" style="margin-top:40px">
<div class="card reveal"><h3>Doctor-led care</h3><p>Every treatment plan starts with a consultation with our doctors.</p></div>
<div class="card reveal"><h3>Personal plans</h3><p>Treatments are chosen for your skin type, concern and lifestyle.</p></div>
<div class="card reveal"><h3>Modern equipment</h3><p>Laser and aesthetic devices used under medical supervision.</p></div>
<div class="card reveal"><h3>Honest advice</h3><p>Clear information on sessions, aftercare and realistic expectations.</p></div>
</div></div></section>

<section class="section"><div class="wrap">
<div class="center reveal"><span class="eyebrow">Treatments in Kollam</span><h2>Find care for your concern</h2><hr class="rule"></div>
<div class="grid g4" style="margin-top:34px">''' + "".join(f'<a class="card reveal" style="text-decoration:none" href="{x[0]}.html"><h3 style="font-size:1.15rem">{x[1]}</h3><p style="font-size:.88rem">{x[4].split(". ")[0]}.</p></a>' for x in L) + '''</div>
<p class="center" style="margin-top:26px"><a class="textlink" href="treatments.html">All treatments →</a></p></div></section>

<section class="section alt"><div class="wrap" style="max-width:860px">
<div class="center reveal"><span class="eyebrow">Frequently asked questions</span><h2>Before your visit</h2><hr class="rule"></div>
''' + "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '''
</div></section>

<section class="section"><div class="wrap split">
<div class="reveal"><span class="eyebrow">Contact and location</span><h2>Visit DERMEON in Asramam, Kollam</h2><hr class="rule">
<ul class="info-list"><li><span>Address</span><div data-address>Asramam, Kollam, Kerala – 691002</div></li><li><span>Phone</span><a data-phone href="tel:+919074903650">+91 90749 03650</a></li><li><span>Hours</span><div data-hours></div></li></ul>
<div class="btn-row" style="margin-top:24px"><a class="btn btn-gold" href="book.html">Book an Appointment</a><a class="btn btn-ghost" data-wa href="#">WhatsApp</a></div></div>
<div class="reveal"><iframe class="map" data-map title="DERMEON location on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div></section>
''' + cta() + FOOT
pages["index.html"] = home

# ------------------------------------------------------------------ ABOUT
about = head("about.html", "About DERMEON | Dermatology &amp; Aesthetic Medicine Clinic, Kollam",
             "Learn about DERMEON, a doctor-led dermatology and aesthetic medicine clinic at Asramam, Kollam, a unit of Chaithram Healthcare.")
about += page_hero("About", "About DERMEON", "A dermatology, medical cosmetology and aesthetic medicine clinic in Asramam, Kollam. A unit of Chaithram Healthcare.")
blocks = [
 ("Our clinic", "DERMEON is a doctor-led clinic for skin, hair and aesthetic care. Our team includes two dermatologists and a managing director who is a medical doctor and aesthetic physician. Patients come to us for medical dermatology, cosmetology procedures, laser treatments and hair care."),
 ("Our vision", "To be a trusted name in Kollam for dermatology and aesthetic medicine, where patients receive careful, honest and modern care."),
 ("Our mission", "To diagnose accurately, explain clearly and treat safely, using treatment plans that respect each patient's skin, health and goals."),
 ("Clinical philosophy", "We believe good aesthetic results come from good medicine. A correct diagnosis comes before any procedure, and we recommend treatment only when it is suitable."),
 ("Patient-centred care", "We listen first. Your concerns, expectations, budget and time are part of every plan, and we explain sessions, aftercare and possible side effects before you decide."),
 ("Medical expertise", "Our dermatologists manage conditions such as acne, pigmentation, allergies, hair loss and scalp disorders. Our aesthetic physician leads injectable and skin-quality treatments."),
 ("Advanced infrastructure", "The clinic has dedicated consultation and treatment rooms and modern laser and aesthetic equipment."),
 ("Safety and hygiene", "We follow clinical hygiene practices for consultations and procedures, and patients receive aftercare instructions for every treatment."),
 ("Personalised treatment planning", "No two patients are the same. Your plan may combine medical treatment, skin care advice and procedures, and is reviewed at follow-up visits."),
]
about += '<section class="section"><div class="wrap split"><div class="reveal">' + ph("Clinic photograph – to be added", "tall") + '</div><div class="reveal"><span class="eyebrow">Introduction</span><h2>Advanced dermatology. Refined aesthetics.</h2><hr class="rule"><p class="lead">' + blocks[0][1] + '</p></div></div></section>'
about += '<section class="section alt"><div class="wrap"><div class="grid g2">' + "".join(f'<div class="card reveal"><h3>{t}</h3><p>{p}</p></div>' for t, p in blocks[1:]) + '</div></div></section>'
about += cta() + FOOT
pages["about.html"] = about

# ------------------------------------------------------------------ DOCTORS
doc = head("doctors.html", "Our Doctors | Dermatologists &amp; Aesthetic Physician – DERMEON Kollam",
           "Meet the dermatologists and aesthetic physician at DERMEON, Asramam, Kollam.")
doc += page_hero("Our Doctors", "Our Doctors", "Two dermatologists and an aesthetic physician. Full profiles will be added soon.")
doc += '<section class="section"><div class="wrap"><div class="grid g3" data-doctors></div></div></section>' + cta() + FOOT
pages["doctors.html"] = doc

# ------------------------------------------------------------------ DERMATOLOGY
dm = head("dermatology.html", "Dermatology Services in Kollam | Acne, Pigmentation, Hair Fall – DERMEON",
          "Dermatologist consultations in Kollam for acne and acne scars, pigmentation and melasma, skin allergy, hair fall, dandruff and other skin conditions.")
dm += svc_schema([n for _, n, *_ in DERM])
dm += page_hero("Dermatology", "Dermatology Services", "Medical diagnosis and treatment of skin, hair, scalp and nail conditions by our dermatologists.")
dm += '<section class="section"><div class="wrap"><div class="toc">' + "".join(f'<a href="#{s}">{n}</a>' for s, n, *_ in DERM) + '</div>'
dm += "".join(service_block(s, n, w, r, ev, "Dermatology") for s, n, w, r, ev in DERM)
dm += '<p class="disclaimer">Results vary between individuals. A consultation is needed to confirm the diagnosis and the right treatment.</p></div></section>' + cta() + FOOT
pages["dermatology.html"] = dm

# ------------------------------------------------------------------ AESTHETICS
am = head("aesthetics.html", "Aesthetic Treatments in Kollam | Anti-Wrinkle, Fillers, HIFU, Laser – DERMEON",
          "Doctor-led aesthetic medicine in Kollam: anti-wrinkle injections, dermal fillers, HydraFacial, HIFU, MNRF, Pico and CO2 laser, laser hair removal and more at DERMEON.")
am += svc_schema([n for _, n, *_ in AES])
am += page_hero("Aesthetic Medicine", "Aesthetic Medicine", "Treatments chosen after a doctor's assessment, with clear information on sessions, aftercare and realistic expectations.")
am += '<section class="section"><div class="wrap"><div class="toc">' + "".join(f'<a href="#{s}">{n.split(" (")[0]}</a>' for s, n, *_ in AES) + '</div>'
def dept_for(sid): return "Laser Treatments" if sid in ("pico", "co2", "laserrejuv", "lhr", "electrolysis", "tattoo", "carbon") else ("Hair Restoration" if sid in ("gfc",) else "Aesthetic Medicine")
am += "".join(service_block(s, n, w, r, ev, dept_for(s), d) for s, n, w, r, ev, d in AES)
am += '<p class="disclaimer">Aesthetic treatments are medical procedures. Suitability, number of sessions and results differ for each person and are discussed at consultation. We do not publish before-and-after photographs without patient consent.</p></div></section>' + cta() + FOOT
pages["aesthetics.html"] = am

# ------------------------------------------------------------------ TECHNOLOGY
tc = head("technology.html", "Laser &amp; Advanced Technology | Diode, Pico, CO2, HIFU, MNRF – DERMEON Kollam",
          "Laser and aesthetic technology at DERMEON, Kollam: diode laser hair reduction, pico laser, CO2 fractional laser, HIFU and MNRF.")
tc += page_hero("Laser &amp; Technology", "Laser and Advanced Technology", "Energy-based devices used under medical supervision, after a doctor confirms they suit your skin.")
tc += '<section class="section"><div class="wrap"><div class="grid g2">' + "".join(
    f'<article class="card reveal" id="{s}">{ph("Machine photograph – to be added", "wide", n[0])}<span class="eyebrow" style="margin-top:20px">{u}</span><h3>{n}</h3><h4 style="font-family:var(--sans);font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-ink);margin-top:14px">Common clinical applications</h4><ul>{"".join(f"<li>{x}</li>" for x in a)}</ul><a class="btn btn-ghost" href="book.html?dept=Laser+Treatments">Book consultation</a></article>'
    for s, n, u, a in TECH) + '</div><p class="disclaimer">Device descriptions are general. Specifications and suitability are explained by our doctors at consultation.</p></div></section>' + cta() + FOOT
pages["technology.html"] = tc

# ------------------------------------------------------------------ HAIR
hr = head("hair.html", "Hair Fall &amp; Hair Restoration Treatment in Kollam – DERMEON",
          "Hair loss consultation, scalp assessment, PRP and GFC hair treatments planned by doctors at DERMEON, Asramam, Kollam.")
hair = [
 ("consult", "Hair Loss Consultation", "A doctor's consultation to understand why hair fall is happening.", ["Increased hair fall", "Thinning or receding hairline", "Patchy hair loss"], ["History, diet, stress and medicines", "Family history", "Blood tests where needed"]),
 ("scalp", "Scalp Assessment", "Examination of the scalp and hair to identify the pattern and cause of hair loss.", ["Itchy or flaky scalp", "Thinning areas", "Breakage"], ["Scalp and hair examination", "Pattern of hair loss", "Scalp conditions"]),
 ("prp", "PRP for Hair", "Platelet-rich plasma prepared from your own blood, used in selected hair-loss plans.", ["Hair thinning", "Pattern hair loss"], ["Suitability and medical history", "Number of sessions"]),
 ("gfc", "GFC for Hair", "Growth factor concentrate from your own blood, used in selected hair-loss plans.", ["Hair thinning", "Hair fall"], ["Cause and pattern of hair loss", "Suitability"]),
 ("plan", "Hair Restoration Treatment Planning", "A combined plan that may include medicines, scalp care and procedures, with regular review.", ["Long-standing hair loss", "Wanting a structured plan"], ["Goals and expectations", "Follow-up schedule"]),
]
hr += svc_schema([n for _, n, *_ in hair])
hr += page_hero("Hair Restoration", "Hair Restoration", "Hair loss treated after its cause is understood.")
hr += '<section class="section"><div class="wrap">' + "".join(service_block(s, n, w, r, ev, "Hair Restoration", s in ("prp", "gfc")) for s, n, w, r, ev in hair) + '<p class="disclaimer">Hair treatment results vary. Our doctors will explain what can be expected in your case.</p></div></section>' + cta() + FOOT
pages["hair.html"] = hr

# ------------------------------------------------------------------ FACILITIES
fc = head("facilities.html", "Clinic Facilities | DERMEON Dermatology Clinic, Asramam, Kollam",
          "Reception, consultation rooms, treatment rooms and laser rooms at DERMEON clinic, Asramam, Kollam.")
fc += page_hero("Facilities", "Our Clinical Facilities", "Designed for comfort, privacy and clinical care.")
fac = [("Reception", "A welcoming reception for registration and appointments."), ("Consultation rooms", "Private rooms for consultations with our doctors."),
       ("Treatment rooms", "Rooms for procedures and aesthetic treatments."), ("Laser rooms", "Dedicated spaces for laser and energy-based treatments."),
       ("Equipment", "Modern laser and aesthetic devices."), ("Patient facilities", "Comfortable waiting areas for patients and families.")]
fc += '<section class="section"><div class="wrap"><div class="grid g3">' + "".join(f'<div class="card reveal" style="padding:0;overflow:hidden">{ph(t + " – photo to be added", "", t[0])}<div style="padding:22px 24px"><h3>{t}</h3><p>{p}</p></div></div>' for t, p in fac) + '</div><p class="center" style="margin-top:30px"><a class="textlink" href="gallery.html">View gallery →</a></p></div></section>' + cta() + FOOT
pages["facilities.html"] = fc

# ------------------------------------------------------------------ GALLERY
gl = head("gallery.html", "Gallery | DERMEON Clinic, Kollam", "Photographs of the DERMEON clinic, treatment rooms, equipment and events.")
gl += page_hero("Gallery", "Gallery", "A look inside DERMEON.")
gl += '<section class="section"><div class="wrap"><div class="filters"></div><div class="gallery" data-gallery></div><p class="note center" style="margin-top:20px">Only photographs approved for publication are shown.</p></div></section>'
gl += '<div class="lightbox" role="dialog" aria-label="Photo viewer"><button class="x" aria-label="Close">×</button><div class="inner"><img alt=""><div class="cap"></div></div></div>' + FOOT
pages["gallery.html"] = gl

# ------------------------------------------------------------------ REVIEWS
rv = head("reviews.html", "DERMEON on Google | Clinic in Asramam, Kollam", "Find DERMEON clinic, Asramam, Kollam on Google Maps for directions, hours and patient feedback.")
rv += page_hero("Google", "Find Us on Google", "Directions, opening hours and patient feedback on our Google Business Profile.")
rv += '''<section class="section"><div class="wrap center" style="max-width:760px"><p class="lead">Patients can read and share feedback on our Google Business Profile.</p>
<div class="btn-row" style="justify-content:center;margin-top:24px"><a class="btn btn-gold" data-google href="#">Open Google Maps</a><a class="btn btn-ghost" href="book.html">Book an Appointment</a></div></div></section>''' + cta() + FOOT
pages["reviews.html"] = rv

# ------------------------------------------------------------------ CONTACT
ct = head("contact.html", "Contact DERMEON | Skin Clinic, Asramam, Kollam – +91 90749 03650",
          "Contact DERMEON clinic at Asramam, Kollam, Kerala 691002. Call +91 90749 03650, WhatsApp us or book an appointment online.")
ct += clinic_schema()
ct += page_hero("Contact", "Contact Us", "Call, WhatsApp or request an appointment online.")
ct += '''<section class="section"><div class="wrap split">
<div class="reveal"><h2>DERMEON Clinic</h2><p>Dermeon Clinic (A Unit of Chaithram Healthcare)</p><hr class="rule">
<ul class="info-list"><li><span>Address</span><div data-address>Asramam, Kollam, Kerala – 691002</div></li>
<li><span>Phone</span><a data-phone href="tel:+919074903650">+91 90749 03650</a></li>
<li><span>WhatsApp</span><a data-wa href="#">Chat on WhatsApp</a></li>
<li><span>Email</span><a data-email href="#"></a></li>
<li><span>Hours</span><div data-hours></div></li>
<li><span>Social</span><div><a data-instagram href="https://www.instagram.com/dermeon_clinic/" target="_blank" rel="noopener">Instagram</a><span> · <a data-facebook href="#" target="_blank" rel="noopener">Facebook</a></span> · <a data-google href="#">Google Business Profile</a></div></li></ul>
<div class="btn-row" style="margin-top:26px"><a class="btn btn-gold" href="book.html">Book an Appointment</a><a class="btn btn-ghost" data-phone href="tel:+919074903650">Call</a></div></div>
<div class="reveal"><iframe class="map" style="height:460px" data-map title="DERMEON location on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>''' + FOOT
pages["contact.html"] = ct

# ------------------------------------------------------------------ BOOK
dept_opts = "".join(f"<option>{d}</option>" for d in ["Dermatology", "Medical Cosmetology", "Aesthetic Medicine", "Laser Treatments", "Hair Restoration", "General Enquiry"])
bk = head("book.html", "Book an Appointment | DERMEON Clinic, Kollam", "Request an appointment at DERMEON, Asramam, Kollam. Our team will call or WhatsApp you to confirm the time.")
bk += page_hero("Book an Appointment", "Request an Appointment", "Send your preferred date and time. Our team will call or WhatsApp you to confirm.")
bk += f'''<section class="section"><div class="wrap" style="max-width:820px">
<form id="booking" class="form" novalidate>
<div class="steps"><span class="on">1 · Department</span><span>2 · Treatment</span><span>3 · Doctor</span><span>4 · Date &amp; time</span><span>5 · Contact</span></div>
<div class="row2">
<div class="field"><label for="department">Department</label><select id="department" required><option value="">Select</option>{dept_opts}</select><div class="err">Please choose a department.</div></div>
<div class="field"><label for="treatment">Treatment / reason for visit</label><select id="treatment" disabled><option value="">Select a department first</option></select><div class="err"></div></div>
</div>
<div class="field"><label for="doctor">Preferred doctor</label><select id="doctor"><option>Any available doctor</option><option>Dermatologist 1</option><option>Dermatologist 2</option><option>Managing Director / Aesthetic Physician</option></select><div class="err"></div></div>
<div class="row2">
<div class="field"><label for="date">Preferred date</label><input type="date" id="date" required><div class="err">Please choose a date from today onwards.</div></div>
<div class="field"><label for="time">Preferred time</label><select id="time" required><option value="">Select</option><option>Morning (before 12 PM)</option><option>Afternoon (12 – 4 PM)</option><option>Evening (after 4 PM)</option></select><div class="err">Please choose a time.</div></div>
</div>
<div class="field"><label for="name">Patient name</label><input id="name" autocomplete="name" maxlength="80" required><div class="err">Please enter the patient's name.</div></div>
<div class="row2">
<div class="field"><label for="mobile">Mobile number</label><input id="mobile" type="tel" inputmode="tel" autocomplete="tel" placeholder="10-digit mobile" maxlength="18" required><div class="err">Please enter a valid mobile number.</div></div>
<div class="field"><label for="whatsappNo">WhatsApp number <span class="opt">(if different)</span></label><input id="whatsappNo" type="tel" inputmode="tel" maxlength="18"><div class="err">Please check the WhatsApp number.</div></div>
</div>
<div class="field"><label for="email">Email address <span class="opt">(optional)</span></label><input id="email" type="email" autocomplete="email" maxlength="120"><div class="err">Please check the email address.</div></div>
<div class="field"><label for="message">Additional message <span class="opt">(optional – please do not share detailed medical records here)</span></label><textarea id="message" rows="3" maxlength="600"></textarea></div>
<div class="hp" aria-hidden="true"><label for="company">Company</label><input id="company" tabindex="-1" autocomplete="off"></div>
<label class="consent"><input type="checkbox" id="consent"> <span>I agree that DERMEON may contact me by phone, SMS or WhatsApp about this appointment request, and I have read the <a class="textlink" href="privacy.html">Privacy Policy</a>.</span></label>
<div id="consentErr" class="note" style="display:none;color:#A23B2A;margin:-10px 0 16px">Please tick the consent box.</div>
<button class="btn btn-gold" id="submitBtn" type="submit" style="width:100%">Send Appointment Request</button>
<p class="disclaimer">This is an appointment <strong>request</strong>. Your slot is confirmed only after our team contacts you. For emergencies, please visit the nearest hospital.</p>
</form>
<div class="success form" role="status">
<span class="eyebrow">Request received</span><h2>Thank you</h2><p>Your booking reference number is</p><div class="ref"></div>
<p class="sendnote">Our team will call or WhatsApp you to confirm your appointment. Please keep this reference number.</p>
<div class="btn-row" style="justify-content:center"><a class="btn btn-gold wa-ref" target="_blank" rel="noopener" href="#">Contact us on WhatsApp</a><a class="btn btn-ghost" href="index.html">Back to home</a></div>
</div></div></section>''' + FOOT
pages["book.html"] = bk

# ------------------------------------------------------------------ LEGAL
pp = head("privacy.html", "Privacy Policy | DERMEON", "How DERMEON collects and protects information sent through this website.")
pp += page_hero("Privacy Policy", "Privacy Policy", "Last updated: November 2026")
pp += '''<section class="section"><div class="wrap" style="max-width:820px">
<h3>Information we collect</h3><p>When you request an appointment we collect your name, mobile and WhatsApp number, optional email address, the department and treatment you are interested in, your preferred doctor, date and time, and any message you write. We do not ask for medical records through this website.</p>
<h3>How we use it</h3><p>We use this information only to contact you about your appointment request, to schedule your visit and for related follow-up by phone, SMS or WhatsApp.</p>
<h3>Storage and access</h3><p>Appointment requests are stored in a secure account of the clinic and are accessible only to authorised clinic staff.</p>
<h3>Sharing</h3><p>We do not sell or share your information with third parties for marketing. Information may be disclosed where required by law.</p>
<h3>Patient photographs and reviews</h3><p>We do not publish patient photographs or personal information on this website without the patient's permission.</p>
<h3>Your choices</h3><p>You can ask us to correct or delete your appointment request details by calling <a data-phone href="tel:+919074903650">+91 90749 03650</a>.</p>
<h3>Website services</h3><p>This website uses Google Maps and Google Fonts, which may process technical information such as your IP address under Google's own policies.</p>
</div></section>''' + FOOT
pages["privacy.html"] = pp

tm = head("terms.html", "Terms &amp; Conditions | DERMEON", "Terms of use for the DERMEON website.")
tm += page_hero("Terms", "Terms &amp; Conditions", "Last updated: November 2026")
tm += '''<section class="section"><div class="wrap" style="max-width:820px">
<h3>Medical information</h3><p>Content on this website is for general information and does not replace a consultation with a qualified doctor. Do not use it to diagnose or treat any condition.</p>
<h3>Appointments</h3><p>Online submissions are appointment requests. An appointment is confirmed only when clinic staff contact you. The clinic may reschedule appointments when needed.</p>
<h3>Treatments and results</h3><p>Treatment availability, suitability, number of sessions and results vary between individuals and are decided by our doctors after consultation. No result is guaranteed.</p>
<h3>Pricing</h3><p>Fees are explained at the clinic and may change without notice.</p>
<h3>Website content</h3><p>Text, design and images on this website belong to Dermeon Clinic (A Unit of Chaithram Healthcare) or are used with permission.</p>
<h3>Contact</h3><p>For questions about these terms, call <a data-phone href="tel:+919074903650">+91 90749 03650</a>.</p>
</div></section>''' + FOOT
pages["terms.html"] = tm

nf = head("404.html", "Page not found | DERMEON", "The page you are looking for could not be found.")
nf += page_hero("Not found", "Page not found", "The page you are looking for may have moved.") + '<section class="section"><div class="wrap center"><a class="btn btn-gold" href="index.html">Go to home page</a></div></section>' + FOOT
pages["404.html"] = nf

exec(open(os.path.join(ROOT, "landing_gen.py"), encoding="utf-8").read())

# ------------------------------------------------------------------ write
if os.path.exists(OUT): shutil.rmtree(OUT)
shutil.copytree(os.path.join(ROOT, "src"), OUT)
for name, content in pages.items():
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(content)
urls = [p for p in pages if p not in ("404.html",)]
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{BASE}/{'' if p == 'index.html' else p}</loc><lastmod>2026-11-28</lastmod></url>\n" for p in urls) + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
print("built", len(pages), "pages")
