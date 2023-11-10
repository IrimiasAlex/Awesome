import http.server
import socketserver
import json

PORT = 8000

data = []

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global data
        if self.path == '/data_json':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            response_data = json.dumps(data, indent=2)
            self.wfile.write(response_data.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        global data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_data = json.loads(post_data.decode('utf-8'))
        
        print("Data received in the POST request:")
        print(received_data)
        
        data += received_data
        
        self.send_response(200)
        self.end_headers()



with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"The local server is running on the port {PORT}")
    httpd.serve_forever()
