import os
import sys
import json
import ssl
import time
import urllib.request
import urllib.parse
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context

TOKEN_FILE = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/token.json"

class YouTubeDirectPublisher:
    """
    Module Đăng Video YouTube Trực Tiếp Cho Kênh @LidoAILab:
    - Sử dụng Pure Python + OAuth2 tự động refresh token
    - Đăng ở chế độ 'private' để người dùng tự click vào link review
    - Chuẩn SEO: Title, Description, Tags, Call To Action
    """
    def __init__(self, token_path=TOKEN_FILE):
        self.token_path = token_path

    def refresh_access_token(self, tokens):
        url = tokens.get("token_uri", "https://oauth2.googleapis.com/token")
        post_data = urllib.parse.urlencode({
            "client_id": tokens["client_id"],
            "client_secret": tokens["client_secret"],
            "refresh_token": tokens["refresh_token"],
            "grant_type": "refresh_token"
        }).encode("utf-8")

        req = urllib.request.Request(url, data=post_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                new_data = json.loads(resp.read().decode("utf-8"))
                tokens["access_token"] = new_data["access_token"]
                tokens["expires_in"] = new_data.get("expires_in", 3600)
                
            with open(self.token_path, "w", encoding="utf-8") as f:
                json.dump(tokens, f, indent=2)
        except Exception as e:
            print(f"⚠️ [YouTubePublisher] Cảnh báo refresh token: {e}")
            
        return tokens

    def get_valid_token(self):
        if not os.path.exists(self.token_path):
            print(f"❌ Không tìm thấy token tại {self.token_path}")
            return None
        with open(self.token_path, "r", encoding="utf-8") as f:
            tokens = json.load(f)
            if "refresh_token" in tokens:
                return self.refresh_access_token(tokens)
        return None

    def upload_short(self, video_path, title, description=None, tags=None, privacy_status="public"):
        tokens = self.get_valid_token()
        if not tokens or "access_token" not in tokens:
            print("❌ Không thể xác thực YouTube API!")
            return None

        access_token = tokens["access_token"]
        file_size = os.path.getsize(video_path)
        clean_title = title[:95]

        if tags is None:
            tags = ["Shorts", "AI", "Technology", "LidoAILab", "TechNews", "Trending"]

        if description is None:
            description = (
                f"{clean_title}\n\n"
                f"Bản tin công nghệ AI độc quyền từ Lido AI Lab.\n\n"
                f"🔔 ĐỪNG QUÊN BẤM LIKE, SHARE VÀ ĐĂNG KÝ KÊNH ĐỂ CẬP NHẬT XU HƯỚNG AI MỖI NGÀY!\n"
                f"👉 Kênh chính thức: https://www.youtube.com/@LidoAILab\n\n"
                f"#LidoAILab #AI #Shorts #TechNews #ArtificialIntelligence"
            )

        metadata = {
            "snippet": {
                "title": clean_title,
                "description": description,
                "tags": tags,
                "categoryId": "28" # Science & Technology
            },
            "status": {
                "privacyStatus": privacy_status, # CÔNG KHAI (public) HOẶC RIÊNG TƯ (private)
                "selfDeclaredMadeForKids": False
            }
        }

        upload_init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
        meta_bytes = json.dumps(metadata).encode("utf-8")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Length": str(file_size),
            "X-Upload-Content-Type": "video/mp4"
        }

        location = None
        for init_attempt in range(5):
            try:
                print(f"📡 Đang kết nối tới máy chủ YouTube (Lần thử {init_attempt + 1}/5)...")
                req = urllib.request.Request(upload_init_url, data=meta_bytes, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=45) as resp:
                    location = resp.headers.get("Location")
                    if location:
                        break
            except Exception as e:
                print(f"⚠️ Lỗi kết nối khởi tạo (Lần {init_attempt + 1}): {e}")
                time.sleep(3)

        if not location:
            print("❌ Không thể thiết lập phiên upload sau 5 lần thử.")
            return None

        print(f"🚀 [YouTubePublisher] Bắt đầu truyền tải dữ liệu video ({file_size / (1024*1024):.2f} MB)...")
        with open(video_path, "rb") as f:
            video_bytes = f.read()

        for upload_attempt in range(5):
            try:
                upload_req = urllib.request.Request(location, data=video_bytes, headers={
                    "Content-Length": str(file_size),
                    "Content-Type": "video/mp4"
                }, method="PUT")

                with urllib.request.urlopen(upload_req, timeout=180) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                    video_id = result.get("id")

                watch_url = f"https://youtu.be/{video_id}"
                shorts_url = f"https://www.youtube.com/shorts/{video_id}"

                print("=" * 65)
                print("🎉 UPLOAD THÀNH CÔNG LÊN KÊNH @LidoAILab (CHẾ ĐỘ PRIVATE)!")
                print(f"🔗 Link Shorts: {shorts_url}")
                print(f"🔗 Link Video: {watch_url}")
                print("=" * 65)

                return {
                    "video_id": video_id,
                    "watch_url": watch_url,
                    "shorts_url": shorts_url,
                    "title": clean_title,
                    "status": privacy_status
                }
            except Exception as e:
                print(f"⚠️ Đứt kết nối khi truyền tải (Lần {upload_attempt + 1}/5): {e}. Đang thử lại...")
                time.sleep(5)

        return None

    def upload_public_short(self, video_path, title, description=None, tags=None):
        return self.upload_short(video_path, title, description=description, tags=tags, privacy_status="public")

    def upload_private_short(self, video_path, title, description=None, tags=None):
        return self.upload_short(video_path, title, description=description, tags=tags, privacy_status="private")

if __name__ == "__main__":
    pub = YouTubeDirectPublisher()
    token = pub.get_valid_token()
    if token:
        print("✅ Xác thực token thành công! Sẵn sàng upload lên YouTube @LidoAILab.")
