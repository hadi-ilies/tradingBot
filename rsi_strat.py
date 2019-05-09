def rsi_inc(candles):
    res = 0
    i = 0
    for candle in candles:
        if candle.getOpen() < candle.getClose():
            res += candle.getClose() - candle.getOpen()
            i = i + 1
    if i == 0:
        return i
    return res / i

def rsi_dec(candles):
    res = 0
    i = 0
    for candle in candles:
        if candle.getOpen() > candle.getClose():
            res += candle.getOpen() - candle.getClose()
            i += 1
    if i == 0:
        return 0
    return res / i

def compute_rsi(candles):
    inc = rsi_inc(candles)
    dec = rsi_dec(candles)
    return 100 - (100 / (1 + (inc / dec)))

def rsi_strat(candles):
    prev = compute_rsi(candles[0:len(candles) - 1])
    new = compute_rsi(candles[1:])
    if prev > 70 and new <= 70:
        return (-1)
    elif prev < 30 and new >= 30:
        return (1)
    else:
        return 0