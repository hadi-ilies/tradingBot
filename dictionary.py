def setValue(*args, command):
    args = int(command)

settings =	{
  "timebank": 0,
  "timer_per_move": 0,
  "player_name": 0,
  "your_bot": 0,
  "candle_interval": 0,
  "candles_total": 0,
  "candles_given": 0,
  "transaction_fee_percent": 0,
  "USDT": 0,
  "BTC": 0,
  "ETH": 0,
  "candle_format": str("pair,date,high,low,open,close,volume").split(",")
}