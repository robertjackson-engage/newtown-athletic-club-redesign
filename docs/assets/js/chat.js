/* Newtown Athletic Club Concierge — powered by Wellgentic.
   The agent's knowledge and instructions live entirely on the Wellgentic side.
   This widget just sends the visitor's message + a thread id and renders the reply.
   Endpoint/auth/field mapping are configured in chat-config.js (window.NAC_CHAT). */
(function () {
  "use strict";

  var CFG = window.NAC_CHAT || {};
  // Where the browser POSTs {message, thread_id}. Locally, serve.py proxies to
  // Wellgentic (key stays server-side); in production set CFG.endpoint.
  var ENDPOINT = CFG.proxyUrl || CFG.endpoint || "";
  var F_MSG = CFG.fieldMessage || "message";
  var F_THREAD = CFG.fieldThread || "thread_id";
  var RESP_PATH = CFG.responsePath || "reply";
  var THREAD_PATH = CFG.threadPath || "thread_id";

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
    '<div class="chat-panel" role="dialog" aria-label="NAC Concierge chat">' +
    '  <div class="chat-head">' +
    '    <div class="chat-head__icon">' + MARK + "</div>" +
    '    <div><div class="chat-head__name">NAC Concierge</div><div class="chat-head__sub">AI Concierge · Powered by Wellgentic</div></div>' +
    '    <button class="chat-head__close" aria-label="Close chat">✕</button>' +
    "  </div>" +
    '  <div class="chat-msgs"></div>' +
    '  <div class="chat-input">' +
    '    <textarea rows="1" placeholder="Ask about classes, pricing, hours…" aria-label="Message"></textarea>' +
    '    <button class="chat-send" aria-label="Send">→</button>' +
    "  </div>" +
    '  <div class="chat-note">NAC Concierge is an AI assistant — for account questions call (215) 968-0600.</div>' +
    "</div>";
  document.body.appendChild(root);

  var orb = root.querySelector(".chat-orb");
  var hint = root.querySelector(".chat-orb__hint");
  var msgs = root.querySelector(".chat-msgs");
  var input = root.querySelector(".chat-input textarea");
  var sendBtn = root.querySelector(".chat-send");

  var history = [];
  try { history = JSON.parse(sessionStorage.getItem("nac-chat") || "[]"); } catch (e) {}

  /* per-visitor Wellgentic thread id (kept in this browser) */
  var threadId = "";
  try { threadId = localStorage.getItem("nac-thread") || ""; } catch (e) {}
  if (!threadId) {
    try { threadId = (crypto && crypto.randomUUID) ? crypto.randomUUID() : ("nac-" + Date.now() + "-" + Math.random().toString(16).slice(2)); }
    catch (e) { threadId = "nac-" + Date.now() + "-" + Math.random().toString(16).slice(2); }
    try { localStorage.setItem("nac-thread", threadId); } catch (e) {}
  }

  /* optional direct-call auth key — only via #ck=<key> (browser only, never in the repo) */
  try {
    var ckm = location.hash.match(/[#&]ck=([^&]+)/);
    if (ckm) {
      localStorage.setItem("nac-wg-key", decodeURIComponent(ckm[1]));
      try { window.history.replaceState(null, "", location.pathname + location.search); } catch (e) {}
    }
  } catch (e) {}
  function getKey() {
    if (CFG.apiKey) return CFG.apiKey;
    try { return localStorage.getItem("nac-wg-key") || ""; } catch (e) { return ""; }
  }

  function dotget(obj, path) {
    var parts = String(path).split(".");
    for (var i = 0; i < parts.length; i++) {
      if (obj && typeof obj === "object" && parts[i] in obj) obj = obj[parts[i]];
      else return null;
    }
    return obj;
  }

  /* ---------- rendering ---------- */
  function md(t) {
    t = String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
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
    w.innerHTML = "<h3>How can we help you today?</h3><p>Classes, pricing, hours, the resort, programs — ask me anything about the NAC.</p>" +
      '<div class="chat-chips">' + CHIPS.map(function (c) { return "<button>" + c + "</button>"; }).join("") + "</div>";
    msgs.appendChild(w);
    w.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () { input.value = b.textContent; send(); });
    });
  }

  function restore() {
    if (!history.length) { welcome(); }
    else history.forEach(function (m) { addMsg(m.role, m.role === "user" ? m.content : md(m.content)); });
  }

  /* ---------- Wellgentic call ---------- */
  function send() {
    var text = input.value.trim();
    if (!text) return;
    if (!ENDPOINT) {
      addMsg("ai", "<p>The concierge isn't connected yet. Please set your Wellgentic endpoint in <code>chat-config.js</code>.</p>");
      return;
    }
    input.value = "";
    input.style.height = "auto";
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

    var headers = { "content-type": "application/json" };
    var key = getKey();
    if (key && !CFG.proxyUrl) {
      if ((CFG.authStyle || "bearer") === "xapikey") headers["x-api-key"] = key;
      else headers["authorization"] = "Bearer " + key;
    }
    var payload = {};
    payload[F_MSG] = text;
    payload[F_THREAD] = threadId;

    fetch(ENDPOINT, { method: "POST", headers: headers, body: JSON.stringify(payload) })
      .then(function (res) {
        return res.text().then(function (raw) {
          var data; try { data = JSON.parse(raw); } catch (e) { data = raw; }
          if (!res.ok) throw new Error((data && data.error) || ("HTTP " + res.status));
          return data;
        });
      })
      .then(function (data) {
        if (typing.parentNode) typing.remove();
        var tid = (data && typeof data === "object") ? dotget(data, THREAD_PATH) : null;
        if (tid) { threadId = tid; try { localStorage.setItem("nac-thread", threadId); } catch (e) {} }
        var reply = (data && typeof data === "object") ? dotget(data, RESP_PATH) : null;
        if (reply === null || reply === undefined) reply = (typeof data === "string") ? data : "";
        addMsg("ai", md(String(reply)));
        history.push({ role: "assistant", content: String(reply) });
        try { sessionStorage.setItem("nac-chat", JSON.stringify(history.slice(-20))); } catch (e) {}
      })
      .catch(function () {
        if (typing.parentNode) typing.remove();
        addMsg("ai", "<p>I'm having trouble connecting right now. You can always reach us at <a href='tel:2159680600'>(215) 968-0600</a>.</p>");
        history.pop();
      })
      .finally(function () {
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
    try { sessionStorage.setItem("nac-chat-hint", "1"); } catch (er) {}
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

  /* teaser popup, once per session */
  try {
    if (!sessionStorage.getItem("nac-chat-hint")) {
      setTimeout(function () {
        if (!document.body.classList.contains("chat-open")) hint.classList.add("is-on");
      }, 3500);
      setTimeout(function () {
        hint.classList.remove("is-on");
        try { sessionStorage.setItem("nac-chat-hint", "1"); } catch (er) {}
      }, 16000);
    }
  } catch (e) {}
})();
