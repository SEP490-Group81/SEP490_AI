from google.adk.agents import Agent
from hospital_booking_agent import prompt
from hospital_booking_agent.tools.memory import _load_precreated_itinerary

root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    description="A Doctor Booking Apointment Assistant using the services of multiple sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    before_agent_callback=_load_precreated_itinerary
)