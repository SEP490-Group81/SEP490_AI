from google.adk.agents import Agent
from hospital_booking_agent.tools.step_loader import get_services_config
from hospital_booking_agent.sub_agents.plan_agent import prompt
from hospital_booking_agent.shared_libraries import types
from hospital_booking_agent.tools.step_loader import get_service_config_file
import requests

def get_specialties_by_hospital() -> list[dict]:
    url = f"https://sep490-dabs-gsdjgbfbdgd8gkbb.eastasia-01.azurewebsites.net/api/v1/specialization"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

specialty_tool = Agent(
    model="gemini-2.0-flash-001",
    name="specialty_selection",
    description="Chọn chuyên khoa phù hợp dựa trên lý do khám của bệnh nhân",
    instruction=prompt.SPECIALTY_SELECTION_AGENT_INSTR,
    input_schema=types.SpecialtyInput,
    tools=[get_specialties_by_hospital]
)

timeline_tool = Agent(
    model="gemini-2.0-flash-001",
    name="timeline_selection",
    description="Đề xuất khung giờ khám dựa trên chuyên khoa và bệnh viện",
    instruction=prompt.TIMELINE_SELECTION_AGENT_INSTR,
    input_schema= types.TimelineInput,
)

doctor_tool = Agent(
    model="gemini-2.0-flash-001",
    name="doctor_selection",
    description="Chọn bác sĩ dựa trên chuyên khoa và tiêu chí",
    instruction=prompt.DOCTOR_SELECTION_AGENT_INSTR,
    input_schema= types.DoctorInput,
    )

hospital_services_agent = Agent(
    model="gemini-2.0-flash-001",
    name="hospital_services_agent",
    description="Tác nhân này sẽ cung cấp các dịch vụ của bệnh viện dựa trên cấu hình đã được tải",
    instruction=prompt.HOSPITAL_SERVICES_AGENT_INSTR,
    tools=[get_services_config],
    input_schema= types.HospitalServicesInput
)