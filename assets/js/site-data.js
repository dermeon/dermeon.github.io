/* =====================================================================
   DERMEON – EDITABLE SITE DATA
   Change the text between the quotes and save. Nothing else needs editing.
   Lines marked TODO still need real, verified information from the clinic.
   ===================================================================== */
window.DERMEON = {

  /* ---------- Contact ---------- */
  clinicName: "DERMEON Clinic",
  legalName: "Dermeon Clinic (A Unit of Chaithram Healthcare)",
  address: "Asramam, Kollam, Kerala – 691002",
  phone: "+91 90749 03650",
  phoneLink: "+919074903650",
  whatsapp: "919074903650",
  email: "",                      // TODO: clinic email, e.g. "care@dermeon.in"
  instagram: "https://www.instagram.com/dermeon_clinic/",
  facebook: "",                   // TODO: Facebook page link
  googleProfile: "https://www.google.com/maps/search/?api=1&query=Dermeon+Clinic+Asramam+Kollam", // TODO: replace with the exact Google Business Profile link
  mapEmbed: "https://www.google.com/maps?q=Dermeon+Clinic+Asramam+Kollam&output=embed",

  /* ---------- Opening hours (TODO: confirm before publishing) ---------- */
  hours: [
    // ["Monday – Saturday", "9:30 AM – 7:30 PM"],
    // ["Sunday", "By appointment"],
  ],
  hoursNote: "Please call or WhatsApp us to confirm today's consultation timings.",

  /* ---------- Google rating (updated by hand; not a live feed) ---------- */
  googleRating: "4.9",
  googleReviewCount: "229",
  ratingCheckedOn: "November 2026",

  /* ---------- Selected genuine Google reviews ----------
     Copy only real reviews from the Google profile, with the reviewer's permission
     or as publicly posted. Example format:
     { text: "…", name: "First name L.", when: "October 2026" }            */
  reviews: [],

  /* ---------- Doctors (TODO: add verified details) ---------- */
  doctors: [
    { name: "Dermatologist", role: "Consultant Dermatologist", photo: "", qualifications: "To be added", specialty: "Dermatology", experience: "To be added", bio: "Profile details will be added soon.", availability: "Please call to check consultation days" },
    { name: "Dermatologist", role: "Consultant Dermatologist", photo: "", qualifications: "To be added", specialty: "Dermatology", experience: "To be added", bio: "Profile details will be added soon.", availability: "Please call to check consultation days" },
    { name: "Managing Director", role: "Medical Doctor & Aesthetic Physician", photo: "", qualifications: "To be added", specialty: "Aesthetic Medicine", experience: "To be added", bio: "Profile details will be added soon.", availability: "Please call to check consultation days" }
  ],

  /* ---------- Gallery: add real, approved clinic photos ----------
     { src: "assets/img/gallery/reception-1.jpg", cat: "Reception", caption: "Reception" }
     Categories: Clinic interior, Reception, Treatment rooms, Equipment, Clinic activities, Events */
  gallery: [],

  /* ---------- Booking ----------
     Paste the Google Apps Script web-app URL here after setup (see SETUP-GUIDE). */
  bookingEndpoint: "https://script.google.com/macros/s/AKfycbwpqFs8oe9idY_OjQ7gHfDPAUaxUeutaDVSUMRBFhd_Rixtg7NGideR2PcwASCdGs0a/exec"
};
