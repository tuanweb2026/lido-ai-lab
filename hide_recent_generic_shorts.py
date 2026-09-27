import urllib.request, urllib.parse, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open('/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/credentials/token.json') as f:
    tokens = json.load(f)

# Refresh token
post_data = urllib.parse.urlencode({
    'client_id': tokens['client_id'],
    'client_secret': tokens['client_secret'],
    'refresh_token': tokens['refresh_token'],
    'grant_type': 'refresh_token'
}).encode('utf-8')
req = urllib.request.Request('https://oauth2.googleapis.com/token', data=post_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
with urllib.request.urlopen(req, context=ctx) as resp:
    access_token = json.loads(resp.read().decode('utf-8'))['access_token']

# Các video mới bị gán nhãn "CẢNH BÁO BẢO MẬT AI" dập khuôn:
generic_vids = [
    "6ASnnhih4UE", # OpenAI thừa nhận tác nhân AI
    "KCsIYENUMd8"  # Check is your OpenAI GPT-6-Astra nerfed
]

for vid in generic_vids:
    try:
        get_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={vid}"
        get_req = urllib.request.Request(get_url, headers={'Authorization': f'Bearer {access_token}'})
        with urllib.request.urlopen(get_req, context=ctx) as r:
            vdata = json.loads(r.read().decode('utf-8'))
            if not vdata.get('items'): continue
            item = vdata['items'][0]

        item['status']['privacyStatus'] = 'private'
        update_url = "https://www.googleapis.com/youtube/v3/videos?part=snippet,status"
        update_req = urllib.request.Request(
            update_url,
            data=json.dumps(item).encode('utf-8'),
            headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
            method='PUT'
        )
        with urllib.request.urlopen(update_req, context=ctx) as r:
            print(f"🔒 Đã ẩn video {vid} sang Private thành công!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
