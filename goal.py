from fastpyservers import AsyncHTTPServer, response

ws = AsyncHTTPServer('sms_endpoint')

active_numbers = []

@ws.route('/')
async def index(request):
	if request.method == 'GET':
		return response.redirect('/signup')
	elif request.method == 'POST':
		return response.redirect('/reply')
	else:
		return response.status("404")

@ws.route('/signup', methods=['GET'])
async def signup(request):
	html_body = """
	<html><body>
	<form method="POST" action="/add_number">
	  Enter your number to recieve our texts:<br>
	  <input type="text" name="phone_no" value=""><br><br>
	  <input type="submit" value="Submit">
	</form> 
	</html></body>
	"""

	return response.html(html_body)

@ws.route('/add_number', methods=['POST'])
async def add_number(request):
	activate = active_numbers.append(request.args.value('phone_no'))
	return response.json({"Number Added":"Text 2672294439 to get more details"})

@ws.route('/reply', methods=['POST'])
async def reply_sms(request):
	if request.number is in active_numbers:
		return response.sms('Thanks for signing up')
	else:
		return response.sms('Visit our site to sign up')


		


