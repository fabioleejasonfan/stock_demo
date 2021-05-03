from random import (
    choice,
    randrange,
    sample,
)
from numpy import arange
from datetime import datetime, timedelta
import pytz

utc = pytz.UTC


def create_mock_profile():
    account_balance = 200000
    stock_balance = {
        "00001": {
            "hands": 10,
            "price": 62.700,
        },
        "00002": {
            "hands": 20,
            "price": 76.850,
        },
        "00003": {
            "hands": 0,
            "price": 12.420,
        },
        "00004": {
            "hands": 100,
            "price": 23.400,
        },
        "00005": {
            "name": 200,
            "price": 47.3,
        },
    }
    stock_detail = {
        "00001": {
            "name": "長和",
            "type": "Watch & Jewellery",
            "price": 62.700,
        },
        "00002": {
            "name": "中電控股",
            "type": "E-Commerce & Internet Services",
            "price": 76.850,
        },
        "00003": {
            "name": "香港中華煤氣",
            "type": "E-Commerce & Internet Services",
            "price": 12.420,
        },
        "00004": {
            "name": "九龍倉集團",
            "type": "Watch & Jewellery",
            "price": 23.400,
        },
        "00005": {
            "name": "匯豐控股",
            "type": "Banks",
            "price": 47.3,
        },
    }

    mock_profile = {
        "account_balance": account_balance,
        "stock_balance": stock_balance,
        "stock_detail": stock_detail,
    }
    return mock_profile
