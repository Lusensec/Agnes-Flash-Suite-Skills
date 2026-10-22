# Agnes Image 2.5 Flash Skill

这是一个用于生成图像的 AI 模型 Skill，基于 Agnes AI 的 Image 2.5 Flash 模型。

## 功能特性

- 文生图
- 图生图（图像编辑/风格迁移）
- 多图合成
- 多种尺寸档位（1K/2K/3K/4K）
- 多种宽高比（1:1/3:4/4:3/16:9/9:16/2:3/3:2/21:9）
- URL 或 Base64 输出

## 快速开始

### 1. 配置 API Key

复制 `.env.example` 为 `.env`（放在本 skill 根目录），填入 API Key：

```
AGNESAI_BASE_URL=https://api.agnes-ai.cn
AGNESAI_API_KEY=sk-你的实际API Key
```

> 脚本会自动从 `.env` 加载，无需手动 export。获取 API Key：https://platform.agnes-ai.cn
> `AGNESAI_BASE_URL` 可选：默认官方端点，走自建/代理网关时修改（不含 `/v1` 路径）。

### 2. 文生图

```bash
# 参数：[提示词] [尺寸] [比例]，均可选（不传使用默认演示内容）
python examples/text-to-image.py "一只可爱的田园犬在稻田边" "2K" "16:9"
```

### 3. 图生图

```bash
# 参数：[输入图片URL] [提示词]，均可选
python examples/image-to-image.py https://example.com/input.png "转换为赛博朋克风格"
```

### 4. 多图合成

```bash
# 参数：[图片1URL] [图片2URL] [提示词]，均可选
python examples/multi-image-combine.py https://example.com/a.png https://example.com/b.png "将两张图合成"
```

### 5. 文生图（Base64 输出）

```bash
# 参数：[提示词] [尺寸]，均可选
python examples/text-to-image-base64.py "一个玻璃立方体产品照" "1K"
```

## 使用场景

| 场景 | 推荐配置 |
|------|----------|
| 社交媒体封面 | 2K + 16:9 |
| 产品海报 | 2K + 3:4 或 4:3 |
| 手机壁纸 | 2K + 9:16 |
| 横版视频缩略图 | 2K + 16:9 |
| 方形头像 | 1K + 1:1 |

## 价格

- 当前限时免费
- 原价：¥0.07-0.16/张（按尺寸）

## 文件结构

```
agnes-2.5-image-flash/
├── SKILL.md                        # 详细说明文档
├── README.md                       # 本文件
└── examples/
    ├── load_env.py                 # .env 自动加载（自包含）
    ├── text-to-image.py            # 参数：[提示词] [尺寸] [比例]
    ├── text-to-image-base64.py     # 参数：[提示词] [尺寸]
    ├── image-to-image.py           # 参数：[输入图片URL] [提示词]
    └── multi-image-combine.py      # 参数：[图片1URL] [图片2URL] [提示词]
```

## 相关文档

- [Agnes Image 2.5 Flash 官方文档](https://agnes-ai.cn/zh-Hans/docs/agnes-image-25-flash)
