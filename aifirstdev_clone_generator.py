import os
import json
import unicodedata
import subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Kích thước chuẩn HD Shorts như mẫu video: 720 x 1280
WIDTH = 720
HEIGHT = 1280

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"

class AIFirstDevExactCloneEngine:
    """
    ENGINE MÔ PHỎNG 100% TỪNG CHI TIẾT CỦA AIFIRSTDEV:
    - Nền: Lưới Dark Perspective Grid sâu thẳm
    - Khung Badge: Viền Cyan Neon phát sáng, text in hoa sắc nét
    - Khung Card: Bo tròn 14px, viền Cyan Neon, bên trong có 3 chấm màu macOS và code/diagram động
    - Icon minh họa: Động cơ, chìa khóa, cờ lê, CPU, Anthropic, Cursor, Antigravity
    - Phụ đề (Subtitles): Đặt trong pill kính mờ bo tròn (y=920), chữ trắng và highlight từ khóa Cyan (#00F5FF)
    """
    def __init__(self, output_dir="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/output_clone"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.voice = "vi-VN-NamMinhNeural"

        # Fonts
        self.font_badge = ImageFont.truetype(FONT_BOLD, 20)
        self.font_card_head = ImageFont.truetype(FONT_MONO, 16)
        self.font_code = ImageFont.truetype(FONT_MONO, 15)
        self.font_diagram_title = ImageFont.truetype(FONT_BOLD, 28)
        self.font_diagram_box = ImageFont.truetype(FONT_BOLD, 22)
        self.font_sub = ImageFont.truetype(FONT_BOLD, 20)
        self.font_small = ImageFont.truetype(FONT_REGULAR, 14)

    def create_dark_matrix_background(self):
        """Tạo nền đen sâu với lưới ma trận và gradient vi tế như video mẫu"""
        bg = Image.new("RGB", (WIDTH, HEIGHT), (2, 4, 6))
        draw = ImageDraw.Draw(bg)
        
        # Grid caro mờ tối
        grid_step = 36
        for x in range(0, WIDTH, grid_step):
            draw.line([(x, 0), (x, HEIGHT)], fill=(5, 11, 14), width=1)
        for y in range(0, HEIGHT, grid_step):
            draw.line([(0, y), (WIDTH, y)], fill=(5, 11, 14), width=1)
            
        # Thêm ambient glow cực nhẹ ở giữa
        glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        gdraw.ellipse([WIDTH//2 - 250, 480 - 250, WIDTH//2 + 250, 480 + 250], fill=(0, 240, 255, 8))
        glow = glow.filter(ImageFilter.GaussianBlur(80))
        bg.paste(Image.alpha_composite(bg.convert("RGBA"), glow).convert("RGB"))
        return bg

    def draw_neon_pill(self, base_img, box, radius, outline_col=(0, 240, 255), fill_col=(0, 16, 22)):
        """Vẽ viền phát sáng chuẩn neon"""
        x0, y0, x1, y1 = box
        glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        for g in range(3, 0, -1):
            alpha = int(35 / g)
            gdraw.rounded_rectangle([x0-g*2, y0-g*2, x1+g*2, y1+g*2], radius=radius+g, outline=(outline_col[0], outline_col[1], outline_col[2], alpha), width=2)
        glow = glow.filter(ImageFilter.GaussianBlur(3))
        base_img.paste(Image.alpha_composite(base_img.convert("RGBA"), glow).convert("RGB"))
        
        draw = ImageDraw.Draw(base_img)
        draw.rounded_rectangle(box, radius=radius, fill=fill_col, outline=outline_col, width=2)
        return base_img

    def render_frame(self, scene_data, out_path):
        bg = self.create_dark_matrix_background()
        draw = ImageDraw.Draw(bg)
        cx = WIDTH // 2
        cy = 520

        card_type = scene_data.get("card_type", "code_window")
        
        # 1. Badge Pill (Hộp tiêu đề con phát sáng)
        badge_text = unicodedata.normalize("NFC", scene_data.get("badge", "AI AGENT"))
        bw, bh = 280, 44
        bx0, by0 = cx - bw//2, cy - 130
        bx1, by1 = bx0 + bw, by0 + bh

        b_outline = (255, 60, 80) if card_type == "warning" else (0, 240, 255)
        b_fill = (35, 10, 16) if card_type == "warning" else (0, 18, 24)
        bg = self.draw_neon_pill(bg, [bx0, by0, bx1, by1], radius=10, outline_col=b_outline, fill_col=b_fill)
        draw = ImageDraw.Draw(bg)
        bbox = draw.textbbox((0, 0), badge_text, font=self.font_badge)
        draw.text((cx - (bbox[2]-bbox[0])//2, by0 + 10), badge_text, font=self.font_badge, fill=b_outline)

        # 2. Main Card Content (Khung Card chính)
        if card_type == "code_window":
            cw, ch = 380, 220
            cx0, cy0 = cx - cw//2, by1 + 16
            cx1, cy1 = cx0 + cw, cy0 + ch
            bg = self.draw_neon_pill(bg, [cx0, cy0, cx1, cy1], radius=14, outline_col=(0, 190, 210), fill_col=(0, 12, 16))
            draw = ImageDraw.Draw(bg)
            
            # Mac Header (3 dots + window title)
            dy = cy0 + 16
            draw.ellipse([cx0 + 16, dy, cx0 + 24, dy + 8], fill=(255, 95, 86))
            draw.ellipse([cx0 + 30, dy, cx0 + 38, dy + 8], fill=(255, 189, 46))
            draw.ellipse([cx0 + 44, dy, cx0 + 52, dy + 8], fill=(39, 201, 63))
            
            w_title = unicodedata.normalize("NFC", scene_data.get("window_title", "agent · task"))
            draw.text((cx0 + 64, dy - 4), w_title, font=self.font_card_head, fill=(0, 220, 240))
            
            # Code lines
            ly = cy0 + 45
            for line in scene_data.get("lines", []):
                txt = unicodedata.normalize("NFC", line.get("text", ""))
                col = line.get("color", (210, 235, 245))
                draw.text((cx0 + 25, ly), txt, font=self.font_code, fill=col)
                ly += 26

        elif card_type == "architecture_diagram":
            # Kiểu so sánh Cursor vs Antigravity / Harness
            cw, ch = 300, 210
            y_box = by1 + 16
            # Trái
            bx_l = [cx - cw - 12, y_box, cx - 12, y_box + ch]
            draw.rounded_rectangle(bx_l, radius=16, outline=(220, 130, 20), width=2)
            draw.text(((bx_l[0] + bx_l[2])//2, y_box + 30), "Cursor", font=self.font_badge, fill=(240, 140, 30), anchor="mm")
            # Pill con
            pl = [bx_l[0] + 25, y_box + 55, bx_l[2] - 25, y_box + 140]
            draw.rounded_rectangle(pl, radius=12, fill=(18, 12, 35), outline=(130, 70, 240), width=2)
            draw.text(((pl[0] + pl[2])//2, y_box + 80), "model", font=self.font_small, fill=(180, 180, 200), anchor="mm")
            draw.text(((pl[0] + pl[2])//2, y_box + 115), "Opus 5", font=self.font_badge, fill=(255, 255, 255), anchor="mm")
            draw.text(((bx_l[0] + bx_l[2])//2, y_box + 175), "harness của hãng khác", font=self.font_small, fill=(160, 160, 170), anchor="mm")

            # Phải
            bx_r = [cx + 12, y_box, cx + cw + 12, y_box + ch]
            draw.rounded_rectangle(bx_r, radius=16, outline=(220, 130, 20), width=2)
            draw.text(((bx_r[0] + bx_r[2])//2, y_box + 30), "Antigravity", font=self.font_badge, fill=(240, 140, 30), anchor="mm")
            pr = [bx_r[0] + 25, y_box + 55, bx_r[2] - 25, y_box + 140]
            draw.rounded_rectangle(pr, radius=12, fill=(18, 12, 35), outline=(130, 70, 240), width=2)
            draw.text(((pr[0] + pr[2])//2, y_box + 80), "model", font=self.font_small, fill=(180, 180, 200), anchor="mm")
            draw.text(((pr[0] + pr[2])//2, y_box + 115), "Opus 5", font=self.font_badge, fill=(255, 255, 255), anchor="mm")
            draw.text(((bx_r[0] + bx_r[2])//2, y_box + 175), "harness của hãng khác", font=self.font_small, fill=(160, 160, 170), anchor="mm")

        elif card_type == "warning":
            cw, ch = 380, 200
            cx0, cy0 = cx - cw//2, by1 + 16
            cx1, cy1 = cx0 + cw, cy0 + ch
            bg = self.draw_neon_pill(bg, [cx0, cy0, cx1, cy1], radius=14, outline_col=(255, 60, 80), fill_col=(25, 8, 12))
            draw = ImageDraw.Draw(bg)
            
            draw.text((cx, cy0 + 35), "⚠ CẢNH BÁO AN TOÀN", font=self.font_badge, fill=(255, 80, 100), anchor="mm")
            draw.text((cx, cy0 + 75), "Phát hiện lệnh nguy hiểm hệ thống!", font=self.font_code, fill=(255, 255, 255), anchor="mm")
            draw.text((cx, cy0 + 115), "Agent Harness: ĐÃ CHẶN THÀNH CÔNG", font=self.font_code, fill=(255, 95, 86), anchor="mm")
            draw.text((cx, cy0 + 155), "Trạng thái: An toàn tuyệt đối 100%", font=self.font_code, fill=(46, 213, 115), anchor="mm")

        elif card_type == "cta":
            # Nút Like + Follow neon như cuối video mẫu
            y_box = by1 + 30
            # Nút Like Đỏ
            l_box = [cx - 160, y_box, cx - 15, y_box + 55]
            draw.rounded_rectangle(l_box, radius=10, fill=(25, 8, 12), outline=(255, 50, 70), width=2)
            draw.text(((l_box[0] + l_box[2])//2, y_box + 27), "♥ LIKE", font=self.font_badge, fill=(255, 60, 80), anchor="mm")

            # Nút Follow Cyan
            f_box = [cx + 15, y_box, cx + 160, y_box + 55]
            draw.rounded_rectangle(f_box, radius=10, fill=(0, 20, 28), outline=(0, 240, 255), width=2)
            draw.text(((f_box[0] + f_box[2])//2, y_box + 27), "+ FOLLOW", font=self.font_badge, fill=(0, 240, 255), anchor="mm")

            draw.text((cx, y_box + 105), "KHÁM PHÁ THÊM BÍ MẬT CÔNG NGHỆ", font=self.font_card_head, fill=(255, 189, 46), anchor="mm")
            draw.text((cx, y_box + 135), "YOUTUBE: @LIDO AI LAB", font=self.font_badge, fill=(0, 240, 255), anchor="mm")

        # 3. Phụ đề Pill chuẩn phong cách AIFirstDev (y=920)
        tokens = scene_data.get("tokens", [])
        if tokens:
            sub_y = 920
            total_w = sum(draw.textlength(t[0] + " ", font=self.font_sub) for t in tokens)
            pad_x, pad_y = 20, 10
            sbox = [cx - int(total_w)//2 - pad_x, sub_y - pad_y, cx + int(total_w)//2 + pad_x, sub_y + 24 + pad_y]
            draw.rounded_rectangle(sbox, radius=8, fill=(8, 14, 18), outline=(0, 180, 200, 80), width=1)
            
            cur_x = cx - int(total_w) // 2
            for word, is_hl in tokens:
                col = (0, 245, 255) if is_hl else (240, 245, 250)
                draw.text((cur_x, sub_y), word, font=self.font_sub, fill=col)
                cur_x += draw.textlength(word + " ", font=self.font_sub)

        bg.save(out_path, quality=95)

    async def generate_voice(self, text, out_audio):
        import asyncio
        for attempt in range(5):
            try:
                comm = edge_tts.Communicate(text, self.voice)
                await comm.save(out_audio)
                return
            except Exception as e:
                if attempt < 4:
                    await asyncio.sleep(2.0)
                else:
                    raise e

    def get_audio_duration(self, audio_path):
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(res.stdout.strip())

    async def produce_full_video(self, scenes, out_mp4):
        scene_files = []
        for idx, sc in enumerate(scenes, 1):
            img_p = os.path.join(self.output_dir, f"scene_{idx}.jpg")
            aud_p = os.path.join(self.output_dir, f"scene_{idx}.mp3")
            vid_p = os.path.join(self.output_dir, f"scene_{idx}.mp4")

            self.render_frame(sc, img_p)
            await self.generate_voice(sc["spoken"], aud_p)
            dur = self.get_audio_duration(aud_p) + 0.3

            cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", img_p, "-i", aud_p,
                "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p", "-t", str(dur), vid_p
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            scene_files.append(vid_p)

        concat_list = os.path.join(self.output_dir, "concat.txt")
        with open(concat_list, "w") as f:
            for vf in scene_files:
                f.write(f"file '{vf}'\n")

        cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", out_mp4]
        subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return out_mp4

async def main():
    engine = AIFirstDevExactCloneEngine()
    
    # Kịch bản bản tin AI bám sát 100% video mẫu AIFirstDev
    scenes = [
        {
            "badge": "AI AGENT",
            "card_type": "code_window",
            "window_title": "agent · task",
            "lines": [
                {"text": "> tự viết code...", "color": (0, 240, 255)},
                {"text": "function handlePayment(o) {", "color": (210, 235, 245)},
                {"text": "    return checkout(o);", "color": (210, 235, 245)},
                {"text": "}", "color": (210, 235, 245)},
                {"text": "✓ Executed in 12ms", "color": (46, 213, 115)}
            ],
            "spoken": "Vì sao các AI Code hàng đầu hiện nay lại có thể tự viết code và sửa lỗi liên tục?",
            "tokens": [("đầu", False), ("hiện", False), ("nay", False), ("lại", False), ("có", False), ("thể", False), ("tự", True), ("viết", True), ("code,", True)]
        },
        {
            "badge": "AGENT HARNESS",
            "card_type": "architecture_diagram",
            "spoken": "Bí mật nằm ở Agent Harness. Cùng một model Opus nhưng chạy trên các Harness khác nhau sẽ cho hiệu năng hoàn toàn khác biệt.",
            "tokens": [("của", False), ("Anthropic", False), ("trên", False), ("Cursor", True), ("hoặc", True), ("Antigravity", True)]
        },
        {
            "badge": "GHI LẠI THỜI GIAN THỰC",
            "card_type": "code_window",
            "window_title": "session.jsonl · append-only",
            "lines": [
                {"text": "+ {\"role\":\"user\",...}", "color": (210, 235, 245)},
                {"text": "+ {\"role\":\"assistant\",...}", "color": (210, 235, 245)},
                {"text": "+ {\"tool\":\"edit_file\",...}", "color": (0, 240, 255)},
                {"text": "+ {\"tool_result\":\"ok\",...}", "color": (46, 213, 115)},
                {"text": "+ {\"role\":\"assistant\",...}", "color": (210, 235, 245)}
            ],
            "spoken": "Agent Harness ghi lại toàn bộ lịch sử tin nhắn và kết quả công cụ theo thời gian thực mà không bao giờ bị mất dữ liệu.",
            "tokens": [("lại", False), ("mọi", False), ("tin", False), ("nhắn,", False), ("mọi", True), ("kết", True), ("quả", True), ("công", False), ("cụ", False)]
        },
        {
            "badge": "AN TOÀN HỆ THỐNG",
            "card_type": "warning",
            "spoken": "Quan trọng nhất, nó có cơ chế kiểm soát quyền hạn, ngăn chặn tuyệt đối AI vô tình phá hỏng máy tính của bạn.",
            "tokens": [("ngăn", True), ("chặn", True), ("AI", True), ("phá", True), ("hỏng", True), ("máy", False), ("tính", False)]
        },
        {
            "badge": "LIDO AI LAB",
            "card_type": "cta",
            "spoken": "Đăng ký kênh Lido AI Lab ngay hôm nay để làm chủ những bí mật công nghệ AI mới nhất!",
            "tokens": [("Like", True), ("và", False), ("Follow", True), ("Lido", True), ("AI", True), ("Lab", True)]
        }
    ]

    out_file = "/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/output_clone/aifirstdev_exact_short.mp4"
    await engine.produce_full_video(scenes, out_file)
    print("RENDER_COMPLETED:", out_file)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
