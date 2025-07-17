import json
import requests
from typing import Dict, Any, List
from pathlib import Path
from typing import Optional
from google.adk.tools import ToolContext

agent_root = Path(__file__).resolve().parent.parent
config_file = agent_root / "config" / "services_config.json"

def tools_for_service(service_id: str, config_path: str = str(config_file)):
    from hospital_booking_agent.sub_agents.plan_agent.tools import specialty_tool, timeline_tool, doctor_tool
    tool_map = {
        "select_specialty": specialty_tool,
        "select_doctor": doctor_tool,
        "select_timeline": timeline_tool
    }
    config_file = Path(config_path)
    cfg = json.loads(config_file.read_text(encoding="utf-8"))
    svc_cfg = cfg.get(service_id, {})
    steps = svc_cfg.get("steps", [])
    step_tools = [tool_map[step] for step in steps if step in tool_map]
    return {"steps": step_tools}

def get_services_config(config_path: str = str(config_file), tool_context: Optional[ToolContext] = None):
    print(f"DEBUG: ToolContext state: {tool_context.state["selected_hospital_id"] if tool_context else "No ToolContext provided"}")
    config_file = Path(config_path)
    cfg = json.loads(config_file.read_text(encoding="utf-8"))
    return cfg