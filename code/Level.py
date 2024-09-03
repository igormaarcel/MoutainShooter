#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
from asyncio import timeout

import pygame.display
from pygame import Surface, Rect
from pygame.font import Font

from Code.Const import C_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME, C_GREEN, C_CYAN, EVENT_TIMEOUT, \
    TIMEOUT_STEP, TIMEOUT_LEVEL3
from Code.background import Background
from Code.enemy import Enemy
from Code.entity import Entity
from Code.entityFactory import EntityFactory
from Code.entityMediator import EntityMediator
from Code.player import Player
from Code.enemy import  Enemy



class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL3
        self.timeout3 = TIMEOUT_LEVEL3
        self.window = window
        self.name = name
        self.game_mode = game_mode  # Modo do jogo
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]  # score do p1
        self.entity_list.append(player)
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:  # criação do player2
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]  # score do p2
            self.entity_list.append(player)  # adicionando na cena
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)  # 100ms


    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./Assets/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        pygame.mixer_music.set_volume(0.1)
        clock = pygame.time.Clock()

        if self.name == 'Level3':  # Checa se está na fase 3
            self.timeout = TIMEOUT_LEVEL3 # Muda o tempo da fase 3


        while True:
            clock.tick(60)
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()

                if isinstance(ent, (Player, Enemy)):  # os tiros vem do player ou inimigo
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)
                if ent.name == 'Player1':  # mostrando HUD
                    self.level_text(14, f'Player 1 - Health: {ent.health} || Score: {ent.score}', C_GREEN, (10, 25))
                if ent.name == 'Player2':  # mostrando HUD
                    self.level_text(14, f'Player 2 - Health: {ent.health} || Score: {ent.score}', C_CYAN, (10, 40))



            for event in pygame.event.get():  # checa eventos
                if event.type == pygame.QUIT:  # se fecha a janela
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:  # spawn inimigos
                    if self.name == 'Level1' or self.name == 'Level2':
                        choice = random.choice(('Enemy1', 'Enemy2'))
                        self.entity_list.append(EntityFactory.get_entity(choice))
                if self.name == 'Level3':
                    if event.type == EVENT_ENEMY:  # spawn inimigos
                        self.entity_list.append(EntityFactory.get_entity('Enemy3'))







                if event.type == EVENT_TIMEOUT: # checa o contador a cada seg
                    self.timeout -= TIMEOUT_STEP

                    if self.timeout == 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == "Player1":
                                player_score[0] = ent.score
                            if isinstance(ent, Player) and ent.name == "Player2":
                                player_score[1] = ent.score

                        return True  # volta para verificar a fase do jogo game.py

                found_player = False
                for ent in self.entity_list:
                    if isinstance(ent, Player):
                        found_player = True

                if not found_player:
                    return False

            # printando texto LEVEL e TEMPO de jogo, FPS e ENTIDADE

            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))
            pygame.display.flip()

            # verify collision and health
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
