import os

new_books_path = r"C:\Users\Otzaria\Desktop\otzaria"

replace_folder_names = {
    "ראשונים על": "ראשונים",
    "אחרונים על": "אחרונים",
    "פירושים מודרניים": "מחברי זמננו",
    "חידושי רמבן": "רמבן",
    "ספרות מודרנית": "מחברי זמננו"
}

talmud_path = os.path.join(new_books_path, "תלמוד")
os.rename(os.path.join(talmud_path, "בבלי"), os.path.join(new_books_path, "תלמוד בבלי"))
os.rename(os.path.join(talmud_path, "ירושלמי"), os.path.join(new_books_path, "תלמוד ירושלמי"))
os.rmdir(talmud_path)

for root, folders, files in os.walk(new_books_path, topdown=False):
    for folder in folders:
            for key, value in replace_folder_names.items():
                if key in folder:
                    folder_path = os.path.join(root, folder)
                    folder = value
                    new_path = os.path.join(root, folder)
                    os.rename(folder_path, new_path)
