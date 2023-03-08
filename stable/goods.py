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
        option0 = Good(100, "Токенов", 19, "RUB")
        option1 = Good(300, "Токенов", 49, "RUB")
        option2 = Good(1500, "Токенов", 299, "RUB")
        option3 = Good(3750, "Токенов", 499, "RUB")
