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

// Header: tighten + deepen shadow once the page scrolls
const navEl = document.querySelector(".nav");
const onScroll = () => navEl && navEl.classList.toggle("scrolled", window.scrollY > 16);
onScroll();
window.addEventListener("scroll", onScroll, { passive: true });

// Nav + footer links: a soft pill slides to whichever link you point at or tab to
document.querySelectorAll("[data-ind]").forEach((group) => {
  const ind = group.querySelector(".nav-ind");
  if (!ind) return;
  const moveTo = (link) => {
    // appearing from hidden: jump into place, then slide between links after that
    const fresh = ind.style.opacity !== "1";
    if (fresh) ind.style.transition = "opacity .2s ease";
    ind.style.width = link.offsetWidth + "px";
    ind.style.height = link.offsetHeight + "px";
    ind.style.top = link.offsetTop + "px";
    ind.style.transform = `translateX(${link.offsetLeft}px)`;
    ind.style.opacity = "1";
    if (fresh) { ind.offsetWidth; ind.style.transition = ""; }
  };
  const hide = () => (ind.style.opacity = "0");
  group.querySelectorAll(".nav-link").forEach((link) => {
    link.addEventListener("pointerenter", (e) => e.pointerType === "mouse" && moveTo(link));
    link.addEventListener("focus", () => link.matches(":focus-visible") && moveTo(link));
    link.addEventListener("blur", hide);
  });
  group.addEventListener("pointerleave", hide);
  group.querySelectorAll(".btn").forEach((b) => b.addEventListener("pointerenter", hide));
});

// Back to top
document.querySelectorAll('a[href="#top"]').forEach((a) =>
  a.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: calmMotion() ? "auto" : "smooth" });
  })
);
function calmMotion() { return window.matchMedia("(prefers-reduced-motion: reduce)").matches; }

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
    const btn = form.querySelector('button[type="submit"]');
    if (btn) { btn.setAttribute("aria-busy", "true"); setTimeout(() => btn.removeAttribute("aria-busy"), 1500); }
    window.location.href = `mailto:${form.dataset.mailto}?subject=${subject}&body=${body}`;
    const ok = form.querySelector(".form-ok");
    if (ok) ok.style.display = "block";
  });
});

// Lets iOS Safari show :active press states on tap
document.addEventListener("touchstart", () => {}, { passive: true });

// ---------- Sparkles ----------
const calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const STAR = '<svg viewBox="-10 -10 20 20" fill="currentColor"><path d="M0 -10Q1 -1 10 0Q1 1 0 10Q-1 1 -10 0Q-1 -1 0 -10Z"/></svg>';
const COLORS = ["#b35a53", "#ff7143", "#b35a53", "#ffaea3", "#be522f"];
let live = 0;

// x, y are viewport coordinates
function spark(x, y, spread, colors = COLORS) {
  if (calm || !document.body.animate || live > 50) return;
  live++;
  const el = document.createElement("span");
  el.className = "sparkle-fx";
  el.innerHTML = STAR;
  const size = spread > 50 ? 12 + Math.random() * 20 : 8 + Math.random() * 12;
  el.style.cssText = `left:${x}px;top:${y}px;width:${size}px;height:${size}px;margin:${-size / 2}px 0 0 ${-size / 2}px;color:${colors[(Math.random() * colors.length) | 0]}`;
  document.body.appendChild(el);
  const a = Math.random() * Math.PI * 2, d = spread * (0.4 + Math.random() * 0.6);
  el.animate(
    [
      { transform: "translate(0,0) scale(.2) rotate(0deg)", opacity: 0 },
      { transform: `translate(${Math.cos(a) * d * 0.35}px, ${Math.sin(a) * d * 0.35}px) scale(1.15) rotate(30deg)`, opacity: 1, offset: 0.2 },
      { transform: `translate(${Math.cos(a) * d}px, ${Math.sin(a) * d + 24}px) scale(.5) rotate(120deg)`, opacity: 0 },
    ],
    { duration: 900 + Math.random() * 600, easing: "cubic-bezier(.2,.7,.3,1)" }
  ).onfinish = () => { el.remove(); live--; };
}

// Every button: a small burst from where it was pressed
document.addEventListener("pointerdown", (e) => {
  const btn = e.target.closest(".btn");
  if (!btn) return;
  const r = btn.getBoundingClientRect();
  const x = e.clientX || r.left + r.width / 2, y = e.clientY || r.top + r.height / 2;
  const onDark = btn.classList.contains("btn-pink");
  for (let i = 0; i < 9; i++) spark(x, y, 55, onDark ? ["#ffaea3", "#edc2b4", "#ff7143"] : COLORS);
});

// Hero: trail follows the mouse, tap/click anywhere bursts
const hero = document.querySelector("[data-sparkle]");
if (hero) {
  let last = 0;
  hero.addEventListener("pointermove", (e) => {
    if (e.pointerType !== "mouse") return;
    const now = performance.now();
    if (now - last < 45) return;
    last = now;
    spark(e.clientX, e.clientY, 30);
  });
  hero.addEventListener("pointerdown", (e) => {
    if (e.target.closest(".btn, a")) return;
    for (let i = 0; i < 14; i++) spark(e.clientX, e.clientY, 110);
  });

  // The floating mark leans gently toward the cursor
  const tilt = hero.querySelector("[data-tilt] .hs-svg");
  if (tilt && !calm) {
    hero.addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse") return;
      const r = tilt.getBoundingClientRect();
      const dx = (e.clientX - (r.left + r.width / 2)) / window.innerWidth;
      const dy = (e.clientY - (r.top + r.height / 2)) / window.innerHeight;
      tilt.style.setProperty("--px", `${dx * 28}px`);
      tilt.style.setProperty("--py", `${dy * 28}px`);
      tilt.style.setProperty("--rot", `${dx * 8}deg`);
    });
    hero.addEventListener("pointerleave", () => {
      ["--px", "--py", "--rot"].forEach((p) => tilt.style.removeProperty(p));
    });
  }

  // One welcome burst from the big star
  const origin = hero.querySelector(".hs-svg .s1") || hero.querySelector(".shimmer");
  if (origin) {
    setTimeout(() => {
      const r = origin.getBoundingClientRect();
      for (let i = 0; i < 18; i++) setTimeout(() => spark(r.left + r.width / 2, r.top + r.height / 2, 160), i * 35);
    }, 600);
  }
}
