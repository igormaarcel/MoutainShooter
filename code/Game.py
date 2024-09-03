from sys import platform

import pygame

import code.Const
from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Score import Score
from code.Level import Level
from code.Menu import Menu


# !/usr/bin/python
# -*- coding: utf-8 -*-

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))


    def run(self):

        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()
            actual_fase = ''

            if menu_return in [MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]]: #chamando a primeira fase
                actual_fase = '1'
                player_score = [0, 0]  # [Player1, Player2]
                level = Level(self.window, 'Level1', menu_return, player_score)
                level_return = level.run(player_score) # se ganhar
                if level_return: # chamando level 2
                    actual_fase = '2'
                    level = Level(self.window, 'Level2', menu_return, player_score)
                    level_return = level.run(player_score)
                    if level_return: # chamando level 3
                        actual_fase = '3'
                        level = Level(self.window, 'Level3', menu_return, player_score)
                        level_return = level.run(player_score)
                        if level_return:
                            score.save(menu_return, player_score)

            elif menu_return == MENU_OPTION[3]:
                score.show()

            elif menu_return == MENU_OPTION[4]:
                pygame.quit()
                quit()
            else:
                pass
