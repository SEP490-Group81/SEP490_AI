import requests
from typing import Dict, Any, List
from pathlib import Path
from typing import Optional
from google.adk.tools import ToolContext
from dateutil import parser
from datetime import datetime, timezone, time, timedelta

agent_root = Path(__file__).resolve().parent.parent
config_file = agent_root / "config" / "services_list.json"

API_BASE_URL = "https://sep490-dabs-gsdjgbfbdgd8gkbb.eastasia-01.azurewebsites.net/api/v1"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWRlbnRpZmllciI6IjEiLCJlbWFpbCI6ImFkbWluQGhvc3RuYW1lLmNvbSIsImZ1bGxOYW1lIjoiU3VwZXIgVXNlciIsIm5hbWUiOiJTdXBlciIsInN1cm5hbWUiOiJVc2VyIiwiaXBBZGRyZXNzIjoiMC4wLjAuMSIsImF2YXRhclVybCI6IiIsIm1vYmlsZXBob25lIjoiIiwiZXhwIjoxNzgxMjcwNDgzLCJpc3MiOiJodHRwczovL0JFLlNFUDQ5MC5uZXQiLCJhdWQiOiJCRS5TRVA0OTAifQ.kQIX9uvjN9UOPiBitp9JsO2DlPlFyIU4VTP1ZyM4k3Y"

HEADERS = {
    "Authorization": f"Bearer {JWT_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def fetch_services(hospital_id: str) -> List[Dict[str, Any]]:
    resp = requests.get(f"{API_BASE_URL}/hospitals/{hospital_id}/services", headers=HEADERS, verify=False)
    resp.raise_for_status()
    return resp.json()

def fetch_service_steps(service_id: int) -> List[Dict[str, Any]]:
    resp = requests.get(f"{API_BASE_URL}/services/{service_id}/servicesteps", headers=HEADERS, verify=False)
    resp.raise_for_status()
    return resp.json()

def get_services_list(tool_context: Optional[ToolContext] = None):
    hospital_id = tool_context.state.get("selected_hospital") if tool_context else None

    STEP_TYPE_CODE_MAP = {
        1: "select_specialty",
        2: "select_doctor",
        3: "select_timeline",
    }

    config: dict[str, dict] = {}
    services = fetch_services(str(hospital_id))["result"]

    if not services:
        print(f"DEBUG: No services found for hospital ID {hospital_id}")
        return config

    print(f"DEBUG: services = {services})") 

    for svc in services:
        print(f"DEBUG: svc = {svc} ({type(svc)})") 
        svc_id = svc["id"]
        svc_name = svc["name"]
        steps_data = fetch_service_steps(svc_id)
        steps_data.sort(key=lambda x: x["stepOrder"])

        step_codes = []
        for s in steps_data:
            step_type = s["steps"]["stepType"]
            step_code = STEP_TYPE_CODE_MAP.get(step_type)
            if step_code:
                step_codes.append(step_code)

        config[str(svc_id)] = {
            "name": svc_name,
            "steps": step_codes
        }

    if tool_context:
        tool_context.state["services_list"] = config
    print(f"DEBUG: config content: {config}")
    return config

def get_specialization_by_hospital(tool_context: Optional[ToolContext] = None):
    if not tool_context:
        raise ValueError("tool_context is required")
    
    hospital_id = tool_context.state.get("selected_hospital")
    if not hospital_id:
        raise ValueError("Missing 'selected_hospital' in tool_context.state")
    print(f"DEBUG: hospital_id = {hospital_id}")
    resp = requests.get(f"{API_BASE_URL}/hospitals/{hospital_id}/specialization", headers=HEADERS, verify=False)
    resp.raise_for_status()

    data = resp.json()
    raw_list = data.get("result", [])
    structured: Dict[str, Dict[str, str]] = {}
    for item in raw_list:
        sid = item.get("id")
        name = item.get("name", "")
        description = item.get("description", "")
        # Bỏ qua nếu id hoặc name không hợp lệ
        if not isinstance(sid, int) or not isinstance(name, str):
            continue
        structured[name] = {
            "id": str(sid),
            "description": description
        }

    print(f"DEBUG: specialization data = {structured}")
    tool_context.state["specialization_list"] = structured
    return structured

def get_doctor_list(tool_context: Optional[ToolContext] = None)  -> List[Dict[str, Any]]:
    if not tool_context:
        raise ValueError("tool_context is required")
    
    hospital_id = tool_context.state.get("selected_hospital")
    if not hospital_id:
        raise ValueError("Missing 'selected_hospital' in tool_context.state")
    print(f"DEBUG: hospital_id = {hospital_id}")

    specialization_id = tool_context.state.get("selected_specialization")
    print(f"DEBUG: specialization_id = {specialization_id}")

    resp = {}
    if not specialization_id:
        resp = requests.get(f"{API_BASE_URL}/doctors/by-hospital/{hospital_id}", headers=HEADERS, verify=False)
        resp.raise_for_status()

    else:
        resp = requests.get(f"{API_BASE_URL}/hospitals/{hospital_id}/doctors/by-specialization/{specialization_id}", headers=HEADERS, verify=False)
        resp.raise_for_status()
    
    data = resp.json()
    raw_list = data.get("result", [])

    doctors: List[Dict[str, Any]] = []
    for item in raw_list:
        user = item.get("user", {})
        
        raw_quals = item.get("qualification", [])
        quals = []
        for q in raw_quals:
            quals.append({
                "id": q.get("id"),
                "qualificationName": q.get("qualificationName") or q.get("qualification_name") or "",
                "instituteName": q.get("instituteName") or q.get("institute_name") or "",
                "procurementYear": q.get("procurementYear") or q.get("procurement_year") or None
            })
        raw_specs = item.get("specializations", [])
        specs = []
        for s in raw_specs:
            specs.append({
                "id": s.get("id"),
                "name": s.get("name", ""),
                "description": s.get("description", "")
            })
        
        doctors.append({
            "id": item.get("id"),
            "userName": user.get("userName") or user.get("username") or "",
            "description": item.get("description", ""),
            "fullname": user.get("fullname") or user.get("fullName") or "",
            "avatarUrl": user.get("avatarUrl") or user.get("avatar_url") or "",
            "qualification": quals,
            "specializations": specs
        })
    print(f"DEBUG: data doctor = {doctors}")
    tool_context.state["doctor_list"] = doctors
    return doctors

def get_timeline_list(date_from: str, date_to: str, tool_context: Optional[ToolContext] = None): 
    """
    Trả về danh sách các khung giờ khám của bác sĩ trong khoảng thời gian nhất định.

    Args:
        date_from: là chỉ số chứa thông tin về ngày bắt đầu để lọc khung giờ khám (YYYY‑MM‑DD format).
        date_to: là chỉ số chứa thông tin về ngày kết thúc để lọc khung giờ khám (YYYY‑MM‑DD format).
        tool_context: là ngữ cảnh công cụ ADK, chứa thông tin về bệnh viện, chuyên khoa và bác sĩ đã chọn.

    Returns:
        Danh sách các khung giờ khám.
    """
    if not tool_context:
        raise ValueError("tool_context is required")
    
    hospital_id = int(tool_context.state.get("selected_hospital"))
    if not hospital_id:
        raise ValueError("Missing 'selected_hospital' in tool_context.state")
    print(f"DEBUG: hospital_id = {hospital_id}")

    specialization_id = int(tool_context.state.get("selected_specialization"))
    print(f"DEBUG: specialization_id = {specialization_id}")

    doctor_id = int(tool_context.state.get("selected_doctor"))
    print(f"DEBUG: doctor_id = {doctor_id}")

    payload = {
        "doctorIds": [doctor_id] or [],
        "specializationId": specialization_id or None,
        "dateFrom": parse_to_iso_date(date_from) or datetime.now(timezone.utc),
        "dateTo": parse_to_iso_date(date_to) or datetime.now(timezone.utc) + timedelta(days=30)
    }
    print(f"DEBUG: payload = {payload}")
    url = f"{API_BASE_URL}/schedules/{hospital_id}/hospital/specialization"
    resp = requests.post(url, json=payload, headers=HEADERS, verify=False)
    resp.raise_for_status()
    data = resp.json()
    print(f"DEBUG: timeline result = {data}")
    tool_context.state["timeline_list"] = data
    return data
    

def parse_to_iso_date(user_input: str) -> str:
    """
    Nhận chuỗi đầu vào là ngày (ví dụ '24/7/2025', 'July 24 2025').
    Trả về ISO timestamp: YYYY‑MM‑DDT00:00:00.000Z (không quan tâm giờ).
    """
    dt = parser.parse(user_input, dayfirst=True,
                      default=datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0))
    dt = datetime.combine(dt.date(), time(0, 0, 0, tzinfo=dt.tzinfo))
    if dt.tzinfo is None:
        from dateutil import tz
        dt = dt.replace(tzinfo=tz.UTC)
    # Xuất ISO có Z
    iso_str = dt.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return iso_str