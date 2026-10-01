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

        # 1. Chủ đề Giáo dục & Đào tạo
        if any(k in t_low for k in ["giáo dục", "trường học", "đại học", "học sinh", "sinh viên", "giảng viên"]):
            badge_title = "AI TRONG GIÁO DỤC"
            h1 = "ỨNG DỤNG AI TRONG ĐÀO TẠO"
            t1 = f"Thông tin đáng chú ý trong lĩnh vực giáo dục vừa được ghi nhận: {clean_t}!"
            h2 = "ĐỔI MỚI PHƯƠNG PHÁP HỌC TẬP"
            t2 = f"Thay vì học vẹt, các cơ sở đào tạo đang hướng dẫn người học tận dụng AI như trợ thủ nghiên cứu thông minh nhằm phát triển tư duy phản biện."
            h3 = "CÁ NHÂN HÓA LỘ TRÌNH HỌC TẬP"
            t3 = f"Các công cụ AI giúp giải quyết bài toán thiếu hụt tài liệu, hỗ trợ người học tiếp cận kiến thức phù hợp theo năng lực cá nhân."
            h4 = "NÂNG CAO KỸ NĂNG CÔNG NGHỆ"
            t4 = f"Làm chủ kỹ năng khai thác và tương tác với AI là lợi thế cạnh tranh rất lớn cho thế hệ trẻ trong kỷ nguyên số!"
            cmd = "edu-portal --modernize-curriculum --ai-assisted"
            status = "[EDU TECH] Cập nhật phương pháp ứng dụng AI trong giảng dạy..."
            res = "✓ Tối ưu hóa lộ trình học tập thông minh thành công"
            stamp = "🎓 GIÁO DỤC & AI"
            kws = ["University students modern campus laptop studying", "Students technology modern classroom"]

        # 2. Chủ đề Doanh nghiệp & Vận hành kinh doanh
        elif any(k in t_low for k in ["kinh tế", "doanh nghiệp", "nhà máy", "tiết kiệm", "chiến lược", "sản xuất", "bán hàng"]):
            badge_title = "DOANH NGHIỆP & AI"
            h1 = "DOANH NGHIỆP TĂNG TỐC NHỜ AI"
            t1 = f"Xu hướng ứng dụng công nghệ trong kinh doanh vừa được cập nhật: {clean_t}!"
            h2 = "TỐI ƯU HÓA QUY TRÌNH VẬN HÀNH"
            t2 = f"Việc triển khai các giải pháp AI tự hành giúp các doanh nghiệp tinh gọn bộ máy, cắt giảm chi phí vận hành và gia tăng năng suất rõ rệt."
            h3 = "TĂNG TỐC ĐỘ RA QUYẾT ĐỊNH"
            t3 = f"Nhờ các mô hình phân tích dữ liệu lớn, các nhà quản lý có thể nắm bắt biến động thị trường và nhu cầu khách hàng theo thời gian thực."
            h4 = "NÂNG CAO NĂNG LỰC CẠNH TRANH"
            t4 = f"Ứng dụng AI vào thực tế không còn là trào lưu mà đã trở thành công cụ quan trọng để giữ vững lợi thế cạnh tranh!"
            cmd = "biz-ai --optimize-workflow --data-driven"
            status = "[ENTERPRISE] Ứng dụng giải pháp AI vào phân tích dữ liệu..."
            res = "✓ Năng suất tăng trưởng vượt trội, tinh gọn quy trình"
            stamp = "💼 DOANH NGHIỆP AI"
            kws = ["Modern office building digital technology analytics", "Business professionals analyzing digital dashboard data"]

        # 3. Chủ đề Chính sách / Sắc lệnh Quốc Tế (Mỹ, Trump, EU, Toàn cầu)
        elif any(k in t_low for k in ["trump", "mỹ", "white house", "nhà trắng", "eu", "trung quốc", "châu âu"]):
            badge_title = "CHÍNH SÁCH AI QUỐC TẾ"
            h1 = "ĐỘNG THÁI CHÍNH SÁCH MỚI"
            t1 = f"Thông tin chính sách công nghệ quốc tế vừa được truyền thông đưa tin: {clean_t}!"
            h2 = "TÁC ĐỘNG TỚI NGÀNH CÔNG NGHỆ"
            t2 = f"Các sắc lệnh và quy định mới từ các cường quốc công nghệ đang định hình lại tiêu chuẩn phát triển của các phòng lab AI lớn nhất thế giới."
            h3 = "GIÁM SÁT AN TOÀN VÀ CẠNH TRANH"
            t3 = f"Cuộc đua xây dựng khung pháp lý đang diễn ra quyết liệt nhằm cân bằng giữa việc thúc đẩy đột phá và kiểm soát rủi ro của siêu trí tuệ."
            h4 = "THEO DÕI BIẾN ĐỘNG TOÀN CẦU"
            t4 = f"Những thay đổi chính sách từ các nước đi đầu sẽ tác động trực tiếp đến cách các công cụ AI được cung cấp trên toàn thế giới!"
            cmd = "global-policy --track-regulatory-changes --ai-safety"
            status = "[POLICY RADAR] Theo dõi biến động chính sách công nghệ quốc tế..."
            res = "✓ Đã cập nhật phân tích tác động quy định mới"
            stamp = "🏛️ CHÍNH SÁCH QUỐC TẾ"
            kws = ["International government press conference technology", "Global digital policy conference world summit"]

        # 4. Chủ đề Chính sách & Chuyển đổi số trong nước
        elif any(k in t_low for k in ["thủ tướng", "chính phủ", "nghị định", "bộ trưởng", "luật", "chính sách", "chuyển đổi số", "công đoàn"]):
            badge_title = "CHÍNH SÁCH & ĐỜI SỐNG SỐ"
            h1 = "ĐỊNH HƯỚNG CHUYỂN ĐỔI SỐ"
            t1 = f"Chủ trương thúc đẩy công nghệ vừa được công bố rộng rãi: {clean_t}!"
            h2 = "HÀNH LANG PHÁP LÝ RÕ RÀNG"
            t2 = f"Việc chuẩn hóa khung pháp lý và kế hoạch chuyển đổi số giúp xã hội tiếp cận công nghệ mới một cách an toàn và hiệu quả."
            h3 = "PHỔ CẬP TIỆN ÍCH CHO NGƯỜI DÂN"
            t3 = f"Từ thủ tục hành chính công đến tiện ích đời sống, các ứng dụng số đang từng bước được đưa vào phục vụ nhu cầu thực tế."
            h4 = "BẮT KỊP XU HƯỚNG THỜI ĐẠI"
            t4 = f"Làn sóng số hóa sâu rộng đang tạo cơ hội bình đẳng để mọi người dân cùng tiếp cận những tiện ích hiện đại nhất!"
            cmd = "digital-gov --citizen-services --smart-access"
            status = "[DIGITAL GOV] Tối ưu hóa dịch vụ số và trải nghiệm người dùng..."
            res = "✓ Hoàn tất đồng bộ dữ liệu tiện ích công dân"
            stamp = "📋 CHUYỂN ĐỔI SỐ"
            kws = ["Vietnam government digital transformation hall", "Modern smart city citizens using mobile devices"]

        # 5. Chủ đề Hạ tầng, Mạng lưới & Phần cứng công nghệ
        elif any(k in t_low for k in ["5g", "viễn thông", "hạ tầng", "chip", "bán dẫn", "mạng", "internet"]):
            badge_title = "HẠ TẦNG CÔNG NGHỆ"
            h1 = "ĐỘT PHÁ HẠ TẦNG KỸ THUẬT"
            t1 = f"Bước tiến mới trong lĩnh vực hạ tầng kết nối vừa được công bố: {clean_t}!"
            h2 = "BĂNG THÔNG VÀ TỐC ĐỘ VƯỢT TRỘI"
            t2 = f"Hạ tầng mạng thế hệ mới với tốc độ siêu nhanh và độ trễ cực thấp là nền tảng sống còn để vận hành các hệ thống AI quy mô lớn."
            h3 = "ĐẢM BẢO KẾT NỐI LIÊN TỤC"
            t3 = f"Các trung tâm xử lý dữ liệu và hệ thống máy chủ hiện đại đang được mở rộng nhằm đáp ứng nhu cầu truyền tải dữ liệu khổng lồ."
            h4 = "NỀN MÓNG CHO TƯƠNG LAI SỐ"
            t4 = f"Một hạ tầng kỹ thuật vững chắc là điều kiện tiên quyết để toàn bộ hệ sinh thái công nghệ phát triển bùng nổ!"
            cmd = "infra-core --deploy-network-grid --high-speed"
            status = "[INFRASTRUCTURE] Kiểm tra chất lượng đường truyền và máy chủ..."
            res = "✓ Đường truyền ổn định, sẵn sàng chịu tải các tác vụ AI"
            stamp = "📡 HẠ TẦNG SỐ"
            kws = ["Modern datacenter fiber optic cables glowing", "High tech telecommunication server room"]

        # 6. Mặc định Điểm tin Công nghệ & AI
        else:
            badge_title = "ĐIỂM TIN CÔNG NGHỆ"
            h1 = f"TÂM ĐIỂM: {clean_t[:45].upper()}"
            t1 = f"Tin tức công nghệ đáng chú ý vừa được truyền thông chia sẻ: {clean_t}!"
            h2 = "TÍNH NĂNG VÀ ĐỘT PHÁ MỚI"
            t2 = f"Cập nhật này đem tới những trải nghiệm mới mẻ, giúp người dùng theo dõi sát sao những bước tiến công nghệ mới nhất."
            h3 = "TIỀM NĂNG ỨNG DỤNG THỰC TẾ"
            t3 = f"Cộng đồng người dùng và các chuyên gia đang tích cực khám phá cách khai thác tối đa những tiện ích thông minh này."
            h4 = "ĐÓN ĐẦU XU HƯỚNG MỚI"
            t4 = f"Hãy luôn cập nhật tin tức để không bỏ lỡ những phát triển công nghệ đột phá đang diễn ra từng ngày!"
            cmd = "tech-radar --scan-latest-updates --summary"
            status = "[TECH RADAR] Cập nhật bản tin công nghệ mới nhất..."
            res = "✓ Bản tin đã được chọn lọc và kiểm chứng thông tin"
            stamp = "⚡ ĐIỂM TIN AI"
            kws = ["Modern technology background abstract blue network", "Futuristic high tech digital interface display"]

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
            sc["source_label"] = f"{src_clean} • {today_str} (ĐIỂM TIN)"

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
            f"Điểm tin cập nhật công nghệ trí tuệ nhân tạo và chuyển đổi số từ Lido AI Lab.\n"
            f"Nguồn trích dẫn: {topic.get('source', 'Báo chí')} (Cập nhật thời gian thực).\n\n"
            f"👉 HÃY BẤM LIKE, SHARE VÀ ĐĂNG KÝ KÊNH LIDO AI LAB ĐỂ ĐÓN ĐẦU XU HƯỚNG MỖI NGÀY:\n"
            f"https://www.youtube.com/@LidoAILab\n\n"
            f"#LidoAILab #TriTueNhanTao #AI #CongNghe #Shorts #TechNews"
        )

        upload_res = publisher.upload_public_short(
            video_path=final_video_path,
            title=script_data["title"],
            description=desc,
            tags=["TriTueNhanTao", "AI", "CongNghe", "LidoAILab", "TechNews", "Shorts"]
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
