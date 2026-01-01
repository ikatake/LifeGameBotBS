import sys
import os
import requests
from datetime import datetime, timezone
import _key_secret_
import common

PDS_URL = "https://bsky.social"
BASE_URL = "https://wetsteam.org/"  # GIF公開用のベースURL（要確認・変更）

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
    run, gene, loop_from = common.readLoopFile(loop_file)
    gif_path = f"/home/ikatake/www/wetsteam/LifeGameBotBS/gifs/{run:08d}.gif"
    
    if os.path.exists(gif_path):
        with open(gif_path, 'rb') as f:
            gif_data = f.read()
        
        # サムネイル用にGIFをアップロード
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
        
        # 外部リンクカードとしてGIFアニメーションを添付
        gif_url = f"{BASE_URL}/LifeGameBotBS/gifs/{run:08d}.gif"
        embed = {
            "$type": "app.bsky.embed.external",
            "external": {
                "uri": gif_url,
                "title": f"Life Game Run {run:08d} Animation",
                "description": f"Conway's Game of Life - Run {run:08d} ({gene} generations, loop from {loop_from})",
                "thumb": blob
            }
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