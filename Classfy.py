from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy
import csv
import os

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

plt.plot([k for k, v in counts], [v for k, v in counts])
plt.show()
plt.close()
plt.cla()
plt.clf()
i = int(input('max:'))

x = sequence.pad_sequences(X, maxlen=i)
y = np_utils.to_categorical(Y)
print(x, 'X')
print(y, 'Y')

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.3, random_state=77)
print('Split Complete')

print(len(X_train), X_train.shape, len(x))
print(len(Y_train), Y_train.shape, len(y))
print(len(X_test), X_test.shape, len(x))
print(len(Y_test), Y_test.shape, len(y))

model = Sequential()
model.add(Embedding(317424, i, input_length=i))
model.add(LSTM(i, activation='tanh'))
model.add(Dense(6, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print('modeling complete')

history = model.fit(X_train, Y_train, batch_size=1000, epochs=5, validation_data=(X_test, Y_test))

print("\n Test Accuracy: %.4f" % (model.evaluate(X_test, Y_test)[1]))

y_vloss = history.history['val_loss']
y_loss = history.history['loss']

x_len = numpy.arange(len(y_loss))
plt.plot(x_len, y_vloss, marker='.', c='red', label='Testset_loss')
plt.plot(x_len, y_loss, marker='.', c='blue', label='Trainset_loss')

plt.legend(loc='upper right')
plt.grid()
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()

model.save('categorical_article_model1.h5')