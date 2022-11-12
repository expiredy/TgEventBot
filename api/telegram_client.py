from os import getenv
from dotenv import load_dotenv
load_dotenv(".env")

import requests
import asyncio
from datetime import datetime

import logging

API_URL = getenv('API_URL')
TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
DEFAULT_CONFIGURATION_FILE_PATH = getenv('DEFAULT_CONFIGURATION_FILE_PATH')


class TelegramClient:
    def __init__(self):
        pass

    def run():
        pass

def get_api_response(request_method: Callable = requests.get, method_name: str = "getMe", parameters_dict: dict = {}) -> dict:
    try:
        return request_method(str(API_URL + TELEGRAM_BOT_TOKEN + "/" + method_name), params=parameters_dict).json()
    except requests.exceptions.ConnectionError:
        logging.exception("message")
        return {}

def test():
    test_client = TelegramClient()

if __name__ == "__main__":
    test()