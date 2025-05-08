from gaode_mcp_server.src.amap.client import AMapClient

class IPAPI:
    def __init__(self, client: AMapClient):
        self.client = client

    def ip_location(self, ip: str = None):
        url = "https://restapi.amap.com/v3/ip"
        params = {}
        if ip:
            params["ip"] = ip
        return self.client.get(url, params)
