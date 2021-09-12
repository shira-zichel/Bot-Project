from datetime import date
import model
#import Currency_convertor
import requests


class app_controller:
    """
    A class that provides data to the view.
    """
    # A flag that marker if the user need to choose a video from the suggestions.
    COUNTER = 0
    # A list of the links of the suggestions.
    con = []


class HistoryController:
    """
    warpped class to handle the bot history
    """

    @classmethod
    def create(cls, num: int) -> None:
        """ 
        connect to function from model     
        """
        model.HistoryModelWrapper.create(num)

    @classmethod
    def get_all_history(cls) -> list:
        """ 
        connect to function from model
        :return: list of the user request history
        """
        return model.HistoryModelWrapper.get_all_history()


class Currency_convertor:
    # empty dict to store the conversion rates
    rates = {}

    def __init__(self, url):
        data = requests.get(url).json()

        # Extracting only the rates from the json data
        self.rates = data["rates"]

    # function to do a simple cross multiplication between
    # the amount and the conversion rates
    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != 'EUR':
            amount = amount / self.rates[from_currency]
        # limiting the precision to 2 decimal places
        amount = round(amount * self.rates[to_currency], 2)
        return str(date.today()) + '\n'+'{} {} = {} {}'.format(initial_amount, from_currency, amount, to_currency)


def converter(from_, to_, amount_):
    # YOUR_ACCESS_KEY = 'GET YOUR ACCESS KEY FROM fixer.io'
    url = str.__add__('http://data.fixer.io/api/latest?access_key=', "84a47226de202b6d2c731cedb76423d0")
    c = Currency_convertor(url)
    HistoryController.create(to_)
    return c.convert(from_, to_, int(amount_))


def convert_temp(from_, to_, amount_):
    """
    Converts temperature
    :param from_: str
    :param to_: str
    :param amount_: int
    :return:
    """
    if from_ == "C":
        if to_ == "F":
            amount = float(amount_)*(9/5)+ 32
        elif to_ == "K":
            amount = float(amount_)+273.15
        else:
            return "Use C (Celsius), F (Fahrenheit) or K (kelvin) "
    elif from_ == "F":
        if to_ == "C":
            amount= (float(amount_)-32)*(5/9)
        elif to_ == "K":
            amount= (float(amount_)+459.67)*(5/9)
        else:
            return "Use C (Celsius), F (Fahrenheit) or K (kelvin) "
    elif from_ == "K":
        if to_ == "C":
            amount = float(amount_)-273.15
        elif to_ == "F":
            amount = float(amount_)*(9/5) - 459.67
        else:
            return "Use C (Celsius), F (Fahrenheit) or K (kelvin) "
    else:
        return "Use C (Celsius), F (Fahrenheit) or K (kelvin) "
    return '{} {} = {} {}'.format(amount_, from_, amount, to_)


def convert_weight(from_, to_, amount_):
    """
    Converts weights
    :param from_: str
    :param to_: str
    :param amount_: int
    :return:
    """
    if from_ == 'kg':  # convert to pounds
        if to_ == "lbs":
            return '{} {} = {} {}'.format(amount_, from_, float(amount_)*2.2046, to_)
        return "Use kg (for kilogram) or lbs (for pound)"
    elif from_ == "lbs":  # convert to kilos
        if to_ == 'kg':
            return '{} {} = {} {}'.format(amount_, from_, float(amount_)*0.453592, to_)
        return "Use kg (for kilogram) or lbs (for pound)"
    return "Use kg (for kilogram) or lbs (for pound)"


def popular():
    """
    find the currency that appeared the most in the bot history
    :return: the most popular number in the bot history
    """
    list = []
    for i in HistoryController.get_all_history():
        list.append(i['amount'])
    amount = max(list)
    return "The currency which the conversion has made the most often is "+[i['currency'] for i in HistoryController.get_all_history() if i['amount'] == amount][0]


def start():
    return "Hello! " \
           "\nWelcome to our bot. A bot that allows quick conversion between currencies, weights and temperature. " \
           "\n\nWe work on the bot and constantly improve its functionality so that we can provide you with the most relevant and requested information." \
           "\n\nTo view all possible actions press /menu" \
           "\n\nWe wish you a useful and enjoyable use!"


def menu():
    return "MENU: " \
           "\nYou can control me by sending these commands:" \
           "\n/coins - for currency exchange" \
           "\n/popular_coin - For the currency to which the conversion has made the most often" \
           "\n/weight - for weight conversion " \
           "\n/temp - for temperature conversion " \
           "\n/options - options for performing the conversion depending on the type of conversion requested " \
           "\nWe are working at all times to add new options!"


def gen_function(func_name, from_, to_, amount_):
    if func_name == "/coins":
        return converter(from_, to_, amount_)
    elif func_name == "/weight":
        return convert_weight(from_, to_, amount_)
    elif func_name == "/temp":
        return convert_temp(from_, to_, amount_)
    else:
        return "ERROR"