import csv
from pathlib import Path

from utils import CONFIG

old_books_path = Path(CONFIG["otzaria"]["old_books_path"])
new_books_path = Path(CONFIG["otzaria"]["export_books_path"])
api_books_path = Path(CONFIG["otzaria"]["api_books_path"])


def get_folder_content(books_path: Path) -> tuple[dict[str, Path], ...]:
    files_dict = {}
    folders_dict = {}
    for root, folders, files in books_path.walk():
        for file in files:
            rel_path = get_rel_path(root, file, books_path)
            files_dict[file] = rel_path
        for folder in folders:
            rel_path = get_rel_path(root, folder, books_path)
            folders_dict[folder] = rel_path
    return files_dict, folders_dict


def get_rel_path(root: Path, name: str, books_path: Path) -> Path:
    path = root / name
    return path.relative_to(books_path)


new_books_files, _ = get_folder_content(new_books_path)
old_books_files, _ = get_folder_content(old_books_path)
api_books_files, _ = get_folder_content(api_books_path)
delete_api_files = CONFIG["otzaria"]["delete_api_files"]
not_in_old = {}
not_in_new = {}
in_api_dict = {}
new_books_files_copy = new_books_files.copy()
for file_name, rel_path in new_books_files_copy.items():
    old_books_full_path = old_books_path / rel_path
    if old_books_full_path.exists():
        continue
    in_old = old_books_files.get(file_name)
    if in_old:
        target_path = new_books_path / in_old
        target_path.parent.mkdir(parents=True, exist_ok=True)
        new_book_full_path = new_books_path / rel_path
        new_book_full_path.rename(target_path)
        new_books_files[file_name] = in_old
        continue

    not_in_old[file_name] = rel_path
    in_api = api_books_files.get(file_name)
    if in_api:
        if delete_api_files:
            (api_books_path / in_api).unlink()
        else:
            in_api_dict[file_name] = in_api


for file_name, rel_path in old_books_files.items():
    if new_books_files.get(file_name):
        continue
    not_in_new[file_name] = rel_path

for root, folders, _ in new_books_path.walk(top_down=False):
    for folder in folders:
        folder_path = root / folder
        if not folder_path.iterdir():
            folder_path.rmdir()

log_file_path = Path(CONFIG["otzaria"]["log_path"])
not_in_new_file_path = log_file_path / "not_in_new.csv"
with not_in_new_file_path.open("w", encoding="windows-1255", newline="") as f:
    writer = csv.writer(f)
    for key, value in not_in_new.items():
        writer.writerow([key, value])


not_in_old_file_path = log_file_path / "not_in_old.csv"
with not_in_old_file_path.open("w", encoding="windows-1255", newline="") as f:
    writer = csv.writer(f)
    for key, value in not_in_old.items():
        writer.writerow([key, value])

if not delete_api_files and in_api_dict:
    in_api_file_path = log_file_path / "in_api.csv"
    with in_api_file_path.open("w", encoding="windows-1255", newline="") as f:
        writer = csv.writer(f)
        for key, value in in_api_dict.items():
            writer.writerow([key, value])
