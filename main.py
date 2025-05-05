import pygame as pg

from data.scripts.utils import *
from data.scripts.color import *
from data.scripts.player import *
from data.scripts.ball import *
from data.scripts.block import *
from data.scripts.board import *
from data.scripts.animations import *

pg.init()


class Game:
    """Classe principal do jogo, responsavel por gerenciar aspectos gerais"""

    def __init__(self):
        self.init()
        self.state = 0 # Indica o estado do jogo -> 0: Não iniciado, 1: Rodando, 2: Pausado
        self.lifes = 3 # Quantidade de vidas do jogador

        # Cria o player e o centraliza horizontalmente
        self.player = Player(self, 0, 0, 150, 15)
        self.player.rect.centerx = self.screen.get_width() / 2
        self.player.rect.bottom = self.screen.get_height() - 100
        # Cria a bola e a posiciona acima do jogador
        self.balls = [
            Ball(self, [self.player.rect.centerx, self.player.rect.y-25], 17, 'white')
        ]
        # Cria o "quadro" que mostra a quantidade de vida e pontos do jogador
        self.board = Board(self)

        # Gera os blocos
        self.blocks: list[Block] = generate_blocks(self)
        self.new_blocks_animation = NewBlocksAnimation(120)

        # Carrega os assets dos blocos
        self.assets = {
            'red': load_images('/red'),
            'blue': load_images('/blue'),
            'green': load_images('/green'),
            'gold': load_images('/gold'),
        }

        self.colors = {
            'white': (255, 255, 255),
            'red': (237, 84, 84),
            'green': (11, 174, 25),
            'gold': (230, 214, 36),
            'blue': (71, 76, 235)
        }

        # Define o nome da janela
        pg.display.set_caption('Breakout')

    def run(self):
        """Roda o loop principal"""
        delta_time = 0
        while True:
            self.screen.fill((28,24,31)) # Preenche a tela de preto
            check_events(self)

            # Checa a animação de descida dos blocos
            self.new_blocks_animation.check_delay()
            if self.new_blocks_animation.on_animation:
                self.new_blocks_animation.update(self.blocks, delta_time)

            # Desenha os elementos do quadro
            self.board.draw(self.screen)

            # Atualiza a posição do player e o desenha na tela
            self.player.update(delta_time)
            self.player.draw(self.screen)

            # Atualiza a posição da bola e a colisão com o player
            for ball in self.balls.copy():
                ball.update(delta_time)
                if ball.center[1] - ball.radius - 10 > self.screen.get_height():
                    self.balls.remove(ball)

                ball.check_player_collision(self.player)

            for block in self.blocks.copy():

                # Se o bloco estiver no estado 1 ou 2(estados de destruição), atualiza seu temporizador de destruição
                if block.state == 1 or block.state == 2:
                    block.update()

                # Se o bloco estiver completamente destruido, o remove da tela
                elif block.state == -1:
                    self.blocks.remove(block)

                # Se o bloco estiver no estado 0(estado ativo), verifica colisão com a bola
                elif block.state == 0 and block.can_collide:
                    collided = False
                    for ball in self.balls:
                        collision = check_collision_circle_rect(ball.get_list(), block.rect)

                        if collision[0] or collision[1]:
                            resolve_block_ball_collision(self, collision, block, ball)
                            collided = True
                            break

                    if not collided and block.type == 'invisible':
                        if block.collided and block.stage == 'invisible':
                            block.stage = 'visible'

                    if collided:
                        break

            # Verifica se todos os blocos foram destruidos
            if len(self.blocks) == 0:
                # Gera novos blocos acima da tela
                self.blocks = generate_blocks(self, -200)
                # Inicia contador do delay para o inicio da animação de descida
                self.new_blocks_animation.delay = 30
                # Move o y da animação para o primeiro bloco, para que ele acompanhe os blocos na descida
                self.new_blocks_animation.y = self.blocks[0].rect.y
                Ball.speed *= 1.2
            
            # Desenha os blocos
            for block in self.blocks:
                block.draw(self.screen)

            # Desenha as bolas
            for ball in self.balls:
                ball.draw(self.screen)


            # Verifica se o jogo deve ser resetado
            if len(self.balls) == 0:
                self.lifes -= 1
                if self.lifes != 0:
                    self.reset_game()

            # Reseta o jogo se o jogador perder todas as vidas
            if self.lifes == 0:
                self.lifes = 3
                self.reset_game(True)
                # Inicia contador do delay para o inicio da animação de descida
                self.new_blocks_animation.delay = 30
                # Move o y da animação para o primeiro bloco, para que ele acompanhe os blocos na descida
                self.new_blocks_animation.y = self.blocks[0].rect.y

            pg.display.flip()
            delta_time = self.clock.tick(60) / 1000

    def reset_game(self, total_reset=False):
        """Faz o processo de reset do jogo"""
        # Move o jogador e a bola de volta para a posição inicial
        self.player.rect.centerx = self.screen.get_width() / 2

        # Reseta o estado do jogo
        self.state = 0

        self.balls = [
            Ball(self, [self.player.rect.centerx, self.player.rect.y-25], 17, 'white')
        ]

        if total_reset:
            # Cria novos blocos
            self.blocks = generate_blocks(self, -200)

            points = get_higher_points()
            
            if points < self.board.points:
                set_higher_points(self.board.points)

            self.state = 3

            Ball.speed = 600
    
    def spawn_new_ball(self, pos: list, color: str):
        new_ball = Ball(self, pos.copy(), 17, color)
        angle = random.uniform(math.radians(30), math.radians(150))
        new_ball.directions = [math.cos(angle), math.sin(angle)]
        self.balls.append(new_ball)

    def init(self):
        """Inicializa a tela e o relogio do pygame"""
        self.screen = pg.display.set_mode((920, 850)) # Inicia a tela
        self.clock = pg.time.Clock() # Inicia o relogio


Game().run()