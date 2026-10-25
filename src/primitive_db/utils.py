import json
import os

DATA_DIR = "data"

def _ensure_data_dir():
    """Создает папку data, если ее не существует."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_metadata(filepath):
    """Загружает метаданные из JSON-файла."""
    if not os.path.exists(filepath):
        return {}
    
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_table_data(table_name):
    """Загружает данные конкретной таблицы из data/<table_name>.json"""
    _ensure_data_dir()
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_table_data(table_name, data):
    """Сохраняет список словарей в data/<table_name>.json"""
    _ensure_data_dir()
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)