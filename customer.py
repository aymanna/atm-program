class Customer:

    def __init__(self, id: str, name: str, pin: str, balance: int, type: int):
        self.id = id
        self.name = name
        self.pin = pin
        self.balance = balance
        self.type = type
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["id"],data["name"],data["pin"],data["balance"],data["type"])

    @classmethod
    def from_tuple(cls, data: tuple):
        id, name, pin, balance, type = data
        return cls(id, name, pin, balance, type)

    def __repr__(self) -> str:
        ans = "Customer('%s','%s','%s',%d,%d)" % (
            self.id, self.name, self.pin,self.balance,self.type)
        return ans
    
    def __str__(self) -> str:
        ans = "%s, Type %d, ID: %s\nBalance: %d, PIN: %s" % (
            self.name, self.type, self.id,self.balance, self.pin)
        return ans
