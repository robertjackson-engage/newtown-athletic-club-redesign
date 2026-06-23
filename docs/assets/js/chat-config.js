/* Newtown Athletic Club Concierge configuration.
   The API key lives server-side in `.env` (ANTHROPIC_API_KEY) at the project
   root — serve.py proxies chat calls so the key never ships to the browser.
   On static hosting (GitHub Pages) the widget falls back to an in-browser key
   gate: visit any page with #ck=YOUR_KEY once to store it in localStorage. */
window.NAC_CHAT = {
  proxyUrl: (location.hostname === "localhost" || location.hostname === "127.0.0.1") ? "/api/chat" : "",
  apiKey: "",
  model: "claude-sonnet-4-6"
};
