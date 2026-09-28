import asyncio
import os
import subprocess
import unicodedata
import edge_tts
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from agents.visual_scout import VisualAssetScoutAgent

WIDTH, HEIGHT = 720, 1280
FPS = 30

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"

class StepFlowMediaProducerAgent:
    """
    ENGINE DỰNG PHIM HOẠT HỌA CHUYỂN ĐỘNG KỸ THUẬT (STEP-BY-STEP FLOW ANIMATION):
    - Tự động săn ảnh công nghệ / báo chí thật liên quan đến chủ đề tin tức (VisualAssetScout)
    - Xử lý nền Cinematic Tech: Ảnh mờ nhẹ nghệ thuật kết hợp lưới Cyan Grid và vignette tạo chiều sâu
    - Quy trình từng bước lập trình viên: Bước 1 -> Mũi tên -> Bước 2 -> Terminal gõ code từng chữ -> Bước 4 Unit Test
    - Con dấu an toàn bảo vệ hệ thống
    - Phụ đề Karaoke Highlight màu Cyan (#00F5FF) chia dòng chuẩn xác theo nhịp nói
    """
    def __init__(self, output_dir="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.scout = VisualAssetScoutAgent()
        self.voice = "vi-VN-NamMinhNeural"

        self.font_title = ImageFont.truetype(FONT_BOLD, 22)
        self.font_box = ImageFont.truetype(FONT_BOLD, 18)
        self.font_mono = ImageFont.truetype(FONT_MONO, 16)
        self.font_sub = ImageFont.truetype(FONT_BOLD, 20)
        self.font_stamp = ImageFont.truetype(FONT_BOLD, 24)

    async def generate_voice_for_text(self, text, out_audio_path):
        for attempt in range(5):
            try:
                comm = edge_tts.Communicate(text, self.voice, rate="+4%")
                await comm.save(out_audio_path)
                return
            except Exception as e:
                if attempt < 4:
                    await asyncio.sleep(2.0)
                else:
                    raise e

    def get_audio_duration(self, audio_path):
        cmd = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", audio_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(res.stdout.strip())

    def prepare_topic_cinematic_background(self, topic_keywords, topic_title):
        """
        Tự động tìm kiếm ảnh tin tức/công nghệ thật tương ứng và xử lý thành nền Cyberpunk điện ảnh:
        - Giữ lại nhận diện thực tế của hãng/công nghệ (OpenAI, ChatGPT, Robot, Claude, Nvidia...)
        - Hòa trộn ánh sáng tối mờ và lưới Cyan Matrix huyền ảo
        """
        search_queries = []
        if topic_keywords:
            search_queries.extend([f"{k} technology official" for k in topic_keywords[:3]])
        search_queries.append(f"{topic_title[:35]} news photo")

        raw_img_path = self.scout.get_diverse_images_for_scene(search_queries)
        
        try:
            raw = Image.open(raw_img_path).convert('RGB')
            rw, rh = raw.size
            
            # Giữ ảnh nền sáng rõ 100% (KHÔNG BLUR, KHÔNG LÀM TỐI ĐEN)
            scale = max(WIDTH / rw, HEIGHT / rh)
            nw, nh = int(rw * scale), int(rh * scale)
            raw_resized = raw.resize((nw, nh), Image.Resampling.LANCZOS)
            left = (nw - WIDTH) // 2
            top = (nh - HEIGHT) // 2
            base = raw_resized.crop((left, top, left + WIDTH, top + HEIGHT))

            # Phủ một lớp lưới công nghệ Cyan nhẹ nhàng, giữ trọn độ sáng và chi tiết của ảnh
            overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
            odraw = ImageDraw.Draw(overlay)

            # Lưới Cyan công nghệ mờ siêu mảnh
            for x in range(0, WIDTH, 45):
                odraw.line([(x, 0), (x, HEIGHT)], fill=(0, 240, 255, 25), width=1)
            for y in range(0, HEIGHT, 45):
                odraw.line([(0, y), (WIDTH, y)], fill=(0, 240, 255, 25), width=1)

            return Image.alpha_composite(base.convert('RGBA'), overlay).convert('RGB')
        except Exception as e:
            print(f"[StepFlowProducer] Lỗi render nền ảnh: {e}, fallback sang nền lưới tiêu chuẩn.")
            img = Image.new("RGB", (WIDTH, HEIGHT), (2, 4, 6))
            draw = ImageDraw.Draw(img)
            for x in range(0, WIDTH, 36):
                draw.line([(x, 0), (x, HEIGHT)], fill=(6, 12, 16), width=1)
            for y in range(0, HEIGHT, 36):
                draw.line([(0, y), (WIDTH, y)], fill=(6, 12, 16), width=1)
            return img

    def render_workflow_frame(self, bg_img, t, total_dur, workflow_meta, current_sub_text, hl_word):
        img = bg_img.copy()
        draw = ImageDraw.Draw(img)
        cx = WIDTH // 2

        # Header Badge
        badge_txt = workflow_meta.get("badge_title", "QUY TRÌNH KỸ THUẬT AI")
        bbox = draw.textbbox((0, 0), badge_txt, font=self.font_title)
        bw = (bbox[2] - bbox[0]) + 40
        t_box = [cx - bw//2, 335, cx + bw//2, 385]
        draw.rounded_rectangle(t_box, radius=8, outline=(0, 240, 255), width=2, fill=(0, 20, 28))
        draw.text((cx - (bbox[2]-bbox[0])//2, 348), badge_txt, font=self.font_title, fill=(0, 240, 255))

        # Bước 1: Khởi động / Input (Hiện từ t >= 0s)
        y1 = 410
        step1_txt = unicodedata.normalize("NFC", workflow_meta.get("step1", "Bước 1: Tiếp nhận dữ liệu & Yêu cầu")[:38])
        s1_bbox = draw.textbbox((0, 0), step1_txt, font=self.font_box)
        draw.rounded_rectangle([cx - 210, y1, cx + 210, y1 + 45], radius=10, outline=(0, 180, 200), width=1, fill=(10, 25, 35))
        draw.text((cx - (s1_bbox[2]-s1_bbox[0])//2, y1 + 12), step1_txt, font=self.font_box, fill=(230, 245, 255))

        # Mũi tên 1: t >= 18% thời lượng
        t_arr1 = total_dur * 0.18
        if t >= t_arr1:
            draw.line([(cx, y1 + 48), (cx, y1 + 72)], fill=(0, 240, 255), width=2)
            draw.polygon([(cx, y1 + 76), (cx - 5, y1 + 68), (cx + 5, y1 + 68)], fill=(0, 240, 255))

        # Bước 2: Phân tích / Xử lý (t >= 22% thời lượng)
        t_step2 = total_dur * 0.22
        if t >= t_step2:
            y2 = y1 + 80
            step2_txt = unicodedata.normalize("NFC", workflow_meta.get("step2", "Bước 2: Phân tích kiến trúc & Lập kế hoạch")[:38])
            s2_bbox = draw.textbbox((0, 0), step2_txt, font=self.font_box)
            glow2 = (0, 240, 255) if (t < total_dur * 0.42) else (0, 140, 160)
            draw.rounded_rectangle([cx - 210, y2, cx + 210, y2 + 45], radius=10, outline=glow2, width=2, fill=(10, 30, 42))
            draw.text((cx - (s2_bbox[2]-s2_bbox[0])//2, y2 + 12), step2_txt, font=self.font_box, fill=(255, 255, 255))

        # Mũi tên 2: t >= 40% thời lượng
        t_arr2 = total_dur * 0.40
        if t >= t_arr2:
            y2 = y1 + 80
            draw.line([(cx, y2 + 48), (cx, y2 + 72)], fill=(0, 240, 255), width=2)
            draw.polygon([(cx, y2 + 76), (cx - 5, y2 + 68), (cx + 5, y2 + 68)], fill=(0, 240, 255))

        # Bước 3: Terminal gõ lệnh / Thực thi code (t >= 42% thời lượng)
        t_step3 = total_dur * 0.42
        if t >= t_step3:
            y3 = y1 + 160
            cw, ch = 440, 145
            cx0, cy0 = cx - cw//2, y3
            draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=12, outline=(0, 240, 255), width=2, fill=(8, 14, 20))
            # Mac dots
            draw.ellipse([cx0 + 14, cy0 + 12, cx0 + 22, cy0 + 20], fill=(255, 95, 86))
            draw.ellipse([cx0 + 28, cy0 + 12, cx0 + 36, cy0 + 20], fill=(255, 189, 46))
            draw.ellipse([cx0 + 42, cy0 + 12, cx0 + 50, cy0 + 20], fill=(39, 201, 63))
            term_title = workflow_meta.get("term_title", "terminal · agent runtime")
            draw.text((cx0 + 60, cy0 + 9), term_title, font=self.font_mono, fill=(0, 180, 200))
            draw.line([(cx0, cy0 + 32), (cx0 + cw, cy0 + 32)], fill=(0, 100, 120), width=1)

            full_cmd = workflow_meta.get("code_cmd", "agent refactor --fix-all")
            elapsed_type = max(0.0, t - t_step3)
            chars_to_show = int(elapsed_type * 18)
            shown_cmd = full_cmd[:chars_to_show]
            cursor_blink = "_" if (int(t * 4) % 2 == 0 and chars_to_show < len(full_cmd)) else ""
            draw.text((cx0 + 20, cy0 + 48), f"> {shown_cmd}{cursor_blink}", font=self.font_mono, fill=(0, 240, 255))

            if chars_to_show >= len(full_cmd):
                status_txt = workflow_meta.get("code_status", "[RUN] Quét toàn bộ hệ thống...")
                draw.text((cx0 + 20, cy0 + 78), status_txt[:40], font=self.font_mono, fill=(255, 189, 46))
                if elapsed_type >= 2.0:
                    ok_txt = workflow_meta.get("code_result", "✓ Xử lý thành công trong 0.8s")
                    draw.text((cx0 + 20, cy0 + 104), ok_txt[:40], font=self.font_mono, fill=(46, 213, 115))

        # Mũi tên 3: t >= 72% thời lượng
        t_arr3 = total_dur * 0.72
        if t >= t_arr3:
            draw.line([(cx, y1 + 308), (cx, y1 + 332)], fill=(46, 213, 115), width=2)
            draw.polygon([(cx, y1 + 336), (cx - 5, y1 + 328), (cx + 5, y1 + 328)], fill=(46, 213, 115))

        # Bước 4: Kiểm thử / Hoàn thành (t >= 74% thời lượng)
        t_step4 = total_dur * 0.74
        if t >= t_step4:
            y4 = y1 + 340
            step4_txt = unicodedata.normalize("NFC", workflow_meta.get("step4", "✓ Bước 4: Tự động chạy Unit Test")[:38])
            s4_bbox = draw.textbbox((0, 0), step4_txt, font=self.font_box)
            draw.rounded_rectangle([cx - 210, y4, cx + 210, y4 + 45], radius=10, outline=(46, 213, 115), width=2, fill=(10, 36, 24))
            draw.text((cx - (s4_bbox[2]-s4_bbox[0])//2, y4 + 12), step4_txt, font=self.font_box, fill=(46, 213, 115))

        # Đóng dấu bảo vệ / Kêu gọi hành động (t >= 88% thời lượng)
        t_stamp = total_dur * 0.88
        if t >= t_stamp:
            stamp_txt = workflow_meta.get("stamp_text", "🔒 BẢO VỆ TOÀN DIỆN")
            sx, sy = cx - 140, 810
            draw.rounded_rectangle([sx, sy, sx + 280, sy + 50], radius=8, outline=(255, 50, 70), width=3, fill=(35, 10, 16))
            bbox = draw.textbbox((0, 0), stamp_txt, font=self.font_stamp)
            draw.text((cx - (bbox[2]-bbox[0])//2, sy + 11), stamp_txt, font=self.font_stamp, fill=(255, 60, 80))

        # Phụ đề Karaoke Highlight màu Cyan (#00F5FF) chia dòng chuẩn
        if current_sub_text:
            raw_words = current_sub_text.split()
            chunks = []
            cur_c = []
            for w in raw_words:
                cur_c.append(w)
                if len(" ".join(cur_c)) >= 28 or len(cur_c) >= 6:
                    chunks.append(" ".join(cur_c))
                    cur_c = []
            if cur_c:
                chunks.append(" ".join(cur_c))

            sub_display = chunks[0] if chunks else ""
            if len(chunks) > 1:
                chunk_idx = int((t * 2.2) % len(chunks))
                sub_display = chunks[chunk_idx]

            s_words = sub_display.split()
            total_w = sum(draw.textlength(w + " ", font=self.font_sub) for w in s_words)
            sb = [cx - int(total_w)//2 - 16, 920, cx + int(total_w)//2 + 16, 965]
            draw.rounded_rectangle(sb, radius=8, fill=(8, 14, 18), outline=(0, 180, 200, 100), width=1)
            
            cur_x = cx - int(total_w) // 2
            for w in s_words:
                col = (0, 245, 255) if (hl_word and hl_word.lower() in w.lower()) else (240, 245, 250)
                draw.text((cur_x, 930), w, font=self.font_sub, fill=col)
                cur_x += draw.textlength(w + " ", font=self.font_sub)

        return img

    async def produce_step_animated_short(self, script_data, topic_info=None):
        """Sản xuất video chuyển động hoàn chỉnh với hình nền công nghệ riêng biệt cho từng tin tức"""
        scenes = script_data["scenes"]
        full_text = " ".join([s["text"] for s in scenes])
        
        audio_file = os.path.join(self.output_dir, "temp_step_voice.mp3")
        final_mp4 = os.path.join(self.output_dir, "lido_step_animated_short.mp4")

        print("[StepFlowProducer] 1. Tạo audio giọng đọc AI thuyết minh...")
        await self.generate_voice_for_text(full_text, audio_file)
        duration = self.get_audio_duration(audio_file)
        print(f" -> Thời lượng video: {duration:.2f}s")

        # 2. Chuẩn bị hình nền công nghệ/tin tức tương ứng
        print("[StepFlowProducer] 2. Tự động săn ảnh và chuẩn bị nền công nghệ tương ứng cho tin tức...")
        kw_list = []
        if topic_info:
            kw_list = topic_info.get("keywords", [])
        if not kw_list and scenes:
            kw_list = scenes[0].get("search_keywords", [])
            
        topic_title = topic_info.get("title", script_data.get("title", "AI Technology")) if topic_info else script_data.get("title", "AI Technology")
        tech_bg = self.prepare_topic_cinematic_background(kw_list, topic_title)

        # Chuẩn bị metadata cho các bước dựa trên kịch bản (đồng bộ 100% theo từng thể loại)
        meta = script_data.get("workflow_metadata", {})
        if not meta:
            meta = {
                "badge_title": scenes[0].get("metric_badge", "QUY TRÌNH KỸ THUẬT AI").upper()[:28],
                "step1": f"Bước 1: {scenes[0].get('headline', 'Nhận dữ liệu & Yêu cầu')}",
                "step2": f"Bước 2: {scenes[1].get('headline', 'Phân tích & Lập kế hoạch')}",
                "term_title": "terminal · agent engine",
                "code_cmd": "agent run optimize --production",
                "code_status": f"[RUN] {scenes[2].get('overlay_data', 'Thực thi lệnh...')[:30]}",
                "code_result": "✓ Xử lý hoàn tất trong 0.8s",
                "step4": f"✓ Bước 4: {scenes[3].get('headline', 'Kiểm thử & Tối ưu')}",
                "stamp_text": "🔒 BẢO VỆ TOÀN DIỆN"
            }

        # Tính toán phân đoạn phụ đề theo thời gian
        scene_dur = duration / len(scenes)
        total_frames = int(duration * FPS) + 15
        print(f"[StepFlowProducer] 3. Render {total_frames} frames chuyển động mượt mà (30 FPS)...")

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-f", "rawvideo", "-vcodec", "rawvideo",
            "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24",
            "-r", str(FPS), "-i", "-",
            "-i", audio_file,
            "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", final_mp4
        ]

        pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        for f_idx in range(total_frames):
            t = f_idx / FPS
            cur_scene_idx = min(int(t / scene_dur), len(scenes) - 1)
            cur_scene = scenes[cur_scene_idx]
            
            hl = "AI"
            words = cur_scene["text"].split()
            for w in words:
                if any(hw in w.lower() for hw in ["tự", "lệnh", "code", "agent", "robot", "mô hình", "nhanh", "an toàn"]):
                    hl = w
                    break

            frame = self.render_workflow_frame(tech_bg, t, duration, meta, cur_scene["text"], hl)
            pipe.stdin.write(frame.tobytes())

        pipe.stdin.close()
        pipe.wait()
        print(f"[StepFlowProducer] 4. 🔥 XUẤT VIDEO CHUYỂN ĐỘNG NỀN CÔNG NGHỆ THÀNH CÔNG: {final_mp4}")
        return final_mp4
