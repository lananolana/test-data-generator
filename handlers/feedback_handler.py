from config import bot
from telebot import types
from generator import messages, check_request


def feedback_handler(message: types.Message):
    feedback_button = types.InlineKeyboardMarkup()
    url = 'https://www.buymeacoffee.com/lananolana'
    coffee = types.InlineKeyboardButton(text='Buy creator a coffee ☕️',
                                        url=url)
    feedback_button.add(coffee)

    bot.send_message(message.chat.id, messages["idea_message"])
    reply = bot.send_message(message.chat.id,
                             messages["support_message"],
                             reply_markup=feedback_button)
    bot.register_next_step_handler(reply, check_request)
