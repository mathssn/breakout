import pygame as pg


class Block:
    """Representa os blocos que a bola pode destruir"""

    def __init__(self, game, x, y, width, height, color):
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        # Representa se o bloco esta ativo, sendo destruido ou destruido
        self.state = 0
        # Temporizador para o bloco ser destruido completamente após a colisão com a bola
        self.break_timer = 0
        self.points = 50 # Quantidade que o bloco da ao ser destruido
        self.can_collide = True
        self.type = 'normal'

    def update(self):
        """Atualiza o temporizador de destruição se o bloco estiver sendo destruido"""
        if self.state in [1, 2] and self.game.state == 1:
            self.break_timer -= 1
            if self.break_timer == 2:
                self.state = 2
            elif self.break_timer == 0:
                self.state = -1

    def draw(self, screen: pg.Surface):
        """Desenha o bloco na tela de acordo com seu estado"""
        if 0 <= self.state <= 2:
            screen.blit(self.game.assets[self.color][self.state], self.rect)
    

class BallBlock(Block):

    def __init__(self, game, x, y, width, height, color):
        super().__init__(game, x, y, width, height, color)
        self.type = 'ball'
    
    def draw(self, screen):
        if self.state == 0:
            screen.blit(self.game.assets[self.color][3], self.rect)
        elif 1 <= self.state <= 2:
            screen.blit(self.game.assets[self.color][self.state], self.rect)


class BrickBlock(Block):

    def __init__(self, game, x, y, width, height, color):
        super().__init__(game, x, y, width, height, color)
        self.type = 'brick'
        self.stage = 0
    
    def draw(self, screen):
        if self.state == 0:
            screen.blit(self.game.assets[self.color][4+self.stage], self.rect)
        elif 1 <= self.state <= 2:
            screen.blit(self.game.assets[self.color][self.state], self.rect)



class InvisibleBlock(Block):

    def __init__(self, game, x, y, width, height, color):
        super().__init__(game, x, y, width, height, color)
        self.type = 'invisible'
        self.stage = 'invisible'
        self.collided = False
    
    def draw(self, screen):
        if self.state == 0 and self.stage == 'invisible':
            screen.blit(self.game.assets[self.color][6], self.rect)
        elif 0 <= self.state <= 2:
            screen.blit(self.game.assets[self.color][self.state], self.rect)

