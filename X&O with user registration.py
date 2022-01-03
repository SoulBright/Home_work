pasw = {'user1' : '123', 'user2' : '321'}

# Проверка пользователя:

def user_check():
    count = 3
    while True:
        if count == 0:
            print('Превышено колличество попыток!')
            return False
        count -= 1
        print(f'Осталось попыток: {count + 1}')
        login = input('Введите Логин: ').lower()
        password = input('Введите пароль: ')

        if login in pasw:
            if pasw[login] == password:
                print (' --- Вход выполнен! --- ')
                return True
            else:
                print('Не верный пароль!')
        else:
            print('Пользователь не найден!')

# регистрация пользователяЖ

def registration():
    while True:
        reg_login = input('Введите логин: ')
        if reg_login in pasw:
            print('Пользователь с таким именем уже существует!')
        else:
            break
    reg_pass = input('Введите пароль: ')
    pasw[reg_login] = reg_pass
    return pasw

# Игра:

def game():
    print('')
    print(' --- КРЕСТИКИ НОЛИКИ --- ')
    print('')
    print(' -- Чтобы сделать ход -- ')
    print(' - Введите  координаты - ')
    print(' ---  " X " и " Y "  --- ')
    print('')

    # Поле:

    field = [['▒'] * 3 for _ in range(3)]


    def show_field():
        print('  0 1 2')
        for i in range(len(field)):
            print(str(i), *field[i])


    # Ввод данных:

    def user_turn():
        while True:
            turn = input('Введите координаты: ').split()
            if len(turn) != 2:
                print('Не верные координаты! Введите две цифры!')
                continue

            x, y = turn

            if not turn[0].isdigit() or not turn[1].isdigit():
                print('Не верные координаты! Введите цифры!')
                continue

            x, y = int(x), int(y)

            if not (2 >= x >= 0) or not (2 >= y >= 0):
                print('Не верные координаты! Введите цифры в диапазоне от 0 до 2!')
                continue

            if field[x][y] != '▒':
                print('Ход невозможен! Клетка занята!')
                continue

            return x, y


    # Условие победы:

    def win_condition():
        win_cond = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                    ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                    ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
        for cord in win_cond:
            turn = []
            for c in cord:
                turn.append(field[c[0]][c[1]])
                if turn == ['X', 'X', 'X']:
                    show_field()
                    print('Игра окончена! Победил -- X -- !!!')
                    return True
                if turn == ['O', 'O', 'O']:
                    show_field()
                    print('Игра окончена! Победил -- O -- !!!')
                    return True
        return False


    # Основной код:

    count = 0
    while True:
        count += 1
        show_field()
        if count % 2 == 1:
            print('')
            print(' --- Ходит Крестик! --- ')
        else:
            print('')
            print(' --- Ходит Нолик --- ')

        x, y = user_turn()

        if count % 2 == 1:
            field[x][y] = 'X'
        else:
            field[x][y] = 'O'

        if win_condition():
            break

        if count == 9:
            show_field()
            print('')
            print('Игра окончена! Победитель не выявлен!')
            break

print(' - Чтобы продолжить: войдите или зарегистрируйтесь! - ')
print(' ---  Для входа введите "L" для Регистрации "R"   --- ')
R_L = input(': ')
if R_L == 'L':
    user_check()
else:
    registration()
    print(' --- Регистрация завершена! --- ')
    print(' --- Выолните вход в систему! --- ')
    user_check()

if True:
    game()