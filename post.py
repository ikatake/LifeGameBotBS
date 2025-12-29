import sys
import os
import requests
from datetime import datetime, timezone
import _key_secret_
import common

PDS_URL = "https://bsky.social"

# Blueskyセッション作成
session_resp = requests.post(
    f"{PDS_URL}/xrpc/com.atproto.server.createSession",
    json={
        "identifier": _key_secret_.BSKY_HANDLE,
        "password": _key_secret_.BSKY_APP_PASSWORD,
    },
    timeout=10,
)
session_resp.raise_for_status()
session = session_resp.json()

# 投稿内容を読み込み
file_name = sys.argv[1]
with open(file_name, encoding='utf-8') as f:
    post_text = f.read()

# GIF添付の処理（loop.txtが指定されている場合）
embed = None
if len(sys.argv) > 2:
    loop_file = sys.argv[2]
    gene, step, loop_from = common.readLoopFile(loop_file)
    gif_path = f"/home/ikatake/www/wetsteam/lifegamebot/gifs/{gene:08d}.gif"
    
    if os.path.exists(gif_path):
        with open(gif_path, 'rb') as f:
            gif_data = f.read()
        
        # GIFをアップロード
        upload_resp = requests.post(
            f"{PDS_URL}/xrpc/com.atproto.repo.uploadBlob",
            headers={
                "Authorization": f"Bearer {session['accessJwt']}",
                "Content-Type": "image/gif",
            },
            data=gif_data,
            timeout=30,
        )
        upload_resp.raise_for_status()
        blob = upload_resp.json()['blob']
        
        # embedに画像を追加
        embed = {
            "$type": "app.bsky.embed.images",
            "images": [{"alt": "Life Game Animation", "image": blob}]
        }

# 投稿レコードを構築
record = {
    "$type": "app.bsky.feed.post",
    "text": post_text,
    "createdAt": datetime.now(timezone.utc).isoformat(),
}
if embed:
    record["embed"] = embed

# Blueskyに投稿
post_resp = requests.post(
    f"{PDS_URL}/xrpc/com.atproto.repo.createRecord",
    headers={
        "Authorization": f"Bearer {session['accessJwt']}",
        "Content-Type": "application/json",
    },
    json={
        "repo": session["did"],
        "collection": "app.bsky.feed.post",
        "record": record,
    },
    timeout=10,
)
post_resp.raise_for_status()
print(f"Posted: {post_resp.json()['uri']}")