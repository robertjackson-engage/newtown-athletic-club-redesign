/* Newtown Athletic Club Concierge — powered by Wellgentic.
   The agent's instructions/knowledge live on the Wellgentic side; this only
   tells the widget where to send each message + thread id, and how to read
   the reply back. */
window.NAC_CHAT = {
  /* Local dev: serve.py proxies /api/chat to Wellgentic so the key stays
     server-side. In production (static hosting), set `endpoint` to your
     Wellgentic message endpoint below. */
  proxyUrl: (location.hostname === "localhost" || location.hostname === "127.0.0.1") ? "/api/chat" : "",

  /* PRODUCTION: your Wellgentic message endpoint (the one that takes a message
     + thread id). Leave proxyUrl behavior as-is; this is used when not on localhost. */
  endpoint: "",                 // <-- e.g. "https://api.wellgentic.com/v1/threads/message"

  /* Optional auth for direct (non-proxied) calls. Leave blank — never commit a
     secret. For testing you can load any page once with #ck=YOUR_KEY to store
     it in this browser only. */
  apiKey: "",
  authStyle: "bearer",          // "bearer" -> Authorization: Bearer <key>, or "xapikey" -> x-api-key

  /* Request body field names your endpoint expects */
  fieldMessage: "message",
  fieldThread: "thread_id",

  /* Where to read the reply text / updated thread id from the JSON response
     (dot paths, e.g. "reply" or "data.message" or "choices.0.message.content") */
  responsePath: "reply",
  threadPath: "thread_id"
};
