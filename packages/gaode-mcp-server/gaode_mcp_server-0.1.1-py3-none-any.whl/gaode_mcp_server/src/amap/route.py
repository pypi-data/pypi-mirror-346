from gaode_mcp_server.src.amap.client import AMapClient

class RouteAPI:
    def __init__(self, client: AMapClient):
        self.client = client

    def driving(self, origin: str, destination: str, **kwargs):
        url = "https://restapi.amap.com/v3/direction/driving"
        params = {"origin": origin, "destination": destination}
        params.update(kwargs)
        return self.client.get(url, params)

    def walking(self, origin: str, destination: str, **kwargs):
        url = "https://restapi.amap.com/v3/direction/walking"
        params = {"origin": origin, "destination": destination}
        params.update(kwargs)
        return self.client.get(url, params)

    def bicycling(self, origin: str, destination: str, **kwargs):
        url = "https://restapi.amap.com/v4/direction/bicycling"
        params = {"origin": origin, "destination": destination}
        params.update(kwargs)
        return self.client.get(url, params)

    def transit(self, origin: str, destination: str, city: str, **kwargs):
        url = "https://restapi.amap.com/v3/direction/transit/integrated"
        params = {"origin": origin, "destination": destination, "city": city}
        params.update(kwargs)
        return self.client.get(url, params)
