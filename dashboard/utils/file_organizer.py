import os
import shutil

CATEGORIES = {
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css", ".php"],
    "Others": []
}

def get_category(extension):
    for category, exts in CATEGORIES.items():
        if extension.lower() in exts:
            return category
    return "Others"

def organize_file(file_path, base_dir):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1]
    category = get_category(ext)
    dest_dir = os.path.join(os.path.dirname(file_path), category)

    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, os.path.basename(file_path))

    shutil.move(file_path, dest_path)
    return dest_path
