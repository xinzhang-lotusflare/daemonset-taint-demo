#! /usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timedelta
import json

non_ready_deadline = datetime.now()

class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if datetime.now() < non_ready_deadline:
            self.send_response(500)
        else:
            self.send_response(200)
        self.end_headers()

    def _get_post_response_body(self):
        return json.dumps(
            {
                "non_ready_deadline": str(non_ready_deadline)
            }
        )

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length))
        non_ready_duration = body.get('duration', 30)
        global non_ready_deadline
        non_ready_deadline = datetime.now() + timedelta(seconds = non_ready_duration)
        self.send_response(201)
        self.end_headers()
        self.wfile.write(self._get_post_response_body().encode('utf-8'))

        

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8000), HttpHandler)
    server.serve_forever()

