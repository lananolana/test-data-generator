import importlib
from telebot import types
from config import faker, bot, iban_objects
from data.commands import COMMANDS
from utils.constants import common


class BotHandler:

    @staticmethod
    def markup_setup(options, row_width):
        return types.ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(*options, row_width=row_width)

    @staticmethod
    def send_message(
        message, *args, markup=None,
        next_handler=None, trans_data=None
    ):
        reply = bot.send_message(
            message.chat.id, *args,
            reply_markup=markup, parse_mode='HTML')
        if next_handler:
            bot.register_next_step_handler(reply, next_handler, trans_data)

    @staticmethod
    def send_document(message, f, caption, reply_markup):
        return bot.send_document(
            message.chat.id, f, caption=caption, reply_markup=reply_markup
        )

    @staticmethod
    def error(message, error, markup=None, next_handler=None, trans_data=None):
        BotHandler.send_message(
            message, error, markup, next_handler, trans_data)

    @staticmethod
    def add_back_button(markup):
        markup.add("Back")

    @staticmethod
    def add_back_to_start_button(markup):
        markup.add("Back to start")

    @staticmethod
    def is_back(text):
        return text == 'Back'

    @staticmethod
    def is_back_to_start(text):
        return text in {'Back to start', '/start'}

    @staticmethod
    def are_back_buttons(
        message, back_handler, error, markup,
        next_handler, trans_data=None
    ):
        if BotHandler.is_back(message.text):
            back_handler()
        elif BotHandler.is_back_to_start(message.text):
            BotHandler.send_welcome_message(message)
        else:
            BotHandler.error(
                message, error, markup,
                next_handler, trans_data)

    @staticmethod
    def send_welcome_message(message):
        username = message.from_user.first_name
        requests = [command.button for command in COMMANDS]
        markup = BotHandler.markup_setup(requests, 2)
        reply = {username} + common.HELLO_MESSAGE
        BotHandler.send_message(message, reply, markup=markup)

    @staticmethod
    def get_handler(handler_name):
        handler_module = importlib.import_module(
            f'generator.handlers.{handler_name}'
        )
        return getattr(handler_module, handler_name)

    @staticmethod
    def convert_to_bytes(unit, size):
        UNIT_CONVERSION = {'MB': 1024 * 1024, 'KB': 1024}
        return size * UNIT_CONVERSION.get(unit, 1)

    @staticmethod
    def generate_account_number(country):
        bban = faker.bban()[-iban_objects.acc_num_len[country]:]
        total = 0

        for i in range(iban_objects.acc_num_len[country]):
            digit = int(bban[i])
            if i % 2 == 1:
                digit *= 2
            total += digit

        bban_check_digit = total % 11
        return bban + str(bban_check_digit)
