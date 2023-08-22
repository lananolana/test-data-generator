# Set up libraries
import json
from secrets import token_urlsafe

from faker import Faker
from telebot import TeleBot, types

# TODO: Paste Telegram token here
TOKEN = 'PASTE_TOKEN_HERE'
bot = TeleBot(TOKEN, parse_mode='html')

# Library for generation testing full names in English and Russian
faker = Faker('en_EN')

# Main keyboard objects
requests = ['Users', 'File', 'Credit card', 'Text']

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

def users_handler(message):
    users = ['1️⃣', '2️⃣', '5️⃣', '🔟']
    users_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    users_reply_markup.add(*users, row_width = 2)

    bot.send_message(message.chat.id, f"Got it, let's generate test users. Choose how many users you want 👇")
    reply_markup = users_reply_markup

    payload_len = 0
    if message.text == '1️⃣':
        payload_len = 1
    elif message.text == "2️⃣":
        payload_len = 2
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    else:
        bot.send_message(message.chat.id, f"Sorry, I don't understand your query, try again.", reply_markup = users_reply_markup)
        return
    
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
                     reply_markup = users_reply_markup)

# def file_handler(message):

# def card_handler(message):

# def text_handler(message):

def check_request(message):
    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
    elif message.text == 'Users':
        users_handler(message)
    elif message.text == 'File':
        file_handler(message)
    elif message.text == 'Credit card':
        card_handler(message)
    elif message.text == 'Text':
        text_handler(message)
    else:
        bot.send_message(message.chat.id, f"Sorry, I don't understand your query, try again.", reply_markup = welcome.markup)

def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()