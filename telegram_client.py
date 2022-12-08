import telebot


class TelegramClient(telebot.TeleBot):
    def __init__(self, api_token: str, parse_mode=None):
        super().__init__(api_token)
    
    def run(self):
        pass

    def bind_command_router(self):
        pass


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(".env")
    import os
    TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
    client = TelegramClient(TELEGRAM_API_TOKEN)