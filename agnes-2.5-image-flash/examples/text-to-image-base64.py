#!/usr/bin/env python3
"""
文生图示例 - Base64 输出
使用 agnes-image-2.5-flash 生成图像（返回 Base64）
用法：python text-to-image-base64.py [提示词] [尺寸]
"""

import json
import os
import urllib.request
import sys

import load_env
load_env.load_env()

API_KEY = os.environ.get("AGNESAI_API_KEY", "your-api-key-here")
BASE_URL = os.environ.get("AGNESAI_BASE_URL", "https://api.agnes-ai.cn").rstrip("/")

PROMPT = sys.argv[1] if len(sys.argv) > 1 else "A clean product photo of a glass cube on a white studio background, soft shadows, high detail"
SIZE = sys.argv[2] if len(sys.argv) > 2 else "1K"

print("提交文生图请求（Base64 输出）...")
print(f"  提示词: {PROMPT}")
print(f"  尺寸: {SIZE}")

payload = {
    "model": "agnes-image-2.5-flash",
    "prompt": PROMPT,
    "size": SIZE,
    "ratio": "1:1",
    "return_base64": True
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

b64_data = result["data"][0]["b64_json"]
if not b64_data:
    print("[ERR] 获取 Base64 数据失败")
    sys.exit(1)

print("[OK] 图片生成完成！")
print(f"Base64 长度：{len(b64_data)} 字符")
print("\nData URI 格式：")
print(f"data:image/png;base64,{b64_data[:100]}...")
