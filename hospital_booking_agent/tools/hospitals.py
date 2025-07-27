import math
from typing import Dict, Any, Optional
from google.adk.tools import ToolContext
from hospital_booking_agent.shared_libraries.api_constants import *
from hospital_booking_agent.tools.api_tools import fetch_hospital_data
from difflib import get_close_matches


"""hospitals use for location tool to get position of hospitals"""

#Dữ liệu Hospital
_list_hospitals = None 

def _get_hospitals_data():
    global _list_hospitals 
    if _list_hospitals is None: 
        print("DEBUG: Lần đầu tiên tải dữ liệu bệnh viện từ API...")
        _list_hospitals = fetch_hospital_data(HOSPITALS_API) 
    return _list_hospitals

# Hàm tính khoảng cách giữa hai điểm dựa trên vĩ độ và kinh độ (Haversine formula)
def _calculate_distance(lat1, lon1, lat2, lon2):
    """
    Tính khoảng cách giữa hai điểm trên Trái Đất (đơn vị km).
    Sử dụng công thức Haversine.
    """
    R = 6371  # Bán kính Trái Đất ở đơn vị km

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Hàm chính: Tìm bệnh viện theo vị trí hoặc địa chỉ
def hos_location_tool(
                  user_lat: Optional[float] = None, 
                  user_lon: Optional[float] = None, 
                  user_address: Optional[str] = None, 
                  radius_km: int = 10, 
                  tool_context: Optional[ToolContext] = None) -> list[Dict[str, Any]]:

    found_hospitals = []
    list_hospitals_data = _get_hospitals_data()

    if tool_context:
        print(f"DEBUG: ToolContext state: {tool_context.state}")
        # Bạn có thể đọc/ghi vào tool_context.state ở đây nếu logic tìm kiếm cần
        # Ví dụ: user_id = tool_context.state.get("user_id")

    # TH2: Nếu người dùng CHO PHÉP truy cập vị trí (có lat, lon)
    if user_lat is not None and user_lon is not None:
        print(f"DEBUG: Tìm bệnh viện gần tọa độ: ({user_lat}, {user_lon}) trong bán kính {radius_km} km.")
        for hospital in list_hospitals_data:
            if hospital.get("latitude") is not None and hospital.get("longitude") is not None:
                distance = _calculate_distance(user_lat, user_lon, hospital["latitude"], hospital["longitude"])
                if distance <= radius_km:
                    hospital_info = hospital.copy()
                    hospital_info["distance_km"] = round(distance, 2)
                    found_hospitals.append(hospital_info)
        found_hospitals.sort(key=lambda x: x.get("distance_km", float('inf')))

    # TH1: Nếu người dùng KHÔNG CHO PHÉP truy cập vị trí (lat, lon là "")
    # hoặc không tìm thấy bệnh viện gần đó, và có địa chỉ người dùng
    elif user_address:
        print(f"DEBUG: Tìm bệnh viện theo địa chỉ: '{user_address}'")
        raw_search_terms = user_address.lower().replace(',', ' ').replace('/', ' ').split()
        search_terms = [term.strip() for term in raw_search_terms if term.strip()]
        
        required_terms = set(search_terms)

        for hospital in list_hospitals_data:
            hospital_full_info = (
                f"{hospital.get('name', '')} "
                f"{hospital.get('address', '')} "
            ).lower()

            if all(term in hospital_full_info for term in required_terms):
                found_hospitals.append(hospital)

    return found_hospitals

def hos_select_tool(
    user_input: str,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Tool để user chọn bệnh viện bằng tên. 
    """
    key = user_input.strip().lower()
    list_hospitals_data = _get_hospitals_data()

    name_to_hospital = {h["name"].lower(): h for h in list_hospitals_data}

    print(f"DEBUG: list_hospitals: {name_to_hospital}")
    print(f"DEBUG: key: {key}")

    if key in name_to_hospital:
        selected = name_to_hospital[key]
        if tool_context:
            tool_context.state["selected_hospital"] = str(selected["id"])
        return {
            "message": f"Bạn đã chọn: {selected['name']} (ID={selected['id']})",
            "hospital": selected
        }

    names = list(name_to_hospital.keys())
    matches = get_close_matches(key, names, n=3, cutoff=0.6)

    if not matches:
        return {
            "error": "Không tìm thấy bệnh viện nào trùng hoặc gần giống tên bạn nhập."
        }

    if len(matches) > 1:
        return {
            "ambiguous": True,
            "candidates": matches
        }
    
    matched = matches[0]
    selected = name_to_hospital[matched]

    if tool_context:
        tool_context.state["selected_hospital"] = str(selected["id"])

    return {
        "message": f"Bạn đã chọn: {selected['name']} (ID={selected['id']})",
        "hospital": selected
    }
