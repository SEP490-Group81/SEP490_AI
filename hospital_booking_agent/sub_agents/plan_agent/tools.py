from google.adk.agents import Agent
from hospital_booking_agent.tools.step_loader import get_services_list, get_specialization_by_hospital, get_doctor_list, get_timeline_list
from hospital_booking_agent.sub_agents.plan_agent import prompt

specialization_tool = Agent(
    model="gemini-2.0-flash-001",
    name="specialization_selection",
    description="Chọn chuyên khoa phù hợp dựa trên lý do khám của bệnh nhân",
    instruction=prompt.specialization_selection_AGENT_INSTR,
    tools=[get_specialization_by_hospital]
)

timeline_tool = Agent(
    model="gemini-2.0-flash-001",
    name="timeline_selection",
    description="Đề xuất khung giờ khám dựa trên chuyên khoa và bệnh viện",
    instruction=prompt.TIMELINE_SELECTION_AGENT_INSTR,
    tools=[get_timeline_list]
)

doctor_tool = Agent(
    model="gemini-2.0-flash-001",
    name="doctor_selection",
    description="Chọn bác sĩ dựa trên chuyên khoa và tiêu chí",
    instruction=prompt.DOCTOR_SELECTION_AGENT_INSTR,
    tools=[get_doctor_list]
)

hospital_services_agent = Agent(
    model="gemini-2.0-flash-001",
    name="hospital_services_agent",
    description="Tác nhân này sẽ cung cấp các dịch vụ của bệnh viện dựa trên gọi `get_services_list`",
    instruction=prompt.HOSPITAL_SERVICES_AGENT_INSTR,
    tools=[get_services_list],
)