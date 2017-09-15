# encoding:utf-8
import numpy as np
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

# KNN算法
def neighborKNN(trainVec,trainScore):
    knn = KNeighborsClassifier()
    knn.fit(trainVec,trainScore)
    return knn
# Logistics回归
def linearLogistic(trainVec,trainScore):
    '''
    注意：
        针对二维或三维变量
    '''
    model = linear_model.LogisticRegression(penalty = 'l1')
    model.fit(trainVec,trainScore)
    return model
# 随机森林
def randomForest(trainVec,trainScore):
    model = RandomForestClassifier(max_depth=None)
    model.fit(trainVec, trainScore)
    return model
# 多分类支持向量机
def SVM(trainVec,trainScore):
    model = SVC()
    model.fit(trainVec, trainScore)
    return model
# 采取多项式朴素贝叶斯
def naiveBayes(trainVec,trainScore):
    model = MultinomialNB()
    model.fit(trainVec,trainScore)
    return model

def saveModel(model,modelname):
    '''
    参数：
        model：训练好的模型
        modelname：模型的名称
    '''
    try:
        with open(modelname,'wb',encoding='utf-8') as f:
            f.dump(model,modelname)
    except Exception as error:
        print('模型存储失败，因为：',error)

def readModel(modelname):
    try:
        model = None
        with open(modelname,'rb',encoding='utf-8') as f:
            model = f.load(f)
    except Exception as error:
        print('模型读取失败，因为：',error)
    else:
        return model