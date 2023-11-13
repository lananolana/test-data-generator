import random
from schwifty import IBAN
from config import faker, bot
from data.keyboard_objects import iban_countries
from data.iban_data import country_codes, bank_codes, acc_num_len
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
    country = country_codes.get(message.text)
    if country == 'gb':
        iban = faker.iban()
        iban_sender(iban, message)
    elif country:
        iban_generator(message, country)
    elif message.text in {'Back to start', '/start'}:
        welcome(message)
    else:
        reply = bot.send_message(message.chat.id, messages["query_error"])
        bot.register_next_step_handler(reply, country_check)


def iban_generator(message, country):
    bank_code = random.choice(bank_codes[country])
    bban = faker.bban()[-acc_num_len[country]:]
    total = 0

    for i in range(acc_num_len[country]):
        digit = int(bban[i])
        if i % 2 == 1:
            digit *= 2
        total += digit

    bban_check_digit = total % 11
    account_number = bban + str(bban_check_digit)

    iban = IBAN.generate(country.upper(), bank_code, account_number)
    iban_sender(iban, message)


def iban_sender(iban, message):
    bot.send_message(message.chat.id,
                     f"{message.text} IBAN:"
                     f"\n\n<code>{iban}</code>")

    reply = bot.send_message(message.chat.id, messages["generator_again"])
    bot.register_next_step_handler(reply, country_check)
