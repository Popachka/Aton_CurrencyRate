class Cache:
    def __init__(self) -> None:
        self.currency_cache = {}
        self.country_cache = {}
    def get_currency(self, code):
        return self.currency_cache.get(code)
    def set_currency(self,code,currency_data):
        self.currency_cache[code] = currency_data
    def get_country(self, country):
        return self.country_cache.get(country)
    def set_country(self, country, code):
        self.country_cache[country] = code