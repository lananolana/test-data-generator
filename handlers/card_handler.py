from config import faker, bot, cards
from telebot import types
from generator import welcome, messages


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
    match message.text:
        case 'Back to start' | '/start':
            welcome(message)
        case 'VISA':
            card_type = 'visa'
        case 'MasterCard':
            card_type = 'mastercard'
        case 'Maestro':
            card_type = 'maestro'
        case 'JCB':
            card_type = 'jcb'
        case 'AmEx':
            card_type = 'amex'
        case 'Discover':
            card_type = 'discover'
        case _:
            reply = bot.send_message(message.chat.id, messages["query_error"])
            bot.register_next_step_handler(reply, payment_system)

    card_data = faker.credit_card_full(card_type)

    bot.send_message(message.chat.id,
                     f"{message.text} card details:"
                     f"\n\n<code>{card_data}</code>")
    reply = bot.send_message(message.chat.id, messages["generator_again"])
    bot.register_next_step_handler(reply, payment_system)
