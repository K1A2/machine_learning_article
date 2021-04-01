import plaidml.keras
plaidml.keras.install_backend()

from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding
from keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import keras.backend

f = open(os.getcwd() + "/set/11y_1236/AllallCategores.csv", 'r', encoding='utf-8')
yy = csv.reader(f)
Y = list(map(int, next(yy)))
f.close()
print('Load categories finish')

f = open(os.getcwd() + "/set/11y_1236/AllallArticles.csv", 'r', encoding='utf-8')
xx = csv.reader(f)
X = []
for l in xx:
    l = list(map(int, l))
    l.sort(reverse=True)
    X.append(l)
f.close()
print('Load articles finish')

maxlen = 250

X = np.array(X)
yy = np.array(Y)
x = sequence.pad_sequences(X, maxlen=maxlen)
y = np_utils.to_categorical(Y)
print(x.shape,'\n',x)
print(y.shape,'\n',y)

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.3, random_state=1024)
print('Split Complete')

f = open(os.getcwd() + "/set/11y_1236/AllwordsToken.csv", 'r', encoding='utf-8')
ww = csv.reader(f)
next(ww)
wordsCount = max(list(map(int, next(ww))))

model = Sequential()
# model.add(Embedding(wordsCount + 1, maxlen, input_length=maxlen))
model.add(LSTM(maxlen, activation='tanh'))
model.add(Dense(6, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print("model compile complete")

MODEL_DIR = './model/11y_1236/'
if not os.path.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)

modelpath = './model/11y_1236/Drop{epoch:02d}-{val_loss:.4f}.hdf5'
checkpinter = ModelCheckpoint(filepath=modelpath, monitor='val_loss', verbose=1)
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=2)

history = model.fit(X_train, Y_train, batch_size=256, epochs=10,
                        validation_data=(X_test, Y_test), callbacks=[checkpinter, early_stopping_callback])
print("\n Test Accuracy: %.4f" % (model.evaluate(X_test, Y_test)[1]))

y_vloss = history.history['val_loss']
y_loss = history.history['loss']

x_len = np.arange(len(y_loss))
plt.plot(x_len, y_vloss, marker='.', c='red', label='Testset_loss')
plt.plot(x_len, y_loss, marker='.', c='blue', label='Trainset_loss')

plt.legend(loc='upper right')
plt.grid()
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()