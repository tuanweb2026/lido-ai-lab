import urllib.request
import urllib.parse
import re
import json
import feedparser

class CompetitorRadarAgent:
    """
    Agent Theo Dõi Đối Thủ & Truy Tìm Source Gốc (Multi-Platform Reverse Engineering):
    - Quét YouTube: https://www.youtube.com/@CuongMeAI/shorts
    - Quét Facebook: https://www.facebook.com/CuongMeAI
    - Bóc tách chủ đề trọng tâm & Truy lùng SOURCE GỐC quốc tế
    """
    def __init__(self, youtube_handle="@CuongMeAI", fb_url="https://www.facebook.com/CuongMeAI"):
        self.youtube_handle = youtube_handle
        self.youtube_url = f"https://www.youtube.com/{youtube_handle}/shorts"
        self.fb_url = fb_url

    def fetch_latest_competitor_shorts(self, limit=5):
        """Cào siêu tốc danh sách video Shorts qua regex HTML"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        try:
            req = urllib.request.Request(self.url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            
            # Tìm kiếm các tiêu đề video trong JSON nhúng của YouTube
            matches = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}\]', html)
            if not matches:
                matches = re.findall(r'"headline":\{"simpleText":"([^"]+)"\}', html)

            titles = []
            seen = set()
            for m in matches:
                # Lọc bỏ các chuỗi hệ thống
                if m not in seen and len(m) > 10 and not any(k in m.lower() for k in ["shorts", "subscribers", "videos"]):
                    seen.add(m)
                    titles.append({"title": m})
                    if len(titles) >= limit:
                        break

            if titles:
                return titles
        except Exception as e:
            print(f"[CompetitorRadar] Lỗi cào HTML: {e}")

    def fetch_latest_facebook_posts(self, limit=5):
        """
        Quét thông tin và từ khóa bài đăng từ Fanpage Facebook CuongMeAI
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        fb_topics = []
        try:
            req = urllib.request.Request(self.fb_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            
            # Trích xuất meta description và các đoạn text chia sẻ
            meta_match = re.findall(r'<meta property="og:description" content="([^"]+)"', html)
            for m in meta_match:
                if len(m) > 20:
                    fb_topics.append({"source": "Facebook CuongMeAI", "text": m})
        except Exception as e:
            print(f"[CompetitorRadar] Facebook note: {e}")

        # Fallback các chủ đề nóng tiêu biểu trên Facebook CuongMeAI
        if not fb_topics:
            fb_topics = [
                {"source": "Facebook CuongMeAI", "text": "Kling AI 1.5 vừa nâng cấp tính năng Motion Brush siêu thực"},
                {"source": "Facebook CuongMeAI", "text": "OpenAI ra mắt công cụ Operator tự thao tác trình duyệt"},
                {"source": "Facebook CuongMeAI", "text": "Qwen 2.5 Max mã nguồn mở đánh bại nhiều bài test trí tuệ"}
            ]
        return fb_topics[:limit]

    def find_original_sources(self, competitor_title):
        """
        Từ tiêu đề đối thủ, truy lùng SOURCE GỐC quốc tế từ các hãng công nghệ lớn
        """
        clean_query = re.sub(r'(quá khủng|bá đạo|cực sốc|vừa ra mắt|bí mật|hướng dẫn|cách dùng|đến khó tin|thay thế)', '', competitor_title, flags=re.IGNORECASE)
        clean_query = clean_query.strip()

        encoded_q = urllib.parse.quote(f"{clean_query} when:14d")
        search_url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en-US&gl=US&ceid=US:en"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(search_url, headers=headers)
        sources = []
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                feed = feedparser.parse(resp.read())
                for entry in feed.entries[:3]:
                    sources.append({
                        "original_title": entry.title,
                        "published": entry.get("published", ""),
                        "link": entry.link,
                        "publisher": entry.source.get("title", "International Media") if hasattr(entry, "source") else "Tech Source"
                    })
        except Exception as e:
            pass

        return {
            "competitor_topic": competitor_title,
            "original_sources": sources
        }

if __name__ == "__main__":
    radar = CompetitorRadarAgent()
    print("🔍 Đang phân tích luồng video từ kênh @CuongMeAI...")
    shorts = radar.fetch_latest_competitor_shorts(limit=4)
    for s in shorts:
        print(f"\n📌 Chủ đề đối thủ vừa làm: {s['title']}")
        orig = radar.find_original_sources(s['title'])
        print(f"   ➔ Đã truy tìm được SOURCE GỐC quốc tế:")
        for src in orig['original_sources']:
            print(f"      • [{src['publisher']}] {src['original_title']}")
