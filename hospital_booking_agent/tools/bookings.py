from typing import Dict, List, Any, Optional
from hospital_booking_agent.tools.api_tools import get_patient_profile, create_appointment
from hospital_booking_agent.sub_agents.booking_agent.token_test import *
from google.adk.tools import ToolContext

"""bookings is tool for booking_agent"""

#Hàm lấy Patient Profile
def fetch_patient_profile(
        # patient_id: str, 
        # patient_token: str,
        tool_context: Optional[ToolContext] = None):
    patient_token = login_test()
    patient_id = decode_jwt_token(patient_token)
    tool_context.state["patient_token"] = patient_token
    profile_response = get_patient_profile(patient_id, patient_token)

    if profile_response and profile_response.get("success"):
        result = profile_response.get("result", {})
        
        # Construct the full address
        address_parts = []
        if result.get("streetAddress"):
            address_parts.append(result["streetAddress"])
        if result.get("ward"):
            address_parts.append(result["ward"])
        if result.get("province"):
            address_parts.append(result["province"])
        full_address = ", ".join(address_parts)

        user_profile = {
            "patient_id": str(result.get("id", "")), # Convert ID to string as per your state structure
            "fullname": result.get("fullname", ""),
            "dob": result.get("dob", ""),
            "gender": "Nữ" if result.get("gender") == False else ("Nam" if result.get("gender") == True else ""), # Assuming False for Nữ, True for Nam, adjust as needed
            "cccd": result.get("cccd", ""),
            "phone": result.get("phoneNumber", ""),
            "email": result.get("email", ""),
            "address": full_address
        }

        if tool_context:
            tool_context.state["user_profile"] = user_profile
            print("Patient profile saved to tool_context.state:", tool_context.state["user_profile"])
        else:
            print("ToolContext not provided, profile not saved to state.")
            
        return profile_response
    else:
        print("Failed to fetch patient profile.")
        return None

def get_time_appoint(timeline_list: Dict[str, Any], selected_timeline: int, tool_context: Optional[ToolContext] = None):
    appointment_date = None
    slot_time_work = None
    display_slot_time = None
    slot_time = None
    if timeline_list and "schedules" in timeline_list and selected_timeline is not None:
        for schedule in timeline_list["schedules"]:
            if schedule.get("id") == selected_timeline:
                appointment_date = schedule.get("workDate")
                slot_time_work = schedule.get("startTime")
                tool_context.state["appointment_date"] = appointment_date
                break
    
    # Determine slot_time based on slot_time_work
    if slot_time_work == "07:30:00": # Use the exact string from your data
        slot_time = 1
        display_slot_time = "Ca sáng 7h30"
    elif slot_time_work == "12:30:00": # Use the exact string from your data
        slot_time = 2
        display_slot_time = "Ca chiều 12h30"
    else:
        slot_time = None
    
    tool_context.state["display_slot_time"] = display_slot_time
    tool_context.state["slot_time"] = slot_time

    return appointment_date, display_slot_time, slot_time
    

def book_appointment(
    hospital_id: int,
    service_id: int,
    specialization_id: Optional[int], 
    doctor_id: Optional[int],         
    appointment_date: str,
    slot_time: int,                     
    payment_method: int,
    note: str,
    token: str): 
    data = create_appointment(hospital_id,service_id,specialization_id,doctor_id,appointment_date,slot_time,payment_method,note,token)
    return data

