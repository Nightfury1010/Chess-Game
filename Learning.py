import pygame
import os

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Move Sprite with Cursor")

# Define the Sprite class
class MySprite(pygame.sprite.Sprite):
    def __init__(self, image_file):
        super().__init__()
        self.image = pygame.image.load(image_file).convert_alpha()  # Load the image
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.center = (screen_width // 2, screen_height // 2)  # Position the sprite in the center
        self.dragging = False  # Flag to check if sprite is being dragged

    def update(self):
        if self.dragging:
            # Get the current mouse position and update the sprite's position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.center = (mouse_x, mouse_y)

# Load the sprite image
sprite_image_path = os.path.join("Assets", "NightWhite.png")
sprite = MySprite(sprite_image_path)

# Create a sprite group
sprite_group = pygame.sprite.Group()
sprite_group.add(sprite)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is over the sprite
            if sprite.rect.collidepoint(event.pos):
                # Check if the mouse is within the screen bounds
                if 0 <= event.pos[0] < screen_width and 0 <= event.pos[1] < screen_height:
                    sprite.dragging = True  # Start dragging the sprite

                

        
        if event.type == pygame.MOUSEBUTTONUP:
            sprite.dragging = False  # Stop dragging the sprite

    # Update the sprite position if it's being dragged
    sprite.update()

    # Fill the screen with a background color
    screen.fill((255, 255, 255))  # White background

    # Draw the sprite
    sprite_group.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
