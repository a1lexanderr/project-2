#!/usr/bin/env python3
from primitive_db.engine import run


def main():
    try:
        run()
    except Exception as e:
        print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()