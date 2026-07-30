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

const storyFeeds = {
  "/old-man-otaku/": [
    ["gundam-xarx-zero/", "ANIME NEWS", "A New Gundam Universe Begins With XARX-ZERO"],
    ["../news/movies/avatar-aang/", "MOVIES / ANIMANGA", "Avatar Aang Is Back—and All Grown Up"],
    ["luke-cage-doctor-doom/", "COMIC HISTORY", "Luke Cage Went to Latveria for His Money"],
    ["mjolnir-worthiness/", "COMIC LORE", "What Does It Actually Take to Lift Mjolnir?"]
  ],
  "/news/movies/": [
    ["avatar-aang/", "NOW STREAMING", "Avatar Aang Is Back—and All Grown Up"],
    ["ryan-gosling-ghost-rider/", "MARVEL NEWS", "Ryan Gosling Rides Into the MCU as Ghost Rider"],
    ["jumanji-open-world/", "TRAILER REPORT", "Jumanji: Open World Brings the Game Into Reality"],
    ["transformers-update/", "FRANCHISE UPDATE", "Transformers at 40: What Is Actually Confirmed"]
  ],
  "/news/": [
    ["fayetteville-skyeton/", "LOCAL CULTURE", "Skyeton Picks Fayetteville for Its U.S. Headquarters"]
  ]
};

const feed = storyFeeds[location.pathname];
const shell = document.querySelector(".content-shell");
if (feed && shell) {
  const list = document.createElement("div");
  list.className = "story-list";
  list.innerHTML = feed.map(([href, tag, title]) =>
    `<a href="${href}"><small>${tag}</small><h3>${title}</h3></a>`
  ).join("");
  shell.append(list);
}
