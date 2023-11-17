import json
from telebot import types
from config import bot, requests
from utils.common_handlers import handlers
from utils.constants import common
from .handlers import (
    users_handler,
    card_handler,
    iban_handler,
    file_handler,
    text_handler,
    feedback_handler
)


class Generator:
    def __init__(self):
        self.command_handlers = {
            '/start': self.welcome,
            '/users': users_handler.users_handler,
            '/file': file_handler.file_handler,
            '/card': card_handler.card_handler,
            '/iban': iban_handler.iban_handler,
            '/text': text_handler.text_handler,
            '/feedback': feedback_handler.feedback_handler,
        }
        self.load_messages()

    def load_messages(self):
        with open("commands.json", "r") as file:
            commands_data = json.load(file)

        self.bot_commands = [
            types.BotCommand(command["command"],
                             command["description"],
                             command.get("icon", None))
            for command in commands_data
            ]

    def run(self):
        bot.set_my_commands(self.bot_commands)
        bot.infinity_polling()

    @bot.message_handler(commands=['start'])
    def welcome(self, message):
        self.send_welcome_message(message)

    def send_welcome_message(self, message):
        username = message.from_user.first_name
        markup = handlers.markup_setup(requests, 2)

        reply = {username} + common.HELLO_MESSAGE
        handlers.send_message(message, reply, markup, self.check_request)

    @bot.message_handler(func=lambda message: True)
    def check_request(self, message):
        command = message.text.lower()
        handler = self.command_handlers.get(
            command, handlers.error(
                message, common.QUERY_ERROR, self.markup, self.check_request
            )
        )
        handler(message)
