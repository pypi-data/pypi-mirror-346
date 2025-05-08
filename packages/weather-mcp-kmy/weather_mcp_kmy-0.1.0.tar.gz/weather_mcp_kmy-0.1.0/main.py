import json
import httpx
import argparse
from typing import Any
from mcp.server.fastmcp import FastMCP

# 初始化mcp服务器
mcp=FastMCP("WeatherServer")

# 查询天气api配置
OPENWEATHER_API_BASE="https://api.openweathermap.org/data/2.5/weather"
API_KEY=None
USER_AGENT="weather-app/1.0"

# 获取天气的函数
async def fetch_weather(city:str)->dict[str,Any]|None:
    """
       从API中获取天气
    """
    if API_KEY is None:
        return "请输入天气查询的api_key"
    # 构建参数
    params={
        "q":city,
        "appid":API_KEY,
        "units":"metric",
        "lang": "zh_cn"
    }
    # 头部信息
    headers = {"User-Agent":USER_AGENT}
    async with httpx.AsyncClient() as client:
        try:
            # 执行查询天气
            response = await client.get(OPENWEATHER_API_BASE, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        # 异常情况
        except httpx.HTTPStatusError as e:
            return f"http状态异常{e.response.status_code}:{e.response.content}"
        except Exception as e:
            return f"http请求异常:{str(e)}"
# 格式化天气的函数
def format_weather(data:dict[str,Any]|str)->str:
    """
    将天气转化成易于理解的文本
    :param data:
    :return:
    """
    # 判断如果是字符串类型  则转换为json类型
    if isinstance(data,str):
        try:
            data = json.loads(data)
        except Exception as e:
            return f"无法解读的天气数据{str(e)}"
    if "error" in data:
        return f"{data['error']}"
    # 获取天气数据中的变量
    city=data.get("name","未知")
    country=data.get("sys",{}).get("country","未知")
    temp=data.get("main",{}).get("temp","N/A")
    humidity=data.get("main",{}).get("humidity","N/A")
    wind_speed=data.get("wind",{}).get("speed","N/A")
    weather_list=data.get("weather",[{}])
    # 描述
    description=weather_list[0].get("description","未知")
    # 返回数据
    return (
        f"{city},{country}\n"
        f"温度:{temp}\n"
        f"湿度:{humidity}\n"
        f"风速:{wind_speed}\n"
        f"天气:{description}\n"
    )

# mcp的工具
@mcp.tool()
async def query_weather(city:str)->str:
    """
    输入指定城市的英文名称 返回今日的天气查询结果
    :param city:
    :return:
    """
    # 获取指定城市从的天气
    data=await fetch_weather(city)
    # 格式化天气数据
    return format_weather(data)


# 主函数
def main():
    parser=argparse.ArgumentParser(description="Weather Server")
    parser.add_argument("--api_key",type=str,required=True,help="你的天气网站的api_key")
    args=parser.parse_args()
    print("哈哈哈")
    # 声明全局变量
    global API_KEY
    # 设置变量值
    API_KEY=args.api_key
    # API_KEY="dshjsdjksdjkkjds"
    # 启动mcp服务
    mcp.run(transport="stdio")

# 启动逻辑
if __name__=="__main__":
    main()






