import math
import random

import pyray


class Explosion:
    def __init__(self, cluster, pos, angle, speed):
        self.cluster = cluster
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed

        self.color = random.choice([pyray.RED, pyray.ORANGE, pyray.YELLOW, pyray.GOLD])

    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)
        if self.speed <= 0:
            self.cluster.explosions.remove(self)

    def render(self):
        render_points = [
            (self.pos[0] + math.cos(self.angle)*self.speed*random.randint(2,5),
             self.pos[1] + math.sin(self.angle)*self.speed*random.randint(2,5)),
            (self.pos[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * random.randint(2,5),
             self.pos[1] + math.sin(self.angle + math.pi * 0.5) * self.speed * random.randint(2,5)),
            (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * random.randint(2,5),
             self.pos[1] + math.sin(self.angle + math.pi) * self.speed * random.randint(2,5)),
            (self.pos[0] + math.cos(self.angle + math.pi * 1.5) * self.speed * random.randint(2,5),
             self.pos[1] + math.sin(self.angle + math.pi * 1.5) * self.speed * random.randint(2,5))
        ]

        pyray.draw_triangle(render_points[0], render_points[3], render_points[1], self.color)
        pyray.draw_triangle(render_points[2], render_points[1], render_points[3], self.color)