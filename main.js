document.documentElement.classList.add("js");

// Mobile menu
const toggle = document.querySelector(".menu-toggle");
const links = document.querySelector(".nav-links");
if (toggle) {
  const setOpen = (open) => {
    links.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open);
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  };
  toggle.addEventListener("click", () => setOpen(!links.classList.contains("open")));
  links.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setOpen(false)));
  document.addEventListener("keydown", (e) => e.key === "Escape" && setOpen(false));
}

// Reveal on scroll
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    }),
    { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
} else {
  document.querySelectorAll(".reveal").forEach((el) => el.classList.add("in"));
}

// Forms: no backend yet, so they open a pre-filled email to ohhey@fairydust.vc
document.querySelectorAll("form[data-mailto]").forEach((form) => {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const lines = [];
    for (const [k, v] of new FormData(form).entries()) if (v) lines.push(`${k}: ${v}`);
    const subject = encodeURIComponent(form.dataset.subject || "Hello Fairydust");
    const body = encodeURIComponent(lines.join("\n\n"));
    window.location.href = `mailto:${form.dataset.mailto}?subject=${subject}&body=${body}`;
    const ok = form.querySelector(".form-ok");
    if (ok) ok.style.display = "block";
  });
});
