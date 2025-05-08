from mcp.server.fastmcp import FastMCP
from .amap.client import AMapClient
from .amap import WeatherAPI
from .amap.geo import GeoAPI
from .amap.route import RouteAPI
from .amap.ip import IPAPI
from .amap import POIAPI
from .config import AMAP_KEY, parser
from gaode_mcp_server.src.utils.tool_wrapper import tool_wrapper

mcp = FastMCP("高德MCP服务")

amap_client = AMapClient(AMAP_KEY)

@tool_wrapper("天气查询")
@mcp.tool()
def query_weather(city: str, extensions: str = 'base'):
    """
    查询天气信息
    :param city: 城市编码或名称
    :param extensions: base(实时) 或 all(预报)
    :return: 天气信息
    """
    weather_api = WeatherAPI(amap_client)
    data = weather_api.get_weather(city, extensions)
    if 'lives' in data and data['lives']:
        for item in data['lives']:
            item['weather_desc'] = item.get('weather', '')
    if 'forecasts' in data and data['forecasts']:
        for forecast in data['forecasts']:
            for cast in forecast.get('casts', []):
                cast['weather_desc_day'] = cast.get('dayweather', '')
                cast['weather_desc_night'] = cast.get('nightweather', '')
    return data

@tool_wrapper("地理编码")
@mcp.tool()
def geocode(address: str, city: str = None):
    """
    地理编码（地址转经纬度）
    :param address: 地址文本
    :param city: 城市
    :return: 地理编码结果
    """
    geo_api = GeoAPI(amap_client)
    return geo_api.geocode(address, city)

@tool_wrapper("逆地理编码")
@mcp.tool()
def reverse_geocode(location: str, poitype: str = None, radius: int = 1000, extensions: str = 'base'):
    """
    逆地理编码（经纬度转地址）
    :param location: 经纬度（如 '116.481488,39.990464'）
    :param poitype: 兴趣点类型（可选）
    :param radius: 查询半径，单位米（默认1000）
    :param extensions: base或all，返回内容控制
    :return: 逆地理编码结果
    """
    geo_api = GeoAPI(amap_client)
    return geo_api.regeocode(location, poitype, radius, extensions)

@tool_wrapper("驾车路径规划")
@mcp.tool()
def route_driving(origin: str, destination: str, **kwargs):
    """
    路径规划-驾车
    :param origin: 起点经纬度
    :param destination: 终点经纬度
    :param kwargs: 其他高德API支持的参数
    :return: 路径规划结果
    """
    route_api = RouteAPI(amap_client)
    return route_api.driving(origin, destination, **kwargs)

@tool_wrapper("步行路径规划")
@mcp.tool()
def route_walking(origin: str, destination: str, **kwargs):
    """
    路径规划-步行
    :param origin: 起点经纬度
    :param destination: 终点经纬度
    :param kwargs: 其他高德API支持的参数
    :return: 路径规划结果
    """
    route_api = RouteAPI(amap_client)
    return route_api.walking(origin, destination, **kwargs)

@tool_wrapper("骑行路径规划")
@mcp.tool()
def route_bicycling(origin: str, destination: str, **kwargs):
    """
    路径规划-骑行
    :param origin: 起点经纬度
    :param destination: 终点经纬度
    :param kwargs: 其他高德API支持的参数
    :return: 路径规划结果
    """
    route_api = RouteAPI(amap_client)
    return route_api.bicycling(origin, destination, **kwargs)

@tool_wrapper("公交路径规划")
@mcp.tool()
def route_transit(origin: str, destination: str, city: str, **kwargs):
    """
    路径规划-公交
    :param origin: 起点经纬度
    :param destination: 终点经纬度
    :param city: 城市名称
    :param kwargs: 其他高德API支持的参数
    :return: 路径规划结果
    """
    route_api = RouteAPI(amap_client)
    return route_api.transit(origin, destination, city, **kwargs)

@tool_wrapper("IP定位")
@mcp.tool()
def ip_location(ip: str = None):
    """
    IP定位
    :param ip: IP地址（可选，默认取客户端IP）
    :return: 定位结果
    """
    ip_api = IPAPI(amap_client)
    return ip_api.ip_location(ip)

@tool_wrapper("POI搜索")
@mcp.tool()
def poi_search(keywords: str, city: str = None, types: str = None, **kwargs):
    """
    POI搜索（地点/兴趣点检索）
    :param keywords: 关键字
    :param city: 城市名称（可选）
    :param types: POI类型（可选）
    :param kwargs: 其他高德API支持的参数
    :return: 搜索结果
    """
    poi_api = POIAPI(amap_client)
    return poi_api.search(keywords, city, types, **kwargs)

def main():
    args, _ = parser.parse_known_args()
    
    print(f"Server starting with API key: {'*' * len(args.key) if args.key else '(none)'}")
    mcp.run()
    print("Server stopped")

if __name__ == "__main__":
    main()