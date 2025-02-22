import math
import random

import pyray

from entities.ship import Ship
from entities.black_hole import BlackHole
from entities.star import Star
from utilities import raylib_utils


class Game:
    WINDOW_HEIGHT = 972
    WINDOW_WIDTH = 1728
    MAX_STARS = 5

    def __init__(self):
        pyray.init_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Black Hole Bounce")
        pyray.init_audio_device()

        pyray.set_target_fps(60)

        # Load assets
        self.images = {
            'ship': raylib_utils.load_image_to_texture('ship.png'),
            'star': raylib_utils.load_image_to_texture('star.png'),
            'asteroid': raylib_utils.load_image_to_texture('asteroid.png'),
            'black_hole': raylib_utils.load_image_to_texture('black_hole.png')
        }

        # Instantiate the core components
        self.reload_game_components()



    def reload_game_components(self):
        self.ship = Ship(self, (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2), 5, pyray.YELLOW, self.images['ship'])
        self.black_hole_list = []
        self.star_list = []
        for i in range(self.MAX_STARS):
            self.star_list.append(self.generate_random_star())
        self.game_over = False
        self.score = 0

    def update(self):
        if self.game_over:
            self.reload_game_components() # TODO: Pretty up the transition
        self.ship.update()
        for black_hole in self.black_hole_list:
            black_hole.update()
        for point in self.star_list:
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
        self.ship.render()
        for point in self.star_list:
            point.render()
        for black_hole in self.black_hole_list:
            black_hole.render()

        # UI elements
        pyray.draw_text(f"Score: {self.score}", 10, 10, 20, pyray.RAYWHITE)

        pyray.end_drawing()

    def handle_input(self):
        if pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT):
            self.ship.angle += math.pi / 60
        if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT):
            self.ship.angle -= math.pi / 60
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_UP):
            self.ship.engine_speed += 0.5
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
            self.ship.engine_speed -= 0.5

    def score_point(self, point):
        self.score += 100
        self.star_list.remove(point)
        self.star_list.append(self.generate_random_star())

    def add_black_hole(self, pos):
        self.black_hole_list.append(BlackHole(self, pos, 45.0, self.images['black_hole']))

    def generate_random_star(self):
        point_x = random.randrange(20, self.WINDOW_WIDTH - 20)
        point_y = random.randrange(20, self.WINDOW_HEIGHT - 20)
        return Star(self, (point_x, point_y), 5, self.images['star'])