import pyray


class Asteroid:
    def __init__(self, game, pos, radius, texture, velocity):
        self.game = game
        self.pos = list(pos)
        self.radius = radius
        self.texture = texture
        self.velocity = list(velocity)

    def render(self):
        pyray.draw_texture(self.texture, int(self.pos[0]), int(self.pos[1]), pyray.WHITE)

    def update(self):
        # Remove if we've gone out of bounds
        if self.pos[1] < -50 or self.pos[1] > self.game.WINDOW_HEIGHT + 50 or self.pos[0] < -50 or self.pos[0] > self.game.WINDOW_WIDTH + 50:
            self.game.asteroid_list.remove(self)
            return

        # Check to see if we've been crushed
        for black_hole in self.game.black_hole_list:
            if pyray.check_collision_circles(self.pos, self.radius, black_hole.pos, black_hole.death_radius):
                self.game.asteroid_list.remove(self)
                return

        # Calculate velocity updates from black hole gravity
        for black_hole in self.game.black_hole_list:
            x_force, y_force = black_hole.calculate_force_on_object(self.pos[0], self.pos[1])
            self.velocity[0] += x_force
            self.velocity[1] += y_force

        # Calculate new position
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def get_collision_circle(self):
        pos_x = self.pos[0] + (self.texture.width / 2)
        pos_y = self.pos[1] + (self.texture.height / 2)
        radius = self.radius

        return int(pos_x), int(pos_y), radius