import math
import random

import pyray

class Star:
    RENDER_SCALE = 2.0
    def __init__(self, game, pos, radius, texture):
        self.game = game
        self.pos = list(pos)
        self.radius = radius
        self.texture = texture
        self.angle = random.random() * 2*math.pi
        self.turning_direction = random.randint(0, 1)

        self.time_to_detonation = random.randint(300, 600)
        self.detonation_counter = self.time_to_detonation

    def update(self):
        if self.turning_direction:
            self.angle += math.pi / 120
        else:
            self.angle -= math.pi / 120
        self.detonation_counter -= 1

        if self.detonation_counter == 0:
            self.game.star_list.remove(self)
            self.game.add_black_hole(self.pos)

    def render(self):
        color = pyray.YELLOW
        if self.detonation_counter < (self.time_to_detonation * (2/3)):
            color = pyray.ORANGE
        if self.detonation_counter < (self.time_to_detonation * (1/3)):
            color = pyray.RED

        pyray.draw_texture_pro(
            self.texture,
            pyray.Rectangle(0, 0, self.texture.width, self.texture.height),
            pyray.Rectangle(self.pos[0], self.pos[1], self.texture.width * self.RENDER_SCALE, self.texture.height * self.RENDER_SCALE),
            ((self.texture.width / 2) * self.RENDER_SCALE, (self.texture.height / 2) * self.RENDER_SCALE),
            self.angle * (180 / math.pi),
            color
        )
        #pyray.draw_poly(self.pos, self.sides, self.radius, self.rotation, color)