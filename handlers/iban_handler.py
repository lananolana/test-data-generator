from config import faker, bot, iban_countries
from telebot import types
from generator import welcome, messages


@bot.message_handler(commands=['iban'])
def iban_handler(message):
    iban_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    iban_markup.add(*iban_countries, row_width=3)
    iban_markup.add('Back to start')

    reply = bot.send_message(message.chat.id,
                             messages["iban_generator"],
                             reply_markup=iban_markup)
    bot.register_next_step_handler(reply, country_check)


def country_check(message: types.Message):
    match message.text:
        case 'Back to start' | '/start':
            welcome(message)
        case 'GB 🇬🇧':
            country = 'gb'
        # case 'BE 🇧🇪':
        #     country = 'be'
        # case 'GE 🇩🇪':
        #     country = 'ge'
        # case 'FR 🇫🇷':
        #     country = 'fr'
        # case 'NL 🇳🇱':
        #     country = 'nl'
        # case 'PT 🇵🇹':
        #     country = 'pt'
        case _:
            reply = bot.send_message(message.chat.id, messages["query_error"])
            bot.register_next_step_handler(reply, country_check)

    bot.register_next_step_handler(reply, iban_generator, country)


def iban_generator(message, country):
    match country:
        case 'gb':
            iban = faker.iban()

    bot.send_message(message.chat.id,
                     f"{message.text} IBAN:"
                     f"\n\n<code>{iban}</code>")
    reply = bot.send_message(message.chat.id, messages["generator_again"])
    bot.register_next_step_handler(reply, country_check)
