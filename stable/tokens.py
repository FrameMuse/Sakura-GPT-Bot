from pyee.cls import evented
from pyee.twisted import TwistedEventEmitter


DEFAULT_TOKENS_AMOUNT = 500
DEFAULT_TOKENS_CONVERSION_RATE = 0.75

@evented
class Tokens:
    """
        asd
    """

    def __init__(self, amount: "float | str" = DEFAULT_TOKENS_AMOUNT, conversion_rate: float = DEFAULT_TOKENS_CONVERSION_RATE):
        self.amount = float(amount)
        self.conversion_rate = conversion_rate

        self.event_emitter = TwistedEventEmitter()

    def debit(self, amount: float) -> float:
        """
        Removes `amount` of tokens.
        """

        self.amount -= amount
        self.event_emitter.emit("amount_update")

        return self.amount
    def debit_chars(self, chars: float) -> float:
        tokens = self.to_tokens(chars)
        self.debit(tokens)

        return self.amount

    def credit(self, amount: int) -> float:
        """
        Adds `amount` of tokens.
        """

        self.amount += amount
        self.event_emitter.emit("amount_update")

        return self.amount

    def to_tokens(self, chars: float) -> float:
        return chars / self.conversion_rate

    def to_chars(self, tokens: float) -> float:
        return tokens * self.conversion_rate

    def __str__(self) -> str:
        return str(self.amount)

    def on_amount_update(self, callback):
        self.event_emitter.on("amount_update", callback)