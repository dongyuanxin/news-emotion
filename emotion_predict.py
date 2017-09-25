import os

import numpy as np
import operate_data as od
import ml_model

def getModel():
    best_vector = "wordfreq"
    best_model = 1  # linearLogistic

    xpath = os.path.join('result', 'vector', 'resultX.npz')
    ypath = os.path.join('result', 'vector', 'resultY.npz')

    resultX = np.load(xpath)
    resultY = np.load(ypath)

    od.loadStopwords()
    od.loadEmotionwords()
    od.loadWords(od.stopList)
    od.loadDocument(od.stopList)

    new_x, new_y = od.twoTag(resultX[best_vector], resultY[best_vector])
    model = ml_model.linearLogistic(new_x, new_y)
    return model

news = "                                                    《经济通通讯社13日专讯》日股早市偏软,日经225指数报18312跌239点。  美元兑日圆疲软,新报108﹒78╱80。(tt)                                                                         "
