---
name: agnes-2.5-video-flash
description: |
  Agnes Video 2.5 Flash 视频生成 Skill（模型 ID: agnes-video-2.5-flash）。
  支持文生视频、首尾帧控制、图片参考、音频参考等多种模式。
  官方文档：https://agnes-ai.cn/zh-Hans/docs/agnes-video-25-flash
  触发词：视频生成、视频、video generation、首尾帧、图片转视频
---

# Agnes Video 2.5 Flash 视频生成 Skill

## 概述

Agnes Video 2.5 Flash 是 Agnes AI 的视频生成模型，支持多种生成模式：

| 模式 | API mode | 说明 |
|------|----------|------|
| **文生视频** | `text` | 纯文本生成视频 |
| **首尾帧控制** | `keyframe` | 指定开始和结束帧 |
| **图片参考** | `reference` | 使用图片作为参考（最多 5 张） |
| **音频参考** | `reference` | 使用音频作为参考（最多 3 段） |

## API 信息

- **提交端点**: `POST https://api.agnes-ai.cn/v1/videos`
- **查询端点**: `GET https://api.agnes-ai.cn/agnesapi?video_id=<ID>&model_name=agnes-video-2.5-flash`
- **模型 ID**: `agnes-video-2.5-flash`

## 支持的参数

### 公共参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 模型名称，使用 `agnes-video-2.5-flash` |
| `prompt` | string | ✅ | 视频描述提示词 |
| `seconds` | string | ✅ | 视频时长，字符串 `"4"`–`"12"`，默认 `"5"` |
| `mode` | string | ✅ | 生成模式：`text` / `keyframe` / `reference` |
| `size` | string | ✅ | 固定 `"720P"` |
| `aspect_ratio` | string | ❌ | 画幅比例，可省略（服务端有默认值，2026-10 实测缺省提交可正常受理） |
| `n` | number | ❌ | 可省略；指定时固定为 `1`（2026-10 实测缺省提交可正常受理） |
| `seed` | number | ❌ | 随机种子，可选 |

### 画幅比例 (aspect_ratio)

| 值 | 输出像素 |
|----|----------|
| `21:9` | 1680×720 |
| `16:9` | 1280×720 |
| `4:3` | 960×720 |
| `1:1` | 720×720 |
| `3:4` | 720×960 |
| `9:16` | 720×1280 |

### 首尾帧控制 (keyframe 模式)

| 参数 | 类型 | 说明 |
|------|------|------|
| `first_frame` | string | 首帧图像 URL 或 Base64 |
| `last_frame` | string | 尾帧图像 URL 或 Base64 |

**至少需要一个（首帧或尾帧）**

### 图片参考 (reference 模式)

| 参数 | 类型 | 说明 |
|------|------|------|
| `images` | string[] | 参考图片数组（最多 5 张） |

在 prompt 中使用 `<Picture N>` 指代图片：
```
以 <Picture 1> 中的角色和美术风格为参考，角色在花田中自然奔跑，保持外观一致
```

### 音频参考 (reference 模式)

| 参数 | 类型 | 说明 |
|------|------|------|
| `audios` | string[] | 参考音频数组（最多 3 段）。每项可为**公开 URL** 或 **Base64 Data URI**（`data:audio/mpeg;base64,…`，免托管） |

约束（Flash）：单段 < 15MB、音频总时长 2–12 秒、单次请求媒体总量 < 64MB。
URL 形式须 Agnes 服务可公开访问且在任务完成前保持有效；Data URI 形式无此限制。

在 prompt 中使用 `<Audio N>` 指代音频：
```
以 <Audio 1> 的节奏和环境氛围作为参考，生成电影感夜间驾驶画面
```

## Flash 专属限制

| 校验项 | Flash 规则 | 失败响应 |
|--------|------------|----------|
| `size` | 仅支持 `"720P"` | HTTP 400: `size must be 720P` |
| `reference.images` | 最多 5 张 | HTTP 400: `images length must not exceed 5` |
| `reference.audios` | 最多 3 段 | HTTP 400: `audios length must not exceed 3` |
| `reference.videos` | **不支持** | HTTP 400: `videos is not supported` |

**重要：** Flash 专属校验在任务创建、排队、计费和推理前执行。校验失败的请求不会创建视频任务，也不会产生费用。

## 请求示例

### 1. 文生视频

```python
# 运行 python examples/text-to-video.py [提示词]（参数可选）
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/videos",
    data=json.dumps({
        "model": "agnes-video-2.5-flash",
        "prompt": "雨后的未来城市街道，霓虹灯倒映在地面，一辆银色跑车缓慢驶过，电影级运镜，自然环境声",
        "seconds": "5",
        "mode": "text",
        "size": "720P",
        "aspect_ratio": "16:9"
    }).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST"
)).read()
print(json.loads(resp)["video_id"])
```

### 2. 首尾帧控制

```python
# 运行 python examples/keyframe-video.py [首帧URL] [尾帧URL] [提示词]（参数可选）
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/videos",
    data=json.dumps({
        "model": "agnes-video-2.5-flash",
        "prompt": "人物从首帧姿态自然转身走向窗边，镜头缓慢推进并平滑过渡到尾帧",
        "seconds": "5",
        "mode": "keyframe",
        "size": "720P",
        "first_frame": "https://example.com/first.png",
        "last_frame": "https://example.com/last.png"
    }).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST"
)).read()
print(json.loads(resp)["video_id"])
```

### 3. 图片参考

```python
# 运行 python examples/image-reference.py [参考图片URL] [提示词]（参数可选）
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/videos",
    data=json.dumps({
        "model": "agnes-video-2.5-flash",
        "prompt": "以 <Picture 1> 中的角色和美术风格为参考，角色在花田中自然奔跑，保持外观一致",
        "seconds": "5",
        "mode": "reference",
        "size": "720P",
        "aspect_ratio": "16:9",
        "images": ["https://example.com/character.png"]
    }).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST"
)).read()
print(json.loads(resp)["video_id"])
```

### 4. 音频参考

```python
# 运行 python examples/audio-reference.py [参考音频URL或本地文件路径] [提示词]（参数可选）
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/videos",
    data=json.dumps({
        "model": "agnes-video-2.5-flash",
        "prompt": "以 <Audio 1> 的节奏和环境氛围作为参考，生成电影感夜间驾驶画面",
        "seconds": "5",
        "mode": "reference",
        "size": "720P",
        "aspect_ratio": "16:9",
        "audios": ["https://example.com/reference-audio.mp3"]
    }).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST"
)).read()
print(json.loads(resp)["video_id"])
```

### 5. 音频参考（本地文件 / Base64 内联）

本地音频无需公开托管：读文件转 Base64 Data URI 直接放进 `audios`（官方文档未写明，服务端校验门实测接受，2026-10 验证）：

```python
# 运行 python examples/audio-reference-base64.py [本地音频文件路径] [提示词]（参数可选）
import base64, json, os, urllib.request
API_KEY = os.environ.get("AGNESAI_API_KEY")
with open("beat.mp3", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("ascii")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/videos",
    data=json.dumps({
        "model": "agnes-video-2.5-flash",
        "prompt": "以 <Audio 1> 的节拍节奏为参考，画面动作与节拍同步",
        "seconds": "5",
        "mode": "reference",
        "size": "720P",
        "aspect_ratio": "16:9",
        "audios": [f"data:audio/mpeg;base64,{audio_b64}"]
    }).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST"
)).read()
print(json.loads(resp)["video_id"])
```

> **注意**：Base64 编码后体积膨胀约 33%，注意 Flash 单段 15MB / 单次请求 64MB 上限；
> 若某格式被 400 拒收（`did not return valid supported media`），用 ffmpeg 转 mp3 再试。

## 查询任务结果

```python
# 运行 python examples/query-video.py <video_id> [api_key]
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    f"https://api.agnes-ai.cn/agnesapi?video_id={VIDEO_ID}&model_name=agnes-video-2.5-flash",
    headers={"Authorization": f"Bearer {API_KEY}"}
)).read()
result = json.loads(resp)
print(result["status"], result.get("url"))
```

**响应示例：**
```json
{
  "status": "completed",
  "progress": 100,
  "video_id": "xxx",
  "url": "https://cdn.agnes-ai.cn/output/xxx.mp4",
  "metadata": {
    "url": "https://cdn.agnes-ai.cn/output/xxx.mp4"
  }
}
```

**状态值：**
- `pending` - 排队中
- `processing` - 生成中
- `completed` - 完成
- `failed` - 失败

## 计费规则

```
视频总金额 = 输出秒数 × 输出分辨率单价
           + 输入视频秒数 × 输出分辨率单价
           + max(0, 图片数 - 免费图片张数) × 图片超额单价
```

**当前优惠：**
- 输出：¥0 / 秒（原价 ¥0.15 / 秒）
- 参考图片：前 5 张免费
- 输入视频：¥0

## TypeScript 实现示例

```typescript
interface VideoConfig {
  duration: number;
  resolution: string;
  aspectRatio: "16:9" | "9:16";
  prompt: string;
  referenceList?: ReferenceList[];
  mode: VideoMode[];
}

type VideoMode =
  | "singleImage"
  | "startEndRequired"
  | "endFrameOptional"
  | "startFrameOptional"
  | "text"
  | (`videoReference:${number}` | `imageReference:${number}` | `audioReference:${number}`)[];

const videoRequestFlash = async (config: VideoConfig, _model: VideoModel): Promise<string> => {
  const apiKey = getApiKey();
  
  // seconds（字符串 "4"-"12"，默认 "5"）
  const seconds = String(Math.min(12, Math.max(4, Math.round(config.duration || 5))));
  
  // aspect_ratio
  const FLASH_SUPPORTED_RATIOS: Record<string, string> = {
    "21:9": "21:9",
    "16:9": "16:9",
    "4:3": "4:3",
    "1:1": "1:1",
    "3:4": "3:4",
    "9:16": "9:16",
  };
  const aspectRatio = FLASH_SUPPORTED_RATIOS[config.aspectRatio] || "16:9";
  
  // 收集参考素材
  const refImages = collectImageDataURIs(config);
  const refAudios = ((config.referenceList || []) as ReferenceList[])
    .filter((r) => r.type === "audio")
    .map((r) => ensureDataUriHead(r.base64));
  
  // 模式判定
  const needsKeyframe =
    config.mode.includes("startEndRequired") ||
    config.mode.includes("startFrameOptional") ||
    config.mode.includes("endFrameOptional");
  
  let mode: "text" | "keyframe" | "reference";
  if (needsKeyframe) {
    mode = "keyframe";
  } else if (refImages.length > 0 || refAudios.length > 0) {
    mode = "reference";
  } else {
    mode = "text";
  }
  
  // 构建请求体
  const body: Record<string, any> = {
    model: "agnes-video-2.5-flash",
    prompt: config.prompt,
    seconds,
    mode,
    size: "720P",
    aspect_ratio: aspectRatio,
    n: 1,
  };
  
  if (mode === "keyframe") {
    if (refImages.length >= 1) body.first_frame = refImages[0];
    if (refImages.length >= 2) body.last_frame = refImages[1];
  } else if (mode === "reference") {
    if (refImages.length > 0) body.images = refImages.slice(0, 5);
    if (refAudios.length > 0) body.audios = refAudios;
  }
  
  // 提交任务
  const submitResp = await axios.post(
    `${AGNES_BASE_URL}/videos`,
    body,
    { headers: getAuthHeaders(), timeout: 60 * 1000 },
  );
  
  const videoId = submitResp.data.video_id;
  
  // 轮询查询结果
  const pollRes = await pollTask(
    async () => {
      const queryResp = await axios.get(AGNES_POLL_URL, {
        headers: { Authorization: `Bearer ${apiKey}` },
        params: { video_id: videoId, model_name: "agnes-video-2.5-flash" },
        timeout: 30 * 1000,
      });
      const queryData = queryResp.data;
      
      switch (queryData.status) {
        case "completed":
          return {
            completed: true,
            data: queryData.metadata?.url || queryData.url || ""
          };
        case "failed":
          return {
            completed: true,
            error: queryData.error?.message || "视频生成失败"
          };
        default:
          return { completed: false };
      }
    },
    5000,
    600000,
  );
  
  if (pollRes.error) throw new Error(`[Agnes Video Flash] ${pollRes.error}`);
  if (!pollRes.data) throw new Error("[Agnes Video Flash] 结果 URL 为空");
  return pollRes.data;
};
```

## 常见问题

### Q: Flash 不支持视频参考？

A: 是的，`agnes-video-2.5-flash` 不支持 `videos` 参考。如果传入有效视频内容，会返回 HTTP 400 错误：`videos is not supported`。如需视频参考功能，请使用 `agnes-video-2.5`（非 Flash）模型。

### Q: 首尾帧必须同时传吗？

A: 不需要。`first_frame` 和 `last_frame` 至少需要一个。可以只传首帧、只传尾帧，或两者都传。

### Q: 图片参考最多几张？

A: Flash 版本最多支持 5 张图片。超过 5 张会返回 HTTP 400 错误：`images length must not exceed 5`。

### Q: 如何获取视频结果？

A: 提交任务后，使用 `video_id` 轮询查询接口。当 `status` 为 `completed` 时，从 `metadata.url` 或 `url` 字段获取视频地址。

### Q: 超时时间建议？

A: 视频生成可能需要较长时间，**通常需 2–5 分钟**完成，建议：
- 提交请求超时：60 秒
- 轮询间隔：5 秒
- 总超时：600 秒（10 分钟）

### Q: 为什么进度一直显示 10%？

A: 服务端的 `progress` 字段只有两档：生成中恒为 **10**，完成后跳到 **100**，中间不细分。轮询期间长时间停留在 10% 属正常现象（视频生成通常需 2–5 分钟），并非任务卡住。

### Q: 本地音频文件能直接做参考吗，必须放公开 URL？

A: 不必。`audios` 支持 **Base64 Data URI**（`data:audio/mpeg;base64,…`），本地文件读出来编码即可，免去公开托管；注意单段 < 15MB、请求体 < 64MB。参见示例 `examples/audio-reference-base64.py`。

## 相关文档

- [Agnes Video 2.5 Flash 官方文档](https://agnes-ai.cn/zh-Hans/docs/agnes-video-25-flash)
- [Agnes AI 平台](https://platform.agnes-ai.cn)
