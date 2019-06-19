# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 23:15:40 2019

@author: caiyq
"""
import re
from pyhanlp import *


def extract_time(text):
    if text=='':
        return []
    
    allTime = []
    # 1. 匹配xxxx年xx月xx日
    time1 = re.compile(u'([0-9]{4}[年]?[初末底春夏秋冬]?[——-—至到][0-9]{4}[年]?[初末底春夏秋冬])|([0-9]{4}年[0-9]{1,2}月[——-—至到][0-9]{4}年[0-9]{1,2}月)|([0-9]{4}年[0-9]{1,2}月[——-—至到][0-9]{1,2}月)|([0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日[——-—至到][0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日)|([0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日)|([0-9]{4}年[0-9]{1,2}月)|([0-9]{4}年[初末底春夏秋冬]?)').findall(text)
    for t in time1:
        allTime.extend(list(tuple(t)))
    while '' in allTime:
        allTime.remove('')    
    
    # 3. 匹配xxxx-xx-xx
    time3 = re.compile('\d{4}[-/]\d{1,2}[-/]\d{1,2}').findall(text)
    for t in time3:
        strTime = t[:4] + '年' + t[5] + '月' + t[7] + '日'
        allTime.extend([strTime])
        
    # 3. 匹配“同年xx月xx日”！！！！！
    # time3 = re.compile(u'同年[0-9]{1,2}月[0-9]{1,2}日').findall(text)
        
    return allTime


# 去除几个、几岁、几年、几天、几月、几日的文字，为了提取日期
def replace_age(text):
    pattern = re.compile(u'[0-9]{1,}[岁天个]')
    match = pattern.findall(text)
    for word in match:
        text = text.replace(word,'')
    return text


# 提取人物姓名
def extract_person(text):
    if text=='':
        return []
    seg_list = [(str(t.word), str(t.nature)) for t in HanLP.segment(text)]
    names = []
    for ele_tup in seg_list:
        if 'nr' in ele_tup[1]:
            names.append(ele_tup[0])
            # print(ele_tup[0],ele_tup[1])
    names = list(set(names))
    return names

# 提取音乐作品（有《》的）
def extract_work(text):
    rule = r'《(.*?)》'
    wlist = re.findall(rule, text)
    newlist = []
    for work in wlist:
        newlist.append('《' + work + '》')
    newlist = list(set(newlist))
    return newlist


# 提取地点
def get_location(word_pos_list):
    """
    get location by the pos of the word, such as 'ns'
    eg: get_location('内蒙古赤峰市松山区')
    
    :param: word_pos_list<list>
    :return: location_list<list> eg: ['陕西省安康市汉滨区', '安康市汉滨区', '汉滨区']
    """
    location_list = []
    if word_pos_list==[]:
        return []
    
    for i,t in enumerate(word_pos_list):
        word = t[0]
        nature = t[1]
        if nature == 'ns':
            loc_tmp = word
            count = i + 1
            while count < len(word_pos_list):
                next_word_pos = word_pos_list[count]
                next_pos = next_word_pos[1]
                next_word = next_word_pos[0]
                if next_pos=='ns' or 'n' == next_pos[0]:
                    loc_tmp += next_word
                else:
                    break
                count += 1
            location_list.append(loc_tmp)
    return location_list # max(location_list)


def extract_locations(text):
    """
    extract locations by from texts
    eg: extract_locations('我家住在陕西省安康市汉滨区。')
    
    :param: raw_text<string>
    :return: location_list<list> eg: ['陕西省安康市汉滨区', '安康市汉滨区', '汉滨区']
    
    """
    if text=='':
        return []
    seg_list = [(str(t.word), str(t.nature)) for t in HanLP.segment(text)]
    location_list = get_location(seg_list)
    location_list = list(set(location_list))
    return location_list


def extract(text):
    # time= extract_time(text)
    # print(time)
    
    person = extract_person(text)
    # print(person)
    
    location = extract_locations(text)
    # print(location)
    
    work = extract_work(text)
    # print(work)
    
    return " ".join(person), " ".join(location), " ".join(work)
    

if __name__ == '__main__':
    text = '1778-5-5 ，1778年3月8岁的贝多芬在维也纳和德国师从宫廷管风琴师H·伊登学习《音乐基础理论》及管风琴，同年8月26日第一次登台演出 。'
    extract(text)