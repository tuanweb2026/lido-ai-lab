import asyncio
import os
from agents.media_producer import RealPhotoMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.notifier import NotificationAgent

async def run_60s_epic_short():
    print("==========================================================================")
    print("🎬 SẢN XUẤT SIÊU PHẨM SHORTS DÀI 60-70 GIÂY: CUỐN HÚT, KỊCH TÍNH TỪNG GIÂY")
    print("==========================================================================")

    source_tag = "NBC NEWS • 20/09/2026 (XUẤT BẢN HÔM NAY)"

    scenes = [
        {
            "scene_id": 1,
            "image_file": "epic_1_white_house.jpg",
            "source_label": source_tag,
            "headline": "MỸ SẮP LẬP 'QUÂN CHỦNG AI'?",
            "metric_badge": "TUYÊN BỐ GÂY CHẤN ĐỘNG",
            "text": "Liệu nước Mỹ có đang chuẩn bị thành lập một Quân Chủng AI độc lập... tương tự như Lực Lượng Không Gian Space Force cách đây vài năm? Tuyên bố gây chấn động vừa được phát đi sáng nay!",
            "overlay_data": "KẾ HOẠCH LẬP 'AI FORCE'"
        },
        {
            "scene_id": 2,
            "image_file": "epic_2_war_room.jpg",
            "source_label": source_tag,
            "headline": "BỔ NHIỆM 'TỔNG TƯ LỆNH AI'",
            "metric_badge": "ĐỘC QUYỀN TỪ NBC NEWS",
            "text": "Theo báo cáo độc quyền từ đài NBC News hôm nay: Giới chức cấp cao cam kết sẽ bổ nhiệm một Tổng chỉ huy AI, còn gọi là AI Czar, nắm giữ toàn quyền giám sát các siêu mô hình đang phát triển vượt tầm kiểm soát!",
            "overlay_data": "BỔ NHIỆM TỔNG CHỈ HUY AI CZAR"
        },
        {
            "scene_id": 3,
            "image_file": "epic_3_cyber_grid.jpg",
            "source_label": source_tag,
            "headline": "VÌ SAO LẠI LÀ NGAY BÂY GIỜ?",
            "metric_badge": "MỐI ĐE DỌA AN NINH QUỐC GIA",
            "text": "Tại sao lại là lúc này? Bởi vì chỉ trong vài tuần qua, hàng loạt vụ việc AI tự động tìm ra lỗ hổng bảo mật, tự bẻ khóa mật khẩu và qua mặt các bức tường lửa phòng thủ đã khiến Lầu Năm Góc phải giật mình thức tỉnh!",
            "overlay_data": "NGUY CƠ MẤT KIỂM SOÁT AGI"
        },
        {
            "scene_id": 4,
            "image_file": "epic_4_datacenter_racks.jpg",
            "source_label": source_tag,
            "headline": "CUỘC ĐUA VŨ TRANG THUẬT TOÁN",
            "metric_badge": "SIÊU MÁY TÍNH QUÂN SỰ",
            "text": "Cuộc chiến tương lai không còn nằm ở súng đạn hay xe tăng truyền thống. Nó đang diễn ra bên trong những trung tâm dữ liệu khổng lồ, nơi hàng triệu dòng code tự học đang điều phối toàn bộ hệ thống phòng thủ!",
            "overlay_data": "THUẬT TOÁN LÀ VŨ KHÍ TỐI THƯỢNG"
        },
        {
            "scene_id": 5,
            "image_file": "epic_5_robot_combat.jpg",
            "source_label": source_tag,
            "headline": "RANH GIỚI MONG MANH",
            "metric_badge": "CÂU HỎI ĐẠO ĐỨC CÔNG NGHỆ",
            "text": "Câu hỏi lớn nhất đặt ra lúc này là: Liệu con người có nên trao quyền đưa ra quyết định sinh tử cho một hệ thống trí tuệ nhân tạo tự hành trong chiến tranh hay không?",
            "overlay_data": "CON NGƯỜI vs AI TỰ HÀNH"
        },
        {
            "scene_id": 6,
            "image_file": "epic_6_future_tech.jpg",
            "source_label": source_tag,
            "headline": "THEO DÕI LIDO AI LAB",
            "metric_badge": "BÌNH LUẬN GÓC NHÌN CỦA BẠN",
            "text": "Bạn nghĩ Quân Chủng AI có thực sự cần thiết? Hãy để lại ý kiến của bạn bên dưới và Đăng ký kênh Lido AI Lab để không bỏ lỡ những biến chuyển công nghệ lớn nhất thời đại!",
            "overlay_data": "SUBSCRIBE: YOUTUBE.COM/@LidoAILab"
        }
    ]

    title = "MỸ SẮP THÀNH LẬP 'QUÂN CHỦNG AI' VÀ BỔ NHIỆM TỔNG TƯ LỆNH AI? 🇺🇸🚨 #Shorts #AIForce #Tech"

    producer = RealPhotoMediaProducerAgent()
    out_video_path = os.path.join(producer.output_dir, "lido_ai_epic_65s_short.mp4")

    # Render video
    video_f = await producer.produce_real_photo_short(scenes)
    os.rename(video_f, out_video_path)

    # Metadata
    metadata = {
        "title": title,
        "source": "NBC News & AZ Family",
        "published_date": "Sunday, 20 Sep 2026",
        "video_file": out_video_path,
        "duration": "Khoảng 65 giây",
        "description": (
            "KỶ NGUYÊN QUÂN CHỦNG AI (AI FORCE) ĐÃ BẮT ĐẦU?\n\n"
            "Tin tức độc quyền vừa xuất bản hôm nay từ NBC News:\n"
            "Chính phủ Mỹ đề xuất thành lập một quân chủng AI độc lập ('AI Force') và bổ nhiệm Tổng tư lệnh AI (AI Czar) để giám sát và dẫn dắt cuộc chạy đua an ninh công nghệ toàn cầu.\n\n"
            "Liệu trí tuệ nhân tạo tự hành có nên được trao quyền điều phối hệ thống phòng thủ chiến lược?\n\n"
            "👉 Nhấn ĐĂNG KÝ KÊNH Lido AI Lab để cập nhật những phân tích sâu sắc nhất về AI:\n"
            "https://www.youtube.com/@LidoAILab\n\n"
            "#NBCNews #AIForce #LidoAILab #Technology #AICzar #Shorts #BreakingNews"
        ),
        "tags": ["AI Force", "Quân chủng AI", "NBC News", "AI Czar", "Lido AI Lab", "Shorts", "Công nghệ 2026"],
        "pinned_comment": "🚨 Bạn nghĩ con người có nên trao quyền đưa ra quyết định phòng thủ cho một hệ thống AI tự hành? Hãy để lại góc nhìn của bạn bên dưới nhé! 👇"
    }

    uploader = YouTubeUploaderAgent()
    manifest_path = uploader.prepare_release(out_video_path, metadata)

    # Bắn thông báo macOS
    notifier = NotificationAgent()
    notifier.notify_user_for_review(title, out_video_path)

    print("\n" + "="*70)
    print("🏆 HOÀN THÀNH SIÊU PHẨM 65 GIÂY CUỐN HÚT, KỊCH TÍNH TỪNG GIÂY!")
    print(f"🎥 File video: file://{out_video_path}")
    print(f"📄 Báo cáo: file://{manifest_path}")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(run_60s_epic_short())
