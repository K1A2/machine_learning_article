from keras.models import load_model
from konlpy.tag import Mecab
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding
import numpy
import csv
import re

model = load_model('./model/02-0.3217.hdf5')
model.summary()

daum_article_categoty = ["society", "politics", "economic", "foreign", "culture", "entertain", "sports", "digital"]

def analyzeWord(s):
    okt = Mecab()
    munjang = str(s).split('.')

    words = []
    for m in munjang:
        hangul = re.compile('[^ ㄱ-ㅣ가-힣0-9a-zA-Z]+')  # ???? ????? ?????? ??? ????
        result = hangul.sub(' ', m)  # ???? ????? ?????? ??? ?κ??? ????
        result1 = okt.nouns(result)
        if len(result1) != 0:
            words += result1

    return words

article = input("??????: ")

wordToken1 = []
wordToken2 = []
path = "./set/wordsToken.csv"
f = open(path, 'r', encoding='utf-8')
rdr = csv.reader(f)
c = 0
for i in rdr:
    if c == 0:
        wordToken1 = i
    else:
        i = list(map(int, i))
        wordToken2 = i
    c+=1
f.close()
token_dic = dict()
for i in range(0, len(wordToken1)):
    token_dic[wordToken1[i]] = wordToken2[i]

excludeWords = list()
path = "./set/excludeWords.csv"
f = open(path, 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    excludeWords = line
f.close()

words = analyzeWord(article)
print(words)
words_dic = dict()
words_l = list()
for w in words:
    if w not in excludeWords:
        if words_l not in words_l:
            words_l.append(w)

for w in words_l:
    if w in token_dic:
        words_dic[w] = token_dic[w]

wordsDic_sorted = {k: v for k, v in sorted(words_dic.items(), key=lambda item: item[1], reverse=True)}
wordsSquenced = [[v for k, v in wordsDic_sorted.items()]]

X = numpy.array(wordsSquenced)
print(X)
wordsSquenced_ = sequence.pad_sequences(X, maxlen=140)
print(wordsSquenced_)
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
print(daum_article_categoty[model.predict_classes(wordsSquenced_)[0]])