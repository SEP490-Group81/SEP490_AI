from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from hospital_booking_agent.sub_agents.plan_agent import prompt
from hospital_booking_agent.shared_libraries import types

specialty_tool = Agent(
    model="gemini-2.0-flash-001",
    name="specialty_selection",
    description="Chọn chuyên khoa phù hợp dựa trên lý do khám của bệnh nhân",
    instruction=prompt.SPECIALTY_SELECTION_AGENT_INSTR,
    input_schema=types.SpecialtyInput,
    output_schema= types.SpecialtyOutput
)

timeline_tool = Agent(
    model="gemini-2.0-flash-001",
    name="timeline_selection",
    description="Đề xuất khung giờ khám dựa trên chuyên khoa và bệnh viện",
    instruction=prompt.TIMELINE_SELECTION_AGENT_INSTR,
    input_schema= types.TimelineInput,
    output_schema= types.TimelineOutput
)

doctor_tool = Agent(
    model="gemini-2.0-flash-001",
    name="doctor_selection",
    description="Chọn bác sĩ dựa trên chuyên khoa và tiêu chí",
    instruction=prompt.DOCTOR_SELECTION_AGENT_INSTR,
    input_schema= types.DoctorInput,
    output_schema= types.DoctorOutput
)

hospital_services_agent = Agent(
    model="gemini-2.0-flash-001",
    name="hospital_services_agent",
    description="Lấy danh sách dịch vụ khám tương ứng với bệnh viện được chọn",
    instruction=prompt.HOSPITAL_SERVICES_AGENT_INSTR,
    input_schema= types.HospitalServicesInput,
    output_schema= types.HospitalServicesOutput
)