from config import faker, bot, cards_objects
from utils.bot_handler import BotHandler
from utils.constants import common, accounts


@bot.message_handler(commands=['card'])
def card_handler(message):
    card_markup = BotHandler.markup_setup(cards_objects.cards, 3)
    BotHandler.send_message(
        message, accounts.CARDS_GENERATOR, card_markup, payment_system
    )


def payment_system(message):
    card = cards_objects.card_types.get(message.text)

    if card:
        card_data = faker.credit_card_full(card)
        reply = f"{message.text} card details:\n\n<code>{card_data}</code>"
        BotHandler.send_message(
            message, reply, common.GENERATOR_AGAIN, next_handler=payment_system
        )
    elif BotHandler.is_back_to_start(message.text):
        BotHandler.send_welcome_message(message)
    else:
        BotHandler.error(message, payment_system)
