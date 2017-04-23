from asyncio.streams import StreamReader

class BaseHTTPRequest(StreamReader):

	def __init__(self, name=None):
		self.name = name


class Request(dict):
	
	__slots__ = (
		'app', 'headers', 'body', '_method', 
		'_url', '_http_type', 'data', 
	)

	def __init__(self, data=None, app=None):
		self.data = data

	def parser(self):
		prse = self.data.rstrip("\n").split('\n')[0].split(' ')
		self._method = prse[0]
		self._url = prse[1]
		
	@property
	def method(self):
		return self._method
		
	@property
	def url(self):
		return self._url
