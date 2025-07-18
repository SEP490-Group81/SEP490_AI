import json
import requests
from typing import Dict, Any, List
from pathlib import Path
from typing import Optional
from google.adk.tools import ToolContext

agent_root = Path(__file__).resolve().parent.parent
config_file = agent_root / "config" / "services_config.json"

API_BASE_URL = "https://localhost:8175/api/v1"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWRlbnRpZmllciI6IjEiLCJlbWFpbCI6ImFkbWluQGhvc3RuYW1lLmNvbSIsImZ1bGxOYW1lIjoiU3VwZXIgVXNlciIsIm5hbWUiOiJTdXBlciIsInN1cm5hbWUiOiJVc2VyIiwiaXBBZGRyZXNzIjoiMC4wLjAuMSIsImF2YXRhclVybCI6IiIsIm1vYmlsZXBob25lIjoiIiwiZXhwIjoxNzgxMjcwNDgzLCJpc3MiOiJodHRwczovL0JFLlNFUDQ5MC5uZXQiLCJhdWQiOiJCRS5TRVA0OTAifQ.kQIX9uvjN9UOPiBitp9JsO2DlPlFyIU4VTP1ZyM4k3Y"

HEADERS = {
    "Authorization": f"Bearer {JWT_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def tools_for_service(service_id: str, tool_context: Optional[ToolContext] = None):
    tool_map = {
        "select_specialty": "specialization_tool",
        "select_doctor": "doctor_tool",
        "select_timeline": "timeline_tool"
    }

    if not tool_context:
        raise ValueError("tool_context is required")

    if tool_context:
        tool_context.state["selected_service"] = service_id
    cfg = tool_context.state.get("services_config")
    if not cfg:
        raise ValueError("Missing 'services_config' in tool_context.state")

    svc_cfg = cfg.get(service_id, {})
    if not svc_cfg:
        raise ValueError(f"Service config for service_id '{service_id}' not found in services_config")

    steps = svc_cfg.get("steps", [])
    step_tools = [tool_map[step] for step in steps if step in tool_map]

    print(f"DEBUG: tools_for_service({service_id}) -> steps: {steps} -> tools: {step_tools}")
    return {"steps": step_tools}

def fetch_services(hospital_id: str) -> List[Dict[str, Any]]:
    resp = requests.get(f"{API_BASE_URL}/hospitals/{hospital_id}/services", headers=HEADERS, verify=False)
    resp.raise_for_status()
    return resp.json()

def fetch_service_steps(service_id: int) -> List[Dict[str, Any]]:
    resp = requests.get(f"{API_BASE_URL}/services/{service_id}/servicesteps", headers=HEADERS, verify=False)
    resp.raise_for_status()
    return resp.json()

def get_services_config(tool_context: Optional[ToolContext] = None):
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
        tool_context.state["services_config"] = config
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
    tool_context.state["specialization_config"] = structured
    return structured