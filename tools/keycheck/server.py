#!/usr/bin/env python3
"""Local-only keyboard check page plus macOS consumer-key event bridge."""

import json
import os
from pathlib import Path
import queue
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent
LISTENERS = set()
LOCK = threading.Lock()
STATUS = {"native": False, "error": "Starting macOS HID listener"}


def broadcast(item):
    with LOCK:
        for listener in tuple(LISTENERS):
            listener.put(item)


def listen_media(binary):
    global STATUS
    process = subprocess.Popen([str(binary)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
    for line in process.stdout:
        try:
            item = json.loads(line)
            if item.get("type") == "ready":
                STATUS = {"native": True, "error": ""}
                broadcast({"type": "status", **STATUS})
            else:
                broadcast(item)
        except ValueError:
            pass
    STATUS = {"native": False, "error": process.stderr.read().strip() or "HID listener stopped"}
    broadcast({"type": "status", **STATUS})


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            listener = queue.Queue()
            with LOCK:
                LISTENERS.add(listener)
            try:
                self.wfile.write(("data: " + json.dumps({"type": "status", **STATUS}) + "\n\n").encode())
                self.wfile.flush()
                while True:
                    try:
                        item = listener.get(timeout=15)
                        self.wfile.write(("data: " + json.dumps(item) + "\n\n").encode())
                    except queue.Empty:
                        self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                with LOCK:
                    LISTENERS.discard(listener)
            return
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        body = (ROOT / "index.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    folder = ROOT / ".build"
    folder.mkdir(exist_ok=True)
    binary = folder / "media-listener"
    if not binary.exists() or binary.stat().st_mtime < (ROOT / "media.m").stat().st_mtime:
        compile_result = subprocess.run(
            ["clang", "-fobjc-arc", "-fblocks", "-framework", "AppKit", "-framework", "CoreGraphics", str(ROOT / "media.m"), "-o", str(binary)],
            text=True, capture_output=True,
            env={**os.environ, "CLANG_MODULE_CACHE_PATH": str(Path(folder) / "module-cache")},
        )
        if compile_result.returncode != 0:
            STATUS.update(error="Media listener did not compile: " + compile_result.stderr.strip())
            print(STATUS["error"])
    if binary.exists():
        threading.Thread(target=listen_media, args=(binary,), daemon=True).start()
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Open http://127.0.0.1:8765/ in Safari or Chrome", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
