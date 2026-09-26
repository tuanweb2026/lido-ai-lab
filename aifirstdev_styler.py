import os
import json
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_MONO = "/System/Library/Fonts/Menlo.ttc"

class AIFirstDevStyler:
    """
    Tái tạo 100% phong cách thẩm mỹ Cyberpunk / Minimal Dark Terminal của AIFirstDev:
    - Nền: Dark Mesh Grid (Lưới ma trận tối vi tế trên nền đen sâu)
    - Card: Cyan/Teal Neon Border (Khung bo tròn viền phát sáng cyan tinh tế, có gradient/mờ)
    - Header: Cyan Badge pill (Hộp badge cyan phát sáng phía trên)
    - Code Window: Terminal bar đỏ-vàng-xanh với font Menlo/Monospace
    - Phụ đề: Chữ trắng hiện đại, từ khóa quan trọng được Highlight màu Cyan (#00F0FF) rực rỡ
    """
    def __init__(self, width=1080, height=1920):
        self.width = width
        self.height = height
        
        # Load fonts
        self.font_badge = ImageFont.truetype(FONT_BOLD, 36)
        self.font_card_title = ImageFont.truetype(FONT_BOLD, 42)
        self.font_code = ImageFont.truetype(FONT_MONO, 32)
        self.font_sub_bold = ImageFont.truetype(FONT_BOLD, 46)
        self.font_sub_reg = ImageFont.truetype(FONT_REGULAR, 46)

    def create_dark_grid_background(self):
        """Tạo nền lưới đen sâu đẳng cấp lập trình viên (Dark Grid Matrix)"""
        bg = Image.new("RGBA", (self.width, self.height), (7, 10, 15, 255))
        draw = ImageDraw.Draw(bg)
        
        # Vẽ lưới caro mờ ảo
        grid_size = 60
        grid_color = (18, 25, 38, 120)
        
        for x in range(0, self.width, grid_size):
            draw.line([(x, 0), (x, self.height)], fill=grid_color, width=1)
        for y in range(0, self.height, grid_size):
            draw.line([(0, y), (self.width, y)], fill=grid_color, width=1)
            
        # Thêm một chút ambient glow ở trung tâm
        glow = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        cx, cy = self.width // 2, self.height // 2 - 100
        gdraw.ellipse([cx - 400, cy - 400, cx + 400, cy + 400], fill=(0, 240, 255, 12))
        glow = glow.filter(ImageFilter.GaussianBlur(80))
        
        return Image.alpha_composite(bg, glow)

    def draw_glowing_rounded_box(self, base_img, box, radius=24, outline=(0, 240, 255, 220), fill=(11, 17, 26, 230), glow_intensity=3):
        """Vẽ khung card bo tròn viền neon phát sáng chuẩn Cyberpunk"""
        x0, y0, x1, y1 = box
        
        # Glow layer
        glow_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow_layer)
        for g in range(glow_intensity, 0, -1):
            alpha = int(35 / g)
            g_out = (outline[0], outline[1], outline[2], alpha)
            gdraw.rounded_rectangle([x0 - g*2, y0 - g*2, x1 + g*2, y1 + g*2], radius=radius+g*2, outline=g_out, width=2)
            
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(4))
        base_img = Image.alpha_composite(base_img, glow_layer)
        
        # Main solid box
        draw = ImageDraw.Draw(base_img)
        draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=3)
        return base_img

    def render_aifirstdev_card_scene(self, badge_text, card_type, content_data, subtitle_tokens):
        """
        Dựng 1 khung hình hoàn chỉnh chuẩn phong cách AIFirstDev:
        - badge_text: Chữ trong tab nhỏ phía trên (vd: AI AGENT, AGENT HARNESS)
        - card_type: "code" (màn hình gõ lệnh/code), "architecture" (sơ đồ khối), "warning" (cảnh báo đỏ)
        - content_data: Nội dung bên trong card
        - subtitle_tokens: List từ vựng [(word, is_highlight), ...]
        """
        img = self.create_dark_grid_background()
        draw = ImageDraw.Draw(img)
        
        cx = self.width // 2
        cy = self.height // 2 - 80
        
        # 1. Vẽ Badge Pill phía trên
        badge_w, badge_h = 320, 64
        bx0 = cx - badge_w // 2
        by0 = cy - 280
        bx1 = bx0 + badge_w
        by1 = by0 + badge_h
        
        img = self.draw_glowing_rounded_box(img, [bx0, by0, bx1, by1], radius=16, 
                                           outline=(0, 240, 255, 230), fill=(10, 28, 38, 240))
        draw = ImageDraw.Draw(img)
        # Canh giữa badge text
        bbox = draw.textbbox((0, 0), badge_text, font=self.font_badge)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, by0 + 12), badge_text, font=self.font_badge, fill=(0, 240, 255, 255))
        
        # 2. Vẽ Card Trung Tâm (Main Frame)
        card_w, card_h = 880, 480
        cx0 = cx - card_w // 2
        cy0 = by1 + 30
        cx1 = cx0 + card_w
        cy1 = cy0 + card_h
        
        if card_type == "warning":
            card_outline = (255, 50, 70, 240)
            card_fill = (28, 12, 16, 240)
        else:
            card_outline = (0, 210, 230, 200)
            card_fill = (10, 16, 25, 240)
            
        img = self.draw_glowing_rounded_box(img, [cx0, cy0, cx1, cy1], radius=24, 
                                           outline=card_outline, fill=card_fill)
        draw = ImageDraw.Draw(img)
        
        # Header của Card (3 chấm Mac + nhãn)
        dot_y = cy0 + 28
        draw.ellipse([cx0 + 26, dot_y, cx0 + 38, dot_y + 12], fill=(255, 95, 86, 255))
        draw.ellipse([cx0 + 46, dot_y, cx0 + 58, dot_y + 12], fill=(255, 189, 46, 255))
        draw.ellipse([cx0 + 66, dot_y, cx0 + 78, dot_y + 12], fill=(39, 201, 63, 255))
        
        header_title = content_data.get("window_title", "agent · task")
        draw.text((cx0 + 96, dot_y - 4), header_title, font=self.font_code, fill=(0, 200, 210, 200))
        draw.line([(cx0, cy0 + 56), (cx1, cy0 + 56)], fill=(card_outline[0], card_outline[1], card_outline[2], 80), width=1)
        
        # Nội dung bên trong Card
        lines = content_data.get("lines", [])
        line_y = cy0 + 85
        for l in lines:
            txt = l.get("text", "")
            col = l.get("color", (220, 235, 245, 255))
            draw.text((cx0 + 40, line_y), txt, font=self.font_code, fill=col)
            line_y += 50
            
        # 3. Phụ đề dưới màn hình (Dynamic Karaoke-style Highlight Subtitles)
        sub_y = self.height - 420
        # Đo chiều dài tổng cộng của dòng phụ đề
        total_w = 0
        token_measures = []
        for word, is_hl in subtitle_tokens:
            f = self.font_sub_bold if is_hl else self.font_sub_reg
            w = draw.textlength(word + " ", font=f)
            token_measures.append((word, is_hl, f, w))
            total_w += w
            
        # Vẽ hộp đen mờ đằng sau phụ đề
        pad_x, pad_y = 36, 18
        s_box = [cx - int(total_w)//2 - pad_x, sub_y - pad_y, cx + int(total_w)//2 + pad_x, sub_y + 60 + pad_y]
        draw.rounded_rectangle(s_box, radius=20, fill=(6, 10, 16, 210), outline=(0, 220, 240, 100), width=1)
        
        curr_x = cx - int(total_w) // 2
        for word, is_hl, f, w in token_measures:
            if is_hl:
                col = (0, 245, 255, 255) # Cyan neon rực sáng
            else:
                col = (255, 255, 255, 240) # Trắng tinh khôi
            draw.text((curr_x, sub_y), word, font=f, fill=col)
            curr_x += w
            
        return img

if __name__ == "__main__":
    styler = AIFirstDevStyler()
    test_img = styler.render_aifirstdev_card_scene(
        badge_text="AI AGENT",
        card_type="code",
        content_data={
            "window_title": "agent · task",
            "lines": [
                {"text": "> tự viết code...", "color": (0, 240, 255, 255)},
                {"text": "function handlePayment(o) {", "color": (240, 245, 255, 255)},
                {"text": "    return checkout(o);", "color": (240, 245, 255, 255)},
                {"text": "}", "color": (240, 245, 255, 255)},
                {"text": "✓ Executed in 12ms", "color": (46, 213, 115, 255)}
            ]
        },
        subtitle_tokens=[
            ("đầu", False), ("hiện", False), ("nay", False), 
            ("lại", False), ("có", False), ("thể", False), 
            ("tự", True), ("viết", True), ("code,", True)
        ]
    )
    test_img.convert("RGB").save("/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/test_aifirstdev_frame.jpg")
    print("Saved test frame!")
