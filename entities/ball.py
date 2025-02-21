import math

import pyray

class Ball:
    def __init__(self, game, pos, radius, color):
        self.game = game
        self.pos = list(pos) # x,y
        self.radius = radius
        self.color = color

        self.velocity = [0.0, 5.0] # X velocity, Y velocity

    def render(self):
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius, self.color)

    def update(self):
        # Adjust for impulse from paddle
        if pyray.check_collision_circle_rec(self.pos, self.radius, self.game.paddle.get_pyray_rec()):
            self.velocity[1] = -10.0

        # Adjust if we are colliding with the walls
        if self.pos[1] <= 0:
            self.velocity[1] = 10.0

        if self.pos[0] <= 0:
            self.velocity[0] = 10.0

        if self.pos[0] >= self.game.WINDOW_WIDTH:
            self.velocity[0] = -10.0

        # Calculate new position
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        # Calculate velocity updates from downwards gravity
        self.velocity[1] += 0.1 # Natural gravity + impact from black hole

        # Calculate velocity updates from black hole gravity
        for black_hole in self.game.black_hole_list:
            x_force, y_force = black_hole.calculate_force_on_ball(self.pos[0], self.pos[1])
            self.velocity[0] += x_force
            self.velocity[1] += y_force

        # Cap velocities so we don't get TOO crazy
        self.velocity[0] = min(10.0, self.velocity[0])
        self.velocity[1] = min(10.0, self.velocity[1])