from config import faker, bot
from telebot import types
from generator import welcome, messages
from data.keyboard_objects import cards, card_types


@bot.message_handler(commands=['card'])
def card_handler(message):
    card_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    card_markup.add(*cards, row_width=3)
    card_markup.add('Back to start')

    reply = bot.send_message(message.chat.id,
                             messages["cards_generator"],
                             reply_markup=card_markup)
    bot.register_next_step_handler(reply, payment_system)


def payment_system(message: types.Message):
    card = card_types.get(message.text)
    if card:
        card_data = faker.credit_card_full(card)
    elif message.text in {'Back to start', '/start'}:
        welcome(message)
    else:
        reply = bot.send_message(message.chat.id, messages["query_error"])
        bot.register_next_step_handler(reply, payment_system)

    bot.send_message(message.chat.id,
                     f"{message.text} card details:"
                     f"\n\n<code>{card_data}</code>")
    reply = bot.send_message(message.chat.id, messages["generator_again"])
    bot.register_next_step_handler(reply, payment_system)
