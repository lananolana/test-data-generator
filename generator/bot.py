from config import bot
from telebot.types import BotCommand
from data.commands import COMMANDS


class Generator:
    def __init__(self):
        self.load_messages()

    def load_messages(self):
        self.bot_commands = [
            BotCommand(command.command, command.description)
            for command in COMMANDS
        ]

    def run(self):
        bot.set_my_commands(self.bot_commands)
        bot.infinity_polling()
