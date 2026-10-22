#!/usr/bin/env python3
"""
图片参考示例
使用 agnes-video-2.5-flash 生成视频（图片作为参考）
用法：python image-reference.py [参考图片URL] [提示词]
"""

import json
import os
import sys
import time
import urllib.request

import load_env
load_env.load_env()

API_KEY = os.environ.get("AGNESAI_API_KEY", "your-api-key-here")
BASE_URL = os.environ.get("AGNESAI_BASE_URL", "https://api.agnes-ai.cn").rstrip("/")
POLL_URL = f"{BASE_URL}/agnesapi"

IMAGE_URL = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/character.png"
PROMPT = sys.argv[2] if len(sys.argv) > 2 else "以 <Picture 1> 中的角色和美术风格为参考，角色在花田中自然奔跑，保持外观一致"

print("提交图片参考视频请求...")
print(f"  参考图片: {IMAGE_URL}")
print(f"  提示词: {PROMPT}")

payload = {
    "model": "agnes-video-2.5-flash",
    "prompt": PROMPT,
    "seconds": "5",
    "mode": "reference",
    "size": "720P",
    "aspect_ratio": "16:9",
    "images": [IMAGE_URL]
}

req = urllib.request.Request(
    f"{BASE_URL}/v1/videos",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    method="POST"
)

with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode("utf-8"))

print("响应：")
print(json.dumps(result, indent=2, ensure_ascii=False))

video_id = result.get("video_id")
if not video_id:
    print("[ERR] 获取 video_id 失败")
    sys.exit(1)

print(f"[OK] 任务已提交，video_id: {video_id}")
print("开始轮询查询结果（视频生成通常需要 2-5 分钟）...")

MAX_RETRIES = 120
RETRY_INTERVAL = 5

for i in range(1, MAX_RETRIES + 1):
    time.sleep(RETRY_INTERVAL)

    poll_req = urllib.request.Request(
        f"{POLL_URL}?video_id={video_id}&model_name=agnes-video-2.5-flash",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    with urllib.request.urlopen(poll_req) as poll_resp:
        poll_result = json.loads(poll_resp.read().decode("utf-8"))

    status = poll_result.get("status")
    progress = poll_result.get("progress", 0)
    print(f"状态: {status}, 进度: {progress}%")

    if status == "completed":
        video_url = poll_result.get("metadata", {}).get("url") or poll_result.get("url") or poll_result.get("video_url")
        print("[OK] 视频生成完成！")
        print(f"视频地址：{video_url}")
        sys.exit(0)
    elif status == "failed":
        error_msg = (poll_result.get("error") or {}).get("message") or poll_result.get("error") or "未知错误"
        print(f"[ERR] 视频生成失败：{error_msg}")
        sys.exit(1)

print(f"超时：等待超过 {MAX_RETRIES}x{RETRY_INTERVAL} 秒")
sys.exit(1)
