from telebot import types
from config import faker, bot, cards_objects
from utils.common_handlers import Handlers
from utils.constants import common, accounts


@bot.message_handler(commands=['card'])
def card_handler(message):
    card_markup = Handlers.markup_setup(*cards_objects.cards, 3)
    Handlers.send_message(
        message, accounts.CARDS_GENERATOR, card_markup, payment_system
    )


def payment_system(message: types.Message):
    card = cards_objects.card_types.get(message.text)

    if card:
        card_data = faker.credit_card_full(card)
    elif Handlers.is_back_to_start(message.text):
        Handlers.welcome(message)
    else:
        Handlers.error(message, payment_system)

    reply = f"{message.text} card details:\n\n<code>{card_data}</code>"
    Handlers.send_message(message, reply)
    Handlers.send_message(
        message, common.GENERATOR_AGAIN, next_handler=payment_system
    )
