DEFAULT_TOKENS_AMOUNT = 500
DEFAULT_TOKENS_CONVERSION_RATE = 0.75

class Tokens:
    """
        asd
    """

    def __init__(self, amount: float = DEFAULT_TOKENS_AMOUNT, rate: float = DEFAULT_TOKENS_CONVERSION_RATE):
        self.amount = amount
        self.rate = rate

    def debit(self) -> float:
        """
        Removes `amount` of tokens.
        """

    def credit(self) -> float

    def from_chars(self, chars: float) -> float:
        return chars * (1 - chars)

    def to_chars(self, tokens: float) -> float:
        return tokens * (1 - chars)