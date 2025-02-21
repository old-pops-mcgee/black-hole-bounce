import math
import pyray

class BlackHole:
    STANDARD_FORCE = 4000.0
    def __init__(self, game, pos, radius):
        self.game = game
        self.pos = list(pos)
        self.radius = radius
        self.force = self.STANDARD_FORCE

    def update(self):
        pass # TODO: Add animation effects on the black hole

    def render(self):
        # Render hole from out to in: RED -> ORANGE -> YELLOW -> BLACK
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius, pyray.RED)
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius*0.95, pyray.ORANGE)
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius * 0.9, pyray.YELLOW)
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius * 0.85, pyray.BLACK)

    def calculate_force_on_ball(self, ball_x, ball_y):
        angle = math.atan((self.pos[1] - ball_y) / (self.pos[0] - ball_x))
        dis = math.sqrt(math.pow(self.pos[1] - ball_y, 2) + math.pow(self.pos[0] - ball_x, 2))

        # Normal equation is G*(mass1*mass2)/dis^2
        # Gravity being applied separately, need to calculate component of force on each end
        # Hardcode force as something over the distance squared
        g_force = self.force / math.pow(dis, 2)
        x_force = abs(math.cos(angle) * g_force)
        if self.pos[0] < ball_x:
            # black hole to left of ball, so pull ball left
            x_force *= -1
        y_force = math.sin(angle) * g_force
        if self.pos[1] < ball_y:
            # black hole above ball, so pull ball up
            y_force *= -1

        return x_force, y_force