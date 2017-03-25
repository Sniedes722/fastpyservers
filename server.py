import asyncio
import uvloop

from httptools import HttpRequestParser
import functools
import os
import signal
import logging

log = logging.getLogger(__name__)

clients = {}  # task -> (reader, writer)

def accept_client(client_reader, client_writer):
    task = asyncio.Task(handle_client(client_reader, client_writer))
    clients[task] = (client_reader, client_writer)

    def client_done(task):
        del clients[task]
        client_writer.close()
        log.info("End Connection")

    log.info("New Connection")
    task.add_done_callback(client_done)
    
@asyncio.coroutine
def handle_client(client_reader, client_writer):
    # send a hello to let the client know they are connected
    client_writer.write("HELLO\n".encode())

    # give client a chance to respond, timeout after 10 seconds
    data = yield from asyncio.wait_for(client_reader.readline(),
                                       timeout=10.0)

    if data is None:
        log.warning("Expected GET, received None")
        return

    sdata = data.decode().rstrip()
    if sdata != "GET / HTTP/1.1":
        log.warning("Expected GET, received '%s'", sdata)
        return

    # now be an echo back server until client sends a bye
    i = 0  # sequence number
    # let client know we are ready
    client_writer.write("READY\n".encode())
    while True:
        i = i + 1
        # wait for input from client
        data = yield from asyncio.wait_for(client_reader.readline(),
                                           timeout=10.0)
        if data is None:
            log.warning("Received no data")
            # exit echo loop and disconnect
            return

        sdata = data.decode().rstrip()
        if sdata.upper() == 'BYE':
            client_writer.write("BYE\n".encode())
            break
        response = ("ECHO %d: %s\n" % (i, sdata))
        client_writer.write(response.encode())

def ask_exit(signame, loop):
    print("got signal %s: exit" % signame)
    loop.stop()

def main():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                functools.partial(ask_exit, signame, loop))
    
    f = asyncio.start_server(accept_client, host="0.0.0.0", port=8080)
    print("Event loop running forever, press Ctrl+C to interrupt.")
    print("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())
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
