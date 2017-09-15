# encoding:utf-8
import pickle
import os
from collections import OrderedDict # 有序词典
import numpy as np
import ml_model as ml
import operate_data as od
import pandas as pd
from pandas import DataFrame

def loocv(xData,yData,mode,vecName=None):
    '''
    :param xData: 测试样例的元素
    :param yData: 测试样例的标签
    :return: None
    '''
    assert len(xData)==len(yData),str(vecName)+":自变量/因变量维度缺失"
    error = 0
    length = len(xData)
    for i in range(length):
        lenList = [l for l in range(length)]
        del lenList[i]
        if mode==0:
            model = ml.neighborKNN(xData[lenList],yData[lenList])
        elif mode==1:
            model = ml.linearLogistic(xData[lenList],yData[lenList])
        elif mode==2:
            model = ml.randomForest(xData[lenList],yData[lenList])
        elif mode==3:
            model = ml.SVM(xData[lenList],yData[lenList])
        elif mode==4:
            model = ml.naiveBayes(xData[lenList],yData[lenList])
        if model.predict(xData[i].reshape(1,-1))!=yData[i]: # 修复Bug
            error+=1
    # print('准确率是：',1-error/length)
    return 1-error/length

def loocvModel():
    loocvPath = os.path.join('result', 'vector', 'ml_rate.plk')
    xpath = os.path.join('result', 'vector', 'resultX.npz')
    ypath = os.path.join('result', 'vector', 'resultY.npz')
    resultX = np.load(xpath)
    resultY = np.load(ypath)
    ###### 留一验证部分的代码 #####
    modes = 5
    accuracyDict = OrderedDict()  # 有序词典
    for key in resultX.keys():
        print('[+][+]', key)
        accuracyDict[key] = []
        for mode in range(modes):  # 5种模型机器训练模型
            accuracyDict[key].append(loocv(resultX[key], resultY[key], mode=mode, vecName=key))
            print('   [+]Model:', mode, '=> Finished')
    with open(loocvPath, 'wb') as f:
        pickle.dump(accuracyDict, f)
    print('Over')

def showResult():
    loocvPath = os.path.join('result','log','loocv.plk')
    loocv = None
    with open(loocvPath,'rb') as f:
        loocv = pickle.load(f)
    print(loocv)
    loocv = DataFrame(loocv,index=['KNN','Logistic','RandomForest','SVM','NBayes'])
    loocv.index.name = r'Model\Vector'
    loocv.rename(columns=str.title,inplace=True)
    print(loocv)
    resultExcel = os.path.join('result', 'show','result.xlsx')
    resultCSV = os.path.join('result','show','result.csv')
    try:
        loocv.to_excel(resultExcel)
    except Exception as e:
        print('Can not call packages about excel')
    finally:
        loocv.to_csv(resultCSV)

if __name__=='__main__':
    loocvModel()
    showResult()