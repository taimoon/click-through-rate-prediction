# deployment.py
import pandas as pd
import numpy as np
from ELT import *
import joblib

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


window_time = 10000
chunksize = 1000
clf = joblib.load('saved_model/xgb_1.joblib')
gen_df = get_data_generator('test_transaction.csv', chunksize=chunksize)

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [])

def init():
    ax.set_xlabel('timestamp')
    ax.set_ylabel('isFraud')
    ax.set_xlim(0, 1)
    ax.set_ylim(-2, 2)
    return ln,

def update(frame):
    transactions = next(gen_df)
    times = transactions['TransactionDT'].values
    X = preprocessor.fit_transform(transactions)
    y = clf.predict(X)
    if frame > window_time // chunksize:
        del xdata[0:chunksize]
        del ydata[0:chunksize]
    xdata.extend(times)
    ydata.extend(y)
    ax.set_xlim(xdata[0], xdata[-1])
    ln.set_data(xdata, ydata)
    return ln,

if __name__ == '__main__':
    ani = FuncAnimation(fig, update,
                        init_func=init, blit=False)
    plt.show()
