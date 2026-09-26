import asyncio
import os
import time
from agents.script_writer import TechnicalDeepDiveScriptWriterAgent
from agents.media_producer import RealPhotoMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.youtube_api_publisher import YouTubeDirectPublisher
from agents.notifier import NotificationAgent

TOP_5_TOPICS = [
    {
        "rank": 1,
        "title": "DeepSeek is joining OpenAI and Anthropic at the UN Security Council to discuss AI risks - qz.com",
        "source": "QZ News",
        "keywords": ["deepseek", "openai", "anthropic", "un", "security council"]
    },
    {
        "rank": 2,
        "title": "Anthropic is setting up a biology lab where Claude guides robots through drug experiments - the-decoder.com",
        "source": "The Decoder",
        "keywords": ["anthropic", "claude", "robot", "drug", "biology"]
    },
    {
        "rank": 3,
        "title": "XPENG's Iron Humanoid Robot Walked Out Immediately After Being Assembled - Engadget",
        "source": "Engadget",
        "keywords": ["xpeng", "iron", "robot", "humanoid"]
    },
    {
        "rank": 4,
        "title": "Accelerating a ROS 2 Node with an AI Agent and NVIDIA Isaac ROS - developer.nvidia.com",
        "source": "NVIDIA Developer",
        "keywords": ["nvidia", "isaac", "ros", "agent"]
    },
    {
        "rank": 5,
        "title": "Runway & Minimax Launch Physical Motion Simulation Benchmark for Video AI - Tech Radar",
        "source": "Tech Radar",
        "keywords": ["runway", "minimax", "video", "motion"]
    }
]

async def produce_and_upload_top5():
    print("==========================================================================")
    print("🚀 BẮT ĐẦU SẢN XUẤT VÀ TẢI LÊN TOP 5 TIN TỨC AI NÓNG NHẤT CHO KÊNH @LidoAILab")
    print("==========================================================================")

    writer = TechnicalDeepDiveScriptWriterAgent(channel_name="@LidoAILab")
    producer = RealPhotoMediaProducerAgent()
    uploader = YouTubeUploaderAgent()
    publisher = YouTubeDirectPublisher()
    notifier = NotificationAgent()

    results = []

    for idx, topic in enumerate(TOP_5_TOPICS, 1):
        print("\n" + "="*70)
        print(f"🎬 [TIẾN TRÌNH {idx}/5] ĐANG XỬ LÝ: {topic['title']}")
        print("="*70)

        # 1. Soạn kịch bản độc bản
        script_data = writer.generate_script_from_topic(topic)
        print(f"📝 Tiêu đề: {script_data['title']}")

        # 2. Tạo tên file ngữ nghĩa & render video
        memorable_name = uploader.generate_memorable_filename(topic["title"], source=topic.get("source", "news"))
        final_video_path = os.path.join(producer.output_dir, memorable_name)

        temp_video = await producer.produce_real_photo_short(script_data["scenes"])
        if os.path.exists(final_video_path):
            os.remove(final_video_path)
        os.rename(temp_video, final_video_path)
        print(f"🎥 Đã render xong video: {final_video_path}")

        # 3. Tải lên YouTube @LidoAILab ở chế độ Private
        desc = (
            f"{script_data['title']}\n\n"
            f"Bản tin công nghệ AI độc quyền từ Lido AI Lab.\n"
            f"Nguồn trích dẫn: {topic['source']} (Cập nhật thời gian thực).\n\n"
            f"👉 HÃY BẤM LIKE, SHARE VÀ ĐĂNG KÝ KÊNH LIDO AI LAB ĐỂ THEO DÕI XU HƯỚNG MỚI MỖI NGÀY:\n"
            f"https://www.youtube.com/@LidoAILab\n\n"
            f"#LidoAILab #AI #Shorts #TechNews #ArtificialIntelligence"
        )

        upload_res = publisher.upload_private_short(
            video_path=final_video_path,
            title=script_data["title"],
            description=desc,
            tags=["Shorts", "AI", "Technology", "LidoAILab", "TechNews"]
        )

        if upload_res:
            results.append({
                "rank": topic["rank"],
                "title": script_data["title"],
                "video_id": upload_res["video_id"],
                "shorts_url": upload_res["shorts_url"],
                "watch_url": upload_res["watch_url"]
            })
            print(f"🎉 Upload thành công: {upload_res['shorts_url']}")
        
        # Nghỉ nhẹ 3s giữa các video
        await asyncio.sleep(3)

    print("\n" + "="*70)
    print(f"🎉 HOÀN THÀNH TẤT CẢ {len(results)}/5 VIDEO TOP NÓNG!")
    for r in results:
        print(f"\n{r['rank']}. {r['title']}")
        print(f"   👉 Shorts: {r['shorts_url']}")
        print(f"   👉 Watch:  {r['watch_url']}")
    print("="*70)

    # Gửi thông báo macOS
    notifier.notify_user_for_review(f"Đã xuất bản xong Top 5 Video AI Mới Lên YouTube!", producer.output_dir)

if __name__ == "__main__":
    asyncio.run(produce_and_upload_top5())
