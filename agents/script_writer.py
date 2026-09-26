import re

class TechnicalDeepDiveScriptWriterAgent:
    """
    Agent 2 NÂNG CẤP ĐA DẠNG NỘI DUNG TUYỆT ĐỐI (HYPER-DIVERSE TECHNICAL STORYTELLER):
    - Tự động nhận diện chính xác từng chủ đề hoàn toàn khác biệt:
      1. ĐẤU VÕ ĐÀI ROBOT: Người thật đấu lồng sắt với Robot hình người (NBC News)
      2. MẠNG XÃ HỘI AI AGENT: Grok AI Agent của Elon Musk trên X / SpaceX
      3. LẬP TRÌNH TỰ ĐỘNG: Đại chiến Devin vs Cursor AI
      4. TRANH CHẤP BẢN QUYỀN / PHÁP LÝ: Vụ kiện OpenAI xem trộm hội thoại ChatGPT
      5. TIÊU CHUẨN ĐẠO ĐỨC ROBOT: UBTECH công bố sách trắng quản trị Robot
      6. SIÊU MÔ HÌNH MỚI: Claude Opus 5.5, GPT-6 Sol/Luna, DeepSeek-R1...
    - Kịch bản bám sát 100% tình tiết của từng tin tức, câu thoại kịch tính, hấp dẫn.
    - Cung cấp từ khóa tìm kiếm ảnh thật ĐỘC NHẤT cho từng cảnh.
    """
    def __init__(self, channel_name="@LidoAILab"):
        self.channel_name = channel_name

    def generate_script_from_topic(self, topic):
        title = topic.get("title", "")
        keywords = topic.get("keywords", [])
        source_name = topic.get("source", "TIN TỨC CÔNG NGHỆ")
        t_lower = title.lower()

        # 1. ĐẤU VÕ ĐÀI ROBOT: Người đấu với Robot hình người trong lồng sắt (NBC News)
        if any(k in t_lower for k in ["cage match", "influencer takes on humanoid", "man versus robot"]) or ("robot" in t_lower and "cage" in t_lower):
            headline_1 = "ĐẠI CHIẾN NGƯỜI VÀ ROBOT"
            badge_1 = "TRẬN CHIẾN LỒNG SẮT LỊCH SỬ"
            text_1 = "Một sự kiện chưa từng có vừa gây chấn động truyền thông Mỹ! Một võ sĩ người thật vừa bước vào võ đài lồng sắt để so găng trực tiếp với một Robot hình người tự hành!"
            overlay_1 = "NGƯỜI THẬT ĐẤU LỒNG SẮT VỚI ROBOT"
            search_kw_1 = ["Humanoid robot boxing match cage", "NBC news robot fight cage match"]

            headline_2 = "PHẢN XẠ VƯỢT TRỘI CỦA CƠ THỂ KIM LOẠI"
            badge_2 = "CẢM BIẾN LỰC VÀ THỊ GIÁC 3D"
            text_2 = "Khác với những cú đấm chậm chạp thông thường, robot được trang bị cảm biến lực phản hồi và thị giác máy tính với tốc độ tính toán hàng nghìn khung hình mỗi giây!"
            overlay_2 = "TÍNH TOÁN CÚ ĐẤM TRONG MILI-GIÂY"
            search_kw_2 = ["Humanoid robot punching athletic movements", "Robot athletic dynamic balance"]

            headline_3 = "CƠ THỂ SINH HỌC BỊ ÁP ĐẢO"
            badge_3 = "SỨC BỀN KHÔNG BIẾT MỆT MỎI"
            text_3 = "Võ sĩ con người nhanh chóng hụt hơi trước một cỗ máy không biết kiệt sức và sở hữu lực đấm chuẩn xác đến từng mi-li-mét mà không hề có cảm xúc run sợ!"
            overlay_3 = "SỨC MẠNH VẬT LÝ VƯỢT TRỘI"
            search_kw_3 = ["Athlete fighting humanoid robot arena", "Robot combat martial arts technology"]

            headline_4 = "RANH GIỚI THỂ THAO ĐÃ BỊ PHÁ BỎ"
            badge_4 = "TƯƠNG LAI CỦA THỂ THAO AI"
            text_4 = "Trận đấu này là lời cảnh báo rõ ràng nhất: Kỷ nguyên mà cơ bắp con người bị vượt mặt bởi robot thông minh không còn là phim viễn tưởng, mà đã bắt đầu ngay hôm nay!"
            overlay_4 = "KỶ NGUYÊN THỂ THAO ROBOT 2026"
            search_kw_4 = ["Futuristic robot arena championship crowd", "Humanoid robot victorious stance"]

            video_title = "CHẤN ĐỘNG: VÕ SĨ NGƯỜI THẬT ĐẤU LỒNG SẮT VỚI ROBOT HÌNH NGƯỜI! 🥊🤖 #Shorts #Robot #NBCNews"

        # 2. SPACEX & X: Grok AI Agent vượt 400.000 người dùng của Elon Musk
        elif any(k in t_lower for k in ["grok", "spacexai", "grok bot", "grok ai agent"]):
            headline_1 = "VŨ KHÍ MỚI CỦA ELON MUSK"
            badge_1 = "GROK AI AGENT BÙNG NỔ"
            text_1 = "Elon Musk vừa kích hoạt một bước đi chiến lược mới! Grok AI Agent trên nền tảng X đã chính thức vượt mốc bốn trăm nghìn người dùng hoạt động chỉ sau vài ngày!"
            overlay_1 = "GROK AI AGENT VƯỢT 400.000 USERS"
            search_kw_1 = ["Elon Musk Grok AI announcement", "xAI Grok logo interface"]

            headline_2 = "AI TỰ ĐỘNG THỰC THI TRÊN MẠNG XÃ HỘI"
            badge_2 = "AGENTIC AI THẾ HỆ MỚI"
            text_2 = "Không chỉ dừng lại ở việc trả lời câu hỏi, Grok Agent có thể tự động đọc luồng dữ liệu thời gian thực, tóm tắt tin nóng và tự thực thi các lệnh phức tạp thay cho người dùng!"
            overlay_2 = "TỰ THỰC THI THEO THỜI GIAN THỰC"
            search_kw_2 = ["xAI Colossus supercomputer Nvidia GPUs", "Elon Musk presentation xAI"]

            headline_3 = "ĐỐI ĐẦU TRỰC DIỆN METAI VÀ OPENAI"
            badge_3 = "CUỘC CHIẾN MẠNG XÃ HỘI AI"
            text_3 = "Tận dụng kho dữ liệu khổng lồ của nền tảng X và siêu máy tính Colossus lớn nhất thế giới, Elon Musk đang biến Grok thành AI Agent phổ cập nhất hành tinh!"
            overlay_3 = "TẬN DỤNG SIÊU MÁY TÍNH COLOSSUS"
            search_kw_3 = ["Data center servers xAI Memphis", "SpaceX Starlink AI technology"]

            headline_4 = "BƯỚC ĐẦU CỦA ĐẾ CHẾ AGENTIC"
            badge_4 = "TƯƠNG LAI CỦA INTERNET"
            text_4 = "Cách chúng ta sử dụng mạng xã hội đang thay đổi hoàn toàn. Thay vì tự tay lướt bài, AI Agent sẽ thay bạn quản lý toàn bộ dòng chảy thông tin trên internet!"
            overlay_4 = "AI THAY BẠN LƯỚT MẠNG XÃ HỘI"
            search_kw_4 = ["Person using smartphone with AI assistant futuristic", "Social media algorithm interface"]

            video_title = "ELON MUSK TUNG CHIÊU: GROK AI AGENT BÙNG NỔ 400.000 NGƯỜI DÙNG! 🚀⚡ #Shorts #ElonMusk #Grok"

        # 3. ĐẠI CHIẾN LẬP TRÌNH: Devin vs Cursor AI (Hostinger Review)
        elif any(k in t_lower for k in ["devin", "cursor"]) and any(k in t_lower for k in ["vs", "better", "coding"]):
            headline_1 = "ĐẠI CHIẾN CÔNG CỤ CODE AI"
            badge_1 = "DEVIN VS CURSOR AI"
            text_1 = "Cuộc tranh luận nóng nhất trong giới lập trình viên toàn cầu: Liệu kỹ sư ảo Devin tự hành có thể đánh bại trình soạn thảo Cursor AI được yêu thích nhất hiện nay?"
            overlay_1 = "DEVIN HAY CURSOR AI MẠNH HƠN?"
            search_kw_1 = ["Cursor AI editor code dark theme", "Devin AI software engineer Cognition Labs"]

            headline_2 = "CURSOR: BẠN ĐỒNG HÀNH HOÀN HẢO"
            badge_2 = "TỐC ĐỘ GÕ PHÍM NHÂN ĐÔI"
            text_2 = "Cursor AI giúp lập trình viên tăng tốc gấp ba lần nhờ khả năng thấu hiểu toàn bộ codebase và dự đoán chuẩn xác đoạn mã tiếp theo chỉ bằng một phím Tab!"
            overlay_2 = "CURSOR: TỐI ƯU CHO LẬP TRÌNH VIÊN"
            search_kw_2 = ["Programmer typing code multiple screens terminal", "Modern VS Code coding setup"]

            headline_3 = "DEVIN: KỸ SƯ ẢO TỰ ĐỘNG HOÀN TOÀN"
            badge_3 = "TỰ FIX BUG VÀ TỰ DEPLOY"
            text_3 = "Trong khi đó, Devin lại là một Agent độc lập: Bạn chỉ cần giao nhiệm vụ, Devin sẽ tự mở terminal, tự cài thư viện, tự sửa lỗi và đẩy code lên GitHub mà không cần ai trợ giúp!"
            overlay_3 = "DEVIN: TỰ CODE VÀ TỰ DEPLOY TỪ A ĐẾN Z"
            search_kw_3 = ["Cognition Labs Scott Wu Devin demo", "Automated code generation interface"]

            headline_4 = "CÔNG CỤ NÀO DÀNH CHO BẠN?"
            badge_4 = "LỰA CHỌN CỦA NĂM 2026"
            text_4 = "Nếu bạn muốn kiểm soát từng dòng code, hãy chọn Cursor. Nhưng nếu muốn giao phó toàn bộ dự án để đi uống cà phê, Devin chính là tương lai không thể chối từ!"
            overlay_4 = "LỰA CHỌN CỦA KỶ NGUYÊN MỚI"
            search_kw_4 = ["Software team collaborating AI startup", "Future of programming workspace"]

            video_title = "ĐẠI CHIẾN KỸ SƯ AI: NÊN CHỌN DEVIN HAY CURSOR ĐỂ LẬP TRÌNH? 💻🔥 #Shorts #Devin #CursorAI"

        # 4. TRANH CHẤP BẢN QUYỀN / BẢO MẬT: OpenAI bị kiện xem trộm hội thoại ChatGPT
        elif any(k in t_lower for k in ["sued", "lawsuit", "undisclosed human review", "conversations"]) and "openai" in t_lower:
            headline_1 = "BÊ BỐI BẢO MẬT TẠI OPENAI"
            badge_1 = "VỤ KIỆN XEM TRỘM TIN NHẮN"
            text_1 = "OpenAI vừa bị đệ đơn kiện tập thể tại tòa án Mỹ với cáo buộc bí mật để con người đọc và đánh giá các đoạn hội thoại nhạy cảm của người dùng ChatGPT!"
            overlay_1 = "OPENAI BỊ KIỆN XEM TRỘM CHATGPT"
            search_kw_1 = ["OpenAI lawsuit court documents", "ChatGPT privacy security breach"]

            headline_2 = "DỮ LIỆU RIÊNG TƯ BỊ PHƠI BÀY"
            badge_2 = "KHÔNG HỀ THÔNG BÁO CHO NGƯỜI DÙNG"
            text_2 = "Đơn kiện chỉ rõ: Hàng triệu bí mật kinh doanh, mã code doanh nghiệp và tâm sự y tế của người dùng đã bị chuyển đến các nhân viên kiểm duyệt bên thứ ba mà không hề có sự đồng ý!"
            overlay_2 = "HÀNG TRIỆU BÍ MẬT BỊ TIẾT LỘ"
            search_kw_2 = ["Cyber security data leak shield padlock", "Confidential business document leaked"]

            headline_3 = "RỦI RO CHO DOANH NGHIỆP"
            badge_3 = "BÀI HỌC VỀ QUYỀN RIÊNG TƯ"
            text_3 = "Đây là hồi chuông cảnh tỉnh cho mọi công ty: Đừng bao giờ dán các file bí mật, API key hoặc dữ liệu khách hàng lên các AI đám mây nếu chưa bật chế độ bảo mật nghiêm ngặt!"
            overlay_3 = "CẢNH BÁO: ĐỪNG ĐƯA BÍ MẬT LÊN AI"
            search_kw_3 = ["Corporate boardroom security meeting", "Server room encrypted data lock"]

            headline_4 = "LUẬT CHƠI MỚI CHO BẢO MẬT AI"
            badge_4 = "QUYỀN LỰC THUỘC VỀ NGƯỜI DÙNG"
            text_4 = "Vụ kiện này có thể buộc các hãng AI phải minh bạch hoàn toàn cơ chế huấn luyện và trao quyền kiểm soát dữ liệu tuyệt đối lại cho cộng đồng người dùng toàn cầu!"
            overlay_4 = "PHẢI MINH BẠCH DỮ LIỆU HUẤN LUYỆN"
            search_kw_4 = ["US federal courthouse building facade", "AI regulation legal gavel"]

            video_title = "CHẤN ĐỘNG: OPENAI BỊ KIỆN VÌ BÍ MẬT XEM TRỘM HỘI THOẠI CHATGPT! 🚨⚖️ #Shorts #OpenAI #ChatGPT"

        # 5. Fallback thông minh: Phân tích sâu thực thể cụ thể
        else:
            clean_title = re.sub(r' - [^-\n]+$', '', title).strip()
            extracted_entity = "CÔNG NGHỆ MỚI"
            for candidate in ["ChatGPT", "DeepSeek", "Claude", "OpenAI", "Anthropic", "NVIDIA", "Gemini", "Sora", "Kling", "Cursor", "Apple Intelligence", "UBTECH"]:
                if candidate.lower() in clean_title.lower():
                    extracted_entity = candidate
                    break

            headline_1 = f"TÂM ĐIỂM: {extracted_entity.upper()}"
            badge_1 = f"BƯỚC TIẾN CỦA {extracted_entity.upper()}"
            text_1 = f"Bản tin công nghệ nóng: {clean_title}! Đây là bước ngoặt đang được toàn bộ Thung lũng Silicon và giới đầu tư toàn cầu theo dõi sát sao!"
            overlay_1 = f"ĐỘT PHÁ MỚI: {extracted_entity.upper()}"
            search_kw_1 = [f"{extracted_entity} official event presentation", f"{extracted_entity} keynote speech"]

            headline_2 = "BẢN CHẤT CÔNG NGHỆ ĐỘT PHÁ"
            badge_2 = "KIẾN TRÚC THỜI GIAN THỰC"
            text_2 = "Mô hình mới đã phá vỡ giới hạn hiệu năng cũ, tăng tốc độ xử lý lên gấp nhiều lần và giảm thiểu tối đa các lỗi ảo giác logic thường gặp!"
            overlay_2 = "TỐC ĐỘ TĂNG GẤP NHIỀU LẦN"
            search_kw_2 = [f"{extracted_entity} headquarters building", "Advanced supercomputer processor"]

            headline_3 = "TÁC ĐỘNG TỚI NGƯỜI TIÊU DÙNG"
            badge_3 = "LỢI ÍCH TRỰC TIẾP"
            text_3 = "Người dùng giờ đây có thể ứng dụng trực tiếp công cụ này vào công việc hàng ngày, giải quyết các tác vụ phức tạp chỉ trong vài cú nhấp chuột!"
            overlay_3 = "TIẾT KIỆM HÀNG CHỤC GIỜ LÀM VIỆC"
            search_kw_3 = ["Young professional working with modern AI laptop", "Productive digital workspace"]

            headline_4 = "KỶ NGUYÊN TRÍ TUỆ NHÂN TẠO 2026"
            badge_4 = "XU HƯỚNG BẮT BUỘC"
            text_4 = "Công nghệ đang thay đổi theo từng ngày. Việc nắm bắt công cụ này sớm nhất sẽ mang lại cho bạn lợi thế cạnh tranh áp đảo trên thị trường!"
            overlay_4 = "ĐÓN ĐẦU LÀN SÓNG 2026"
            search_kw_4 = ["Global technology network connections", "Futuristic smart city innovation"]

            video_title = f"BẢN TIN ĐỘC QUYỀN: {clean_title[:65]}! 🚀🔥 #Shorts #LidoAILab #AI"

        # Cảnh 5 Call to Action với từ khóa ảnh độc quyền
        scenes = [
            {"scene_id": 1, "headline": headline_1, "metric_badge": badge_1, "text": text_1, "overlay_data": overlay_1, "search_keywords": search_kw_1},
            {"scene_id": 2, "headline": headline_2, "metric_badge": badge_2, "text": text_2, "overlay_data": overlay_2, "search_keywords": search_kw_2},
            {"scene_id": 3, "headline": headline_3, "metric_badge": badge_3, "text": text_3, "overlay_data": overlay_3, "search_keywords": search_kw_3},
            {"scene_id": 4, "headline": headline_4, "metric_badge": badge_4, "text": text_4, "overlay_data": overlay_4, "search_keywords": search_kw_4},
            {
                "scene_id": 5,
                "headline": "CẬP NHẬT CÔNG NGHỆ ĐỘC QUYỀN",
                "metric_badge": "LIDO AI LAB INSIDER",
                "text": "Bấm Like và Đăng ký ngay kênh Lido AI Lab để không bỏ lỡ những phân tích công nghệ đỉnh cao mỗi ngày!",
                "overlay_data": "SUBSCRIBE: YOUTUBE.COM/@LidoAILab",
                "search_keywords": ["YouTube subscribe button glowing neon red", "Modern tech creator studio neon setup"]
            }
        ]

        return {
            "title": video_title,
            "scenes": scenes,
            "full_voice_text": " ".join([s["text"] for s in scenes])
        }
