'''
Created on Mar 24, 2015

@author: Disley
'''

from collections import Counter, OrderedDict
import math
from words import Word, strip_punctuation, is_boring
import random
import pygame


class WordCloud():
    '''
    Generate a word cloud
    Dependencies
    *pygame
    '''

    def __init__(self, filename,
                 MAX_WORDS=50, MAX_FONT_SIZE=500):
        '''
        Generate a word cloud from a list of words
        '''
        self.MAX_WORDS = MAX_WORDS
        self.MAX_FONT_SIZE = MAX_FONT_SIZE
        self.word_hist = self.list_from_file(filename)
        self.word_sizes = self.sizes_from_list(self.word_hist)
        self.placed_words = []
        random.seed(1)
        self.arrange()
        self.tighten()
        self.cloudSurf = None
        self.draw()

    def list_from_file(self, filename):
        '''
        Load a text file and create a counter of each individual word
        Discarding "boring" words and punctuation
        '''
        word_hist = Counter()

        with open(filename, 'r') as f:
            for line in f:
                for word in line.split():
                    word = strip_punctuation(word)
                    if not is_boring(word):
                        word_hist[word] += 1

        return word_hist

    def sizes_from_list(self, word_hist):
        '''
        Calculate the font size of each word and store them in an OrderedDict
        ordered by font size.
        '''
        highest_freq = word_hist.most_common(1)[0][1]
        word_sizes = OrderedDict()
        for word in word_hist.most_common(self.MAX_WORDS):
            word_sizes[word[0]] = self.size_from_freq(word[1], highest_freq)
        return word_sizes

    def size_from_freq(self, freq, highest_freq):
        exp_factor = 1.9
        x = freq/highest_freq
        y = (self.MAX_FONT_SIZE/math.exp(exp_factor))*math.exp(exp_factor*x)
        return round(y)

    def arrange(self):
        # spiral parameters
        a = 0
        b = -.1

        for word, size in self.word_sizes.items():
            # initialize word at random start position
            newWord = Word(word, size=size, x=self._random_x(),
                           y=self._random_y())

            if not self.placed_words:
                # if its the first word just plonk it down and move on
                self.placed_words.append(newWord)
                continue

            theta = 0
            k = 1 if random.randint(0, 1) == 1 else -1

            while True:
                for placed_word in self.placed_words:
                    if placed_word.collision(newWord):
                        # spiral the position outwards
                        theta += math.pi/50
                        r = a + b*k*theta
                        newWord.set_xy(newWord.x + r*math.cos(theta),
                                       newWord.y + 0.5*r*math.sin(theta))
                        break
                else:
                    break

            self.placed_words.append(newWord)

    def tighten(self):
        for word in self.placed_words:
            # try and move the word closer to the y origin
            if word.y == 0:
                continue

            y_direction = 1 if word.y < 0 else -1
            while True:
                if ((word.y < 0) == (y_direction < 0)):
                    break
                old_x, old_y = word.x, word.y
                word.set_xy(word.x, word.y + y_direction)
                for placed_word in self.placed_words:
                    if placed_word.s != word.s:
                        if word.collision(placed_word):
                            word.set_xy(old_x, old_y)
                            break
                else:
                    continue
                break

        # tighten x axis
        for word in self.placed_words:
            # try and move the word closer to the x origin
            if word.x == 0:
                continue

            x_direction = 1 if word.x < 0 else -1
            while True:
                if ((word.x < 0) == (x_direction < 0)):
                    break
                old_x, old_y = word.x, word.y
                word.set_xy(word.x + x_direction, word.y)
                for placed_word in self.placed_words:
                    if placed_word.s != word.s:
                        if word.collision(placed_word):
                            word.set_xy(old_x, old_y)
                            break
                else:
                    continue
                break

    def draw(self):
        background = self.create_background_surface()
        w, h = background.get_size()
        for word in self.placed_words:
            word.draw(background, (w/2, h/2))
        background.set_colorkey((255, 255, 255))
        clip_rect = background.get_bounding_rect()
        self.cloudSurf = pygame.Surface((clip_rect.w+2, clip_rect.h+2))
        self.cloudSurf.fill((255, 255, 255))
        self.cloudSurf.blit(background, (1, 1), area=clip_rect)

    def create_background_surface(self):
        l, t, r, b = 0, 0, 0, 0
        for word in self.placed_words:
            if word.x < l:
                l = word.x
            if word.y < t:
                t = word.y
            if word.x + word.w > r:
                r = word.x + word.w
            if word.y + word.h > b:
                b = word.y + word.h

        backSurf = pygame.Surface((r-l+500, b-t+500))
        backSurf.fill((255, 255, 255))
        return backSurf

    def _random_x(self):
        return round(random.gauss(0, 20))

    def _random_y(self):
        return 0
