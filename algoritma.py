from math import sqrt
import time

cnt = [0, 0, 0, 0]

def find_next_move(board, player_on_move, using_local_search):
    '''
    input 
    board : array 2 dimensi, yang cell nya bernilai 0/1/2 
    player on move: 1/2

    ouput
    best_move: ((Xawal, Yawal), (Xakhir, Yakhir))
    '''

    _, best_move = minimax(0, float("-inf"), float("inf"), True, player_on_move, board, using_local_search)    
    return best_move 
    
def minimax(depth, alpha, beta, is_max, player_on_move, board, using_local_search=True):
    cnt[depth]+=1
    # basis    
    if (depth==3):
        return utility_function(board, player_on_move), None

    best_val = float("-inf") if is_max else float("inf")
    best_move = None

    len_board = len(board)
    # iterate every possible neighboor
    for i in range(len_board):
        for j in range(len_board):
            if (board[i][j]==player_on_move): # pawn milik player
                list_possible_moves = find_possible_moves(board, player_on_move, i, j, using_local_search)
                
                if (len(list_possible_moves)==0): # pionnya gabisa gerak
                    continue
                
                for move in list_possible_moves:
                    if (move == None):  # jaga jaga misal ada yang move nya none
                        continue

                    # jalanin move nya
                    board[move[0]][move[1]] = player_on_move
                    board[i][j] = 0

                    cnt_in_goal = 0
                    if (player_on_move==1):
                        for k in range(len_board):
                            for l in range(len_board):
                                if (board[k][l]==1 and is_daerah_player(2,k,l,len_board)):
                                    cnt_in_goal+=1
                    else:
                        for k in range(len_board):
                            for l in range(len_board):
                                if (board[k][l]==2 and is_daerah_player(1,k,l,len_board)):
                                    cnt_in_goal+=1

                    if (cnt_in_goal==10):
                        # undo move nya dulu 
                        board[move[0]][move[1]] = 0
                        board[i][j] = player_on_move
                        return 500, ((i, j), (move[0],move[1]))
                    
                    # hitung value minimax
                    val, _ = minimax(depth+1, alpha, beta, not is_max, player_on_move ^ 3, board, using_local_search)

                    # undo movenya
                    board[move[0]][move[1]] = 0
                    board[i][j] = player_on_move

                    if (is_max):
                        if (val > best_val):
                            best_move = ((i, j), (move[0],move[1]))
                            best_val = val
            
                        alpha = max(alpha, best_val)
                    else:
                        if (val < best_val):
                            best_move = ((i, j), (move[0],move[1]))
                            best_val = val

                        beta = min(beta, best_val)
        
                    if (beta <= alpha):
                        return best_val, best_move

    return best_val, best_move

def find_possible_moves(board, player_on_move, i, j, using_local_search=True):
    x = []
    y = []
    if (player_on_move==1): # hanya milih gerakan maju ke arah lawan
        x = [1, 1, 0]
        y = [1, 0, 1]
    else:
        x = [-1, -1, 0]
        y = [-1, 0, -1]

    len_board = len(board)
    list_possible_moves = []
    for k in range(3):
        if (is_coor_valid(i + x[k], j + y[k], len_board)):
            if (board[i + x[k]][j + y[k]]==0):
                list_possible_moves.append((i + x[k], j + y[k]))
            else:    # jika cell depannya ga kosong, coba lompat
                try_to_jump((i,j), board, x, y, list_possible_moves)
                
    if (len(list_possible_moves)==0):
        x = [-1,-1,-1,0,0,0,1,1,1]
        y = [-1,0,1,-1,0,1,-1,0,1]
        for k in range(9):
            if (is_coor_valid(i + x[k], j + y[k], len_board)):
                if (board[i + x[k]][j + y[k]]==0):
                    list_possible_moves.append((i + x[k], j + y[k]))

    if (using_local_search): # kalau pake local search, tiap pawn cuma pilih 1 langkah terbaik (terdekat dengan goal)
        best_move = None
        best_val = float("inf") 
        goal = (len_board-1, len_board-1) if player_on_move==1 else (0, 0)
        for move in list_possible_moves:
            is_move_on_goal = False
            if (player_on_move==1):
                if (is_daerah_player(2,move[0],move[1], len_board)):
                    is_move_on_goal = True
            else:
                if (is_daerah_player(1,move[0],move[1], len_board)):
                    is_move_on_goal = True

            is_move_before_on_goal = False
            if (not (best_move == None)):
                if (player_on_move==1):
                    if (is_daerah_player(2,best_move[0],best_move[1], len_board)):
                        is_move_on_goal = True
                else:
                    if (is_daerah_player(1,best_move[0],best_move[1], len_board)):
                        is_move_on_goal = True

            if (is_move_on_goal and (not (is_move_before_on_goal==None)) and is_move_before_on_goal):
                val = find_distance(move, goal) - 50
                if (val < best_val):
                    best_move = move
                    best_val = val
            elif (is_move_on_goal):
                val = find_distance(move, goal) - 50
                best_move = move
                best_val = val
            elif ((not is_move_on_goal) and (not (is_move_before_on_goal==None)) and (not is_move_before_on_goal)):
                val = find_distance(move, goal)
                if (val < best_val):
                    best_move = move
                    best_val = val
            elif((not is_move_on_goal) and (is_move_before_on_goal==None)):
                val = find_distance(move, goal)
                if (val < best_val):
                    best_move = move
                    best_val = val

        list_possible_moves = [best_move]

    return list_possible_moves

def try_to_jump(pos_now, board, x, y, list_possible_moves):
    len_board = len(board)
    ada_lompatan = False
    for k2 in range(3):
        if ((is_coor_valid(pos_now[0] + x[k2], pos_now[1] + y[k2], len_board)) and (board[pos_now[0] + x[k2]][pos_now[1] + y[k2]]!=0)):
            if ((is_coor_valid(pos_now[0] + 2*x[k2], pos_now[1] + 2*y[k2], len_board)) and (board[pos_now[0] + 2*x[k2]][pos_now[1] + 2*y[k2]]==0)):
                ada_lompatan = True
                list_possible_moves.append((pos_now[0] + 2*x[k2], pos_now[1] + 2*y[k2]))
                
                pos_baru = (pos_now[0] + 2*x[k2], pos_now[1] + 2*y[k2])
                try_to_jump(pos_baru, board, x, y, list_possible_moves)
    
    if(not ada_lompatan):
        return

def is_coor_valid(i, j, len_board):
    return (i >= 0 and i < len_board and j >= 0 and j < len_board)

def utility_function(board, player_on_move):
    len_board = len(board)

    val = 0.0
    cnt1 = 0
    cnt2 = 0
    for i in range(len_board):
        for j in range(len_board):
            if (board[i][j]==1): # pawn player 1
                val += find_distance((i,j), (len_board-1,len_board-1))  
                if (is_daerah_player(2, i, j, len_board)):
                    val -= 50 
                    cnt1 += 1    
            elif (board[i][j]==2): # pawn player 2
                val -= find_distance((i,j), (0,0))
                if (is_daerah_player(1, i, j, len_board)):
                    val += 50
                    cnt2 += 1
    
    

    if (player_on_move==1):
        if (cnt1==10):
            val -= 500
        return val
    else:
        if (cnt2==10):
            val += 500
        return -val

def find_distance(p1, p2):
    return sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))

def is_daerah_player(player, x, y, len_board):
    # asumsi koordinat valid, masuk ke area board
    if (player==1):
        return (x + y <= 3)
    else:
        return (x + y >= 2*(len_board-3)+1 )

if __name__=="__main__":
    # ini buat nyoba aja
    
    board = [[1,1,1,1,0,0,0,0],
             [1,1,1,0,0,0,0,0],
             [1,1,0,0,0,0,0,0],
             [1,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,2],
             [0,0,0,0,0,0,2,2],
             [0,0,0,0,0,2,2,2],
             [0,0,0,0,2,2,2,2]]

    # board = [[2, 2, 0, 2, 0, 0, 0, 0],
    #         [2, 2, 2, 2, 0, 0, 0, 0],
    #         [2, 2, 0, 0, 0, 0, 0, 0],
    #         [2, 0, 0, 0, 0, 0, 1, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 1],
    #         [0, 0, 0, 0, 0, 0, 0, 1],
    #         [0, 0, 0, 0, 0, 1, 1, 1],
    #         [0, 0, 0, 0, 1, 1, 1, 1],]
             
    start_awal = time.time()
    turn = 1
    for i in range(60):
        print(i)
        start = time.time()
        tup = find_next_move(board, turn, using_local_search=True)
        if tup == None:
            break
        print(turn)
        print(tup)
        board[tup[1][0]][tup[1][1]] = turn
        board[tup[0][0]][tup[0][1]] = 0
        turn = turn ^ 3
        print(cnt)
        end = time.time()
        print(end-start)
        for row in board:
            print(row)
    end = time.time()
    print(end-start_awal)

    
