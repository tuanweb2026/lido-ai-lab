import asyncio
import os
import json
import unicodedata
import subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"

class AIFirstDevProducer:
    """
    Template Studio đẳng cấp mô phỏng 100% phong cách AIFirstDev:
    - Nhịp điệu: Giảng giải kỹ thuật cực sâu, logic, gãy gọn, không giật gân rẻ tiền.
    - Thị giác: Dark Matrix Grid + Cyberpunk Neon Glowing Cards + Terminal Code Windows.
    - Âm thanh: Microsoft TTS Nam Minh đĩnh đạc kết hợp âm báo công nghệ.
    """
    def __init__(self, output_dir="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/output_aifirstdev"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.width = 1080
        self.height = 1920
        self.voice = "vi-VN-NamMinhNeural"

        # Fonts
        self.font_badge = ImageFont.truetype(FONT_BOLD, 36)
        self.font_title = ImageFont.truetype(FONT_BOLD, 46)
        self.font_code = ImageFont.truetype(FONT_MONO, 34)
        self.font_sub_bold = ImageFont.truetype(FONT_BOLD, 46)
        self.font_sub_reg = ImageFont.truetype(FONT_REGULAR, 46)

    def create_background(self):
        bg = Image.new("RGBA", (self.width, self.height), (6, 9, 14, 255))
        draw = ImageDraw.Draw(bg)
        grid_size = 64
        grid_color = (15, 23, 35, 140)
        for x in range(0, self.width, grid_size):
            draw.line([(x, 0), (x, self.height)], fill=grid_color, width=1)
        for y in range(0, self.height, grid_size):
            draw.line([(0, y), (self.width, y)], fill=grid_color, width=1)
            
        glow = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        cx, cy = self.width // 2, self.height // 2 - 120
        gdraw.ellipse([cx - 420, cy - 420, cx + 420, cy + 420], fill=(0, 230, 255, 14))
        glow = glow.filter(ImageFilter.GaussianBlur(90))
        return Image.alpha_composite(bg, glow)

    def draw_glowing_card(self, base_img, box, radius=24, outline=(0, 240, 255, 220), fill=(10, 16, 26, 240)):
        x0, y0, x1, y1 = box
        glow = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        for g in range(3, 0, -1):
            alpha = int(35 / g)
            gdraw.rounded_rectangle([x0 - g*2, y0 - g*2, x1 + g*2, y1 + g*2], radius=radius+g*2, 
                                    outline=(outline[0], outline[1], outline[2], alpha), width=2)
        glow = glow.filter(ImageFilter.GaussianBlur(4))
        base_img = Image.alpha_composite(base_img, glow)
        
        draw = ImageDraw.Draw(base_img)
        draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=3)
        return base_img

    def render_scene_frame(self, scene_data, out_path):
        img = self.create_background()
        draw = ImageDraw.Draw(img)
        
        cx = self.width // 2
        cy = self.height // 2 - 80
        
        badge_text = unicodedata.normalize("NFC", scene_data.get("badge", "SYSTEM ARCHITECTURE"))
        card_type = scene_data.get("type", "code")
        
        # 1. Badge Pill
        badge_w, badge_h = 360, 68
        bx0 = cx - badge_w // 2
        by0 = cy - 300
        bx1 = bx0 + badge_w
        by1 = by0 + badge_h
        
        badge_outline = (255, 60, 80, 240) if card_type == "warning" else (0, 240, 255, 240)
        badge_fill = (35, 12, 18, 245) if card_type == "warning" else (10, 30, 42, 245)
        badge_text_col = (255, 80, 100, 255) if card_type == "warning" else (0, 240, 255, 255)
        
        img = self.draw_glowing_card(img, [bx0, by0, bx1, by1], radius=18, outline=badge_outline, fill=badge_fill)
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), badge_text, font=self.font_badge)
        draw.text((cx - (bbox[2]-bbox[0])//2, by0 + 13), badge_text, font=self.font_badge, fill=badge_text_col)
        
        # 2. Main Card
        card_w, card_h = 920, 520
        cx0 = cx - card_w // 2
        cy0 = by1 + 32
        cx1 = cx0 + card_w
        cy1 = cy0 + card_h
        
        card_outline = (255, 50, 70, 240) if card_type == "warning" else (0, 220, 240, 210)
        card_fill = (22, 10, 14, 245) if card_type == "warning" else (9, 15, 24, 245)
        
        img = self.draw_glowing_card(img, [cx0, cy0, cx1, cy1], radius=24, outline=card_outline, fill=card_fill)
        draw = ImageDraw.Draw(img)
        
        # Card Header: 3 dots Mac style
        dot_y = cy0 + 26
        draw.ellipse([cx0 + 28, dot_y, cx0 + 40, dot_y + 12], fill=(255, 95, 86, 255))
        draw.ellipse([cx0 + 48, dot_y, cx0 + 60, dot_y + 12], fill=(255, 189, 46, 255))
        draw.ellipse([cx0 + 68, dot_y, cx0 + 80, dot_y + 12], fill=(39, 201, 63, 255))
        
        win_title = unicodedata.normalize("NFC", scene_data.get("window_title", "agent · pipeline"))
        draw.text((cx0 + 98, dot_y - 6), win_title, font=self.font_code, fill=(0, 210, 230, 220))
        draw.line([(cx0, cy0 + 56), (cx1, cy0 + 56)], fill=(card_outline[0], card_outline[1], card_outline[2], 80), width=1)
        
        # Content Inside Card
        lines = scene_data.get("lines", [])
        line_y = cy0 + 90
        for l in lines:
            txt = unicodedata.normalize("NFC", l.get("text", ""))
            col = l.get("color", (230, 240, 250, 255))
            draw.text((cx0 + 42, line_y), txt, font=self.font_code, fill=col)
            line_y += 54
            
        # 3. Subtitles
        subtitle_tokens = scene_data.get("tokens", [])
        sub_y = self.height - 420
        total_w = 0
        token_measures = []
        for word, is_hl in subtitle_tokens:
            w_norm = unicodedata.normalize("NFC", word)
            f = self.font_sub_bold if is_hl else self.font_sub_reg
            w = draw.textlength(w_norm + " ", font=f)
            token_measures.append((w_norm, is_hl, f, w))
            total_w += w
            
        pad_x, pad_y = 38, 20
        s_box = [cx - int(total_w)//2 - pad_x, sub_y - pad_y, cx + int(total_w)//2 + pad_x, sub_y + 60 + pad_y]
        draw.rounded_rectangle(s_box, radius=20, fill=(5, 9, 15, 225), outline=(0, 220, 240, 110), width=1)
        
        curr_x = cx - int(total_w) // 2
        for word, is_hl, f, w in token_measures:
            col = (0, 245, 255, 255) if is_hl else (250, 250, 255, 245)
            draw.text((curr_x, sub_y), word, font=f, fill=col)
            curr_x += w
            
        img.convert("RGB").save(out_path, quality=95)

    async def generate_voice(self, text, out_audio_path):
        comm = edge_tts.Communicate(text, self.voice, rate="+4%", pitch="-1Hz")
        await comm.save(out_audio_path)

    def get_audio_duration(self, audio_path):
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(res.stdout.strip())

    async def render_full_short(self, scenes, out_mp4):
        scene_videos = []
        
        for idx, sc in enumerate(scenes, 1):
            img_path = os.path.join(self.output_dir, f"frame_{idx}.jpg")
            audio_path = os.path.join(self.output_dir, f"audio_{idx}.mp3")
            sc_mp4 = os.path.join(self.output_dir, f"scene_{idx}.mp4")
            
            self.render_scene_frame(sc, img_path)
            await self.generate_voice(sc["spoken_text"], audio_path)
            dur = self.get_audio_duration(audio_path) + 0.35
            
            # Render video clip using ffmpeg with subtle zoom effect
            cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", img_path, "-i", audio_path,
                "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p", "-t", str(dur), sc_mp4
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            scene_videos.append(sc_mp4)
            
        # Concat all scenes
        list_file = os.path.join(self.output_dir, "concat_list.txt")
        with open(list_file, "w") as f:
            for sv in scene_videos:
                f.write(f"file '{sv}'\n")
                
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
            "-c", "copy", out_mp4
        ]
        subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return out_mp4

async def main():
    producer = AIFirstDevProducer()
    
    # Kịch bản bản tin AI phong cách AIFirstDev: "Agent Harness là gì? Vì sao AI Code lại mạnh đột phá?"
    scenes = [
        {
            "badge": "AI AGENT",
            "type": "code",
            "window_title": "agent · architecture",
            "lines": [
                {"text": "> khởi tạo tác vụ...", "color": (0, 240, 255, 255)},
                {"text": "model: Claude-3.7-Sonnet", "color": (255, 255, 255, 255)},
                {"text": "task: fix Bug Payment Gateway", "color": (255, 189, 46, 255)},
                {"text": "while (task.notDone()) {", "color": (200, 220, 240, 255)},
                {"text": "    agent.execute();", "color": (46, 213, 115, 255)},
                {"text": "}", "color": (200, 220, 240, 255)}
            ],
            "spoken_text": "Vì sao các AI Code hàng đầu hiện nay lại có thể tự viết mã và sửa lỗi như một lập trình viên thực thụ?",
            "tokens": [("Các", False), ("AI Code", True), ("hiện nay", False), ("đang", False), ("tự viết mã", True), ("thế nào?", False)]
        },
        {
            "badge": "AGENT HARNESS",
            "type": "code",
            "window_title": "system · core",
            "lines": [
                {"text": "┌────────── AGENT HARNESS ──────────┐", "color": (0, 240, 255, 255)},
                {"text": "│  [Context]  [While-Loop]  [Tools] │", "color": (255, 255, 255, 255)},
                {"text": "│                                   │", "color": (100, 100, 100, 255)},
                {"text": "│        ┌─────────────────┐        │", "color": (0, 240, 255, 255)},
                {"text": "│        │   LLM ENGINE    │        │", "color": (255, 255, 255, 255)},
                {"text": "│        └─────────────────┘        │", "color": (0, 240, 255, 255)},
                {"text": "└───────────────────────────────────┘", "color": (0, 240, 255, 255)}
            ],
            "spoken_text": "Bí mật không chỉ nằm ở mô hình ngôn ngữ lớn, mà chính là Agent Harness, khung sườn điều phối toàn bộ hành vi.",
            "tokens": [("Bí mật", False), ("chính là", False), ("Agent Harness,", True), ("khung sườn", True), ("điều phối.", True)]
        },
        {
            "badge": "CONTEXT MANAGEMENT",
            "type": "code",
            "window_title": "memory · auto-compress",
            "lines": [
                {"text": "> dung lượng bộ nhớ: 200,000 tokens", "color": (255, 189, 46, 255)},
                {"text": "Status: 85% full -> Auto-compress", "color": (255, 95, 86, 255)},
                {"text": "Compressing history log...", "color": (0, 240, 255, 255)},
                {"text": "✓ Token reduced: 170k -> 25k tokens", "color": (46, 213, 115, 255)},
                {"text": "State: Preserved without data loss", "color": (240, 240, 240, 255)}
            ],
            "spoken_text": "Nó liên tục nén ngữ cảnh thông minh, giúp AI không bao giờ bị quên mã nguồn hay tràn bộ nhớ khi xử lý dự án khổng lồ.",
            "tokens": [("Tự động", False), ("nén ngữ cảnh,", True), ("chống tràn", True), ("bộ nhớ", True), ("triệt để.", False)]
        },
        {
            "badge": "PARALLEL WORKFLOW",
            "type": "code",
            "window_title": "sub-agents · execution",
            "lines": [
                {"text": "Spawn sub-agents:", "color": (0, 240, 255, 255)},
                {"text": "├─ Sub-agent 1: Tìm kiếm tài liệu API [✓]", "color": (46, 213, 115, 255)},
                {"text": "├─ Sub-agent 2: Viết testcase tự động [✓]", "color": (46, 213, 115, 255)},
                {"text": "└─ Sub-agent 3: Debug mã nguồn [Running]", "color": (255, 189, 46, 255)}
            ],
            "spoken_text": "Và kích hoạt các sub-agent chạy song song, biến một câu lệnh đơn giản thành cả một đội ngũ kỹ sư thực thi trong chớp mắt.",
            "tokens": [("Chạy", False), ("song song", True), ("nhiều sub-agent,", True), ("tăng tốc", True), ("vượt trội.", False)]
        },
        {
            "badge": "LIDO AI LAB",
            "type": "code",
            "window_title": "follow · lido_ai_lab",
            "lines": [
                {"text": "> Đăng ký kênh Lido AI Lab", "color": (0, 240, 255, 255)},
                {"text": "Channel: @LidoAILab", "color": (255, 255, 255, 255)},
                {"text": "Update: Tin tức & Đột phá AI mỗi ngày", "color": (255, 189, 46, 255)},
                {"text": "Follow to master the future of AI!", "color": (46, 213, 115, 255)}
            ],
            "spoken_text": "Đăng ký kênh Lido AI Lab ngay hôm nay để không bỏ lỡ những phân tích công nghệ AI chuyên sâu và thực chiến nhất.",
            "tokens": [("Bấm Đăng Ký", True), ("kênh", False), ("@LidoAILab", True), ("để cập nhật", False), ("mỗi ngày!", True)]
        }
    ]
    
    out_file = "/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/output_aifirstdev/lido_aifirstdev_demo.mp4"
    await producer.render_full_short(scenes, out_file)
    print("FINISHED_RENDER:", out_file)

if __name__ == "__main__":
    asyncio.run(main())
