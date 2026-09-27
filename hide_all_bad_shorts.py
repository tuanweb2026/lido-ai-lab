import urllib.request, urllib.parse, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open('/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/credentials/token.json') as f:
    tokens = json.load(f)

# Refresh access token
post_data = urllib.parse.urlencode({
    'client_id': tokens['client_id'],
    'client_secret': tokens['client_secret'],
    'refresh_token': tokens['refresh_token'],
    'grant_type': 'refresh_token'
}).encode('utf-8')
req = urllib.request.Request('https://oauth2.googleapis.com/token', data=post_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
with urllib.request.urlopen(req, context=ctx) as resp:
    access_token = json.loads(resp.read().decode('utf-8'))['access_token']

# Danh sách 14 video cũ từ 22/09 đến 26/09 bị lỗi dập khuôn lời thoại "BẢN TIN ĐỘC QUYỀN"
bad_vids = [
    "i9tkTMCNQbs",
    "40jcFEAHmZo",
    "wiPAqScL6bw",
    "c720mtkjRKc",
    "sBl-egrvgTI",
    "g8s7ejfpesA",
    "n7K6fwBUy8c",
    "gkg5u8B5OGk",
    "WqQjum70OYk",
    "QnmldvVFw2c",
    "wuORQWHwD9I",
    "sixWPMP9hYE",
    "ui0LOfPsx40",
    "GNLiK95MMoE"
]

print(f"Bắt đầu chuyển {len(bad_vids)} video bị lỗi lời thoại sang chế độ PRIVATE...")
hidden_count = 0
for vid in bad_vids:
    try:
        # Lấy metadata
        get_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={vid}"
        get_req = urllib.request.Request(get_url, headers={'Authorization': f'Bearer {access_token}'})
        with urllib.request.urlopen(get_req, context=ctx) as r:
            vdata = json.loads(r.read().decode('utf-8'))
            if not vdata.get('items'):
                continue
            item = vdata['items'][0]

        # Đổi sang private
        item['status']['privacyStatus'] = 'private'
        update_url = "https://www.googleapis.com/youtube/v3/videos?part=snippet,status"
        update_req = urllib.request.Request(
            update_url,
            data=json.dumps(item).encode('utf-8'),
            headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
            method='PUT'
        )
        with urllib.request.urlopen(update_req, context=ctx) as r:
            hidden_count += 1
            print(f"  🔒 [{hidden_count}/{len(bad_vids)}] Đã ẩn video https://youtu.be/{vid} thành công!")
    except Exception as e:
        print(f"  ❌ Lỗi khi ẩn {vid}: {e}")

print(f"\n✅ ĐÃ ẨN THÀNH CÔNG {hidden_count}/{len(bad_vids)} VIDEO LỖI KHỎI KÊNH CÔNG KHAI!")
