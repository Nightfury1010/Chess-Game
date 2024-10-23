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
            if ChessData.get_chess_turn() in piece_name:  # Ensure turn matches the piece clicked
                ChessData.update_active_piece(piece_name)
            else:
                return

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
                        if ChessData.get_chess_board()[new_x][new_y] != ".":  # If there is a piece in the target square
                            captured_piece = ChessData.get_chess_board()[new_x][new_y]  # Get the captured piece
                            print(f"{captured_piece} was removed")
                            ChessData.update_removed_pieces(captured_piece)  # Update removed pieces list
                        piece_position[old_x][old_y]="."
                        piece_position[new_x][new_y]=ChessData.get_active_piece()
                        
                        ChessData.update_chess_board(piece_position)
                        ChessData.false_outline_flag()
                        ChessData.update_chess_turn()
                        ChessData.update_active_piece("")
                        break    
                
                if(not self.updated_flag):
                    active_piece= ChessData.get_active_piece()
                    x,y=np.argwhere(ChessData.get_chess_board()==active_piece)[0]
                    x_position=int(x)*100+20
                    y_position=int(y)*77.5+7.5
                    self.rect.topleft=(x_position,y_position)

                    

            #if position is not available go back to previous position
            #else if the ending position is true , set new position
            #will continue this later

    def get_possible_moves(self,piece):
        current_position = np.argwhere(ChessData.get_chess_board() == piece)
        possible_moves = np.empty((0, 2))
        if("pawn" in piece):
            x_coord,y_coord=current_position[0]
            x_coord,y_coord=int(x_coord),int(y_coord)

            pawn_takes_one,pawn_takes_two=np.array([[-1,-1]]),np.array([[1,-1]])
            pawn_takes_color="black"
            if("black" in piece):
                pawn_takes_one,pawn_takes_two=np.array([[-1,1]]),np.array([[1,1]])
                pawn_takes_color="white"
            pawn_takes_one_x,pawn_takes_one_y= pawn_takes_one[0]
            pawn_takes_two_x,pawn_takes_two_y= pawn_takes_two[0]
            if (current_position[0][0] + pawn_takes_one_x <= 7 and
                current_position[0][0] + pawn_takes_one_x >= 0 and
                current_position[0][1] + pawn_takes_one_y <= 7 and
                current_position[0][1] + pawn_takes_one_y >= 0 and
                pawn_takes_color in ChessData.get_chess_board()[current_position[0][0] + pawn_takes_one_x][current_position[0][1] + pawn_takes_one_y]):
                    possible_moves = np.append(possible_moves, current_position[0] + pawn_takes_one, axis=0)
            if (current_position[0][0] + pawn_takes_two_x <= 7 and
                current_position[0][0] + pawn_takes_two_x >= 0 and
                current_position[0][1] + pawn_takes_two_y <= 7 and
                current_position[0][1] + pawn_takes_two_y >= 0 and
                pawn_takes_color in ChessData.get_chess_board()[current_position[0][0] + pawn_takes_two_x][current_position[0][1] + pawn_takes_two_y]):
                possible_moves = np.append(possible_moves, current_position + pawn_takes_two, axis=0)

            first_move=np.array([[0, -1]])
            if ("black" in piece): 
                first_move=np.array([[0, 1]])
            if ("." in ChessData.get_chess_board()[x_coord][y_coord+first_move[0][1]]):
                possible_moves = np.append(possible_moves, current_position + first_move, axis=0)
            else:
                return possible_moves   
            second_move=np.empty((0,2))
            if y_coord==6 and "white" in piece:
                second_move = np.array([[0, -2]])
            elif ("black" in piece and y_coord==1):
                second_move = np.array([[0, 2]])
            else:
                return possible_moves                     
            if ("." in ChessData.get_chess_board()[x_coord][y_coord+second_move[0][1]]):
                possible_moves = np.append(possible_moves, current_position + second_move, axis=0)


        if("knight" in piece):
            move_offsets = np.array([[2, 1], [2, -1], [-2, 1], [-2, -1],[1, 2], [1, -2], [-1, 2], [-1, -2]])
            knight_cannot_move="white"
            if("black" in piece):
                knight_cannot_move="black"
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
                
                if (not knight_cannot_move in ChessData.get_chess_board()[x_coord][y_coord]):
                    new_possible_moves=np.append(new_possible_moves,new_position,axis=0)
                   
            
            possible_moves= new_possible_moves
        

        if "rook" in piece:
            x_coord, y_coord = current_position[0]
            rook_takes = "black" if "white" in piece else "white"

            # Moving left, right, up, and down
            possible_moves = add_moves_in_direction(x_coord - 1, y_coord, -1, 0, possible_moves, rook_takes)
            possible_moves = add_moves_in_direction(x_coord + 1, y_coord, 1, 0, possible_moves, rook_takes)
            possible_moves = add_moves_in_direction(x_coord, y_coord - 1, 0, -1, possible_moves, rook_takes)
            possible_moves = add_moves_in_direction(x_coord, y_coord + 1, 0, 1, possible_moves, rook_takes)

        if "bishop" in piece:
            x_coord, y_coord = current_position[0]
            bishop_takes = "black" if "white" in piece else "white"

            # Moving diagonally in all four directions
            possible_moves = add_moves_in_direction(x_coord - 1, y_coord - 1, -1, -1, possible_moves, bishop_takes)  # top-left
            possible_moves = add_moves_in_direction(x_coord + 1, y_coord - 1, 1, -1, possible_moves, bishop_takes)   # top-right
            possible_moves = add_moves_in_direction(x_coord - 1, y_coord + 1, -1, 1, possible_moves, bishop_takes)   # bottom-left
            possible_moves = add_moves_in_direction(x_coord + 1, y_coord + 1, 1, 1, possible_moves, bishop_takes)     # bottom-right

        if "queen" in piece:
            x_coord, y_coord = current_position[0]
            queen_takes = "black" if "white" in piece else "white"

            # Rook-like moves (horizontal and vertical)
            possible_moves = add_moves_in_direction(x_coord - 1, y_coord, -1, 0, possible_moves, queen_takes)  # left
            possible_moves = add_moves_in_direction(x_coord + 1, y_coord, 1, 0, possible_moves, queen_takes)   # right
            possible_moves = add_moves_in_direction(x_coord, y_coord - 1, 0, -1, possible_moves, queen_takes)  # up
            possible_moves = add_moves_in_direction(x_coord, y_coord + 1, 0, 1, possible_moves, queen_takes)   # down

            # Bishop-like moves (diagonal)
            possible_moves = add_moves_in_direction(x_coord - 1, y_coord - 1, -1, -1, possible_moves, queen_takes)  # top-left
            possible_moves = add_moves_in_direction(x_coord + 1, y_coord - 1, 1, -1, possible_moves, queen_takes)   # top-right
            possible_moves = add_moves_in_direction(x_coord - 1, y_coord + 1, -1, 1, possible_moves, queen_takes)   # bottom-left
            possible_moves = add_moves_in_direction(x_coord + 1, y_coord + 1, 1, 1, possible_moves, queen_takes)     # bottom-right

        if "king" in piece:
            x_coord, y_coord = current_position[0]
            king_takes = "black" if "white" in piece else "white"
    
    # Possible directions the king can move (dx, dy)
            directions = [(-1, -1),(-1, 0), (-1, 1), (0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]

            for dx, dy in directions:
                new_x = x_coord + dx
                new_y = y_coord + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if king_takes in ChessData.get_chess_board()[new_x][new_y] or ChessData.get_chess_board()[new_x][new_y] == ".":
                        possible_moves = np.append(possible_moves, [[new_x, new_y]], axis=0)

               
        return possible_moves
    
    def show_possible_moves(self, event):
        if (event.type== pygame.MOUSEBUTTONDOWN):
            ChessData.true_outline_flag()

            if (not ChessData.get_chess_turn() in ChessData.get_active_piece()):
                ChessData.false_outline_flag()
                return
            outline_moves=self.get_possible_moves(ChessData.get_active_piece())
            ChessData.update_outline_moves(outline_moves)
        if ChessData.get_outline_flag() :
        # Check if the mouse is over the piece
            takes_color="black"
            if "black" in ChessData.get_active_piece():
                takes_color="white"
                
            move_marker = pygame.image.load("Assets/direction.png").convert_alpha()  # Use your own marker image here
            move_marker = pygame.transform.scale(move_marker, (100, 77.6))  # Scale the marker to fit your grid
            takes_marker = pygame.image.load("Assets/direction2.png").convert_alpha()  # Use your own marker image here
            takes_marker = pygame.transform.scale(takes_marker, (100, 77.6))  # Scale the marker to fit your grid
            for i in ChessData.get_outline_moves():
                x, y = i
                x,y=int(x),int(y)
                x2 = x * 100   # Adjust x to fit the grid
                y2 = y * 77.6   # Adjust y to fit the grid
                if takes_color in ChessData.get_chess_board()[x][y]:
                    self.screen.blit(takes_marker, (x2, y2))
                    continue
                self.screen.blit(move_marker, (x2, y2))


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to find the closest point
def find_closest_point(event_pos):
    closest_point = min(points, key=lambda point: distance(point, event_pos))
    return closest_point

def add_moves_in_direction(x, y, dx, dy, possible_moves, capture_color):
    while 0 <= x < 8 and 0 <= y < 8:
        if capture_color in ChessData.get_chess_board()[x][y]:
            possible_moves = np.append(possible_moves, [[x, y]], axis=0)
            break
        if ChessData.get_chess_board()[x][y] != ".":  
            break
        possible_moves = np.append(possible_moves, [[x, y]], axis=0)
        x += dx
        y += dy
    return possible_moves
