# 🤖 Lido AI Lab - Autonomous AI Tech Shorts Factory

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Ready-green?logo=ffmpeg)
![YouTube API](https://img.shields.io/badge/YouTube-Data%20API%20v3-red?logo=youtube)
![License](https://img.shields.io/badge/License-MIT-purple)

**Hệ thống AI Agents tự động hóa 100% quy trình sản xuất và đăng tải video YouTube Shorts công nghệ cao cho kênh [@LidoAILab](https://www.youtube.com/@LidoAILab).**

[Bản Trình Diễn Mẫu](https://www.youtube.com/shorts/g8s7ejfpesA) • [Cấu Trúc Hệ Thống](#-kiến-trúc-hệ-thống-agents) • [Hướng Dẫn Cài Đặt](#-hướng-dẫn-cài-đặt--vận-hành)

</div>

---

## 🌟 Các Tính Năng Đột Phá

### 1. 📡 Smart Trend Hunter & Anti-Duplicate Radar (`agents/trend_hunter.py`)
* **Quét đa nguồn toàn cầu theo thời gian thực**: Tự động lấy tin mới nhất từ hơn 10 nguồn uy tín (TechCrunch AI, The Verge, MIT Technology Review, HackerNews Trending AI, Google News US/Global/VN).
* **Cơ chế chống trùng lặp tuyệt đối (Semantic Keyword Overlap)**: Phân tích các thực thể và từ khóa trọng tâm của từng bài báo, so sánh với cơ sở dữ liệu `seen_news.json` để ngăn chặn 100% nguy cơ làm lại các đề tài cũ.

### 2. 🧐 Script Auditor & Quality Gate Agent (`agents/script_auditor.py`)
* **Kiểm duyệt chéo & Chống trùng lặp tuyệt đối**: Phân tích tương đồng câu chữ (Jaccard Similarity) với cơ sở dữ liệu `seen_scripts.json`. Tự động từ chối mọi kịch bản trùng lặp trên 35%.
* **Chặn đứng mọi mẫu câu sáo rỗng**: Ngăn chặn 100% các câu thoại dập khuôn chung chung.
* **Xác thực thực thể trọng tâm**: Đảm bảo từng kịch bản bám sát 100% tên hãng, dòng chip, model hay hành vi kỹ thuật trong bài báo.

### 3. 📸 Săn Ảnh Thực Tế Chuyên Sâu (`agents/visual_scout.py`)
* Tự động tìm kiếm hình ảnh báo chí, linh kiện, robot hoặc giao diện thực tế của từng chủ đề công nghệ.
* **Content Hashing Check**: Băm nội dung ảnh để loại bỏ trùng lặp ảnh ngay cả khi khác URL tải về.

### 4. 🎬 Step-by-Step Flow Animation Engine (`agents/step_flow_producer.py`)
* **Thiết kế đồ họa trực quan phong cách Lập trình viên**:
  * Hiển thị quy trình kỹ thuật: **Bước 1** $\rightarrow$ **Mũi tên động** $\rightarrow$ **Bước 2** $\rightarrow$ **Cửa sổ Terminal macOS gõ lệnh thời gian thực** $\rightarrow$ **Bước kiểm thử Unit Test & Tem bảo vệ**.
  * **Hình nền công nghệ sáng rõ 100%**: Sử dụng ảnh sản phẩm công nghệ thật, không bị tối đen hoặc làm mờ nhòe, kết hợp cùng lưới Cyan Matrix mỏng tạo cảm giác tương lai.
  * **Phụ đề Karaoke Highlight Cyan (`#00F5FF`)**: Tự động ngắt dòng thông minh (tối đa 6 từ/dòng), bắt sáng từng chữ chuẩn xác theo nhịp đọc.

### 5. 🛡️ Channel Security Guard & Auto Publisher (`channel_guard.py` & `agents/youtube_api_publisher.py`)
* **Rào chắn bảo mật nghiêm ngặt (`ChannelSecurityGuard`)**: Kiểm tra định tuyến kênh trước khi đăng tải. Bắt buộc Channel ID phải khớp chính xác với kênh `@LidoAILab` (`UCcegmQUbGsoFqRlQa_ULy7g`), ngăn ngừa hoàn toàn việc upload nhầm kênh.
* Tự động gắn thẻ tag, tiêu đề chuẩn SEO, mô tả đầy đủ nguồn tin và hashtag xu hướng.

### 6. ⏰ Tự Động Hóa Toàn Trình 24/7 (`auto_scheduler.py`)
* Tự động chạy nền tuần hoàn (mỗi 2 tiếng/chu kỳ).
* Chi tiết phân công kỹ năng xem tại: [TEAM_SKILLS.md](file:///Users/abc/.gemini/antigravity/scratch/lido_ai_lab/TEAM_SKILLS.md).

---

## 📁 Cấu Trúc Dự Án

```plaintext
lido-ai-lab/
├── README.md                     # Tài liệu hướng dẫn dự án
├── TEAM_SKILLS.md                # Bản đặc tả kỹ năng và quy trình phối hợp của Biệt đội AI Agents
├── auto_scheduler.py             # Tiến trình chạy nền tự động 24/7
├── channel_guard.py              # Bộ bảo vệ định tuyến an toàn kênh YouTube
├── seen_news.json                # Cơ sở dữ liệu lưu các tin tức đã sản xuất
├── seen_scripts.json             # Cơ sở dữ liệu lưu trữ kịch bản thoại để kiểm duyệt chéo
│
├── agents/                       # Hệ thống các AI Agents chuyên biệt
│   ├── trend_hunter.py           # Agent quét tin tức & lọc trùng
│   ├── script_auditor.py         # Agent kiểm duyệt chéo nội dung & chặn sáo rỗng
│   ├── visual_scout.py           # Agent săn ảnh thực tế & băm chống trùng
│   ├── script_writer.py          # Agent biên kịch phân cảnh kỹ thuật độc bản
│   ├── step_flow_producer.py     # Agent dựng video đồ họa chuyển động & Terminal
│   ├── youtube_api_publisher.py  # Agent đăng video lên YouTube qua API
│   ├── notifier.py               # Agent gửi thông báo hệ thống macOS
│   └── knowledge_expander.py     # Agent tự học và mở rộng kho từ khóa
│
├── credentials/                  # Thư mục chứa token xác thực (Được bảo mật)
│   ├── client_secret.json        # Google OAuth 2.0 Client credentials
│   └── token.json                # User access & refresh token
│
└── output/                       # Thư mục lưu trữ video thành phẩm (MP4)
```

---

## 🚀 Hướng Dẫn Cài Đặt & Vận Hành

### Bước 1: Clone kho mã nguồn
```bash
git clone https://github.com/tuanweb2026/lido-ai-lab.git
cd lido-ai-lab
```

### Bước 2: Thiết lập môi trường ảo
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt # hoặc cài đặt các gói bên dưới
pip install feedparser edge-tts Pillow google-api-python-client google-auth-oauthlib google-auth-httplib2
```

> **Lưu ý:** Yêu cầu máy đã cài đặt sẵn công cụ `ffmpeg`:
> ```bash
> brew install ffmpeg
> ```

### Bước 3: Cấu hình YouTube API
1. Tải file `client_secret.json` từ Google Cloud Console và đặt vào thư mục `credentials/client_secret.json`.
2. Chạy kịch bản ủy quyền lần đầu để tạo `token.json`:
   ```bash
   python3 auth_lido_ai_lab.py
   ```

### Bước 4: Khởi chạy hệ thống tự động
```bash
python3 auto_scheduler.py
```

---

## 🔒 Chính Sách Bảo Mật

* Toàn bộ mã ủy quyền OAuth2 (`credentials/token.json` và `credentials/client_secret.json`) đã được đưa vào `.gitignore` và không bao giờ được commit lên GitHub.
* Mọi hành vi đẩy video lên YouTube đều phải vượt qua bộ lọc kiểm tra Channel ID của `ChannelSecurityGuard`.

---

<div align="center">
Phát triển và bảo trợ bởi <b>Lido AI Lab</b> • 2026
</div>
