'''
Created on Mar 24, 2015

@author: Disley
'''

import re
import pygame
from collections import namedtuple


class Word(object):
    '''
    classdocs
    '''

    def __init__(self, s, size=10, font='georgia', x=0, y=0):
        '''
        Constructor
        '''
        self.s = s
        self.fontSize = size
        self.fontName = font
        self.font = pygame.font.SysFont(self.fontName, self.fontSize)
        tmpSurf = self.font.render(self.s, True, (0, 0, 0))
        self.clip_rect = tmpSurf.get_bounding_rect()
        self.clip_rect.x -= 2
        self.clip_rect.y -= 2
        self.clip_rect.w += 4
        self.clip_rect.h += 4
        self.msgSurf = pygame.Surface((self.clip_rect.w, self.clip_rect.h))
        self.msgSurf.fill((255, 255, 255))
        self.msgSurf.blit(tmpSurf, (0, 0), area=self.clip_rect)
        self.msgSurf.set_colorkey((255, 255, 255))
        self.x, self.y, self.w, self.h = (x, y,
                                          self.clip_rect.w, self.clip_rect.h)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def get_bb(self):
        BoundingBox = namedtuple('BoundingBox', 'x y w h')
        return BoundingBox(self.x, self.y, self.w, self.h)

    def set_xy(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def collision(self, word):
        return self.rect.colliderect(word.rect)

    def draw(self, surface, offsets):
        surface.blit(self.msgSurf, (self.x+offsets[0], self.y+offsets[1]))


def strip_punctuation(s):
    pattern = r'[!"&\(\)\*,\.\/\\?;:\[\]\-]|(\' )'
    return re.sub(pattern, "", s)


def is_boring(s):
    boring_list = ["the", "and", "this", "that", "for", "will", "of"]
    return True if s in boring_list else False
