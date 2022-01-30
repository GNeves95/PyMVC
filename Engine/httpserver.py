import threading
import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import time


class ServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
		self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
		self.wfile.write(bytes("<body>", "utf-8"))
		self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
		self.wfile.write(bytes("</body></html>", "utf-8"))

class HttpServer():
	def __init__(self):
		self.webServer = HTTPServer(("localhost", 8000), ServerHandler)
		print("Server started http://%s:%s" % ("localhost", 8000))
		#self.webServer.serve_forever()
		self.serverThread = threading.Thread(target=self.serve)
		self.serverThread.start()

	def serve(self):
		print("Serving")
		try:
			self.webServer.serve_forever()
		except KeyboardInterrupt:
			pass

	def stop(self):
		self.webServer.shutdown()
		self.webServer.server_close()
		#self.serverThread.join()