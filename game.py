import math
import random

import pyray

from entities.asteroid import Asteroid
from entities.explosion_cluster import ExplosionCluster
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
            'black_hole': raylib_utils.load_image_to_texture('black_hole.png'),
            'background': raylib_utils.load_image_to_texture('background.png')
        }
        pyray.set_window_icon(pyray.load_image('assets/images/icon.png'))

        self.sounds = {
            'music': pyray.load_sound('assets/sound/scifi_background.wav'),
            'explosion': pyray.load_sound('assets/sound/explosion.wav'),
            'engine': pyray.load_sound('assets/sound/engine.wav')
        }

        pyray.play_sound(self.sounds['music'])

        # Instantiate the core components
        self.reload_game_components()



    def reload_game_components(self):
        self.ship = Ship(self, (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2), 5, pyray.YELLOW, self.images['ship'])
        self.black_hole_list = []
        self.star_list = []
        self.asteroid_list = []
        self.explosion_list = []
        self.added_final_explosion = False
        self.restart_counter = 120
        self.asteroid_countdown_range = (180, 300)
        self.star_addition_countdown = 1800 # Get harder every 30 seconds
        self.star_multiplier = 1
        self.asteroid_countdown = random.randint(self.asteroid_countdown_range[0], self.asteroid_countdown_range[1])
        for i in range(self.MAX_STARS):
            self.star_list.append(self.generate_random_star())
        self.score = 0

    def update(self):
        if not pyray.is_sound_playing(self.sounds['music']):
            pyray.play_sound(self.sounds['music'])
        if self.ship.is_dead:
            if not self.added_final_explosion:
                self.create_new_explosion(self.ship.pos, 50)
                self.added_final_explosion = True
            self.restart_counter -= 1
        if self.restart_counter <= 0:
            self.reload_game_components() # TODO: Pretty up the transition
        self.asteroid_countdown -= 1
        self.star_addition_countdown -= 1
        if not self.ship.is_dead:
            self.score += 1
        if self.asteroid_countdown <= 0:
            self.create_new_asteroid()
        if self.star_addition_countdown <= 0:
            self.star_multiplier = min(5, self.star_multiplier + 1)
            self.star_addition_countdown = 1800
        self.ship.update()
        for black_hole in self.black_hole_list:
            black_hole.update()
        for point in self.star_list:
            point.update()
        for asteroid in self.asteroid_list:
            asteroid.update()
        for explosion in self.explosion_list:
            explosion.update()

    def run(self):
        while not pyray.window_should_close():
            self.handle_input()
            self.update()
            self.render()

        pyray.close_audio_device()
        pyray.close_window()


    def render(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)

        # Background
        pyray.draw_texture(self.images['background'], 0, 0, (255, 255, 255, 100))
        # Game elements
        for point in self.star_list:
            point.render()
        for black_hole in self.black_hole_list:
            black_hole.render()
        for asteroid in self.asteroid_list:
            asteroid.render()
        for explosion in self.explosion_list:
            explosion.render()
        self.ship.render()

        # UI elements
        pyray.draw_text(f"Score: {self.score}", 10, 10, 20, pyray.RAYWHITE)

        pyray.end_drawing()

    def handle_input(self):
        if pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT):
            self.ship.angle += math.pi / 60
        if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT):
            self.ship.angle -= math.pi / 60
        if pyray.is_key_down(pyray.KeyboardKey.KEY_UP):
            self.ship.increase_speed()
        if pyray.is_key_down(pyray.KeyboardKey.KEY_DOWN):
            self.ship.decrease_speed()

    def add_black_hole(self, pos):
        self.black_hole_list.append(BlackHole(self, pos, 45.0, self.images['black_hole']))

    def generate_random_star(self):
        point_x = random.randrange(20, self.WINDOW_WIDTH - 20)
        point_y = random.randrange(20, self.WINDOW_HEIGHT - 20)
        return Star(self, (point_x, point_y), 5, self.images['star'])

    def create_new_asteroid(self):
        # First determine which edge of the screen we're coming from
        side = random.randint(0, 3)
        initial_velocity = [0, 0]
        direction_of_free_side = random.choice([-1, 1]) # We should aim for screen, but there's a free axis
        pos = [0,0]
        velocity_scale = random.random() * 20.0
        match side:
            case 0:
                # Top side
                pos[0] = random.randint(40, self.WINDOW_WIDTH - 40)
                pos[1] = self.WINDOW_HEIGHT - 20
                initial_velocity[0] = random.random() * direction_of_free_side * velocity_scale
                initial_velocity[1] = random.random() * velocity_scale
            case 1:
                # Right side
                pos[0] = self.WINDOW_WIDTH + 20
                pos[1] = random.randint(40, self.WINDOW_HEIGHT - 40)
                initial_velocity[0] = random.random() * -velocity_scale
                initial_velocity[1] = random.random() * direction_of_free_side * velocity_scale
            case 2:
                pos[0] = random.randint(40, self.WINDOW_WIDTH - 40)
                pos[1] = self.WINDOW_HEIGHT + 20
                initial_velocity[0] = random.random() * direction_of_free_side * velocity_scale
                initial_velocity[1] = random.random() * -velocity_scale
            case _:
                # Left side
                pos[0] = self.WINDOW_WIDTH - 20
                pos[1] = random.randint(40, self.WINDOW_HEIGHT - 40)
                initial_velocity[0] = random.random() * velocity_scale
                initial_velocity[1] = random.random() * direction_of_free_side * velocity_scale

        self.asteroid_list.append(Asteroid(self, pos, 10.0, self.images['asteroid'], initial_velocity))
        self.asteroid_countdown_range = (max(20, self.asteroid_countdown_range[0] - 10), max(40, self.asteroid_countdown_range[1] - 10))
        self.asteroid_countdown = random.randint(self.asteroid_countdown_range[0], self.asteroid_countdown_range[1])

    def create_new_explosion(self, pos, explosion_count):
        self.explosion_list.append(ExplosionCluster(self, pos, explosion_count))