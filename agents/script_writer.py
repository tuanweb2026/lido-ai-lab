import re
import urllib.parse

class TechnicalDeepDiveScriptWriterAgent:
    """
    AGENT 2 NÂNG CẤP ĐỘT PHÁ (HYPER-DIVERSE TECHNICAL STORYTELLER & DYNAMIC WORKFLOW):
    - ĐA DẠNG HÓA 100% LỜI THOẠI CHO TỪNG BẢN TIN:
      Loại bỏ hoàn toàn kịch bản khuôn mẫu dập khuôn cũ ("Bản tin công nghệ nóng... phá vỡ giới hạn cũ...").
      Thay vào đó là 7 thể loại phân tích chuyên sâu độc bản:
      1. SECURITY_BREACH (Cảnh báo an ninh mạng, rò rỉ dữ liệu, Agent mất kiểm soát, lỗ hổng zero-day)
      2. ROBOTICS_HUMANOID (Cơ điện tử, robot hình người, tương tác người-máy, động lực học)
      3. MODEL_BENCHMARK (Ra mắt mô hình mới, cuộc chiến giá API, tốc độ suy luận, tokens/giây)
      4. LEGAL_COPYRIGHT (Tranh chấp bản quyền dữ liệu huấn luyện, điều tra pháp lý, kiện tụng)
      5. CODING_AGENTIC (Lập trình tự hành, bộ điều phối tác nhân, Cursor vs Devin, refactor code)
      6. CHIP_HARDWARE (Phần cứng, chip GPU, siêu máy tính, hạ tầng bán dẫn Blackwell/AMD)
      7. TECH_INNOVATION (Ứng dụng thực tiễn, thương mại điện tử, sản phẩm đột phá)
    - Đồng bộ hóa các hộp đồ họa, lệnh Terminal và tem bảo vệ theo đúng thể loại của từng bài viết.
    """
    def __init__(self, channel_name="@LidoAILab"):
        self.channel_name = channel_name

    def clean_title(self, raw_title):
        # Bỏ tên nguồn báo ở đuôi (ví dụ: " - Ars Technica", " - The New Stack")
        return re.sub(r'\s*-\s*[A-Za-z0-9. -]+$', '', raw_title).strip()

    def identify_main_entities(self, text):
        t_low = text.lower()
        known = [
            "OpenAI", "ChatGPT", "Claude", "Anthropic", "Tesla", "Optimus",
            "Google", "Gemini", "Cursor", "DeepSeek", "Sora", "Nvidia",
            "Meta", "YouTube", "Palo Alto Networks", "GitHub Copilot", "Devin", "Grok"
        ]
        found = [b for b in known if b.lower() in t_low]
        return found[0] if found else "Công nghệ AI"

    def generate_script_from_topic(self, topic):
        raw_title = topic.get("title", "")
        clean_t = self.clean_title(raw_title)
        t_low = clean_t.lower()
        entity = self.identify_main_entities(clean_t)

        # 1. THỂ LOẠI: AN NINH MẠNG / BÊ BỐI BẢO MẬT / RÒ RỈ DỮ LIỆU / ROGUE AGENT
        if any(k in t_low for k in ["leak", "breach", "rogue", "unsecured", "hacked", "stole", "nerfed", "down", "bug", "flaw", "tải ảnh", "lỗ hổng", "bảo mật", "lộ ảnh"]):
            badge_title = "CẢNH BÁO BẢO MẬT AI"
            h1 = f"SỰ CỐ AN NINH: {entity.upper()}"
            t1 = f"Cảnh báo an ninh mạng khẩn cấp! Cộng đồng công nghệ đang chấn động trước thông tin: {clean_t}."
            
            h2 = "HÀNH VI TỰ HÀNH NGOÀI TẦM KIỂM SOÁT"
            t2 = f"Các chuyên gia bảo mật phát hiện hệ thống của {entity} đã phát sinh những hành vi nguy hiểm, tự ý truy cập hoặc làm lộ thông tin nhạy cảm của người dùng ra internet."
            
            h3 = "CẢNH BÁO KHẨN CHO DOANH NGHIỆP"
            t3 = "Nếu bạn đang sử dụng công cụ này trong công việc, hãy lập tức kiểm tra lại các phân quyền, thu hồi khóa API và ngắt các quyền tự động tải dữ liệu nhạy cảm!"
            
            h4 = "BÀI HỌC VỀ RÀO CHẮN AN TOÀN"
            t4 = "Sự việc một lần nữa khẳng định: Khi trao quyền tự hành cho AI, nếu thiếu cơ chế kiểm duyệt độc lập thì rủi ro an ninh mạng là vô cùng khôn lường."
            
            code_cmd = f"{entity.lower()}-audit --scan-leak --quarantine"
            code_status = "[SECURITY CHECK] Phát hiện luồng truy cập bất thường!"
            code_res = "🔒 Đã cách ly dữ liệu & vá lỗ hổng thành công"
            stamp_text = "⚠️ CẢNH BÁO BẢO MẬT"
            search_kws = [f"{entity} cybersecurity leak alert", "Cyber attack server room security glitch"]

        # 2. THỂ LOẠI: ROBOT HÌNH NGƯỜI & TƯƠNG TÁC NHÀ MÁY
        elif any(k in t_low for k in ["robot", "humanoid", "optimus", "balk", "cowers", "knees", "worker", "factory", "digit", "unitree", "boston dynamics"]):
            badge_title = "BẢN TIN ROBOT HÌNH NGƯỜI"
            h1 = f"TÂM ĐIỂM CƠ ĐIỆN TỬ: {entity.upper()}"
            t1 = f"Tin tức chấn động ngành chế tạo robot: {clean_t}! Làn sóng tự động hóa đang tạo ra những diễn biến bất ngờ tại các nhà máy."
            
            h2 = "PHẢN XẠ VÀ CẢM BIẾN MỚI CỦA ROBOT"
            t2 = "Không còn là những cỗ máy cứng nhắc, robot hình người thế hệ mới được trang bị cảm biến không gian cực nhạy, có khả năng nhận diện cự ly và chủ động né tránh khi người thật đến gần."
            
            h3 = "XUNG ĐỘT TỰ ĐỘNG HÓA VÀ VIỆC LÀM"
            t3 = "Nhiều người lao động lo ngại rằng việc trực tiếp hỗ trợ huấn luyện các cỗ máy thông minh này sẽ khiến chính họ nhanh chóng bị thay thế trong dây chuyền sản xuất tương lai."
            
            h4 = "XU THẾ CHUYỂN DỊCH KHÔNG THỂ ĐẢO NGƯỢC"
            t4 = "Dù còn nhiều tranh cãi, các tập đoàn công nghiệp vẫn đang rót hàng tỷ đô la để hoàn thiện thế hệ robot lao động tiếp theo trước năm 2026."
            
            code_cmd = "humanoid-safety --proximity-stop 1.2m"
            code_status = "[PROXIMITY] Phát hiện con người trong cự ly an toàn..."
            code_res = "✓ Kích hoạt tư thế phòng thủ an toàn"
            stamp_text = "🤖 KỶ NGUYÊN ROBOT"
            search_kws = [f"{entity} humanoid robot factory production", "Modern humanoid robot standing in lab"]

        # 3. THỂ LOẠI: CUỘC CHIẾN MÔ HÌNH NỀN TẢNG / GIÁ CẢ & BENCHMARK
        elif any(k in t_low for k in ["gpt-6", "sol", "luna", "pricing", "benchmark", "astra", "release", "launch", "model", "supervoting", "deepseek-r1"]):
            badge_title = "ĐỘT PHÁ MÔ HÌNH AI MỚI"
            h1 = f"BƯỚC ĐI CHIẾN LƯỢC CỦA {entity.upper()}"
            t1 = f"Thị trường AI toàn cầu lại dậy sóng với thông tin mới nhất: {clean_t}! Cuộc đua vị thế giữa các hãng công nghệ lớn đang bước vào giai đoạn quyết định."
            
            h2 = "THIẾT LẬP KỶ LỤC HIỆU NĂNG MỚI"
            t2 = f"Các số liệu benchmark vừa được công bố cho thấy mô hình mới của {entity} đã đạt bước nhảy vọt về khả năng suy luận logic, đồng thời cắt giảm mạnh mẽ chi phí token cho lập trình viên."
            
            h3 = "ĐÒN ĐÁNH THẲNG VÀO ĐỐI THỦ"
            t3 = "Mức giá cực kỳ cạnh tranh này đang trực tiếp phả hơi nóng lên các công ty AI đối thủ, buộc toàn bộ thị trường phải giảm giá dịch vụ để giữ chân khách hàng."
            
            h4 = "LỢI ÍCH TRỰC TIẾP CHO NGƯỜI DÙNG"
            t4 = "Cộng đồng lập trình viên và người dùng cá nhân giờ đây có thể khai thác sức mạnh của siêu AI với chi phí dễ tiếp cận hơn bao giờ hết!"
            
            code_cmd = f"curl https://api.{entity.lower()}.com/v1/benchmarks --compare-all"
            code_status = f"[BENCHMARK] Đo đạc tốc độ suy luận {entity}..."
            code_res = "✓ Đạt 156 tokens/giây, tiết kiệm 60% chi phí"
            stamp_text = "⚡ ĐỘT PHÁ MÔ HÌNH"
            search_kws = [f"{entity} artificial intelligence keynote official", "Supercomputing neural network cluster data"]

        # 4. THỂ LOẠI: TRANH CHẤP BẢN QUYỀN / PHÁP LÝ / ĐIỀU KHOẢN DỊCH VỤ
        elif any(k in t_low for k in ["violation", "sue", "lawsuit", "pentagon", "investigate", "court", "ban", "training on", "bản quyền", "vi phạm"]):
            badge_title = "TRANH CHẤP PHÁP LÝ AI"
            h1 = f"CĂNG THẲNG PHÁP LÝ: {entity.upper()}"
            t1 = f"Một cuộc đối đầu bản quyền gay gắt vừa nổ ra trong ngành công nghệ: {clean_t}!"
            
            h2 = "RANH GIỚI BẢN QUYỀN DỮ LIỆU HUẤN LUYỆN"
            t2 = "Vấn đề sử dụng nội dung sáng tạo, video và dữ liệu của các nền tảng khác để huấn luyện AI mà không xin phép đang đẩy mâu thuẫn lên đỉnh điểm."
            
            h3 = "CÁC ÔNG LỚN TRỰC DIỆN ĐỐI ĐẦU"
            t3 = "Các nhà cung cấp nội dung tuyên bố sẽ áp dụng các biện pháp kỹ thuật và pháp lý mạnh tay nhất để bảo vệ quyền lợi tài sản trí tuệ của mình."
            
            h4 = "ĐỊNH HÌNH LẠI LUẬT CHƠI BẢN QUYỀN"
            t4 = "Kết quả của vụ tranh chấp này sẽ thiết lập tiền lệ pháp lý cực kỳ quan trọng cho toàn bộ ngành công nghiệp AI trong kỷ nguyên số."
            
            code_cmd = "compliance-engine --audit-training-data --strict"
            code_status = "[SCAN] Kiểm tra bản quyền các tập dữ liệu đào tạo..."
            code_res = "⚠️ Đã ghi nhận cảnh báo vi phạm điều khoản"
            stamp_text = "⚖️ PHÁP LÝ & BẢN QUYỀN"
            search_kws = [f"{entity} legal battle press room", "Digital copyright data protection court"]

        # 5. THỂ LOẠI: LẬP TRÌNH TỰ ĐỘNG & ĐIỀU PHỐI AI AGENT
        elif any(k in t_low for k in ["cursor", "devin", "copilot", "coordinator", "agent", "coding", "code", "ide", "mcp"]):
            badge_title = "KỸ SƯ LẬP TRÌNH AI AGENT"
            h1 = f"CUỘC ĐUA CÔNG CỤ LẬP TRÌNH: {entity.upper()}"
            t1 = f"Thông tin chấn động giới lập trình viên quốc tế: {clean_t}!"
            
            h2 = "CƠ CHẾ ĐIỀU PHỐI ĐA TÁC NHÂN"
            t2 = "Không dừng lại ở việc gợi ý code đơn lẻ, công nghệ mới cho phép nhiều AI Agent cùng phối hợp: một agent phân tích kiến trúc, một agent viết mã và một agent tự chạy test sửa lỗi."
            
            h3 = "TRANH CÃI QUYỀN KIỂM SOÁT CODEBASE"
            t3 = "Mâu thuẫn lớn nhất hiện nay là liệu các hãng mô hình hay các môi trường lập trình IDE sẽ trở thành trung tâm chỉ huy của toàn bộ quy trình phát triển phần mềm."
            
            h4 = "TƯƠNG LAI NGHỀ LẬP TRÌNH ĐÃ ĐẾN"
            t4 = "Lập trình viên trong tương lai sẽ chuyển mình thành các kiến trúc sư chỉ huy, điều hành cả một hạm đội AI Agent tạo ra sản phẩm với tốc độ phi thường."
            
            code_cmd = "agent-orchestrator --delegate --auto-fix"
            code_status = "[COORDINATOR] Phân bổ nhiệm vụ cho 3 agents..."
            code_res = "✓ Toàn bộ module phần mềm đã biên dịch thành công"
            stamp_text = "💻 KỸ SƯ AI TỰ HÀNH"
            search_kws = [f"{entity} coding interface software development", "Programmer developer dual screens terminal IDE"]

        # 6. THỂ LOẠI: PHẦN CỨNG, CHIP & SIÊU MÁY TÍNH
        elif any(k in t_low for k in ["nvidia", "chip", "b200", "blackwell", "gpu", "tsmc", "hardware", "datacenter", "turbine"]):
            badge_title = "HẠ TẦNG & SIÊU PHẦN CỨNG"
            h1 = f"CUỘC ĐUA PHẦN CỨNG: {entity.upper()}"
            t1 = f"Tin nóng về nền móng hạ tầng bán dẫn toàn cầu: {clean_t}!"
            
            h2 = "CƠN KHÁT ĐIỆN VÀ TÍNH TOÁN HIỆU NĂNG CAO"
            t2 = "Sự bùng nổ của các siêu mô hình AI đang đẩy các trung tâm dữ liệu vào bài toán cực hạn về năng lượng tiêu thụ, hệ thống tản nhiệt và băng thông xử lý."
            
            h3 = "TÁI ĐỊNH HÌNH CHUỖI CUNG ỨNG BÁN DẪN"
            t3 = "Các kế hoạch đầu tư hàng chục tỷ USD đang được điều chỉnh liên tục nhằm tìm kiếm các giải pháp điện toán xanh và vi kiến trúc chip tối ưu hơn."
            
            h4 = "KỶ NGUYÊN SIÊU MÁY TÍNH AI"
            t4 = "Hãng công nghệ nào làm chủ được nguồn cung bán dẫn và điện năng sẽ nắm giữ chìa khóa định đoạt tương lai của toàn bộ ngành công nghiệp AI."
            
            code_cmd = "nvidia-smi --query-gpu=utilization.gpu,power.draw"
            code_status = "[HARDWARE MONITOR] Quét công suất 1024 cụm GPUs..."
            code_res = "✓ Hiệu suất điện toán đạt 98.4%, tản nhiệt ổn định"
            stamp_text = "⚡ SIÊU CHIP BÁN DẪN"
            search_kws = [f"{entity} advanced microchip semiconductor", "AI supercomputer datacenter servers glowing"]

        # 7. THỂ LOẠI: ỨNG DỤNG THƯƠNG MẠI & SẢN PHẨM ĐỘT PHÁ (Mặc định phong phú)
        else:
            badge_title = "ĐỘT PHÁ CÔNG NGHỆ MỚI"
            h1 = f"BƯỚC TIẾN MỚI CỦA {entity.upper()}"
            t1 = f"Bản tin công nghệ đặc biệt: {clean_t}! Một bước tiến mới đang thu hút sự chú ý lớn từ các chuyên gia toàn cầu."
            
            h2 = "TỐI ƯU HÓA TRẢI NGHIỆM THỰC TẾ"
            t2 = "Khác với các nghiên cứu lý thuyết trong phòng lab, giải pháp này tập trung giải quyết trực tiếp nhu cầu thực tế của người dùng và các bài toán kinh doanh cụ thể."
            
            h3 = "TẠO RA LỢI THẾ CẠNH TRANH MỚI"
            t3 = "Việc sớm tích hợp công nghệ này sẽ giúp các cá nhân và doanh nghiệp gia tăng năng suất vượt trội, rút ngắn thời gian xử lý công việc từ vài ngày xuống còn vài phút."
            
            h4 = "BẮT KỊP LÀN SÓNG ĐỔI MỚI 2026"
            t4 = "Công nghệ đang thay đổi diện mạo từng ngành nghề. Hãy theo dõi sát sao để không bị tụt lại phía sau trong cuộc cách mạng này!"
            
            code_cmd = f"app-deploy --product {entity.lower()} --live"
            code_status = "[DEPLOY] Triển khai tính năng mới lên hệ thống..."
            code_res = "✓ Khởi chạy tính năng thành công trên toàn cầu"
            stamp_text = "🚀 ĐỔI MỚI CÔNG NGHỆ"
            search_kws = [f"{entity} innovative technology presentation", "Futuristic technology user interface digital"]

        scenes = [
            {"scene_id": 1, "headline": h1, "metric_badge": badge_title, "text": t1, "overlay_data": h1, "search_keywords": search_kws},
            {"scene_id": 2, "headline": h2, "metric_badge": badge_title, "text": t2, "overlay_data": h2, "search_keywords": search_kws},
            {"scene_id": 3, "headline": h3, "metric_badge": badge_title, "text": t3, "overlay_data": h3, "search_keywords": search_kws},
            {"scene_id": 4, "headline": h4, "metric_badge": badge_title, "text": t4, "overlay_data": h4, "search_keywords": search_kws},
            {
                "scene_id": 5,
                "headline": "CẬP NHẬT CÔNG NGHỆ ĐỘC QUYỀN",
                "metric_badge": "LIDO AI LAB",
                "text": "Bấm Like và Đăng ký kênh Lido AI Lab ngay hôm nay để đón đầu những đột phá công nghệ mới nhất!",
                "overlay_data": "SUBSCRIBE @LidoAILab",
                "search_keywords": ["YouTube subscribe button glowing neon red", "Modern tech creator studio neon setup"]
            }
        ]

        video_title = f"{badge_title}: {clean_t[:65]}! 🚀⚡ #Shorts #LidoAILab #AI"

        workflow_metadata = {
            "badge_title": badge_title,
            "step1": h1,
            "step2": h2,
            "term_title": f"terminal · {entity.lower()} runtime",
            "code_cmd": code_cmd,
            "code_status": code_status,
            "code_result": code_res,
            "step4": h4,
            "stamp_text": stamp_text
        }

        return {
            "title": video_title,
            "scenes": scenes,
            "workflow_metadata": workflow_metadata,
            "full_voice_text": " ".join([s["text"] for s in scenes])
        }

if __name__ == "__main__":
    writer = TechnicalDeepDiveScriptWriterAgent()
    samples = [
        "Check is your OpenAI GPT-6-Astra nerfed?",
        "New humanoid robot 'cowers' and drops to its knees when workers get too close",
        "OpenAI thừa nhận tác nhân AI tự ý tải ảnh người dùng ChatGPT lên mạng",
        "ChatGPT-6 Sol and Luna are here: Pricing and benchmarks data",
        "YouTube CEO: OpenAI Training Sora on Our Videos Would Be Clear Violation",
        "OpenAI and Cursor agree on agent coordinators. They disagree on who runs them."
    ]
    for s in samples:
        res = writer.generate_script_from_topic({"title": s})
        print(f"\n=======================================================")
        print(f"TITLE: {s}")
        print(f"BADGE: {res['workflow_metadata']['badge_title']}")
        print(f"CMD:   {res['workflow_metadata']['code_cmd']}")
        print(f"TEXT1: {res['scenes'][0]['text']}")
        print(f"TEXT2: {res['scenes'][1]['text']}")
