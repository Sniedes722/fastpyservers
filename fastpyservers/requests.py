from asyncio.streams import StreamReader

class BaseHTTPRequest(StreamReader):

	def __init__(self, name=None):
		self.name = name


class Request(dict):
	
	__slots__ = (
		'app', 'headers', 'body', '_method', 
		'_url', '_http_type', 'data', 
	)

	def __init__(self, data, app=None):
		_first_line = data.decode().rstrip("\n").split('\n')[0].split(' ')
		
		self.app = app
		self._method = _first_line[0]
		self._url = _first_line[1]
		self._http_type = _first_line[2]
		
	@property
	def method(self):
		return self._method
		
	@property
	def url(self):
		return self._url
		
	@property
	def http_type(self):
		return self._http_type
