# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:24:42 2019

@author: caiyq
"""
import re
import pandas as pd
from myExtract import *
from abstract import *

#step1: 读入文本，并将空格、换行去掉，整合成一个字符串
def readFile(filename):
    with open(filename + '.txt', 'r', encoding="UTF-8") as inFile:
        file = inFile.readlines()
        f = "".join(file)
        f = "".join(f.split()) 
        f = re.sub(u"\\{.*?}|\\[.*?]", "", f)
        print(f)
    return f


#step2: 识别所有时间，根据时间在文章字符串中的定位，将文章按照时间点分割成list，和时间组合成dic返回
def divideUseTime(fileText):
    allTimes = extract_time(fileText)
    print(allTimes)
    index = []
    for time in allTimes:
        key = fileText.find(time)
        index.append(key)
    dicText = []
    for i in range(1,len(index)):
        oneNode = fileText[index[i-1]:index[i]]
        dicText.append({'time':allTimes[i-1], 'text': oneNode})
    dicText.append({'time':allTimes[-1], 'text': fileText[index[-1]:]})
    
    for dic in dicText:
        if dic['time']=='':
            dicText.remove(dic)
    
    return dicText


#step3: 将每个时间节点的文本，进行信息抽取(time, person, location, work)和提炼一句话摘要，并写入文件
def extractText(dicText, filename):
    result = []
    for node in dicText:
        res = {}
        res['time'] = node['time']
        res['person'] , res['location'], res['work'] = extract(node['text'])
        res['keyword'], res['abstract'] = getAbstract(node['text'])
        res['filter'] = getFilter(res['abstract'])
        print(res)
        result.append(res)
    
    outFilename = filename + '_out'
    # 写到txt文件中
    printAsTXT(result, outFilename)
    # 写到csv文件中，目前编码还存在问题
    printAsCSV(result, outFilename)
       

def printAsTXT(result, outFilename):
    with open(outFilename + '.txt', 'w', encoding='utf-8') as outFile:
        for res in result:
            outFile.write(res['time']+'\n')
            outFile.write(res['person']+'\n')
            outFile.write(res['location']+'\n')
            outFile.write(res['work']+'\n')
            outFile.write(res['keyword']+'\n')
            outFile.write(res['abstract']+'\n')
            outFile.write(res['filter']+'\n')
        outFile.close()
    print("success write .txt")


def printAsCSV(result, outFilename):
    data = pd.DataFrame(result)
    data.to_csv(outFilename+ '.csv', index=False, encoding="UTF-8")
    print("success write .csv")


def doExtract(filename):
    file= readFile(filename)
    dicText = divideUseTime(file)
    extractText(dicText, filename)


if __name__ == '__main__':
    doExtract('test1')
    doExtract('test2')
    doExtract('test3')