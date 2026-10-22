# Agnes Video 2.5 Flash Skill

这是一个用于生成视频的 AI 模型技能，基于 Agnes AI 的 Video 2.5 Flash 模型。

## 功能特性

- 文生视频
- 首尾帧控制
- 图片参考（最多 5 张）
- 音频参考（最多 3 段）
- 多种画幅比例

## 快速开始

### 1. 配置 API Key

复制 `.env.example` 为 `.env`（放在本 skill 根目录），填入 API Key：

```
AGNESAI_BASE_URL=https://api.agnes-ai.cn
AGNESAI_API_KEY=sk-你的实际API Key
```

> 脚本会自动从 `.env` 加载，无需手动 export。获取 API Key：https://platform.agnes-ai.cn
> `AGNESAI_BASE_URL` 可选：默认官方端点，走自建/代理网关时修改（不含 `/v1` 路径）。

### 2. 文生视频

```bash
# 不传参数使用默认示例，传参数则使用你的提示词
python examples/text-to-video.py "小猫在客厅里追逐激光笔"
```

### 3. 其他模式

```bash
# 首尾帧控制
python examples/keyframe-video.py https://example.com/first.png https://example.com/last.png "人物转身走向窗边"

# 图片参考
python examples/image-reference.py https://example.com/character.png "以 <Picture 1> 中的角色为参考跳舞"

# 音频参考（URL 或本地文件）
python examples/audio-reference.py https://example.com/beat.mp3 "以 <Audio 1> 的节奏为参考生成夜间驾驶画面"

# 音频参考（本地文件 Base64 内联，免公开托管；不传参数自动生成 8s 演示音）
python examples/audio-reference-base64.py ./beat.mp3 "以 <Audio 1> 的节拍节奏为参考"

# 查询任务结果
python examples/query-video.py <video_id>
```

> 视频生成为异步任务：提交后脚本自动轮询并输出视频地址。所有参数均可选。
>
> **耗时说明：** 视频生成通常需要 **2–5 分钟**（比图像/文本任务慢，属正常现象），脚本会以 5 秒间隔轮询，最长等待 10 分钟。
> **进度显示说明：** 服务端进度只有两档——生成中显示 **10%**，完成后跳到 **100%**，中间不会细分。因此轮询输出中 `10%` 可能停留几分钟，这是正常现象，并非卡住。

## 使用场景

| 场景 | 推荐模式 |
|------|----------|
| 纯文本描述生成视频 | `text` |
| 指定开始和结束画面 | `keyframe` |
| 角色一致性视频 | `reference` + 图片 |
| 声音同步视频 | `reference` + 音频 |

## 价格

- 当前限时免费
- 原价：¥0.15/秒

## 文件结构

```
agnes-2.5-video-flash/
├── SKILL.md                        # 详细说明文档
├── README.md                       # 本文件
└── examples/
    ├── load_env.py                 # .env 自动加载（自包含）
    ├── text-to-video.py            # 参数：[提示词]
    ├── keyframe-video.py           # 参数：[首帧URL] [尾帧URL] [提示词]
    ├── image-reference.py          # 参数：[参考图片URL] [提示词]
    ├── audio-reference.py          # 参数：[参考音频URL或本地文件] [提示词]
    ├── audio-reference-base64.py   # 参数：[本地音频文件路径] [提示词]（Base64 内联，免托管）
    └── query-video.py              # 参数：<video_id> [api_key]
```

## 文档

详见 [SKILL.md](./SKILL.md)
