import math

import pyray

class Ship:
    MAX_SPEED = 5.0

    def __init__(self, game, pos, radius, color, texture):
        self.game = game
        self.pos = list(pos) # x,y
        self.radius = radius
        self.color = color
        self.angle = 0.0
        self.texture = texture
        self.velocity = [0.0, 0.0] # X velocity, Y velocity
        self.engine_speed = 0.0

    def render(self):
        pyray.draw_texture_pro(
            self.texture,
            pyray.Rectangle(0, 0, self.texture.width, self.texture.height),
            pyray.Rectangle(self.pos[0], self.pos[1], self.texture.width, self.texture.height),
            (self.texture.width / 2, self.texture.height / 2),
            self.angle * (180 / math.pi) + 90,
            pyray.WHITE
        )

    def update(self):
        # Blow up if we've gone out of bounds
        if self.pos[1] < 0 or self.pos[1] > self.game.WINDOW_HEIGHT or self.pos[0] < 0 or self.pos[0] > self.game.WINDOW_WIDTH:
            self.game.game_over = True
            return

        # Blow up if we've collided with an asteroid
        for asteroid in self.game.asteroid_list:
            ax, ay, ar = asteroid.get_collision_circle()
            if pyray.check_collision_circles(self.pos, self.radius, (ax, ay), ar):
                self.game.game_over = True
                return

        # Check to see if we've been crushed
        for black_hole in self.game.black_hole_list:
            if pyray.check_collision_circles(self.pos, self.radius, black_hole.pos, black_hole.death_radius):
                self.game.game_over = True
                return

        # Calculate velocity updates from black hole gravity
        for black_hole in self.game.black_hole_list:
            x_force, y_force = black_hole.calculate_force_on_object(self.pos[0], self.pos[1])
            self.velocity[0] += x_force
            self.velocity[1] += y_force

        # Calculate new position
        self.pos[0] += math.cos(self.angle)*self.engine_speed + self.velocity[0]
        self.pos[1] += math.sin(self.angle)*self.engine_speed + self.velocity[1]

        # Cap velocities so we don't get TOO crazy
        self.velocity[0] = min(self.MAX_SPEED, max(-self.MAX_SPEED, self.velocity[0]))
        self.velocity[1] = min(self.MAX_SPEED, max(-self.MAX_SPEED, self.velocity[1]))

