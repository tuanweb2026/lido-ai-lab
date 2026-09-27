import asyncio
import os
import sys
import json
import time
from datetime import datetime
from agents.script_writer import TechnicalDeepDiveScriptWriterAgent
from agents.script_auditor import ScriptAuditorAgent
from agents.step_flow_producer import StepFlowMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.youtube_api_publisher import YouTubeDirectPublisher
from agents.notifier import NotificationAgent
from channel_guard import ChannelSecurityGuard
from manage_bad_shorts import set_video_privacy

INTERVAL_MINUTES = 15
INTERVAL_SECONDS = INTERVAL_MINUTES * 60

# DANH SÁCH TOÀN BỘ 14 VIDEO CŨ CẦN THAY THẾ (ĐÃ ĐƯỢC CHUẨN HÓA KỊCH BẢN ĐỘC BẢN)
ALL_14_TARGETS = [
    {
        "old_id": "i9tkTMCNQbs",
        "title": "Check is your OpenAI GPT-6-Astra nerfed?",
        "source": "HackerNews Trending AI",
        "keywords": ["openai", "gpt-6", "astra", "nerfed"]
    },
    {
        "old_id": "40jcFEAHmZo",
        "title": "The Claude Sonnet 5.5 leak beating GPT-6 Sol is not what it looks like",
        "source": "Startup Fortune",
        "keywords": ["claude", "sonnet", "gpt-6", "leak"]
    },
    {
        "old_id": "wiPAqScL6bw",
        "title": "The Notice Had Nowhere to Land: The OpenAI Agent Breach in Australia",
        "source": "HackerNews",
        "keywords": ["openai", "agent", "breach", "australia"]
    },
    {
        "old_id": "c720mtkjRKc",
        "title": "Anthropic's Reported Supervoting Structure, an Opus 5.5 Field Note",
        "source": "FourWeekMBA",
        "keywords": ["anthropic", "opus", "supervoting", "governance"]
    },
    {
        "old_id": "sBl-egrvgTI",
        "title": "OpenAI rogue agents leaked 53 ChatGPT user images",
        "source": "Fortune",
        "keywords": ["openai", "rogue agent", "leak", "chatgpt"]
    },
    {
        "old_id": "g8s7ejfpesA",
        "title": "Tesla workers balk at training Optimus humanoid robots as replacements",
        "source": "Ars Technica",
        "keywords": ["tesla", "optimus", "humanoid robot", "factory"]
    },
    {
        "old_id": "n7K6fwBUy8c",
        "title": "Agility Robotics, maker of Digit humanoid, exploring wheeled robots",
        "source": "The Robot Report",
        "keywords": ["agility", "digit", "wheeled robot", "humanoid"]
    },
    {
        "old_id": "gkg5u8B5OGk",
        "title": "Omneky Brings Premier Agentic Harness for Advertising and GTM to ChatGPT",
        "source": "MarTech Cube",
        "keywords": ["omneky", "advertising", "agentic", "chatgpt"]
    },
    {
        "old_id": "WqQjum70OYk",
        "title": "ChatGPT or Claude? For just $40, you can ask them both (and many others)",
        "source": "Mashable",
        "keywords": ["chatgpt", "claude", "$40", "subscription"]
    },
    {
        "old_id": "QnmldvVFw2c",
        "title": "Ando wants to take on Slack with a team messaging app that lets humans and agents work together",
        "source": "TechCrunch AI",
        "keywords": ["ando", "slack", "messaging", "agent"]
    },
    {
        "old_id": "wuORQWHwD9I",
        "title": "With AMD Ryzen AI Max Series Processors, Perplexity Brings Portable Computer to Agentic PCs",
        "source": "newsroom.amd.com",
        "keywords": ["amd", "ryzen", "perplexity", "agentic pc"]
    },
    {
        "old_id": "sixWPMP9hYE",
        "title": "This Open Source Software Fixes Herky-Jerky Humanoid Robots, Kind Of By Copying Humans",
        "source": "Forbes",
        "keywords": ["open source", "herky-jerky", "humanoid robot", "copying humans"]
    },
    {
        "old_id": "ui0LOfPsx40",
        "title": "With AMD Ryzen AI Max Series Processors, Perplexity Brings Portable Computer to Agentic PCs (Tech Note)",
        "source": "AMD",
        "keywords": ["amd", "ryzen ai max", "perplexity", "hardware"]
    },
    {
        "old_id": "GNLiK95MMoE",
        "title": "How to Customize Your AI Tools, From ChatGPT to Gemini and Claude",
        "source": "CNET",
        "keywords": ["customize", "chatgpt", "gemini", "claude"]
    }
]

async def remanufacture_and_upload(item, index, total):
    print("\n" + "="*80)
    print(f"🔄 [REMASTER & REPLACE] ĐANG XỬ LÝ VIDEO {index}/{total}")
    print(f"📌 Tiêu đề: {item['title']}")
    print(f"🎯 Video cũ (Đã ẩn): https://youtu.be/{item['old_id']}")
    print("="*80)

    # 1. Soạn thảo kịch bản
    writer = TechnicalDeepDiveScriptWriterAgent(channel_name="@LidoAILab")
    script_data = writer.generate_script_from_topic(item)

    # 2. CỔNG KIỂM DUYỆT CHÉO: ScriptAuditorAgent
    auditor = ScriptAuditorAgent()
    audit_res = auditor.audit_script(item["title"], script_data)
    print(f"🧐 [Auditor Gate] Kết quả kiểm duyệt: {audit_res['reason']}")
    if not audit_res["passed"]:
        print(f"❌ [Auditor Gate] Kịch bản bị từ chối: {audit_res['reason']}")
        return None

    # Đánh dấu kịch bản đã qua duyệt vào kho lưu trữ
    auditor.record_passed_script(item["title"], script_data)

    print(f"🗣️ Lời thoại mới 1: {script_data['scenes'][0]['text']}")
    print(f"🗣️ Lời thoại mới 2: {script_data['scenes'][1]['text']}")

    today_str = datetime.now().strftime("%d/%m/%Y")
    src_clean = item.get("source", "BÁO CHÍ QUỐC TẾ").upper()
    for sc in script_data["scenes"]:
        sc["source_label"] = f"{src_clean} • {today_str} (REMASTERED)"

    # 3. Sản xuất đồ họa chuyển động & Terminal
    producer = StepFlowMediaProducerAgent()
    uploader = YouTubeUploaderAgent()
    
    memorable_name = uploader.generate_memorable_filename(item["title"], source=item.get("source", "news"))
    final_video_path = os.path.join(producer.output_dir, f"remastered_{memorable_name}")

    temp_video = await producer.produce_step_animated_short(script_data, topic_info=item)
    os.rename(temp_video, final_video_path)

    # 4. Bảo vệ kênh
    guard = ChannelSecurityGuard("lido_ai_lab", os.path.join(os.path.dirname(__file__), "credentials"))
    guard.verify_channel_or_fail({"title": script_data["title"]})

    # 5. Xuất bản lên YouTube (Public)
    publisher = YouTubeDirectPublisher(token_path=str(guard.token_file))
    desc = (
        f"{script_data['title']}\n\n"
        f"Bản tin công nghệ AI độc quyền từ Lido AI Lab (Bản nâng cấp chất lượng cao).\n"
        f"Nguồn trích dẫn: {item.get('source', 'International Media')} (Cập nhật thời gian thực).\n\n"
        f"👉 HÃY BẤM LIKE, SHARE VÀ ĐĂNG KÝ KÊNH LIDO AI LAB ĐỂ THEO DÕI XU HƯỚNG MỚI MỖI NGÀY:\n"
        f"https://www.youtube.com/@LidoAILab\n\n"
        f"#LidoAILab #AI #Shorts #TechNews #ArtificialIntelligence"
    )

    upload_res = publisher.upload_public_short(
        video_path=final_video_path,
        title=script_data["title"],
        description=desc,
        tags=["Shorts", "AI", "Technology", "LidoAILab", "TechNews"]
    )

    notifier = NotificationAgent()
    if upload_res:
        new_yt_link = upload_res["shorts_url"]
        print("\n" + "="*80)
        print(f"🎉 ĐÃ ĐĂNG THÀNH CÔNG VIDEO {index}/{total} LÊN @LidoAILab!")
        print(f"🔗 Link Shorts mới: {new_yt_link}")
        print("="*80)

        # Chuyển video cũ về Private (phòng hờ)
        try:
            set_video_privacy(item["old_id"], status="private")
        except Exception:
            pass

        notifier.notify_user_for_review(f"Video mới {index}/{total} ĐÃ ĐĂNG: {new_yt_link}", final_video_path)
        return new_yt_link
    return None

async def main():
    print("="*80)
    print(f"🚀 KHỞI ĐỘNG TIẾN TRÌNH SẢN XUẤT & ĐĂNG 14 VIDEO REMASTERED")
    print(f"⏱️ Khoảng cách an toàn giữa mỗi lần đăng: {INTERVAL_MINUTES} phút")
    print("="*80)

    for idx, item in enumerate(ALL_14_TARGETS, 1):
        try:
            yt_link = await remanufacture_and_upload(item, idx, len(ALL_14_TARGETS))
        except Exception as e:
            print(f"❌ Lỗi xử lý video {idx}: {e}")

        if idx < len(ALL_14_TARGETS):
            print(f"\n⏳ Đợi {INTERVAL_MINUTES} phút trước khi đăng video tiếp theo ({idx+1}/{len(ALL_14_TARGETS)})...")
            await asyncio.sleep(INTERVAL_SECONDS)

    print("\n" + "="*80)
    print(f"🏆 ĐÃ HOÀN TẤT TOÀN BỘ 14 VIDEO NÂNG CẤP!")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
