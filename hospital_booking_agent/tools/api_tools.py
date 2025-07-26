import requests
from typing import Dict, List, Any, Optional
import json
from hospital_booking_agent.shared_libraries.api_constants import *
"""API_Tools use for get data from API."""

#Hàm GET Hospitals Data 
def fetch_hospital_data(api_url: str) -> List[Dict[str, Any]]:
    """
    Hàm GET API.
    """
    print(f"DEBUG: Đang cố gắng lấy dữ liệu từ API")
    try:
        response = requests.get(api_url, timeout=10) 
        response.raise_for_status() 
        raw_hospital_data = response.json()

        # Kiểm tra xem có trường 'result' trong dữ liệu trả về không
        if isinstance(raw_hospital_data, dict) and "result" in raw_hospital_data:
            hospitals_data = raw_hospital_data["result"]
            print(f"DEBUG: Đã lấy thành công {len(hospitals_data)} bệnh viện từ trường 'result' của API.")
            return hospitals_data
        else:
            # Xử lý trường hợp cấu trúc JSON khác hoặc không có trường 'result'
            print(f"WARNING: API trả về dữ liệu không có trường 'result' hoặc không phải là dict: {raw_hospital_data}")
            # Thử trả về toàn bộ raw_api_data nếu nó đã là một list
            if isinstance(raw_hospital_data, list):
                print("DEBUG: API trả về trực tiếp một danh sách. Sử dụng toàn bộ dữ liệu.")
                return raw_hospital_data
            else:
                # Nếu không phải dict có 'result' và cũng không phải list, trả về rỗng hoặc mẫu
                print("ERROR: Cấu trúc dữ liệu API không mong muốn. Trả về dữ liệu mẫu.")
                return [
                    {"name": "BV Mẫu 1", "address": "123 Đường A", "latitude": 10.0, "longitude": 100.0},
                    {"name": "BV Mẫu 2", "address": "456 Đường B", "latitude": 11.0, "longitude": 101.0},
                ]

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Không thể kết nối hoặc lấy dữ liệu từ API: {e}")
        # Luôn trả về dữ liệu mẫu khi có lỗi kết nối
        return [
            {"name": "BV Mẫu 1", "address": "123 Đường A", "latitude": 10.0, "longitude": 100.0},
            {"name": "BV Mẫu 2", "address": "456 Đường B", "latitude": 11.0, "longitude": 101.0},
        ]
    except Exception as e: # Bắt các lỗi phân tích JSON hoặc lỗi khác
        print(f"ERROR: Xảy ra lỗi không mong muốn khi xử lý phản hồi API: {e}")
        return [
            {"name": "BV Mẫu 1", "address": "123 Đường A", "latitude": 10.0, "longitude": 100.0},
            {"name": "BV Mẫu 2", "address": "456 Đường B", "latitude": 11.0, "longitude": 101.0},
        ]

#Hàm POST Đặt Lịch Khám
def create_appointment(
    hospital_id: int,
    service_id: int,
    specialization_id: int,
    doctor_id: int,
    appointment_date: str,
    slot_time: int,
    payment_method: int,
    note: str,
    token: str # Thêm api_key làm đối số
) -> Dict[str, Any]:
    """
    Gọi API của bệnh viện để hoàn tất việc đặt lịch hẹn.
    Chỉ tập trung vào việc gửi yêu cầu POST và trả về kết quả thô từ API.
    """
    endpoint = BOOKING_API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}" # Sử dụng api_key được truyền vào
    }
    payload = {
        "hospitalId": hospital_id,
        "serviceId": service_id,
        "specializationId": specialization_id,
        "doctorId": doctor_id,
        "appointmentDate": appointment_date,
        "slotTime": slot_time,
        "paymentMethod": payment_method,
        "note": note
    }

    print(f"Đang gọi API POST tạo cuộc hẹn tại: {endpoint} với dữ liệu: {json.dumps(payload, indent=2)}")
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"status": "error", "message": f"Lỗi không xác định khi gọi API tạo cuộc hẹn: {e}"}

#Hàm GET Patient Data
def get_patient_profile(patient_id: str, token: str) -> Dict[str, Any]: #
    """
    Truy xuất hồ sơ đã lưu của bệnh nhân từ API.
    Chỉ tập trung vào việc gửi yêu cầu GET và trả về kết quả thô từ API.
    """
    endpoint = f"{PATIENT_API}/{patient_id}"
    headers = {
        "Authorization": f"Bearer {token}", 
        "Accept": "application/json"
    }

    print(f"Đang gọi API GET lấy hồ sơ bệnh nhân từ: {endpoint}")
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"status": "error", "message": f"Lỗi không xác định khi gọi API lấy hồ sơ bệnh nhân: {e}"}