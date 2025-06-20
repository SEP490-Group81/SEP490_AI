"""Booking agent and sub-agents, handling the confirmation and payment of bookable events."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

from hospital_booking_agent.shared_libraries.types import PatientProfile
from hospital_booking_agent.sub_agents.booking_agent import prompt

# Example functions
def create_appointment()-> dict:
    """Call the hospital’s custom booking API to finalize the appointment"""
    return {
        "status": "success",
        "message": "Booking agent initialized successfully."
    }

# Example functions
def fetch_patient_profile() -> dict:
    """Fetch the patient's stored profile."""
    return {
        "name": "John Doe",
        "date_of_birth": "1990-01-01",
        "phone": "+1234567890",
        "email": "Doe12345@gmail.com"
    }

# Example functions
def confirm_patient_info(patient_profile: PatientProfile) -> dict:
    """Confirm or correct the patient's profile."""
    # Simulate user confirmation
    return {
        "confirmed": True,
        "profile": patient_profile
    }

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