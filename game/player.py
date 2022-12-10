import pygame
from game.config import screenWidth, gravity, terminalVelocity

class Player():
  width = 20
  height = 31
  
  walkSpeed = 150
  ySpeed = 0
  
  airtime = 0
  jumpPower = 350
    
  isFalling = False
  isJumping = False
  
  platform = False

  def __init__(self, x, y):
    self.position = pygame.Vector2()
    self.position.x = x
    self.position.y = y
    

  def update(self, delta):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      self.direction = -1
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      self.direction = 1
    else:
      self.direction = 0
      
    # Jumping
    if keys[pygame.K_SPACE]:
      if self.isFalling == False and self.isJumping == False:
        self.isJumping = True
        self.ySpeed = -self.jumpPower
        
    # Checking for edge of screen
    if not (self.position.x < 0 and self.direction == -1) and not (self.position.x > screenWidth and self.direction == 1):
      self.position.x += self.direction * self.walkSpeed * delta
    
    # Moving with the platform they stand on
    if self.platform:
      self.position.x += self.platform.speed * self.platform.direction * delta

    if self.isFalling: 
      self.airtime += delta
      
      # Fall faster when they start falling
      if self.airtime < 0.5:
        self.ySpeed += gravity
      
      if self.ySpeed < terminalVelocity:
        self.ySpeed += self.airtime * gravity
        
    elif self.isJumping:
      self.airtime += delta
      self.ySpeed += self.airtime * gravity
      
      if self.ySpeed > 0:
        self.isJumping = False
        self.airtime = 0
    else:
      self.airtime = self.ySpeed = 0
      
    self.position.y += self.ySpeed * delta
      