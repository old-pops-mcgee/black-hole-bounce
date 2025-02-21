import pyray

class Paddle:
    def __init__(self, game, pos, height, width, color):
        self.game = game
        self.pos = list(pos) # x,y
        self.height = height
        self.width = width
        self.color = color

    def render(self):
        pyray.draw_rectangle(self.pos[0], self.pos[1], self.width, self.height, self.color)

    def update(self):
        pass

    def get_pyray_rec(self):
        return pyray.Rectangle(self.pos[0], self.pos[1], self.width, self.height)