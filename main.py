import telebot
from telebot import types, custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()

# Вставить свой токен или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6719420354:AAFmJQehRB8pQqa6FP7vn3dWUqBtYrymZqs", state_storage=state_storage, parse_mode='Markdown')

class PollState(StatesGroup):
    name = State()
    age = State()

class HelpState(StatesGroup):
    wait_text = State()

text_poll = "команда"  # Можно менять текст
text_button_1 = "1 разряд"  # Можно менять текст
text_button_2 = "2 разряд"  # Можно менять текст
text_button_3 = "3 разряд"  # Можно менять текст

menu_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(types.KeyboardButton(text_poll))
menu_keyboard.add(types.KeyboardButton(text_button_1))

menu_keyboard.add(types.KeyboardButton(text_button_2), types.KeyboardButton(text_button_3))

@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(message.chat.id, 'Ку! Что будем делать?', reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! *Ваше* _имя_?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)

@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! [Ваш](https://www.example.com/) `возраст?`')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)

@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'тхэнкс за регистрацию!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command_1(message):
    bot.send_message(message.chat.id, "Текст 1", reply_markup=menu_keyboard)  # Можно менять текст

@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command_2(message):
    bot.send_message(message.chat.id, "Текст 2", reply_markup=menu_keyboard)  # Можно менять текст

@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command_3(message):
    bot.send_message(message.chat.id, "Текст 3", reply_markup=menu_keyboard)  # Можно менять текст

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()

