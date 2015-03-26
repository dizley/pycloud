'''
Created on Mar 24, 2015

@author: Disley
'''

from wordcloud import WordCloud


if __name__ == "__main__":
    filename = 'speech.txt'
    cloud = WordCloud(filename)
    cloud.save_img()
    print("Saved!")
