const SHOP_URL = "#"; // Replace with the full Square store URL.

document.querySelectorAll("[data-shop-link]").forEach((link) => {
  link.href = SHOP_URL;
  if (SHOP_URL !== "#") {
    link.target = "_blank";
    link.rel = "noopener";
  } else {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      alert("The RogueVerse Studio shop is coming soon.");
    });
  }
});

document.querySelectorAll("[data-year]").forEach((node) => {
  node.textContent = new Date().getFullYear();
});

const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".site-nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
    nav.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }));
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll(".reveal").forEach((node) => observer.observe(node));
