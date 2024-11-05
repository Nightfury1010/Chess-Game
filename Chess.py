from GameController import GameController

if __name__ == "__main__":
    game = GameController()
      # Initializes the chess pieces
    while True:
        game.initialize_pieces()
        game.run()  # Start the game loop
        game.game_over_menu()
        if game.game_over:
            break
