import prompt


def welcome():
    print("Первая попытка запустить проект!\n")
    print("***")

    help_message = (
        "<command> exit - выйти из программы\n"
        "<command> help - справочная информация"
    )

    while True:
        print(help_message)
        command = prompt.string("Введите команду: ")

        if command == "exit":
            break
        elif command == "help":
            print()
        else:
            print()