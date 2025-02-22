import random

import pyray

class Point:
    def __init__(self, game, pos, sides, radius, color, rotation):
        self.game = game
        self.pos = list(pos)
        self.sides = sides
        self.radius = radius
        self.rotation = rotation

        self.time_to_detonation = random.randint(300, 600)
        self.detonation_counter = self.time_to_detonation

    def update(self):
        self.rotation += 0.1
        self.detonation_counter -= 1

        if self.detonation_counter == 0:
            self.game.point_list.remove(self)
            self.game.add_black_hole(self.pos)

    def render(self):
        color = pyray.YELLOW
        if self.detonation_counter < (self.time_to_detonation * (2/3)):
            color = pyray.ORANGE
        if self.detonation_counter < (self.time_to_detonation * (1/3)):
            color = pyray.RED
        pyray.draw_poly(self.pos, self.sides, self.radius, self.rotation, color)