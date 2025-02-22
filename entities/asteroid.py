import math
import random

import pyray


class Asteroid:
    def __init__(self, game, pos, radius, texture, velocity):
        self.game = game
        self.pos = list(pos)
        self.radius = radius
        self.texture = texture
        self.velocity = list(velocity)
        self.vapor_trail = []

    def render(self):
        pyray.draw_texture(self.texture, int(self.pos[0]), int(self.pos[1]), pyray.WHITE)

        for vapor_dot in self.vapor_trail.copy():
            pyray.draw_circle(vapor_dot[0], vapor_dot[1], vapor_dot[2], (255, 190, 51, 100))

    def update(self):
        # Remove if we've gone out of bounds
        if self.pos[1] < -50 or self.pos[1] > self.game.WINDOW_HEIGHT + 50 or self.pos[0] < -50 or self.pos[0] > self.game.WINDOW_WIDTH + 50:
            self.game.asteroid_list.remove(self)
            return

        # Check to see if we've been crushed
        for black_hole in self.game.black_hole_list:
            if pyray.check_collision_circles(self.pos, self.radius, black_hole.pos, black_hole.death_radius):
                self.game.asteroid_list.remove(self)
                self.game.create_new_explosion(self.pos, 15)
                return

        # Calculate velocity updates from black hole gravity
        for black_hole in self.game.black_hole_list:
            x_force, y_force = black_hole.calculate_force_on_object(self.pos[0], self.pos[1])
            self.velocity[0] += x_force
            self.velocity[1] += y_force

        # Calculate new position
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        # Update the vapor trail
        for vapor_dot in self.vapor_trail:
            vapor_dot[2] -= 0.1
            if vapor_dot[2] <= 0:
                self.vapor_trail.remove(vapor_dot)

        # Add vapor dots to the trail
        self.vapor_trail.append([int(self.pos[0] + self.texture.width / 2), int(self.pos[1] + self.texture.height / 2), 3.0])

    def get_collision_circle(self):
        pos_x = self.pos[0] + (self.texture.width / 2)
        pos_y = self.pos[1] + (self.texture.height / 2)
        radius = self.radius

        return int(pos_x), int(pos_y), radius