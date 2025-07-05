import requests
from typing import Dict, List, Any, Optional

"""API_Tools use for get data from API."""


#Hàm GET Hospitals Data 
def fetch_hospital_from_api(api_url: str) -> List[Dict[str, Any]]:
    """
    Hàm GET API.
    """
    print(f"DEBUG: Đang cố gắng lấy dữ liệu từ API: {api_url}")
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
    