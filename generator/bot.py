import json
from config import bot
from telebot.types import BotCommand
from data.commands import COMMANDS
from utils.bot_handler import BotHandler
from utils.constants import common


class Generator:
    def __init__(self):
        self.command_handlers = {
            command.command: BotHandler.get_handler(command.handler)
            for command in COMMANDS
        }
        self.load_messages()

    def load_messages(self):
        with open("commands.json", "r") as file:
            commands_data = json.load(file)

        self.bot_commands = [
            BotCommand(command["command"],
                       command["description"])
            for command in commands_data
            ]

    def run(self):
        bot.set_my_commands(self.bot_commands)
        bot.infinity_polling()

    @bot.message_handler(commands=['start'])
    def welcome(self, message):
        command = message.text
        if command in self.command_handlers:
            BotHandler.send_welcome_message(message)
            self.command_handlers[command](message)
        else:
            BotHandler.error(
                message, common.QUERY_ERROR, next_handler=self.welcome
            )
