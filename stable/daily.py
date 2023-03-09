from time import time
from pyee.twisted import TwistedEventEmitter

DAILY_TOKENS = 100
DAILY_PREDIOD = 1 * 60 * 60 * 24


class DailyTokens:
    def __init__(self, last_daily: "float | str" = -1):
        self.__last_daily = float(last_daily)
        self.__events = TwistedEventEmitter()

    def __str__(self) -> str:
        return str(self.__last_daily)

    def obtain(self):
        self.__last_daily = time()
        self.__events.emit("obtained", DAILY_TOKENS)

        return DAILY_TOKENS
    
    def on_obtain(self, callback):
        self.__events.on("obtained", callback)

    def available(self) -> bool:
        return time() - self.__last_daily > DAILY_PREDIOD