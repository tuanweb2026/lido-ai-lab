import asyncio
import os
from agents.script_writer import TechnicalDeepDiveScriptWriterAgent
from agents.media_producer import RealPhotoMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.youtube_api_publisher import YouTubeDirectPublisher
from agents.notifier import NotificationAgent

async def regenerate_and_publish_perfect_short():
    print("==========================================================================")
    print("🚀 BẮT ĐẦU SẢN XUẤT VIDEO SỐNG ĐỘNG, NỘI DUNG RÕ RÀNG & ẢNH THẬT CHUẨN XÁC 100%")
    print("==========================================================================")

    topic = {
        "title": "Claude Opus 5.5 and OpenAI GPT-6 Sol & Luna both launch today with lower costs - 9to5Google",
        "source": "9to5Google",
        "keywords": ["claude", "gpt-6", "openai", "opus", "sol", "luna"]
    }

    writer = TechnicalDeepDiveScriptWriterAgent(channel_name="@LidoAILab")
    producer = RealPhotoMediaProducerAgent()
    uploader = YouTubeUploaderAgent()
    publisher = YouTubeDirectPublisher()
    notifier = NotificationAgent()

    script_data = writer.generate_script_from_topic(topic)
    print(f"📝 Tiêu đề mới cực rõ ràng: {script_data['title']}")

    memorable_name = uploader.generate_memorable_filename(topic["title"], source="perfect_v3_clear")
    final_video_path = os.path.join(producer.output_dir, memorable_name)

    temp_video = await producer.produce_real_photo_short(script_data["scenes"])
    if os.path.exists(final_video_path):
        os.remove(final_video_path)
    os.rename(temp_video, final_video_path)
    print(f"🎥 Đã render xong video với hình ảnh thật và nội dung chuẩn: {final_video_path}")

    desc = (
        f"{script_data['title']}\n\n"
        f"Bản tin phân tích công nghệ AI độc quyền từ Lido AI Lab.\n"
        f"Nguồn trích dẫn: 9to5Google & Thông cáo báo chí chính thức từ Anthropic & OpenAI.\n\n"
        f"👉 HÃY BẤM LIKE, SHARE VÀ ĐĂNG KÝ KÊNH LIDO AI LAB ĐỂ CẬP NHẬT CÔNG NGHỆ MỚI MỖI NGÀY:\n"
        f"https://www.youtube.com/@LidoAILab\n\n"
        f"#LidoAILab #Claude #GPT6 #OpenAI #Anthropic #Shorts #TechNews"
    )

    upload_res = publisher.upload_public_short(
        video_path=final_video_path,
        title=script_data["title"],
        description=desc,
        tags=["Claude Opus", "GPT-6", "OpenAI", "Anthropic", "Sol", "Luna", "Shorts", "LidoAILab"]
    )

    if upload_res:
        print("\n" + "="*70)
        print("🎉 UPLOAD THÀNH CÔNG VIDEO MỚI CHUẨN XÁC LÊN KÊNH @LidoAILab (PUBLIC)!")
        print(f"🔗 Link Shorts: {upload_res['shorts_url']}")
        print(f"🔗 Link Video:  {upload_res['watch_url']}")
        print("="*70)
        notifier.notify_user_for_review(f"Video mới với hình ảnh thật & nội dung rõ ràng đã lên YouTube!", final_video_path)

if __name__ == "__main__":
    asyncio.run(regenerate_and_publish_perfect_short())
