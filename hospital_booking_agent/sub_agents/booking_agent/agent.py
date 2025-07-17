"""Booking agent and sub-agents, handling the confirmation and payment of bookable events."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from hospital_booking_agent.sub_agents.booking_agent import prompt
from hospital_booking_agent.tools.api_tools import *
from hospital_booking_agent.tools.bookings import *



booking_agent = Agent(
    model="gemini-2.0-flash-001",
    name="booking_agent",
    description="A Doctor Booking Appointment Assistant that finalizes the booking process.",
    instruction=prompt.BOOKING_AGENT_INSTR,
    tools=[
        fetch_patient_profile,
        confirm_patient_info,
        create_appointment
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.0, top_p=0.5
    )
)