from random import randint
from colorama import init, Fore
init(autoreset=True)


class Dot:  # Координаты
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot[{self.x}, {self.y}]'


class BoardException(Exception):  # Исключения
    pass


class BoardMissException(BoardException):
    def __str__(self):
        return Fore.RED + 'Shot out of bounds!'


class BoardRepeatException(BoardException):
    def __str__(self):
        return Fore.RED + 'we already shot there!'


class BoardShipOutException(BoardException):
    pass


class Warships:  # Корабли
    def __init__(self, sh_road, sh_size, sh_fairway):
        self.sh_road = sh_road
        self.sh_size = sh_size
        self.sh_fairway = sh_fairway

        self.lives = sh_size

    @property
    def dots(self):
        sh_dots = []
        for i in range(self.sh_size):
            fairway_x = self.sh_road.x
            fairway_y = self.sh_road.y

            if self.sh_fairway == 0:
                fairway_x += i

            else:
                fairway_y += i

            sh_dots.append(Dot(fairway_x, fairway_y))

        return sh_dots

    def chek_hit(self, shot):
        return shot in self.dots


class Board:  # Поле
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.count = 0

        self.field = [[Fore.BLUE + '~'] * size for _ in range(size)]

        self.worships = []
        self.inaccess = []

    def __str__(self):
        res = ''
        res += '' + Fore.BLUE + '     1 | 2 | 3 | 4 | 5 | 6    \n  ==========================='

        for i, row in enumerate(self.field):
            res += f'\n{i + 1} || ' + ' | '.join(row) + ' ||'

        if self.hid:
            res = res.replace('■', Fore.BLUE + '~')
        return res

    def out_board(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1)]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out_board(cur)) and cur not in self.inaccess:
                    if verb:
                        self.field[cur.x][cur.y] = Fore.YELLOW + '¤' + Fore.BLUE
                    self.inaccess.append(cur)

    def add_warship(self, ship):
        for d in ship.dots:
            if self.out_board(d) or d in self.inaccess:
                raise BoardShipOutException
        for d in ship.dots:
            self.field[d.x][d.y] = Fore.GREEN + '■' + Fore.BLUE
            self.inaccess.append(d)

        self.worships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out_board(d):
            print(Fore.RED + 'Shot out of bounds!')
            return BoardMissException

        if d in self.inaccess:
            raise BoardRepeatException

        self.inaccess.append(d)

        for ship in self.worships:
            if ship.chek_hit(d):
                ship.lives -= 1
                self.field[d.x][d.y] = Fore.RED + 'X' + Fore.BLUE
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print(Fore.GREEN + 'Ship destroyed!')
                    return True
                else:
                    print(Fore.GREEN + 'Excellent shot!')
                    return True

        self.field[d.x][d.y] = Fore.YELLOW + '¤' + Fore.BLUE
        print(Fore.YELLOW + 'Miss!')
        return False

    def begin(self):
        self.inaccess = []


class Player:  # Игроки
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(Fore.RED + f'Enemy shot: {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input(Fore.GREEN + 'Your shot: ').split()
            if len(cords) != 2:
                print(Fore.RED + 'Enter 2 coordinates')
                continue

            x, y = cords

            if not(x.isdigit()) or not (y.isdigit()):
                print(Fore.RED + 'Enter numbers! ')
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class GamePlay:

    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):

        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for i in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Warships(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0, 1))
                try:
                    board.add_warship(ship)
                    break
                except BoardShipOutException:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def print_boards(self):
        print(Fore.BLUE + '≈' * 29)
        print(Fore.GREEN + 'Your field ')
        print(self.us.board)
        print(Fore.BLUE + '≈' * 29)
        print(Fore.RED + 'Enemy field')
        print(self.ai.board)
        print(Fore.BLUE + '≈' * 29)

    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                repeat = self.us.move()
            else:
                print(Fore.RED + 'Enemy shot')
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                self.print_boards()
                print(Fore.BLUE + '≈' * 29)
                print(Fore.GREEN + '≈ ¤ ≈ VICTORY! ≈ ¤ ≈')
                break

            if self.us.board.count == 7:
                self.print_boards()
                print(Fore.BLUE + '≈' * 29)
                print(Fore.RED + '≈ ☠ ≈ DEFEAT! ≈ ☠ ≈')
                break
            num += 1

    def greet(self):
        print(Fore.BLUE + '≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈')
        print(Fore.BLUE + '≈≈≈≈≈≈≈≈ ' + Fore.CYAN + 'Welcome  to' + Fore.BLUE + ' ≈≈≈≈≈≈≈≈')
        print(Fore.BLUE + '≈≈≈≈ ' + Fore.CYAN + 'Battle  of Worships' + Fore.BLUE + ' ≈≈≈≈')
        print(Fore.BLUE + '≈≈≈≈≈≈≈≈≈≈≈ ' + Fore.CYAN + 'Game!' + Fore.BLUE + ' ≈≈≈≈≈≈≈≈≈≈≈')
        print(Fore.BLUE + '≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈')
        print(Fore.BLUE + '≈≈≈≈≈≈ ' + Fore.CYAN + 'To made a shot:' + Fore.BLUE + ' ≈≈≈≈≈≈')
        print(Fore.BLUE + '≈≈≈ ' + Fore.CYAN + 'Enter X and Y values!' + Fore.BLUE + ' ≈≈≈')

    def start(self):
        self.greet()
        self.loop()


g = GamePlay()
g.start()
