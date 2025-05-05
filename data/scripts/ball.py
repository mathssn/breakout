import pygame as pg
import math
import random
from data.scripts.utils import check_collision_circle_rect

class Ball:
    """Representa a bola"""
    speed = 430 # Velocidade da bola

    def __init__(self, game, center: list, radius: int, color: str):
        self.game = game
        self.center = center # Centro da esfera
        self.radius = radius # Raio da esfera
        self.color = color
        self.directions = [0, 0] # Direção que a bola deve ir
        self.collision_horizontal = True # Define se a bola pode ou não colidir horizontalmente
        self.collision_horizontal_cooldown = 0 # Cooldown que a bola fica sem colisão horizontal

    def update(self, delta_time: int):
        # Se o estado do jogo for 0(Não iniciado), a bola segue o player
        if self.game.state == 0:
            self.center[0] = self.game.player.rect.centerx
        # Sai da função se o jogo não estiver rodando
        if self.game.state != 1:
            return None
        
        # Checa o cooldown de colisão horizontal da bola
        if self.collision_horizontal_cooldown > 0:
            self.collision_horizontal_cooldown -= 1
            # Se o cooldown chegar a 0, a bola pode colidir horizontalmente de novo
            if self.collision_horizontal_cooldown == 0:
                self.collision_horizontal = True
        
        # Move a bola no eixo x
        self.center[0] += Ball.speed * self.directions[0] * delta_time

        # Verifica se a bola saiu da tela e muda sua direção
        if self.center[0] + self.radius > self.game.screen.get_width():
            self.center[0] = self.game.screen.get_width() - self.radius
            self.directions[0] *= -1
        elif self.center[0] - self.radius < 0:
            self.center[0] = self.radius
            self.directions[0] *= -1

        # Move a bola no eixo y
        self.center[1] += Ball.speed * self.directions[1] * delta_time
        # Verifica se a bola saiu da tela e muda sua direção
        if self.center[1] - self.radius < 0:
            self.center[1] = self.radius
            self.directions[1] *= -1

        
        Ball.speed = min(450, Ball.speed) # Limita a velocidade a 8

    def check_player_collision(self, player):
        """Checa a colisão com o player"""
        collision = check_collision_circle_rect(self.get_list(), player.rect)

        if collision[1]:
            # Se houve colisão vertical, corrigi a posição da bola
            if self.center[1] < player.rect.centery:
                self.center[1] = player.rect.top - self.radius
            else:
                self.center[1] = player.rect.bottom + self.radius

            # Calcula o novo angulo de inclinação vertical da bola
            relative = (self.center[1] - player.rect.top) / player.rect.height
            variation = random.choice([1.1, -1.1])
            angle = math.radians(max(min(relative * 75, 75), -75))
            self.directions[1] = math.sin(angle) * variation
            
        # Checa se houve colisão horizontal e se o player pode colidir horizontalmente naquele frame
        if collision[0] and self.collision_horizontal:
            # Se houve colisão vertical, corrigi a posição da bola
            if self.center[0] < player.rect.centerx:
                self.center[0] = player.rect.left - self.radius
            else:
                self.center[0] = player.rect.right + self.radius

            # Inverte a direção da bola
            if self.directions[0] < 0 and player.movement[1]:
                self.directions[0] *= -1
            elif self.directions[0] > 0 and player.movement[0]:
                self.directions[0] *= -1
            elif not player.movement[0] and not player.movement[1]:
                self.directions[0] *= -1

            # Defini que a bola não pode mais colidir horizontalmente por 5 frames
            self.collision_horizontal = False
            self.collision_horizontal_cooldown = 5


    def get_list(self) -> list[int]:
        """Retorna uma lista contendo o centro da bola e seu raio"""
        return [self.center[0], self.center[1], self.radius]
    
    def start(self):
        """Inicia o movimento da bola e escolhe uma inclinação randomica para ela"""
        direction = random.choice([1, -1])
        angle = math.radians(random.uniform(40, 70))
        self.directions[0] = direction * math.cos(angle)
        self.directions[1] = -math.sin(angle)

    def draw(self, screen: pg.Surface):
        """Desenha a bola"""
        pg.draw.circle(screen, self.game.colors[self.color], self.center, self.radius)