from functools import cache, wraps
import time

def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper

def confirm_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            confirmation = input(f"Вы уверены, что хотите {action_name}? [y/n]: ")
            if confirmation.lower() == 'y':
                return func(*args, **kwargs)
            else:
                print(f"Действие '{action_name}' отменено пользователем.")
        return wrapper
    return decorator

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {elapsed_time:.3f} секунд.")
        return result
    return wrapper

def create_cacher():
    cache_dict = {}

    def cache_result(key, value_func):
        if key in cache_dict:
            return cache_dict[key]
        else:
            result = value_func()
            cache_dict[key] = result
            return result

    return cache_result

    
