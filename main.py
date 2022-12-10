import pygame
from game.config import screenSize, screenWidth, screenHeight
from game.player import Player
from game.platform import Platform

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(screenSize)

pygame.display.set_caption('Hello World!')

# Sprites and colors
backgroundColor = (255, 255, 255)
playerSprite = pygame.image.load("assets/gfx/player.png").convert_alpha()

# Game objects
player = Player(120, 80)
platforms = []

platforms.append(Platform(100, 150, 200, True, 100, 1, 50))
platforms.append(Platform(0, screenWidth, screenHeight, False))

def main():
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    # Logic
    delta = clock.tick(60) / 1000
    
    # Moves platforms
    for platform in platforms:
      platform.update(delta)
    
    # Checks if player is falling
    player.isFalling = True if not player.isJumping else False
    player.platform = False
    for platform in platforms:
      if checkCollisions(player.position.x, player.position.y, player.width, player.height, platform.x1, platform.y - platform.thickness / 2, platform.x2 - platform.x1, platform.thickness):
        player.position.y = platform.y - player.height - platform.thickness / 2
        player.isFalling = False
        
        # To move the player with the platform
        player.platform = platform
    
    player.update(delta)
    
    # Graphics
    screen.fill(backgroundColor)

    # Player
    screen.blit(playerSprite, (player.position.x, player.position.y))

    for platform in platforms:
      pygame.draw.line(screen, (0,0,0), (platform.x1, platform.y), (platform.x2, platform.y), platform.thickness)
    
    pygame.display.flip()
  
def checkCollisions(ax, ay, awidth, aheight, bx, by, bwidth, bheight):
  return (ay + aheight >= by and ay <= by + bheight) and (ax + awidth >= bx and ax <= bx + bwidth)

if __name__ == "__main__":
  main()