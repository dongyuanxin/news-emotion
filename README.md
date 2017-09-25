## 0.快速开始
挑战杯项目：金融文本情感分析模型  || Challenge Cup Project: Financial Text Emotion Analysis Model

## 1.使用方法
### 1.0 配置方法
```shell
cd 你的python脚本目录/
sudo git clone https://github.com/AsuraDong/news-emotion.git news_emotion
sudo mv ./news_emotion/data ./
```

### 1.1 代码使用样例

```python
import pickle
import os

import news_emotion
from news_emotion import operate_data as od
vector_dict = {
    'onehot':0,\
    'wordfreq':1,\
    'twovec':2,\
    'tf-idf':3,\
    'outofdict':4
}
od.loadStopwords()
od.loadEmotionwords()
# od.loadWords(od.stopList) # 针对不基于词典
# od.loadDocument(od.stopList) # 针对tf-idf

news = "这是一段新闻样本：全国股票暴跌" # 待转化的文本
vector = od.words2Vec(news,od.emotionList,od.stopList,od.posList,od.negList,mode = vector_dict['wordfreq']) # 翻译后的词向量
model = None # 我们帮您训练好的模型
with open(os.join('news_emotion','model','wrodfreq_1.ml'),'rb') as f:
    model = pickle.load(f)
tag = model.fit(vector)
print(tag) # 你可以在这里查看上面这句话的结果

```
