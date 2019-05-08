import math
from dictionary import *
from Candle import Candle
import statistics

nb_candle_g = 20
std_mult = 2

class Bot:
    def __init__(self):
        self.usdt_eth_candles = list()
        self.usdt_btc_candles = list()
        self.btc_eth_candles = list()

    def settings(self, command):
        if (command[0] == "initial_stack"):
            settings.update({"USDT" : command[1]})
        else:
            settings.update({command[0] : command[1]})

    def next_candles(self, command):
        candles = command.split(';')
        for strCandle in candles:
            candle = strCandle.split(',')
            if (candle[0] == "BTC_ETH"):
                self.btc_eth_candles.append(Candle(candle))
                if (len(self.btc_eth_candles) > nb_candle_g + 1):
                    self.btc_eth_candles.pop(0)
            elif (candle[0] == "USDT_BTC"):
                self.usdt_btc_candles.append(Candle(candle))
                if (len(self.usdt_btc_candles) > nb_candle_g + 1):
                    self.usdt_btc_candles.pop(0)
            elif (candle[0] == "USDT_ETH"):
                self.usdt_eth_candles.append(Candle(candle))
                if (len(self.usdt_eth_candles) > nb_candle_g + 1):
                    self.usdt_eth_candles.pop(0)

    #TODO maybe we should remove this function.
    def stacks(self, command):
        # BTC:0.00379240,ETH:0.00000000,USDT:957.90
        stacks = command.split(",")
        for stack in stacks:
            money = stack.split(":")
            settings.update({money[0] : money[1]})

    #TODO maybe the site can send not enough candles so it may result in error
    def sma(self, candles):
        res = 0
        for x in candles:
            res += x.getClose()
        res -= candles[-1].getClose()
        return (res / nb_candle_g)

    ##NOTE standartDeviation == l'écart type
    def standardDeviation(self, candles):
        deviation = 0.0
        average = self.sma(candles)
        for x in candles:
            deviation += pow(x.getClose() - average, 2)
        deviation -= pow(candles[-1].getClose() - average, 2)
        return math.sqrt(deviation / nb_candle_g)

    def compute_node(self, candles):
        average = 0
        for x in candles:
            average += math.fabs(x.getClose() - x.getOpen())
        average -= math.fabs(candles[-1].getClose() - candles[-1].getOpen())
        average /= nb_candle_g
        current = math.fabs(candles[-1].getClose() - candles[-1].getOpen())
        if current > average:
           return(1 - (average / current))
        if current < average:
            return(1 - (current / average))
        return (0)

    def compute_money(self, candles):
        sma = self.sma(candles)
        stand_dev = self.standardDeviation(candles)
        top = sma + stand_dev * std_mult
        bot = sma - stand_dev * std_mult
        close = candles[-1].getClose()
        # print ("SMA : " + str(sma))
        # print ("Stand dev : " + str(stand_dev))
        # print ("Top : " + str(top))
        # print ("Bot : " + str(bot))
        # print ("Close : " + str(close))
        if close > top:
            return (1)
        elif close < bot:
            return (-1)
        else:
            return (0.0)

    def node_strat(self, candles):
        node_indice = self.compute_node(candles)
        # print ("Indice de noeud : " + str(node_indice))
        if node_indice < 0.4:
            return (0.0)
        else:
            return (self.compute_money(candles))

    #NOTE for x in candles[::-1]:
    #   print item

    def rsi_inc(self, candles):
        res = 0
        i = 0
        for candle in candles:
            if candle.getOpen() < candle.getClose():
                res += candle.getClose() - candle.getOpen()
                i = i + 1
        if i == 0:
            return i
        return res / i

    def rsi_dec(self, candles):
        res = 0
        i = 0
        for candle in candles:
            if candle.getOpen() > candle.getClose():
                res += candle.getOpen() - candle.getClose()
                i += 1
        if i == 0:
            return 0
        return res / i

    def compute_rsi(self, candles):
        inc = self.rsi_inc(candles)
        dec = self.rsi_dec(candles)
        return 100 - (100 / (1 + (inc / dec)))

    def rsi_strat(self, candles):
        prev = self.compute_rsi(candles[0:len(candles) - 1])
        new = self.compute_rsi(candles[1:])
        if prev > 70 and new <= 70:
            return (-1)
        elif prev < 30 and new >= 30:
            return (1)
        else:
            return 0

    def action(self, candles):
        node = self.node_strat(candles)
        rsi = self.rsi_strat(candles)
        print("NODE I : " + str(node))
        print("RSI  I : " + str(rsi))
        result = ""
        if (node == 1 and rsi == 1):
            result += "buy " + candles[0].getPair() + " "
            if (candles[0].getName() == "BTC_ETH"):
                toBuy = float (settings["btc"]) / candles[-1].getClose()
            else:
                toBuy = float(settings["usdt"] / candles[-1].getClose())
            result += str(toBuy) + ";"
        elif (node != 0 and rsi != 0):
            result += "sell " + candles[0].getPair() + " "
            if (candles[0].getName() == "USDT_BTC"):
                toSell = float (settings["btc"] / candles[-1].getClose())
            else:
                toSell = float (settings["eth"] / candles[-1].getClose())
            result += str(toSell) + ";"
        return result

    def sendAction(self):
        usdt_btc = self.action(self.usdt_btc_candles)
        usdt_eth = self.action(self.usdt_eth_candles)
        btc_eth = self.action(self.btc_eth_candles)
        if (usdt_btc == "" and usdt_eth == "" and btc_eth == ""):
            print("pass")
        else:
            print(usdt_btc + usdt_eth + btc_eth)

    def update(self, command):
        if (command[0] == "next_candles"):
            self.next_candles(command[1])
        elif (command[0] == "stacks"):
            self.stacks(command[1])

    def parser(self, command):
        if (command[0] == "settings"):
            self.settings(command[1:])
        elif (command[0] == "update"):
            self.update(command[2:])
        elif (command[0] == "action"):
            self.sendAction()
        else:
            print("KO")
            exit()

    def run(self):
        while (True):
            string = input()
            string = string.split(" ")
            self.parser(string)
            ##code