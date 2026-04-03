<p align="center">
  <img src="examples/orthodox-example.png" width="300" alt="Americano Universe">
</p>

<h1 align="center">☕ Americano Universe</h1>

<p align="center">
  <b>Upload a coffee photo → AI generates a certificate card</b>
</p>

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python: 3.8+">
  <img src="https://img.shields.io/badge/AI-Vision-green.svg" alt="AI: Vision">
</p>

---

<a name="english"></a>
## 🇬🇧 English

### 🎯 What is this?

**Americano Universe** is an AI-powered coffee identification system that generates beautiful certificate cards.

Upload any coffee photo, and the AI will:
1. **Identify** the coffee type (Americano, Espresso, Latte, etc.)
2. **Calculate** the concentration (0.000 - 1.000)
3. **Generate** a certificate card with a unique digital story
4. **Return** the image file (not text!)

### 🎭 Two Paths

| Type | Result | Card Theme |
|------|--------|------------|
| **☕ Orthodox** | Concentration value + Cool story | Black + Coffee Brown |
| **⚠️ Heretic** | "HERETIC" warning | Black + Red |

**Orthodox**: Americano, Espresso, Water  
**Heretic**: Latte, Cappuccino, Flat White, Mocha (anything with milk/sugar)

### 🚀 Quick Start

#### For AI Agents

Copy the content from `src/agent/agent-prompt-v6-image-generation.md` and use it as your system prompt.

**Key requirement**: The agent must support image generation (Pillow, Canvas, or similar).

#### For Developers

```bash
# Clone the repository
git clone https://github.com/fluxreborn/americano-universe.git
cd americano-universe

# Install dependencies
pip install -r requirements.txt

# Generate a certificate
python src/generator/certificate_generator.py
```

### 🎨 Certificate Example

```
┌─────────────────────────────┐
│   ☕ 今日美式鉴定卡          │
│                             │
│    [Coffee Photo]           │
│                             │
│  这是一杯冰美式              │
│                             │
│  浓度: 0.618                │
│  信息强度: Strong           │
│  ─────────────────────      │
│                             │
│  0.618是黄金分割比例。       │
│  这杯咖啡的完美浓度，        │
│  就像古希腊神庙一样和谐。    │
│                             │
│  github.com/fluxreborn/...  │
└─────────────────────────────┘
```

### 📚 Digital Stories

Each concentration has a unique story:

| Concentration | Story |
|---------------|-------|
| 0.000 | 0 is void, also the beginning... |
| 0.288 | 2.88 seconds is F1 racing acceleration... |
| 0.314 | First 3 digits of pi... |
| 0.618 | The golden ratio... |
| 1.000 | Espresso, the ultimate form... |

### 📁 Project Structure

```
americano-universe/
├── src/
│   ├── agent/
│   │   └── agent-prompt-v6-image-generation.md  ⭐ Use this
│   ├── stories/
│   │   └── coffee-stories.json
│   ├── generator/
│   │   └── certificate_generator.py
│   └── utils/
│       └── font_fallback_config.md
├── examples/
│   ├── orthodox-example.png
│   └── heretic-example.png
└── README.md
```

### 📜 License

MIT License - see [LICENSE](LICENSE) file.

---

<a name="中文"></a>
## 🇨🇳 中文

### 🎯 这是什么？

**美式咖啡宇宙**是一个AI咖啡识别系统，能生成精美的鉴定卡图片。

上传任意咖啡照片，AI会：
1. **识别** 咖啡类型（美式、浓缩、拿铁等）
2. **计算** 浓度值（0.000 - 1.000）
3. **生成** 带数字故事的鉴定卡图片
4. **返回** 图片文件（不是文字！）

### 🎭 两条路径

| 类型 | 结果 | 卡片配色 |
|------|------|---------|
| **☕ 纯正** | 浓度值 + 冷知识故事 | 黑 + 咖啡棕 |
| **⚠️ 异端** | "异端"警告 | 黑 + 红色 |

**纯正**: 美式、浓缩、水  
**异端**: 拿铁、卡布奇诺、澳白、摩卡（任何加奶/加糖的）

### 🚀 快速开始

#### AI Agent使用

复制 `src/agent/agent-prompt-v6-image-generation.md` 的内容作为系统提示词。

**关键要求**: Agent必须支持图片生成能力（Pillow、Canvas等）。

#### 开发者使用

```bash
# 克隆仓库
git clone https://github.com/fluxreborn/americano-universe.git
cd americano-universe

# 安装依赖
pip install -r requirements.txt

# 生成鉴定卡
python src/generator/certificate_generator.py
```

### 🎨 鉴定卡示例

```
┌─────────────────────────────┐
│   ☕ 今日美式鉴定卡          │
│                             │
│    [咖啡照片]               │
│                             │
│  这是一杯冰美式              │
│                             │
│  浓度: 0.618                │
│  信息强度: Strong           │
│  ─────────────────────      │
│                             │
│  0.618是黄金分割比例。       │
│  这杯咖啡的完美浓度，        │
│  就像古希腊神庙一样和谐。    │
│                             │
│  github.com/fluxreborn/...  │
└─────────────────────────────┘
```

### 📚 数字故事集

每个浓度值都有独特故事：

| 浓度值 | 故事 |
|--------|------|
| 0.000 | 0是虚无，也是起点... |
| 0.288 | 2.88秒是F1赛车加速时间... |
| 0.314 | 圆周率前三位... |
| 0.618 | 黄金分割比例... |
| 1.000 | 意式浓缩，终极形态... |

### 📁 项目结构

```
americano-universe/
├── src/
│   ├── agent/
│   │   └── agent-prompt-v6-image-generation.md  ⭐ 使用这个
│   ├── stories/
│   │   └── coffee-stories.json
│   ├── generator/
│   │   └── certificate_generator.py
│   └── utils/
│       └── font_fallback_config.md
├── examples/
│   ├── orthodox-example.png
│   └── heretic-example.png
└── README.md
```

### 📜 开源协议

MIT协议 - 详见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  <i>"This is not just coffee. This is a way of life."</i><br>
  <i>"这不只是咖啡。这是一种生活方式。"</i>
</p>

<p align="center">
  ☕ <b>Americano Universe</b> ☕
</p>
