import json
import os
import re
from datetime import datetime

class YouTubeUploaderAgent:
    def __init__(self, output_dir="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/output"):
        self.output_dir = output_dir

    @staticmethod
    def generate_memorable_filename(topic_title, source="news", ext="mp4"):
        """
        Tạo tên file gợi nhớ chuẩn: YYYY-MM-DD_noi-dung-chinh_nguon.mp4
        Ví dụ: 2026-09-20_my-lap-quan-chung-ai-force_nbc.mp4
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Bỏ dấu tiếng Việt và ký tự đặc biệt
        import unicodedata
        nfkd = unicodedata.normalize('NFKD', topic_title)
        ascii_text = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        ascii_text = ascii_text.replace('đ', 'd').replace('Đ', 'D')
        
        # Làm sạch chuỗi
        clean_slug = re.sub(r'[^a-zA-Z0-9\s-]', '', ascii_text).strip().lower()
        clean_slug = re.sub(r'[\s-]+', '-', clean_slug)[:45].strip('-')
        clean_source = re.sub(r'[^a-zA-Z0-9]', '', source).lower()[:15]
        
        filename = f"{date_str}_{clean_slug}_{clean_source}.{ext}"
        return filename

    def prepare_release(self, video_path, metadata):
        manifest_path = os.path.join(self.output_dir, "release_manifest.json")
        release_info = {
            "status": "READY_FOR_PUBLISH",
            "video_file": video_path,
            "target_channel": "https://www.youtube.com/@LidoAILab",
            "upload_metadata": metadata,
            "instructions": [
                "1. Vào YouTube Studio của kênh https://www.youtube.com/@LidoAILab",
                "2. Bấm 'Tạo' -> 'Tải video lên'",
                "3. Chọn file video trong thư mục output",
                "4. Sao chép Tiêu đề, Mô tả và Thẻ Tags từ file này vào",
                "5. Ghim (Pin) bình luận tương tác có sẵn trong mục pinned_comment"
            ]
        }

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(release_info, f, indent=2, ensure_ascii=False)

        print(f"[YouTubeUploader] Đã tạo gói phát hành sẵn sàng tại: {manifest_path}")
        return manifest_path

if __name__ == "__main__":
    uploader = YouTubeUploaderAgent()
    uploader.prepare_release("sample.mp4", {"title": "Test Title"})
