import telebot
from telebot import types


TELEGRAM_API_TOKEN="5673742860:AAG0H3DHkNztp-9rTIa1eAb1rAO2ZTNJiCM"


class TaskData:
    name: str
    date: str
    start_time: str
    duration: str

    def __init__(self):
        pass

    def __repr__(self):
        return f"""Название задачт {self.name}\n
                   Начало выполнения {self.date} {self.start_time}\n
                   Общее время выполнения {self.duration}"""

def form_start_replay_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    first_button = types.KeyboardButton("Добавить задачу")
    second_button = types.KeyboardButton('Посмотреть рассписание')
    markup.add(first_button, second_button)
    return markup

task_database = {}
active_session = []
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

def send_task_info(chat_id, task_id=-1):
    bot.send_message(chat_id, task_database[chat_id][task_id], )


@bot.message_handler(commands=['start', 'help'])
def navigation_help(message):
    bot.send_message(message.chat.id, "Приветствую в боте!\n Выберете одну из двух предложенных функция", reply_markup=form_start_replay_markup())


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
    print(call)
    if call.data == 1:
        pass
    elif call.data == 2:
        pass

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == "Добавить задачу":
        active_session.append(message.chat.id)

    elif message.text == "Посмотреть рассписение":
        if 
# bot.register_next_step_handler

def main():
    print("run")
    bot.infinity_polling()

if __name__ == "__main__":
    main()