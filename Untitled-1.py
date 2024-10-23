import numpy as np
chess_board = np.array([
        ['black_rook1', 'black_pawn1', '.', '.', '.', '.', 'white_pawn1', 'white_rook1'],
        ['black_knight1', 'black_pawn2', '.', '.', '.', '.', 'white_pawn2', 'white_knight1'],
        ['black_bishop1', 'black_pawn3', '.', '.', '.', '.', 'white_pawn3', 'white_bishop1'],
        ['black_queen', 'black_pawn4', '.', '.', '.', '.', 'white_pawn4', 'white_queen'],
        ['black_king', 'black_pawn5', '.', '.', '.', '.', 'white_pawn5', 'white_king'],
        ['black_bishop2', 'black_pawn6', '.', '.', '.', '.', 'white_pawn6', 'white_bishop2'],
        ['black_knight2', 'black_pawn7', '.', '.', '.', '.', 'white_pawn7', 'white_knight2'],
        ['black_rook2', 'black_pawn8', '.', '.', '.', '.', 'white_pawn8', 'white_rook2']
    ])
a=np.array([1,1])
print(chess_board[a][0])