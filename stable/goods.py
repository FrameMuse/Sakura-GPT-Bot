class Good:
    def __init__(self, quantity: int, name: str, price: int, currency: str):
        self.price = price
        self.quantity = quantity
        self.name = name
        self.currency = currency
    
    def __str__(self):
        return str(self.quantity) + " " + self.name + " - " + str(self.price) + " " + self.currency

class Goods:
    class Tokens:
        option1 = Good(75, "Токенов", 69, "RUB")
        option2 = Good(750, "Токенов", 299, "RUB")
        option3 = Good(1500, "Токенов", 499, "RUB")
