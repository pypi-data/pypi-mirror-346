import requests
from .errors import handle_amap_error
from gaode_mcp_server.src.config import AMAP_KEY

class AMapClient:
    def __init__(self, key=AMAP_KEY):
        self.key = key

    def get(self, url, params):
        params['key'] = self.key
        try:
            resp = requests.get(url, params=params, timeout=5)
            data = resp.json()
        except Exception as e:
            raise Exception(f"请求高德API失败: {e}")
        if data.get('status') != '1':
            handle_amap_error(data)
        return data
