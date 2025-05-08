from gaode_mcp_server.src.amap.client import AMapClient

class GeoAPI:
    def __init__(self, client: AMapClient):
        self.client = client

    def geocode(self, address: str, city: str = None):
        url = "https://restapi.amap.com/v3/geocode/geo"
        params = {"address": address}
        if city:
            params["city"] = city
        return self.client.get(url, params)

    def regeocode(self, location: str, poitype: str = None, radius: int = 1000, extensions: str = 'base'):
        url = "https://restapi.amap.com/v3/geocode/regeo"
        params = {"location": location, "radius": radius, "extensions": extensions}
        if poitype:
            params["poitype"] = poitype
        return self.client.get(url, params)
