from hospital_booking_agent.shared_libraries.types import PatientProfile
from typing import Dict, List, Any, Optional

"""Bookings is tools for Booking_Agent"""

#Hàm Confirm Hồ sơ của bệnh nhân
def confirm_patient_info(patient_profile: PatientProfile) -> Dict[str, Any]:
    """
    Xác nhận hoặc chỉnh sửa hồ sơ bệnh nhân. Đây là hàm tương tác với người dùng,
    """
    print("\nVui lòng xác nhận thông tin hồ sơ của bạn:")
    for key, value in patient_profile.items():
        print(f"- {key.replace('_', ' ').title()}: {value}")

    #Giả định người dùng luôn xác nhận.
    user_confirmed = True

    if not user_confirmed:
        print("Người dùng đã không xác nhận thông tin.")
        return {"confirmed": False, "profile": patient_profile, "message": "Người dùng không xác nhận."}

    print("Thông tin bệnh nhân đã được xác nhận.")
    return {
        "confirmed": True,
        "profile": patient_profile,
        "message": "Thông tin bệnh nhân đã được xác nhận."
    }