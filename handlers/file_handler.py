import os
import time

from config import bot
from telebot import types
from generator import welcome, messages
from data.keyboard_objects import formats


@bot.message_handler(commands=['file'])
def file_handler(message):
    files_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    files_markup.add(*formats, row_width=5)
    files_markup.add('Back to start')

    reply = bot.send_message(message.chat.id,
                             messages["files_generator"],
                             reply_markup=files_markup)
    bot.register_next_step_handler(reply, check_format)


# Checking the selected extension
def check_format(message):
    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
    elif (message.text in formats):
        files_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        files_markup.add("B", "KB", "MB", "Back to start")

        # Selecting the unit of measurement
        reply = bot.send_message(message.chat.id,
                                 messages["files_ext"]
                                 + f"<b>{message.text}</b>\n\n"
                                 + messages["files_generator_unit"],
                                 reply_markup=files_markup)
        bot.register_next_step_handler(reply, check_unit, message)

    else:
        files_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        files_markup.add(*formats, row_width=5)
        files_markup.add("Back to start")

        reply = bot.send_message(message.chat.id,
                                 messages["files_generator_ext_error"],
                                 reply_markup=files_markup)
        bot.register_next_step_handler(reply, check_format)


# Checking the selected unit of measurement
def check_unit(message, format):
    if (message.text == 'Back'):
        check_format(format)

    elif (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)

    elif (message.text in ['B', 'KB', 'MB']):
        files_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        files_markup.add('Back', 'Back to start')

        reply = bot.send_message(message.chat.id,
                                 messages["files_ext"]
                                 + f"<b>{format.text}</b>"
                                 + messages["files_unit"]
                                 + f"<b>{message.text}</b>\n\n"
                                 + messages["files_generator_size"],
                                 reply_markup=files_markup)
        bot.register_next_step_handler(reply, check_size, format, message)

    else:
        files_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        files_markup.add('B', 'KB', 'MB', 'Back to start')

        reply = bot.send_message(message.chat.id,
                                 messages["files_generator_unit_error"],
                                 reply_markup=files_markup)
        bot.register_next_step_handler(reply, check_unit, format)


# Checking the entered size
def check_size(message, format, unit):
    if (message.text == 'Back'):
        check_format(format)
    elif (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
    elif (isinstance(message.text, type(None)) or not message.text.isdigit()):
        files_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        files_markup.add('Back', 'Back to start')

        reply = bot.send_message(message.chat.id,
                                 messages["files_generator_size_error"],
                                 reply_markup=files_markup)
        bot.register_next_step_handler(reply, check_size, format, unit)

    else:
        size = int(message.text)

        if unit.text == 'MB':
            size_bytes = size * 1024 * 1024
        elif unit.text == 'KB':
            size_bytes = size * 1024
        else:
            size_bytes = size

        # File size check
        if (size_bytes < 1 or size_bytes > 47185920):
            reply = bot.send_message(message.chat.id,
                                     messages["files_generator_big_file"])
            bot.register_next_step_handler(reply, check_size, format, unit)
        else:
            timestamp = int(time.time())
            filename = f'{timestamp}-{size_bytes}-bytes{format.text}'

            # Generate a file with a given name and random bytes
            f = open(filename, "wb")
            random_bytes = os.urandom(size_bytes)
            f.write(random_bytes)
            f.close()

            # Smart output of the final message
            if (unit.text == 'MB' or unit.text == 'KB'):
                size_format = '{0:,}'.format(size).replace(',', ' ')
                bytes_format = '{0:,}'.format(size_bytes).replace(',', ' ')

                caption = f"Yay, your test <b>{format.text}</b> file"
                f"(<b>{size_format} {unit.text}</b> — {bytes_format} B)"
                "has been successfully generated!"
            else:
                bytes_format = '{0:,}'.format(size_bytes).replace(',', ' ')

                caption = f"Yay, your test <b>{format.text}</b> file"
                f"(<b>{bytes_format} {unit.text}</b>)"
                "has been successfully generated!"

            f = open(filename, "rb")
            files_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            files_markup.add('Back to start')
            reply = bot.send_document(message.chat.id, f,
                                      caption=caption,
                                      reply_markup=files_markup)

            f.close()
            os.unlink(filename)
            bot.register_next_step_handler(reply, welcome)
