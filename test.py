from fastpyservers import AsyncWebApp

import logging

app = AsyncWebApp('sms_endpoint')

if __name__ == '__main__':
    app.run(port=8080)
