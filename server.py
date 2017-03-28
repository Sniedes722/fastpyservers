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
    print("Exiting fastwebserver %s" % signame)
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
    http_response = b'''HTTP/1.1 200 OK
    Server: Sneed/0.0.1 (Linux x86_64)
    Last-Modified: Mon, 27 Mar 2017 11:33:56 EST
    Content-Length: 12
    Content-Type: text/html
    Connection: Closed
    
    <html>
    <body>
    <h1>Hello, World!</h1>
    </body>
    </html>
    '''
    response.write(http_response)

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
    
    response.write(http_response)


def main():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    host = "0.0.0.0"
    port = os.environ['PORT']
    f = asyncio.start_server(accept_client, host=host, port=port, loop=loop)
    log.info('Fast WebPy Server running @ http://{}:{}'.format(host, port))
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