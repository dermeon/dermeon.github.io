(function () {
  var D = window.DERMEON || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var wa = function (text) { return "https://wa.me/" + D.whatsapp + "?text=" + encodeURIComponent(text); };

  /* Mobile navigation */
  var tog = $(".nav-toggle"), nav = $("nav.main");
  if (tog && nav) tog.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    tog.setAttribute("aria-expanded", open ? "true" : "false");
  });

  /* Fill shared contact details */
  $$("[data-phone]").forEach(function (a) { a.textContent = D.phone; a.href = "tel:" + D.phoneLink; });
  $$("[data-address]").forEach(function (e) { e.textContent = D.address; });
  $$("[data-wa]").forEach(function (a) { a.href = wa(a.getAttribute("data-wa") || "Hello DERMEON, I would like to enquire about an appointment."); a.target = "_blank"; a.rel = "noopener"; });
  $$("[data-instagram]").forEach(function (a) { a.href = D.instagram; });
  $$("[data-facebook]").forEach(function (a) { if (D.facebook) a.href = D.facebook; else a.parentNode.style.display = "none"; });
  $$("[data-google]").forEach(function (a) { a.href = D.googleProfile; a.target = "_blank"; a.rel = "noopener"; });
  $$("[data-email]").forEach(function (a) { if (D.email) { a.textContent = D.email; a.href = "mailto:" + D.email; } else a.closest("li").style.display = "none"; });
  $$("[data-map]").forEach(function (f) { f.src = D.mapEmbed; });
  $$("[data-rating]").forEach(function (e) { e.textContent = D.googleRating; });
  $$("[data-reviewcount]").forEach(function (e) { e.textContent = D.googleReviewCount; });
  $$("[data-ratingdate]").forEach(function (e) { e.textContent = D.ratingCheckedOn; });
  $$("[data-year]").forEach(function (e) { e.textContent = new Date().getFullYear(); });

  /* Opening hours */
  $$("[data-hours]").forEach(function (el) {
    if (D.hours && D.hours.length) {
      el.innerHTML = '<table class="hours">' + D.hours.map(function (h) { return "<tr><td>" + esc(h[0]) + "</td><td>" + esc(h[1]) + "</td></tr>"; }).join("") + "</table>";
    } else el.textContent = D.hoursNote;
  });

  /* Reviews */
  $$("[data-reviews]").forEach(function (el) {
    var max = +el.getAttribute("data-reviews") || 99;
    if (!D.reviews || !D.reviews.length) {
      el.innerHTML = '<div class="review" style="grid-column:1/-1;text-align:center"><p style="margin:0">Read what our patients say about DERMEON on our Google Business Profile.</p></div>';
      return;
    }
    el.innerHTML = D.reviews.slice(0, max).map(function (r) {
      return '<figure class="review"><div class="stars" aria-label="5 stars">★★★★★</div><blockquote>“' + esc(r.text) + '”</blockquote><cite>' + esc(r.name) + (r.when ? " · " + esc(r.when) : "") + " · Google review</cite></figure>";
    }).join("");
  });

  /* Doctors */
  $$("[data-doctors]").forEach(function (el) {
    el.innerHTML = (D.doctors || []).map(function (d) {
      var photo = d.photo ? '<div class="ph tall"><img src="' + esc(d.photo) + '" alt="' + esc(d.name) + ', ' + esc(d.role) + '" loading="lazy"></div>'
        : '<div class="ph tall"><span class="mono">D</span><span class="ph-label">Photograph to be added</span></div>';
      return '<article class="doc reveal">' + photo + '<div class="body"><span class="role">' + esc(d.role) + '</span><h3>' + esc(d.name) + '</h3>' +
        '<dl><dt>Qualifications</dt><dd>' + esc(d.qualifications) + '</dd><dt>Specialty</dt><dd>' + esc(d.specialty) + '</dd><dt>Experience</dt><dd>' + esc(d.experience) + '</dd><dt>Availability</dt><dd>' + esc(d.availability) + '</dd></dl>' +
        '<p>' + esc(d.bio) + '</p><a class="btn btn-ghost" href="book.html">Book a consultation</a></div></article>';
    }).join("");
  });

  /* Gallery + lightbox */
  var gal = $("[data-gallery]");
  if (gal) {
    var items = D.gallery || [];
    var cats = ["All", "Clinic interior", "Reception", "Treatment rooms", "Equipment", "Clinic activities", "Events"];
    var fil = $(".filters");
    var draw = function (cat) {
      var list = items.filter(function (i) { return cat === "All" || i.cat === cat; });
      if (!list.length) {
        gal.innerHTML = cats.slice(1).map(function (c) { return '<div class="ph sq"><span class="mono">' + c.charAt(0) + '</span><span class="ph-label">' + c + ' – photo to be added</span></div>'; }).join("");
        return;
      }
      gal.innerHTML = list.map(function (i, k) { return '<button data-k="' + k + '"><div class="ph sq"><img src="' + esc(i.src) + '" alt="' + esc(i.caption) + '" loading="lazy"></div></button>'; }).join("");
      $$("button", gal).forEach(function (b) {
        b.addEventListener("click", function () {
          var it = list[+b.getAttribute("data-k")], lb = $(".lightbox");
          $("img", lb).src = it.src; $("img", lb).alt = it.caption; $(".cap", lb).textContent = it.caption;
          lb.classList.add("open");
        });
      });
    };
    if (fil) {
      fil.innerHTML = cats.map(function (c, i) { return '<button type="button" class="' + (i ? "" : "on") + '">' + c + "</button>"; }).join("");
      $$("button", fil).forEach(function (b) { b.addEventListener("click", function () { $$("button", fil).forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on"); draw(b.textContent); }); });
    }
    draw("All");
    var lb = $(".lightbox");
    if (lb) {
      lb.addEventListener("click", function (e) { if (e.target === lb || e.target.classList.contains("x")) lb.classList.remove("open"); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") lb.classList.remove("open"); });
    }
  }

  /* Floating WhatsApp + enquiry widget (on every page) */
  var waIcon = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.8 2 6.8L3 29l6.6-2c1.9 1 4.1 1.6 6.4 1.6 7.2 0 13-5.7 13-12.8S23.2 3 16 3zm0 23.3c-2.1 0-4.1-.6-5.8-1.7l-.4-.3-3.9 1.2 1.3-3.8-.3-.4c-1.2-1.7-1.8-3.7-1.8-5.7C5.1 10 10 5.2 16 5.2S26.9 10 26.9 15.8 22 26.3 16 26.3zm6-7.8c-.3-.2-2-1-2.3-1.1-.3-.1-.5-.2-.8.2-.2.3-.9 1.1-1.1 1.3-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.7-1.7-1-.9-1.7-2-1.9-2.3-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.3.3-.6.1-.2 0-.4 0-.6l-1.1-2.5c-.3-.7-.6-.6-.8-.6h-.7c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.6 5.8 5 2.8 1.1 3.4.9 4 .8.6-.1 2-.8 2.3-1.6.3-.8.3-1.5.2-1.6-.1-.2-.3-.3-.6-.4z"/></svg>';
  var f = document.createElement("a");
  f.className = "wa-float"; f.href = wa("Hello DERMEON, I would like to enquire about an appointment."); f.target = "_blank"; f.rel = "noopener";
  f.setAttribute("aria-label", "Chat with DERMEON on WhatsApp"); f.innerHTML = waIcon;
  document.body.appendChild(f);
  var cb = document.createElement("button");
  cb.className = "chat-btn"; cb.type = "button"; cb.textContent = "How can we help?"; cb.setAttribute("aria-expanded", "false");
  var cp = document.createElement("div");
  cp.className = "chat-panel"; cp.setAttribute("role", "dialog"); cp.setAttribute("aria-label", "Enquiry options");
  cp.innerHTML = '<header>DERMEON</header><div class="msg">Welcome to DERMEON. How can we help you today?</div><div class="opts">' +
    '<a href="book.html">Book an Appointment</a>' +
    '<a target="_blank" rel="noopener" href="' + wa("Hello DERMEON, I have a dermatology enquiry.") + '">Dermatology Enquiry</a>' +
    '<a target="_blank" rel="noopener" href="' + wa("Hello DERMEON, I would like to know about aesthetic treatments.") + '">Aesthetic Treatment Enquiry</a>' +
    '<a target="_blank" rel="noopener" href="' + wa("Hello DERMEON, I have a hair treatment enquiry.") + '">Hair Treatment Enquiry</a>' +
    '<a href="contact.html">Contact Our Clinic</a></div><div class="fine">For medical advice, please consult our doctors in person. This assistant does not diagnose or prescribe.</div>';
  document.body.appendChild(cb); document.body.appendChild(cp);
  cb.addEventListener("click", function () { var o = cp.classList.toggle("open"); cb.setAttribute("aria-expanded", o ? "true" : "false"); cb.textContent = o ? "Close" : "How can we help?"; });

  /* Subtle reveal on scroll */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { threshold: .12 });
    $$(".reveal").forEach(function (e) { io.observe(e); });
  } else $$(".reveal").forEach(function (e) { e.classList.add("in"); });

  /* ================= Appointment request form ================= */
  var form = $("#booking");
  if (!form) return;
  var loaded = Date.now();
  var treatments = {
    "Dermatology": ["Acne and acne scars", "Pigmentation and melasma", "Skin allergy and dermatitis", "Hair fall and scalp disorders", "Dandruff and scalp care", "Skin rejuvenation", "Other skin concern"],
    "Medical Cosmetology": ["Chemical peel", "HydraFacial", "Carbon laser peel", "Skin boosters", "Skin rejuvenation", "Other"],
    "Aesthetic Medicine": ["Botox", "Dermal fillers", "Skin boosters", "HIFU", "RF skin tightening", "MNRF", "Exosome treatment", "Other"],
    "Laser Treatments": ["Laser hair removal", "Pico laser", "CO2 fractional laser", "Laser skin rejuvenation", "Tattoo removal", "Electrolysis", "Other"],
    "Hair Restoration": ["Hair loss consultation", "PRP", "GFC", "Scalp assessment", "Other"],
    "General Enquiry": ["General enquiry"]
  };
  var dep = $("#department"), tr = $("#treatment"), date = $("#date");
  var params = new URLSearchParams(location.search);
  var fillTr = function () {
    var list = treatments[dep.value] || [];
    tr.innerHTML = '<option value="">Select</option>' + list.map(function (t) { return "<option>" + t + "</option>"; }).join("");
    tr.disabled = !list.length;
  };
  dep.addEventListener("change", fillTr);
  if (params.get("dept") && treatments[params.get("dept")]) { dep.value = params.get("dept"); fillTr(); if (params.get("t")) tr.value = params.get("t"); }
  var today = new Date(); today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
  date.min = today.toISOString().slice(0, 10);
  var max = new Date(); max.setDate(max.getDate() + 90); date.max = max.toISOString().slice(0, 10);

  var steps = $$(".steps span");
  form.addEventListener("input", function () {
    var n = dep.value ? (tr.value ? ($("#doctor").value ? (date.value ? 4 : 3) : 2) : 1) : 0;
    steps.forEach(function (s, i) { s.classList.toggle("on", i <= n); });
  });

  var phoneOk = function (v) { var d = v.replace(/[^\d]/g, ""); return /^(91)?[6-9]\d{9}$/.test(d) || (v.trim().charAt(0) === "+" && d.length >= 8 && d.length <= 15); };
  var check = function (id, ok) { var f = $("#" + id).closest(".field"); f.classList.toggle("bad", !ok); return ok; };
  var makeRef = function () {
    var d = new Date(), p = function (n) { return ("0" + n).slice(-2); };
    var r = Math.random().toString(36).slice(2, 6).toUpperCase();
    return "DRM-" + String(d.getFullYear()).slice(2) + p(d.getMonth() + 1) + p(d.getDate()) + "-" + r;
  };

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var v = function (id) { return $("#" + id).value.trim(); };
    var ok = true;
    ok = check("name", v("name").length >= 2) && ok;
    ok = check("mobile", phoneOk(v("mobile"))) && ok;
    ok = check("whatsappNo", !v("whatsappNo") || phoneOk(v("whatsappNo"))) && ok;
    ok = check("email", !v("email") || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v("email"))) && ok;
    ok = check("department", !!v("department")) && ok;
    ok = check("date", !!v("date") && v("date") >= date.min) && ok;
    ok = check("time", !!v("time")) && ok;
    var consent = $("#consent").checked;
    $("#consentErr").style.display = consent ? "none" : "block";
    if (!ok || !consent) { var bad = $(".field.bad"); if (bad) bad.scrollIntoView({ behavior: "smooth", block: "center" }); return; }

    // Spam protection: hidden field and too-fast submissions
    if ($("#company").value || Date.now() - loaded < 4000) return;

    // Duplicate protection: same mobile + date within 30 minutes on this device
    var key = "dermeon_last_booking";
    var last = null; try { last = JSON.parse(localStorage.getItem(key) || "null"); } catch (x) {}
    var digits = v("mobile").replace(/\D/g, "");
    if (last && last.m === digits && last.d === v("date") && Date.now() - last.t < 30 * 60 * 1000) { showDone(last.ref, true); return; }

    var ref = makeRef();
    var data = {
      ref: ref, name: v("name"), mobile: v("mobile"), whatsapp: v("whatsappNo") || v("mobile"), email: v("email"),
      department: v("department"), treatment: v("treatment"), doctor: v("doctor"), date: v("date"), time: v("time"),
      message: v("message").slice(0, 600), source: "dermeon.in", website: $("#company").value
    };
    var btn = $("#submitBtn"); btn.disabled = true; btn.textContent = "Sending…";

    var finish = function (sent) {
      try { localStorage.setItem(key, JSON.stringify({ m: digits, d: data.date, t: Date.now(), ref: ref })); } catch (x) {}
      showDone(ref, false, sent, data);
    };
    if (D.bookingEndpoint) {
      fetch(D.bookingEndpoint, { method: "POST", mode: "no-cors", body: new URLSearchParams(data) })
        .then(function () { finish(true); })
        .catch(function () { finish(false); });
    } else finish(false);
  });

  function showDone(ref, dup, sent, data) {
    form.style.display = "none";
    var box = $(".success"); box.style.display = "block";
    $(".ref", box).textContent = ref;
    var txt = "Hello DERMEON, my appointment request reference is " + ref + ".";
    if (data && !sent) {
      txt += "\nName: " + data.name + "\nMobile: " + data.mobile + "\nDepartment: " + data.department + (data.treatment ? " – " + data.treatment : "") +
        "\nPreferred doctor: " + data.doctor + "\nPreferred date: " + data.date.split("-").reverse().join("/") + ", " + data.time + (data.message ? "\nMessage: " + data.message : "");
      $(".sendnote", box).textContent = "Please tap the WhatsApp button below to send your request details to our clinic.";
    } else if (dup) {
      $(".sendnote", box).textContent = "We already received this request from you. Our team will contact you shortly.";
    }
    $(".wa-ref", box).href = wa(txt);
    box.scrollIntoView({ behavior: "smooth", block: "center" });
  }
})();
