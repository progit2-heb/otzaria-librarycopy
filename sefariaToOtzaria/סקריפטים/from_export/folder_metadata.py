import json
from pathlib import Path

from utils import CONFIG, read_csv_file

toc_file_path = Path(CONFIG["sefaria"]["toc_file"])
folder_metadata_file_path = Path(CONFIG["otzaria"]["folder_metadata_file_path"])


def recursive_register_categories(category: list | dict, data: list | None = None) -> list[dict]:
    if data is None:
        data = []
    if isinstance(category, list):
        for item in category:
            recursive_register_categories(item, data)
    if 'contents' in category:
        for item in category['contents']:
            recursive_register_categories(item, data)
    if 'heCategory' in category:
        he_category = category['heCategory']
        he_short_desc = category['heShortDesc'] if 'heShortDesc' in category else None
        he_desc = category['heDesc'] if 'heDesc' in category else None
        order = category['order'] if 'order' in category else None
        data.append({"title": he_category, 'heDesc': he_desc, "heShortDesc": he_short_desc, "order": order})
    return data


with toc_file_path.open('r', encoding='utf-8') as f:
    toc = json.load(f)
folder_name_replacements_file_path = Path(CONFIG["otzaria"]["folder_name_replacements_file_path"])
folder_name_replacements = read_csv_file(folder_name_replacements_file_path)

data = recursive_register_categories(toc)
data_copy = data.copy()
for index, entry in enumerate(data_copy):
    for key, value in folder_name_replacements.items():
        if key in entry["title"]:
            data[index]["title"] = value

with folder_metadata_file_path.open('w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
