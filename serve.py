#!/usr/bin/env python3
"""Static server that refuses to be cached.

python -m http.server sends Last-Modified and no Cache-Control, so browsers happily
serve a stale copy on reload - which repeatedly made edits look like they had not
landed. This sends no-store on everything.
"""
import functools, http.server, socketserver, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8932

class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()
    def log_message(self, *a):
        pass

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), H) as httpd:
    print(f"no-cache server on http://localhost:{PORT}")
    httpd.serve_forever()
