import os
import sys
import json
from collections import defaultdict

def analyze_folder(path):
    if not os.path.exists(path):
        print(f"Error: Path '{path}' not found.")
        return None

    stats = {
        "target_path": os.path.abspath(path),
        "total_files": 0,
        "total_size_bytes": 0,
        "extensions": {},
        "files_detail": []
    }

    ext_counter = defaultdict(int)

    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(full_path)
                    _, ext = os.path.splitext(file)
                    ext = ext.lower() if ext else "no_extension"
                    
                    stats["total_files"] += 1
                    stats["total_size_bytes"] += size
                    ext_counter[ext] += 1
                    
                    rel_path = os.path.relpath(full_path, path)
                    stats["files_detail"].append({
                        "name": file,
                        "relative_path": rel_path,
                        "size_bytes": size,
                        "extension": ext
                    })
                except PermissionError:
                    continue
                except Exception:
                    continue
        
        stats["extensions"] = dict(ext_counter)
        return stats

    except Exception as e:
        print(f"Critical Error: {e}")
        return None

def save_report(stats, filename="report.json"):
    if not stats:
        return False
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
        print(f"Report saved to {filename}")
        return True
    except Exception as e:
        print(f"Save Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python folder_analyzer.py <path>")
        print("Example: python folder_analyzer.py .")
        sys.exit(1)

    target_path = sys.argv[1]
    result = analyze_folder(target_path)
    
    if result:
        save_report(result)
        print(f"Total files: {result['total_files']}")
        print(f"Total size: {result['total_size_bytes']} bytes")
    else:
        sys.exit(1)
