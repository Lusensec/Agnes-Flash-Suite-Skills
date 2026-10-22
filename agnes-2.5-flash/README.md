# Agnes 2.5 Flash Skill

这是一个用于对话和推理的 AI 模型技能，基于 Agnes AI 的 2.5 Flash 语言模型。

## 功能特性

- 聊天补全
- 多轮对话（512K 上下文）
- 图像理解（Vision）
- 工具调用（Function Calling）
- Thinking 模式
- 流式输出
- 代码专项任务优化

## 快速开始

### 1. 配置 API Key

复制 `.env.example` 为 `.env`（放在本 skill 根目录），填入 API Key：

```
AGNESAI_BASE_URL=https://api.agnes-ai.cn
AGNESAI_API_KEY=sk-你的实际API Key
```

> 脚本会自动从 `.env` 加载，无需手动 export。获取 API Key：https://platform.agnes-ai.cn
> `AGNESAI_BASE_URL` 可选：默认官方端点，走自建/代理网关时修改（不含 `/v1` 路径）。

### 2. 基础聊天

```bash
# 不传参数使用默认示例，传参数则使用你的问题
python examples/basic-chat.py "用 Python 写一个快速排序算法"
```

### 3. 图像理解

```bash
python examples/image-understanding.py https://example.com/image.jpg
```

### 4. 工具调用

```bash
python examples/tool-calling.py "查询新加坡今天的天气"
```

### 5. Thinking 模式

```bash
# 参数：[问题] [思考等级] [max_tokens]，均可选
# - 思考等级：不传则不设置（默认）；可选等级：none/low/medium/high/max
# - max_tokens：不传或传 0 则不设置；正整数限制输出预算
python examples/thinking-mode.py "帮我写一个 Python 脚本处理 CSV 文件"
python examples/thinking-mode.py "复杂多步推理任务" "high"
python examples/thinking-mode.py "复杂多步推理任务" "high" "8192"
```

> 思考等级通过顶层 `reasoning_effort` 参数控制。2.5 支持 `none/low/medium/high/max` 5 档，
> 不支持 `minimal` 和 `xhigh`（传入返回 400）。任务越复杂可越高设置等级。
> `max_tokens` 默认不设置（省略或传 0）；思考链与回答共用输出预算，复杂推理任务建议调高（如 8192）避免截断。

> 所有参数均可选：不传参数时使用默认演示内容，传参数时动态替换。

## 使用场景

| 场景 | 说明 |
|------|------|
| **AI 助手** | 通用问答、效率助手、个人助理 |
| **自主智能体** | 多步骤任务执行、规划、工具使用 |
| **编码助手** | 代码生成、Bug 排查、重构建议 |
| **图像理解** | 截图分析、图片描述、视觉问答 |
| **客户支持** | FAQ 自动回复、客服机器人 |

## 价格

- 当前限时免费
- 原价：输入 ¥0.20/百万 Token，输出 ¥1.00/百万 Token

## 文件结构

```
agnes-2.5-flash/
├── SKILL.md                        # 详细说明文档
├── README.md                       # 本文件
└── examples/
    ├── load_env.py                 # .env 自动加载（自包含）
    ├── basic-chat.py               # 参数：[用户问题]
    ├── image-understanding.py      # 参数：[图片URL]
    ├── tool-calling.py             # 参数：[用户问题]
    └── thinking-mode.py            # 参数：[问题] [思考等级] [max_tokens]
```

## 文档

详见 [SKILL.md](./SKILL.md)
