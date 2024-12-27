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
            current_event=None
            if not ChessData.get_game():
                self.check_mate_sound.play()
                self.menu_over=False
                break

            for event in pygame.event.get():
                current_event=event
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Handle events for each piece
                for piece in self.chessboard.pieces:
                    piece.handle_event(event)

            if ChessData.get_move_sound() and not ChessData.get_castling_side():
                self.piece_move_sound.play()
                ChessData.update_move_sound(False)

            
                
            if ChessData.get_bot()=="easy" and ChessData.get_chess_turn()=='black':
                if easy_bot_algorithm(1) is None:
                    ChessData.game_over()
                    
                else:
                    moves,piece = easy_bot_algorithm(1)
                    new_x,new_y=moves
                    new_x,new_y=int(new_x),int(new_y)
                    ChessData.update_active_piece(piece)
                    ChessData.update_bot_move(moves,piece)
                    self.updated_flag=True
                    piece_position=ChessData.get_chess_board()
                    old_x,old_y=np.argwhere(ChessData.get_chess_board()==ChessData.get_active_piece())[0]
                    if ChessData.get_chess_board()[new_x][new_y] != ".":  # If there is a piece in the target square
                        captured_piece = ChessData.get_chess_board()[new_x][new_y]  # Get the captured piece
                        ChessData.update_removed_piece(captured_piece)  # Update removed pieces list
                    else:
                        ChessData.update_move_sound(True)
                            
                    if ('king' in ChessData.get_active_piece()):
                        if(new_x==6 and ChessPiece.is_right_castling_availabe()):
                            piece_position[5][new_y]=ChessData.get_chess_turn()+"_rook2"
                            piece_position[7][new_y]="."
                            ChessData.update_get_castling_side("right")
                        if(new_x==2 and ChessPiece.is_left_castling_availabe()):
                            piece_position[3][new_y]=ChessData.get_chess_turn()+"_rook1"
                            piece_position[0][new_y]="."
                            ChessData.update_get_castling_side("left")
                    piece_position[old_x][old_y]="."
                    piece_position[new_x][new_y]=ChessData.get_active_piece()   
                    ChessData.update_chess_board(piece_position)
                    ChessData.update_chess_turn()
                    ChessData.update_has_piece_moved(ChessData.get_active_piece())
                    ChessData.update_active_piece("")

                    piece_type = piece[6:-1].capitalize() + piece[:5].capitalize()
                    if 'king' in piece:
                        piece_type = piece[6:].capitalize() + piece[:5].capitalize()
                    self.chessboard.remove_piece(piece)
                    x,y = moves
                    x,y= int(x),int(y)
                    piece_two = ChessData.get_chess_board()[x][y]
                    self.chessboard.remove_piece(piece_two)
                    self.chessboard.add_piece(ChessPiece(piece, piece[:5], f"Assets/{piece_type}.png", [x*100+20, 7.5+y*77.5], self.screen))
                    ChessData.update_bot_move([],"")



            

            if ChessData.get_castling_side()=="left":
                color="white"
                if ChessData.get_chess_turn()=="white":
                    color="black"
                self.chessboard.remove_piece(f"{color}_rook1")
                y=7.5
                if color=="white":
                    y=550
                self.chessboard.add_piece(ChessPiece(f"{color}_rook1", color, f"Assets/Rook{color.capitalize()}.png", [320,y], self.screen))
                ChessData.update_get_castling_side("")
                self.castling_sound.play()
            
            elif ChessData.get_castling_side()=="right":
                color="white"
                if ChessData.get_chess_turn()=="white":
                    color="black"
                self.chessboard.remove_piece(f"{color}_rook2")
                y=7.5
                if color=="white":
                    y=550
                self.chessboard.add_piece(ChessPiece(f"{color}_rook2", color, f"Assets/Rook{color.capitalize()}.png", [520,y], self.screen))
                ChessData.update_get_castling_side("")
                self.castling_sound.play()


            if ChessData.get_removed_piece():
                for removed_piece in ChessData.get_removed_piece():
                    self.chessboard.remove_piece(removed_piece)
                    print(f'{removed_piece} is removed')
                self.piece_capture_sound.play()
                ChessData.update_removed_piece("")
                ChessData.update_active_piece("")

            
                

                
            # Update pieces
            for piece in self.chessboard.pieces:
                piece.update()
            
               

            self.screen.fill((255, 255, 255))  # Fill screen with white
            self.chessboard.draw(self.screen)  # Draw the chessboard and pieces
            
            if ChessData.get_promotion_piece():
                
                self.menu_over = False
                while(not self.menu_over):
                   
                    pygame.display.flip()
                    main_menu = pygame.image.load("Assets/wooden_board.png").convert_alpha()  # Use your own marker image here
                    main_menu = pygame.transform.scale(main_menu, (300, 380)) 
                    self.screen.blit(main_menu, (270, 162.5))
                    font = pygame.font.Font(None, 40)  # Use default font and set size
                    winner_text = "Promotion: " 
                    game_over_text = font.render(winner_text, True, (0, 0, 0))  # Black text
                    self.screen.blit(game_over_text, (345, 200))
                    self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Queen",size=(150, 50),position=(345, 240))
                    self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Rook",size=(150, 50),position=(345, 305))
                    self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Bishop",size=(150, 50),position=(345, 370))
                    self.chessboard.display_sub_menu(self.screen,image_path="Assets/Asset 9@4x.png",text="Knight",size=(150, 50),position=(345, 435))
                    location, piece = ChessData.get_promotion_piece()
                    x , y = location
                    x , y= int(x)*100+20, int(y)*77.5+7.5
                    color = 'white' if ChessData.get_chess_turn()=='black' else 'black'
                    if ChessData.get_bot():
                        color = 'white' if color == 'black' else 'white'
                    self.chessboard.remove_piece(piece)
                    promoted_piece_name = None
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.game_over = False
                            self.running = False 
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position

                    # Check if the mouse is over the submenu
                            if (345 <= mouse_pos[0] <= 345 + 150 and 220 <= mouse_pos[1] <= 240 + 50):  # Change these values based on your submenu position and size
                                self.menu_over=True
                                ChessData.update_promotion_piece(None,'')
                                try:
                                    self.queen_count+=1
                                except:
                                    self.queen_count=2
                                finally:
                                    promoted_piece_name = f"{color}_queen{self.queen_count}"
                                    self.chessboard.add_piece(ChessPiece(f"{color}_queen{self.queen_count}", color, f"Assets/Queen{color.capitalize()}.png", [x, y], self.screen))    


                            elif (345 <= mouse_pos[0] <= 345 + 150 and 305 <= mouse_pos[1] <= 305 + 50):  # Change these values based on your submenu position and size
                                self.menu_over=True
                                ChessData.update_promotion_piece(None,'')
                                try:
                                    self.rook_count+=1
                                except:
                                    self.rook_count=3
                                finally:
                                    promoted_piece_name = f"{color}_rook{self.rook_count}"
                                    self.chessboard.add_piece(ChessPiece(f"{color}_rook{self.rook_count}", color, f"Assets/Rook{color.capitalize()}.png", [x, y], self.screen)) 

                            elif (345 <= mouse_pos[0] <= 345 + 150 and 350 <= mouse_pos[1] <= 370 + 50):
                                self.menu_over=True
                                ChessData.update_promotion_piece(None,'')
                                try:
                                    self.bishop_count+=1
                                except:
                                    self.bishop_count=3
                                finally:
                                    promoted_piece_name = f"{color}_bishop{self.bishop_count}"
                                    self.chessboard.add_piece(ChessPiece(f"{color}_bishop{self.bishop_count}", color, f"Assets/Bishop{color.capitalize()}.png", [x, y], self.screen)) 

                            elif (345 <= mouse_pos[0] <= 345 + 150 and 350 <= mouse_pos[1] <= 435 + 50):
                                self.menu_over=True
                                ChessData.update_promotion_piece(None,'')
                                try:
                                    self.knight_count+=1
                                except:
                                    self.knight_count=3
                                finally:
                                    promoted_piece_name = f"{color}_knight{self.knight_count}"
                                    self.chessboard.add_piece(ChessPiece(f"{color}_knight{self.knight_count}", color, f"Assets/Knight{color.capitalize()}.png", [x, y], self.screen)) 
                self.promotion_sound.play()
                temp_chessboard = ChessData.get_chess_board().copy()
                temp_chessboard[int((x-20)/100)][int((y-7.5)/77.5)]=promoted_piece_name
                ChessData.update_chess_board(temp_chessboard) 

            # Show possible moves for all pieces (if any)
            for piece in self.chessboard.pieces:
                piece.show_possible_moves(current_event)

            

            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 frames per second
        
        
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

import numpy as np
import random

def easy_bot_algorithm(depth):
    chessboard = ChessData.get_chess_board()
    valid_moves = []
    
    color = "black" if depth % 2 ==1 else "white" 
    # Cache positions of all black pieces
    pieces_positions = {
        (x, y): chessboard[x, y]
        for x, y in zip(*np.where(chessboard != "."))
        if color in str(chessboard[x, y])
    }

    # Pre-define piece merits
    piece_merits = {
        "queen": 9,
        "rook": 5,
        "knight": 3,
        "bishop": 3,
        "pawn": 1
    }

    # Find the black king's position
    
    king_location = tuple(np.argwhere(chessboard == f"{color}_king")[0])

    
    # Iterate through each black piece
    for (old_x, old_y), piece in pieces_positions.items():
        possible_moves = ChessPiece.get_possible_moves(piece, chessboard)
        removed_king_in_check=np.empty((0,2))
            # Get the current chessboard state
        current_chessboard = ChessData.get_chess_board()

            # Initialize the array to store valid moves
        removed_king_in_check = np.empty((0, 2))

            # Get the position of the active piece
        old_x, old_y = np.argwhere(current_chessboard == piece)[0]

            # Removing future checks
        for moves in possible_moves:  
            new_x, new_y = moves
            new_x, new_y = int(new_x), int(new_y)
            original_target = current_chessboard[new_x][new_y]  
            original_source = current_chessboard[old_x][old_y] 
            current_chessboard[new_x][new_y] = piece
            current_chessboard[old_x][old_y] = "."
            if (np.argwhere(current_chessboard == f"{color}_king").size ==0):
                print(current_chessboard)
            king_location = np.argwhere(current_chessboard == f"{color}_king")[0]
            if not is_piece_in_check(ChessData.get_chess_turn(), current_chessboard, king_location):
                removed_king_in_check = np.append(removed_king_in_check, [[new_x, new_y]], axis=0)
            current_chessboard[new_x][new_y] = original_target
            current_chessboard[old_x][old_y] = original_source

        # Finding moves
        for new_x, new_y in removed_king_in_check:
            new_x, new_y = int(new_x), int(new_y)
            target_square = chessboard[new_x, new_y]
            if color in str(target_square):
                continue
            merit = next(
                (value for key, value in piece_merits.items() if key in str(target_square)),0
            )
            original_target = chessboard[new_x, new_y]
            chessboard[new_x, new_y], chessboard[old_x, old_y] = piece, "."
            if not is_piece_in_check(color, chessboard, king_location):
                valid_moves.append(((new_x, new_y), piece, merit))
            chessboard[new_x, new_y], chessboard[old_x, old_y] = original_target, piece

    # Sort valid moves by merit and pick one
    if valid_moves:
        valid_moves.sort(key=lambda x: x[2], reverse=True)
        highest_merit = valid_moves[0][2]
        top_moves = [move for move in valid_moves if move[2] == highest_merit]
        selected_move = random.choice(top_moves)
        return selected_move[0],selected_move[1]

    # If no valid moves are found
    return None
