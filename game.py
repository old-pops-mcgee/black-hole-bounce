import pyray

from entities.ball import Ball
from entities.black_hole import BlackHole
from entities.paddle import Paddle


class Game:
    WINDOW_HEIGHT = 640
    WINDOW_WIDTH = 480
    MAX_BLACK_HOLES = 3

    def __init__(self):
        pyray.init_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Black Hole Bounce")
        pyray.init_audio_device()

        pyray.set_target_fps(60)

        # Instantiate the core components
        self.paddle = Paddle(self, (0, 0), 0, 0, pyray.WHITE)
        self.ball = Ball(self, (0, 0), 0, pyray.WHITE)
        self.black_hole_list = []
        self.black_hole_count = 0

        self.reload_game_components()

    def reload_game_components(self):
        self.paddle = Paddle(self, (190, 600), 5, 100, pyray.SKYBLUE)
        self.ball = Ball(self, (240, 100), 5, pyray.YELLOW)
        self.black_hole_list = []
        self.black_hole_count = 0

    def update(self):
        self.paddle.update()
        self.ball.update()

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

        self.paddle.render()
        self.ball.render()
        for black_hole in self.black_hole_list:
            black_hole.render()
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