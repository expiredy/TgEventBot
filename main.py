from dotenv import load_config
load_config(".env")
import os

TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

def main():
    pass

if __name__ == "__main__":
    main()