import telebot
from telebot import types
from telebot.util import quick_markup

TELEGRAM_API_TOKEN="5673742860:AAG0H3DHkNztp-9rTIa1eAb1rAO2ZTNJiCM"
DURATION_DEFAULT = {"1m": "1 миинута",
                    "3m": "3 минуты", 
                    "5m": "5 минут",
                    "10m": "10 минут",
                    "15m": "15 минут",
                    "20m": "20 минут",
                    "30m": "30 минут",
                    "1h": "1 час",
                    "2h": "2 часа",
                    "4h": "4 часа",
                    "10h": "10 часов"}


bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
task_database = {}
active_session = {}


class TaskData:
    name: str
    date: str
    start_time: str
    duration: str

    def __init__(self, message: types.Message):
        self.__start_task_record(message)

    def set_name(self, message: types.Message):
        self.name = message.text
        bot.register_next_step_handler(message, self.set_date)
        bot.send_message(message.chat.id, "Отправьте дату начала события в формате dd.mm.yyyy")

    def set_date(self, message: types.Message):
        if len(message.text.split(".")) != 3:
            bot.register_next_step_handler(message, self.set_date)
            bot.send_message(message.chat.id, "Вы ввели дату не в том формате, попробуйте ещё раз")
            return
        self.date = message.text
        bot.register_next_step_handler(message, self.set_start_time)
        bot.send_message(message.chat.id, "Отправьте, пожалуйста, время начала события, в формате hh:mm")

    def set_start_time(self, message: types.Message):
        if not message.text.split(":") != 2:
            bot.register_next_step_handler(message, self.set_start_time)
            bot.send_message(message.chat.id, "Вы ввели время не в том формате, попробуйте ещё раз")
        self.start_time = message.text
        bot.send_message(message.chat.id, "Выберите, пожалуйста, время продолжительности события",
                                       reply_markup=quick_markup(values={value: {"callback_data": key} for key, value in list(DURATION_DEFAULT.items())}, row_width=2))
        

    def set_duration(self, message: types.Message, duration="69sec"):
        self.duration = duration
        bot.send_message(message.chat.id, "Проверьте, всё ли правильно?:\n" + str(self),
                         reply_markup=quick_markup(values= {'✔': {'callback_data': 'ok'}, '✖': {'callback_data': 'not_ok'}}, row_width=2))

    def __start_task_record(self, message: types.Message):
        bot.register_next_step_handler(message, self.set_name)
        bot.send_message(message.chat.id, "Отправьте, пожалуйста название мероприятия")
        
    def save(self, chat_id: int):
        if self.date not in list(task_database[chat_id].keys()):
            task_database[chat_id][self.date] = []
        task_database[chat_id][self.date].append(active_session[chat_id])
        del active_session[chat_id]        
        bot.send_message(chat_id, f"Задача {self.name} была успешно добавлена", reply_markup=form_start_reply_markup())


    def __repr__(self):
        return f"""Название задачи {self.name}\n
                   Начало выполнения {self.date} {self.start_time}\n
                   Общее время выполнения {self.duration}"""

    def __str__(self):
        return self.__repr__()
                   

def form_start_reply_markup():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    first_button = types.KeyboardButton("Добавить задачу")
    second_button = types.KeyboardButton("Посмотреть рассписание")
    markup.add(first_button, second_button)
    return markup

def send_all_task_data(message: types.Message):
    def send_tasks_info(chat_id: int, task_date: str):

        if task_date not in list(task_database[chat_id].keys()):
            bot.send_message(chat_id, "Пока у вас нет ни одной задачи на эту дату")
            return
        for task in task_database[chat_id][task_date]:
            bot.send_message(chat_id, str(task))

    def get_task_date(message: types.Message):
        if len(message.text.split(".")) != 3:
            bot.register_next_step_handler(message, get_task_date)
            bot.send_message(message.chat.id, "Вы ввели дату не в том формате, попробуйте ещё раз")
            return
        send_tasks_info(message.chat.id, message.text)
    
    bot.send_message(message.chat.id, "Отправьте дату начала события в формате dd.mm.yyyy")
    bot.register_next_step_handler(message, get_task_date)



@bot.message_handler(commands=['start', 'help'])
def navigation_help(message):
    bot.send_message(message.chat.id, "Приветствую в боте!\n Выберете одну из двух предложенных функция", reply_markup=form_start_reply_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "ok":
        active_session[call.message.chat.id].save(call.message.chat.id)
    elif call.data == "not_ok":
        bot.send_message(call.message.chat.id, f"Задача {active_session[call.message.chat.id].name} не была добавлена", reply_markup=form_start_reply_markup())
        del active_session[call.message.chat.id]
    elif call.data in list(DURATION_DEFAULT.keys()):
        active_session[call.message.chat.id].set_duration(call.message, DURATION_DEFAULT[call.data])
    

@bot.message_handler(func=lambda m: True)
def message_update(message):
    if message.text == "Добавить задачу":
        if not (message.chat.id in list(task_database.keys())):
            task_database[message.chat.id] = dict()
        if not (message.chat.id in list(active_session.keys())):
            active_session[message.chat.id] = (TaskData(message))
        else:
            bot.send_message(message.chat.id, "Простите, но кажется, что вы уже добавляете задачу",)

    if message.text == "Посмотреть рассписание":
        if not (message.chat.id in list(task_database.keys())):
            bot.send_message(message.chat.id, "Простите, но вы не добавили ещё ни одного события")
        else:
            send_all_task_data(message)

def main():
    bot.infinity_polling()

if __name__ == "__main__":
    main()