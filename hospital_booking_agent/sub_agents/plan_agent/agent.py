from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from hospital_booking_agent.sub_agents.plan_agent import prompt
from hospital_booking_agent.tools.step_loader import tools_for_service

hospital_services_agent = Agent(
    model="gemini-2.0-flash-001",
    name="hospital_services_agent",
    description="Lấy danh sách dịch vụ khám tương ứng với bệnh viện được chọn",
    instruction=prompt.HOSPITAL_SERVICES_AGENT_INSTR,
    input_schema={
        "hospital_id": str
    },
    output_schema={
        "services": list
    }
)

service_loader_tool = AgentTool(
    name="load_service_steps",
    description="Nhập vào service_code (string), trả về danh sách các bước (tool) cần thực hiện từ services_config.json",
    fn=tools_for_service,
    input_schema={"service_code": str},
    output_schema={"steps": list}
)


plan_agent = Agent(
    model="gemini-2.0-flash-001",
    name="plan_agent",
    description="A sub-agent that plans the hospital appoinment base on user input",
    instruction=prompt.PLAN_AGENT_INSTR,
    output_key="appointment_plan",
    tools=[service_loader_tool, AgentTool(agent=hospital_services_agent)],
    before_agent_callback=None
)