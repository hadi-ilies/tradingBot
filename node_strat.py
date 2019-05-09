import math
nb_candle_g = 30

def sma(candles):
    res = 0
    for x in candles:
        res += x.getClose()
    return (res / nb_candle_g)

##NOTE standartDeviation == l'écart type
def standardDeviation(candles):
    deviation = 0.0
    average = sma(candles)
    for x in candles:
        deviation += pow(x.getClose() - average, 2)
    return math.sqrt(deviation / nb_candle_g)

def node_strat(candles):
    x = sma(candles[1:])
    std_dev = standardDeviation(candles[1:])
    A1 = x + std_dev * 2
    B1 = x + std_dev
    B2 = x - std_dev
    A2 = x - std_dev * 2
    close = candles[-1].getClose()
    if (close >= B1 and close <= A1):
        return 1
    elif (close < B2 and close >= A2):
        return -1
    else:
        return 0