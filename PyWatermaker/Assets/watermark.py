import math
from PIL import Image, ImageDraw, ImageFont

def apply_text_watermark(img, text, font_path, opacity=0.5):
    """
    6. Image.new('RGBA'): Создание прозрачного слоя.
    7. ImageFont.truetype: Загрузка кастомного шрифта.
    8. ImageDraw.Draw: Утилита рисования.
    """
    # Вычисляем размер шрифта относительно изображения
    # 9. img.size: Доступ к геометрии.
    width, height = img.size
    font_size = int(math.sqrt(width * height) / 20)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Шрифт не найден по пути {font_path}. Используется дефолтный.")
        font = ImageFont.load_default()

    # Слой для текста
    text_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)
    
    # 10. draw.text: Рисование с прозрачностью.
    # Вычисляем координаты (центр)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    x = (width - text_w) // 2
    y = (height - text_h) // 2
    
    fill_color = (255, 255, 255, int(255 * opacity))
    draw.text((x, y), text, font=font, fill=fill_color)
    
    # 11. img.alpha_composite: Наложение слоев.
    # Работает только если оба RGB(A)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
        
    return Image.alpha_composite(img, text_layer)

def apply_logo_watermark(img, logo_path, position='bottom_right', padding=20):
    """
    12. logo.rotate: Поворот логотипа.
    13. img.paste: Наложение по координатам с маской.
    """
    logo = Image.open(logo_path)
    # Гарантируем наличие альфа-канала у лого
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')
        
    # Масштабируем лого под 15% ширины основного фото
    img_w, img_h = img.size
    logo_w_target = int(img_w * 0.15)
    
    # 14. Image.Resampling.LANCZOS: Качественный ресайз.
    logo.thumbnail((logo_w_target, logo_w_target), Image.Resampling.LANCZOS)
    
    # Применяем вращение для стиля
    logo = logo.rotate(15, expand=True, resample=Image.Resampling.BICUBIC)
    logo_w, logo_h = logo.size
    
    # Расчет позиции
    if position == 'bottom_right':
        x = img_w - logo_w - padding
        y = img_h - logo_h - padding
        
    # 15. img.paste(..., mask=...): Наложение с прозрачностью.
    # Лого само выступает маской для себя
    img.paste(logo, (x, y), logo)
    return img
