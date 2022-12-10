import pygame
from game.config import screenWidth

class Platform():
  thickness = 8
  
  def __init__(self, x, width, y, moving, distance, speed):
    self.x1 = x
    self.x2 = x + width
    self.y = y
    
    self.moving = moving
    self.speed = speed
    self.initialDistance = distance
    self.direction = 1
    
    self.distance = 0
    
  def update(self, delta, scroll):
    if self.moving:
      self.x1 += self.direction * self.speed * delta
      self.x2 += self.direction * self.speed * delta
      self.distance += self.direction * self.speed * delta
      
      if self.distance > self.initialDistance or self.distance < 0:
        self.direction *= -1
        
    self.y += scroll