import math
import random

from entities.explosion import Explosion


class ExplosionCluster:
    def __init__(self, game, pos, explosion_count):
        self.game = game
        self.pos = list(pos)
        self.explosions = []

        for i in range(explosion_count):
            pos_x = self.pos[0] + random.randrange(-5, 5)
            pos_y = self.pos[1] + random.randrange(-5, 5)
            self.explosions.append(Explosion(self, (pos_x, pos_y), random.random() * 2 * math.pi, random.random() * 5.0))

    def render(self):
        for explosion in self.explosions:
            explosion.render()

    def update(self):
        for explosion in self.explosions:
            explosion.update()

        if len(self.explosions) == 0:
            self.game.explosion_list.remove(self)
