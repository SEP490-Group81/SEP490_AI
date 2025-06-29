import json
from pathlib import Path
from hospital_booking_agent.sub_agents.plan_agent.tools import specialty_tool, timeline_tool, doctor_tool

agent_root = Path(__file__).resolve().parent.parent
config_file = agent_root / "config" / "services_config.json"

tool_map = {
    "select_specialty": specialty_tool,
    "select_doctor": doctor_tool,
    "select_timeline": timeline_tool
}

def tools_for_service(service_code: str, config_path: str = config_file):
    config_file = Path(config_path)
    cfg = json.loads(config_file.read_text(encoding="utf-8"))
    svc_cfg = cfg.get(service_code, {})
    steps = svc_cfg.get("steps", [])
    constraints = svc_cfg.get("constraints", {})
    step_tools = [tool_map[step] for step in steps if step in tool_map]
    return {"steps": step_tools, "constraints": constraints}