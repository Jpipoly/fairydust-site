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

// Sparkle trail on the hero: follows the mouse, bursts on tap/click
const hero = document.querySelector("[data-sparkle]");
const calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (hero && !calm && hero.animate) {
  const STAR = '<svg viewBox="-10 -10 20 20" fill="currentColor"><path d="M0 -10Q1 -1 10 0Q1 1 0 10Q-1 1 -10 0Q-1 -1 0 -10Z"/></svg>';
  const colors = ["#b35a53", "#ff7143", "#b35a53", "#ffaea3", "#be522f"];
  let live = 0, last = 0;

  const spark = (x, y, spread) => {
    if (live > 40) return;
    live++;
    const el = document.createElement("span");
    el.className = "sparkle-fx";
    el.innerHTML = STAR;
    const size = spread > 50 ? 12 + Math.random() * 20 : 10 + Math.random() * 14;
    el.style.cssText = `left:${x}px;top:${y}px;width:${size}px;height:${size}px;margin:${-size / 2}px 0 0 ${-size / 2}px;color:${colors[(Math.random() * colors.length) | 0]}`;
    hero.appendChild(el);
    const a = Math.random() * Math.PI * 2, d = spread * (0.4 + Math.random() * 0.6);
    el.animate(
      [
        { transform: "translate(0,0) scale(.2) rotate(0deg)", opacity: 0 },
        { transform: `translate(${Math.cos(a) * d * 0.35}px, ${Math.sin(a) * d * 0.35}px) scale(1.15) rotate(30deg)`, opacity: 1, offset: 0.2 },
        { transform: `translate(${Math.cos(a) * d}px, ${Math.sin(a) * d + 24}px) scale(.5) rotate(120deg)`, opacity: 0 },
      ],
      { duration: 900 + Math.random() * 600, easing: "cubic-bezier(.2,.7,.3,1)" }
    ).onfinish = () => { el.remove(); live--; };
  };

  const local = (e) => {
    const r = hero.getBoundingClientRect();
    return [e.clientX - r.left, e.clientY - r.top];
  };
  hero.addEventListener("pointermove", (e) => {
    if (e.pointerType !== "mouse") return;
    const now = performance.now();
    if (now - last < 45) return;
    last = now;
    const [x, y] = local(e);
    spark(x, y, 30);
  });
  hero.addEventListener("pointerdown", (e) => {
    const [x, y] = local(e);
    for (let i = 0; i < 14; i++) spark(x, y, 110);
  });

  // One welcome burst from the logo card's star mark
  // (on phones the tile is hidden, so burst from the headline instead)
  const tileStar = hero.querySelector(".hero-mark .mark-lg");
  const tile = tileStar && tileStar.offsetParent ? tileStar : hero.querySelector(".shimmer");
  if (tile) {
    setTimeout(() => {
      const r = tile.getBoundingClientRect(), h = hero.getBoundingClientRect();
      const x = r.left - h.left + r.width / 2, y = r.top - h.top + r.height / 2;
      for (let i = 0; i < 18; i++) setTimeout(() => spark(x, y, 160), i * 35);
    }, 600);
  }
}
