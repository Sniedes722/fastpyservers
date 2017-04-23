async def router(method, route):
	return await match_route(route), await match_method(method)

async def match_route(_route):
	route = _route
	return route

async def match_method(_method):
	method = _method
	return method
		
