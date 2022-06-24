class HouseProperty:
    def __init__(self, name, url, address, price, unit_price, ping, patterns, floors):
        self.name = name
        self.url = url
        self.address = address
        self.price = price
        self.unit_price = unit_price
        self.ping = ping
        self.patterns = patterns
        self.floors = floors

    # compare object instances for equality by url and price of property
    def __eq__(self, other):
        if not isinstance(other, HouseProperty):
            return NotImplemented

        return self.url == other.url and self.price == other.price
