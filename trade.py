#!/usr/local/bin/python3.7
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def trade ():
    #importing data
    df = pd.read_csv('training_set.csv')
    USDT_BTC = df[0:720]
    USDT_ETH = df[720:1441]
    BTC_ETH = df[1441:2160]
    print(USDT_BTC)
    print("---------------------------------------------")
    print(USDT_ETH)
    print("---------------------------------------------")
    print(BTC_ETH)
if __name__ == '__main__':
    trade()