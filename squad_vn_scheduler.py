import asyncio
import os
import sys
import json
import time
import re
from datetime import datetime
from agents.trend_hunter import SmartTrendHunterAgent
from agents.step_flow_producer import StepFlowMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.youtube_api_publisher import YouTubeDirectPublisher
from agents.notifier import NotificationAgent
from agents.script_auditor import ScriptAuditorAgent
from channel_guard import ChannelSecurityGuard

INTERVAL_HOURS = 2
INTERVAL_SECONDS = INTERVAL_HOURS * 3600
VOICE_VN = "vi-VN-NamMinhNeural"
DB_PATH = "/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/seen_news_vn.json"

class SquadVNScheduler:
    def __init__(self):
        self.hunter = SmartTrendHunterAgent(db_path=DB_PATH)
        self.hunter.sources = [
            {"name": "Google News (Việt Nam AI)", "url": "https://news.google.com/rss/search?q=Tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20OR%20ChatGPT%20when%3A48h&hl=vi&gl=VN&ceid=VN:vi"},
            {"name": "Google News (Công Nghệ VN)", "url": "https://news.google.com/rss/search?q=AI%20chuy%E1%BB%83n%20%C4%91%E1%BB%95i%20s%E1%BB%91%20when%3A48h&hl=vi&gl=VN&ceid=VN:vi"}
        ]
        self.hunter.hot_keywords = {
            "trí tuệ nhân tạo": 5, "chatgpt": 5, "chuyển đổi số": 4, "giáo dục": 4, "đại học": 4,
            "doanh nghiệp": 4, "công cụ ai": 4, "tự động hóa": 4, "ứng dụng": 3,
            "việt nam": 3, "robot": 3, "gemini": 4, "deepseek": 4
        }
        self.auditor = ScriptAuditorAgent(history_file="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/seen_scripts_vn.json")

    def generate_vietnamese_script(self, topic):
        clean_t = topic["title"].split(" - ")[0].strip()
        t_low = clean_t.lower()

        # 1. Chủ đề Giáo dục & Đại học
        if any(k in t_low for k in ["giáo dục", "trường học", "đại học", "học sinh", "sinh viên"]):
            badge_title = "AI TRONG GIÁO DỤC VN"
            h1 = "ĐỔI MỚI GIÁO DỤC THỜI ĐẠI AI"
            t1 = f"Thông điệp chuyển đổi số mạnh mẽ trong ngành giáo dục vừa được nhấn mạnh: {clean_t}!"
            h2 = "DẠY TƯ DUY THAY VÌ HỌC VẸT"
            t2 = "Trước sự phổ biến của ChatGPT và các trợ lý ảo, giảng viên và sinh viên bắt buộc phải chuyển từ phương pháp ghi nhớ thụ động sang rèn luyện tư duy phản biện và khả năng kiểm chứng dữ liệu."
            h3 = "ỨNG DỤNG TRỢ LÝ HỌC TẬP THÔNG MINH"
            t3 = "Nhiều trường đại học hàng đầu đã bắt đầu thí điểm đưa AI vào phòng thí nghiệm, hỗ trợ nghiên cứu khoa học và cá nhân hóa tài liệu học tập cho từng sinh viên."
            h4 = "CHUẨN BỊ CHO THỊ TRƯỜNG LAO ĐỘNG"
            t4 = "Thế hệ sinh viên làm chủ công nghệ trí tuệ nhân tạo ngay từ giảng đường sẽ nắm giữ lợi thế cạnh tranh áp đảo trong kỷ nguyên số!"
            cmd = "edu-portal --modernize-curriculum --ai-assisted"
            status = "[EDU TECH] Đồng bộ giáo trình giảng dạy thích ứng AI..."
            res = "✓ Đã tích hợp module trợ lý AI vào 100% môn học chuyên ngành"
            stamp = "🎓 GIÁO DỤC AI"
            kws = ["Vietnam university students modern campus laptop", "Vietnamese students technology classroom"]

        # 2. Chủ đề Doanh nghiệp & Kinh tế số
        elif any(k in t_low for k in ["kinh tế số", "doanh nghiệp", "nhà máy", "tiết kiệm", "chiến lược"]):
            badge_title = "AI DOANH NGHIỆP VIỆT"
            h1 = "DOANH NGHIỆP BỨT PHÁ BẰNG AI"
            t1 = f"Bước chuyển dịch công nghệ mang tính chiến lược đang diễn ra sôi động: {clean_t}!"
            h2 = "TỰ ĐỘNG HÓA TỐI ƯU CHI PHÍ"
            t2 = "Việc triển khai các giải pháp AI tự hành giúp các doanh nghiệp tinh gọn bộ máy vận hành, cắt giảm hàng tỷ đồng chi phí lãng phí và gia tăng năng suất chuỗi cung ứng."
            h3 = "NÂNG TẦM TRẢI NGHIỆM KHÁCH HÀNG"
            t3 = "Từ các chatbot chăm sóc khách hàng 24/7 đến hệ thống phân tích xu hướng thị trường, AI đang trở thành đòn bẩy sống còn của các thương hiệu Việt."
            h4 = "CƠ HỘI ĐỘT PHÁ NĂM 2026"
            t4 = "Doanh nghiệp nào sớm chuyển đổi số toàn diện sẽ nhanh chóng chiếm lĩnh thị phần và vươn tầm ra thị trường quốc tế!"
            cmd = "vn-enterprise --automate-operations --ai-core"
            status = "[ENTERPRISE] Tích hợp AI vào chuỗi vận hành doanh nghiệp..."
            res = "✓ Năng suất tăng 35%, tiết kiệm 40% chi phí vận hành"
            stamp = "💼 DOANH NGHIỆP AI"
            kws = ["Modern Vietnam office building digital technology", "Vietnam business conference digital transformation"]

        # 3. Mặc định Đổi mới Công nghệ
        else:
            badge_title = "CÔNG NGHỆ AI VIỆT NAM"
            h1 = f"TÂM ĐIỂM: {clean_t[:45].upper()}"
            t1 = f"Tin tức công nghệ đáng chú ý nhất trong nước vừa được công bố: {clean_t}!"
            h2 = "TIÊN PHONG THỬ NGHIỆM TÍNH NĂNG MỚI"
            t2 = "Công nghệ này mở ra khả năng tương tác thông minh, giúp người dùng phổ thông tiếp cận với những đột phá mới nhất của cuộc cách mạng AI."
            h3 = "ĐÒN BẨY CHO XÃ HỘI SỐ"
            t3 = "Sự lan tỏa nhanh chóng của các công cụ thông minh đang thúc đẩy mạnh mẽ quá trình phổ cập kỹ năng số trong cộng đồng."
            h4 = "ĐÓN ĐẦU XU HƯỚNG CÔNG NGHỆ"
            t4 = "Hãy chủ động trải nghiệm và ứng dụng công nghệ này vào công việc hàng ngày để nâng cao hiệu suất làm việc của bạn!"
            cmd = "vn-ai --deploy-solution --smart-service"
            status = "[VN-TECH] Kích hoạt cổng dịch vụ công nghệ thông minh..."
            res = "✓ Khởi chạy hệ thống thành công phục vụ người dùng Việt"
            stamp = "🇻🇳 AI VIỆT NAM"
            kws = [f"{clean_t[:25]} Vietnam technology", "Vietnam modern smart city technology"]

        scenes = [
            {"scene_id": 1, "headline": h1, "metric_badge": badge_title, "text": t1, "overlay_data": h1, "search_keywords": kws},
            {"scene_id": 2, "headline": h2, "metric_badge": badge_title, "text": t2, "overlay_data": h2, "search_keywords": kws},
            {"scene_id": 3, "headline": h3, "metric_badge": badge_title, "text": t3, "overlay_data": h3, "search_keywords": kws},
            {"scene_id": 4, "headline": h4, "metric_badge": badge_title, "text": t4, "overlay_data": h4, "search_keywords": kws},
            {
                "scene_id": 5,
                "headline": "KÊNH CÔNG NGHỆ LIDO AI LAB",
                "metric_badge": "LIDO AI LAB",
                "text": "Bấm Like và Đăng ký kênh Lido AI Lab ngay hôm nay để đón đầu những xu hướng công nghệ mới nhất!",
                "overlay_data": "SUBSCRIBE @LidoAILab",
                "search_keywords": ["YouTube subscribe button glowing neon red", "Modern tech creator studio setup"]
            }
        ]

        workflow_metadata = {
            "badge_title": badge_title,
            "step1": h1,
            "step2": h2,
            "term_title": "terminal · lido vn-ai runtime",
            "code_cmd": cmd,
            "code_status": status,
            "code_result": res,
            "step4": h4,
            "stamp_text": stamp
        }

        return {
            "title": f"{badge_title}: {clean_t[:65]}! 🚀⚡ #Shorts #LidoAILab #AI",
            "scenes": scenes,
            "workflow_metadata": workflow_metadata,
            "full_voice_text": " ".join([s["text"] for s in scenes])
        }

    async def run_cycle(self):
        print("\n" + "="*75)
        print(f"🇻🇳 [SQUAD VN] BẮT ĐẦU CHU KỲ QUÉT TIN VIỆT NAM (MỖI {INTERVAL_HOURS} TIẾNG)...")
        print("="*75)

        candidates = self.hunter.fetch_all_fresh_topics(limit_per_source=10)
        if not candidates:
            print("💤 [SQUAD VN] Không có tin tức mới tại Việt Nam trong chu kỳ này.")
            return

        selected_topic = None
        selected_script = None

        for topic in candidates:
            script_data = self.generate_vietnamese_script(topic)
            audit_res = self.auditor.audit_script(topic["title"], script_data)
            if audit_res["passed"]:
                print(f"🎯 [SQUAD VN] Đã chọn tin VN hot nhất: '{topic['title']}' (Điểm: {topic['score']})")
                print(f"🧐 [SQUAD VN Auditor] {audit_res['reason']}")
                selected_topic = topic
                selected_script = script_data
                break
            else:
                print(f"⚠️ [SQUAD VN Auditor] Bỏ qua '{topic['title'][:40]}...': {audit_res['reason']}")

        if not selected_topic or not selected_script:
            print("💤 [SQUAD VN] Toàn bộ tin quét được chưa đạt chuẩn kiểm duyệt chéo.")
            return

        topic = selected_topic
        script_data = selected_script
        self.auditor.record_passed_script(topic["title"], script_data)

        today_str = datetime.now().strftime("%d/%m/%Y")
        src_clean = topic.get("source", "BÁO CHÍ VIỆT NAM").upper()
        for sc in script_data["scenes"]:
            sc["source_label"] = f"{src_clean} • {today_str} (BẢN TIN VN)"

        producer = StepFlowMediaProducerAgent()
        producer.voice = VOICE_VN
        uploader = YouTubeUploaderAgent()

        memorable_name = uploader.generate_memorable_filename(topic["title"], source="vn_news")
        final_video_path = os.path.join(producer.output_dir, f"vn_{memorable_name}")

        temp_video = await producer.produce_step_animated_short(script_data, topic_info=topic)
        os.rename(temp_video, final_video_path)

        self.hunter.save_seen_title(topic["title"])

        guard = ChannelSecurityGuard("lido_ai_lab", os.path.join(os.path.dirname(__file__), "credentials"))
        guard.verify_channel_or_fail({"title": script_data["title"]})

        publisher = YouTubeDirectPublisher(token_path=str(guard.token_file))
        desc = (
            f"{script_data['title']}\n\n"
            f"Bản tin công nghệ trí tuệ nhân tạo Việt Nam từ Lido AI Lab.\n"
            f"Nguồn trích dẫn: {topic.get('source', 'Báo chí Việt Nam')} (Cập nhật thời gian thực).\n\n"
            f"👉 HÃY BẤM LIKE, SHARE VÀ ĐĂNG KÝ KÊNH LIDO AI LAB ĐỂ ĐÓN ĐẦU XU HƯỚNG MỖI NGÀY:\n"
            f"https://www.youtube.com/@LidoAILab\n\n"
            f"#LidoAILab #AIVietNam #TriTueNhanTao #Shorts #TechNews"
        )

        upload_res = publisher.upload_public_short(
            video_path=final_video_path,
            title=script_data["title"],
            description=desc,
            tags=["AIVietNam", "TriTueNhanTao", "CongNghe", "LidoAILab", "Shorts"]
        )

        notifier = NotificationAgent()
        if upload_res:
            yt_link = upload_res["shorts_url"]
            notifier.notify_user_for_review(f"[SQUAD VN] Video mới ĐÃ ĐĂNG: {yt_link}", final_video_path)
            print("\n" + "="*75)
            print(f"🎉 [SQUAD VN] ĐÃ ĐĂNG THÀNH CÔNG LÊN @LidoAILab!")
            print(f"🔗 Link Shorts: {yt_link}")
            print("="*75)

    async def start(self):
        print("🚀 [SQUAD VN] BIỆT ĐỘI AI VIỆT NAM ĐÃ KHỞI CHẠY (QUÉT MỖI 2 TIẾNG)!")
        while True:
            try:
                await self.run_cycle()
            except Exception as e:
                print(f"⚠️ [SQUAD VN] Lỗi trong chu kỳ: {e}")
            print(f"\n⏳ [SQUAD VN] Nghỉ {INTERVAL_HOURS} tiếng trước chu kỳ quét tiếp theo...")
            await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    squad = SquadVNScheduler()
    asyncio.run(squad.start())
