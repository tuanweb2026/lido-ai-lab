import asyncio
import os
from agents.script_writer import TechnicalDeepDiveScriptWriterAgent
from agents.media_producer import RealPhotoMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.youtube_api_publisher import YouTubeDirectPublisher
from agents.notifier import NotificationAgent

async def produce_breakthrough_non_repeated_short():
    print("==========================================================================")
    print("🚀 BẮT ĐẦU SẢN XUẤT VIDEO CHỦ ĐỀ MỚI TINH (ROBOT ĐẤU VÕ ĐÀI LỒNG SẮT - NBC NEWS)")
    print("   VỚI AGENT 5 SĂN ẢNH THẬT ĐỘC QUYỀN MỚI 100%, KHÔNG TRÙNG ẢNH CŨ!")
    print("==========================================================================")

    topic = {
        "title": "Man versus Robot: Influencer takes on humanoid robot in cage match - NBC News",
        "source": "NBC News",
        "keywords": ["humanoid robot", "robot", "cage match", "influencer"]
    }

    writer = TechnicalDeepDiveScriptWriterAgent(channel_name="@LidoAILab")
    producer = RealPhotoMediaProducerAgent()
    uploader = YouTubeUploaderAgent()
    publisher = YouTubeDirectPublisher()
    notifier = NotificationAgent()

    script_data = writer.generate_script_from_topic(topic)
    print(f"📝 Tiêu đề mới toanh: {script_data['title']}")

    memorable_name = uploader.generate_memorable_filename(topic["title"], source="nbc_robot_fight_unique")
    final_video_path = os.path.join(producer.output_dir, memorable_name)

    temp_video = await producer.produce_real_photo_short(script_data["scenes"])
    if os.path.exists(final_video_path):
        os.remove(final_video_path)
    os.rename(temp_video, final_video_path)
    print(f"🎥 Đã render xong video với 5 ảnh mới toanh: {final_video_path}")

    desc = (
        f"{script_data['title']}\n\n"
        f"Bản tin công nghệ và Robotics độc quyền từ Lido AI Lab.\n"
        f"Nguồn trích dẫn: NBC News (Trận chiến lồng sắt giữa con người và robot tự hành).\n\n"
        f"👉 HÃY BẤM LIKE, SHARE VÀ ĐĂNG KÝ KÊNH LIDO AI LAB ĐỂ THEO DÕI XU HƯỚNG MỚI MỖI NGÀY:\n"
        f"https://www.youtube.com/@LidoAILab\n\n"
        f"#LidoAILab #Robot #HumanoidRobot #NBCNews #Shorts #TechNews #Robotics"
    )

    upload_res = publisher.upload_public_short(
        video_path=final_video_path,
        title=script_data["title"],
        description=desc,
        tags=["Robot", "Humanoid Robot", "NBC News", "Cage match", "Robotics", "Shorts", "LidoAILab"]
    )

    if upload_res:
        print("\n" + "="*70)
        print("🎉 UPLOAD THÀNH CÔNG VIDEO CHỦ ĐỀ MỚI TINH LÊN KÊNH @LidoAILab (PUBLIC)!")
        print(f"🔗 Link Shorts: {upload_res['shorts_url']}")
        print(f"🔗 Link Video:  {upload_res['watch_url']}")
        print("="*70)
        notifier.notify_user_for_review(f"Video mới tinh (Robot đấu võ đài) đã lên sóng YouTube!", final_video_path)

if __name__ == "__main__":
    asyncio.run(produce_breakthrough_non_repeated_short())
