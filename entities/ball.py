import math

import pyray

class Ball:
    MAX_SPEED = 5.0

    def __init__(self, game, pos, radius, color):
        self.game = game
        self.pos = list(pos) # x,y
        self.radius = radius
        self.color = color

        self.velocity = [0.0, 0.0] # X velocity, Y velocity

    def render(self):
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius, self.color)

    def update(self):

        # Check to see if we've scored
        for point in self.game.point_list:
            if pyray.check_collision_circles(self.pos, self.radius, point.pos, point.radius):
                self.game.score_point(point)

        # Adjust if we are colliding with the walls
        if self.pos[1] < 0 or self.pos[1] > self.game.WINDOW_HEIGHT:
            self.velocity[1] *= -1

        if self.pos[0] < 0 or self.pos[0] > self.game.WINDOW_WIDTH:
            self.velocity[0] *= -1

        # Check to see if we've been crushed
        for black_hole in self.game.black_hole_list:
            if pyray.check_collision_circles(self.pos, self.radius, black_hole.pos, black_hole.death_radius):
                self.game.game_over = True
                return

        # Calculate new position
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        # Calculate velocity updates from black hole gravity
        for black_hole in self.game.black_hole_list:
            x_force, y_force = black_hole.calculate_force_on_ball(self.pos[0], self.pos[1])
            self.velocity[0] += x_force
            self.velocity[1] += y_force

        # Cap velocities so we don't get TOO crazy
        self.velocity[0] = min(self.MAX_SPEED, max(-self.MAX_SPEED, self.velocity[0]))
        self.velocity[1] = min(self.MAX_SPEED, max(-self.MAX_SPEED, self.velocity[1]))