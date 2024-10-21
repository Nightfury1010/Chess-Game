import pygame
import math
import numpy as np
from ChessData import ChessData

points = []
for i in range(8):  # For rows (Y values)
    for j in range(8):  # For columns (X values)
        x = 50 + j * 100  # X values: 50, 150, 250, ..., 750
        y = 55 + i * 75   # Y values: 55, 130, 205, ..., up to 8th term
        points.append((x, y))
class ChessPiece(pygame.sprite.Sprite):
    def __init__(self, piece_type, color, image_file, position,screen):
        super().__init__()
        self.piece_type = piece_type
        self.color = color
        self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.dragging = False  # Flag to check if the piece is being dragged
        self.screen = screen
        self.updated_flag= False

    def update(self):
        if self.dragging:
            # Update the position of the piece to follow the mouse cursor
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.center = (mouse_x, mouse_y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = find_closest_point(event.pos)
            x = int((x - 50) / 100)
            y = int((y - 55) / 75)
            piece_name=ChessData.get_chess_board()[x][y]
            ChessData.update_active_piece(piece_name)

            if self.rect.collidepoint(event.pos):
                self.dragging = True  # Start dragging the piece

        if event.type == pygame.MOUSEBUTTONUP:
            self.updated_flag= False
            self.dragging = False  # Stop dragging the piece
            released_position= find_closest_point(event.pos)
            x,y=released_position
            x=int((x-50)/100)
            y=int((y-55)/75)
            released_position=np.array([x,y])
            
            if self.piece_type== ChessData.get_active_piece():
                for moves in ChessData.get_outline_moves():
                    x,y=moves
                    x,y=int(x),int(y)
                    moves=np.array([x,y])

                    if np.array_equal(released_position, moves):
                        new_x,new_y=released_position
                        x_position=int(new_x)*100+20
                        y_position=int(new_y)*77.5+7.5
                        self.rect.topleft=(x_position,y_position)
                        self.updated_flag=True
                        piece_position=ChessData.get_chess_board()
                        old_x,old_y=np.argwhere(ChessData.get_chess_board()==ChessData.get_active_piece())[0]
                        piece_position[old_x][old_y]="."
                        piece_position[new_x][new_y]=ChessData.get_active_piece()
                        ChessData.false_outline_flag()
                        ChessData.update_chess_turn()
                        if(ChessData.get_is_first_move() and self.color=="black") :
                            ChessData.update_is_first_move()
                        break    
                
                if(not self.updated_flag):
                    active_piece= ChessData.get_active_piece()
                    print(np.argwhere(ChessData.get_chess_board()==active_piece))
                    x,y=np.argwhere(ChessData.get_chess_board()==active_piece)[0]
                    x_position=int(x)*100+20
                    y_position=int(y)*77.5+7.5
                    self.rect.topleft=(x_position,y_position)
            if(ChessData.get_is_first_move() and self.color=="black") :
                ChessData.update_is_first_move

                    

            #if position is not available go back to previous position
            #else if the ending position is true , set new position
            #will continue this later

    def get_possible_moves(self,piece):
        current_position = np.argwhere(ChessData.get_chess_board() == piece)
        possible_moves = np.empty((0, 2))
        if("pawn" in piece):
            first_move=np.array([[0, -1]])
            if ("black" in piece): 
                first_move=np.array([[0, 1]])
            possible_moves = np.append(possible_moves, current_position + first_move, axis=0)
            if ChessData.get_is_first_move():
                second_move = np.array([[0, -2]])
                if ("black" in piece):
                    second_move = np.array([[0, 2]])                     
                possible_moves = np.append(possible_moves, current_position + second_move, axis=0)
        if("knight" in piece):
            move_offsets = np.array([[2, 1], [2, -1], [-2, 1], [-2, -1],[1, 2], [1, -2], [-1, 2], [-1, -2]])

        # Loop through each offset and append the possible moves
            for offset in move_offsets:
                new_move = current_position + offset
                x,y = new_move[0]
                if x<0 or x>7 or y>7 or y<0:
                    continue
                possible_moves = np.append(possible_moves, new_move, axis=0)
                
            new_possible_moves=np.empty((0, 2))
            for position in possible_moves:
                
                
                x_coord,y_coord=position
                x_coord,y_coord=int(x_coord),int(y_coord)
                new_position=np.array([[x_coord,y_coord]])
                
                if (not 'white' in ChessData.get_chess_board()[x_coord][y_coord]):
                    new_possible_moves=np.append(new_possible_moves,new_position,axis=0)
                   
            
            possible_moves= new_possible_moves
        return possible_moves
    
    def show_possible_moves(self, event):
        if (event.type== pygame.MOUSEBUTTONDOWN):
            ChessData.true_outline_flag()
            #x,y = find_closest_point(event.pos)
            #x = int((x - 50) / 100)
            #y = int((y - 55) / 75)
            #piece_name=ChessData.get_chess_board()[x][y]
            #ChessData.update_active_piece(piece_name)
            if (not ChessData.get_chess_turn() in ChessData.get_active_piece()):
                ChessData.false_outline_flag()
                return
            outline_moves=self.get_possible_moves(ChessData.get_active_piece())
            ChessData.update_outline_moves(outline_moves)
        if ChessData.get_outline_flag() :
        # Check if the mouse is over the piece
            move_marker = pygame.image.load("Assets/direction.png").convert_alpha()  # Use your own marker image here
            move_marker = pygame.transform.scale(move_marker, (100, 77.6))  # Scale the marker to fit your grid

            for i in ChessData.get_outline_moves():
                x, y = i
                x = x * 100   # Adjust x to fit the grid
                y = y * 77.5   # Adjust y to fit the grid
                self.screen.blit(move_marker, (x, y))


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to find the closest point
def find_closest_point(event_pos):
    closest_point = min(points, key=lambda point: distance(point, event_pos))
    return closest_point

