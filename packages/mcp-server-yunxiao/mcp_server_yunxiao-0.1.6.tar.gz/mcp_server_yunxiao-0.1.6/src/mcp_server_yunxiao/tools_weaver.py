from typing import Annotated, Optional, List
from pydantic import Field
from .client import _call_api
from . import mcp
import json
from datetime import datetime

REGION_ALIAS_MAP = {
    "sheec": "ap-shenyang-ec",
    "sh": "ap-shanghai",
    "sao": "sa-saopaulo",
    "bjjr": "ap-beijing-fsi",
    "hzec": "ap-hangzhou-ec",
    "cgoec": "ap-zhengzhou-ec",
    "use": "na-ashburn",
    "xiyec": "ap-xian-ec",
    "cd": "ap-chengdu",
    "cq": "ap-chongqing",
    "shjr": "ap-shanghai-fsi",
    "szjr": "ap-shenzhen-fsi",
    "usw": "na-siliconvalley",
    "jkt": "ap-jakarta",
    "in": "ap-mumbai",
    "jnec": "ap-jinan-ec",
    "gz": "ap-guangzhou",
    "szsycft": "ap-shenzhen-sycft",
    "qyxa": "ap-qingyuan-xinan",
    "hk": "ap-hongkong",
    "sjwec": "ap-shijiazhuang-ec",
    "tpe": "ap-taipei",
    "gzopen": "ap-guangzhou-open",
    "jp": "ap-tokyo",
    "hfeec": "ap-hefei-ec",
    "qy": "ap-qingyuan",
    "bj": "ap-beijing",
    "whec": "ap-wuhan-ec",
    "csec": "ap-changsha-ec",
    "tsn": "ap-tianjin",
    "nj": "ap-nanjing",
    "de": "eu-frankfurt",
    "th": "ap-bangkok",
    "sg": "ap-singapore",
    "kr": "ap-seoul",
    "fzec": "ap-fuzhou-ec",
    "szx": "ap-shenzhen",
    "xbec": "ap-xibei-ec",
    "shadc": "ap-shanghai-adc",
    "shwxzf": "ap-shanghai-wxzf",
    "gzwxzf": "ap-guangzhou-wxzf",
    "szjxcft": "ap-shenzhen-jxcft",
    "shhqcft": "ap-shanghai-hq-cft",
    "shhqcftfzhj": "ap-shanghai-hq-uat-cft",
    "shwxzfjpyzc": "ap-shanghai-wxp-ops",
    "njxfcft": "ap-nanjing-xf-cft",
}

@mcp.tool()
def query_task_message(
    region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
    task_id: Annotated[str, Field(description="任务ID")],
    start_time: Annotated[Optional[str], Field(description="起始时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    end_time: Annotated[Optional[str], Field(description="结束时间，格式：YYYY-MM-DD HH:mm:ss")] = None,
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None
) -> str:
    """
    查询 VStation 事件
    Args:
        region: 地域，如 ap-guangzhou
        task_id: 任务ID
        start_time: 起始时间，格式：YYYY-MM-DD HH:mm:ss（可选，默认当天 00:00:00）
        end_time: 结束时间，格式：YYYY-MM-DD HH:mm:ss（可选，默认当天 23:59:59）
        region_alias: 地域别名（可选，若未传则自动匹配）
    Returns:
        str: 查询结果的JSON字符串
    """
    # 自动补全时间
    if not start_time or not end_time:
        today = datetime.now().strftime("%Y-%m-%d")
        if not start_time:
            start_time = f"{today} 00:00:00"
        if not end_time:
            end_time = f"{today} 23:59:59"
    # regionAlias 自动匹配
    alias = region_alias
    if not alias:
        for k, v in REGION_ALIAS_MAP.items():
            if v == region:
                alias = k
                break
    filters = [{
        "Name": "task_id",
        "Values": [task_id]
    }]
    params = {
        "Region": region,
        "Filters": filters,
        "StartTime": start_time,
        "EndTime": end_time,
        "Offset": 0,
        "Limit": 100,
        "Action": "QueryTaskMessage",
        "AppId": "251006228",
        "RequestSource": "YunXiao",
        "SubAccountUin": "493083759",
        "Uin": "493083759",
        "regionAlias": alias or ""
    }
    return _call_api("/weaver/upstream/terra/QueryTaskMessage", params)

@mcp.tool()
def describe_error_codes(
    region: Annotated[str, Field(description="地域，如 ap-guangzhou")],
    region_alias: Annotated[Optional[str], Field(description="地域别名")] = None
) -> str:
    """
    查询 VStation 错误码
    Args:
        region: 地域，如 ap-guangzhou
        region_alias: 地域别名（可选，若未传则自动匹配）
    Returns:
        str: 查询结果的JSON字符串
    """
    # regionAlias 自动匹配
    alias = region_alias
    if not alias:
        for k, v in REGION_ALIAS_MAP.items():
            if v == region:
                alias = k
                break
    params = {
        "Region": region,
        "AppId": "251006228",
        "Action": "DescribeErrorCodes",
        "Uin": "493083759",
        "SubAccountUin": "493083759",
        "RequestSource": "YunXiao",
        "regionAlias": alias or ""
    }
    return _call_api("/weaver/upstream/terra/QueryTaskMessage", params) 