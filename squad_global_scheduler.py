import asyncio
import os
import sys
import json
import time
from datetime import datetime
from agents.trend_hunter import SmartTrendHunterAgent
from agents.global_en_script_writer import GlobalEnglishScriptWriterAgent
from agents.step_flow_producer import StepFlowMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.youtube_api_publisher import YouTubeDirectPublisher
from agents.notifier import NotificationAgent
from agents.script_auditor import ScriptAuditorAgent
from channel_guard import ChannelSecurityGuard

INTERVAL_HOURS = 2
INTERVAL_SECONDS = INTERVAL_HOURS * 3600
VOICE_EN = "en-US-AndrewNeural" # Giọng đọc tiếng Anh chuyên gia
DB_PATH = "/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/seen_news.json"

class SquadGlobalScheduler:
    def __init__(self):
        self.hunter = SmartTrendHunterAgent(db_path=DB_PATH)
        # Nguồn tin chuyên biệt Quốc Tế
        self.hunter.sources = [
            {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
            {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"},
            {"name": "HackerNews Trending AI", "url": "https://hnrss.org/newest?q=AI+OR+LLM+OR+GPT+OR+Agent"},
            {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"},
            {"name": "Google News (Top AI)", "url": "https://news.google.com/rss/search?q=Artificial%20Intelligence%20when:24h&hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News (ChatGPT & DeepSeek)", "url": "https://news.google.com/rss/search?q=ChatGPT%20OR%20DeepSeek%20OR%20Claude%20OR%20Perplexity%20when:24h&hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News (Video AI & Sora)", "url": "https://news.google.com/rss/search?q=Sora%20OR%20Kling%20OR%20Runway%20OR%20Flux%20AI%20when:48h&hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News (NVIDIA & Robot)", "url": "https://news.google.com/rss/search?q=NVIDIA%20OR%20Robot%20OR%20Humanoid%20OR%20Blackwell%20when:48h&hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News (AI Agents & Coding)", "url": "https://news.google.com/rss/search?q=Cursor%20AI%20OR%20AI%20Agent%20OR%20Devin%20OR%20Manus%20when:48h&hl=en-US&gl=US&ceid=US:en"}
        ]
        self.auditor = ScriptAuditorAgent(history_file="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/seen_scripts_global.json")
        self.writer = GlobalEnglishScriptWriterAgent(channel_name="@LidoAILab")

    async def run_cycle(self):
        print("\n" + "="*75)
        print(f"🌍 [SQUAD GLOBAL] BẮT ĐẦU CHU KỲ QUÉT TIN TOÀN CẦU (MỖI {INTERVAL_HOURS} TIẾNG)...")
        print("="*75)

        candidates = self.hunter.fetch_all_fresh_topics(limit_per_source=10)
        if not candidates:
            print("💤 [SQUAD GLOBAL] Không có tin tức mới đạt điểm cao trong chu kỳ này.")
            return

        selected_topic = None
        selected_script = None

        for topic in candidates:
            script_data = self.writer.generate_script_from_topic(topic)
            audit_res = self.auditor.audit_script(topic["title"], script_data)
            if audit_res["passed"]:
                print(f"🎯 [SQUAD GLOBAL] Đã chọn tin quốc tế hot nhất: '{topic['title']}' (Điểm: {topic['score']})")
                print(f"🧐 [SQUAD GLOBAL Auditor] {audit_res['reason']}")
                selected_topic = topic
                selected_script = script_data
                break
            else:
                print(f"⚠️ [SQUAD GLOBAL Auditor] Bỏ qua '{topic['title'][:40]}...': {audit_res['reason']}")

        if not selected_topic or not selected_script:
            print("💤 [SQUAD GLOBAL] Toàn bộ tin quét được chưa đạt chuẩn kiểm duyệt chéo.")
            return

        topic = selected_topic
        script_data = selected_script
        self.auditor.record_passed_script(topic["title"], script_data)

        today_str = datetime.now().strftime("%d/%m/%Y")
        src_clean = topic.get("source", "INTERNATIONAL MEDIA").upper()
        for sc in script_data["scenes"]:
            sc["source_label"] = f"{src_clean} • {today_str} (GLOBAL NEWS)"

        producer = StepFlowMediaProducerAgent()
        producer.voice = VOICE_EN
        uploader = YouTubeUploaderAgent()

        memorable_name = uploader.generate_memorable_filename(topic["title"], source=topic.get("source", "global_news"))
        final_video_path = os.path.join(producer.output_dir, f"global_{memorable_name}")

        temp_video = await producer.produce_step_animated_short(script_data, topic_info=topic)
        os.rename(temp_video, final_video_path)

        self.hunter.save_seen_title(topic["title"])

        guard = ChannelSecurityGuard("lido_ai_lab", os.path.join(os.path.dirname(__file__), "credentials"))
        guard.verify_channel_or_fail({"title": script_data["title"]})

        publisher = YouTubeDirectPublisher(token_path=str(guard.token_file))
        desc = (
            f"{script_data['title']}\n\n"
            f"Exclusive AI technology news from Lido AI Lab Global.\n"
            f"Source: {topic.get('source', 'International Media')} (Real-time updates).\n\n"
            f"👉 SUBSCRIBE TO LIDO AI LAB FOR DAILY AI BREAKTHROUGHS:\n"
            f"https://www.youtube.com/@LidoAILab\n\n"
            f"#LidoAILab #AI #Shorts #TechNews #ArtificialIntelligence #SiliconValley"
        )

        upload_res = publisher.upload_public_short(
            video_path=final_video_path,
            title=script_data["title"],
            description=desc,
            tags=["AI", "Shorts", "TechNews", "LidoAILab", "GlobalAI", "ArtificialIntelligence"]
        )

        notifier = NotificationAgent()
        if upload_res:
            yt_link = upload_res["shorts_url"]
            notifier.notify_user_for_review(f"[SQUAD GLOBAL] Video mới ĐÃ ĐĂNG: {yt_link}", final_video_path)
            print("\n" + "="*75)
            print(f"🎉 [SQUAD GLOBAL] ĐÃ ĐĂNG THÀNH CÔNG LÊN @LidoAILab!")
            print(f"🔗 Link Shorts: {yt_link}")
            print("="*75)

    async def start(self):
        print("🚀 [SQUAD GLOBAL] BIỆT ĐỘI AI TOÀN CẦU ĐÃ KHỞI CHẠY (QUÉT MỖI 2 TIẾNG)!")
        while True:
            try:
                await self.run_cycle()
            except Exception as e:
                print(f"⚠️ [SQUAD GLOBAL] Lỗi trong chu kỳ: {e}")
            print(f"\n⏳ [SQUAD GLOBAL] Nghỉ {INTERVAL_HOURS} tiếng trước chu kỳ quét tiếp theo...")
            await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    squad = SquadGlobalScheduler()
    asyncio.run(squad.start())
