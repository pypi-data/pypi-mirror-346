import datetime
import re

import requests


def inject_year(text):
    pattern = re.compile(r'\[yyyy\]|<year>')
    return pattern.sub(str(datetime.date.today().year), text)


def resolve(expression):
    """
    Resolve an SPDX license expression into a license text.

    >>> resolve('MIT')
    'MIT License...'
    """
    url = f"https://raw.githubusercontent.com/spdx/license-list-data/main/text/{expression}.txt"
    return inject_year(requests.get(url).text)
