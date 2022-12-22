from math import exp
import numpy as np

import pygame
from pygame.locals import *

import gym
from gym import spaces

from sprites import Player, Sensor, Bit
from utils import Color
from config import *



class Environment(gym.Env):
    metadata = {'render_modes': ['human'], 'render_fps': 60}

    def __init__(self, render_mode=None):
        assert render_mode is None or render_mode in Environment.metadata['render_modes']
        self.render_mode = render_mode

        self.observation_space = spaces.MultiDiscrete(SENSOR_COUNT * [3], dtype=np.int32)
        self.action_space = spaces.MultiDiscrete((2, 3), dtype=np.int32)

        pygame.init()
        self.clock = None
        self.screen = None

        self.UPDATEBITS = pygame.USEREVENT + 1
        pygame.time.set_timer(self.UPDATEBITS, 1000)


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.player = Player()
        self.bits = pygame.sprite.Group()
        self.sensors = pygame.sprite.Group(
            [
                Sensor(self.player, t) for t in
                np.linspace(-SENSOR_FOV / 2, SENSOR_FOV / 2, SENSOR_COUNT)
            ]
        )
        self.all_sprites = pygame.sprite.Group(self.player, self.sensors)

        observation = np.array(
            [sensor.update(self.bits) for sensor in self.sensors], dtype=np.int32
        ) + 1
        info = self.player.score

        self._render_frame()

        return (observation, info)

    def step(self, action):    
        for event in pygame.event.get():
            if event.type == self.UPDATEBITS:
                p = 1 / (1 + exp(12 - len(self.bits)))

                if np.random.random() > p:
                    new_bit = Bit()
                    self.bits.add(new_bit)
                    self.all_sprites.add(new_bit)
                if np.random.random() < p:
                    old_bit = self.bits.sprites()[0]
                    old_bit.kill()
        
        keys = {K_w: False, K_a: False, K_d: False}

        if action[0] == 1: keys[K_w] = True

        if action[1] == 0: keys[K_a] = True
        elif action[1] == 2: keys[K_d] = True

        reward = self.player.update(keys, self.bits)
        observation = np.array([sensor.update(self.bits) for sensor in self.sensors], dtype=np.int32)
        info = self.player.score

        self._render_frame()

        return observation, reward, False, False, info


    def render(self):
        pass


    def _render_frame(self):
        if self.screen is None and self.render_mode == 'human':
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.clock == None and self.render_mode == 'human':
            self.clock = pygame.time.Clock()
        
        for sprite in self.all_sprites:
            sprite.draw()

        if self.render_mode == 'human':
            self.screen.fill(Color.WHITE)
            for e in self.all_sprites:
                self.screen.blit(e.surf, e.rect)
            pygame.display.flip()
            self.clock.tick(Environment.metadata['render_fps'])


    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()


    def play(self):
        self.reset()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                elif event.type == self.UPDATEBITS:
                    p = 1 / (1 + exp(12 - len(self.bits)))

                    if np.random.random() > p:
                        new_bit = Bit()
                        self.bits.add(new_bit)
                        self.all_sprites.add(new_bit)
                    if np.random.random() < p:
                        old_bit = self.bits.sprites()[0]
                        old_bit.kill()

                elif event.type == QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.player.update(keys, self.bits)
            self.sensors.update(self.bits)
            
            for sprite in self.all_sprites:
                sprite.draw()

            self.screen.fill(Color.WHITE)
            for e in self.all_sprites:
                self.screen.blit(e.surf, e.rect)

            pygame.display.flip()
            print(f'Score: {self.player.score}', end=' ' * 8 + '\r')
            self.clock.tick(Environment.metadata['render_fps'])      



if __name__ == '__main__':
    env = Environment('human')
    env.play()
    env.close()
