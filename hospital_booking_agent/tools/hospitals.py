import math
from typing import Dict, List, Any, Optional
from google.adk.tools import ToolContext


# Dữ liệu bệnh viện mẫu (trong thực tế sẽ lấy từ DB hoặc API)
# Bao gồm tên, địa chỉ, tỉnh/thành phố, và tọa độ (latitude, longitude)
SAMPLE_HOSPITALS_DATA = [
    {
      "id": 105,
      "code": "624bc08637a2390d84005424",
      "name": "Bệnh viện Đại học Y Dược TP.HCM",
      "address": "CS2: 201 Nguyễn Chí Thanh, Phường 12, Quận 5, TP. Hồ Chí Minh",
      "image": "https://bo-api.medpro.com.vn/static/images/umc2/web/logo.png",
      "googleMapUri": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6592.097836827651!2d106.65788221568286!3d10.758755674850875!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31752ef1d207e647%3A0x1bcd85bdaf5050f5!2zMjAxIE5ndXnhu4VuIENow60gVGhhbmgsIFBoxrDhu51uZyAxMiwgUXXhuq1uIDUsIEjhu5MgQ2jDrSBNaW5oLCBWaWV0bmFt!5e0!3m2!1sen!2s!4v1593595660777!5m2!1sen!2s",
      "banner": "",
      "type": 1,
      "phoneNumber": "",
      "email": "",
      "openTime": "2025-06-19T17:49:43.6658601",
      "closeTime": "2025-06-19T15:49:43.6658686",
      "longitude": 106.65788221568286,
      "latitude": 10.758755674850875
    },
    {
      "id": 106,
      "code": "67b6acf94bcad93a515bca05",
      "name": "Bệnh viện Bệnh Nhiệt đới",
      "address": "764 Võ Văn Kiệt, Phường 1, Quận 5, Tp.Hồ Chí Minh",
      "image": "https://cdn.medpro.vn/prod-partner/aa438828-15f9-4789-a461-d82b882b0f16-logo-benh-vien-nhiet-doi-1.png",
      "googleMapUri": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3434.8972978661886!2d106.678919!3d10.752668599999998!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31752f0186de2bb7%3A0x1392b898bea9c54!2zQuG7h25oIHZp4buHbiBC4buHbmggTmhp4buHdCDEkeG7m2k!5e1!3m2!1svi!2s!4v1740025294499!5m2!1svi!2s",
      "banner": "https://cdn.medpro.vn/prod-partner/c1354ce8-1d92-4281-8dda-268cee6b975c-thong-bao-benh-vien-benh-nhiet-doi.jpg",
      "type": 1,
      "phoneNumber": "",
      "email": "",
      "openTime": "2025-06-19T17:49:43.8252745",
      "closeTime": "2025-06-19T15:49:43.8252765",
      "longitude": 106.678919,
      "latitude": 10.752668599999998
    },
    {
      "id": 107,
      "code": "67ac3ff84bcad951de5bc33c",
      "name": "Bệnh viện Nhân Dân 115",
      "address": "527 Sư Vạn Hạnh, Phường 12, Quận 10, Thành phố Hồ Chí Minh",
      "image": "https://cdn.medpro.vn/prod-partner/0072b5f2-2f06-4bc1-910d-1d4da86aad4e-logo_icon.png",
      "googleMapUri": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3434.654420403097!2d106.66189412695307!3d10.773981200000005!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31752fa0cad4da25%3A0x6170fb9603ff966!2zQuG7h25oIHZp4buHbiBOaMOibiBEw6JuIDExNQ!5e1!3m2!1svi!2s!4v1739342472589!5m2!1svi!2s",
      "banner": "",
      "type": 1,
      "phoneNumber": "",
      "email": "",
      "openTime": "2025-06-19T17:49:43.8272524",
      "closeTime": "2025-06-19T15:49:43.8272532",
      "longitude": 106.66189412695307,
      "latitude": 10.773981200000005
    },
    {
      "id": 108,
      "code": "6732ff304bcad959975b8845",
      "name": "Bệnh viện Nhân Dân Gia Định",
      "address": "Số 1 Nơ Trang Long, Phường 7, Quận Bình Thạnh, TP.HCM",
      "image": "https://cdn.medpro.vn/prod-partner/721f45d6-348b-4ce2-bce0-260516ad21a0-logo_512x512px.png",
      "googleMapUri": "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d15676.395067245752!2d106.6941388!3d10.8037471!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x317528c663a9375f%3A0x342683919bcbff10!2sNhan%20dan%20Gia%20Dinh%20Hospital!5e0!3m2!1sen!2s!4v1731396910564!5m2!1sen!2s",
      "banner": "",
      "type": 1,
      "phoneNumber": "",
      "email": "",
      "openTime": "2025-06-19T17:49:43.8275105",
      "closeTime": "2025-06-19T15:49:43.8275109",
      "longitude": 106.6941388,
      "latitude": 10.8037471
    },
    {
      "id": 109,
      "code": "681d9e3b4bcad960655c0d68",
      "name": "Phòng Khám Chuyên Khoa Da Liễu Dr. Choice Clinic",
      "address": "92 Đường D5, Phường 25, Quận Bình Thạnh, TP. Hồ Chí Minh",
      "image": "https://cdn.medpro.vn/prod-partner/a033fe7f-01f6-4036-808b-2303a018e989-logo-drc-02.png",
      "googleMapUri": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3434.289366452085!2d106.71522739999999!3d10.8059367!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3175297a6c66b51b%3A0xcc1daba36e269229!2zVHLhu4sgU-G6uW8gUuG7lyAtIFPhurlvIEzhu5NpIC0gVHLhu4sgVGjDom0gLVRy4buLIE3hu6VuIC0gRHIuIENob2ljZSBjbGluaWM!5e1!3m2!1svi!2s!4v1746771645387!5m2!1svi!2s",
      "banner": "",
      "type": 1,
      "phoneNumber": "",
      "email": "",
      "openTime": "2025-06-19T17:49:43.8277171",
      "closeTime": "2025-06-19T15:49:43.8277176",
      "longitude": 106.71522739999999,
      "latitude": 10.8059367
    },
    {
      "id": 110,
      "code": "64d9f80d32cef9e1769228d6",
      "name": "Bệnh viện đa khoa Singapore (Singapore General Hospital)",
      "address": "Bukit Merah, Central Region, Singapore",
      "image": "https://cdn-pkh.longvan.net/prod-partner/6e45965e-09bd-4a35-b396-5df82f3e443e-logo_sgh_512x512_(2).png",
      "googleMapUri": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.8226312435063!2d103.83322440840124!3d1.2800648691130114!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31da196f954c6cd5%3A0x5c6009b161544a96!2sSingapore%20General%20Hospital!5e0!3m2!1sen!2s!4v1710232768924!5m2!1sen!2s\" width=\"600\" height=\"450\" style=\"border:0",
      "banner": "https://cdn-pkh.longvan.net/prod-partner/d078c83c-7445-4f4b-bb42-7cd5ffaeecb2-20231005-144832.jpeg",
      "type": 2,
      "phoneNumber": "",
      "email": "",
      "openTime": "2025-06-19T17:49:43.8279379",
      "closeTime": "2025-06-19T15:49:43.8279382",
      "longitude": 103.83322440840124,
      "latitude": 1.2800648691130114
    },
    {
      "id": 111,
      "code": "682ebfbd4bcad9a6685c1a80",
      "name": "Trung Tâm Mắt Kỹ Thuật Cao Nam Việt",
      "address": "18 - 20 Phước Hưng, Phường 8, Quận 5, TP.HCM",
      "image": "https://cdn.medpro.vn/prod-partner/ecda04b6-d646-4257-81be-4df38eafabd9-logo_nam_viet.png",
      "googleMapUri": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3434.8697857030525!2d106.66890079999999!3d10.7550849!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31752efb989904cf%3A0x3bf992b81d6fe4b!2zVHJ1bmcgVMOibSBN4bqvdCBL4bu5IFRodeG6rXQgQ2FvIE5hbSBWaeG7h3Q!5e1!3m2!1svi!2s!4v1747894312400!5m2!1svi!2s",
      "banner": "https://cdn.medpro.vn/prod-partner/6dc258d8-e536-4740-a8ef-0ca184e0ff49-banner.png",
      "type": 1,
      "phoneNumber": "",
      "email": "",
      "openTime": "2025-06-19T17:49:43.8281908",
      "closeTime": "2025-06-19T15:49:43.8281913",
      "longitude": 106.66890079999999,
      "latitude": 10.7550849
    },
    {
      "id": 112,
      "code": "64001a1854e6130024b5cee9",
      "name": "Trung Tâm Nội Soi Tiêu Hoá Doctor Check",
      "address": " 429 Tô Hiến Thành, Phường 14, Quận 10, Thành phố Hồ Chí Minh",
      "image": "https://cdn.medpro.vn/prod-partner/4db1fb51-2669-492f-b3d7-f08005451770-mark_dc-removebg-preview.png",
      "googleMapUri": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3919.4706612933487!2d106.6601678245749!3d10.775218459216921!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31752f3eacecd9a9%3A0x800b5bd5427447e7!2zRG9jdG9yIENoZWNrIC0gVOG6p20gU2_DoXQgQuG7h25oIMSQ4buDIFPhu5FuZyBUaOG7jSBIxqFu!5e0!3m2!1svi!2s!4v1731555829534!5m2!1svi!2s",
      "banner": "https://cdn.medpro.vn/prod-partner/97264996-2c7f-4bfd-b4ba-edc2db6e17ff-coaa_soaaaa_y_teaaaa1.png",
      "type": 3,
      "phoneNumber": "",
      "email": "",
      "openTime": "2025-06-19T17:49:43.828428",
      "closeTime": "2025-06-19T15:49:43.8284284",
      "longitude": 106.6601678245749,
      "latitude": 10.775218459216921
    },
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

    # TH1: Nếu người dùng KHÔNG CHO PHÉP truy cập vị trí (lat, lon là "")
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

