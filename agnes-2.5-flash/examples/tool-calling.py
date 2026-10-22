#!/usr/bin/env python3
"""
工具调用示例 - 使用 agnes-2.5-flash 进行 Function Calling
用法：python tool-calling.py [用户问题]
"""

import json
import os
import sys
import urllib.request

import load_env
load_env.load_env()

API_KEY = os.environ.get("AGNESAI_API_KEY", "your-api-key-here")
BASE_URL = os.environ.get("AGNESAI_BASE_URL", "https://api.agnes-ai.cn").rstrip("/")

USER_MESSAGE = sys.argv[1] if len(sys.argv) > 1 else "What is the weather like in Singapore today?"

print("发送工具调用请求...")
print(f"  用户: {USER_MESSAGE}")

payload = {
    "model": "agnes-2.5-flash",
    "messages": [
        {"role": "user", "content": USER_MESSAGE}
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and country"
                        }
                    },
                    "required": ["location"]
                }
            }
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

message = result["choices"][0]["message"]
tool_calls = message.get("tool_calls")

print("\n工具调用：")
if tool_calls:
    print(json.dumps(tool_calls, indent=2, ensure_ascii=False))
    print("\n 请实现工具执行逻辑，并将结果发送回模型")
else:
    print("无工具调用")
