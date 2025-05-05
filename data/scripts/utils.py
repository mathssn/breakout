"""
Modulo responsavel por funções sem nicho especifico no jogo
"""

import pygame as pg
import sys
import os
import random
from data.scripts.block import *
from data.scripts.color import *

BASE_IMAGE_PATH = 'data/sprites'

def check_events(game):
    """Checa o loop de eventos do jogo"""
    for event in pg.event.get():
        if event.type == pg.QUIT: # Sai do jogo
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            # Move o jogador
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                game.player.movement[0] = True
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                game.player.movement[1] = True
            
            # Inicia o jogo se ainda não iniciado
            if event.key == pg.K_SPACE:
                if game.state == 0:
                    game.state = 1
                    for ball in game.balls:
                        ball.start()
                    game.board.show_start_message = False
                if game.state == 3:
                    game.board.points = 0
                    game.board.render()

                    game.state = 0
                    game.board.show_start_message = True
            
            # Pausa e despausa o jogo
            if event.key == pg.K_ESCAPE:
                if game.state == 1:
                    game.state = 2
                elif game.state == 2:
                    game.state = 1

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                game.player.movement[0] = False
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                game.player.movement[1] = False


def load_image(path):
    """Carrega uma imagem"""
    img = pg.image.load(f'{BASE_IMAGE_PATH}{path}').convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    """Carrega uma lista de imagens de uma pasta"""
    images = []
    for file in sorted(os.listdir(BASE_IMAGE_PATH + path)):
        images.append(
            load_image(path + '/' + file)
        )
    return images

def check_collision_circle_rect(circle: list[int], rect: pg.Rect) -> list[bool]:
    """Checa se houve colisão entre um circulo e um retangulo"""
    # Calcula o ponto mais proximo do circulo dentro do retangulo
    closest_x = max(rect.x, min(circle[0], rect.x + rect.width))
    closest_y = max(rect.y, min(circle[1], rect.y + rect.height))

    # Calcula a distância entre o centro do circulo e o ponto mais proximo
    dx = circle[0] - closest_x
    dy = circle[1] - closest_y
    dist_squared = dx**2 + dy**2
    
    # Se a distância for menor que o raio houve colisão
    if dist_squared < circle[2]**2:
        if abs(dx) > abs(dy):
            return (True, False)
        else:
            return (False, True)
        
    return (False, False)


def generate_blocks(game, y=None) -> list[Block]:
    """Gera uma chunck de blocos"""
    collumns_qntd = 7
    rows_qntd = 4
    colors = ('blue', 'red', 'gold', 'green')

    blocks = []
    space = 5 # Espaçamento entre os blocos

    # Se nenhum y tiver sido informado, os blocos são criados a partir da posição 70
    if y != None:
        current_y = y
    else:
        current_y = 70

    # Index da cor atual
    color_index = 0
    # Cor atual
    current_color = colors[color_index]
    # Tamanho dos blocos
    block_width = 108
    block_height = 45

    for y in range(rows_qntd):
        current_x = space + 60 # Reseta a posição x para o inicio da tela

        for x in range(collumns_qntd):
            # Gera um numero aleatorio que indica que tipo de blocos sera
            random_num = random.randint(0, 100)
            if random_num <= 5:
                block = BallBlock(game, current_x, current_y, block_width, block_height, current_color)
            elif 5 <= random_num <= 10:
                block = BrickBlock(game, current_x, current_y, block_width, block_height, current_color)
            elif 10 <= random_num <= 15:
                block = InvisibleBlock(game, current_x, current_y, block_width, block_height, current_color)
            else:
                block = Block(game, current_x, current_y, block_width, block_height, current_color)
            blocks.append(block)
            # Atualiza a posição x que o proximo bloco deve ser colocado
            current_x = block.rect.right + space
        
        # Move o y atual para a linha de baixo
        current_y = block.rect.bottom + space
        # Atualiza a cor para a proxima linha de blocos
        color_index += 1
        if color_index >= len(colors):
            color_index = 0
        current_color = colors[color_index]

    return blocks


def get_higher_points() -> int:
    """Retorna a maior pontuação ja feita"""
    # Verifica se o arquivo existe
    if os.path.exists('data/highscore.txt'):
        with open('data/highscore.txt') as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    
    else:
        set_higher_points(0)
        return 0


def set_higher_points(points: int) -> None:
    with open('data/highscore.txt', 'w') as file:
        file.write(str(points))

    

def resolve_block_ball_collision(game, collision, block, ball):
    # Define se deve adicionar pontos ou não
    add_points = True

    if collision[0]:
        # Se a colisão foi horizontal, inverte a direção horizontal da bola
        ball.directions[0] *= -1
    if collision[1]:
        # Se a colisão foi vertical, inverte a direção vertical da bola
        ball.directions[1] *= -1
    
    block.state = 1 # Muda o estado do bloco para 1(destruindo)
    block.break_timer = 5 # Temporizador para o bloco desaparecer
    block.can_collide = False
    if block.type == 'ball':
        game.spawn_new_ball(list(block.rect.center), block.color)

    elif block.type == 'brick' and block.stage == 0:
        block.state = 0
        block.stage = 1
        block.can_collide = True
    
    elif block.type == 'invisible' and block.stage == 'invisible':
        block.collided = True
        block.state = 0
        block.can_collide = True
        if collision[0]:
            # Se a colisão foi horizontal, inverte a direção horizontal da bola
            ball.directions[0] *= -1
        if collision[1]:
            # Se a colisão foi vertical, inverte a direção vertical da bola
            ball.directions[1] *= -1
        add_points = False
    
    if add_points:
        # Atualiza os pontos do jogador 
        game.board.points += block.points 
        game.board.render()