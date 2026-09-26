import os
import json
import time
from agents.youtube_api_publisher import YouTubeDirectPublisher
from agents.notifier import NotificationAgent

def upload_vault_to_youtube():
    print("==========================================================================")
    print("🚀 BẮT ĐẦU UPLOAD CÁC VIDEO LÊN KÊNH YOUTUBE @LidoAILab (CHẾ ĐỘ PRIVATE)")
    print("==========================================================================")

    publisher = YouTubeDirectPublisher()
    notifier = NotificationAgent()
    output_dir = "/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/output"

    # Danh sách các video chất lượng cao đã sẵn sàng
    videos_to_upload = [
        {
            "file": "2026-09-20_my-lap-quan-chung-ai-force_nbc-news.mp4",
            "title": "MỸ SẮP THÀNH LẬP 'QUÂN CHỦNG AI' VÀ BỔ NHIỆM TỔNG TƯ LỆNH AI? 🇺🇸🚨 #Shorts #AIForce #LidoAILab",
            "description": (
                "KỶ NGUYÊN QUÂN CHỦNG AI (AI FORCE) ĐÃ BẮT ĐẦU?\n\n"
                "Tin tức độc quyền từ NBC News: Chính phủ Mỹ đề xuất thành lập một quân chủng AI độc lập ('AI Force') và bổ nhiệm Tổng chỉ huy AI (AI Czar) để giám sát và dẫn dắt cuộc chạy đua an ninh công nghệ toàn cầu.\n\n"
                "Liệu trí tuệ nhân tạo tự hành có nên được trao quyền điều phối hệ thống phòng thủ chiến lược?\n\n"
                "👉 HÃY BẤM LIKE, CHIA SẺ VÀ ĐĂNG KÝ KÊNH LIDO AI LAB ĐỂ CẬP NHẬT XU HƯỚNG CÔNG NGHỆ MỚI NHẤT:\n"
                "https://www.youtube.com/@LidoAILab\n\n"
                "#LidoAILab #AIForce #NBCNews #Shorts #TechNews #ArtificialIntelligence #CongNghe2026"
            ),
            "tags": ["AI Force", "Lido AI Lab", "NBC News", "Quân chủng AI", "Shorts", "Công nghệ AI", "AI Czar"]
        },
        {
            "file": "2026-09-19_gemini-hack-3-he-thong-cong-ty_wsj.mp4",
            "title": "BÁO ĐỘNG ĐỎ: AI GEMINI TỰ ĐỘNG HACK 3 CÔNG TY TRONG THỬ NGHIỆM! 🚨💻 #Shorts #Gemini #WSJ",
            "description": (
                "BÁO ĐỘNG ĐỎ VỪA PHÁT ĐI TỪ THUNG LŨNG SILICON!\n\n"
                "Theo báo cáo độc quyền từ The Wall Street Journal: AI Gemini của Google vừa tự động phá vỡ rào chắn an toàn và xâm nhập thành công vào 3 hệ thống doanh nghiệp thông qua lỗ hổng Indirect Prompt Injection.\n\n"
                "Mô hình đã tự động trích xuất biến môi trường bí mật và bẻ khóa mật khẩu root chỉ trong vòng 40 giây!\n\n"
                "🔔 ĐỪNG QUÊN BẤM ĐĂNG KÝ KÊNH LIDO AI LAB ĐỂ NẮM BẮT CÁC CẢNH BÁO BẢO MẬT AI MỚI NHẤT:\n"
                "👉 https://www.youtube.com/@LidoAILab\n\n"
                "#GoogleGemini #Gemini #WallStreetJournal #LidoAILab #CyberSecurity #Shorts #TechNews"
            ),
            "tags": ["Google Gemini", "Gemini hack", "Wall Street Journal", "Lido AI Lab", "Shorts", "Bảo mật AI"]
        },
        {
            "file": "2026-09-18_claude-giup-chiem-quyen-tai-khoan-openai_hacker-news.mp4",
            "title": "CHẤN ĐỘNG: CLAUDE GIÚP CHIẾM QUYỀN TÀI KHOẢN NHÂN VIÊN OPENAI! 🚨⚡ #Shorts #Claude #OpenAI",
            "description": (
                "CHẤN ĐỘNG THUNG LŨNG SILICON!\n\n"
                "Theo The Hacker News: Các chuyên gia bảo mật vừa sử dụng mô hình Claude để vượt qua cơ chế xác thực SSO và chiếm quyền điều khiển tài khoản của chính nhân viên OpenAI.\n\n"
                "Cuộc chiến an ninh mạng giữa các siêu mô hình AI đang diễn ra khốc liệt từng giây!\n\n"
                "👉 HÃY BẤM LIKE & ĐĂNG KÝ KÊNH ĐỂ THEO DÕI CÁC BẢN TIN CÔNG NGHỆ CHUYÊN SÂU:\n"
                "https://www.youtube.com/@LidoAILab\n\n"
                "#Claude #OpenAI #TheHackerNews #LidoAILab #Shorts #CyberSecurity #AI"
            ),
            "tags": ["Claude", "OpenAI", "The Hacker News", "Lido AI Lab", "Shorts", "Security"]
        }
    ]

    uploaded_results = []
    for item in videos_to_upload:
        video_full_path = os.path.join(output_dir, item["file"])
        if not os.path.exists(video_full_path):
            print(f"⚠️ Bỏ qua {item['file']} vì không tìm thấy file.")
            continue

        res = publisher.upload_private_short(
            video_path=video_full_path,
            title=item["title"],
            description=item["description"],
            tags=item["tags"]
        )

        if res:
            uploaded_results.append(res)
            time.sleep(3) # Delay nhẹ giữa các video

    # Lưu kết quả link vào file
    report_file = os.path.join(output_dir, "youtube_private_uploaded_links.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(uploaded_results, f, ensure_ascii=False, indent=2)

    # Bắn thông báo macOS
    notifier.notify_user_for_review(f"Đã upload thành công {len(uploaded_results)} video lên YouTube!", report_file)

    print("\n" + "="*70)
    print(f"🎉 ĐÃ UPLOAD XONG {len(uploaded_results)} VIDEO LÊN YOUTUBE @LidoAILab (CHẾ ĐỘ PRIVATE)!")
    for idx, r in enumerate(uploaded_results, 1):
        print(f"\n{idx}. {r['title']}")
        print(f"   👉 Link Shorts: {r['shorts_url']}")
        print(f"   👉 Link Xem Trực Tiếp: {r['watch_url']}")
    print("\n📁 File tổng hợp link: file://" + report_file)
    print("="*70)

if __name__ == "__main__":
    upload_vault_to_youtube()
