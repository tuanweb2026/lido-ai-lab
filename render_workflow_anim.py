import os
import sys
import subprocess
import asyncio
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 720, 1280
FPS = 30
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"

f_title = ImageFont.truetype(FONT_PATH, 22)
f_sub = ImageFont.truetype(FONT_PATH, 20)
f_box = ImageFont.truetype(FONT_PATH, 18)
f_mono = ImageFont.truetype(FONT_MONO, 16)
f_stamp = ImageFont.truetype(FONT_PATH, 24)

def create_grid_bg():
    img = Image.new("RGB", (WIDTH, HEIGHT), (2, 4, 6))
    draw = ImageDraw.Draw(img)
    for x in range(0, WIDTH, 36):
        draw.line([(x, 0), (x, HEIGHT)], fill=(6, 12, 16), width=1)
    for y in range(0, HEIGHT, 36):
        draw.line([(0, y), (WIDTH, y)], fill=(6, 12, 16), width=1)
    return img

def render_anim_frame(t, total_dur, spoken_step):
    img = create_grid_bg()
    draw = ImageDraw.Draw(img)
    cx = WIDTH // 2

    # Top Badge Title
    t_box = [cx - 150, 340, cx + 150, 386]
    draw.rounded_rectangle(t_box, radius=8, outline=(0, 240, 255), width=2, fill=(0, 20, 28))
    draw.text((cx - 110, 353), "QUY TRÌNH AI AGENT", font=f_title, fill=(0, 240, 255))

    # Step 1: Nhận Task (Xuất hiện từ giây 0.0)
    y1 = 415
    draw.rounded_rectangle([cx - 180, y1, cx + 180, y1 + 45], radius=10, outline=(0, 180, 200), width=1, fill=(10, 25, 35))
    draw.text((cx - 150, y1 + 12), "Bước 1: Nhận yêu cầu lập trình", font=f_box, fill=(230, 245, 255))

    # Mũi tên 1: Xuất hiện từ giây 1.8
    if t >= 1.8:
        draw.line([(cx, y1 + 48), (cx, y1 + 72)], fill=(0, 240, 255), width=2)
        draw.polygon([(cx, y1 + 76), (cx - 5, y1 + 68), (cx + 5, y1 + 68)], fill=(0, 240, 255))

    # Step 2: Phân tích & Lập Kế hoạch (Xuất hiện từ giây 2.0)
    if t >= 2.0:
        y2 = y1 + 80
        glow_step2 = (0, 240, 255) if (2.0 <= t < 4.0) else (0, 140, 160)
        draw.rounded_rectangle([cx - 180, y2, cx + 180, y2 + 45], radius=10, outline=glow_step2, width=2, fill=(10, 30, 42))
        draw.text((cx - 150, y2 + 12), "Bước 2: Phân tích & Lập kế hoạch", font=f_box, fill=(255, 255, 255))

    # Mũi tên 2: Xuất hiện từ giây 3.8
    if t >= 3.8:
        y2 = y1 + 80
        draw.line([(cx, y2 + 48), (cx, y2 + 72)], fill=(0, 240, 255), width=2)
        draw.polygon([(cx, y2 + 76), (cx - 5, y2 + 68), (cx + 5, y2 + 68)], fill=(0, 240, 255))

    # Step 3: Terminal gõ lệnh từng ký tự (Bắt đầu từ giây 4.0)
    if t >= 4.0:
        y3 = y1 + 160
        cw, ch = 440, 145
        cx0, cy0 = cx - cw//2, y3
        draw.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + ch], radius=12, outline=(0, 240, 255), width=2, fill=(8, 14, 20))
        # 3 dots
        draw.ellipse([cx0 + 14, cy0 + 12, cx0 + 22, cy0 + 20], fill=(255, 95, 86))
        draw.ellipse([cx0 + 28, cy0 + 12, cx0 + 36, cy0 + 20], fill=(255, 189, 46))
        draw.ellipse([cx0 + 42, cy0 + 12, cx0 + 50, cy0 + 20], fill=(39, 201, 63))
        draw.text((cx0 + 60, cy0 + 9), "terminal · bash", font=f_mono, fill=(0, 180, 200))
        draw.line([(cx0, cy0 + 32), (cx0 + cw, cy0 + 32)], fill=(0, 100, 120), width=1)

        full_cmd = "agent refactor --fix-all"
        chars_to_show = int((t - 4.0) * 16) # gõ 16 ký tự mỗi giây
        shown_cmd = full_cmd[:chars_to_show]
        cursor_blink = "_" if (int(t * 4) % 2 == 0 and chars_to_show < len(full_cmd)) else ""
        draw.text((cx0 + 20, cy0 + 48), f"> {shown_cmd}{cursor_blink}", font=f_mono, fill=(0, 240, 255))

        if chars_to_show >= len(full_cmd):
            draw.text((cx0 + 20, cy0 + 78), "[RUN] Quét toàn bộ 14 files codebase...", font=f_mono, fill=(255, 189, 46))
            if t >= 6.2:
                draw.text((cx0 + 20, cy0 + 104), "✓ Refactor thành công trong 0.8s", font=f_mono, fill=(46, 213, 115))

    # Mũi tên 3: Xuất hiện từ giây 7.2
    if t >= 7.2:
        draw.line([(cx, y1 + 308), (cx, y1 + 332)], fill=(46, 213, 115), width=2)
        draw.polygon([(cx, y1 + 336), (cx - 5, y1 + 328), (cx + 5, y1 + 328)], fill=(46, 213, 115))

    # Step 4: Chạy Unit Test kiểm tra (Từ giây 7.4)
    if t >= 7.4:
        y4 = y1 + 340
        draw.rounded_rectangle([cx - 180, y4, cx + 180, y4 + 45], radius=10, outline=(46, 213, 115), width=2, fill=(10, 36, 24))
        draw.text((cx - 150, y4 + 12), "✓ Bước 4: Tự động chạy Unit Test", font=f_box, fill=(46, 213, 115))

    # Đóng dấu Phê duyệt / DỪNG LẠI (An toàn hệ thống từ giây 9.5)
    if t >= 9.5:
        # Hộp cảnh báo an toàn đè nổi bật (như con dấu DỪNG LẠI của AIFirstDev)
        sx, sy = cx - 130, 810
        draw.rounded_rectangle([sx, sy, sx + 260, sy + 50], radius=8, outline=(255, 50, 70), width=3, fill=(35, 10, 16))
        draw.text((cx - 105, sy + 12), "🔒 BẢO VỆ TOÀN DIỆN", font=f_stamp, fill=(255, 60, 80))

    # Subtitle động theo thời gian
    sub_text = ""
    highlight_word = ""
    if t < 2.0:
        sub_text = "Đầu tiên, Agent tiếp nhận yêu cầu lập trình"
        highlight_word = "tiếp nhận"
    elif t < 4.0:
        sub_text = "Bước tiếp theo, nó tự phân tích và lập kế hoạch"
        highlight_word = "phân tích"
    elif t < 7.4:
        sub_text = "Sau đó, Agent tự gõ lệnh và sửa từng dòng code"
        highlight_word = "tự gõ lệnh"
    elif t < 9.5:
        sub_text = "Cuối cùng, nó chạy Unit Test để đảm bảo không có lỗi"
        highlight_word = "Unit Test"
    else:
        sub_text = "Toàn bộ chu trình diễn ra khép kín và an toàn tuyệt đối"
        highlight_word = "an toàn tuyệt đối"

    s_words = sub_text.split()
    total_w = sum(draw.textlength(w + " ", font=f_sub) for w in s_words)
    sb = [cx - int(total_w)//2 - 16, 920, cx + int(total_w)//2 + 16, 965]
    draw.rounded_rectangle(sb, radius=8, fill=(8, 14, 18), outline=(0, 180, 200, 100), width=1)
    
    cur_x = cx - int(total_w) // 2
    for w in s_words:
        col = (0, 245, 255) if (highlight_word in w) else (240, 245, 250)
        draw.text((cur_x, 930), w, font=f_sub, fill=col)
        cur_x += draw.textlength(w + " ", font=f_sub)

    return img

async def main():
    out_dir = "/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/step_anim_output"
    os.makedirs(out_dir, exist_ok=True)
    voice_audio = os.path.join(out_dir, "step_voice.mp3")

    full_voice_text = (
        "Đầu tiên, Agent tiếp nhận yêu cầu lập trình của bạn. "
        "Bước tiếp theo, nó tự phân tích và lập kế hoạch chi tiết. "
        "Sau đó, Agent mở terminal, tự gõ lệnh và sửa từng dòng code trong codebase. "
        "Cuối cùng, nó tự động chạy Unit Test để kiểm tra chất lượng. "
        "Toàn bộ chu trình diễn ra tự động và an toàn tuyệt đối!"
    )

    import edge_tts
    print("[1/3] Tạo giọng đọc thuyết minh từng bước...")
    comm = edge_tts.Communicate(full_voice_text, "vi-VN-NamMinhNeural", rate="+4%")
    await comm.save(voice_audio)

    # Đo độ dài audio
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", voice_audio]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    duration = float(res.stdout.strip())
    print(f" -> Thời lượng audio: {duration:.2f}s")

    # Render video bằng ffmpeg pipe
    out_video = "/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/step_by_step_animated_demo.mp4"
    total_frames = int(duration * FPS) + 15
    print(f"[2/3] Dựng chuyển động từng bước (tổng cộng {total_frames} frames @ 30fps)...")

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}", "-pix_fmt", "rgb24",
        "-r", str(FPS), "-i", "-",
        "-i", voice_audio,
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", out_video
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    for f_idx in range(total_frames):
        t = f_idx / FPS
        frame = render_anim_frame(t, duration, 0)
        pipe.stdin.write(frame.tobytes())
        if f_idx % 60 == 0:
            print(f" -> Đã render {f_idx}/{total_frames} frames ({t:.1f}s)...")

    pipe.stdin.close()
    pipe.wait()
    print(f"[3/3] HOÀN TẤT DỰNG PHIM TỪNG BƯỚC CHUYỂN ĐỘNG: {out_video}")

if __name__ == "__main__":
    asyncio.run(main())
