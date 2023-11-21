import json
from config import bot
from telebot.types import BotCommand


class Generator:
    def __init__(self):
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
