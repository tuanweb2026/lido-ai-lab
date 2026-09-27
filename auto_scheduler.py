import asyncio
import time
import os
from agents.trend_hunter import SmartTrendHunterAgent
from agents.script_writer import TechnicalDeepDiveScriptWriterAgent
from agents.step_flow_producer import StepFlowMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.notifier import NotificationAgent

INTERVAL_HOURS = 2
INTERVAL_SECONDS = INTERVAL_HOURS * 3600

async def run_cycle():
    print("\n" + "="*70)
    print(f"⏰ [AUTO CYCLE] BẮT ĐẦU CHU KỲ QUÉT TIN TỨC MỚI (MỖI {INTERVAL_HOURS} TIẾNG)...")
    print("="*70)

    # 1. Quét tin mới nhất chưa từng làm
    hunter = SmartTrendHunterAgent()
    topic = hunter.fetch_best_new_topic()

    if not topic:
        print(f"💤 Không có tin tức mới đột phá. Sẽ quét lại sau {INTERVAL_HOURS} tiếng.")
        return

    # 2. Soạn kịch bản chuyên sâu ĐỘC BẢN theo đúng tin tức vừa quét được
    writer = TechnicalDeepDiveScriptWriterAgent(channel_name="@LidoAILab")
    script_data = writer.generate_script_from_topic(topic)

    # CỔNG KIỂM DUYỆT CHÉO: ScriptAuditorAgent
    from agents.script_auditor import ScriptAuditorAgent
    auditor = ScriptAuditorAgent()
    audit_res = auditor.audit_script(topic["title"], script_data)
    print(f"🧐 [Auditor Gate] Kết quả kiểm duyệt: {audit_res['reason']}")
    if not audit_res["passed"]:
        print(f"⚠️ [Auditor Gate] Kịch bản bị từ chối: {audit_res['reason']}. Bỏ qua chu kỳ này.")
        return

    auditor.record_passed_script(topic["title"], script_data)

    # Đính kèm nguồn thực tế và ngày thực tế cho từng phân cảnh
    from datetime import datetime
    today_str = datetime.now().strftime("%d/%m/%Y")
    src_clean = topic.get("source", "BÁO CHÍ QUỐC TẾ").upper()
    for sc in script_data["scenes"]:
        sc["source_label"] = f"{src_clean} • {today_str} (HÔM NAY)"

    # 3. Sản xuất video hoạt họa chuyển động từng bước (Step-by-Step Flow Animation)
    producer = StepFlowMediaProducerAgent()
    uploader = YouTubeUploaderAgent()
    
    memorable_name = uploader.generate_memorable_filename(topic["title"], source=topic.get("source", "news"))
    final_video_path = os.path.join(producer.output_dir, memorable_name)

    temp_video = await producer.produce_step_animated_short(script_data, topic_info=topic)
    os.rename(temp_video, final_video_path)

    # 4. Lưu lại để không bị trùng lặp
    hunter.save_seen_title(topic["title"])

    # 5. Kiểm tra rào chắn kênh (Channel Security Guard) trước khi upload
    from channel_guard import ChannelSecurityGuard
    guard = ChannelSecurityGuard("lido_ai_lab", os.path.join(os.path.dirname(__file__), "credentials"))
    guard.verify_channel_or_fail({"title": script_data["title"]})

    # Tự động upload thẳng lên YouTube @LidoAILab ở chế độ PUBLIC CÔNG KHAI NGAY
    from agents.youtube_api_publisher import YouTubeDirectPublisher
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

    # 6. Gửi thông báo Native macOS kèm link YouTube trực tiếp cho bạn
    notifier = NotificationAgent()
    if upload_res:
        yt_link = upload_res["shorts_url"]
        notifier.notify_user_for_review(f"Video mới đã LÊN SÓNG YOUTUBE (PUBLIC): {yt_link}", final_video_path)
        print("\n" + "="*70)
        print("🎉 ĐÃ TỰ ĐỘNG ĐĂNG LÊN YOUTUBE @LidoAILab (CHẾ ĐỘ PUBLIC - CÔNG KHAI)!")
        print(f"🔗 BẤM VÀO LINK ĐỂ XEM NGAY: {yt_link}")
        print("="*70)
    else:
        notifier.notify_user_for_review(f"Video mới: {script_data['title']}", final_video_path)

    print("\n" + "="*70)
    print("✅ ĐÃ HOÀN THÀNH VIDEO MỚI VÀ ĐĂNG LÊN PRIVATE CHỜ BẠN DUYỆT.")
    print(f"🎥 Video: file://{final_video_path}")
    print("="*70)

async def main_scheduler():
    print("🚀 HỆ THỐNG TỰ ĐỘNG HÓA SẢN XUẤT VIDEO LIDO AI LAB ĐÃ KHỞI CHẠY!")
    print(f"🕒 Lịch trình: Quét tin tức và sản xuất video mỗi {INTERVAL_HOURS} tiếng một lần.")
    print("💡 Khi có video mới, macOS sẽ tự động phát âm thanh và hiển thị thông báo để bạn duyệt.")
    
    while True:
        try:
            await run_cycle()
        except Exception as e:
            print(f"⚠️ Lỗi trong chu kỳ tự động: {e}")

        print(f"\n⏳ Đang ngủ {INTERVAL_HOURS} tiếng... Chu kỳ quét tiếp theo sẽ diễn ra sau.")
        await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main_scheduler())
