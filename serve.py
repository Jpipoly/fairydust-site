# Local preview server that mimics Vercel clean URLs (/founders -> founders.html)
import http.server, os, sys

class H(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.path.split("?")[0].split("#")[0]
        if path != "/" and "." not in os.path.basename(path) and os.path.exists("." + path + ".html"):
            self.path = path + ".html"
        return super().send_head()

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
http.server.ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
