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
