from config import bot
from utils.bot_handler import BotHandler
from utils.constants import common
from data.commands import COMMANDS


@bot.message_handler(commands=['start'])
def welcome(message):
    command = message.text
    command_handlers = {
            command.command: BotHandler.get_handler(command.handler)
            for command in COMMANDS
        }
    
    if command in command_handlers:
        BotHandler.send_welcome_message(message)
        command_handlers[command](message)
    else:
        BotHandler.error(
            message, common.QUERY_ERROR, next_handler=welcome
        )
