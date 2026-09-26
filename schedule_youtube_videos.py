#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import ssl
from datetime import datetime, timedelta

# YouTube API Update Video Schedule
# YouTube Data API v3 cho phép set status.publishAt khi status.privacyStatus = "private"
# Format publishAt: ISO 8601 (RFC 3339) e.g. "2026-09-23T04:30:00.000Z"

ctx = ssl._create_unverified_context()
token_path = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/token.json"
with open(token_path) as f:
    token = json.load(f)["access_token"]

# Danh sách 5 video hiện có trên kênh Lido AI Lab
# Khung giờ vàng Việt Nam (UTC+7):
# 1. Trưa: 11:30 - 12:30 (UTC: 04:30 - 05:30)
# 2. Chiều tối: 18:30 - 19:30 (UTC: 11:30 - 12:30)
# 3. Tối cao điểm: 20:00 - 21:00 (UTC: 13:00 - 14:00)

schedules = [
    {
        "id": "Yrc3I0i0YAs",
        "title": "CHẤN ĐỘNG: NVIDIA RA MẮT HỆ ĐIỀU HÀNH AI CHO ROBOT HÌNH NGƯỜI! 🤖⚡ #Shorts #NVIDIA #Robotics",
        "slot_desc": "Khung giờ vàng Sáng mai (07:30 VN ngày 23/09/2026)",
        "publish_at_iso": "2026-09-23T00:30:00.000Z"
    },
    {
        "id": "fvaF3sdhiUE",
        "title": "BÓC MẼ KỸ THUẬT: AI GEMINI TỰ ĐỘNG HACK HỆ THỐNG NHƯ THẾ NÀO? 🧠💻 #Shorts #CyberSecurity #AI",
        "slot_desc": "Khung giờ vàng Trưa mai (11:45 VN ngày 23/09/2026)",
        "publish_at_iso": "2026-09-23T04:45:00.000Z"
    },
    {
        "id": "vtk7Rw9vWuk",
        "title": "CHẤN ĐỘNG: CLAUDE GIÚP CHIẾM QUYỀN TÀI KHOẢN NHÂN VIÊN OPENAI! 🚨⚡ #Shorts #Claude #OpenAI",
        "slot_desc": "Khung giờ vàng Chiều tối mai (18:15 VN ngày 23/09/2026)",
        "publish_at_iso": "2026-09-23T11:15:00.000Z"
    },
    {
        "id": "SvoEkF9YkYU",
        "title": "BÁO ĐỘNG ĐỎ: AI GEMINI TỰ ĐỘNG HACK 3 CÔNG TY TRONG THỬ NGHIỆM! 🚨💻 #Shorts #Gemini #WSJ",
        "slot_desc": "Khung giờ vàng Tối mai (20:00 VN ngày 23/09/2026)",
        "publish_at_iso": "2026-09-23T13:00:00.000Z"
    },
    {
        "id": "-eO6b_vNTTU",
        "title": "MỸ SẮP THÀNH LẬP 'QUÂN CHỦNG AI' VÀ BỔ NHIỆM TỔNG TƯ LỆNH AI? 🇺🇸🚨 #Shorts #AIForce #LidoAILab",
        "slot_desc": "Khung giờ vàng Trưa ngày kia (11:45 VN ngày 24/09/2026)",
        "publish_at_iso": "2026-09-24T04:45:00.000Z"
    }
]

print("==========================================================================")
print("🕒 BẮT ĐẦU THIẾT LẬP LỊCH CÔNG KHAI TỰ ĐỘNG THEO KHUNG GIỜ VÀNG (YOUTUBE)")
print("==========================================================================")

for item in schedules:
    vid = item["id"]
    print(f"\n⚙️ Đang lên lịch cho video: {item['title'][:50]}...")
    print(f"   📅 Thời gian lên sóng: {item['slot_desc']} ({item['publish_at_iso']})")
    
    # Lấy snippet hiện tại của video để giữ nguyên
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
            
        # Chuẩn bị body cập nhật status.publishAt
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
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"   ❌ Lỗi HTTP: {err_msg}")
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")

print("\n" + "="*70)
print("🎉 ĐÃ HOÀN TẤT LÊN LỊCH CÔNG KHAI TOÀN BỘ VIDEO THEO KHUNG GIỜ VÀNG!")
print("======================================================================")
