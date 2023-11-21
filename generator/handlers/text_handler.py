from config import bot
from utils.bot_handler import BotHandler
from utils.constants import text


@bot.message_handler(commands=['text'])
def text_handler(message):
    text_markup = BotHandler.markup_setup(None, 1)
    BotHandler.add_back_to_start_button(text_markup)
    BotHandler.send_message(
        message, text.TEXT_GENERATOR,
        markup=text_markup, next_handler=text_generator, trans_data=text_markup
    )


def text_generator(message, text_markup):
    symbols = int(message.text)
    if 0 < symbols < 4001:
        data = text.LOREM_IPSUM[:symbols]
        text_sender(symbols, data, message, text_markup)
    elif symbols < 1 or symbols > 4000:
        BotHandler.error(
            message, text.TEXT_GENERATOR_SIZE_ERROR,
            text_markup, text_generator
        )
    else:
        BotHandler.are_back_buttons(
            message, None, text.TEXT_GENERATOR_INT_ERROR,
            text_markup, text_generator
        )


def text_sender(symbols, data, message, text_markup):

    BotHandler.send_message(
        message, text.TEXT_GENERATED, symbols, f"\n\n<code>{data}</code>"
    )
    BotHandler.send_message(
        message, text.TEXT_GENERATOR_AGAIN,
        markup=text_markup, next_handler=text_generator
    )
