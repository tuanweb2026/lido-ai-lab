import feedparser
import urllib.request
import urllib.parse
import json
import os
import ssl
import re

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

try:
    from agents.knowledge_expander import KnowledgeExpanderAgent
except ImportError:
    from knowledge_expander import KnowledgeExpanderAgent

class SmartTrendHunterAgent:
    """
    Agent 1: SIÊU QUÉT ĐA NGUỒN TOÀN CẦU (MASSIVE GLOBAL RADAR)
    - Quét trực tiếp 15+ cổng thông tin công nghệ hàng đầu thế giới (TechCrunch, TheVerge, HackerNews, MIT Tech Review, ArXiv, Google News Global & VN)
    - Theo dõi radar đối thủ CuongMeAI & các trend AI hot nhất
    - Bảng 100+ từ khóa điểm số cao, đa dạng các mảng (Mô hình LLM, Video AI, Coding Agents, Robot hình người, Chip AI, Bảo mật)
    - Mục tiêu: Luôn có 50 - 100 tin tức tươi mới mỗi ngày phục vụ chiến dịch tăng trưởng 1K Sub cho @LidoAILab.
    """
    def __init__(self, db_path="/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/seen_news.json"):
        self.db_path = db_path
        self.seen_titles = self.load_seen_titles()
        self.expander = KnowledgeExpanderAgent()

        # Nạp từ khóa động từ knowledge base
        try:
            with open(self.expander.keywords_file, "r", encoding="utf-8") as f:
                self.hot_keywords = json.load(f)
        except Exception:
            self.hot_keywords = {}

        # DANH MỤC 100+ TỪ KHÓA BẮT TREND BÙNG NỔ (VIRAL & HIGH-RETENTION)
        additional_keywords = {
            # 1. Các siêu mô hình AI & Hãng dẫn đầu
            "chatgpt": 4, "gpt-5": 5, "gpt-4o": 4, "openai": 4, "deepseek": 5, "deepseek-r1": 5, "deepseek v3": 5,
            "claude": 4, "claude 3.7": 5, "anthropic": 4, "sonnet": 4, "opus": 4,
            "gemini": 4, "gemini 2.0": 5, "google deepmind": 4, "grok": 4, "grok 3": 5, "xai": 4,
            "perplexity": 5, "meta ai": 3, "llama 3": 4, "llama 4": 5, "mistral": 3, "qwen": 4, "qwen 2.5": 4,

            # 2. AI Video, Phim Ảnh & Giọng Nói Hollywood
            "sora": 5, "sora 2": 5, "kling": 4, "kling 1.5": 4, "kling 3.0": 5, "runway": 4, "gen-3": 4,
            "luma": 4, "dream machine": 4, "pika": 3, "hailuo": 4, "minimax": 4, "wan 2.1": 4,
            "midjourney": 4, "flux": 4, "elevenlabs": 4, "suno": 3, "udio": 3, "veo": 4, "veo 2": 5,

            # 3. Kỹ sư ảo, Lập trình & AI Agent tự hành
            "cursor": 5, "cursor ai": 5, "windsurf": 4, "devin": 5, "manus": 5, "manus ai": 5,
            "ai agent": 4, "agentic": 5, "computer use": 5, "operator": 5, "deep research": 5,
            "mcp": 4, "model context protocol": 4, "autogen": 3, "crewai": 3, "langchain": 3,

            # 4. Phần cứng, Siêu máy tính & Chip bán dẫn
            "nvidia": 4, "blackwell": 5, "b200": 5, "gb200": 5, "h100": 3, "jensen huang": 4,
            "tsmc": 4, "asml": 3, "amd": 3, "mi300": 4, "apple intelligence": 4, "qualcomm": 3,

            # 5. Robot hình người & AGI
            "robot": 4, "humanoid": 5, "optimus": 5, "tesla robot": 5, "figure 02": 5, "unitree": 4,
            "boston dynamics": 4, "atlas": 4, "agi": 5, "isaac ros": 4,

            # 6. Bảo mật, Bẻ khóa & Hack
            "hack": 4, "jailbreak": 5, "vulnerability": 4, "prompt injection": 5, "leak": 4, "breach": 4, "bypass": 4,

            # 7. Từ khóa tiếng Việt & Ứng dụng thực chiến
            "trí tuệ nhân tạo": 3, "công cụ ai": 3, "kiếm tiền ai": 4, "tự động hóa": 3, "ứng dụng ai": 3
        }
        self.hot_keywords.update(additional_keywords)

        # MẠNG LƯỚI NGUỒN CÀO TIN TỨC ĐA NỀN TẢNG (15+ NGUỒN TƯƠI MỚI)
        self.sources = [
            # Nguồn Quốc Tế Chuyên Sâu Công Nghệ
            {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
            {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"},
            {"name": "HackerNews Trending AI", "url": "https://hnrss.org/newest?q=AI+OR+LLM+OR+GPT+OR+Agent"},
            {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"},
            
            # Google News Phân Luồng Chuyên Biệt
            {"name": "Google News (Top AI)", "url": "https://news.google.com/rss/search?q=" + urllib.parse.quote("Artificial Intelligence when:24h") + "&hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News (ChatGPT & DeepSeek)", "url": "https://news.google.com/rss/search?q=" + urllib.parse.quote("ChatGPT OR DeepSeek OR Claude OR Perplexity when:24h") + "&hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News (Video AI & Sora)", "url": "https://news.google.com/rss/search?q=" + urllib.parse.quote("Sora OR Kling OR Runway OR Flux AI when:48h") + "&hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News (NVIDIA & Robot)", "url": "https://news.google.com/rss/search?q=" + urllib.parse.quote("NVIDIA OR Robot OR Humanoid OR Blackwell when:48h") + "&hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News (AI Agents & Coding)", "url": "https://news.google.com/rss/search?q=" + urllib.parse.quote("Cursor AI OR AI Agent OR Devin OR Manus when:48h") + "&hl=en-US&gl=US&ceid=US:en"},
            {"name": "Google News (Việt Nam AI)", "url": "https://news.google.com/rss/search?q=" + urllib.parse.quote("Trí tuệ nhân tạo OR ChatGPT when:48h") + "&hl=vi&gl=VN&ceid=VN:vi"}
        ]

    def load_seen_titles(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_seen_title(self, title):
        self.seen_titles.append(title)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.seen_titles, f, ensure_ascii=False, indent=2)

    def fetch_all_fresh_topics(self, limit_per_source=15):
        """Quét toàn diện tất cả các nguồn và trả về danh sách các tin nóng nhất đã lọc trùng"""
        all_candidates = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*'
        }

        print(f"📡 [SmartHunter] Đang quét {len(self.sources)} kênh tin tức AI công nghệ toàn cầu...")
        for src in self.sources:
            try:
                req = urllib.request.Request(src["url"], headers=headers)
                with urllib.request.urlopen(req, timeout=8, context=ssl_ctx) as resp:
                    feed = feedparser.parse(resp.read())
                    for entry in feed.entries[:limit_per_source]:
                        title = entry.title.strip()
                        if title in self.seen_titles:
                            continue

                        # Kiểm tra chống trùng lặp tuyệt đối (Semantic Keyword Overlap)
                        # Nếu tiêu đề mới trùng từ 3 từ khóa ý nghĩa với bất kỳ video nào trong quá khứ -> LẬP TỨC BỎ QUA
                        t_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', title.lower()))
                        # Loại bỏ các từ quá phổ biến
                        common_stopwords = {"news", "with", "from", "that", "this", "will", "what", "have", "more", "your", "into", "their"}
                        t_words = t_words - common_stopwords
                        
                        is_duplicate_topic = False
                        for st in self.seen_titles:
                            st_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', st.lower())) - common_stopwords
                            # Nếu trùng từ 3 từ khóa quan trọng trở lên -> Trùng chủ đề
                            if len(t_words & st_words) >= 3:
                                is_duplicate_topic = True
                                break
                        
                        if is_duplicate_topic:
                            continue

                        # Tự động học thực thể mới vào knowledge base
                        self.expander.extract_and_learn_from_text(title)

                        # Chấm điểm độ hot
                        score = 1
                        t_lower = title.lower()
                        matched_kw = []
                        for kw, weight in self.hot_keywords.items():
                            if kw in t_lower:
                                score += weight
                                matched_kw.append(kw)

                        all_candidates.append({
                            "title": title,
                            "link": entry.link,
                            "source": src["name"],
                            "score": score,
                            "keywords": matched_kw
                        })
            except Exception as e:
                # Bỏ qua nguồn lỗi nhẹ, tiếp tục quét nguồn khác
                pass

        # Sắp xếp theo điểm số hot nhất
        all_candidates.sort(key=lambda x: x["score"], reverse=True)
        return all_candidates

    def fetch_best_new_topic(self):
        candidates = self.fetch_all_fresh_topics()
        if candidates:
            best = candidates[0]
            print(f"🎯 [SmartHunter] Tìm thấy tin hot nhất: '{best['title']}'")
            print(f"   ➔ Điểm số: {best['score']} | Nguồn: {best['source']} | Khớp: {best['keywords']}")
            return best
        print("ℹ️ [SmartHunter] Chưa có tin mới phù hợp trong chu kỳ này.")
        return None

if __name__ == "__main__":
    hunter = SmartTrendHunterAgent()
    topics = hunter.fetch_all_fresh_topics()
    print(f"\n✅ ĐÃ QUÉT ĐƯỢC TỔNG CỘNG: {len(topics)} TIN TỨC MỚI CHƯA TỪNG LÀM!")
    print("\nTop 5 tin tức hot nhất sẵn sàng sản xuất Shorts:")
    for idx, t in enumerate(topics[:5], 1):
        print(f"{idx}. [{t['score']} điểm] ({t['source']}) {t['title']}")
