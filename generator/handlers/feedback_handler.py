from telebot import types
from config import bot
from utils.bot_handler import BotHandler
from utils.constants import common
from .welcome import welcome


@bot.message_handler(commands=['feedback'])
def feedback_handler(message: types.Message):
    coffee = types.InlineKeyboardButton(
        text='Buy creator a coffee ☕️',
        url='https://www.buymeacoffee.com/lananolana'
    )
    feedback_button = types.InlineKeyboardMarkup()
    feedback_button.add(coffee)

    BotHandler.send_message(message, common.IDEA_MESSAGE)
    BotHandler.send_message(
        message, common.SUPPORT_MESSAGE, feedback_button, welcome(message)
    )
