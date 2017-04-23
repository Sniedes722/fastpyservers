from fastpyservers import AsyncWebApp
from fastpyservers.requests import methods
from fastpyservers.responses import field, json

app = AsyncWebApp('v1')

app.queue([
	
	{"task": "Task 1", "on": field.datetime('')},
	{"task": "Task 2", "on": field.datetime('')},
	{"task": "Task 3", "on": field.datetime('')}
	
	
])

app.model("users": {
	"first_name": field.string(1, 60),
	"last_name": field.string(1, 100),
	"age": field.integer(>, 18),
	"birthday": field.datetime(''),
	"stocks": [
		{
			"price": field.price(USD), 
			"ticker_name": field.string(=, 3)
		}
	
	]
	
})

app.handler(model, methods['POST'], json) ## will return http://0.0.0.0:8080/users/?first_name=Shawn&last_name=Needz
app.handler('/queue', methods['GET','POST'], json)


if __name__ == '__main__':
	app.run()

## Route handlers elder version
async def router_handler(route, method, content_type, body):
	Response(body=body, content_type

## Error Handler
async def handle_method_error():
	Response(body='Method not allowed for URL', status=405)

async def handle_method_error():
	Response(body='URL not found', status=404)
