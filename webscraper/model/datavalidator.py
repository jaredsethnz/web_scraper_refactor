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

