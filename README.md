## 0.快速开始
挑战杯项目：金融文本情感分析模型  || Challenge Cup Project: Financial Text Emotion Analysis Model

## 1.使用方法
### 1.0 下载
```shell
sudo git clone https://github.com/AsuraDong/news-emotion.git news_emotion
mv -R ./news_emotion/ 你的程序路径/
```

### 1.1 文件结构

```python
clean_data/ # 清洗数据
    __init__.py
    clean_html.py # 清洗网页标签
    langconv.py # 简体和繁体转化
    zh_wiki.py # 简体和繁体转化
data/ # 存放训练集和词典
    emdict/ # 存放词典
        material/
            emotion_word.py # 知网情感词典
            stopword.txt # 中文停用词典
            NTUSD_simplified/ # 台湾大学NTUSD情感词典
                ...
        collect_dict.py # 生成之后程序需要的plk和用户词典
    trainset/ # 存放训练集
        ...
model/ # 我们训练好的model模型
    wordfreq_logistic.ml
other/ # 根据具体情况自行添加
    ...
result/ #结果展示
    log/
       best_model/ #　针对最好的模型的详细信息
            PR.json
            error_tag.json
        ml_rate.plk
        logfile.plk
        3plus3arr.plk
    show/ # 组合模型的全部结果
        result.csv
        result.xlsx
    vector/ # 文本翻译后的词向量
        result.csv
        result.xlsx
__init__.py
loocv_model.py # 对组合模型进行留一验证,并且将结果写入csv和excel文件
ml_model.py # 集成sklearn常用的自然语言的机器学习模型
operate_data.py # 将文本处理成词向量,并且保存了logfile.plk
README.md
demo.py # 使用者(非开发者)调用框架的样例
run_best.py # 人工找出loocv_model.py的最好结果后,进行最好模型的更详细分析
```

### 1.2 使用方法
**请参照`demo.py`的代码**    
1. 打开`demo.py`
2. 如果：
    - **直接使用我们训练好的模型，在`if __name__=='__main__':`里面输入：**
    ```python
    od.loadStopwords()
    od.loadEmotionwords()
    od.loadWords(od.stopList)
    od.loadDocument(od.stopList)
    ##### 单例模式 #####
    predictor = Predictor()
    predictor.load_model()
    predictor.set_mode(mode="wordfreq") # 以上代码是初始化配置，只需要调用一次

    ##### 下面的代码可以循环调用 #####
    news = "                                                    《经济通通讯社13日专讯》日股早市偏软,日经225指数报18312跌239点。  美元兑日圆疲软,新报108﹒78╱80。(tt)" # 这是您的新闻样本

    predictor.set_news(news=news)
    predictor.trans_vec()

    tag = predictor() # 分类结果
    ```

    - 需要重新训练模型，那么在配置好`1.1`的文件后，在`if __name__=='__main__':`里面输入：
    ```python
    best_vector = "wordfreq"
    best_model = 1  # linearLogistic
    save_model(best_vector, best_model)
    ##### 单例模式 #####
    predictor = Predictor()
    predictor.load_model()
    predictor.set_mode(mode="wordfreq") # 以上代码是初始化配置，只需要调用一次

    ##### 下面的代码可以循环调用 #####
    news = "                                                    《经济通通讯社13日专讯》日股早市偏软,日经225指数报18312跌239点。  美元兑日圆疲软,新报108﹒78╱80。(tt)" # 这是您的新闻样本

    predictor.set_news(news=news)
    predictor.trans_vec()

    tag = predictor()
    ```
3. 成功后，相信你也差不多理解框架的用法，请尽情使用吧。

