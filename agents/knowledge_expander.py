import json
import os
import re

class KnowledgeExpanderAgent:
    """
    Agent Tự Học & Mở Rộng Tri Thức (Self-Expanding Knowledge Base):
    - Tự động phát hiện các thực thể, công cụ AI, thuật toán và nguồn báo mới
    - Lưu trữ bền vững vào knowledge_base/dynamic_keywords.json và custom_sources.json
    - Giúp hệ thống ngày càng giàu từ khóa và không bao giờ cạn kiệt ý tưởng
    """
    def __init__(self, kb_dir="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/knowledge_base"):
        self.kb_dir = kb_dir
        self.keywords_file = os.path.join(kb_dir, "dynamic_keywords.json")
        self.sources_file = os.path.join(kb_dir, "custom_sources.json")
        os.makedirs(self.kb_dir, exist_ok=True)
        self.init_default_storage()

    def init_default_storage(self):
        if not os.path.exists(self.keywords_file):
            default_kws = {
                "chatgpt": 3, "deepseek": 4, "claude": 3, "perplexity": 4,
                "cursor": 4, "gemini": 3, "sora": 4, "kling": 3, "flux": 3,
                "nvidia": 3, "blackwell": 3, "optimus": 3, "qwen": 3, "wan": 3,
                "manus": 4, "devin": 3, "windsurf": 3, "deepresearch": 4
            }
            with open(self.keywords_file, "w", encoding="utf-8") as f:
                json.dump(default_kws, f, ensure_ascii=False, indent=2)

        if not os.path.exists(self.sources_file):
            default_sources = [
                {"name": "Hugging Face Daily Papers", "url": "https://huggingface.co/papers"},
                {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/"},
                {"name": "The Verge Tech", "url": "https://www.theverge.com/ai-artificial-intelligence"}
            ]
            with open(self.sources_file, "w", encoding="utf-8") as f:
                json.dump(default_sources, f, ensure_ascii=False, indent=2)

    def learn_new_keyword(self, new_keyword, weight=3):
        """Tự động thêm từ khóa mới vào hệ thống nếu chưa có"""
        new_keyword = new_keyword.strip().lower()
        if len(new_keyword) < 3:
            return False

        with open(self.keywords_file, "r", encoding="utf-8") as f:
            kws = json.load(f)

        if new_keyword not in kws:
            kws[new_keyword] = weight
            with open(self.keywords_file, "w", encoding="utf-8") as f:
                json.dump(kws, f, ensure_ascii=False, indent=2)
            print(f"💡 [KnowledgeExpander] ĐÃ TỰ ĐỘNG HỌC TỪ KHÓA MỚI: '{new_keyword}' (Trọng số: {weight})")
            return True
        return False

    def learn_new_source(self, source_name, source_url):
        """Tự động bổ sung nguồn tin tức mới tìm được"""
        with open(self.sources_file, "r", encoding="utf-8") as f:
            sources = json.load(f)

        existing_urls = [s["url"] for s in sources]
        if source_url not in existing_urls:
            sources.append({"name": source_name, "url": source_url})
            with open(self.sources_file, "w", encoding="utf-8") as f:
                json.dump(sources, f, ensure_ascii=False, indent=2)
            print(f"🌐 [KnowledgeExpander] ĐÃ THÊM NGUỒN TIN MỚI: '{source_name}' -> {source_url}")
            return True
        return False

    def extract_and_learn_from_text(self, text):
        """Phân tích văn bản tin tức để tự động phát hiện tên model / công cụ AI mới"""
        # Bắt các model công nghệ AI cụ thể như GPT-*, Claude-*, Qwen-*, Wan-*, Sora, Deep*, v.v.
        pattern = r'\b((?:GPT|Qwen|Claude|Gemini|Llama|DeepSeek|Wan|Manus|Kling|Runway|Mistral|Devin|Cursor|Flux|Optimus|Blackwell)[a-zA-Z0-9.-]*)\b'
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        learned_count = 0

        for m in matches:
            clean_m = m.strip().lower()
            if len(clean_m) > 2:
                if self.learn_new_keyword(clean_m, weight=3):
                    learned_count += 1
        return learned_count

if __name__ == "__main__":
    expander = KnowledgeExpanderAgent()
    expander.learn_new_keyword("manus ai", 4)
    expander.learn_new_keyword("wan 2.1", 3)
    expander.learn_new_source("OpenAI Engineering Blog", "https://openai.com/index/")
