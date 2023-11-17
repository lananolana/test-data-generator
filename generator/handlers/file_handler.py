import os
import time
from utils.common_handlers import handlers
from config import bot, formats, units
from utils.constants import common, files


@bot.message_handler(commands=['file'])
def file_handler(message):
    files_markup = handlers.markup_setup(formats, 5)
    handlers.send_message(
        message, files.FILES_GENERATOR, files_markup, check_format)


def check_format(message):
    if message.text in formats:
        files_markup = handlers.markup_setup(units, 3)
        handlers.add_back_to_start_button(files_markup)
        handlers.send_message(
            message, files.FILES_EXT,
            f"<b>{message.text}</b>", files.FILES_GENERATOR_UNIT,
            markup=files_markup, next_handler=check_unit, trans_data=message
        )
    else:
        handlers.are_back_buttons(
            message, handlers.welcome(message),
            files.FILES_GENERATOR_EXT_ERROR,
            files_markup, check_format
        )


# Checking the selected unit of measurement
def check_unit(message, format):
    if message.text in units:
        files_markup = handlers.markup_setup(formats, 5)
        handlers.add_back_button(files_markup)
        handlers.add_back_to_start_button(files_markup)
        handlers.send_message(
            message, files.FILES_EXT, f"<b>{format.text}</b>",
            files.FILES_UNIT, f"<b>{message.text}</b>",
            files.FILES_GENERATOR_SIZE, markup=files_markup,
            next_handler=check_size, trans_data=(format, message)
        )
    else:
        handlers.are_back_buttons(
            message, check_format, files.FILES_GENERATOR_UNIT_ERROR,
            files_markup, check_unit, format
        )


# Checking the entered size
def check_size(message, format, unit):
    size = int(message.text)
    size_bytes = handlers.convert_to_bytes(unit.text, size)

    files_markup = handlers.markup_setup(formats, 5)
    handlers.add_back_button(files_markup)
    handlers.add_back_to_start_button(files_markup)

    if 0 < size_bytes < 47185921:
        timestamp = int(time.time())
        filename = f'{timestamp}-{size_bytes}-bytes{format.text}'
        generate_file(message, filename, size_bytes, unit, size)
    elif size_bytes < 1 or size_bytes > 47185920:
        handlers.error(
            message, files.FILES_GENERATOR_BIG_FILE,
            files_markup, check_size, (format, unit)
        )
    else:
        handlers.are_back_buttons(
            message, check_format, files.FILES_GENERATOR_SIZE_ERROR,
            files_markup, check_size, (format, unit)
        )


def generate_file(message, filename, size_bytes, unit, size):
    # Generate a file with a given name and random bytes
    f = open(filename, "wb")
    random_bytes = os.urandom(size_bytes)
    f.write(random_bytes)
    f.close()

    # Smart output of the final message
    if (unit.text == 'MB' or unit.text == 'KB'):
        size_format = '{0:,}'.format(size).replace(',', ' ')
        bytes_format = '{0:,}'.format(size_bytes).replace(',', ' ')

        caption = f"{files.TEST_FILE} <b>{format.text}</b>(<b>{size_format}"
        f"{unit.text}</b> — {bytes_format} B) {files.SUCCESSFULLY_GENERATED}"
    else:
        bytes_format = '{0:,}'.format(size_bytes).replace(',', ' ')

        caption = f"{files.TEST_FILE} <b>{format.text}</b>"
        f"(<b>{bytes_format} {unit.text}</b>) {files.SUCCESSFULLY_GENERATED}"

    send_file(message, filename, caption)


def send_file(message, filename, caption):
    files_markup = handlers.markup_setup(formats, 5)
    handlers.add_back_to_start_button(files_markup)

    f = open(filename, "rb")
    handlers.send_document(message, f, caption, files_markup)
    f.close()
    os.unlink(filename)

    handlers.send_message(
        message, common.GENERATOR_AGAIN, next_handler=file_handler
    )
