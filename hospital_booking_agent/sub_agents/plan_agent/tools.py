from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from hospital_booking_agent.sub_agents.plan_agent import prompt

specialty_tool = AgentTool(
    name="specialty_selection",
    description="Chọn chuyên khoa phù hợp dựa trên lý do khám của bệnh nhân",
    agent_name="specialty_selection_agent",
    instruction=prompt.SPECIALTY_SELECTION_AGENT_INSTR,
    input_schema={"reason": str},
    output_schema={"specialties": list}
)

timeline_tool = AgentTool(
    name="timeline_selection",
    description="Đề xuất khung giờ khám dựa trên chuyên khoa và bệnh viện",
    agent_name="timeline_selection_agent",
    instruction=prompt.TIMELINE_SELECTION_AGENT_INSTR,
    input_schema={"specialty": str, "hospital_id": str},
    output_schema={"available_slots": list}
)

hospital_tool = AgentTool(
    name="select_hospital",
    description="Chọn bệnh viện nơi khám",
    agent_name="hospital_selection_agent",
    instruction=prompt.HOSPITAL_SELECTION_AGENT_INSTR,
    input_schema={"user_profile": dict},
    output_schema={"hospital_id": str, "hospital_name": str}
)

doctor_tool = AgentTool(
    name="doctor_selection",
    description="Chọn bác sĩ dựa trên chuyên khoa và tiêu chí",
    agent_name="doctor_selection_agent",
    instruction=prompt.DOCTOR_SELECTION_AGENT_INSTR,
    input_schema={"specialty": str, "constraints": dict},
    output_schema={"doctor_id": str, "doctor_name": str}
)
