import pygame
import random
from game.config import screenWidth, screenHeight, maxPlatforms
from game.player import Player
from game.platform import Platform

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Caption and icon
pygame.display.set_caption('Infinite Platforms!')

# Assets
backgroundColor = (200, 255, 255)
playerSprite = pygame.image.load("assets/gfx/player.png").convert_alpha()

font32 = pygame.font.Font("assets/font/font.otf", 32)
font64 = pygame.font.Font("assets/font/font.otf", 64)

def main():
  # Game objects
  player = Player(190, screenHeight - 150)
  platforms = []

  # Creating starting platform
  lastPlatform = Platform(screenWidth / 2 - 100, 200, screenHeight - 100, False, 0, 0)
  platforms.append(lastPlatform)
  
  running = True
  gameover = False
  
  score = highscore =  0
  newHighscore = False
  
  while running:
    # Checking if game window closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False

    if not gameover:
      # Logic
      delta = clock.tick(60) / 1000
      
      # Finds how much to scroll
      scroll = player.update(delta)
      score += scroll
      
      # Checks if there is a new highscore
      if score > highscore:
        highscore = score
        newHighscore = True
      
      # Moves platforms
      for platform in platforms:
        platform.update(delta, scroll)
        
        # Removes platforms that are offscreen
        if platform.y > screenHeight:
          platforms.remove(platform)
      
      # Adds new platforms if necessary
      if len(platforms) < maxPlatforms:
        platformWidth = random.randint(60, 100)
        
        moving = False
        distance = 0
        speed = 0
            
        # Begin adding moving platforms if the score is high enough
        if score > 1000:
          moving = random.choice([True, False, False])
          
          if moving:
            distance = random.randint(50, 100)
            speed = random.randint(50, 100)
          
        # Need to factor in platform width and how far it is moving when getting the X
        platformX = random.randint(0, screenWidth - platformWidth - distance)
        platformY = lastPlatform.y - screenHeight / maxPlatforms
        
        # I use the variable lastPlatform so I can use that to create new platforms
        lastPlatform = Platform(platformX, platformWidth, platformY, moving, distance, speed)
        platforms.append(lastPlatform)
        
      # Checks if player is falling
      player.isFalling = False if player.isJumping else True
      player.platform = False
      
      if player.isFalling:
        for platform in platforms:
          if checkCollisions(player.position.x, player.position.y, player.width, player.height, platform.x1, platform.y - platform.thickness / 2, platform.x2 - platform.x1, platform.thickness, player.height / 1.25):
            player.position.y = platform.y - player.height - platform.thickness / 2
            player.isFalling = False
            
            # To move the player with the platform
            player.platform = platform
      
      # Checks if the player is offscreen
      if player.position.y > screenHeight:
        gameover = True
            
      # Graphics
      screen.fill(backgroundColor)
      
      # Score
      writeText(f"SCORE: {round(score)}", font32, (255, 200, 200), 5, 0, False)

      # Player
      screen.blit(playerSprite, (player.position.x, player.position.y))
      
      # Platforms
      for platform in platforms:
        pygame.draw.line(screen, (255, 200, 200), (platform.x1, platform.y), (platform.x2, platform.y), platform.thickness)
    
    # Game over screen  
    else:
      screen.fill(backgroundColor)
      
      writeText("GAME OVER", font64, (255, 200, 200), 0, 100, True)
      writeText("PRESS SPACE TO RESTART", font32, (255, 200, 200), 0, 175, True)
      writeText(f"SCORE THIS RUN: {round(score)}", font32, (255, 200, 200), 0, 200, True)
      
      if newHighscore:
        writeText(f"NEW HIGH SCORE!!!", font32, (255, 200, 200), 0, 225, True)
      else:
        writeText(f"HIGH SCORE: {round(highscore)}", font32, (255, 200, 200), 0, 225, True)
      
      # Waits for player to restart with space bar
      keys = pygame.key.get_pressed()
      if keys[pygame.K_SPACE]:
        # Resets variables and restarts game
        gameover = False
        newHighscore = False
        scroll = 0
        score = 0
        
        player.position.x = 190
        player.position.y = screenHeight - 150
        
        platforms = []
        lastPlatform = Platform(screenWidth / 2 - 100, 200, screenHeight - 100, False, 0, 0)
        platforms.append(lastPlatform)
    
    pygame.display.flip()

def writeText(text, font, color, x, y, centreX):
  renderedText = font.render(text, True, color)

  # Centering
  
  if centreX:
    textPos = renderedText.get_rect()
    textPos.y += y
    textPos.centerx = screen.get_rect().centerx
  else:
    textPos = x, y
  
  screen.blit(renderedText, textPos)
    
  
def checkCollisions(ax, ay, aWidth, aHeight, bx, by, bWidth, bHeight, yTolerance=0):
  # Y tolerance is for when you only want the player to collide with the platform if their feet touch it
  return (ay + aHeight >= by and ay + yTolerance <= by + bHeight) and (ax + aWidth >= bx and ax <= bx + bWidth)

if __name__ == "__main__":
  main()