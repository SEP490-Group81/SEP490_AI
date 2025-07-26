import requests
import json
import jwt 
from jwt.exceptions import DecodeError
from typing import Dict, List, Any, Optional

LOGIN_API = "https://sep490-dabs-gsdjgbfbdgd8gkbb.eastasia-01.azurewebsites.net/api/v1/tokens" 

def login_test():
    if not LOGIN_API:
        print("Lỗi: LOGIN_API chưa được cấu hình. Vui lòng đặt URL API đăng nhập.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "email": "lapthd2k3@gmail.com",
        "password": "30012003"
    }

    try:
        # Gửi yêu cầu POST tới API
        response = requests.post(LOGIN_API, headers=headers, data=json.dumps(payload))

        # Kiểm tra mã trạng thái HTTP
        if response.status_code == 200:
            print("Đăng nhập thành công!")
            try:
                response_data = response.json()
                if "token" in response_data:
                    token = response_data["token"]
                    return token
                else:
                    print("Lỗi: Phản hồi JSON không chứa khóa 'token'.")
                    print(f"Phản hồi đầy đủ: {json.dumps(response_data, indent=2)}")
                    return response_data # Vẫn trả về dữ liệu nếu muốn xử lý thêm
            except json.JSONDecodeError:
                print("Lỗi: Phản hồi không phải là JSON hợp lệ.")
                print(f"Phản hồi thô: {response.text}")
                return None
        elif response.status_code == 401:
            print("Đăng nhập thất bại: Thông tin đăng nhập không hợp lệ.")
            try:
                return response.json() # API có thể trả về lỗi chi tiết hơn
            except json.JSONDecodeError:
                return {"error": "Unauthorized"}
        elif response.status_code == 400:
            print("Đăng nhập thất bại: Yêu cầu không hợp lệ (ví dụ: thiếu trường).")
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"error": "Bad Request"}
        else:
            print(f"Đăng nhập thất bại với mã trạng thái: {response.status_code}")
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"error": f"HTTP Error {response.status_code}", "raw_response": response.text}

    except requests.exceptions.ConnectionError:
        print("Lỗi kết nối: Không thể kết nối tới server API. Vui lòng kiểm tra URL hoặc kết nối mạng.")
        return None
    except requests.exceptions.Timeout:
        print("Lỗi thời gian chờ: Yêu cầu API đã hết thời gian.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Đã xảy ra lỗi không xác định khi gọi API: {e}")
        return None

def decode_jwt_token(token: str) -> Dict[str, Any]:
    try:
        # Giải mã token mà không xác minh chữ ký
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload['nameidentifier']
    except DecodeError as e:
        print(f"Lỗi giải mã token: {e}")
        return None
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn: {e}")
        return None
