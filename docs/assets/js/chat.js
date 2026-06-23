/* Newtown Athletic Club Concierge — Claude-powered */
(function () {
  "use strict";

  var CFG = window.NAC_CHAT || {};
  var MODEL = CFG.model || "claude-sonnet-4-6";

  var SYSTEM = [
    "You are the NAC Concierge, the friendly AI assistant for the Newtown Athletic Club (the 'NAC') — newtownathletic.com, a 250,000 sq. ft. lifestyle club in Newtown, Bucks County, Pennsylvania. You live on their website.",
    "Voice: warm, premium, welcoming and concise — like a knowledgeable, hospitable member of the club, never a pushy salesperson. Short paragraphs. The brand spirit is 'Your Home for Health' and 'More than a health club — a lifestyle.' Building community since 1978.",
    "FACTS:",
    "- LOCATION: 120 Pheasant Run, Newtown, PA 18940. Main phone (215) 968-0600. The Newtown Performance Institute (NPI, HYROX & CrossFit) is at 114 Pheasant Run. Club hours: Mon-Fri 5am-11pm, Sat-Sun 6am-9pm.",
    "- MEMBERSHIP: Age-based pricing; financial assistance available; HSA/FSA accepted. Three join options: NAC Lifestyle ($229/mo adult — full campus, all studios, pools, HYROX & CrossFit), NPI Membership ($169/mo — performance gym with HYROX & CrossFit, or MMA-only), and NPI Gym Access ($79/mo — gym only). Membership types: Signature (30+), Couple, Family, Mid-Adult (26-29), Youth Individual (14-25), and 25% off for active Military/Police/Firefighters. Every membership includes a complimentary Health Strategy Session (InBody 770 + movement screen). When unsure of an exact rate, point to [Pricing](pricing.html) or a free pass and (215) 968-0600 — don't invent prices.",
    "- BOUTIQUE STUDIOS (200+ classes/week, all included across ~10 studios): THE PRACTICE (yoga, 50+ classes/wk, aerial yoga), REFORM (Pilates, 30 reformers), PULSE (dance/strength/cardio, 165\" LCD wall), REV (cycling, Les Mills THE TRIP), Barre Lab, SIX ZONE (35-min heart-rate HIIT), 105 Hot Studio (90-105°F), FIT 22 (22-min Technogym Biocircuit strength), and HYROX. Back Gym is a 10,000+ sq ft collegiate weight room.",
    "- AQUATICS & RESORT: Two indoor pools (renovated competition pool), NAC Swim School (lessons from 6 months), AquaFit, lap & Masters swim, and American Red Cross lifeguard/CPR certifications. The Escape Resort is a 4-acre, 4-pool outdoor club — two 35-ft slides, lazy river, cabanas, full bar, Friday Night Live music; open May-Oct, with a heated adult pool open all winter (80°+).",
    "- FAMILY & YOUTH: Kids Club childcare (6 weeks+, 2 free hrs/day included), kids fitness & dance classes, Camp NAC (ages 3-15, best in Bucks County), gymnastics (rec to USAIGC team), Youth Performance / Newtown Performance Institute (formerly Parisi Speed School), a 40,000 sq ft Sports Training Center, Newtown Discovery Preschool, birthday parties and in-club golf.",
    "- WELLNESS & MEDICINE: One of the first clubs in the nation with an in-house physician. YOUR.Life Functional Medicine led by Dr. Meg Zakarewicz, MD (functional medicine, metabolic weight loss, hormone health, longevity, peptides). Plus registered-dietitian nutrition, stretch & recovery (assisted stretch, NormaTec), The Well Lounge Med Spa, and NAC Premier upgrade ($100/mo). The Have a Heart Foundation gives $1M+/yr to the community.",
    "RULES: Answer only about the Newtown Athletic Club, fitness, its programs/studios, wellness, and visiting/joining. Link pages with markdown like [Join](join.html), [Free Pass](join.html#trial), [Pricing](pricing.html), [Membership](membership.html), [Boutique Studios](studios.html), [HYROX](hyrox.html), [Six Zone](six-zone.html), [Escape Resort](resort.html), [Swim](swim.html), [Family](family.html), [Functional Medicine](functional-medicine.html), [Hours](hours.html), [Contact](contact.html). For billing/account specifics, suggest calling (215) 968-0600. Keep answers under 120 words unless asked for detail. End with a helpful next step when natural.",
  ].join("\n");

  // NAC diamond mark
  var MARK = '<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="16.5" y="16.5" width="31" height="31" rx="3" transform="rotate(45 32 32)" fill="none" stroke="currentColor" stroke-width="2.6"/><rect x="21" y="21" width="22" height="22" rx="2" transform="rotate(45 32 32)" fill="none" stroke="currentColor" stroke-width="1.1" opacity="0.55"/><text x="32" y="35" text-anchor="middle" dominant-baseline="middle" font-family="Raleway, Arial, sans-serif" font-size="13" font-weight="800" fill="currentColor">NAC</text></svg>';

  var CHIPS = [
    "What's included in a membership?",
    "How much does it cost?",
    "Tell me about the boutique studios",
    "Can I get a free pass?",
    "What is the Escape Resort?"
  ];

  /* ---------- build DOM ---------- */
  var root = document.createElement("div");
  root.innerHTML =
    '<button class="chat-orb" aria-label="Chat with the NAC Concierge">' + MARK + "</button>" +
    '<div class="chat-orb__hint" role="button" tabindex="0">' +
    '  <span class="chat-orb__hint-avatar">' + MARK + "</span>" +
    '  <span class="chat-orb__hint-text"><em>Have questions?</em> I\'m here to help.</span>' +
    '  <button class="chat-orb__hint-x" aria-label="Dismiss">✕</button>' +
    "</div>" +
    '<div class="chat-panel" role="dialog" aria-label="Club Concierge chat">' +
    '  <div class="chat-head">' +
    '    <div class="chat-head__icon">' + MARK + "</div>" +
    '    <div><div class="chat-head__name">Club Concierge</div><div class="chat-head__sub">AI Concierge · Powered by Claude</div></div>' +
    '    <button class="chat-head__close" aria-label="Close chat">✕</button>' +
    "  </div>" +
    '  <div class="chat-msgs"></div>' +
    '  <div class="chat-input">' +
    '    <textarea rows="1" placeholder="Ask about classes, pricing, hours…" aria-label="Message"></textarea>' +
    '    <button class="chat-send" aria-label="Send">→</button>' +
    "  </div>" +
    '  <div class="chat-note">Club Concierge is an AI assistant — for account questions call (501) 225-3600.</div>' +
    "</div>";
  document.body.appendChild(root);

  var orb = root.querySelector(".chat-orb");
  var hint = root.querySelector(".chat-orb__hint");
  var msgs = root.querySelector(".chat-msgs");
  var input = root.querySelector(".chat-input textarea");
  var sendBtn = root.querySelector(".chat-send");
  var history = [];
  try { history = JSON.parse(sessionStorage.getItem("tac-chat") || "[]"); } catch (e) {}

  /* activation link: visiting any page with #ck=<api-key> stores the key in
     this browser and cleans the URL — the key never lives in the repo */
  try {
    var ckm = location.hash.match(/[#&]ck=([^&]+)/);
    if (ckm) {
      localStorage.setItem("tac-anthropic-key", decodeURIComponent(ckm[1]));
      history_replace_safe();
    }
  } catch (e) {}
  function history_replace_safe() {
    try { window.history.replaceState(null, "", location.pathname + location.search); } catch (e) {}
  }

  function getKey() {
    if (CFG.proxyUrl) return "proxy"; /* key lives server-side; nothing needed here */
    if (CFG.apiKey) return CFG.apiKey;
    try { return localStorage.getItem("tac-anthropic-key") || ""; } catch (e) { return ""; }
  }

  /* ---------- rendering ---------- */
  function md(t) {
    t = t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    t = t.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
    t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    var blocks = t.split(/\n{2,}/).map(function (b) {
      var lines = b.split("\n");
      var items = lines.filter(function (l) { return /^\s*[-•]\s+/.test(l); });
      if (items.length && items.length === lines.length) {
        return "<ul>" + items.map(function (l) { return "<li>" + l.replace(/^\s*[-•]\s+/, "") + "</li>"; }).join("") + "</ul>";
      }
      return "<p>" + b.replace(/\n/g, "<br>") + "</p>";
    });
    return blocks.join("");
  }

  function addMsg(role, html) {
    var d = document.createElement("div");
    d.className = "chat-msg chat-msg--" + (role === "user" ? "user" : "ai");
    d.innerHTML = role === "user" ? html.replace(/</g, "&lt;") : html;
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
    return d;
  }

  function welcome() {
    var w = document.createElement("div");
    w.className = "chat-welcome";
    w.innerHTML = "<h3>What can we help you crush today?</h3><p>Classes, pricing, hours, programs — ask me anything about GHF.</p>" +
      '<div class="chat-chips">' + CHIPS.map(function (c) { return "<button>" + c + "</button>"; }).join("") + "</div>";
    msgs.appendChild(w);
    w.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () { input.value = b.textContent; send(); });
    });
  }

  function keyGate() {
    var g = document.createElement("div");
    g.className = "chat-gate";
    g.innerHTML = "<p><strong>One-time setup:</strong> paste your Anthropic API key to activate Club Concierge. It's stored only in this browser.</p>" +
      '<input type="password" placeholder="sk-ant-…" aria-label="Anthropic API key">' +
      '<button class="btn btn--solid btn--sm">Activate Coach →</button>';
    msgs.appendChild(g);
    g.querySelector("button").addEventListener("click", function () {
      var v = g.querySelector("input").value.trim();
      if (!v) return;
      try { localStorage.setItem("tac-anthropic-key", v); } catch (e) {}
      g.remove();
      addMsg("ai", "<p>All set! Ask me anything about GHF. 💪</p>");
    });
  }

  function restore() {
    if (!history.length) { welcome(); }
    else history.forEach(function (m) { addMsg(m.role, m.role === "user" ? m.content : md(m.content)); });
    if (!getKey()) keyGate();
  }

  /* ---------- Claude call (streaming) ---------- */
  function send() {
    var text = input.value.trim();
    if (!text) return;
    if (!getKey()) { keyGate(); return; }
    input.value = "";
    var wEl = msgs.querySelector(".chat-welcome");
    if (wEl) wEl.remove();
    addMsg("user", text);
    history.push({ role: "user", content: text });
    sendBtn.disabled = true;

    var typing = document.createElement("div");
    typing.className = "chat-typing";
    typing.innerHTML = "<i></i><i></i><i></i>";
    msgs.appendChild(typing);
    msgs.scrollTop = msgs.scrollHeight;

    var aiEl = null;
    var full = "";

    var apiUrl = CFG.proxyUrl || "https://api.anthropic.com/v1/messages";
    var apiHeaders = { "content-type": "application/json" };
    if (!CFG.proxyUrl) {
      apiHeaders["x-api-key"] = getKey();
      apiHeaders["anthropic-version"] = "2023-06-01";
      apiHeaders["anthropic-dangerous-direct-browser-access"] = "true";
    }
    fetch(apiUrl, {
      method: "POST",
      headers: apiHeaders,
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 700,
        system: SYSTEM,
        messages: history.slice(-12),
        stream: true
      })
    }).then(function (res) {
      if (!res.ok) return res.text().then(function (t) { throw new Error("API " + res.status + ": " + t.slice(0, 200)); });
      var reader = res.body.getReader();
      var dec = new TextDecoder();
      var buf = "";
      function pump() {
        return reader.read().then(function (r) {
          if (r.done) return;
          buf += dec.decode(r.value, { stream: true });
          var lines = buf.split("\n");
          buf = lines.pop();
          lines.forEach(function (ln) {
            if (ln.indexOf("data: ") !== 0) return;
            try {
              var ev = JSON.parse(ln.slice(6));
              if (ev.type === "content_block_delta" && ev.delta && ev.delta.text) {
                if (!aiEl) { typing.remove(); aiEl = addMsg("ai", ""); }
                full += ev.delta.text;
                aiEl.innerHTML = md(full);
                msgs.scrollTop = msgs.scrollHeight;
              }
            } catch (e) {}
          });
          return pump();
        });
      }
      return pump();
    }).then(function () {
      if (typing.parentNode) typing.remove();
      if (full) {
        history.push({ role: "assistant", content: full });
        try { sessionStorage.setItem("tac-chat", JSON.stringify(history.slice(-20))); } catch (e) {}
      }
    }).catch(function (err) {
      if (typing.parentNode) typing.remove();
      var isAuth = /401|403/.test(err.message);
      if (isAuth) { try { localStorage.removeItem("tac-anthropic-key"); } catch (e) {} }
      addMsg("ai", "<p>" + (isAuth
        ? "That API key didn't work — let's try again."
        : "I'm having trouble connecting right now. You can always reach us at <a href='tel:5012253600'>(501) 225-3600</a>.") + "</p>");
      if (isAuth) keyGate();
      history.pop();
    }).finally(function () {
      sendBtn.disabled = false;
      input.focus();
    });
  }

  /* ---------- events ---------- */
  function openChat() {
    document.body.classList.add("chat-open");
    hint.classList.remove("is-on");
    if (!msgs.children.length) restore();
    setTimeout(function () { input.focus(); }, 400);
  }
  orb.addEventListener("click", openChat);
  /* clicking the popup bubble opens the chat too */
  hint.addEventListener("click", function (e) {
    if (e.target.closest(".chat-orb__hint-x")) return;
    openChat();
  });
  hint.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openChat(); }
  });
  hint.querySelector(".chat-orb__hint-x").addEventListener("click", function (e) {
    e.stopPropagation();
    hint.classList.remove("is-on");
    try { sessionStorage.setItem("tac-chat-hint", "1"); } catch (er) {}
  });
  root.querySelector(".chat-head__close").addEventListener("click", function () {
    document.body.classList.remove("chat-open");
  });
  sendBtn.addEventListener("click", send);
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
  });
  input.addEventListener("input", function () {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 110) + "px";
  });

  /* teaser popup, once per session — appears shortly after load, lingers */
  try {
    if (!sessionStorage.getItem("tac-chat-hint")) {
      setTimeout(function () {
        if (!document.body.classList.contains("chat-open")) hint.classList.add("is-on");
      }, 3500);
      setTimeout(function () {
        hint.classList.remove("is-on");
        try { sessionStorage.setItem("tac-chat-hint", "1"); } catch (er) {}
      }, 16000);
    }
  } catch (e) {}
})();
