import math
import random

import pyray

class Ship:
    MAX_SPEED = 5.0
    MAX_ENGINE_SPEED = 50.0

    def __init__(self, game, pos, radius, color, texture):
        self.game = game
        self.pos = list(pos) # x,y
        self.radius = radius
        self.color = color
        self.angle = 0.0
        self.texture = texture
        self.velocity = [0.0, 0.0] # X velocity, Y velocity
        self.engine_speed = 0.0
        self.vapor_trail = []
        self.is_dead = False

    def render(self):
        if not self.is_dead:
            pyray.draw_texture_pro(
                self.texture,
                pyray.Rectangle(0, 0, self.texture.width, self.texture.height),
                pyray.Rectangle(self.pos[0], self.pos[1], self.texture.width, self.texture.height),
                (self.texture.width / 2, self.texture.height / 2),
                self.angle * (180 / math.pi) + 90,
                pyray.WHITE
            )
            for vapor_dot in self.vapor_trail.copy():
                pyray.draw_circle(vapor_dot[0], vapor_dot[1], vapor_dot[2], (255, 95, 31, 100))

    def update(self):
        if not self.is_dead:
            # Put a floor on the engine speed
            self.engine_speed = min(self.MAX_ENGINE_SPEED, max(0, self.engine_speed))

            # Play the engine sound if we're moving
            engine_sound = self.game.sounds['engine']
            if self.engine_speed > 0 and not pyray.is_sound_playing(engine_sound):
                pyray.play_sound(engine_sound)

            if self.engine_speed <= 0 and pyray.is_sound_playing(engine_sound):
                pyray.stop_sound(engine_sound)

            if pyray.is_sound_playing(engine_sound):
                pyray.set_sound_volume(engine_sound, 12.5*self.engine_speed / self.MAX_ENGINE_SPEED)

            # Blow up if we've gone out of bounds
            if self.pos[1] < 0 or self.pos[1] > self.game.WINDOW_HEIGHT or self.pos[0] < 0 or self.pos[0] > self.game.WINDOW_WIDTH:
                self.is_dead = True
                return

            # Blow up if we've collided with an asteroid
            for asteroid in self.game.asteroid_list.copy():
                ax, ay, ar = asteroid.get_collision_circle()
                if pyray.check_collision_circles(self.pos, self.radius, (ax, ay), ar):
                    self.is_dead = True
                    self.game.asteroid_list.remove(asteroid)
                    self.game.create_new_explosion(asteroid.pos, 15)
                    return

            # Check to see if we've been crushed
            for black_hole in self.game.black_hole_list:
                if pyray.check_collision_circles(self.pos, self.radius, black_hole.pos, black_hole.death_radius):
                    self.is_dead = True
                    return

            # Calculate velocity updates from black hole gravity
            for black_hole in self.game.black_hole_list:
                x_force, y_force = black_hole.calculate_force_on_object(self.pos[0], self.pos[1])
                self.velocity[0] += x_force
                self.velocity[1] += y_force

            # Calculate new position
            self.pos[0] += math.cos(self.angle)*self.engine_speed + self.velocity[0]
            self.pos[1] += math.sin(self.angle)*self.engine_speed + self.velocity[1]

            # Cap velocities so we don't get TOO crazy
            self.velocity[0] = min(self.MAX_SPEED, max(-self.MAX_SPEED, self.velocity[0]))
            self.velocity[1] = min(self.MAX_SPEED, max(-self.MAX_SPEED, self.velocity[1]))

            # Update the vapor trail
            for vapor_dot in self.vapor_trail:
                vapor_dot[2] -= 0.1
                if vapor_dot[2] <= 0:
                    self.vapor_trail.remove(vapor_dot)

            # Add vapor dots to the trail
            vapor_fudge_factor = (random.random() - 0.5) * 8.0
            theta = (math.pi/2) - self.angle
            vapor_x = self.pos[0] - (self.texture.height + vapor_fudge_factor) * math.sin(theta) / 2
            vapor_y = self.pos[1] - (self.texture.height + vapor_fudge_factor) * math.cos(theta) / 2
            self.vapor_trail.append([int(vapor_x), int(vapor_y), self.engine_speed / 2.0])

    def increase_speed(self):
        self.engine_speed += 0.1

    def decrease_speed(self):
        self.engine_speed -= 0.1
