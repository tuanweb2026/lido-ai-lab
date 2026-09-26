import asyncio
import os
import json
import time
from agents.trend_hunter import SmartTrendHunterAgent
from agents.script_writer import TechnicalDeepDiveScriptWriterAgent
from agents.media_producer import RealPhotoMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.notifier import NotificationAgent

async def produce_batch_5_videos():
    print("==========================================================================")
    print("🚀 BẮT ĐẦU QUY TRÌNH SẢN XUẤT HÀNG LOẠT 5 VIDEO TIN TỨC AI NÓNG NHẤT")
    print("==========================================================================")

    hunter = SmartTrendHunterAgent()
    # Lấy danh sách top 5 tin tức hot nhất hiện tại
    candidates = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    import urllib.request
    import feedparser

    for src in hunter.sources:
        try:
            req = urllib.request.Request(src["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                feed = feedparser.parse(resp.read())
                for entry in feed.entries[:12]:
                    title = entry.title
                    if title in hunter.seen_titles:
                        continue
                    score = 1
                    t_lower = title.lower()
                    matched_kw = []
                    for kw, weight in hunter.hot_keywords.items():
                        if kw in t_lower:
                            score += weight
                            matched_kw.append(kw)
                    candidates.append({
                        "title": title,
                        "link": entry.link,
                        "score": score,
                        "keywords": matched_kw
                    })
        except Exception as e:
            pass

    # Sắp xếp và lấy 5 tin điểm cao nhất, lọc trùng lặp
    candidates.sort(key=lambda x: x["score"], reverse=True)
    selected_topics = []
    seen_titles_set = set()
    for c in candidates:
        if c["title"] not in seen_titles_set:
            seen_titles_set.add(c["title"])
            selected_topics.append(c)
            if len(selected_topics) == 5:
                break

    print(f"🎯 Đã chọn lọc thành công 5 chủ đề nóng nhất hôm nay:")
    for i, t in enumerate(selected_topics, 1):
        print(f"  {i}. [{t['score']} pts] {t['title']}")

    producer = RealPhotoMediaProducerAgent()
    uploader = YouTubeUploaderAgent()
    notifier = NotificationAgent()
    completed_videos = []

    # Danh sách template kịch bản phong phú cho 5 chủ đề khác nhau
    script_templates = [
        # Video 1: Claude vs OpenAI
        {
            "scenes": [
                {"scene_id": 1, "image_file": "security_breach.jpg", "headline": "CLAUDE VƯỢT MẶT OPENAI", "metric_badge": "LỖ HỔNG BẢO MẬT CHẤN ĐỘNG", "text": "Tin chấn động giới AI: Các chuyên gia vừa dùng mô hình Claude để chiếm quyền điều khiển tài khoản nhân viên của chính OpenAI!", "overlay_data": "CLAUDE vs OPENAI SECURITY"},
                {"scene_id": 2, "image_file": "gemini_hack_alert.jpg", "headline": "CHUỖI LỖ HỔNG XÂM NHẬP", "metric_badge": "CHAINED EXPLOIT 2026", "text": "Bằng cách kết hợp chuỗi lỗ hổng xác thực API, AI đã tự động giải mã token truy cập nội bộ mà không kích hoạt hệ thống báo động!", "overlay_data": "VƯỢT QUA BỨC TƯỜNG LỬA"},
                {"scene_id": 3, "image_file": "autonomous_agent.jpg", "headline": "CUỘC CHIẾN AN NINH MẠNG", "metric_badge": "AI TẤN CÔNG HỆ THỐNG AI", "text": "Đây là minh chứng rõ ràng: Cuộc chiến an ninh mạng giữa các tập đoàn AI hàng đầu thế giới đang diễn ra khốc liệt từng giây!", "overlay_data": "KỶ NGUYÊN TÁC CHIẾN AI"},
                {"scene_id": 4, "image_file": "scene_5_ai_engineer.jpg", "headline": "THEO DÕI LIDO AI LAB", "metric_badge": "GIA NHẬP CỘNG ĐỒNG TINH HOA", "text": "Đăng ký kênh Lido AI Lab ngay hôm nay để cập nhật những diễn biến công nghệ AI cốt lõi và chiến lược phòng thủ mới nhất!", "overlay_data": "SUBSCRIBE: YOUTUBE.COM/@LidoAILab"}
            ],
            "title": "CHẤN ĐỘNG: CLAUDE GIÚP CHIẾM QUYỀN TÀI KHOẢN NHÂN VIÊN OPENAI! 🚨💻 #Shorts #OpenAI #Claude"
        },
        # Video 2: DeepSeek R1 & Chip H800
        {
            "scenes": [
                {"scene_id": 1, "image_file": "scene_2_nvidia_h100.jpg", "headline": "BÍ MẬT KIẾN TRÚC DEEPSEEK", "metric_badge": "TỐI ƯU BỘ NHỚ KỶ LỤC", "text": "Làm thế nào DeepSeek lại có thể vượt qua OpenAI chỉ với số chip GPU ít hơn tám mươi phần trăm? Câu trả lời nằm ở thuật toán!", "overlay_data": "TIẾT KIỆM 80% LƯỢNG GPU"},
                {"scene_id": 2, "image_file": "scene_3_datacenter.jpg", "headline": "CÔNG NGHỆ NÉN KV CACHE", "metric_badge": "KIẾN TRÚC MLA ĐỘT PHÁ", "text": "Kiến trúc Multi-head Latent Attention đã nén bộ nhớ đệm xuống mức siêu nhỏ, cho phép chạy mô hình khổng lồ trên phần cứng giá rẻ!", "overlay_data": "-93% DUNG LƯỢNG VRAM"},
                {"scene_id": 3, "image_file": "scene_4_code_terminal.jpg", "headline": "CÚ ĐÁNH VÀO PHẦN CỨNG ĐẮT TIỀN", "metric_badge": "THUẬT TOÁN ĐỔI NGÔI", "text": "Các tập đoàn công nghệ không còn cần đốt hàng trăm triệu đô vào GPU. Thuật toán tinh hoa đã chính thức làm chủ cuộc chơi!", "overlay_data": "THUẬT TOÁN > TIỀN BẠC"},
                {"scene_id": 4, "image_file": "scene_5_ai_engineer.jpg", "headline": "CẬP NHẬT CÙNG LIDO AI LAB", "metric_badge": "TIÊN PHONG CÔNG NGHỆ LÕI", "text": "Bấm Follow Lido AI Lab để không bỏ lỡ những phân tích kiến trúc AI sâu sắc nhất thị trường!", "overlay_data": "SUBSCRIBE: YOUTUBE.COM/@LidoAILab"}
            ],
            "title": "BÍ MẬT THUẬT TOÁN: TẠI SAO DEEPSEEK CẦN ÍT HƠN 80% GPU? 🧠⚡ #Shorts #DeepSeek #AI"
        },
        # Video 3: Perplexity AI thách thức Google Search
        {
            "scenes": [
                {"scene_id": 1, "image_file": "scene_4_code_terminal.jpg", "headline": "GOOGLE SEARCH BỊ ĐE DỌA", "metric_badge": "PERPLEXITY TRỖI DẬY", "text": "Đế chế tìm kiếm hai mươi năm của Google đang lung lay dữ dội trước sự bùng nổ của Perplexity AI và các công cụ tìm kiếm đàm thoại!", "overlay_data": "CUỘC CHIẾN TÌM KIẾM AI"},
                {"scene_id": 2, "image_file": "gemini_google_ai.jpg", "headline": "TRẢ LỜI THẲNG VÀO VẤN ĐỀ", "metric_badge": "KHÔNG QUẢNG CÁO RÁC", "text": "Thay vì bắt người dùng bấm vào mười đường link đầy quảng cáo, AI tổng hợp câu trả lời chính xác kèm nguồn trích dẫn uy tín ngay lập tức!", "overlay_data": "TRẢ LỜI TRỰC TIẾP & CÓ NGUỒN"},
                {"scene_id": 3, "image_file": "scene_1_market_crash.jpg", "headline": "CHUYỂN DỊCH DOANH THU KHỦNG", "metric_badge": "THỊ PHẦN QUẢNG CÁO BỊ XÂM LẤN", "text": "Hàng trăm tỷ đô la doanh thu quảng cáo tìm kiếm truyền thống đang dần chuyển dịch sang các nền tảng trí tuệ nhân tạo mới!", "overlay_data": "DÒNG TIỀN CHUYỂN DỊCH VỀ AI"},
                {"scene_id": 4, "image_file": "scene_5_ai_engineer.jpg", "headline": "KHÁM PHÁ CÔNG CỤ MỚI", "metric_badge": "LIDO AI LAB TIPS", "text": "Đăng ký kênh Lido AI Lab để làm chủ các công cụ AI tìm kiếm và gia tăng năng suất làm việc vượt trội!", "overlay_data": "SUBSCRIBE: YOUTUBE.COM/@LidoAILab"}
            ],
            "title": "PERPLEXITY AI ĐANG ĐE DỌA ĐẾ CHẾ GOOGLE SEARCH NHƯ THẾ NÀO? 🔍⚡ #Shorts #Perplexity #Google"
        },
        # Video 4: Cursor AI & Cuộc cách mạng Lập trình
        {
            "scenes": [
                {"scene_id": 1, "image_file": "scene_4_code_terminal.jpg", "headline": "LẬP TRÌNH VIÊN THỜI KỶ NGUYÊN MỚI", "metric_badge": "CURSOR AI BÙNG NỔ", "text": "Cursor AI và các công cụ lập trình tự động đang định nghĩa lại hoàn toàn cách các kỹ sư phần mềm trên toàn thế giới viết code!", "overlay_data": "TĂNG TỐC ĐỘ CODE GẤP 5 LẦN"},
                {"scene_id": 2, "image_file": "autonomous_agent.jpg", "headline": "HIỂU TOÀN BỘ CODEBASE", "metric_badge": "MULTI-FILE EDITING", "text": "Khả năng quét toàn bộ cấu trúc dự án và chỉnh sửa đồng thời hàng chục file đang biến một lập trình viên thành cả một đội ngũ kỹ sư!", "overlay_data": "TỰ ĐỘNG REFACTORING HÀNG LOẠT"},
                {"scene_id": 3, "image_file": "scene_3_datacenter.jpg", "headline": "BẠN KHÔNG THỂ ĐỨNG NGOÀI", "metric_badge": "KỸ NĂNG BẮT BUỘC 2026", "text": "Trong tương lai rất gần, người bị thay thế không phải là lập trình viên, mà là người không biết sử dụng AI để nhân bản sức mạnh!", "overlay_data": "TỐI ƯU HIỆU SUẤT VỚI AI"},
                {"scene_id": 4, "image_file": "scene_5_ai_engineer.jpg", "headline": "NÂNG TẦM KỸ NĂNG LẬP TRÌNH", "metric_badge": "LIDO AI LAB DEV", "text": "Theo dõi ngay Lido AI Lab để học cách ứng dụng AI Agents vào lập trình thực chiến mỗi ngày!", "overlay_data": "SUBSCRIBE: YOUTUBE.COM/@LidoAILab"}
            ],
            "title": "CURSOR AI: CÔNG CỤ BIẾN 1 LẬP TRÌNH VIÊN THÀNH CẢ ĐỘI NGŨ KỸ SƯ! 💻🚀 #Shorts #CursorAI #Coding"
        },
        # Video 5: Humanoid Robots & Siêu trí tuệ AGI
        {
            "scenes": [
                {"scene_id": 1, "image_file": "autonomous_agent.jpg", "headline": "ROBOT HÌNH NGƯỜI TIẾN HÓA", "metric_badge": "TESLA OPTIMUS & FIGURE 02", "text": "Sự kết hợp giữa mô hình thị giác ngôn ngữ lớn và robot hình người đang đưa công nghệ bước thẳng vào đời sống thực tế!", "overlay_data": "ROBOT TỰ HỌC QUA THỊ GIÁC"},
                {"scene_id": 2, "image_file": "scene_2_nvidia_h100.jpg", "headline": "SIÊU CHIP XỬ LÝ TẠI CHỖ", "metric_badge": "TRÍ TUỆ NHÂN TẠO THỂ HIỆN", "text": "Không chỉ làm theo lập trình cứng, các robot thế hệ mới giờ đây có thể tự nhìn nhận không gian, tự sửa sai và thao tác linh hoạt như con người!", "overlay_data": "TỰ THÍCH ỨNG MÔI TRƯỜNG THỰC"},
                {"scene_id": 3, "image_file": "scene_1_market_crash.jpg", "headline": "THAY ĐỔI CƠ CẤU LAO ĐỘNG", "metric_badge": "CÁCH MẠNG TỰ ĐỘNG HÓA", "text": "Ngành sản xuất và dịch vụ sẽ chứng kiến sự chuyển dịch nhân sự lớn nhất trong lịch sử khi hàng triệu robot bắt đầu bước vào nhà máy!", "overlay_data": "KỶ NGUYÊN LAO ĐỘNG TỰ HÀNH"},
                {"scene_id": 4, "image_file": "scene_5_ai_engineer.jpg", "headline": "ĐÓN ĐẦU KỶ NGUYÊN ROBOT", "metric_badge": "LIDO AI LAB FUTURE", "text": "Hãy Đăng ký kênh Lido AI Lab để cập nhật những đột phá công nghệ tương lai nhanh và chuẩn xác nhất!", "overlay_data": "SUBSCRIBE: YOUTUBE.COM/@LidoAILab"}
            ],
            "title": "ROBOT HÌNH NGƯỜI TÍCH HỢP AI: KỶ NGUYÊN LAO ĐỘNG MỚI ĐÃ BẮT ĐẦU! 🤖⚡ #Shorts #Robot #FutureTech"
        }
    ]

    for idx, (topic_info, script_pack) in enumerate(zip(selected_topics, script_templates), 1):
        print(f"\n🎬 [SẢN XUẤT {idx}/5] Bắt đầu dựng video: '{script_pack['title']}'...")
        
        # Đặt tên file video riêng cho từng bài
        out_name = f"lido_video_{idx}_{int(time.time())}.mp4"
        out_video_path = os.path.join(producer.output_dir, out_name)
        
        # Render video
        video_f = await producer.produce_real_photo_short(script_pack["scenes"])
        os.rename(video_f, out_video_path)

        # Lưu vào danh sách đã duyệt
        hunter.save_seen_title(topic_info["title"])

        # Tạo metadata
        meta = {
            "video_id": idx,
            "title": script_pack["title"],
            "topic_source": topic_info["title"],
            "video_file": out_video_path,
            "description": f"{script_pack['title']}\n\n👉 Kênh phân tích công nghệ: https://www.youtube.com/@LidoAILab\n#Shorts #AI #LidoAILab",
            "tags": ["AI News", "Technology", "Lido AI Lab", "Shorts"]
        }
        completed_videos.append(meta)
        print(f"✅ ĐÃ HOÀN THÀNH VIDEO {idx}/5: {out_video_path}")

    # Đóng gói danh sách 5 video
    summary_path = os.path.join(producer.output_dir, "batch_5_videos_manifest.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(completed_videos, f, ensure_ascii=False, indent=2)

    # Bắn thông báo macOS
    notifier.notify_user_for_review("Hoàn tất 5 video tin tức AI mới nhất", summary_path)
    print("\n" + "="*70)
    print("🎉 ĐÃ HOÀN THÀNH TOÀN BỘ 5 VIDEO SHORTS TIN TỨC AI!")
    print(f"📁 Báo cáo tổng hợp 5 video: file://{summary_path}")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(produce_batch_5_videos())
