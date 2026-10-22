#!/usr/bin/env python3
"""
基础聊天示例 - 使用 agnes-2.5-flash 进行对话
用法：python basic-chat.py [用户问题]
"""

import json
import os
import sys
import urllib.request

import load_env
load_env.load_env()

API_KEY = os.environ.get("AGNESAI_API_KEY", "your-api-key-here")
BASE_URL = os.environ.get("AGNESAI_BASE_URL", "https://api.agnes-ai.cn").rstrip("/")

USER_MESSAGE = sys.argv[1] if len(sys.argv) > 1 else "Explain how autonomous agents use tools to complete tasks."

print("发送聊天请求...")
print(f"  用户: {USER_MESSAGE}")

payload = {
    "model": "agnes-2.5-flash",
    "messages": [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": USER_MESSAGE}
    ],
    "temperature": 0.7,
    "max_tokens": 1024
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
print("\n模型回复：")
print(content)
