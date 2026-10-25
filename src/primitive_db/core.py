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