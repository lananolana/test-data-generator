# Set up libraries
import os
import time
import telebot
import json

from telebot import TeleBot, types
from faker import Faker
from secrets import token_urlsafe
from lorem_text import lorem

# TODO: Paste Telegram token here
token = 'YOUR_TOKEN'
bot = telebot.TeleBot(token, parse_mode = 'html')
faker = Faker()

# Main keyboard objects
requests = ['Users', 'File', 'Credit card', 'Text']

# Custom command /start
bot.set_my_commands([types.BotCommand('/start', 'Bot restart')])

# Start command handler
@bot.message_handler(commands = ['start'])
def welcome(message):
    # Getting the Telegram username
    username = message.from_user.first_name

    # Main keyboard object
    markup = types.ReplyKeaboardMarkup(resize_keyboard = True)
    markup.add(*requests, row_width = 2)

    # Sending reply for start command handler with keaboard object
    reply = bot.send_message(message.chat.id, f"Hey, <b>{username}</b>! I'm a bot for generating test users, files, credit cards ans texts. Always ready to save your testing time."\
                             "Choose exactly what you need to generate 👇", reply_markup = markup)
    
    # Register the transition to the next step
    bot.register_next_step_handler(reply, check_request)

def check_request(message):
    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
    elif message.text == 'Users':
        users_handler(message)
    elif message.text == 'File':
        files_handler(message)
    elif message.text == 'Credit card':
        card_handler(message)
    elif message.text == 'Text':
        text_handler(message)
    else:
        bot.send_message(message.chat.id, f"Sorry, I don't understand your query, try again.", reply_markup = welcome.markup)

def users_handler(message):
    users = ['1️⃣', '2️⃣', '5️⃣', '🔟']
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.add(*users, row_width = 2)
    markup.add('Back to start')

    bot.send_message(message.chat.id, f"Got it, let's generate test users. Choose how many users you want 👇")
    reply_markup = markup

    payload_len = 0
    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
    elif message.text == '1️⃣':
        payload_len = 1
    elif message.text == "2️⃣":
        payload_len = 2
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    else:
        bot.send_message(message.chat.id, f"Sorry, I don't understand your query, try again.", reply_markup = markup)
    
    # Generate test data for the selected number of users using the simple_profile method
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+XXX {faker.msisdn()[4:]}'

        # Use the secrets library to generate a password
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)
    
    # Serialise the data into a string
    payload_str = json.dumps(
        obj = total_payload,
        indent = 2,
        sort_keys = True,
        ensure_ascii = False,
        default = str
    )

    # Sending the result
    bot.send_message(message.chat.id, f"Data of {payload_len} test users:\n<code>"\
                     f"{payload_str}</code>")
    bot.send_message(message.chat.id, f"If you need more data, select again 👇",
                     reply_markup = markup)

def files_handler(message):
    formats = ['.jpg', '.png', '.svg', '.gif', '.ico', '.mp4', '.avi', '.webm', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.pdf', '.css', '.html', '.js', '.json', '.zip', '.rar']
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.add(*formats, row_width = 5)

    reply = bot.send_message(message.chat.id, f"Got it. I can generate files of various extensions from 1 byte up to 45 megabytes. Choose the extension you need 👇", reply_markup = markup)
    bot.register_next_step_handler(reply, check_format)

    # Checking the selected extension
    def check_format(message):
        if (message.text == 'Back to start' or message.text == '/start'):
            welcome(message)
        elif (message.text in formats):
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup.add("B", "KB", "MB", "Back to start")
            
            # Selecting the unit of measurement
            reply = bot.send_message(message.chat.id, f"The selected extension is <b>{message.text}</b>\n\nNow choose a unit of measure.\n<u>A little size guide:</u>\n1 kilobyte = 1,024 bytes\n1 megabyte = 1,024 kilobytes = 1,048,576 bytes", reply_markup = markup)
            bot.register_next_step_handler(reply, check_unit, message)
        
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup.add(*formats, row_width = 5)
            markup.add("Back to start")

            reply = bot.send_message(message.chat.id, f"You may have chosen the wrong file extension, please choose one from the menu below 👇", reply_markup=markup)
            bot.register_next_step_handler(reply, check_format)
    
    # Checking the selected unit of measurement
    def check_unit(message, format):
        if (message.text == 'Back'):
            check_format(format)
        
        elif (message.text == 'Back to start' or message.text == '/start'):
            welcome(message)
        
        elif (message.text in ['B', 'KB', 'MB']):
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup.add('Back', 'Back to start')

            reply = bot.send_message(message.chat.id, f"The selected extension is <b>{format.text}</b>\nUnit of measurement is <b>{message.text}</b>\n\nLast step left! Write the size of the file. I only accept integers, no spaces or other characters.\n⛔️ <u>Size limits:</u>\n<b>Minimum</b> — 1 byte\n<b>Maximum</b> — 45 MB (that's 46,080 KB or 47,185,920 bytes)", reply_markup = markup)
            bot.register_next_step_handler(reply, check_size, format, message)
        
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup.add('B', 'KB', 'MB', 'Back to start')

            reply = bot.send_message(message.chat.id, f"You may have selected the wrong unit of measurement, please choose one from the menu below 👇", reply_markup = markup)
            bot.register_next_step_handler(reply, check_unit, format)
	
    # Checking the entered size
    def check_size(message, format, unit):
        if (message.text == 'Back'):
            check_format(format)
        elif (message.text == 'Back to start' or message.text == '/start'):
            welcome(message)
        elif (isinstance(message.text, type(None)) or not message.text.isdigit()):
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup.add('Back', 'Back to start')

            reply = bot.send_message(message.chat.id, f"Incorrect file size. Please enter the correct one, I only accept positive integers, no spaces or other characters 🙂", reply_markup = markup)
            bot.register_next_step_handler(reply, check_size, format, unit)
        
        else:
            size = int(message.text)

            if (unit.text == 'MB'):
                size_bytes = size * 1024 * 1024
            elif (unit.text == 'KB'):
                size_bytes = size * 1024
            else:
                size_bytes = size
            
        # File size check
        if (size_bytes < 1 or size_bytes > 47185920):
            reply = bot.send_message(message.chat.id, f"The file size is beyond my capacity.\n<u>⛔️ <u>Size limits:</u>\n<b>Minimum</b> — 1 byte\n<b>Maximum</b> — 45 MB (that's 46,080 KB or 47,185,920 bytes)\n\nPlease enter the appropriate size 🙂")
            bot.register_next_step_handler(reply, check_size, format, unit)
        else:
            timestamp = int(time.time())
            filename = f'{timestamp}-{size_bytes}-bytes{format.text}'

            # Generate a file with a given name and random bytes
            f = open(filename,"wb")
            random_bytes = os.urandom(size_bytes)
            f.write(random_bytes)
            f.close()

            # Smart output of the final message, depending on the selected units of measurement
            if (unit.text == 'MB' or unit.text == 'KB'):
                 size_format = '{0:,}'.format(size).replace(',', ' ')
                 size_bytes_format = '{0:,}'.format(size_bytes).replace(',', ' ')
                 caption = f'Yay, your test file with the extension of <b>{format.text}</b> has been successfully generated!\n\nIts size is <b>{size_format} {unit.text}</b>\nIn bytes — <b>{size_bytes_format} B</b>'
            else:
                 size_bytes_format = '{0:,}'.format(size_bytes).replace(',', ' ')
                 caption = f'Yay, your test file with the extension of <b>{format.text}</b> has been successfully generated!\n\nIts size is <b>{size_bytes_format} {unit.text}</b>'
            
            f = open(filename,"rb")
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup.add('Back to start')
            reply = bot.send_document(message.chat.id, f, caption=caption, reply_markup=markup)

            f.close()
            os.unlink(filename)
            bot.register_next_step_handler(reply, files_handler)

def card_handler(message):
    cards = ['MasterCard', 'VISA', 'AmEx', 'Maestro', 'Discover', 'JCB']
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.add(*cards, row_width = 3)
    markup.add('Back to start')

    bot.send_message(message.chat.id, f"Got it, let's generate the test bank card details. Select the payment system you need 👇")
    reply_markup = markup

    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)        
    elif message.text == 'VISA':
        card_type = 'visa'
    elif message.text == 'MasterСard':
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
        bot.send_message(message.chat.id, f"Sorry, I don't understand your query, try again.", reply_markup = markup)
    
    card_data = faker.credit_card_full(card_type)

    bot.send_message(message.chat.id, f'Test bank card {card_type}:\n<code>{card_data}</code>')
    bot.send_message(message.chat.id, f"If you need one more, select again 👇",
                     reply_markup = markup)

def text_handler(message):
    bot.send_message(message.chat.id, f"Got it! I can generate text from 1 up to 4000 characters.\n\nPlease enter an integer without spaces or other characters 👇")
    bot.register_next_step_handler(check_size)

    def check_size(message):
        if (message.text == 'Back to start' or message.text == '/start'):
            welcome(message)

        elif (isinstance(message.text, type(None)) or not message.text.isdigit()):
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup.add('Back to start')

            reply = bot.send_message(message.chat.id, f"Wrong number of characters. Please enter the correct one, I only accept positive integers from 1 to 4000, no spaces or other characters 🙂", reply_markup = markup)
            bot.register_next_step_handler(check_size)

        elif (message.text < 1 or message.text > 4000):
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup.add('Back to start')

            reply = bot.send_message(message.chat.id, f"The number of characters is beyond my capacity. Please enter the correct one, I only accept positive integers from 1 to 4000, no spaces or other characters 🙂", reply_markup = markup)
            bot.register_next_step_handler(check_size)

        else:
            symbols = int(message.text)
            reply = lorem.words(symbols)
            bot.send_message(message.chat.id, f"This is your generated text with {symbols} characters.\n\n{reply}")
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup.add('Back to start')
            bot.register_next_step_handler(check_size)

# Main function, launching the polling bot
def main():
    bot.infinity_polling()

# The special construct for the program entry point (main function)
if __name__ == '__main__':
    main()