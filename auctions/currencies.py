import threading
import time
from pip._vendor import requests


url = 'http://www.apilayer.net/api/live?access_key=8b972a65ee9a3bd9aa92b29887149f17&format=1'
currency_list = []
currency_dict = {}
lock = False


class UpdateCurrenciesThread(threading.Thread):

    def run(self):

        global currency_list
        global currency_dict
        global lock

        while True:

            response = requests.get(url)
            data = response.json()
            lock = True
            currency_dict = data['quotes']
            # print(currency_dict)
            lock = False
            for q in currency_dict:
                if q not in currency_list:
                    currency_list.append(q[3:])

            time.sleep(3600)


# Also works for USD since there is a key 'USDUSD'
def get_dollar_value(currency_code):

    if not lock:
        for code in currency_dict:
            if currency_code in code[3:]:
                return currency_dict[code]
    else:
        # currency_dict is updating
        pass

    return None


def convert(input_currency, input_amount, target_currency):

    input_dollar_rate = float(get_dollar_value(input_currency))
    value_in_dollars = input_amount / input_dollar_rate

    target_dollar_rate = float(get_dollar_value(target_currency))
    value_in_target_currency = value_in_dollars * target_dollar_rate

    # print(input_dollar_rate)
    # print(value_in_dollars)
    # print(target_currency)
    # print(target_dollar_rate)
    # print(value_in_target_currency)

    return value_in_target_currency


def get_currencies():
    return currency_list


def get_currency_dict():
    return currency_dict
