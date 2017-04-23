"""
Copyright (c) Shawn Niederriter 2017

"""
from fastpyservers.logger import run_logger

from fastpyservers.server import FastHTTPServer

class AsyncWebApp:

	def __init__(self, name=None):
		self.name = name
		self.server = FastHTTPServer()
		self.route_methods = []
		self.data_handlers = []
		self.handlers = []

	def run(self, host="0.0.0.0", port=8080):
		run_logger()
		self.server.run_server(self, host, port)

	def handler(self, func, method, content_type, route):
		reg_handle = (method, route)
		data_handle = (func, content_type)
		handle_all = (route, method, content_type, func)
		self.route_methods.append(reg_handle)
		self.data_handlers.append(data_handle)
		self.handlers.append(handle_all)

	def print_handlers(self):
		print(self.route_methods)
		print(self.data_handlers)
		print(self.handlers)

		


