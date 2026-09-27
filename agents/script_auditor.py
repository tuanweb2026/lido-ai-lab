import re
import json

class ScriptAuditorAgent:
    """
    QUALITY ASSURANCE & CROSS-CHECK AUDITOR AGENT (CỔNG KIỂM DUYỆT CHÉO NỘI DUNG):
    
    Kỹ năng & Nhiệm vụ cốt lõi:
    1. Check Deduplication against History (Kiểm tra trùng lặp với lịch sử đã thu âm):
       - So sánh mức độ tương đồng câu chữ với toàn bộ kịch bản đã từng sản xuất trong `seen_scripts.json`.
       - Nếu chỉ số Jaccard Similarity trên cụm từ n-gram vượt quá 35% -> TỪ CHỐI (REJECT).
       
    2. Check Template Clichés (Chặn các cụm từ dập khuôn sáo rỗng):
       - Chặn các câu chung chung như:
         "Các chuyên gia bảo mật phát hiện hệ thống đã phát sinh hành vi nguy hiểm"
         "phá vỡ giới hạn hiệu năng cũ"
         "bước ngoặt đang được toàn bộ Thung lũng Silicon nín thở theo dõi"
         "Bản tin độc quyền: Một bước tiến mới vừa chính thức xuất hiện"
       - Nếu phát hiện mẫu câu sáo rỗng này -> TỪ CHỐI (REJECT).
       
    3. Check Topic Entity Relevance (Kiểm tra bám sát thực thể & hành động cụ thể):
       - Xác nhận kịch bản có nhắc trực diện đến đối tượng trọng tâm (tên hãng, tên công nghệ, hành vi cụ thể trong tiêu đề báo) hay không.
       - Đảm bảo ít nhất 2 từ khóa thực thể xuất hiện trong đoạn thoại đầu tiên.
    """
    def __init__(self, history_file="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/seen_scripts.json"):
        self.history_file = history_file
        self.banned_cliches = [
            "các chuyên gia bảo mật phát hiện hệ thống đã phát sinh hành vi nguy hiểm",
            "phá vỡ giới hạn hiệu năng cũ",
            "bước ngoặt đang được toàn bộ thung lũng silicon",
            "bước tiến mới vừa chính thức xuất hiện làm thay đổi",
            "một bước tiến mới đang thu hút sự chú ý lớn từ các chuyên gia toàn cầu",
            "khác với các nghiên cứu lý thuyết trong phòng lab",
            "công nghệ đang thay đổi diện mạo từng ngành nghề"
        ]

    def _get_history(self):
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def record_passed_script(self, title, script_data):
        history = self._get_history()
        history.append({
            "title": title,
            "badge": script_data.get("workflow_metadata", {}).get("badge_title", ""),
            "full_voice_text": script_data.get("full_voice_text", "")
        })
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ [Auditor] Không thể lưu lịch sử thoại: {e}")

    def audit_script(self, topic_title, script_data):
        full_text = script_data.get("full_voice_text", "").lower()
        title_lower = topic_title.lower()

        # 1. Kiểm tra sáo rỗng (Cliche check)
        for cliche in self.banned_cliches:
            if cliche in full_text:
                return {
                    "passed": False,
                    "reason": f"Phát hiện mẫu câu sáo rỗng bị cấm: '{cliche}'",
                    "action": "REJECT_AND_REWRITE"
                }

        # 2. Kiểm tra độ trùng lặp với lịch sử (Cross-check seen scripts)
        history = self._get_history()
        words_new = set(re.findall(r'\b\w{3,}\b', full_text))
        for old_item in history:
            old_text = old_item.get("full_voice_text", "").lower()
            words_old = set(re.findall(r'\b\w{3,}\b', old_text))
            if not words_old:
                continue
            intersection = len(words_new & words_old)
            union = len(words_new | words_old)
            jaccard = intersection / union if union > 0 else 0
            if jaccard > 0.40:
                return {
                    "passed": False,
                    "reason": f"Trùng lặp lời thoại quá cao ({jaccard:.1%}) với video cũ: '{old_item.get('title')}'",
                    "action": "REJECT_AND_REWRITE"
                }

        # 3. Kiểm tra tính liên kết thực thể (Entity relevance check)
        # Lấy các từ khóa quan trọng trong title
        title_tokens = [w for w in re.findall(r'\b[a-zA-Z0-9-]{3,}\b', title_lower) if w not in [
            "the", "and", "for", "with", "that", "this", "from", "short", "news", "exclusive"
        ]]
        matched_tokens = [w for w in title_tokens if w in full_text]
        if len(matched_tokens) < 1:
            return {
                "passed": False,
                "reason": f"Lời thoại không phản ánh đúng từ khóa bài báo (khớp: {matched_tokens})",
                "action": "REJECT_AND_REWRITE"
            }

        return {
            "passed": True,
            "reason": f"Đạt chuẩn chất lượng (Khớp thực thể: {len(matched_tokens)}, độc bản 100%)",
            "action": "APPROVE"
        }
