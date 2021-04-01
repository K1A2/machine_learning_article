import csv
import os
import random

path = os.getcwd() + "/set/excludeWords.csv"
f = open(path, 'r', encoding='utf-8')
e = csv.reader(f)
exclude = next(e)
print(exclude)

daum_article_categoty = ["society", "politics", "economic", "foreign", "culture", "entertain", "sports", "digital"]
l1,l2,l3,l4,l5,l6,l7,l8 = list(),list(),list(),list(),list(),list(),list(),list()

for categoryInt in range(0, len(daum_article_categoty)):
    print("--------------------", daum_article_categoty[categoryInt], "--------------------")
    c = categoryInt
    i = 0
    recent = 0
    # aa2 = list()
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
                        if c == 0:
                            l1.append([c, line])
                            # print('기사 갯수', format(len(l1), ","), "/ +",format(len(l1) - recent, ","))
                            recent = len(l1)
                        elif c == 1:
                            l2.append([c, line])
                            # print('기사 갯수', format(len(l2), ","), "/ +",format(len(l2) - recent, ","))
                            recent = len(l2)
                        elif c == 2:
                            l3.append([c, line])
                            # print('기사 갯수', format(len(l3), ","), "/ +",format(len(l3) - recent, ","))
                            recent = len(l3)
                        elif c == 3:
                            l4.append([c, line])
                            # print('기사 갯수', format(len(l4), ","), "/ +",format(len(l4) - recent, ","))
                            recent = len(l4)
                        elif c == 4:
                            l5.append([c, line])
                            # print('기사 갯수', format(len(l5), ","), "/ +",format(len(l5) - recent, ","))
                            recent = len(l5)
                        elif c == 5:
                            l6.append([c, line])
                            # print('기사 갯수', format(len(l6), ","), "/ +",format(len(l6) - recent, ","))
                            recent = len(l6)
                        elif c == 6:
                            l7.append([c, line])
                            # print('기사 갯수', format(len(l7), ","), "/ +",format(len(l7) - recent, ","))
                            recent = len(l7)
                        elif c == 7:
                            l8.append([c, line])
                            # print('기사 갯수', format(len(l8), ","), "/ +",format(len(l8) - recent, ","))
                            recent = len(l8)
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
                        if c == 0:
                            l1.append([c, line])
                            # print('기사 갯수', format(len(l1), ","), "/ +",format(len(l1) - recent, ","))
                            recent = len(l1)
                        elif c == 1:
                            l2.append([c, line])
                            # print('기사 갯수', format(len(l2), ","), "/ +",format(len(l2) - recent, ","))
                            recent = len(l2)
                        elif c == 2:
                            l3.append([c, line])
                            # print('기사 갯수', format(len(l3), ","), "/ +",format(len(l3) - recent, ","))
                            recent = len(l3)
                        elif c == 3:
                            l4.append([c, line])
                            # print('기사 갯수', format(len(l4), ","), "/ +",format(len(l4) - recent, ","))
                            recent = len(l4)
                        elif c == 4:
                            l5.append([c, line])
                            # print('기사 갯수', format(len(l5), ","), "/ +",format(len(l5) - recent, ","))
                            recent = len(l5)
                        elif c == 5:
                            l6.append([c, line])
                            # print('기사 갯수', format(len(l6), ","), "/ +",format(len(l6) - recent, ","))
                            recent = len(l6)
                        elif c == 6:
                            l7.append([c, line])
                            # print('기사 갯수', format(len(l7), ","), "/ +",format(len(l7) - recent, ","))
                            recent = len(l7)
                        elif c == 7:
                            l8.append([c, line])
                            # print('기사 갯수', format(len(l8), ","), "/ +",format(len(l8) - recent, ","))
                            recent = len(l8)
    print("*************************", daum_article_categoty[categoryInt], "끝 *************************")

print("1234567##################################################")
random.shuffle(l1)
random.shuffle(l2)
random.shuffle(l3)
random.shuffle(l6)
random.shuffle(l7)
lls = [l1,l2,l3,l6,l7]

m = min([len(i) for i in lls])
print('min',m)

articles = list()
wordsDic = dict()
for i in range(0, len(lls)):
    print(daum_article_categoty[i], format(len(lls[i]), ','))
    for c in range(0, m):
        l = lls[i][c]
        articles.append(l)
        for w in l[1]:
            if w not in exclude:
                if w in wordsDic:
                    wordsDic[w] += 1
                else:
                    wordsDic[w] = 1

wordsDic_last = dict()
i = 1
for k, v in wordsDic.items():
    wordsDic_last[k] = i
    i += 1

random.shuffle(articles)
wordsDic_last = {k: v for k, v in sorted(wordsDic_last.items(), key=lambda item: item[1], reverse=True)}
# print(wordsDic_last)

allArticles_last = list()
category_last = list()
for l in articles:
    category_last.append(l[0])
    tokens = list()
    for w in l[1]:
        if w in wordsDic_last:
            tokens.append(wordsDic_last[w])
    allArticles_last.append(tokens)


iii = 0
print('Words save start')
f = open(os.getcwd() + "/set/11y_12367/AllallArticles.csv", 'w', encoding='utf-8')
wr = csv.writer(f)
for l in allArticles_last:
    if iii % 10000 == 0:
        print(iii,'번쨰 기사 완료', len(allArticles_last) - iii,'개 남음')
    iii+=1
    wr.writerow(l)
f.close()
print('Words save finish')

print('Category save start')
f = open(os.getcwd() + "/set/11y_12367/AllallCategores.csv", 'w', encoding='utf-8')
wr = csv.writer(f)
wr.writerow(category_last)
f.close()
print('Category save finish')

print('Word Token save start')
f = open(os.getcwd() + "/set/11y_12367/AllwordsToken.csv", 'w', encoding='utf-8')
w = csv.DictWriter(f, wordsDic_last.keys())
w.writeheader()
w.writerow(wordsDic_last)
f.close()
print('Word Token save finish')