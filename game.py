import math
import random

import pyray

from entities.ball import Ball
from entities.black_hole import BlackHole
from entities.point import Point


class Game:
    WINDOW_HEIGHT = 800
    WINDOW_WIDTH = 1200
    MAX_POINTS = 5

    def __init__(self):
        pyray.init_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Black Hole Bounce")
        pyray.init_audio_device()

        pyray.set_target_fps(60)

        # Instantiate the core components
        self.reload_game_components()

    def reload_game_components(self):
        self.ball = Ball(self, (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2), 5, pyray.YELLOW)
        self.black_hole_list = []
        self.point_list = []
        for i in range(self.MAX_POINTS):
            self.point_list.append(self.generate_random_point())
        self.game_over = False
        self.score = 0

    def update(self):
        if self.game_over:
            self.reload_game_components() # TODO: Pretty up the transition
        self.ball.update()
        for black_hole in self.black_hole_list:
            black_hole.update()
        for point in self.point_list:
            point.update()

    def run(self):
        while not pyray.window_should_close():
            self.handle_input()
            self.update()
            self.render()

        pyray.close_audio_device()
        pyray.close_window()


    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.DARKPURPLE)

        # Game elements
        self.ball.render()
        for point in self.point_list:
            point.render()
        for black_hole in self.black_hole_list:
            black_hole.render()

        # UI elements
        pyray.draw_text(f"Score: {self.score}", 10, 10, 20, pyray.RAYWHITE)

        pyray.end_drawing()

    def handle_input(self):
        if pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT):
            self.ball.angle += math.pi/60
        if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT):
            self.ball.angle -= math.pi/60
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_UP):
            self.ball.engine_speed += 0.5
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
            self.ball.engine_speed -= 0.5

    def score_point(self, point):
        self.score += 100
        self.point_list.remove(point)
        self.point_list.append(self.generate_random_point())

    def add_black_hole(self, pos):
        self.black_hole_list.append(BlackHole(self, pos, 45.0))

    def generate_random_point(self):
        point_x = random.randrange(0, self.WINDOW_WIDTH)
        point_y = random.randrange(0, self.WINDOW_HEIGHT)
        rotation = random.randrange(0, 72)
        return Point(self, (point_x, point_y), 5, 15.0, pyray.GOLD, rotation)