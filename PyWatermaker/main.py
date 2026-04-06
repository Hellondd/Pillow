import os
import glob
from core.utils import load_and_standardize, extract_exif_json
from core.watermark.py import apply_text_watermark, apply_logo_watermark
from PIL import Image

INPUT_DIR = "input"
OUTPUT_DIR = "output"
ASSETS_DIR = "assets"

def process_pipeline():
    # Настройки
    text = "Property of MyStudio, 2026"
    font_path = os.path.join(ASSETS_DIR, "font.ttf")
    logo_path = os.path.join(ASSETS_DIR, "logo.png")
    
    # Создаем папки, если нет
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(INPUT_DIR, exist_ok=True)

    # Поиск изображений (jpeg, jpg, png)
    images = glob.glob(os.path.join(INPUT_DIR, "*.*"))
    print(f"Найдено {len(images)} изображений.")

    for img_path in images:
        filename = os.path.basename(img_path)
        print(f"Обработка: {filename}...")
        
        try:
            # 1. Загрузка и ресайз
            img = load_and_standardize(img_path)
            
            # 2. Анализ (выводим EXIF в консоль)
            exif_json = extract_exif_json(img)
            if exif_json:
                print(f"  EXIF extracted for {filename}")

            # 3. Наложение текста (центр)
            img = apply_text_watermark(img, text, font_path)
            
            # 4. Наложение лого (угол)
            img = apply_logo_watermark(img, logo_path)
            
            # 5. Сохранение
            # 16. img.convert('RGB'): Перед сохранением в JPEG убираем альфа-канал.
            if img.mode == 'RGBA':
                img = img.convert('RGB')
                
            out_name = f"marked_{os.path.splitext(filename)[0]}.jpg"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            
            # 17. img.save: Сохранение с оптимизацией и прогрессивной загрузкой.
            img.save(out_path, format="JPEG", quality=85, optimize=True, progressive=True)
            
        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")

if __name__ == "__main__":
    process_pipeline()
