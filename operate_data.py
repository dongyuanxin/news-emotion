#encoding:utf-8
import os
import pickle
import math
import jieba
import jieba.posseg as pseg
import numpy as np
from clean_data.clean_html import cleanHtml
from langconv import *

dictPath = os.path.join('data','emdict','userdict') # 针对linux兼容
jieba.load_userdict(dictPath) # 加载个人词典
stopwordsPath = os.path.join('data','emdict','stopword.plk')
negwordsPath = os.path.join('data','emdict','negword.plk')
poswordsPath = os.path.join('data','emdict','posword.plk')
documentPath = os.path.join('data','trainset')

stopList = []
emotionList = []
posList = []
negList = []
wordsList = [] #针对不基于词典，基于所有文档的词
docList = [] #tf-idf所需要的list，一次性加载，防止多次重复读取

# 转换繁体到简体
def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line
# 转换简体到繁体
def chs_to_cht(line):
    line = Converter('zh-hant').convert(line)
    line.encode('utf-8')
    return line

# 新闻格式一体化
def clearNews(news,mode=False):
    '''
    :param news: 包括繁体，网页格式
    :param mode: 默认是繁体->简体
    :return: 清洗后的标准格式news
    '''
    if not mode:
        return cleanHtml(cht_to_chs(news))
    else:
        return cleanHtml(chs_to_cht(news))

# 加载停用词
def loadStopwords(path = stopwordsPath):
    global stopList
    with open(stopwordsPath,'rb') as f:
        stopList = pickle.load(f)

# 加载感情词
def loadEmotionwords(*paths):
    global posList,emotionList,negList
    if not len(paths):
        with open(negwordsPath,'rb') as f:
            negList = pickle.load(f)
            # t.extend(pickle.load(f))
        with open(poswordsPath,'rb') as f:
            posList = pickle.load(f)
            # t.extend(pickle.load(f))
        emotionList = posList+negList
    else:
        for path in paths:
            with open (path,'rb') as f:
                emotionList = pickle.load(f)

# 针对不基于词典
# 直接调用一次后，然后请调用 全局变量 wordsList
def loadWords(stopList,path=documentPath):
    global wordsList
    wordsSet = set()
    for file in os.listdir(path):
        news = None
        with open(os.path.join(path,file),'r',encoding='utf-8') as f:
            news = f.read()
            noun = [word for word, flag in pseg.lcut(news) if flag.startswith('n')]
            news = set(jieba.cut_for_search(news))
            news = {word for word in news if (word not in stopList) and (word not in noun)}  # 过滤停用词和名词
        wordsSet = news | wordsSet
    wordsList = list(wordsSet)
    return None

# 针对TF-IDF
# 读取所有数据集的词，是的全局变量变成二维的List
def loadDocument(stopList,path=documentPath):
    global docList
    docList = []
    for file in os.listdir(path):
        news = None
        with open(os.path.join(path,file),'r',encoding='utf-8') as f:
            news = f.read()
            noun = [word for word, flag in pseg.lcut(news) if flag.startswith('n')]
            news = list(jieba.cut_for_search(news))
            news = [word for word in news if (word not in stopList) and (word not in noun)]  # 过滤停用词和名词
        docList.append(news)
    return None

# news翻译成词向量
def words2Vec(news,emotionList,stopList,posList,negList,mode=0): # 优化：引用global
    assert isinstance(stopList,list) and isinstance(emotionList,list),"类型不对。Function 'word2vec' at OperateDat.py"
    news = clearNews(news)
    noun = [word for word,flag in pseg.lcut(news) if flag.startswith('n')] # 名词列表
    newswords = list(jieba.cut_for_search(news))
    newswords = [word for word in newswords if (word not in stopList) and (word not in noun)] #过滤停用词和名词
    wordsVec = []
    # one-hot
    if mode==0:
        for word in emotionList:
            if word in newswords:  wordsVec.append(1)
            else:  wordsVec.append(0)
    # frequency
    elif mode==1:
        for word in emotionList:
            wordsVec.append(newswords.count(word))
    # two Vec
    elif mode==2:
        negTimes = 0;posTimes = 0
        for word in posList:
            posTimes+=(newswords.count(word))
        for word in negList:
            negTimes+=(newswords.count(word))
        wordsVec.append(posTimes);wordsVec.append(negTimes)
    # tf-idf
    elif mode==3:
        global docList # 引用加载后的全局变量
        docSum = len(docList) # 第一维len代表了文件数
        for word in emotionList:
            TF = 0
            IDF= 0
            times = 0
            for doc in docList:
                if word in doc: times+=1
            IDF = math.log10(docSum/abs(times+1))
            times = 0
            for doc in docList:
                times+=doc.count(word)
            TF = newswords.count(word)/(times+1)
            wordsVec.append(TF*IDF)
    # out-of-dict
    elif mode==4:
        global wordsList
        for word in wordsList:
            wordsVec.append(newswords.count(word))
    return wordsVec

# 数据归一化
def dataNormal(vecArr):
    '''
    :param vecArr: array类型vec向量
    :return: 归一化的词向量，减小影响。
    '''
    return (vecArr-vecArr.min())/(vecArr.max()-vecArr.min())

# 随机生成训练集和测试集
def randomData(xData,yData,w=0.1,logFile=None):
    np.random.seed(0)
    if logFile:
        assert len(logFile)==len(xData)==len(yData),'缺少维度 at OperateData.py'
    else:
        assert  len(xData)==len(yData),'缺少维度 at OperateData.py'
    length = len(xData)
    indices = np.random.permutation(length) # 对[0:length]区间的整数随机排列得到对应的index
    trainX = xData[indices[:(-1)*int(w*length)]] # 取出对应的index对应的元素
    trainY = yData[indices[:(-1)*int(w*length)]]
    testX = xData[indices[(-1)*int(w*length):]]
    testY = yData[indices[(-1)*int(w*length):]]
    logTrain = [logFile[i] for i in indices[:(-1)*int(w*length)]]
    logTest = [logFile[i] for i in indices[(-1)*int(w*length):]]
    if logFile:
        return trainX,trainY,testX,testY,logTrain,logTest
    return trainX,trainY,testX,testY


if __name__=='__main__':
    modes = 5 #一共5种word2vec方法
    loadStopwords()
    loadEmotionwords()
    loadWords(stopList)
    loadDocument(stopList)
    resultX = []
    resultY = []
    logfile = [] # 留作bug
    for doc in os.listdir(documentPath):
        logfile.append(doc)

    with open(os.path.join('result','log','logfile.plk'),'wb') as f:
        pickle.dump(logfile,f) #存取

    for mode in range(modes):
        x = []
        y = []
        for doc in os.listdir(documentPath):
            news = None
            news_file_path = os.path.join(documentPath,doc)

            if doc[:3] in ('neg','neu','pos'):
                with open(news_file_path,'r',encoding='utf-8') as f:
                    news = f.read()
                x.append(words2Vec(news,emotionList,stopList,posList,negList,mode=mode))
                if doc.startswith('neg'):
                    y.append(-1)
                elif doc.startswith('neu'):
                    y.append(0)
                else:
                    y.append(1)
                print('In', mode, news_file_path)
        resultX.append(np.array(x))
        resultY.append(np.array(y))

    np.savez(os.path.join('result','vector','resultX.npz'),onehot = resultX[0],wordfreq=resultX[1],twovec=resultX[2],tfidf=resultX[3],outofdict=resultX[4])
    np.savez(os.path.join('result','vector','resultY.npz'),onehot = resultY[0],wordfreq=resultY[1],twovec=resultY[2],tfidf=resultY[3],outofdict=resultY[4])
    print('Over')
