import os
import pickle
import material.emotion_word as em

__posdict_path = os.path.join('material','NTUSD_simplified','pos.txt')
__negdict_path = os.path.join('material','NTUSD_simplified','neg.txt')
__stopdict_path = os.path.join('material','stopword.txt')
__jieba_weight = 1000000

def collectEmotionWord(posdict_path,negdict_path):
    posSet = set()
    negSet = set()
    ########## 收集台湾大学NTUSD和知网的积极情感词 ##########
    with open(posdict_path, 'r', encoding='utf-8')as f:
        for line in f.readlines():
            word = line.strip('\n').strip()
            if word:
                posSet.add(line.strip('\n').strip())
    for word in em.pos_emotion:
        posSet.add(word)
    for word in em.pos_envalute:
        posSet.add(word)

    ########## 收集台湾大学NTUSD和知网的消极情感词 ##########
    with open(negdict_path, 'r', encoding='utf-8')as f:
        for line in f.readlines():
            word = line.strip('\n').strip()
            if word:
                negSet.add(line.strip('\n').strip())
    for word in em.neg_emotion:
        negSet.add(word)
    for word in em.neg_envalute:
        negSet.add(word)

    return list(posSet),list(negSet)


def collectStopWord(stopdict_path,*emotion):
    em_dict = set()
    for em in emotion:
        for word in em:
            em_dict.add(word)

    stopSet = set()
    ########## 收集N-gram和停用词典的垃圾词 ##########
    with open(stopdict_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            word = line.strip('\n').strip()
            if word and (word not in em_dict):  # 防止停用词和感情词出错
                stopSet.add(line.strip('\n').strip())
    return list(stopSet)


def saveDict(**args):
    for (name,mdict) in args.items():
        try:
            if not isinstance(mdict,list):
                raise TypeError("目前仅支持list类型")
        except Exception as error:
            pass
        else:
            with open(name,'w',encoding='utf-8') as f:
                f.write('\n'.join(mdict))

def savePickle(**args):
    for (name,mdict) in args.items():
        try:
            if not isinstance(mdict,list):
                raise TypeError("目前仅支持list类型")
        except Exception as error:
            pass
        else:
            with open(name+'.plk','wb') as f:
                pickle.dump(mdict,f)

def addWeight(emdict):
    global __jieba_weight
    return list(map(lambda word:str(word)+"  "+str(__jieba_weight),emdict))

def collectDict():
    pos_dict, neg_dict = collectEmotionWord(posdict_path=__posdict_path, negdict_path=__negdict_path) # 积极和消极词典
    pos_w_dict, neg_w_dict = addWeight(pos_dict), addWeight(neg_dict) # 带有权重的积极和消极词典
    stop_dict = collectStopWord(__stopdict_path, pos_dict, neg_dict) # 停用词典
    savePickle(stopword = stop_dict,negword = neg_dict,posword = pos_dict)
    saveDict(userdict=pos_w_dict + neg_w_dict, stopword=stop_dict)

if __name__=='__main__':
    collectDict()