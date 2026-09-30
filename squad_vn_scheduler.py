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
            {"name": "Google News VN – AI", "url": "https://news.google.com/rss/search?q=Tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20OR%20ChatGPT%20when%3A48h&hl=vi&gl=VN&ceid=VN:vi"},
            {"name": "Google News VN – Chuyển đổi số", "url": "https://news.google.com/rss/search?q=AI%20chuy%E1%BB%83n%20%C4%91%E1%BB%95i%20s%E1%BB%91%20when%3A48h&hl=vi&gl=VN&ceid=VN:vi"},
            {"name": "VnExpress AI & Số Hóa", "url": "https://vnexpress.net/rss/so-hoa.rss"},
            {"name": "Znews Công Nghệ", "url": "https://znews.vn/rss/cong-nghe.rss"},
            {"name": "VietnamNet AI & Công Nghệ", "url": "https://vietnamnet.vn/rss/cong-nghe.rss"},
            {"name": "GenK AI & Công Nghệ", "url": "https://genk.vn/rss/home.rss"},
            {"name": "Tinhte AI & Công Nghệ", "url": "https://tinhte.vn/rss"},
            {"name": "ICTNews (Bộ TT&TT / VNN)", "url": "https://vietnamnet.vn/rss/thong-tin-truyen-thong.rss"}
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
        if any(k in t_low for k in ["giáo dục", "trường học", "đại học", "học sinh", "sinh viên", "giảng viên"]):
            badge_title = "AI TRONG GIÁO DỤC VN"
            h1 = "ĐỔI MỚI GIÁO DỤC THỜI ĐẠI AI"
            t1 = f"Thông điệp chuyển đổi số mạnh mẽ trong ngành giáo dục vừa được nhấn mạnh: {clean_t}!"
            h2 = "DẠY TƯ DUY THAY VÌ HỌC VẸT"
            t2 = f"Thay vì cấm đoán công nghệ, các cơ sở đào tạo đang định hướng sinh viên sử dụng AI như trợ thủ nghiên cứu đắc lực nhằm nâng cao tư duy phản biện."
            h3 = "CÁ NHÂN HÓA LỘ TRÌNH HỌC TẬP"
            t3 = f"Trợ lý AI giúp giải quyết bài toán thiếu hụt tài nguyên học tập, hỗ trợ từng học viên tiếp cận giáo trình theo năng lực riêng biệt."
            h4 = "LỢI THẾ CẠNH TRANH KỶ NGUYÊN SỐ"
            t4 = f"Làm chủ kỹ năng tương tác và điều khiển AI ngay từ giảng đường là tấm vé bảo chứng việc làm bền vững cho người trẻ!"
            cmd = "edu-portal --modernize-curriculum --ai-assisted"
            status = "[EDU TECH] Đồng bộ giáo trình giảng dạy thích ứng AI..."
            res = "✓ Đã tích hợp module trợ lý AI vào 100% môn học chuyên ngành"
            stamp = "🎓 GIÁO DỤC AI"
            kws = ["Vietnam university students modern campus laptop", "Vietnamese students technology classroom"]

        # 2. Chủ đề Doanh nghiệp & Kinh tế số
        elif any(k in t_low for k in ["kinh tế số", "doanh nghiệp", "nhà máy", "tiết kiệm", "chiến lược", "sản xuất"]):
            badge_title = "AI DOANH NGHIỆP VIỆT"
            h1 = "DOANH NGHIỆP BỨT PHÁ BẰNG AI"
            t1 = f"Bước chuyển dịch công nghệ mang tính chiến lược đang diễn ra sôi động: {clean_t}!"
            h2 = "TỰ ĐỘNG HÓA TỐI ƯU CHI PHÍ"
            t2 = f"Hàng loạt tập đoàn và startup trong nước đang ứng dụng AI để tối ưu hóa quy trình, giảm tải hàng ngàn giờ lao động thủ công mỗi tháng."
            h3 = "TĂNG TỐC ĐỘ RA QUYẾT ĐỊNH"
            t3 = f"Nhờ các mô hình phân tích dữ liệu lớn, lãnh đạo doanh nghiệp có thể nắm bắt biến động thị trường và nhu cầu khách hàng theo thời gian thực."
            h4 = "NÂNG CAO NĂNG LỰC CẠNH TRANH"
            t4 = f"Ứng dụng AI thực chiến không còn là lựa chọn mà đã trở thành yếu tố quyết định sự sống còn của doanh nghiệp trong nền kinh tế số!"
            cmd = "vn-enterprise --automate-operations --ai-core"
            status = "[ENTERPRISE] Tích hợp AI vào chuỗi vận hành doanh nghiệp..."
            res = "✓ Năng suất tăng 35%, tiết kiệm 40% chi phí vận hành"
            stamp = "💼 DOANH NGHIỆP AI"
            kws = ["Modern Vietnam office building digital technology", "Vietnam business conference digital transformation"]

        # 3. Chủ đề Chính sách & Quyết định tầm quốc gia
        elif any(k in t_low for k in ["thủ tướng", "chính phủ", "nghị định", "sắc lệnh", "quốc gia", "bộ trưởng", "luật", "chính sách"]):
            badge_title = "CHÍNH SÁCH AI VIỆT NAM"
            h1 = "ĐỊNH HƯỚNG CHIẾN LƯỢC QUỐC GIA"
            t1 = f"Quyết sách chiến lược thúc đẩy công nghệ vừa được công bố: {clean_t}!"
            h2 = "XÂY DỰNG HÀNH LANG PHÁP LÝ"
            t2 = f"Việc chuẩn hóa khung pháp lý an toàn và minh bạch giúp thu hút dòng vốn đầu tư công nghệ cao, bảo vệ dữ liệu công dân số."
            h3 = "THÚC ĐẨY HẠ TẦNG SỐ VÀ DỮ LIỆU"
            t3 = f"Đầu tư mạnh mẽ vào các trung tâm dữ liệu và siêu máy tính AI trong nước nhằm bảo đảm chủ quyền số quốc gia trên không gian mạng."
            h4 = "VIỆT NAM VƯƠN TẦM CÔNG NGHỆ"
            t4 = f"Chiến lược công nghệ quốc gia bài bản đang tạo bệ phóng vững chắc đưa Việt Nam trở thành điểm đến đổi mới sáng tạo hàng đầu khu vực!"
            cmd = "gov-strategy --deploy-national-ai-framework"
            status = "[NATIONAL POLICY] Hoàn thiện khung kiến trúc dữ liệu và AI quốc gia..."
            res = "✓ Đã ban hành hướng dẫn triển khai cho các bộ ngành và địa phương"
            stamp = "🏛️ CHÍNH SÁCH SỐ"
            kws = ["Vietnam government digital transformation hall", "Hanoi modern skyline smart government technology"]

        # 4. Chủ đề Ứng dụng thực chiến & Đời sống số
        elif any(k in t_low for k in ["ứng dụng", "công đoàn", "người dân", "bán hàng", "kinh doanh", "đời sống", "tiện ích"]):
            badge_title = "AI TRONG ĐỜI SỐNG VIỆT"
            h1 = "CÔNG NGHỆ PHỤC VỤ ĐỜI SỐNG"
            t1 = f"Tin tức ứng dụng thiết thực vừa được triển khai sâu rộng: {clean_t}!"
            h2 = "ĐƯA AI ĐẾN TẬN TAY NGƯỜI DÂN"
            t2 = f"Các giải pháp AI thông minh đang được đơn giản hóa để bất kỳ người dân hay người lao động nào cũng có thể thao tác dễ dàng trên điện thoại."
            h3 = "GIẢI QUYẾT BÀI TOÁN HÀNG NGÀY"
            t3 = f"Từ hỗ trợ soạn thảo văn bản, bán hàng trực tuyến đến tra cứu thủ tục hành chính, công nghệ đang trực tiếp nâng cao chất lượng cuộc sống."
            h4 = "PHỔ CẬP KỸ NĂNG SỐ TOÀN DÂN"
            t4 = f"Làn sóng phổ cập công nghệ đang xóa nhòa khoảng cách số, giúp mọi người cùng bắt nhịp tiến bộ của thời đại!"
            cmd = "smart-life --bridge-digital-divide --citizen-app"
            status = "[SMART LIFE] Triển khai nền tảng tiện ích AI tới cộng đồng..."
            res = "✓ Hoàn thành cài đặt và hướng dẫn ứng dụng thực tế"
            stamp = "📱 TIỆN ÍCH AI"
            kws = ["Vietnamese people using smart mobile phone digital app", "Vietnam modern lifestyle digital community"]

        # 5. Chủ đề Phần cứng, Hạ tầng viễn thông & 5G
        elif any(k in t_low for k in ["5g", "viễn thông", "hạ tầng", "chip", "bán dẫn", "mạng"]):
            badge_title = "HẠ TẦNG CÔNG NGHỆ VN"
            h1 = "BƯỚC TIẾN HẠ TẦNG VIỆT NAM"
            t1 = f"Đột phá về hạ tầng kỹ thuật vừa chính thức được ghi nhận: {clean_t}!"
            h2 = "NỀN TẢNG KẾT NỐI TỐC ĐỘ CAO"
            t2 = f"Triển khai mạng lưới thế hệ mới cung cấp băng thông siêu rộng và độ trễ cực thấp, đáp ứng các mô hình AI tính toán lớn."
            h3 = "LÀM CHỦ CÔNG NGHỆ MAKE IN VIETNAM"
            t3 = f"Các kỹ sư Việt Nam đang từng bước nghiên cứu, tự chủ thiết kế và sản xuất các thiết bị viễn thông công nghệ cao vươn tầm quốc tế."
            h4 = "SẴN SÀNG CHO KỶ NGUYÊN SIÊU KẾT NỐI"
            t4 = f"Hạ tầng số hiện đại chính là xương sống thúc đẩy toàn bộ nền kinh tế số bùng nổ trong những năm tới!"
            cmd = "infra-core --deploy-5g-network --mesh-ready"
            status = "[TELECOM] Kiểm thử trạm phát sóng và trung tâm xử lý dữ liệu..."
            res = "✓ Độ trễ dưới 1 mili-giây, tương thích toàn bộ hệ thống AI"
            stamp = "📡 HẠ TẦNG SỐ"
            kws = ["Vietnam 5g telecommunication tower antenna sunset", "Modern server room datacenter Vietnam technology"]

        # 6. Mặc định Đổi mới Công nghệ & Đột phá AI
        else:
            badge_title = "CÔNG NGHỆ AI VIỆT NAM"
            h1 = f"TÂM ĐIỂM: {clean_t[:45].upper()}"
            t1 = f"Tin tức công nghệ đáng chú ý nhất trong nước vừa được công bố: {clean_t}!"
            h2 = "KHÁM PHÁ CÔNG NGHỆ MỚI NHẤT"
            t2 = f"Đột phá này đem tới những trải nghiệm mới mẻ, giúp người dùng trong nước tiếp cận nhanh nhất với các công cụ dẫn đầu xu thế toàn cầu."
            h3 = "MỞ RỘNG KHẢ NĂNG ỨNG DỤNG"
            t3 = f"Cộng đồng công nghệ Việt Nam đang nhanh chóng tích hợp các tính năng tiên tiến này vào học tập, làm việc và nghiên cứu chuyên sâu."
            h4 = "ĐÓN ĐẦU LÀN SÓNG ĐỔI MỚI"
            t4 = f"Hãy luôn cập nhật và làm chủ các bước tiến mới để chủ động kiến tạo tương lai trong kỷ nguyên trí tuệ nhân tạo!"
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
