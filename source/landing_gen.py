# Builds treatment landing pages and the treatments hub. Executed inside gen.py's namespace.

def faq_schema(faqs):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}, ensure_ascii=False) + "</script>\n"

def crumb_schema(items):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u} for i, (n, u) in enumerate(items)]}, ensure_ascii=False) + "</script>\n"

NAME = {x[0]: x[1] for x in L}
for slug, short, h1, meta, intro, who, approach, options, sessions, faqs, dept, related in L:
    pg = head(slug + ".html", f"{h1} | DERMEON, Asramam", meta)
    pg += clinic_schema() + faq_schema(faqs) + crumb_schema([("Home", ""), ("Treatments", "treatments.html"), (short, slug + ".html")])
    pg += '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "MedicalWebPage", "name": h1, "about": short,
        "url": f"{BASE}/{slug}.html", "audience": "Patient", "publisher": {"@type": "MedicalClinic", "name": "DERMEON Clinic", "url": BASE + "/"}}, ensure_ascii=False) + "</script>\n"
    pg += f'<section class="page-hero"><div class="wrap"><div class="crumbs"><a href="index.html">Home</a> / <a href="treatments.html">Treatments</a> / {e(short)}</div><h1>{e(h1)}</h1><p>{e(meta.split(". ")[0])}.</p></div></section>'
    who_li = "".join(f"<li>{e(x)}</li>" for x in who)
    app_li = "".join(f"<li>{e(x)}</li>" for x in approach)
    opt_cards = "".join(f'<div class="card"><h3 style="font-size:1.15rem">{e(n)}</h3><p>{e(t)}</p></div>' for n, t in options)
    faq_html = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs)
    rel = " · ".join(f'<a class="textlink" href="{r}.html">{e(NAME[r])}</a>' for r in related if r in NAME)
    deptq = dept.replace(" ", "+")
    pg += f"""<section class="section"><div class="wrap split">
<div class="reveal"><span class="eyebrow">{e(short)} at DERMEON</span><h2>What to know</h2><hr class="rule"><p class="lead">{e(intro)}</p>
<div class="btn-row" style="margin-top:24px"><a class="btn btn-gold" href="book.html?dept={deptq}">Book a Consultation</a><a class="btn btn-ghost" data-wa href="#">WhatsApp Us</a></div></div>
<div class="reveal card"><h3>Clinic details</h3><ul class="info-list"><li><span>Location</span><div data-address>Asramam, Kollam, Kerala – 691002</div></li><li><span>Open</span><div>All days, including Sunday</div></li><li><span>Consultation</span><div>10:00 AM – 7:00 PM</div></li><li><span>Phone</span><a data-phone href="tel:+919074903650">{PHONE}</a></li></ul><a class="textlink" data-google href="#">Get directions on Google Maps →</a></div>
</div></section>
<section class="section alt"><div class="wrap"><div class="grid g2">
<div class="card reveal"><h3>Who may benefit</h3><ul>{who_li}</ul></div>
<div class="card reveal"><h3>How our doctors approach it</h3><ul>{app_li}</ul></div>
</div>
<div class="reveal" style="margin-top:40px"><h2>Treatment options</h2><hr class="rule"><div class="grid g3">{opt_cards}</div>
<p style="margin-top:22px"><strong>Sessions and results:</strong> {e(sessions)} The right option for you is decided after a consultation.</p></div>
</div></section>
<section class="section"><div class="wrap" style="max-width:860px"><div class="center reveal"><span class="eyebrow">Questions</span><h2>{e(short)} – FAQs</h2><hr class="rule"></div>
{faq_html}
<p class="disclaimer">This page is general information and does not replace a consultation. Results vary between individuals and are not guaranteed.</p>
<h3 style="margin-top:34px">Related treatments</h3><p>{rel}</p></div></section>
""" + cta() + FOOT
    pages[slug + ".html"] = pg

hub = head("treatments.html", "Skin, Hair &amp; Aesthetic Treatments in Kollam | DERMEON", "All skin, hair, laser, aesthetic and weight-management treatments at DERMEON clinic, Asramam, Kollam.")
hub += clinic_schema() + page_hero("Treatments", "Treatments at DERMEON, Kollam", "Skin, hair, laser, aesthetic and weight-management care, planned after a doctor's consultation.")
groups = [("Skin conditions", ["acne-treatment-kollam", "pigmentation-melasma-treatment-kollam", "skin-allergy-eczema-treatment-kollam", "wart-skin-tag-removal-kollam", "dark-circles-treatment-kollam"]),
          ("Hair and scalp", ["hair-fall-treatment-kollam", "dandruff-scalp-treatment-kollam"]),
          ("Laser", ["laser-hair-removal-kollam", "tattoo-removal-kollam", "acne-scar-treatment-kollam"]),
          ("Aesthetic medicine", ["anti-wrinkle-treatment-kollam", "dermal-fillers-kollam", "skin-tightening-kollam", "hydrafacial-kollam", "chemical-peel-kollam"]),
          ("Weight management", ["weight-management-kollam"])]
LD = {x[0]: x for x in L}
body = ""
for g, items in groups:
    cards = "".join(f'<a class="card reveal" style="text-decoration:none" href="{sl}.html"><h3 style="font-size:1.2rem">{e(LD[sl][2])}</h3><p style="font-size:.9rem">{e(LD[sl][4].split(". ")[0])}.</p></a>' for sl in items)
    body += f'<h2 class="reveal" style="margin-top:30px">{g}</h2><hr class="rule"><div class="grid g3">{cards}</div>'
hub += '<section class="section"><div class="wrap">' + body + '</div></section>' + cta() + FOOT
pages["treatments.html"] = hub
pages["index.html"] = pages["index.html"].replace("</script>\n", "</script>\n" + faq_schema(FAQ), 1)
