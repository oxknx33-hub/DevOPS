import os
import sys
import json

# 1. Получаем путь из аргументов
if len(sys.argv) < 2:
    print("ОШИБКА: Вы не указали папку!")
    print("Правильно: python folder_analyzer.py .")
    sys.exit(1)

target_path = sys.argv[1]
print(f"Анализирую папку: {target_path}")

# 2. Проверка существования
if not os.path.exists(target_path):
    print(f"ОШИБКА: Папка '{target_path}' не найдена.")
    sys.exit(1)

# 3. Сбор статистики
files_count = 0
total_size = 0
extensions = {}
file_list = []

# Проходим по всем файлам
for root, dirs, files in os.walk(target_path):
    for name in files:
        full_path = os.path.join(root, name)
        
        # Игнорируем сам отчет, если он уже есть в этой папке, чтобы не зациклиться (опционально)
        if name == "report.json" and root == target_path:
            continue
            
        try:
            size = os.path.getsize(full_path)
            ext = os.path.splitext(name)[1].lower()
            if not ext:
                ext = "no_ext"
            
            files_count += 1
            total_size += size
            
            if ext in extensions:
                extensions[ext] += 1
            else:
                extensions[ext] = 1
            
            file_list.append({
                "name": name,
                "size": size,
                "ext": ext
            })
        except Exception as e:
            print(f"Пропущен файл {name}: {e}")

# 4. Формирование отчета
report = {
    "path": os.path.abspath(target_path),
    "total_files": files_count,
    "total_size_bytes": total_size,
    "extensions": extensions,
    "files": file_list
}

# 5. Запись в JSON
output_file = "report.json"
try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    print(f"ГОТОВО! Отчет сохранен в {output_file}")
    print(f"Найдено файлов: {files_count}")
    print(f"Размер: {total_size} байт")
except Exception as e:
    print(f"КРИТИЧЕСКАЯ ОШИБКА записи файла: {e}")
    sys.exit(1)
