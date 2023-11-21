import random
from schwifty import IBAN
from config import faker, bot, iban_objects
from utils.bot_handler import BotHandler
from utils.constants import common, accounts


@bot.message_handler(commands=['iban'])
def iban_handler(message):

    iban_markup = BotHandler.markup_setup(iban_objects.iban_countries, 3)
    BotHandler.add_back_to_start_button(iban_markup)

    BotHandler.send_message(
        message, accounts.IBAN_GENERATOR,
        markup=iban_markup, next_handler=country_check
    )


def country_check(message):
    country = iban_objects.country_codes.get(message.text)
    if country == 'gb':
        iban = faker.iban()
        iban_sender(iban, message)
    elif country:
        iban_generator(message, country)
    else:
        BotHandler.are_back_buttons(
            message, None, common.QUERY_ERROR, None, country_check
        )


def iban_generator(message, country):
    bank_code = random.choice(iban_objects.bank_codes[country])
    account_number = BotHandler.generate_account_number(country)
    iban = IBAN.generate(country.upper(), bank_code, account_number)
    iban_sender(iban, message)


def iban_sender(iban, message):
    BotHandler.send_message(
        message, f"{message.text} IBAN:", f"\n\n<code>{iban}</code>"
    )
    BotHandler.send_message(
        message, common.GENERATOR_AGAIN, next_handler=country_check
    )
