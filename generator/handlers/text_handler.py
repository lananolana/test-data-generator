from config import bot
from telebot import types
from utils.common_handlers import handlers
from utils.constants import text


@bot.message_handler(commands=['text'])
def text_handler(message):
    text_markup = handlers.markup_setup()
    handlers.add_back_to_start_button(text_markup)
    handlers.send_message(
        message, text.TEXT_GENERATOR,
        markup=text_markup, next_handler=text_generator, trans_data=text_markup
    )


def text_generator(message: types.Message, text_markup):
    symbols = int(message.text)
    if 0 < symbols < 4001:
        data = text.LOREM_IPSUM[:symbols]
        text_sender(symbols, data, message, text_markup)
    elif symbols < 1 or symbols > 4000:
        handlers.error(
            message, text.TEXT_GENERATOR_SIZE_ERROR,
            text_markup, text_generator
        )
    else:
        handlers.are_back_buttons(
            message, None, text.TEXT_GENERATOR_INT_ERROR,
            text_markup, text_generator
        )


def text_sender(symbols, data, message, text_markup):

    handlers.send_message(
        message, text.TEXT_GENERATED, symbols, f"\n\n<code>{data}</code>"
    )
    handlers.send_message(
        message, text.TEXT_GENERATOR_AGAIN,
        markup=text_markup, next_handler=text_generator
    )
