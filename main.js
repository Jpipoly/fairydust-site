// Nav: solid background after scrolling, mobile menu toggle
const nav = document.querySelector(".nav");
const onScroll = () => nav.classList.toggle("scrolled", window.scrollY > 24);
onScroll();
window.addEventListener("scroll", onScroll, { passive: true });

const toggle = document.querySelector(".menu-toggle");
const links = document.querySelector(".nav-links");
if (toggle) {
  toggle.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    nav.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", open);
    toggle.textContent = open ? "×" : "☰";
  });
  links.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", () => {
      links.classList.remove("open");
      nav.classList.remove("menu-open");
      toggle.textContent = "☰";
    })
  );
}

// Reveal on scroll
const io = new IntersectionObserver(
  (entries) =>
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("in");
        io.unobserve(e.target);
      }
    }),
  { threshold: 0.12 }
);
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

// Fairy dust particles in the hero
const canvas = document.getElementById("dust");
if (canvas && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const ctx = canvas.getContext("2d");
  let w, h, dpr, parts = [];
  const mouse = { x: -9999, y: -9999 };
  const colors = ["233,196,106", "246,223,160", "184,164,255", "255,255,255"];

  const resize = () => {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = canvas.offsetWidth;
    h = canvas.offsetHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.round(Math.min(140, (w * h) / 9000));
    parts = Array.from({ length: count }, () => spawn(true));
  };
  const spawn = (anywhere) => ({
    x: Math.random() * w,
    y: anywhere ? Math.random() * h : h + 10,
    r: Math.random() * 1.8 + 0.4,
    vy: -(Math.random() * 0.35 + 0.08),
    vx: (Math.random() - 0.5) * 0.15,
    tw: Math.random() * Math.PI * 2,
    c: colors[Math.floor(Math.random() * colors.length)],
  });

  const tick = () => {
    ctx.clearRect(0, 0, w, h);
    for (const p of parts) {
      const dx = p.x - mouse.x, dy = p.y - mouse.y;
      const d2 = dx * dx + dy * dy;
      if (d2 < 12000) {
        p.vx += dx * 0.00004 * 6;
        p.vy += dy * 0.00004 * 6;
      }
      p.vx *= 0.99;
      p.x += p.vx;
      p.y += p.vy;
      p.tw += 0.03;
      if (p.y < -10 || p.x < -10 || p.x > w + 10) Object.assign(p, spawn(false));
      const a = 0.35 + Math.sin(p.tw) * 0.35;
      ctx.beginPath();
      ctx.fillStyle = `rgba(${p.c},${a})`;
      ctx.shadowBlur = p.r * 6;
      ctx.shadowColor = `rgba(${p.c},${a})`;
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
    requestAnimationFrame(tick);
  };

  canvas.parentElement.addEventListener("mousemove", (e) => {
    const r = canvas.getBoundingClientRect();
    mouse.x = e.clientX - r.left;
    mouse.y = e.clientY - r.top;
  });
  canvas.parentElement.addEventListener("mouseleave", () => (mouse.x = mouse.y = -9999));
  window.addEventListener("resize", resize);
  resize();
  tick();
}

// Forms: no backend yet, so they open a pre-filled email to ohhey@fairydust.vc
document.querySelectorAll("form[data-mailto]").forEach((form) => {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const lines = [];
    for (const [k, v] of data.entries()) if (v) lines.push(`${k}: ${v}`);
    const subject = encodeURIComponent(form.dataset.subject || "Hello Fairydust");
    const body = encodeURIComponent(lines.join("\n\n"));
    window.location.href = `mailto:${form.dataset.mailto}?subject=${subject}&body=${body}`;
    const ok = form.querySelector(".form-ok");
    if (ok) ok.style.display = "block";
  });
});

document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
