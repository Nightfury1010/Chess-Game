import pygame
from ChessPiece import ChessPiece

screen_width = 800
screen_height = 620
class ChessBoard(pygame.sprite.Sprite):
    def __init__(self, image_file):
        super().__init__()  # Initialize the parent class
        # Load the background image
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.rect.topleft = (0, 0)  # Set the position of the chessboard
        self.pieces = pygame.sprite.Group()  # Group to hold all chess pieces
        self.piece_dict = {}  # Dictionary for quick access to pieces

    def add_piece(self, piece):
        self.pieces.add(piece)  # Add the piece to the sprite group
        self.piece_dict[piece.piece_type] = piece  # Store the piece using its name for quick access
  # Store piece in the dictionary

    def draw(self, screen):
        # Draw the chessboard image first
        screen.blit(self.image, self.rect)  # Draw the chessboard background
        self.pieces.draw(screen)  # Draw all chess pieces

    def update(self):
        self.pieces.update()  # Call the update method for all pieces if needed

    def remove_piece(self, piece_name):
        print(f"Removed piece: {piece_name}")
        if piece_name in self.piece_dict:
            piece = self.piece_dict[piece_name]
            piece.kill()  # Removes the sprite from all groups
            self.pieces.remove(piece)  # Remove from the sprite group
            del self.piece_dict[piece_name]  # Remove from the dictionary
            