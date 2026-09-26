#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import ssl

ctx = ssl._create_unverified_context()
token_path = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/token.json"
with open(token_path) as f:
    token = json.load(f)["access_token"]

# Danh sách 6 video mới sản xuất gần đây nhất cần xếp lịch phát sóng tiếp nối
# Lịch phát sóng nối tiếp bắt đầu từ chiều tối ngày 24/09 sang ngày 25/09 và 26/09:
# Khung giờ vàng VN (UTC+7):
# - 07:30 Sáng (00:30 UTC)
# - 11:45 Trưa (04:45 UTC)
# - 18:15 Chiều (11:15 UTC)
# - 20:00 Tối (13:00 UTC)

new_schedules = [
    {
        "id": "UPT4x2_OEus",
        "title": "BÁO ĐỘNG: ROBOT XPENG VỪA LẮP RÁP XONG ĐÃ TỰ BƯỚC RA KHỎI XƯỞNG! (ẢNH ĐỘC QUYỀN MỚI)",
        "slot_desc": "Khung giờ vàng Chiều tối ngày kia (18:15 VN ngày 24/09/2026)",
        "publish_at_iso": "2026-09-24T11:15:00.000Z"
    },
    {
        "id": "eVN21JiQMGE",
        "title": "CHẤN ĐỘNG: DEEPSEEK BẮT TAY OPENAI VÀ ANTHROPIC TẠI LIÊN HỢP QUỐC!",
        "slot_desc": "Khung giờ vàng Tối ngày kia (20:00 VN ngày 24/09/2026)",
        "publish_at_iso": "2026-09-24T13:00:00.000Z"
    },
    {
        "id": "obTbHv_BwR4",
        "title": "CHẤN ĐỘNG Y HỌC: CLAUDE ĐIỀU HÀNH DÀN ROBOT TỰ CHẾ THUỐC TRỊ BỆNH!",
        "slot_desc": "Khung giờ vàng Sáng (07:30 VN ngày 25/09/2026)",
        "publish_at_iso": "2026-09-25T00:30:00.000Z"
    },
    {
        "id": "TPqQvMVIBLQ",
        "title": "NVIDIA RA MẮT ISAAC ROS 5.0: ĐỘT PHÁ TỐC ĐỘ CHO ROBOT THÔNG MINH!",
        "slot_desc": "Khung giờ vàng Trưa (11:45 VN ngày 25/09/2026)",
        "publish_at_iso": "2026-09-25T04:45:00.000Z"
    },
    {
        "id": "Oo1vCDlYHuQ",
        "title": "RUNWAY VÀ MINIMAX TUNG CHIÊU: CHUẨN VẬT LÝ VIDEO AI ĐỈNH CAO!",
        "slot_desc": "Khung giờ vàng Chiều tối (18:15 VN ngày 25/09/2026)",
        "publish_at_iso": "2026-09-25T11:15:00.000Z"
    },
    {
        "id": "6U4WmPM5AUw",
        "title": "BẢN TIN ĐỘC QUYỀN: DeepSeek, Moonshot Face Scrutiny Over Anthropic!",
        "slot_desc": "Khung giờ vàng Tối (20:00 VN ngày 25/09/2026)",
        "publish_at_iso": "2026-09-25T13:00:00.000Z"
    }
]

print("==========================================================================")
print("🕒 BẮT ĐẦU THIẾT LẬP LỊCH CÔNG KHAI TIẾP NỐI CHO 6 VIDEO MỚI (YOUTUBE)")
print("==========================================================================")

for item in new_schedules:
    vid = item["id"]
    print(f"\n⚙️ Đang lên lịch cho video: {item['title'][:55]}...")
    print(f"   📅 Thời gian lên sóng: {item['slot_desc']} ({item['publish_at_iso']})")
    
    get_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={vid}"
    req = urllib.request.Request(get_url)
    req.add_header("Authorization", f"Bearer {token}")
    
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            v_data = json.loads(resp.read().decode("utf-8"))
            if not v_data.get("items"):
                print(f"   ❌ Không tìm thấy video {vid}")
                continue
            item_data = v_data["items"][0]
            snippet = item_data["snippet"]
            
        update_body = {
            "id": vid,
            "snippet": {
                "title": snippet["title"],
                "description": snippet["description"],
                "categoryId": snippet.get("categoryId", "28"),
                "tags": snippet.get("tags", [])
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": item["publish_at_iso"]
            }
        }
        
        put_url = "https://www.googleapis.com/youtube/v3/videos?part=snippet,status"
        put_req = urllib.request.Request(put_url, data=json.dumps(update_body).encode("utf-8"), method="PUT")
        put_req.add_header("Authorization", f"Bearer {token}")
        put_req.add_header("Content-Type", "application/json")
        
        with urllib.request.urlopen(put_req, context=ctx) as put_resp:
            res_data = json.loads(put_resp.read().decode("utf-8"))
            pub_at = res_data.get("status", {}).get("publishAt", "")
            print(f"   ✅ ĐÃ LÊN LỊCH THÀNH CÔNG! YouTube xác nhận phát hành lúc: {pub_at}")
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")

print("\n" + "="*70)
print("🎉 ĐÃ HOÀN TẤT LÊN LỊCH CÔNG KHAI TẤT CẢ VIDEO THEO KHUNG GIỜ VÀNG NỐI TIẾP!")
print("======================================================================")
