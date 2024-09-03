#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from Code.Const import ENTITY_SPEED, WIN_WIDTH, ENTITY_SHOT_DELAY, WIN_HEIGHT
from Code.enemyShot import EnemyShot
from Code.entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.vertical_speed = 1.5
        self.direction = 1  # 1 sobe | -1 desce

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]  # velocidade do Enemy

        if self.name == 'Enemy3':
            self.rect.x -= self.speed
            self.rect.y += self.vertical_speed * self.direction
            if self.rect.top <= 0:
                self.direction = 1
                self.vertical_speed = 4
            elif self.rect.bottom >= pygame.display.get_surface().get_height():
                self.vertical_speed = 2
                self.direction = -1


    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))