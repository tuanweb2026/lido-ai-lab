#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
CREDENTIALS_DIR = BASE_DIR / "credentials"
TOKEN_FILE = CREDENTIALS_DIR / "token.json"
SEEN_VN = BASE_DIR / "seen_news_vn.json"
SEEN_GLOBAL = BASE_DIR / "seen_news.json"
OUTPUT_DIR = BASE_DIR / "output"

def get_valid_token():
    if not TOKEN_FILE.exists():
        return None
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    token = data.get("access_token")
    # Tự động refresh nếu cần
    refresh_token = data.get("refresh_token")
    if refresh_token:
        import urllib.parse
        try:
            url = data.get("token_uri", "https://oauth2.googleapis.com/token")
            post_data = urllib.parse.urlencode({
                "client_id": data["client_id"],
                "client_secret": data["client_secret"],
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            }).encode("utf-8")
            req = urllib.request.Request(url, data=post_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                new_data = json.loads(resp.read().decode("utf-8"))
                token = new_data["access_token"]
                data["access_token"] = token
                with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
        except Exception:
            pass
    return token

def fetch_youtube_recent_videos(token, limit=12):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCcegmQUbGsoFqRlQa_ULy7g&maxResults={limit}&order=date&type=video"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("items", [])
    except Exception as e:
        return []

def main():
    print("\n" + "="*80)
    print("📊 BÁO CÁO TIẾN TRÌNH XUẤT BẢN TIN TỨC - KÊNH @LidoAILab")
    print(f"⏰ Thời gian kết xuất: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80)

    # 1. Thống kê Database
    total_vn = 0
    total_gb = 0
    if SEEN_VN.exists():
        with open(SEEN_VN, "r", encoding="utf-8") as f:
            total_vn = len(json.load(f))
    if SEEN_GLOBAL.exists():
        with open(SEEN_GLOBAL, "r", encoding="utf-8") as f:
            total_gb = len(json.load(f))

    print(f"📁 Tổng số đề tài đã xử lý: {total_vn + total_gb} đề tài")
    print(f"   ├─ 🇻🇳 Biệt đội Tiếng Việt (8 nguồn RSS VN): {total_vn} đề tài")
    print(f"   └─ 🌍 Biệt đội Toàn Cầu (9 nguồn Tech quốc tế): {total_gb} đề tài")
    print("-" * 80)

    # 2. Lấy danh sách video thực tế trên kênh YouTube
    token = get_valid_token()
    if token:
        items = fetch_youtube_recent_videos(token, limit=10)
        if items:
            print(f"🎬 DANH SÁCH 10 SHORTS MỚI NHẤT TRÊN YOUTUBE (@LidoAILab):")
            print(f"{'STT':<4} | {'NGÀY ĐĂNG':<10} | {'LINK YOUTUBE SHORTS':<40} | {'TIÊU ĐỀ'}")
            print("-" * 80)
            for idx, item in enumerate(items, 1):
                vid = item["id"]["videoId"]
                title = item["snippet"]["title"].replace("&amp;", "&")
                pub_date = item["snippet"]["publishedAt"][:10]
                link = f"https://www.youtube.com/shorts/{vid}"
                print(f"{idx:<4} | {pub_date:<10} | {link:<40} | {title[:45]}")
        else:
            print("⚠️ Không thể lấy danh sách từ YouTube API (quota hoặc kết nối).")
    else:
        print("⚠️ Không tìm thấy token xác thực.")

    # 3. File video đã render tại máy local
    if OUTPUT_DIR.exists():
        mp4_files = sorted(OUTPUT_DIR.glob("*.mp4"), key=lambda f: f.stat().st_mtime, reverse=True)
        print("-" * 80)
        print(f"💾 CÁC FILE VIDEO GẦN NHẤT ĐÃ RENDER TRONG THƯ MỤC LOCAL ({len(mp4_files)} files):")
        for f in mp4_files[:5]:
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%d/%m %H:%M')
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"   • [{mtime}] ({size_mb:.2f} MB) {f.name}")

    print("="*80 + "\n")

if __name__ == "__main__":
    main()
