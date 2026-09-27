import asyncio
import time
import os
import sys
from datetime import datetime
from agents.trend_hunter import SmartTrendHunterAgent
from agents.script_writer import TechnicalDeepDiveScriptWriterAgent
from agents.step_flow_producer import StepFlowMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.youtube_api_publisher import YouTubeDirectPublisher
from agents.notifier import NotificationAgent
from channel_guard import ChannelSecurityGuard

INTERVAL_MINUTES = 15
INTERVAL_SECONDS = INTERVAL_MINUTES * 60
TOTAL_VIDEOS_TARGET = 6

async def produce_and_publish_one(topic, video_index, total_target=6):
    print("\n" + "="*75)
    print(f"🎬 [BATCH WORKFLOW] BẮT ĐẦU SẢN XUẤT VIDEO {video_index}/{total_target}")
    print(f"📌 Chủ đề: {topic['title']}")
    print(f"⭐ Điểm hot: {topic.get('score', 1)} | Nguồn: {topic.get('source', 'News')}")
    print("="*75)

    # 1. Soạn kịch bản chuyên sâu
    writer = TechnicalDeepDiveScriptWriterAgent(channel_name="@LidoAILab")
    script_data = writer.generate_script_from_topic(topic)

    # Đính kèm nguồn thực tế và ngày thực tế cho từng phân cảnh
    today_str = datetime.now().strftime("%d/%m/%Y")
    src_clean = topic.get("source", "BÁO CHÍ QUỐC TẾ").upper()
    for sc in script_data["scenes"]:
        sc["source_label"] = f"{src_clean} • {today_str} (HÔM NAY)"

    # 2. Dựng hoạt họa quy trình kỹ thuật chuyển động & terminal gõ code
    producer = StepFlowMediaProducerAgent()
    uploader = YouTubeUploaderAgent()
    
    memorable_name = uploader.generate_memorable_filename(topic["title"], source=topic.get("source", "news"))
    final_video_path = os.path.join(producer.output_dir, memorable_name)

    temp_video = await producer.produce_step_animated_short(script_data, topic_info=topic)
    os.rename(temp_video, final_video_path)

    # 3. Lưu vào lịch sử để chống trùng lặp vĩnh viễn
    hunter = SmartTrendHunterAgent()
    hunter.save_seen_title(topic["title"])

    # 4. Kiểm tra rào chắn kênh (Channel Guard)
    guard = ChannelSecurityGuard("lido_ai_lab", os.path.join(os.path.dirname(__file__), "credentials"))
    guard.verify_channel_or_fail({"title": script_data["title"]})

    # 5. Xuất bản công khai lên YouTube @LidoAILab
    publisher = YouTubeDirectPublisher(token_path=str(guard.token_file))
    desc = (
        f"{script_data['title']}\n\n"
        f"Bản tin công nghệ AI độc quyền từ Lido AI Lab.\n"
        f"Nguồn trích dẫn: {topic.get('source', 'International Media')} (Cập nhật thời gian thực).\n\n"
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
        yt_link = upload_res["shorts_url"]
        notifier.notify_user_for_review(f"Video {video_index}/{total_target} ĐÃ ĐĂNG YOUTUBE: {yt_link}", final_video_path)
        print("\n" + "="*75)
        print(f"🎉 ĐÃ ĐĂNG THÀNH CÔNG VIDEO {video_index}/{total_target} LÊN @LidoAILab!")
        print(f"🔗 Link Shorts xem ngay: {yt_link}")
        print("="*75)
        return yt_link
    else:
        notifier.notify_user_for_review(f"Video {video_index}/{total_target}: {script_data['title']}", final_video_path)
        return None

async def run_batch_schedule():
    print("="*75)
    print(f"🚀 KHỞI ĐỘNG KẾ HOẠCH SẢN XUẤT & ĐĂNG 6 TIN TỨC ĐỈNH CAO")
    print(f"⏱️ Khoảng cách giữa mỗi lần đăng: {INTERVAL_MINUTES} phút")
    print("="*75)

    hunter = SmartTrendHunterAgent()
    candidates = hunter.fetch_all_fresh_topics(limit_per_source=10)

    if len(candidates) < TOTAL_VIDEOS_TARGET:
        print(f"⚠️ Chỉ tìm thấy {len(candidates)} tin mới. Sẽ dùng toàn bộ tin tìm được.")
        selected_topics = candidates
    else:
        selected_topics = candidates[:TOTAL_VIDEOS_TARGET]

    print(f"\n📋 DANH SÁCH 6 TIN TỨC ĐƯỢC CHỌN:")
    for idx, t in enumerate(selected_topics, 1):
        print(f"  {idx}. [{t['score']}đ] {t['title']} ({t['source']})")

    published_links = []
    for i, topic in enumerate(selected_topics, 1):
        try:
            yt_link = await produce_and_publish_one(topic, video_index=i, total_target=len(selected_topics))
            if yt_link:
                published_links.append((topic['title'], yt_link))
        except Exception as e:
            print(f"❌ Lỗi khi sản xuất/đăng video {i}: {e}")

        if i < len(selected_topics):
            print(f"\n⏳ Đang đợi {INTERVAL_MINUTES} phút trước khi đăng video tiếp theo ({i+1}/{len(selected_topics)})...")
            await asyncio.sleep(INTERVAL_SECONDS)

    print("\n" + "="*75)
    print(f"🏆 ĐÃ HOÀN THÀNH TOÀN BỘ CHIẾN DỊCH {len(published_links)}/{TOTAL_VIDEOS_TARGET} VIDEOS!")
    for idx, (title, link) in enumerate(published_links, 1):
        print(f"  {idx}. {link} - {title}")
    print("="*75)

    # Sau khi kết thúc 6 bài, khởi động lại auto_scheduler chu kỳ 2 tiếng như thường lệ
    print("\n🔄 Tái kích hoạt auto_scheduler chạy định kỳ mỗi 2 tiếng...")
    from auto_scheduler import main_scheduler
    await main_scheduler()

if __name__ == "__main__":
    asyncio.run(run_batch_schedule())
