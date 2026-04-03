"""
Americano Universe - Certificate Generator
Generates coffee concentration certificate cards.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple, Optional


def get_system_font(size: int) -> ImageFont.FreeTypeFont:
    """
    Load system font with fallback for cross-platform compatibility.
    
    Priority:
    1. macOS: PingFang (苹方)
    2. Windows: Microsoft YaHei (微软雅黑)
    3. Linux: WenQuanYi (文泉驿)
    4. Default: Load default font
    """
    font_paths = [
        # macOS
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/PingFang SC.ttf',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        # Windows
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/msyhbd.ttc',
        'C:/Windows/Fonts/simhei.ttf',
        # Linux
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    
    # Fallback to default font
    print(f"Warning: No suitable font found, using default font")
    return ImageFont.load_default()


def generate_orthodox_certificate(
    user_photo_path: str,
    coffee_type: str,
    concentration: float,
    story: str,
    output_path: str = 'output.png'
) -> str:
    """
    Generate an orthodox coffee certificate.
    
    Args:
        user_photo_path: Path to user's coffee photo
        coffee_type: Type of coffee (e.g., "冰美式", "Iced Americano")
        concentration: Concentration value (0.000-1.000)
        story: The digital story for this concentration
        output_path: Where to save the generated image
    
    Returns:
        Path to the generated certificate image
    """
    # Canvas setup
    width, height = 1080, 1500
    card = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(card)
    
    # Load fonts (scaled 30% larger)
    font_title = get_system_font(62)
    font_type = get_system_font(42)
    font_info = get_system_font(34)
    font_number = get_system_font(130)
    font_strength = get_system_font(47)
    font_fact = get_system_font(31)
    font_org = get_system_font(23)
    
    # Colors: Black + Coffee Brown
    black = '#000000'
    coffee_brown = '#3D2314'
    medium_gray = '#444444'
    light_gray = '#666666'
    border_color = '#CCCCCC'
    
    # Draw border
    margin = 60
    draw.rectangle([margin, margin, width-margin, height-margin], 
                   outline=border_color, width=2)
    
    # 1. Title
    title = "今日美式鉴定卡"  # Can be translated based on language
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 70), title, 
              font=font_title, fill=black)
    
    # 2. User photo
    try:
        user_img = Image.open(user_photo_path)
        min_size = min(user_img.size)
        left = (user_img.width - min_size) // 2
        top = (user_img.height - min_size) // 2
        right = left + min_size
        bottom = top + min_size
        user_img = user_img.crop((left, top, right, bottom))
        
        img_size = 550
        user_img = user_img.resize((img_size, img_size), Image.Resampling.LANCZOS)
        
        # Rounded corners mask
        mask = Image.new('L', (img_size, img_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, img_size, img_size], 
                                    radius=25, fill=255)
        user_img.putalpha(mask)
        
        img_x = (width - img_size) // 2
        img_y = 160
        card.paste(user_img, (img_x, img_y), user_img)
    except Exception as e:
        print(f"Error loading user photo: {e}")
        # Draw placeholder
        img_size = 550
        img_x = (width - img_size) // 2
        img_y = 160
        draw.rectangle([img_x, img_y, img_x + img_size, img_y + img_size],
                       fill='#F0F0F0', outline='#DDDDDD', width=1)
    
    # 3. Coffee type (bold)
    coffee_type_text = f"这是一杯{coffee_type}"
    bbox = draw.textbbox((0, 0), coffee_type_text, font=font_type)
    type_width = bbox[2] - bbox[0]
    draw.text(((width - type_width) // 2, img_y + img_size + 50), 
              coffee_type_text, font=font_type, fill=black)
    
    # 4. Concentration info
    info_text = "根据美式咖啡宇宙传回的信息，这杯咖啡的浓度为"
    bbox = draw.textbbox((0, 0), info_text, font=font_info)
    info_width = bbox[2] - bbox[0]
    draw.text(((width - info_width) // 2, img_y + img_size + 120), 
              info_text, font=font_info, fill=medium_gray)
    
    # Concentration number (bold + largest)
    concentration_str = f"{concentration:.3f}"
    bbox = draw.textbbox((0, 0), concentration_str, font=font_number)
    num_width = bbox[2] - bbox[0]
    draw.text(((width - num_width) // 2, img_y + img_size + 170), 
              concentration_str, font=font_number, fill=coffee_brown)
    
    # Strength level (bold)
    if concentration < 0.25:
        strength = "Lite"
    elif concentration < 0.5:
        strength = "Regular"
    else:
        strength = "Strong"
    
    strength_text = f"信息强度为 {strength}"
    bbox = draw.textbbox((0, 0), strength_text, font=font_strength)
    strength_width = bbox[2] - bbox[0]
    draw.text(((width - strength_width) // 2, img_y + img_size + 320), 
              strength_text, font=font_strength, fill=black)
    
    # Separator line
    line_y = img_y + img_size + 400
    draw.line([(width//2 - 200, line_y), (width//2 + 200, line_y)], 
              fill=border_color, width=1)
    
    # 5. Digital story
    fact_intro = f"根据美式咖啡宇宙定律，{concentration:.3f}代表了以下意义："
    bbox = draw.textbbox((0, 0), fact_intro, font=font_fact)
    intro_width = bbox[2] - bbox[0]
    draw.text(((width - intro_width) // 2, line_y + 40), 
              fact_intro, font=font_fact, fill=medium_gray)
    
    # Story content (handle multiline)
    fact_lines = story.split('\n') if '\n' in story else [story[i:i+20] for i in range(0, len(story), 20)]
    fact_y = line_y + 85
    for i, line in enumerate(fact_lines[:3]):  # Max 3 lines
        bbox = draw.textbbox((0, 0), line, font=font_fact)
        line_width = bbox[2] - bbox[0]
        draw.text(((width - line_width) // 2, fact_y + i * 48), 
                  line, font=font_fact, fill=medium_gray)
    
    # 6. Footer
    org_y = height - 120
    org_text = '鉴定组织："人为什么要喝美式咖啡"'
    bbox = draw.textbbox((0, 0), org_text, font=font_org)
    org_width = bbox[2] - bbox[0]
    draw.text(((width - org_width) // 2, org_y), 
              org_text, font=font_org, fill=light_gray)
    
    github_text = "github.com/fluxreborn/americano-universe"
    bbox = draw.textbbox((0, 0), github_text, font=font_org)
    github_width = bbox[2] - bbox[0]
    draw.text(((width - github_width) // 2, org_y + 32), 
              github_text, font=font_org, fill=light_gray)
    
    # Save
    card.save(output_path, 'PNG')
    return output_path


def generate_heretic_certificate(
    user_photo_path: str,
    coffee_type: str,
    output_path: str = 'output_heretic.png'
) -> str:
    """
    Generate a heretic coffee certificate (for coffee with milk/sugar).
    
    Args:
        user_photo_path: Path to user's coffee photo
        coffee_type: Type of coffee (e.g., "冰拿铁", "Latte")
        output_path: Where to save the generated image
    
    Returns:
        Path to the generated certificate image
    """
    # Canvas setup
    width, height = 1080, 1500
    card = Image.new('RGB', (width, height), '#FFFFFF')
    draw = ImageDraw.Draw(card)
    
    # Load fonts
    font_title = get_system_font(62)
    font_type = get_system_font(47)
    font_info = get_system_font(34)
    font_heretic = get_system_font(130)
    font_org = get_system_font(23)
    
    # Colors: Black + Red
    black = '#000000'
    heretic_red = '#CC0000'
    medium_gray = '#444444'
    light_gray = '#666666'
    border_color = '#CCCCCC'
    
    # Draw border
    margin = 60
    draw.rectangle([margin, margin, width-margin, height-margin], 
                   outline=border_color, width=2)
    
    # 1. Title
    title = "今日美式鉴定卡"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 70), title, font=font_title, fill=black)
    
    # Warning label (red)
    warning = "⚠️ 异端警告"
    bbox = draw.textbbox((0, 0), warning, font=font_info)
    warning_width = bbox[2] - bbox[0]
    draw.text(((width - warning_width) // 2, 145), warning, 
              font=font_info, fill=heretic_red)
    
    # 2. User photo
    try:
        user_img = Image.open(user_photo_path)
        min_size = min(user_img.size)
        left = (user_img.width - min_size) // 2
        top = (user_img.height - min_size) // 2
        right = left + min_size
        bottom = top + min_size
        user_img = user_img.crop((left, top, right, bottom))
        
        img_size = 550
        user_img = user_img.resize((img_size, img_size), Image.Resampling.LANCZOS)
        
        mask = Image.new('L', (img_size, img_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, img_size, img_size], 
                                    radius=25, fill=255)
        user_img.putalpha(mask)
        
        img_x = (width - img_size) // 2
        img_y = 215
        card.paste(user_img, (img_x, img_y), user_img)
    except Exception as e:
        print(f"Error loading user photo: {e}")
        img_size = 550
        img_x = (width - img_size) // 2
        img_y = 215
        draw.rectangle([img_x, img_y, img_x + img_size, img_y + img_size],
                       fill='#F0F0F0', outline='#DDDDDD', width=1)
    
    # 3. Coffee type (bold)
    coffee_type_text = f"这是一杯{coffee_type}"
    bbox = draw.textbbox((0, 0), coffee_type_text, font=font_type)
    type_width = bbox[2] - bbox[0]
    draw.text(((width - type_width) // 2, img_y + img_size + 55), 
              coffee_type_text, font=font_type, fill=black)
    
    # 4. Heretic verdict
    info_text = "美式咖啡宇宙返回了无效值，这杯咖啡是："
    bbox = draw.textbbox((0, 0), info_text, font=font_info)
    info_width = bbox[2] - bbox[0]
    draw.text(((width - info_width) // 2, img_y + img_size + 125), 
              info_text, font=font_info, fill=medium_gray)
    
    # Heretic label (bold + red)
    heretic_text = "异端"
    bbox = draw.textbbox((0, 0), heretic_text, font=font_heretic)
    heretic_width = bbox[2] - bbox[0]
    draw.text(((width - heretic_width) // 2, img_y + img_size + 175), 
              heretic_text, font=font_heretic, fill=heretic_red)
    
    # Strength level (bold + red)
    strength_text = "信息强度为：NONSENSE"
    bbox = draw.textbbox((0, 0), strength_text, font=font_type)
    strength_width = bbox[2] - bbox[0]
    draw.text(((width - strength_width) // 2, img_y + img_size + 330), 
              strength_text, font=font_type, fill=heretic_red)
    
    # Separator line
    line_y = img_y + img_size + 410
    draw.line([(width//2 - 200, line_y), (width//2 + 200, line_y)], 
              fill=border_color, width=1)
    
    # 5. Heretic law
    fact_line1 = "根据美式咖啡宇宙定律，加了奶的咖啡"
    bbox = draw.textbbox((0, 0), fact_line1, font=font_info)
    fact_width = bbox[2] - bbox[0]
    draw.text(((width - fact_width) // 2, line_y + 45), 
              fact_line1, font=font_info, fill=medium_gray)
    
    # WEAK warning (red)
    weak_text = "代表了身体和心灵的WEAK。"
    bbox = draw.textbbox((0, 0), weak_text, font=font_info)
    weak_width = bbox[2] - bbox[0]
    draw.text(((width - weak_width) // 2, line_y + 90), 
              weak_text, font=font_info, fill=heretic_red)
    
    # 6. Footer
    org_y = height - 120
    org_text = '鉴定组织："人为什么要喝美式咖啡"'
    bbox = draw.textbbox((0, 0), org_text, font=font_org)
    org_width = bbox[2] - bbox[0]
    draw.text(((width - org_width) // 2, org_y), 
              org_text, font=font_org, fill=light_gray)
    
    github_text = "github.com/fluxreborn/americano-universe"
    bbox = draw.textbbox((0, 0), github_text, font=font_org)
    github_width = bbox[2] - bbox[0]
    draw.text(((width - github_width) // 2, org_y + 32), 
              github_text, font=font_org, fill=light_gray)
    
    # Save
    card.save(output_path, 'PNG')
    return output_path


# Example usage
if __name__ == "__main__":
    # Example: Orthodox coffee
    result = generate_orthodox_certificate(
        user_photo_path="examples/coffee.jpg",
        coffee_type="冰美式",
        concentration=0.288,
        story="2.88秒是F1赛车0-100km/h加速时间。\n第一口下去，2.88秒内从"慵懒模式"\n切换到"赛道模式"。",
        output_path="output_orthodox.png"
    )
    print(f"Generated: {result}")
    
    # Example: Heretic coffee
    result = generate_heretic_certificate(
        user_photo_path="examples/latte.jpg",
        coffee_type="冰拿铁",
        output_path="output_heretic.png"
    )
    print(f"Generated: {result}")
