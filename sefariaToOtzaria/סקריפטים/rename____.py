import json
from pathlib import Path
import csv

csv_file_path = r"C:\Users\Otzaria\Desktop\שמות לשינוי.csv"
books_file_path = r"C:\Users\Otzaria\Desktop\otzaria\אוצריא"
links_file_path = r"C:\Users\Otzaria\Desktop\otzaria\links"

csv_file_path = Path(csv_file_path)
links_file_path = Path(links_file_path)
books_file_path = Path(books_file_path)
files_dif = {}
with csv_file_path.open("r", encoding="windows-1255") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        files_dif[row[0]] = row[1]
for file in links_file_path.iterdir():
    if file.name in files_dif:
        file_path = links_file_path / file
        new_path = links_file_path / files_dif[file.name]
        file = file.rename(new_path)
    with file.open("r", encoding="utf-8") as f:
        content = json.load(f)
        content_copy = content.copy()
        for index, entry in enumerate(content_copy):
            if entry["path_2"] in files_dif:
                content[index]["path_2"] = files_dif[entry["path_2"]]
    with file.open("w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
for root, folders, files in books_file_path.walk():
    for file in files:
        if file in files_dif:
            file_path = root / file
            new_path = root / files_dif[file]
            file_path.rename(new_path)




