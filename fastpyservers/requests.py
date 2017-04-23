from asyncio.streams import StreamReader

async def get_request(BaseHTTPRequest, Request):
	data = await BaseHTTPRequest.read(1024)
	return Request._parse_request(data=data)


class BaseHTTPRequest(StreamReader):

	def __init__(self, name=None):
		self.name = name


class Request(dict):
	
	__slots__ = (
		'app', 'headers', 'body',  
	)

	def __init__(self, app=None):
		self.app = app
		self.headers = None
		self.body = None

	def _parse_request(self, data):
		return data
