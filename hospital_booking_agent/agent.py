from google.adk.agents import Agent
from hospital_booking_agent import prompt
from hospital_booking_agent.sub_agents.booking_agent.agent import booking_agent
from hospital_booking_agent.sub_agents.hospital_suggestion_agent.agent import hosptal_suggestion_agent
from hospital_booking_agent.sub_agents.plan_agent.agent import plan_agent
from hospital_booking_agent.tools.memory import _load_precreated_itinerary

root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="hospital_booking_agent",
    description="A Doctor Booking Apointment Assistant using the services of multiple sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        hosptal_suggestion_agent,
        plan_agent,
        booking_agent
    ],
    before_agent_callback=_load_precreated_itinerary
)
