import pyray

class Point:
    def __init__(self, game, pos, sides, radius, color, rotation):
        self.game = game
        self.pos = list(pos)
        self.sides = sides
        self.radius = radius
        self.color = color
        self.rotation = rotation

    def update(self):
        self.rotation += 0.1

    def render(self):
        pyray.draw_poly(self.pos, self.sides, self.radius, self.rotation, self.color)