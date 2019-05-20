import os
import pandas as pd

# 1. 导入数据
path = r"E:\pythonProjects\cluebearpython\chapter8\data"
origin_file = "comment_nm.xlsx"
comments_df = pd.read_excel(os.path.join(path, origin_file), encoding="utf8")
comments_df.shape
comments_df.head()
# 留个备份, 这样之后覆盖写错了就不用重新覆盖
comments_df2 = comments_df.copy()

# 2. 清洗数据, 删除空的数据
def clean_sents(txt):
    txt = str(txt) if txt is not None else ""
    if len(txt) == 0:
        return None
    else:
        return txt

comments_df2["评价内容"] = comments_df2["评价内容"].apply(clean_sents)
comments_df2 = comments_df2[comments_df2["评价内容"] != "nan"]
len(comments_df2)

# 2. 引入停用词文本
import jieba

stopwords_file = "stopwords.txt"
with open(os.path.join(path, stopwords_file), "r", encoding="utf8") as f:
    stopwords_list = [word.strip() for word in f.read()]

def filter_stopwords(txt):
    """过滤停用词"""
    sent = jieba.lcut(txt)
    words = []
    for word in sent:
        word = word.strip()
        if(word in stopwords_list):
            continue
        else:
            words.append(word)
    return words

comments_df2["评价内容"] = comments_df2["评价内容"].apply(filter_stopwords)
comments_df2.head()

# 3. 切分训练集和验证集和测试集
from sklearn.model_selection import train_test_split

train_X, val_X, train_y, val_y = train_test_split(comments_df2["评价内容"], comments_df2["评分"], test_size=0.3)
val_X, test_X, val_y, test_y = train_test_split(val_X, val_y, test_size=0.5)

# 4. 统计词频
from nltk import FreqDist

all_words = []
for comment in comments_df2["评价内容"]:
    all_words.extend(comment)

len(all_words)

fdisk = FreqDist(all_words)
TOP_COMMON_WORDS = 1000
most_common_words = fdisk.most_common(TOP_COMMON_WORDS)
most_common_words[:10]

# 5. 生成前N个高频词的词云
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

mask = np.array(Image.open(os.path.join(path, "火锅图片.png")))
wc = WordCloud(font_path=os.path.join(path, "simkai.ttf"),
               background_color="white",
               contour_width=3,
               contour_color='steelblue',
               mask=mask,
               width=1000,
               height=1000)


wc.generate_from_frequencies(dict(most_common_words))
fig = plt.figure(figsize=(10, 10))
plt.imshow(wc)
plt.axis("off")
plt.savefig(os.path.join(path, "火锅词云.png"), dpi=1000)
plt.show()

# 6.生成TF-IDF
from nltk.text import TextCollection

tfidf_generator = TextCollection(train_X.values.tolist())

def extract_tfidf(texts, targets, text_collection, common_words):
    """
    提取文本的tf-idf.
        texts: 输入的文本.
        targets: 对应的评价.
        text_collection: 预先初始化的TextCollection.
        common_words: 输入的前N个词作为特征进行计算.
    """
    # 得到行向量的维度
    n_sample = len(texts)
    # 得到列向量的维度
    n_feat = len(common_words)

    # 初始化X矩阵, X为最后要输出的TF-IDF矩阵
    X = np.zeros([n_sample, n_feat])
    y = np.zeros(n_sample)
    for i, text in enumerate(texts):
        if i % 5000 == 0:
            print("已经完成{}个样本的特征提取.".format(i))

        # 每一行对应一个文档, 计算这个文档中的词的tf-idf, 没出现的词则为0
        feature_vector = []
        for word in common_words:
            if word in text:
                tf_idf = text_collection.tf_idf(word, text)
            else:
                tf_idf = 0.0

            feature_vector.append(tf_idf)

        X[i, :] = np.array(feature_vector)
        y[i] = targets.iloc[i]

    return X, y

cleaned_train_X, cleaned_train_y = extract_tfidf(train_X, train_y, tfidf_generator, dict(most_common_words).keys())
cleaned_val_X, cleaned_val_y = extract_tfidf(val_X, val_y, tfidf_generator, dict(most_common_words).keys())

# 7. 特征提取
from sklearn import svm

clf = svm.SVC()
clf.fit(cleaned_train_X, cleaned_train_y)
clf.score(cleaned_train_X, cleaned_train_y)
clf.score(cleaned_val_X, cleaned_val_y)
