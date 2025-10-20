import os
import csv

old_books_path = r"D:\Users\Administrator\Documents\otzaria-library\sefaria and more"
new_books_path = r"C:\Users\Otzaria\Desktop\otzaria\אוצריא"

def get_folder_content(books_path: str) -> tuple[dict[str, str], ...]:
    files_dict = {}
    folders_dict = {}
    for root, folders, files in os.walk(books_path):
        for file in files:
            rel_path = get_rel_path(root, file, books_path)
            files_dict[file] = rel_path
        for folder in folders:
            rel_path = get_rel_path(root, folder, books_path)
            folders_dict[folder] = rel_path
    return files_dict, folders_dict

def get_rel_path(root: str, name: str, books_path: str) -> str:
    path = os.path.join(root, name)
    rel_path = os.path.relpath(path, books_path)
    return rel_path

new_books_files, _ = get_folder_content(new_books_path)
old_books_files, _ = get_folder_content(old_books_path)
not_in_old = {}
not_in_new = {}
new_books_files_copy = new_books_files.copy()
for file_name, rel_path in new_books_files_copy.items():
    if os.path.exists(os.path.join(old_books_path, rel_path)):
        continue
    in_old = old_books_files.get(file_name)
    if in_old:
        target_path = os.path.join(new_books_path, in_old)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        os.rename(os.path.join(new_books_path, rel_path), target_path)
        new_books_files[file_name] = in_old
        continue
    not_in_old[file_name] = rel_path
for file_name, rel_path in old_books_files.items():
    if new_books_files.get(file_name):
        continue
    not_in_new[file_name] = rel_path

for root, folders, _ in os.walk(new_books_path, topdown=False):
    for folder in folders:
        folder_path = os.path.join(root, folder)
        if not os.listdir(folder_path):
            os.rmdir(folder_path)

with open("not_in_new.csv", "w", encoding="windows-1255", newline="") as f:
    writer = csv.writer(f)
    for key, value in not_in_new.items():
        writer.writerow([key, value])


with open("not_in_old.csv", "w", encoding="windows-1255", newline="") as f:
    writer = csv.writer(f)
    for key, value in not_in_old.items():
        writer.writerow([key, value])

