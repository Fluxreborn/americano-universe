# 咖啡浓度鉴定卡 - 字体回退配置

## 多平台字体回退策略

```python
# 字体加载顺序（按优先级）
font_paths = [
    # macOS - 苹方（最优先）
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/PingFang SC.ttf',
    
    # macOS - 备选华文黑体
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    
    # Windows - 微软雅黑（最优先）
    'C:/Windows/Fonts/msyh.ttc',
    'C:/Windows/Fonts/msyhbd.ttc',
    
    # Windows - 备选黑体
    'C:/Windows/Fonts/simhei.ttf',
    'C:/Windows/Fonts/simsun.ttc',
    
    # Linux - 文泉驿
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    
    # Linux - Noto
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
    
    # Android
    '/system/fonts/NotoSansCJK-Regular.ttc',
    '/system/fonts/DroidSansFallback.ttf',
]

def load_font_with_fallback(size):
    """
    加载字体，支持多平台回退
    如果都找不到，返回默认字体
    """
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    
    # 回退到默认字体
    return ImageFont.load_default()
```

## 字体优先级说明

| 优先级 | 系统 | 字体 | 特点 |
|--------|------|------|------|
| 1 | macOS | 苹方 (PingFang) | 系统默认，现代黑体 |
| 2 | Windows | 微软雅黑 (Microsoft YaHei) | 系统默认，清晰易读 |
| 3 | Linux | 文泉驿 (WenQuanYi) | 开源，通用性强 |
| 4 | Linux | Noto Sans CJK | Google开源，全平台 |
| 5 | All | 默认字体 | 最后回退 |

## 注意事项

1. **苹方在Windows上显示**：如果没有苹方，自动回退到微软雅黑
2. **字体大小差异**：不同字体视觉大小略有差异，但都在可接受范围
3. **中文支持**：所有候选字体都支持简体中文

## 最终代码片段

```python
import os
from PIL import ImageFont

def get_system_font(size):
    """获取系统字体，支持多平台回退"""
    font_paths = [
        # macOS
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        # Windows
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simhei.ttf',
        # Linux
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    
    return ImageFont.load_default()

# 使用
font_title = get_system_font(62)
font_type = get_system_font(42)
# ...
```
