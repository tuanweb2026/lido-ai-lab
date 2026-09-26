import os
import json
import urllib.parse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"
CLIENT_SECRET_FILE = f"{SCRATCH_DIR}/client_secret.json"
TOKEN_FILE = f"{SCRATCH_DIR}/token.json"

class OAuthHandler(BaseHTTPRequestHandler):
    auth_code = None

    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            OAuthHandler.auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h1>Xác thực thành công cho kênh Lido AI Lab!</h1><p>Bạn có thể đóng tab này lại.</p>".encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()

def authenticate_channel():
    with open(CLIENT_SECRET_FILE, "r") as f:
        data = json.load(f)
        client_info = data.get("installed") or data.get("web")
        client_id = client_info["client_id"]
        client_secret = client_info["client_secret"]

    redirect_uri = "http://localhost:8080/"
    scope = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube"

    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urllib.parse.urlencode({
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope,
            "access_type": "offline",
            "prompt": "consent" # Bắt buộc hiện danh sách chọn kênh
        })
    )

    print("\n" + "="*70)
    print("👉 HÃY MỞ ĐƯỜNG LINK DƯỚI ĐÂY BẰNG TRÌNH DUYỆT:")
    print("⚠️ LƯU Ý: HÃY CHỌN ĐÚNG KÊNH 'Lido AI Lab' TRONG DANH SÁCH!")
    print("="*70)
    print(auth_url)
    print("="*70 + "\n")

    # Mở tự động trên Mac
    os.system(f'open "{auth_url}"')

    server = HTTPServer(("localhost", 8080), OAuthHandler)
    while OAuthHandler.auth_code is None:
        server.handle_request()

    code = OAuthHandler.auth_code
    token_url = "https://oauth2.googleapis.com/token"
    token_data = urllib.parse.urlencode({
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }).encode("utf-8")

    req = urllib.request.Request(token_url, data=token_data)
    with urllib.request.urlopen(req) as resp:
        tokens = json.loads(resp.read().decode("utf-8"))

    tokens["client_id"] = client_id
    tokens["client_secret"] = client_secret
    tokens["token_uri"] = token_url

    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2)

    print("🎉 ĐÃ LƯU TOKEN CHO KÊNH MỚI THÀNH CÔNG!")

if __name__ == "__main__":
    authenticate_channel()
