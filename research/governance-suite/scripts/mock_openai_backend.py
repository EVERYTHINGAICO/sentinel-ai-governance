from http.server import BaseHTTPRequestHandler, HTTPServer
import json, time

class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"ok": True})
            return
        if self.path == "/v1/models":
            self._send(200, {"object": "list", "data": [{"id": "mock-gpt", "object": "model"}]})
            return
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/v1/chat/completions":
            self._send(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        req = json.loads(raw.decode("utf-8") or "{}")
        model = req.get("model", "mock-gpt")
        content = "Mock backend allowed response."
        self._send(200, {
            "id": f"chatcmpl-mock-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 6, "total_tokens": 16}
        })

HTTPServer(("127.0.0.1", 18000), Handler).serve_forever()
