"""
Copyright (c) Shawn Niederriter 2017

"""
import asyncio
import uvloop

import functools
import os
import signal

from fastpyservers.constants import HTTP_METHODS
from fastpyservers.responses import BaseHTTPResponse, Response
from fastpyservers.requests import BaseHTTPRequest, Request
from fastpyservers.logger import log
from fastpyservers.routes import router

clients = {}  # task -> (reader, writer)

def ask_exit(signame, loop):
	print("Exiting Sneed Web Server %s" % signame)
	loop.stop()

## This should eventually be part of a worker
async def accept_client(tasks, BaseHTTPRequest, BaseHTTPResponse):
	task = asyncio.ensure_future(route_handler("/index", 'GET', BaseHTTPRequest, BaseHTTPResponse))
	clients[task] = (BaseHTTPRequest, BaseHTTPResponse)
		
	def client_done(task):
		del clients[task]
		BaseHTTPResponse.close()

	task.add_done_callback(client_done)


## This should be moved to app.py, as it's what we want people to be writing
async def route_handler(url, method, BaseHTTPRequest, BaseHTTPResponse):
	data = await BaseHTTPRequest.read(1024)
	sdata = data.decode()
	req = Request(data=sdata)
	req.parser()
	if req.url == url and req.method == method:
		resp = Response(body='Sneed Server', content_type="text/html")
	elif req.url != url:
		resp = Response(body='URL Not Found', status=404)
	elif req.method != method:
		resp = Response(body='Method Not Allowed', status=405)
	else:
		resp = Response(body='Internal Server Error', status=500)
	
	x = resp.output()

	return BaseHTTPResponse.write(x)


class FastHTTPServer:

	def run_server(self, app, host="0.0.0.0", port=8000):
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
