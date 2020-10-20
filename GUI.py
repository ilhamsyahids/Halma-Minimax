from tkinter import *
from functools import partial
from tkinter import ttk
from math import floor
from timeit import default_timer as timer
from datetime import timedelta

import random
import Halma
import algoritma

# COLORS
RED = "#C62828"
GREEN = "#2E7D32"
BLUE_GRAY = "#B0BEC5"
LIGHT_BLUE_GRAY = "#ECEFF1"
DARK_GRAY = "#212121"
MAGENTA = "#880E4F"
YELLOW = "#ffe082"
TILE_COLORS = (BLUE_GRAY, LIGHT_BLUE_GRAY)
TILE_COLORS_RED = ("#f48fb1", "#f8bbd0")
TILE_COLORS_GREEN = ("#aed581", "#c5e1a5")
TARGET_COLORS = ("#000000", "#e57373", "#81c784")

# TUPLES
GAME_MODE = ("Minimax Bot vs Human", "Minimax+LS Bot vs Human", "Minimax vs Minimax+LS")
TURN_LABEL = ("Red's Turn", "Green's Turn")
TURN_LABEL_DESC = ("Human", "Minimax Bot", "Minimax + Local Search Bot")

class Window(object):

    def __init__(self, master):
        # Setup main window
        self.master = master
        self.master.title("Halma")
        self.master.resizable(True, True)
        window_width = 960
        window_height = 480
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        # -- MENU --
        self.frame_menu = Frame(self.master)
        self.frame_menu.place(anchor="w", relx=0.01, rely=0.5, width=240, height=400)

        i_row = 0

        ttk.Separator(self.frame_menu, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        # MODE
        self.label_mode = Label(self.frame_menu, text="Mode", font=("Verdana", 10, "bold"))
        self.label_mode.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.var_mode = StringVar()
        self.var_mode.set("Minimax Bot vs Human")
        self.dropdown_mode = OptionMenu(self.frame_menu, self.var_mode,
                                        GAME_MODE[0],
                                        GAME_MODE[1],
                                        GAME_MODE[2])
        self.dropdown_mode.grid(row=i_row, column=0, sticky="we")
        self.frame_menu.columnconfigure(0, weight=1)
        i_row += 1

        ttk.Separator(self.frame_menu, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        # BOARD SIZE
        self.label_board_size = Label(self.frame_menu, text="Board Size (NxN)", font=("Verdana", 10, "bold"))
        self.label_board_size.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.var_board_size = IntVar()
        self.var_board_size.set(16)
        self.scale_board_size = Scale(self.frame_menu, variable=self.var_board_size, from_=8, to=20, orient=HORIZONTAL)
        self.scale_board_size.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        ttk.Separator(self.frame_menu, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        # TIME LIMIT
        self.label_time_limit = Label(self.frame_menu, text="Time Limit (seconds)", font=("Verdana", 10, "bold"))
        self.label_time_limit.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.label_time_limit_desc = Label(self.frame_menu, text="Set 0 for no time limit",
                                           font=("Verdana", 8, "normal"))
        self.label_time_limit_desc.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.var_time_limit = IntVar()
        self.var_time_limit.set(30)
        self.scale_time_limit = Scale(self.frame_menu, variable=self.var_time_limit, from_=0, to=120, resolution=5,
                                      orient=HORIZONTAL)
        self.scale_time_limit.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        ttk.Separator(self.frame_menu, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        # HUMAN PLAYER
        self.label_human_player = Label(self.frame_menu, text="Human Player", font=("Verdana", 10, "bold"))
        self.label_human_player.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.frame_human_player = Frame(self.frame_menu)
        self.frame_human_player.grid(row=i_row, column=0)
        i_row += 1

        self.var_human_player = IntVar()
        self.var_human_player.set(1)

        self.radio_human_player_red = Radiobutton(self.frame_human_player, text="Red", value=1,
                                                  variable=self.var_human_player)
        self.radio_human_player_red.grid(row=0, column=0, sticky="we")
        self.radio_human_player_green = Radiobutton(self.frame_human_player, text="Green", value=2,
                                                    variable=self.var_human_player)
        self.radio_human_player_green.grid(row=0, column=1, sticky="we")

        ttk.Separator(self.frame_menu, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        # START GAME
        self.button_start_game = Button(self.frame_menu, text="Start Game", font=("Verdana", 14, "bold"), bg=BLUE_GRAY,
                                        command=self.start_game)
        self.button_start_game.grid(row=i_row, column=0)

        # -- INFO --
        self.frame_info = Frame(self.master)
        self.frame_info.place(anchor="e", relx=0.99, rely=0.5, width=240, height=400)

        i_row = 0

        ttk.Separator(self.frame_info, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        # TIMER
        self.label_timer = Label(self.frame_info, text="Timer", font=("Verdana", 10, "bold"))
        self.label_timer.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.var_timer = StringVar()
        self.var_timer.set("-")
        self.timer = Label(self.frame_info, textvariable=self.var_timer, font=("Verdana", 10, "bold"))
        self.timer.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        ttk.Separator(self.frame_info, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        # TURN
        self.var_turn = StringVar()
        self.var_turn.set("Game not started")
        self.label_turn = Label(self.frame_info, textvariable=self.var_turn, font=("Verdana", 10, "bold"))
        self.label_turn.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.var_turn_desc = StringVar()
        self.var_turn_desc.set("-")
        self.label_turn_desc = Label(self.frame_info, textvariable=self.var_turn_desc, font=("Verdana", 8, "normal"))
        self.label_turn_desc.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        ttk.Separator(self.frame_info, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1

        # TIME OUT BEHAVIOR
        self.label_time_out_behavior = Label(self.frame_info, text="Time Out Behavior", font=("Verdana", 10, "bold"))
        self.label_time_out_behavior.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.frame_time_out_behavior = Frame(self.frame_info)
        self.frame_time_out_behavior.grid(row=i_row, column=0)
        i_row += 1

        self.var_time_out_behavior = IntVar()
        self.var_time_out_behavior.set(0)

        self.radio_time_out_behavior_skip = Radiobutton(self.frame_time_out_behavior, text="Skip", value=0,
                                                        variable=self.var_time_out_behavior)
        self.radio_time_out_behavior_skip.grid(row=0, column=0, sticky="we")
        self.radio_time_out_behavior_random = Radiobutton(self.frame_time_out_behavior, text="Random", value=1,
                                                          variable=self.var_time_out_behavior)
        self.radio_time_out_behavior_random.grid(row=0, column=1, sticky="we")

        ttk.Separator(self.frame_info, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1
        
        # BOT DELAY
        self.label_bot_delay = Label(self.frame_info, text="Bot Delay (milliseconds)", font=("Verdana", 10, "bold"))
        self.label_bot_delay.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.label_bot_delay_desc = Label(self.frame_info, text="Move delay time for bot vs bot",
                                           font=("Verdana", 8, "normal"))
        self.label_bot_delay_desc.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        self.var_bot_delay_1 = IntVar()
        self.var_bot_delay_1.set(200)
        self.scale_bot_delay_1 = Scale(self.frame_info, variable=self.var_bot_delay_1, from_=100, to=1000, resolution=100,
                                      orient=HORIZONTAL)
        self.scale_bot_delay_1.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        Label(self.frame_info, text="Bot 1").grid(row=i_row, column=0, sticky="w")
        i_row += 1

        self.var_bot_delay_2 = IntVar()
        self.var_bot_delay_2.set(500)
        self.scale_bot_delay_2 = Scale(self.frame_info, variable=self.var_bot_delay_2, from_=100, to=1000, resolution=100,
                                       orient=HORIZONTAL)
        self.scale_bot_delay_2.grid(row=i_row, column=0, sticky="we")
        i_row += 1

        Label(self.frame_info, text="Bot 2").grid(row=i_row, column=0, sticky="w")
        i_row += 1

        
    def start_game(self):
        self.board_size = self.var_board_size.get()
        self.mode = self.var_mode.get()
        self.time_limit = self.var_time_limit.get()
        self.human_player = 3 if self.mode == GAME_MODE[2] else self.var_human_player.get()
        self.bot_player = 2 if self.human_player == 1 else 1
        self.time_out_behavior = self.var_time_out_behavior.get()

        self.halma = Halma.Halma(self.board_size, self.time_limit, self.human_player)

        self.frame_board = Frame(self.master)
        self.frame_board.place(anchor="center", relx=0.5, rely=0.5, width=400, height=400)
        self.frame_board.config(borderwidth=2, relief="solid")
        for i in range(self.board_size):
            self.frame_board.columnconfigure(i, weight=1)
            self.frame_board.rowconfigure(i, weight=1)

        self.selected_tile = (-1, -1)

        self.tiles = [[None for i in range(self.board_size)] for i in range(self.board_size)]  # tile border
        self.tile_labels = [[None for i in range(self.board_size)] for i in range(self.board_size)]  # actual tile
        for i in range(self.board_size):
            for j in range(self.board_size):
                # selang-seling warna tile
                kind = self.halma.board[i][j].kind
                tile_color = self.get_tile_color(i, j)
                color = RED if kind == Halma.RED else GREEN if kind == Halma.GREEN else tile_color
                self.tiles[i][j] = Frame(self.frame_board, bg=tile_color)
                self.tile_labels[i][j] = Label(self.tiles[i][j], bg=tile_color, bd=0, fg=color, text=u"\u2B24",
                                               font=("Helvetica", int(40 - 1.6 * self.board_size), "bold"),
                                               anchor="center")
                self.tiles[i][j].grid(row=i, column=j, sticky="nesw")
                self.tile_labels[i][j].pack(padx=2, pady=2)
                self.tiles[i][j].bind('<Button-1>', partial(self.on_click_tile, x=i, y=j))  # klik kiri mouse
                self.tile_labels[i][j].bind('<Button-1>', partial(self.on_click_tile, x=i, y=j))
                self.tiles[i][j].bind("<Enter>", partial(self.on_enter_tile, x=i, y=j))  # hover enter
                self.tiles[i][j].bind("<Leave>", partial(self.on_leave_tile, x=i, y=j))  # hover leave

        self.run_number = 0
        self.winner = 0

        if self.time_limit != 0:
            self.timer_start = timer()
            self.update_timer()
        else:
            self.var_timer.set(u"\u221e")

        if self.mode == GAME_MODE[2]:
            self.run_bot_vs_bot()
        elif self.human_player == 2:  # bot jalan duluan
            using_ls = self.mode == GAME_MODE[1]
            self.move_bot(self.bot_player, using_ls)
        else:
            self.var_turn.set(TURN_LABEL[self.human_player-1])
            self.var_turn_desc.set(TURN_LABEL_DESC[0])
            self.label_turn['fg'] = RED if self.human_player == 1 else GREEN

    def update_timer(self):
        if self.time_limit != 0 and not self.winner:
            time_left = self.time_limit - floor(timedelta(seconds=timer() - self.timer_start).total_seconds())
            if time_left >= 0:
                self.var_timer.set(time_left)
                self.master.after(1000, self.update_timer)
            else:
                if self.time_out_behavior == 1:
                    self.move_random()
                # move bot   
                using_ls = self.mode == GAME_MODE[1]
                self.move_bot(self.bot_player, using_ls)
                self.update_timer()

    def run_bot_vs_bot(self):
        if not self.winner:
            self.run_number += 1
            if self.run_number % 2 == 0:
                self.play_bot_1()
            else:
                self.play_bot_2()
        elif self.winner == 1:
            self.var_turn.set("Red wins")
        elif self.winner == 2:
            self.var_turn.set("Green wins")


    def play_bot_1(self):
        self.move_bot(1, False)
        self.master.after(self.var_bot_delay_2.get(), self.run_bot_vs_bot)
        self.var_turn.set(TURN_LABEL[0])
        self.var_turn_desc.set(TURN_LABEL_DESC[1])
        self.label_turn['fg'] = RED
    def play_bot_2(self):
        self.move_bot(2, True)
        self.master.after(self.var_bot_delay_1.get(), self.run_bot_vs_bot)
        self.var_turn.set(TURN_LABEL[1])
        self.var_turn_desc.set(TURN_LABEL_DESC[2])
        self.label_turn['fg'] = GREEN

    def on_enter_tile(self, e, x, y):  # tile button on hover enter event
        self.tiles[x][y].config(bg=DARK_GRAY)

    def on_leave_tile(self, e, x, y):  # tile button on hover leave event
        if self.selected_tile != (x, y):
            self.tiles[x][y].config(bg=self.get_tile_color(x, y))
        else:
            self.tiles[x][y].config(bg=MAGENTA)

    def on_click_tile(self, e, x, y):
        if self.winner:
            return
        if self.selected_tile == (x, y):  # deselect tile
            self.hide_possible_moves()
            self.tiles[x][y].config(bg=DARK_GRAY)
            self.selected_tile = (-1, -1)
        elif self.selected_tile == (-1, -1):  # select a tile, sebelumnya belum ada yg di-select
            if self.halma.board[x][y].kind == self.human_player:
                # self.tiles[x][y].config(bg=MAGENTA)
                self.selected_tile = (x, y)
                self.show_possible_moves()
        else:  # pindah selection ke tile lain
            self.hide_possible_moves()
            a, b = self.selected_tile  # tile yg di-select sebelumnya
            possible_moves = []
            self.halma.get_possible_move((a, b), possible_moves)
            if self.halma.board[a][b].kind == self.human_player and self.halma.board[x][y].kind == 0 and (
            x, y) in possible_moves:  # bisa mindahin pawn
                self.move((a, b), (x, y))
                self.tiles[a][b].config(bg=self.get_tile_color(a, b))
                self.selected_tile = (-1, -1)
                # move bot   
                using_ls = self.mode == GAME_MODE[1]
                self.move_bot(self.bot_player, using_ls)
            else:  # cuma pindah selection
                if self.halma.board[x][y].kind == self.human_player:
                    self.tiles[a][b].config(bg=self.get_tile_color(a, b))
                    self.tiles[x][y].config(bg=MAGENTA)
                    self.selected_tile = (x, y)
                    self.show_possible_moves()
                else:
                    self.tiles[a][b].config(bg=self.get_tile_color(a, b))
                    self.selected_tile = (-1, -1)

    def show_possible_moves(self):
        x, y = self.selected_tile
        if self.halma.board[x][y].kind == self.human_player:
            possible_moves = []
            self.halma.get_possible_move(self.selected_tile, possible_moves)
            for p in possible_moves:
                self.tile_labels[p[0]][p[1]].config(fg=TARGET_COLORS[self.human_player])

    def hide_possible_moves(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.halma.board[i][j].kind == 0:
                    self.tile_labels[i][j].config(fg=self.get_tile_color(i, j))
    
    def move(self, point_from, point_to):  # mindahin pawn di game dan di interface
        self.halma.move(point_from, point_to)
        self.tile_labels[point_to[0]][point_to[1]].config(fg=self.tile_labels[point_from[0]][point_from[1]]['fg'])
        self.tile_labels[point_from[0]][point_from[1]].config(fg=self.get_tile_color(point_from[0], point_from[1]))
        self.winner = self.halma.check_winner()
        if self.winner == 1:
            self.var_turn.set("Red wins")
        elif self.winner == 2:
            self.var_turn.set("Green wins")
        else:
            self.timer_start = timer()

            
        self.var_turn.set(TURN_LABEL[1 if self.human_player == 1 else 0])
        self.var_turn_desc.set(TURN_LABEL_DESC[1 if self.mode == GAME_MODE[0] else 2])
        self.label_turn['fg'] = RED if self.human_player == 1 else GREEN

    def move_bot(self, bot_player, using_ls):
        bot_from, bot_to = algoritma.find_next_move(self.halma.get_board_numeric(), bot_player, using_ls)
        self.move(bot_from, bot_to)
        self.var_turn.set(TURN_LABEL[0 if self.human_player == 1 else 1])
        self.var_turn_desc.set(TURN_LABEL_DESC[0])
        self.label_turn['fg'] = RED if self.human_player == 1 else GREEN

    def move_random(self):  # random move human player kalo waktu habis
        random.seed(timer())
        pawns_position = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.halma.board[i][j].kind == self.human_player:
                    pawns_position.append((i, j))
        selected_from = random.choice(pawns_position)
        possible_moves = []
        self.halma.get_possible_move(selected_from, possible_moves)
        selected_to = random.choice(possible_moves)
        self.move(selected_from, selected_to)
    
    def skip_turn(self):
        # move bot   
        using_ls = self.mode == GAME_MODE[1]
        self.move_bot(self.bot_player, using_ls)

    def get_tile_color(self, x, y):  # selang-seling warna tile
        home_info = self.halma.get_home_info(x, y).kind
        if home_info == 1:
            return TILE_COLORS_RED[(x + y) % 2]
        elif home_info == 2:
            return TILE_COLORS_GREEN[(x + y) % 2]
        return TILE_COLORS[(x + y) % 2]

if __name__ == "__main__":
    app = Tk()
    Window = Window(app)
    app.mainloop()
