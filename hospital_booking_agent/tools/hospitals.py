import math
from typing import Dict, List, Any, Optional
from google.adk.tools import ToolContext


# Dữ liệu bệnh viện mẫu (trong thực tế sẽ lấy từ DB hoặc API)
# Bao gồm tên, địa chỉ, tỉnh/thành phố, và tọa độ (latitude, longitude)
SAMPLE_HOSPITALS_DATA = [
    {
        "name": "Bệnh viện Bạch Mai",
        "address": "78 Giải Phóng, Phương Đình, Đống Đa",
        "city": "Hà Nội",
        "province": "Hà Nội",
        "lat": 20.9990,
        "lon": 105.8459,
        "specialties": ["Đa khoa", "Tim mạch", "Tiêu hóa", "Nội tiết", "Thận-Tiết niệu"]
    },
    {
        "name": "Bệnh viện Hữu nghị Việt Đức",
        "address": "40 Tràng Thi, Hàng Bông, Hoàn Kiếm",
        "city": "Hà Nội",
        "province": "Hà Nội",
        "lat": 21.0264,
        "lon": 105.8447,
        "specialties": ["Ngoại", "Chấn thương chỉnh hình", "Tiết niệu", "Phẫu thuật", "Gây mê hồi sức"]
    },
    {
        "name": "Bệnh viện Phụ sản Trung ương",
        "address": "43 Tràng Thi, Hàng Bông, Hoàn Kiếm",
        "city": "Hà Nội",
        "province": "Hà Nội",
        "lat": 21.0260,
        "lon": 105.8445,
        "specialties": ["Sản khoa", "Phụ khoa", "Kế hoạch hóa gia đình", "Sơ sinh"]
    },
    {
        "name": "Bệnh viện Nhi Trung ương",
        "address": "18/879 La Thành, Láng Thượng, Đống Đa",
        "city": "Hà Nội",
        "province": "Hà Nội",
        "lat": 21.0225,
        "lon": 105.8010,
        "specialties": ["Nhi khoa", "Tim mạch nhi", "Hô hấp nhi", "Tiêu hóa nhi"]
    },
    {
        "name": "Bệnh viện E",
        "address": "89 Trần Cung, Nghĩa Tân, Cầu Giấy",
        "city": "Hà Nội",
        "province": "Hà Nội",
        "lat": 21.0370,
        "lon": 105.7830,
        "specialties": ["Đa khoa", "Tim mạch", "Tiêu hóa", "Cơ xương khớp"]
    },
    {
        "name": "Bệnh viện Quân y 103",
        "address": "261 Phùng Hưng, Phúc La, Hà Đông",
        "city": "Hà Nội",
        "province": "Hà Nội",
        "lat": 20.9631,
        "lon": 105.7725,
        "specialties": ["Đa khoa", "Nội", "Ngoại", "Chấn thương", "Y học cổ truyền"]
    }
]

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
def location_tool(user_lat: Optional[float] = None, 
                  user_lon: Optional[float] = None, 
                  user_address: Optional[str] = None, 
                  radius_km: int = 10, tool_context: Optional[ToolContext] = None) -> list[Dict[str, Any]]:
    """
    Hàm chính để tìm kiếm bệnh viện dựa trên vị trí (lat, lon) hoặc địa chỉ cụ thể.
    Nó cũng có thể truy cập ToolContext nếu cần để ghi log hoặc lấy trạng thái.

    Args:
        user_lat (float, optional): Vĩ độ của người dùng. Mặc định là None.
        user_lon (float, optional): Kinh độ của người dùng. Mặc định là None.
        user_address (str, optional): Địa chỉ người dùng cung cấp (ví dụ: "Thành phố, quận/huyện, phường/xã,..."). Mặc định là None.
        radius_km (int): Bán kính tìm kiếm (chỉ áp dụng khi có lat/lon), đơn vị km. Mặc định là 10km.
        tool_context (ToolContext, optional): Đối tượng ToolContext từ Google ADK, cho phép truy cập trạng thái phiên.

    Returns:
        list[dict]: Danh sách các bệnh viện phù hợp, kèm theo khoảng cách nếu tìm theo tọa độ.
    """
    found_hospitals = []

    # Ví dụ về cách sử dụng tool_context (nếu cần)
    if tool_context:
        print(f"DEBUG: ToolContext state: {tool_context.state}")
        # Bạn có thể đọc/ghi vào tool_context.state ở đây nếu logic tìm kiếm cần
        # Ví dụ: user_id = tool_context.state.get("user_id")

    # TH2: Nếu người dùng CHO PHÉP truy cập vị trí (có lat, lon)
    if user_lat is not None and user_lon is not None:
        print(f"DEBUG: Tìm bệnh viện gần tọa độ: ({user_lat}, {user_lon}) trong bán kính {radius_km} km.")
        for hospital in SAMPLE_HOSPITALS_DATA:
            if hospital.get("lat") is not None and hospital.get("lon") is not None:
                distance = _calculate_distance(user_lat, user_lon, hospital["lat"], hospital["lon"])
                if distance <= radius_km:
                    hospital_info = hospital.copy()
                    hospital_info["distance_km"] = round(distance, 2)
                    found_hospitals.append(hospital_info)
        found_hospitals.sort(key=lambda x: x.get("distance_km", float('inf')))

    # TH1: Nếu người dùng KHÔNG CHO PHÉP truy cập vị trí (lat, lon là null)
    # hoặc không tìm thấy bệnh viện gần đó, và có địa chỉ người dùng
    elif user_address:
        print(f"DEBUG: Tìm bệnh viện theo địa chỉ: '{user_address}'")
        raw_search_terms = user_address.lower().replace(',', ' ').replace('/', ' ').split()
        search_terms = [term.strip() for term in raw_search_terms if term.strip()]
        
        required_terms = set(search_terms)

        for hospital in SAMPLE_HOSPITALS_DATA:
            hospital_full_info = (
                f"{hospital.get('name', '')} "
                f"{hospital.get('address', '')} "
                f"{hospital.get('city', '')} "
                f"{hospital.get('province', '')}"
            ).lower()

            if all(term in hospital_full_info for term in required_terms):
                found_hospitals.append(hospital)

    return found_hospitals

# --- Ví dụ cách sử dụng ---
if __name__ == "__main__":
    print("\n--- TEST CASE 1: Tìm bệnh viện gần vị trí (Hà Nội, gần BV Bạch Mai) ---")
    nearby_hospitals_hn_coord = location_tool(user_lat=20.9995, user_lon=105.8460, radius_km=2)
    if nearby_hospitals_hn_coord:
        print("Bệnh viện gần nhất ở Hà Nội:")
        for h in nearby_hospitals_hn_coord:
            print(f"- {h['name']} ({h.get('distance_km', 'N/A')} km) - {h['address']}")
    else:
        print("Không tìm thấy bệnh viện nào gần đó ở Hà Nội.")

    print("\n--- TEST CASE 2: Tìm bệnh viện theo địa chỉ (địa chỉ đầy đủ: '261 Phùng Hưng, Phúc La, Hà Đông') ---")
    # Địa chỉ này là của Bệnh viện Quân y 103
    hospitals_by_full_address = location_tool(user_address="261 Phùng Hưng, Phúc La, Hà Đông")
    if hospitals_by_full_address:
        print("Bệnh viện ở '261 Phùng Hưng, Phúc La, Hà Đông' theo địa chỉ:")
        for h in hospitals_by_full_address:
            print(f"- {h['name']} - {h['address']}")
    else:
        print("Không tìm thấy bệnh viện nào cho '261 Phùng Hưng, Phúc La, Hà Đông' theo địa chỉ.")

    print("\n--- TEST CASE 3: Tìm bệnh viện theo địa chỉ (thành phố và quận/huyện: 'Hà Nội, Đống Đa') ---")
    # Sẽ chỉ hiển thị bệnh viện ở Đống Đa
    hospitals_by_city_district_hn = location_tool(user_address="Hà Nội, Đống Đa")
    if hospitals_by_city_district_hn:
        print("Bệnh viện ở 'Hà Nội, Đống Đa' theo địa chỉ:")
        for h in hospitals_by_city_district_hn:
            print(f"- {h['name']} - {h['address']}")
    else:
        print("Không tìm thấy bệnh viện nào cho 'Hà Nội, Đống Đa' theo địa chỉ.")

    print("\n--- TEST CASE 5: Không có thông tin vị trí hay địa chỉ ---")
    no_info_hospitals = location_tool()
    if not no_info_hospitals:
        print("Vui lòng cung cấp vị trí hoặc địa chỉ để tìm bệnh viện.")

