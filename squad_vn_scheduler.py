import asyncio
import os
import sys
import json
import time
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
        # Nguồn tin chuyên biệt cho Việt Nam
        self.hunter.sources = [
            {"name": "Google News (Việt Nam AI)", "url": "https://news.google.com/rss/search?q=Tr%C3%AD%20tu%E1%BB%87%20nh%C3%A2n%20t%E1%BA%A1o%20OR%20ChatGPT%20when%3A48h&hl=vi&gl=VN&ceid=VN:vi"},
            {"name": "Google News (Công Nghệ VN)", "url": "https://news.google.com/rss/search?q=AI%20chuy%E1%BB%83n%20%C4%91%E1%BB%95i%20s%E1%BB%91%20when%3A48h&hl=vi&gl=VN&ceid=VN:vi"}
        ]
        # Bộ từ khóa ưu tiên thực tiễn Việt Nam
        self.hunter.hot_keywords = {
            "trí tuệ nhân tạo": 5, "chatgpt": 5, "chuyển đổi số": 4, "giáo dục": 4,
            "doanh nghiệp": 4, "công cụ ai": 4, "tự động hóa": 4, "ứng dụng": 3,
            "việt nam": 3, "robot": 3, "gemini": 4, "deepseek": 4
        }
        self.auditor = ScriptAuditorAgent(history_file="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/seen_scripts_vn.json")

    def generate_vietnamese_script(self, topic):
        clean_t = topic["title"].split(" - ")[0].strip()
        badge_title = "CÔNG NGHỆ AI VIỆT NAM"
        h1 = f"TÂM ĐIỂM: {clean_t[:45].upper()}"
        t1 = f"Thông tin công nghệ đáng chú ý nhất vừa được ghi nhận: {clean_t}!"
        
        h2 = "ỨNG DỤNG THỰC TIỄN NỔI BẬT"
        t2 = "Công nghệ này đang nhanh chóng được ứng dụng vào đời sống và doanh nghiệp, giúp rút ngắn thời gian xử lý công việc và tối ưu hóa hiệu suất vượt bậc."
        
        h3 = "CƠ HỘI BỨT PHÁ TRONG NƯỚC"
        t3 = "Các chuyên gia nhận định việc sớm làm chủ các giải pháp tự động hóa thông minh sẽ mở ra lợi thế cạnh tranh rất lớn cho các cá nhân và tổ chức."
        
        h4 = "LỜI KHUYÊN CHO NGƯỜI DÙNG"
        t4 = "Hãy chủ động tìm hiểu và tích hợp các công cụ AI vào quy trình làm việc ngay hôm nay để đón đầu làn sóng chuyển đổi số!"

        scenes = [
            {"scene_id": 1, "headline": h1, "metric_badge": badge_title, "text": t1, "overlay_data": h1, "search_keywords": [f"{clean_t[:30]} Vietnam technology", "Vietnam modern digital tech"]},
            {"scene_id": 2, "headline": h2, "metric_badge": badge_title, "text": t2, "overlay_data": h2, "search_keywords": ["AI business application modern office", "Digital transformation dashboard"]},
            {"scene_id": 3, "headline": h3, "metric_badge": badge_title, "text": t3, "overlay_data": h3, "search_keywords": ["Vietnam software engineer working laptop", "AI technology innovation presentation"]},
            {"scene_id": 4, "headline": h4, "metric_badge": badge_title, "text": t4, "overlay_data": h4, "search_keywords": ["Vietnamese youth innovative technology", "Modern creator studio neon setup"]},
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
            "code_cmd": "vn-ai --deploy-solution --vietnam-region",
            "code_status": "[VN-AI] Đang kích hoạt giải pháp tự động hóa...",
            "code_result": "✓ Triển khai giải pháp thành công cho người dùng Việt",
            "step4": h4,
            "stamp_text": "🇻🇳 AI VIỆT NAM"
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

        topic = candidates[0]
        print(f"🎯 [SQUAD VN] Đã chọn tin VN hot nhất: '{topic['title']}' (Điểm: {topic['score']})")

        script_data = self.generate_vietnamese_script(topic)
        
        # Kiểm duyệt chéo
        audit_res = self.auditor.audit_script(topic["title"], script_data)
        print(f"🧐 [SQUAD VN Auditor] {audit_res['reason']}")
        if not audit_res["passed"]:
            print(f"⚠️ [SQUAD VN] Kịch bản bị từ chối: {audit_res['reason']}")
            return

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
