import os


from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 720, 1280
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"

f_title = ImageFont.truetype(FONT_PATH, 22)
f_sub = ImageFont.truetype(FONT_PATH, 20)
f_box = ImageFont.truetype(FONT_PATH, 18)
f_mono = ImageFont.truetype(FONT_MONO, 16)

def create_base():
    img = Image.new("RGB", (WIDTH, HEIGHT), (2, 4, 6))
    draw = ImageDraw.Draw(img)
    for x in range(0, WIDTH, 36):
        draw.line([(x, 0), (x, HEIGHT)], fill=(6, 12, 16), width=1)
    for y in range(0, HEIGHT, 36):
        draw.line([(0, y), (WIDTH, y)], fill=(6, 12, 16), width=1)
    return img

def render_step_frame(step_progress, typed_chars, subtitle_text):
    img = create_base()
    draw = ImageDraw.Draw(img)
    cx = WIDTH // 2

    # Title
    t_box = [cx - 140, 360, cx + 140, 404]
    draw.rounded_rectangle(t_box, radius=8, outline=(0, 240, 255), width=2, fill=(0, 20, 28))
    draw.text((cx - 105, 372), "AI AGENT WORKFLOW", font=f_title, fill=(0, 240, 255))

    # Step 1: User Prompt Box
    y1 = 430
    draw.rounded_rectangle([cx - 180, y1, cx + 180, y1 + 45], radius=10, outline=(0, 180, 200), width=1, fill=(10, 25, 35))
    draw.text((cx - 150, y1 + 12), "Bước 1: Nhận yêu cầu lập trình", font=f_box, fill=(230, 245, 255))

    # Arrow 1 (chỉ hiện khi step >= 1)
    if step_progress >= 1:
        draw.line([(cx, y1 + 48), (cx, y1 + 72)], fill=(0, 240, 255), width=2)
        draw.polygon([(cx, y1 + 76), (cx - 5, y1 + 68), (cx + 5, y1 + 68)], fill=(0, 240, 255))

    # Step 2: Agent Suy nghĩ / Phân tích
    if step_progress >= 1:
        y2 = y1 + 80
        alpha_col = (0, 240, 255) if step_progress == 1 else (0, 150, 170)
        draw.rounded_rectangle([cx - 180, y2, cx + 180, y2 + 45], radius=10, outline=alpha_col, width=2, fill=(10, 30, 40))
        draw.text((cx - 150, y2 + 12), "Bước 2: Phân tích & Lập kế hoạch", font=f_box, fill=(255, 255, 255))

    # Arrow 2
    if step_progress >= 2:
        y2 = y1 + 80
        draw.line([(cx, y2 + 48), (cx, y2 + 72)], fill=(0, 240, 255), width=2)
        draw.polygon([(cx, y2 + 76), (cx - 5, y2 + 68), (cx + 5, y2 + 68)], fill=(0, 240, 255))

    # Step 3: Terminal gõ lệnh thực thi code
    if step_progress >= 2:
        y3 = y1 + 160
        cw, ch = 440, 140
        cx0, cy0 = cx - cw//2, y3
        draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=12, outline=(0, 240, 255), width=2, fill=(8, 14, 20))
        # dots
        draw.ellipse([cx0 + 14, cy0 + 12, cx0 + 22, cy0 + 20], fill=(255, 95, 86))
        draw.ellipse([cx0 + 28, cy0 + 12, cx0 + 36, cy0 + 20], fill=(255, 189, 46))
        draw.ellipse([cx0 + 42, cy0 + 12, cx0 + 50, cy0 + 20], fill=(39, 201, 63))
        draw.text((cx0 + 60, cy0 + 9), "terminal · bash", font=f_mono, fill=(0, 180, 200))
        draw.line([(cx0, cy0 + 32), (cx0 + cw, cy0 + 32)], fill=(0, 100, 120), width=1)

        code_text = "agent run refactor_core.py"
        shown_code = "> " + code_text[:typed_chars] + ("_" if typed_chars < len(code_text) else "")
        draw.text((cx0 + 20, cy0 + 48), shown_code, font=f_mono, fill=(0, 240, 255))
        if typed_chars >= len(code_text):
            draw.text((cx0 + 20, cy0 + 78), "[OK] 14 files updated successfully", font=f_mono, fill=(46, 213, 115))
            draw.text((cx0 + 20, cy0 + 104), "Done in 0.84s", font=f_mono, fill=(150, 160, 170))

    # Arrow 3
    if step_progress >= 3:
        y4 = y1 + 310
        draw.line([(cx, y1 + 302), (cx, y4 - 6)], fill=(46, 213, 115), width=2)
        draw.polygon([(cx, y4 - 2), (cx - 5, y4 - 10), (cx + 5, y4 - 10)], fill=(46, 213, 115))
        # Step 4: Kiểm tra & Hoàn tất
        draw.rounded_rectangle([cx - 180, y4, cx + 180, y4 + 45], radius=10, outline=(46, 213, 115), width=2, fill=(10, 35, 25))
        draw.text((cx - 150, y4 + 12), "✓ Bước 4: Tự động chạy Unit Test", font=f_box, fill=(46, 213, 115))

    # Subtitle
    if subtitle_text:
        s_w = draw.textlength(subtitle_text, font=f_sub)
        sb = [cx - int(s_w)//2 - 20, 920, cx + int(s_w)//2 + 20, 965]
        draw.rounded_rectangle(sb, radius=8, fill=(8, 14, 18), outline=(0, 180, 200, 100), width=1)
        draw.text((cx - int(s_w)//2, 930), subtitle_text, font=f_sub, fill=(240, 245, 250))

    return img

print("Testing render_step_frame...")
img = render_step_frame(3, 26, "Agent tự động chạy kiểm thử và hoàn thành")
img.save("/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/test_step_frame.jpg")
print("Saved test_step_frame.jpg")
