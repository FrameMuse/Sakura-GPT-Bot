from pyee.twisted import TwistedEventEmitter


MAX_TOKENS_AMOUNT = 50_000
DEFAULT_TOKENS_AMOUNT = 500
DEFAULT_TOKENS_CONVERSION_RATE = 0.75


class Tokens:
    """
        asd
    """

    def __init__(self, amount: "float | str" = DEFAULT_TOKENS_AMOUNT, conversion_rate: float = DEFAULT_TOKENS_CONVERSION_RATE):
        self.amount = float(amount)
        self.__conversion_rate = conversion_rate

        self.__events = TwistedEventEmitter()

    def __str__(self) -> str:
        return str(self.amount)

    def debit(self, amount: float) -> float:
        """
        Removes `amount` of tokens.
        """

        self.amount -= amount
        self.__events.emit("amount_update")

        return self.amount

    def debit_chars(self, chars: float) -> float:
        tokens = self.to_tokens(chars)
        self.debit(tokens)

        return self.amount

    def credit(self, amount: float) -> float:
        """
        Adds `amount` of tokens.
        """

        self.amount += amount
        self.__events.emit("amount_update")

        return self.amount

    def on_amount_update(self, callback):
        self.__events.on("amount_update", callback)

    def sufficient(self, tokens: float = 0):
        return self.amount >= tokens

    def sufficient_chars(self, chars: float = 0):
        tokens = self.to_tokens(chars)
        return self.amount >= tokens

    def limit_exceeded(self, extra: float = 0):
        return self.amount + extra > MAX_TOKENS_AMOUNT

    def to_tokens(self, chars: float) -> float:
        return chars / self.__conversion_rate

    def to_chars(self, tokens: float) -> float:
        return tokens * self.__conversion_rate
