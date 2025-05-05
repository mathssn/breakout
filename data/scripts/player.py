import pygame as pg


class Player:
    """Representa a raquete que fica na parte de baixo da tela"""

    def __init__(self, game, x, y, width, height):
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.movement = [False, False] # Define se o player deve se mover para esquerda ou direita
        self.speed = 700 # Velocidade do player

    def update(self, delta_time: int):
        if self.game.state not in [0, 1]:
            return None
        
        if self.movement[0] and not self.movement[1]:
            self.rect.x -= self.speed * delta_time
            if self.rect.x < 0:
                self.rect.x = 0
                
        if self.movement[1] and not self.movement[0]:
            self.rect.x += self.speed * delta_time
            if self.rect.right > self.game.screen.get_width():
                self.rect.right = self.game.screen.get_width()

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, (255, 255, 255), self.rect, border_radius=10)