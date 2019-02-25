"""
This was the animation module I used in the previous version of the game
"""

__author__ = 'Joshua Akangah'

import pygame

class Animation():
    def __init__(self, sprites, frame_duration, scale):
        self.images = []
        for i in sprites:
            image = pygame.image.load(i).convert_alpha()
            images = pygame.transform.scale(image, (int(image.get_rect().width * scale), int(image.get_rect().height * scale)))
            self.images.append(images)
            
        self.animation_time = frame_duration
        self.current_time = 0
        self.animation_frames = len(self.images)
        self.current_frame = 0
        self.index = 0

    def update(self, dt):
        self.current_time += dt

        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def get_current_image(self):
        return self.images[self.index]

    def get_rect(self):
        return self.get_current_image().get_rect()

    def get_mask(self):
        return pygame.mask.from_surface(self.get_current_image())


