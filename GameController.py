import pygame
import numpy as np
from ChessBoard import ChessBoard
from ChessPiece import ChessPiece,is_piece_in_check  # Import your piece class
from ChessData import ChessData
import random


class GameController:
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen_width = 800
        self.screen_height = 620
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Chess Game")  # Adds a title to the window
        self.clock = pygame.time.Clock()
        self.chessboard = ChessBoard("Assets/Board.png")
        self.chessboard.draw(self.screen)
        self.running = True
        self.pause = False
        self.game_over = False
        self.game_start_sound=pygame.mixer.Sound("Assets/game_start.mp3")
        self.piece_capture_sound=pygame.mixer.Sound("Assets/capture.mp3")
        self.piece_move_sound=pygame.mixer.Sound("Assets/move.mp3")
        self.check_mate_sound=pygame.mixer.Sound("Assets/game over checkmate.mp3")
        self.castling_sound=pygame.mixer.Sound("Assets/castling.mp3")
        self.promotion_sound=pygame.mixer.Sound("Assets/promotion.mp3")
        self.menu_over = False
        self.singleplayer = False
        self.choose_difficulty = False
        self.bot = None
        

        
        
    def initialize_pieces(self):

        for pieces in self.chessboard.piece_dict.copy():
            self.chessboard.remove_piece(pieces)
        # Add pawns
        for i in range(8):
            self.chessboard.add_piece(ChessPiece(f"white_pawn{i + 1}", "white", "Assets/PawnWhite.png", [i * 100 + 20, 472.5], self.screen))
            self.chessboard.add_piece(ChessPiece(f"black_pawn{i + 1}", "black", "Assets/PawnBlack.png", [i * 100 + 20, 85], self.screen))

        # Add other pieces
        self.chessboard.add_piece(ChessPiece("white_rook1", "white", "Assets/RookWhite.png", [20, 550], self.screen))
        self.chessboard.add_piece(ChessPiece("white_rook2", "white", "Assets/RookWhite.png", [720, 550], self.screen))

        self.chessboard.add_piece(ChessPiece("white_bishop1", "white", "Assets/BishopWhite.png", [220, 550], self.screen))
        self.chessboard.add_piece(ChessPiece("white_bishop2", "white", "Assets/BishopWhite.png", [520, 550], self.screen))

        self.chessboard.add_piece(ChessPiece("white_king", "white", "Assets/KingWhite.png", [420, 550], self.screen))
        self.chessboard.add_piece(ChessPiece("white_queen1", "white", "Assets/QueenWhite.png", [320, 550], self.screen))

        self.chessboard.add_piece(ChessPiece("white_knight1", "white", "Assets/KnightWhite.png", [120, 550], self.screen))
        self.chessboard.add_piece(ChessPiece("white_knight2", "white", "Assets/KnightWhite.png", [620, 550], self.screen))

        self.chessboard.add_piece(ChessPiece("black_rook1", "black", "Assets/RookBlack.png", [20,7.5], self.screen))
        self.chessboard.add_piece(ChessPiece("black_rook2", "black", "Assets/RookBlack.png", [720, 7.5], self.screen))

        self.chessboard.add_piece(ChessPiece("black_bishop1", "black", "Assets/BishopBlack.png", [220, 7.5], self.screen))
        self.chessboard.add_piece(ChessPiece("black_bishop2", "black", "Assets/BishopBlack.png", [520, 7.5], self.screen))

        self.chessboard.add_piece(ChessPiece("black_king", "black", "Assets/KingBlack.png", [420, 7.5], self.screen))
        self.chessboard.add_piece(ChessPiece("black_queen1", "black", "Assets/QueenBlack.png", [320, 7.5], self.screen))

        self.chessboard.add_piece(ChessPiece("black_knight1", "black", "Assets/KnightBlack.png", [120, 7.5], self.screen))
        self.chessboard.add_piece(ChessPiece("black_knight2", "black", "Assets/KnightBlack.png", [620, 7.5], self.screen))
        
        self.game_start_sound.play()
    def run(self):
        while self.running:
            current_event = None
            if not ChessData.get_game():
                self.check_mate_sound.play()
                self.menu_over = False
                break
            self.handle_bot_move()
            for event in pygame.event.get():
                current_event = event
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Handle events for each piece
                for piece in self.chessboard.pieces:
                    piece.handle_event(event)

            if ChessData.get_move_sound() and not ChessData.get_castling_side():
                self.piece_move_sound.play()
                ChessData.update_move_sound(False)
            for piece in self.chessboard.pieces:
                piece.update()
            
            self.handle_castling()
            self.handle_removed_pieces()

            # Update pieces
            for piece in self.chessboard.pieces:
                piece.update()

            self.screen.fill((255, 255, 255))  # Fill screen with white
            self.chessboard.draw(self.screen)  # Draw the chessboard and pieces
            self.handle_promotion()

            # Show possible moves for all pieces (if any)
            for piece in self.chessboard.pieces:
                piece.show_possible_moves(current_event)

            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 frames per second

    def handle_bot_move(self):
        if ChessData.get_bot() == "easy" and ChessData.get_chess_turn() == 'black':
            if easy_bot_algorithm(3) is None:
                    ChessData.game_over()
                    print('game over')
            else:
                moves, piece = easy_bot_algorithm(3)
                self.update_board_for_bot_move(moves, piece)

    def update_board_for_bot_move(self, moves, piece):
        new_x, new_y = map(int, moves)
        ChessData.update_active_piece(piece)
        ChessData.update_bot_move(moves, piece)
        self.updated_flag = True
        piece_position = ChessData.get_chess_board()
        old_x, old_y = np.argwhere(piece_position == ChessData.get_active_piece())[0]
        self.capture_piece_if_needed(new_x, new_y)
        self.handle_castling_for_king(new_x, new_y, piece_position)
        piece_position[old_x][old_y] = "."
        piece_position[new_x][new_y] = ChessData.get_active_piece()
        ChessData.update_chess_board(piece_position)
        ChessData.update_chess_turn()
        ChessData.update_has_piece_moved(ChessData.get_active_piece())
        ChessData.update_active_piece("")
        self.update_chessboard_pieces(moves, piece)

    def capture_piece_if_needed(self, new_x, new_y):
        if ChessData.get_chess_board()[new_x][new_y] != ".":
            captured_piece = ChessData.get_chess_board()[new_x][new_y]
            ChessData.update_removed_piece(captured_piece)
        else:
            ChessData.update_move_sound(True)

    def handle_castling_for_king(self, new_x, new_y, piece_position):
        if 'king' in ChessData.get_active_piece():
            if new_x == 6 and ChessPiece.is_right_castling_availabe():
                piece_position[5][new_y] = ChessData.get_chess_turn() + "_rook2"
                piece_position[7][new_y] = "."
                ChessData.update_get_castling_side("right")
            if new_x == 2 and ChessPiece.is_left_castling_available():
                piece_position[3][new_y] = ChessData.get_chess_turn() + "_rook1"
                piece_position[0][new_y] = "."
                ChessData.update_get_castling_side("left")

    def update_chessboard_pieces(self, moves, piece):
        piece_type = piece[6:-1].capitalize() + piece[:5].capitalize()
        if 'king' in piece:
            piece_type = piece[6:].capitalize() + piece[:5].capitalize()
        self.chessboard.remove_piece(piece)
        x, y = map(int, moves)
        piece_two = ChessData.get_chess_board()[x][y]
        self.chessboard.remove_piece(piece_two)
        self.chessboard.add_piece(ChessPiece(piece, piece[:5], f"Assets/{piece_type}.png", [x * 100 + 20, 7.5 + y * 77.5], self.screen))
        ChessData.update_bot_move([], "")

    def handle_castling(self):
        if ChessData.get_castling_side() in ["left", "right"]:
            color = "white" if ChessData.get_chess_turn() == "black" else "black"
            rook = f"{color}_rook1" if ChessData.get_castling_side() == "left" else f"{color}_rook2"
            self.chessboard.remove_piece(rook)
            y = 7.5 if color == "black" else 550
            x = 320 if ChessData.get_castling_side() == "left" else 520
            self.chessboard.add_piece(ChessPiece(rook, color, f"Assets/Rook{color.capitalize()}.png", [x, y], self.screen))
            ChessData.update_get_castling_side("")
            self.castling_sound.play()

    def handle_removed_pieces(self):
        if ChessData.get_removed_piece():
            for removed_piece in ChessData.get_removed_piece():
                self.chessboard.remove_piece(removed_piece)
                print(f'{removed_piece} is removed')
            self.piece_capture_sound.play()
            ChessData.update_removed_piece("")
            ChessData.update_active_piece("")

    def handle_promotion(self):
        if ChessData.get_promotion_piece():
            self.menu_over = False
            while not self.menu_over:
                pygame.display.flip()
                self.display_promotion_menu()
                location, piece = ChessData.get_promotion_piece()
                x, y = map(int, location)
                x, y = x * 100 + 20, y * 77.5 + 7.5
                color = 'white' if ChessData.get_chess_turn() == 'black' else 'black'
                if ChessData.get_bot():
                    color = 'white' if color == 'black' else 'white'
                self.chessboard.remove_piece(piece)
                promoted_piece_name = None
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.menu_over = True
                        self.game_over = True
                        self.running = False
                        pygame.mixer.stop()
                        pygame.mixer.quit()
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        promoted_piece_name = self.check_promotion_selection(mouse_pos, color, x, y)
                if promoted_piece_name:
                    self.promotion_sound.play()
                    temp_chessboard = ChessData.get_chess_board().copy()
                    temp_chessboard[int((x - 20) / 100)][int((y - 7.5) / 77.5)] = promoted_piece_name
                    ChessData.update_chess_board(temp_chessboard)

    def display_promotion_menu(self):
        main_menu = pygame.image.load("Assets/wooden_board.png").convert_alpha()
        main_menu = pygame.transform.scale(main_menu, (300, 380))
        self.screen.blit(main_menu, (270, 162.5))
        font = pygame.font.Font(None, 40)
        winner_text = "Promotion: "
        game_over_text = font.render(winner_text, True, (0, 0, 0))
        self.screen.blit(game_over_text, (345, 200))
        self.chessboard.display_sub_menu(self.screen, image_path="Assets/Asset 9@4x.png", text="Queen", size=(150, 50), position=(345, 240))
        self.chessboard.display_sub_menu(self.screen, image_path="Assets/Asset 9@4x.png", text="Rook", size=(150, 50), position=(345, 305))
        self.chessboard.display_sub_menu(self.screen, image_path="Assets/Asset 9@4x.png", text="Bishop", size=(150, 50), position=(345, 370))
        self.chessboard.display_sub_menu(self.screen, image_path="Assets/Asset 9@4x.png", text="Knight", size=(150, 50), position=(345, 435))

    def check_promotion_selection(self, mouse_pos, color, x, y):
        promoted_piece_name = None
        if 345 <= mouse_pos[0] <= 495:
            if 220 <= mouse_pos[1] <= 290:
                self.menu_over = True
                ChessData.update_promotion_piece(None, '')
                promoted_piece_name = self.promote_piece(color, "queen", x, y)
            elif 305 <= mouse_pos[1] <= 355:
                self.menu_over = True
                ChessData.update_promotion_piece(None, '')
                promoted_piece_name = self.promote_piece(color, "rook", x, y)
            elif 370 <= mouse_pos[1] <= 420:
                self.menu_over = True
                ChessData.update_promotion_piece(None, '')
                promoted_piece_name = self.promote_piece(color, "bishop", x, y)
            elif 435 <= mouse_pos[1] <= 485:
                self.menu_over = True
                ChessData.update_promotion_piece(None, '')
                promoted_piece_name = self.promote_piece(color, "knight", x, y)
        return promoted_piece_name

    def promote_piece(self, color, piece_type, x, y):
        count_attr = f"{piece_type}_count"
        try:
            count = getattr(self, count_attr)
            setattr(self, count_attr, count + 1)
        except AttributeError:
            setattr(self, count_attr, 1)
        finally:
            count = getattr(self, count_attr)
            promoted_piece_name = f"{color}_{piece_type}{count}"
            self.chessboard.add_piece(ChessPiece(promoted_piece_name, color, f"Assets/{piece_type.capitalize()}{color.capitalize()}.png", [x, y], self.screen))
        return promoted_piece_name  # Limit to 60 frames per second
        
        
    def game_over_menu(self):
        while(not self.menu_over):
            pygame.display.flip()
            game_over_menu = pygame.image.load("Assets/wooden_board.png").convert_alpha()  # Use your own marker image here
            game_over_menu = pygame.transform.scale(game_over_menu, (300, 310)) 
            self.screen.blit(game_over_menu, (270, 162.5))
            font = pygame.font.Font(None, 40)  # Use default font and set size
            winner_text = "Black Wins!" if ChessData.get_chess_turn() == "white" else "White Wins!"
            game_over_text = font.render(winner_text, True, (0, 0, 0))  # Black text
            self.screen.blit(game_over_text, (335, 200))
            self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Restart",size=(150, 50),position=(345, 240))
            self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Main Menu",size=(150, 50),position=(345, 305))
            self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Quit",size=(150, 50),position=(345, 370))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = False
                    self.running = False 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
            
            # Check if the mouse is over the submenu
                    if (345 <= mouse_pos[0] <= 345 + 150 and 220 <= mouse_pos[1] <= 240 + 50):  # Change these values based on your submenu position and size
                        self.running = True
                        ChessData.new_game()
                        ChessData.board_reset()
                        self.menu_over=True

                    elif (345 <= mouse_pos[0] <= 345 + 150 and 350 <= mouse_pos[1] <= 370 + 50):
                        self.menu_over=True
                        self.game_over = True  # Exit game over state
                        self.running = False  # Stop the main loop
                        pygame.mixer.stop()  # Stop all sounds
                        pygame.mixer.quit()  # Quit the mixer
                        pygame.quit()  # Quit Pygame

    def menu(self):
        while(not self.menu_over):
            pygame.display.flip()
            main_menu = pygame.image.load("Assets/wooden_board.png").convert_alpha()  # Use your own marker image here
            main_menu = pygame.transform.scale(main_menu, (300, 310)) 
            self.screen.blit(main_menu, (270, 162.5))
            font = pygame.font.Font(None, 40)  # Use default font and set size
            winner_text = "Main Menu" 
            game_over_text = font.render(winner_text, True, (0, 0, 0))  # Black text
            self.screen.blit(game_over_text, (345, 200))
            self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Singleplayer",size=(150, 50),position=(345, 240))
            self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Multiplayer",size=(150, 50),position=(345, 305))
            self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Quit",size=(150, 50),position=(345, 370))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = False
                    self.running = False 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
            
            # Check if the mouse is over the submenu
                    if (345 <= mouse_pos[0] <= 345 + 150 and 220 <= mouse_pos[1] <= 240 + 50):  # Change these values based on your submenu position and size
                        self.running = True
                        ChessData.new_game()
                        self.menu_over=True
                        self.singleplayer=True
                        self.choose_difficulty = True

                    if (345 <= mouse_pos[0] <= 345 + 150 and 305 <= mouse_pos[1] <= 305 + 50):  # Change these values based on your submenu position and size
                        self.running = True
                        ChessData.new_game()
                        self.menu_over=True
                        self.singleplayer=False
                        

                    elif (345 <= mouse_pos[0] <= 345 + 150 and 350 <= mouse_pos[1] <= 370 + 50):
                        self.menu_over=True
                        self.game_over = True  # Exit game over state
                        self.running = False  # Stop the main loop
                        pygame.mixer.stop()  # Stop all sounds
                        pygame.mixer.quit()  # Quit the mixer
                        pygame.quit()  # Quit Pygame

    def choose_difficulty_menu(self):
        self.menu_over=False
        while(not self.menu_over):
            pygame.display.flip()
            main_menu = pygame.image.load("Assets/wooden_board.png").convert_alpha()  # Use your own marker image here
            main_menu = pygame.transform.scale(main_menu, (300, 310)) 
            self.screen.blit(main_menu, (270, 162.5))
            font = pygame.font.Font(None, 40)  # Use default font and set size
            winner_text = "Single Player" 
            game_over_text = font.render(winner_text, True, (0, 0, 0))  # Black text
            self.screen.blit(game_over_text, (345, 200))
            self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Easy Bot",size=(150, 50),position=(345, 240))
            self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Medium Bot",size=(150, 50),position=(345, 305))
            self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Hard Bot",size=(150, 50),position=(345, 370))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = False
                    self.running = False 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
            
            # Check if the mouse is over the submenu
                    if (345 <= mouse_pos[0] <= 345 + 150 and 220 <= mouse_pos[1] <= 240 + 50):  # Change these values based on your submenu position and size
                        self.running = True
                        ChessData.new_game()
                        ChessData.board_reset()
                        self.menu_over=True
                        ChessData.update_bot_level("easy")

                    elif (345 <= mouse_pos[0] <= 345 + 150 and 350 <= mouse_pos[1] <= 370 + 50):
                        self.menu_over=True
                        self.game_over = True  # Exit game over state
                        self.running = False  # Stop the main loop
                        pygame.mixer.stop()  # Stop all sounds
                        pygame.mixer.quit()  # Quit the mixer
                        pygame.quit()  # Quit Pygame                   



def minmax_algorithm(chessboard, depth, is_maximizing_player, alpha, beta):
    if depth == 0 or not ChessData.get_game():
        return evaluate_board(chessboard)

    color = "black" if is_maximizing_player else "white"
    pieces_positions = {
        (x, y): chessboard[x, y]
        for x, y in zip(*np.where(chessboard != "."))
        if color in str(chessboard[x, y])
    }

    if is_maximizing_player:
        max_eval = float('-inf')
        for (old_x, old_y), piece in pieces_positions.items():
            possible_moves = get_moves(ChessPiece.get_possible_moves(piece, chessboard), piece)
            for new_x, new_y in possible_moves:
                new_x, new_y = int(new_x), int(new_y)
                original_target = chessboard[new_x, new_y]
                chessboard[new_x, new_y], chessboard[old_x, old_y] = piece, "."
                eval = minmax_algorithm(chessboard, depth - 1, False, alpha, beta)
                chessboard[new_x, new_y], chessboard[old_x, old_y] = original_target, piece
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for (old_x, old_y), piece in pieces_positions.items():
            possible_moves = get_moves(ChessPiece.get_possible_moves(piece, chessboard), piece)
            for new_x, new_y in possible_moves:
                new_x, new_y = int(new_x), int(new_y)
                original_target = chessboard[new_x, new_y]
                chessboard[new_x, new_y], chessboard[old_x, old_y] = piece, "."
                eval = minmax_algorithm(chessboard, depth - 1, True, alpha, beta)
                chessboard[new_x, new_y], chessboard[old_x, old_y] = original_target, piece
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def evaluate_board(chessboard):
    piece_values = {
        "king": 1000,
        "queen": 9,
        "rook": 5,
        "bishop": 3,
        "knight": 3,
        "pawn": 1
    }
    evaluation = 0
    for x in range(8):
        for y in range(8):
            piece = chessboard[x, y]
            if piece != ".":
                value = next((v for k, v in piece_values.items() if k in piece), 0)
                evaluation += value if "white" in piece else -value
    return evaluation

def easy_bot_algorithm(depth):
    chessboard = ChessData.get_chess_board()
    best_move = None
    best_value = float('-inf')
    color = "black"
    pieces_positions = {
        (x, y): chessboard[x, y]
        for x, y in zip(*np.where(chessboard != "."))
        if color in str(chessboard[x, y])
    }

    positive_moves = []

    for (old_x, old_y), piece in pieces_positions.items():
        possible_moves = get_moves(ChessPiece.get_possible_moves(piece, chessboard), piece)
        for new_x, new_y in possible_moves:
            new_x, new_y = int(new_x), int(new_y)
            original_target = chessboard[new_x, new_y]
            chessboard[new_x, new_y], chessboard[old_x, old_y] = piece, "."
            move_value = minmax_algorithm(chessboard, depth - 1, False, float('-inf'), float('inf'))
            chessboard[new_x, new_y], chessboard[old_x, old_y] = original_target, piece
            if move_value > 0:
                positive_moves.append(((new_x, new_y), piece, move_value))
            if move_value > best_value:
                best_value = move_value
                best_move = ((new_x, new_y), piece)

    if positive_moves:
        best_move = random.choice(positive_moves)[:2]

    return best_move if best_move else None

def get_moves(possible_moves, piece):
    removed_king_in_check = []
    current_chessboard = ChessData.get_chess_board()
    old_x, old_y = np.argwhere(current_chessboard == piece)[0]

    for moves in possible_moves:
        new_x, new_y = map(int, moves)
        original_target = current_chessboard[new_x][new_y]
        original_source = current_chessboard[old_x][old_y]
        current_chessboard[new_x][new_y] = piece
        current_chessboard[old_x][old_y] = "."

        king_location = np.argwhere(current_chessboard == (ChessData.get_chess_turn() + "_king"))[0]
        if not is_piece_in_check(ChessData.get_chess_turn(), current_chessboard, king_location):
            removed_king_in_check.append((new_x, new_y))

        current_chessboard[new_x][new_y] = original_target
        current_chessboard[old_x][old_y] = original_source

    outline_moves = removed_king_in_check
    king_location = np.argwhere(ChessData.get_chess_board() == (ChessData.get_chess_turn() + "_king"))[0]
    if piece == ChessData.get_chess_turn() + "_king" and not ChessData.get_has_piece_moved(piece) and not is_piece_in_check(ChessData.get_chess_turn(), ChessData.get_chess_board(), king_location):
        y = 7 if ChessData.get_chess_turn() == "white" else 0
        if ChessPiece.is_right_castling_available() and ChessData.get_chess_board()[5][y] == "." and ChessData.get_chess_board()[6][y] == ".":
            outline_moves.append((6, y))
        if ChessPiece.is_left_castling_available() and ChessData.get_chess_board()[3][y] == "." and ChessData.get_chess_board()[2][y] == "." and ChessData.get_chess_board()[1][y] == ".":
            outline_moves.append((2, y))

    return outline_moves
