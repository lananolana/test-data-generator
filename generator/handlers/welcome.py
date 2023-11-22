from config import bot
from utils.bot_handler import BotHandler
from utils.constants import common
from data.commands import COMMANDS


@bot.message_handler(commands=['start'])
def welcome(message):
    command = message.text
    command_handlers = {
        cmd.command: cmd.handler for cmd in COMMANDS
    }

    if command in command_handlers:
        handler_function = BotHandler.get_handler(command_handlers[command])
        BotHandler.send_welcome_message(message)
        handler_function(message)
    else:
        BotHandler.error(
            message, common.QUERY_ERROR, next_handler=welcome
        )
