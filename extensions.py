import requests
import json

from config import keys


class API_Exception(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise API_Exception('Неверный формат ввода (Введены одинаковые значения валют)')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise API_Exception(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise API_Exception(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise API_Exception(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base