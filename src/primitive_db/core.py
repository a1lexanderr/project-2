from primitive_db.parser import cast_value

SUPPORTED_TYPES = {"int", "str", "bool"}

def create_table(metadata, table_name, columns_raw):
    """Создает новую таблицу и добавляет ее в метаданные."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata, False

    columns = {"ID": "int"}

    for col in columns_raw:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata, False
        
        col_name, col_type = col.split(":", 1)
        
        if col_type not in SUPPORTED_TYPES:
            print(f"Некорректное значение: {col_type}. Попробуйте снова.")
            return metadata, False
        
        columns[col_name] = col_type

    metadata[table_name] = columns
    
    columns_str = ", ".join(f"{name}:{type_}" for name, type_ in columns.items())
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')
    
    return metadata, True


def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata, False
    
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata, True


def list_tables(metadata):
    """Выводит список всех таблиц."""
    if not metadata:
        return
        
    for table_name in metadata.keys():
        print(f"- {table_name}")

def insert(metadata, table_name, table_data, values):
    columns = list(metadata[table_name].items())
    if len(values) != len(columns) - 1:
        return table_data, False, "Некорректное количество значений."
    
    new_id = max([row.get("ID", 0) for row in table_data], default=0) + 1
    new_record = {"ID": new_id}
    
    try:
        for i, val_str in enumerate(values):
            col_name = columns[i+1][0]
            col_type = columns[i+1][1]
            new_record[col_name] = cast_value(val_str, col_type)
    except ValueError as e:
        return table_data, False, f"Ошибка типа: {e}"
        
    table_data.append(new_record)
    return table_data, True, f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".'

def select(table_data, where_clause=None):
    if not where_clause:
        return table_data
    return [row for row in table_data if all(row.get(k) == v for k, v in where_clause.items())]

def update(table_data, table_name, set_clause, where_clause):
    updated_ids = []
    for row in table_data:
        if not where_clause or all(row.get(k) == v for k, v in where_clause.items()):
            for k, v in set_clause.items():
                row[k] = v
            updated_ids.append(row["ID"])
    
    if updated_ids:
        ids_str = ", ".join(map(str, updated_ids))
        return table_data, True, f'Запись с ID={ids_str} в таблице "{table_name}" успешно обновлена.'
    return table_data, False, "Записи по условию не найдены."

def delete(table_data, table_name, where_clause):
    to_delete = []
    for row in table_data:
        if not where_clause or all(row.get(k) == v for k, v in where_clause.items()):
            to_delete.append(row["ID"])
    
    if not to_delete:
        return table_data, False, "Записи по условию не найдены."
        
    table_data = [row for row in table_data if row["ID"] not in to_delete]
    ids_str = ", ".join(map(str, to_delete))
    return table_data, True, f'Запись с ID={ids_str} успешно удалена из таблицы "{table_name}".'

def info(metadata, table_name, table_data):
    cols_str = ", ".join([f"{k}:{v}" for k, v in metadata[table_name].items()])
    msg = (f"Таблица: {table_name}\n"
           f"Столбцы: {cols_str}\n"
           f"Количество записей: {len(table_data)}")
    return True, msg