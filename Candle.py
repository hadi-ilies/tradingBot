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