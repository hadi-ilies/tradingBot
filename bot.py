import math
from node_strat import node_strat
from rsi_strat import rsi_strat
from dictionary import settings
from Candle import Candle
import statistics

nb_candle_g = 30
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

    def stacks(self, command):
        # BTC:0.00379240,ETH:0.00000000,USDT:957.90
        stacks = command.split(",")
        for stack in stacks:
            money = stack.split(":")
            settings.update({money[0] : money[1]})

    def update(self, command):
        if (command[0] == "next_candles"):
            self.next_candles(command[1])
        elif (command[0] == "stacks"):
            self.stacks(command[1])

    def action(self, candles):
        node = node_strat(candles)
        rsi = rsi_strat(candles)
        result = ""
        toSell = 0
        toBuy = 0

        pair = candles[-1].getPair().split("_")
        acc1 = float(settings[pair[0]])
        acc2 = float(settings[pair[1]])
        fee = float(settings["transaction_fee_percent"])

        if (node == 1 or rsi == 1):
            if (acc1 != 0):
                toBuy = acc1 / candles[-1].getClose()
        elif (node == -1 or rsi == -1):
            if (acc2 != 0):
                toSell = acc2
        if (toBuy > 0):
            result += "buy " + candles[-1].getPair() + " " + str(toBuy) + ";"
            newAcc1 = acc1 - (toBuy * candles[-1].getClose())
            settings.update({pair[0] : str(newAcc1)})
            settings.update({pair[1] : str(acc2 + toBuy)})
        elif (toSell > 0):
            result += "sell " + candles[-1].getPair() + " " + str(toSell) + ";"
            newAcc1 = acc1 + toSell * candles[-1].getClose()
            settings.update({pair[0] : str(newAcc1)})
            settings.update({pair[1] : str(acc2 - toSell)})
        return result

    def sendAction(self):
        # print ("\nBEFORE\nUSDT : " + str(float(settings["USDT"])))
        # print ("BTC : " + str(float(settings["BTC"])))
        # print ("ETH : " + str(float(settings["ETH"])))
        usdt_btc = self.action(self.usdt_btc_candles)
        usdt_eth = self.action(self.usdt_eth_candles)
        btc_eth = self.action(self.btc_eth_candles)
        if (usdt_btc == "" and usdt_eth == "" and btc_eth == ""):
            print("pass")
        else:
            # print ("\nAFTER\nUSDT : " + str(float(settings["USDT"])))
            # print ("BTC : " + str(float(settings["BTC"])))
            # print ("ETH : " + str(float(settings["ETH"])))
            print(usdt_btc + usdt_eth + btc_eth)

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