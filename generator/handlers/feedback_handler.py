from telebot import types
from config import bot
from utils.common_handlers import handlers
from utils.constants import common
from bot import check_request


@bot.message_handler(commands=['feedback'])
def feedback_handler(message: types.Message):
    coffee = types.InlineKeyboardButton(
        text='Buy creator a coffee ☕️',
        url='https://www.buymeacoffee.com/lananolana'
    )
    feedback_button = types.InlineKeyboardMarkup()
    feedback_button.add(coffee)

    handlers.send_message(message, common.IDEA_MESSAGE)
    handlers.send_message(
        message, common.SUPPORT_MESSAGE, feedback_button, check_request
    )
