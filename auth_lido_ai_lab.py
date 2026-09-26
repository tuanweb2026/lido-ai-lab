import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Credentials của Lido AI Lab
CLIENT_SECRET_FILE = Path("/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/credentials/client_secret.json")
TOKEN_FILE = Path("/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/credentials/token.json")

with open(CLIENT_SECRET_FILE, "r") as f:
    secret_data = json.load(f)["installed"]

CLIENT_ID = secret_data["client_id"]
CLIENT_SECRET = secret_data["client_secret"]
REDIRECT_URI = "http://localhost:8080/"

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        if "code" in params:
            code = params["code"][0]
            print(f"\n[+] Đã nhận Authorization Code: {code[:15]}...", flush=True)
            
            # Đổi code lấy token
            token_url = "https://oauth2.googleapis.com/token"
            data = urllib.parse.urlencode({
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code"
            }).encode('utf-8')
            
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
            try:
                with urllib.request.urlopen(req, context=ctx) as resp:
                    tokens = json.loads(resp.read().decode('utf-8'))
                    tokens["client_id"] = CLIENT_ID
                    tokens["client_secret"] = CLIENT_SECRET
                    
                    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                        json.dump(tokens, f, indent=2)
                    print("\n🎉 [✓] ĐÃ LƯU TOKEN CHÍNH XÁC CHO KÊNH LIDO AI LAB!", flush=True)
                    
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    html = """
                    <html><body style="font-family:sans-serif; text-align:center; padding:50px;">
                    <h2 style="color:green;">🎉 Xác thực thành công cho kênh Lido AI Lab!</h2>
                    <p>Hệ thống đã nhận đúng quyền cho kênh @LidoAILab. Bạn có thể đóng tab này lại.</p>
                    </body></html>
                    """
                    self.wfile.write(html.encode('utf-8'))
                    sys.exit(0)
            except Exception as e:
                print(f"[-] Lỗi đổi token: {e}", flush=True)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Error exchange token")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code received")

def main():
    scopes = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtube.force-ssl"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": scopes,
        "access_type": "offline",
        "prompt": "select_account consent"
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    print("\n" + "="*80)
    print("🔑 LINK ỦY QUYỀN DUY NHẤT DÀNH CHO KÊNH [LIDO AI LAB]:")
    print("👉 HÃY BẤM VÀO LINK DƯỚI ĐÂY, CHỌN ĐÚNG KÊNH 'LIDO AI LAB':")
    print(url)
    print("="*80 + "\n")
    print("[*] Đang lắng nghe phản hồi tại http://localhost:8080/ ...", flush=True)
    server = HTTPServer(("localhost", 8080), OAuthHandler)
    server.handle_request()

if __name__ == "__main__":
    main()
