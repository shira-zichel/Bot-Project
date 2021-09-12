from dataclasses import dataclass
from tinydb import TinyDB, where

DB_PATH = 'mvc-history-db.json'
db = TinyDB(DB_PATH)
history_numbers_table = db.table('history')


@dataclass
class history:
    """
    represent commands history
    :attribute number: the number that entered by the user in the request
    :attribute amount: the number of times this number has appeared in the bot history
    """
    currency: str
    amount: int


class HistoryModelWrapper:
    """
    warpped class to handle request history and store it in the db
    """
    @classmethod
    def get_by_currency(cls, currency: str) -> history:
        """
        return the record that fits num
        :return: record from the db by num
        """
        return history_numbers_table.search(where('currency') == currency)
    
    
    @classmethod
    def create(cls, currency: int) -> None:
        """  
        insert the db new record or update the amount if the number already exists
        """
        if cls.get_by_currency(currency):
            amount = cls.get_by_currency(currency)[0]['amount'] + 1
            history_numbers_table.update({'amount': amount},where('currency') == currency)
        else:    
            history_numbers_table.insert({'currency': currency, 'amount': 1})

    @classmethod
    def get_all_history(cls) -> list:
        """
        return all the records
        :return: list of all records from the db
        """
        return history_numbers_table.all()

    @classmethod
    def get_most_converted_to_currency(cls):
        return max(history_numbers_table, key=history_numbers_table.get)

