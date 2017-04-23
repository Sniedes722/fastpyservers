"""
Copyright (c) Shawn Niederriter 2017

"""
import asyncio
import uvloop

import functools
import os
import signal
import logging

from fastpyservers.constants import HTTP_METHODS
from fastpyservers.responses import BaseHTTPResponse
from fastpyservers.requests import BaseHTTPRequest, Request, get_request



log = logging.getLogger(__name__)

clients = {}  # task -> (reader, writer)

def ask_exit(signame, loop):
	print("Exiting Sneed Web Server %s" % signame)
	loop.stop()

async def accept_client(BaseHTTPRequest, BaseHTTPResponse):
	task = asyncio.ensure_future(handler(BaseHTTPRequest, BaseHTTPResponse))
	clients[task] = (BaseHTTPRequest, BaseHTTPResponse)
		
	def client_done(task):
		del clients[task]
		BaseHTTPResponse.close()
		log.info("End Connection")
		
	log.info("New Connection")
	task.add_done_callback(client_done)

async def handler(BaseHTTPRequest, BaseHTTPResponse):
	r = Request()
	hdrs = await get_request(BaseHTTPRequest, r)
	print(hdrs)
	BaseHTTPResponse.write(b'HTTP/1.1 200 OK\r\n')
	BaseHTTPResponse.write(b'Server: Sneed/0.0.1 (Linux x86_64)\r\n')
	BaseHTTPResponse.write(b'Last-Modified: Mon, 27 Mar 2017 11:33:56 EST\r\n')
	BaseHTTPResponse.write(b'Content-Length: 48\r\n')
	BaseHTTPResponse.write(b'Content-Type: text/html\r\n')
	BaseHTTPResponse.write(b'Connection: Closed\r\n')
	BaseHTTPResponse.write(b'\r\n')
	BaseHTTPResponse.write(b'<html><body><h1>Sneed Async Python Web Server</h1></body></html>\r\n')
	#print(r)


class FastHTTPServer:

	def run_server(self, host="0.0.0.0", port=8000):
		loop = uvloop.new_event_loop()
		asyncio.set_event_loop(loop)
		f = asyncio.start_server(accept_client, host=host, port=port, loop=loop)
		log.info('Sneed Web Server running @ http://{}:{}'.format(host, port))
		for signame in ('SIGINT', 'SIGTERM'):
		    loop.add_signal_handler(getattr(signal, signame),
		                            functools.partial(ask_exit, signame, loop))
		loop.run_until_complete(f)
		try:
		    loop.run_forever()
		finally:
		    loop.close()
