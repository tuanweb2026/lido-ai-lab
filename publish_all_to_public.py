#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import ssl

ctx = ssl._create_unverified_context()
token_path = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/token.json"
with open(token_path) as f:
    token = json.load(f)["access_token"]

# Danh sách toàn bộ các video trên kênh cần chuyển ngay sang PUBLIC (Công khai)
# Đặc biệt ưu tiên 6 video tin nóng sốt dẻo nhất vừa sản xuất
video_ids_to_publish = [
    "UPT4x2_OEus", # XPENG Iron Robot (Ảnh mới phong phú độc quyền)
    "eVN21JiQMGE", # DeepSeek + OpenAI + Anthropic LHQ
    "obTbHv_BwR4", # Claude điều hành Lab sinh học & Robot chế thuốc
    "TPqQvMVIBLQ", # NVIDIA Isaac ROS 5.0
    "Oo1vCDlYHuQ", # Runway & Minimax Video AI
    "Yrc3I0i0YAs", # NVIDIA ra mắt HĐH Robot hình người
    "fvaF3sdhiUE", # Bóc mẽ kỹ thuật Gemini hack
    "vtk7Rw9vWuk", # Claude chiếm quyền tài khoản OpenAI
    "SvoEkF9YkYU", # Gemini hack 3 công ty (WSJ)
    "-eO6b_vNTTU"  # Mỹ lập quân chủng AI Force
]

print("==========================================================================")
print("⚡ BẮT ĐẦU CHUYỂN TOÀN BỘ VIDEO TIN NÓNG SANG CHẾ ĐỘ PUBLIC (CÔNG KHAI NGAY)")
print("==========================================================================")

success_count = 0
for vid in video_ids_to_publish:
    print(f"\n🚀 Đang kích hoạt Public ngay cho video ID: {vid}...")
    
    get_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={vid}"
    req = urllib.request.Request(get_url)
    req.add_header("Authorization", f"Bearer {token}")
    
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            v_data = json.loads(resp.read().decode("utf-8"))
            if not v_data.get("items"):
                print(f"   ❌ Không tìm thấy video {vid}")
                continue
            item = v_data["items"][0]
            snippet = item["snippet"]
            
        update_body = {
            "id": vid,
            "snippet": {
                "title": snippet["title"],
                "description": snippet["description"],
                "categoryId": snippet.get("categoryId", "28"),
                "tags": snippet.get("tags", [])
            },
            "status": {
                "privacyStatus": "public" # CÔNG KHAI NGAY LẬP TỨC
            }
        }
        
        put_url = "https://www.googleapis.com/youtube/v3/videos?part=snippet,status"
        put_req = urllib.request.Request(put_url, data=json.dumps(update_body).encode("utf-8"), method="PUT")
        put_req.add_header("Authorization", f"Bearer {token}")
        put_req.add_header("Content-Type", "application/json")
        
        with urllib.request.urlopen(put_req, context=ctx) as put_resp:
            res_data = json.loads(put_resp.read().decode("utf-8"))
            status = res_data.get("status", {}).get("privacyStatus", "")
            title = res_data.get("snippet", {}).get("title", "")
            print(f"   ✅ ĐÃ CÔNG KHAI THÀNH CÔNG: {title}")
            print(f"   👉 Trạng thái: {status.upper()} | Link: https://www.youtube.com/shorts/{vid}")
            success_count += 1
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")

print("\n" + "="*70)
print(f"🎉 ĐÃ CHUYỂN THÀNH CÔNG {success_count} VIDEO SANG CÔNG KHAI (PUBLIC) TRÊN KÊNH!")
print("======================================================================")
