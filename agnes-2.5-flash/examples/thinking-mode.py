#!/usr/bin/env python3
"""
Thinking 模式示例 - 使用 agnes-2.5-flash 进行深度推理
用法：python thinking-mode.py [问题] [思考等级] [max_tokens]

思考等级（可选，reasoning_effort 顶层参数）：
  none / low / medium / high / max
注意：2.5 不支持 minimal 和 xhigh（传入会返回 400 错误）。
不传则不设置思考等级（默认行为）。

最大输出 Token [max_tokens]（可选）：
  省略或传 0：不设置（交给服务端默认上限）
  正整数：限制输出预算；思考链与回答共用该预算，
  复杂推理任务建议调高（如 8192）避免截断
"""

import json
import os
import sys
import urllib.request

import load_env
load_env.load_env()

API_KEY = os.environ.get("AGNESAI_API_KEY", "your-api-key-here")
BASE_URL = os.environ.get("AGNESAI_BASE_URL", "https://api.agnes-ai.cn").rstrip("/")

USER_MESSAGE = sys.argv[1] if len(sys.argv) > 1 else "Help me write a Python script to process a CSV file and generate a summary report."
THINKING_LEVEL = sys.argv[2] if len(sys.argv) > 2 else None
MAX_TOKENS = 0
if len(sys.argv) > 3:
    if not sys.argv[3].isdigit():
        print(f"[ERR] 无效的 max_tokens: {sys.argv[3]}（正整数；省略或 0 表示不设置）")
        sys.exit(1)
    MAX_TOKENS = int(sys.argv[3])

VALID_LEVELS = ("none", "low", "medium", "high", "max")
if THINKING_LEVEL and THINKING_LEVEL not in VALID_LEVELS:
    print(f"[ERR] 无效的思考等级: {THINKING_LEVEL}，可选值: {'/'.join(VALID_LEVELS)}")
    print("（2.5-flash 不支持 minimal / xhigh）")
    sys.exit(1)

print("发送 Thinking 模式请求...")
print(f"  用户: {USER_MESSAGE}")
if THINKING_LEVEL:
    print(f"  思考等级: {THINKING_LEVEL}")
if MAX_TOKENS > 0:
    print(f"  最大输出 Token: {MAX_TOKENS}")

payload = {
    "model": "agnes-2.5-flash",
    "messages": [
        {"role": "user", "content": USER_MESSAGE}
    ],
    "chat_template_kwargs": {"enable_thinking": True}
}
# 默认不设置思考等级与 max_tokens；指定后通过顶层 reasoning_effort 控制思考强度
if THINKING_LEVEL:
    payload["reasoning_effort"] = THINKING_LEVEL
if MAX_TOKENS > 0:
    payload["max_tokens"] = MAX_TOKENS

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
print("\n模型思考过程 + 回复：")
print(content)
