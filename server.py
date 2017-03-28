"""
Copyright (c) Shawn Niederriter 2017

"""
import asyncio
import uvloop

import functools
import os
import signal
import logging

from constants import HTTP_METHODS

log = logging.getLogger(__name__)

clients = {}  # task -> (reader, writer)

def ask_exit(signame, loop):
    print("Exiting Sneed Web Server %s" % signame)
    loop.stop()

# this is the function causing the issues
async def accept_client(request, response):
    task = asyncio.ensure_future(handler(request, response))
    clients[task] = (request, response)
    
    def client_done(task):
        del clients[task]
        response.close()
        log.info("End Connection")
        
    log.info("New Connection")
    task.add_done_callback(client_done)

async def handler(request, response):
    http_body = '<html><body><h1>Hello, World!</h1></body></html>'
    test_response = 200
    # give client a chance to respond, timeout after 10 seconds
    data = await request.read(1024)
    sdata = data.decode().rstrip().replace('\r',' ').replace('\n','')
    method = sdata.split(' ')[0]
    url = sdata.split(' ')[1]
    http_type = sdata.split(' ')[2]
    headers = sdata.split(' ')[3:]
    test = dict(zip(headers[1::2], map(str, headers[1::2])))
    log.info("Method: %s", method)
    log.info("URL: %s", url)
    log.info("HTTP Type: %s", http_type)
    log.info("Headers: %s", headers)
    log.info("%s", len(http_body))
    
    response.write(b'HTTP/1.1 200 OK\r\n')
    response.write(b'Server: Sneed/0.0.1 (Linux x86_64)\r\n')
    response.write(b'Last-Modified: Mon, 27 Mar 2017 11:33:56 EST\r\n')
    response.write(b'Content-Length: 48\r\n')
    response.write(b'Content-Type: text/html\r\n')
    response.write(b'Connection: Closed\r\n')
    response.write(b'\r\n')
    response.write(b'<html><body><h1>Sneed Async Python Web Server</h1></body></html>\r\n')
    #print(r)


def main():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    host = "0.0.0.0"
    port = os.environ['PORT']
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

if __name__ == '__main__':
    log = logging.getLogger("")
    formatter = logging.Formatter("%(asctime)s %(levelname)s " +
                                  "[%(module)s:%(lineno)d] %(message)s")
    # setup console logging
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(formatter)
    log.addHandler(ch)
    main()