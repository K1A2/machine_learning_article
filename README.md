# 기사 자동 류 모델 만들기
프로젝트 설명
-----------
기사 전문을 입력하면 기사가 8가지 카테고리중 어디에 속하는지 자동으로 분류해 주는 모델을 직접 학습하여 만들어 보는 프로젝트.
- 목적: 학습 하는것 자체보다는 전처리 과정을 직접 해보기 위해 진행.
- 프로젝트 기간: 2020년 7월 ~ 2020년 9월
- 이용한 라이브러리: KonlPy, Keras, numpy, matplotlib

프로젝트 진행 과정
-------
1. 학습에 사용할 기사 크롤링 시작.
    - 2010년 1월 ~ 2020년 5월까지 3일에 한번씩 그 날 작성된 기사를 모두 가져옴.
    - 문화, IT, 경제, 엔터테이먼트, 외국, 정치, 사회, 스포츠 8개의 카테고리에서 각각 기사 수집.

2. 가져온 기사 명사 추출
    - KonlPy 라이브러리를 이용해 명사만 추출후 다시 저장. [저장된 기사](https://github.com/K1A2/machine_learning_article/tree/main/set/articles)

3. 각 단어마다 고유의 번호 지정
    - 딕셔너리 이용
>[파일 형식](https://drive.google.com/file/d/15vD4DHYc2ilkL7cxql0lkFFrG0Pi2qkD/view?usp=sharing)
>-------
>8026,23541,550,12014,56,3748,77,90785,51947,110548,...422,12,171,437,648,466,425,2,200
>456,4980,4980,1833,372,805,1539,1480,265,....265,2687,1480,553,1418,322
>.....

4. 명사만 추출되어 저장된 csv파일을 불러와 고유 번호로 치환 후 다시 저장
5. 카테고리 정보를 합쳐서 하나의 csv로 저장
    - 카테고리 정보도 3번과 동일한 방법으로 저장
> [클래스 파일 형식](https://drive.google.com/file/d/1yuHrnMgpHdxzz9RJx6cLuUncO_5uZkuu/view?usp=sharing)
> -------
> 0,1,5,2,5,5,5,2,2,1,0,5,5,7,6,0,5,5,4,2,2,5,2,2,4,3,2,0,2,5,1,0,2,6,2,5,0,5,0,2,5,.....

7. 학습 진행

학습 과정
-----
[Classfy.py 참고](https://github.com/K1A2/machine_learning_article/blob/main/Classfy.py)

- 단어 저장 csv와 카테고리 분류 csv를 모두 가져와 numpy로 백터화 시킴
```python
f = open(os.getcwd() + "/set/allCategores.csv", 'r', encoding='utf-8')
yy = csv.reader(f)
Y = []
for l in yy:
    l = list(map(int, l))
    Y.append(l)
f.close()

f = open(os.getcwd() + "/set/allArticles.csv", 'r', encoding='utf-8')
xx = csv.reader(f)
X = list()
counts = dict()
for l in xx:
    l = list(map(int, l))
    l.sort(reverse=True)
    X.append(l)
    count = len(l)
    if count in counts:
        counts[count] += 1
    else:
        counts[count] = 1
f.close()
counts = sorted(counts.items())

X = numpy.array(X)
Y = numpy.array(Y)
Y = Y[0, :]
```
- Keras에 LSTM을 이용
```python
model = Sequential()
model.add(Embedding(317424, i, input_length=i))
model.add(LSTM(i, activation='tanh'))
model.add(Dense(6, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
```
완성된 모델
-----
[모델](https://drive.google.com/drive/folders/1aBBaMmJu1x1cRdzV0nz_m8NIsW2sRZg9?usp=sharing)

아쉬운점
-----
1. 명사가 아닌 조사, 동사등을 완벽히 걸러내지 못했다.
2. 각 카테고리에 학습 시킬 기사의 개수를 통일해야 하는데, 갯수를 통일하지 않았다.

참고
------
- 책
    - [모두의 딥러닝](http://www.yes24.com/Product/Goods/86611190)
    - [케라스 창시자에게 배우는 딥러닝](http://www.yes24.com/Product/Goods/65050162)
- 그밖에 여러 구글 검색 결과
