import pygame

class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.size = 40
        self.speed = 5
        self.hp = 3

    def move(self, target_x, target_y):
     if self.x < target_x:
        self.x += self.speed
     if self.x > target_x:
        self.x -= self.speed
     if self.y < target_y:
        self.y += self.speed
     if self.y > target_y:
        self.y -= self.speed

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))