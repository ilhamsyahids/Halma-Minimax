from tkinter import *
from functools import partial
from tkinter import ttk

import Halma

# CONST
BOARD_SIZE = 16

# COLORS
RED = "#C62828"
GREEN = "#2E7D32"
BLUE_GRAY = "#B0BEC5"
LIGHT_BLUE_GRAY = "#ECEFF1"
DARK_GRAY = "#212121"


class Window(object):

    def __init__(self, master):
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

        self.frame_menu = Frame(self.master)
        self.frame_menu.place(anchor="w", rely=0.5, width=240, height=400)

        # -- MENU --
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
                                        "Minimax Bot vs Human",
                                        "Minimax+LS Bot vs Human",
                                        "Minimax vs Minimax+LS")
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

        self.var_time_limit = IntVar()
        self.var_time_limit.set(30)
        self.scale_time_limit = Scale(self.frame_menu, variable=self.var_time_limit, from_=0, to=120, resolution=5, orient=HORIZONTAL)
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

        self.var_human_player = StringVar()
        self.var_human_player.set(1)
    
        self.radio_human_player_red = Radiobutton(self.frame_human_player, text="Red", value=1, variable=self.var_human_player)
        self.radio_human_player_red.grid(row=0, column=0, sticky="we")
        self.radio_human_player_green = Radiobutton(self.frame_human_player, text="Green", value=2, variable=self.var_human_player)
        self.radio_human_player_green.grid(row=0, column=1, sticky="we")


        ttk.Separator(self.frame_menu, orient=HORIZONTAL).grid(row=i_row, column=0, sticky="we", pady=10)
        i_row += 1
        
        # START GAME
        self.button_start_game = Button(self.frame_menu, text="Start Game", font=("Verdana", 14, "bold"), bg=BLUE_GRAY, command=self.initiate_board)
        self.button_start_game.grid(row=i_row, column=0)

    def initiate_board(self):
        self.board_size = self.var_board_size.get()
        self.mode = self.var_mode.get()
        self.time_limit = self.var_time_limit.get()
        self.human_player = self.var_human_player.get()

        self.halma = Halma.Halma(self.board_size, self.time_limit, self.human_player)

        self.frame_board = Frame(self.master)
        self.frame_board.place(anchor="center", relx=0.5, rely=0.5, width=400, height=400)
        self.frame_board.config(borderwidth=2, relief="solid")
        for i in range(self.board_size):
            self.frame_board.columnconfigure(i, weight=1)
            self.frame_board.rowconfigure(i, weight=1)
        tile_color = (BLUE_GRAY, LIGHT_BLUE_GRAY)
        self.tiles = [[None for i in range(self.board_size)] for i in range(self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                kind = self.halma.board[i][j].kind
                color = RED if kind == Halma.RED else GREEN if kind == Halma.GREEN else "black"
                self.tiles[i][j] = Label(self.frame_board, bg=tile_color[(i + j) % 2], bd=0, fg=color, text=u"\u2B24", font=("Helvetica", int(40-1.6*self.board_size), "bold"), anchor="center")
                self.tiles[i][j].grid(row=i, column=j, sticky="nesw")
                self.tiles[i][j].config(borderwidth=2, relief="flat")
                self.tiles[i][j].bind("<Enter>", partial(self.on_enter_tile, btn=self.tiles[i][j]))
                self.tiles[i][j].bind("<Leave>", partial(self.on_leave_tile, btn=self.tiles[i][j]))
    

    def on_enter_tile(self, e, btn):  # tile button on hover enter event
        btn.config(relief="solid")

    def on_leave_tile(self, e, btn):  # tile button on hover leave event
        btn.config(relief="flat")


app = Tk()
Window = Window(app)
app.mainloop()
