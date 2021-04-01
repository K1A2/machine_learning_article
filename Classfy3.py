from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding, Dropout
from keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt
import numpy
import csv
import os

model = Sequential()
model.add(Embedding(317424,600, input_length=600))
model.add(LSTM(600, activation='tanh'))
model.add(Dropout(0.25))
model.add(Dense(450, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(270, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(135, activation='relu'))
model.add(Dense(8, activation='softmax'))
print('modeling complete')

f = open(os.getcwd() + "/set/AllallCategores.csv", 'r', encoding='utf-8')
yy = csv.reader(f)
Y = []
i = 1
for l in yy:
    for w in l:
        w = int(w)
        Y.append(w)
        # if i == 7000000:
        #     print('break')
        #     break
        i+=1
f.close()
print(Y)

f = open(os.getcwd() + "/set/AllallArticles.csv", 'r', encoding='utf-8')
xx = csv.reader(f)

X = list()
# X = numpy.zeros((0,600))
# print(X)

counts = dict()
co = 1
dump = list()
for l in xx:
    l = list(map(int, l))
    l.sort()
    X.append(l)
    # nl = list()
    # if len(l) <= 600:
    #     for nn in l:
    #         nl.append(nn)
    #     for i in range(0, 600 - len(l)):
    #         nl.append(0)
    # else:
    #     for i in range(0, 600):
    #         nl.append(l[i])
    # nl = numpy.array([nl])
    # X = numpy.append(X, nl, axis=0)
    # count = len(l)
    # if count in counts:
    #     counts[count] += 1
    # else:
    #     counts[count] = 1
    # dump.append(nl)
    if co % 1000000 == 0:
        print(format(co, ","), end=" ")
        # for nin in range(0, len(dump)):
        #     np = numpy.array([dump[0]])
        #     X = numpy.append(X, np, axis=0)
        #     dump.remove(dump[0])
        print('번', len(X))
    # if co == 7000000:
    #         print('break')
    #         break
    co += 1
f.close()
# counts = sorted(counts.items())
# X = numpy.genfromtxt(os.getcwd() + "/set/AllallArticles.csv", delimiter=',')
# X = numpy.genfromtxt(os.getcwd() + "/set/AllallArticles.csv",encoding='utf-8',delimiter='\n',dtype=None)
X = numpy.array(X)
Y = numpy.array(Y)
print(X)
print(Y)

# plt.plot([k for k, v in counts], [v for k, v in counts])
# plt.show()
# plt.close()
# plt.cla()
# plt.clf()
# i = 600

x = sequence.pad_sequences(X, maxlen=600)
y = np_utils.to_categorical(Y)
# x = X
print(x, 'X')
print(y, 'Y')

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.3, random_state=77)
print('Split Complete')

print(len(X_train), X_train.shape, len(x))
print(len(Y_train), Y_train.shape, len(y))
print(len(X_test), X_test.shape, len(x))
print(len(Y_test), Y_test.shape, len(y))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

MODEL_DIR = './model/'
if not os.path.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)

modelpath = './model/11y/Drop{epoch:02d}-{val_loss:.4f}.hdf5'
checkpinter = ModelCheckpoint(filepath=modelpath, monitor='val_loss', verbose=1)
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=2)

history = model.fit(X_train, Y_train, batch_size=256, epochs=10,
                        validation_data=(X_test, Y_test), callbacks=[checkpinter, early_stopping_callback])
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