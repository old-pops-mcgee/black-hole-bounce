import random

import pyray

from entities.ball import Ball
from entities.black_hole import BlackHole
from entities.paddle import Paddle
from entities.point import Point


class Game:
    WINDOW_HEIGHT = 640
    WINDOW_WIDTH = 480
    MAX_BLACK_HOLES = 3

    def __init__(self):
        pyray.init_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Black Hole Bounce")
        pyray.init_audio_device()

        pyray.set_target_fps(60)

        # Instantiate the core components
        self.reload_game_components()

    def reload_game_components(self):
        self.paddle = Paddle(self, (165, 600), 5, 150, pyray.SKYBLUE)
        self.ball = Ball(self, (240, 250), 5, pyray.YELLOW)
        self.black_hole_list = []
        self.black_hole_count = 0
        self.point_list = []
        self.point_list.append(Point(self, (240, 100), 5, 15.0, pyray.GOLD, 0))
        for i in range(4):
            self.point_list.append(self.generate_random_point())
        self.game_over = False
        self.score = 0
        self.counter_to_game_over = 600 # 10 s

    def update(self):
        if self.game_over:
            self.reload_game_components() # TODO: Pretty up the transition
        self.paddle.update()
        self.ball.update()
        for point in self.point_list:
            point.update()
        self.counter_to_game_over -= 1
        if self.counter_to_game_over == 0:
            self.reload_game_components()

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
        self.paddle.render()
        self.ball.render()
        for point in self.point_list:
            point.render()
        for black_hole in self.black_hole_list:
            black_hole.render()

        # UI elements
        pyray.draw_text(f"Score: {self.score}", 10, 10, 20, pyray.RAYWHITE)
        pyray.draw_text(f"Black Holes Left: {self.MAX_BLACK_HOLES - self.black_hole_count}", 10, 30, 20,
                        pyray.RAYWHITE)
        pyray.draw_text(f"Time Left: {int(self.counter_to_game_over / 60) + 1}", 10, 50, 20, pyray.RAYWHITE)

        pyray.end_drawing()

    def handle_input(self):
        if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            if self.black_hole_count < self.MAX_BLACK_HOLES:
                # add a black hole
                mouse_position = pyray.get_mouse_position()
                processed_click = False
                for black_hole in self.black_hole_list:
                    if pyray.check_collision_point_circle(mouse_position, black_hole.pos, black_hole.radius):
                        black_hole.force += black_hole.STANDARD_FORCE
                        black_hole.radius += 10.0
                        processed_click = True
                if not processed_click:
                    self.black_hole_list.append(BlackHole(self, (mouse_position.x, mouse_position.y), 45.0))
                self.black_hole_count += 1
        if pyray.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_RIGHT):
            mouse_position = pyray.get_mouse_position()
            for black_hole in self.black_hole_list.copy():
                if pyray.check_collision_point_circle(mouse_position, black_hole.pos, black_hole.radius):
                    black_hole_level = int(black_hole.force / black_hole.STANDARD_FORCE)
                    if black_hole_level == 1:
                        self.black_hole_list.remove(black_hole)
                    else:
                        black_hole.force -= black_hole.STANDARD_FORCE
                        black_hole.radius -= 10.0
                    self.black_hole_count -= 1

    def score_point(self, point):
        self.score += 100
        self.point_list.remove(point)
        self.point_list.append(self.generate_random_point())
        self.counter_to_game_over = 600

    def generate_random_point(self):
        point_x = random.randrange(0, self.WINDOW_WIDTH)
        point_y = random.randrange(0, self.WINDOW_HEIGHT)
        rotation = random.randrange(0, 72)
        return Point(self, (point_x, point_y), 5, 15.0, pyray.GOLD, rotation)