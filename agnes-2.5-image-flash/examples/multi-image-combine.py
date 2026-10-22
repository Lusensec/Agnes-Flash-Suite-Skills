#!/usr/bin/env python3
"""
多图合成示例
使用 agnes-image-2.5-flash 将多张参考图组合生成新图像
用法：python multi-image-combine.py [图片1URL] [图片2URL] [提示词]
"""

import json
import os
import sys
import urllib.request

import load_env
load_env.load_env()

API_KEY = os.environ.get("AGNESAI_API_KEY", "your-api-key-here")
BASE_URL = os.environ.get("AGNESAI_BASE_URL", "https://api.agnes-ai.cn").rstrip("/")

IMAGE1 = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/character-1.png"
IMAGE2 = sys.argv[2] if len(sys.argv) > 2 else "https://example.com/character-2.png"
PROMPT = sys.argv[3] if len(sys.argv) > 3 else "Combine the two characters into an intense fantasy battle scene, dynamic lighting, detailed background, cinematic composition"

print("提交多图合成请求...")
print(f"  参考图片 1: {IMAGE1}")
print(f"  参考图片 2: {IMAGE2}")
print(f"  提示词: {PROMPT}")

payload = {
    "model": "agnes-image-2.5-flash",
    "prompt": PROMPT,
    "size": "2K",
    "ratio": "1:1",
    "extra_body": {
        "image": [IMAGE1, IMAGE2],
        "response_format": "url"
    }
}

req = urllib.request.Request(
    f"{BASE_URL}/v1/images/generations",
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

image_url = result["data"][0]["url"]
if not image_url:
    print("[ERR] 获取图片 URL 失败")
    sys.exit(1)

print("[OK] 图片生成完成！")
print(f"图片地址：{image_url}")
