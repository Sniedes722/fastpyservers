"""
Copyright (c) Shawn Niederriter 2017

"""
from fastpyservers.logger import run_logger

from fastpyservers.server import FastHTTPServer

class AsyncWebApp:

	def __init__(self, name=None):
		self.name = name
		self.server = FastHTTPServer()

	def run(self, host="0.0.0.0", port=8080):
		run_logger()
		self.server.run_server(host, port)


