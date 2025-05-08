from gaode_mcp_server.src.amap.client import AMapClient

class WeatherAPI:
    def __init__(self, client: AMapClient):
        self.client = client

    def get_weather(self, city: str, extensions: str = 'base'):
        url = "https://restapi.amap.com/v3/weather/weatherInfo"
        params = {"city": city, "extensions": extensions}
        return self.client.get(url, params)
