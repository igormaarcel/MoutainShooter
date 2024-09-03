from operator import truediv

from Code.Const import WIN_HEIGHT, WIN_WIDTH
from Code.enemy import Enemy
from Code.enemyShot import EnemyShot
from Code.entity import Entity
from Code.player import Player
from Code.playerShot import PlayerShot


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):  ## __ priva o metodo dentro da classe em que ele está
        ## e verifica se ele esta na janela (ent)
        if isinstance(ent, Enemy):  # se o inimigo passar da janela
            if ent.rect.right <= 0:
                ent.health = 0  # vida zera e ele sai da cena
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):  # verifica a colisão entre tiro e players/enemies
        valid_interaction = False
        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True

        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True

        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True

        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True

        if valid_interaction:  # comparação
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):
                #tomando dano
                ent1.health -= ent2.damage
                ent2.health -= ent1.damage

                #saber quem matou o inimigo
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]): # dando score para quem mata
        if enemy.last_dmg == 'Player1Shot':
            for ent in entity_list:
                if ent.name == 'Player1':
                    ent.score += enemy.score

        elif enemy.last_dmg == 'Player2Shot':
            for ent in entity_list:
                if ent.name == 'Player2':
                    ent.score += enemy.score



    @staticmethod
    def verify_collision(entity_list: list[Entity]):  # verifica a colisão
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)  # verifica se esta na janela
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list:
            if ent.health <= 0:
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)
                entity_list.remove(ent)  # remove da cena se a vida for < 0