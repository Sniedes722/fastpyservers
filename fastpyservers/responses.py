from asyncio.streams import StreamWriter

COMMON_STATUS_CODES = {
	200: b'OK',
	400: b'Bad Request',
	404: b'Not Found',
	500: b'Internal Server Error',
}
ALL_STATUS_CODES = {
	100: b'Continue',
	101: b'Switching Protocols',
	102: b'Processing',
	200: b'OK',
	201: b'Created',
	202: b'Accepted',
	203: b'Non-Authoritative Information',
	204: b'No Content',
	205: b'Reset Content',
	206: b'Partial Content',
	207: b'Multi-Status',
	208: b'Already Reported',
	226: b'IM Used',
	300: b'Multiple Choices',
	301: b'Moved Permanently',
	302: b'Found',
	303: b'See Other',
	304: b'Not Modified',
	305: b'Use Proxy',
	307: b'Temporary Redirect',
	308: b'Permanent Redirect',
	400: b'Bad Request',
	401: b'Unauthorized',
	402: b'Payment Required',
	403: b'Forbidden',
	404: b'Not Found',
	405: b'Method Not Allowed',
	406: b'Not Acceptable',
	407: b'Proxy Authentication Required',
	408: b'Request Timeout',
	409: b'Conflict',
	410: b'Gone',
	411: b'Length Required',
	412: b'Precondition Failed',
	413: b'Request Entity Too Large',
	414: b'Request-URI Too Long',
	415: b'Unsupported Media Type',
	416: b'Requested Range Not Satisfiable',
	417: b'Expectation Failed',
	422: b'Unprocessable Entity',
	423: b'Locked',
	424: b'Failed Dependency',
	426: b'Upgrade Required',
	428: b'Precondition Required',
	429: b'Too Many Requests',
	431: b'Request Header Fields Too Large',
	500: b'Internal Server Error',
	501: b'Not Implemented',
	502: b'Bad Gateway',
	503: b'Service Unavailable',
	504: b'Gateway Timeout',
	505: b'HTTP Version Not Supported',
	506: b'Variant Also Negotiates',
	507: b'Insufficient Storage',
	508: b'Loop Detected',
	510: b'Not Extended',
	511: b'Network Authentication Required'
}

def _parse_headers(_headers):
	headers = b''
	for key, value in _headers:
		headers += (b'%b: %b\r\n' % (str(key).encode(), str(value).encode('utf-8')))
	return headers

def _encode_body(data):
	try:
		return data.encode()
	except AttributeError:
		return str(data).encode()

class BaseHTTPResponse(StreamWriter):
	
	def __init__(self):
		self.name = None

class Response(dict):

	__slots__ = ('body', 'status', 'status_code', 'content_type', 'headers', )
	
	def __init__(self, body=None, status=200, headers=None, content_type='text/plain', body_bytes=b''):
		
		self.content_type = content_type
		
		if body is not None:
			self.body = _encode_body(body)
		else:
			self.body = body_bytes
		
		self.headers = headers or {}
		
		self.status = status
		self.status_code = ALL_STATUS_CODES.get(self.status)
		
	def output(self, version="1.1", keep_alive=False, keep_alive_timeout=None):
		timeout_header = b''
		if keep_alive and keep_alive_timeout is not None:
			timeout_header = b'Keep-Alive: %d\r\n' % keep_alive_timeout
			self.headers['Content-Length'] = self.headers.get('Content-Length', len(self.body))
			
			if not status:
				status = ALL_STATUS_CODES.get(self.status, b'UNKNOWN RESPONSE')
		self.headers['Content-Length'] = self.headers.get('Content-Length', len(self.body))
		self.headers['Content-Type'] = self.headers.get('Content-Type', self.content_type)
		headers = _parse_headers(self.headers.items())
		return (b'HTTP/%b %d %b\r\n'
				b'Connection: %b\r\n'
				b'%b'
				b'%b\r\n'
				b'%b') % (
					version.encode(), 
					self.status, 
					self.status_code,
					b'keep-alive' if keep_alive else b'close',
					timeout_header,
					headers,
					self.body)
