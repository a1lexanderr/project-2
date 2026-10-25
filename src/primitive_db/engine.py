import shlex

from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import load_metadata, save_metadata

DB_FILE = "db_meta.json"

def print_help():
    """Prints the help message for the current mode."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print("***База данных***")
    
    while True:
        metadata = load_metadata(DB_FILE)
        
        try:
            user_input = input(">>>Введите команду: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
            
        if not user_input:
            continue
            
        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Ошибка: не удалось разобрать команду (проверьте кавычки).")
            continue
            
        command = args[0]
        
        match command:
            case "exit":
                break
                
            case "help":
                print_help()
                
            case "list_tables":
                list_tables(metadata)
                
            case "create_table":
                if len(args) < 2:
                    print("Некорректное значение: имя_таблицы. Попробуйте снова.")
                else:
                    table_name = args[1]
                    columns_raw = args[2:]
                    metadata, success = create_table(metadata, table_name, columns_raw)
                    if success:
                        save_metadata(DB_FILE, metadata)
                        
            case "drop_table":
                if len(args) < 2:
                    print("Некорректное значение: имя_таблицы. Попробуйте снова.")
                else:
                    table_name = args[1]
                    metadata, success = drop_table(metadata, table_name)
                    if success:
                        save_metadata(DB_FILE, metadata)
                        
            case _:
                print(f"Функции {command} нет. Попробуйте снова.")