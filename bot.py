import re
from dictionnary import *

class Candle:
    def __init__(self, candles):
        self._pair = candles[0]
        self._date = int(candles[1])
        self._high = float(candles[2])
        self._low = float(candles[3])
        self._open = float(candles[4])
        self._close = float(candles[5])
        self._volume = float(candles[6])
    def getPair(self):
        return self._pair

    def getDate(self):
        return self._date

    def getHigh(self):
        return self._high

    def getLow(self):
        return self._low

    def getOpen(self):
        return self._open

    def getClose(self):
        return self._close

    def getVolume(self):
        return self._volume

class Bot:
    def __init__(self):
        self.usdt_eth_candles = list()
        self.usdt_btc_candles = list()
        self.btc_eth_candles = list()

    def settings(self, command):
        print(settings)
        settings.update({command[0] : command[1]})
        print("After " + settings[command[0]])

    def next_candles(self, command):
        candles = command.split(';')
        for strCandle in candles:
            candle = strCandle.split(',')
            if (candle[0] == "BTC_ETH"):
                self.btc_eth_candles.append(Candle(candle))
            elif (candle[0] == "USDT_BTC"):
                self.usdt_btc_candles.append(Candle(candle))
            elif (candle[0] == "USDT_ETH"):
                self.usdt_eth_candles.append(Candle(candle))

    #TODO maybe we should remove this function.
    def stacks(self, command):
        print(command)

    def sendAction(self):
        print("buy,USDT_BTC,1.0")

    def update(self, command):
        if (command[0] == "next_candles"):
            self.next_candles(command[1])
        elif (command[0] == "stacks"):
            self.stacks(command[1])

    def parser(self, command):
        if (command[0] == "settings"):
            print("Settings")
            self.settings(command[1:])
        elif (command[0] == "update"):
            print("Update")
            self.update(command[2:])
        elif (command[0] == "action"):
            self.sendAction()
        else:
            print("KO")

    def run(self):
        while (True):
            string = input()
            string = string.split(" ")
            self.parser(string)