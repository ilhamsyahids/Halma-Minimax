NEUTRAL = 0
RED = 1
GREEN = 2
MOVEMENTS = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]

from Pawn import Pawn
from typing import Tuple
import algoritma

class Halma:
    def __init__(self, board_size=16, time_limit=30, user_color=RED):
        self.board_size = board_size
        self.time_limit = time_limit
        self.user_color = user_color

        # set board with all blank
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        # init pawns
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j] = self.get_home_info(i, j)


    def __str__(self):
        s = ''
        for row in self.board:
            for el in row:
                s += str(el) + ' '
            s+='\n'
        return s

    def move(self, point_from:Tuple, point_to:Tuple):
        self.board[point_to[0]][point_to[1]].kind = self.board[point_from[0]][point_from[1]].kind
        self.board[point_from[0]][point_from[1]].kind = NEUTRAL

    def get_home_info(self, x, y):
        if x + y < 4:
            return Pawn(x, y, RED)
        elif x + y > 2*(self.board_size-3):
            return Pawn(x, y, GREEN)
        else:
            return Pawn(x, y)

    def is_on_board(self, point):
        return 0 <= point[0] < self.board_size and 0 <= point[1] < self.board_size

    def check_winner(self):
        goal_red, goal_green = self.get_goal()
        if all(pawn.kind == RED for pawn in goal_red):
            return RED
        elif all(pawn.kind == GREEN for pawn in goal_green):
            return GREEN
        else:
            return None
    
    def get_goal(self):
        goal_red = []
        goal_green = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if i + j > 2 * (self.board_size-3):
                    goal_red.append(self.board[i][j])
                if i + j < 4:
                    goal_green.append(self.board[i][j])
        return goal_red, goal_green

    def get_board_numeric(self):
        board = []
        for row in self.board:
            row_el = []
            for pawn in row:
                row_el.append(pawn.kind)
            board.append(row_el)
        return board

    def get_possible_move(self, point, possible_moves=[], adj=True, depth=0):
        possible_moves.append(point)
        for movement in MOVEMENTS:
            point_to = (point[0]+movement[0],point[1]+movement[1])
            # cek apa di dalam board
            if self.is_on_board(point_to):
                # kalau sampingnya kosong, append jika adj true
                if self.is_empty_cell(point_to):
                    # validasi move
                    if self.is_valid_move(point, point_to):
                        if adj and (point_to not in possible_moves):
                            possible_moves.append(point_to)
                    continue
                # coba lompat
                point_to = (point_to[0]+movement[0],point_to[1]+movement[1])
                if self.is_on_board(point_to):
                    # kalau sampingnya kosong, append lalu cek movenya
                    if self.is_valid_move(point, point_to) and point_to not in possible_moves:
                        possible_moves.append(point_to)
                        self.move(point, point_to) # dipindah dulu
                        self.get_possible_move(point_to, possible_moves, False, depth+1)
                        self.move(point_to, point) # dibalikin lagi
        possible_moves.remove(point)
        if depth==0:
            print(point, possible_moves)
            print(self)

    def is_valid_move(self, point_from, point_to):
        '''
        Validasi masuk/keluar home/target
        '''
        kind_from = self.board[point_from[0]][point_from[1]].kind
        kind_to = self.board[point_to[0]][point_to[1]].kind
        res = kind_to == NEUTRAL
        if res:
            if kind_from==RED:
                # udah masuk target, gak boleh keluar dari target
                if point_from[0]+point_from[1] > 2*(self.board_size-3):
                    res = point_to[0]+point_to[1] > 2*(self.board_size-3)
                # udah keluar home, gak boleh masuk ke home
                elif not (point_from[0]+point_from[1]<4):
                    res = not (point_to[0]+point_to[1]<4)
            elif kind_from==GREEN:
                # udah masuk target, gak boleh keluar dari target
                if point_from[0]+point_from[1]<4:
                    res = point_to[0]+point_to[1]<4
                # udah keluar home, gak boleh masuk ke home
                elif not (point_from[0]+point_from[1] > 2*(self.board_size-3)):
                    res = not (point_to[0]+point_to[1] > 2*(self.board_size-3))
        return res

    def is_empty_cell(self, point):
        return self.board[point[0]][point[1]].kind == NEUTRAL


if __name__ == "__main__":
    # coba2 doang
    halma = Halma(8)
    print(halma)
    print(halma.check_winner())
    arr = []
    halma.get_possible_move((3,0),arr)
    print(arr)
    print(halma.get_board_numeric())
