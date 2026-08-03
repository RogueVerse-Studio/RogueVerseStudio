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

const rogueSignupButton = [...document.querySelectorAll(".mega-footer .button")]
  .find((button) => button.textContent.trim() === "Join the Community");

if (rogueSignupButton) {
  const signupContainer = rogueSignupButton.parentElement;
  rogueSignupButton.remove();

  const signupForm = document.createElement("form");
  signupForm.className = "rogue-signup-form embeddable-buttondown-form";
  signupForm.action = "https://buttondown.com/api/emails/embed-subscribe/RogueVersemedia";
  signupForm.method = "post";
  signupForm.target = "_blank";
  signupForm.innerHTML = `
    <label class="sr-only" for="rogueverse-email">Email address</label>
    <input
      id="rogueverse-email"
      class="rogue-signup-form__email"
      type="email"
      name="email"
      autocomplete="email"
      inputmode="email"
      placeholder="you@example.com"
      aria-label="Email address"
      required
    >
    <input type="hidden" name="embed" value="1">
    <input type="hidden" name="tag" value="website">
    <button class="button button-primary rogue-signup-button" type="submit" aria-label="I’m going rogue">
      <span class="rogue-signup-button__lead">I’M GOING</span>
      <span class="rogue-signup-button__rogue">ROGUE</span>
    </button>
    <small class="rogue-signup-form__note">New stories, news, culture, and original-world updates. Unsubscribe anytime.</small>
  `;
  signupContainer.append(signupForm);

  const signupStyle = document.createElement("style");
  signupStyle.textContent = `
    .rogue-signup-form{display:grid;grid-template-columns:minmax(150px,1fr) auto;gap:10px;align-items:stretch;margin-top:12px;max-width:430px}
    .rogue-signup-form__email{min-width:0;padding:12px 14px;border:1px solid rgba(255,255,255,.22);border-radius:7px;background:#080d15;color:#fff;font:600 13px Inter,sans-serif;outline:none;transition:border-color .2s,box-shadow .2s}
    .rogue-signup-form__email::placeholder{color:#7f8a99}
    .rogue-signup-form__email:focus{border-color:#1687ff;box-shadow:0 0 0 3px rgba(22,135,255,.16)}
    .rogue-signup-button{position:relative;overflow:hidden;display:inline-flex!important;align-items:center;justify-content:center;gap:6px;min-height:44px;padding:10px 16px!important;border:1px solid rgba(22,135,255,.65)!important;border-radius:7px!important;background:linear-gradient(125deg,#ff6a00 0%,#ff7b19 58%,#e85100 100%)!important;box-shadow:0 0 0 1px rgba(255,106,0,.28),0 0 18px rgba(22,135,255,.22);color:#fff!important;font-family:Orbitron,sans-serif!important;font-weight:800!important;letter-spacing:.04em;text-transform:uppercase;transform:skewX(-5deg);cursor:pointer;transition:transform .18s,box-shadow .18s,filter .18s}
    .rogue-signup-button::before{content:"";position:absolute;inset:-40% auto -40% -45%;width:32%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.65),transparent);transform:rotate(15deg);transition:left .45s ease}
    .rogue-signup-button:hover::before{left:120%}
    .rogue-signup-button:hover{transform:skewX(-5deg) translateY(-2px);box-shadow:0 0 0 1px rgba(255,106,0,.35),0 0 26px rgba(22,135,255,.38);filter:saturate(1.12)}
    .rogue-signup-button:active{transform:skewX(-5deg) translateY(1px) scale(.98)}
    .rogue-signup-button__lead,.rogue-signup-button__rogue{position:relative;z-index:1;display:inline-block;transform:skewX(5deg)}
    .rogue-signup-button__lead{font-size:10px}
    .rogue-signup-button__rogue{font:900 15px Russo One,sans-serif;letter-spacing:.06em;text-shadow:1px 0 #1687ff,-1px 0 #ff6a00}
    .rogue-signup-form__note{grid-column:1/-1;color:#8f98a8;font-size:10px;line-height:1.45}
    @media(max-width:560px){.rogue-signup-form{grid-template-columns:1fr}.rogue-signup-button{width:100%}.rogue-signup-form__note{grid-column:1}}
    @media(prefers-reduced-motion:reduce){.rogue-signup-button,.rogue-signup-button::before{transition:none}.rogue-signup-button:hover{transform:skewX(-5deg)}}
  `;
  document.head.append(signupStyle);
}

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

// RogueVerse Signal visitor counter. CounterAPI V1 is suitable for a lightweight
// public counter on a static site. A browser is counted at most once per day.
(() => {
  const footer = document.querySelector(".mega-footer");
  if (!footer) return;

  const counter = document.createElement("div");
  counter.className = "rv-signal-counter";
  counter.setAttribute("aria-live", "polite");
  counter.innerHTML = `
    <span class="rv-signal-counter__label">ROGUEVERSE SIGNAL</span>
    <strong class="rv-signal-counter__value" data-rv-visitor-count>---</strong>
    <span class="rv-signal-counter__copy">Rogues have entered the Verse.</span>
  `;

  const copyright = footer.querySelector(".copyright");
  if (copyright) footer.insertBefore(counter, copyright);
  else footer.append(counter);

  const style = document.createElement("style");
  style.textContent = `
    .rv-signal-counter{grid-column:1/-1;display:grid;grid-template-columns:auto auto 1fr;gap:9px 14px;align-items:center;margin-top:14px;padding:14px 16px;border:1px solid rgba(22,135,255,.32);border-left:3px solid #ff6a00;border-radius:8px;background:linear-gradient(110deg,rgba(255,106,0,.07),rgba(22,135,255,.07) 60%,rgba(8,13,21,.35));box-shadow:inset 0 0 24px rgba(22,135,255,.04)}
    .rv-signal-counter__label{font:800 10px Orbitron,sans-serif;letter-spacing:.16em;color:#ff7b19}
    .rv-signal-counter__value{font:900 20px Orbitron,sans-serif;letter-spacing:.04em;color:#fff;text-shadow:0 0 12px rgba(22,135,255,.42)}
    .rv-signal-counter__copy{font:600 11px Inter,sans-serif;color:#8f98a8}
    @media(max-width:620px){.rv-signal-counter{grid-template-columns:1fr auto}.rv-signal-counter__copy{grid-column:1/-1}}
  `;
  document.head.append(style);

  const valueNode = counter.querySelector("[data-rv-visitor-count]");
  const namespace = "rogueversemedia.com";
  const name = "site-visitors";
  const base = `https://api.counterapi.dev/v1/${encodeURIComponent(namespace)}/${encodeURIComponent(name)}`;
  const today = new Date().toISOString().slice(0, 10);
  const storageKey = "rv-visitor-counted-date";

  let endpoint = base;
  try {
    if (localStorage.getItem(storageKey) !== today) endpoint = `${base}/up`;
  } catch (_) {
    endpoint = `${base}/up`;
  }

  fetch(endpoint, { method: "GET", mode: "cors", cache: "no-store" })
    .then((response) => {
      if (!response.ok) throw new Error(`Counter request failed: ${response.status}`);
      return response.json();
    })
    .then((data) => {
      const raw = data.count ?? data.value;
      const numeric = Number(raw);
      valueNode.textContent = Number.isFinite(numeric)
        ? numeric.toLocaleString()
        : String(raw ?? "---");
      if (endpoint.endsWith("/up")) {
        try { localStorage.setItem(storageKey, today); } catch (_) {}
      }
    })
    .catch(() => {
      valueNode.textContent = "ONLINE";
      counter.querySelector(".rv-signal-counter__copy").textContent = "Signal tracking is active.";
    });
})();
