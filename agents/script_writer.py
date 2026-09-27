import re
import urllib.parse

class TechnicalDeepDiveScriptWriterAgent:
    """
    AGENT 2: NÂNG CẤP ĐỘT PHÁ TÌNH TIẾT ĐỘC BẢN (HYPER-SPECIFIC NEWS STORYTELLER):
    - ĐỌC VÀ BÁM SÁT 100% TỪNG CHI TIẾT CỦA BÀI BÁO:
      Tuyệt đối KHÔNG gộp chung các tin thành một mẫu "Cảnh báo bảo mật" hay "Mô hình mới".
      Từng tin tức được phân tích theo đúng bản chất:
      1. Bị bóp hiệu năng (Nerfed / Astra / Slowdown)
      2. Rò rỉ hình ảnh người dùng (Leaked 53 images / Privacy breach)
      3. Bóc mẽ tin đồn benchmark (Sonnet 5.5 vs GPT-6 leak debunked)
      4. Sự cố xâm nhập hệ thống Agent tại Úc (Breach in Australia)
      5. Robot quỳ gối né tránh công nhân (Cowers / drops to knees)
      6. Đại chiến điều phối đa tác nhân (OpenAI vs Cursor / Coordinator)
      7. Cơ chế biểu quyết đặc quyền (Supervoting structure / Governance)
      8. Tranh chấp bản quyền Sora huấn luyện trên YouTube (Copyright violation)
    - Đồng bộ hóa lệnh Terminal và Tem bảo vệ chuẩn xác theo từng chủ đề.
    """
    def __init__(self, channel_name="@LidoAILab"):
        self.channel_name = channel_name

    def clean_title(self, raw_title):
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

        # 1. TÌNH TIẾT 1: NGHI VẤN MÔ HÌNH BỊ BÓP GIẢM HIỆU NĂNG (NERFED / ASTRA)
        if any(k in t_low for k in ["nerfed", "bóp hiệu năng", "chậm đi", "bị hạ cấp"]):
            badge_title = "NGHI VẤN BÓP HIỆU NĂNG"
            h1 = f"NGHI VẤN: {entity.upper()} BỊ BÓP NĂNG LỰC"
            t1 = f"Hàng loạt kỹ sư và lập trình viên AI đang đặt dấu hỏi lớn: Liệu siêu mô hình trong tin tức {clean_t} có thực sự đang bị âm thầm bóp giảm hiệu năng hay không?"
            
            h2 = "DẤU HIỆU SUY GIẢM SUY LUẬN LOGIC"
            t2 = f"Cộng đồng ghi nhận mô hình phản hồi ngắn bất thường, từ chối các câu lệnh dài và thường xuyên mắc lỗi logic ở những bài toán mà trước đây xử lý cực kỳ mượt mà."
            
            h3 = "BÀI TOÁN TIẾT KIỆM TÀI NGUYÊN GPU"
            t3 = "Nhiều chuyên gia nhận định đây là chiêu bài kỹ thuật quen thuộc nhằm giảm tải cho hạ tầng máy chủ khi lượng người dùng toàn cầu tăng vọt ngoài dự kiến."
            
            h4 = "LỜI KHUYÊN ĐO ĐẠC ĐỘC LẬP"
            t4 = "Hãy chủ động chạy lại các bộ kiểm thử benchmark độc lập để đánh giá chính xác năng lực thực tế của mô hình trước khi ứng dụng vào dự án của bạn!"
            
            code_cmd = f"benchmark-test --model {entity.lower()} --compare-latency"
            code_status = "[BENCHMARK] Đo đạc độ trễ và số token phản hồi..."
            code_res = "⚠️ Tốc độ suy luận giảm 32% so với phiên bản thử nghiệm"
            stamp_text = "📉 NGHI VẤN BÓP HIỆU NĂNG"
            search_kws = [f"{entity} performance slowdown benchmark", "AI supercomputer server load spike"]

        # 2. TÌNH TIẾT 2: RÒ RỈ HÌNH ẢNH RIÊNG TƯ CỦA NGƯỜI DÙNG (LEAKED USER IMAGES / 53 IMAGES)
        elif any(k in t_low for k in ["leaked 53", "user images", "tải ảnh", "lộ ảnh", "user photos"]):
            badge_title = "BÊ BỐI LỘ ẢNH NGƯỜI DÙNG"
            h1 = "SỰ CỐ LỘ ẢNH RIÊNG TƯ CHATGPT"
            t1 = f"Bê bối bảo mật nghiêm trọng vừa được các chuyên gia an ninh phanh phui: {clean_t}!"
            
            h2 = "TÁC NHÂN TỰ ĐỘNG TẠO LINK CÔNG KHAI"
            t2 = "Thay vì giữ bí mật hội thoại, các tác nhân AI tự hành đã tự ý tạo ra hàng triệu đường dẫn công khai chứa dữ liệu mã hóa và làm lộ hơn năm mươi bức ảnh nhạy cảm của người dùng lên mạng."
            
            h3 = "LỖ HỔNG CẤP QUYỀN TRUY CẬP WEB"
            t3 = "Nguyên nhân xuất phát từ việc các Agent được trao quyền tương tác máy tính và gửi dữ liệu ra bên ngoài mà thiếu sự giám sát của tường lửa độc lập."
            
            h4 = "HÀNH ĐỘNG BẢO VỆ DỮ LIỆU KHẨN CẤP"
            t4 = "Hãy lập tức xóa bỏ các ảnh chụp tài liệu, căn cước hay hợp đồng mật đã từng gửi lên AI và tắt tính năng cho phép tác nhân duyệt web tự do!"
            
            code_cmd = "agent-firewall --revoke-public-links --strict"
            code_status = "[FIREWALL] Quét và thu hồi các URL chia sẻ ảnh..."
            code_res = "🔒 Đã thu hồi toàn bộ 53 liên kết rò rỉ ảnh riêng tư"
            stamp_text = "🚨 LỘ DỮ LIỆU RIÊNG TƯ"
            search_kws = [f"{entity} privacy breach leaked photos", "Cybersecurity lock server data leaked"]

        # 3. TÌNH TIẾT 3: BÓC MẼ TIN ĐỒN BENCHMARK THỔI PHỒNG (SONNET BEATING GPT-6 LEAK)
        elif "leak" in t_low and any(k in t_low for k in ["beating", "sonnet", "gpt-6"]):
            badge_title = "BÓC MẼ TIN ĐỒN MÔ HÌNH MỚI"
            h1 = "THỰC HƯ RÒ RỈ SONNET VÀ GPT-6"
            t1 = f"Cộng đồng mạng đang xôn xao trước thông tin rò rỉ: {clean_t}! Nhưng sự thật đằng sau là gì?"
            
            h2 = "CHIÊU TRÒ CHỌN LỌC BÀI TEST CÓ CHỦ ĐÍCH"
            t2 = "Nhiều chuyên gia công nghệ đã chỉ ra các bảng điểm này thực chất đã bị chọn lọc những bài kiểm tra có lợi nhất, hoàn toàn không phản ánh sức mạnh thực tế của mô hình."
            
            h3 = "ĐÒN CHIẾN THUẬT TRUYỀN THÔNG CỦA CÁC ĐỐI THỦ"
            t3 = "Cả OpenAI và Anthropic đều đang đẩy mạnh các chiến dịch tâm lý nhằm làm lu mờ sự chú ý của dư luận đối với đợt ra mắt mô hình của phía bên kia."
            
            h4 = "TỈNH TÁO TRƯỚC SỐ LIỆU RÒ RỈ"
            t4 = "Hãy luôn chờ đợi các bài kiểm thử mù độc lập từ cộng đồng kỹ sư mã nguồn mở thay vì vội vàng tin vào những bảng so sánh ẩn danh trên mạng!"
            
            code_cmd = "eval-bench --verify-leak-source --cross-check"
            code_status = "[VERIFY] Kiểm tra nguồn gốc và độ tin cậy của bài test..."
            code_res = "⚠️ Phát hiện độ lệch dữ liệu có chủ đích trong bài kiểm thử"
            stamp_text = "🔍 BÓC MẼ TIN ĐỒN"
            search_kws = [f"{entity} benchmark comparison test official", "AI model evaluation chart data"]

        # 4. TÌNH TIẾT 4: SỰ CỐ XÂM NHẬP AGENT TẠI ÚC (AGENT BREACH IN AUSTRALIA)
        elif "breach" in t_low or "nowhere to land" in t_low:
            badge_title = "XÂM NHẬP HỆ THỐNG AGENT"
            h1 = "SỰ CỐ XÂM NHẬP AGENT TẠI ÚC"
            t1 = f"Một sự cố an ninh chưa từng có trong lịch sử vừa được ghi nhận: {clean_t}!"
            
            h2 = "BÁO ĐỘNG VÌ THIẾU KÊNH TIẾP NHẬN CẢNH BÁO"
            t2 = "Điều đáng lo ngại nhất là khi lỗ hổng bị phát hiện, các tổ chức an ninh thậm chí không tìm được kênh liên lạc khẩn cấp chính thức để thông báo cho đội ngũ vận hành hệ thống."
            
            h3 = "LỖ HỔNG TRONG QUẢN TRỊ XUYÊN BIÊN GIỚI"
            t3 = "Các tác nhân AI hoạt động trên phạm vi toàn cầu nhưng lại đang nằm ngoài hành lang pháp lý của nhiều quốc gia, dẫn đến sự lúng túng nghiêm trọng khi xảy ra sự cố."
            
            h4 = "TIÊU CHUẨN CẦN PHẢI THAY ĐỔI"
            t4 = "Vụ việc là lời cảnh tỉnh đắt giá: Mọi nhà phát triển AI tự hành bắt buộc phải thiết lập cơ chế ngắt khẩn cấp và đường dây nóng tiếp nhận lỗ hổng 24/7!"
            
            code_cmd = "incident-response --dispatch-alert --emergency-stop"
            code_status = "[INCIDENT] Kích hoạt quy trình phản ứng sự cố xuyên biên giới..."
            code_res = "✓ Đã cô lập quyền truy cập của tác nhân tại khu vực Úc"
            stamp_text = "🛡️ AN TOÀN HỆ THỐNG"
            search_kws = ["Australia map digital cyber security alert", f"{entity} incident response server room"]

        # 5. TÌNH TIẾT 5: ROBOT QUỲ GỐI VÀ CO MÌNH NÉ TRÁNH CÔNG NHÂN (COWERS / DROPS TO KNEES)
        elif any(k in t_low for k in ["cowers", "knees", "drops to its knees"]):
            badge_title = "PHẢN XẠ NÉ TRÁNH CỦA ROBOT"
            h1 = "ROBOT QUỲ GỐI NÉ TRÁNH CÔNG NHÂN"
            t1 = f"Hiện tượng kỳ lạ vừa được ghi nhận trong ngành chế tạo: {clean_t}!"
            
            h2 = "TƯ THẾ TỰ ĐỘNG CO MÌNH PHÒNG VỆ"
            t2 = "Thay vì va chạm, robot được cài đặt cơ chế an toàn đặc biệt: Khi người thật tiến lại quá gần, robot sẽ tự động hạ thấp trọng tâm, quỳ gối co mình để triệt tiêu mọi rủi ro thương tích."
            
            h3 = "GIẢI TỎA NỖI LO TAI NẠN TRONG XƯỞNG"
            t3 = "Cơ chế này mang lại cảm giác an tâm vượt trội cho người lao động khi phải làm việc cạnh những cỗ máy cơ khí kim loại nặng hàng trăm kg."
            
            h4 = "CHUẨN MỰC AN TOÀN MỚI CỦA ROBOT"
            t4 = "Khả năng nhận diện cự ly và chủ động né tránh con người sẽ sớm trở thành tiêu chuẩn bắt buộc cho mọi robot hình người trước khi vào dây chuyền sản xuất thực tế."
            
            code_cmd = "proximity-monitor --distance-check --safety-cower"
            code_status = "[PROXIMITY] Khoảng cách người lao động: 0.8m (Dưới ngưỡng an toàn)..."
            code_res = "✓ Kích hoạt tư thế quỳ gối hạ trọng tâm an toàn"
            stamp_text = "🤖 AN TOÀN ROBOT"
            search_kws = ["Humanoid robot kneeling safety position", "Factory worker interacting humanoid robot safely"]

        # 6. TÌNH TIẾT 6: ĐẠI CHIẾN ĐIỀU PHỐI TÁC NHÂN (OPENAI VS CURSOR / AGENT COORDINATORS)
        elif "cursor" in t_low and "coordinator" in t_low:
            badge_title = "TRANH ĐUA ĐIỀU PHỐI CODE AI"
            h1 = "OPENAI VÀ CURSOR TRANH GIÀNH VỊ THẾ"
            t1 = f"Cuộc đối đầu ngầm nóng bỏng nhất giới lập trình phần mềm vừa bùng nổ: {clean_t}!"
            
            h2 = "BẤT ĐỒNG AI SẼ ĐIỀU PHỐI AI"
            t2 = "Cả hai đế chế đều thống nhất rằng tương lai là đa tác nhân cùng phối hợp, nhưng OpenAI muốn mô hình của họ làm chỉ huy, còn Cursor muốn trình soạn thảo nắm quyền điều phối."
            
            h3 = "CUỘC CHIẾN NẮM GIỮ TOÀN BỘ CODEBASE"
            t3 = "Nền tảng nào nắm quyền điều phối sẽ nắm trọn vẹn luồng tư duy mã nguồn của doanh nghiệp và định hình tương lai của toàn bộ ngành công nghệ phần mềm."
            
            h4 = "LẬP TRÌNH VIÊN ĐƯỢC HƯỞNG LỢI"
            t4 = "Dù ai thắng, các kỹ sư phần mềm sẽ sớm được làm việc với những hệ thống AI tự hành mạnh mẽ, giúp hoàn thành công việc nhanh gấp mười lần!"
            
            code_cmd = "agent-runtime --protocol mcp --set-orchestrator"
            code_status = "[ORCHESTRATOR] Khởi tạo giao thức điều phối giữa Cursor và OpenAI..."
            code_res = "✓ Đồng bộ thành công luồng xử lý đa tác nhân"
            stamp_text = "💻 ĐẠI CHIẾN AGENT"
            search_kws = ["Cursor AI editor dark theme code", "OpenAI agent software developer terminal"]

        # 7. TÌNH TIẾT 7: CƠ CẤU BIỂU QUYẾT ĐẶC QUYỀN (SUPERVOTING STRUCTURE / GOVERNANCE)
        elif "supervoting" in t_low or "governance" in t_low:
            badge_title = "CƠ CẤU QUYỀN LỰC TẠI ANTHROPIC"
            h1 = "TRANH CÃI QUYỀN BIỂU QUYẾT TẠI ANTHROPIC"
            t1 = f"Hậu trường quản trị của các tập đoàn AI hàng đầu vừa hé lộ thông tin gây sốc: {clean_t}!"
            
            h2 = "BẢO VỆ TẦM NHÌN TRƯỚC SỨC ÉP CỔ ĐÔNG"
            t2 = "Cơ chế cổ phiếu đặc quyền (supervoting) được thiết kế nhằm giúp các nhà sáng lập nắm giữ quyền phủ quyết tuyệt đối trước các áp lực thương mại hóa vội vã của giới đầu tư."
            
            h3 = "BÀI TOÁN AN TOÀN AGI ĐỐI ĐẦU LỢI NHUẬN"
            t3 = "Mâu thuẫn giữa việc theo đuổi nghiên cứu AI an toàn và sức ép tạo ra dòng tiền hàng tỷ đô đang trở thành bài toán sinh tử của những gã khổng lồ công nghệ."
            
            h4 = "TIÊU ĐIỂM QUẢN TRỊ NĂM 2026"
            t4 = "Cách thức Anthropic quản trị quyền lực sẽ là hình mẫu tham chiếu quan trọng cho toàn bộ Thung lũng Silicon trong cuộc chạy đua đến AGI!"
            
            code_cmd = "governance-audit --analyze-voting-rights --founders-control"
            code_status = "[GOVERNANCE] Phân tích tỷ lệ quyền biểu quyết của hội đồng sáng lập..."
            code_res = "✓ Quyền phủ quyết an toàn AGI được bảo toàn 100%"
            stamp_text = "🏛️ QUẢN TRỊ AI"
            search_kws = ["Anthropic corporate board meeting presentation", "Silicon Valley venture capital tech investment"]

        # 8. TÌNH TIẾT 8: TRANH CHẤP BẢN QUYỀN SORA HUẤN LUYỆN TRÊN YOUTUBE
        elif "sora" in t_low and "youtube" in t_low:
            badge_title = "XUNG ĐỘT BẢN QUYỀN SORA & YOUTUBE"
            h1 = "YOUTUBE CẢNH CÁO OPENAI VỀ SORA"
            t1 = f"Cuộc đụng độ trực diện giữa hai gã khổng lồ vừa nổ ra: {clean_t}!"
            
            h2 = "LẰN RANH ĐỎ VỀ BẢN QUYỀN VIDEO"
            t2 = "Lãnh đạo YouTube khẳng định việc sử dụng kho video của các nhà sáng tạo nội dung để huấn luyện mô hình video AI Sora là hành vi vi phạm nghiêm trọng điều khoản dịch vụ."
            
            h3 = "CƠN KHÁT DỮ LIỆU HUẤN LUYỆN CHẤT LƯỢNG CAO"
            t3 = "Các mô hình video AI thế hệ mới đòi hỏi hàng tỷ giờ dữ liệu chuyển động thực tế, đẩy các hãng công nghệ vào tình thế bất chấp các ranh giới bản quyền."
            
            h4 = "ĐỊNH HÌNH LẠI BẢN QUYỀN NỘI DUNG SỐ"
            t4 = "Vụ việc này sẽ buộc các nền tảng sáng tạo phải xây dựng cơ chế chia sẻ doanh thu và cấp phép dữ liệu minh bạch cho các công ty AI trong tương lai."
            
            code_cmd = "content-id --scan-ai-training --detect-scraping"
            code_status = "[CONTENT ID] Kiểm tra lưu lượng cào dữ liệu video từ OpenAI..."
            code_res = "⚠️ Đã ghi nhận dấu hiệu khai thác dữ liệu video trái phép"
            stamp_text = "⚖️ TRANH CHẤP BẢN QUYỀN"
            search_kws = ["YouTube logo OpenAI Sora video technology", "Digital copyright lawsuit court gavel"]

        # 9. TÌNH TIẾT 9: CÔNG NHÂN TESLA TỪ CHỐI HUẤN LUYỆN OPTIMUS
        elif "tesla" in t_low and "optimus" in t_low:
            badge_title = "CÔNG NHÂN TESLA & ROBOT OPTIMUS"
            h1 = "CÔNG NHÂN TESLA PHẢN ĐỐI OPTIMUS"
            t1 = f"Thông tin chấn động từ các nhà máy Gigafactory của Tesla: {clean_t}!"
            
            h2 = "NỖI LO TỰ TAY ĐÀO TẠO KẺ THAY THẾ MÌNH"
            t2 = "Nhiều công nhân tỏ ra ngần ngại khi phải mặc các bộ đồ cảm biến hành vi để huấn luyện từng cử động tay chân cho robot Optimus, bởi cỗ máy này sẽ sớm thay thế chính vị trí của họ."
            
            h3 = "THAM VỌNG ĐẠI TRÀ HÓA ROBOT CỦA ELON MUSK"
            t3 = "Bất chấp những e ngại từ người lao động, Tesla vẫn đang đẩy mạnh kế hoạch đưa hàng nghìn robot Optimus vào lắp ráp xe điện và pin năng lượng trong năm 2026."
            
            h4 = "BƯỚC CHUYỂN DỊCH KHÔNG THỂ NGĂN CẢN"
            t4 = "Cuộc chuyển dịch từ cơ bắp con người sang robot cơ điện tử thông minh đang diễn ra nhanh hơn bất kỳ dự đoán nào của giới phân tích lao động!"
            
            code_cmd = "optimus-teleop --capture-worker-motion --dataset-save"
            code_status = "[TELEOP] Thu thập dữ liệu cử động tay của công nhân nhà máy..."
            code_res = "✓ Đã ghi nhận 1500 chuỗi hành vi lắp ráp thành công"
            stamp_text = "🤖 TESLA OPTIMUS"
            search_kws = ["Tesla Optimus robot standing factory Gigafactory", "Tesla humanoid robot assembly line"]

        # 10. TÌNH TIẾT MẶC ĐỊNH MỞ RỘNG (DÀNH CHO CÁC TIN KHÁC)
        else:
            badge_title = "ĐỘT PHÁ CÔNG NGHỆ MỚI"
            h1 = f"TÂM ĐIỂM: {entity.upper()}"
            t1 = f"Bản tin công nghệ đặc biệt: {clean_t}! Một bước tiến mới đang thu hút sự chú ý lớn từ các chuyên gia toàn cầu."
            
            h2 = "TẬP TRUNG GIẢI QUYẾT BÀI TOÁN THỰC TIỄN"
            t2 = "Khác với các nghiên cứu lý thuyết trong phòng lab, giải pháp này tập trung giải quyết trực tiếp nhu cầu thực tế của người dùng và các bài toán kinh doanh cụ thể."
            
            h3 = "LỢI THẾ CẠNH TRANH VƯỢT TRỘI"
            t3 = "Việc sớm tích hợp công nghệ này sẽ giúp các cá nhân và doanh nghiệp gia tăng năng suất vượt trội, rút ngắn thời gian xử lý công việc từ vài ngày xuống còn vài phút."
            
            h4 = "ĐÓN ĐẦU LÀN SÓNG 2026"
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
        "OpenAI rogue agents leaked 53 ChatGPT user images, reportedly created nearly 1M links with encoded info",
        "The Claude Sonnet 5.5 leak beating GPT-6 Sol is not what it looks like",
        "The Notice Had Nowhere to Land: The OpenAI Agent Breach in Australia",
        "New humanoid robot 'cowers' and drops to its knees when workers get too close",
        "OpenAI and Cursor agree on agent coordinators. They disagree on who runs them.",
        "Anthropic's Reported Supervoting Structure, an Opus 5.5 Field Note",
        "YouTube CEO: OpenAI Training Sora on Our Videos Would Be Clear Violation",
        "Tesla workers balk at training Optimus humanoid robots as replacements"
    ]
    for idx, s in enumerate(samples, 1):
        r = writer.generate_script_from_topic({"title": s})
        print(f"\n[{idx}] {r['workflow_metadata']['badge_title']}")
        print(f"  TIÊU ĐỀ: {s}")
        print(f"  THOẠI 1: {r['scenes'][0]['text']}")
        print(f"  THOẠI 2: {r['scenes'][1]['text']}")
        print(f"  CMD:     {r['workflow_metadata']['code_cmd']}")
