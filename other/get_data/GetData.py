import numpy as np
import pandas as pd

df = pd.read_excel('news_r.xls')
id_list = []
news_list = []
tag_list = []
for (_id,news,tag) in zip(df['id'],df['news_content'],df['tag']):
    if tag>0:
        em = 'pos'
    elif tag==0:
        em = 'neu'
    else:
        em = 'neg'
    txtname = "%s_%d.txt" % (em,_id)
    with open(txtname,'w',encoding='utf-8') as f:
        f.write(news)
