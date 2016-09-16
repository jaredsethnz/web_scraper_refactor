import re
from urllib.parse import urlparse
from decimal import Decimal
from datetime import date


class DataValidator(object):

    PARAMETER_ONE = 0
    PARAMETER_TWO = 1
    PARAMETER_THREE = 2
    URL_SCHEME = 0
    URL_SCHEME_HTTP = 'http'
    URL_SCHEME_HTTPS = 'https'

    def __init__(self, console_view):
        self.view = console_view

    def check_data_type(self, str_value):
        currency_value = self.check_data_currency(str_value)
        if currency_value is not None:
            return currency_value
        int_value = self.check_data_int(str_value)
        if int_value is not None:
            return int_value
        date_value = self.check_data_date(str_value)
        if date_value is not None:
            return date_value
        return str_value

    def check_data_int(self, str_value):
        pattern = re.compile('^[0-9]+$')
        int_value = None
        if pattern.match(str_value):
            int_value = int(str_value)
        return int_value

    def check_data_currency(self, str_value):
        pattern = re.compile('\$[1-9]?[0-9]+\.[0-9][0-9]$')
        currency_value = None
        if pattern.match(str_value):
            str_value = str_value.strip('$')
            currency_value = Decimal(str_value)
        return currency_value

    def check_data_date(self, str_value):
        pattern = re.compile('[.,/#!$%\^&*;:{}=\-_`~()a-zA-Z]+')
        date_value = None
        str_values = str_value.split(' ')
        month_number = months.get(str_values[self.PARAMETER_ONE])
        if month_number is not None:
            month = month_number
            try:
                day = int(pattern.sub('', str_values[self.PARAMETER_TWO]))
                year = int(str_values[self.PARAMETER_THREE])
                date_value = date(year, month, day)
            except TypeError:
                self.view.display_item('Error parsing date.....')
        return date_value

    def check_url(self, url):
        valid_url = False
        match = urlparse(url)
        if match[self.URL_SCHEME] == self.URL_SCHEME_HTTP or \
                match[self.URL_SCHEME] == self.URL_SCHEME_HTTPS:
            valid_url = True
        return valid_url


months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
          'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
          'November': 11, 'December': 12}
