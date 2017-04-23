from fastpyservers import AsyncWebApp

import logging

app = AsyncWebApp('sms_endpoint')

model = {'sneed':'server'}
info = 'This is some text'

app.handler(func=model, route='/kv', method='POST', content_type='JSON')
app.handler(func=info, route='/text', method='GET', content_type='Text')
app.print_handlers()

if __name__ == '__main__':
    app.run(port=8080)
