import json

from pyee.twisted import TwistedEventEmitter

from db.repositories.promocodes import PromocodesRepository


class Promocodes(PromocodesRepository):
    def __init__(self, applied: "list[str] | str" = []):
        if isinstance(applied, list):
            self.__applied: "list[str]" = applied
        if isinstance(applied, str):
            self.__applied: "list[str]" = json.loads(applied)

        self.__events = TwistedEventEmitter()

    def __str__(self) -> str:
        return json.dumps(self.__applied, sort_keys=True)

    def apply(self, code: str) -> bool:
        """
        Returns False if promocode doesn't exist.
        """
        promocode = self.find(code)
        if not promocode: return False
        
        self.__applied.append(promocode.code)
        self.__events.emit("applied", promocode.tokens)

        return True
    
    def applied(self, code: str) -> bool:
        return code in self.__applied
    
    def on_applied(self, callback):
        self.__events.on("applied", callback)
        
    def find(self, code: str):
        self = PromocodesRepository()
        promocode = self.find(code)
        self._close()

        return promocode
