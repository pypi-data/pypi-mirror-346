from mcp.server.fastmcp import FastMCP
from hashlib import md5
import requests

mcp = FastMCP("DemoMCP")

APP_KEY = "AI_MEETING"
SECRET_KEY = "0266a29fa1fa4e02a1e960f25e4ae87e"
BASE_URL = "https://shrg.test.searegal.com"

def generate_x_sign(app_key: str, secret_key: str) -> str:
    combined = f"{app_key}{secret_key}"
    first_hash = md5(combined.encode("utf-8")).hexdigest().lower()
    return md5(first_hash.encode("utf-8")).hexdigest().lower()

def auth_headers():
    return {
        "X-App-Key": APP_KEY,
        "X-Sign": generate_x_sign(APP_KEY, SECRET_KEY),
        "Content-Type": "application/json"
    }

def check_meeting_permission(staffId: str) -> bool:
    url = f"{BASE_URL}/enterprise/staff/ai/all-permission"
    params = {"staffId": staffId}
    try:
        response = requests.get(url, params=params, headers=auth_headers(), timeout=5)
        if response.status_code != 200:
            return False
        permissions = response.json().get("data", [])
        return any(p.get("permissionKey") == "meeting-reservation-list" for p in permissions)
    except Exception as e:
        print(f"[Error] Permission check failed: {e}")
        return False

@mcp.tool()
def get_meeting_room_list():
    url = f"{BASE_URL}/enterprise/oa/meeting-room/ai/list"
    response = requests.post(url, headers=auth_headers())
    return response.json()

@mcp.tool()
def create_meeting_reservation(createBy: int, meetingDate: str, beginDt: str, endDt: str, meetingRoom: int, meetingTheme: str):
    if not check_meeting_permission(str(createBy)):
        return {"code": 403, "message": "This user does not have conference reservation permission."}

    url = f"{BASE_URL}/enterprise/oa/meeting-reservation/ai/create"
    payload = {
        "createBy": createBy,
        "meetingDate": meetingDate,
        "beginDt": beginDt,
        "endDt": endDt,
        "meetingRoom": meetingRoom,
        "meetingTheme": meetingTheme
    }
    response = requests.post(url, json=payload, headers=auth_headers())
    return response.json()

def main():
    print("Starting Meeting MCP server...")
    mcp.run(transport="stdio")