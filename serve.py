#!/usr/bin/env python3
"""NAC demo server: static site + server-side Wellgentic proxy.

The browser calls POST /api/chat with {"message": "...", "thread_id": "..."}.
This server forwards it to the Wellgentic endpoint with the key from the
WELLGENTIC_API_KEY environment variable, so the key never appears in any
committed file or in client-side code.

Provide the config either way:
  1. Export it:  WELLGENTIC_API_KEY=... WELLGENTIC_ENDPOINT=https://... python3 serve.py
  2. Or drop a .env:  printf 'WELLGENTIC_API_KEY=...\\nWELLGENTIC_ENDPOINT=https://...\\n' > .env
The .env file is gitignored, so the key never reaches the repo.
"""
import http.server
import json
import os
import socketserver
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "docs")
PORT = int(os.environ.get("PORT", "4177"))

# Match these to your Wellgentic endpoint's expected request/response shape.
FIELD_MESSAGE = os.environ.get("WELLGENTIC_FIELD_MESSAGE", "message")
FIELD_THREAD = os.environ.get("WELLGENTIC_FIELD_THREAD", "thread_id")
FIELD_WORKFLOW = os.environ.get("WELLGENTIC_FIELD_WORKFLOW", "workflow_id")
WORKFLOW_ID = os.environ.get("WELLGENTIC_WORKFLOW_ID", "78")
AUTH_STYLE = os.environ.get("WELLGENTIC_AUTH_STYLE", "bearer")  # "bearer" or "xapikey"


def load_dotenv():
    """Populate os.environ from a local .env (KEY=value lines) if present.
    Real environment variables always win over .env values."""
    path = os.path.join(ROOT, ".env")
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


load_dotenv()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE, **kwargs)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return
        key = os.environ.get("WELLGENTIC_API_KEY", "").strip()
        endpoint = os.environ.get("WELLGENTIC_ENDPOINT", "").strip()
        if not key or not endpoint:
            self._json(503, {"error": "Server missing WELLGENTIC_API_KEY / WELLGENTIC_ENDPOINT. "
                                      "Restart with those set (or in .env)."})
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            incoming = json.loads(self.rfile.read(length) or "{}")
        except Exception:
            incoming = {}
        message = (incoming.get("message") or "").strip()
        thread = (incoming.get("thread_id") or "").strip()
        if not message:
            self._json(400, {"error": "Empty message"})
            return

        payload = {FIELD_MESSAGE: message}
        if thread:
            payload[FIELD_THREAD] = thread
        if WORKFLOW_ID:
            payload[FIELD_WORKFLOW] = WORKFLOW_ID

        headers = {"content-type": "application/json", "accept": "application/json"}
        if AUTH_STYLE == "xapikey":
            headers["x-api-key"] = key
        else:
            headers["authorization"] = "Bearer " + key

        req = urllib.request.Request(
            endpoint, data=json.dumps(payload).encode(), headers=headers, method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                self._raw(resp.status, resp.read(),
                          resp.headers.get("Content-Type", "application/json"))
        except urllib.error.HTTPError as e:
            self._raw(e.code, e.read())
        except Exception as e:  # noqa: BLE001 — surface anything to the widget
            self._json(502, {"error": str(e)})

    def _raw(self, status, data, ctype="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, status, obj):
        self._raw(status, json.dumps(obj).encode())

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), Handler) as srv:
        ready = "yes" if (os.environ.get("WELLGENTIC_API_KEY") and os.environ.get("WELLGENTIC_ENDPOINT")) else "NO — set WELLGENTIC_API_KEY + WELLGENTIC_ENDPOINT"
        print(f"NAC site on http://localhost:{PORT}  (Wellgentic configured: {ready})")
        srv.serve_forever()
