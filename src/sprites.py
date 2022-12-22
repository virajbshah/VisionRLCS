import numpy as np

import pygame
from pygame.locals import *

from utils import Color, rotate
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.v = np.array([PLAYER_SPEED, 0], dtype=np.float64)
        self.theta = 0
        self.score = 0

        self.surf = pygame.Surface(2 * (PLAYER_SIZE,), pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))


    def update(self, keys, bits):
        if keys[K_w]:
            self.rect.move_ip(rotate(self.v, self.theta))
        if keys[K_a]:
            self.theta -= PLAYER_TORQUE
        if keys[K_d]:
            self.theta += PLAYER_TORQUE

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        delta = 0
        collided_bits = pygame.sprite.spritecollide(self, bits, True)
        for bit in collided_bits:
            delta += bit.point
            bit.kill()

        self.score += delta
        return delta


    def draw(self):
        arrow = rotate(
            np.array([
                [ 10, -5, -5],
                [  0,  5, -5]
            ], dtype=np.int32),
            self.theta
        ) + np.array([2 * [PLAYER_SIZE / 2]], dtype=np.int32).T

        pygame.draw.circle(self.surf, Color.CYAN, 2 * (PLAYER_SIZE / 2,), PLAYER_SIZE / 2)
        pygame.draw.circle(self.surf, Color.BLUE, 2 * (PLAYER_SIZE / 2,), PLAYER_SIZE / 2, 3)
        pygame.draw.polygon(self.surf, Color.BLACK, list(zip(arrow[0], arrow[1])))



class Sensor(pygame.sprite.Sprite):
    def __init__(self, player, theta_offset):
        super(Sensor, self).__init__()

        self.player = player
        self.init_los_a = rotate(np.array([PLAYER_SIZE / 2, 0], dtype=np.int32), theta_offset)
        self.init_los_b = rotate(np.array([SENSOR_LOS_LEN, 0], dtype=np.int32), theta_offset)
        self.los_a = self.init_los_a
        self.los_b = self.init_los_b
        self.reading = 0

        self.surf = pygame.Surface(2 * (SENSOR_LOS_LEN * 2,), pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(
            center=self.player.rect.center
        )


    def update(self, bits):
        self.los_a = rotate(self.init_los_a, self.player.theta)
        self.los_b = rotate(self.init_los_b, self.player.theta)
        self.rect.clamp_ip(self.player.rect)

        self.reading = 0
        for bit in filter(lambda b: pygame.sprite.collide_mask(self, b), bits):
            self.reading += bit.point
        self.reading = np.clip(self.reading, -1, 1)

        return self.reading + 1


    def draw(self):
        color = {-1: Color.RED, 0: Color.WHITE, 1: Color.GREEN}[self.reading]

        self.surf.fill(pygame.SRCALPHA)
        pygame.draw.line(
            self.surf, color,
            2 * (SENSOR_LOS_LEN,) + self.los_a,
            2 * (SENSOR_LOS_LEN,) + self.los_b,
        )

        self.mask = pygame.mask.from_surface(self.surf)



class Bit(pygame.sprite.Sprite):
    def __init__(self):
        super(Bit, self).__init__()

        self.point = -1 if np.random.random() < 0.25 else 1

        self.surf = pygame.Surface(2 * (BIT_SIZE,), pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(
            center=(
                np.random.randint(10, SCREEN_WIDTH - 10),
                np.random.randint(10, SCREEN_HEIGHT - 10)
            )
        )


    def update(self):
        # The bits just stay where they are, for now atleast.
        pass


    def draw(self):
        pygame.draw.circle(self.surf,
            Color.GREEN if self.point > 0 else
            Color.RED, 2 * (BIT_SIZE / 2,), BIT_SIZE / 2
        )
        pygame.draw.circle(self.surf,
            Color.BLACK, 2 * (BIT_SIZE / 2,), BIT_SIZE / 2, 2
        )

        self.mask = pygame.mask.from_surface(self.surf)
