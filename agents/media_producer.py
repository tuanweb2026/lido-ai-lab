import asyncio
import os
import subprocess
import edge_tts
import unicodedata
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from agents.visual_scout import VisualAssetScoutAgent

FONT_UNICODE = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

class RealPhotoMediaProducerAgent:
    def __init__(self, 
                 images_dir="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/real_images",
                 output_dir="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/output"):
        self.images_dir = images_dir
        self.output_dir = output_dir
        self.scout = VisualAssetScoutAgent()
        # Giọng đọc Nam công nghệ Microsoft - Trầm ấm, đĩnh đạc, bản lĩnh chuyên gia
        self.voice = "vi-VN-NamMinhNeural"
        os.makedirs(self.output_dir, exist_ok=True)

        # Sử dụng Arial Unicode để không bao giờ bị ô vuông lỗi dấu tiếng Việt
        self.font_header = ImageFont.truetype(FONT_BOLD, 36)
        self.font_badge = ImageFont.truetype(FONT_UNICODE, 34)
        self.font_title = ImageFont.truetype(FONT_UNICODE, 48)
        self.font_code = ImageFont.truetype(FONT_UNICODE, 32)
        self.font_metric = ImageFont.truetype(FONT_UNICODE, 44)
        self.font_sub = ImageFont.truetype(FONT_UNICODE, 44)

    async def generate_voice_for_scene(self, text, out_audio_path):
        for attempt in range(5):
            try:
                communicate = edge_tts.Communicate(text, self.voice, rate="+3%", pitch="-2Hz")
                await communicate.save(out_audio_path)
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

    def draw_text_with_stroke(self, draw, pos, text, font, fill_col, stroke_col=(0, 0, 0), stroke_w=4, anchor="mm"):
        draw.text(pos, text, font=font, fill=fill_col, stroke_width=stroke_w, stroke_fill=stroke_col, anchor=anchor)

    def process_real_image_scene(self, scene, out_image_path):
        # --- PHONG CÁCH CHUẨN AIFIRSTDEV (CYBERPUNK NEON CARD & DARK GRID) ---
        width, height = 1080, 1920
        from datetime import datetime
        today_str = datetime.now().strftime("%d/%m/%Y")
        src_label = scene.get("source_label") or f"TIN TỨC CÔNG NGHỆ • {today_str} (HÔM NAY)"

        # 1. Dark Grid Background (Nền lưới ma trận tối sâu)
        bg = Image.new("RGBA", (width, height), (7, 10, 15, 255))
        draw_bg = ImageDraw.Draw(bg)
        grid_size = 64
        grid_col = (15, 22, 32, 140)
        for x in range(0, width, grid_size):
            draw_bg.line([(x, 0), (x, height)], fill=grid_col, width=1)
        for y in range(0, height, grid_size):
            draw_bg.line([(0, y), (width, y)], fill=grid_col, width=1)

        # Ambient Glow
        glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        cx, cy = width // 2, height // 2 - 120
        gdraw.ellipse([cx - 420, cy - 420, cx + 420, cy + 420], fill=(0, 230, 255, 12))
        glow = glow.filter(ImageFilter.GaussianBlur(90))
        bg = Image.alpha_composite(bg, glow)

        # 2. Top Header: Nguồn tin & Ngày thực tế
        draw = ImageDraw.Draw(bg)
        draw.rounded_rectangle([width//2 - 450, 75, width//2 + 450, 155], radius=15, fill=(10, 20, 32, 230), outline=(0, 240, 255, 200), width=2)
        self.draw_text_with_stroke(draw, (width // 2, 115), f"NGUỒN: {src_label}", self.font_header, (0, 240, 255), stroke_w=0)

        # 3. Badge Pill phía trên card (vd: SYSTEM ARCHITECTURE, AGENT HARNESS)
        badge_text = unicodedata.normalize("NFC", scene.get("metric_badge", "TIN NÓNG 24H"))
        is_warning = any(w in scene.get("headline", "").lower() for w in ["cảnh báo", "nguy hiểm", "lỗ hổng", "hack", "sập"])
        
        bw, bh = 420, 68
        bx0, by0 = cx - bw//2, cy - 280
        bx1, by1 = bx0 + bw, by0 + bh
        b_out = (255, 60, 80) if is_warning else (0, 240, 255)
        b_fill = (35, 12, 18, 240) if is_warning else (10, 28, 42, 240)
        
        draw.rounded_rectangle([bx0, by0, bx1, by1], radius=16, fill=b_fill, outline=b_out, width=2)
        bbox = draw.textbbox((0, 0), badge_text, font=self.font_badge)
        draw.text((cx - (bbox[2]-bbox[0])//2, by0 + 14), badge_text, font=self.font_badge, fill=b_out)

        # 4. Main Cyberpunk Terminal Card (Khung card bo tròn phát sáng)
        cw, ch = 920, 520
        cx0, cy0 = cx - cw//2, by1 + 32
        cx1, cy1 = cx0 + cw, cy0 + ch
        c_out = (255, 50, 70) if is_warning else (0, 220, 240)
        c_fill = (20, 10, 14, 245) if is_warning else (9, 15, 25, 245)

        # Vẽ viền phát sáng (Glow border)
        for g in range(3, 0, -1):
            alpha = int(35 / g)
            draw.rounded_rectangle([cx0 - g*2, cy0 - g*2, cx1 + g*2, cy1 + g*2], radius=24+g*2, 
                                   outline=(c_out[0], c_out[1], c_out[2], alpha), width=2)
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=24, fill=c_fill, outline=c_out, width=3)

        # Card Top Bar: 3 dots Mac style + Window Title
        dy = cy0 + 26
        draw.ellipse([cx0 + 28, dy, cx0 + 40, dy + 12], fill=(255, 95, 86))
        draw.ellipse([cx0 + 48, dy, cx0 + 60, dy + 12], fill=(255, 189, 46))
        draw.ellipse([cx0 + 68, dy, cx0 + 80, dy + 12], fill=(39, 201, 63))
        
        headline_title = scene.get("headline", "AI Architecture · Analysis")
        draw.text((cx0 + 98, dy - 6), headline_title[:45], font=self.font_code, fill=(0, 210, 230))
        draw.line([(cx0, cy0 + 56), (cx1, cy0 + 56)], fill=(c_out[0], c_out[1], c_out[2], 90), width=1)

        # Nội dung dòng lệnh/phân tích bên trong Card
        overlay_txt = scene.get("overlay_data", "")
        lines = [
            f"> Tác vụ: {scene.get('headline', '')[:35]}",
            f"Điểm nhấn: {overlay_txt[:40]}",
            "────────────────────────────────────────",
            f"Trạng thái: Hoạt động thời gian thực [OK]",
            "Hiệu suất: Vượt trội & Tối ưu hóa 100%"
        ]
        ly = cy0 + 85
        line_colors = [
            (0, 240, 255), (255, 189, 46), (80, 100, 120), (46, 213, 115), (230, 240, 250)
        ]
        for l_idx, l_str in enumerate(lines):
            draw.text((cx0 + 38, ly), unicodedata.normalize("NFC", l_str), font=self.font_code, fill=line_colors[l_idx % len(line_colors)])
            ly += 54

        # 5. Phụ đề dưới màn hình (Subtitles với Highlight từ khóa Cyan)
        sub_text = unicodedata.normalize("NFC", scene["text"])
        words = sub_text.split()
        
        # Tách dòng phụ đề tự động (tối đa 6-7 từ 1 dòng để giữ mắt người xem)
        sub_lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 24:
                sub_lines.append(" ".join(cur))
                cur = []
        if cur:
            sub_lines.append(" ".join(cur))

        # Hiển thị 2-3 dòng phụ đề nổi bật với hộp nền mờ bo góc
        sy = height - 440
        for l_text in sub_lines[:2]:
            l_words = l_text.split()
            total_w = sum(draw.textlength(w + " ", font=self.font_sub) for w in l_words)
            pad_x, pad_y = 36, 16
            s_box = [cx - int(total_w)//2 - pad_x, sy - pad_y, cx + int(total_w)//2 + pad_x, sy + 56 + pad_y]
            draw.rounded_rectangle(s_box, radius=18, fill=(5, 9, 15, 220), outline=(0, 220, 240, 110), width=1)
            
            cur_x = cx - int(total_w) // 2
            for w in l_words:
                # Highlight các từ kỹ thuật quan trọng
                is_hl = any(hw in w.lower() for hw in ["ai", "mô hình", "robot", "hệ thống", "tự động", "code", "mạnh", "đột phá", "claude", "gpt", "gemini", "nvidia", "chip"])
                col = (0, 245, 255) if is_hl else (255, 255, 255)
                draw.text((cur_x, sy), w, font=self.font_sub, fill=col)
                cur_x += draw.textlength(w + " ", font=self.font_sub)
            sy += 90

        # 6. Call To Action Subscribe nhỏ gọn ở đáy
        draw.rounded_rectangle([width//2 - 380, 1720, width//2 + 380, 1800], radius=20, fill=(10, 25, 40, 230), outline=(0, 240, 255, 200), width=2)
        self.draw_text_with_stroke(draw, (width // 2, 1760), "SUBSCRIBE: YOUTUBE.COM/@LidoAILab", self.font_header, (0, 240, 255), stroke_w=0)

        bg.convert("RGB").save(out_image_path, quality=95)

    async def produce_real_photo_short(self, scenes):
        scene_files = []
        print(f"[RealPhotoProducer] Dựng {len(scenes)} cảnh với FONT TIẾNG VIỆT SIÊU TO & ẢNH THẬT RÕ NÉT...")

        for s in scenes:
            sid = s["scene_id"]
            audio_f = os.path.join(self.output_dir, f"v2_audio_{sid}.mp3")
            img_f = os.path.join(self.output_dir, f"v2_img_{sid}.jpg")
            video_f = os.path.join(self.output_dir, f"v2_scene_{sid}.mp4")

            await self.generate_voice_for_scene(s["text"], audio_f)
            dur = self.get_audio_duration(audio_f)

            self.process_real_image_scene(s, img_f)

            # Ghép video và sóng âm Cyan
            filter_complex = (
                f"[1:a]showwaves=s=760x100:mode=p2p:colors=0x00f0ff|0xffcc00:scale=sqrt[w];"
                f"[0:v][w]overlay=x=(W-w)/2:y=1600:shortest=1[out]"
            )
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-framerate", "30", "-t", str(dur), "-i", img_f,
                "-i", audio_f,
                "-filter_complex", filter_complex,
                "-map", "[out]", "-map", "1:a",
                "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest", video_f
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            scene_files.append(video_f)
            print(f" -> Xong cảnh {sid}/{len(scenes)} ({dur:.2f}s)")

        # Ghép video
        concat_txt = os.path.join(self.output_dir, "v2_concat.txt")
        with open(concat_txt, "w") as f:
            for vf in scene_files:
                f.write(f"file '{vf}'\n")

        final_short = os.path.join(self.output_dir, "lido_ai_fixed_short.mp4")
        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_txt,
            "-c", "copy",
            final_short
        ]
        subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(f"[RealPhotoProducer] 🔥 ĐÃ XUẤT VIDEO SỬA LỖI HOÀN HẢO: {final_short}")
        return final_short
