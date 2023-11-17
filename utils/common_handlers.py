from telebot import types
from config import faker, bot, acc_num_len
from generator.bot import Generator

generator = Generator()


class handlers:
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
        formatted_text = ''.join([generator.messages[arg] for arg in args])
        reply = bot.send_message(
            message.chat.id, formatted_text,
            reply_markup=markup, parse_mode='HTML')
        if next_handler:
            bot.register_next_step_handler(reply, next_handler, trans_data)

    @staticmethod
    def send_document(message, f, caption, reply_markup):
        return bot.send_document(
            message.chat.id, f, caption=caption, reply_markup=reply_markup
        )

    @staticmethod
    def error(message, error, markup, next_handler, trans_data=None):
        handlers.send_message(
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
        if handlers.is_back(message.text):
            back_handler()
        elif handlers.is_back_to_start(message.text):
            handlers.welcome(message)
        else:
            handlers.error(
                message, error, markup,
                next_handler, trans_data)

    @staticmethod
    def welcome(message):
        generator.welcome(message)

    @staticmethod
    def convert_to_bytes(unit, size):
        UNIT_CONVERSION = {'MB': 1024 * 1024, 'KB': 1024}
        return size * UNIT_CONVERSION.get(unit, 1)

    @staticmethod
    def generate_account_number(country):
        bban = faker.bban()[-acc_num_len[country]:]
        total = 0

        for i in range(acc_num_len[country]):
            digit = int(bban[i])
            if i % 2 == 1:
                digit *= 2
            total += digit

        bban_check_digit = total % 11
        return bban + str(bban_check_digit)
