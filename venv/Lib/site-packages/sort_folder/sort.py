import sys
from pathlib import Path
import os
import re
import shutil

# Словник категорій файлів та відповідних розширень
CATEGORIES = {"Audio": [".mp3", ".ogg", ".wav", ".amr", ".flac", ".wma"],
              "Documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
              "Images": [".jpeg", ".png", ".jpg", ".svg"],
              "Video": [".avi", ".mp4", ".mov", ".mkv"],
              "Arkhives": [".zip", ".gz", ".tar"]
              }

# Функція для визначення категорії файлу на основі його розширення
def get_categories(file:Path):
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

# Функція для нормалізації імен файлів
def normalize(name, without_extenshion = False):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
        
    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = t
        TRANS[ord(c.upper())] = t.upper()
        
    file_name, file_extension = os.path.splitext(name)
    normalized_name = re.sub(r'[^0-9a-zA-Z]', '_', file_name.translate(TRANS))
    
    if without_extenshion == True:
        return normalized_name
    
    return normalized_name + file_extension

# Функція для переміщення файлу в відповідну категорію та нормалізації імені
def move_file(file:Path, category:str, root_dir:Path) -> None:
    # Розділяємо шлях до файлу на частини (папки)
    path_parts = file.parts
    
    # Перевіряємо, чи "Arkhives" не міститься в шляху
    if "Arkhives" not in path_parts:
        if category == "Arkhives":
            target_dir = root_dir.joinpath(category)
            if not target_dir.exists():
                target_dir.mkdir()
            
            # Створюємо нову папку з назвою архіву (без розширення)    
            new_path_1 = target_dir.joinpath(normalize(file.name, True))
            if not new_path_1.exists():
                new_path_1.mkdir()
                
            # Розархівовуємо архів
            shutil.unpack_archive(file, new_path_1)
            os.remove(file)
        else:
            # Якщо категорія не є "Arkhives"    
            target_dir = root_dir.joinpath(category)
            if not target_dir.exists():
                target_dir.mkdir()
            if category == "Other":
                new_path = target_dir.joinpath(file.name)
                if not new_path.exists():
                    file.replace(new_path)    
            else:   
                new_path = target_dir.joinpath(normalize(file.name))
                if not new_path.exists():
                    file.replace(new_path)
    
def sort_folder_recursive(path: Path) -> None:
    for element in path.iterdir():
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
        elif element.is_dir():
            sort_folder_recursive(element)

def sort_folder(path: Path) -> None:
    sort_folder_recursive(path)
    
    # Перевірка чи пуста папка        
    for element in path.glob("**/*"):    
        if element.is_dir():
            if not any(element.iterdir()):
                shutil.rmtree(element)
                

def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return "Folder dos not exists"
    
    sort_folder(path)
    
    return "All Ok"

if __name__ == '__main__':
    print(main())