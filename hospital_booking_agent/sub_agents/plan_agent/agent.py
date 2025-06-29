from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from hospital_booking_agent.sub_agents.plan_agent import prompt
from hospital_booking_agent.tools.step_loader import tools_for_service
import hospital_booking_agent.sub_agents.plan_agent.tools as tools
from hospital_booking_agent.shared_libraries import types


plan_agent = Agent(
    model="gemini-2.0-flash-001",
    name="plan_agent",
    description="A sub-agent that plans the hospital appoinment base on user input",
    instruction=prompt.PLAN_AGENT_INSTR,
    output_key="appointment_plan",
    tools=[tools_for_service, AgentTool(agent=tools.hospital_services_agent)],
    before_agent_callback=None
)