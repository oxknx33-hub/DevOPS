import os
import sys
import json
from collections import defaultdict
from pathlib import Path

def analyze_folder(path):
    """
    Анализирует содержимое папки: количество файлов, расширения, размеры.
    """
    if not os.path.exists(path):
        print(f"Ошибка: Путь '{path}' не существует.")
        return None

    stats = {
        "target_path": os.path.abspath(path),
        "total_files": 0,
        "total_size_bytes": 0,
        "extensions": defaultdict(int),
        "files_detail": []
    }

    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    stats["total_files"] += 1
                    stats["total_size_bytes"] += file_size
                    stats["extensions"][file_ext if file_ext else "без расширения"] += 1
                    
                    stats["files_detail"].append({
                        "name": file,
                        "path": os.path.relpath(file_path, path),
                        "size": file_size,
                        "extension": file_ext if file_ext else "без расширения"
                    })
                except PermissionError:
                    continue
    except Exception as e:
        print(f"Произошла ошибка при сканировании: {e}")
        return None

    # Преобразуем defaultdict в dict для JSON сериализации
    stats["extensions"] = dict(stats["extensions"])
    return stats

def save_report(stats, output_file="report.json"):
    """
    Сохраняет статистику в JSON файл.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
        print(f"Отчет успешно сохранен в {output_file}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении отчета: {e}")
        return False

if __name__ == "__main__":
    # Проверка аргументов командной строки
    if len(sys.argv) < 2:
        print("Использование: python folder_analyzer.py <путь_к_папке>")
        print("Пример: python folder_analyzer.py .")
        sys.exit(1)

    target_path = sys.argv[1]
    
    print(f"Начало анализа папки: {target_path}...")
    result = analyze_folder(target_path)
    
    if result:
        save_report(result)
        print(f"\nИтого файлов: {result['total_files']}")
        print(f"Общий размер: {result['total_size_bytes']} байт")
        print("Расширения:", result['extensions'])
    else:
        sys.exit(1)
