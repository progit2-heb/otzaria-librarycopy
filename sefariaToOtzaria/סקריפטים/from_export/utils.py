import csv
from pathlib import Path

import tomllib

CONFIG_FILE_PATH = Path(__file__).parent / "config.toml"
with CONFIG_FILE_PATH.open("rb") as f:
    CONFIG = tomllib.load(f)


def read_csv_file(file_path: Path, with_headers: bool = False) -> dict[str, str]:
    dict_replacements = {}
    with file_path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        if with_headers:
            next(reader)
        for row in reader:
            if row[0] and row[1]:
                dict_replacements[row[0]] = row[1]
    return dict_replacements
