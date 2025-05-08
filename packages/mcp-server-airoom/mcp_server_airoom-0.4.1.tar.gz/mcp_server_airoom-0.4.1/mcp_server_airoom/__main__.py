"""MCP服务器主入口点 - 会议管理系统"""

import sys
import traceback
from hashlib import md5
import requests
from mcp.server.fastmcp import FastMCP

# 服务器配置
APP_KEY = "AI_MEETING"
SECRET_KEY = "0266a29fa1fa4e02a1e960f25e4ae87e"
BASE_URL = "https://shrg.test.searegal.com"

# 初始化MCP服务器
mcp = FastMCP("AIROOM会议管理系统")

def generate_x_sign(app_key: str, secret_key: str) -> str:
    """生成API请求签名"""
    combined = f"{app_key}{secret_key}"
    first_hash = md5(combined.encode("utf-8")).hexdigest().lower()
    return md5(first_hash.encode("utf-8")).hexdigest().lower()

def auth_headers():
    """生成认证请求头"""
    return {
        "X-App-Key": APP_KEY,
        "X-Sign": generate_x_sign(APP_KEY, SECRET_KEY),
        "Content-Type": "application/json"
    }

def check_meeting_permission(staffId: str) -> bool:
    """检查用户会议权限"""
    url = f"{BASE_URL}/enterprise/staff/ai/all-permission"
    try:
        response = requests.get(
            url,
            params={"staffId": staffId},
            headers=auth_headers(),
            timeout=5
        )
        if response.status_code == 200:
            permissions = response.json().get("data", [])
            return any(p.get("permissionKey") == "meeting-reservation-list" 
                      for p in permissions)
        return False
    except Exception as e:
        print(f"[权限检查错误] {str(e)}", file=sys.stderr)
        return False

@mcp.tool()
def get_meeting_room_list():
    """
    获取会议室列表
    
    返回:
        dict: 包含会议室数据的字典
    """
    try:
        response = requests.post(
            f"{BASE_URL}/enterprise/oa/meeting-room/ai/list",
            headers=auth_headers()
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "code": 500,
            "message": f"API请求失败: {str(e)}",
            "data": None
        }

@mcp.tool()
def create_meeting_reservation(
    createBy: int,
    meetingDate: str,
    beginDt: str,
    endDt: str,
    meetingRoom: int,
    meetingTheme: str
):
    """
    创建会议预约
    
    参数:
        createBy (int): 创建人ID
        meetingDate (str): 会议日期 (YYYY-MM-DD)
        beginDt (str): 开始时间 (HH:mm:ss)
        endDt (str): 结束时间 (HH:mm:ss)
        meetingRoom (int): 会议室ID
        meetingTheme (str): 会议主题
    """
    if not check_meeting_permission(str(createBy)):
        return {
            "code": 403,
            "message": "该用户无会议预约权限",
            "data": None
        }

    try:
        payload = {
            "createBy": createBy,
            "meetingDate": meetingDate,
            "beginDt": f"{meetingDate} {beginDt}",
            "endDt": f"{meetingDate} {endDt}",
            "meetingRoom": meetingRoom,
            "meetingTheme": meetingTheme
        }
        
        response = requests.post(
            f"{BASE_URL}/enterprise/oa/meeting-reservation/ai/create",
            json=payload,
            headers=auth_headers()
        )
        
        return {
            "code": response.status_code,
            "message": "操作成功" if response.ok else "操作失败",
            "data": response.json().get("data")
        }
        
    except Exception as e:
        return {
            "code": 500,
            "message": f"服务器内部错误: {str(e)}",
            "data": None
        }

def main():
    """主启动函数"""
    try:
        print("AIROOM会议管理系统启动中...", file=sys.stderr)
        mcp.run()
        print("服务器已正常停止", file=sys.stderr)
    except Exception as e:
        print(f"严重错误: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()