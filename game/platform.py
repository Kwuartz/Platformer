import pygame
from game.config import screenWidth

class Platform():
  thickness = 6
  
  def __init__(self, x1, x2, y, moving, distance = 0, direction = 0, speed = 0):
    self.x1 = x1
    self.x2 = x2
    self.y = y
    
    self.moving = moving
    self.speed = speed
    self.initialDistance = distance
    self.direction = direction
    
    if self.direction == -1:
      self.distance = distance
    else:
      self.distance = 0
    
  def update(self, delta):
    if self.moving:
      self.x1 += self.direction * self.speed * delta
      self.x2 += self.direction * self.speed * delta
      self.distance += self.direction * self.speed * delta
      
      if self.distance > self.initialDistance or self.distance < 0:
        self.direction *= -1
        