"""
收集、生成、存储金融词典
"""
#encoding:utf-8
import os
import pickle
# em是知网的情感词和程度词
try:
    from material import emotion_word as em
except Exception as error:
    from .material import emotion_word as em

__posdict_path = os.path.join('material','NTUSD_simplified','pos.txt') # 积极情感词路径
__negdict_path = os.path.join('material','NTUSD_simplified','neg.txt') # 消极情感词路径
__stopdict_path = os.path.join('material','stopword.txt') # 停用词（垃圾词）路径
__jieba_weight = 1000000 # 添加的新词的权重

def collectEmotionWord(posdict_path,negdict_path):
    """
    针对情感词
    :param posdict_path: 积极情感词路径
    :param negdict_path: 消极情感词路径
    :return: 积极词列表和消极词列表
    """
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
    """
    针对停用词
    :param stopdict_path: 停用词路径
    :param emotion: 情感词集合
    :return: 停用词列表
    """
    em_dict = set()  # 收集情感词
    for em in emotion:
        for word in em:
            em_dict.add(word)

    stopSet = set()
    ########## 收集N-gram和停用词典的垃圾词 ##########
    with open(stopdict_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            word = line.strip('\n').strip()
            if word and (word not in em_dict):  # 过滤情感词
                stopSet.add(line.strip('\n').strip())
    return list(stopSet)


def saveDict(**args):
    """
    存储训练好的词典
    :param args: 键值对，形式：key(文件名)-value(存储内容)
    :return: None
    """
    for (name,mdict) in args.items():
        try:
            if not isinstance(mdict,list):
                raise TypeError("目前仅支持list类型")
        except Exception as error:
            pass
        else:
            with open(name,'w',encoding='utf-8') as f:
                f.write('\n'.join(mdict))

# 作用同：saveDict(**args)
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
    """
    为生成的用户词典增加权重（jieba词库分词需要）
    :param emdict: 不带权重的词列表
    :return: 带有权重的词列表
    """
    global __jieba_weight
    return list(map(lambda word:str(word)+"  "+str(__jieba_weight),emdict))

# 主函数
def main():
    pos_dict, neg_dict = collectEmotionWord(posdict_path=__posdict_path, negdict_path=__negdict_path) # 积极和消极词典
    pos_w_dict, neg_w_dict = addWeight(pos_dict), addWeight(neg_dict) # 带有权重的积极和消极词典
    stop_dict = collectStopWord(__stopdict_path, pos_dict, neg_dict) # 停用词典
    savePickle(stopword = stop_dict,negword = neg_dict,posword = pos_dict)
    saveDict(userdict=pos_w_dict + neg_w_dict, stopword=stop_dict)

if __name__=='__main__':
    main()