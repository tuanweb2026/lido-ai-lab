#!/usr/bin/env python3
import json
import urllib.parse
import urllib.request
import ssl
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Create unverified SSL context to bypass macOS python certificate verify failed
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

CLIENT_SECRET_FILE = Path("/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/client_secret.json")
TOKEN_FILE = Path("/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management/token.json")

with open(CLIENT_SECRET_FILE) as f:
    client_info = json.load(f)["installed"]

client_id = client_info["client_id"]
client_secret = client_info["client_secret"]
token_uri = client_info.get("token_uri", "https://oauth2.googleapis.com/token")

port = 8080
redirect_uri = f"http://localhost:{port}/"

scopes = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": "code",
    "scope": " ".join(scopes),
    "access_type": "offline",
    "prompt": "select_account consent"
}

auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

print("="*70)
print("VUI LÒNG MỞ LIÊN KẾT SAU ĐỂ CẤP QUYỀN CHO KÊNH LIDO AI LAB:")
print(auth_url)
print("="*70)
sys.stdout.flush()

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if "code" in qs:
            code = qs["code"][0]
            print(f"\n[+] Đã nhận authorization code thành công!")
            
            post_data = urllib.parse.urlencode({
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            }).encode("utf-8")
            
            req = urllib.request.Request(token_uri, data=post_data, method="POST")
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
            
            try:
                with urllib.request.urlopen(req, context=ctx) as resp:
                    tokens = json.loads(resp.read().decode("utf-8"))
                    tokens["client_id"] = client_id
                    tokens["client_secret"] = client_secret
                    tokens["token_uri"] = token_uri
                    
                    with open(TOKEN_FILE, "w") as f:
                        json.dump(tokens, f, indent=2)
                        
                    print(f"[+] Đã lưu token mới vào: {TOKEN_FILE}")
                    
                    # Check channel info
                    access_token = tokens["access_token"]
                    ch_req = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true")
                    ch_req.add_header("Authorization", f"Bearer {access_token}")
                    ch_title = "Unknown"
                    ch_handle = "Unknown"
                    try:
                        with urllib.request.urlopen(ch_req, context=ctx) as ch_resp:
                            ch_data = json.loads(ch_resp.read().decode("utf-8"))
                            if ch_data.get("items"):
                                item = ch_data["items"][0]
                                ch_title = item["snippet"]["title"]
                                ch_handle = item["snippet"].get("customUrl", "No customUrl")
                                print(f"[+] KÊNH ĐÃ KẾT NỐI THÀNH CÔNG: {ch_title} ({ch_handle})")
                    except Exception as e:
                        print(f"[-] Lỗi kiểm tra kênh: {e}")

                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    html = f"""
                    <html>
                    <head><title>Xác thực thành công</title></head>
                    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                        <h2 style="color: #2e7d32;">Đã cấp quyền thành công cho kênh: {ch_title} ({ch_handle})!</h2>
                        <p style="font-size: 16px;">Hệ thống Lido AI Lab đã nhận được quyền đăng video chính xác 100%.</p>
                        <p style="color: #666;">Bạn có thể đóng tab này lại và quay lại Antigravity Chat.</p>
                    </body>
                    </html>
                    """
                    self.wfile.write(html.encode("utf-8"))
            except Exception as e:
                print(f"[-] Lỗi đổi code lấy token: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Lỗi: {e}".encode("utf-8"))
            
            import threading
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code found.")

    def log_message(self, format, *args):
        pass

server = HTTPServer(("localhost", port), OAuthHandler)
print(f"OAuth Server đang lắng nghe tại port {port}...")
sys.stdout.flush()
server.serve_forever()
print("OAuth hoàn tất! Server đã dừng.")
