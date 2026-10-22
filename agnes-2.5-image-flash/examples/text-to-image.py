#!/usr/bin/env python3
"""
文生图示例 - URL 输出
使用 agnes-image-2.5-flash 生成图像
用法：python text-to-image.py [提示词] [尺寸] [比例]
"""

import json
import os
import sys
import urllib.request

import load_env
load_env.load_env()

API_KEY = os.environ.get("AGNESAI_API_KEY", "your-api-key-here")
BASE_URL = os.environ.get("AGNESAI_BASE_URL", "https://api.agnes-ai.cn").rstrip("/")

# 从命令行参数读取（可选），否则使用默认值
PROMPT = sys.argv[1] if len(sys.argv) > 1 else "A luminous floating city above a misty canyon at sunrise, cinematic realism, wide angle, rich architectural details, soft golden light, high visual density"
SIZE = sys.argv[2] if len(sys.argv) > 2 else "2K"
RATIO = sys.argv[3] if len(sys.argv) > 3 else "16:9"

print(f"提交文生图请求...")
print(f"  提示词: {PROMPT}")
print(f"  尺寸: {SIZE}, 比例: {RATIO}")

payload = {
    "model": "agnes-image-2.5-flash",
    "prompt": PROMPT,
    "size": SIZE,
    "ratio": RATIO,
    "extra_body": {"response_format": "url"}
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
