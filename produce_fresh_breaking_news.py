import asyncio
import os
from agents.media_producer import RealPhotoMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent
from agents.notifier import NotificationAgent

async def run_fresh_breaking_news():
    print("==========================================================================")
    print("🚨 SẢN XUẤT VIDEO TIN NÓNG NHẤT: NBC NEWS (20/09/2026 - HÔM NAY)")
    print("==========================================================================")

    # Kịch bản thực tế 100% bóc tách bài báo vừa xuất bản của NBC News
    source_tag = "NBC NEWS • 20/09/2026 (CÁCH ĐÂY VÀI GIỜ)"
    scenes = [
        {
            "scene_id": 1,
            "image_file": "news_trump_ai_force.jpg",
            "source_label": source_tag,
            "headline": "MỸ SẮP LẬP 'QUÂN CHỦNG AI'?",
            "metric_badge": "TUYÊN BỐ GÂY CHẤN ĐỘNG",
            "text": "Liệu Mỹ có chuẩn bị thành lập một Quân Chủng AI chuyên trách, tương tự như Lực Lượng Vũ Trụ Space Force? Tuyên bố gây sốc vừa được phát đi sáng nay!",
            "overlay_data": "ĐỀ XUẤT THÀNH LẬP 'AI FORCE'"
        },
        {
            "scene_id": 2,
            "image_file": "news_military_ai_command.jpg",
            "source_label": source_tag,
            "headline": "BỔ NHIỆM 'TỔNG CHỈ HUY AI' (AI CZAR)",
            "metric_badge": "GIÁM SÁT AN NINH QUỐC GIA",
            "text": "Theo tin độc quyền từ NBC News hôm nay, cựu Tổng thống Donald Trump vừa cam kết sẽ bổ nhiệm một Tổng chỉ huy AI và lập lực lượng phản ứng nhanh... trước nỗi sợ AI vượt tầm kiểm soát!",
            "overlay_data": "BỔ NHIỆM TỔNG TƯ LỆNH AI"
        },
        {
            "scene_id": 3,
            "image_file": "news_pentagon_supercomputer.jpg",
            "source_label": source_tag,
            "headline": "CUỘC ĐUA VŨ TRANG THUẬT TOÁN",
            "metric_badge": "CHI PHÍ PHÒNG THỦ KHỦNG",
            "text": "Từ việc phòng thủ tấn công mạng, bảo vệ lưới điện quốc gia, đến điều phối siêu máy tính quân sự... Trí tuệ nhân tạo đã chính thức trở thành chiến trường địa chính trị sống còn!",
            "overlay_data": "AI LÀ VŨ KHÍ CHIẾN LƯỢC"
        },
        {
            "scene_id": 4,
            "image_file": "news_ai_satellite_defense.jpg",
            "source_label": source_tag,
            "headline": "CẬP NHẬT CÙNG LIDO AI LAB",
            "metric_badge": "THEO DÕI TIN MỚI NHẤT",
            "text": "Bấm Đăng ký kênh Lido AI Lab ngay hôm nay để đón đầu những bước chuyển dịch công nghệ và an ninh AI nóng bỏng nhất thế giới!",
            "overlay_data": "SUBSCRIBE: YOUTUBE.COM/@LidoAILab"
        }
    ]

    title = "MỸ SẮP LẬP 'QUÂN CHỦNG AI' VÀ BỔ NHIỆM TỔNG TƯ LỆNH AI? 🇺🇸🚨 #Shorts #NBCNews #AI"

    producer = RealPhotoMediaProducerAgent()
    out_video_path = os.path.join(producer.output_dir, "lido_fresh_news_20sep2026.mp4")
    
    # Render video
    video_f = await producer.produce_real_photo_short(scenes)
    os.rename(video_f, out_video_path)

    # Đóng gói metadata
    metadata = {
        "title": title,
        "source": "NBC News & AZ Family",
        "published_date": "Sunday, 20 Sep 2026 (Hôm nay)",
        "original_article": "Trump vows to create 'AI Force' and appoint AI czar amid concerns over rapidly developing tech",
        "video_file": out_video_path,
        "description": (
            "BẢN TIN CÔNG NGHỆ THỜI SỰ TỪ LIDO AI LAB (20/09/2026):\n\n"
            "Theo thông tin độc quyền vừa đăng tải trên NBC News hôm nay:\n"
            "Cựu Tổng thống Donald Trump tuyên bố kế hoạch thành lập một lực lượng quân chủng chuyên trách về AI ('AI Force') và bổ nhiệm một Tổng chỉ huy AI (AI Czar) để giám sát công nghệ đang phát triển với tốc độ chóng mặt.\n\n"
            "Liệu trí tuệ nhân tạo có chính thức trở thành một nhánh tác chiến quân sự độc lập?\n\n"
            "👉 Đăng ký kênh Lido AI Lab để cập nhật tin tức công nghệ AI nóng nhất từng giờ:\n"
            "https://www.youtube.com/@LidoAILab\n\n"
            "#NBCNews #AIForce #Trump #LidoAILab #AI #ArtificialIntelligence #Shorts #BreakingNews"
        ),
        "tags": ["AI Force", "NBC News", "Trump AI", "Quân chủng AI", "Lido AI Lab", "Shorts", "Tin tức AI 2026"]
    }

    uploader = YouTubeUploaderAgent()
    manifest_path = uploader.prepare_release(out_video_path, metadata)

    # Gửi thông báo macOS
    notifier = NotificationAgent()
    notifier.notify_user_for_review(title, out_video_path)

    print("\n" + "="*70)
    print("🎉 ĐÃ HOÀN TẤT VIDEO TIN NÓNG HỔI HÔM NAY (20/09/2026)!")
    print(f"🎥 Video: file://{out_video_path}")
    print(f"📄 Chi tiết nguồn báo: file://{manifest_path}")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(run_fresh_breaking_news())
