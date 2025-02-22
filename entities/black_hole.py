import math
import pyray

class BlackHole:
    STANDARD_FORCE = 2500.0
    FUDGE_FACTOR = 3.5
    DECAYING_FORCE_ADDER = 20.0
    DECAY_RATE = 0.25
    def __init__(self, game, pos, radius):
        self.game = game
        self.pos = list(pos)
        self.radius = radius
        self.force = self.STANDARD_FORCE
        self.level = 1
        self.death_radius = 0.2*self.radius

    def update(self):
        # TODO: Add animation effects on the black hole
        self.radius -= self.DECAY_RATE
        self.death_radius -= 0.2*self.DECAY_RATE
        self.force += self.DECAYING_FORCE_ADDER
        if self.radius < self.DECAY_RATE:
            self.game.black_hole_list.remove(self)

    def render(self):
        # Render hole from out to in: RED -> ORANGE -> YELLOW -> BLACK
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius, pyray.RED)
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius*0.95, pyray.ORANGE)
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius * 0.9, pyray.YELLOW)
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius * 0.85, pyray.BLACK)

        # Render 'death radius' that crushes ball
        pyray.draw_circle(int(self.pos[0]), int(self.pos[1]), self.death_radius, pyray.DARKPURPLE)

    def calculate_force_on_ball(self, ball_x, ball_y):
        angle = math.atan2((self.pos[1] - ball_y), (self.pos[0] - ball_x))
        dis = math.sqrt(math.pow(self.pos[1] - ball_y, 2) + math.pow(self.pos[0] - ball_x, 2))

        # Normal equation is G*(mass1*mass2)/dis^2
        # Gravity being applied separately, need to calculate component of force on each end
        # Hardcode force as something over the distance squared
        # Add a 'fudge factor' to give players more reaction time
        g_force = self.force / (self.FUDGE_FACTOR*math.pow(dis, 2))
        x_force = math.cos(angle) * g_force
        y_force = math.sin(angle) * g_force

        return x_force, y_force