# 🤖 Lido AI Lab - Autonomous AI Tech Shorts Factory

Hệ thống AI Agents tự động hóa 100% quy trình sản xuất và đăng tải video YouTube Shorts công nghệ cao cho kênh **@LidoAILab**.

---

## 🌟 Tính Năng Nổi Bật

1. **Smart Trend Radar (`agents/trend_hunter.py`)**:
   - Quét thời gian thực 10+ kênh công nghệ hàng đầu thế giới (TechCrunch, The Verge, MIT Technology Review, Google News US & Global).
   - Cơ chế lọc trùng thông minh (Semantic Keyword Overlap) đảm bảo không bao giờ làm trùng tin tức đã sản xuất.

2. **Visual Asset Scout (`agents/visual_scout.py`)**:
   - Tự động tìm kiếm và tải hình ảnh báo chí / sản phẩm công nghệ thật với độ phân giải cao.
   - Cơ chế chống trùng lặp hình ảnh bằng mã băm nội dung (Content Hashing).

3. **Step-by-Step Flow Animation Engine (`agents/step_flow_producer.py`)**:
   - Dựng phim hoạt họa quy trình kỹ thuật chuyển động mượt mà (30 FPS).
   - Hiệu ứng gõ code trực tiếp trên Terminal macOS, mũi tên động, tem chứng nhận an toàn.
   - Phụ đề chạy chữ Karaoke Highlight màu Cyan (`#00F5FF`) đồng bộ chuẩn xác theo từng từ của giọng đọc AI.
   - Hình nền công nghệ sáng rõ 100%, không bị tối đen hay mờ ảo.

4. **Kênh An Toàn & Tự Động Upload (`channel_guard.py` & `agents/youtube_api_publisher.py`)**:
   - Rào chắn bảo mật nghiêm ngặt (`ChannelSecurityGuard`): chỉ cho phép xuất bản lên đúng Channel ID của kênh `@LidoAILab`.
   - Đăng tải trực tiếp qua YouTube Data API v3 (OAuth2).

5. **Bộ Lập Lịch Tự Động (`auto_scheduler.py`)**:
   - Chạy nền 24/7, tự động quét tin và sản xuất video mới theo chu kỳ định kỳ.
   - Gửi thông báo native trên macOS kèm đường link video sau khi xuất bản.

---

## 🚀 Cài Đặt & Sử Dụng

### 1. Chuẩn bị môi trường
```bash
python3 -m venv venv
source venv/bin/activate
pip install feedparser edge-tts Pillow google-api-python-client google-auth-oauthlib google-auth-httplib2
```

### 2. Thiết lập xác thực YouTube Data API
Đặt file `client_secret.json` vào thư mục `credentials/` và kích hoạt OAuth2:
```bash
python3 auth_lido_ai_lab.py
```

### 3. Chạy chu kỳ tự động
```bash
python3 auto_scheduler.py
```
