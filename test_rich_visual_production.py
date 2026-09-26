import asyncio
import os
from agents.script_writer import TechnicalDeepDiveScriptWriterAgent
from agents.media_producer import RealPhotoMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.youtube_api_publisher import YouTubeDirectPublisher
from agents.notifier import NotificationAgent

async def produce_single_rich_visual_video():
    print("==========================================================================")
    print("🚀 BẮT ĐẦU SẢN XUẤT VIDEO MẪU VỚI AGENT 5 (VISUAL ASSET SCOUT) SĂN ẢNH ĐA DẠNG")
    print("==========================================================================")

    topic = {
        "title": "XPENG's Iron Humanoid Robot Walked Out Immediately After Being Assembled - Engadget",
        "source": "Engadget",
        "keywords": ["xpeng", "iron", "robot", "humanoid"]
    }

    writer = TechnicalDeepDiveScriptWriterAgent(channel_name="@LidoAILab")
    producer = RealPhotoMediaProducerAgent()
    uploader = YouTubeUploaderAgent()
    publisher = YouTubeDirectPublisher()
    notifier = NotificationAgent()

    script_data = writer.generate_script_from_topic(topic)
    print(f"📝 Tiêu đề: {script_data['title']}")

    memorable_name = uploader.generate_memorable_filename(topic["title"], source="engadget_hd_visual")
    final_video_path = os.path.join(producer.output_dir, memorable_name)

    temp_video = await producer.produce_real_photo_short(script_data["scenes"])
    if os.path.exists(final_video_path):
        os.remove(final_video_path)
    os.rename(temp_video, final_video_path)
    print(f"🎥 Đã render xong video với hình ảnh mới: {final_video_path}")

    desc = (
        f"{script_data['title']}\n\n"
        f"Bản tin công nghệ AI & Robotics độc quyền từ Lido AI Lab.\n"
        f"Nguồn trích dẫn: Engadget (Cập nhật hình ảnh thực tế từ hiện trường).\n\n"
        f"👉 HÃY BẤM LIKE, SHARE VÀ ĐĂNG KÝ KÊNH LIDO AI LAB ĐỂ THEO DÕI XU HƯỚNG MỚI MỖI NGÀY:\n"
        f"https://www.youtube.com/@LidoAILab\n\n"
        f"#LidoAILab #XPENG #Robot #Shorts #TechNews #Robotics #Iron"
    )

    upload_res = publisher.upload_private_short(
        video_path=final_video_path,
        title=script_data["title"],
        description=desc,
        tags=["XPENG", "Robot", "Iron", "Robotics", "Shorts", "LidoAILab"]
    )

    if upload_res:
        print("\n" + "="*70)
        print("🎉 UPLOAD THÀNH CÔNG VIDEO HÌNH ẢNH MỚI LÊN KÊNH @LidoAILab (PRIVATE)!")
        print(f"🔗 Link Shorts: {upload_res['shorts_url']}")
        print(f"🔗 Link Video:  {upload_res['watch_url']}")
        print("="*70)
        notifier.notify_user_for_review(f"Video hình ảnh phong phú mới đã lên YouTube!", final_video_path)

if __name__ == "__main__":
    asyncio.run(produce_single_rich_visual_video())
