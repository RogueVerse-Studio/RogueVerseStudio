const SHOP_URL = "#"; // Replace with the full Square store URL.

// Add the GA4 web data stream's Measurement ID (for example, "G-ABC123DE45")
// to activate analytics across the entire site.
const GA_MEASUREMENT_ID = "";

function initializeAnalytics(measurementId) {
  if (!/^G-[A-Z0-9]+$/i.test(measurementId)) return;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() {
    window.dataLayer.push(arguments);
  };

  const pathParts = window.location.pathname.split("/").filter(Boolean);
  const section = pathParts[0] || "home";
  const isArticle = Boolean(document.querySelector("article, .article-shell"));

  window.gtag("js", new Date());
  window.gtag("config", measurementId, {
    send_page_view: false
  });
  window.gtag("event", "page_view", {
    page_title: document.title,
    page_location: window.location.href,
    page_path: window.location.pathname + window.location.search,
    content_group: section,
    content_type: isArticle ? "article" : "section"
  });

  const googleTag = document.createElement("script");
  googleTag.async = true;
  googleTag.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
  document.head.append(googleTag);

  const sendEvent = (eventName, parameters = {}) => {
    window.gtag("event", eventName, {
      page_path: window.location.pathname,
      content_group: section,
      ...parameters
    });
  };

  document.addEventListener("click", (event) => {
    const target = event.target instanceof Element
      ? event.target.closest("a, button")
      : null;
    if (!target) return;

    const label = (target.dataset.analyticsLabel || target.textContent || "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 100);
    const rawHref = target instanceof HTMLAnchorElement
      ? target.getAttribute("href") || ""
      : "";
    const absoluteUrl = target instanceof HTMLAnchorElement
      ? new URL(target.href, window.location.href)
      : null;
    const analyticsText = `${label} ${rawHref}`.toLowerCase();
    const isOutbound = Boolean(
      absoluteUrl &&
      absoluteUrl.protocol.startsWith("http") &&
      absoluteUrl.hostname !== window.location.hostname
    );

    let eventName = target.dataset.analyticsEvent || "";
    if (!eventName && analyticsText.includes("going rogue")) {
      eventName = "going_rogue_click";
    } else if (
      !eventName &&
      (analyticsText.includes("square.site") ||
        analyticsText.includes("/shop/") ||
        /\b(shop|store)\b/.test(label.toLowerCase()))
    ) {
      eventName = "store_link_click";
    } else if (
      !eventName &&
      rawHref.toLowerCase().startsWith("mailto:") &&
      /creator|mythra|artist|writer|portfolio|guidelines|submit|inquiry|join/.test(analyticsText)
    ) {
      eventName = "creator_application_click";
    } else if (!eventName && isOutbound) {
      eventName = "outbound_link_click";
    }

    if (!eventName) return;

    sendEvent(eventName, {
      link_text: label,
      link_url: rawHref.toLowerCase().startsWith("mailto:")
        ? "mailto"
        : absoluteUrl?.href || rawHref,
      link_domain: absoluteUrl?.hostname || "",
      outbound: isOutbound
    });
  });

  const readingMilestones = isArticle ? [30, 60, 180] : [30, 60];
  readingMilestones.forEach((seconds) => {
    window.setTimeout(() => {
      if (document.visibilityState === "visible") {
        sendEvent("reading_milestone", { engagement_time_seconds: seconds });
      }
    }, seconds * 1000);
  });

  const reachedScrollDepths = new Set();
  const reportScrollDepth = () => {
    const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (scrollableHeight <= 0) return;

    const depth = Math.round((window.scrollY / scrollableHeight) * 100);
    [25, 50, 75, 90].forEach((milestone) => {
      if (depth >= milestone && !reachedScrollDepths.has(milestone)) {
        reachedScrollDepths.add(milestone);
        sendEvent("scroll_depth", { percent_scrolled: milestone });
      }
    });
  };

  window.addEventListener("scroll", reportScrollDepth, { passive: true });
}

initializeAnalytics(GA_MEASUREMENT_ID);

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
    ["horikoshi-horror-one-shot/", "MANGA NEWS", "Horikoshi Is Coming Back—and He Brought Horror With Him"],
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
