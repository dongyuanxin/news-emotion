import pickle
import json
import os
from collections import OrderedDict # 有序词典
import numpy as np
import ml_model as ml
import operate_data as od

def runBest(vector='wordfreq',m_model = ml.naiveBayes):
    ##### 开启记录模式的代码(只记录留一验证后准确率最高的模型) #####
    logpath = os.path.join('result','log','logfile.plk')
    logfile = None
    with open(logpath,'rb') as f:
        logfile = pickle.load(f)
    trainX,trainY,testX,testY,logTrain,logTest = od.randomData(resultX[vector],resultY[vector],0.1,logfile) # 选取最好的vector方法
    model = m_model(trainX,trainY) # 选取最好的机器训练模型
    predictY = [model.predict(x.reshape(1,-1))[0] for x in testX]
    logDict = OrderedDict()
    logDict['+2+'] = [];logDict['+2.'] = [];logDict['+2-'] = []
    logDict['-2+'] = [];logDict['-2.'] = [];logDict['-2-'] = []
    logDict['.2+'] = [];logDict['.2.'] = [];logDict['.2-'] = []
    for i in range(len(predictY)):
        if predictY[i] == testY[i]:
            if predictY[i]>0:
                logDict['+2+'].append(logTest[i])
            elif predictY[i]==0:
                logDict['.2.'].append(logTest[i])
            else:
                logDict['-2-'].append(logTest[i])
        elif predictY[i]>0 and testY[i]==0:
            logDict['.2+'].append(logTest[i])
        elif predictY[i]>0 and testY[i]<0:
            logDict['-2+'].append(logTest[i])

        elif predictY[i]<0 and testY[i]==0:
            logDict['.2-'].append(logTest[i])
        elif predictY[i]<0 and testY[i]>0:
            logDict['+2-'].append(logTest[i])

        elif predictY[i]==0 and testY[i]>0:
            logDict['+2.'].append(logTest[i])
        elif predictY[i]==0 and testY[i]<0:
            logDict['-2.'].append(logTest[i])

    with open(os.path.join('result','log','3plus3arr.plk'),'wb') as f:
        pickle.dump(logDict,f)
    print('Over')

def logBest():
    arr = None # 存放3*3的矩阵(实际是数组)
    with open(os.path.join('result','log','3plus3arr.plk'),'rb') as f:
        arr = pickle.load(f)

    ErrorTag = {}
    key_arr = [] # 含有错误标签的键组成的数组

    for key in arr.keys():
        if key not in ('+2+','-2-','.2.') and len(arr[key]):
            key_arr.append(key)
            message = 'At: '+key+'; Total '+str(len(arr[key]))+"; \n  "+",".join(arr[key])
            print(message)
            ErrorTag[key] = message
    with open(os.path.join('result','log','best_model','error_tag.json'),'w',encoding="utf-8") as f:
        json.dump(ErrorTag,f)

    print("="*30)

    for key in arr.keys():
        if key not in key_arr:
            print('At: ' + key + '; Total ' + str(len(arr[key])) + "; \n  " + ",".join(arr[key]))

    ##### 计算PR并且写入文件 #####
    pr = {} #p:精确率 r:召回率
    pr['+'] = {\
        'p':len(arr['+2+'])/(len(arr['+2+'])+len(arr['-2+'])+len(arr['.2+'])),\
        'r':len(arr['+2+'])/(len(arr['+2+'])+len(arr['+2-'])+len(arr['+2.'])) \
    }
    pr['-'] = {\
        'p':len(arr['-2-'])/(len(arr['-2-'])+len(arr['+2-'])+len(arr['.2-'])),\
        'r':len(arr['-2-'])/(len(arr['-2-'])+len(arr['-2+'])+len(arr['-2.'])) \
    }
    pr['.'] = {\
        'p':len(arr['.2.'])/(len(arr['.2.'])+len(arr['+2.'])+len(arr['-2.'])),\
        'r':len(arr['.2.'])/(len(arr['.2.'])+len(arr['.2+'])+len(arr['.2-'])) \
    }
    with open(os.path.join('result','log','best_model','PR.json'),'w',encoding="utf-8") as f:
        json.dump(pr,f)

if __name__=='__main__':
    best_vec = 'wordfreq'
    m_model = ml.naiveBayes
    runBest(vector = best_vec,m_model= bset_model)
    logBest()
