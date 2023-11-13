import json
from config import bot
from telebot import types
from generator import welcome, messages


@bot.message_handler(commands=['text'])
def text_handler(message):
    text_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text_markup.add('Back to start')
    reply = bot.send_message(message.chat.id,
                             messages["text_generator"],
                             reply_markup=text_markup)

    bot.register_next_step_handler(reply, text_generator)


def text_generator(message: types.Message):
    text_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text_markup.add('Back to start')

    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)

    elif (isinstance(message.text, type(None)) or not message.text.isdigit()):
        bot.send_message(message.chat.id,
                         messages["text_generator_int_error"],
                         reply_markup=text_markup)
        bot.register_next_step_handler(message, text_generator)

    elif (int(message.text) < 1 or int(message.text) > 4000):
        bot.send_message(message.chat.id,
                         messages["text_generator_size_error"],
                         reply_markup=text_markup)
        bot.register_next_step_handler(message, text_generator)

    else:
        symbols = int(message.text)

        with open("/data/lorem_ipsum.json", "r", encoding="utf-8") as file:
            json_data = json.load(file)
            data = json_data["lorem_ipsum"]
            reply = data[:symbols]

        bot.send_message(message.chat.id,
                         f"This is generated text with {symbols} characters."
                         f"\n\n<code>{reply}</code>")

        bot.send_message(message.chat.id,
                         messages["text_generator_again"],
                         reply_markup=text_markup)

        bot.register_next_step_handler(message, text_generator)
