import sys
import requests
from datetime import datetime, timezone
import _key_secret_

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
        "record": {
            "$type": "app.bsky.feed.post",
            "text": post_text,
            "createdAt": datetime.now(timezone.utc).isoformat(),
        },
    },
    timeout=10,
)
post_resp.raise_for_status()
print(f"Posted: {post_resp.json()['uri']}")