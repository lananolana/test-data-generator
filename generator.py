import os
import time
import json
import random
import string

from config import faker, bot, messages, requests, users, cards, formats
from telebot import types
from secrets import token_urlsafe

# Custom command /start
bot.set_my_commands([types.BotCommand('/start', 'Restart')])


def load_messages():
    with open("messages.json", "r", encoding="utf-8") as file:
        messages = json.load(file)
    return messages


def initialize_messages():
    global messages
    messages = load_messages()


# Start command handler
@bot.message_handler(commands=['start'])
def welcome(message):
    # Getting the Telegram username
    username = message.from_user.first_name

    # Main keyboard object
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*requests, row_width=2)

    # Sending reply for start command handler with keyboard object
    reply = f"Hey, <b>{username}</b>!" + messages["hello_message"]
    bot.send_message(message.chat.id, reply, reply_markup=markup)

    # Register the transition to the next step
    bot.register_next_step_handler(reply, check_request)


def check_request(message):
    if message.text == '/start':
        welcome(message)
    elif message.text == 'Users':
        users_handler(message)
    elif message.text == 'File':
        files_handler(message)
    elif message.text == 'Credit card':
        card_handler(message)
    elif message.text == 'Text':
        text_handler(message)
    elif message.text == '💬 Share feedback':
        feedback_handler(message)
    else:
        reply = bot.send_message(message.chat.id, messages["query_error"])
        bot.register_next_step_handler(reply, check_request)


def users_handler(message):
    users_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    users_markup.add(*users, row_width=2)
    users_markup.add('Back to start')

    reply = bot.send_message(message.chat.id,
                             messages["users_generator"],
                             reply_markup=users_markup)
    bot.register_next_step_handler(reply, users_number)


def users_number(message: types.Message):
    payload_len = 0
    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
    elif message.text == '1️⃣':
        payload_len = 1
    elif message.text == "3️⃣":
        payload_len = 3
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    elif (message.text.isdigit() and 0 < int(message.text) <= 15):
        payload_len = int(message.text)
    elif message.text.isdigit():
        bot.send_message(message.chat.id, messages["users_generator_error"])
        bot.register_next_step_handler(message, users_number)
    else:
        bot.send_message(message.chat.id, messages["query_error"])
        bot.register_next_step_handler(message, users_number)

    # Generate test data for the selected number of users
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'{faker.msisdn()[4:]}'

        # Use the secrets library to generate a password
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    # Serialise the data into a string
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str)

    # Sending the result
    if payload_len != 0:
        bot.send_message(message.chat.id, f"Data of {payload_len} test users:"
                         f"\n\n<code>{payload_str}</code>")
        reply = bot.send_message(message.chat.id,
                                 messages["generator_again"])
        bot.register_next_step_handler(reply, users_number)


def files_handler(message):
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


def card_handler(message):
    card_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    card_markup.add(*cards, row_width=3)
    card_markup.add('Back to start')

    reply = bot.send_message(message.chat.id,
                             messages["cards_generator"],
                             reply_markup=card_markup)
    bot.register_next_step_handler(reply, payment_system)


def payment_system(message: types.Message):
    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
    elif message.text == 'VISA':
        card_type = 'visa'
    elif message.text == 'MasterCard':
        card_type = 'mastercard'
    elif message.text == 'Maestro':
        card_type = 'maestro'
    elif message.text == 'JCB':
        card_type = 'jcb'
    elif message.text == 'AmEx':
        card_type = 'amex'
    elif message.text == 'Discover':
        card_type = 'discover'
    else:
        reply = bot.send_message(message.chat.id, messages["query_error"])
        bot.register_next_step_handler(reply, payment_system)

    card_data = faker.credit_card_full(card_type)

    bot.send_message(message.chat.id,
                     f"{message.text} card details:"
                     f"\n\n<code>{card_data}</code>")
    reply = bot.send_message(message.chat.id, messages["generator_again"])
    bot.register_next_step_handler(reply, payment_system)


def text_handler(message):
    text_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text_markup.add('Back to start')
    reply = bot.send_message(message.chat.id,
                             messages["text_generator"],
                             reply_markup=text_markup)

    bot.register_next_step_handler(reply, text_generator)


def text_generator(message: types.Message):
    text_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text_markup.add('Back to start')

    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)

    elif (isinstance(message.text, type(None)) or not message.text.isdigit()):
        bot.send_message(message.chat.id,
                         messages["text_generator_int_error"],
                         reply_markup=text_markup)
        bot.register_next_step_handler(message, text_generator)

    elif (int(message.text) < 1 or int(message.text) > 4000):
        bot.send_message(message.chat.id,
                         messages["text_generator_size_error"],
                         reply_markup=text_markup)
        bot.register_next_step_handler(message, text_generator)

    else:
        symbols = int(message.text)
        chars = string.ascii_letters + string.digits
        final_reply = ''.join(random.choice(chars) for _ in range(symbols))

        bot.send_message(message.chat.id,
                         f"This is generated text with {symbols} characters."
                         f"\n\n<code>{final_reply}</code>")
        bot.send_message(message.chat.id,
                         messages["text_generator_again"],
                         reply_markup=text_markup)

        bot.register_next_step_handler(message, text_generator)


def feedback_handler(message: types.Message):
    feedback_button = types.InlineKeyboardMarkup()
    url = 'https://www.buymeacoffee.com/lananolana'
    coffee = types.InlineKeyboardButton(text='Buy creator a coffee ☕️',
                                        url=url)
    feedback_button.add(coffee)

    bot.send_message(message.chat.id, messages["idea_message"])
    reply = bot.send_message(message.chat.id,
                             messages["support_message"],
                             reply_markup=feedback_button)
    bot.register_next_step_handler(reply, check_request)


# Main function, launching the polling bot
def main():
    bot.infinity_polling()


# The special construct for the program entry point (main function)
if __name__ == '__main__':
    main()
