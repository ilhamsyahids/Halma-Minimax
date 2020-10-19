NEUTRAL = 0
RED = 1
GREEN = 2
MOVEMENTS = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]

from Board import Board
from Pawn import Pawn
from typing import Tuple
import algoritma

class Halma:
    def __init__(self, board_size=8, time_limit=30, user_color=RED):
        self.board_size = board_size
        self.time_limit = time_limit
        self.user_color = user_color

        # set board with all blank
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        # init pawns
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j] = self.get_home_info(i, j)

        # set goal
        self.goal_r = [i for row in self.board for i in row if i.kind == RED]
        self.goal_g = [i for row in self.board for i in row if i.kind == GREEN]

        # self.board = Board(self.board)    # kayaknya jadi susah gan kalau pakai ini
        

        # giliran pemain
        self.turn = GREEN

    def __str__(self):
        s = ''
        for row in self.board:
            for el in row:
                s += str(el) + ' '
            s+='\n'
        return s

    def move(self, point_from:Tuple, point_to:Tuple):
        self.board[point_to[0]][point_to[1]] = self.board[point_from[0]][point_from[1]]
        self.board[point_from[0]][point_from[1]] = Pawn(point_from[0], point_from[1])

    def get_home_info(self, x, y):
        if x + y < 4:
            return Pawn(x, y, 1)
        elif x + y > 2*(self.board_size-3):
            return Pawn(x, y, 2)
        else:
            return Pawn(x, y)

    def is_on_board(self, point):
        return 0 <= point[0] < self.board_size and 0 <= point[1] < self.board_size

    def check_winner(self):
        if all(pawn.kind == RED for pawn in self.goal_g):
            return RED
        elif all(pawn.kind == GREEN for pawn in self.goal_r):
            return GREEN
        else:
            return None

    def get_board_numeric(self):
        board = []
        for row in self.board:
            row_el = []
            for pawn in row:
                row_el.append(pawn.kind)
            board.append(row_el)
        return board

    def computer_turn(self):
        move = algoritma.find_next_move(self.get_board_numeric(), \
            RED if self.user_color==GREEN else GREEN)
        self.move(move[0], move[1])

    def get_possible_move(self, point, possible_moves=[], adj=True):
        for movement in MOVEMENTS:
            point_to = (point[0]+movement[0],point[1]+movement[1])
            # cek apa di dalam board
            if self.is_on_board(point_to):
                # kalau sampingnya kosong, append jika adj true
                if self.board[point_to[0]][point_to[1]].kind == NEUTRAL:
                    if adj:
                        possible_moves.append(point_to)
                    continue
            # coba lompat
            point_to = (point_to[0]+movement[0],point_to[1]+movement[1])
            if self.is_on_board(point_to):
                # kalau sampingnya kosong, append lalu cek movenya
                if self.board[point_to[0]][point_to[1]].kind == NEUTRAL and point_to not in possible_moves:
                    possible_moves.append(point_to)
                    self.get_possible_move(point_to, possible_moves, False)


if __name__ == "__main__":
    # coba2 doang
    halma = Halma(8)
    print(halma)
    print(halma.check_winner())
    arr = []
    halma.get_possible_move((3,0),arr,True)
    print(arr)
    print(halma.get_board_numeric())
    halma.computer_turn()
    print(halma)
