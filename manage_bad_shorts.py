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
    new_tok = json.loads(resp.read().decode('utf-8'))
    access_token = new_tok['access_token']

def set_video_privacy(video_id, status='private'):
    """Chuyển trạng thái video sang private để ẩn khỏi kênh công khai"""
    # 1. Lấy thông tin video hiện tại
    get_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={video_id}"
    get_req = urllib.request.Request(get_url, headers={'Authorization': f'Bearer {access_token}'})
    with urllib.request.urlopen(get_req, context=ctx) as r:
        vdata = json.loads(r.read().decode('utf-8'))
        if not vdata.get('items'):
            return False, "Not found"
        item = vdata['items'][0]

    # 2. Cập nhật privacyStatus
    item['status']['privacyStatus'] = status
    update_url = "https://www.googleapis.com/youtube/v3/videos?part=snippet,status"
    update_req = urllib.request.Request(
        update_url,
        data=json.dumps(item).encode('utf-8'),
        headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
        method='PUT'
    )
    with urllib.request.urlopen(update_req, context=ctx) as r:
        return True, "Success"

def delete_video(video_id):
    """Xóa hoàn toàn video khỏi kênh"""
    del_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}"
    del_req = urllib.request.Request(del_url, headers={'Authorization': f'Bearer {access_token}'}, method='DELETE')
    with urllib.request.urlopen(del_req, context=ctx) as r:
        return True

if __name__ == "__main__":
    print("Script sẵn sàng hỗ trợ quản lý video cũ an toàn.")
