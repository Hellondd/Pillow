import orjson
from PIL import Image, ImageOps, ExifTags

def load_and_standardize(image_path, max_size=(1920, 1080)):
    """
    1. Image.open: Открытие.
    2. ImageOps.exif_transpose: Коррекция ориентации на основе EXIF.
    3. img.thumbnail: Адаптивное изменение размера.
    """
    img = Image.open(image_path)
    img = ImageOps.exif_transpose(img) # Исправляет перевернутые фото
    
    # 4. img.mode: Проверка режима (конвертируем в RGB для JPEG, если надо)
    if img.mode != 'RGB' and img.mode != 'RGBA':
        img = img.convert('RGB')
        
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    return img

def extract_exif_json(img):
    """5. img.getexif: Извлечение EXIF и конвертация в JSON."""
    exif_data = img.getexif()
    if not exif_data:
        return None
    
    # Декодируем теги
    readable_exif = {}
    for tag_id, value in exif_data.items():
        tag_name = ExifTags.TAGS.get(tag_id, tag_id)
        # Обработка байтовых данных для JSON
        if isinstance(value, bytes):
            value = value.hex()
        readable_exif[str(tag_name)] = str(value)
        
    # Сериализация через orjson
    return orjson.dumps(readable_exif, option=orjson.OPT_INDENT_2)
