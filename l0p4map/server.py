#!/usr/bin/env python3
"""Simple HTTP server for L0p4Map dashboard + API."""
import http.server
import json
import os
import subprocess
import threading
from datetime import datetime

DATA_DIR = "/data"
DASH_DIR = "/opt/l0p4map/dashboard"
L0P4MAP_DIR = "/opt/l0p4map"
LAST_SCAN_FILE = os.path.join(DATA_DIR, "scan_results.json")
SCAN_LOCK = threading.Lock()

def run_scan():
    """Run L0p4Map scan in background."""
    with SCAN_LOCK:
        target = os.environ.get("L0P4MAP_TARGET", "")
        iface = os.environ.get("L0P4MAP_INTERFACE", "")
        if not target:
            try:
                result = subprocess.run(
                    ["python3", "-c",
                     "from core.scanner import get_local_subnet; print(get_local_subnet())"],
                    capture_output=True, text=True, cwd=L0P4MAP_DIR, timeout=15
                )
                target = result.stdout.strip() or "192.168.1.0/24"
            except Exception:
                target = "192.168.1.0/24"

        cmd = ["python3", "__main__.py", "scan", "--target", target, "--output", "json", "--file", LAST_SCAN_FILE]
        if iface:
            cmd += ["--interface", iface]

        try:
            subprocess.run(cmd, cwd=L0P4MAP_DIR, capture_output=True, text=True, timeout=300)
        except Exception as e:
            print(f"Scan error: {e}")


class Handler(http.server.BaseHTTPRequestHandler):
    def _headers(self):
        return {
            'host': self.headers.get('host', ''),
            'forwarded': self.headers.get('forwarded', ''),
            'x-forwarded-for': self.headers.get('x-forwarded-for', ''),
            'x-forwarded-proto': self.headers.get('x-forwarded-proto', 'http'),
            'x-forwarded-host': self.headers.get('x-forwarded-host', ''),
        }

    def do_GET(self):
        h = self._headers()
        path = self.path.split('?')[0]
        if path == '/api/hosts':
            self.serve_hosts()
        elif path == '/api/status':
            self.serve_status()
        elif path == '/health' or path == '/healthz':
            self.send_json({'status': 'ok'})
        else:
            self.serve_file(path)

    def do_POST(self):
        if self.path == "/api/scan":
            threading.Thread(target=run_scan, daemon=True).start()
            self.send_json({"status": "scan started"})
        else:
            self.send_json({"error": "unknown endpoint"}, 404)

    def serve_hosts(self):
        try:
            if os.path.exists(LAST_SCAN_FILE):
                with open(LAST_SCAN_FILE) as f:
                    data = json.load(f)
                self.send_json(data)
            else:
                self.send_json([])
        except Exception as e:
            self.send_json({"error": str(e)}, 500)

    def serve_status(self):
        try:
            exists = os.path.exists(LAST_SCAN_FILE)
            size = os.path.getsize(LAST_SCAN_FILE) if exists else 0
            self.send_json({
                "last_scan": datetime.fromtimestamp(os.path.getmtime(LAST_SCAN_FILE)).isoformat() if exists else None,
                "hosts_count": len(json.load(open(LAST_SCAN_FILE))) if exists else 0,
                "file_exists": exists,
                "file_size": size
            })
        except Exception as e:
            self.send_json({"error": str(e)}, 500)

    def serve_file(self, path):
        if path == "/" or path == "":
            path = "/index.html"
        filepath = os.path.join(DASH_DIR, path.lstrip("/"))
        if not os.path.isfile(filepath):
            self.send_error(404)
            return
        ext = os.path.splitext(filepath)[1]
        mime = {".html": "text/html", ".js": "application/javascript", ".css": "text/css",
                ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml"}.get(ext, "text/plain")
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.end_headers()
        with open(filepath, "rb") as f:
            self.wfile.write(f.read())

    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass  # silence logs


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    port = int(os.environ.get("DASHBOARD_PORT", "8099"))
    server = http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Dashboard on :{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()