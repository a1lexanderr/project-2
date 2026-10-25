import shlex
from prettytable import PrettyTable
from primitive_db.core import create_table, drop_table, list_tables, insert, select, update, delete, info
from primitive_db.utils import load_metadata, save_metadata, load_table_data, save_table_data
from primitive_db.parser import parse_where, parse_update, parse_insert_values

DB_FILE = "db_meta.json"

def print_help():
    print("\n***Операции с данными***\n")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit - выход из программы")
    print("<command> help- справочная информация\n")

def run():
    print("***База данных***")
    
    while True:
        metadata = load_metadata(DB_FILE)
        
        try:
            user_input = input(">>> Введите команду: ").strip()
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
            
        command = args[0].lower()
        
        match command:
            case "exit":
                break
            case "help":
                print_help()
            case "list_tables":
                list_tables(metadata)
            case "create_table":
                if len(args) < 2:
                    print("Некорректное значение: имя_таблицы.")
                else:
                    table_name = args[1]
                    columns_raw = args[2:]
                    metadata, success = create_table(metadata, table_name, columns_raw)
                    if success: save_metadata(DB_FILE, metadata)
                    
            case "drop_table":
                if len(args) < 2:
                    print("Некорректное значение: имя_таблицы.")
                else:
                    table_name = args[1]
                    metadata, success = drop_table(metadata, table_name)
                    if success: save_metadata(DB_FILE, metadata)
                    
            case "insert":
                if len(args) < 5 or args[1].lower() != "into" or args[3].lower() != "values":
                    print("Синтаксис: insert into <имя_таблицы> values (<значение1>, ...)")
                    continue
                table_name = args[2]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue
                    
                values, err = parse_insert_values(user_input)
                if err:
                    print(err)
                    continue
                    
                table_data = load_table_data(table_name)
                new_data, success, msg = insert(metadata, table_name, table_data, values)
                print(msg)
                if success:
                    save_table_data(table_name, new_data)

            case "select":
                if len(args) < 3 or args[1].lower() != "from":
                    print("Синтаксис: select from <имя_таблицы> [where ...]")
                    continue
                table_name = args[2]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue
                    
                where_clause = None
                if len(args) > 3:
                    where_clause, err = parse_where(metadata, table_name, args, 3)
                    if err:
                        print(err)
                        continue
                        
                table_data = load_table_data(table_name)
                results = select(table_data, where_clause)
                
                if results:
                    pt = PrettyTable()
                    columns = list(metadata[table_name].keys())
                    pt.field_names = columns
                    for row in results:
                        pt.add_row([row.get(col, "") for col in columns])
                    print(pt)
                else:
                    print("Записи не найдены.")

            case "update":
                if len(args) < 6:
                    print("Синтаксис: update <имя_таблицы> set <столбец> = <значение> [where ...]")
                    continue
                table_name = args[1]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue
                    
                set_clause, where_clause, err = parse_update(args, metadata, table_name)
                if err:
                    print(err)
                    continue
                    
                table_data = load_table_data(table_name)
                new_data, success, msg = update(table_data, table_name, set_clause, where_clause)
                print(msg)
                if success:
                    save_table_data(table_name, new_data)

            case "delete":
                if len(args) < 3 or args[1].lower() != "from":
                    print("Синтаксис: delete from <имя_таблицы> where ...")
                    continue
                table_name = args[2]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue
                    
                where_clause = None
                if len(args) > 3:
                    where_clause, err = parse_where(metadata, table_name, args, 3)
                    if err:
                        print(err)
                        continue
                else:
                    print("Ошибка: Укажите условие WHERE для удаления.")
                    continue
                    
                table_data = load_table_data(table_name)
                new_data, success, msg = delete(table_data, table_name, where_clause)
                print(msg)
                if success:
                    save_table_data(table_name, new_data)
                    
            case "info":
                if len(args) < 2:
                    print("Синтаксис: info <имя_таблицы>")
                    continue
                table_name = args[1]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue
                    
                table_data = load_table_data(table_name)
                _, msg = info(metadata, table_name, table_data)
                print(msg)
                
            case _:
                print(f"Функции {command} нет. Попробуйте снова.")