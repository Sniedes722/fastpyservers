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

clients = {}  # task -> (reader, writer)

def ask_exit(signame, loop):
	print("Exiting Sneed Web Server %s" % signame)
	loop.stop()

## This should eventually be part of a worker
async def accept_client(BaseHTTPRequest, BaseHTTPResponse):
	task = asyncio.ensure_future(handler("/event", BaseHTTPRequest, BaseHTTPResponse))
	clients[task] = (BaseHTTPRequest, BaseHTTPResponse)
		
	def client_done(task):
		del clients[task]
		BaseHTTPResponse.close()

	task.add_done_callback(client_done)


## This should be moved to app.py, as it's what we want people to be writing
async def handler(url, BaseHTTPRequest, BaseHTTPResponse):
	data = await BaseHTTPRequest.read(1024)
	req = Request(data=data)
	resp = Response(body='{"sneed":"server"}', content_type="application/json")
	return BaseHTTPResponse.write(resp.output())



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
