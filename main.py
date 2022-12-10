import pygame
import random
from game.config import screenWidth, screenHeight, maxPlatforms
from game.player import Player
from game.platform import Platform

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption('Hello World!')

# Sprites and colors
backgroundColor = (200, 255, 255)
playerSprite = pygame.image.load("assets/gfx/player.png").convert_alpha()

# Game objects
player = Player(100, screenHeight - 150)
platforms = []

# Creating starting platform
lastPlatform = Platform(screenWidth / 2 - 100, 200, screenHeight - 100, False)
platforms.append(lastPlatform)

def main():
  global lastPlatform
  
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    # Logic
    delta = clock.tick(60) / 1000
    
    # Finds how much to scroll
    scroll = player.update(delta)
    
    # Moves platforms
    for platform in platforms:
      platform.update(delta, scroll)
      
      if platform.y > screenHeight:
        platforms.remove(platform)
        
    if len(platforms) < maxPlatforms:
      platformWidth = random.randint(60, 100)
      platformX = random.randint(0, screenWidth - platformWidth)
      
      # I use the variable lastPlatform so I can use that to create new platforms
      platformY = lastPlatform.y - screenHeight / maxPlatforms
      lastPlatform = Platform(platformX, platformWidth, platformY, False)
      platforms.append(lastPlatform)
    
    # Checks if player is falling
    player.isFalling = False if player.isJumping else True
    
    if player.isFalling:
      player.platform = False
      for platform in platforms:
        if checkCollisions(player.position.x, player.position.y, player.width, player.height, platform.x1, platform.y - platform.thickness / 2, platform.x2 - platform.x1, platform.thickness, player.height / 1.25):
          player.position.y = platform.y - player.height - platform.thickness / 2
          player.isFalling = False
          
          # To move the player with the platform
          player.platform = platform
          
    # Graphics
    screen.fill(backgroundColor)

    # Player
    screen.blit(playerSprite, (player.position.x, player.position.y))

    for platform in platforms:
      pygame.draw.line(screen, (0,0,0), (platform.x1, platform.y), (platform.x2, platform.y), platform.thickness)
    
    pygame.display.flip()
  
def checkCollisions(ax, ay, awidth, aheight, bx, by, bwidth, bheight, yTolerance):
  # Y tolerance is for when you only want the player to collide with the platform if their feet touch it
  return (ay + aheight >= by and ay + yTolerance <= by + bheight) and (ax + awidth >= bx and ax <= bx + bwidth)

if __name__ == "__main__":
  main()