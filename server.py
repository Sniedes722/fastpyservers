import asyncio
import uvloop

from httptools import HttpRequestParser
import functools
import os
import signal
import logging

from httptools import HttpRequestParser
from httptools.parser.errors import HttpParserError

from constants import HTTP_METHODS

log = logging.getLogger(__name__)

clients = {}  # task -> (reader, writer)

def ask_exit(signame, loop):
    print("Exiting fastwebserver %s" % signame)
    loop.stop()

def accept_client(request, response):
    task = asyncio.Task(handler(request, response))
    clients[task] = (request, response)
    
    def client_done(task):
        del clients[task]
        response.close()
        log.info("End Connection")
        
    log.info("New Connection")
    task.add_done_callback(client_done)


@asyncio.coroutine
def handler(request, response):
    http_response = b"""\
    HTTP/1.1 200 OK
    
    Hello, World!
    """
    response.write(http_response)

    # give client a chance to respond, timeout after 10 seconds
    data = yield from asyncio.wait_for(request.read(1024),
                                       timeout=10.0)
    sdata = data.decode().rstrip()
    log.info("%s", sdata)


def main():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    host = "0.0.0.0"
    port = 8080
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