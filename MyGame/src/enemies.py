import random
import pygame

class Enemy:
    def __init__(self):
        self.type = random.choice(["normal", "fast", "tank"])
        self.x = random.randint(0, 760)
        self.y = random.randint(0, 560)

        if self.type == "normal":
            self.speed = 2
            self.hp = 1
            self.size = 30

        elif self.type == "fast":
            self.speed = 4
            self.hp = 1
            self.size = 20

        elif self.type == "tank":
            self.speed = 1
            self.hp = 3
            self.size = 50

    def move_towards(self, px, py):
        if self.x < px:
            self.x += self.speed
        if self.x > px:
            self.x -= self.speed
        if self.y < py:
            self.y += self.speed
        if self.y > py:
            self.y -= self.speed

    def draw(self, screen):
        if self.type == "fast":
            color = (255, 150, 150)
        elif self.type == "tank":
            color = (150, 0, 0)
        else:
            color = (255, 50, 50)

        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))