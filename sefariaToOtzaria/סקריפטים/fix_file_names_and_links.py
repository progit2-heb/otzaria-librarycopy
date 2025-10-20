import os
import json

old_books_folder_path = r"C:\Users\Otzaria\Desktop\otzaria"
links_folder_path = r"C:\Users\Otzaria\Desktop\otzaria\links"

for root, folders, files in os.walk(old_books_folder_path, topdown=False):
    for file in files:
        if "״" in file or "''" in file:
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(root, file.replace("״", "").replace("''", ""))
            os.rename(file_path, new_file_path)
    for folder in folders:
        if "״" in folder or "''" in folder:
            folder_path = os.path.join(root, folder)
            new_folder_path = os.path.join(root, folder.replace("״", "").replace("''", ""))
            os.rename(folder_path, new_folder_path)
for link_file in os.listdir(links_folder_path):
    file_path = os.path.join(links_folder_path, link_file)
    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    for index, entry in enumerate(content):
        path_2 = entry["path_2"]
        if "״" in folder or "''" in folder:
            content[index]["path_2"] = path_2.replace("״", "").replace("''", "")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
        