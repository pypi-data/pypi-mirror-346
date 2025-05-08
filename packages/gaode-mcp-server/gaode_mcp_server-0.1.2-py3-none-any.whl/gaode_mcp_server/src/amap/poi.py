from gaode_mcp_server.src.amap.client import AMapClient

class POIAPI:
    def __init__(self, client: AMapClient):
        self.client = client

    def search(self, keywords: str, city: str = None, types: str = None, **kwargs):
        url = "https://restapi.amap.com/v3/place/text"
        params = {"keywords": keywords}
        if city:
            params["city"] = city
        if types:
            params["types"] = types
        params.update(kwargs)
        return self.client.get(url, params)
