#!/usr/bin/env python3
"""
音频参考示例 - 本地文件 Base64 内联
使用 agnes-video-2.5-flash 生成视频，参考音频为本地文件（自动转 Base64 Data URI，无需公开托管）
用法：python audio-reference-base64.py [本地音频文件路径] [提示词]
  - 不传参数时：用 Python 标准库自动生成 8 秒 440Hz 演示音（wav）并提交
  - 支持格式：mp3 / wav / m4a / aac / ogg / flac 等（单段 < 15MB）
  - 若服务端返回 400 "did not return valid supported media"：该格式不在支持列表，
    用 ffmpeg 转 mp3 后重试：ffmpeg -i in.wav -codec:a libmp3lame out.mp3
"""

import base64
import json
import math
import os
import struct
import sys
import tempfile
import time
import urllib.error
import urllib.request
import wave

import load_env
load_env.load_env()

API_KEY = os.environ.get("AGNESAI_API_KEY", "your-api-key-here")
BASE_URL = os.environ.get("AGNESAI_BASE_URL", "https://api.agnes-ai.cn").rstrip("/")
POLL_URL = f"{BASE_URL}/agnesapi"

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


def make_demo_tone() -> str:
    """生成 8 秒 440Hz 正弦演示音（带 2Hz 慢包络），返回临时 wav 路径"""
    sr = 44100
    seconds = 8
    freq = 440.0
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        for i in range(sr * seconds):
            t = i / sr
            env = min(1.0, i / (sr * 0.5), (sr * seconds - i) / (sr * 0.5))
            v = 0.5 * math.sin(2 * math.pi * freq * t) * env
            w.writeframes(struct.pack("<h", int(max(-1.0, min(1.0, v)) * 32767)))
    return path


def file_to_data_uri(path: str) -> str:
    if not os.path.isfile(path):
        raise SystemExit(f"[ERR] 音频文件不存在: {path}")
    size = os.path.getsize(path)
    if size > MAX_AUDIO_BYTES:
        raise SystemExit(f"[ERR] 音频文件 {size / 1048576:.1f}MB 超过 Flash 单段 15MB 限制")
    ext = os.path.splitext(path)[1].lower()
    mime = AUDIO_MIME.get(ext, "audio/mpeg")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    print(f"  本地音频 -> Base64 Data URI（{mime}, {size / 1024:.0f}KB -> 编码后 {len(b64) // 1024}KB）")
    return f"data:{mime};base64,{b64}"


if len(sys.argv) > 1:
    AUDIO_PATH = sys.argv[1]
else:
    AUDIO_PATH = make_demo_tone()
    print(f"  未传参数，使用自动生成的演示音: {AUDIO_PATH} ({os.path.getsize(AUDIO_PATH) / 1024:.0f}KB)")

PROMPT = sys.argv[2] if len(sys.argv) > 2 else "以 <Audio 1> 的节奏作为参考，节拍小球在木地板上弹跳，节奏感强烈，固定机位"

AUDIO_REF = file_to_data_uri(AUDIO_PATH)

print("提交音频参考视频请求（Base64 内联，无外部依赖）...")
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

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8", "replace")
    if e.code == 400 and "valid supported media" in body:
        print(f"[ERR] 音频格式不被支持（HTTP 400），请用 ffmpeg 转 mp3 后重试：\n{body[:300]}")
        sys.exit(1)
    if e.code == 503:
        print(f"[ERR] 视频队列已满（HTTP 503），请稍后重试：\n{body[:300]}")
        sys.exit(1)
    print(f"[ERR] 提交失败 HTTP {e.code}：{body[:300]}")
    sys.exit(1)

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
