import asyncio
import os
import sys
import json
from datetime import datetime
from agents.script_writer import TechnicalDeepDiveScriptWriterAgent
from agents.step_flow_producer import StepFlowMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.youtube_api_publisher import YouTubeDirectPublisher
from channel_guard import ChannelSecurityGuard
from manage_bad_shorts import set_video_privacy

# Danh sách các video cũ cần làm lại lời thoại chuẩn và thay thế
TARGET_REPLACES = [
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
        "keywords": ["openai", "agent", "breach", "security"]
    },
    {
        "old_id": "c720mtkjRKc",
        "title": "Anthropic's Reported Supervoting Structure, an Opus 5.5 Field Note",
        "source": "FourWeekMBA",
        "keywords": ["anthropic", "opus", "supervoting", "model"]
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
    }
]

async def remanufacture_one(item, index, total):
    print("\n" + "="*75)
    print(f"🔄 [RE-PRODUCE & REPLACE] LÀM MỚI VIDEO {index}/{total}")
    print(f"📌 Chủ đề: {item['title']}")
    print(f"🎯 Video cũ cần thay thế: https://youtu.be/{item['old_id']}")
    print("="*75)

    writer = TechnicalDeepDiveScriptWriterAgent(channel_name="@LidoAILab")
    script_data = writer.generate_script_from_topic(item)

    print(f"🗣️ Lời thoại mới 1: {script_data['scenes'][0]['text']}")
    print(f"🗣️ Lời thoại mới 2: {script_data['scenes'][1]['text']}")

    today_str = datetime.now().strftime("%d/%m/%Y")
    src_clean = item.get("source", "BÁO CHÍ QUỐC TẾ").upper()
    for sc in script_data["scenes"]:
        sc["source_label"] = f"{src_clean} • {today_str} (BẢN MỚI)"

    producer = StepFlowMediaProducerAgent()
    uploader = YouTubeUploaderAgent()
    
    memorable_name = uploader.generate_memorable_filename(item["title"], source=item.get("source", "news"))
    final_video_path = os.path.join(producer.output_dir, f"remastered_{memorable_name}")

    temp_video = await producer.produce_step_animated_short(script_data, topic_info=item)
    os.rename(temp_video, final_video_path)

    # Kiểm tra rào chắn kênh
    guard = ChannelSecurityGuard("lido_ai_lab", os.path.join(os.path.dirname(__file__), "credentials"))
    guard.verify_channel_or_fail({"title": script_data["title"]})

    # Upload video mới lên YouTube công khai
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

    if upload_res:
        new_yt_link = upload_res["shorts_url"]
        print(f"🎉 ĐÃ ĐĂNG VIDEO MỚI CHUẨN THOẠI: {new_yt_link}")
        
        # Chuyển video cũ bị sai thoại về Private để không làm phiền khán giả
        try:
            ok, msg = set_video_privacy(item["old_id"], status="private")
            if ok:
                print(f"🔒 ĐÃ CHUYỂN VIDEO CŨ ({item['old_id']}) VỀ CHẾ ĐỘ PRIVATE AN TOÀN.")
            else:
                print(f"⚠️ Không thể ẩn video cũ: {msg}")
        except Exception as e:
            print(f"⚠️ Lỗi khi ẩn video cũ: {e}")

        return new_yt_link
    return None

async def main():
    print(f"🚀 BẮT ĐẦU QUY TRÌNH THAY THẾ DẦN DẦN {len(TARGET_REPLACES)} VIDEOS CŨ (CÁCH NHAU 15 PHÚT)...")
    for idx, item in enumerate(TARGET_REPLACES, 1):
        try:
            await remanufacture_one(item, idx, len(TARGET_REPLACES))
        except Exception as e:
            print(f"❌ Lỗi xử lý item {idx}: {e}")

        if idx < len(TARGET_REPLACES):
            print(f"\n⏳ Đợi 15 phút trước khi thay thế video tiếp theo ({idx+1}/{len(TARGET_REPLACES)})...")
            await asyncio.sleep(15 * 60)

if __name__ == "__main__":
    asyncio.run(main())
