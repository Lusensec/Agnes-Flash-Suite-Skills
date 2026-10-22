#!/usr/bin/env python3
"""
图生图示例 - URL 输出
使用 agnes-image-2.5-flash 进行图像编辑/风格迁移
用法：python image-to-image.py [输入图片URL] [提示词]
"""

import json
import os
import sys
import urllib.request

import load_env
load_env.load_env()

API_KEY = os.environ.get("AGNESAI_API_KEY", "your-api-key-here")
BASE_URL = os.environ.get("AGNESAI_BASE_URL", "https://api.agnes-ai.cn").rstrip("/")

INPUT_IMAGE = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/input-image.png"
PROMPT = sys.argv[2] if len(sys.argv) > 2 else "Transform the scene into a rain-soaked cyberpunk night with neon reflections while preserving the original composition"

print("提交图生图请求...")
print(f"  输入图片: {INPUT_IMAGE}")
print(f"  提示词: {PROMPT}")

payload = {
    "model": "agnes-image-2.5-flash",
    "prompt": PROMPT,
    "size": "2K",
    "ratio": "16:9",
    "extra_body": {
        "image": [INPUT_IMAGE],
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
