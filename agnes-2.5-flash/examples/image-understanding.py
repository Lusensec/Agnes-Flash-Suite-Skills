#!/usr/bin/env python3
"""
图像理解示例 - 使用 agnes-2.5-flash 分析图片
用法：python image-understanding.py [图片URL]
"""

import json
import os
import sys
import urllib.request

import load_env
load_env.load_env()

API_KEY = os.environ.get("AGNESAI_API_KEY", "your-api-key-here")
BASE_URL = os.environ.get("AGNESAI_BASE_URL", "https://api.agnes-ai.cn").rstrip("/")

IMAGE_URL = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/image.jpg"

print("发送图像理解请求...")
print(f"图片地址：{IMAGE_URL}")

payload = {
    "model": "agnes-2.5-flash",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "请详细描述这张图片的内容"},
                {
                    "type": "image_url",
                    "image_url": {"url": IMAGE_URL}
                }
            ]
        }
    ]
}

req = urllib.request.Request(
    f"{BASE_URL}/v1/chat/completions",
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

content = result["choices"][0]["message"]["content"]
print("\n模型分析：")
print(content)
