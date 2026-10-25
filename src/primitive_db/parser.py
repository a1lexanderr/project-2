import re
import csv

def cast_value(val_str, expected_type):
    """Конвертирует строку в нужный тип данных на основе метаданных таблицы."""
    val_str = str(val_str).strip().strip("'\"")
    
    if expected_type == "int":
        return int(val_str)
    elif expected_type == "bool":
        if val_str.lower() in ("true", "1", "t"): return True
        if val_str.lower() in ("false", "0", "f"): return False
        raise ValueError(f"Некорректное boolean значение: {val_str}")
    return val_str

def parse_where(metadata, table_name, tokens, start_idx):
    """Разбирает условие WHERE: where <col> = <val>"""
    if len(tokens) <= start_idx:
        return None, None
    if tokens[start_idx].lower() != "where":
        return None, "Ошибка синтаксиса: ожидалось WHERE."
    if len(tokens) - start_idx < 4:
        return None, "Ошибка синтаксиса WHERE: ожидалось <столбец> = <значение>."
    
    col = tokens[start_idx + 1]
    op = tokens[start_idx + 2]
    val_str = tokens[start_idx + 3]
    
    if op != "=":
        return None, "Поддерживается только оператор '='"
    if col not in metadata[table_name]:
        return None, f"Столбец '{col}' не найден."
        
    try:
        val = cast_value(val_str, metadata[table_name][col])
    except ValueError:
        return None, f"Некорректное значение '{val_str}' для типа {metadata[table_name][col]}."
        
    return {col: val}, None

def parse_update(tokens, metadata, table_name):
    """Разбирает запрос UPDATE: set <col> = <val> where ..."""
    if len(tokens) < 6:
        return None, None, "Синтаксис: update <имя_таблицы> set <столбец> = <значение> [where ...]"
    
    if tokens[2].lower() != "set" or tokens[4] != "=":
        return None, None, "Ошибка синтаксиса: ожидалось SET <столбец> = <значение>."
        
    col = tokens[3]
    val_str = tokens[5]
    
    if col not in metadata[table_name]:
        return None, None, f"Столбец '{col}' не найден."
        
    try:
        val = cast_value(val_str, metadata[table_name][col])
    except ValueError:
        return None, None, f"Некорректное значение '{val_str}' для типа {metadata[table_name][col]}."
        
    set_clause = {col: val}
    
    where_clause = None
    if len(tokens) > 6:
        where_clause, err = parse_where(metadata, table_name, tokens, 6)
        if err:
            return None, None, err
            
    return set_clause, where_clause, None

def parse_insert_values(user_input):
    """Вытаскивает значения из скобок values (...)"""
    match = re.search(r'(?i)values\s*\((.*)\)', user_input)
    if not match:
        return None, "Синтаксис: insert into <имя_таблицы> values (<значение1>, ...)"
    
    values_str = match.group(1)
    try:
        reader = csv.reader([values_str], skipinitialspace=True)
        values = [v.strip().strip("'\"") for v in next(reader)]
        return values, None
    except Exception:
        return None, "Ошибка разбора значений."