---
name: agnes-flash-suite-skills
description: |
  Agnes Flash 全能力套件 Skill。
  包含 3.0/2.5 对话模型、图像生成、视频生成四大核心能力。
  
  子 Skill 列表：
  - agnes-3.0-flash (Agent 编程/工具编排/可信交付)
  - agnes-2.5-flash (对话/推理/图像理解)
  - agnes-2.5-image-flash (文生图/图生图/多图合成)
  - agnes-2.5-video-flash (文生视频/首尾帧/图片参考)
  
  触发词：agnes、AI助手、聊天、生图、图像生成、视频生成、文生视频、图片理解、工具调用、thinking、agent、3.0
---

# Agnes Flash 全能力套件

> **灵活使用：** 本套件可整体安装，也可单独提取任意子目录（如 `agnes-2.5-image-flash/`）作为独立 Skill 使用。每个子 Skill 自包含 `SKILL.md` + `examples/*.py`（含 `load_env.py`），无需依赖其他模块。

## 概述

Agnes Flash 套件是一个多功能 AI 能力平台，整合了四种核心模型能力：

| 子 Skill | 模型 ID | 核心能力 | 触发场景 |
|----------|---------|----------|----------|
| **agnes-3.0-flash** | `agnes-3.0-flash` | Agent 编程、工具编排、可信交付 | 复杂任务、代码智能体、长任务 |
| **agnes-2.5-flash** | `agnes-2.5-flash` | 对话、推理、图像理解、工具调用 | 问答、代码、分析、Vision |
| **agnes-image-2.5-flash** | `agnes-image-2.5-flash` | 文生图、图生图、多图合成 | 图像创作、设计、编辑 |
| **agnes-video-2.5-flash** | `agnes-video-2.5-flash` | 文生视频、首尾帧、图片/音频参考 | 视频制作、动画、创意 |

## 快速开始（推荐使用 Python）

所有示例脚本均位于各子 Skill 的 `examples/` 目录，**支持命令行参数传入用户内容**：

```bash
# 文生图（可选传提示词、尺寸、比例）
python agnes-2.5-image-flash/examples/text-to-image.py "一只可爱的田园犬在稻田边" "2K" "16:9"

# 图像理解（可选传图片URL）
python agnes-2.5-flash/examples/image-understanding.py https://example.com/image.jpg

# 基础聊天（可选传用户问题）
python agnes-2.5-flash/examples/basic-chat.py "用 Python 写一个快速排序算法"

# 文生视频（可选传提示词）
python agnes-2.5-video-flash/examples/text-to-video.py "小猫在客厅里追逐激光笔"

# 工具调用（可选传用户问题）
python agnes-3.0-flash/examples/tool-calling.py "查询新加坡今天的天气"
```

> **不传参数时使用默认演示内容**，方便快速体验；**传参数时动态替换**，满足实际使用需求。

API Key 从 `.env` 文件自动加载（环境变量 `AGNESAI_API_KEY`），无需手动设置。

> **视频生成耗时提示：** 视频类任务通常需 **2–5 分钟**（明显慢于图像/文本，属正常）。轮询时进度恒显示 10%，完成后跳到 100%（服务端仅两档，中间不细分），请勿误判为卡住。

---

## 各子 Skill 详情

### 1. Agent 编程模型 (agnes-3.0-flash)

```python
# 基础任务执行（保存为 examples/basic-chat.py，直接运行）
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/chat/completions",
    data=json.dumps({"model":"agnes-3.0-flash","messages":[
        {"role":"system","content":"You are a helpful AI assistant."},
        {"role":"user","content":"Explain how autonomous agents use tools to complete tasks."}
    ],"temperature":0.7,"max_tokens":1024}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()
print(json.loads(resp)["choices"][0]["message"]["content"])
```

**文档**: [agnes-3.0-flash/SKILL.md](./agnes-3.0-flash/SKILL.md)

---

### 2. 对话模型 (agnes-2.5-flash)

```python
# 基础聊天
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/chat/completions",
    data=json.dumps({"model":"agnes-2.5-flash","messages":[
        {"role":"user","content":"你好，请介绍一下自己"}
    ]}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()
print(json.loads(resp)["choices"][0]["message"]["content"])

# 图像理解
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/chat/completions",
    data=json.dumps({"model":"agnes-2.5-flash","messages":[{
        "role":"user",
        "content":[
            {"type":"text","text":"这张图片里有什么？"},
            {"type":"image_url","image_url":{"url":"https://example.com/image.jpg"}}
        ]
    }]}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()

# Thinking 模式
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/chat/completions",
    data=json.dumps({"model":"agnes-2.5-flash","messages":[
        {"role":"user","content":"帮我写一个 Python 脚本"}
    ],"chat_template_kwargs":{"enable_thinking":True}}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()
```

> **思考等级**：顶层 `reasoning_effort` 参数。2.5 支持 `none/low/medium/high/max`（`minimal`/`xhigh` 会 400）；
> 3.0 支持 `none/minimal/low/medium/high/xhigh/max` 共 7 档。默认不设置。详见各子 Skill 文档。

**文档**: [agnes-2.5-flash/SKILL.md](./agnes-2.5-flash/SKILL.md)

---

### 3. 图像生成 (agnes-image-2.5-flash)

```python
# 文生图
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/images/generations",
    data=json.dumps({"model":"agnes-image-2.5-flash","prompt":"一只可爱的田园犬在稻田边","size":"2K","ratio":"16:9","extra_body":{"response_format":"url"}}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()
print(json.loads(resp)["data"][0]["url"])

# 图生图
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/images/generations",
    data=json.dumps({"model":"agnes-image-2.5-flash","prompt":"转换为赛博朋克风格","size":"2K","extra_body":{"image":["https://example.com/input.png"],"response_format":"url"}}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()

# 多图合成
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/images/generations",
    data=json.dumps({"model":"agnes-image-2.5-flash","prompt":"将两张图合成","size":"2K","extra_body":{"image":["https://example.com/img1.png","https://example.com/img2.png"],"response_format":"url"}}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()
```

**文档**: [agnes-2.5-image-flash/SKILL.md](./agnes-2.5-image-flash/SKILL.md)

---

### 4. 视频生成 (agnes-video-2.5-flash)

```python
# 文生视频
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/videos",
    data=json.dumps({"model":"agnes-video-2.5-flash","prompt":"小猫在客厅跳舞","seconds":"5","mode":"text","size":"720P","aspect_ratio":"16:9"}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()
video_id = json.loads(resp)["video_id"]

# 首尾帧控制
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/videos",
    data=json.dumps({"model":"agnes-video-2.5-flash","prompt":"人物转身走向窗边","seconds":"5","mode":"keyframe","first_frame":"https://example.com/first.png","last_frame":"https://example.com/last.png"}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()

# 图片参考
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/videos",
    data=json.dumps({"model":"agnes-video-2.5-flash","prompt":"以 <Picture 1> 中的角色为参考跳舞","seconds":"5","mode":"reference","images":["https://example.com/character.png"]}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()
```

**查询任务**:
```python
resp = urllib.request.urlopen(urllib.request.Request(
    f"https://api.agnes-ai.cn/agnesapi?video_id=VIDEO_ID&model_name=agnes-video-2.5-flash",
    headers={"Authorization":f"Bearer {API_KEY}"}
)).read()
```

**文档**: [agnes-2.5-video-flash/SKILL.md](./agnes-2.5-video-flash/SKILL.md)

---

## 完整工作流示例

### 从文字到视频的完整创作流程

```python
import json, urllib.request, os, time

API_KEY = os.environ.get("AGNESAI_API_KEY")

# Step 1: 生成田园犬图片
def gen_image(prompt, size="2K", ratio="16:9", extra_body=None):
    # 文生图可不传 extra_body；多图合成时传 {"image":[...],"response_format":"url"}
    payload = {"model":"agnes-image-2.5-flash","prompt":prompt,"size":size,"ratio":ratio,
               "extra_body": extra_body or {"response_format":"url"}}
    resp = urllib.request.urlopen(urllib.request.Request(
        "https://api.agnes-ai.cn/v1/images/generations",
        data=json.dumps(payload).encode(),
        headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
        method="POST"
    )).read()
    return json.loads(resp)["data"][0]["url"]

# Step 2: 生成狸花猫图片
url1 = gen_image("一只可爱的田园犬在阳光明媚的乡村田园中")
url2 = gen_image("一只漂亮的狸花猫在阳光斑驳的老槐树下")

# Step 3: 多图合成
merged_url = gen_image(
    "田园犬和狸花猫在大山背景下和谐共处",
    extra_body={"image":[url1,url2],"response_format":"url"}
)

# Step 4: 使用合成图生成视频
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/videos",
    data=json.dumps({"model":"agnes-video-2.5-flash","prompt":"田园犬和狸花猫在大山背景下快乐玩耍","seconds":"5","mode":"reference","images":[merged_url]}).encode(),
    headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
    method="POST"
)).read()
video_id = json.loads(resp)["video_id"]
print(f"视频任务已提交: {video_id}")
```

---

## 技术规格对比

| 特性 | agnes-3.0-flash / agnes-2.5-flash | agnes-image-2.5-flash | agnes-video-2.5-flash |
|------|-----------------------------------|-----------------------|-----------------------|
| **模型 ID** | `agnes-3.0-flash` / `agnes-2.5-flash` | `agnes-image-2.5-flash` | `agnes-video-2.5-flash` |
| **API 端点** | `/v1/chat/completions` | `/v1/images/generations` | `/v1/videos` |
| **上下文** | 512K | - | - |
| **最大输出** | 65.5K | - | - |
| **超时** | 60s | 360s | 600s |
| **计费** | 免费 | 免费 | 免费 |

---

## 使用场景矩阵

| 需求 | 推荐子 Skill | 说明 |
|------|-------------|------|
| Agent 编程/复杂任务 | agnes-3.0-flash | 强化工具编排与可信交付 |
| 长任务多轮执行 | agnes-3.0-flash | 指令与上下文遵循 |
| 问答/聊天 | agnes-2.5-flash | 通用对话、知识问答 |
| 代码生成/调试 | agnes-2.5-flash | 支持 Thinking 模式 |
| 图像理解 | agnes-2.5-flash | 支持 Vision 输入 |
| 工具调用 | agnes-2.5-flash | Function Calling |
| 文生图 | agnes-image-2.5-flash | 从文字描述生成图片 |
| 图生图 | agnes-image-2.5-flash | 图像编辑/风格迁移 |
| 多图合成 | agnes-image-2.5-flash | 组合多张参考图 |
| 文生视频 | agnes-video-2.5-flash | 纯文本生成视频 |
| 图片转视频 | agnes-video-2.5-flash | 使用图片作为参考 |
| 首尾帧控制 | agnes-video-2.5-flash | 指定开始和结束画面 |

---

## 文件结构

```
agnes-flash-suite/
├── SKILL.md                          # 本文件（主文档）
├── README.md                         # 安装与使用说明
├── .env.example                      # API Key 模板（复制为 .env）
├── agnes-3.0-flash/                  # Agent 编程模型子 Skill
│   ├── SKILL.md
│   ├── README.md
│   └── examples/
│       ├── load_env.py               # .env 自动加载（自包含）
│       ├── basic-chat.py             # 参数：[用户问题]
│       ├── image-understanding.py    # 参数：[图片URL]
│       ├── tool-calling.py           # 参数：[用户问题]
│       └── thinking-mode.py          # 参数：[问题] [思考等级] [max_tokens]
├── agnes-2.5-flash/                  # 对话模型子 Skill
│   ├── SKILL.md
│   ├── README.md
│   └── examples/
│       ├── load_env.py
│       ├── basic-chat.py             # 参数：[用户问题]
│       ├── image-understanding.py    # 参数：[图片URL]
│       ├── tool-calling.py           # 参数：[用户问题]
│       └── thinking-mode.py          # 参数：[问题] [思考等级] [max_tokens]
├── agnes-2.5-image-flash/            # 图像生成子 Skill
│   ├── SKILL.md
│   ├── README.md
│   └── examples/
│       ├── load_env.py
│       ├── text-to-image.py          # 参数：[提示词] [尺寸] [比例]
│       ├── text-to-image-base64.py   # 参数：[提示词] [尺寸]
│       ├── image-to-image.py         # 参数：[输入图片URL] [提示词]
│       └── multi-image-combine.py    # 参数：[图片1URL] [图片2URL] [提示词]
└── agnes-2.5-video-flash/            # 视频生成子 Skill
    ├── SKILL.md
    ├── README.md
    └── examples/
        ├── load_env.py
        ├── text-to-video.py          # 参数：[提示词]
        ├── keyframe-video.py         # 参数：[首帧URL] [尾帧URL] [提示词]
        ├── image-reference.py        # 参数：[参考图片URL] [提示词]
        ├── audio-reference.py        # 参数：[参考音频URL或本地文件] [提示词]
        ├── audio-reference-base64.py # 参数：[本地音频文件路径] [提示词]（Base64 内联，免托管）
        └── query-video.py            # 参数：<video_id> [api_key]
```

---

## 常见问题

### Q: 四个模型可以同时使用吗？
A: 是的，它们是完全独立的服务，可以任意组合使用。

### Q: API Key 是否通用？
A: 是的，使用同一个 API Key 即可访问所有模型。

### Q: 定价如何计算？
A: 当前所有模型均处于免费推广期，未来定价请参考官方文档。

### Q: 如何选择使用哪个模型？
A: 根据需求选择：
- 需要对话/理解/推理 → 使用对话模型
- 需要生成图片 → 使用图像模型
- 需要生成视频 → 使用视频模型

---

## 相关文档

- [Agnes AI 官方文档](https://agnes-ai.cn/zh-Hans/docs)
- [Agnes AI 平台](https://platform.agnes-ai.cn)
- [完整文档索引](https://wiki.agnes-ai.cn/llms.txt)
