class SeoPackagerAgent:
    def __init__(self, channel_url="https://www.youtube.com/@LidoAILab"):
        self.channel_url = channel_url

    def package_metadata(self, topic, script_data):
        title = "AI AGENTS ĐANG THAY ĐỔI THẾ GIỚI NHƯ THẾ NÀO? 🤖⚡ #Shorts #AI #Tech"
        
        description = (
            f"Kỷ nguyên AI Agents tự động hóa đã chính thức bắt đầu!\n\n"
            f"Các mô hình AI thế hệ mới nhất không chỉ dừng lại ở việc phản hồi câu hỏi, mà giờ đây đã có thể tự động viết mã, điều khiển hệ thống máy tính và thực hiện các tác vụ phức tạp một cách độc lập.\n\n"
            f"🔔 Hãy nhấn SUBSCRIBE để không bỏ lỡ những bước chuyển dịch công nghệ AI nóng nhất:\n"
            f"👉 Kênh chính thức: {self.channel_url}\n\n"
            f"#LidoAILab #AI #ArtificialIntelligence #Technology #AIAgents #Shorts #TechNews #TuDongHoa"
        )

        tags = [
            "Lido AI Lab", "AI", "Trí tuệ nhân tạo", "AI Agents", "Công nghệ 2026",
            "ChatGPT", "Google Gemini", "Claude", "Shorts", "Tech News", "Tự động hóa"
        ]

        pinned_comment = (
            "🔥 Bạn nghĩ AI Agents sẽ giúp con người tăng gấp 10 lần hiệu suất làm việc hay sẽ thay thế hoàn toàn một số ngành nghề? "
            "Hãy để lại bình luận phía dưới và ĐĂNG KÝ KÊNH để cập nhật nhé! 👇👇👇"
        )

        return {
            "title": title,
            "description": description,
            "tags": tags,
            "pinned_comment": pinned_comment
        }

if __name__ == "__main__":
    agent = SeoPackagerAgent()
    meta = agent.package_metadata({}, {})
    print("Title:", meta["title"])
    print("\nPinned Comment:\n", meta["pinned_comment"])
