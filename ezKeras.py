import tensorflow as tf
import os
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras import optimizers

# from tf.keras.models import Sequential  # This does not work!
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Input, Dense, GRU, Embedding
from tensorflow.python.keras.optimizers import RMSprop
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau

from pandas.tseries.offsets import MonthEnd
from pandas.tseries.offsets import Minute

# Normalize
from sklearn.preprocessing import MinMaxScaler

from keras.layers import LSTM
from keras.models import Sequential
from keras.layers import Dense
import keras.backend as K
from keras.callbacks import EarlyStopping

from keras.models import load_model


##############################################################

def main():
    machine = Machine()
    machine.run(epochs=1, units=1, batch_size=512)

# Machine learning class
class Machine():
    #def __init__(self):
        #self.data = data
        #self.fname = fname
        #self.fname = fname
        #self.data = Dataset(fname='C:\\Users\PJ\PycharmProjects\ezKeras\inner_data_new_0705.csv') # Data 생성
        #shape = self.data.X.shape[1:] # LSTM 입력계층 크기 정의
        #shape = self.data.X_train.shape[0]

    # 실행함수
    def datasetLoad(self, fname):
        #self.data = Dataset(fname='C:\\Users\PJ\PycharmProjects\ezKeras\inner_data_new_0705.csv') # Data 생성
        self.data = Dataset(fname=fname)
        #shape = self.data.X.shape[1:] # LSTM 입력계층 크기 정의
        shape = self.data.X_train.shape[0]

    def totalDatasetNumber(self):
        total = self.data.totalDataNumber()
        return total

    def trainDatasetNumber(self):
        total = self.data.trainDataNumber()
        return total

    def testDatasetNumber(self):
        total = self.data.testDataNumber()
        return total

    def datasethead(self):
        total = self.data.df_temp.head(50)
        return total

    def dayOfStart(self):
        return self.data.df_temp.index[0]

    def dayOfEnd(self):
        return self.data.df_temp.index[-1]

    def run(self, epochs, units, batch_size):
        d = self.data
        X_train, X_test, y_train, y_test = d.X_train, d.X_test, d.y_train, d.y_test
        X_train_t = d.X_train_t
        X_test_t = d.X_test_t

        K.clear_session()
        model = Sequential()  # Sequeatial Model  # 190709 : 20
        model.add(LSTM(units, input_shape=(177, 1)))  # (timestep, feature)
        model.add(Dense(3))  # output = 1
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        # self.loss = 'mean_squared_error'
        # self.optimizer = 'adam'

        model.compile(loss=d.loss, optimizer=d.optimizer, metrics=['accuracy'])
        model.summary()

        self.epochs = epochs
        self.units = units
        self.batch_size = batch_size
        # self.model = model


        early_stop = EarlyStopping(monitor='loss', patience=1, verbose=1)

        hist = model.fit(d.X_train_t, d.y_train, epochs=epochs,
                         batch_size=batch_size, verbose=1)
        # , callbacks=[early_stop]))
        print("result : \n" + str(hist))

        from keras.models import load_model
        model.save('190711_200_unit256_batch128.h5')

        target_names = ['inner_temperature', 'inner_humidity', 'inner_co2']

        y_pred = model.predict(X_test_t)

        # %matplotlib inline

        fig, loss_ax = plt.subplots()

        acc_ax = loss_ax.twinx()

        loss_ax.plot(hist.history['loss'], 'y', label='train loss')
        acc_ax.plot(hist.history['acc'], 'b', label='train acc')

        loss_ax.set_xlabel('epoch')
        loss_ax.set_ylabel('loss')
        acc_ax.set_ylabel('accuray')

        loss_ax.legend(loc='upper left')
        acc_ax.legend(loc='lower left')

        plt.show()

        y_pred = model.predict(X_test_t)
        plt.figure(figsize=(10, 5))
        plt.ylabel(target_names[1])
        plt.plot(y_test[:, 1])
        plt.plot(y_pred[:, 1])
        plt.show()


        y_pred = model.predict(X_test_t)
        plt.figure(figsize=(10, 5))
        plt.ylabel(target_names[0])
        plt.plot(y_test[:, 0])
        plt.plot(y_pred[:, 0])
        plt.show()


        y_pred = model.predict(X_test_t)
        plt.figure(figsize=(10, 5))

        plt.ylabel(target_names[2])
        plt.plot(y_test[:, 2])
        plt.plot(y_pred[:, 2])
        plt.show()


        print("\n Acc : %.4f" % (model.evaluate(X_train_t, y_train)[1]))

        print("\n Loss : %.4f" % (model.evaluate(X_train_t, y_train)[0]))

    def display_hyperParameter(self):
        #print(self.model.summary())
        print('total data : ', self.data.totalDataNumber())
        print('test data : ', self.data.testDataNumber())
        print('train data : ', self.data.trainDataNumber())
        print('epochs : ', self.epochs)
        print('units : ', self.units)
        print('batch_size : ', self.batch_size)
        print('optimizer : adam')
        print('loss function : mean_squared_error ')



class Dataset:
   # def __init__(self, fname='C:\\Users\PJ\PycharmProjects\ezKeras\inner_data_new_0705.csv'):
    def __init__(self, fname):
        self.fname = fname

        df_temp = load_data(fname=self.fname)

        split_date = pd.Timestamp('20190625 08:49:26')  # 5000

        train = df_temp.loc[:split_date, ['inner_temperature', 'inner_humidity', 'inner_co2']]
        test = df_temp.loc[split_date:, ['inner_temperature', 'inner_humidity', 'inner_co2']]

        # Scaler()
        sc = MinMaxScaler()

        train_sc = sc.fit_transform(train)
        test_sc = sc.transform(test)
        train_sc_df = pd.DataFrame(train_sc, columns=['inner_temperature', 'inner_humidity', 'inner_co2'],
                                   index=train.index)
        test_sc_df = pd.DataFrame(test_sc, columns=['inner_temperature', 'inner_humidity', 'inner_co2'],
                                  index=test.index)

        for s in range(1, 60):
            train_sc_df['shift_{}_1'.format(s)] = train_sc_df['inner_temperature'].shift(s)
            train_sc_df['shift_{}_2'.format(s)] = train_sc_df['inner_humidity'].shift(s)
            train_sc_df['shift_{}_3'.format(s)] = train_sc_df['inner_co2'].shift(s)

            test_sc_df['shift_{}_1'.format(s)] = test_sc_df['inner_temperature'].shift(s)
            test_sc_df['shift_{}_2'.format(s)] = test_sc_df['inner_humidity'].shift(s)
            test_sc_df['shift_{}_3'.format(s)] = test_sc_df['inner_co2'].shift(s)

        target_names = ['inner_temperature', 'inner_humidity', 'inner_co2']

        # d.X_train, d.X_test, d.y_train, d.y_test
        X_train = train_sc_df.dropna().drop(target_names, axis=1)
        y_train = train_sc_df.dropna()[target_names]

        X_test = test_sc_df.dropna().drop(target_names, axis=1)
        y_test = test_sc_df.dropna()[target_names]

        X_train = X_train.values
        X_test = X_test.values

        y_train = y_train.values
        y_test = y_test.values

        X_train_t = X_train.reshape(X_train.shape[0], 177, 1)
        X_test_t = X_test.reshape(X_test.shape[0], 177, 1)

        ## Number of Data ##
        self.df_temp = df_temp
        self.train = train
        self.test = test
        #######################
        self.X_train, self.X_test, self.y_train, self.y_test = X_train, X_test, y_train, y_test
        self.X_train_t = X_train_t
        self.X_test_t = X_test_t

        self.loss = 'mean_squared_error'
        self.optimizer = 'adam'


    def totalDataNumber(self):
        return str(self.df_temp.values.shape[0])

    def trainDataNumber(self):
        return str(self.train.shape[0])

    def testDataNumber(self):
        return str(self.test.values.shape[0])

    def origindataframe(self):
        return self.df_temp


def load_data(fname):
    df = pd.read_csv(fname, engine='python')
    df['date'] = pd.to_datetime(df['date']) + Minute(1)
    df = df.set_index('date')
    target_names = ['inner_temperature', 'inner_humidity', 'inner_co2']
    df_targets = df[target_names]

    return df_targets


if __name__ == '__main__':
    main()
