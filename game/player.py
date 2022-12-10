import pygame
from game.config import screenWidth, gravity, terminalVelocity

class Player():
  width = 20
  height = 31
  
  walkSpeed = 100
  ySpeed = 0
  
  falltime = 0
  jumpPower = 250
    
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

    if keys[pygame.K_SPACE]:
      if self.isFalling == False and self.isJumping == False:
        self.isJumping = True
        self.ySpeed = -self.jumpPower

    if not (self.position.x < 0 and self.direction == -1) and not (self.position.x > screenWidth and self.direction == 1):
      self.position.x += self.direction * self.walkSpeed * delta
      
    if self.platform:
      self.position.x += self.platform.speed * self.platform.direction * delta

    if self.isFalling:
      self.falltime += delta
      if self.ySpeed < terminalVelocity:
        self.ySpeed += self.falltime * gravity
    elif self.isJumping:
      self.ySpeed -= gravity * delta
      
      if self.ySpeed < 0:
        self.isJumping = False
    else:
      self.falltime = self.ySpeed = 0
      
    self.position.y += self.ySpeed * delta
      