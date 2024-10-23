import pygame
import numpy as np
from ChessBoard import ChessBoard
from ChessPiece import ChessPiece  # Import your piece class
from ChessData import ChessData



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
        self.running = True
        self.game_start_sound=pygame.mixer.Sound("Assets/game_start.mp3")
        self.piece_capture_sound=pygame.mixer.Sound("Assets/capture.mp3")
        self.piece_move_sound=pygame.mixer.Sound("Assets/move.mp3")
        self.initialize_pieces()  # Initializes the chess pieces
        
        
    def initialize_pieces(self):
        # Add pawns
        for i in range(8):
            self.chessboard.add_piece(ChessPiece(f"white_pawn{i + 1}", "white", "Assets/PawnWhite.png", [i * 100 + 20, 472.5], self.screen))
            self.chessboard.add_piece(ChessPiece(f"black_pawn{i + 1}", "black", "Assets/PawnBlack.png", [i * 100 + 20, 85], self.screen))

        # Add other pieces
        self.chessboard.add_piece(ChessPiece("white_rook1", "white", "Assets/RookWhite.png", [20, 550], self.screen))
        self.chessboard.add_piece(ChessPiece("white_rook2", "white", "Assets/RookWhite.png", [720, 550], self.screen))

        self.chessboard.add_piece(ChessPiece("white_bishop1", "white", "Assets/BishopWhite.png", [220, 550], self.screen))
        self.chessboard.add_piece(ChessPiece("white_bishop2", "white", "Assets/BishopWhite.png", [520, 550], self.screen))

        self.chessboard.add_piece(ChessPiece("white_king", "white", "Assets/KingWhite.png", [320, 550], self.screen))
        self.chessboard.add_piece(ChessPiece("white_queen", "white", "Assets/QueenWhite.png", [420, 550], self.screen))

        self.chessboard.add_piece(ChessPiece("white_knight1", "white", "Assets/KnightWhite.png", [120, 550], self.screen))
        self.chessboard.add_piece(ChessPiece("white_knight2", "white", "Assets/KnightWhite.png", [620, 550], self.screen))

        self.chessboard.add_piece(ChessPiece("black_rook1", "black", "Assets/RookBlack.png", [20,7.5], self.screen))
        self.chessboard.add_piece(ChessPiece("black_rook2", "black", "Assets/RookBlack.png", [720, 7.5], self.screen))

        self.chessboard.add_piece(ChessPiece("black_bishop1", "black", "Assets/BishopBlack.png", [220, 7.5], self.screen))
        self.chessboard.add_piece(ChessPiece("black_bishop2", "black", "Assets/BishopBlack.png", [520, 7.5], self.screen))

        self.chessboard.add_piece(ChessPiece("black_king", "black", "Assets/KingBlack.png", [320, 7.5], self.screen))
        self.chessboard.add_piece(ChessPiece("black_queen", "black", "Assets/QueenBlack.png", [420, 7.5], self.screen))

        self.chessboard.add_piece(ChessPiece("black_knight1", "black", "Assets/KnightBlack.png", [120, 7.5], self.screen))
        self.chessboard.add_piece(ChessPiece("black_knight2", "black", "Assets/KnightBlack.png", [620, 7.5], self.screen))
        
        self.game_start_sound.play()
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Handle events for each piece
                for piece in self.chessboard.pieces:
                    piece.handle_event(event)

            if ChessData.get_removed_piece():
                self.chessboard.remove_piece(ChessData.get_removed_piece())
                self.piece_capture_sound.play()
                ChessData.update_removed_piece("")

            if ChessData.get_move_sound():
                self.piece_move_sound.play()
                ChessData.update_move_sound(False)

                
            # Update pieces
            for piece in self.chessboard.pieces:
                piece.update()

            self.screen.fill((255, 255, 255))  # Fill screen with white
            self.chessboard.draw(self.screen)  # Draw the chessboard and pieces
            
            # Show possible moves for all pieces (if any)
            for piece in self.chessboard.pieces:
                piece.show_possible_moves(event)

            

            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 frames per second

        pygame.quit()
