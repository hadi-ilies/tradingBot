import math

nb_candle_g = 30

##NOTE Déviation standard = l'écart type

def sma(candles, n):
    res = 0
    for x in candles:
        res += x.getClose()
    return (res / n)

def standardDeviation(candles, n):
    deviation = 0.0
    average = sma(candles, n)
    for x in candles:
        deviation += pow(x.getClose() - average, 2)
    return math.sqrt(deviation / n)

def bollinger_strat(candles, n):
    n = n - 1
    x = sma(candles[-n:], n)
    std_dev = standardDeviation(candles[-n:], n)
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