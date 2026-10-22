#!/usr/bin/env python3
"""
音频参考示例
使用 agnes-video-2.5-flash 生成视频（音频作为参考）
用法：python audio-reference.py [参考音频URL或本地文件路径] [提示词]
  - http(s):// URL 或 data: URI：原样发送
  - 本地文件路径：自动读取并转 Base64 Data URI（无需公开托管）
"""

import base64
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

AUDIO_SOURCE = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/reference-audio.mp3"
PROMPT = sys.argv[2] if len(sys.argv) > 2 else "以 <Audio 1> 的节奏和环境氛围作为参考，生成电影感夜间驾驶画面"

# 常见音频扩展名 -> MIME
AUDIO_MIME = {
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".oga": "audio/ogg",
    ".flac": "audio/flac",
}

MAX_AUDIO_BYTES = 15 * 1024 * 1024  # Flash 限制：单段音频 < 15MB


def resolve_audio_ref(source):
    """把音频参考参数解析为可直接提交的值：
    - http(s):// URL：原样返回（须 Agnes 服务可公开访问，且在任务完成前保持有效）
    - data: URI：原样返回
    - 本地文件路径：读取并转 Base64 Data URI（免托管；未文档化但服务端校验门接受，2026-10 实测）
    """
    if source.startswith(("http://", "https://", "data:")):
        return source
    if not os.path.isfile(source):
        raise SystemExit(f"[ERR] 音频文件不存在: {source}（也可传公开 URL 或 data: URI）")
    size = os.path.getsize(source)
    if size > MAX_AUDIO_BYTES:
        raise SystemExit(f"[ERR] 音频文件 {size / 1048576:.1f}MB 超过 Flash 单段 15MB 限制，请压缩或截短后重试")
    ext = os.path.splitext(source)[1].lower()
    mime = AUDIO_MIME.get(ext, "audio/mpeg")
    with open(source, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    print(f"  本地音频 -> Base64 Data URI（{mime}, {size / 1024:.0f}KB -> 编码后 {len(b64) // 1024}KB）")
    return f"data:{mime};base64,{b64}"


AUDIO_REF = resolve_audio_ref(AUDIO_SOURCE)

print("提交音频参考视频请求...")
print(f"  参考音频: {AUDIO_REF[:100]}{'...' if len(AUDIO_REF) > 100 else ''}")
print(f"  提示词: {PROMPT}")

payload = {
    "model": "agnes-video-2.5-flash",
    "prompt": PROMPT,
    "seconds": "5",
    "mode": "reference",
    "size": "720P",
    "aspect_ratio": "16:9",
    "audios": [AUDIO_REF]
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
