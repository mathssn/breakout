import pygame as pg
from data.scripts.color import Color


class Board:
    """Quadro responsavel por mostrar as vidas do jogador e os pontos"""

    def __init__(self, game, points=0):
        self.game = game
        self.points = points
        self.font = pg.Font('data/fonts/font.ttf', 30)
        self.points_rect = pg.Rect(0, 5, 0, 0)

        # Coordenadas do circulos que representam as vidas, 10 é o raio dos circulos
        self.circles_lifes = [[15, 15], [40, 15], [65, 15], 10]
        self.render()

        # Cria mensagens que serão exibidas na tela em determinados momentos
        self.messages = {
            "start": Text("Press 'space' to start", Color.white, self.font),
            "game_over": Text("Game Over! Pontuação final:", Color.white, self.font)
        }
        # Define se a mensaem 'start' deve ser mostrada
        self.show_start_message = True

        # Posiciona as mensagens
        self.messages['start'].rect.centerx = game.screen.get_width() // 2
        self.messages['start'].rect.centery = game.screen.get_height() // 2
        self.messages['game_over'].rect.centerx = game.screen.get_width() // 2
        self.messages['game_over'].rect.centery = game.screen.get_height() // 2

    def render(self):
        """Renderiza textos"""

        # Garante que os pontos sempre tenham 5 caracteres
        txt = str(self.points)
        for _ in range(5-len(txt)):
            txt = '0' + txt

        # Renderiza a quantidade de pontos e a reposiociona
        self.points_img = self.font.render(txt, True, Color.white)
        self.points_rect.width = self.points_img.get_width()
        self.points_rect.height = self.points_img.get_height()
        self.points_rect.centerx = self.game.screen.get_width() / 2
        
    def draw(self, screen: pg.Surface):
        """Desenha a quantidade de vidas e os pontos"""
        for i in range(3):
            if i+1 < self.game.lifes:
                # Desenha as vidas restantes preenchidas
                pg.draw.circle(screen, Color.white, self.circles_lifes[i], self.circles_lifes[3]) 
            else: 
                # Desenha as vidas ja usadas apenas com contorno
                pg.draw.circle(screen, Color.white, self.circles_lifes[i], self.circles_lifes[3], 2)

        if self.game.state == 3:
            self.messages['game_over'].draw(screen)
            pos = [self.game.screen.get_width() / 2 - self.points_img.get_width(), self.messages['game_over'].rect.bottom]
            screen.blit(self.points_img, pos)
        else:
            screen.blit(self.points_img, self.points_rect)

        if self.game.state == 0 and self.show_start_message:
            self.messages['start'].draw(screen)


class Text:
    """Representa um texto a ser exibido na tela"""

    def __init__(self, txt: str, color: list[int], font: pg.Font):
        self.txt = txt
        self.color = color
        self.rect = pg.Rect(0, 0, 0, 0)
        self.render(font)
    
    def render(self, font: pg.Font):
        """Renderiza texto"""
        self.txt_img = font.render(self.txt, True, self.color)
        self.rect.width = self.txt_img.get_width()
        self.rect.height = self.txt_img.get_height()

    def draw(self, screen: pg.Surface):
        screen.blit(self.txt_img, self.rect)