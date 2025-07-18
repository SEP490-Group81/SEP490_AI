from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from hospital_booking_agent.sub_agents.plan_agent import prompt
from hospital_booking_agent.tools.step_loader import tools_for_service
import hospital_booking_agent.sub_agents.plan_agent.tools as tools
from hospital_booking_agent.tools.hospitals import hos_select_tool
from hospital_booking_agent.tools.memory import memorize


plan_agent = Agent(
    model="gemini-2.0-flash-001",
    name="plan_agent",
    description="A sub-agent that plans the hospital appoinment base on user input",
    instruction=prompt.PLAN_AGENT_INSTR,
    output_key="appointment_plan",
    tools=[hos_select_tool, tools_for_service, memorize,
           AgentTool(agent=tools.hospital_services_agent),
            AgentTool(agent=tools.specialization_tool),
            AgentTool(agent=tools.doctor_tool),
            AgentTool(agent=tools.timeline_tool)],
    before_agent_callback=None
)