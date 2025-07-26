from hospital_booking_agent.shared_libraries.types import PatientProfile
from typing import Dict, List, Any, Optional
from hospital_booking_agent.tools.api_tools import *
from hospital_booking_agent.sub_agents.booking_agent.token_test import *
from google.adk.tools import ToolContext

"""Bookings is tools for Booking_Agent"""

#Hàm lấy Patient Profile
def fetch_patient_profile(
        patient_id: str, 
        patient_token: str,
        tool_context: Optional[ToolContext] = None):
    if not tool_context:
        raise ValueError("tool_context is required")
    patient_token = login_test()
    patient_id = decode_jwt_token(patient_token)
    profile = get_patient_profile(patient_id,patient_token)
    return profile

def book_appointment(
        hospital_id: int,
        service_id: int,
        specialization_id: int,
        doctor_id: int,
        appointment_date: str,
        slot_time: int,
        payment_method: int,
        note: str,
        token: str,
        tool_context: Optional[ToolContext] = None):
    if not tool_context:
        raise ValueError("tool_context is required")
    hospital_id = tool_context.state.get("selected_hospital") if tool_context else None
    service_id = tool_context.state.get("selected_service") if tool_context else None
    specialization_id = tool_context.state.get("selected_specialization") if tool_context else None
    doctor_id = tool_context.state.get("selected_doctor") if tool_context else None

    time_list = tool_context.state.get("timeline_list") if tool_context else None
    selected_timeline_id = tool_context.state.get("selected_timeline")
    appointment_date = None
    slot_time_work = None
    if time_list and "schedules" in time_list and selected_timeline_id is not None:
        for schedule in time_list["schedules"]:
            if schedule.get("id") == selected_timeline_id:
                appointment_date = schedule.get("workDate")
                slot_time_work = schedule.get("startTime")
                break

    # Determine slot_time based on selected_slot name
    if slot_time_work == "7:30 - 11:30":
        slot_time = 1
        display_slot_time = "Ca sáng 7h30"
    elif slot_time_work == "12h30 - 16:30": 
        slot_time = 2
        display_slot_time = "Ca chiều 12h30"
    else:
        slot_time = None 

    payment_method = 1
    note = "AI Đặt Lịch Khám Hộ Người Dùng"
    token = login_test()
    create_appointment(hospital_id,service_id,specialization_id,doctor_id,appointment_date,slot_time,payment_method,note,token)