import asyncio
import os
import sys
from datetime import datetime
from agents.step_flow_producer import StepFlowMediaProducerAgent
from agents.script_auditor import ScriptAuditorAgent

OUTPUT_DIR = "/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/output/review_samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_sample_vn():
    print("\n" + "="*70)
    print("🇻🇳 [SQUAD VN] BẮT ĐẦU SẢN XUẤT BẢN TIN TIẾNG VIỆT (GIỌNG VI-VN)")
    print("="*70)

    title_vn = "Ứng dụng Trí tuệ nhân tạo A.I. bùng nổ trong trường học tại Việt Nam"
    badge_title = "AI GIÁO DỤC VIỆT NAM"
    h1 = "AI ĐỔ BỘ TRƯỜNG HỌC VIỆT NAM"
    t1 = "Làn sóng ứng dụng trí tuệ nhân tạo đang tạo nên bước ngoặt lớn tại các trường học trên cả nước theo ghi nhận mới nhất từ VTV!"
    
    h2 = "TRỢ LÝ HỌC TẬP CÁ NHÂN HÓA"
    t2 = "Thay vì phương pháp giảng dạy truyền thống, giáo viên và học sinh nay sử dụng AI để tự động chấm điểm, cá nhân hóa lộ trình học và giải thích bài tập trực quan theo thời gian thực."
    
    h3 = "THỬ THÁCH VỀ TÍNH TRUNG THỰC"
    t3 = "Bên cạnh những tiện ích vượt trội, ngành giáo dục cũng đối mặt bài toán kiểm soát đạo văn và đảm bảo tính tư duy độc lập của học sinh trước sự phụ thuộc vào các công cụ AI."
    
    h4 = "ĐÓN ĐẦU CHUYỂN ĐỔI SỐ 2026"
    t4 = "Việc trang bị kỹ năng làm chủ công nghệ AI ngay từ ghế nhà trường sẽ là chìa khóa vàng giúp thế hệ trẻ Việt Nam tự tin hội nhập thị trường lao động toàn cầu!"

    scenes = [
        {"scene_id": 1, "headline": h1, "metric_badge": badge_title, "text": t1, "overlay_data": h1, "search_keywords": ["Vietnam students using laptop classroom technology", "Vietnamese students modern school"]},
        {"scene_id": 2, "headline": h2, "metric_badge": badge_title, "text": t2, "overlay_data": h2, "search_keywords": ["AI education learning interface laptop", "Teacher teaching students digital tablet"]},
        {"scene_id": 3, "headline": h3, "metric_badge": badge_title, "text": t3, "overlay_data": h3, "search_keywords": ["Cybersecurity education digital shield", "AI ethics education classroom"]},
        {"scene_id": 4, "headline": h4, "metric_badge": badge_title, "text": t4, "overlay_data": h4, "search_keywords": ["Vietnamese youth innovative technology presentation", "Future classroom digital artificial intelligence"]},
        {
            "scene_id": 5,
            "headline": "KÊNH CÔNG NGHỆ LIDO AI LAB",
            "metric_badge": "LIDO AI LAB",
            "text": "Bấm Like và Đăng ký kênh Lido AI Lab ngay hôm nay để đón đầu những xu hướng công nghệ mới nhất!",
            "overlay_data": "SUBSCRIBE @LidoAILab",
            "search_keywords": ["YouTube subscribe button glowing neon red", "Modern tech creator studio setup"]
        }
    ]

    workflow_metadata = {
        "badge_title": badge_title,
        "step1": h1,
        "step2": h2,
        "term_title": "terminal · lido edu-ai runtime",
        "code_cmd": "edu-agent --deploy-school --adaptive-learning",
        "code_status": "[EDU AI] Khởi tạo hệ thống gia sư AI cá nhân hóa...",
        "code_result": "✓ Tối ưu lộ trình học tập cho 1200 học sinh thành công",
        "step4": h4,
        "stamp_text": "🇻🇳 AI VIỆT NAM"
    }

    script_data = {
        "title": f"{badge_title}: {title_vn} 🚀⚡ #Shorts #LidoAILab #AI",
        "scenes": scenes,
        "workflow_metadata": workflow_metadata,
        "full_voice_text": " ".join([s["text"] for s in scenes])
    }

    today_str = datetime.now().strftime("%d/%m/%Y")
    for sc in script_data["scenes"]:
        sc["source_label"] = f"VTV.VN • {today_str} (BẢN TIN VN)"

    producer = StepFlowMediaProducerAgent(output_dir=OUTPUT_DIR)
    producer.voice = "vi-VN-NamMinhNeural" # Giọng Nam Minh Tiếng Việt tự nhiên
    
    out_video_path = os.path.join(OUTPUT_DIR, "sample_vietnamese_short.mp4")
    temp_video = await producer.produce_step_animated_short(script_data, topic_info={"title": title_vn, "source": "VTV.vn"})
    os.rename(temp_video, out_video_path)
    print(f"\n✅ ĐÃ XUẤT BẢN TIN TIẾNG VIỆT THÀNH CÔNG: {out_video_path}")
    return out_video_path

async def generate_sample_en():
    print("\n" + "="*70)
    print("🌍 [SQUAD GLOBAL] BẮT ĐẦU SẢN XUẤT BẢN TIN TIẾNG ANH (GIỌNG EN-US ANDREW)")
    print("="*70)

    title_en = "Jobber Launches Model Context Protocol for ChatGPT and Claude"
    badge_title = "GLOBAL AI BREAKTHROUGH"
    h1 = "JOBBER BRINGS MCP TO CHATGPT"
    t1 = "Massive news in the AI agent space! Jobber has officially launched Model Context Protocol integration for ChatGPT and Claude."
    
    h2 = "CONNECTING REAL BUSINESS DATA"
    t2 = "Instead of static chat responses, AI models can now securely access live client data, schedule field service jobs, and trigger real-world business workflows."
    
    h3 = "THE RISE OF THE AGENTIC ERA"
    t3 = "This integration proves that Model Context Protocol is quickly becoming the universal open standard connecting enterprise software with intelligent agents."
    
    h4 = "WHAT THIS MEANS FOR YOU"
    t4 = "Companies that plug their operational workflows directly into AI agents will gain massive competitive speed and leave slow competitors far behind!"

    scenes = [
        {"scene_id": 1, "headline": h1, "metric_badge": badge_title, "text": t1, "overlay_data": h1, "search_keywords": ["Model Context Protocol MCP Claude OpenAI", "AI agent protocol futuristic dashboard"]},
        {"scene_id": 2, "headline": h2, "metric_badge": badge_title, "text": t2, "overlay_data": h2, "search_keywords": ["Business dashboard analytics glowing screen", "Field service dispatch software tablet"]},
        {"scene_id": 3, "headline": h3, "metric_badge": badge_title, "text": t3, "overlay_data": h3, "search_keywords": ["Open standard network nodes glowing digital", "Enterprise software AI integration"]},
        {"scene_id": 4, "headline": h4, "metric_badge": badge_title, "text": t4, "overlay_data": h4, "search_keywords": ["Futuristic software developer workspace dual monitors", "AI agent automate business workflow"]},
        {
            "scene_id": 5,
            "headline": "EXCLUSIVE TECH UPDATES",
            "metric_badge": "LIDO AI LAB",
            "text": "Subscribe to Lido AI Lab today to stay ahead of the most powerful AI breakthroughs!",
            "overlay_data": "SUBSCRIBE @LidoAILab",
            "search_keywords": ["YouTube subscribe button glowing neon red", "Modern tech creator studio setup"]
        }
    ]

    workflow_metadata = {
        "badge_title": badge_title,
        "step1": h1,
        "step2": h2,
        "term_title": "terminal · mcp-agent runtime",
        "code_cmd": "mcp-server --connect-jobber --runtime-claude-opus",
        "code_status": "[MCP PROTOCOL] Establishing secure handshake with Jobber API...",
        "code_result": "✓ Connected to 25,000 active service dispatch streams",
        "step4": h4,
        "stamp_text": "🌐 MCP AGENTIC"
    }

    script_data = {
        "title": f"{badge_title}: {title_en} 🚀⚡ #Shorts #LidoAILab #AI",
        "scenes": scenes,
        "workflow_metadata": workflow_metadata,
        "full_voice_text": " ".join([s["text"] for s in scenes])
    }

    today_str = datetime.now().strftime("%d/%m/%Y")
    for sc in script_data["scenes"]:
        sc["source_label"] = f"AITHORITY • {today_str} (GLOBAL NEWS)"

    producer = StepFlowMediaProducerAgent(output_dir=OUTPUT_DIR)
    producer.voice = "en-US-AndrewNeural" # Giọng đọc tiếng Anh chuyên nghiệp hàng đầu (Andrew Neural)
    
    out_video_path = os.path.join(OUTPUT_DIR, "sample_english_short.mp4")
    temp_video = await producer.produce_step_animated_short(script_data, topic_info={"title": title_en, "source": "AiThority"})
    os.rename(temp_video, out_video_path)
    print(f"\n✅ ĐÃ XUẤT BẢN TIN TIẾNG ANH THÀNH CÔNG: {out_video_path}")
    return out_video_path

async def main():
    print("="*70)
    print("🎬 KHỞI TẠO 2 VIDEO MẪU LOCAL: 1 TIẾNG VIỆT & 1 TIẾNG ANH")
    print("="*70)
    
    vn_file = await generate_sample_vn()
    en_file = await generate_sample_en()
    
    print("\n" + "="*70)
    print("🎉 HOÀN THÀNH CẢ 2 VIDEO MẪU TẠI THƯ MỤC LOCAL!")
    print(f"1. Video Tiếng Việt: file://{vn_file}")
    print(f"2. Video Tiếng Anh:  file://{en_file}")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
