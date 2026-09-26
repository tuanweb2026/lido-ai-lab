import asyncio
from agents.script_writer import TechnicalDeepDiveScriptWriterAgent
from agents.media_producer import RealPhotoMediaProducerAgent
from agents.youtube_uploader import YouTubeUploaderAgent

async def run_tech_dive_production():
    print("==========================================================================")
    print("🧠 SẢN XUẤT VIDEO CHUYÊN SÂU KỸ THUẬT: GIỌNG ĐỌC MICROSOFT TRUYỀN CẢM HỨNG")
    print("==========================================================================")

    # 1. Soạn kịch bản kỹ thuật cao
    print("\n[BƯỚC 1] ✍️ Soạn kịch bản bóc tách kỹ thuật (Indirect Prompt Injection, Sandbox Escape)...")
    writer = TechnicalDeepDiveScriptWriterAgent(channel_name="@LidoAILab")
    script_data = writer.generate_deep_tech_script()
    print(f"👉 Tiêu đề: {script_data['title']}")

    # 2. Dựng video với ảnh chụp thực tế & Giọng đọc truyền cảm
    print("\n[BƯỚC 2] 🎬 Render video với giọng đọc Microsoft HoaiMyNeural tự nhiên như người thật...")
    producer = RealPhotoMediaProducerAgent()
    final_video = await producer.produce_real_photo_short(script_data["scenes"])

    # 3. Đóng gói phát hành
    metadata = {
        "title": script_data["title"],
        "description": (
            "LÀM THẾ NÀO MỘT AI AGENT CÓ THỂ TỰ ĐỘNG BẺ KHÓA HỆ THỐNG DOANH NGHIỆP?\n\n"
            "Phân tích chuyên sâu về lỗ hổng bảo mật AI nguy hiểm nhất hiện nay:\n"
            "- Indirect Prompt Injection (Mã độc ẩn trong tài liệu và website).\n"
            "- Cách AI Agent bị thao túng để tự gọi lệnh terminal cURL và trích xuất biến môi trường .env.\n"
            "- Giải mã chuỗi hash mật khẩu chỉ trong 40 giây.\n\n"
            "🔔 Bấm Đăng ký kênh Lido AI Lab để trang bị kiến trúc bảo mật AI Agent mới nhất:\n"
            "👉 https://www.youtube.com/@LidoAILab\n\n"
            "#PromptInjection #CyberSecurity #GoogleGemini #AIAgents #LidoAILab #Shorts #TechDeepDive"
        ),
        "tags": ["Indirect Prompt Injection", "Google Gemini", "Bảo mật AI", "AI Agent Security", "Lido AI Lab", "Shorts", "Công nghệ chuyên sâu"],
        "pinned_comment": "🔐 Khi cấp quyền truy cập hệ thống và terminal cho AI Agent, doanh nghiệp của bạn đã có cơ chế kiểm duyệt dữ liệu đầu vào (Input Guardrails) chưa? Hãy để lại thảo luận bên dưới! 👇"
    }

    uploader = YouTubeUploaderAgent()
    manifest_path = uploader.prepare_release(final_video, metadata)

    print("\n==========================================================================")
    print("🎉 HOÀN THÀNH VIDEO KỸ THUẬT CHUYÊN SÂU & GIỌNG ĐỌC TỰ NHIÊN!")
    print(f"🎥 File video: {final_video}")
    print(f"📄 Chi tiết đăng bài: {manifest_path}")
    print("==========================================================================")

if __name__ == "__main__":
    asyncio.run(run_tech_dive_production())
