# Set up libraries
# pip install pyTelegramBotAPI
# pip install Faker

import os
import time
import telebot
import json
import random
import string

from telebot import TeleBot, types
from faker import Faker
from secrets import token_urlsafe

# TODO: Paste Telegram token here
token = 'TOKEN'
bot = TeleBot(token, parse_mode = 'html')
faker = Faker()

# Main keyboard objects
requests = ['Users', 'File', 'Credit card', 'Text', '💬 Share feedback']
users = ['1️⃣', '3️⃣', '5️⃣', '🔟']
cards = ['MasterCard', 'VISA', 'AmEx', 'Maestro', 'Discover', 'JCB']
formats = ['.jpg', '.png', '.svg', '.gif', '.ico', '.mp4', '.avi', '.webm', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.pdf', '.css', '.html', '.js', '.json', '.zip', '.rar']

# Custom command /start
bot.set_my_commands([types.BotCommand('/start', 'Restart')])

# Start command handler
@bot.message_handler(commands = ['start'])
def welcome(message):
    # Getting the Telegram username
    username = message.from_user.first_name

    # Main keyboard object
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.add(*requests, row_width = 2)

    # Sending reply for start command handler with keyboard object
    reply = bot.send_message(message.chat.id, f"Hey, <b>{username}</b>! I'm a bot for generating test users, files, credit cards and texts. Always ready to save your testing time.\n\nChoose exactly what you need to generate 👇", reply_markup = markup)
    
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
        reply = bot.send_message(message.chat.id, f"Sorry, I don't understand your query, try again.")
        bot.register_next_step_handler(reply, check_request)

def users_handler(message):
    users_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    users_markup.add(*users, row_width = 2)
    users_markup.add('Back to start')

    reply = bot.send_message(message.chat.id, f"Got it, let's generate test users. Choose how many users you want 👇", reply_markup = users_markup)
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
    else:
        bot.send_message(message.chat.id, f"Sorry, I don't understand your query, try again.")
        bot.register_next_step_handler(reply, users_number)
        
    # Generate test data for the selected number of users using the simple_profile method
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'{faker.msisdn()[4:]}'

        # Use the secrets library to generate a password
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)
        
    # Serialise the data into a string
    payload_str = json.dumps(
        obj = total_payload,
        indent = 2,
        sort_keys = True,
        ensure_ascii = False,
        default = str)

    # Sending the result
    if payload_len != 0:
      bot.send_message(message.chat.id, f"Data of {payload_len} test users:\n\n<code>"\
                    f"{payload_str}</code>")
      reply = bot.send_message(message.chat.id, f"If you need more data, select again 👇")
      bot.register_next_step_handler(reply, users_number)

def files_handler(message):
    files_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    files_markup.add(*formats, row_width = 5)
    files_markup.add('Back to start')

    reply = bot.send_message(message.chat.id, f"Got it. I can generate files of various extensions from 1 byte up to 45 megabytes. Choose the extension you need 👇", reply_markup = files_markup)
    bot.register_next_step_handler(reply, check_format)

    # Checking the selected extension
def check_format(message):
    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
    elif (message.text in formats):
        files_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        files_markup.add("B", "KB", "MB", "Back to start")
            
        # Selecting the unit of measurement
        reply = bot.send_message(message.chat.id, f"The selected extension is <b>{message.text}</b>\n\nNow choose a unit of measure.\n\n<b>A little size guide:</b>\n\n1 kilobyte = 1,024 bytes\n1 megabyte = 1,024 kilobytes = 1,048,576 bytes", reply_markup = files_markup)
        bot.register_next_step_handler(reply, check_unit, message)
        
    else:
        files_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        files_markup.add(*formats, row_width = 5)
        files_markup.add("Back to start")

        reply = bot.send_message(message.chat.id, f"You may have chosen the wrong file extension, please choose one from the menu below 👇", reply_markup = files_markup)
        bot.register_next_step_handler(reply, check_format)
    
# Checking the selected unit of measurement
def check_unit(message, format):
    if (message.text == 'Back'):
        check_format(format)
        
    elif (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
        
    elif (message.text in ['B', 'KB', 'MB']):
        files_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        files_markup.add('Back', 'Back to start')

        reply = bot.send_message(message.chat.id, f"The selected extension is <b>{format.text}</b>\nUnit of measurement is <b>{message.text}</b>\n\nLast step left! Write the size of the file. I only accept integers, no spaces or other characters.\n\n⛔️Size limits:\n\n<b>Minimum</b> — 1 byte\n<b>Maximum</b> — 45 MB (that's 46,080 KB or 47,185,920 bytes)", reply_markup = files_markup)
        bot.register_next_step_handler(reply, check_size, format, message)
        
    else:
        files_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        files_markup.add('B', 'KB', 'MB', 'Back to start')

        reply = bot.send_message(message.chat.id, f"You may have selected the wrong unit of measurement, please choose one from the menu below 👇", reply_markup = files_markup)
        bot.register_next_step_handler(reply, check_unit, format)
	
# Checking the entered size
def check_size(message, format, unit):
    if (message.text == 'Back'):
        check_format(format)
    elif (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
    elif (isinstance(message.text, type(None)) or not message.text.isdigit()):
        files_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        files_markup.add('Back', 'Back to start')

        reply = bot.send_message(message.chat.id, f"Incorrect file size. Please enter the correct one, I only accept positive integers, no spaces or other characters 🙂", reply_markup = files_markup)
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
            reply = bot.send_message(message.chat.id, f"The file size is beyond my capacity.\n\n⛔️ Size limits:\n\n<b>Minimum</b> — 1 byte\n<b>Maximum</b> — 45 MB (that's 46,080 KB or 47,185,920 bytes)\n\nPlease enter the appropriate size 🙂")
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
                caption = f'Yay, your test <b>{format.text}</b> file (<b>{size_format} {unit.text}</b> — {size_bytes_format} B) has been successfully generated!'
            else:
                size_bytes_format = '{0:,}'.format(size_bytes).replace(',', ' ')
                caption = f'Yay, your test <b>{format.text}</b> file (<b>{size_bytes_format} {unit.text}</b>) has been successfully generated!'
                
            f = open(filename,"rb")
            files_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            files_markup.add('Back to start')
            reply = bot.send_document(message.chat.id, f, caption=caption, reply_markup = files_markup)

            f.close()
            os.unlink(filename)
            bot.register_next_step_handler(reply, welcome)

def card_handler(message):
    card_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    card_markup.add(*cards, row_width = 3)
    card_markup.add('Back to start')

    reply = bot.send_message(message.chat.id, f"Got it, let's generate the test bank card details. Select the payment system you need 👇", reply_markup = card_markup)
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
        bot.send_message(message.chat.id, f"Sorry, I don't understand your query, try again.")
        bot.register_next_step_handler(reply, payment_system)
        
    card_data = faker.credit_card_full(card_type)

    bot.send_message(message.chat.id, f'{message.text} card details:\n\n<code>{card_data}</code>')
    reply = bot.send_message(message.chat.id, f"If you need one more, select again 👇")
    bot.register_next_step_handler(reply, payment_system)

def text_handler(message):
    text_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    text_markup.add('Back to start')
    reply = bot.send_message(message.chat.id, f"Got it! I can generate text from 1 up to 4000 characters.\n\nPlease enter an integer without spaces or other characters 👇", reply_markup = text_markup)

    bot.register_next_step_handler(reply, text_generator)

def text_generator(message: types.Message):
    text_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    text_markup.add('Back to start')
    
    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)

    elif (isinstance(message.text, type(None)) or not message.text.isdigit()):
        reply = bot.send_message(message.chat.id, f"Wrong number of characters. Please enter the correct one, I only accept positive integers from 1 to 4000, no spaces or other characters 🙂", reply_markup = text_markup)
        bot.register_next_step_handler(message, text_generator)

    elif (int(message.text) < 1 or int(message.text) > 4000):
        reply = bot.send_message(message.chat.id, f"The number of characters is beyond my capacity. Please enter the correct one, I only accept positive integers from 1 to 4000, no spaces or other characters 🙂", reply_markup = text_markup)
        bot.register_next_step_handler(message, text_generator)

    else:
        symbols = int(message.text)
        characters = string.ascii_letters + string.digits
        final_reply = ''.join(random.choice(characters) for _ in range(symbols))

        bot.send_message(message.chat.id, f"This is your generated text with {symbols} characters.\n\n<code>{final_reply}</code>")
        bot.send_message(message.chat.id, f"If you need more data, enter an integer from 1 up to 4000 again 👇", reply_markup = text_markup)

        bot.register_next_step_handler(message, text_generator)

def feedback_handler(message: types.Message):
    feedback_button = types.InlineKeyboardMarkup()
    coffee = types.InlineKeyboardButton(text = 'Buy creator a coffee ☕️', url = 'https://www.buymeacoffee.com/lananolana')
    feedback_button.add(coffee)
    
    bot.send_message(message.chat.id, f"💡 Do you have any ideas on how to improve this simple bot for testing needs? Text to the creator @schoegar")
    reply = bot.send_message(message.chat.id, f"To support the Test Data Generator project and say thank you, click the button below.", reply_markup = feedback_button)
    bot.register_next_step_handler(reply, check_request)

# Main function, launching the polling bot
def main():
    bot.infinity_polling()

# The special construct for the program entry point (main function)
if __name__ == '__main__':
    main()
