from math import sqrt

cnt = [0, 0, 0, 0]

def find_next_move(board, player_on_move):
    '''
    input 
    board : array 2 dimensi, yang cell nya bernilai 0/1/2 
    player on move: 1/2

    ouput
    best_move: ((Xawal, Yawal), (Xakhir, Yakhir))
    '''

    best_val, best_move = minimax(0, float("-inf"), float("inf"), True, player_on_move, board)    
    return best_move 
    
def minimax(depth, alpha, beta, is_max, player_on_move, board):
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
                list_possible_moves = find_possible_moves(board, player_on_move, i, j)

                for move in list_possible_moves:
                    # jalanin move nya
                    board[move[0]][move[1]] = player_on_move
                    board[i][j] = 0
                
                    # hitung value minimax
                    val, _ = minimax(depth+1, alpha, beta, not is_max, player_on_move ^ 3, board)

                    # undo movenya
                    board[move[0]][move[1]] = 0
                    board[i][j] = player_on_move

                    if (is_max):
                        if (val > best_val):
                            best_move = ((i, j), (move[0],move[1]))
                            best_val = val
            
                        alpha = max(alpha, best_val); 
                    else:
                        if (val < best_val):
                            best_move = ((i, j), (move[0],move[1]))
                            best_val = val

                        beta = min(beta, best_val); 
        
                    if (beta <= alpha):
                        return best_val, best_move

    return best_val, best_move

def find_possible_moves(board, player_on_move, i, j):
    x = []
    y = []
    if (player_on_move==1): # hanya milih gerakan maju ke arah lawan
        x = [1, 1, 0]
        y = [1, 0, 1]
    else: # kalau player dua milih gerakan ke bawah
        x = [-1, -1, 0]
        y = [-1, 0, -1]

    list_possible_moves = []
    for k in range(3):
        if (is_coor_valid(i + x[k], j + y[k], len(board))):
            if (board[i + x[k]][j + y[k]]==0):
                list_possible_moves.append((i + x[k], j + y[k]))
            else:    # jika cell depannya ga kosong, coba lompat 1 kali
                if (is_coor_valid(i + 2*x[k], j + 2*y[k], len(board))):
                    if (board[i + 2*x[k]][j + 2*y[k]]==0):
                        list_possible_moves.append((i + 2*x[k], j + 2*y[k]))

    return list_possible_moves

def is_coor_valid(i, j, len_board):
    return (i >= 0 and i < len_board and j >= 0 and j < len_board)

def utility_function(board, player_on_move):
    len_board = len(board)

    val = 0.0
    for i in range(len_board):
        for j in range(len_board):
            if (board[i][j]==1): # pawn player 1
                val += find_distance((i,j), (len_board-1,len_board-1))               
            elif (board[i][j]==2): # pawn player 2
                val -= find_distance((i,j), (0,0))

    if (player_on_move==1):
        return val
    else:
        return -val

def find_distance(p1, p2):
    return sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))


if __name__=="__main__":
    board = [[1,1,1,1,0,0,0,0],
             [1,1,1,0,0,0,0,0],
             [1,1,0,0,0,0,0,0],
             [1,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,2],
             [0,0,0,0,0,0,2,2],
             [1,0,0,0,0,2,2,2],
             [1,0,0,0,2,2,2,2]]

    print(find_next_move(board, 2))
    print(cnt)



# ganti coor di utility function, sama di move