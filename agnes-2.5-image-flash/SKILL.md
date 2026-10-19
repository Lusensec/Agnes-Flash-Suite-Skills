---
name: agnes-2.5-image-flash
description: |
  Agnes Image 2.5 Flash 图像生成 Skill（模型 ID: agnes-image-2.5-flash）。
  支持文生图、图生图和多图合成工作流，整体能力全面超过旧版本。
  官方文档：https://agnes-ai.cn/zh-Hans/docs/agnes-image-25-flash
  触发词：生图、图像生成、文生图、图生图、图片生成、image generation
---

# Agnes Image 2.5 Flash 图像生成 Skill

## 概述

Agnes Image 2.5 Flash 是 Agnes AI 最新一代图像模型，整体能力全面超过旧版本。支持文生图、图生图和多图合成工作流，特别适合高信息密度图像、复杂视觉细节和语义对齐。

**核心优化：**
- 高信息密度图像生成
- 复杂视觉细节呈现
- 语义对齐增强
- 构图保留（图生图编辑时保留原始布局）

## API 信息

- **端点**: `POST https://api.agnes-ai.cn/v1/images/generations`
- **模型 ID**: `agnes-image-2.5-flash`
- **响应格式**: URL 或 Base64

## 支持的参数

### 基础参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 模型名称，使用 `agnes-image-2.5-flash` |
| `prompt` | string | ✅ | 图像生成或编辑的文本指令 |
| `size` | string | ✅ | 输出尺寸档位：`1K` / `2K` / `3K` / `4K` |
| `ratio` | string | ❌ | 宽高比，默认 `1:1` |
| `return_base64` | boolean | ❌ | 文生图 Base64 输出时使用 |
| `extra_body` | object | ❌ | 高级工作流的附加参数 |
| `extra_body.response_format` | string | ❌ | 输出格式：`url` 或 `b64_json` |
| `extra_body.image` | string[] | 图生图/多图合成必填 | 输入图像数组（最多 6 张，超出返回 400 `too many input images`；支持公开 URL 或 Base64 Data URI） |

### 宽高比 (ratio)

| 值 | 说明 |
|----|------|
| `1:1` | 正方形（默认） |
| `3:4` | 竖向 3:4 |
| `4:3` | 横向 4:3 |
| `16:9` | 宽屏 16:9 |
| `9:16` | 手机竖屏 9:16 |
| `2:3` | 竖向 2:3 |
| `3:2` | 横向 3:2 |
| `21:9` | 超宽屏 21:9 |

### 输出尺寸参考

| Ratio | 1K | 2K | 3K | 4K |
|-------|-----|-----|-----|-----|
| `1:1` | 1024×1024 | 2048×2048 | 3072×3072 | 4096×4096 |
| `3:4` | 864×1152 | 1728×2304 | 2592×3456 | 3456×4608 |
| `4:3` | 1152×864 | 2304×1728 | 3456×2592 | 4608×3456 |
| `16:9` | 1312×736 | 2624×1472 | 3936×2208 | 5248×2944 |
| `9:16` | 736×1312 | 1472×2624 | 2208×3936 | 2944×5248 |
| `2:3` | 832×1248 | 1664×2496 | 2496×3744 | 3328×4992 |
| `3:2` | 1248×832 | 2496×1664 | 3744×2496 | 4992×3328 |
| `21:9` | 1568×672 | 3136×1344 | 4704×2016 | 6272×2688 |

## 核心能力

### 1. 文生图

```python
# 运行 python examples/text-to-image.py [提示词] [尺寸] [比例]（参数可选）
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/images/generations",
    data=json.dumps({
        "model": "agnes-image-2.5-flash",
        "prompt": "A luminous floating city above a misty canyon at sunrise, cinematic realism",
        "size": "2K",
        "ratio": "16:9",
        "extra_body": {"response_format": "url"}
    }).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST"
)).read()
print(json.loads(resp)["data"][0]["url"])
```

### 2. 图生图

```python
# 运行 python examples/image-to-image.py [输入图片URL] [提示词]（参数可选）
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/images/generations",
    data=json.dumps({
        "model": "agnes-image-2.5-flash",
        "prompt": "Transform the scene into a rain-soaked cyberpunk night with neon reflections while preserving the original composition",
        "size": "2K",
        "ratio": "16:9",
        "extra_body": {
            "image": ["https://example.com/input-image.png"],
            "response_format": "url"
        }
    }).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST"
)).read()
print(json.loads(resp)["data"][0]["url"])
```

### 3. 多图合成

> `extra_body.image` **最多 6 张**（官方 400 校验：`too many input images: N provided, at most 6 allowed`；10/19 双网关实测）。更多图片请分批合成接力。

```python
# 运行 python examples/multi-image-combine.py [图片1URL] [图片2URL] [提示词]（参数可选）
import json, urllib.request, os
API_KEY = os.environ.get("AGNESAI_API_KEY")
resp = urllib.request.urlopen(urllib.request.Request(
    "https://api.agnes-ai.cn/v1/images/generations",
    data=json.dumps({
        "model": "agnes-image-2.5-flash",
        "prompt": "Combine the two characters into an intense fantasy battle scene, dynamic lighting, detailed background, cinematic composition",
        "size": "2K",
        "ratio": "1:1",
        "extra_body": {
            "image": [
                "https://example.com/character-1.png",
                "https://example.com/character-2.png"
            ],
            "response_format": "url"
        }
    }).encode(),
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    method="POST"
)).read()
print(json.loads(resp)["data"][0]["url"])
```

## 响应格式

### URL 输出

```json
{
  "created": 1780000000,
  "data": [
    {
      "url": "https://storage.googleapis.com/agnes-aigc/xxx.png",
      "b64_json": null,
      "revised_prompt": null
    }
  ]
}
```

### Base64 输出

```json
{
  "created": 1780000000,
  "data": [
    {
      "url": null,
      "b64_json": "iVBORw0KGgoAAAANSUhEUgAA...",
      "revised_prompt": null
    }
  ]
}
```

## 推荐提示词结构

### 文生图

```
[主体] + [场景/环境] + [风格] + [光照] + [构图] + [质量要求]
```

**示例：**
```
日出时分薄雾峡谷上方的发光浮空城市，电影级写实风格，广角构图，丰富的建筑细节，柔和的金色光线，高视觉密度
```

### 图生图

```
[改变要求] + [新风格/场景] + [需要添加或移除的元素] + [需要保留的元素]
```

**示例：**
```
将白天街道场景改为电影级赛博朋克夜景，添加霓虹招牌和湿滑路面倒影，同时保留原始街道布局、相机角度和主要建筑形状
```

### 多图合成

```
[参考图角色] + [目标场景] + [图像之间的关系] + [风格/光照/构图]
```

**示例：**
```
将第一张图作为主要角色，第二张图作为产品参考，生成一张电影级活动海报，保留角色身份和产品外形，使用自然光照和干净的商业构图
```

### 高信息密度图像

```
清晰描述视觉层次结构：主要主体 + 背景环境 + 重要次要细节 + 风格 + 光照 + 构图约束
```

**示例：**
```
建在悬崖上的大型奇幻港口城市，数百艘小船，层叠的石桥，发光的窗户，远山，多云的日落天空，电影级奇幻写实风格，广角构图，丰富的建筑细节，高视觉密度
```

## 重要注意事项

⚠️ **请勿在请求体顶层放置 `response_format`**

```bash
# ❌ 错误写法
{
  "model": "agnes-image-2.5-flash",
  "prompt": "...",
  "size": "2K",
  "response_format": "url"  # 错误！
}

# ✅ 正确写法
{
  "model": "agnes-image-2.5-flash",
  "prompt": "...",
  "size": "2K",
  "extra_body": {
    "response_format": "url"  # 正确！
  }
}
```

⚠️ **图生图不需要传递 `tags: ["img2img"]`**

只需在 `extra_body.image` 中提供输入图像即可。

## 常见错误与故障排除

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 顶层放置 response_format | 参数位置错误 | 移到 `extra_body` 中 |
| 图生图传递 tags | 多余参数 | 删除 `tags` 字段 |
| 输入图像 URL 无法访问 | 网络问题 | 使用公共 HTTPS URL 或 Data URI Base64 |
| 请求超时 | 生成时间过长 | 增加超时时间至 60-360s |
| 图生图缺少 image 参数 | 必填参数缺失 | 在 `extra_body.image` 中提供输入图像 |

## 计费说明

| 计费项 | 刊例价（原价） | 现价（优惠价） |
|--------|--------------|---------------|
| 1K 输出图片 | ¥0.07/张 | **¥0** |
| 2K 输出图片 | ¥0.12/张 | **¥0** |
| 3K 输出图片 | ¥0.14/张 | **¥0** |
| 4K 输出图片 | ¥0.16/张 | **¥0** |
| 第 4 张起的输入参考图片 | ¥0.02/张 | **¥0/张** |

**当前优惠：所有输出分辨率档位和输入参考图片均免费！**

## 适用场景

| 场景 | 说明 |
|------|------|
| **创意设计** | 概念艺术、视觉探索和海报草稿 |
| **营销内容** | 活动图片、产品视觉和社交媒体创意 |
| **高密度视觉** | 精细场景、复杂环境和丰富构图 |
| **图像转换** | 风格迁移、场景重打光和背景变换 |
| **产品可视化** | 产品照片、模型图和商业视觉 |
| **社交媒体素材** | 封面、横幅、缩略图和帖子图片 |

## 接入检查清单

- [ ] 使用 `agnes-image-2.5-flash` 作为模型名称
- [ ] 使用 `https://api.agnes-ai.cn/v1/images/generations` 作为 API 端点
- [ ] 文生图请求包含 `model`、`prompt` 和 `size`
- [ ] 使用 `1K`/`2K`/`3K`/`4K` 等档位式 `size`，并配合 `ratio`
- [ ] 图生图和多图合成在 `extra_body.image` 中提供输入图像
- [ ] 将 `response_format` 放在 `extra_body` 中，而非顶层
- [ ] 不传递 `tags: ["img2img"]`

## 相关文档

- [Agnes Image 2.5 Flash 官方文档](https://agnes-ai.cn/zh-Hans/docs/agnes-image-25-flash)
- [Agnes AI 平台](https://platform.agnes-ai.cn)
