#!/usr/bin/env python3
import json
import urllib.parse
import urllib.request
import ssl
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
redirect_uri = "http://localhost:8080/"

code = "4/0ATsMZqCZ7jTCExxsZDFOrtBFErwuwJ2C8vyRgLOe4-V9p76bygxRoP7cATSU5QCetx6Kpw"

print(f"[+] Trao đổi authorization code lấy token...")

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
            
        print(f"[+] ĐÃ LƯU TOKEN MỚI VÀO: {TOKEN_FILE}")
        
        access_token = tokens["access_token"]
        ch_req = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true")
        ch_req.add_header("Authorization", f"Bearer {access_token}")
        with urllib.request.urlopen(ch_req, context=ctx) as ch_resp:
            ch_data = json.loads(ch_resp.read().decode("utf-8"))
            if ch_data.get("items"):
                item = ch_data["items"][0]
                ch_title = item["snippet"]["title"]
                ch_handle = item["snippet"].get("customUrl", "No customUrl")
                ch_id = item["id"]
                print(f"[SUCCESS] KÊNH ĐÃ ĐƯỢC XÁC THỰC THÀNH CÔNG: {ch_title} ({ch_handle}) - ID: {ch_id}")
            else:
                print("[!] Không tìm thấy thông tin kênh.")
except Exception as e:
    print(f"[-] Lỗi: {e}")
