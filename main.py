'''
Created on Mar 24, 2015

@author: Disley
'''

import pygame
from wordcloud import WordCloud


if __name__ == "__main__":
    pygame.init()

    filename = 'speech.txt'

    cloud = WordCloud(filename)

    pygame.image.save(cloud.cloudSurf, "cloud.png")
    print("Saved!")

    pygame.quit()
