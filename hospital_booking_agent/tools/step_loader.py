import json
import requests
from typing import Dict, Any, List
from pathlib import Path
config_file = "./hospital_booking_agent/config/services_config.json"

API_BASE_URL = "https://localhost:8175/api/v1"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWRlbnRpZmllciI6IjEiLCJlbWFpbCI6ImFkbWluQGhvc3RuYW1lLmNvbSIsImZ1bGxOYW1lIjoiU3VwZXIgVXNlciIsIm5hbWUiOiJTdXBlciIsInN1cm5hbWUiOiJVc2VyIiwiaXBBZGRyZXNzIjoiMC4wLjAuMSIsImF2YXRhclVybCI6IiIsIm1vYmlsZXBob25lIjoiIiwiZXhwIjoxNzgxMjcwNDgzLCJpc3MiOiJodHRwczovL0JFLlNFUDQ5MC5uZXQiLCJhdWQiOiJCRS5TRVA0OTAifQ.kQIX9uvjN9UOPiBitp9JsO2DlPlFyIU4VTP1ZyM4k3Y"

HEADERS = {
    "Authorization": f"Bearer {JWT_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

CONFIG_PATH = Path(config_file)

def fetch_services() -> List[Dict[str, Any]]:
    resp = requests.get(f"{API_BASE_URL}/services", headers=HEADERS, verify=False)
    resp.raise_for_status()
    return resp.json()

def fetch_service_steps(service_id: int) -> List[Dict[str, Any]]:
    resp = requests.get(f"{API_BASE_URL}/services/{service_id}/servicesteps", headers=HEADERS, verify=False)
    resp.raise_for_status()
    return resp.json()

def init_config_file(path: Path = CONFIG_PATH):
    STEP_TYPE_CODE_MAP = {
        1: "select_specialty",
        2: "select_doctor",
        3: "select_timeline",
    }
    
    config: dict[str, dict] = {}

    services = fetch_services()
    for svc in services:
        svc_id = svc["id"]
        svc_name = svc["name"]
        steps_data = fetch_service_steps(svc_id)
        steps_data.sort(key=lambda x: x["stepOrder"])

        step_codes = []
        for s in steps_data:
            code = STEP_TYPE_CODE_MAP.get(s["steps"]["stepType"])
            if code:
                step_codes.append(code)

        config[str(svc_id)] = {
            "name": svc_name,
            "steps": step_codes
        }

    path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[init_config_file] Đã khởi tạo {path.resolve()}")

def get_service_config_file(config_path: str = config_file):
    config_file = Path(config_path)
    return json.loads(config_file.read_text(encoding="utf-8"))