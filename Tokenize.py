import csv
import os
import random
from multiprocessing import Process, Manager
import time

path = os.getcwd() + "/set/excludeWords.csv"
f = open(path, 'r', encoding='utf-8')
e = csv.reader(f)
exclude = []
for l in e:
    exclude.append(l)
# print(exclude)

daum_article_categoty = ["society", "politics", "economic", "foreign", "culture", "entertain", "sports", "digital"]
aa2 = list()
dd = dict()
recent = 0
for categoryInt in range(0, len(daum_article_categoty)):
    print("--------------------", daum_article_categoty[categoryInt], "--------------------")
    c = categoryInt
    i = 0
    for y in range(2010, 2021):
        if y == 2020:
            for m in range(1, 6):
                aa = list()
                path = os.getcwd() + "/set/articles/" + daum_article_categoty[c] + "/" + str(y) + "/" + str(
                    m) + "/articles.csv"
                print(path)
                f = open(path, 'r', encoding='utf-8')
                rdr = csv.reader(f)
                for line in rdr:
                    if line not in aa:
                        aa.append(line)
                        aa2.append([c, line])
                        for w in line:
                            if w in dd:
                                dd[w] += 1
                            else:
                                dd[w] = 1
                print('기사 갯수', format(len(aa2), ","), "/ +",format(len(aa2) - recent, ","))
                recent = len(aa2)
        else:
            for m in range(1, 13):
                aa = list()
                path = os.getcwd() + "/set/articles/" + daum_article_categoty[c] + "/" + str(y) + "/" + str(
                    m) + "/articles.csv"
                print(path)
                f = open(path, 'r', encoding='utf-8')
                rdr = csv.reader(f)
                for line in rdr:
                    if line not in aa:
                        aa.append(line)
                        aa2.append([c, line])
                        for w in line:
                            if w in dd:
                                dd[w] += 1
                            else:
                                dd[w] = 1
                print('기사 갯수', format(len(aa2), ","), "/ +",format(len(aa2) - recent, ","))
                recent = len(aa2)
    print("*************************", daum_article_categoty[categoryInt], "끝 *************************")

print("##################################################")
# print(aa2)
print('wordDic start')
wordsDic_sorted = {k: v for k, v in sorted(dd.items(), key=lambda item: item[1], reverse=True)}
wordsDic_last = dict()
count = 1
for k, v in wordsDic_sorted.items():
    if k not in exclude[0]:
        if count % 10000 == 0:
            print(count,'번쨰 단어',k)
        wordsDic_last[k] = count
        count += 1
print('wordDic finish')

print('Tokenize start')
allArticles_last = list()
category_last = list()
random.shuffle(aa2)
iii = 0
for i in aa2:
    c = i[0]
    li = list()
    for w in i[1]:
        if w not in exclude[0]:
            li.append(wordsDic_last[w])
    if iii % 10000 == 0:
        print(iii,'번쨰 기사 완료', len(aa2) - iii,'개 남음')
    iii+=1
    category_last.append(c)
    allArticles_last.append(li)
print('Tokenize finish')

iii = 0
print('Words save start')
f = open(os.getcwd() + "/set/AllallArticles.csv", 'w', encoding='utf-8')
wr = csv.writer(f)
for l in allArticles_last:
    if iii % 10000 == 0:
        print(iii,'번쨰 기사 완료', len(allArticles_last) - iii,'개 남음')
    iii+=1
    wr.writerow(l)
f.close()
print('Words save finish')

print('Category save start')
f = open(os.getcwd() + "/set/AllallCategores.csv", 'w', encoding='utf-8')
wr = csv.writer(f)
wr.writerow(category_last)
f.close()
print('Category save finish')

print('Word Token save start')
f = open(os.getcwd() + "/set/AllwordsToken.csv", 'w', encoding='utf-8')
w = csv.DictWriter(f, wordsDic_last.keys())
w.writeheader()
w.writerow(wordsDic_last)
f.close()
print('Word Token save finish')