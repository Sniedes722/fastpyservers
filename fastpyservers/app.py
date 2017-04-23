"""
Copyright (c) Shawn Niederriter 2017

"""
import asyncio
import uvloop

import functools
import os
import signal
import logging

from fastpyservers.server import FastHTTPServer

class AsyncWebApp:

	def __init__(self, name=None):
		self.name = name
		self.server = FastHTTPServer()

	def run(self, host="0.0.0.0", port=8080):
		self.server.run_server(host, port)


