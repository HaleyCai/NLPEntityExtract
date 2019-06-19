#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence


def getAbstract(text):
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    
    keywords = []
    #关键词：
    for item in tr4w.get_keywords(num = 3, word_min_len=1):
        keywords.append(item.word)
        #print(item.word, item.weight)

    #关键短语：
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
        keywords.append(phrase)
        
    #摘要：
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')

    item = tr4s.get_key_sentences(num=5)
    if len(item)>0:
        return ','.join(keywords), item[0].sentence

    return ','.join(keywords), ''


def getFilter(text):
    if text == '':
        return ''
    
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)

    # words_all_filters
    words = tr4w.words_all_filters
    
    return ''.join(words[0])


if __name__ == '__main__':
    getAbstract('1778年，8岁的贝多芬师从宫廷老管风琴师H・伊登学习音乐基础理论及管风琴，同年8月26日第一次登台演出 。')
    getFilter('1778年，8岁的贝多芬师从宫廷老管风琴师H・伊登学习音乐基础理论及管风琴，同年8月26日第一次登台演出 。')