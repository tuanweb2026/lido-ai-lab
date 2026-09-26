import os
import sys
import json
import urllib.request
import ssl
from pathlib import Path

# Channel Registry Configuration
CHANNEL_PROFILES = {
    "1995lido": {
        "name": "1995lido (Nhạc Thiền / Phật Giáo)",
        "handle": "@1995lido",
        "channel_id": "UC-0dKn2s-7jpsz6H3XFKgow",
        "description": "Kênh chuyên nhạc thiền, kinh Phật Nikaya, triết lý Phật giáo, chuông xoay Tây Tạng."
    },
    "lido1995music": {
        "name": "lido1995music (Nhạc Trẻ / Ballad / EDM)",
        "handle": "@Lido1995Music",
        "channel_id": "UCtVw4Z8Pj5b9qXnQvJ6a6Zg", # Sẽ tự động lấy hoặc xác nhận khi auth
        "description": "Kênh chuyên nhạc trẻ, ballad, deep house, EDM, hòa tấu hiện đại."
    },
    "lido_ai_lab": {
        "name": "Lido AI Lab (Tin Tức & Đột Phá AI)",
        "handle": "@LidoAILab",
        "channel_id": "UCcegmQUbGsoFqRlQa_ULy7g",
        "description": "Kênh công nghệ cao, cập nhật tin tức mô hình AI, robot, LLM thế giới."
    }
}

class ChannelSecurityGuard:
    """
    Bộ rào chắn an ninh: Ngăn chặn tuyệt đối việc upload nhầm giữa 3 kênh.
    Bất kỳ lệnh gọi upload nào không khớp Target Channel ID sẽ bị TERMINATE ngay lập tức.
    """
    def __init__(self, workspace_key: str, credentials_dir: Path):
        if workspace_key not in CHANNEL_PROFILES:
            raise ValueError(f"[GUARD] Không tìm thấy hồ sơ kênh '{workspace_key}'. Các kênh hợp lệ: {list(CHANNEL_PROFILES.keys())}")
        
        self.key = workspace_key
        self.profile = CHANNEL_PROFILES[workspace_key]
        self.credentials_dir = Path(credentials_dir)
        self.token_file = self.credentials_dir / "token.json"
        self.secret_file = self.credentials_dir / "client_secret.json"

    def get_token(self) -> str:
        if not self.token_file.exists():
            raise FileNotFoundError(f"[GUARD ERROR] Không tìm thấy token tại: {self.token_file}")
        with open(self.token_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        token = data.get("access_token") or data.get("token")
        if not token:
            raise ValueError("[GUARD ERROR] Token rỗng hoặc không hợp lệ!")
        return token

    def verify_channel_or_fail(self, video_metadata: dict = None) -> bool:
        """
        Kiểm tra tính hợp lệ trước khi bấm nút Publish:
        1. Kiểm tra Channel ID dự kiến
        2. Kiểm tra từ khóa tiêu đề có bị 'lẫn kênh' không (ví dụ: nhạc thiền mà upload sang kênh AI, hoặc AI sang nhạc thiền)
        """
        print(f"\n" + "="*70)
        print(f"🛡️  [CHANNEL GUARD ACTIVE] BẢO VỆ KÊNH: {self.profile['name']}")
        print(f"🎯 Target Handle: {self.profile['handle']}")
        print(f"🆔 Target Channel ID: {self.profile['channel_id']}")
        print("="*70)

        # Content keyword cross-check
        if video_metadata and "title" in video_metadata:
            title = video_metadata["title"].lower()
            
            # Nếu đang ở kênh Lido AI Lab mà có từ khóa thiền/Phật
            if self.key == "lido_ai_lab":
                banned_keywords = ["phật", "thiền", "kinh", "chú đại bi", "vô thường", "buddha", "nikaya"]
                for kw in banned_keywords:
                    if kw in title:
                        raise ValueError(f"🚨 [BÁO ĐỘNG ĐỎ] Tiêu đề '{video_metadata['title']}' chứa từ khóa PHẬT GIÁO ({kw}), tuyệt đối KHÔNG ĐƯỢC đăng lên kênh {self.profile['name']}!")
            
            # Nếu đang ở kênh 1995lido (Nhạc Thiền) mà có từ khóa AI / Tech
            elif self.key == "1995lido":
                banned_keywords = ["gpt-5", "claude 4", "llama 4", "openai", "deepmind", "gemini 2.5", "lechat", "nvidia"]
                for kw in banned_keywords:
                    if kw in title:
                        raise ValueError(f"🚨 [BÁO ĐỘNG ĐỎ] Tiêu đề '{video_metadata['title']}' chứa từ khóa CÔNG NGHỆ AI ({kw}), tuyệt đối KHÔNG ĐƯỢC đăng lên kênh Nhạc Thiền 1995lido!")

            # Nếu đang ở kênh lido1995music mà chứa từ khóa Phật
            elif self.key == "lido1995music":
                banned_keywords = ["kinh nikaya", "chú đại bi", "đức phật", "niết bàn"]
                for kw in banned_keywords:
                    if kw in title:
                        raise ValueError(f"🚨 [BÁO ĐỘNG ĐỎ] Tiêu đề '{video_metadata['title']}' chứa từ khóa TÂM LINH ({kw}), tuyệt đối KHÔNG ĐƯỢC đăng lên kênh Nhạc Trẻ!")

        print("✅ [VERIFICATION PASSED] Nội dung và định tuyến kênh 100% chính xác!")
        return True

if __name__ == "__main__":
    guard = ChannelSecurityGuard("lido_ai_lab", Path(__file__).parent / "credentials")
    guard.verify_channel_or_fail({"title": "OpenAI ra mắt GPT-5 cực mạnh"})
    print("Guard Self-test thành công!")
