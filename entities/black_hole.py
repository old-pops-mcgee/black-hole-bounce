import math
import random

import pyray

class BlackHole:
    STANDARD_FORCE = 2500.0
    FUDGE_FACTOR = 3.5
    DECAYING_FORCE_ADDER = 20.0
    DECAY_RATE = 0.25
    RENDER_SCALE = 3.5
    def __init__(self, game, pos, radius, texture):
        self.game = game
        self.pos = list(pos)
        self.initial_radius = radius
        self.radius = radius
        self.force = self.STANDARD_FORCE
        self.level = 1
        self.death_radius = 0.2*self.radius
        self.texture = texture
        self.angle = random.random() * 2*math.pi
        self.turning_direction = random.randint(0, 1)
        self.rotation_speed = random.random() * math.pi / 15

    def update(self):
        self.radius -= self.DECAY_RATE
        self.death_radius -= 0.2*self.DECAY_RATE
        self.force += self.DECAYING_FORCE_ADDER
        if self.turning_direction:
            self.angle += self.rotation_speed
        else:
            self.angle -= self.rotation_speed
        if self.radius < self.DECAY_RATE:
            self.game.black_hole_list.remove(self)
            self.game.star_list.append(self.game.generate_random_star())

    def render(self):
        scale = self.radius / self.initial_radius
        pyray.draw_texture_pro(
            self.texture,
            pyray.Rectangle(0, 0, self.texture.width, self.texture.height),
            pyray.Rectangle(
                self.pos[0],
                self.pos[1],
                self.RENDER_SCALE * self.texture.width * scale,
                self.RENDER_SCALE * self.texture.height * scale
            ),
            ((self.texture.width / 2) * self.RENDER_SCALE * scale, (self.texture.height / 2) * self.RENDER_SCALE * scale),
            self.angle * (180 / math.pi),
            pyray.WHITE
        )

    def calculate_force_on_object(self, obj_x, obj_y):
        angle = math.atan2((self.pos[1] - obj_y), (self.pos[0] - obj_x))
        dis = math.sqrt(math.pow(self.pos[1] - obj_y, 2) + math.pow(self.pos[0] - obj_x, 2))

        # Normal equation is G*(mass1*mass2)/dis^2
        # Gravity being applied separately, need to calculate component of force on each end
        # Hardcode force as something over the distance squared
        # Add a 'fudge factor' to give players more reaction time
        g_force = self.force / (self.FUDGE_FACTOR*math.pow(dis, 2))
        x_force = math.cos(angle) * g_force
        y_force = math.sin(angle) * g_force

        return x_force, y_force